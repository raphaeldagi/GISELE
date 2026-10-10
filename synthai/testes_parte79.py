"""Testes de unidade da Parte 79 (causa e confiança): `python3 -m unittest synthai.testes_parte79`."""

import unittest

import calculos


class TesteParte79(unittest.TestCase):
    def test_p1811_confusao(self):
        ing, aj, itv = calculos.p1811_confusao()
        self.assertAlmostEqual(ing, 1.0, delta=0.0101)
        self.assertAlmostEqual(aj, 0.5, delta=0.0116)
        self.assertAlmostEqual(itv, 0.5, delta=0.0116)
        # sem confusão (a = 0), a ingênua já acerta o efeito
        self.assertAlmostEqual(calculos.p1811_confusao(a=0.0)[0], 0.5, delta=0.02)

    def test_p1812_minha_calibracao(self):
        n, ac, por = calculos.p1812_minha_calibracao()
        self.assertEqual(n, sum(v[0] for v in por.values()))
        self.assertTrue(0.0 < ac < 1.0)

    def test_p1813_fator_de_alargamento(self):
        # acertar o nominal dá fator 1; acertar 68,27% (± 1 desvio) quando se declara 90% dá 1,645
        self.assertAlmostEqual(calculos.p1813_fator_de_alargamento(0.9)[2], 1.0, places=12)
        self.assertAlmostEqual(calculos.p1813_fator_de_alargamento(0.682689492137086)[2], 1.6448536269514715, places=9)


if __name__ == "__main__":
    unittest.main()
