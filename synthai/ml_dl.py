"""ML como DL e DL como ML (Parte 114). Biblioteca padrão. A fronteira entre "aprendizado de máquina clássico" e "aprendizado profundo"
medida em quatro travessias:
  1. ML → DL: a regressão logística com L2 é uma rede de UMA camada (linear + sigmoide + entropia cruzada). Treinada como DL (descida do
     gradiente pela retropropagação), ela tem de chegar ao mesmo ponto que o solucionador clássico (Newton/IRLS), porque o problema é
     fortemente convexo.
  2. DL → ML: uma rede LINEAR profunda (duas camadas, sem ativação) é um modelo linear sobreparametrizado. O produto W₂W₁ treinado por
     gradiente deve chegar à solução de mínimos quadrados (OLS, forma fechada).
  3. DL → ML: a camada oculta de uma rede como FEATURES (aleatórias ou treinadas) e a cabeça resolvida em forma fechada (ridge), contra a
     rede inteira treinada por retropropagação.
  4. ML → DL e volta: os GRAUS DE LIBERDADE (uma medida clássica de complexidade, tr H(H+λI)⁻¹ para a ridge) aplicados à cabeça de uma rede,
     conferidos pela definição de Efron (Σ cov(ŷᵢ, yᵢ)/σ², medida por simulação)."""

import math
import random


def _resolver(A, c):
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
        s = M[i][n]
        for k in range(i + 1, n):
            s -= M[i][k] * x[k]
        x[i] = s / M[i][i]
    return x


def _sig(z):
    return 1.0 / (1.0 + math.exp(-z)) if z >= 0 else math.exp(z) / (1.0 + math.exp(z))


# --- dados (fixtures) ---

def dados_logistica(n=300, semente=114):
    """x ~ N(0, I₃) com uma coluna de 1 (o viés); y ~ Bernoulli(σ(1,5x₁ − 2x₂ + 0,5x₃ + 0,3))."""
    rng = random.Random(semente)
    X, y = [], []
    for _ in range(n):
        x = [rng.gauss(0, 1) for _ in range(3)]
        p = _sig(1.5 * x[0] - 2.0 * x[1] + 0.5 * x[2] + 0.3)
        X.append(x + [1.0])
        y.append(1.0 if rng.random() < p else 0.0)
    return X, y


def dados_regressao(n=200, semente=114, sigma=0.1):
    """x ~ U(−2, 2)², y = sen(x₁) + 0,5·x₂² + ruído N(0, σ²): uma função não-linear (precisa de features)."""
    rng = random.Random(semente)
    X, y = [], []
    for _ in range(n):
        x = [rng.uniform(-2, 2), rng.uniform(-2, 2)]
        X.append(x)
        y.append(math.sin(x[0]) + 0.5 * x[1] * x[1] + rng.gauss(0, sigma))
    return X, y


# --- 1. a logística: solucionador clássico × rede de uma camada ---

def gradiente_logistica(w, X, y, lam):
    """∇ da perda média (entropia cruzada) + (λ/2)‖w‖² (o viés também penalizado, para a convexidade forte ser exata)."""
    n, d = len(X), len(w)
    g = [lam * wj for wj in w]
    for x, yi in zip(X, y):
        z = 0.0
        for j in range(d):
            z += w[j] * x[j]
        r = _sig(z) - yi
        for j in range(d):
            g[j] += r * x[j] / n
    return g


def newton_logistica(X, y, lam, iteracoes=30):
    """O solucionador CLÁSSICO (ML): Newton/IRLS, H = XᵀSX/n + λI."""
    d = len(X[0])
    w = [0.0] * d
    for _ in range(iteracoes):
        g = gradiente_logistica(w, X, y, lam)
        H = [[lam if a == b else 0.0 for b in range(d)] for a in range(d)]
        for x in X:
            z = sum(w[j] * x[j] for j in range(d))
            s = _sig(z) * (1 - _sig(z)) / len(X)
            for a in range(d):
                for b in range(d):
                    H[a][b] += s * x[a] * x[b]
        passo = _resolver(H, g)
        w = [wj - pj for wj, pj in zip(w, passo)]
    return w


def constantes_logistica(X, lam):
    """μ = λ (convexidade forte) e L = λ + λ_max(XᵀX)/(4n) (suavidade: σ′ ≤ 1/4), λ_max por iteração de potência."""
    d, n = len(X[0]), len(X)
    G = [[sum(x[a] * x[b] for x in X) / n for b in range(d)] for a in range(d)]
    v = [1.0] * d
    lmax = 0.0
    for _ in range(200):
        u = [sum(G[a][b] * v[b] for b in range(d)) for a in range(d)]
        lmax = math.sqrt(sum(t * t for t in u))
        v = [t / lmax for t in u]
    return lam, lam + lmax / 4.0


def rede_logistica(X, y, lam, passos, lr):
    """A MESMA logística como REDE de uma camada (DL): pesos começando em zero, descida do gradiente (retropropagação = a regra da cadeia
    sobre sigmoide + entropia cruzada, que dá o mesmo p − y)."""
    w = [0.0] * len(X[0])
    for _ in range(passos):
        g = gradiente_logistica(w, X, y, lam)
        w = [wj - lr * gj for wj, gj in zip(w, g)]
    return w


# --- 2. a rede linear profunda × OLS ---

def ols(X, y):
    d = len(X[0])
    A = [[sum(x[a] * x[b] for x in X) for b in range(d)] for a in range(d)]
    c = [sum(x[a] * yi for x, yi in zip(X, y)) for a in range(d)]
    return _resolver(A, c)


def rede_linear_profunda(X, y, h=4, passos=3000, lr=0.02, semente=1, escala=0.1):
    """f(x) = W₂(W₁x), W₁ h×d e W₂ 1×h, sem ativação; perda média quadrática; GD. Devolve o produto β = W₂W₁ (um vetor de d)."""
    rng = random.Random(semente)
    d, n = len(X[0]), len(X)
    W1 = [[rng.gauss(0, escala) for _ in range(d)] for _ in range(h)]
    W2 = [rng.gauss(0, escala) for _ in range(h)]
    for _ in range(passos):
        g1 = [[0.0] * d for _ in range(h)]
        g2 = [0.0] * h
        for x, yi in zip(X, y):
            a = [sum(W1[k][j] * x[j] for j in range(d)) for k in range(h)]
            r = sum(W2[k] * a[k] for k in range(h)) - yi
            for k in range(h):
                g2[k] += 2 * r * a[k] / n
                for j in range(d):
                    g1[k][j] += 2 * r * W2[k] * x[j] / n
        for k in range(h):
            W2[k] -= lr * g2[k]
            for j in range(d):
                W1[k][j] -= lr * g1[k][j]
    return [sum(W2[k] * W1[k][j] for k in range(h)) for j in range(d)]


# --- 3. features de rede + cabeça em forma fechada × rede inteira por retropropagação ---

def _oculta(X, W, b):
    return [[math.tanh(sum(W[k][j] * x[j] for j in range(len(x))) + b[k]) for k in range(len(W))] + [1.0] for x in X]


def ridge(H, y, lam):
    """A cabeça em forma fechada: (HᵀH + λI)⁻¹Hᵀy (o viés, a última coluna, sem penalidade)."""
    d = len(H[0])
    A = [[sum(r[a] * r[b] for r in H) + (lam if a == b and a < d - 1 else 0.0) for b in range(d)] for a in range(d)]
    c = [sum(r[a] * yi for r, yi in zip(H, y)) for a in range(d)]
    return _resolver(A, c)


def mse(H, w, y):
    return sum((sum(a * b for a, b in zip(r, w)) - yi) ** 2 for r, yi in zip(H, y)) / len(y)


def features_aleatorias(Xtr, ytr, Xte, yte, h=40, lam=1e-3, semente=2):
    """DL como ML (1): uma camada oculta tanh ALEATÓRIA, congelada; só a cabeça, por ridge. Devolve o MSE de teste."""
    rng = random.Random(semente)
    W = [[rng.gauss(0, 1) for _ in range(len(Xtr[0]))] for _ in range(h)]
    b = [rng.uniform(-2, 2) for _ in range(h)]
    w = ridge(_oculta(Xtr, W, b), ytr, lam)
    return mse(_oculta(Xte, W, b), w, yte)


def mlp_retropropagacao(Xtr, ytr, Xte, yte, h=40, passos=3000, lr=0.05, semente=2):
    """A rede INTEIRA (camada oculta tanh + cabeça linear), a mesma inicialização das features aleatórias, treinada por retropropagação
    (GD de lote inteiro). Devolve (MSE de teste da rede, W, b treinados)."""
    rng = random.Random(semente)
    d, n = len(Xtr[0]), len(Xtr)
    W = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(h)]
    b = [rng.uniform(-2, 2) for _ in range(h)]
    v = [0.0] * (h + 1)
    for _ in range(passos):
        gW = [[0.0] * d for _ in range(h)]
        gb = [0.0] * h
        gv = [0.0] * (h + 1)
        for x, yi in zip(Xtr, ytr):
            a = [math.tanh(sum(W[k][j] * x[j] for j in range(d)) + b[k]) for k in range(h)] + [1.0]
            r = sum(v[k] * a[k] for k in range(h + 1)) - yi
            for k in range(h + 1):
                gv[k] += 2 * r * a[k] / n
            for k in range(h):
                da = 2 * r * v[k] * (1 - a[k] * a[k]) / n
                gb[k] += da
                for j in range(d):
                    gW[k][j] += da * x[j]
        for k in range(h + 1):
            v[k] -= lr * gv[k]
        for k in range(h):
            b[k] -= lr * gb[k]
            for j in range(d):
                W[k][j] -= lr * gW[k][j]
    return mse(_oculta(Xte, W, b), v, yte), W, b


def features_treinadas_mais_ridge(Xtr, ytr, Xte, yte, W, b, lam=1e-3):
    """DL como ML (2): as features que a retropropagação APRENDEU, congeladas; a cabeça refeita por ridge em forma fechada."""
    w = ridge(_oculta(Xtr, W, b), ytr, lam)
    return mse(_oculta(Xte, W, b), w, yte)


# --- 4. graus de liberdade (a medida clássica) na cabeça de uma rede ---

def df_ridge_fechado(H, lam):
    """tr(S), S = H(HᵀH + λI*)⁻¹Hᵀ (o chapéu da ridge; I* sem o viés), coluna a coluna."""
    d = len(H[0])
    A = [[sum(r[a] * r[b] for r in H) + (lam if a == b and a < d - 1 else 0.0) for b in range(d)] for a in range(d)]
    tot = 0.0
    for i, hi in enumerate(H):
        z = _resolver(A, hi)
        tot += sum(a * b for a, b in zip(hi, z))
    return tot


def df_ridge_efron(H, f, lam, sigma=0.1, reps=400, semente=3):
    """A definição de Efron: df = Σᵢ cov(ŷᵢ, yᵢ)/σ², medida por simulação: y = f + ruído N(0, σ²), ajusta a ridge, mede ŷ."""
    rng = random.Random(semente)
    n = len(H)
    soma_yy = [0.0] * n
    soma_y = [0.0] * n
    soma_yh = [0.0] * n
    for _ in range(reps):
        y = [fi + rng.gauss(0, sigma) for fi in f]
        w = ridge(H, y, lam)
        yh = [sum(a * b for a, b in zip(r, w)) for r in H]
        for i in range(n):
            soma_yy[i] += yh[i] * y[i]
            soma_y[i] += y[i]
            soma_yh[i] += yh[i]
    cov = sum(soma_yy[i] / reps - (soma_y[i] / reps) * (soma_yh[i] / reps) for i in range(n))
    return cov / (sigma * sigma)
