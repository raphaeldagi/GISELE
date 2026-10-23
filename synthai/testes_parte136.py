"""Testes da Parte 136: synthai/passos.py (a quadrática de objetivos_cognitivos.py, os passos de inovacao_guiada.py, o auditor de
capacidades) e as funções P3177–P3180 pelo nome."""
import math
import random
import unittest

import calculos as c
from synthai import passos as p


class TestesPassos(unittest.TestCase):
    def test_quadratica_espectro(self):
        A, lam, Q = p.quadratica_anisotropica(5, 20.0, 3)
        self.assertAlmostEqual(lam[0], 1.0)
        self.assertAlmostEqual(lam[-1], 20.0)
        for i in range(5):
            Av = [sum(A[r][k] * Q[i][k] for k in range(5)) for r in range(5)]
            for r in range(5):
                self.assertAlmostEqual(Av[r], lam[i] * Q[i][r], places=12)

    def test_fixo_igual_a_forma_fechada(self):
        A, lam, Q = p.quadratica_anisotropica(4, 7.0, 11)
        x0, alvo = [0.3, -1.2, 0.8, 2.0], [0.1, 0.0, -0.4, 0.5]
        cs = p.descer(A, x0, alvo, 10, metodo="fixo", passo=0.03)
        self.assertAlmostEqual(cs[-1] / cs[0], p.razao_fixo_fechada(lam, p.coordenadas_proprias(Q, x0, alvo), 0.03, 10), places=12)

    def test_media_igual_a_recorrencia_por_modo(self):
        A, lam, Q = p.quadratica_anisotropica(4, 7.0, 11)
        x0, alvo = [0.3, -1.2, 0.8, 2.0], [0.0] * 4
        cs = p.descer(A, x0, alvo, 12, metodo="media", passo=0.03, beta=0.5)
        rec = p.razao_media_por_modo(lam, p.coordenadas_proprias(Q, x0, alvo), 0.03, 0.5, 12)
        self.assertLess(abs(cs[-1] / cs[0] - rec) / rec, 1e-9)

    def test_passo_secante_protegido(self):
        self.assertEqual(p.passo_secante(None, None, 0.05), (0.05, False))
        self.assertEqual(p.passo_secante([1.0, 0.0], [-1.0, 0.0], 0.05), (0.05, False))  # s·y < 0: sem curvatura
        self.assertEqual(p.passo_secante([1.0, 0.0], [4.0, 0.0], 0.05), (0.8 * 1.0 / 4.0, True))
        self.assertEqual(p.passo_secante([1.0, 0.0], [0.5, 0.0], 0.05), (0.4, True))  # recortado no máximo

    def test_limite_da_norma(self):
        A, _, _ = p.quadratica_anisotropica(3, 2.0, 1)
        cs = p.descer(A, [10.0, 0.0, 0.0], [0.0] * 3, 1, metodo="fixo", passo=1.0, limite=0.1)
        self.assertLess(cs[1], cs[0])

    def test_raio_media(self):
        # λ = 1, η = 0,05, β = 0,6: z² − 1,34z + 0,4 = 0, maior raiz (1,34 + √0,1956)/2
        self.assertAlmostEqual(p.raio_media(1.0, 0.05, 0.6), (1.34 + math.sqrt(1.34 ** 2 - 1.6)) / 2, places=14)
        self.assertEqual(p.ganhos_por_modo([10.0], 0.05, 0.6, 24), [math.inf])

    def test_variancia_media_exponencial(self):
        self.assertAlmostEqual(p.variancia_media_exponencial(0.5, n=60000, semente=2), 0.5 / 1.5, delta=0.01)

    def test_soma_sequencial(self):
        self.assertEqual(p._soma([1e16, 1.0, -1e16]), 0.0)  # o sum() compensado daria 1.0


class TestesAuditor(unittest.TestCase):
    def test_defeitos_plantados(self):
        a = p.auditar_capacidades("import subprocess, pickle\nimport os\nsubprocess.Popen(['x'])\nos.system('ls')\nos.fork()\n"
                                  "eval('1')\nexec('x=1')\n__import__('os')\npickle.loads(b'')\nspec.loader.exec_module(m)\n"
                                  "import requests\nimport nltk\nnltk.download('wordnet')\n")
        self.assertIn("chamada:subprocess.Popen", a["processo"])
        self.assertIn("chamada:os.system", a["processo"])
        self.assertIn("chamada:os.fork", a["processo"])
        for k in ("chamada:eval", "chamada:exec", "chamada:__import__", "chamada:spec.loader.exec_module"):
            self.assertIn(k, a["dinamico"])
        self.assertIn("chamada:pickle.loads", a["desserializacao"])
        self.assertIn("import:requests", a["rede"])
        self.assertIn("chamada:nltk.download", a["rede"])

    def test_caso_limpo(self):
        self.assertEqual(p.auditar_capacidades("s = 'subprocess.Popen eval( exec( urllib.request'\nimport math, json\n"
                                               "from urllib.parse import quote\nimport nltk\nfrom nltk.corpus import wordnet\n"), {})

    def test_nao_analisavel(self):
        self.assertIn("nao_analisavel", p.auditar_capacidades("def f(:\n"))

    def test_proprio_fonte(self):
        with open(p.__file__, encoding="utf-8") as f:
            self.assertEqual(p.auditar_capacidades(f.read()), {})


class TestesFuncoesParte136(unittest.TestCase):
    def test_p3177_passo_fixo_e_secante(self):
        r = c.p3177_passo_fixo_e_secante()
        self.assertLess(r["erro_rel"], 1e-10)
        self.assertAlmostEqual(r["fechada"], -4.7891, places=3)
        self.assertLess(r["secante"], -11.0)
        self.assertAlmostEqual(r["media_menos_fixo"], -0.405, places=2)

    def test_p3178_ruido_e_media(self):
        v, vf, cm, piso = c.p3178_ruido_e_media()
        self.assertAlmostEqual(vf, 0.6 / 1.4, places=12)
        self.assertLess(abs(v - vf), 0.0026)
        self.assertLess(abs(cm / piso - 1), 0.07)

    def test_p3179_capacidades_recebidas(self):
        proprio, por, com, com_pac, nao = c.p3179_capacidades_recebidas()
        self.assertEqual((proprio, com, com_pac, nao), ({}, 6, 0, 1))

    def test_p3180_media_por_modo(self):
        r = c.p3180_media_por_modo()
        self.assertEqual(len(r), 4)
        for erro, d, dentro in r:
            self.assertLess(erro, 1e-9)
            self.assertTrue(dentro)


if __name__ == "__main__":
    unittest.main()
