"""Testes de unidade da Parte 69 (a forma de GPT): `python3 -m unittest synthai.testes_parte69`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import math
import random
import unittest

import calculos
from synthai.gpt import GPT


class TesteGPT(unittest.TestCase):
    def test_gradiente_por_diferencas_finitas(self):
        # todos os termos diferentes de zero (vieses sorteados), regra da Parte 30
        g = GPT(list("abcde"), T=5, d=4, h=6, semente=1)
        r = random.Random(2)
        g.p["b1"] = [[r.gauss(0, 0.3) for _ in range(6)]]
        g.p["c"] = [[r.gauss(0, 0.3) for _ in range(5)]]
        x, y = [0, 1, 2, 3, 4], [1, 2, 3, 4, 0]
        _, G = g.gradiente(x, y)
        for k, M in g.p.items():
            for i in range(len(M)):
                for j in range(len(M[i])):
                    old = M[i][j]
                    M[i][j] = old + 1e-6
                    lp = g.perda(x, y)
                    M[i][j] = old - 1e-6
                    lm = g.perda(x, y)
                    M[i][j] = old
                    num = (lp - lm) / 2e-6
                    self.assertLess(abs(num - G[k][i][j]), 1e-5 * (abs(num) + abs(G[k][i][j])) + 1e-9, (k, i, j))

    def test_atencao_e_causal(self):
        # mudar um caractere futuro não muda a distribuição de uma posição anterior
        g = GPT(list("abcde"), T=5, d=4, h=6, semente=3)
        a = g.adiante([0, 1, 2, 3])["probs"][1]
        b = g.adiante([0, 1, 4, 4])["probs"][1]
        self.assertEqual(a, b)

    def test_treino_baixa_a_perda(self):
        g = GPT(list("ab "), T=4, d=4, h=8, semente=5)
        perdas = g.treinar("ab ab ab ab ab ab ab ab ab ", passos=300, lr=0.05, semente=5)
        self.assertLess(sum(perdas[-20:]) / 20, 0.5 * sum(perdas[:20]) / 20)


class TesteParte69(unittest.TestCase):
    def test_p1512_ngrama_bits(self):
        # unigrama de Witten-Bell sobre o uniforme (V = 34): treino 'aab', teste 'ab'; λ = 3/5
        pa, pb = 3 / 5 * 2 / 3 + 2 / 5 / 34, 3 / 5 * 1 / 3 + 2 / 5 / 34
        self.assertAlmostEqual(calculos.p1512_ngrama_bits("aab", "ab", 1), (-math.log2(pa) - math.log2(pb)) / 2, places=12)

    def test_p1514_pi_hex_digitos(self):
        self.assertEqual(calculos.p1514_pi_hex_digitos(16), "243f6a8885a308d3")

    def test_p1515_bits_hex(self):
        # uma sequência constante é prevista quase de graça; o acaso fica perto de 4 bits
        self.assertLess(calculos.p1515_bits_hex("a" * 1000, 2), 0.1)
        r = random.Random(9)
        self.assertAlmostEqual(calculos.p1515_bits_hex("".join("0123456789abcdef"[r.randrange(16)] for _ in range(5000)), 1), 4.0, delta=0.1)

    def test_p1511_corpus_de_glosas(self):
        treino, teste = calculos.p1511_corpus_de_glosas("pt")
        self.assertTrue(set(treino) <= set(calculos.VOCAB_GPT))
        self.assertAlmostEqual(len(teste) / (len(treino) + len(teste)), 0.1, delta=0.03)

    def test_p1513_gpt_bits(self):
        b, n, perda, g = calculos.p1513_gpt_bits("ab ab ab ab ab ab ab ab ab ab ab ab ab ab ", "ab ab ab ab ab ab ab ab ab ab ",
                                                 passos=200, T=4, d=4, h=8, lr=0.05, janelas=5)
        self.assertLess(b, 1.0)
        self.assertEqual(n, sum(len(v) * len(v[0]) for v in g.p.values()))


if __name__ == "__main__":
    unittest.main()
