"""Testes de unidade da Parte 97 (a cura da variancia e o bloco inteiro): `python3 -m unittest synthai.testes_parte97`."""

import unittest

import calculos
from synthai import mundo


class TesteParte97(unittest.TestCase):
    def test_p2351_ridge_u(self):
        ls, rt, interior = calculos.p2351_ridge_faz_u()
        self.assertTrue(interior)  # o melhor lambda e interior (curva em U)
        self.assertGreater(ls, 0.0)

    def test_ridge_sweep_forma_u(self):
        # o teste piora para lambda=0 (overfit) e para lambda grande (subfit); o melhor esta no meio
        linha, (ls, rt) = mundo.ridge_sweep(grau=5, n=40, lams=(0.0, 1.0, 10.0))
        por_lam = {lam: te for lam, _, te in linha}
        self.assertLess(por_lam[1.0], por_lam[0.0])
        self.assertLess(por_lam[1.0], por_lam[10.0])

    def test_p2352_mitiga_nao_cura(self):
        best, rlin = calculos.p2352_ridge_mitiga_nao_cura()
        # o melhor ridge ainda perde para o modelo linear simples (n pequeno)
        self.assertGreater(best, rlin)
        self.assertLess(rlin, 0.2)

    def test_p2353_mlp_capacidade(self):
        cap, nao_cresce, razao = calculos.p2353_mlp_capacidade()
        self.assertTrue(nao_cresce)
        self.assertLess(razao, 0.5)

    def test_p2354_rodada64(self):
        arg, logits = calculos.p2354_rodada64()
        self.assertIn(arg, (0, 1))
        self.assertEqual(len(logits), 2)

    def test_p2355_dados_curam(self):
        l40, l160, r160 = calculos.p2355_dados_curam_variancia()
        # mais dados -> menos regularizacao precisa, e o teste despenca
        self.assertGreater(l40, l160)
        self.assertLess(r160, 1e-3)

    def test_p2356_limiar(self):
        npar, rlim = calculos.p2356_limiar_de_parametros(grau=5)
        self.assertEqual(npar, 56)  # C(5+3,3) = 56
        self.assertLess(rlim, 1e-6)  # n acima do limiar, lambda~0 -> exato

    def test_ridge_lambda_zero_vs_grande(self):
        # caso de controle: ridge com lambda enorme encolhe os pesos para perto de zero
        X, U, Y = mundo.gerar_transicoes_nl(0, 100, 0.1)
        th = mundo.ajustar_features_ridge(X, U, Y, mundo.monomios(2), 1e9)
        self.assertLess(max(abs(c) for c in th[0]), 0.1)

    def test_p1961_com_parte_97(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[97], (4, 5))
        self.assertEqual((ok, tot), (77, 91))


if __name__ == "__main__":
    unittest.main()
