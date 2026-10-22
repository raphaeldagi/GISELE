"""SYNTHAI — módulo TRANSFERÊNCIA SEM RETREINO (Parte 124). Arquivo único, só biblioteca padrão.

Um agente que já resolveu M tarefas de uma família não precisa reaprender do zero: o que ele leva para a tarefa nova é uma
PRIORI. Nada é retreinado — só a priori muda. Bandidos de Bernoulli com K braços; em cada tarefa da família as médias dos
braços vêm de Betas por braço (o braço 0 costuma ser bom). Três agentes, todos Thompson:
- FRIO: priori Beta(1, 1) em cada braço;
- TRANSFERIDO: priori Beta(α_k, β_k) por braço, estimada nas tarefas antigas pelo método dos momentos (Bayes empírico);
- MISTO: mistura das duas prioris, com o peso atualizado pela verossimilhança marginal Beta-Binomial dos dados da tarefa
  nova (se a tarefa nova não se parece com a família, o peso migra para a priori fria): protege da transferência NEGATIVA.

Conta fechada usada: verossimilhança marginal de s sucessos em n puxadas sob Beta(a, b): B(a + s, b + n − s) / B(a, b).

Uso:  python3 transferencia.py           (demonstração)
      python3 transferencia.py --testes  (testes de unidade)
"""

import math
import random
import sys
import unittest


def ln_beta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def ln_marginal(s, n, a, b):
    return ln_beta(a + s, b + n - s) - ln_beta(a, b)


FAMILIA = ((8.0, 2.0), (2.0, 6.0), (2.0, 6.0), (2.0, 6.0), (2.0, 6.0))      # (α, β) do braço 0 bom, dos outros fracos
INVERSA = ((2.0, 8.0), (6.0, 2.0), (2.0, 6.0), (2.0, 6.0), (2.0, 6.0))      # o braço 0 ruim, o braço 1 bom: a família traída


def sortear_tarefa(familia, rng):
    return [rng.betavariate(a, b) for a, b in familia]


def momentos(amostras, minimo=0.5):
    """Beta pelo método dos momentos a partir de médias observadas: m, v → α = m·κ, β = (1 − m)·κ, κ = m(1 − m)/v − 1."""
    n = len(amostras)
    m = sum(amostras) / n
    v = sum((x - m) ** 2 for x in amostras) / (n - 1)
    kappa = max(2 * minimo, m * (1 - m) / max(v, 1e-9) - 1)
    return (max(minimo, m * kappa), max(minimo, (1 - m) * kappa))


def aprender_priori(tarefas_antigas):
    """Uma Beta por braço a partir das médias empíricas por braço nas tarefas antigas (cada tarefa vista com muitas puxadas)."""
    k = len(tarefas_antigas[0])
    return tuple(momentos([t[i] for t in tarefas_antigas]) for i in range(k))


class Thompson:
    def __init__(self, prioris, mistura=None):
        """prioris: tupla de (α, β) por braço; mistura: segunda tupla de prioris (a fria) para o agente MISTO."""
        self.p1 = prioris
        self.p2 = mistura
        k = len(prioris)
        self.s = [0] * k
        self.n = [0] * k
        self.ln_peso = [0.0, 0.0]                  # log-pesos a priori iguais

    def peso_transferido(self):
        if self.p2 is None:
            return 1.0
        a, b = self.ln_peso
        return 1.0 / (1.0 + math.exp(b - a))

    def escolher(self, rng):
        if self.p2 is not None and rng.random() >= self.peso_transferido():
            pri = self.p2
        else:
            pri = self.p1
        amostras = [rng.betavariate(a + s, b + n - s) for (a, b), s, n in zip(pri, self.s, self.n)]
        return max(range(len(amostras)), key=lambda i: amostras[i])

    def atualizar(self, i, r):
        if self.p2 is not None:
            # atualização sequencial exata do log-peso: preditiva de 1 observação sob cada priori
            for j, pri in enumerate((self.p1, self.p2)):
                a, b = pri[i]
                pa = (a + self.s[i]) / (a + b + self.n[i])
                self.ln_peso[j] += math.log(pa if r else 1 - pa)
        self.s[i] += r
        self.n[i] += 1


def arrependimento(agente, medias, passos, rng):
    melhor = max(medias)
    soma = 0.0
    for _ in range(passos):
        i = agente.escolher(rng)
        r = 1 if rng.random() < medias[i] else 0
        agente.atualizar(i, r)
        soma += melhor - medias[i]
    return soma


def experimento(familia_alvo, m_antigas=30, tarefas=200, passos=100, semente=0):
    """Arrependimento médio por tarefa dos três agentes; a priori transferida vem de FAMILIA (as tarefas antigas)."""
    rng = random.Random(semente)
    antigas = [sortear_tarefa(FAMILIA, rng) for _ in range(m_antigas)]
    pri = aprender_priori(antigas)
    fria = tuple((1.0, 1.0) for _ in FAMILIA)
    tot = {"frio": 0.0, "transferido": 0.0, "misto": 0.0}
    for _ in range(tarefas):
        medias = sortear_tarefa(familia_alvo, rng)
        for nome, ag in (("frio", Thompson(fria)), ("transferido", Thompson(pri)), ("misto", Thompson(pri, fria))):
            tot[nome] += arrependimento(ag, medias, passos, random.Random(rng.random()))
    return {k: v / tarefas for k, v in tot.items()}, pri


def demonstracao():
    for nome, fam in (("mesma família", FAMILIA), ("família traída", INVERSA)):
        res, pri = experimento(fam, semente=5)
        print(f"== tarefa nova da {nome} (100 puxadas, 200 tarefas)")
        print("   priori aprendida: " + ", ".join(f"({a:.1f}, {b:.1f})" for a, b in pri))
        for k, v in res.items():
            print(f"   {k:>12}: arrependimento médio {v:.2f}")


class Testes(unittest.TestCase):
    def test_marginal_uniforme(self):
        # sob Beta(1,1), P(s sucessos em n) = 1/(n+1) para cada sequência ordenada ponderada: marginal da sequência = 1/((n+1)·C(n,s))
        n, s = 7, 3
        self.assertAlmostEqual(math.exp(ln_marginal(s, n, 1, 1)), 1 / ((n + 1) * math.comb(n, s)), places=12)

    def test_momentos_recuperam_beta(self):
        rng = random.Random(1)
        a, b = momentos([rng.betavariate(8, 2) for _ in range(20000)])
        self.assertAlmostEqual(a / (a + b), 0.8, delta=0.01)
        self.assertAlmostEqual(a + b, 10.0, delta=1.0)

    def test_peso_sequencial_igual_a_marginal(self):
        p1, p2 = ((8.0, 2.0),), ((1.0, 1.0),)
        ag = Thompson(p1, p2)
        obs = [1, 0, 1, 1, 0, 0, 0, 1]
        for r in obs:
            ag.atualizar(0, r)
        s, n = sum(obs), len(obs)
        esperado = ln_marginal(s, n, 8, 2) - ln_marginal(s, n, 1, 1)
        self.assertAlmostEqual(ag.ln_peso[0] - ag.ln_peso[1], esperado, places=10)

    def test_transferir_ajuda_na_mesma_familia(self):
        res, _ = experimento(FAMILIA, tarefas=60, semente=2)
        self.assertLess(res["transferido"], res["frio"])

    def test_misto_nao_fica_muito_atras_do_frio_na_familia_traida(self):
        res, _ = experimento(INVERSA, tarefas=60, semente=3)
        self.assertLess(res["misto"], res["transferido"])


if __name__ == "__main__":
    if "--testes" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demonstracao()
