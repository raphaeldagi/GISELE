"""SYNTHAI — módulo MEMÓRIA COM TRAÇO (Parte 124). Arquivo único, só biblioteca padrão.

A Parte 123 mediu que nenhuma memória de catástrofe por RAIO (P204, P214, kernel que afina) domina: a armadilha é DISCRETA
(uma marca que algumas ações têm) e a memória mede DISTÂNCIA no espaço contínuo (risco, vantagem). Raio largo: fobia
(recusa ações seguras vizinhas); raio estreito: esquece a armadilha que reaparece em outro lugar. O problema é de
REPRESENTAÇÃO, não de raio. Este módulo dá à memória um TRAÇO: as ações têm um vetor de B bits observáveis; a armadilha é
uma conjunção desconhecida de bits; a memória guarda, por bit, a contagem Beta de catástrofes com e sem ele, e recusa uma
ação se a probabilidade posterior de catástrofe (Naive Bayes sobre os traços) passar de um limiar.

Mundo: cada episódio oferece A ações; ação = (valor ~ N(0, 1), bits ~ Bernoulli(0,5)^B). Armadilha: bits[0] e bits[1]
ligados → catástrofe com prob. p_cat (valor −C). Agentes:
- INGÊNUO: escolhe o maior valor;
- RAIO: lembra a posição (valor) de cada catástrofe e recusa ações a menos de r de alguma;
- TRAÇO: Naive Bayes sobre os bits;
- ORÁCULO: conhece a regra (o teto).

Uso:  python3 memoria_traco.py           (demonstração)
      python3 memoria_traco.py --testes  (testes de unidade)
"""

import math
import random
import sys
import unittest


class Mundo:
    def __init__(self, bits=8, acoes=6, p_cat=0.9, c=10.0):
        self.bits, self.acoes, self.p_cat, self.c = bits, acoes, p_cat, c

    def oferta(self, rng):
        return [(rng.gauss(0, 1), tuple(rng.random() < 0.5 for _ in range(self.bits))) for _ in range(self.acoes)]

    def armadilha(self, bits):
        return bits[0] and bits[1]

    def resultado(self, acao, rng):
        valor, bits = acao
        if self.armadilha(bits) and rng.random() < self.p_cat:
            return -self.c, True
        return valor, False


class Ingenuo:
    def escolher(self, oferta):
        return max(oferta, key=lambda a: a[0])

    def aprender(self, acao, catastrofe):
        pass


class Oraculo(Ingenuo):
    def __init__(self, mundo):
        self.m = mundo

    def escolher(self, oferta):
        seguras = [a for a in oferta if not self.m.armadilha(a[1])]
        return max(seguras or oferta, key=lambda a: a[0])


class Raio(Ingenuo):
    def __init__(self, raio=0.3):
        self.raio = raio
        self.memorias = []

    def escolher(self, oferta):
        livres = [a for a in oferta if all(abs(a[0] - x) >= self.raio for x in self.memorias)]
        return max(livres or oferta, key=lambda a: a[0])

    def aprender(self, acao, catastrofe):
        if catastrofe:
            self.memorias.append(acao[0])


class Traco(Ingenuo):
    """Naive Bayes: P(cat | bits) ∝ P(cat) Π P(b_i | cat), cada termo com Beta(1, 1). Também usa pares de bits?
    Não: só bits isolados (B parâmetros por classe); a conjunção bits[0]∧bits[1] fica visível porque cada um dos dois
    bits sozinho já dobra a taxa de catástrofe."""

    def __init__(self, bits, limiar=0.3):
        self.b = bits
        self.limiar = limiar
        self.n = [0, 0]                          # [seguras, catástrofes]
        self.um = [[0] * bits, [0] * bits]       # contagem de bit ligado por classe

    def p_cat(self, bits):
        ln = [math.log((self.n[c] + 1) / (sum(self.n) + 2)) for c in (0, 1)]
        for c in (0, 1):
            for i, x in enumerate(bits):
                p1 = (self.um[c][i] + 1) / (self.n[c] + 2)
                ln[c] += math.log(p1 if x else 1 - p1)
        m = max(ln)
        e = [math.exp(v - m) for v in ln]
        return e[1] / (e[0] + e[1])

    def escolher(self, oferta):
        livres = [a for a in oferta if self.p_cat(a[1]) < self.limiar]
        return max(livres or oferta, key=lambda a: a[0])

    def aprender(self, acao, catastrofe):
        c = 1 if catastrofe else 0
        self.n[c] += 1
        for i, x in enumerate(acao[1]):
            self.um[c][i] += x


def rodar(agente, mundo, episodios=3000, semente=0):
    """(valor médio, catástrofes por episódio, recusas-de-segura por episódio) na 2ª metade."""
    rng = random.Random(semente)
    soma = cat = fobia = 0.0
    meio = episodios // 2
    for t in range(episodios):
        oferta = mundo.oferta(rng)
        a = agente.escolher(oferta)
        v, c = mundo.resultado(a, rng)
        agente.aprender(a, c)
        if t >= meio:
            soma += v
            cat += c
            melhor_segura = max((o for o in oferta if not mundo.armadilha(o[1])), key=lambda o: o[0], default=None)
            fobia += melhor_segura is not None and a is not melhor_segura and not mundo.armadilha(a[1]) and a[0] < melhor_segura[0]
    k = episodios - meio
    return soma / k, cat / k, fobia / k


def demonstracao():
    m = Mundo()
    for nome, fab in (("ingênuo", Ingenuo), ("raio 0,3", lambda: Raio(0.3)), ("raio 0,05", lambda: Raio(0.05)),
                      ("traço", lambda: Traco(m.bits)), ("oráculo", lambda: Oraculo(m))):
        res = [rodar(fab(), m, semente=s) for s in range(10)]
        v = sum(r[0] for r in res) / 10
        c = sum(r[1] for r in res) / 10
        f = sum(r[2] for r in res) / 10
        print(f"{nome:>10}: valor {v:+.3f}  catástrofes/ep {c:.4f}  fobia (segura melhor recusada)/ep {f:.3f}")


class Testes(unittest.TestCase):
    def test_oraculo_nunca_cai_se_ha_segura(self):
        m = Mundo()
        rng = random.Random(0)
        o = Oraculo(m)
        for _ in range(500):
            of = m.oferta(rng)
            if any(not m.armadilha(a[1]) for a in of):
                self.assertFalse(m.armadilha(o.escolher(of)[1]))

    def test_traco_sem_dados_e_meio(self):
        self.assertAlmostEqual(Traco(4).p_cat((True, False, True, False)), 0.5)

    def test_traco_aprende_a_marca(self):
        t = Traco(3)
        for _ in range(50):
            t.aprender((0.0, (True, True, False)), True)
            t.aprender((0.0, (False, False, True)), False)
        self.assertGreater(t.p_cat((True, True, False)), 0.99)
        self.assertLess(t.p_cat((False, False, True)), 0.01)

    def test_raio_lembra_posicao(self):
        r = Raio(0.5)
        r.aprender((1.0, ()), True)
        self.assertEqual(r.escolher([(1.2, ()), (0.0, ())])[0], 0.0)

    def test_traco_bate_ingenuo(self):
        m = Mundo()
        vi = rodar(Ingenuo(), m, episodios=2000, semente=1)[0]
        vt = rodar(Traco(m.bits), m, episodios=2000, semente=1)[0]
        self.assertGreater(vt, vi)


if __name__ == "__main__":
    if "--testes" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demonstracao()
