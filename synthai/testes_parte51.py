"""Testes de unidade da Parte 51: `python3 -m unittest synthai.testes_parte51`."""

import importlib.util
import math
import os
import unittest

import calculos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TesteParte51(unittest.TestCase):
    def test_kaprekar_base_10(self):
        # o 6174 atrai todos os números de 4 dígitos decimais que não são repdígitos (9999 − 9 = 9990)
        cs, bacia, total = calculos.p973_kaprekar_hex(4, 10)
        self.assertEqual((cs, total, bacia[(6174,)]), ([(6174,)], 9990, 9990))

    def test_kaprekar_passo_a_mao(self):
        # 0x1234 -> 0x4321 − 0x1234 = 0x30ED -> 0xED30 − 0x03DE = 0xE952: os dois estão no mesmo ciclo
        cs, _, _ = calculos.p973_kaprekar_hex()
        ciclo = next(c for c in cs if 0x30ED in c)
        self.assertIn(0xE952, ciclo)

    def test_duas_exponenciais_recupera_parametros(self):
        spec = importlib.util.spec_from_file_location("rodada25", os.path.join(RAIZ, "dialogo", "rodada25.py"))
        r25 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(r25)
        # curva exata 0,1 e^(−L/1,5) + 0,02 e^(−L/40), os dois tempos na grade: o ajuste recupera A, B, t1, t2 e erro ~0
        ys = [0.1 * math.exp(-L / 1.5) + 0.02 * math.exp(-L / 40) for L in range(1, 21)]
        sse, A, B, t1, t2 = r25.duas_exponenciais(ys)
        self.assertEqual((t1, t2), (1.5, 40.0))
        self.assertAlmostEqual(A, 0.1, places=9)
        self.assertAlmostEqual(B, 0.02, places=9)
        self.assertLess(sse, 1e-20)
        # AIC = n ln(SSE/n) + 2k: n = 20, SSE = 2, k = 2 -> 20 ln 0,1 + 4
        self.assertAlmostEqual(r25.aic(2.0, 20, 2), 20 * math.log(0.1) + 4, places=12)


if __name__ == "__main__":
    unittest.main()


class TesteFaixas(unittest.TestCase):
    def test_conta_unilaterais(self):
        import tempfile
        from unittest import mock
        texto = ("# t\n\n## Previsões pré-registradas\n- (a) em **[0,2; 0,3]**\n- (b) pelo menos 5\n- (c) ≥ 50%\n"
                 "- (d) razão > 5\n- (e) entre 2 e 6, faixa [2; 6] e ≥ 1\n\n---\n- (f) ≥ 9 fora do bloco\n")
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "ASI_AGI_parte99_teste.md"), "w", encoding="utf-8").write(texto)
            with mock.patch("os.path.abspath", return_value=os.path.join(d, "calculos.py")):
                r = calculos.p974_previsoes_sem_largura([99])
        # (a) e (e) têm faixa; (b), (c), (d) são unilaterais; (f) está fora do bloco
        self.assertEqual(r, {99: (5, 3, ["b", "c", "d"])})
