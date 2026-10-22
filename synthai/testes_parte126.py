"""Testes da Parte 126: as medidas de um lote de textos (P3151–P3154), chamadas pelo nome."""

import os
import tempfile
import unittest

import calculos as c


class TestesParte126(unittest.TestCase):
    def test_p3151_lote_de_textos(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "l.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write("um texto\n---\noutro texto\n---\n\n")
            self.assertEqual(c.p3151_lote_de_textos(p), ["um texto", "outro texto"])

    def test_p3152_medir_lote(self):
        textos = ["eu vejo a casa azul. quem vê?", "eu vejo a casa verde. de novo.", "eu vejo a casa e o mar?"]
        m = c.p3152_medir_lote(textos)
        self.assertEqual(m["repetidos"], [("eu vejo a", 3), ("vejo a casa", 3)])
        self.assertAlmostEqual(m["perguntas"], 2 / 5)        # 5 frases, 2 com "?"
        self.assertAlmostEqual(m["autorref"], 3 / 21)
        # novidade do 2º: trigramas {eu vejo a, vejo a casa, a casa verde, casa verde de, verde de novo}; 2 vistos → 3/5
        self.assertAlmostEqual(m["novidade"][0], 3 / 5)
        self.assertEqual(len(m["bits"]), 2)

    def test_p3153_cruzado(self):
        x = c.p3153_cruzado(["a b c d"], ["a b c e"])
        self.assertAlmostEqual(x["trigramas_herdados"], 1 / 2)
        self.assertGreater(x["bits"], 0)

    def test_p3154_moldes(self):
        textos = ["talvez sim. então não.", "nada aqui. curto.", "a consciência da consciência. fim.", "mais um texto. e outro aqui."]
        mo = c.p3154_moldes(textos)
        self.assertAlmostEqual(mo["talvez"], 0.25)
        self.assertAlmostEqual(mo["entao"], 0.25)
        self.assertAlmostEqual(mo["cdc"], 0.25)
        self.assertIn("t_novidade", mo)

    def test_lote1_regressao(self):
        m = c.p3152_medir_lote(c.p3151_lote_de_textos("textos_parte126/lote1.txt"))
        self.assertEqual(m["repetidos"][0], ("consciência da consciência", 11))


if __name__ == "__main__":
    unittest.main()
