"""Testes de unidade da Parte 105 (o blefe; a fronteira medida do seno): `python3 -m unittest synthai.testes_parte105`."""

import unittest

import calculos
from synthai import blefe


class TesteParte105(unittest.TestCase):
    def test_p2591_blefe(self):
        a, asim = calculos.p2591_frequencia_do_blefe()
        self.assertAlmostEqual(a, 1.0 / 3.0, places=12)
        self.assertTrue(0.30 <= asim <= 0.37)

    def test_p2592_pagar(self):
        c, csim = calculos.p2592_frequencia_de_pagar()
        self.assertEqual(c, 0.5)
        self.assertTrue(0.47 <= csim <= 0.53)

    def test_p2593_indiferenca(self):
        ip, ib, plana = calculos.p2593_indiferenca()
        self.assertLess(ip, 1e-9)
        self.assertLess(ib, 1e-9)
        self.assertLess(plana, 1e-9)
        # controle: fora do equilibrio NAO e indiferente (todos os termos != 0, regra da Parte 30)
        self.assertGreater(abs(blefe.ev_blefar(0.9)), 0.5)   # pagador paga demais -> blefar perde

    def test_p2594_fronteira_existe(self):
        # na faixa larga (k/1000) a libm sin NAO e corretamente arredondada -> a 6a face existe (corrige a Parte 104)
        self.assertGreaterEqual(calculos.p2594_fronteira_das_trigonometricas(500), 1)

    def test_p2595_rodada72(self):
        al, c, b, evp, evb = calculos.p2595_rodada72()
        self.assertAlmostEqual(al, 1.0 / 3.0, places=12)
        self.assertEqual(c, 0.5)
        self.assertLess(abs(evp), 1e-9)
        self.assertLess(abs(evb), 1e-9)

    def test_p1961_com_parte_105(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 106))))
        self.assertEqual(por[105], (4, 5))
        self.assertEqual((ok, tot), (115, 131))


if __name__ == "__main__":
    unittest.main()
