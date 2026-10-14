"""Parte 95: reimplementação em biblioteca padrão das IDEIAS de um relatório recebido ("SYNTHAI v2.0"),
auditadas pela árvore sintática e escritas do zero (NUNCA executo o código recebido; regra da Parte 72/85).

Quatro ideias, cada uma uma peça conhecida da literatura, medidas aqui contra o que o relatório afirma:
  - TTTS (Top-Two Thompson Sampling, Russo 2016): identificação do melhor braço.
  - Limiar bayesiano P* = c / ((1−ε)·L): o ponto de indiferença entre agir e consultar.
  - EWC (Elastic Weight Consolidation, Kirkpatrick 2017): ancoragem ponderada pela diagonal de Fisher.
  - Quantização adaptativa em hexadecimal (b bits), variância Δ²/12.

Só biblioteca padrão; só +−×÷, sqrt e a betavariate/gauss do `random`."""

import math
import random


# --- Limiar bayesiano P* e a direção da sua dependência em ε ---

def p_estrela(eps, c, L):
    """Limiar de abstenção P* = c / ((1−ε)·L). Acima dele (p_cat > P*) o agente consulta o oráculo."""
    return c / max(1e-9, (1.0 - eps) * L)


def p_estrela_cresce_com_eps(c=0.10, L=500.0, eps_lo=0.10, eps_hi=0.45):
    """Mostra a DIREÇÃO de P* em ε: como P* = c/((1−ε)L) e (1−ε) decresce, P* CRESCE com ε. Devolve (P*(eps_lo), P*(eps_hi), cresce?).
    Consequência: com mais ruído o limiar é MAIOR, logo o gatilho p_cat>P* dispara MENOS (abstém-se MENOS), não mais."""
    lo, hi = p_estrela(eps_lo, c, L), p_estrela(eps_hi, c, L)
    return lo, hi, hi > lo


# --- Top-Two Thompson Sampling ---

class ThompsonBernoulli:
    """Amostragem de Thompson padrão para braços Beta-Bernoulli."""
    def __init__(self, k, rng):
        self.k = k
        self.a = [1.0] * k
        self.b = [1.0] * k
        self.rng = rng

    def escolher(self):
        am = [self.rng.betavariate(self.a[i], self.b[i]) for i in range(self.k)]
        return max(range(self.k), key=lambda i: am[i])

    def atualizar(self, braco, sucesso):
        if sucesso:
            self.a[braco] += 1.0
        else:
            self.b[braco] += 1.0

    def recomendar(self):
        """Braço de maior média posterior a/(a+b)."""
        return max(range(self.k), key=lambda i: self.a[i] / (self.a[i] + self.b[i]))


class TopTwoThompson(ThompsonBernoulli):
    """Top-Two Thompson Sampling (Russo 2016): com prob beta joga o líder I¹; senão reamostra até achar um
    concorrente distinto I² e joga esse. Concentra as amostras no par competitivo -> identifica o melhor braço mais rápido."""
    def __init__(self, k, rng, beta=0.5, max_reamostra=100):
        super().__init__(k, rng)
        self.beta = beta
        self.max_reamostra = max_reamostra

    def escolher(self):
        am = [self.rng.betavariate(self.a[i], self.b[i]) for i in range(self.k)]
        i1 = max(range(self.k), key=lambda i: am[i])
        if self.rng.random() < self.beta:
            return i1
        for _ in range(self.max_reamostra):
            am2 = [self.rng.betavariate(self.a[i], self.b[i]) for i in range(self.k)]
            i2 = max(range(self.k), key=lambda i: am2[i])
            if i2 != i1:
                return i2
        return i1


def comparar_ttts_thompson(medias, T=200, sementes=200, beta=0.5):
    """Identificação do melhor braço: em T puxadas, qual fração das sementes recomenda o braço de maior média verdadeira,
    com TTTS e com Thompson padrão? Devolve (frac_correto_ttts, frac_correto_thompson, melhor_verdadeiro)."""
    melhor = max(range(len(medias)), key=lambda i: medias[i])
    ok_t = ok_s = 0
    for s in range(sementes):
        for Cls, cont in ((TopTwoThompson, "t"), (ThompsonBernoulli, "s")):
            rng = random.Random(10000 + s)
            ag = Cls(len(medias), rng, beta) if Cls is TopTwoThompson else Cls(len(medias), rng)
            for _ in range(T):
                i = ag.escolher()
                suc = rng.random() < medias[i]
                ag.atualizar(i, suc)
            if ag.recomendar() == melhor:
                if cont == "t":
                    ok_t += 1
                else:
                    ok_s += 1
    return ok_t / sementes, ok_s / sementes, melhor


# --- EWC: ancoragem ponderada pela diagonal de Fisher ---

def drift_ewc_vs_isotropico(dim=6, passos=400, lr=0.05, lam=0.3, semente=95):
    """Uma tarefa nova empurra TODOS os pesos; o EWC (penalidade lam·F_i·(w−w0)²) segura os de Fisher alto (importantes para
    a tarefa antiga) e deixa os de Fisher baixo derivarem; a ancoragem ISOTRÓPICA (lam·(w−w0)²) segura todos igual. Devolve
    (deriva nos coords de Fisher ALTO: ewc, isotropico) e (deriva nos de Fisher BAIXO: ewc, isotropico)."""
    rng = random.Random(semente)
    w0 = [rng.uniform(-1, 1) for _ in range(dim)]
    # Fisher: metade dos coords importante (alto), metade não (baixo)
    fisher = [10.0 if i < dim // 2 else 0.1 for i in range(dim)]
    # gradiente de uma tarefa nova: empurra todos os pesos na mesma direção g
    g = [rng.uniform(-1, 1) for _ in range(dim)]

    def rodar(usar_fisher):
        w = w0[:]
        for _ in range(passos):
            for i in range(dim):
                f = fisher[i] if usar_fisher else 1.0
                w[i] = w[i] - lr * (g[i] + lam * f * (w[i] - w0[i]))
        return w
    w_ewc, w_iso = rodar(True), rodar(False)
    alto = range(dim // 2)
    baixo = range(dim // 2, dim)
    d_alto_ewc = math.sqrt(sum((w_ewc[i] - w0[i]) ** 2 for i in alto))
    d_alto_iso = math.sqrt(sum((w_iso[i] - w0[i]) ** 2 for i in alto))
    d_baixo_ewc = math.sqrt(sum((w_ewc[i] - w0[i]) ** 2 for i in baixo))
    d_baixo_iso = math.sqrt(sum((w_iso[i] - w0[i]) ** 2 for i in baixo))
    return (d_alto_ewc, d_alto_iso), (d_baixo_ewc, d_baixo_iso)


# --- Quantização hexadecimal adaptativa ---

def quantizar_hex(w, bits=8):
    """Quantiza o vetor w em b bits sobre [−R, R], R = max|w|. Devolve (w quantizado, códigos hex, passo Δ)."""
    R = max(0.01, max(abs(x) for x in w))
    niveis = (1 << bits) - 1
    passo = (2.0 * R) / niveis
    qw, codigos = [], []
    for x in w:
        norm = (x + R) / (2.0 * R)
        idx = max(0, min(niveis, int(round(norm * niveis))))
        codigos.append(hex(idx))
        qw.append(-R + idx * passo)
    return qw, codigos, passo


def rms_quantizacao(w, bits=8):
    """RMS real do erro de quantização de w em b bits, e o desvio teórico Δ/√12. Devolve (rms medido, Δ/√12)."""
    qw, _, passo = quantizar_hex(w, bits)
    rms = math.sqrt(sum((a - b) ** 2 for a, b in zip(w, qw)) / len(w))
    return rms, passo / math.sqrt(12.0)
