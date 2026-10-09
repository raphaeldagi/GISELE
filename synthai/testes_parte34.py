"""Testes de unidade da Parte 34: `python3 -m unittest synthai.testes_parte34`."""

import random
import unittest

from .decisao import ThompsonMorris
from .dicionario import LogisticaSGD, NaiveBayesContagens


class TesteMorris(unittest.TestCase):
    def test_sem_vies_e_um_digito_hex(self):
        rng = random.Random(1)
        est = []
        for _ in range(4000):
            t = ThompsonMorris(1, rng)
            for _ in range(100):
                t.atualizar(0, 1)
            self.assertLessEqual(t.ca[0], 15)
            est.append(t.a[0] - 1)
        m = sum(est) / len(est)
        self.assertLess(abs(m - 100) / 100, 0.05)  # E[2^c - 1] = n; dp relativo ~ 0,7/sqrt(4000) ~ 1%


class TesteClassificadores(unittest.TestCase):
    def test_naive_bayes_ordem_nao_importa(self):
        dados = [(["cat", "fur"], "n"), (["run", "fast"], "v"), (["dog", "fur"], "n"), (["walk", "slow"], "v"),
                 (["fur", "pet"], "n")]
        a, b = NaiveBayesContagens(), NaiveBayesContagens()
        for x, y in dados:
            a.aprender(x, y)
        for x, y in reversed(dados):
            b.aprender(x, y)
        self.assertEqual(a.cont, b.cont)
        self.assertEqual(a.prever(["fur"]), "n")
        self.assertEqual(a.prever(["fast", "walk"]), "v")

    def test_logistica_aprende_o_simples(self):
        m = LogisticaSGD(["n", "v"], passo=0.5)
        for _ in range(20):
            m.aprender(["fur"], "n")
            m.aprender(["run"], "v")
        self.assertEqual(m.prever(["fur"]), "n")
        self.assertEqual(m.prever(["run"]), "v")


if __name__ == "__main__":
    unittest.main()
