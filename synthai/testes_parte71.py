"""Testes de unidade da Parte 71 (os autovalores da atenção): `python3 -m unittest synthai.testes_parte71`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import unittest

import calculos


class Cadeia:
    # profundidades: 1 nó em 0, 2 em 1, 4 em 2 (fator 2 por nível); substantivos
    indice = {f"n:{i}": i for i in range(7)}
    sinsets = [("n", ["r"], [], "")] + [("n", [f"a{i}"], ["n:0"], "") for i in (1, 2)] + [("n", [f"b{i}"], [f"n:{1 + (i - 3) // 2}"], "") for i in (3, 4, 5, 6)]


class TesteParte71(unittest.TestCase):
    def test_p1571_autovalores_jacobi(self):
        # uma matriz 3×3 com todos os termos diferentes de zero: autovalores conhecidos 2 − √2, 2, 2 + √2
        lam = calculos.p1571_autovalores_jacobi([[2.0, -1.0, 0.5], [-1.0, 2.0, -1.0], [0.5, -1.0, 2.0]])
        traco = sum(lam)
        self.assertAlmostEqual(traco, 6.0, places=12)
        self.assertEqual(len(lam), 3)
        self.assertTrue(lam[0] >= lam[1] >= lam[2])
        # o determinante (produto dos autovalores) confere com o calculado à mão: 2(4 − 1) + 1(−2 + 0,5) + 0,5(1 − 1) = 4,5
        self.assertAlmostEqual(lam[0] * lam[1] * lam[2], 4.5, places=10)

    def test_p1572_participacao(self):
        # uma matriz de posto 1 tem PR = 1; a identidade d×d tem PR = d
        pr1, f1, _ = calculos.p1572_participacao([[1.0, 2.0], [2.0, 4.0]])
        self.assertAlmostEqual(pr1, 1.0, places=9)
        self.assertAlmostEqual(f1, 1.0, places=9)
        prI, fI, _ = calculos.p1572_participacao([[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)])
        self.assertAlmostEqual(prI, 4.0, places=12)

    def test_p1573_crescimento_da_taxonomia(self):
        f, por, rmax = calculos.p1573_crescimento_da_taxonomia("n", 2, Cadeia())
        self.assertEqual((por, rmax), ({0: 1, 1: 2, 2: 4}, 2))
        self.assertAlmostEqual(f, 2.0, places=12)

    def test_p1574_irredutiveis_gf2(self):
        # Gauss: N(5) = (32 − 2)/5 = 6; com um bit trocado não há gêmeos (paridade); grau 15: 2.182
        self.assertEqual(calculos.p1574_irredutiveis_gf2(5, 2)[:3], (6, 6, 0))
        self.assertEqual(calculos.p1574_irredutiveis_gf2(15, 6)[:3], (2182, 2182, 224))

    def test_p1579_serie_singular_gf2(self):
        # só os graus 1 e 2: S = 2 · 2 · (8/9) (x e x + 1 dobram; x² + x + 1 multiplica por (2/4)/(9/16)); grau 5: N = 6, conta 36/32 · S/2
        serie, conta = calculos.p1579_serie_singular_gf2(5, ate=2)
        self.assertAlmostEqual(serie, 32 / 9, places=12)
        self.assertAlmostEqual(conta, 36 / 32 * serie / 2, places=12)
        self.assertAlmostEqual(calculos.p1579_serie_singular_gf2(17)[1], 755.458, places=3)

    def test_p1578_autovalores_da_atencao(self):
        pr, frac, lam = calculos.p1578_autovalores_da_atencao()
        self.assertEqual(len(lam), 16)
        self.assertAlmostEqual(pr, sum(lam) ** 2 / sum(x * x for x in lam), places=9)
        self.assertLess(pr, 3.0)


if __name__ == "__main__":
    unittest.main()
