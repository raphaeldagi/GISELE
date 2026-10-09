"""Testes de unidade da Parte 54: `python3 -m unittest synthai.testes_parte54`."""

import unittest

import calculos
from .testes_parte53 import DicionarioFalso


class TesteParte54(unittest.TestCase):
    def test_autodescritivos(self):
        # conferido por código antes (regra da Parte 53): C210000000001000 tem doze 0, dois 1, um 2 e um C
        self.assertEqual(calculos.p1063_autodescritivos(16), ["C210000000001000"])
        self.assertEqual(calculos.p1063_autodescritivos(10), ["6210001000"])
        self.assertEqual(calculos.p1063_autodescritivos(4), ["1210", "2020"])

    def test_folhas(self):
        # raiz -> filho -> neto (cadeia): só o neto é folha; os dois internos têm 1 filho cada
        frac, media, n = calculos.p1062_folhas(DicionarioFalso())
        self.assertEqual(n, 3)
        self.assertAlmostEqual(frac, 1 / 3, places=12)
        self.assertAlmostEqual(media, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
