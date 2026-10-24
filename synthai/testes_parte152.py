"""Testes da Parte 152: o colapso das vizinhas de mesma letra (synthai/tabuleiro.py) e a P3209 pelo nome."""
import itertools
import math
import unittest

import calculos as c
from synthai import tabuleiro as T


class TestesParte152(unittest.TestCase):
    def test_distintas_forma_fechada(self):
        # duas letras com p = 0,7 e 0,3, n = 2: K = 1 com 0,7² + 0,3² = 0,58; K = 2 com 2·0,7·0,3 = 0,42
        dist, comc = T._distintas([0.7, 0.3], 2)
        self.assertAlmostEqual(dist[1], 0.58, places=14)
        self.assertAlmostEqual(dist[2], 0.42, places=14)
        # a 1ª letra presente e K = 1: só "AA", 0,49
        self.assertAlmostEqual(comc[0][1], 0.49, places=14)

    def test_tabela_fecha_em_um(self):
        tab = T.tabela_colapso({"A": 3.0, "B": 2.0, "C": 1.0})
        for n in range(1, 9):
            parar, com, sem = tab[n]
            self.assertAlmostEqual(parar + sum(com.values()), 1.0, places=12)
            self.assertAlmostEqual(sum(sem.values()), 1.0, places=12)

    def test_sem_colapso_com_letras_raras(self):
        # 26 letras uniformes e n = 1: P(parar) = 1/2 exato (K = 1 sempre)
        tab = T.tabela_colapso({chr(65 + i): 1.0 for i in range(26)})
        self.assertAlmostEqual(tab[1][0], 0.5, places=14)

    def test_aleatorio_colapso_controle_total(self):
        f = {"A": 1.0, "B": 1.0}
        todas = ["".join(x) for L in (3, 4, 5) for x in itertools.product("ab", repeat=L)]
        self.assertAlmostEqual(T.aleatorio_colapso(todas, f), 1.0, places=12)

    def test_p3209_aleatorio_colapso(self):
        m, s, g, k = c.p3209_aleatorio_colapso("embutido", "en", 5, 3, 5, sementes=(181, 182), avaliacao=300)
        self.assertTrue(0.0 <= m <= 1.0)
        self.assertGreater(k, g * 0.95)
        self.assertTrue(math.isfinite(k))


if __name__ == "__main__":
    unittest.main()
