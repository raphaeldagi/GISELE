"""Testes de unidade da Parte 43: `python3 -m unittest synthai.testes_parte43`."""

import random
import unittest

from .decisao import ThompsonJeffreys, ThompsonSurpresa, ThompsonSurpresaExposta


class TesteParte43(unittest.TestCase):
    def test_jeffreys_comeca_em_meio(self):
        t = ThompsonJeffreys(3, random.Random(1))
        self.assertEqual((t.a, t.b), ([0.5] * 3, [0.5] * 3))
        t.atualizar(1, 1)
        self.assertEqual(t.a[1], 1.5)

    def test_janela_e_periodo_configuraveis(self):
        self.assertEqual(ThompsonSurpresa(2, random.Random(2), janela=40).janela, 40)
        self.assertEqual(ThompsonSurpresaExposta(2, random.Random(3), periodo=100).periodo, 100)


if __name__ == "__main__":
    unittest.main()
