import contextlib
from decimal import Decimal
import io
import unittest
from unittest.mock import patch

from calculadora import calcular, main


class TestCalculadora(unittest.TestCase):
    def test_operacoes(self):
        for opcao, esperado in [('1', '10'), ('2', '6'), ('3', '16'), ('4', '4')]:
            with self.subTest(opcao=opcao):
                self.assertEqual(calcular(Decimal('8'), Decimal('2'), opcao), Decimal(esperado))

    def test_decimais_e_negativos(self):
        self.assertEqual(calcular(Decimal('0.1'), Decimal('0.2'), '1'), Decimal('0.3'))
        self.assertEqual(calcular(Decimal('-3'), Decimal('2'), '3'), Decimal('-6'))

    def test_divisao_por_zero(self):
        with self.assertRaisesRegex(ValueError, 'zero'):
            calcular(Decimal('5'), Decimal('0'), '4')

    def test_menu_validacao_e_continuidade(self):
        entradas = ['9', '1', 'abc', 'NaN', 'Infinity', '0,1', '0,2', '4', '5', '0', '0']
        saida = io.StringIO()
        with patch('builtins.input', side_effect=entradas), contextlib.redirect_stdout(saida):
            main()
        texto = saida.getvalue()
        self.assertIn('Opção inválida', texto)
        self.assertIn('número válido', texto)
        self.assertIn('= 0.3', texto)
        self.assertIn('dividir por zero', texto)
        self.assertIn('Até a próxima!', texto)


if __name__ == '__main__':
    unittest.main()
