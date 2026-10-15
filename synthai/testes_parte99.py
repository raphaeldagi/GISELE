"""Testes de unidade da Parte 99 (a amostragem e o fecho do modelo de mundo): `python3 -m unittest synthai.testes_parte99`."""

import math
import unittest

import calculos
from synthai import evoluido


class TesteParte99(unittest.TestCase):
    def test_p2411_entropia_cresce(self):
        hs, cresce = calculos.p2411_entropia_cresce_com_T()
        self.assertTrue(cresce)
        self.assertTrue(hs[0] < hs[1] < hs[2])

    def test_entropia_limites(self):
        # uniforme tem entropia ln V; um pico tem entropia ~0
        V = 5
        unif = [1.0 / V] * V
        self.assertAlmostEqual(evoluido.entropia_shannon(unif), math.log(V), places=10)
        pico = [1.0, 0.0, 0.0, 0.0, 0.0]
        self.assertAlmostEqual(evoluido.entropia_shannon(pico), 0.0, places=10)

    def test_p2412_argmax(self):
        todos, arg, top1 = calculos.p2412_T_zero_vira_argmax()
        self.assertTrue(todos)
        self.assertEqual(arg, 0)
        self.assertGreater(top1, 0.999)

    def test_p2413_top_k(self):
        full, tk, levantou = calculos.p2413_top_k_levanta_massa()
        self.assertTrue(levantou)
        self.assertGreater(tk, full)

    def test_top_k_soma_um(self):
        p = evoluido.softmax_temperatura([1.0, 2.0, 3.0, 0.5], 1.0)
        pk = evoluido.top_k_renormalizado(p, 2)
        self.assertAlmostEqual(sum(pk), 1.0, places=12)
        self.assertEqual(sum(1 for x in pk if x > 0), 2)

    def test_p2414_piso_ruidoso(self):
        rr, rl, s2 = calculos.p2414_piso_teste_ruidoso()
        # o piso ruidoso ~ sqrt(2)*sigma e maior que o limpo
        self.assertTrue(0.13 <= rr <= 0.15)
        self.assertGreater(rr, rl)
        self.assertAlmostEqual(rr, s2, delta=0.01)

    def test_p2415_rodada66(self):
        casos = calculos.p2415_rodada66()
        self.assertEqual(len(casos), 5)
        for tok, top1, h in casos:
            self.assertTrue(0 <= tok <= 4 and 0.0 < top1 <= 1.0 and h >= 0.0)

    def test_p2416_retrospecto(self):
        retro = calculos.p2416_retrospecto_modelo_mundo()
        # os tres pisos: forma ~0,12, dados ~0,6 (overfit), ruido sqrt(2)*0,1
        self.assertTrue(0.08 < retro["forma"] < 0.16)
        self.assertGreater(retro["dados"], 0.3)
        self.assertAlmostEqual(retro["ruido"], math.sqrt(2) * 0.1, places=6)

    def test_p1961_com_parte_99(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 100))))
        self.assertEqual(por[99], (5, 5))
        self.assertEqual((ok, tot), (87, 101))


if __name__ == "__main__":
    unittest.main()
