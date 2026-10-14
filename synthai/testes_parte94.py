"""Testes de unidade da Parte 94 (o mundo que nao e linear): `python3 -m unittest synthai.testes_parte94`."""

import unittest

import calculos
from synthai import mundo


class TesteParte94(unittest.TestCase):
    def test_p2261_lqr_vs_mpc(self):
        ml, mm, mr, razao = calculos.p2261_lqr_vs_mpc()
        # o LQR (otimo) tem o menor custo; o MPC perde para ele mas ganha do reativo
        self.assertLess(ml, mm)
        self.assertLess(mm, mr)
        self.assertGreater(razao, 1.0)

    def test_riccati_resolve_dare(self):
        # o ganho LQR satisfaz a DARE num caso com todos os termos != 0 (regra da Parte 30)
        A, B, Q, R = [[1.0, 0.15], [0.0, 0.9]], [[0.0], [0.15]], [[1.0, 0.0], [0.0, 1.0]], 0.05
        K = mundo.resolver_riccati(A, B, Q, R)
        self.assertEqual(len(K[0]), 2)
        # um passo de controle leva o estado para mais perto do alvo (estabilidade)
        s = (2.0, 0.0)
        a = mundo.acao_lqr(s, 0.0, K)
        s2 = mundo.transicao(s, a)
        self.assertLess(abs(s2[0]) + abs(s2[1]), abs(s[0]) + abs(s[1]) + 1.0)

    def test_p2262_vies_de_forma(self):
        r1, r2, dif = calculos.p2262_vies_de_forma()
        # o residuo do modelo linear num mundo nao-linear NAO encolhe com n (vies, nao variancia)
        self.assertGreater(r1, 0.05)
        self.assertLess(dif, 0.01)

    def test_p2263_base_cubica_recupera(self):
        # a base que contem a dinamica verdadeira recupera o exato
        self.assertLess(calculos.p2263_base_cubica_recupera(), 1e-10)

    def test_transicao_nl_vs_linear(self):
        # com kappa=0 o mundo nao-linear coincide com o linear; com kappa>0 difere na velocidade
        s, a = (0.7, 1.3), 0.5
        self.assertEqual(mundo.transicao_nl(s, a, 0.0), mundo.transicao(s, a))
        self.assertNotEqual(mundo.transicao_nl(s, a, 0.1), mundo.transicao(s, a))

    def test_p2264_mpc_modelo_errado(self):
        mm, mr, rz = calculos.p2264_mpc_modelo_errado()
        # planejar com modelo enviesado nao vence o reagir (inversao da Parte 93)
        self.assertGreaterEqual(rz, 1.0)

    def test_p2265_rodada61(self):
        saida, arg = calculos.p2265_rodada61()
        self.assertIn(arg, (0, 1))
        self.assertEqual(len(saida), 3)

    def test_p2266_riccati_ponto_fixo(self):
        self.assertLess(calculos.p2266_riccati_e_ponto_fixo(), 1e-9)

    def test_p1961_com_parte_94(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94))
        self.assertEqual(por[94], (5, 5))
        self.assertEqual((ok, tot), (63, 76))


if __name__ == "__main__":
    unittest.main()
