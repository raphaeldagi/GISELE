"""Testes da Parte 155: as estatísticas exatas do fim do episódio (synthai/tabuleiro.py) e a P3214 pelo nome."""
import itertools
import unittest

import calculos as c
from synthai import tabuleiro as T


class TestesParte155(unittest.TestCase):
    def test_acerto_igual_ao_de_aleatorio_exato(self):
        _, B, f = c._casos_p154()[0]
        a = T.aleatorio_exato(B, f, 3, 3, 4)
        e = T.estatisticas_exatas(B, f, 3, 3, 4)["acerto"]
        self.assertAlmostEqual(a, e, places=12)

    def test_simetria_da_ordem_reversa(self):
        # rotação de 180°: acerto igual, deslocamento com o sinal trocado
        _, B, f = c._casos_p154()[0]
        d = T.estatisticas_exatas(B, f, 3, 3, 4)
        r = T.estatisticas_exatas(B, f, 3, 3, 4, ordem="reversa")
        self.assertAlmostEqual(d["acerto"], r["acerto"], places=12)
        self.assertAlmostEqual(d["dr"], -r["dr"], places=12)
        self.assertAlmostEqual(d["dc"], -r["dc"], places=12)

    def test_uniforme_sem_deriva(self):
        todas = ["".join(x) for L in (3, 4) for x in itertools.product("ab", repeat=L)]
        u = T.estatisticas_exatas(todas, {"A": 0.6, "B": 0.4}, 3, 3, 4, casa="uniforme")
        self.assertAlmostEqual(u["dr"], 0.0, places=12)
        self.assertAlmostEqual(u["dc"], 0.0, places=12)
        self.assertAlmostEqual(u["acerto"], 1.0, places=12)

    def test_comprimento_forma_fechada_2x2(self):
        # grade 2×2, de 2 a 3 letras, uma letra só: com 2 letras, 1 vizinha livre (colapso de 2 em 1? não: as 2 livres têm a mesma letra -> 1 ação) + PARAR
        # -> para com 2 letras com chance 1/2; senão 3 letras. E[comprimento] = 2,5
        e = T.estatisticas_exatas(["aa"], {"A": 1.0}, 2, 2, 3)
        self.assertAlmostEqual(e["comprimento"], 2.5, places=14)

    def test_p3214_deriva_do_setdefault(self):
        r = c.p3214_deriva_do_setdefault(maximo=4, casos=("B",))
        self.assertLess(r["B"]["direta"]["dr"], 0.0)
        self.assertGreater(r["B"]["reversa"]["dr"], 0.0)

    def test_p3215_deriva_por_comprimento(self):
        r = c.p3215_deriva_por_comprimento(maximos=(4,))
        self.assertAlmostEqual(r[4]["dr"], -0.3984, places=4)


if __name__ == "__main__":
    unittest.main()
