"""Testes de unidade da Parte 76 (a forma do byte): `python3 -m unittest synthai.testes_parte76`."""

import unittest

import calculos
from synthai.gpt_kronecker import GPTKronecker


class TesteGPTKronecker(unittest.TestCase):
    def setUp(self):
        self.g = GPTKronecker(calculos.VOCAB_GPT, T=6, d1=2, d2=3, h=5, semente=3)
        self.x, self.y = self.g.codificar("the do"), self.g.codificar("he dog")

    def test_embedding_e_o_produto_de_kronecker(self):
        g = self.g
        c = g.indice["k"]  # 'k' = 0x6B: nibble alto 6, baixo 11
        self.assertEqual((g.alto[c], g.baixo[c]), (6, 11))
        for i in range(2):
            for j in range(3):
                self.assertEqual(g.p["E"][c][i * 3 + j], g.p["A"][6][i] * g.p["B"][11][j])

    def test_gradiente_por_diferencas_finitas(self):
        g = self.g
        _, G = g.gradiente(self.x, self.y)
        eps = 1e-6
        for k, linha, i in (("A", g.alto[self.x[0]], 1), ("B", g.baixo[self.x[2]], 2), ("A", g.alto[self.x[3]], 0)):
            v = g.p[k][linha][i]
            g.p[k][linha][i] = v + eps
            lp = g.perda(self.x, self.y)
            g.p[k][linha][i] = v - eps
            lm = g.perda(self.x, self.y)
            g.p[k][linha][i] = v
            self.assertAlmostEqual((lp - lm) / (2 * eps), G[k][linha][i], places=7)
        self.assertTrue(all(v == 0.0 for linha in G["E"] for v in linha))

    def test_pesos_de_embedding(self):
        # nibbles altos do vocabulário: 2 (espaço , ( ) -), 3 (; ?), 6 (a-o), 7 (p-z |): 4; baixos: os 16
        self.assertEqual(self.g.pesos_de_embedding(), (4 * 2 + 16 * 3, 34 * 6))

    def test_treino_baixa_a_perda(self):
        g = GPTKronecker(calculos.VOCAB_GPT, T=6, d1=2, d2=2, h=4, semente=5)
        perdas = g.treinar("the cat sat on the mat " * 20, passos=60, lr=0.02, semente=5)
        self.assertLess(sum(perdas[-10:]) / 10, sum(perdas[:10]) / 10)



class TesteParte76(unittest.TestCase):
    def test_p1721_kronecker_contra_cheio(self):
        # poucos passos: o teste confere a forma da saída e o controle (sem o cheio)
        ch, kr = calculos.p1721_kronecker_contra_cheio("pt", 76, passos=20)
        self.assertTrue(ch > 0 and kr > 0)
        nada, emb = calculos.p1721_kronecker_contra_cheio("pt", 76, embaralhar=True, passos=20)
        self.assertIsNone(nada)
        self.assertNotEqual(emb, kr)

    def test_p1722_libm_nas_duas_linguagens(self):
        r = calculos.p1722_libm_nas_duas_linguagens()
        self.assertEqual(sorted(r), ["48"])  # a Parte 77 corrigiu a 09 e a 14
        self.assertEqual(r["48"], (["log2"], True, []))


if __name__ == "__main__":
    unittest.main()
