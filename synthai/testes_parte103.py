"""Testes de unidade da Parte 103 (o dicionario como numeros, o baralho numero+palavra): `python3 -m unittest synthai.testes_parte103`."""

import math
import unittest

import calculos
from synthai import baralho, numeros


class TesteParte103(unittest.TestCase):
    def test_p2531_entropia_baralho(self):
        e, teto = calculos.p2531_entropia_do_baralho()
        self.assertAlmostEqual(teto, math.log2(52), places=12)
        self.assertTrue(5.68 <= e <= 5.7004)  # amostra finita subestima o teto fechado

    def test_p2532_numero_e_palavra(self):
        so, amb = calculos.p2532_numero_e_palavra()
        self.assertTrue(0.48 <= so <= 0.52)   # so o numero e cego a cor -> moeda
        self.assertEqual(amb, 1.0)            # numero + palavra recupera a cor, exato

    def test_p2533_posto_gf2(self):
        self.assertEqual(calculos.p2533_posto_gf2_do_dicionario(), 4)  # posto de coluna cheio
        # caso de controle: um unico vetor tem posto 1, nao 4
        self.assertEqual(numeros.posto_gf2([[1, 0, 1, 0]]), 1)
        # caso TODOS != 0 (regra da Parte 30): dois vetores independentes -> posto 2
        self.assertEqual(numeros.posto_gf2([[1, 1, 0, 0], [0, 1, 1, 0]]), 2)

    def test_p2534_colisoes(self):
        col, esp = calculos.p2534_colisoes_do_dicionario()
        self.assertAlmostEqual(esp, 1000 * 999 / 2 / 10007, places=9)
        self.assertTrue(38 <= col <= 62)  # Poisson ~50 +- 1,645*sqrt(50)

    def test_p2535_recusa(self):
        self.assertEqual(calculos.p2535_recusa_proposta_parte103(), (True, True))  # rede + replicacao -> RECUSADO
        self.assertEqual(calculos.p2535_recusa_proposta_parte103("dicionario_em_numeros+baralho"), (False, False))  # nucleo
        self.assertEqual(calculos.p2535_recusa_proposta_parte103("yfinance"), (True, False))
        self.assertEqual(calculos.p2535_recusa_proposta_parte103("auto_replicacao"), (False, True))

    def test_baralho_cor_so_do_naipe(self):
        # a cor e funcao SO do naipe (palavra), nao do valor (numero): control dos dois lados
        self.assertEqual(baralho.cor("ouros"), "vermelho")
        self.assertEqual(baralho.cor("paus"), "preto")
        self.assertEqual(len(baralho.baralho()), 52)
        self.assertEqual(sorted(baralho.codigo(c) for c in baralho.baralho()), list(range(52)))

    def test_p2536_rodada70(self):
        saida = calculos.p2536_rodada70()
        self.assertEqual(len(saida), 3)
        self.assertEqual(len(saida[0]), 4)

    def test_p1961_com_parte_103(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 104))))
        self.assertEqual(por[103], (5, 5))
        self.assertEqual((ok, tot), (107, 121))


if __name__ == "__main__":
    unittest.main()
