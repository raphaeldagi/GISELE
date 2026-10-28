"""Testes da Parte 158: o expoente pelas frequências (synthai/zipf_frequencias.py) e a P3219 pelo nome."""
import math
import unittest

import calculos as c
from synthai import zipf_frequencias as F


class TestesParte158(unittest.TestCase):
    def test_zeta_de_riemann(self):
        self.assertAlmostEqual(F._zeta_e_dlog(2.0, 1)[0], math.pi ** 2 / 6, places=12)
        self.assertAlmostEqual(F._zeta_e_dlog(4.0, 1)[0], math.pi ** 4 / 90, places=12)

    def test_derivada_do_zeta(self):
        # Σ k^-a ln k = −dζ/da: confere por diferença finita centrada
        a, h = 2.5, 1e-5
        dz = (F._zeta_e_dlog(a + h, 3)[0] - F._zeta_e_dlog(a - h, 3)[0]) / (2 * h)
        self.assertAlmostEqual(F._zeta_e_dlog(a, 3)[1], -dz, places=7)

    def test_escore_zera_no_alfa(self):
        xs = [1, 1, 1, 2, 2, 3, 5, 8, 13, 40]
        a = F.alfa_mle(xs, 1)
        alvo = sum(math.log(x) for x in xs) / len(xs)
        self.assertAlmostEqual(F.media_log_esperada(a, 1), alvo, places=8)

    def test_s_de_alfa(self):
        self.assertAlmostEqual(F.s_de_alfa(2.0), 1.0, places=14)
        self.assertAlmostEqual(F.s_de_alfa(1 + 1 / 1.5), 1.5, places=12)

    def test_p3219_zipf_pelas_frequencias(self):
        r = c.p3219_zipf_pelas_frequencias(casos=(("B", 1.5, 5000, (2,)),), sementes=range(100, 103))
        self.assertLess(r[("B", 2)][0], -0.05)


if __name__ == "__main__":
    unittest.main()
