"""Testes de unidade da Parte 81 (o que não serve): `python3 -m unittest synthai.testes_parte81`."""

import unittest

import calculos


class TesteParte81(unittest.TestCase):
    def test_p1871_o_que_nao_serve(self):
        a, b, c = calculos.p1871_o_que_nao_serve()
        self.assertEqual((a, b), ([], []))
        # o verificador acha o que procura: os RodadaNN.java não têm o nome escrito em lugar nenhum (o verificar.py os acha por glob)
        self.assertIn("dialogo/Rodada45.java", c)

    def test_p1872_candidatos_explicados(self):
        # caso de controle dos dois lados (a regra da Parte 75): um arquivo inventado fica sem motivo; um RodadaNN.java tem motivo
        contagem, sobra = calculos.p1872_candidatos_explicados(["dialogo/Rodada45.java", "lixo/nada.txt"])
        self.assertEqual((contagem, sobra), ({"verificar.py (glob)": 1}, ["lixo/nada.txt"]))
        self.assertEqual(calculos.p1872_candidatos_explicados()[1], [])


if __name__ == "__main__":
    unittest.main()
