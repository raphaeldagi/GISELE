"""Testes de unidade do `dicionario` (Parte 30): `python3 -m unittest synthai.testes_dicionario`."""

import unittest
from math import log2

from .dicionario import Dicionario, componentes_fortes, entropia, fecho, minset_guloso, nucleo, zipf
from .testes import acessos_escondidos

# um dicionário de brinquedo: "a" e "b" se definem um pelo outro (um círculo); "c" se define por "a";
# "d" por "c" e "b"; "e" ninguém usa para definir nada
BRINQUEDO = {"a": {"b"}, "b": {"a"}, "c": {"a"}, "d": {"c", "b"}, "e": {"d"}}


class TesteDicionario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = Dicionario()

    def test_tamanho_do_wordnet(self):
        self.assertEqual(len(self.d.sinsets), 117659)

    def test_morphy(self):
        for flexionada, base in (("children", "child"), ("cities", "city"), ("geese", "goose"), ("wolves", "wolf")):
            self.assertEqual(self.d.morphy(flexionada), base)
        self.assertIsNone(self.d.morphy("xqzzv"))

    def test_definicao_sem_exemplos(self):
        self.assertEqual(Dicionario.definicao('a dog; "the dog barked"').strip(), "a dog")

    def test_nucleo_do_brinquedo(self):
        self.assertEqual(nucleo(BRINQUEDO), {"a", "b"})

    def test_componentes_fortes(self):
        comps = componentes_fortes(set(BRINQUEDO), BRINQUEDO)
        self.assertIn({"a", "b"}, comps)
        self.assertEqual(sum(len(c) for c in comps), 5)

    def test_minset_quebra_os_ciclos_e_o_fecho_define_tudo(self):
        ms = minset_guloso(set(BRINQUEDO), BRINQUEDO)
        self.assertEqual(len(ms), 1)
        conhecidas, rodadas = fecho(ms, BRINQUEDO)
        self.assertEqual(conhecidas, set(BRINQUEDO))
        self.assertEqual(rodadas, 4)  # b (ou a) -> o outro -> c -> d -> e

    def test_zipf_e_entropia(self):
        self.assertAlmostEqual(zipf([10 ** 6 / r for r in range(1, 20001)]), 1.0, places=6)
        self.assertAlmostEqual(entropia([1] * 26), log2(26))

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("dicionario"), [])


if __name__ == "__main__":
    unittest.main()
