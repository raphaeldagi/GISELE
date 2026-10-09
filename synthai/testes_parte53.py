"""Testes de unidade da Parte 53: `python3 -m unittest synthai.testes_parte53`."""

import os
import tempfile
import unittest
from unittest import mock

import calculos
from .dicionario import Dicionario


class DicionarioFalso:
    """raiz (definição de 3 palavras) -> filho (2) -> neto (1): profundidades 0, 1, 2."""
    definicao = staticmethod(Dicionario.definicao)

    def __init__(self):
        self.sinsets = [("n", ["raiz"], [], "a b c"), ("n", ["filho"], ["n:1"], "a b"), ("n", ["neto"], ["n:2"], "a")]
        self.indice = {"n:1": 0, "n:2": 1, "n:3": 2}


class TesteParte53(unittest.TestCase):
    def test_preditor_de_mim(self):
        # valores 2, 4, 9 (k = 8 pega os três): média 5; desvios −3, −1, 4: soma dos quadrados 26; variância 13; meia-largura 1,645 √13
        h = {1: {"caracteres": 2, "compressao": 0.2, "testes_unidade": 1, "testes": 3, "erros": 1, "redundancia": 0.5},
             2: {"caracteres": 4, "compressao": 0.4, "testes_unidade": 2, "testes": None, "erros": 2, "redundancia": 0.6},
             3: {"caracteres": 9, "compressao": 0.9, "testes_unidade": 3, "testes": 5, "erros": 3, "redundancia": 0.7}}
        p = calculos.p1032_preditor_de_mim(h)
        m, w, u = p["caracteres"]
        self.assertEqual((m, u), (5.0, 9))
        self.assertAlmostEqual(w, 1.645 * 13 ** 0.5, places=12)
        self.assertEqual(p["testes"][0], 4.0)  # o None fica de fora: média de 3 e 5

    def test_historico_le_o_placar(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "ASI_AGI_parte99_x.md"), "w", encoding="utf-8").write(
                "# t\n\n### P1 (0x1). Placar\n\nParte 99: **12 testes, 4 erros**.\n")
            with mock.patch("os.path.abspath", return_value=os.path.join(d, "calculos.py")):
                h = calculos.p1031_historico_de_mim([99])
        self.assertEqual((h[99]["testes"], h[99]["erros"], h[99]["testes_unidade"]), (12, 4, 0))

    def test_definicao_e_profundidade(self):
        rho, n, faixas = calculos.p1033_definicao_e_profundidade(DicionarioFalso())
        self.assertEqual(n, 3)
        self.assertAlmostEqual(rho, -1.0, places=12)  # quanto mais fundo, mais curta: postos invertidos
        self.assertAlmostEqual(faixas["0-4"], 2.0, places=12)

    def test_pi_hexadecimal(self):
        ac, n, inicio, chi2 = calculos.p1034_pi_hexadecimal(16)
        # π = 3,243F6A8885A308D3... em hexadecimal; nos 16 dígitos: 8 quatro vezes, 3 três, A duas; 0, 2, 4, 5, 6, D, F uma; seis ausentes
        self.assertEqual((ac, n, inicio), (16, 16, "243F6A88"))
        cont = {0: 1, 2: 1, 3: 3, 4: 1, 5: 1, 6: 1, 8: 4, 0xA: 2, 0xD: 1, 0xF: 1}
        self.assertAlmostEqual(chi2, sum((c - 1) ** 2 for c in cont.values()) + (16 - len(cont)) * 1.0, places=9)  # 14 + 6 = 20


if __name__ == "__main__":
    unittest.main()
