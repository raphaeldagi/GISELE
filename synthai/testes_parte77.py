"""Testes de unidade da Parte 77 (as duas abertas): `python3 -m unittest synthai.testes_parte77`."""

import unittest

import calculos


class TesteParte77(unittest.TestCase):
    def test_p1751_rodada09_nova_contra_antiga(self):
        n, mud, rel = calculos.p1751_rodada09_nova_contra_antiga()
        self.assertEqual((n, mud), (13, 6))
        self.assertTrue(0.0 < rel < 1e-12)

    def test_fronteira_fechada(self):
        # nenhuma rodada usa exp/log da biblioteca fora da preparação (a 48 só prepara dados que o Java lê)
        r = calculos.p1722_libm_nas_duas_linguagens()
        self.assertTrue(all(prep is True and not java for _, prep, java in r.values()))


if __name__ == "__main__":
    unittest.main()
