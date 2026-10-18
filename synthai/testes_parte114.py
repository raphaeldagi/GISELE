"""Testes de unidade da Parte 114 (ML como DL e DL como ML): `python3 -m unittest synthai.testes_parte114`. Cada pNN pelo nome (Parte 58),
casos com todos os termos diferentes de zero (Parte 30) e controles dos dois lados (Parte 75)."""

import unittest

import calculos
from synthai import ml_dl as M


class TesteMLDL(unittest.TestCase):
    def test_gradiente_logistica_contra_diferenca_finita(self):
        X, y = M.dados_logistica(40, 5)
        w = [0.3, -0.2, 0.1, 0.05]
        g = M.gradiente_logistica(w, X, y, 0.01)

        def perda(v):
            import math
            tot = 0.0
            for x, yi in zip(X, y):
                z = sum(a * b for a, b in zip(v, x))
                p = M._sig(z)
                tot -= (yi * math.log(p) + (1 - yi) * math.log(1 - p)) / len(X)
            return tot + 0.005 * sum(t * t for t in v)
        for j in range(4):
            e = [0.0] * 4
            e[j] = 1e-6
            num = (perda([a + b for a, b in zip(w, e)]) - perda([a - b for a, b in zip(w, e)])) / 2e-6
            self.assertAlmostEqual(num, g[j], places=7)

    def test_ols_recupera_exato(self):
        X = [[1.0, 2.0, 1.0], [2.0, -1.0, 1.0], [0.5, 0.3, 1.0], [-1.0, 1.5, 1.0]]
        y = [0.7 * a - 0.3 * b + 0.1 for a, b, _ in X]
        for c, alvo in zip(M.ols(X, y), (0.7, -0.3, 0.1)):
            self.assertAlmostEqual(c, alvo, places=12)

    def test_df_ridge_extremos(self):
        H = [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 1.0], [2.0, -1.0, 1.0]]
        self.assertAlmostEqual(M.df_ridge_fechado(H, 1e-12), 3.0, places=6)   # sem cumeeira: df = nº de parâmetros
        self.assertLess(M.df_ridge_fechado(H, 1e6), 1.01)                    # cumeeira enorme: sobra só o viés (sem penalidade)


class TesteParte114(unittest.TestCase):
    def test_p2861_logistica_como_rede(self):
        dw, gn, kap = calculos.p2861_logistica_como_rede()
        self.assertLessEqual(dw, 1e-8)
        self.assertLess(gn, 1e-12)
        self.assertAlmostEqual(kap, 32.7234, places=3)

    def test_p2862_rede_linear_profunda(self):
        self.assertLessEqual(calculos.p2862_rede_linear_profunda(), 1e-10)

    def test_p2863_features_e_cabeca(self):
        rf, bp, tr = calculos.p2863_features_e_cabeca()
        self.assertTrue(0.0091 <= rf <= 0.020)
        self.assertTrue(0.80 <= bp / rf <= 1.60)
        self.assertTrue(0.60 <= tr / bp <= 0.99)

    def test_p2864_graus_de_liberdade(self):
        d1, e1, d2, e2 = calculos.p2864_graus_de_liberdade()
        self.assertTrue(30 <= d1 <= 41)
        self.assertLessEqual(abs(e1 - d1), 1.0)
        self.assertLessEqual(abs(e2 - d2), 1.0)
        self.assertTrue(0.40 <= d2 / d1 <= 0.65)

    def test_p2865_rodada81(self):
        br, bo = calculos.p2865_rodada81()
        self.assertEqual(br[0].hex(), "0x1.56469e859e0e0p-1")
        self.assertGreater(abs(br[0] - bo[0]), 0.01)   # em 500 passos a rede ainda NÃO chegou ao OLS (o que a rodada mede é a igualdade entre línguas)

    def test_p1961_com_parte_114(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[114], (10, 10))
        self.assertEqual((ok, tot), (207, 228))


if __name__ == "__main__":
    unittest.main()
