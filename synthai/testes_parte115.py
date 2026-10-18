"""Testes de unidade da Parte 115 (dez camadas contrapostas, o dicionário em algarismos e algoritmos, a escala contra a meta-medida):
`python3 -m unittest synthai.testes_parte115`. Cada pNN pelo nome (Parte 58), casos com todos os termos ≠ 0 (Parte 30), controles dos dois lados (Parte 75)."""

import unittest

import calculos
from synthai import contraposto as C


class TesteContraposto(unittest.TestCase):
    def test_gradiente_da_cadeia_contra_diferenca_finita(self):
        w = [0.9, -1.3, 1.7, 0.6, -0.8, 1.1, 1.4, -0.5, 0.7, 1.2]
        _, g, gw = C.cadeia(w, 0.4)
        h1, _, _ = C.cadeia(w, 0.4 + 1e-6)
        h0, _, _ = C.cadeia(w, 0.4 - 1e-6)
        self.assertAlmostEqual((h1 - h0) / 2e-6, g, places=8)
        for k in (0, 4, 9):
            wp, wm = list(w), list(w)
            wp[k] += 1e-6
            wm[k] -= 1e-6
            self.assertAlmostEqual((C.cadeia(wp, 0.4)[0] - C.cadeia(wm, 0.4)[0]) / 2e-6, gw[k], places=8)

    def test_base26_bijetiva(self):
        self.assertEqual(C.em_algarismos("a"), 1)
        self.assertEqual(C.em_algarismos("z"), 26)
        self.assertEqual(C.em_algarismos("aa"), 27)              # bijetiva: não há "zero à esquerda"
        self.assertEqual(C.de_algarismos(C.em_algarismos("synthai")), "synthai")

    def test_algoritmos_comutam_e_nao(self):
        afim = C.alfabeto_de_algoritmos(115)
        trans = C.alfabeto_de_algoritmos(115, comutam=True)
        self.assertEqual(C.executar("dog", trans), C.executar("god", trans))   # anagramas: translações comutam
        self.assertNotEqual(C.executar("dog", afim), C.executar("god", afim))  # afins não comutam: a ordem importa


class TesteParte115(unittest.TestCase):
    def test_p2891_dez_camadas(self):
        e1, e2, g3, g4 = calculos.p2891_dez_camadas()
        self.assertLessEqual(e1, 1e-14)
        self.assertLessEqual(e2, 1e-14)
        self.assertTrue(0.06 <= g3 <= 0.09)
        self.assertTrue(1.0e-7 <= g4 <= 4.0e-7)

    def test_p2892_sobrepostos(self):
        r1, r2, incl, gw = calculos.p2892_gradientes_sobrepostos()
        self.assertTrue(1.8 <= incl <= 2.2)
        self.assertEqual(len(gw), 10)

    def test_p2893_dicionario(self):
        porc, brutos, distintos, total, pt = calculos.p2893_palavras_do_dicionario()
        self.assertEqual(porc, {"n": 117798, "v": 11529, "a": 21479, "r": 4481})
        self.assertEqual(brutos, 206978)        # (g) previu 206.941 para os BRUTOS e errou
        self.assertEqual(distintos, 206941)     # (q): os distintos, sem marcador, dão o número publicado
        self.assertEqual(total, 147306)
        self.assertGreater(pt[0], 0)

    def test_p2894_algarismos(self):
        col, iv, dig = calculos.p2894_em_algarismos()
        self.assertEqual((col, iv), (0, True))

    def test_p2895_algoritmos(self):
        af, tr, A = calculos.p2895_em_algoritmos()
        self.assertTrue(2900 <= af[1] <= 3081)
        self.assertTrue(69831 <= tr[0] <= 70000)
        self.assertEqual(A, 72547)

    def test_p2896_escala(self):
        (m4, s4), (m256, s256), nulos = calculos.p2896_escala_e_meta_medida()
        self.assertTrue(0.678 <= s4 <= 0.736)
        self.assertTrue(0.065 <= s256 <= 0.112)
        self.assertTrue(0.974 <= m4 <= 1.026)
        self.assertEqual(nulos, 1)

    def test_p2897_rodada82(self):
        h, g, gw = calculos.p2897_rodada82()
        self.assertEqual(g.hex(), "0x1.32d264963ff7cp-4")

    def test_p1961_com_parte_115(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[115], (15, 16))
        self.assertEqual((ok, tot), (222, 244))


if __name__ == "__main__":
    unittest.main()
