"""Testes de unidade da Parte 118 (o MCCFR com o acaso amostrado e o 3º lote do determinante): `python3 -m unittest synthai.testes_parte118`.
Cada pNN pelo nome (Parte 58), controles dos dois lados (Parte 75)."""

import unittest

import calculos
from synthai import mccfr as M


class TesteMCCFR(unittest.TestCase):
    def test_lcg_cobre_as_seis(self):
        g = M.LCG(7)
        vistos = {g.proximo(6) for _ in range(200)}
        self.assertEqual(vistos, set(range(6)))

    def test_uma_iteracao_toca_uma_distribuicao(self):
        c = M.CFRAcaso().iterar_amostrado(1, 3)
        tocados = [k for k, v in c.soma.items() if v != [0.0, 0.0]]
        cartas_p1 = {k[0] for k in tocados if k[1] in ("", "pb")}
        cartas_p2 = {k[0] for k in tocados if k[1] in ("p", "b")}
        self.assertEqual((len(cartas_p1), len(cartas_p2)), (1, 1))   # uma distribuição: uma carta de cada jogador


    def test_explorabilidade_amostrada_calibracao(self):
        # a calibração do pré-registro: T = 600, semente 1181 deu 0,0531
        self.assertAlmostEqual(M.explorabilidade_amostrada(600, 1181), 0.0531, places=3)


class TesteParte118(unittest.TestCase):
    def test_p2981_terceiro_lote(self):
        mu, sd = calculos.p2981_terceiro_lote()
        self.assertTrue(0.4872 <= sd <= 0.4956)
        self.assertTrue(-4.5990 <= mu <= -4.5876)

    def test_p2982_mccfr(self):
        e, q, ev = calculos.p2982_mccfr()
        self.assertTrue(0.0031 <= e <= 0.0105)
        self.assertTrue(0.313 <= q <= 0.354)
        self.assertLess(ev, e)                    # mesmo trabalho: o vanilla (sem ruído de amostragem) explora menos

    def test_p2983_rodada85(self):
        mr, dif = calculos.p2983_rodada85()
        self.assertEqual(dif, 0)
        self.assertEqual(len(mr), 12)

    def test_p2984_rodadas_verificadas(self):
        n, maior = calculos.p2984_rodadas_verificadas()
        self.assertEqual(maior, 85)
        self.assertEqual(n, 85)

    def test_p1961_com_parte_118(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[118], (6, 6))
        self.assertEqual((ok, tot), (257, 280))


if __name__ == "__main__":
    unittest.main()
