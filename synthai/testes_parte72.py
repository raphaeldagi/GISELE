"""Testes de unidade da Parte 72 (o que está disfuncional): `python3 -m unittest synthai.testes_parte72`. Cada pNN nova chamada PELO NOME."""

import math
import unittest

import calculos


class Mini:
    # três sinsets: "knowledge" definido com "information", "information" sem "knowledge"; sinônimos a/b
    sinsets = [("n", ["knowledge"], [], "g0"), ("n", ["information", "info"], [], "g1"), ("n", ["a", "b"], [], "g2")]
    _defs = {"g0": "information acquired by study", "g1": "a message received", "g2": "letters"}

    def definicao(self, g):
        return self._defs[g]


class TesteParte72(unittest.TestCase):
    def test_p1601_auditoria_do_repositorio(self):
        defeitos = calculos.p1601_auditoria_do_repositorio(71)
        self.assertEqual(set(defeitos), {"docs", "sem_teste", "testes_fora_da_lista", "rodadas_sem_java", "partes_fora_do_resultados", "constantes"})
        self.assertEqual(defeitos["rodadas_sem_java"], [])
        self.assertEqual(defeitos["constantes"], [])

    def test_p1602_entropia_de_unigrama(self):
        # "aab": p = 2/3, 1/3; H = −(2/3)log₂(2/3) − (1/3)log₂(1/3) = 0,9183; 2 símbolos: redundância 1 − H/1; contra 8 bits: 1 − H/8
        h, n, r, r8 = calculos.p1602_entropia_de_unigrama("aab")
        hh = -(2 / 3) * math.log2(2 / 3) - (1 / 3) * math.log2(1 / 3)
        self.assertAlmostEqual(h, hh, places=12)
        self.assertEqual(n, 2)
        self.assertAlmostEqual(r, 1 - hh, places=12)
        self.assertAlmostEqual(r8, 1 - hh / 8, places=12)

    def test_p1603_ciclos_de_glosas(self):
        r = calculos.p1603_ciclos_de_glosas((("information", "knowledge"),), Mini())
        self.assertEqual(r, [("information", "knowledge", True, False)])

    def test_p1604_hash_como_peso(self):
        ms, mr, z = calculos.p1604_hash_como_peso(50, 1, Mini())
        self.assertAlmostEqual(z, (ms - mr) / math.sqrt(2 / 18 / 50), places=12)
        self.assertTrue(0 <= ms <= 1 and 0 <= mr <= 1)


    def test_p1608_auditoria_estatica(self):
        # o texto recebido: run_tests tem 6 verificações e declara 6; test_engine tem 7 (5 asserts + 2 por exceção no laço de duas) e declara 8
        self.assertEqual(calculos.p1608_auditoria_estatica(), [("run_tests", 6, 4, 6), ("test_engine", 7, 5, 8)])

    def test_p1609_horn_linear(self):
        # regra de duas premissas (a, b ⇒ c), premissa repetida (c, c ⇒ d), ciclo sem fato (x ⇒ y, y ⇒ x) e regra sem premissa (⇒ e)
        regras = [(("a", "b"), "c"), (("c", "c"), "d"), (("x",), "y"), (("y",), "x"), ((), "e")]
        ordem, prova, dec = calculos.p1609_horn_linear(["a", "b"], regras)
        self.assertEqual(ordem, ["a", "b", "e", "c", "d"])
        self.assertEqual(prova, {"a": None, "b": None, "e": 4, "c": 0, "d": 1})
        self.assertEqual(dec, 3)
        self.assertEqual(calculos.p1609_horn_linear(["a"], regras)[0], ["a", "e"])

    def test_p1610_horn_ingenuo(self):
        # regras em ordem desfavorável: c ⇒ d antes de b ⇒ c antes de a ⇒ b: três passagens que mudam e uma que não muda
        regras = [(("c",), "d"), (("b",), "c"), (("a",), "b")]
        conhecidos, passagens, checagens = calculos.p1610_horn_ingenuo(["a"], regras)
        self.assertEqual((conhecidos, passagens), ({"a", "b", "c", "d"}, 4))
        self.assertEqual(checagens, 3 + 2 + 1)

    def test_p1611_regras_de_animal(self):
        fatos, regras = calculos.p1611_regras_de_animal()
        self.assertEqual(len(regras), 84427)
        self.assertTrue(all(len(p) == 1 for p, _ in regras))

    def test_p1612_animais_por_horn(self):
        self.assertEqual(calculos.p1612_animais_por_horn()[:4], (4017, True, True, 4))

    def test_p1613_fecho_horn(self):
        self.assertEqual(calculos.p1613_fecho_horn("person"), 10297)

    def test_p1614_rodada46(self):
        r = calculos.p1614_rodada46()
        self.assertEqual([x[1] for x in r], [4017, 10297])
        self.assertEqual(r[0][3], 4051)


    def test_p1615_imports_sem_uso(self):
        # o primeiro bloco usa json e hashlib; o segundo importa deque e não usa (a fila prometida ficou para depois)
        self.assertEqual(calculos.p1615_imports_sem_uso(), [[], ["deque"]])


if __name__ == "__main__":
    unittest.main()
