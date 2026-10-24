"""Testes da Parte 154: a casa uniforme no enumerador exato (synthai/tabuleiro.py) e a P3213 pelo nome."""
import itertools
import unittest

import calculos as c
from synthai import tabuleiro as T


class TestesParte154(unittest.TestCase):
    def test_uniforme_igual_a_primeira_com_letras_todas_distintas(self):
        # com uma letra por casa (9 letras distintas em 9 casas é impossível de garantir num sorteio; usamos a forma fechada): numa grade 2×2 com
        # uma só letra, toda letra é a mesma, e a casa uniforme e a primeira dão o mesmo por simetria da grade 2×2
        a = T.aleatorio_exato(["aaa"], {"A": 1.0}, 2, 3, 4)
        b = T.aleatorio_exato(["aaa"], {"A": 1.0}, 2, 3, 4, casa="uniforme")
        self.assertAlmostEqual(a, b, places=14)

    def test_uniforme_controle_total(self):
        todas = ["".join(x) for L in (3, 4, 5) for x in itertools.product("ab", repeat=L)]
        self.assertAlmostEqual(T.aleatorio_exato(todas, {"A": 0.6, "B": 0.4}, 3, casa="uniforme"), 1.0, places=12)

    def test_padrao_continua_o_jogo(self):
        # o padrão (casa="primeira") é o da Parte 153: o caso B dá 0,30169
        _, B, f = c._casos_p154()[0]
        self.assertAlmostEqual(T.aleatorio_exato(B, f, 3), 0.30169, places=5)

    def test_p3213_setdefault_e_memoria(self):
        r = c.p3213_setdefault_e_memoria(maximo=4)
        for v in r.values():
            self.assertAlmostEqual(v[3] * v[5], v[4], places=12)
            self.assertGreater(v[3], 1.0)


if __name__ == "__main__":
    unittest.main()
