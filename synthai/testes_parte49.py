"""Testes de unidade da Parte 49: `python3 -m unittest synthai.testes_parte49`."""

import math
import os
import tempfile
import unittest

import calculos
from .testes_parte48 import DicionarioFalso


class TesteParte49(unittest.TestCase):
    def test_funis(self):
        # mapa: a -> b, b -> c, c -> b, e -> a, d -> nada; graus: b 2 (a, c), a 1, c 1; as 10 mais: 4 de 5 palavras
        top, g, frac, incl, dez = calculos.p912_funis(DicionarioFalso())
        self.assertEqual((top, g, dez), ("b", 2, [("b", 2), ("a", 1), ("c", 1)]))
        self.assertAlmostEqual(frac, 0.8, places=12)
        self.assertTrue(math.isnan(incl))  # um ponto só (k = 2): sem inclinação

    def test_benford_hex(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "r.txt")
            # P12 sai; 1,5 -> 1; 32 = 0x20 -> 2; 0,0625 = 1/16 -> 1; 255 = 0xFF -> F; 0 é ignorado
            open(p, "w").write("P12 x = 1.5; y = 32; z = 0.0625; w = 255; zero = 0\n")
            f1, f8, n, fr = calculos.p913_benford_hex(p)
        self.assertEqual(n, 4)
        self.assertAlmostEqual(f1, 0.5, places=12)
        self.assertAlmostEqual(f8, 0.25, places=12)
        self.assertAlmostEqual(fr[1], 0.25, places=12)

    def test_reta_da_rodada_22(self):
        import importlib.util
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        spec = importlib.util.spec_from_file_location("rodada22", os.path.join(raiz, "dialogo", "rodada22.py"))
        r22 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(r22)
        # y = 1 + 2x com um resíduo: pontos (0, 1), (1, 3), (2, 6): m = 2,5; c = 0,8333...; resíduos 0,1667, -0,3333, 0,1667
        c, m, sse = r22.reta([0.0, 1.0, 2.0], [1.0, 3.0, 6.0])
        self.assertAlmostEqual(m, 2.5, places=12)
        self.assertAlmostEqual(c, 5 / 6, places=12)
        self.assertAlmostEqual(sse, 1 / 6, places=12)


if __name__ == "__main__":
    unittest.main()
