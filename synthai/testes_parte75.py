"""Testes de unidade da Parte 75 (o que se prova): `python3 -m unittest synthai.testes_parte75`. Cada pNN nova chamada PELO NOME. Nenhum código do texto
recebido é executado; as funções testadas são reimplementações."""

import json
import unittest

import calculos


class TesteParte75(unittest.TestCase):
    def test_extracao_com_e_sem_espaco(self):
        # o json.dumps padrão põe ": " entre chave e valor, e a busca do Java procura ":" sem espaço
        self.assertEqual(calculos._java_extract_json_field(json.dumps({"k": "AB"}), "k"), "")
        self.assertEqual(calculos._java_extract_json_field(json.dumps({"k": "AB"}, separators=(",", ":")), "k"), "AB")

    def test_nucleo_utilidade(self):
        # 42 caracteres em 2 linhas: (42 div 4)/(2 + 1) − 0,5 = 10/3 − 0,5; código vazio: −1
        self.assertEqual(calculos._nucleo_utilidade("def compute_factor(x, y):\n    return x * y", "reasoning"), (True, 10 / 3 - 0.5))
        self.assertEqual(calculos._nucleo_utilidade("", ""), (False, -1.0))
        # o split do Java descarta as linhas vazias do fim: "a\n\n" tem 1 linha
        self.assertEqual(calculos._nucleo_utilidade("abcdefgh\n\n", "x")[1], (10 // 4) / 2 - 0.5)

    def test_mutacao(self):
        self.assertEqual(calculos._mutar_soma_em_produto("def f(a, b):\n    return a + b - 1"), ("def f(a, b):\n    return a * b - 1", 1))

    def test_p1691_laco_de_auto_modificacao(self):
        padrao = calculos.p1691_laco_de_auto_modificacao(geracoes=3)
        self.assertEqual([x[:3] for x in padrao], [(False, False, -1.0)] * 3)
        corr = calculos.p1691_laco_de_auto_modificacao(geracoes=3, separador_corrigido=True)
        self.assertEqual(len({x[3] for x in corr}), 1)

    def test_p1692_godel_nas_funcoes(self):
        n, a, m, am = calculos.p1692_godel_nas_funcoes()
        self.assertEqual(a, n)
        self.assertEqual(am, m)

    def test_p1693_godel_no_pacote(self):
        n, a, m = calculos.p1693_godel_no_pacote()
        self.assertEqual(a, n)
        self.assertLess(m, n)

    def test_p1694_verificador_do_texto(self):
        sc, ordem, v, melhor, vmax = calculos.p1694_verificador_do_texto()
        self.assertAlmostEqual(sc["A"], 0.8 * 0.9 / 2, places=15)
        self.assertEqual((ordem, melhor), (["B", "A"], ("A", "B")))
        self.assertAlmostEqual(v, vmax, places=15)


if __name__ == "__main__":
    unittest.main()
