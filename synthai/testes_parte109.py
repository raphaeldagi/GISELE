"""Testes de unidade da Parte 109 (o NEXUS anexado): `python3 -m unittest synthai.testes_parte109`. Um teste por defeito achado no código recebido
(regra da Parte 72) e controles dos dois lados para cada auditor (regra da Parte 75)."""

import inspect
import unittest
from fractions import Fraction

import calculos
from synthai import nexus


class TesteParte109(unittest.TestCase):
    def test_p2711_blobs_pickle_do_r37(self):
        nb, nsha, gl, per = calculos.p2711_blobs_pickle_do_r37()
        self.assertEqual(nb, 18)
        self.assertEqual(nsha, 18)
        self.assertEqual(per, [])
        self.assertTrue(all(m.startswith("numpy") for m, _ in gl))

    def test_p2711b_controle_do_auditor_de_pickle(self):
        plantado, limpo = calculos.p2711b_controle_do_auditor_de_pickle()
        self.assertGreaterEqual(plantado, 1)   # o os.system plantado TEM de ser acusado
        self.assertEqual(limpo, 0)             # o caso limpo TEM de passar

    def test_p2712_nexus_se_acusa(self):
        txt, erros, ast_col, ast_re = calculos.p2712_nexus_se_acusa()
        self.assertEqual(txt, ["exec", "eval", "backdoor_marker"])   # defeito 2 do original: a regex acusa as proprias strings
        self.assertEqual(len(erros), 2)
        self.assertEqual(ast_col, ["chamada:urlopen", "import:urllib"])
        self.assertEqual(ast_re, [])   # defeito 1 corrigido: a versao anexada nao tem rede

    def test_auditor_ast_controles(self):
        # controle dos dois lados: chamadas reais sao acusadas; re.compile, asyncio.run e strings nao
        sujo = "import subprocess\nsubprocess.run(['x'])\neval('1')\nos.system('x')\n"
        limpo = "import re, asyncio\nre.compile('a')\nasyncio.run(f())\ns = 'exec(' + 'eval('\n"
        self.assertEqual(nexus.security_audit_ast(sujo), ["chamada:eval", "chamada:run", "chamada:system", "import:subprocess"])
        self.assertEqual(nexus.security_audit_ast(limpo), [])
        self.assertEqual(nexus.security_audit_texto(limpo), ["exec", "eval"])   # o auditor por texto erra no mesmo caso limpo

    def test_dicionario_sem_rede(self):
        dc = nexus.DictionaryClient()
        self.assertEqual(dc.lookup("Nexus")["source"], "offline")
        self.assertEqual(dc.lookup("zzz"), {"source": "offline-miss", "entry": None, "network": False})
        # pela AST, não pelo texto: a 1ª versão deste teste procurava a STRING "urllib" e falhava no próprio conjunto de imports perigosos
        # do auditor, o mesmo defeito que a Parte 109 aponta no NEXUS recebido
        import ast
        mods = {a.name.split(".")[0] for n in ast.walk(ast.parse(inspect.getsource(nexus))) if isinstance(n, ast.Import) for a in n.names}
        mods |= {(n.module or "").split(".")[0] for n in ast.walk(ast.parse(inspect.getsource(nexus))) if isinstance(n, ast.ImportFrom)}
        self.assertFalse(mods & {"urllib", "http", "socket", "subprocess", "multiprocessing"})

    def test_p2713_kuhn_exato(self):
        vk, sim, v1 = calculos.p2713_kuhn_exato()
        self.assertEqual(vk, Fraction(-1, 12))
        self.assertEqual(v1, Fraction(0))
        self.assertEqual(nexus.kuhn_exato(Fraction(0)), Fraction(-1, 6))   # caso com todos os termos != 0 na outra ponta (regra da Parte 30)
        self.assertLess(abs(sim - (-1 / 12)), 0.25)

    def test_p2714_desvio_da_curva_preditiva(self):
        da, d0, g0 = calculos.p2714_desvio_da_curva_preditiva()
        self.assertEqual((da, d0, g0), (0, 0, 0))   # a agenda original decide sozinha: o P0 nunca vence

    def test_raphael_reproduz_o_original(self):
        # quem_desvia=None + agenda original = o jogo recebido (os dois desviam); o sorteio do desvio acontece em todo lance nos dois modos
        a = nexus.RaphaelGame(7, list(nexus.OFFLINE_LEXICON), 12, deviate=True).play()
        b = nexus.RaphaelGame(7, list(nexus.OFFLINE_LEXICON), 12, deviate=True, quem_desvia=0).play()
        self.assertGreaterEqual(a["unexpected_moves"], b["unexpected_moves"])

    def test_p2715_grafo_e_beta(self):
        ops, soma, bb, br = calculos.p2715_grafo_e_beta()
        self.assertEqual(ops, 910 * 2 + 1820 + 100)
        self.assertEqual(soma, 100)
        self.assertEqual(br, 0.25)
        self.assertTrue(0.176 <= bb <= 0.238)

    def test_p2716_rodada76(self):
        v05, v10 = calculos.p2716_rodada76()
        self.assertAlmostEqual(v05, -1 / 12, places=15)
        self.assertLess(abs(v10), 1e-15)

    def test_p2717_raphael_agenda_justa(self):
        gw, j0, jb = calculos.p2717_raphael_agenda_justa()
        self.assertEqual((gw, j0, jb), (59, -23, -16))

    def test_p2718_artefato_do_sorteio(self):
        tx, ce, z = calculos.p2718_artefato_do_sorteio()
        self.assertLess(abs(z), 1.96)
        self.assertGreater(ce, 2 * (6 / 60))   # a referencia certa e mais que o dobro da declarada
        self.assertAlmostEqual(nexus.chance_minimo_em(range(1, 61)), 1.0, places=12)   # o minimo cai em algum lugar

    def test_p2719_retrospecto_cem_v2(self):
        _, _, deriva = calculos.p2446_retrospecto_cem()
        kf, rod, cal = calculos.p2719_retrospecto_cem_v2()
        self.assertGreater(deriva, 0.88)                     # o defeito: a original deriva com a faixa padrao
        self.assertTrue(0.74 <= cal <= 0.88)                 # a faixa prometida (80-100) cabe no que o teste da Parte 100 pedia
        self.assertGreater(kf, 400)

    def test_p1961_com_parte_109(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 110))))
        self.assertEqual(por[109], (8, 9))
        self.assertEqual((ok, tot), (138, 155))


if __name__ == "__main__":
    unittest.main()
