"""Testes de unidade da Parte 59: `python3 -m unittest synthai.testes_parte59`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import unittest

import calculos


class GrafoFalso:
    @staticmethod
    def grafo_de_definicoes():
        # a é definida por b e c; b por c; c por a; d por c: c define 3, a define 1, b define 1, d não define nada
        return {"a": {"b", "c"}, "b": {"c"}, "c": {"a"}, "d": {"c"}}


class TesteParte59(unittest.TestCase):
    def test_p1213_persistencia_hex(self):
        # conferido por código: de 16 a 0x3F, a maior é 3 (primeiro em 62 = 0x3E: 3·14 = 0x2A, 2·10 = 0x14, 1·4 = 4), média 68/48
        m, q, med = calculos.p1213_persistencia_hex(0x40)
        self.assertEqual((m, q), (3, 62))
        self.assertAlmostEqual(med, 1.4166666666666667, places=12)

    def test_p1212_palavras_que_nao_definem(self):
        frac, n, top = calculos.p1212_palavras_que_nao_definem(GrafoFalso())
        self.assertEqual((n, top[0]), (4, ("c", 3)))
        self.assertAlmostEqual(frac, 0.25, places=12)  # só 'd' não define

    def test_p1211_nome_e_palavra(self):
        n, k, ex = calculos.p1211_nome_e_palavra()
        self.assertEqual((n, k), (9176, 1805))
        self.assertIn("Abril", ex)


if __name__ == "__main__":
    unittest.main()
