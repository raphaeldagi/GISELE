"""SYNTHAI — módulo ADVERSÁRIO ADAPTATIVO CONTRA A ATENÇÃO (Parte 124). Arquivo único, só biblioteca padrão.

A atenção seletiva (Parte 30/P235) lê o sensor de catástrofe só nas `foco` melhores ações pelo proxy, mas o agente quantiliza
(sorteia) entre as `q·N` melhores. Se foco < q, há uma janela de ações que o agente pode EXECUTAR sem nunca ter LIDO. Um
mundo neutro quase não acha essa janela (a Parte 123 mediu +0,0008 catástrofe/episódio). Um ADVERSÁRIO que aprende acha.

O adversário escolhe, em cada episódio, a posição (no ranking do proxy) em que planta uma catástrofe, por Exp3
(Auer et al. 2002), ganhando 1 quando a catástrofe é executada. Três agentes:
- SELETIVA: lê as `foco` primeiras; veta as que o sensor acusa; sorteia entre as não vetadas do topo q·N;
- SOB DEMANDA: sorteia primeiro e lê o sensor só na ação sorteada (se acusa, veta e sorteia de novo);
- TODAS: lê as q·N do topo (o caro).
Sensor: leitura = d·c + N(0, 1); acusa se leitura > τ.

Contas fechadas (melhor resposta do adversário):
- SELETIVA, armadilha numa posição não lida da janela: ≈ 1/(k − V), V = falsos vetos entre as lidas → ≈ 1/k;
- SOB DEMANDA e TODAS: a armadilha só passa se o sensor erra: ≈ Φ(τ − d)/k.

Uso:  python3 adversario_adaptativo.py           (demonstração)
      python3 adversario_adaptativo.py --testes  (testes de unidade)
"""

import math
import random
import sys
import unittest
from statistics import NormalDist

PHI = NormalDist()


def episodio(agente, posicao_armadilha, rng, n=100, k=10, foco=5, d=3.0, tau=1.5):
    """Uma decisão. Devolve (catástrofe executada?, leituras feitas). A posição 0 é a melhor pelo proxy."""
    def acusa(j):
        c = 1.0 if j == posicao_armadilha else 0.0
        return d * c + rng.gauss(0, 1) > tau
    topo = list(range(k))
    leituras = 0
    if agente == "seletiva":
        vetadas = set()
        for j in range(min(foco, n)):
            leituras += 1
            if acusa(j):
                vetadas.add(j)
        candidatas = [j for j in topo if j not in vetadas]
        if not candidatas:
            return False, leituras
        return rng.choice(candidatas) == posicao_armadilha, leituras
    if agente == "todas":
        candidatas = []
        for j in topo:
            leituras += 1
            if not acusa(j):
                candidatas.append(j)
        if not candidatas:
            return False, leituras
        return rng.choice(candidatas) == posicao_armadilha, leituras
    if agente == "sob_demanda":
        restantes = topo[:]
        while restantes:
            j = restantes.pop(rng.randrange(len(restantes)))
            leituras += 1
            if not acusa(j):
                return j == posicao_armadilha, leituras
        return False, leituras
    raise ValueError(agente)


class Exp3:
    def __init__(self, braços, gama=0.05, semente=0):
        self.k = braços
        self.gama = gama
        self.lnw = [0.0] * braços
        self.rng = random.Random(semente)

    def probs(self):
        m = max(self.lnw)
        w = [math.exp(x - m) for x in self.lnw]
        s = sum(w)
        return [(1 - self.gama) * x / s + self.gama / self.k for x in w]

    def escolher(self):
        p = self.probs()
        u = self.rng.random()
        acum = 0.0
        for i, x in enumerate(p):
            acum += x
            if u < acum:
                return i, p
        return self.k - 1, p

    def atualizar(self, i, p, ganho):
        self.lnw[i] += self.gama * (ganho / p[i]) / self.k


def duelo(agente, episodios=20000, n=100, posicoes=20, gama=0.1, semente=0, **kw):
    """O adversário Exp3 (sobre as `posicoes` primeiras do ranking) contra o agente.
    Devolve (taxa de catástrofe na 2ª metade, leituras/episódio, posição preferida)."""
    adv = Exp3(posicoes, gama=gama, semente=semente)
    rng = random.Random(semente + 1)
    cat2 = leit = 0
    for t in range(episodios):
        i, p = adv.escolher()
        c, l = episodio(agente, i, rng, n=n, **kw)
        adv.atualizar(i, p, 1.0 if c else 0.0)
        leit += l
        if t >= episodios // 2:
            cat2 += c
    pos = max(range(posicoes), key=lambda j: adv.lnw[j])
    return cat2 / (episodios - episodios // 2), leit / episodios, pos


def melhor_resposta_fechada(agente, k=10, foco=5, d=3.0, tau=1.5):
    falso = 1 - PHI.cdf(tau)
    perda = PHI.cdf(tau - d)
    if agente == "seletiva":
        # E[1/(k − V)], V ~ Binomial(foco, falso): falsos vetos entre as lidas
        return sum(math.comb(foco, v) * falso ** v * (1 - falso) ** (foco - v) / (k - v) for v in range(foco + 1))
    return perda / k        # 1ª ordem: a armadilha sorteada passa só se o sensor erra (os falsos vetos acrescentam 2ª ordem)


def campo_medio(agente, episodios=20000, posicoes=20, gama=0.1, **kw):
    """Conta sem ruído do Exp3: em esperança, ln w_i cresce γ·r_i/K por rodada (E[ganho/p_i · 1{i escolhido}] = r_i).
    r_i = taxa de catástrofe com a armadilha na posição i (conta fechada aproximada). Devolve a taxa média na 2ª metade."""
    k = kw.get("k", 10)
    foco = kw.get("foco", 5)
    d, tau = kw.get("d", 3.0), kw.get("tau", 1.5)
    perda = PHI.cdf(tau - d)
    r = []
    for i in range(posicoes):
        if i >= k:
            r.append(0.0)
        elif agente == "seletiva" and i >= foco:
            r.append(melhor_resposta_fechada("seletiva", k, foco, d, tau))
        else:
            r.append(perda / k)
    soma = 0.0
    meio = episodios // 2
    for t in range(meio, episodios):
        lnw = [gama * x / posicoes * t for x in r]
        m = max(lnw)
        w = [math.exp(x - m) for x in lnw]
        s = sum(w)
        p = [(1 - gama) * x / s + gama / posicoes for x in w]
        soma += sum(pi * ri for pi, ri in zip(p, r))
    return soma / (episodios - meio)


def taxa_posicao(agente, posicao, episodios=40000, semente=0, **kw):
    rng = random.Random(semente)
    return sum(episodio(agente, posicao, rng, **kw)[0] for _ in range(episodios)) / episodios


def demonstracao():
    for ag in ("seletiva", "sob_demanda", "todas"):
        c, l, pos = duelo(ag, semente=3)
        print(f"{ag:>12}: catástrofe (adversário aprendendo, 2ª metade) {c:.4f}  leituras/ep {l:.2f}  posição preferida {pos}"
              f"  | conta da melhor resposta {melhor_resposta_fechada(ag):.4f}  | campo médio {campo_medio(ag):.4f}"
              f"  | posição 7 fixa {taxa_posicao(ag, 7, semente=9):.4f}")


class Testes(unittest.TestCase):
    def test_fora_do_topo_nunca_e_executada(self):
        rng = random.Random(0)
        for ag in ("seletiva", "sob_demanda", "todas"):
            self.assertFalse(any(episodio(ag, 50, rng)[0] for _ in range(300)))

    def test_sob_demanda_le_pelo_menos_uma(self):
        rng = random.Random(1)
        self.assertTrue(all(episodio("sob_demanda", 3, rng)[1] >= 1 for _ in range(200)))

    def test_seletiva_cega_na_janela(self):
        # sensor perfeito (d enorme) não protege a posição 7, que a seletiva nunca lê
        t = taxa_posicao("seletiva", 7, episodios=20000, semente=2, d=50.0, tau=25.0)
        self.assertAlmostEqual(t, 0.1, delta=4 * math.sqrt(0.09 / 20000))

    def test_sob_demanda_protege_com_sensor_perfeito(self):
        self.assertEqual(taxa_posicao("sob_demanda", 7, episodios=5000, semente=3, d=50.0, tau=25.0), 0.0)

    def test_exp3_probabilidades_somam_1(self):
        e = Exp3(10)
        e.atualizar(3, e.probs(), 1.0)
        self.assertAlmostEqual(sum(e.probs()), 1.0, places=12)

    def test_agente_desconhecido(self):
        with self.assertRaises(ValueError):
            episodio("xyz", 0, random.Random(0))


if __name__ == "__main__":
    if "--testes" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demonstracao()
