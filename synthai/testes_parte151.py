"""Testes da Parte 151: a geometria do braço aleatório (synthai/tabuleiro.py) e P3207-P3208 pelo nome."""
import unittest

import calculos as c
from synthai import tabuleiro as T


class TestesParte151(unittest.TestCase):
    def test_paradas_somam_um(self):
        for tam, mi, ma in ((4, 3, 5), (5, 3, 5), (6, 3, 5), (5, 4, 5)):
            s = T.paradas_por_comprimento(tam, mi, ma)
            self.assertAlmostEqual(sum(s.values()), 1.0, places=12)

    def test_paradas_forma_fechada_2x2(self):
        # grade 2×2, de 2 a 3 letras: toda casa tem 3 vizinhas. Com 1 letra: 3 vizinhas, sem PARAR. Com 2 letras: 2 livres + PARAR, s₂ = 1/3.
        # Com 3 letras: para sempre (máximo). s₃ = 2/3.
        s = T.paradas_por_comprimento(2, 2, 3)
        self.assertAlmostEqual(s[2], 1 / 3, places=14)
        self.assertAlmostEqual(s[3], 2 / 3, places=14)

    def test_aleatorio_geometrico_um_dicionario(self):
        # um dicionário de uma palavra de 3 letras 'aaa' num tabuleiro só de A: D₃ = 1, então a previsão é s₃
        s = T.paradas_por_comprimento()
        self.assertAlmostEqual(T.aleatorio_geometrico(["aaa"], {"A": 1.0}), s[3], places=14)

    def test_p3207_aleatorio_geometria(self):
        m, sd, g = c.p3207_aleatorio_geometria(tamanho=4, sementes=(161, 162))
        self.assertTrue(0.0 < m < 0.1)
        self.assertAlmostEqual(g, 0.02395, places=4)

    def test_p3208_repertorio(self):
        r = c.p3208_repertorio("embutido", "en", sementes=(101, 102), episodios=1000, avaliacao=200)
        self.assertTrue(0.0 <= r["repete"] <= 1.0)
        self.assertTrue(r["distintas"] >= 1)


if __name__ == "__main__":
    unittest.main()
