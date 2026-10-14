"""(Integrado na Parte 82, do pacote SYNTHAI_consolidado.py recebido do usuário; caminhos ajustados para synthai.revisado.)"""
"""Regressões para a validade das comparações usadas na avaliação."""
import math
import unittest
from .metacognicao import comparacao_pareada

class ComparacaoPareadaTestes(unittest.TestCase):
    def test_diferencas_constantes_nao_autorizam_teste_t(self):
        for delta in (-1, 0, 1):
            with self.subTest(delta=delta):
                m, dp, t = comparacao_pareada([1, 2, 3], [1+delta, 2+delta, 3+delta])
                self.assertEqual(m, delta)
                self.assertEqual(dp, 0)
                self.assertTrue(math.isnan(t))
                self.assertFalse(t > 3)

    def test_resultado_conhecido_e_inversao_do_sinal(self):
        # Diferenças 1, 2, 3: média 2, desvio amostral 1.
        a, b = [0, 0, 0], [1, 2, 3]
        self.assertEqual(comparacao_pareada(a, b)[:2], (2, 1))
        self.assertAlmostEqual(comparacao_pareada(a, b)[2], 2*math.sqrt(3))
        self.assertAlmostEqual(comparacao_pareada(b, a)[2], -2*math.sqrt(3))

    def test_amostras_invalidas_sao_recusadas(self):
        casos = [([], []), ([1], [2]), ([1, 2], [3]),
                 ([1, math.nan], [1, 2]), ([1, 2], [1, math.inf]),
                 ([-1e308, 0], [1e308, 0])]
        for a, b in casos:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                comparacao_pareada(a, b)

    def test_aceita_iteradores(self):
        self.assertEqual(comparacao_pareada(iter([0,0,0]), iter([1,2,3]))[:2], (2,1))
