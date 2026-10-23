"""Testes da Parte 147: synthai/grpo_palavras.py (a GRPO de rl_grupos.py no jogo de word_rl_lab) e a P3198 pelo nome."""
import random
import unittest

import calculos as c
from synthai import palavras_rl as P
from synthai import grpo_palavras as g


class TestesParte147(unittest.TestCase):
    def test_probs_somam_um(self):
        a = g.AgenteGRPO()
        a.theta[("AB", "C")] = 2.0
        p = a.probs("AB", ["C", "D", P.STOP])
        self.assertAlmostEqual(sum(p), 1.0, places=14)
        self.assertGreater(p[0], p[1])

    def test_greedy_escolhe_o_maior_logit(self):
        a = g.AgenteGRPO()
        a.theta[("X", "Y")] = 1.0
        self.assertEqual(a.choose("X", ["Z", "Y"], "greedy"), "Y")

    def test_episodio_amostrado_e_trajetoria(self):
        env = P.WordGridEnv(5, 3, 5, rng=random.Random(1))
        env.reset()
        traj, r, ok = g.episodio_amostrado(env, P.Dicionario(P.EMBEDDED_WORDS), g.AgenteGRPO(seed=2), (0, 0))
        self.assertTrue(len(traj) >= 1)
        self.assertIn(r, (P.FAIL_REWARD,) + tuple(float(P.word_score(w)) for w in ["abc", "abcd", "abcde"]) if not ok else (r,))

    def test_treinar_conta_grupos(self):
        a, sem, n = g.treinar(P.Dicionario(P.EMBEDDED_WORDS), episodios=200, G=4, seed=3)
        self.assertEqual(n, 50)
        self.assertLessEqual(sem, n)

    def test_p3198_grpo_no_jogo_de_palavras(self):
        r = c.p3198_grpo_no_jogo_de_palavras()
        self.assertEqual((round(r["Q"], 4), round(r["G2"], 4), round(r["G8"], 4)), (0.1533, 0.2017, 0.1707))


if __name__ == "__main__":
    unittest.main()
