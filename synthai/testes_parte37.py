"""Testes de unidade da Parte 37: `python3 -m unittest synthai.testes_parte37`."""

import random
import unittest

from .decisao import ThompsonBOCPD


class TesteBOCPD(unittest.TestCase):
    def test_pesos_somam_um_e_o_risco_cria_a_hipotese_nova(self):
        t = ThompsonBOCPD(2, random.Random(1), risco=0.1, hipoteses=8)
        t.atualizar(0, 1)
        hs = t.mist[0]
        self.assertAlmostEqual(sum(h[0] for h in hs), 1.0)
        # o braço 1 (não puxado): 0,9 na hipótese antiga Beta(1,1) + 0,1 na nova Beta(1,1) = a mesma hipótese, peso 1
        self.assertEqual(t.mist[1], [[1.0, 1.0, 1.0]])

    def test_preditiva_conta_contra_a_mudanca(self):
        t = ThompsonBOCPD(1, random.Random(2), risco=0.01, hipoteses=50)
        for _ in range(200):
            t.atualizar(0, 1)
        antes = max(h[0] for h in t.mist[0] if h[1] + h[2] > 150)
        for _ in range(15):
            t.atualizar(0, 0)  # o mundo mudou
        depois = sum(h[0] for h in t.mist[0] if h[1] + h[2] > 150)
        self.assertGreater(antes, 0.5)
        self.assertLess(depois, 0.5)  # a maior parte do peso foi para hipóteses jovens

    def test_substituir(self):
        t = ThompsonBOCPD(2, random.Random(3))
        t.substituir([2.0, 3.0], [19.0, 4.0])
        self.assertEqual(t.mist, [[[1.0, 2.0, 19.0]], [[1.0, 3.0, 4.0]]])


if __name__ == "__main__":
    unittest.main()
