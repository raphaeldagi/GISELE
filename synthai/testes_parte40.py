"""Testes de unidade da Parte 40 (o português no data lake): `python3 -m unittest synthai.testes_parte40`."""

import unittest

from .dicionario import DicionarioPT


class TesteDicionarioPT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = DicionarioPT()

    def test_cao_e_o_mesmo_sinset_do_ingles(self):
        self.assertEqual(self.d.lemas["02084071-n"], ["cachorro", "cão"])
        self.assertIn("Canis", self.d.glosas["02084071-n"])

    def test_fichas_e_plurais(self):
        self.assertEqual(DicionarioPT.fichas("Os cães latem à noite"), ["cães", "latem", "noite"])
        self.assertEqual(self.d.lema("cães"), "cão")
        self.assertEqual(self.d.lema("animais"), "animal")
        self.assertEqual(self.d.lema("cães", plurais=False), None)

    def test_grafo_sem_laco(self):
        defs = self.d.grafo_de_definicoes()
        self.assertIn("cão", defs)
        self.assertNotIn("cão", defs["cão"])
        self.assertTrue(all(isinstance(s, set) for s in defs.values()))


if __name__ == "__main__":
    unittest.main()
