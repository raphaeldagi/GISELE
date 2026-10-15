"""Testes de unidade da Parte 108 (o minimax; jogo de soma zero): `python3 -m unittest synthai.testes_parte108`."""

import unittest

import calculos
from synthai import minimax


class TesteParte108(unittest.TestCase):
    def test_p2681_rodada75(self):
        v, p, q = calculos.p2681_rodada75()
        self.assertAlmostEqual(v, 1.0 / 7.0, places=12)
        self.assertAlmostEqual(p, 5.0 / 7.0, places=12)

    def test_p2682_von_neumann(self):
        mm, nm, dif = calculos.p2682_von_neumann()
        self.assertLess(dif, 1e-12)

    def test_p2683_valor_estrategia(self):
        v, p = calculos.p2683_valor_e_estrategia()
        self.assertAlmostEqual(v, 1.0 / 7.0, places=12)
        self.assertAlmostEqual(p, 5.0 / 7.0, places=12)
        # controle: todos os termos != 0 (regra da Parte 30); q tambem fechado
        self.assertAlmostEqual(minimax.estrategia_coluna_2x2(minimax.JOGO_TESTE), 4.0 / 7.0, places=12)

    def test_p2684_jogo_ficticio(self):
        vf, err = calculos.p2684_jogo_ficticio()
        self.assertLess(err, 0.02)

    def test_p2685_ponto_de_sela(self):
        vs, ps = calculos.p2685_ponto_de_sela()
        self.assertEqual(vs, 1.0)       # valor exato
        self.assertEqual(ps, 1.0)       # estrategia pura (controle)
        self.assertIsNotNone(minimax.tem_sela(minimax.JOGO_SELA))
        self.assertIsNone(minimax.tem_sela(minimax.JOGO_TESTE))

    def test_p1961_com_parte_108(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[108], (5, 5))
        self.assertEqual((ok, tot), (130, 146))


if __name__ == "__main__":
    unittest.main()
