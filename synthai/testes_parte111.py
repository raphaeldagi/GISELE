"""Testes de unidade da Parte 111 (o word_rl_lab recebido, reescrito offline): `python3 -m unittest synthai.testes_parte111`. Os autotestes da
própria v2, portados, mais um teste por afirmação medida e os controles dos dois lados do auditor por capacidade (regra da Parte 75)."""

import random
import unittest

import calculos
from synthai import palavras_rl as P


class TesteAutotestesDaV2(unittest.TestCase):
    """Os 14 autotestes da v2 (run_selftests), na versão sem numpy."""

    def test_vetor(self):
        self.assertTrue(any(P.word_to_vector(p) != P.word_to_vector(p[::-1]) for p in ["AB", "CA", "TO", "NO", "ST", "HE"]))
        self.assertAlmostEqual(sum(v * v for v in P.word_to_vector("CAT")), 1.0, places=12)
        self.assertEqual(P.word_score("CAT"), 15)

    def test_ambiente(self):
        env = P.WordGridEnv(size=4, rng=random.Random(1))
        env.reset()
        self.assertTrue(env.path_is_legal([(0, 0), (0, 1), (1, 2)]))
        self.assertFalse(env.path_is_legal([(0, 0), (0, 1), (0, 0)]))
        self.assertFalse(env.path_is_legal([(0, 0), (2, 2)]))
        self.assertEqual((len(env.neighbors((0, 0))), len(env.neighbors((1, 1)))), (3, 8))
        self.assertEqual(list(P.valid_actions(env, [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)])), [P.STOP])
        self.assertNotIn(P.STOP, P.valid_actions(env, [(0, 0)]))

    def test_dicionario_e_metricas(self):
        d = P.Dicionario(P.EMBEDDED_WORDS)
        self.assertTrue(d.is_word("cat") and not d.is_word("xqz"))
        self.assertEqual(len(P.EMBEDDED_WORDS), 493)   # lido da cópia verbatim pela AST
        self.assertEqual((P.brier([1.0, 0.0], [1.0, 0.0]), P.ece([1.0, 0.0], [1.0, 0.0])), (0.0, 0.0))
        lo, hi = P.wilson(3, 10)
        self.assertTrue(0.0 <= lo < 0.3 < hi <= 1.0)

    def test_determinismo(self):
        cfg = P.Config(episodios=300, avaliacao=50, seed=3)
        d = P.Dicionario(P.EMBEDDED_WORDS)
        a1, _, s1 = P.train(cfg, d)
        a2, _, s2 = P.train(cfg, d)
        self.assertEqual((a1.q, s1), (a2.q, s2))


class TesteParte111(unittest.TestCase):
    def test_p2771_guloso_x_aleatorio(self):
        g, a, disj = calculos.p2771_guloso_x_aleatorio()
        self.assertTrue(0.03 <= g <= 0.22)
        self.assertTrue(0.005 <= a <= 0.016)
        self.assertEqual(disj, 5)

    def test_p2772_acao_direcao(self):
        du, df = calculos.p2772_acao_direcao()
        self.assertTrue(0.0 <= du <= 0.004)
        self.assertTrue(-0.004 <= df <= 0.006)

    def test_p2773_confianca_e_ablacoes(self):
        re_, rw, sq, sl = calculos.p2773_confianca_e_ablacoes()
        self.assertTrue(0.35 <= re_ <= 0.97)
        self.assertTrue(0.43 <= rw <= 0.51)
        self.assertLess(sq, 0.80)    # (n) errou: sem o Q, o estimador ainda bate a base
        self.assertLess(sl, 0.85)    # (p) errou: so as letras ainda batem a base
        self.assertTrue(re_ < sq < sl < 1.0)   # a cadeia medida: cada peca carrega uma parte

    def test_p2774_data_lake(self):
        nl, gw, aw, rz = calculos.p2774_data_lake()
        self.assertEqual(nl, 77340)
        self.assertTrue(0.27 <= gw <= 0.39 and 0.037 <= aw <= 0.060 and 3.0 <= rz <= 7.5)

    def test_p2775_auditor_por_capacidade(self):
        v1a, v2a, v1n, v2n, pl, li, pr = calculos.p2775_auditor_por_capacidade()
        self.assertEqual(v1a, [])                      # o defeito da auditoria da Parte 109: nao viu a rede da v1
        self.assertEqual(v2a, ["import:urllib"])       # e acusou o urllib.parse.quote
        self.assertIn("rede:requests.get", v1n)
        self.assertIn("rede:nltk.download", v2n)
        self.assertEqual(len(pl), 7)                   # (k) previu 6: o import urllib.request da fixture nao estava na conta
        self.assertEqual(li, [])
        self.assertEqual(pr, [])                       # o auditor roda sobre o proprio fonte (regra da Parte 109)

    def test_p2776_rodada78(self):
        q = calculos.p2776_rodada78()
        self.assertEqual((len(q), len(q[0])), (5, 3))
        self.assertEqual(q[0][0].hex(), "0x1.3b40a03e5252dp+2")

    def test_p2777_palavras_distintas(self):
        d = calculos.p2777_palavras_distintas_do_guloso()
        self.assertTrue(3 <= len(d) <= 20)
        self.assertEqual(d.most_common(1)[0][0], "EAT")

    def test_p1961_com_parte_111(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 112))))
        self.assertEqual(por[111], (12, 15))
        self.assertEqual((ok, tot), (170, 191))


if __name__ == "__main__":
    unittest.main()
