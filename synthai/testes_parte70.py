"""Testes de unidade da Parte 70 (álgebra e geometria): `python3 -m unittest synthai.testes_parte70`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import math
import unittest

import calculos


class Arvore:
    # uma árvore: raiz r com filhos a, b; a com filhos c, d; b com filho e (só substantivos)
    indice = {"n:r": 0, "n:a": 1, "n:b": 2, "n:c": 3, "n:d": 4, "n:e": 5}
    sinsets = [("n", ["r"], [], ""), ("n", ["a"], ["n:r"], ""), ("n", ["b"], ["n:r"], ""), ("n", ["c"], ["n:a"], ""), ("n", ["d"], ["n:a"], ""),
               ("n", ["e"], ["n:b"], "")]


class Ciclo:
    # um ciclo de 4: x tem dois pais (a e b), filhos da mesma raiz r: r-a-x-b-r; os quatro pontos do ciclo dão δ = 1
    indice = {"n:r": 0, "n:a": 1, "n:b": 2, "n:x": 3}
    sinsets = [("n", ["r"], [], ""), ("n", ["a"], ["n:r"], ""), ("n", ["b"], ["n:r"], ""), ("n", ["x"], ["n:a", "n:b"], "")]


class Embeddings:
    # vogais no eixo 1, consoantes no eixo 2: cos(vogal, vogal) = 1, cos(vogal, consoante) = 0; todos os pontos numa reta: a 1ª componente tem 100%
    def __init__(self):
        letras = "abcdefghijklmnopqrstuvwxyz"
        self.indice = {c: i for i, c in enumerate(letras)}
        self.p = {"E": [[1.0, 0.0] if c in "aeiou" else [0.0, 1.0] for c in letras]}


class TesteParte70(unittest.TestCase):
    def test_p1542_lei_de_potencia(self):
        pontos = [(n, 5.0 * n ** -0.1) for n in (1000, 2000, 4000, 8000)]
        A, alfa, n_alvo = calculos.p1542_lei_de_potencia(pontos, alvo=2.0)
        self.assertAlmostEqual(A, 5.0, places=9)
        self.assertAlmostEqual(alfa, 0.1, places=12)
        self.assertAlmostEqual(n_alvo, (5.0 / 2.0) ** 10, places=3)

    def test_p1543_geometria_dos_embeddings(self):
        vv, vc, cc, frac = calculos.p1543_geometria_dos_embeddings(Embeddings())
        self.assertEqual((vv, vc, cc), (1.0, 0.0, 1.0))
        self.assertAlmostEqual(frac, 1.0, places=9)

    def test_p1544_delta_de_gromov(self):
        self.assertEqual(calculos.p1544_delta_de_gromov("n", 50, 1, Arvore())[:3], (0.0, 0.0, 0.0))  # árvore: δ = 0 sempre
        maximo, media, frac, nos, dist = calculos.p1544_delta_de_gromov("n", 20, 1, Ciclo())
        self.assertEqual((maximo, frac, nos), (1.0, 1.0, 4))  # os 4 nós do ciclo: somas 2, 2, 4 → δ = (4 − 2)/2 = 1

    def test_p1545_bases_gf2(self):
        self.assertEqual(calculos.p1545_bases_gf2("1248")[:1], (1.0,))
        self.assertEqual(calculos.p1545_bases_gf2("1230")[:1], (0.0,))  # 3 = 1 ⊕ 2
        self.assertAlmostEqual(calculos.p1545_bases_gf2("1248")[1], 20160 / 65536, places=15)

    def test_p1541_escala_gpt(self):
        pontos, n, g = calculos.p1541_escala_gpt("en", d=4, marcos=(5, 10), T=6, janelas=2)
        self.assertEqual([p for p, _ in pontos], [5, 10])
        self.assertEqual(n, sum(len(v) * len(v[0]) for v in g.p.values()))
        self.assertTrue(all(0 < b < 10 for _, b in pontos))


if __name__ == "__main__":
    unittest.main()
