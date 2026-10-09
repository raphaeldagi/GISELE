"""Decisão bayesiana exata no lugar do aprendizado por reforço e do aprendizado contínuo por gradiente (Parte 32).

A ideia: quando o modelo do mundo cabe numa família exponencial, o estado de conhecimento inteiro é uma ESTATÍSTICA
SUFICIENTE de tamanho fixo (contagens, X'X e X'y). Atualizá-la é exato, não esquece nada e não tem taxa de aprendizado;
decidir é amostrar do posterior (Thompson; PSRL nos MDPs). Os rivais são os métodos padrão: Q-learning com ε-guloso
(passo constante) e descida de gradiente estocástica.

Só biblioteca padrão. Cada classe recebe o próprio gerador (random.Random) e nunca lê o mundo por dentro.
"""

from math import log, sqrt


# --------------------------------------------------------------------------- bandido de Bernoulli


class ThompsonBernoulli:
    """Posterior Beta(1 + sucessos, 1 + fracassos) por braço; escolhe o braço com a maior amostra. `teto` (opcional)
    limita a memória: quando a + b passa do teto, as duas contagens são reduzidas à metade (P411: quantos dígitos hex
    a memória precisa)."""

    def __init__(self, k, rng, teto=None):
        self.a = [1.0] * k
        self.b = [1.0] * k
        self.rng = rng
        self.teto = teto

    def escolher(self):
        amostras = [self.rng.betavariate(a, b) for a, b in zip(self.a, self.b)]
        return max(range(len(amostras)), key=amostras.__getitem__)

    def atualizar(self, braco, r):
        if r:
            self.a[braco] += 1
        else:
            self.b[braco] += 1
        if self.teto is not None and self.a[braco] + self.b[braco] > self.teto:
            self.a[braco] = max(1.0, self.a[braco] / 2)
            self.b[braco] = max(1.0, self.b[braco] / 2)

    def estado(self):
        return list(self.a), list(self.b)



class ThompsonDescontado(ThompsonBernoulli):
    """Thompson com renovação (Parte 33, ↩ P405): a cada passo, todas as contagens decaem para a crença inicial,
    a ← 1 + γ(a − 1), b ← 1 + γ(b − 1), antes da observação nova. A memória efetiva é ~1/(1 − γ) passos: uma crença
    errada (ou lixo) some em alguns 1/(1 − γ); em troca, o agente nunca fica certo de nada além dessa janela
    (o "Bayes com esquecimento" de Raj e Kalyani, 2017)."""

    def __init__(self, k, rng, gama=0.99):
        super().__init__(k, rng)
        self.gama = gama

    def atualizar(self, braco, r):
        g = self.gama
        self.a = [1.0 + g * (a - 1.0) for a in self.a]
        self.b = [1.0 + g * (b - 1.0) for b in self.b]
        super().atualizar(braco, r)


class ThompsonMorris(ThompsonBernoulli):
    """Thompson com contadores de Morris (1978) (Parte 34, trilha hexadecimal): cada contagem guarda só o expoente c, um
    dígito hex (0..15); um sucesso incrementa c com chance 2^-c; a contagem estimada é 2^c − 1 (sem viés:
    E[2^c − 1] = n). Memória: 2 dígitos hex por braço, para contagens até 2^15."""

    def __init__(self, k, rng):
        super().__init__(k, rng)
        self.ca = [0] * k
        self.cb = [0] * k

    def atualizar(self, braco, r):
        c = self.ca if r else self.cb
        if c[braco] < 15 and self.rng.random() < 2.0 ** -c[braco]:
            c[braco] += 1
        self.a[braco] = 1.0 + 2 ** self.ca[braco] - 1
        self.b[braco] = 1.0 + 2 ** self.cb[braco] - 1


class ThompsonSurpresa(ThompsonBernoulli):
    """Renovação DIRIGIDA (Parte 35, ↩ P408): Thompson exato, mas cada braço guarda também as últimas `janela`
    observações; quando a média delas se afasta da média do posterior por mais de z desvios binomiais
    (|m_janela − m_post| > z·√(m_post(1 − m_post)/janela)), o braço é renovado: a crença vira Beta(1 + sucessos da
    janela, 1 + fracassos da janela). Só o braço desmentido esquece; os outros continuam exatos. É a compensação de
    Jung: a correção vem de onde a crença falhou."""

    def __init__(self, k, rng, janela=20, z=3.0):
        super().__init__(k, rng)
        self.janela, self.z = janela, z
        self.recentes = [[] for _ in range(k)]
        self.renovacoes = 0

    def atualizar(self, braco, r):
        super().atualizar(braco, r)
        rec = self.recentes[braco]
        rec.append(r)
        if len(rec) > self.janela:
            rec.pop(0)
        if len(rec) == self.janela:
            a, b = self.a[braco], self.b[braco]
            m = a / (a + b)
            mj = sum(rec) / self.janela
            if abs(mj - m) > self.z * sqrt(max(m * (1 - m), 1e-9) / self.janela):
                self.a[braco] = 1.0 + sum(rec)
                self.b[braco] = 1.0 + self.janela - sum(rec)
                self.renovacoes += 1


class ThompsonSurpresaExposta(ThompsonSurpresa):
    """A renovação dirigida com EXPOSIÇÃO (Parte 36, ↩ P491): a cada `periodo` escolhas, puxa o braço puxado há mais
    tempo, em vez de amostrar. Um braço desacreditado (que Thompson não puxaria) volta a ser testado e, se a crença sobre
    ele estiver errada, a surpresa a desmente. Custo: periodo⁻¹ das escolhas vão para braços provavelmente ruins."""

    def __init__(self, k, rng, janela=20, z=3.0, periodo=50):
        super().__init__(k, rng, janela, z)
        self.periodo = periodo
        self.passo = 0
        self.ultimo = [-1] * k

    def escolher(self):
        self.passo += 1
        if self.passo % self.periodo == 0:
            i = min(range(len(self.ultimo)), key=self.ultimo.__getitem__)
        else:
            i = super().escolher()
        self.ultimo[i] = self.passo
        return i

class QEpsilon:
    """Q-learning de um passo (o bandido é um MDP de um estado): Q ← Q + α(r − Q), ε-guloso, empate ao acaso."""

    def __init__(self, k, rng, alfa=0.1, eps=0.1, q0=0.0):
        self.q = [q0] * k
        self.rng = rng
        self.alfa = alfa
        self.eps = eps

    def escolher(self):
        if self.rng.random() < self.eps:
            return self.rng.randrange(len(self.q))
        m = max(self.q)
        return self.rng.choice([i for i, x in enumerate(self.q) if x == m])

    def atualizar(self, braco, r):
        self.q[braco] += self.alfa * (r - self.q[braco])


class UCB1:
    """UCB1 (Auer, Cesa-Bianchi e Fischer, 2002): média + √(2 ln t / n)."""

    def __init__(self, k, rng):
        self.n = [0] * k
        self.s = [0.0] * k
        self.t = 0
        self.rng = rng

    def escolher(self):
        for i, n in enumerate(self.n):
            if n == 0:
                return i
        return max(range(len(self.n)), key=lambda i: self.s[i] / self.n[i] + sqrt(2 * log(self.t) / self.n[i]))

    def atualizar(self, braco, r):
        self.n[braco] += 1
        self.s[braco] += r
        self.t += 1


def kl_bernoulli(p, q):
    """Divergência de Kullback–Leibler entre Bernoulli(p) e Bernoulli(q)."""
    eps = 1e-12
    p, q = min(max(p, eps), 1 - eps), min(max(q, eps), 1 - eps)
    return p * log(p / q) + (1 - p) * log((1 - p) / (1 - q))


def cota_lai_robbins(ps, t):
    """A cota inferior assintótica do arrependimento (Lai e Robbins, 1985): Σ_{k subótimo} Δ_k ln T / KL(p_k, p*),
    truncada em Δ_k·T (nenhum braço custa mais do que ser puxado sempre)."""
    m = max(ps)
    return sum(min((m - p) * t, (m - p) * log(t) / kl_bernoulli(p, m)) for p in ps if p < m)


def rodar_bandido(agente, ps, t, rng, dano_em=None, danificar=None):
    """Roda o agente T passos num bandido de Bernoulli com médias `ps` (escondidas do agente). Devolve o arrependimento
    acumulado passo a passo (pela média: Σ (p* − p_escolhido)). `danificar(agente)` é chamado no passo `dano_em`."""
    m = max(ps)
    arrep, total = [], 0.0
    for passo in range(t):
        if dano_em is not None and passo == dano_em:
            danificar(agente)
        i = agente.escolher()
        r = 1 if rng.random() < ps[i] else 0
        agente.atualizar(i, r)
        total += m - ps[i]
        arrep.append(total)
    return arrep


# --------------------------------------------------------------------------- MDP: RiverSwim


def riverswim(n=6):
    """O RiverSwim (Strehl e Littman, 2008): n estados em fila, ações 0 = esquerda (rio abaixo) e 1 = direita (contra a
    correnteza). Devolve (P, R): P[s][a] = lista de (próximo, probabilidade); R[s][a] = recompensa esperada.
    Esquerda: sempre um passo para a esquerda; no estado 0, recompensa 5/1000. Direita: no meio, 0,35 avança, 0,6 fica,
    0,05 volta; no estado 0, 0,4 fica e 0,6 avança; no último, 0,6 fica e 0,4 volta, com recompensa 1."""
    P = [[None, None] for _ in range(n)]
    R = [[0.0, 0.0] for _ in range(n)]
    for s in range(n):
        P[s][0] = [(max(s - 1, 0), 1.0)]
        if s == 0:
            P[s][1] = [(0, 0.4), (1, 0.6)]
        elif s == n - 1:
            P[s][1] = [(s, 0.6), (s - 1, 0.4)]
        else:
            P[s][1] = [(s + 1, 0.35), (s, 0.6), (s - 1, 0.05)]
    R[0][0] = 5 / 1000
    R[n - 1][1] = 0.6  # a recompensa 1 vem com a permanência no último estado (probabilidade 0,6)
    return P, R


def media_otima(P, R, iteracoes=20000):
    """O ganho médio ótimo por passo (iteração de valor relativa, MDP unichain): o g da equação de Bellman
    h(s) + g = max_a [R(s, a) + Σ P(s'|s, a) h(s')]."""
    n = len(P)
    h = [0.0] * n
    g = 0.0
    for _ in range(iteracoes):
        novo = [max(R[s][a] + sum(p * h[x] for x, p in P[s][a]) for a in range(2)) for s in range(n)]
        g = novo[0] - h[0]
        h = [v - novo[0] for v in novo]
    return g


def politica_horizonte(P, R, h):
    """Política ótima de horizonte h (programação dinâmica para trás): devolve pol[passo][s]."""
    n = len(P)
    v = [0.0] * n
    pols = []
    for _ in range(h):
        q = [[R[s][a] + sum(p * v[x] for x, p in P[s][a]) for a in range(2)] for s in range(n)]
        pols.append([0 if q[s][0] >= q[s][1] else 1 for s in range(n)])
        v = [max(q[s]) for s in range(n)]
    return pols[::-1]


def passo_mdp(P, R, s, a, rng):
    u, acum = rng.random(), 0.0
    for x, p in P[s][a]:
        acum += p
        if u < acum:
            break
    r = R[s][a] if (s, a) != (len(P) - 1, 1) else (1.0 if x == s else 0.0)
    return x, r


class PSRL:
    """Amostragem do posterior para RL (Osband, Russo e Van Roy, 2013): posterior Dirichlet(1 + contagens) nas transições
    e média bayesiana das recompensas (Beta(1,1) por (s, a, s') não é preciso: aqui a recompensa por (s, a) tem posterior
    Beta(1 + soma, 1 + n − soma)). A cada episódio de `h` passos sorteia um MDP do posterior e segue a política ótima dele."""

    def __init__(self, n, rng, h=20):
        self.n, self.rng, self.h = n, rng, h
        self.cont = [[[0] * n for _ in range(2)] for _ in range(n)]
        self.rsoma = [[0.0, 0.0] for _ in range(n)]
        self.rn = [[0, 0] for _ in range(n)]
        self.t = 0
        self.pol = None

    def _sortear(self):
        P, R = [], []
        for s in range(self.n):
            ls, lr = [], []
            for a in range(2):
                g = [self.rng.gammavariate(1 + c, 1.0) for c in self.cont[s][a]]
                tot = sum(g)
                ls.append([(x, g[x] / tot) for x in range(self.n)])
                lr.append(self.rng.betavariate(1 + self.rsoma[s][a], 1 + self.rn[s][a] - self.rsoma[s][a]))
            P.append(ls)
            R.append(lr)
        return P, R

    def agir(self, s):
        if self.t % self.h == 0:
            P, R = self._sortear()
            self.pol = politica_horizonte(P, R, self.h)
        return self.pol[self.t % self.h][s]

    def aprender(self, s, a, r, x):
        self.cont[s][a][x] += 1
        self.rsoma[s][a] += r
        self.rn[s][a] += 1
        self.t += 1


class QLearningMDP:
    """Q-learning tabular (Watkins, 1989) com desconto γ, passo α e ε-guloso; q0 > 0 é a variante otimista."""

    def __init__(self, n, rng, alfa=0.1, gama=0.95, eps=0.1, q0=0.0):
        self.q = [[q0, q0] for _ in range(n)]
        self.rng, self.alfa, self.gama, self.eps = rng, alfa, gama, eps

    def agir(self, s):
        if self.rng.random() < self.eps:
            return self.rng.randrange(2)
        a, b = self.q[s]
        return self.rng.randrange(2) if a == b else (0 if a > b else 1)

    def aprender(self, s, a, r, x):
        self.q[s][a] += self.alfa * (r + self.gama * max(self.q[x]) - self.q[s][a])


def rodar_mdp(agente, P, R, t, rng):
    """Roda T passos a partir do estado 0; devolve a recompensa total."""
    s, total = 0, 0.0
    for _ in range(t):
        a = agente.agir(s)
        x, r = passo_mdp(P, R, s, a, rng)
        agente.aprender(s, a, r, x)
        total += r
        s = x
    return total


# --------------------------------------------------------------------------- aprendizado contínuo


class RegressaoBayesiana:
    """Regressão linear bayesiana exata em forma recursiva (mínimos quadrados recursivos): o estado é a inversa de
    (λI + X'X) e a média do posterior; cada exemplo atualiza os dois pela fórmula de Sherman–Morrison, O(d²) por exemplo.
    Depois de qualquer sequência de exemplos, o resultado é IGUAL ao da regressão ridge em lote com todos eles: não há
    o que esquecer."""

    def __init__(self, d, lam=1e-2):
        self.d = d
        self.Pm = [[(1.0 / lam if i == j else 0.0) for j in range(d)] for i in range(d)]
        self.w = [0.0] * d

    def prever(self, f):
        return sum(a * b for a, b in zip(self.w, f))

    def atualizar(self, f, y):
        Pf = [sum(l[j] * f[j] for j in range(self.d)) for l in self.Pm]
        den = 1.0 + sum(a * b for a, b in zip(f, Pf))
        erro = y - self.prever(f)
        k = [x / den for x in Pf]
        self.w = [w + ki * erro for w, ki in zip(self.w, k)]
        self.Pm = [[self.Pm[i][j] - k[i] * Pf[j] for j in range(self.d)] for i in range(self.d)]


class RegressaoSGD:
    """A mesma regressão linear, pelo gradiente estocástico com passo constante (o aprendizado contínuo padrão)."""

    def __init__(self, d, passo=0.01):
        self.w = [0.0] * d
        self.passo = passo

    def prever(self, f):
        return sum(a * b for a, b in zip(self.w, f))

    def atualizar(self, f, y):
        erro = y - self.prever(f)
        self.w = [w + self.passo * erro * x for w, x in zip(self.w, f)]


def ridge_em_lote(fs, ys, lam=1e-2):
    """A solução ridge em lote (λI + X'X)⁻¹X'y, por eliminação de Gauss com pivô: a referência da RegressaoBayesiana."""
    d = len(fs[0])
    A = [[(lam if i == j else 0.0) + sum(f[i] * f[j] for f in fs) for j in range(d)] for i in range(d)]
    b = [sum(f[i] * y for f, y in zip(fs, ys)) for i in range(d)]
    for c in range(d):
        p = max(range(c, d), key=lambda r: abs(A[r][c]))
        A[c], A[p], b[c], b[p] = A[p], A[c], b[p], b[c]
        for r in range(c + 1, d):
            m = A[r][c] / A[c][c]
            if m:
                A[r] = [x - m * y for x, y in zip(A[r], A[c])]
                b[r] -= m * b[c]
    w = [0.0] * d
    for c in range(d - 1, -1, -1):
        w[c] = (b[c] - sum(A[c][j] * w[j] for j in range(c + 1, d))) / A[c][c]
    return w
