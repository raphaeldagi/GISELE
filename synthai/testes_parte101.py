"""Testes de unidade da Parte 101 (dez camadas, recursao-contracao, caos x texto): `python3 -m unittest synthai.testes_parte101`."""

import unittest

import calculos


class TesteParte101(unittest.TestCase):
    def test_p2471_dez_camadas(self):
        it10, conta, it7 = calculos.p2471_dez_camadas()
        self.assertAlmostEqual(it10, conta, places=9)
        self.assertLess(abs(it10 - 0.5), abs(it7 - 0.5))  # 10 camadas mais perto de 0,5 que 7

    def test_p2472_composicao(self):
        comp, conta, fixo = calculos.p2472_composicao_prob_metacog()
        self.assertAlmostEqual(comp, conta, places=12)  # composicao = produto dos fatores
        self.assertAlmostEqual(fixo, 0.5, places=12)     # ponto fixo preservado
        # ordem nao importa (a*b = b*a)
        c1, _, _ = calculos.p2472_composicao_prob_metacog(a=5.0 / 6.0, b=0.7)
        c2, _, _ = calculos.p2472_composicao_prob_metacog(a=0.7, b=5.0 / 6.0)
        self.assertAlmostEqual(c1, c2, places=12)

    def test_p2473_texto_x_caos(self):
        caos, razao = calculos.p2473_texto_x_caos()
        self.assertAlmostEqual(caos, 1.0, delta=0.02)  # caos incompressivel por trigrama
        self.assertTrue(0.45 <= razao <= 0.65)          # texto comprime

    def test_p2474_recursao_contrai(self):
        res, converge = calculos.p2474_recursao_contrai()
        self.assertTrue(converge)
        for r in res:
            self.assertAlmostEqual(r, 0.5, delta=0.01)

    def test_p2475_rodada68(self):
        casos = calculos.p2475_rodada68()
        self.assertEqual(len(casos), 5)
        for tok, p0 in casos:
            self.assertTrue(0 <= tok <= 4 and 0.0 < p0 < 1.0)

    def test_p2476_versa_reversa(self):
        ab, ba, assim = calculos.p2476_versa_reversa()
        self.assertTrue(assim)        # pergunta-em-resposta > resposta-em-pergunta (assimetria da Parte 46)
        self.assertGreater(ab, ba)
        # caso de controle: textos iguais -> containment simetrico (1,1), nao assimetrico
        ab2, ba2, assim2 = calculos.p2476_versa_reversa("abcabc", "abcabc")
        self.assertFalse(assim2)
        self.assertAlmostEqual(ab2, ba2, places=12)

    def test_p1961_com_parte_101(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[101], (5, 5))
        self.assertEqual((ok, tot), (97, 111))


if __name__ == "__main__":
    unittest.main()
