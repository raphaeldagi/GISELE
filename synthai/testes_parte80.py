"""Testes de unidade da Parte 80 (o valor de um conjunto): `python3 -m unittest synthai.testes_parte80`."""

import unittest

import calculos


class TesteParte80(unittest.TestCase):
    def test_p1841_voi_conjunto(self):
        # um sensor perfeito (q = 1) dá a informação perfeita: o VOI do 2 × 2 da P1632, com p = 0,5, u = [[1, 0], [0, 1]]: 1 − 0,5 = 0,5
        u = [[1.0, 0.0], [0.0, 1.0]]
        self.assertAlmostEqual(calculos.p1841_voi_conjunto(0.5, u, [1.0], [0]), 0.5, places=15)
        # um sensor sem informação (q = 0,5) vale zero; o conjunto vazio vale zero
        self.assertAlmostEqual(calculos.p1841_voi_conjunto(0.5, u, [0.5], [0]), 0.0, places=15)
        self.assertEqual(calculos.p1841_voi_conjunto(0.3, u, [0.9], []), 0.0)
        # complementaridade: com p = 0,8 e u favorecendo a ação 1, um sensor de 0,7 não muda a decisão, e dois juntos mudam
        u2 = [[1.0, 0.0], [0.0, 1.0]]
        um = calculos.p1841_voi_conjunto(0.8, u2, [0.7, 0.7], [0])
        dois = calculos.p1841_voi_conjunto(0.8, u2, [0.7, 0.7], [0, 1])
        self.assertAlmostEqual(um, 0.0, places=15)
        self.assertGreater(dois, 2 * um + 1e-6)

    def test_p1842_conjuntos(self):
        a1, b1, c1, d1 = calculos.p1842_conjuntos(semente=80)
        a2, b2, c2, d2 = calculos.p1842_conjuntos(semente=80, olhar=2)
        self.assertEqual(c1, c2)  # a complementaridade é do mundo, não do guloso
        self.assertGreater(a2, a1)
        self.assertLess(d2, d1)

    def test_p1843_rodada49(self):
        # a rodada reproduz a P1842
        a1, a2, b1, b2, d1 = calculos.p1843_rodada49()
        r1, r2 = calculos.p1842_conjuntos(semente=80), calculos.p1842_conjuntos(semente=80, olhar=2)
        self.assertEqual((a1, b1, d1), (r1[0], r1[1], r1[3]))
        self.assertEqual((a2, b2), (r2[0], r2[1]))


if __name__ == "__main__":
    unittest.main()
