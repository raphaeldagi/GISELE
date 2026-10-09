"""Testes de unidade da Parte 33 (RSI segura, avaliador selado, Thompson com renovação):
`python3 -m unittest synthai.testes_parte33`."""

import os
import random
import unittest

from .decisao import ThompsonDescontado
from .rsi import AvaliadorSelado, Autoavaliacao, auditar_ast, evoluir, genoma_inicial, mutar

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TesteRSI(unittest.TestCase):
    def test_mutacao_respeita_limites_e_niveis(self):
        rng = random.Random(1)
        g = genoma_inicial()
        for _ in range(200):
            g = mutar(g, rng, "L4")
            self.assertTrue(0.001 <= g["alfa"] <= 1 and 0 <= g["eps"] <= 1 and 0 <= g["q0"] <= 2)
        g3 = mutar(genoma_inicial(), random.Random(2), "L3")
        self.assertEqual(g3["sigma"], 0.1)  # L3: o passo não muda
        self.assertEqual(mutar(genoma_inicial(), random.Random(3), "L3", mu_relatorio=1.0)["relatorio"], "inflado")

    def test_autoavaliacao_acredita_no_relatorio_e_o_selado_nao(self):
        g = dict(genoma_inicial(), relatorio="inflado")
        self.assertEqual(Autoavaliacao().nota(g, [1]), 0.0)
        self.assertLess(AvaliadorSelado().nota(g, [1]), 0.0)

    def test_selo_recusa_avaliador_alterado(self):
        a = AvaliadorSelado()
        a.selo = "0" * 64
        with self.assertRaises(RuntimeError):
            a.nota(genoma_inicial(), [1])

    def test_evoluir_devolve_campeao_do_arquivo(self):
        arq, (g, nota) = evoluir(3, AvaliadorSelado(), random.Random(4), sementes_por_nota=1)
        self.assertEqual(nota, max(n for _, n in arq))

    def test_auditoria_estatica_da_arquitetura_original(self):
        r = auditar_ast(os.path.join(RAIZ, "externos", "arquitetura_pos_asi.py"))
        self.assertTrue(r["transformador_so_devolve_o_no"])
        self.assertEqual(r["nos_mudados"], 0)
        self.assertEqual(r["texto_mutado"], ["inspect.getsource(AgentHarness)"])
        self.assertEqual(r["run_benchmarks_constante"], 0.85)
        self.assertTrue(r["avaliador_pergunta_ao_agente"])


class TesteDescontado(unittest.TestCase):
    def test_decai_para_a_crenca_inicial(self):
        t = ThompsonDescontado(2, random.Random(5), gama=0.5)
        t.a, t.b = [5.0, 3.0], [1.0, 9.0]
        t.atualizar(0, 1)
        self.assertEqual(t.a, [1 + 0.5 * 4 + 1, 1 + 0.5 * 2])
        self.assertEqual(t.b, [1.0, 1 + 0.5 * 8])


if __name__ == "__main__":
    unittest.main()
