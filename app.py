"""Servidor web local para a calculadora, sem dependências externas."""

import ast
import json
import operator
from decimal import Decimal, InvalidOperation, localcontext
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


HOST = "127.0.0.1"
PORT = 8000
INDEX_FILE = Path(__file__).with_name("index.html")

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _avaliar_no(no):
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
        if isinstance(no.value, bool):
            raise ValueError("Expressão inválida.")
        try:
            numero = Decimal(str(no.value))
        except InvalidOperation as erro:
            raise ValueError("Número inválido.") from erro
        if not numero.is_finite():
            raise ValueError("Número inválido.")
        return numero

    if isinstance(no, ast.UnaryOp) and type(no.op) in (ast.USub, ast.UAdd):
        return _OPERATORS[type(no.op)](_avaliar_no(no.operand))

    if isinstance(no, ast.BinOp) and type(no.op) in (
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
    ):
        esquerda = _avaliar_no(no.left)
        direita = _avaliar_no(no.right)
        if isinstance(no.op, (ast.Div, ast.Mod)) and direita == 0:
            raise ValueError("Não é possível dividir por zero.")
        if isinstance(no.op, ast.Pow) and (
            not direita == int(direita) or abs(direita) > 100
        ):
            raise ValueError("Expoente deve ser um inteiro entre -100 e 100.")
        try:
            resultado = _OPERATORS[type(no.op)](esquerda, direita)
        except (ArithmeticError, ValueError) as erro:
            raise ValueError("Não foi possível calcular a expressão.") from erro
        if not resultado.is_finite() or abs(resultado) > Decimal("1e100"):
            raise ValueError("Resultado fora do limite permitido.")
        return resultado

    raise ValueError("Expressão inválida.")


def calcular_expressao(expressao):
    """Avalia somente números e operadores matemáticos permitidos."""
    if not isinstance(expressao, str) or not expressao.strip():
        raise ValueError("Digite uma expressão.")
    if len(expressao) > 200:
        raise ValueError("A expressão é muito longa.")
    try:
        arvore = ast.parse(expressao, mode="eval")
    except SyntaxError as erro:
        raise ValueError("Expressão inválida.") from erro
    with localcontext() as contexto:
        contexto.prec = 28
        return _avaliar_no(arvore.body)


def _formatar_resultado(resultado):
    texto = format(resultado, "f")
    if "." in texto:
        texto = texto.rstrip("0").rstrip(".")
    return texto or "0"


class CalculadoraHandler(BaseHTTPRequestHandler):
    """Entrega a interface e processa cálculos JSON."""

    def _responder(self, status, corpo, content_type):
        dados = corpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        if self.path != "/":
            self._responder(HTTPStatus.NOT_FOUND, "Não encontrado.", "text/plain")
            return
        try:
            pagina = INDEX_FILE.read_text(encoding="utf-8")
        except OSError:
            self._responder(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Interface indisponível.",
                "text/plain",
            )
            return
        self._responder(HTTPStatus.OK, pagina, "text/html")

    def do_POST(self):
        if self.path != "/calculate":
            self._responder(HTTPStatus.NOT_FOUND, "Não encontrado.", "text/plain")
            return
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if tamanho > 10_000:
                raise ValueError("Requisição muito grande.")
            dados = json.loads(self.rfile.read(tamanho))
            resultado = calcular_expressao(dados.get("expression"))
            resposta = {"result": _formatar_resultado(resultado)}
            self._responder(HTTPStatus.OK, json.dumps(resposta), "application/json")
        except (ValueError, json.JSONDecodeError, TypeError) as erro:
            resposta = {"error": str(erro)}
            self._responder(
                HTTPStatus.BAD_REQUEST, json.dumps(resposta), "application/json"
            )

    def log_message(self, formato, *args):
        print(f"{self.address_string()} - {formato % args}")


def main():
    servidor = ThreadingHTTPServer((HOST, PORT), CalculadoraHandler)
    print(f"Calculadora disponível em http://{HOST}:{PORT}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
