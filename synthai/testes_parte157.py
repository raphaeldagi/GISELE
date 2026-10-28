"""Testes da Parte 157: o expoente de Zipf por máxima verossimilhança (synthai/zipf_mle.py) e a P3217/P3218 pelo nome."""
import math
import unittest

import calculos as c
from synthai import zipf_mle as Z


class TestesParte157(unittest.TestCase):
    def test_escore_zera_no_mle(self):
        # no s de máxima verossimilhança, a média observada de ln r iguala a esperada
        cont = Z.amostrar(1.3, 200, 3000, 1)
        s = Z.mle(cont)
        n = sum(cont)
        alvo = sum(k * math.log(r) for r, k in enumerate(cont, start=1)) / n
        self.assertAlmostEqual(Z.media_log_esperada(200, s), alvo, places=8)

    def test_contagens_proporcionais_dao_o_s_exato(self):
        # contagens exatamente proporcionais a r^-s (sem ruído) devolvem s
        cont = [1e6 * r ** -1.7 for r in range(1, 101)]
        self.assertAlmostEqual(Z.mle(cont), 1.7, places=8)
        self.assertAlmostEqual(Z.ols_loglog(cont), 1.7, places=10)

    def test_harmonico(self):
        self.assertAlmostEqual(Z.harmonico(4, 1.0), 1 + 1 / 2 + 1 / 3 + 1 / 4, places=14)
        self.assertAlmostEqual(Z.harmonico(3, 2.0), 1 + 1 / 4 + 1 / 9, places=14)

    def test_empiricas_ordena_e_tira_zeros(self):
        self.assertEqual(Z.empiricas([0, 3, 1, 0, 5]), [5, 3, 1])

    def test_p3217_zipf_mle_contra_ols(self):
        r = c.p3217_zipf_mle_contra_ols(casos=(("B", 1.5, 5000),), sementes=range(100, 103))
        self.assertLess(r["B"]["ols"][0], -0.2)
        self.assertLess(abs(r["B"]["verd"][0]), 0.03)

    def test_p3218_lote_novo_de_a(self):
        v, e, o, r = c.p3218_lote_novo_de_a(sementes=range(200, 204))
        self.assertLess(e, 0.0)
        self.assertGreater(r, 0.5)


if __name__ == "__main__":
    unittest.main()
