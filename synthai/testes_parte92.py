"""Testes de unidade da Parte 92 (o Adam e a fronteira do pow): `python3 -m unittest synthai.testes_parte92`."""

import unittest

import calculos


class TesteParte92(unittest.TestCase):
    def test_p2201_fronteira_pow(self):
        self.assertEqual(calculos.p2201_fronteira_pow(), 418)
        self.assertGreater(calculos.p2201_fronteira_pow(), 0)   # a fronteira do pow e real

    def test_p2202_produto_portavel(self):
        prod = calculos.p2202_produto_portavel(ate=5)
        # multiplicacao repetida: 0.9, 0.81, ... exata na sequencia de produtos
        self.assertEqual(len(prod), 5)
        self.assertEqual(prod[0], 0.9)
        self.assertEqual(prod[1], 0.9 * 0.9)

    def test_p2203_rodada59(self):
        perdas = calculos.p2203_rodada59()
        self.assertEqual(len(perdas), 5)
        self.assertTrue(all(p > 0 for p in perdas))

    def test_p2204_adam_reduz(self):
        self.assertEqual(calculos.p2204_adam_reduz_perda(), [True] * 5)

    def test_p1961_com_parte_92(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[92], (4, 4))
        self.assertEqual((ok, tot), (53, 65))


if __name__ == "__main__":
    unittest.main()
