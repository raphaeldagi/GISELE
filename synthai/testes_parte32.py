"""Testes de unidade da Parte 32 (decisão bayesiana exata): `python3 -m unittest synthai.testes_parte32`."""

import random
import unittest
from math import log

from .decisao import (PSRL, QEpsilon, QLearningMDP, RegressaoBayesiana, RegressaoSGD, ThompsonBernoulli, UCB1,
                      cota_lai_robbins, kl_bernoulli, media_otima, politica_horizonte, ridge_em_lote, riverswim,
                      rodar_bandido, rodar_mdp)


class TesteBandido(unittest.TestCase):
    def test_thompson_conta_e_teto(self):
        t = ThompsonBernoulli(2, random.Random(1), teto=6)
        for r in (1, 1, 0):
            t.atualizar(0, r)
        self.assertEqual(t.estado(), ([3.0, 1.0], [2.0, 1.0]))
        t.atualizar(0, 1)  # a + b = 4 + 2 = 6: ainda no teto
        t.atualizar(0, 1)  # 5 + 2 = 7 > 6: metade
        self.assertEqual(t.estado()[0][0], 2.5)
        self.assertEqual(t.estado()[1][0], 1.0)

    def test_q_epsilon_passo(self):
        q = QEpsilon(3, random.Random(2), alfa=0.5, eps=0.0)
        q.atualizar(1, 1)
        q.atualizar(1, 0)
        self.assertEqual(q.q, [0.0, 0.25, 0.0])
        self.assertEqual(q.escolher(), 1)

    def test_kl_e_lai_robbins(self):
        self.assertAlmostEqual(kl_bernoulli(0.5, 0.5), 0.0)
        self.assertAlmostEqual(kl_bernoulli(0.2, 0.4), 0.2 * log(0.5) + 0.8 * log(0.8 / 0.6))
        c = cota_lai_robbins([0.2, 0.4], 1000)
        self.assertAlmostEqual(c, 0.2 * log(1000) / kl_bernoulli(0.2, 0.4))

    def test_rodar_bandido_arrependimento_monotono(self):
        a = rodar_bandido(UCB1(3, random.Random(3)), [0.1, 0.5, 0.9], 200, random.Random(4))
        self.assertEqual(len(a), 200)
        self.assertTrue(all(y >= x for x, y in zip(a, a[1:])))
        self.assertLess(a[-1], 200 * 0.8)


class TesteMDP(unittest.TestCase):
    def test_riverswim_probabilidades(self):
        P, R = riverswim(6)
        for s in range(6):
            for a in range(2):
                self.assertAlmostEqual(sum(p for _, p in P[s][a]), 1.0)
        self.assertEqual(R[0][0], 0.005)

    def test_media_otima_mdp_de_brinquedo(self):
        # dois estados; ficar no 1 rende 1 por passo, ir do 0 ao 1 custa um passo: ganho médio ótimo = 1
        P = [[[(0, 1.0)], [(1, 1.0)]], [[(0, 1.0)], [(1, 1.0)]]]
        R = [[0.0, 0.0], [0.0, 1.0]]
        self.assertAlmostEqual(media_otima(P, R, 200), 1.0)
        self.assertEqual(politica_horizonte(P, R, 3)[0], [1, 1])

    def test_agentes_rodam(self):
        P, R = riverswim(6)
        for ag in (PSRL(6, random.Random(5)), QLearningMDP(6, random.Random(6))):
            self.assertGreaterEqual(rodar_mdp(ag, P, R, 100, random.Random(7)), 0.0)


class TesteContinuo(unittest.TestCase):
    def test_recursiva_igual_ao_lote_em_qualquer_ordem(self):
        rng = random.Random(8)
        fs = [[rng.gauss(0, 1) for _ in range(4)] for _ in range(30)]
        ys = [f[0] - 2 * f[1] + 0.5 * f[3] + rng.gauss(0, 0.1) for f in fs]
        lote = ridge_em_lote(fs, ys, lam=0.1)
        for ordem in (range(30), reversed(range(30))):
            r = RegressaoBayesiana(4, lam=0.1)
            for i in ordem:
                r.atualizar(fs[i], ys[i])
            for a, b in zip(r.w, lote):
                self.assertAlmostEqual(a, b, places=9)

    def test_sgd_passo(self):
        s = RegressaoSGD(2, passo=0.5)
        s.atualizar([1.0, 2.0], 3.0)
        self.assertEqual(s.w, [1.5, 3.0])


if __name__ == "__main__":
    unittest.main()
