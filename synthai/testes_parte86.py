"""Testes de unidade da Parte 86 (o cérebro na CPU): `python3 -m unittest synthai.testes_parte86`."""

import math
import unittest

import calculos
from synthai.pulsado import NeuronioLIF, NeuronioIzhikevich, stdp_delta, stdp_liquido, sobreposicao


class TesteParte86(unittest.TestCase):
    def test_p2021_lif_ponto_fixo(self):
        erro, previsto = calculos.p2021_lif_ponto_fixo()
        # o erro NAO e ~0: e gap*beta^200; a conta prevê o erro medido
        self.assertAlmostEqual(erro, previsto, places=12)
        self.assertGreater(erro, 1e-9)  # a minha previsao [0;1e-9] errou: o prefator conta
        # controle: o ponto fixo analitico e exato
        lif = NeuronioLIF(limiar=1e9)
        self.assertEqual(lif.ponto_fixo(20.0), -65.0 + 20.0)

    def test_p2022_izhikevich_tipos(self):
        rs, ch = calculos.p2022_izhikevich_tipos()
        self.assertEqual((rs, ch), (22, 73))
        self.assertGreater(ch, rs)
        # controle: um neuronio sem corrente nao dispara
        self.assertEqual(calculos.p2022_izhikevich_tipos(i_ext=0.0)[0], 0)

    def test_p2023_memoria(self):
        mb, gb, total, inc = calculos.p2023_memoria_relatorio()
        self.assertEqual((mb, gb, total), (32.0, 6.0, 6.032))
        self.assertTrue(inc["padded_csr"][2] and inc["htm"][2])

    def test_p2024_gsops(self):
        self.assertEqual(calculos.p2024_gsops(), (10000, 10000000, 10.0))

    def test_p2025_sdr(self):
        media, teorico = calculos.p2025_sdr_sobreposicao(pares=2000)
        self.assertAlmostEqual(teorico, 40 * 40 / 2048)
        self.assertLess(abs(media - teorico), 0.15)
        # controle: duas SDRs iguais tem sobreposicao k
        self.assertEqual(sobreposicao({1, 2, 3}, {1, 2, 3}), 3)

    def test_p2026_stdp(self):
        sim, assim = calculos.p2026_stdp_liquido()
        self.assertEqual(sim, 0.0)       # A+=A-, tau+=tau-: as areas se cancelam
        self.assertLess(assim, 0.0)      # A- maior: estabilizadora
        # controle: pre antes de post (dt>0) potencia; dt<0 deprime
        self.assertGreater(stdp_delta(5.0), 0)
        self.assertLess(stdp_delta(-5.0), 0)

    def test_p1961_com_parte_86(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86))
        self.assertEqual(por[86], (5, 6))  # a (g) descartada; a,b,c,d,e,f com a❌
        self.assertEqual((ok, tot), (32, 41))

    def test_p2027_rodada53(self):
        v, u, disparos = calculos.p2027_rodada53()
        self.assertEqual(disparos, 5)


if __name__ == "__main__":
    unittest.main()
