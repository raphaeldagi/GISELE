"""Testes de unidade da Parte 91 (o GPT que aprende igual): `python3 -m unittest synthai.testes_parte91`."""

import unittest

import calculos


class TesteParte91(unittest.TestCase):
    def test_p2171_rodada58(self):
        casos = calculos.p2171_rodada58()
        self.assertEqual(len(casos), 5)
        for antes, depois, arg in casos:
            self.assertLess(depois, antes)   # o passo reduz a perda

    def test_p2172_sgd_reduz(self):
        self.assertEqual(calculos.p2172_sgd_reduz_perda(), [True] * 5)

    def test_p2173_gradiente_identidade(self):
        self.assertLess(calculos.p2173_gradiente_p_menos_onehot(), 1e-6)   # p - onehot

    def test_p2174_memoriza(self):
        ini, fim = calculos.p2174_gpt_memoriza()
        self.assertGreater(ini, 0.5)
        self.assertLess(fim, 0.1)            # memoriza o padrao repetido

    def test_p1961_com_parte_91(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91))
        self.assertEqual(por[91], (4, 4))
        self.assertEqual((ok, tot), (49, 61))


if __name__ == "__main__":
    unittest.main()
