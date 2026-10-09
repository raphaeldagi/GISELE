"""Testes de unidade da Parte 44: `python3 -m unittest synthai.testes_parte44`."""

import random
import unittest

from .decisao import ThompsonBOCPDGlobal


class TesteGlobal(unittest.TestCase):
    def test_pesos_e_a_hipotese_nova(self):
        t = ThompsonBOCPDGlobal(3, random.Random(1), risco=0.1)
        t.atualizar(0, 1)
        self.assertAlmostEqual(sum(h[0] for h in t.hs), 1.0)
        # a hipótese nova nasceu com todos os braços em Beta(1, 1) e recebeu a observação: a = 2 no braço 0
        self.assertTrue(any(h[1] == [2.0, 1.0, 1.0] for h in t.hs))

    def test_a_evidencia_de_um_braco_renova_todos(self):
        t = ThompsonBOCPDGlobal(2, random.Random(2), risco=0.01, hipoteses=50)
        for _ in range(150):
            t.atualizar(0, 1)
            t.atualizar(1, 0)
        for _ in range(20):
            t.atualizar(0, 0)  # o braço 0 mudou
        top = t.hs[0]
        self.assertLess(top[1][1] + top[2][1], 100)  # a hipótese mais pesada esqueceu também o braço 1

    def test_substituir(self):
        t = ThompsonBOCPDGlobal(2, random.Random(3))
        t.substituir([2.0, 3.0], [19.0, 4.0])
        self.assertEqual(t.hs, [[1.0, [2.0, 3.0], [19.0, 4.0]]])


if __name__ == "__main__":
    unittest.main()
