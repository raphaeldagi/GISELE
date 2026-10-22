"""SYNTHAI — módulo QUANTILIZAÇÃO ADAPTATIVA (Parte 124). Arquivo único, só biblioteca padrão.

O quantilizador (Taylor 2016) escolhe ao acaso entre as q·N melhores ações pelo PROXY, em vez da melhor: se o proxy tem
armadilhas (ações em que ele erra para cima, lei de Goodhart), sortear entre muitas dilui a chance de pegar uma. Mas o q bom
depende do mundo: sem armadilhas, q pequeno é melhor (mais valor); com armadilhas, q grande é melhor (menos catástrofe).
Um q fixo não serve aos dois mundos. A versão ADAPTATIVA trata cada q de uma grade como um braço de bandido (UCB com a variância de cada braço) e aprende,
pelo resultado das próprias ações, qual q este mundo pede.

Mundo: N ações; valor verdadeiro u ~ N(0, 1); proxy = u + N(0, σ). Uma fração ρ é ARMADILHA: o proxy ganha +T e o valor
verdadeiro é −C (catástrofe).

Uso:  python3 quantilizacao_adaptativa.py           (demonstração com os números medidos)
      python3 quantilizacao_adaptativa.py --testes  (testes de unidade)
"""

import math
import random
import sys
import unittest

GRADE_Q = (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0)


class Mundo:
    def __init__(self, n=100, rho=0.03, t=4.0, c=10.0, sigma=1.0):
        self.n, self.rho, self.t, self.c, self.sigma = n, rho, t, c, sigma
        self.armadilhas = int(round(rho * n))

    def episodio(self, rng):
        """Lista de (proxy, valor_verdadeiro, armadilha)."""
        acoes = []
        for i in range(self.n):
            u = rng.gauss(0, 1)
            if i < self.armadilhas:
                acoes.append((u + rng.gauss(0, self.sigma) + self.t, -self.c, True))
            else:
                acoes.append((u + rng.gauss(0, self.sigma), u, False))
        return acoes


def quantilizar(acoes, q, rng):
    """Sorteia uniformemente entre as max(1, round(q·N)) melhores pelo proxy."""
    k = max(1, int(round(q * len(acoes))))
    topo = sorted(acoes, key=lambda a: -a[0])[:k]
    return topo[rng.randrange(k)]


def valor_esperado_q(mundo, q, episodios=4000, semente=0):
    """Monte Carlo: (valor médio, taxa de catástrofe) do quantilizador fixo q."""
    rng = random.Random(semente)
    soma = cat = 0.0
    for _ in range(episodios):
        a = quantilizar(mundo.episodio(rng), q, rng)
        soma += a[1]
        cat += a[2]
    return soma / episodios, cat / episodios


def p_armadilha_aprox(mundo, q):
    """Conta fechada (cota): se as armadilhas sempre ficam no topo do proxy (T grande), a chance de sortear uma entre as
    k = q·N melhores é min(1, A/k), A = número de armadilhas."""
    k = max(1, int(round(q * mundo.n)))
    return min(1.0, mundo.armadilhas / k)


class QuantilizadorAdaptativo:
    """UCB com a variância empírica de cada braço (Auer et al. 2002, UCB1-Normal simplificado): bônus s_i·√(2 ln t / n_i).
    A recompensa é o valor verdadeiro da ação escolhida (observado depois de agir); a escala vem dos dados, não de fora."""

    def __init__(self, grade=GRADE_Q, piso=0.1):
        self.grade = grade
        self.n = [0] * len(grade)
        self.soma = [0.0] * len(grade)
        self.soma2 = [0.0] * len(grade)
        self.t = 0
        self.piso = piso

    def escolher_q(self):
        self.t += 1
        for i, n in enumerate(self.n):
            if n < 2:
                return i
        def ucb(i):
            m = self.soma[i] / self.n[i]
            v = max(0.0, self.soma2[i] / self.n[i] - m * m) * self.n[i] / (self.n[i] - 1)
            return m + max(self.piso, math.sqrt(v)) * math.sqrt(2 * math.log(self.t) / self.n[i])
        return max(range(len(self.grade)), key=ucb)

    def atualizar(self, i, recompensa):
        self.n[i] += 1
        self.soma[i] += recompensa
        self.soma2[i] += recompensa * recompensa

    def q_preferido(self):
        return self.grade[max(range(len(self.grade)), key=lambda i: self.n[i])]


def rodar(mundo, agente, episodios, semente):
    """Valor médio e taxa de catástrofe de um agente: 'adaptativo' ou um float q fixo."""
    rng = random.Random(semente)
    soma = cat = 0.0
    adapt = QuantilizadorAdaptativo() if agente == "adaptativo" else None
    for _ in range(episodios):
        acoes = mundo.episodio(rng)
        if adapt is None:
            a = quantilizar(acoes, agente, rng)
        else:
            i = adapt.escolher_q()
            a = quantilizar(acoes, adapt.grade[i], rng)
            adapt.atualizar(i, a[1])
        soma += a[1]
        cat += a[2]
    return soma / episodios, cat / episodios, (adapt.q_preferido() if adapt else agente)


def demonstracao():
    mundos = {"com armadilhas (ρ=0,03)": Mundo(rho=0.03), "sem armadilhas (ρ=0)": Mundo(rho=0.0)}
    for nome, m in mundos.items():
        print(f"\n== mundo {nome}")
        melhor = None
        for q in GRADE_Q:
            v, c = valor_esperado_q(m, q, episodios=3000, semente=11)
            print(f"  q fixo {q:>5}: valor {v:+.3f}  catástrofe {c:.4f}  (cota A/k {p_armadilha_aprox(m, q):.3f})")
            if melhor is None or v > melhor[1]:
                melhor = (q, v)
        print(f"  melhor q fixo: {melhor[0]} (valor {melhor[1]:+.3f})")
        for s in (1, 2, 3):
            v, c, qp = rodar(m, "adaptativo", 3000, semente=100 + s)
            v5, c5, _ = rodar(m, 0.05, 3000, semente=100 + s)
            print(f"  semente {s}: adaptativo {v:+.3f} (cat {c:.4f}, q preferido {qp})  x  q=0,05 fixo {v5:+.3f} (cat {c5:.4f})")


class Testes(unittest.TestCase):
    def test_quantilizar_respeita_o_topo(self):
        rng = random.Random(0)
        acoes = [(float(i), float(i), False) for i in range(100)]
        for _ in range(200):
            self.assertGreaterEqual(quantilizar(acoes, 0.1, rng)[0], 90.0)

    def test_q1_e_uniforme(self):
        m = Mundo(rho=0.03)
        _, c = valor_esperado_q(m, 1.0, episodios=4000, semente=1)
        self.assertAlmostEqual(c, 0.03, delta=4 * math.sqrt(0.03 * 0.97 / 4000))

    def test_cota_de_armadilha(self):
        m = Mundo(rho=0.03)
        self.assertEqual(p_armadilha_aprox(m, 0.01), 1.0)
        self.assertAlmostEqual(p_armadilha_aprox(m, 0.1), 0.3)

    def test_sem_armadilhas_nunca_ha_catastrofe(self):
        _, c = valor_esperado_q(Mundo(rho=0.0), 0.01, episodios=500, semente=2)
        self.assertEqual(c, 0.0)

    def test_ucb_explora_cada_braco_uma_vez(self):
        a = QuantilizadorAdaptativo()
        vistos = []
        for _ in range(2 * len(GRADE_Q)):
            i = a.escolher_q()
            a.atualizar(i, 0.0)
            vistos.append(i)
        self.assertEqual(sorted(vistos), sorted(list(range(len(GRADE_Q))) * 2))

    def test_adaptativo_bate_q_fixo_errado_nos_dois_mundos(self):
        for rho, ruim in ((0.03, 0.01), (0.0, 1.0)):
            v_a, _, _ = rodar(Mundo(rho=rho), "adaptativo", 1500, semente=7)
            v_r, _, _ = rodar(Mundo(rho=rho), ruim, 1500, semente=7)
            self.assertGreater(v_a, v_r)


if __name__ == "__main__":
    if "--testes" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demonstracao()
