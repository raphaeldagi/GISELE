"""Testes de unidade da Parte 64: `python3 -m unittest synthai.testes_parte64`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import unittest

import calculos


class DicionarioFalso:
    # go (2 letras) em 3 sinsets, set (3) em 2, aardvark (8) em 1: Spearman −1; go_away não conta (não é só letras)
    sinsets = [("n", ["set", "go"], [], ""), ("v", ["set", "go"], [], ""), ("v", ["go"], [], ""), ("n", ["aardvark"], [], ""),
               ("n", ["go_away"], [], "")]


class TesteParte64(unittest.TestCase):
    def test_p1361_fator_do_final(self):
        linhas = calculos.p1361_fator_do_final()
        self.assertEqual([x[:2] for x in (linhas[0], linhas[7], linhas[11])], [(5, 25), (12, 196), (16, 357)])
        self.assertAlmostEqual(linhas[11][2], linhas[11][3], places=12)  # base 16: o fator exato é o da paridade

    def test_p1362_brevidade_e_sentidos(self):
        rho, n, mono, por = calculos.p1362_brevidade_e_sentidos(DicionarioFalso())
        self.assertEqual((n, por), (3, {2: 3.0, 3: 2.0, 8: 1.0}))
        self.assertAlmostEqual(rho, -1.0, places=12)
        self.assertAlmostEqual(mono, 1 / 3, places=12)

    def test_p1363_quadrados_palindromos(self):
        # base 10, n < 30: 1, 2, 3, 11, 22 e 26 (26² = 676); conta = Σ 10^(−⌊L/2⌋), conferida por código
        k, conta, ns = calculos.p1363_quadrados_palindromos(30, 10)
        self.assertEqual((k, ns), (6, [1, 2, 3, 11, 22, 26]))
        self.assertAlmostEqual(conta, 3 * 1 + 6 * 0.1 + 20 * 0.1, places=12)

    def test_p1367_bases_novas_palindromos(self):
        b, m, bb, s, z = calculos.p1367_bases_novas_palindromos((5,))[0]
        self.assertEqual((b, m), (5, 25))
        self.assertAlmostEqual(bb, calculos.p1361_fator_do_final()[0][3], places=12)
        self.assertAlmostEqual(z, (m - bb) / s, places=12)


if __name__ == "__main__":
    unittest.main()
