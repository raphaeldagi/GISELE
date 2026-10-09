"""Testes de unidade da Parte 52: `python3 -m unittest synthai.testes_parte52`."""

import importlib.util
import math
import os
import random
import unittest

import calculos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("rodada26", os.path.join(RAIZ, "dialogo", "rodada26.py"))
r26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r26)


class PTFalso:
    """glosas: gato -> 'animal felino', cão -> 'animal canino', animal -> 'ser vivo'; felino só adjetivo."""
    lemas = {"1-n": ["gato"], "2-n": ["cão"], "3-n": ["animal"], "4-n": ["ser"], "5-a": ["felino"]}
    glosas = {"1-n": "animal felino", "2-n": "animal canino", "3-n": "ser vivo"}

    @staticmethod
    def fichas(t):
        return t.split()

    @staticmethod
    def lema(w):
        return w


class TesteParte52(unittest.TestCase):
    def test_exp_log_proprios(self):
        rng = random.Random(52)
        for _ in range(2000):
            x, y = rng.uniform(-30, 5), rng.uniform(1e-6, 50)
            self.assertLess(abs(r26.exp_(x) - math.exp(x)) / math.exp(x), 4e-16)
            self.assertLess(abs(r26.log_(y) - math.log(y)), 4e-16 * max(1.0, abs(math.log(y))))
        self.assertEqual((r26.exp_(0.0), r26.log_(1.0)), (1.0, 0.0))

    def test_resolver_4x4(self):
        # sistema com todos os coeficientes diferentes de zero e solução (1, -2, 3, 0,5)
        M = [[4.0, 1.0, 2.0, 1.0], [1.0, 5.0, 1.0, 2.0], [2.0, 1.0, 6.0, 1.0], [1.0, 2.0, 1.0, 7.0]]
        x = [1.0, -2.0, 3.0, 0.5]
        v = [sum(M[i][k] * x[k] for k in range(4)) for i in range(4)]
        for a, b in zip(r26.resolver(M, v), x):
            self.assertAlmostEqual(a, b, places=12)

    def test_inverte_e_soma(self):
        # 0x1A + 0xA1 = 0xBB (1 passo); de 1 a 0x1A: os de um dígito são palíndromos (0 passos)
        f, m, nao = calculos.p1003_inverte_e_soma(0x1A)
        self.assertEqual((f, nao), (1.0, []))
        # em base 10, 196 é o primeiro que não chega em 50 passos
        self.assertEqual(calculos.p1003_inverte_e_soma(196, 10)[2], [196])

    def test_funis_pt(self):
        top, g, frac, n, dez = calculos.p1002_funis_pt(PTFalso())
        # gato -> animal, cão -> animal, animal -> ser: 'animal' recebe 2 de 3
        self.assertEqual((top, g, n, dez), ("animal", 2, 3, [("animal", 2), ("ser", 1)]))
        self.assertAlmostEqual(frac, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
