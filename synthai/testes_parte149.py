"""Testes da Parte 149: lemas_ownpt, P3201 (a GRPO por dicionário), P3202 (o aleatório) e P3203 (a auditoria com o t) pelo nome."""
import unittest

import calculos as c
from synthai import palavras_rl as P


class TestesParte149(unittest.TestCase):
    def test_lemas_ownpt_sem_acentos(self):
        s = P.lemas_ownpt()
        self.assertEqual(len(s), 34384)
        self.assertIn("coracao", s)
        self.assertTrue(all(w.isascii() and w.isalpha() and w == w.lower() for w in s))

    def test_p3201_grpo_por_dicionario(self):
        r = c.p3201_grpo_por_dicionario("pt", sementes=(101, 102), episodios=1000, avaliacao=200)
        self.assertTrue(0.0 <= r["sem8"] <= r["sem2"] <= 1.0)
        self.assertAlmostEqual(r["G2-Q"], r["G2"] - r["Q"], places=12)

    def test_p3202_aleatorio_igual_ao_avaliador(self):
        # o braço aleatório isolado dá o mesmo número que o avaliador da Parte 111 nas mesmas sementes
        m, _, v = c.p3202_aleatorio_por_dicionario("embutido", sementes=(43, 44, 45))
        e = c.p3201_grpo_por_dicionario("embutido", sementes=(43, 44, 45), episodios=200, avaliacao=1000)
        self.assertEqual(v, e["por_semente"]["aleat"])

    def test_p3203_auditoria_t(self):
        out, n = c.p3203_auditoria_t()
        self.assertEqual(n, 1)
        # controle: com n_cal enorme, t -> 1,645 e nenhuma faixa muda de veredito
        out2, n2 = c.p3203_auditoria_t(((1, "x", 0.0, 1.0, 5000, 1.02),))
        self.assertEqual(n2, 0)


if __name__ == "__main__":
    unittest.main()
