"""Testes da Parte 143: as réplicas da Parte 140 (P3195, P3196 pelo nome)."""
import unittest

import calculos as c


class TestesParte143(unittest.TestCase):
    def test_p3195_fluxo_em_portugues(self):
        r, z, met, N, mu = c.p3195_fluxo_em_portugues(k=200, reservatorios=10)
        self.assertEqual(N, 53058)
        self.assertAlmostEqual(mu, 1.7378, places=3)
        self.assertLess(abs(met - 0.5), 0.03)

    def test_p3196_benford16_potencias(self):
        r = c.p3196_benford16_potencias(n=2000)
        self.assertLess(abs(r[2][0] - 3.0), 1e-6)  # √ de um autovalor nulo: tolerância √ε (Parte 143)
        self.assertLess(r[5][1], 0.02)
        self.assertLess(r[7][1], 0.02)


if __name__ == "__main__":
    unittest.main()
