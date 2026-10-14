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
