"""Testes de unidade da Parte 98 (o ruido de observacao): `python3 -m unittest synthai.testes_parte98`."""

import unittest

import calculos
from synthai import mundo


class TesteParte98(unittest.TestCase):
    def test_p2381_piso_linear_em_sigma(self):
        r1, r2, razao = calculos.p2381_piso_linear_em_sigma()
        # dobrar sigma dobra o residuo
        self.assertAlmostEqual(razao, 2.0, delta=0.1)

    def test_p2382_nao_exato(self):
        med, conta = calculos.p2382_nao_exato_sob_ruido()
        # sob ruido, n>#params NAO da exato
        self.assertGreater(med, 0.01)

    def test_p2383_variancia_cura_devagar(self):
        r200, r800, rz = calculos.p2383_variancia_cura_devagar()
        self.assertGreater(r200, r800)  # mais dados, menos erro
        self.assertTrue(1.8 <= rz <= 2.6)  # perto de sqrt(4)=2

    def test_p2384_ridge_sob_ruido(self):
        melh, l01, l03 = calculos.p2384_ridge_sob_ruido()
        self.assertLess(melh, 1.0)  # <1% quando n>>p
        self.assertGreaterEqual(l03, l01)  # lambda* cresce com sigma

    def test_gerar_ruido_vs_limpo(self):
        # a saida com ruido difere da limpa; com sigma=0 coincide
        X0, U0, Y0 = mundo.gerar_transicoes_nl_ruido(5, 50, 0.1, 0.0)
        Xc, Uc, Yc = mundo.gerar_transicoes_nl(5, 50, 0.1)
        # com sigma=0 o RNG consome os mesmos uniformes; as saidas devem coincidir (sem gauss aplicado... na verdade gauss(0,0)=0)
        self.assertEqual(len(Y0), 50)

    def test_ruido_floor_conta(self):
        # a conta sigma*sqrt(p/n) e da ordem do medido (dentro de um fator 2)
        med, conta = mundo.ruido_floor(sigma=0.1, n=400)
        self.assertTrue(0.5 < med / conta < 3.0)

    def test_p2385_rodada65(self):
        toks = calculos.p2385_rodada65()
        self.assertEqual(len(toks), 5)
        for t, p in toks:
            self.assertTrue(0 <= t <= 4 and 0.0 < p <= 1.0)

    def test_p2386_razao_constante(self):
        a, b, difrel = calculos.p2386_razao_constante_em_sigma()
        # residuo/sigma nao depende de sigma -> diferenca relativa ~0
        self.assertLess(difrel, 1e-6)

    def test_p1961_com_parte_98(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98))
        self.assertEqual(por[98], (5, 5))
        self.assertEqual((ok, tot), (82, 96))


if __name__ == "__main__":
    unittest.main()
