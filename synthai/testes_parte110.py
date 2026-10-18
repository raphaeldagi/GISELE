"""Testes de unidade da Parte 110 (a dúvida calculada): `python3 -m unittest synthai.testes_parte110`. Cada peça com o seu caso direto, o seu
inverso e o seu subverso; casos com todos os termos diferentes de zero (regra da Parte 30)."""

import math
import unittest

import calculos
from synthai import duvida


class TesteParte110(unittest.TestCase):
    def test_p2741_duvida_do_gradiente(self):
        ic, ia, melhor, hm, pl = calculos.p2741_duvida_do_gradiente()
        self.assertTrue(1.8 <= ic <= 2.2)
        self.assertTrue(0.9 <= ia <= 1.1)
        self.assertTrue(1e-12 <= melhor <= 1e-8)
        self.assertTrue(1.9 <= pl <= 2.1)   # o controle plantado TEM de ser acusado

    def test_gradiente_caso_limpo(self):
        # controle do outro lado: sem defeito plantado, o verificador passa (erro relativo pequeno no passo bom)
        self.assertLess(duvida.verificar_gradiente(passos=[1e-4])[0][1], 1e-6)

    def test_p2742_duvida_da_inferencia(self):
        c1, c4, cr = calculos.p2742_duvida_da_inferencia()
        self.assertTrue(0.887 <= c1 <= 0.913)
        self.assertTrue(0.53 <= c4 <= 0.65)
        self.assertTrue(3 <= cr <= 5)
        self.assertAlmostEqual(duvida.aglomerado_recuperado(0.90), 1.0, places=9)   # o inverso devolve c = 1 na cobertura nominal

    def test_quantil_beta(self):
        self.assertAlmostEqual(duvida.quantil_beta(0.5, 3, 3), 0.5, places=12)          # simetria
        self.assertAlmostEqual(duvida.quantil_beta(0.25, 1, 1), 0.25, places=12)        # Beta(1,1) = uniforme
        self.assertAlmostEqual(duvida.quantil_beta(0.81, 2, 1), 0.9, places=12)         # Beta(2,1): F(x) = x^2

    def test_p2743_duvida_da_rnn(self):
        el, wr, gt, hT = calculos.p2743_duvida_da_rnn()
        self.assertLessEqual(el, 1e-12)
        self.assertAlmostEqual(wr, 0.9, places=12)
        self.assertTrue(1e-5 <= gt <= 5e-4)     # w > 1 e mesmo assim SOME (saturacao)
        self.assertGreater(1.1 ** 50, 100)      # o que a conta ingenua diria

    def test_p2744_duvida_do_ml(self):
        e, pr, eo = calculos.p2744_duvida_do_ml()
        self.assertTrue(1.23 <= e <= 1.28)
        self.assertTrue(8.5 <= pr <= 11.5)
        self.assertTrue(2.44 <= eo <= 2.58)
        self.assertAlmostEqual(duvida.p_recuperado(1 + 10 / 39), 10.0, places=9)

    def test_p2745_duvida_do_continuo(self):
        g45, tr, o45, n45, b0 = calculos.p2745_duvida_do_continuo()
        self.assertAlmostEqual(g45, 0.5, places=9)
        self.assertAlmostEqual(tr, 45.0, places=6)
        self.assertLess(o45, 1e-30)            # (o) errou a faixa [0; 0]: sobra o residuo da propria tarefa A (1 ulp ao quadrado)
        self.assertAlmostEqual(n45, math.sqrt(2), places=9)
        self.assertEqual(b0, 1.0)
        self.assertAlmostEqual(duvida.continuo(60)[0], 0.25, places=12)

    def test_p2746_duvida_do_reforco(self):
        b2, bd, mr, b10 = calculos.p2746_duvida_do_reforco()
        self.assertTrue(0.175 <= b2 <= 0.182)
        self.assertTrue(-0.004 <= bd <= 0.004)
        self.assertTrue(9 <= mr <= 11)
        self.assertTrue(0.483 <= b10 <= 0.490)

    def test_p2747_rodada77(self):
        e60, n45 = calculos.p2747_rodada77()
        self.assertEqual(e60, 0.25)
        self.assertAlmostEqual(n45, math.sqrt(2), places=12)

    def test_p1961_com_parte_110(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 111))))
        self.assertEqual(por[110], (20, 21))
        self.assertEqual((ok, tot), (158, 176))


if __name__ == "__main__":
    unittest.main()
