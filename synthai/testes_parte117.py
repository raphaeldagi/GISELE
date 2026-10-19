"""Testes de unidade da Parte 117 (as camadas contrapostas com matrizes): `python3 -m unittest synthai.testes_parte117`.
Cada pNN pelo nome (Parte 58), casos com todos os termos ≠ 0 (Parte 30), controles dos dois lados (Parte 75)."""

import math
import random
import unittest

import calculos
from synthai import contraposto_matrizes as M


class TesteMatrizes(unittest.TestCase):
    def test_inversa(self):
        W = M.gaussiana(5, random.Random(3))
        self.assertLess(M.max_abs_menos_identidade(M.matmul(M.inversa(W), W)), 1e-12)

    def test_ortogonal(self):
        Q = M.ortogonal(6, random.Random(4))
        self.assertLess(M.max_abs_menos_identidade(M.matmul(M.transposta(Q), Q)), 1e-14)

    def test_singulares_e_det(self):
        A = [[3.0, 1.0], [1.0, 2.0]]                                # simétrica: valores singulares = autovalores (5 ± √5)/2
        sv = M.valores_singulares(A)
        self.assertAlmostEqual(sv[0], (5 + math.sqrt(5)) / 2, places=12)
        self.assertAlmostEqual(sv[1], (5 - math.sqrt(5)) / 2, places=12)
        self.assertAlmostEqual(M.log_abs_det(A), math.log(5.0), places=12)

    def test_digama_trigama(self):
        self.assertAlmostEqual(M.digama(1.0), -0.5772156649015329, places=10)
        self.assertAlmostEqual(M.trigama(0.5), math.pi ** 2 / 2, places=9)


class TesteParte117(unittest.TestCase):
    def test_p2951_ortogonal_escalada(self):
        a, b = calculos.p2951_ortogonal_escalada()
        self.assertLess(a, 1e-12)
        self.assertLess(b, 1e-12)

    def test_p2952_contrapostas_matriciais(self):
        c, k, d = calculos.p2952_contrapostas_matriciais()
        self.assertLess(c, 1e-11)
        self.assertLess(d, 5e-14)
        self.assertLess(d, c)

    def test_p2954_gaussianas_independentes(self):
        (mu, sd, top), sd2, (m1, v1), (E, V) = calculos.p2954_gaussianas_independentes()
        self.assertTrue(-4.6114 <= mu <= -4.5752)
        self.assertFalse(0.4786 <= sd <= 0.5042)         # (f) errou: a falha original fica no placar (Parte 74)
        self.assertTrue(0.4783 <= sd2 <= 0.5045)
        self.assertTrue(2.365 <= v1 <= 2.465)
        self.assertTrue(-0.07 <= top <= 0.12)

    def test_p2955_superposicao_matricial(self):
        self.assertTrue(1.8 <= calculos.p2955_superposicao_matricial()[2] <= 2.2)

    def test_p2956_rodada84(self):
        self.assertEqual(calculos.p2956_rodada84().hex(), "0x1.7000000000000p-48")

    def test_p1961_com_parte_117(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 118))))
        self.assertEqual(por[117], (10, 11))
        self.assertEqual((ok, tot), (251, 274))


if __name__ == "__main__":
    unittest.main()
