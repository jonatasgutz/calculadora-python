"""Calculadora de terminal sem dependências externas."""

from decimal import Decimal, InvalidOperation, localcontext


def calcular(primeiro, segundo, operacao):
    """Calcula com até 28 algarismos significativos."""
    with localcontext() as contexto:
        contexto.prec = 28
        if operacao == '1':
            return primeiro + segundo
        if operacao == '2':
            return primeiro - segundo
        if operacao == '3':
            return primeiro * segundo
        if operacao == '4':
            if segundo == 0:
                raise ValueError('Não é possível dividir por zero.')
            return primeiro / segundo
        raise ValueError('Operação inválida.')


def ler_numero(mensagem):
    while True:
        entrada = input(mensagem).strip().replace(',', '.')
        try:
            numero = Decimal(entrada)
            if not numero.is_finite() or abs(numero) > Decimal('1e100'):
                raise ValueError
            return numero
        except (InvalidOperation, ValueError):
            print('Digite um número válido entre -1e100 e 1e100, como 12,5.')


def main():
    simbolos = {'1': '+', '2': '-', '3': '×', '4': '÷'}
    print('=== Calculadora Python ===')
    print('Use vírgula ou ponto para decimais, sem separador de milhares.')

    while True:
        print('\n1. Somar\n2. Subtrair\n3. Multiplicar\n4. Dividir\n0. Sair')
        opcao = input('Escolha uma operação: ').strip()
        if opcao == '0':
            print('Até a próxima!')
            return
        if opcao not in simbolos:
            print('Opção inválida. Escolha de 0 a 4.')
            continue

        primeiro = ler_numero('Primeiro número: ')
        segundo = ler_numero('Segundo número: ')
        try:
            resultado = calcular(primeiro, segundo, opcao)
            print(f'Resultado: {primeiro} {simbolos[opcao]} {segundo} = {resultado}')
        except ValueError as erro:
            print(erro)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nCalculadora encerrada.')
