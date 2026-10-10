"""Testes de unidade da Parte 65: `python3 -m unittest synthai.testes_parte65`. Cada pNN nova com o seu teste, chamada PELO NOME."""

from math import gcd
import unittest

import calculos


class DicionarioFalso:
    # uma cadeia a → b → c (profundidades 0, 1, 2) com definições de 2, 3 e 4 palavras: Spearman 1
    indice = {"n:1": 0, "n:2": 1, "n:3": 2}
    sinsets = [("n", ["a"], [], "x y"), ("n", ["b"], ["n:1"], "x y z"), ("n", ["c"], ["n:2"], "x y z w")]

    @staticmethod
    def definicao(glosa):
        return glosa


def ordem_bruta(a, p):
    k, x = 1, a % p
    while x != 1:
        x = x * a % p
        k += 1
    return k


class TesteParte65(unittest.TestCase):
    def test_p1391_o_que_nao_e_divisor(self):
        linhas = calculos.p1391_o_que_nao_e_divisor()
        self.assertEqual(len(linhas), 18)
        self.assertEqual((linhas[0][0], linhas[0][1]), (5, 48))
        self.assertEqual((linhas[11][0], linhas[11][3]), (16, 357))

    def test_p1397_correcao_b2_mais_1(self):
        b, det, cr, m, cc, sg, z = calculos.p1397_correcao_b2_mais_1((20,))[0]
        self.assertEqual((b, m, [r for r, _ in det]), (20, 584, [401, 160001]))
        self.assertLess(cr, 1.0)  # base par: a divisibilidade por 401 é ~10 vezes 1/401
        self.assertAlmostEqual(z, (m - cc) / sg, places=12)

    def test_p1392_profundidade_e_definicao(self):
        rho, n, por = calculos.p1392_profundidade_e_definicao(DicionarioFalso())
        self.assertEqual((n, por), (3, {}))
        self.assertAlmostEqual(rho, 1.0, places=12)

    def test_p1393_periodo_hex(self):
        ps = [p for p in range(3, 60) if all(p % q for q in range(2, p))]
        m16 = sum(ordem_bruta(16, p) / (p - 1) for p in ps) / len(ps)
        m2 = sum(ordem_bruta(2, p) / (p - 1) for p in ps) / len(ps)
        mx = sum(ordem_bruta(16, p) == (p - 1) // gcd(p - 1, 4) for p in ps) / len(ps)
        a, b, c, n = calculos.p1393_periodo_hex(3, 60)
        self.assertEqual(n, len(ps))
        self.assertAlmostEqual(a, m16, places=12)
        self.assertAlmostEqual(b, m2, places=12)
        self.assertAlmostEqual(c, mx, places=12)


if __name__ == "__main__":
    unittest.main()
