"""Testes de unidade da Parte 84 (o delírio e o escrutínio): `python3 -m unittest synthai.testes_parte84`."""

import math
import unittest

import calculos


class TesteParte84(unittest.TestCase):
    def test_p1961_teste_e_da_calibracao(self):
        # controle: um dict sintetico, com a (e) do proprio 84 ignorada (seria circular)
        falso = {80: "(a) ✅ (b) ✅", 81: "(a) ✅ (b) ❌", 83: "(a) ✅", 84: "(a) ✅ (e) ❌ (f) ❌"}
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84), vereditos=falso)
        self.assertEqual(por[84], (1, 2))  # a (e) foi descartada; sobram (a)✅ (f)❌
        self.assertEqual((ok, tot), (5, 7))
        # o valor publicado: as Partes 80, 81, 83, 84 ficaram abaixo de [0,81; 0,99]
        self.assertEqual(calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84))[:2], (23, 31))

    def test_p1962_lyapunov_por_densidade(self):
        lam, razao, uniforme = calculos.p1962_lyapunov_por_densidade(a=0.2, celulas=800, iteracoes=1500)
        self.assertAlmostEqual(uniforme, 0.5 * math.log(1 + 0.2 ** 2 / 4) / (0.2 ** 2 / 8), places=12)
        # a densidade invariante quase uniforme: a razao fica a um fio de 1, NAO acima (fecha a pendencia da P1936)
        self.assertLess(abs(razao - 1), 0.02)
        self.assertLess(razao, 1.005)

    def test_p1963_delirio_e_escrutinio(self):
        g, r, dif, val, emed = calculos.p1963_delirio_e_escrutinio(partidas=60, passos=500)
        self.assertAlmostEqual(dif, r - g)
        self.assertTrue(0 <= g <= 1 and 0 <= r <= 1 and 0 <= val <= 1)
        # controle: o poco largo (i) tem bacia gulosa maior que a agulha (base)
        base = calculos.p1963_delirio_e_escrutinio(partidas=60, passos=500)[0]
        largo = calculos.p1963_delirio_e_escrutinio(partidas=60, passos=500, largura=30)[0]
        self.assertGreater(largo, base)

    def test_p1964_rodada51(self):
        aceitos, soma = calculos.p1964_rodada51()
        self.assertEqual(aceitos, 263)
        # a soma das probabilidades esta entre o numero de pioras aceitas e o total
        self.assertTrue(200 < soma < 280)


if __name__ == "__main__":
    unittest.main()
