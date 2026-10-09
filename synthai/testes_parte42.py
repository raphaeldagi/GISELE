"""Testes de unidade da Parte 42 (semiótica medida): `python3 -m unittest synthai.testes_parte42`."""

import unittest

from .semiotica import comprimido, informacao_condicional, premissas_e_respostas, retorno_da_premissa, trigramas_de_forma


class TesteSemiotica(unittest.TestCase):
    def test_informacao_condicional(self):
        p = "o limite de Landauer a vinte graus " * 5
        c, i, red = informacao_condicional(p, p)
        self.assertLess(i, c)            # a resposta que repete a premissa custa menos depois dela
        self.assertGreater(red, 0.5)
        c2, i2, red2 = informacao_condicional("abc", "zq9 wx7 kj2 mm4 pp0 vv3")
        self.assertEqual(c2, comprimido("zq9 wx7 kj2 mm4 pp0 vv3"))
        self.assertLess(red2, 0.3)

    def test_premissas_e_respostas(self):
        doc = "# A\n\n### P10 (0xA). Por que dois?\n\nPorque sim.\n\n### P11 (0xB). E três?\n\nTalvez.\n\n# B\n"
        self.assertEqual(premissas_e_respostas(doc), [(10, "Por que dois?", "Porque sim."), (11, "E três?", "Talvez.")])

    def test_retorno_e_trigramas(self):
        self.assertEqual(retorno_da_premissa("O núcleo do dicionário", "o núcleo cresce"), 0.5)
        self.assertEqual(trigramas_de_forma("cão"), frozenset({"^cã", "cão", "ão$"}))


if __name__ == "__main__":
    unittest.main()
