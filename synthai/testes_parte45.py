"""Testes de unidade da Parte 45: `python3 -m unittest synthai.testes_parte45`."""

import random
import unittest

from .decisao import ThompsonBOCPDGlobalMAP


class TesteMAP(unittest.TestCase):
    def test_decide_pela_mais_pesada(self):
        t = ThompsonBOCPDGlobalMAP(2, random.Random(1))
        # a mais pesada diz: braço 1 é ótimo, braço 0 é péssimo; uma hipótese leve diz o contrário
        t.hs = [[0.9, [1.0, 500.0], [500.0, 1.0]], [0.1, [500.0, 1.0], [1.0, 500.0]]]
        self.assertEqual({t.escolher() for _ in range(50)}, {1})

    def test_herda_a_atualizacao(self):
        t = ThompsonBOCPDGlobalMAP(3, random.Random(2), risco=0.1)
        t.atualizar(2, 0)
        self.assertAlmostEqual(sum(h[0] for h in t.hs), 1.0)


if __name__ == "__main__":
    unittest.main()
