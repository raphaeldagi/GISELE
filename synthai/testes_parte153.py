"""Testes da Parte 153: o braço aleatório exato (synthai/tabuleiro.py) e P3210-P3212 pelo nome."""
import itertools
import unittest

import calculos as c
from synthai import tabuleiro as T


class TestesParte153(unittest.TestCase):
    def test_exato_controle_um(self):
        todas = ["".join(x) for L in (3, 4, 5) for x in itertools.product("ab", repeat=L)]
        self.assertAlmostEqual(T.aleatorio_exato(todas, {"A": 0.6, "B": 0.4}, 3), 1.0, places=12)

    def test_exato_simetria_meio_a_meio(self):
        # letras meio a meio e um dicionário que só olha a 1ª e a última letra: 1/2 · 1/2, com ou sem colapso
        duas = ["".join(x) for L in (3, 4, 5) for x in itertools.product("ab", repeat=L)]
        A = [w for w in duas if w[0] == "a" and w[-1] == "b"]
        self.assertAlmostEqual(T.aleatorio_exato(A, {"A": 1.0, "B": 1.0}, 3), 0.25, places=12)

    def test_exato_uma_letra(self):
        # uma letra só: em toda casa há uma ação (a letra) + PARAR; com dicionário {aaa}, a chance é s₃ da geometria da grade com colapso total
        e = T.aleatorio_exato(["aaa"], {"A": 1.0}, 2, 3, 4)
        # grade 2×2, 3 a 4 letras: com 1 letra, depois 2: 1 ação (sem PARAR) -> 3 letras: 1 livre + PARAR -> 1/2 de parar
        self.assertAlmostEqual(e, 0.5, places=14)

    def test_p3210_campo_medio_contra_exato(self):
        r = c.p3210_campo_medio_contra_exato()
        self.assertAlmostEqual(r["controle"][0], 1.0, places=12)
        self.assertAlmostEqual(r["B"][3], 1.0429, places=3)

    def test_p3211_simulado_caso_b(self):
        s, e, z = c.p3211_simulado_caso_b(episodios=20000)
        self.assertLess(abs(z), 4.0)

    def test_p3212_campo_medio_lote_novo(self):
        r = c.p3212_campo_medio_lote_novo()
        self.assertAlmostEqual(r["A'"][2], 0.9156, places=3)


if __name__ == "__main__":
    unittest.main()
