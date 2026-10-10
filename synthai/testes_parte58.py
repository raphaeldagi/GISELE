"""Testes de unidade da Parte 58: `python3 -m unittest synthai.testes_parte58`. Cada pNN nova com o seu teste."""

import importlib.util
import os
import unittest

import calculos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DicionariosFalsos:
    # sinset n:1 -> en 'dog', pt 'cão' (3/3); n:2 -> en 'nation', pt 'nação' (5/6); n:3 só em inglês
    sinsets = [("n", ["dog"], [], ""), ("n", ["nation"], [], ""), ("n", ["cat"], [], "")]
    indice = {"n:1": 0, "n:2": 1, "n:3": 2}
    lemas = {"1-n": ["cão"], "2-n": ["nação"]}


class TesteParte58(unittest.TestCase):
    def test_primeiro_digito_hex(self):
        # conferido por código: 2^1..2^8 = 2, 4, 8, 0x10, 0x20, 0x40, 0x80, 0x100 -> 1, 2, 4, 8 duas vezes cada
        self.assertEqual(calculos.p1183_primeiro_digito_hex(2, 8), [0, 2, 2, 0, 2, 0, 0, 0, 2] + [0] * 7)
        # 3, 9, 27 = 0x1B, 81 = 0x51, 243 = 0xF3 -> 3, 9, 1, 5, F
        c = calculos.p1183_primeiro_digito_hex(3, 5)
        self.assertEqual([i for i, x in enumerate(c) if x], [1, 3, 5, 9, 15])

    def test_portugues_contra_ingles(self):
        d = DicionariosFalsos()
        razao, n, maior = calculos.p1182_portugues_contra_ingles(d, d)
        self.assertEqual((n, maior), (2, 0.0))
        self.assertAlmostEqual(razao, (1.0 + 5 / 6) / 2, places=12)

    def test_primeira_diferenca(self):
        spec = importlib.util.spec_from_file_location("rodada32", os.path.join(RAIZ, "dialogo", "rodada32.py"))
        r32 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(r32)
        # ordem de códigos: 'pe' < 'peixe' < 'pé'; primeiras diferenças: 3 ('pe' é prefixo, tamanho 2 + 1), 2 ('i' contra 'é');
        # pela chave portuguesa 'pé' -> 'pe' vem antes de 'peixe': o par (peixe, pé) inverte
        ws = sorted(["pe", "peixe", "pé"])
        self.assertEqual(ws, ["pe", "peixe", "pé"])
        self.assertEqual(r32.medir(ws), (5, 2, 1))


if __name__ == "__main__":
    unittest.main()


class TesteP1181(unittest.TestCase):
    """Acrescentado depois que a auditoria P1092 da própria Parte 58 achou p1181 sem teste pelo nome."""

    def test_p1181(self):
        pos, pares, inv, acento = calculos.p1181_primeira_diferenca()
        self.assertEqual((pares, inv, acento), (37724, 3738, 9236))
        self.assertAlmostEqual(pos, 207209 / 37724, places=12)
