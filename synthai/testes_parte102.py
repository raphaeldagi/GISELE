"""Testes de unidade da Parte 102 (o Global Workspace): `python3 -m unittest synthai.testes_parte102`."""

import unittest

import calculos
from synthai import workspace


class TesteParte102(unittest.TestCase):
    def test_p2501_integracao_vence(self):
        iso, ws, razao = calculos.p2501_integracao_vence()
        self.assertTrue(0.50 <= iso <= 0.62)  # erro irredutivel ~|b|/sqrt(3)
        self.assertLess(ws, 1e-6)             # workspace recupera o exato
        self.assertLess(razao, 0.01)

    def test_p2502_empata(self):
        iso0, ws0 = calculos.p2502_empata_quando_um_basta()
        self.assertLess(iso0, 1e-9)
        self.assertLess(ws0, 1e-9)

    def test_p2503_exato(self):
        self.assertLess(calculos.p2503_recupera_exato(), 1e-6)

    def test_p2504_geometrica(self):
        rs, mono = calculos.p2504_convergencia_geometrica()
        self.assertTrue(mono)
        self.assertTrue(1e-4 <= rs[1] <= 1e-2)

    def test_workspace_recupera_coeficientes(self):
        # caso de controle com TODOS os termos != 0: o workspace bate o alvo y=a x1 + b x2
        X1, X2, Y = workspace.gerar_mundo(7, 300, a=2.0, b=-3.0)
        _, r, _ = workspace.workspace_global(X1, X2, Y, passos=12)
        self.assertLess(r, 1e-6)
        # um especialista isolado sozinho NAO recupera (ve so uma caracteristica)
        _, riso = workspace.especialista_isolado(X1, Y)
        self.assertGreater(riso, 0.5)

    def test_p2505_rodada69(self):
        seq, sc = calculos.p2505_rodada69()
        self.assertEqual(len(seq), 4)
        self.assertLess(sc, 0.0)  # soma de log-probabilidades e negativa

    def test_p2506_recusa(self):
        rede, popen = calculos.p2506_recusa_upload_v015()
        self.assertTrue(rede and popen)
        # caso de controle limpo: um codigo so com matematica nao e acusado
        r2, p2 = calculos.p2506_recusa_upload_v015("def f(x):\n    return x*x+1\n")
        self.assertFalse(r2 or p2)

    def test_p1961_com_parte_102(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[102], (5, 5))
        self.assertEqual((ok, tot), (102, 116))


if __name__ == "__main__":
    unittest.main()
