"""Testes de unidade da Parte 46: `python3 -m unittest synthai.testes_parte46`."""

import importlib.util
import os
import tempfile
import unittest

import calculos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("rodada18", os.path.join(RAIZ, "dialogo", "rodada18.py"))
r18 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r18)


class TesteParte46(unittest.TestCase):
    def test_cauda_binomial(self):
        # P(X >= 2), X ~ Bin(3; 0,4): 3·0,16·0,6 + 0,064 = 0,288 + 0,064 = 0,352 (todos os termos diferentes de zero)
        self.assertAlmostEqual(calculos.p825_cauda_binomial(3, 0.4, 2), 0.352, places=12)
        self.assertAlmostEqual(calculos.p825_cauda_binomial(5, 0.3, 0), 1.0, places=12)

    def test_numeros_tira_rotulos_e_normaliza(self):
        # rótulos somem; "231,5" e "231.5" viram o mesmo número; zeros à esquerda e números curtos saem
        self.assertEqual(r18.numeros("P761 (0x2F9): 231,5 e 0,005 e 82.115 e 12"), {"2315", "82115"})
        self.assertEqual(r18.numeros("P761 231.5"), r18.numeros("231,5"))

    def test_reproducao_conta_diferencas(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = os.path.join(d, "a"), os.path.join(d, "b")
            open(a, "w").write("x 1\ny 2\nz 3\n=== Unificacao\nw\n")
            open(b, "w").write("x 1\ny 9\nz 3\n=== Unificacao\nOUTRA\n")
            fim, iguais, difs = calculos.p823_reproducao(a, b)
            self.assertEqual((fim, iguais, [i for i, _, _ in difs]), (3, 2, [1]))


if __name__ == "__main__":
    unittest.main()
