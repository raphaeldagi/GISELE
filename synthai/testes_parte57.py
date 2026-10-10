"""Testes de unidade da Parte 57: `python3 -m unittest synthai.testes_parte57`. Cada pNN nova com o seu teste."""

import importlib.util
import os
import unittest

import calculos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LemasFalsos:
    # palíndromos de 3+ letras: 'aba', 'civic' (e 'AbA' vira 'aba', repetido); 'ab' é curto; 'abc' não é
    lemas = {"aba": [0], "civic": [1], "abc": [2], "ab": [3], "AbA": [4], "x-y": [5]}


class TesteParte57(unittest.TestCase):
    def test_palindromos(self):
        pal, conta, conta_pontas, n, ex = calculos.p1152_palindromos(LemasFalsos())
        self.assertEqual((pal, n, ex), (2, 3, ["aba", "civic"]))
        # conta à mão conferida por código: letras de 'aba', 'abc', 'civic' = a3 b2 c3 i2 v1 (11): Σp² = (9+4+9+4+1)/121 = 27/121
        q = 27 / 121
        self.assertAlmostEqual(conta, 2 * q + 1 * q ** 2, places=12)

    def test_duplos_palindromos(self):
        # abaixo de 1000: 1..9, 11 (0xB), 353 (0x161), 626 (0x272), 787 (0x313), 979 (0x3D3)
        k, conta, d = calculos.p1153_duplos_palindromos(1000)
        self.assertEqual((k, d), (14, [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 353, 626, 787, 979]))

    def test_alfabeto_portugues(self):
        spec = importlib.util.spec_from_file_location("rodada31", os.path.join(RAIZ, "dialogo", "rodada31.py"))
        r31 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(r31)
        # 'ábaco' vem depois de 'zebra' pelos códigos (á > z), e antes pela ordem portuguesa
        uni, pt, trocas = r31.reordenar([("zebra", 1, 1), ("ábaco", 1, 1)])
        self.assertEqual([g for g, _, _ in uni], ["zebra", "ábaco"])
        self.assertEqual([g for g, _, _ in pt], ["ábaco", "zebra"])
        self.assertEqual(trocas, [("zebra", "ábaco")])
        self.assertEqual(calculos.p1151_alfabeto_portugues(), ([], 2))


if __name__ == "__main__":
    unittest.main()
