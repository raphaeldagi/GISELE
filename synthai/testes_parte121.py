"""Testes de unidade da Parte 121 (o NEXUS–RAPHAEL 2.2.0 medido no próprio código): `python3 -m unittest synthai.testes_parte121`.
Cada pNN e cada função nova pelo nome (Partes 58 e 118), controles dos dois lados (Parte 75)."""

import hashlib
import math
import unittest

import calculos
from synthai import nexus_v2_2 as N


class TesteNexus22(unittest.TestCase):
    def test_megasena_fechada(self):
        f = N.megasena_fechada()
        self.assertEqual(f["total"], 50063860)
        self.assertAlmostEqual(f["acertos"], 0.6, places=12)
        self.assertAlmostEqual(f["e_qui2"], 54.0, places=12)

    def test_pontuar_recebido(self):
        # Caso com todos os termos diferentes de zero: Brier 0,15, ECE |0,15-0| e |0,85-1| = 0,15.
        r = N.recebido_pontuar([0.1, 0.2, 0.8, 0.9], [0, 0, 1, 1])
        self.assertAlmostEqual(r["brier"], (0.01 + 0.04 + 0.04 + 0.01) / 4)
        self.assertAlmostEqual(r["ece"], 0.15)
        self.assertEqual(r["acuracia"], 1.0)
        self.assertAlmostEqual(r["log_loss"], -(math.log(0.9) + math.log(0.8)) / 2)

    def test_ic_por_quantis(self):
        r = list(range(2000))
        lo, hi = N.ic_por_quantis(r)
        self.assertEqual((lo, hi), (49, 1949))           # 2,5% e 97,5% das 2.000 réplicas, não os índices fixos 24 e 974

    def test_velha_por_dois_caminhos(self):
        self.assertEqual(N.estados_velha_por_camadas(), N.recebido_contar_estados_velha())
        self.assertEqual(N.valor_velha_alfa_beta("XX.OO....", "X"), 1)   # controle: X ganha jogando na casa 2
        self.assertEqual(N.valor_velha_alfa_beta(), 0)

    def test_digest_fatiado_do_texto_colado(self):
        # o texto colado fazia hash_obj.digest[:4] (o MÉTODO, não o resultado): reproduzo a expressão para mostrar o TypeError
        h = hashlib.sha256(b"42:contexto")
        with self.assertRaises(TypeError):
            h.digest[:4]
        self.assertEqual(len(h.digest()[:4]), 4)        # controle: chamando digest() funciona

    def test_logistica_e_lyapunov(self):
        m = N.RecebidaLogistica(1)
        self.assertEqual(m.predizer([0.3]), 0.5)
        self.assertAlmostEqual(N.recebido_lyapunov(4.0), math.log(2), delta=0.03)
        self.assertLess(N.recebido_lyapunov(3.2), 0)    # controle: regime periódico


class TesteParte121(unittest.TestCase):
    def test_p3071_experimentos_do_nexus_2_2(self):
        d = calculos.p3071_experimentos_do_nexus_2_2()
        self.assertTrue(0.069 <= d["ganho_m3_s0"] <= 0.176)
        self.assertEqual(d["vereditos_m3"].count("ACEITA"), 4)     # (b) previu 5 e errou: a falha fica no placar (Parte 74)
        self.assertTrue(0.19 <= d["ganho_m2"] <= 0.28)
        self.assertEqual(d["m2_ic_positivo"], 5)
        self.assertEqual(d["deltas_m7"].count(0.0), 4)              # (j) previu 5 e errou

    def test_p3072_megasena(self):
        m = calculos.p3072_megasena()
        self.assertTrue(0.533 <= m["medias"]["aleatoria"] <= 0.667)
        self.assertTrue(-0.094 <= m["delta"] <= 0.094)
        self.assertTrue(37.9 <= m["qui2"] <= 70.1)
        self.assertTrue(m["indexerror_500"])
        self.assertTrue(m["sup_2000_abaixo_mediana"])

    def test_p3073_jogos_e_dinamica(self):
        e1, e2, v, lam = calculos.p3073_jogos_e_dinamica()
        self.assertEqual((e1 - e2, v), (0, 0))
        self.assertTrue(0.67 <= lam <= 0.72)

    def test_p3074_adendo(self):
        ex, od, ac = calculos.p3074_adendo()
        self.assertTrue(-0.022 <= ex - od <= 0.022)
        self.assertFalse(0.957 <= ac <= 0.981)                      # (r) errou: 0,93

    def test_p3075_rodada87(self):
        b1, b2 = calculos.p3075_rodada87()
        self.assertLess(b2, b1)

    def test_p1961_com_parte_121(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[121], (13, 16))
        self.assertEqual((ok, tot), (274, 300))


if __name__ == "__main__":
    unittest.main()
