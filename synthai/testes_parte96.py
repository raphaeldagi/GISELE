"""Testes de unidade da Parte 96 (aprender a base): `python3 -m unittest synthai.testes_parte96`."""

import unittest

import calculos
from synthai import mundo


class TesteParte96(unittest.TestCase):
    def test_p2321_grau2_nao_ajuda(self):
        r1, r2, dif = calculos.p2321_grau2_nao_ajuda()
        # a base de grau 2 nao reduz o vies (falta s1^3, grau 3)
        self.assertGreater(r1, 0.05)
        self.assertLess(dif, 0.01)

    def test_p2322_grau3_recupera(self):
        self.assertLess(calculos.p2322_grau3_recupera(), 1e-10)

    def test_monomios_conta(self):
        # numero de monomios ate grau g em 3 variaveis = C(g+3,3)
        self.assertEqual(mundo.monomios(1).m, 4)
        self.assertEqual(mundo.monomios(2).m, 10)
        self.assertEqual(mundo.monomios(3).m, 20)

    def test_p2323_mlp_entre(self):
        rtr, rte = calculos.p2323_mlp_aprende_a_base()
        # as features aprendidas ficam entre a linear (~0,12) e a cubica dada (~0)
        self.assertLess(rte, 0.12)
        self.assertGreater(rte, 1e-6)

    def test_p2324_overfit(self):
        otr, ote = calculos.p2324_overfit_base_rica()
        # base rica + poucos dados: treino ~0, teste grande
        self.assertLess(otr, 1e-6)
        self.assertGreater(ote, 0.3)

    def test_mlp_reduz_perda(self):
        # o MLP treinado tem residuo menor que um nao treinado (o gradiente desce)
        Xtr, Utr, Ytr = mundo.gerar_transicoes_nl(0, 200, 0.1)
        m0 = mundo.MLP1(h=6, semente=1)
        r0 = m0.residuo(Xtr, Utr, Ytr)
        m0.treinar(Xtr, Utr, Ytr, passos=3000, lr=0.02, semente=1)
        self.assertLess(m0.residuo(Xtr, Utr, Ytr), r0)

    def test_p2325_rodada63(self):
        out = calculos.p2325_rodada63()
        self.assertEqual(len(out), 4)

    def test_p2326_menor_grau(self):
        menor, res = calculos.p2326_menor_grau_exato()
        self.assertEqual(menor, 3)
        self.assertGreater(res[1], 0.05)
        self.assertLess(res[3], 1e-8)

    def test_p1961_com_parte_96(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[96], (5, 5))
        self.assertEqual((ok, tot), (73, 86))


if __name__ == "__main__":
    unittest.main()
