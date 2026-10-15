"""Testes de unidade da Parte 107 (a inducao reversa; duas ruas): `python3 -m unittest synthai.testes_parte107`."""

import unittest

import calculos
from synthai import duas_ruas


class TesteParte107(unittest.TestCase):
    def test_p2651_rodada74(self):
        v1, v2 = calculos.p2651_rodada74()
        self.assertEqual((v1, v2), (1.0, 3.0))

    def test_p2652_valor_otimo(self):
        self.assertEqual(calculos.p2652_valor_otimo_duas_decisoes(), 3.0)

    def test_p2653_reversa_vs_miope(self):
        rt, rs = calculos.p2653_reversa_vs_miope()
        self.assertAlmostEqual(rt, 1.5, places=12)   # reversa bate o miope
        self.assertAlmostEqual(rs, 1.0, places=12)   # separavel: empatam (controle)

    def test_p2654_segunda_decisao(self):
        a1, a2, dif = calculos.p2654_valor_da_segunda_decisao()
        self.assertEqual((a1, a2, dif), (1.0, 3.0, 2.0))

    def test_p2655_voi(self):
        ve, vi = calculos.p2655_voi_estado_oculto()
        self.assertGreater(ve, 0.0)        # espelho: saber importa
        self.assertEqual(vi, 0.0)          # identico: nao importa (controle)
        self.assertTrue(0.3 <= ve <= 1.2)

    def test_p1961_com_parte_107(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[107], (5, 5))
        self.assertEqual((ok, tot), (125, 141))


if __name__ == "__main__":
    unittest.main()
