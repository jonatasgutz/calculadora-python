# Calculadora Python

Calculadora interativa no terminal, com mensagens em português.

Também inclui uma interface web responsiva servida por Python, sem dependências
externas. A API avalia expressões com `ast`, sem usar `eval`.

## Recursos

- Soma, subtração, multiplicação e divisão.
- Números negativos e decimais com vírgula ou ponto.
- Validação das entradas e proteção contra divisão por zero.
- Menu para realizar várias contas e opção para sair.

## Como executar

Instale Python 3, abra o terminal na pasta do projeto e execute:

```sh
python calculadora.py
```

Não é necessário instalar bibliotecas adicionais. Escolha uma operação de 1 a 4,
digite os dois números e veja o resultado. Digite 0 no menu para sair.
Você também pode encerrar com Ctrl+C.

## Interface web

Execute:

```sh
python app.py
```

Abra <http://127.0.0.1:8000> no navegador. Use os botões ou o teclado
(Enter calcula e Esc limpa). A API `POST /calculate` recebe
`{"expression":"2 + 3 * 4"}` e retorna `{"result":"14"}`.

Exemplo: escolha 1, digite `0,1` e `0,2`; o resultado será `0.3`.

Os cálculos usam `decimal` com 28 algarismos significativos. Resultados que
excedem essa precisão são arredondados. Não use separadores de milhares.

## Testes

```sh
python -m unittest -v
```
