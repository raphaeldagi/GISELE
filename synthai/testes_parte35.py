"""Testes de unidade da Parte 35: `python3 -m unittest synthai.testes_parte35`."""

import random
import unittest

from .decisao import ThompsonSurpresa


class TesteSurpresa(unittest.TestCase):
    def test_renova_so_o_braco_desmentido(self):
        t = ThompsonSurpresa(2, random.Random(1), janela=10, z=3.0)
        t.a, t.b = [91.0, 50.0], [11.0, 50.0]  # braço 0 crê em p ~ 0,89
        for _ in range(10):
            t.atualizar(0, 0)  # dez fracassos seguidos: desmentido
        self.assertEqual(t.renovacoes, 1)
        self.assertEqual((t.a[0], t.b[0]), (1.0, 11.0))
        self.assertEqual((t.a[1], t.b[1]), (50.0, 50.0))  # o outro braço não muda

    def test_nao_renova_o_que_confirma(self):
        t = ThompsonSurpresa(1, random.Random(2), janela=10, z=3.0)
        t.a, t.b = [51.0], [51.0]
        for r in [1, 0] * 5:
            t.atualizar(0, r)
        self.assertEqual(t.renovacoes, 0)


if __name__ == "__main__":
    unittest.main()
