"""Testes de unidade da Parte 38: `python3 -m unittest synthai.testes_parte38`."""

import random
import unittest
from math import log

from .decisao import ThompsonMistura


class TesteMistura(unittest.TestCase):
    def test_a_mistura_perde_no_maximo_ln_m_para_o_melhor(self):
        t = ThompsonMistura(3, random.Random(1))
        rng = random.Random(2)
        for passo in range(600):
            ps = (0.2, 0.5, 0.8) if passo < 300 else (0.8, 0.5, 0.2)
            i = t.escolher()
            t.atualizar(i, 1 if rng.random() < ps[i] else 0)
        self.assertLessEqual(t.perda_mistura, min(t.perda) + log(4) + 1e-9)
        self.assertAlmostEqual(sum(t.pesos()), 1.0)

    def test_mundo_estavel_favorece_h_zero(self):
        t = ThompsonMistura(2, random.Random(3))
        rng = random.Random(4)
        for _ in range(1500):
            i = t.escolher()
            t.atualizar(i, 1 if rng.random() < (0.3, 0.7)[i] else 0)
        ws = t.pesos()
        self.assertEqual(max(range(4), key=ws.__getitem__) in (0, 1), True)  # H = 0 ou 1/2000


if __name__ == "__main__":
    unittest.main()
