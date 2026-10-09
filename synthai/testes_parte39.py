"""Testes de unidade da Parte 39 (lógica real diferenciável): `python3 -m unittest synthai.testes_parte39`."""

import random
import unittest

from .neurossimbolico import LOGICAS, Predicado, gradiente_implicacao, satisfacao, sigma, treinar_supervisionado


class TesteLogicas(unittest.TestCase):
    def test_valores_com_termos_nao_nulos(self):
        a, b = 0.7, 0.4
        T, S, I = LOGICAS["lukasiewicz"]
        self.assertAlmostEqual(T(a, b), 0.1)
        self.assertAlmostEqual(S(a, b), 1.0)
        self.assertAlmostEqual(I(a, b), 0.7)
        T, S, I = LOGICAS["godel"]
        self.assertEqual((T(a, b), S(a, b), I(a, b)), (0.4, 0.7, 0.4))
        T, S, I = LOGICAS["produto"]
        self.assertAlmostEqual(T(a, b), 0.28)
        self.assertAlmostEqual(S(a, b), 0.82)
        self.assertAlmostEqual(I(a, b), 0.58)

    def test_gradientes_por_diferenca_finita(self):
        h = 1e-7
        for nome in LOGICAS:
            I = LOGICAS[nome][2]
            for a, b in ((0.7, 0.4), (0.3, 0.6)):
                ga, gb = gradiente_implicacao(nome, a, b)
                self.assertAlmostEqual(ga, (I(a + h, b) - I(a, b)) / h, places=4)
                self.assertAlmostEqual(gb, (I(a, b + h) - I(a, b)) / h, places=4)

    def test_predicado_e_treino(self):
        self.assertAlmostEqual(sigma(0.0), 0.5)
        p = Predicado()
        treinar_supervisionado(p, [({"fur"}, 1), ({"wheel"}, 0)] * 20, taxa=0.5, epocas=3, rng=random.Random(1))
        self.assertGreater(p({"fur"}), 0.9)
        self.assertLess(p({"wheel"}), 0.1)
        self.assertAlmostEqual(satisfacao("lukasiewicz", [(0.7, 0.4), (0.2, 0.9)]), (0.7 + 1.0) / 2)


if __name__ == "__main__":
    unittest.main()
