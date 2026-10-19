"""As camadas contrapostas com MATRIZES (Parte 117; a pendência da Parte 115). Biblioteca padrão.

Uma cadeia linear de 10 camadas h_k = W_k h_{k−1} em d = 8 dimensões. O jacobiano de ponta a ponta é o produto J = W_10 ⋯ W_1. Na Parte 115 a
cadeia era escalar e "contrapor" era alternar a e 1/a; com matrizes há três maneiras:
- a mesma matriz ortogonal escalada, (aQ)¹⁰: todas as direções crescem igual (valores singulares todos a¹⁰);
- W e W⁻¹ alternadas: o produto é a identidade, a menos do arredondamento (que cresce com o número de condição de W);
- Q e Qᵀ alternadas (a inversa da ortogonal é a transposta, sem eliminação): o produto é a identidade com o arredondamento de produtos só.
E, para comparar, 10 matrizes gaussianas INDEPENDENTES N(0, 1/d): o log do |det| do produto tem média e variância em forma fechada
(o |det| é multiplicativo, e o det de uma gaussiana é um produto de raízes de qui-quadrados independentes: Bartlett)."""

import math
import random


def gaussiana(d, rng, escala=None):
    s = escala if escala is not None else 1.0 / math.sqrt(d)
    return [[rng.gauss(0.0, s) for _ in range(d)] for _ in range(d)]


def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    C = [[0.0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            a = A[i][k]
            if a != 0.0:
                Bk = B[k]
                Ci = C[i]
                for j in range(p):
                    Ci[j] += a * Bk[j]
    return C


def transposta(A):
    return [list(c) for c in zip(*A)]


def identidade(d):
    return [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]


def ortogonal(d, rng):
    """Q de Gram-Schmidt modificado (duas passadas) sobre colunas gaussianas."""
    cols = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(d)]
    qs = []
    for v in cols:
        v = list(v)
        for _ in range(2):
            for q in qs:
                p = 0.0
                for a, b in zip(v, q):
                    p += a * b
                for i in range(d):
                    v[i] -= p * q[i]
        n = math.sqrt(sum(x * x for x in v))
        qs.append([x / n for x in v])
    return transposta(qs)          # as colunas de Q são os qs


def inversa(A):
    """Gauss-Jordan com pivô parcial. Só +, −, ×, ÷ (traduzido bit a bit na rodada 84)."""
    d = len(A)
    M = [list(A[i]) + identidade(d)[i] for i in range(d)]
    for c in range(d):
        p = c
        for r in range(c + 1, d):
            if abs(M[r][c]) > abs(M[p][c]):
                p = r
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for r in range(d):
            if r != c:
                f = M[r][c]
                if f != 0.0:
                    M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [linha[d:] for linha in M]


def produto_cadeia(mats):
    """J = W_L ⋯ W_1 (mats[0] é a primeira camada)."""
    J = identidade(len(mats[0]))
    for W in mats:
        J = matmul(W, J)
    return J


def jacobi_autovalores(S, varreduras=60):
    """Autovalores de uma simétrica por Jacobi cíclico."""
    d = len(S)
    A = [list(l) for l in S]
    for _ in range(varreduras):
        fora = sum(A[i][j] * A[i][j] for i in range(d) for j in range(d) if i != j)
        if fora < 1e-300:
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if abs(A[p][q]) < 1e-300:
                    continue
                th = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(d):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(A[i][i] for i in range(d))


def valores_singulares(J):
    """Os valores singulares de J, decrescentes, pelas raízes dos autovalores de JᵀJ (Jacobi)."""
    return sorted((math.sqrt(max(x, 0.0)) for x in jacobi_autovalores(matmul(transposta(J), J))), reverse=True)


def log_abs_det(A):
    """ln|det A| por eliminação com pivô parcial."""
    d = len(A)
    M = [list(l) for l in A]
    s = 0.0
    for c in range(d):
        p = max(range(c, d), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        s += math.log(abs(piv))
        for r in range(c + 1, d):
            f = M[r][c] / piv
            M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return s


def max_abs_menos_identidade(J):
    return max(abs(J[i][j] - (1.0 if i == j else 0.0)) for i in range(len(J)) for j in range(len(J)))


def numero_de_condicao(W):
    sv = valores_singulares(W)
    return sv[0] / sv[-1]


# --- formas fechadas (digama e trigama) ---

def digama(x):
    r = 0.0
    while x < 8.0:
        r -= 1.0 / x
        x += 1.0
    f = 1.0 / (x * x)
    return r + math.log(x) - 0.5 / x - f * (1.0 / 12 - f * (1.0 / 120 - f * (1.0 / 252 - f / 240)))


def trigama(x):
    r = 0.0
    while x < 8.0:
        r += 1.0 / (x * x)
        x += 1.0
    f = 1.0 / (x * x)
    return r + 1.0 / x + f / 2 + (1.0 / x) * f * (1.0 / 6 - f * (1.0 / 30 - f / 42))


def lyapunov_gaussiano(d):
    """Os expoentes de Lyapunov do produto de gaussianas N(0, 1/d) d×d (Newman 1986): λ_i = ½[ln(2/d) + ψ((d − i + 1)/2)]."""
    return [0.5 * (math.log(2.0 / d) + digama((d - i + 1) / 2.0)) for i in range(1, d + 1)]


def log_det_fechado(d):
    """E e Var de ln|det W| para W gaussiana N(0, 1/d) d×d: |det|² = d^(−d)·Π χ²_{d−i+1} (Bartlett). E = Σλ_i; Var = ¼ Σ ψ′((d − i + 1)/2)."""
    return sum(lyapunov_gaussiano(d)), 0.25 * sum(trigama((d - i + 1) / 2.0) for i in range(1, d + 1))


# --- fixtures da Parte 117 ---

D, L = 8, 10


def cadeia_ortogonal_escalada(a=1.2, semente=1170):
    Q = ortogonal(D, random.Random(semente))
    return produto_cadeia([[[a * x for x in l] for l in Q]] * L)


def cadeia_contraposta_inversa(semente=1171):
    W = gaussiana(D, random.Random(semente))
    Wi = inversa(W)
    return produto_cadeia([W if k % 2 == 0 else Wi for k in range(L)]), numero_de_condicao(W)


def cadeia_contraposta_ortogonal(semente=1172):
    Q = ortogonal(D, random.Random(semente))
    return produto_cadeia([Q if k % 2 == 0 else transposta(Q) for k in range(L)])


def gaussianas_independentes(amostras=2000, semente=1173):
    """ln|det J|/L e ln σ_max(J)/L de produtos de L gaussianas independentes."""
    rng = random.Random(semente)
    dets, tops = [], []
    for _ in range(amostras):
        mats = [gaussiana(D, rng) for _ in range(L)]
        J = produto_cadeia(mats)
        dets.append(sum(log_abs_det(W) for W in mats) / L)
        tops.append(math.log(valores_singulares(J)[0]) / L)
    return dets, tops


def superposicao_matricial(eps, semente=1174):
    """Δh real (as 10 matrizes mudam juntas por eps·E_k) contra Σ_k ⟨∂h/∂W_k, eps·E_k⟩ numa cadeia tanh com W_k = Q_k (ortogonais). O
    gradiente de u·h_L em relação a W_k é (δ_k)(h_{k−1})ᵀ. Devolve |Δ(u·h) − Σ|."""
    rng = random.Random(semente)
    Ws = [ortogonal(D, rng) for _ in range(L)]
    Es = [gaussiana(D, rng, 1.0) for _ in range(L)]
    h0 = [rng.gauss(0.0, 1.0) for _ in range(D)]
    u = [rng.gauss(0.0, 1.0) for _ in range(D)]

    def frente(mats):
        hs = [h0]
        for W in mats:
            hs.append([math.tanh(sum(W[i][j] * hs[-1][j] for j in range(D))) for i in range(D)])
        return hs
    hs = frente(Ws)
    g = list(u)                                      # ∂(u·h_L)/∂h_k, de trás para frente
    lin = 0.0
    for k in range(L - 1, -1, -1):
        delta = [g[i] * (1.0 - hs[k + 1][i] * hs[k + 1][i]) for i in range(D)]
        lin += sum(delta[i] * hs[k][j] * eps * Es[k][i][j] for i in range(D) for j in range(D))
        g = [sum(Ws[k][i][j] * delta[i] for i in range(D)) for j in range(D)]
    hs2 = frente([[[w + eps * e for w, e in zip(lw, le)] for lw, le in zip(W, E)] for W, E in zip(Ws, Es)])
    dot = lambda x: sum(a * b for a, b in zip(u, x))
    return abs((dot(hs2[-1]) - dot(hs[-1])) - lin)


def variancia_log_det(amostras=20000, semente=1176):
    """(k) da Parte 117: a variância amostral de ln|det W| para W gaussiana N(0, 1/d) d×d, contra ¼ Σ ψ′((d − i + 1)/2)."""
    rng = random.Random(semente)
    xs = [log_abs_det(gaussiana(D, rng)) for _ in range(amostras)]
    mu = sum(xs) / amostras
    return mu, sum((x - mu) ** 2 for x in xs) / (amostras - 1)


def log_det_produto(amostras=20000, semente=1180):
    """(a)/(b) da Parte 118: o 3º lote, GRANDE, de ln|det J|/L = (1/L) Σ ln|det W_k| (só o det, sem os valores singulares). Devolve (média, desvio)."""
    rng = random.Random(semente)
    xs = []
    for _ in range(amostras):
        xs.append(sum(log_abs_det(gaussiana(D, rng)) for _ in range(L)) / L)
    mu = sum(xs) / amostras
    return mu, math.sqrt(sum((x - mu) ** 2 for x in xs) / (amostras - 1))
