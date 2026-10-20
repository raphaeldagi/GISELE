"""Testes de unidade da Parte 122 (o texto "NEXUS–RAPHAEL v3.0", `synthai/nexus_v30.py`): `python3 -m unittest synthai.testes_parte122`.
Cada pNN e cada peça pelo nome (Partes 58 e 118); as identidades com todos os termos diferentes de zero (Parte 30)."""

import math
import random
import unittest

import calculos
from synthai import nexus_v30 as V


class TestePecas(unittest.TestCase):
    def test_base70_recebida(self):
        self.assertEqual((V.recebido_b70(42), V.recebido_b70(2026)), ("mi", "jote"))      # o texto dizia "pi" e "lize"
        self.assertEqual(V.recebido_b70_inverso("babe"), V.recebido_b70_inverso("be"))   # o zero à esquerda
        self.assertEqual(V.colisoes_b70(2), 70)
        self.assertNotIn("ze", V.MAPA_B70)

    def test_kuhn_recebido_sem_divisao(self):
        v = V.RecebidoKuhn().treinar(400)
        self.assertLess(v, -0.2)                         # ~6 × (−1/18): a soma das 6 distribuições
        self.assertAlmostEqual(v / 6, -1 / 18, delta=0.01)

    def test_aadd_recebido(self):
        ing, aadd, prec = V.recebido_aadd(seed=5)
        self.assertGreater(ing, 0.9)
        self.assertLess(aadd, 0.06)
        self.assertEqual(prec, 1.0)                      # o "auditor forense" não aprende nada

    def test_murphy_completa(self):
        rng = random.Random(9)
        p = [rng.random() for _ in range(2000)]
        y = [int(rng.random() < q ** 1.5) for q in p]
        m = V.MurphyCompleta.decompor(p, y)
        self.assertTrue(all(m[k] > 0 for k in ("rel", "res", "unc", "wbv")))
        self.assertAlmostEqual(m["soma"], m["brier"], places=12)

    def test_componentes_principais(self):
        rng = random.Random(3)
        dados = [[rng.gauss(0, 5), rng.gauss(0, 1), rng.gauss(0, 0.1)] for _ in range(500)]
        d = V.componentes_principais(dados, 1)[0]
        self.assertGreater(abs(d[0]), 0.99)

    def test_sonda_e_potencial(self):
        s = V.SondaColapso.experimento()
        self.assertGreater(s["retencao_supervisionada"], 0.9)
        self.assertLess(s["retencao_pca"], 0.3)
        r = V.ModelagemPorPotencial.comparar(sementes=10)
        self.assertEqual(r["politica_preservada_potencial"], 1.0)

    def test_kl_beta(self):
        self.assertAlmostEqual(V.kl_beta(3, 4, 3, 4), 0.0, places=12)
        self.assertGreater(V.kl_beta(3, 4, 4, 3), 0)


class TesteParte122(unittest.TestCase):
    def test_p3101(self):
        d = calculos.p3101_defeitos_recebidos_v30(sementes=range(3), iteracoes_kuhn=50)
        self.assertEqual(d["forense_diferente_de_1"], 0)
        self.assertEqual(d["colisoes_b70"], 70)
        self.assertLess(d["sab_aadd"], d["sab_ingenuo"])

    def test_p3102(self):
        c = calculos.p3102_pecas_corrigidas_v30(n_mdps=3)
        self.assertLess(c["murphy_fecha"], 1e-12)
        self.assertEqual(c["potencial_preserva"], 3)
        self.assertLess(c["kl_erro"], 1e-6)

    def test_p3103_rodada89(self):
        e, v = calculos.p3103_rodada89()
        self.assertLess(e, 1e-15)
        self.assertEqual(len(v), 7)

    def test_p1961_com_parte_122(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[122], (15, 16))
        self.assertEqual((ok, tot), (297, 325))


if __name__ == "__main__":
    unittest.main()
