"""Testes de unidade da Parte 88 (a arquitetura autopoiética recebida): `python3 -m unittest synthai.testes_parte88`."""

import unittest

import calculos
from synthai.autopoiese import lfi1_negacao, lfi1_conjuncao, lfi1_disjuncao, lfi1_consistencia, nested_probability


class TesteParte88(unittest.TestCase):
    def test_p2081_nested_probability(self):
        self.assertEqual(calculos.p2081_probabilidade_aninhada(), (0.8333, 0.1667, 0.5))
        # P(P(X)) = (10X+1)/12: afim, ponto fixo 0.5
        self.assertAlmostEqual(nested_probability(0.5), 0.5)
        self.assertAlmostEqual(nested_probability(0.0), (10 * 0.001 + 1) / 12, places=6)  # clamp em 0,001

    def test_p2082_iterado(self):
        medido, conta = calculos.p2082_probabilidade_aninhada_iterada()
        self.assertAlmostEqual(medido, conta, places=9)
        self.assertTrue(0.55 < medido < 0.58)

    def test_p2083_lfi1_sem_explosao(self):
        self.assertEqual(calculos.p2083_lfi1_sem_explosao(), (0.5, 0.0, True))
        # controle: a logica classica nos extremos funciona normalmente
        self.assertEqual(lfi1_conjuncao(1.0, lfi1_negacao(1.0)), 0.0)  # A ^ ~A = F quando A consistente
        self.assertEqual(lfi1_consistencia(1.0), 1.0)
        self.assertEqual(lfi1_disjuncao(0.0, 1.0), 1.0)

    def test_p2084_descompasso(self):
        usa_entropia, usa_consistencia = calculos.p2084_descompasso_texto_codigo()
        self.assertTrue(usa_entropia)
        self.assertFalse(usa_consistencia)  # a promessa do texto nao esta no codigo
        # controle: um codigo que de fato checa consistencia e detectado
        com = "def f(self, a, b):\n    return check_consistency(a)\n"
        self.assertTrue(calculos.p2084_descompasso_texto_codigo(com)[1])

    def test_p1961_com_parte_88(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[88], (4, 4))
        self.assertEqual((ok, tot), (38, 50))

    def test_p2085_rodada55(self):
        s = calculos.p2085_rodada55()
        self.assertEqual(len(s), 8)
        self.assertEqual(s[1], 1.2)   # r=1.5, A=1: cortado em 1+eps=1.2


if __name__ == "__main__":
    unittest.main()
