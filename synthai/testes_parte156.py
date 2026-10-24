"""Testes da Parte 156: as esperanças exatas das decisões do episódio (synthai.tabuleiro.ramificacao_exata) e a P3216 pelo nome."""
import itertools
import unittest

import calculos as c
from synthai import tabuleiro as T


class TestesParte156(unittest.TestCase):
    def test_acerto_igual_ao_de_aleatorio_exato(self):
        _, A, f = c._casos_p156(4)[1]
        for casa in ("primeira", "uniforme"):
            self.assertAlmostEqual(T.ramificacao_exata(A, f, 3, 3, 4, casa=casa)["acerto"], T.aleatorio_exato(A, f, 3, 3, 4, casa=casa), places=12)

    def test_decisoes_igual_ao_comprimento(self):
        # cada casa do caminho é uma decisão (inclusive a do PARAR) quando a falha é 0
        todas = ["".join(x) for L in (3, 4) for x in itertools.product("ab", repeat=L)]
        r = T.ramificacao_exata(todas, {"A": 0.6, "B": 0.4}, 3, 3, 4)
        e = T.estatisticas_exatas(todas, {"A": 0.6, "B": 0.4}, 3, 3, 4)
        self.assertAlmostEqual(r["falha"], 0.0, places=14)
        self.assertAlmostEqual(r["decisoes"], e["comprimento"], places=12)

    def test_forma_fechada_2x2(self):
        # grade 2x2, uma letra, de 2 a 3 letras: 1a decisão 3 livres e 1 ação (sem PARAR); 2a decisão 2 livres, 1 ação + PARAR (n = 2); com 1/2 a 3a,
        # sem livres e só o PARAR. decisões 1 + 1 + 1/2 = 2,5; opções 1 + 2 + 1/2 = 3,5; livres 3 + 2 = 5; ações 1 + 1 = 2
        r = T.ramificacao_exata(["aa"], {"A": 1.0}, 2, 2, 3)
        self.assertAlmostEqual(r["decisoes"], 2.5, places=14)
        self.assertAlmostEqual(r["opcoes"], 3.5, places=14)
        self.assertAlmostEqual(r["livres"], 5.0, places=14)
        self.assertAlmostEqual(r["acoes"], 2.0, places=14)
        self.assertAlmostEqual(r["acerto"], 0.5, places=14)

    def test_p3216_ramificacao(self):
        r = c.p3216_ramificacao(4, casos=("A'",))
        self.assertLess(r["A'"]["primeira"]["livres"], r["A'"]["uniforme"]["livres"])
        self.assertAlmostEqual(r["A'"]["primeira"]["livres"], 11.415169, places=5)


if __name__ == "__main__":
    unittest.main()
