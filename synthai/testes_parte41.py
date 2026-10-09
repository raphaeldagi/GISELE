"""Testes de unidade da Parte 41 (metacognição medida): `python3 -m unittest synthai.testes_parte41`."""

import unittest

from .metacognicao import aberturas, cosseno, falas_do_dialogo, frases, ngramas, padroes_repetidos, palavras


class TesteMetacognicao(unittest.TestCase):
    def test_palavras_e_ngramas(self):
        self.assertEqual(palavras("A conta, feita antes: 2,5 é ÓTIMO."), ["a", "conta", "feita", "antes", "é", "ótimo"])
        self.assertEqual(ngramas(["a", "b", "c"], 2), [("a", "b"), ("b", "c")])

    def test_padroes_contam_documentos_e_ocorrencias(self):
        docs = ["a conta feita antes a conta", "a conta depois", "nada aqui"]
        top = padroes_repetidos(docs, n=2, topo=3)
        self.assertEqual(top[0], ("a conta", 2, 3))

    def test_cosseno(self):
        self.assertAlmostEqual(cosseno("a b", "a b"), 1.0)
        self.assertAlmostEqual(cosseno("a a b", "a c"), 2 / (5 ** 0.5 * 2 ** 0.5))
        self.assertEqual(cosseno("a", "b"), 0.0)

    def test_frases_aberturas_e_falas(self):
        self.assertEqual(frases("Uma frase. Outra frase! E mais"), ["Uma frase.", "Outra frase!", "E mais"])
        self.assertEqual(aberturas(["A conta. A regra. O dado."])[1][0], ("a", 2))
        texto = "**IA-Python:** Eu pergunto.\n\n**IA-Java:** Eu respondo muito.\n\n**IA-Java (a pergunta):** Outra."
        f = falas_do_dialogo(texto)
        self.assertEqual(f["IA-Python"], ["Eu pergunto."])
        self.assertEqual(len(f["IA-Java"]), 2)


if __name__ == "__main__":
    unittest.main()
