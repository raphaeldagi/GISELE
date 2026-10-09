"""Testes de unidade da `ancora` (Parte 28): `python3 -m unittest synthai.testes_ancora`."""

import math
import unittest

from .ancora import SynthaiComAncora, quantil_gama
from .mundos import MundoSequencial
from .testes import acessos_escondidos


def _cdf_gama(k, x):
    s = t = 1.0 / k
    n = 1
    while t > 1e-15 * s:
        t *= x / (k + n)
        s += t
        n += 1
    return s * math.exp(-x + k * math.log(x) - math.lgamma(k))


class TesteAncora(unittest.TestCase):
    def test_wilson_hilferty_perto_do_exato(self):
        for k in (2.0, 9.0, 100.0):
            q = quantil_gama(k, 1.0, 0.8416)
            self.assertLess(abs(_cdf_gama(k, q) - 0.8), 0.01)

    def test_quantil_escala_com_a_taxa_e_encosta_na_media(self):
        self.assertAlmostEqual(quantil_gama(9.0, 2.0, 0.8416), quantil_gama(9.0, 1.0, 0.8416) / 2)
        self.assertLess(quantil_gama(10000.0, 10000.0, 0.8416) - 1.0, 0.01)

    def test_auditoria_vira_priori_de_f(self):
        m = MundoSequencial(17)
        a = SynthaiComAncora(17).calibrar(m, 60)
        cats, soma_p = a.f_auditado
        self.assertAlmostEqual(a.f_cat, 0.5 + cats)
        self.assertAlmostEqual(a.f_p, 0.5 + soma_p)
        b = SynthaiComAncora(17, auditoria=False).calibrar(MundoSequencial(17), 60)
        self.assertEqual((b.f_cat, b.f_p), (0.5, 0.5))

    def test_quantil_e_mais_pessimista_que_a_media(self):
        a = SynthaiComAncora(1, auditoria=False)
        a.f_cat, a.f_p = 9.5, 2.3
        a.passos_cat, a.futuro_soma, a.futuro_n = [0], {0: 10.0}, {0: 1}
        a.n_r, a.sx, a.sy, a.sxx, a.sxy = 2.0, 0.0, 0.0, 2.0, 2.0
        a.n_d, a.d_nota = 1.0, 1.0
        self.assertGreater(a.termos()[1], 9.5 / 2.3)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("ancora"), [])


if __name__ == "__main__":
    unittest.main()
