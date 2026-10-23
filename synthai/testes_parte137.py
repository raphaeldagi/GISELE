"""Testes da Parte 137: synthai/grpo_bandido.py (de externos/pacote3/rl_grupos.py), synthai/reservatorio.py (de
externos/pacote3/aprendizagem_continua.py) e as funções P3181–P3183 pelo nome."""
import math
import unittest

import calculos as c
from synthai import grpo_bandido as g
from synthai import reservatorio as r


class TestesGRPO(unittest.TestCase):
    def test_vantagem_sem_contraste_e_zero(self):
        self.assertEqual(g.vantagens_grupo([1.0, 1.0, 1.0]), [0.0, 0.0, 0.0])
        self.assertEqual(g.vantagens_grupo([0.0, 0.0]), [0.0, 0.0])

    def test_vantagem_binaria_fechada(self):
        v = g.vantagens_grupo([1.0, 0.0, 0.0, 0.0])
        a, b = g.vantagens_binarias_fechadas(4, 1)
        self.assertAlmostEqual(a, math.sqrt(3.0))
        self.assertAlmostEqual(v[0], a, places=6)
        self.assertAlmostEqual(v[1], b, places=6)
        self.assertAlmostEqual(sum(v), 0.0, places=12)

    def test_prob_sem_contraste(self):
        self.assertAlmostEqual(g.prob_sem_contraste(1 / 3, 2), 5 / 9)
        self.assertAlmostEqual(g.prob_sem_contraste(0.5, 3), 0.25)

    def test_log_softmax_normaliza(self):
        lp = g.log_softmax([1.0, -2.0, 0.5])
        self.assertAlmostEqual(sum(math.exp(v) for v in lp), 1.0, places=14)

    def test_oraculo_e_recompensa(self):
        f = g.features(0.5, -0.5)
        z = [sum(f[i] * g.ORACULO[i][a] for i in range(5)) for a in range(3)]
        self.assertEqual(g.acao_otima(f), max(range(3), key=lambda a: z[a]))

    def test_gradiente_kl_zero_na_uniforme_sem_vantagem(self):
        pesos = [[0.0] * 3 for _ in range(5)]
        f = g.features(0.3, 0.2)
        lv = g.log_softmax(g.logits(pesos, f))
        grad = g.gradiente(pesos, f, [0, 1], [lv[0], lv[1]], [0.0, 0.0])
        self.assertTrue(all(abs(x) < 1e-15 for l in grad for x in l))

    def test_treinar_melhora_a_uniforme(self):
        tr, te = g.gerar_contextos(64, 1), g.gerar_contextos(64, 2)
        w, _, n = g.treinar(tr, 4, 512, semente=3)
        self.assertEqual(n, 128)
        self.assertGreater(g.retorno_esperado(w, te), g.retorno_esperado([[0.0] * 3 for _ in range(5)], te))


class TestesReservatorio(unittest.TestCase):
    def test_reservatorio_tamanho_e_conteudo(self):
        res = r.Reservatorio(10, semente=1)
        for i in range(100):
            res.adicionar(i)
        self.assertEqual(len(res.itens), 10)
        self.assertEqual(len(set(res.itens)), 10)
        self.assertEqual(res.vistos, 100)

    def test_reservatorio_curto_guarda_tudo(self):
        res = r.Reservatorio(10)
        for i in range(7):
            res.adicionar(i)
        self.assertEqual(res.itens, list(range(7)))

    def test_posto_efetivo_iguais(self):
        # colunas ortogonais de média zero e mesma norma: posto efetivo = número de colunas
        H = [[1.0, 1.0], [1.0, -1.0], [-1.0, 1.0], [-1.0, -1.0]]
        self.assertAlmostEqual(r.posto_efetivo(H), 2.0, places=12)

    def test_posto_efetivo_nulo(self):
        self.assertEqual(r.posto_efetivo([[1.0, 2.0], [1.0, 2.0]]), 0.0)

    def test_fracao_dormente(self):
        self.assertEqual(r.fracao_dormente([[1.0, 0.0, 2.0], [1.0, 0.0, 2.0]]), 1 / 3)
        self.assertEqual(r.fracao_dormente([[0.0, 0.0]]), 1.0)

    def test_esquecimento(self):
        R = [[0.9, 0.1, 0.0], [0.7, 0.8, 0.2], [0.5, 0.85, 0.9]]
        e = r.esquecimento(R)
        self.assertAlmostEqual(e[0], 0.9 - 0.5)
        self.assertAlmostEqual(e[1], 0.8 - 0.85)


class TestesFuncoesParte137(unittest.TestCase):
    def test_p3181_vantagem_e_contraste(self):
        erro, sem = c.p3181_vantagem_e_contraste(n_grupos=2000)
        self.assertLess(erro, 2e-7)
        self.assertAlmostEqual(sem[2][1], 5 / 9)
        self.assertLess(abs(sem[2][0] - 5 / 9), 0.04)

    def test_p3182_grpo_g2_g8(self):
        out, dif = c.p3182_grpo_g2_g8()
        self.assertAlmostEqual(out[2][0], 0.9086, places=3)
        self.assertAlmostEqual(out[8][0], 0.8987, places=3)
        self.assertGreater(dif, 0.0)

    def test_p3183_reservatorio_e_posto(self):
        m, f, e, posto = c.p3183_reservatorio_e_posto(fluxos=200)
        self.assertLess(abs(m - 32), 1.5)
        self.assertLess(e, 1e-9)


if __name__ == "__main__":
    unittest.main()
