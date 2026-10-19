"""Testes de unidade da Parte 119 (o MCCFR com amostragem externa): `python3 -m unittest synthai.testes_parte119`.
Cada pNN e cada função nova pelo nome (Partes 58 e 118), controles dos dois lados (Parte 75)."""

import unittest

import calculos
from synthai import mccfr_externo as M


class TesteExterno(unittest.TestCase):
    def test_uniforme_exato_em_0_1(self):
        g = M.LCGFracao(9)
        us = [g.uniforme() for _ in range(500)]
        self.assertTrue(all(0.0 <= u < 1.0 for u in us))
        self.assertTrue(all((u * 2147483648.0).is_integer() for u in us))   # x/2^31 é exato

    def test_viajante_nao_acumula_media(self):
        # numa travessia, a média só soma onde o ADVERSÁRIO decide: com uma iteração, cada jogador acumulou só nos nós do outro
        c = M.CFRExterno().iterar_externo(1, 4)
        for (carta, h), v in c.soma.items():
            if v != [0.0, 0.0]:
                self.assertAlmostEqual(v[0] + v[1], round(v[0] + v[1]), places=12)   # soma de σ(I) inteiros de visitas

    def test_explorabilidade_externa(self):
        # a calibração do pré-registro: T = 500, semente 1191 deu 0,0477
        self.assertAlmostEqual(M.explorabilidade_externa(500, 1191), 0.0477, places=3)


class TesteParte119(unittest.TestCase):
    def test_p3011_amostragem_externa(self):
        e, q = calculos.p3011_amostragem_externa()
        self.assertTrue(0.0004 <= e <= 0.0213)
        self.assertTrue(0.326 <= q <= 0.384)

    def test_p3012_nos_por_iteracao(self):
        nv, na, ne = calculos.p3012_nos_por_iteracao()
        self.assertEqual(nv, 54.0)                # 6 distribuições × 9 nós
        self.assertEqual(na, 9.0)                 # uma distribuição
        self.assertTrue(na < ne < nv)

    def test_p3013_rodada86(self):
        mr, dif = calculos.p3013_rodada86()
        self.assertEqual(dif, 0)

    def test_p1961_com_parte_119(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[119], (4, 4))
        self.assertEqual((ok, tot), (261, 284))


if __name__ == "__main__":
    unittest.main()
