"""Testes de unidade da Parte 106 (a segunda rua; a reducao de argumento): `python3 -m unittest synthai.testes_parte106`."""

import unittest

import calculos
from synthai import jogo_cartas


class TesteParte106(unittest.TestCase):
    def test_p2621_rodada73(self):
        sn, cs = calculos.p2621_rodada73(0.0)
        self.assertAlmostEqual(sn, 0.0, places=15)
        self.assertAlmostEqual(cs, 1.0, places=15)

    def test_p2622_exatidao(self):
        self.assertLess(calculos.p2622_exatidao_sin_proprio(500), 1e-12)

    def test_p2623_reducao(self):
        d3, d9 = calculos.p2623_reducao_duas_partes()
        self.assertLess(d3, 1e-12)   # 1-parte e 2-partes concordam em x pequeno
        self.assertGreater(d9, 1e-9)  # divergem em x grande (a 2a parte importa)

    def test_p2624_voi_duas_ruas(self):
        frac, fechada = calculos.p2624_voi_duas_ruas()
        self.assertAlmostEqual(fechada, 1 - (7.0 / 13.0) ** 2, places=12)
        self.assertTrue(0.69 <= frac <= 0.73)
        # controle: uma rua so da ~6/13 (todos os termos != 0, regra da Parte 30)
        self.assertTrue(0.44 <= jogo_cartas.fracao_info_muda(20000, 106) <= 0.48)

    def test_p2625_subaditividade(self):
        dobro, duas, dif = calculos.p2625_subaditividade_voi()
        self.assertGreater(dobro, duas)     # sub-aditivo
        self.assertTrue(0.18 <= dif <= 0.25)

    def test_p1961_com_parte_106(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[106], (5, 5))
        self.assertEqual((ok, tot), (120, 136))


if __name__ == "__main__":
    unittest.main()
