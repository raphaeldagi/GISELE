"""Testes de unidade da Parte 100 (o dicionario como data lake encontra o GPT): `python3 -m unittest synthai.testes_parte100`."""

import unittest

import calculos


class TesteParte100(unittest.TestCase):
    def test_p2441_invariancia_4grama(self):
        b_en, b_pt, dif = calculos.p2441_invariancia_4grama()
        # a predizibilidade das glosas e quase a mesma nas duas linguas (genero 'definicao')
        self.assertLess(dif, 0.15)
        self.assertTrue(1.5 < b_en < 3.5 and 1.5 < b_pt < 3.5)

    def test_p2442_nao_e_volume(self):
        b = calculos.p2442_invariancia_nao_e_volume()
        self.assertTrue(2.6 <= b <= 2.9)

    def test_p2443_gpt_perde(self):
        gpt_en, tri_en, gpt_pt, tri_pt = calculos.p2443_gpt_contra_ngrama(passos=500)
        # com so 500 passos o GPT ja perde para o trigrama nas duas linguas (ancora da Parte 69)
        self.assertGreater(gpt_en, tri_en)
        self.assertGreater(gpt_pt, tri_pt)

    def test_p2444_no_meio(self):
        # funcao pura: o GPT fica abaixo do uniforme e em [3,0; 4,1]
        unif, me, mp, meio = calculos.p2444_gpt_no_meio(3.48, 3.41)
        self.assertTrue(me and mp and meio)
        self.assertTrue(unif > 4.1)
        # caso de controle: um GPT no acaso (> uniforme) nao esta "no meio"
        _, _, _, meio2 = calculos.p2444_gpt_no_meio(5.5, 5.5)
        self.assertFalse(meio2)

    def test_p2445_rodada67(self):
        casos = calculos.p2445_rodada67()
        self.assertEqual(len(casos), 5)
        for tok, mant, top1 in casos:
            self.assertTrue(0 <= tok <= 4 and 1 <= mant <= 5 and 0.0 < top1 <= 1.0)

    def test_p2446_retrospecto(self):
        kf, rod, cal = calculos.p2446_retrospecto_cem()
        self.assertGreater(kf, 400)       # centenas de funcoes pNN
        self.assertGreaterEqual(rod, 60)  # dezenas de rodadas do dialogo
        self.assertTrue(0.74 <= cal <= 0.88)

    def test_p1961_com_parte_100(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 101))))
        self.assertEqual(por[100], (5, 5))
        self.assertEqual((ok, tot), (92, 106))


if __name__ == "__main__":
    unittest.main()
