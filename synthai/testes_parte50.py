"""Testes de unidade da Parte 50: `python3 -m unittest synthai.testes_parte50`."""

import unittest

import calculos


class GrafoFalso:
    @staticmethod
    def grafo_de_definicoes():
        return {"a": {"b", "c"}, "b": {"a"}, "c": {"d"}, "d": {"c"}}


class TesteParte50(unittest.TestCase):
    def test_periodo_hex_ate_20(self):
        # ord(2): 3:2, 5:4, 7:3, 11:10, 13:12, 17:8, 19:18; ord(16) = ord(2)/mdc(ord(2), 4): 1, 1, 3, 5, 3, 2, 9
        # ord(16)/(p-1): 1/2, 1/4, 3/6, 5/10, 3/12, 2/16, 9/18 -> soma 2,625 em 7 primos
        r16, r2, rg, k = calculos.p943_periodo_hex(20)
        self.assertEqual(k, 7)
        self.assertAlmostEqual(r16, 2.625 / 7, places=12)
        self.assertAlmostEqual(rg, (1 / 2 + 1 / 4 + 1 + 1 / 2 + 1 / 4 + 1 / 4 + 1 / 2) / 7, places=12)

    def test_definicoes_mutuas(self):
        n, m, pares, esperado, frac, ex = calculos.p942_definicoes_mutuas(GrafoFalso())
        # pares a-b e c-d; M = 5 arestas em N = 4: esperado 5·(5/16)/2 = 0,78125
        self.assertEqual((n, m, pares, ex), (4, 5, 2, [("a", "b"), ("c", "d")]))
        self.assertAlmostEqual(esperado, 0.78125, places=12)
        self.assertAlmostEqual(frac, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()


class TesteTextoVoltou(unittest.TestCase):
    def test_identico_e_diferente(self):
        import os
        import tempfile
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        guardado = os.path.join(raiz, "externos", "arquitetura_pos_asi.py")
        codigo = open(guardado, encoding="utf-8").read().rstrip("\n")
        with tempfile.TemporaryDirectory() as d:
            t1, t2 = os.path.join(d, "t1.md"), os.path.join(d, "t2.md")
            open(t1, "w", encoding="utf-8").write("Texto antes.\n" + codigo + "   \nTexto depois.\n")  # espaços no fim não contam
            open(t2, "w", encoding="utf-8").write("Antes.\n" + codigo.replace("return 0.85", "return 0.95") + "\nDepois.\n")
            igual, aud, _ = calculos.p947_o_texto_voltou(t1, guardado)
            diferente, aud2, _ = calculos.p947_o_texto_voltou(t2, guardado)
        self.assertTrue(igual)
        self.assertFalse(diferente)
        self.assertEqual((aud["nos_mudados"], aud["run_benchmarks_constante"]), (0, 0.85))
        self.assertEqual(aud2["run_benchmarks_constante"], 0.95)
