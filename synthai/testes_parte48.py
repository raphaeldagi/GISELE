"""Testes de unidade da Parte 48: `python3 -m unittest synthai.testes_parte48`."""

import unittest

import calculos


class DicionarioFalso:
    """a -> b -> c -> b (ciclo de dois), e -> a, d sem palavra na definição (sumidouro); x não é substantivo."""

    def __init__(self):
        defs = {"a": "b x", "b": "c", "c": "b", "d": "", "e": "a"}
        self.sinsets = [("n", [w], [], g) for w, g in sorted(defs.items())] + [("v", ["x"], [], "")]
        self.lemas = {w: [i] for i, (_, ls, _, _) in enumerate(self.sinsets) for w in ls}

    @staticmethod
    def palavras_da_definicao(glosa):
        return glosa.split()


class TesteParte48(unittest.TestCase):
    def test_mapa_da_definicao(self):
        n, sumid, cic, nciclos, cauda, bacia, ciclo = calculos.p882_mapa_da_definicao(DicionarioFalso())
        # distâncias: a 1, b 0, c 0, d 0, e 2 -> 3/5; a bacia do ciclo {b, c} tem a, b, c, e = 4/5
        self.assertEqual((n, sumid, cic, nciclos, ciclo), (5, 1, 2, 1, ["b", "c"]))
        self.assertAlmostEqual(cauda, 0.6, places=12)
        self.assertAlmostEqual(bacia, 0.8, places=12)

    def test_felizes_base_10(self):
        # de 1 a 10, felizes: 1, 7, 10; o único outro ciclo em base 10 é o de oito números que começa em 4
        frac, ciclos = calculos.p883_felizes_hex(10, 10)
        self.assertAlmostEqual(frac, 0.3, places=12)
        self.assertEqual(ciclos, [(4, 16, 37, 58, 89, 145, 42, 20)])

    def test_felizes_base_16_ciclo(self):
        # s(13) = 169 = 0xA9 -> 100 + 81 = 181 = 0xB5 -> 121 + 25 = 146 = 0x92 -> 81 + 4 = 85 = 0x55 -> 50 = 0x32 -> 13
        self.assertEqual(calculos.p883_felizes_hex(13)[1], [(13, 169, 181, 146, 85, 50)])


if __name__ == "__main__":
    unittest.main()
