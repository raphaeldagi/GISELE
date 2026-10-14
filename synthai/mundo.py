"""Modelo de mundo latente + controle preditivo (MPC) em Python puro (Parte 93).

Reimplementacao em biblioteca padrao da IDEIA de um pacote recebido do usuario
(modelo_mundo.py, "previsao latente condicionada a acoes e MPC local em um mundo
linear sintetico"): aprender a dinamica de um mundo a partir de transicoes
observadas e planejar acoes nesse modelo aprendido (horizonte receptivo, receding
horizon). NAO roda o codigo recebido; so a ideia, escrita do zero, so +-*/ e sqrt.

Sem rede, sem Popen, sem credenciais, sem aquisicao de recursos, sem
auto-replicacao de processos: os modulos do pacote recebido que fazem isso
(domestico.py: socket.connect; trabalho_continuo.py: Popen/connect) sao RECUSADOS
e nao integrados (ver p2234_recusa_autoreplicacao em calculos.py; regra da Parte 84).

O mundo: estado s em R^2, acao escalar a em [-1, 1]. Dinamica verdadeira linear
determinista  s' = A s + B a, com
    A = [[1, 0.15], [0, 0.9]],  B = [[0], [0.15]].
Uma "posicao" s[0] que integra uma "velocidade" s[1] amortecida, empurrada por a.
"""
import math
import random

# Dinamica verdadeira do mundo (o planejador NAO a conhece; ele aprende Ahat, Bhat).
A_VERDADEIRO = [[1.0, 0.15], [0.0, 0.9]]
B_VERDADEIRO = [[0.0], [0.15]]


def transicao(s, a, A=A_VERDADEIRO, B=B_VERDADEIRO):
    """Um passo da dinamica: s' = A s + B a. s = (s0, s1), a escalar em [-1, 1]."""
    if not (-1.0 - 1e-12 <= a <= 1.0 + 1e-12):
        raise ValueError("acao fora de [-1, 1]")
    s0, s1 = s
    n0 = A[0][0] * s0 + A[0][1] * s1 + B[0][0] * a
    n1 = A[1][0] * s0 + A[1][1] * s1 + B[1][0] * a
    return (n0, n1)


def gerar_transicoes(semente, n):
    """n transicoes (s, a, s') com estados em [-2, 2]^2 e acoes em [-1, 1]."""
    rng = random.Random(semente)
    X, U, Y = [], [], []
    for _ in range(n):
        s = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        a = rng.uniform(-1, 1)
        X.append(s)
        U.append(a)
        Y.append(transicao(s, a))
    return X, U, Y


def resolver_linear(M, b):
    """Resolve M x = b por eliminacao de Gauss com pivoteamento parcial. M quadrada (lista de listas)."""
    n = len(b)
    aug = [list(M[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[piv][col]) < 1e-15:
            raise ValueError("matriz singular")
        aug[col], aug[piv] = aug[piv], aug[col]
        p = aug[col][col]
        for r in range(n):
            if r != col:
                f = aug[r][col] / p
                for c in range(col, n + 1):
                    aug[r][c] -= f * aug[col][c]
    return [aug[i][n] / aug[i][i] for i in range(n)]


def ajustar(X, U, Y):
    """Ajusta Ahat (2x2) e Bhat (2x1) por minimos quadrados (equacoes normais 3x3).

    Regressores z = [s0, s1, a]; para cada saida j, theta_j = (ZtZ)^-1 Zt y_j. Num
    mundo linear sem ruido, recupera A, B ate o erro de ponto flutuante."""
    Z = [[x[0], x[1], u] for x, u in zip(X, U)]
    ZtZ = [[sum(Z[k][i] * Z[k][j] for k in range(len(Z))) for j in range(3)] for i in range(3)]
    Ahat = [[0.0, 0.0], [0.0, 0.0]]
    Bhat = [[0.0], [0.0]]
    for j in range(2):
        Zty = [sum(Z[k][i] * Y[k][j] for k in range(len(Z))) for i in range(3)]
        theta = resolver_linear(ZtZ, Zty)
        Ahat[j][0], Ahat[j][1] = theta[0], theta[1]
        Bhat[j][0] = theta[2]
    return Ahat, Bhat


def erro_modelo(Ahat, Bhat, A=A_VERDADEIRO, B=B_VERDADEIRO):
    """Maior |coeficiente ajustado - verdadeiro| entre A e B."""
    e = 0.0
    for i in range(2):
        for j in range(2):
            e = max(e, abs(Ahat[i][j] - A[i][j]))
        e = max(e, abs(Bhat[i][0] - B[i][0]))
    return e


def rollout(Ahat, Bhat, s0, acoes):
    """Trajetoria prevista pelo modelo aprendido a partir de s0 sob a sequencia de acoes."""
    s = s0
    traj = [s]
    for a in acoes:
        s = transicao(s, a, Ahat, Bhat)
        traj.append(s)
    return traj


def custo_trajetoria(traj, acoes, alvo, peso_acao):
    """Custo = soma das distancias^2 ao alvo (posicao s0) ao longo da trajetoria + peso_acao * soma a^2."""
    c = 0.0
    for s in traj[1:]:
        c += (s[0] - alvo) ** 2 + s[1] * s[1]
    for a in acoes:
        c += peso_acao * a * a
    return c


def mpc(Ahat, Bhat, s0, alvo, H=6, K=64, semente=0, peso_acao=0.05):
    """Controle preditivo: amostra K sequencias de acao de horizonte H (mais a sequencia nula),
    simula cada uma no MODELO APRENDIDO, escolhe a de menor custo previsto e devolve a 1a acao."""
    rng = random.Random(semente)
    candidatos = [[0.0] * H]
    for _ in range(K):
        candidatos.append([rng.uniform(-1, 1) for _ in range(H)])
    melhor, melhor_c = candidatos[0], float("inf")
    for acoes in candidatos:
        traj = rollout(Ahat, Bhat, s0, acoes)
        c = custo_trajetoria(traj, acoes, alvo, peso_acao)
        if c < melhor_c:
            melhor_c, melhor = c, acoes
    return melhor[0]


def acao_reativa(s, alvo, ganho=0.9):
    """Controlador reativo de 1 passo (proporcional ao erro de posicao), saturado em [-1, 1]."""
    a = ganho * (alvo - s[0])
    return max(-1.0, min(1.0, a))


def controlar(politica, s0, alvo, passos=30, **kw):
    """Executa uma politica no mundo VERDADEIRO por `passos`, devolve (custo total realizado, estado final).

    politica(s) -> acao. O custo realizado usa a MESMA metrica do planejador (distancia^2 + velocidade^2),
    sem o termo de acao (mede so o resultado, nao o esforco previsto)."""
    s = s0
    custo = 0.0
    for _ in range(passos):
        a = politica(s)
        a = max(-1.0, min(1.0, a))
        s = transicao(s, a)
        custo += (s[0] - alvo) ** 2 + s[1] * s[1]
    return custo, s


def comparar_mpc_reativo(alvo=1.0, passos=30, H=6, K=64, n_treino=400, semente=0):
    """Compara MPC (no modelo aprendido) com o reativo em 4 condicoes iniciais. Devolve
    (custo medio MPC, custo medio reativo, erro do modelo aprendido, lista por condicao)."""
    X, U, Y = gerar_transicoes(semente, n_treino)
    Ahat, Bhat = ajustar(X, U, Y)
    erro = erro_modelo(Ahat, Bhat)
    iniciais = [(-1.5, 0.0), (1.5, 0.0), (0.0, 1.0), (-1.0, -1.0)]
    por = []
    for i, s0 in enumerate(iniciais):
        pol_mpc = lambda s, _i=i: mpc(Ahat, Bhat, s, alvo, H=H, K=K, semente=1000 + _i)
        pol_re = lambda s: acao_reativa(s, alvo)
        c_mpc, _ = controlar(pol_mpc, s0, alvo, passos)
        c_re, _ = controlar(pol_re, s0, alvo, passos)
        por.append((c_mpc, c_re))
    m_mpc = sum(p[0] for p in por) / len(por)
    m_re = sum(p[1] for p in por) / len(por)
    return m_mpc, m_re, erro, por


# --- Parte 94: o ótimo em forma fechada (LQR) e o mundo não-linear ---

def resolver_riccati(A, B, Q, R, iteracoes=1000, tol=1e-15):
    """Resolve a equação algébrica de Riccati discreta (DARE) por iteração até ponto fixo e devolve o ganho ótimo K (LQR).
    P <- Q + Aᵀ P A − Aᵀ P B (R + Bᵀ P B)⁻¹ Bᵀ P A;  K = (R + Bᵀ P B)⁻¹ Bᵀ P A. A = 2x2, B = 2x1, R escalar.
    Controle ótimo: u = −K (s − s*). Só +−×÷ (R + BᵀPB é escalar, invertido por divisão)."""
    def matmul(M, N):
        return [[sum(M[i][k] * N[k][j] for k in range(len(N))) for j in range(len(N[0]))] for i in range(len(M))]
    def T(M):
        return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
    At, Bt = T(A), T(B)
    P = [row[:] for row in Q]
    Kant = None
    for _ in range(iteracoes):
        AtP = matmul(At, P)              # 2x2
        BtP = matmul(Bt, P)              # 1x2
        BtPB = matmul(BtP, B)[0][0]      # escalar
        s = R + BtPB
        BtPA = matmul(BtP, A)            # 1x2
        K = [[BtPA[0][j] / s for j in range(2)]]   # 1x2
        AtPA = matmul(AtP, A)            # 2x2
        AtPB = matmul(AtP, B)            # 2x1
        # Aᵀ P B (1/s) Bᵀ P A  = AtPB * K
        corr = [[AtPB[i][0] * K[0][j] for j in range(2)] for i in range(2)]
        Pnovo = [[Q[i][j] + AtPA[i][j] - corr[i][j] for j in range(2)] for i in range(2)]
        if Kant is not None and max(abs(K[0][j] - Kant[0][j]) for j in range(2)) < tol:
            P = Pnovo
            break
        P, Kant = Pnovo, K
    return K  # 1x2


def acao_lqr(s, alvo, K):
    """Controle ótimo linear-quadrático: u = −K (s − s*), s* = (alvo, 0), saturado em [−1, 1]."""
    dx0, dx1 = s[0] - alvo, s[1] - 0.0
    u = -(K[0][0] * dx0 + K[0][1] * dx1)
    return max(-1.0, min(1.0, u))


def transicao_nl(s, a, kappa=0.1, A=A_VERDADEIRO, B=B_VERDADEIRO):
    """Mundo NÃO-LINEAR: a mesma dinâmica linear mais um termo cúbico de enrijecimento na velocidade,
    s1' += −kappa·s1³ (uma mola que endurece). Com kappa=0 recupera o mundo linear da Parte 93."""
    if not (-1.0 - 1e-12 <= a <= 1.0 + 1e-12):
        raise ValueError("acao fora de [-1, 1]")
    s0, s1 = s
    n0 = A[0][0] * s0 + A[0][1] * s1 + B[0][0] * a
    n1 = A[1][0] * s0 + A[1][1] * s1 + B[1][0] * a - kappa * s1 * s1 * s1
    return (n0, n1)


def gerar_transicoes_nl(semente, n, kappa=0.1):
    rng = random.Random(semente)
    X, U, Y = [], [], []
    for _ in range(n):
        s = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        a = rng.uniform(-1, 1)
        X.append(s)
        U.append(a)
        Y.append(transicao_nl(s, a, kappa))
    return X, U, Y


def ajustar_cubico(X, U, Y):
    """Mínimos quadrados com a base AMPLIADA z = [s0, s1, a, s1³] (equações normais 4x4). Num mundo com termo cúbico
    em s1, essa base contém a dinâmica verdadeira e o ajuste volta a ser exato (álgebra, não estatística)."""
    Z = [[x[0], x[1], u, x[1] ** 3] for x, u in zip(X, U)]
    m = len(Z[0])
    ZtZ = [[sum(Z[k][i] * Z[k][j] for k in range(len(Z))) for j in range(m)] for i in range(m)]
    thetas = []
    for j in range(2):
        Zty = [sum(Z[k][i] * Y[k][j] for k in range(len(Z))) for i in range(m)]
        thetas.append(resolver_linear(ZtZ, Zty))
    return thetas  # [theta_s0, theta_s1], cada um com 4 coeficientes [s0, s1, a, s1^3]


def residuo_ajuste(thetas_ou_AB, X, U, Y, cubico=False):
    """A raiz do erro quadrático médio do modelo nas transições (X,U)->Y. Mede o VIÉS DE FORMA: um modelo linear num
    mundo não-linear tem resíduo que NÃO vai a zero com n (platô), ao contrário do caso linear (resíduo ~ epsilon)."""
    import math
    soma = 0.0
    for x, u, y in zip(X, U, Y):
        if cubico:
            z = [x[0], x[1], u, x[1] ** 3]
            pred = [sum(z[i] * thetas_ou_AB[j][i] for i in range(len(z))) for j in range(2)]
        else:
            Ahat, Bhat = thetas_ou_AB
            pred = [Ahat[0][0] * x[0] + Ahat[0][1] * x[1] + Bhat[0][0] * u,
                    Ahat[1][0] * x[0] + Ahat[1][1] * x[1] + Bhat[1][0] * u]
        soma += (pred[0] - y[0]) ** 2 + (pred[1] - y[1]) ** 2
    return math.sqrt(soma / len(Y))


def controlar_nl(politica, s0, alvo, passos=30, kappa=0.1):
    """Como `controlar`, mas executa no mundo NÃO-LINEAR (transicao_nl). O planejador pode usar um modelo linear aprendido;
    a execução e o custo usam a dinâmica verdadeira (não-linear)."""
    s = s0
    custo = 0.0
    for _ in range(passos):
        a = max(-1.0, min(1.0, politica(s)))
        s = transicao_nl(s, a, kappa)
        custo += (s[0] - alvo) ** 2 + s[1] * s[1]
    return custo, s


# --- Parte 96: aprender a base (features dadas vs. aprendidas) ---

def monomios(grau):
    """Mapa de características: todos os monômios de (s0, s1, a) até `grau` (inclui a constante 1). Devolve feat(s0,s1,a)->lista."""
    expoentes = []
    for i in range(grau + 1):
        for j in range(grau + 1 - i):
            for k in range(grau + 1 - i - j):
                expoentes.append((i, j, k))

    def feat(s0, s1, a):
        return [(s0 ** i) * (s1 ** j) * (a ** k) for (i, j, k) in expoentes]
    feat.m = len(expoentes)
    return feat


def ajustar_features(X, U, Y, feat):
    """Mínimos quadrados genéricos com um mapa de características `feat(s0,s1,a)->vetor` (equações normais m×m, uma solução por
    saída). Devolve a lista de vetores de pesos [theta_s0, theta_s1]."""
    Z = [feat(x[0], x[1], u) for x, u in zip(X, U)]
    m = len(Z[0])
    ZtZ = [[sum(Z[t][i] * Z[t][j] for t in range(len(Z))) for j in range(m)] for i in range(m)]
    # regularização de Tikhonov minúscula para estabilizar bases grandes (não muda o caso de posto cheio)
    for i in range(m):
        ZtZ[i][i] += 1e-12
    thetas = []
    for d in range(2):
        Zty = [sum(Z[t][i] * Y[t][d] for t in range(len(Z))) for i in range(m)]
        thetas.append(resolver_linear(ZtZ, Zty))
    return thetas


def residuo_features(thetas, X, U, Y, feat):
    """RMS do erro de predição de um modelo de características `feat` com pesos `thetas`."""
    soma = 0.0
    for x, u, y in zip(X, U, Y):
        z = feat(x[0], x[1], u)
        pred = [sum(z[i] * thetas[d][i] for i in range(len(z))) for d in range(2)]
        soma += (pred[0] - y[0]) ** 2 + (pred[1] - y[1]) ** 2
    return math.sqrt(soma / len(Y))


class MLP1:
    """MLP de uma camada escondida (tanh), entradas (s0,s1,a) -> 2 saídas, treinada por gradiente. APRENDE as características
    (os pesos da camada escondida), em vez de recebê-las. Só biblioteca padrão."""
    def __init__(self, h=8, semente=96):
        rng = random.Random(semente)
        self.h = h
        self.W1 = [[rng.uniform(-0.5, 0.5) for _ in range(3)] for _ in range(h)]
        self.b1 = [0.0] * h
        self.W2 = [[rng.uniform(-0.5, 0.5) for _ in range(h)] for _ in range(2)]
        self.b2 = [0.0, 0.0]

    def _forward(self, x):
        z = [sum(self.W1[j][k] * x[k] for k in range(3)) + self.b1[j] for j in range(self.h)]
        hid = [math.tanh(v) for v in z]
        out = [sum(self.W2[d][j] * hid[j] for j in range(self.h)) + self.b2[d] for d in range(2)]
        return hid, out

    def prever(self, s0, s1, a):
        return self._forward([s0, s1, a])[1]

    def treinar(self, X, U, Y, passos=4000, lr=0.02, semente=96):
        rng = random.Random(semente)
        n = len(X)
        dados = [([X[i][0], X[i][1], U[i]], Y[i]) for i in range(n)]
        for _ in range(passos):
            x, y = dados[rng.randrange(n)]
            hid, out = self._forward(x)
            dout = [out[d] - y[d] for d in range(2)]  # gradiente do MSE/2
            for d in range(2):
                for j in range(self.h):
                    self.W2[d][j] -= lr * dout[d] * hid[j]
                self.b2[d] -= lr * dout[d]
            dhid = [sum(dout[d] * self.W2[d][j] for d in range(2)) * (1.0 - hid[j] * hid[j]) for j in range(self.h)]
            for j in range(self.h):
                for k in range(3):
                    self.W1[j][k] -= lr * dhid[j] * x[k]
                self.b1[j] -= lr * dhid[j]
        return self

    def residuo(self, X, U, Y):
        soma = 0.0
        for x, u, y in zip(X, U, Y):
            out = self.prever(x[0], x[1], u)
            soma += (out[0] - y[0]) ** 2 + (out[1] - y[1]) ** 2
        return math.sqrt(soma / len(Y))


# --- Parte 97: a cura da variância (ridge) e a capacidade do MLP ---

def ajustar_features_ridge(X, U, Y, feat, lam):
    """Mínimos quadrados com penalidade de cumeeira (ridge): resolve (ZᵀZ + λI)·θ = Zᵀy. λ grande encolhe os pesos (mais viés,
    menos variância); λ → 0 recupera o ajuste comum. A constante (monômio 1) também é penalizada aqui (simples e suficiente para o brinquedo)."""
    Z = [feat(x[0], x[1], u) for x, u in zip(X, U)]
    m = len(Z[0])
    ZtZ = [[sum(Z[t][i] * Z[t][j] for t in range(len(Z))) for j in range(m)] for i in range(m)]
    for i in range(m):
        ZtZ[i][i] += lam
    thetas = []
    for d in range(2):
        Zty = [sum(Z[t][i] * Y[t][d] for t in range(len(Z))) for i in range(m)]
        thetas.append(resolver_linear(ZtZ, Zty))
    return thetas


def ridge_sweep(grau=5, n=40, kappa=0.1, lams=(0.0, 1e-4, 1e-2, 1e-1, 1.0, 10.0), semente_tr=0, semente_te=777):
    """Varre λ no ajuste de uma base rica (grau alto) com poucos dados. Devolve [(λ, res_treino, res_teste)] e (λ*, melhor res_teste).
    Espera-se uma curva em U no teste: λ=0 superajusta (teste alto), λ grande subajusta, há um λ* no meio."""
    Xtr, Utr, Ytr = gerar_transicoes_nl(semente_tr, n, kappa)
    Xte, Ute, Yte = gerar_transicoes_nl(semente_te, 400, kappa)
    f = monomios(grau)
    linha = []
    for lam in lams:
        th = ajustar_features_ridge(Xtr, Utr, Ytr, f, lam)
        linha.append((lam, residuo_features(th, Xtr, Utr, Ytr, f), residuo_features(th, Xte, Ute, Yte, f)))
    melhor = min(linha, key=lambda r: r[2])
    return linha, (melhor[0], melhor[2])


def mlp_capacidade(hs=(2, 4, 8, 16), kappa=0.1, passos=8000, lr=0.02, semente=97):
    """Resíduo de teste do MLP em função da largura h da camada escondida. Devolve [(h, res_teste)]. Mais capacidade -> menos viés
    (num mundo com dados de sobra), mas não necessariamente monótono por causa do treino estocástico."""
    Xtr, Utr, Ytr = gerar_transicoes_nl(0, 400, kappa)
    Xte, Ute, Yte = gerar_transicoes_nl(777, 400, kappa)
    out = []
    for h in hs:
        m = MLP1(h=h, semente=semente).treinar(Xtr, Utr, Ytr, passos=passos, lr=lr, semente=semente)
        out.append((h, m.residuo(Xte, Ute, Yte)))
    return out
