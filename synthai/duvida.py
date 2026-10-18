"""A dúvida calculada (Parte 110). Seis peças de uma IA, cada uma conferida por um caminho independente do dela, só com a biblioteca padrão:
gradiente (diferença finita), inferência (cobertura empírica), RNN (BPTT contra a forma fechada), ML (erro de generalização contra
σ²(1 + p/(n − p − 1))), aprendizado contínuo (esquecimento contra cos²θ) e reforço (viés do max contra σ/√π). Cada peça tem também o
seu INVERSO (do número medido de volta à premissa) e o seu SUBVERSO (uma premissa derrubada, com a quebra prevista antes)."""

import math
import random
from statistics import NormalDist


# --- 1. gradiente: MLP 3 -> 4 -> 1 com tanh ---

def mlp_inicial(semente=110, d=3, h=4):
    rng = random.Random(semente)
    W = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(h)]
    b = [rng.uniform(-0.5, 0.5) for _ in range(h)]
    v = [rng.uniform(-1, 1) for _ in range(h)]
    x = [rng.uniform(-1, 1) for _ in range(d)]
    return W, b, v, x, 0.3


def _achatar(W, b, v):
    return [w for linha in W for w in linha] + list(b) + list(v)


def _montar(theta, d=3, h=4):
    W = [theta[i * d:(i + 1) * d] for i in range(h)]
    b = theta[h * d:h * d + h]
    v = theta[h * d + h:]
    return W, b, v


def perda_mlp(theta, x, y, d=3, h=4):
    W, b, v = _montar(theta, d, h)
    a = [math.tanh(sum(W[i][j] * x[j] for j in range(d)) + b[i]) for i in range(h)]
    f = sum(v[i] * a[i] for i in range(h))
    return 0.5 * (f - y) ** 2


def gradiente_mlp(theta, x, y, d=3, h=4):
    """O gradiente ANALÍTICO (retropropagação à mão)."""
    W, b, v = _montar(theta, d, h)
    a = [math.tanh(sum(W[i][j] * x[j] for j in range(d)) + b[i]) for i in range(h)]
    f = sum(v[i] * a[i] for i in range(h))
    r = f - y
    gW = [[r * v[i] * (1 - a[i] * a[i]) * x[j] for j in range(d)] for i in range(h)]
    gb = [r * v[i] * (1 - a[i] * a[i]) for i in range(h)]
    gv = [r * a[i] for i in range(h)]
    return _achatar(gW, gb, gv)


def gradiente_numerico(theta, x, y, passo, central=True):
    g = []
    for k in range(len(theta)):
        mais = list(theta)
        mais[k] += passo
        if central:
            menos = list(theta)
            menos[k] -= passo
            g.append((perda_mlp(mais, x, y) - perda_mlp(menos, x, y)) / (2 * passo))
        else:
            g.append((perda_mlp(mais, x, y) - perda_mlp(theta, x, y)) / passo)
    return g


def erro_relativo(ga, gn):
    """O maior erro relativo componente a componente: |ga − gn| / max(|ga|, |gn|)."""
    return max(abs(a - n) / max(abs(a), abs(n), 1e-300) for a, n in zip(ga, gn))


def verificar_gradiente(central=True, passos=None, plantar=None):
    """Erro relativo por passo h. `plantar=k` troca o sinal da componente k do gradiente analítico (o controle que tem de ser acusado)."""
    W, b, v, x, y = mlp_inicial()
    theta = _achatar(W, b, v)
    ga = gradiente_mlp(theta, x, y)
    if plantar is not None:
        ga[plantar] = -ga[plantar]
    passos = passos or [10.0 ** (-e) for e in range(1, 11)]
    return [(hh, erro_relativo(ga, gradiente_numerico(theta, x, y, hh, central))) for hh in passos]


def inclinacao(pares, h1=1e-2, h2=1e-3):
    """Inclinação de log(erro) contra log(h) entre dois passos: a ORDEM do método (o inverso: ler a premissa na curva)."""
    e = dict(pares)
    return (math.log(e[h1]) - math.log(e[h2])) / (math.log(h1) - math.log(h2))


# --- 2. inferência: cobertura do intervalo bayesiano Beta-Bernoulli ---

def _cdf_beta_inteira(xv, a, b):
    """I_x(a, b) com a, b inteiros = P(Binomial(a + b − 1, x) ≥ a)."""
    n = a + b - 1
    return sum(math.comb(n, j) * xv ** j * (1 - xv) ** (n - j) for j in range(a, n + 1))


def quantil_beta(q, a, b, iters=60):
    lo, hi = 0.0, 1.0
    for _ in range(iters):
        meio = (lo + hi) / 2
        if _cdf_beta_inteira(meio, a, b) < q:
            lo = meio
        else:
            hi = meio
    return (lo + hi) / 2


def cobertura_bayes(mundos=2000, n=50, aglomerado=1, nivel=0.90, semente=1100):
    """Fração dos mundos em que o intervalo central de `nivel` contém o p verdadeiro. p ~ U(0,1); as n observações vêm em n/aglomerado
    grupos de `aglomerado` cópias idênticas (aglomerado=1: independentes, o modelo está certo)."""
    rng = random.Random(semente)
    cauda = (1 - nivel) / 2
    dentro = 0
    for _ in range(mundos):
        p = rng.random()
        k = sum(aglomerado for _ in range(n // aglomerado) if rng.random() < p)
        lo = quantil_beta(cauda, 1 + k, 1 + n - k)
        hi = quantil_beta(1 - cauda, 1 + k, 1 + n - k)
        dentro += int(lo <= p <= hi)
    return dentro / mundos


def aglomerado_recuperado(cobertura, nivel=0.90):
    """O inverso: a cobertura de um intervalo nominal z·σ quando o σ real é √c vezes maior é P(|Z| < z/√c); resolve para c."""
    z = NormalDist().inv_cdf((1 + nivel) / 2)
    zc = NormalDist().inv_cdf((1 + cobertura) / 2)
    return (z / zc) ** 2


# --- 3. RNN: o gradiente através do tempo ---

def bptt_linear(w, T, h0=1.0):
    """RNN linear h_t = w·h_{t−1}: frente e trás (BPTT), ∂h_T/∂h_0 acumulado passo a passo."""
    hs = [h0]
    for _ in range(T):
        hs.append(w * hs[-1])
    g = 1.0
    for _ in range(T):
        g *= w
    return g


def bptt_tanh(w, T, h0=0.5):
    """RNN tanh h_t = tanh(w·h_{t−1}): ∂h_T/∂h_0 = Π w(1 − h_t²), pela retropropagação."""
    hs = [h0]
    for _ in range(T):
        hs.append(math.tanh(w * hs[-1]))
    g = 1.0
    for t in range(T, 0, -1):
        g *= w * (1 - hs[t] * hs[t])
    return g, hs[-1]


def w_recuperado(grad, T):
    """O inverso: w = grad^(1/T) (RNN linear, grad > 0)."""
    return math.exp(math.log(grad) / T)


# --- 4. ML: o erro de generalização dos mínimos quadrados ---

def _resolver(A, c):
    """Eliminação de Gauss com pivô parcial."""
    n = len(A)
    M = [list(A[i]) + [c[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        for r in range(col + 1, n):
            f = M[r][col] / M[col][col]
            for k in range(col, n + 1):
                M[r][k] -= f * M[col][k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][k] * x[k] for k in range(i + 1, n))) / M[i][i]
    return x


def erro_generalizacao(p=10, n=50, reps=2000, omitida=0.0, semente=1104):
    """Média de ‖β̂ − β‖² + σ²_efetivo (o erro de teste esperado exato sob x ~ N(0, I)), com σ = 1 e, se `omitida` > 0, uma variável
    z ~ N(0,1) de coeficiente `omitida` fora do modelo (vira ruído). Devolve a média."""
    rng = random.Random(semente)
    beta = [1.0] * p
    soma = 0.0
    for _ in range(reps):
        X = [[rng.gauss(0, 1) for _ in range(p)] for _ in range(n)]
        y = [sum(X[i][j] * beta[j] for j in range(p)) + rng.gauss(0, 1) + omitida * rng.gauss(0, 1) for i in range(n)]
        XtX = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(p)] for a in range(p)]
        Xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(p)]
        bh = _resolver(XtX, Xty)
        soma += sum((bh[j] - beta[j]) ** 2 for j in range(p)) + 1.0 + omitida * omitida
    return soma / reps


def p_recuperado(erro, n=50, sigma2=1.0):
    """O inverso: e = erro/σ² − 1 = p/(n − p − 1) ⇒ p = e(n − 1)/(1 + e)."""
    e = erro / sigma2 - 1
    return e * (n - 1) / (1 + e)


# --- 5. aprendizado contínuo: duas tarefas de posto 1 em ℝ² ---

def continuo(theta_graus, ogd=False, passo=0.1, passos=2000):
    """A tarefa A: perda (w·e1 − 1)² (w_A = (1, 0)). A tarefa B: direção u = (cos θ, sen θ), alvo c_B = u·w_A + 1 (resíduo inicial 1).
    GD em A até convergir, depois em B (OGD: o gradiente de B projetado ortogonal a e1). Devolve (esquecimento de A, perda de B, ‖Δw em B‖)."""
    th = math.radians(theta_graus)
    u = (math.cos(th), math.sin(th))
    w = [0.0, 0.0]
    for _ in range(passos):
        w[0] -= passo * 2 * (w[0] - 1.0)
    wa = list(w)
    cb = u[0] * wa[0] + u[1] * wa[1] + 1.0
    for _ in range(passos):
        r = u[0] * w[0] + u[1] * w[1] - cb
        g = [2 * r * u[0], 2 * r * u[1]]
        if ogd:
            g = [g[0] - g[0] * 1.0, g[1]]      # tira a componente ao longo de e1 (a direção de A)
        w = [w[0] - passo * g[0], w[1] - passo * g[1]]
    esq = (w[0] - 1.0) ** 2
    perda_b = (u[0] * w[0] + u[1] * w[1] - cb) ** 2
    return esq, perda_b, math.sqrt((w[0] - wa[0]) ** 2 + (w[1] - wa[1]) ** 2)


def theta_recuperado(esquecimento):
    """O inverso: esquecimento = cos²θ ⇒ θ = arccos √esquecimento (graus)."""
    return math.degrees(math.acos(math.sqrt(esquecimento)))


# --- 6. reforço: o viés de maximização ---

def vies_do_max(k=2, m=10, ensaios=20000, duplo=False, semente=1106):
    """k ações de valor verdadeiro 0; cada estimativa ~ N(0, 1/m) (média de m recompensas N(0,1)). Simples: E[max das estimativas]
    (o alvo do Q-learning). Duplo: escolhe a ação pelo conjunto A e avalia pelo conjunto B, independente (o Double Q-learning)."""
    rng = random.Random(semente)
    s = 1 / math.sqrt(m)
    tot = 0.0
    for _ in range(ensaios):
        qa = [rng.gauss(0, s) for _ in range(k)]
        if duplo:
            qb = [rng.gauss(0, s) for _ in range(k)]
            tot += qb[max(range(k), key=lambda i: qa[i])]
        else:
            tot += max(qa)
    return tot / ensaios


def m_recuperado(vies):
    """O inverso (k = 2): viés = σₑ/√π = 1/√(π m) ⇒ m = 1/(π·viés²)."""
    return 1 / (math.pi * vies * vies)
