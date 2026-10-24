"""Testes da Parte 150: synthai/tabuleiro.py e P3204-P3206 pelo nome."""
import unittest

import calculos as c
from synthai import palavras_rl as P
from synthai import tabuleiro as T


class TestesParte150(unittest.TestCase):
    def test_frequencias_de(self):
        f = T.frequencias_de(["ab", "aab"])
        self.assertAlmostEqual(f["A"], 60.0)
        self.assertAlmostEqual(f["B"], 40.0)
        self.assertEqual(f["Z"], 0.01)

    def test_densidade_forma_fechada(self):
        # duas letras com p = 0,6 e 0,4: D("aab", "bba") = 0,6²·0,4 + 0,4²·0,6 = 0,24; "ab" fica fora (2 letras)
        self.assertAlmostEqual(T.densidade(["aab", "bba", "ab"], {"A": 60.0, "B": 40.0}), 0.24, places=14)

    def test_com_frequencias_devolve(self):
        antes = P.LETTER_FREQ
        with T.com_frequencias({"A": 1.0}):
            self.assertEqual(P.LETTER_FREQ, {"A": 1.0})
        self.assertIs(P.LETTER_FREQ, antes)
        try:
            with T.com_frequencias({"B": 1.0}):
                raise ValueError
        except ValueError:
            pass
        self.assertIs(P.LETTER_FREQ, antes)

    def test_p3204_densidades(self):
        d, fpt = c.p3204_densidades()
        self.assertAlmostEqual(d["pt/PT"], 0.10927, places=4)
        self.assertGreater(d["pt/PT"], d["pt/EN"])
        self.assertGreater(fpt["A"], fpt["E"])

    def test_p3205_e_p3206(self):
        r = c.p3205_grpo_tabuleiro(sementes=(101, 102), episodios=500, avaliacao=200)
        self.assertTrue(0.0 <= r["aleat"] <= 1.0)
        m, s, v = c.p3206_aleatorio_tabuleiro("embutido", sementes=(141, 142))
        self.assertEqual(len(v), 2)
        self.assertIs(P.LETTER_FREQ, P.LETTER_FREQ)


if __name__ == "__main__":
    unittest.main()
