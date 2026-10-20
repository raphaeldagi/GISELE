"""Testes de unidade da Parte 120 (o pôquer Leduc e o CFR nele, `synthai/leduc.py`): `python3 -m unittest synthai.testes_parte120`.
As regras do jogo conferidas à mão (Parte 47), e cada função nova pelo nome (Parte 118)."""

import unittest

from synthai import leduc as L


class TesteRegras(unittest.TestCase):
    def test_contribuicoes(self):
        self.assertEqual(L.contribuicoes("rrc/rr"), [9, 13])     # 1 + 4 na 1ª rodada; +4 e +8 na 2ª
        self.assertEqual(L.contribuicoes("cc/"), [1, 1])

    def test_terminal(self):
        self.assertEqual(L.terminal("rrc/rrc", 2, 1, 0), 13.0)    # rei contra dama, pública valete: o 1 ganha o pote do 2
        self.assertEqual(L.terminal("rrc/rrc", 1, 2, 1), 13.0)    # a dama pareia com a pública e bate o rei
        self.assertEqual(L.terminal("cc/rf", 0, 1, 2), 1.0)       # o 2 desiste diante da aposta: perde só a ante
        self.assertEqual(L.terminal("cc/cc", 1, 1, 0), 0.0)       # cartas iguais dividem
        self.assertIsNone(L.terminal("cr", 0, 1, 2))

    def test_acoes_e_proximo(self):
        self.assertEqual(L.acoes(""), ("c", "r"))
        self.assertEqual(L.acoes("r"), ("f", "c", "r"))
        self.assertEqual(L.acoes("rr"), ("f", "c"))               # no máximo 2 aumentos por rodada
        self.assertEqual(L.proximo("c", "c"), "cc/")

    def test_conjuntos_de_informacao(self):
        a, b = L.conjuntos_de_informacao()
        self.assertEqual((len(a), len(b)), (144, 144))            # 3 cartas × 3 nós na 1ª rodada + 5 prefixos × 3 nós × 3 × 3 na 2ª

    def test_cfr_reduz_explorabilidade(self):
        uniforme = L.explorabilidade({})
        c = L.CFRLeduc().vanilla(5)
        self.assertLess(L.explorabilidade(c.media()), uniforme)
        self.assertGreaterEqual(L.melhor_resposta(c.media(), 0), L.valor(c.media()))
        self.assertLessEqual(L.melhor_resposta(c.media(), 1), L.valor(c.media()))

    def test_amostradores(self):
        a = L.CFRLeduc().acaso(200, 7)
        e = L.CFRLeduc().externo(200, 7)
        self.assertEqual(a.nos, 200 * 85)                         # uma distribuição por iteração: a árvore inteira dela
        self.assertLess(e.nos, a.nos)



class TesteParte120(unittest.TestCase):
    """As pNN da Parte 120 pelo nome (Parte 58), num custo pequeno (a de 20 milhões de nós roda em calculos.py 120)."""

    def test_p3041_e_p3042(self):
        import calculos
        r = calculos.p3041_leduc(nos=204_000, sementes=(1,))
        self.assertEqual(set(r), {"vanilla", "acaso", "externo"})
        self.assertEqual(r["vanilla"][0][4], 204_000)              # 20 iterações × 10.200 nós
        for v in r.values():
            e, val, br0, br1, _ = v[0]
            self.assertAlmostEqual(e, br0 - br1)                     # explorabilidade = soma do que as duas melhores respostas ganham
            self.assertTrue(br1 <= val <= br0)
        a, b, (lo, hi) = calculos.p3042_razoes_mesmo_custo(r)
        self.assertGreater(a, 0)
        self.assertLessEqual(lo, hi)                                 # o valor do jogo está na interseção dos intervalos

    def test_p3043_rodada88(self):
        import calculos
        self.assertEqual(calculos.p3043_rodada88(), (288, 0))

    def test_p1961_com_parte_120(self):
        import calculos
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[120], (8, 9))
        self.assertEqual((ok, tot), (282, 309))


if __name__ == "__main__":
    unittest.main()
