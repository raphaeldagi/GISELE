"""Testes de unidade da Parte 113 (CFR no Kuhn, a transferência do repertório, o leitor v4): `python3 -m unittest synthai.testes_parte113`.
Cada pNN chamada pelo NOME (regra da Parte 58), controles dos dois lados (Parte 75), casos com todos os termos diferentes de zero (Parte 30)."""

import unittest

import calculos
from synthai import cfr, palavras_rl as P


class TesteCFR(unittest.TestCase):
    def test_terminais_a_mao(self):
        self.assertEqual(cfr._terminal("pp", 3, 1), 1)      # passa-passa: o maior ganha 1
        self.assertEqual(cfr._terminal("bb", 1, 2), -2)     # aposta-paga: o menor perde 2
        self.assertEqual(cfr._terminal("bp", 1, 3), 1)      # o 2 desiste: o 1 ganha o pote, mesmo com o valete
        self.assertEqual(cfr._terminal("pbp", 3, 1), -1)    # o 1 desiste depois de passar
        self.assertIsNone(cfr._terminal("pb", 1, 2))

    def test_valor_do_equilibrio_de_kuhn(self):
        # controle: o perfil de Kuhn com alfa = 1/3, escrito à mão, vale exatamente -1/18 e tem explorabilidade ~0
        a = 1.0 / 3.0
        e = {(1, ""): [1 - a, a], (2, ""): [1.0, 0.0], (3, ""): [0.0, 1.0],
             (1, "pb"): [1.0, 0.0], (2, "pb"): [1 - (a + 1 / 3), a + 1 / 3], (3, "pb"): [0.0, 1.0],
             (1, "p"): [2 / 3, 1 / 3], (2, "p"): [1.0, 0.0], (3, "p"): [0.0, 1.0],
             (1, "b"): [1.0, 0.0], (2, "b"): [2 / 3, 1 / 3], (3, "b"): [0.0, 1.0]}
        self.assertAlmostEqual(cfr.valor(e), -1 / 18, places=12)
        self.assertLess(abs(cfr.explorabilidade(e)), 1e-12)
        # e o caso sujo: um jogador 2 que sempre paga é explorável
        e2 = dict(e)
        for c in (1, 2, 3):
            e2[(c, "b")] = [0.0, 1.0]
        self.assertGreater(cfr.explorabilidade(e2), 0.01)


class TesteParte113(unittest.TestCase):
    def test_p2831_cfr_convergencia(self):
        ex, dv, v = calculos.p2831_cfr_convergencia()
        self.assertTrue(0.0017 <= ex <= 0.013)
        self.assertLessEqual(dv, ex)        # a identidade de (b): |v - v*| <= explorabilidade

    def test_p2832_cfr_equilibrio(self):
        cq, bj, al, d1, d2 = calculos.p2832_cfr_equilibrio()
        self.assertTrue(cq <= 0.03 and bj <= 0.03 and d1 <= 0.03 and d2 <= 0.03)
        self.assertTrue(0.15 <= al <= 0.30)   # INTERIOR da família (o simplex parou no vértice 1/3)

    def test_p2833_p2834_leitor_v4(self):
        self.assertEqual(calculos._numero_pt_v2("5·10⁻⁴"), 0.0005)
        self.assertEqual(calculos._numero_pt_v2("10⁻¹²"), 1e-12)
        self.assertEqual(calculos._numero_pt_v2("−1,96"), -1.96)        # sem sobrescrito: delega à original
        v3 = calculos.p2806_minhas_previsoes_v3(range(110, 111))
        v4 = calculos.p2833_minhas_previsoes_v4(range(110, 111), numero=calculos._numero_pt)
        self.assertEqual([x[:4] for x in v3], [x[:4] for x in v4])   # controle: com o leitor velho, a v4 é a v3
        rec, per, tro, tot = calculos.p2834_v3_contra_v4(range(53, 113))
        self.assertEqual(rec, [(70, "g"), (77, "d"), (110, "c"), (110, "h"), (110, "i"), (112, "g")])
        self.assertEqual((per, tro), ([], []))

    def test_p2835_transferencia(self):
        an, df, ns = calculos.p2835_transferencia_do_repertorio()
        self.assertTrue(0.59 <= an <= 0.70)
        self.assertTrue(0.055 <= df <= 0.23)
        self.assertEqual(ns, 10)
        self.assertEqual(P.auc([1.0, 0.9], [0.1, 0.2]), 1.0)
        self.assertEqual(P.auc([0.5], [0.5]), 0.5)

    def test_p2836_rodada80(self):
        m = calculos.p2836_rodada80()
        self.assertEqual(len(m), 12)
        self.assertEqual(m[0].hex(), "0x1.c1739c94c6931p-3")

    def test_p2837_p2838_placar_v4(self):
        m, ws = calculos.p2837_previsoes_sobre_previsoes_v4(113)
        self.assertEqual(m["m1"], 13)
        linhas, mudam = calculos.p2838_auditoria_do_placar_m_v4()
        self.assertEqual(mudam, 0)
        self.assertEqual(sum(1 for l in linhas if l[3] != l[4]), 5)   # o texto dizia 4 (contado por leitura) e listava 5

    def test_p1961_com_parte_113(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 114))))
        self.assertEqual(por[113], (13, 13))
        self.assertEqual((ok, tot), (197, 218))


if __name__ == "__main__":
    unittest.main()
