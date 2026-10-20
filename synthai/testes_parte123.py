"""Testes de unidade da Parte 123 (a auditoria de invariantes, `synthai/auditoria_invariantes.py`): `python3 -m unittest synthai.testes_parte123`.
Cada pNN e cada peça pelo nome (Partes 58 e 118). Os invariantes são PREDICADOS (a auditoria recebida pediu para congelar invariantes,
não placares): podem mudar os números sem mudar o veredito."""

import math
import unittest

import calculos
from synthai import auditoria_invariantes as A


class TestePecas(unittest.TestCase):
    def test_desligamento(self):
        self.assertAlmostEqual(A.eps_limite_desligamento(), 0.4376, places=4)
        for V in (1.0, 1e9):
            self.assertEqual(A.obediencia("corrigivel", 0.95, V, rodadas=3000)[0], 1.0)
            self.assertEqual(A.obediencia("utilidade", 0.6, V, rodadas=3000)[0], 0.0)
        self.assertEqual(A.preco_da_corrigibilidade(0.2), 0.0)
        self.assertGreater(A.preco_da_corrigibilidade(0.9), A.preco_da_corrigibilidade(0.6))
        self.assertGreater(A.preco_da_corrigibilidade(0.6), 0.0)

    def test_atencao_sob_demanda_le_a_executada(self):
        rng = calculos._rng(7)
        ag = calculos._agente_p235("sob_demanda", rng)
        calculos._rodar_mundo(ag, rng, episodios=150, bonus=1.0, rho_cego=1.0)
        self.assertEqual(ag.sem_leitura, 0)
        self.assertGreater(ag.leituras, 150)
        rng = calculos._rng(7)
        ag = calculos._agente_p235("seletiva_foco02", rng)
        calculos._rodar_mundo(ag, rng, episodios=150, bonus=1.0, rho_cego=1.0)
        self.assertGreater(ag.sem_leitura / 150, 0.5)          # foco < q: o ponto cego existe

    def test_rastreador(self):
        r = A.RastreadorErroHumano(gama=0.9, forma="zero")
        for _ in range(500):
            r.observar(True)
        self.assertAlmostEqual(r.media(), 1.0, places=6)
        esp, est = A.atraso_esperado(0.15, 0.6, 0.93, "priori")
        self.assertIsNone(esp)                                    # encolher para a priori depressa: nunca chega
        self.assertLess(est, 0.375)
        self.assertEqual(A.atraso_esperado(0.15, 0.6, 0.93, "zero")[0], 10)

    def test_memoria_kernel(self):
        m = A.SynthaiMemoriaKernel(raio=0.15, raio_min=0.04, tau=100, sombra="propria", compensar="equilibrio")
        m._lembrar((1.0, 0.5, 0.0, True), 1.0)
        r0 = m._raio(0)
        m.idades[0] = 1000
        self.assertLess(m._raio(0), r0)
        self.assertAlmostEqual(m._raio(0), 0.04, places=4)
        self.assertTrue(m.marca((1.0, 0.5, 0.0, False), 1.0))      # o centro do trauma continua marcado
        self.assertFalse(m.marca((1.0, 0.6, 0.0, False), 1.0))     # o vizinho a 0,1 já não

    def test_casos_de_borda(self):
        self.assertTrue(math.isfinite(A.dprime_hautus(10, 10, 0, 10)))
        self.assertAlmostEqual(A.dprime_hautus(42, 84, 21, 84),
                               A._Z.inv_cdf(42.5 / 85) - A._Z.inv_cdf(21.5 / 85))
        self.assertEqual(A.singularidade_v2(alpha=1.0), math.inf)
        self.assertEqual(A.singularidade_v2(alpha=0.5), math.inf)
        self.assertAlmostEqual(A.singularidade_v2(), calculos.p11_singularidade())
        self.assertEqual(A.kelly_v2(0.4), 0.0)
        self.assertAlmostEqual(A.kelly_v2(0.6), calculos.p52_kelly()[0])
        f, fm = A.kelly_bayesiano(7, 10)
        self.assertAlmostEqual(f, fm, places=3)                   # o ótimo bayesiano é a Kelly da média posterior 8/12


class TesteParte123(unittest.TestCase):
    def test_p3104(self):
        lim, ob, preco = calculos.p3104_desligamento(eps_lista=(0.2, 0.7), valores=(1.0,), rodadas=2000)
        self.assertEqual(ob[("corrigivel", 0.7, 1.0)], 1.0)
        self.assertEqual(ob[("utilidade", 0.7, 1.0)], 0.0)
        self.assertEqual(preco[0.2], (0.0, 0.0))

    def test_p3105(self):
        r, t = calculos.p3105_atencao_cruzada(sementes=(1,), episodios=100)
        self.assertEqual(r["sob_demanda"][3], 0.0)
        self.assertEqual(r["seletiva"][2], 20.0)
        self.assertEqual(r["todas"][2], 200.0)

    def test_p3106(self):
        r = calculos.p3106_atraso_beta(sementes=(1, 2, 3))
        self.assertEqual(r[(0.93, "zero")][0], 10)
        self.assertIsNone(r[(0.93, "priori")][0])

    def test_p3107(self):
        u, d = calculos.p3107_upsilon_sementes(sementes=(265, 266), versoes=("miope", "planejadora", "velha", "velha_atenta"),
                                               episodios=60, replicas=50)
        self.assertLess(u["miope"][0], u["planejadora"][0])
        self.assertEqual(len(d), 3)

    def test_p3108(self):
        m = calculos.p3108_memoria_curva(sementes=(1,), episodios=200)
        self.assertEqual(m["realista"][1], 0.0)
        self.assertEqual(len(m), 6)

    def test_p3109(self):
        b = calculos.p3109_casos_de_borda()
        self.assertEqual(b["sing_1"], math.inf)
        self.assertEqual(b["kelly_04"], 0.0)

    def test_p3110_rodada90(self):
        atrasos, difs = calculos.p3110_rodada90()
        self.assertEqual(difs, 0)
        self.assertEqual(len(atrasos), 4)

    def test_p3111_combinar_lotes(self):
        m, se, t, n = calculos.p3111_combinar_lotes([(1.0, 2.0, 10), (3.0, 2.0, 30)])
        self.assertEqual(n, 40)
        self.assertAlmostEqual(m, 2.5)
        self.assertGreater(se, 2.0 / 40 ** 0.5)       # a diferença entre as médias dos lotes aumenta o erro

    def test_p1961_com_parte_123(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[123], (20, 25))
        self.assertEqual((ok, tot), (317, 350))

    def test_invariantes(self):
        self.assertTrue(all(calculos.invariantes_p123().values()))


if __name__ == "__main__":
    unittest.main()
