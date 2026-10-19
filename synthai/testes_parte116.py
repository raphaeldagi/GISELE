"""Testes de unidade da Parte 116 (o NEXUS-RAPHAEL v2 colado, medido no próprio código): `python3 -m unittest synthai.testes_parte116`.
Cada pNN pelo nome (Parte 58), casos com todos os termos ≠ 0 (Parte 30), controles dos dois lados (Parte 75)."""

import math
import random
import unittest

import calculos
from synthai import nexus_v2 as N


class TesteNexusV2(unittest.TestCase):
    def test_posicional_zero_a_esquerda_e_bijetiva_nao(self):
        self.assertEqual(N.recebido_posicional("abed"), N.recebido_posicional("bed"))   # defeito plantado: o 'a' é um zero
        self.assertNotEqual(N.recebido_posicional("bed"), N.recebido_posicional("bee"))  # controle limpo

    def test_confianca_media_negativa(self):
        self.assertEqual(N.recebido_confianca([-1.0, -100.0, 50.0]), 0.9)
        self.assertGreater(N.confianca_corrigida([-1.0, -100.0, 50.0]), 1.0)
        self.assertLess(N.confianca_corrigida([10.0, 10.1, 9.9]), 0.01)

    def test_ic_recebido_ignora_a_confianca_pedida(self):
        d = [0.3, -1.2, 0.8, 2.1, -0.4]
        self.assertEqual(N.recebido_ic(d, 0.90), N.recebido_ic(d, 0.99))
        self.assertLess(N.ic_t(d, 0.90)[1] - N.ic_t(d, 0.90)[0], N.ic_t(d, 0.99)[1] - N.ic_t(d, 0.99)[0])

    def test_t_quantil(self):
        self.assertAlmostEqual(N.t_quantil(0.975, 4), 2.776445, places=5)
        self.assertAlmostEqual(N.t_cdf(N.t_quantil(0.9, 7), 7), 0.9, places=9)

    def test_vetor_local_nao_toca_o_global(self):
        random.seed(5)
        a = random.random()
        random.seed(5)
        N.vetor_da_palavra("synthai")
        self.assertEqual(random.random(), a)

    def test_memoria_em_memoria(self):
        m = N.Memoria()
        m.guardar_hipotese("H0", "teste")
        m.guardar_experimento("H0", 1.5, 1.0, {"k": 1})
        m.guardar_experimento("H0", 2.5, 1.0)
        self.assertEqual(m.experimentos("H0"), [(1.5, 1.0), (2.5, 1.0)])
        m.fechar()

    def test_dicionario_offline(self):
        d = N.dicionario_offline()
        self.assertTrue(any("distinct existence" in g for _, g in d["entity"]))


class TesteParte116(unittest.TestCase):
    def test_p2921_o_texto_e_a_arvore(self):
        d = calculos.p2921_o_texto_e_a_arvore()
        self.assertEqual(d["classes_comuns"], ["Config"])
        self.assertEqual(d["indefinidos"], ["AdversarialLayer", "GameState", "RaphaelGame"])
        self.assertIn("rede:urllib.request.urlopen", d["rede"])
        self.assertEqual(d["chamadas"], ["random.seed", "sqlite3.connect"])

    def test_p2922_semelhanca_por_hash(self):
        da, ma, ms, dif = calculos.p2922_semelhanca_por_hash()
        self.assertTrue(0.309 <= da <= 0.323)
        self.assertTrue(-0.0165 <= dif <= 0.0165)

    def test_p2923_gerador_global(self):
        self.assertEqual(calculos.p2923_gerador_global(), (1, 1000))

    def test_p2924_codificacoes(self):
        pp, pm, alf, num, ex = calculos.p2924_codificacoes()
        self.assertEqual((pp, pm, alf), (446, 446, 284))
        self.assertLessEqual(num, 0.004)

    def test_p2925_avaliacao_sob_a_nula(self):
        c, r, pa, cf = calculos.p2925_avaliacao_sob_a_nula()
        self.assertTrue(0.3627 <= c <= 0.3739)
        self.assertTrue(0.3495 <= r <= 0.3607)
        self.assertTrue(0.0475 <= pa <= 0.0525)
        self.assertEqual(cf, 0.9)

    def test_p2926_cobertura_do_intervalo(self):
        a, b, t = calculos.p2926_cobertura_do_intervalo()
        self.assertTrue(0.9815 <= a <= 0.9845)
        self.assertTrue(0.9334 <= b <= 0.9390)
        self.assertTrue(0.8965 <= t <= 0.9035)

    def test_p2927_auditoria_de_entrada(self):
        self.assertEqual(calculos.p2927_auditoria_de_entrada(), (7, 3, 0))

    def test_p2928_vetor_identico(self):
        self.assertEqual(calculos.p2928_vetor_identico(), 0)

    def test_p2929_rodada83(self):
        r = calculos.p2929_rodada83()
        self.assertEqual(r[0][1].hex(), "0x1.367cd559777dap+1")
        self.assertEqual([s for s, _ in r], ["confirmed", "inconclusive", "rejected"])

    def test_p1961_com_parte_116(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 117))))
        self.assertEqual(por[116], (19, 19))
        self.assertEqual((ok, tot), (241, 263))


if __name__ == "__main__":
    unittest.main()
