"""Testes de unidade da Parte 61: `python3 -m unittest synthai.testes_parte61`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import math
import unittest

import calculos


class DicionarioFalso:
    # dois adjetivos negativos (um com prefixo), um positivo; o substantivo fica fora
    sinsets = [("a", ["nonliving"], [], "not endowed with life"), ("a", ["rare"], [], "not widely distributed"),
               ("a", ["happy"], [], "enjoying well-being"), ("n", ["x"], [], "not a thing")]

    @staticmethod
    def definicao(glosa):
        return glosa


class TesteParte61(unittest.TestCase):
    def test_p1271_rodadas_verificadas(self):
        n, nums = calculos.p1271_rodadas_verificadas()
        self.assertEqual(nums, list(range(1, n + 1)))
        self.assertEqual(nums[:35], list(range(1, 36)))

    def test_p1272_adjetivos_negativos(self):
        neg, n, pre, ex = calculos.p1272_adjetivos_negativos(DicionarioFalso())
        self.assertEqual(n, 3)
        self.assertAlmostEqual(neg, 2 / 3, places=12)
        self.assertAlmostEqual(pre, 0.5, places=12)
        self.assertEqual(ex[0][0], "nonliving")

    def test_p1273_niven(self):
        # base 10 até 20: 1..10, 12, 18, 20 (conferido por código); eta_10 = 2 ln 10 · 21 / 81
        k, conta = calculos.p1273_niven(20, 10)
        self.assertEqual(k, 13)
        self.assertAlmostEqual(conta, 2 * math.log(10) * 21 / 81 * 20 / math.log(20), places=12)

    def test_p1274_narcisistas_14_bases(self):
        celulas, grupos = calculos.p1274_narcisistas_14_bases()
        self.assertEqual(len(celulas), 84)
        self.assertEqual(dict(celulas)[(10, 3)][0], 4)  # 153, 370, 371, 407
        self.assertEqual(grupos[3][:2], ("sem interruptor", 175))

    def test_p1278_familias_narcisistas(self):
        # base 10, k = 2 e 3: soluções 153, 370, 371, 407; um par (370, 371): 3 famílias
        sol, fam, conta, pares = calculos.p1278_familias_narcisistas(3, (10,))
        self.assertEqual((sol, fam, pares), (4, 3, 1))
        self.assertAlmostEqual(conta, calculos.p1250_esperado_narcisistas(2, 10)[1] + calculos.p1250_esperado_narcisistas(3, 10)[1], places=12)


if __name__ == "__main__":
    unittest.main()
