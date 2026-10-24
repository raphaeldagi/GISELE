"""Testes da Parte 148: a P3199 (a GRPO no dicionário grande), a P3200 (os lotes do Q-learning) e o quantil t pelo nome."""
import unittest

import calculos as c


class TestesParte148(unittest.TestCase):
    def test_p3200_t_student_quantil(self):
        # tabela: t(0,95; 7) = 1,8946; t(0,95; 30) = 1,6973; com muitos graus tende a 1,6449
        self.assertAlmostEqual(c.p3200_t_student_quantil(7), 1.8946, places=3)
        self.assertAlmostEqual(c.p3200_t_student_quantil(30), 1.6973, places=3)
        self.assertAlmostEqual(c.p3200_t_student_quantil(2000), 1.6456, places=2)

    def test_p3200_chi2_cdf(self):
        # gl = 4: CDF(x) = 1 − e^{−x/2}(1 + x/2), forma fechada com todos os termos diferentes de zero
        import math
        x = 3.0
        self.assertAlmostEqual(c.p3200_chi2_cdf(4, x), 1 - math.exp(-x / 2) * (1 + x / 2), places=6)

    def test_p3199_grpo_no_dicionario_grande(self):
        r = c.p3199_grpo_no_dicionario_grande(sementes=(61, 62), episodios=1000, avaliacao=200)
        self.assertEqual(set(r) >= {"Q", "G2", "G8", "sem2", "sem8", "ambas"}, True)
        self.assertTrue(0.0 <= r["sem8"] <= r["sem2"] <= 1.0)  # grupos maiores têm contraste mais vezes

    def test_p3200_lotes_do_q(self):
        r = c.p3200_lotes_do_q(lotes=((5, 13), (61, 63), (71, 73), (13, 15), (23, 25), (1001, 1003)))
        self.assertAlmostEqual(r["sigma_cal"], 0.01601, places=4)
        self.assertEqual(r["todas"][0], 18)
        self.assertGreater(r["meia_t"], 0.0)
        self.assertTrue(0.0 < r["p_sigma_baixo"] < 1.0)


if __name__ == "__main__":
    unittest.main()
