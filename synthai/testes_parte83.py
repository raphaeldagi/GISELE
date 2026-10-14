"""Testes de unidade da Parte 83 (a probabilidade da probabilidade): `python3 -m unittest synthai.testes_parte83`."""

import math
import unittest

import calculos


class TesteParte83(unittest.TestCase):
    def test_p1931_gan_de_dirac(self):
        medido, conta = calculos.p1931_gan_de_dirac()
        # o cosseno do ângulo duplo: arccos(1 − a²/2) = 2·arcsen(a/2)
        self.assertAlmostEqual(conta["phi"], conta["phi_angulo_duplo"], places=12)
        # o síncrono cresce todo passo (a norma final é a máxima); o alternado fica na elipse; as contas fechadas a menos de 0,1%
        self.assertEqual(medido["sincrono"][0], medido["sincrono"][1])
        self.assertLess(abs(medido["sincrono"][0] / conta["sincrono_final"] - 1), 1e-3)
        self.assertLess(abs(medido["alternado"][1] / conta["alternado_maximo"] - 1), 1e-3)
        self.assertEqual(medido["alternado"][2], conta["trocas"])

    def test_p1932_jogo_assincrono(self):
        (m, dp, menores, ln_s, ln_a), conta = calculos.p1932_jogo_assincrono(passos=2000, corridas=40, semente0=7)
        # o síncrono é determinístico e bate com a conta exata; o alternado não cresce; o assíncrono fica entre os dois
        self.assertAlmostEqual(ln_s, 0.5 * 2000 * math.log(1 + 0.05 ** 2), places=9)
        self.assertLess(abs(ln_a), 0.05)
        self.assertLess(ln_a, m)
        self.assertLess(m, ln_s)
        self.assertAlmostEqual(conta["assincrono"], 2000 * 0.0025 / 8)

    def test_p1933_calibracao_composta(self):
        conta, sim, composta, uma, sete = calculos.p1933_calibracao_composta(sorteios=20000)
        # compor h_k sete vezes é h_{k^7} (grupo de escalas): a composição numérica bate com a forma fechada
        self.assertAlmostEqual(composta, conta, places=9)
        self.assertLess(abs(sim - conta), 0.01)
        # controle: k = 1 é idempotente (a calibração perfeita é o único ponto fixo)
        c1 = calculos.p1933_calibracao_composta(k=1.0, sorteios=1000)
        self.assertAlmostEqual(c1[0], 0.9, places=6)
        self.assertAlmostEqual(c1[2], 0.9, places=6)
        self.assertAlmostEqual(uma, 0.9747, places=4)

    def test_p1934_torre_de_placares(self):
        torre, fora = calculos.p1934_torre_de_placares(range(67, 70))
        self.assertEqual(torre[2], (17, 21))
        self.assertEqual(torre[3], (11, 15))
        # controle: uma parte sem a linha (72) fica de fora
        self.assertEqual(calculos.p1934_torre_de_placares(range(72, 73))[1], [72])

    def test_p1935_sete_camadas_recebido(self):
        r = calculos.p1935_sete_camadas_recebido()
        if r is None:
            self.skipTest("NumPy ausente: o módulo recebido não roda")
        self.assertTrue(r["modos_identicos"])
        self.assertEqual(round(r["logistica_adversa"], 6), round(r["rede_adversa"], 6))

    def test_p1936_lyapunov_assincrono(self):
        lam, razao, uniforme = calculos.p1936_lyapunov_assincrono(a=0.2, passos=200000, semente=1)
        self.assertAlmostEqual(uniforme, 0.5 * math.log(1.01) / 0.005, places=12)
        self.assertLess(abs(razao - 1), 0.05)


if __name__ == "__main__":
    unittest.main()
