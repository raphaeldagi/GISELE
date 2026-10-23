"""Testes da Parte 128: as peças da reprodução (P3171–P3173), chamadas pelo nome."""

import os
import tempfile
import unittest

import calculos as c


class TestesParte128(unittest.TestCase):
    def test_p3171_partes_de_saida(self):
        t = "P3 x = 1\n--- Parte 2 ---\nP22 y = 2\n=== Unificacao (sempre ao final) ===\nP96 n = 5\n=== Parte 126: z ===\nP3152 w = 3\n"
        d = c.p3171_partes_de_saida(t, inicio=1)
        self.assertEqual(d, {1: ["P3 x = 1"], 2: ["P22 y = 2"], 126: ["P3152 w = 3"]})
        self.assertNotIn(1, c.p3171_partes_de_saida(t))

    def test_p3172_comparar_reproducao(self):
        ref = ("P3 a = 1\n--- Parte 2 ---\nP143 memoria = 10\nP22 b = 2\nP433 laco = 5\n  (Regressao: nota escrita a mao)\n"
               "P99 mundo = 7\n=== Unificacao ===\n")
        novo = "P3 a = 1\n--- Parte 2 ---\nP143 memoria = 99\nP22 b = 2\nP433 laco = 6\nP99 mundo = 8\n=== Unificacao ===\nRegressao: 1/1\nFIM_OK status=0 segundos=1\n"
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "ref.txt"), "w", encoding="utf-8") as f:
                f.write(ref)
            with open(os.path.join(d, "bloco_1_2.txt"), "w", encoding="utf-8") as f:
                f.write(novo)
            r = c.p3172_comparar_reproducao(os.path.join(d, "ref.txt"), d)
        self.assertEqual(r["linhas"], 6)
        self.assertEqual(r["diferentes"], 4)
        self.assertEqual(r["categorias"], {"projeto": 1, "maquina": 1, "nota": 1, "mundo": 1})
        self.assertEqual(r["mundo"], [(2, "P99 mundo = 7")])
        self.assertEqual((r["blocos"], r["blocos_sem_excecao"], r["regressoes"]), (1, 1, ["Regressao: 1/1"]))

    def test_p3173_rotulo_que_mente(self):
        t = ("P1961 teste (e), Partes 80-85: 30/35 = 0.85\nP1961 teste, Partes 80-90: 30/35 = 0.85\n"
             "P1961 teste, Partes 80-95: 30/35 = 0.85\nP1961 teste, Partes 80-88: 20/25 = 0.80\n")
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "bloco_80.txt"), "w", encoding="utf-8") as f:
                f.write(t)
            self.assertEqual(c.p3173_rotulo_que_mente(d), (4, 2, 35))
            self.assertEqual(c.p3173_rotulo_que_mente(os.path.join(d, "vazia_inexistente")), (0, 0, None))

    def test_volta1_regressao(self):
        r = c.p3172_comparar_reproducao("reproducao/resultados_antes_volta1.txt", "reproducao/volta1")
        self.assertEqual(r["categorias"]["mundo"], 0)
        self.assertEqual(r["sem_referencia"], [91])

    def test_p3174_comparar_voltas(self):
        a = "P3 a = 1\n--- Parte 2 ---\nP143 m = 1\nP433 v = 1\nP99 w = 1\n=== Unificacao ===\nFIM_OK status=0 segundos=1\n"
        b = "P3 a = 1\n--- Parte 2 ---\nP143 m = 2\nP433 v = 2\nP99 w = 2\n--- Parte 3 ---\nP5 z = 0\n=== Unificacao ===\nRegressao: 2/2\nFIM_OK status=0 segundos=1\n"
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "v1"))
            os.makedirs(os.path.join(d, "v2"))
            with open(os.path.join(d, "v1", "bloco_1_2.txt"), "w", encoding="utf-8") as f:
                f.write(a)
            with open(os.path.join(d, "v2", "bloco_1_2_3.txt"), "w", encoding="utf-8") as f:
                f.write(b)
            r = c.p3174_comparar_voltas(os.path.join(d, "v1"), os.path.join(d, "v2"))
        self.assertEqual((r["linhas"], r["diferentes"]), (4, 3))
        self.assertEqual(r["categorias"], {"projeto": 1, "maquina": 1, "nota": 0, "mundo": 1})
        self.assertEqual(r["novas"], [3])
        self.assertEqual(r["regressoes"], ["Regressao: 2/2"])

    def test_volta2_regressao(self):
        r = c.p3174_comparar_voltas("reproducao/volta1", "reproducao/volta2")
        self.assertEqual((r["diferentes"], r["categorias"]["mundo"], r["novas"]), (9, 0, [128]))

    def test_volta3_regressao(self):
        r = c.p3174_comparar_voltas("reproducao/volta2", "reproducao/volta3")
        self.assertEqual((r["diferentes"], r["categorias"]["mundo"], r["novas"]), (8, 0, [129]))

    def test_p3175_arquivos_sem_uso_v2(self):
        # controles dos dois lados: 'citado_so_em_saida.txt' só aparece numa saída (tem de ser acusado);
        # 'usado.py' aparece num .py (não pode ser acusado); a própria saída não é citada por ninguém (é acusada)
        arquivos = {"principal.py": "import usado\n", "usado.py": "x = 1\n", "citado_so_em_saida.txt": "dado\n",
                    "reproducao/v1/saida.txt": "rodei citado_so_em_saida.txt e principal\n", "leia.md": "veja principal.py\n"}
        with tempfile.TemporaryDirectory() as d:
            for nome, conteudo in arquivos.items():
                os.makedirs(os.path.join(d, os.path.dirname(nome)), exist_ok=True)
                with open(os.path.join(d, nome), "w", encoding="utf-8") as f:
                    f.write(conteudo)
            soltos = c.p3175_arquivos_sem_uso_v2(raiz=d, arquivos=list(arquivos))
        self.assertEqual(soltos, ["citado_so_em_saida.txt", "leia.md", "reproducao/v1/saida.txt"])

    def test_volta4_regressao(self):
        r = c.p3174_comparar_voltas("reproducao/volta3", "reproducao/volta4")
        self.assertEqual((r["diferentes"], r["categorias"]["mundo"], r["novas"], r["blocos_sem_excecao"]), (9, 0, [130], 127))

    def test_volta5_regressao(self):
        r = c.p3174_comparar_voltas("reproducao/volta4", "reproducao/volta5")
        self.assertEqual((r["diferentes"], r["categorias"]["mundo"], r["novas"], r["blocos_sem_excecao"]), (8, 0, [131], 128))

    def test_p3176_comparar_voltas_v2(self):
        a = "P3 a = 1\n--- Parte 2 ---\nP3175 n = 1\nP99 w = 1\n=== Unificacao ===\nFIM_OK status=0 segundos=1\n"
        b = "P3 a = 1\n--- Parte 2 ---\nP3175 n = 2\nP99 w = 2\n=== Unificacao ===\nFIM_OK status=0 segundos=1\n"
        with tempfile.TemporaryDirectory() as d:
            for nome, txt in (("v1", a), ("v2", b)):
                os.makedirs(os.path.join(d, nome))
                with open(os.path.join(d, nome, "bloco_1_2.txt"), "w", encoding="utf-8") as f:
                    f.write(txt)
            r0 = c.p3174_comparar_voltas(os.path.join(d, "v1"), os.path.join(d, "v2"))
            r = c.p3176_comparar_voltas_v2(os.path.join(d, "v1"), os.path.join(d, "v2"))
        self.assertEqual(r0["categorias"]["mundo"], 2)                       # a régua antiga chama a P3175 de mundo
        self.assertEqual((r["categorias"]["mundo"], r["categorias"]["projeto"]), (1, 1))
        self.assertEqual(r["mundo"], [(2, "P99 w = 1")])                     # o mundo de verdade continua acusado

    def test_volta6_regressao(self):
        r = c.p3176_comparar_voltas_v2("reproducao/volta5", "reproducao/volta6")
        self.assertEqual((r["diferentes"], r["categorias"]["mundo"], len(r["reclassificadas"])), (9, 0, 1))

    def test_volta7_regressao(self):
        r = c.p3176_comparar_voltas_v2("reproducao/volta6", "reproducao/volta7")
        self.assertEqual((r["diferentes"], r["categorias"]["mundo"], r["novas"], r["blocos_sem_excecao"]), (9, 0, [133], 130))

    def test_volta8_regressao(self):
        r = c.p3176_comparar_voltas_v2("reproducao/volta7", "reproducao/volta8")
        self.assertEqual((r["diferentes"], r["categorias"]["mundo"], r["novas"], r["blocos_sem_excecao"]), (8, 0, [134], 131))

    def test_volta9_regressao(self):
        r = c.p3176_comparar_voltas_v2("reproducao/volta8", "reproducao/volta9")
        self.assertEqual((r["diferentes"], r["categorias"]["mundo"], r["blocos_sem_excecao"]), (17, 0, 137))


if __name__ == "__main__":
    unittest.main()
