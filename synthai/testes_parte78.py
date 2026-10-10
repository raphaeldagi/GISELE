"""Testes de unidade da Parte 78 (a atenção de posto baixo): `python3 -m unittest synthai.testes_parte78`."""

import random
import unittest

import calculos
from synthai.gpt import GPT


class TesteParte78(unittest.TestCase):
    def test_p1781_svd_por_jacobi(self):
        r = random.Random(5)
        M = [[r.gauss(0, 1) for _ in range(4)] for _ in range(4)]
        sig, U, V = calculos.p1781_svd_por_jacobi(M)
        R = [[sum(U[i][k] * sig[k] * V[j][k] for k in range(4)) for j in range(4)] for i in range(4)]
        self.assertLess(max(abs(R[i][j] - M[i][j]) for i in range(4) for j in range(4)), 1e-12)
        self.assertTrue(sig[0] >= sig[1] >= sig[2] >= sig[3] >= 0.0)
        # V é ortogonal: VᵀV = I
        for a in range(4):
            for b in range(4):
                self.assertAlmostEqual(sum(V[k][a] * V[k][b] for k in range(4)), 1.0 if a == b else 0.0, places=12)

    def test_p1782_atencao_de_posto(self):
        g = GPT(calculos.VOCAB_GPT, T=6, d=4, h=5, semente=3)
        h1 = calculos.p1782_atencao_de_posto(g, 1)
        Q, K = h1.p["Q"], h1.p["K"]
        M1 = [[sum(Q[i][k] * K[j][k] for k in range(4)) for j in range(4)] for i in range(4)]
        # posto 1: todas as linhas são proporcionais (os menores 2 × 2 se anulam)
        self.assertAlmostEqual(M1[0][0] * M1[1][1] - M1[0][1] * M1[1][0], 0.0, places=12)
        x, y = g.codificar("the do"), g.codificar("he dog")
        self.assertAlmostEqual(calculos.p1782_atencao_de_posto(g, 4).perda(x, y), g.perda(x, y), places=10)

    def test_p1783_bits_por_posto(self):
        b, por, sig = calculos.p1783_bits_por_posto("pt", 71, postos=(1, 16), passos=10)
        self.assertAlmostEqual(por[16], b, places=9)
        self.assertEqual(len(sig), 16)


if __name__ == "__main__":
    unittest.main()
