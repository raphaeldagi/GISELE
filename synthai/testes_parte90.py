"""Testes de unidade da Parte 90 (a rede que aprende igual): `python3 -m unittest synthai.testes_parte90`."""

import unittest

import calculos


class TesteParte90(unittest.TestCase):
    def test_p2141_rede_stdp(self):
        total, sw, sw0 = calculos.p2141_rede_stdp()
        self.assertEqual(total, 12)
        self.assertEqual(sw0, 2.6)
        self.assertLess(sw, sw0)   # depressao dominante baixa a soma

    def test_p2142_delta_negativo(self):
        d = calculos.p2142_delta_peso()
        self.assertLess(d, 0.0)            # depressao dominante
        self.assertTrue(-0.03 < d < -0.005)

    def test_p2143_disparos_iguais(self):
        aprendiz, fixo, iguais = calculos.p2143_disparos_aprendiz_vs_fixo()
        self.assertEqual((aprendiz, fixo), (12, 12))
        self.assertTrue(iguais)   # STDP lenta demais para mudar o padrao em 300 passos

    def test_p1961_com_parte_90(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90))
        self.assertEqual(por[90], (3, 3))   # a (d) fica fora da VEREDITOS; a,b,c contam
        self.assertEqual((ok, tot), (45, 57))


if __name__ == "__main__":
    unittest.main()
