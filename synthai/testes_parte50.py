"""Testes de unidade da Parte 50: `python3 -m unittest synthai.testes_parte50`."""

import unittest

import calculos


class GrafoFalso:
    @staticmethod
    def grafo_de_definicoes():
        return {"a": {"b", "c"}, "b": {"a"}, "c": {"d"}, "d": {"c"}}


class TesteParte50(unittest.TestCase):
    def test_periodo_hex_ate_20(self):
        # ord(2): 3:2, 5:4, 7:3, 11:10, 13:12, 17:8, 19:18; ord(16) = ord(2)/mdc(ord(2), 4): 1, 1, 3, 5, 3, 2, 9
        # ord(16)/(p-1): 1/2, 1/4, 3/6, 5/10, 3/12, 2/16, 9/18 -> soma 2,625 em 7 primos
        r16, r2, rg, k = calculos.p943_periodo_hex(20)
        self.assertEqual(k, 7)
        self.assertAlmostEqual(r16, 2.625 / 7, places=12)
        self.assertAlmostEqual(rg, (1 / 2 + 1 / 4 + 1 + 1 / 2 + 1 / 4 + 1 / 4 + 1 / 2) / 7, places=12)

    def test_definicoes_mutuas(self):
        n, m, pares, esperado, frac, ex = calculos.p942_definicoes_mutuas(GrafoFalso())
        # pares a-b e c-d; M = 5 arestas em N = 4: esperado 5·(5/16)/2 = 0,78125
        self.assertEqual((n, m, pares, ex), (4, 5, 2, [("a", "b"), ("c", "d")]))
        self.assertAlmostEqual(esperado, 0.78125, places=12)
        self.assertAlmostEqual(frac, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
