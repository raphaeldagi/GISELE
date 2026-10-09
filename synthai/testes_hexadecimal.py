"""Testes de unidade do `hexadecimal` (Parte 30): `python3 -m unittest synthai.testes_hexadecimal`."""

import unittest

from calculos import _rng

from .hexadecimal import efeitos_fatoriais, nome_do_tipo, quantizar, synthai_do_tipo, walsh_hadamard
from .mundos import MundoBandido, MundoSequencial
from .reconhecimento import SynthaiExploradora
from .testes import acessos_escondidos


def _rodar(codigo, mundo_fazer, semente, n):
    m = mundo_fazer(semente)
    return m.rodar(synthai_do_tipo(codigo, semente).calibrar(m, 30), n)


class TesteHexadecimal(unittest.TestCase):
    def test_dezesseis_tipos_constroem(self):
        for c in range(16):
            synthai_do_tipo(c, 1)
        with self.assertRaises(ValueError):
            synthai_do_tipo(0x10, 1)
        self.assertEqual(nome_do_tipo(0x4), "0x4 (Thompson)")

    def test_tipo_0x4_e_a_exploradora(self):
        m = MundoBandido(31)
        a = m.rodar(synthai_do_tipo(0x4, 31).calibrar(m, 30), 1)
        m = MundoBandido(31)
        self.assertEqual(a, m.rodar(SynthaiExploradora(31).calibrar(m, 30), 1))

    def test_thompson_nao_age_fora_do_bandido(self):
        for c in (0x0, 0x3, 0x9):
            self.assertEqual(_rodar(c, MundoSequencial, 32, 8), _rodar(c | 0x4, MundoSequencial, 32, 8))

    def test_ancora_nao_age_no_bandido(self):
        for c in (0x0, 0x5):
            self.assertEqual(_rodar(c, MundoBandido, 33, 1), _rodar(c | 0x2, MundoBandido, 33, 1))

    def test_walsh_hadamard_contra_a_definicao(self):
        rng = _rng(34)
        y = [rng.gauss(0, 1) for _ in range(16)]
        rapido = walsh_hadamard(y)
        for j in range(16):
            direto = sum((-1) ** bin(i & j).count("1") * y[i] for i in range(16))
            self.assertAlmostEqual(rapido[j], direto)

    def test_efeitos_de_um_fatorial_feito_a_mao(self):
        self.assertEqual(efeitos_fatoriais([10, 12, 20, 22]), [16.0, 2.0, 10.0, 0.0])

    def test_interacao_com_sinal_certo(self):
        # A = 21 − 15 = 6; B = 25 − 11 = 14; AB = ((30 − 20) − (12 − 10)) / 2 = 4
        self.assertEqual(efeitos_fatoriais([10, 12, 20, 30]), [18.0, 6.0, 14.0, 4.0])

    def test_efeitos_contra_a_definicao_em_tres_fatores(self):
        rng = _rng(35)
        y = [rng.gauss(0, 1) for _ in range(8)]
        e = efeitos_fatoriais(y)
        for j in range(1, 8):
            sinal = lambda i: 1
            direto = 0.0
            for i in range(8):
                prod = 1
                for k in range(3):
                    if j >> k & 1:
                        prod *= 1 if i >> k & 1 else -1  # +1 no nível alto
                direto += prod * y[i]
            self.assertAlmostEqual(e[j], direto / 4)

    def test_quantizacao_erra_no_maximo_meio_passo(self):
        w = [-6.0, 1.2, 0.5, 0.9, -0.3]
        for bits in (4, 8):
            q, codigos, passo = quantizar(w, bits)
            self.assertEqual(len(codigos), len(w) * bits // 4)
            self.assertTrue(all(abs(a - b) <= passo / 2 + 1e-12 for a, b in zip(w, q)))

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("hexadecimal"), [])


if __name__ == "__main__":
    unittest.main()
