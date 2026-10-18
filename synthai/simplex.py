"""O simplex próprio e o pôquer de Kuhn COMPLETO (Parte 112). Biblioteca padrão; o mesmo código roda sobre `Fraction` (exato) e
sobre `float` (para o diálogo bit a bit), porque só usa +, −, ×, ÷ e comparações.

Um jogo de soma zero n×m vira um programa linear (von Neumann/Dantzig): soma-se c a todas as entradas para o valor ficar positivo, e a
COLUNA resolve  max Σw  s.a.  A·w ≤ 1, w ≥ 0  (a origem é viável, as folgas formam a base inicial). No ótimo, o valor do jogo
deslocado é 1/Σw, a estratégia da coluna é w/Σw, e a da LINHA sai dos preços duais (os custos reduzidos das folgas). A regra de Bland
(menor índice que entra; empate na razão mínima, menor índice básico) garante que o método termina, sem ciclar."""

from fractions import Fraction
from itertools import product


def simplex_max(A, b, c, zero=0):
    """max c·x s.a. A·x ≤ b, x ≥ 0, com b ≥ 0 (base inicial = folgas). Devolve (valor, x, y_dual, pivôs). Regra de Bland."""
    n, m = len(A), len(A[0])
    T = [list(A[i]) + [1 if j == i else 0 for j in range(n)] + [b[i]] for i in range(n)]
    T = [[x * (zero + 1) if isinstance(x, int) else x for x in linha] for linha in T]   # leva os 0/1 inteiros ao tipo numérico
    obj = [-cj for cj in c] + [zero] * n + [zero]
    base = [m + i for i in range(n)]
    pivos = 0
    while True:
        entra = next((j for j in range(m + n) if obj[j] < 0), None)
        if entra is None:
            break
        sai, melhor = None, None
        for i in range(n):
            if T[i][entra] > 0:
                razao = T[i][-1] / T[i][entra]
                if melhor is None or razao < melhor or (razao == melhor and base[i] < base[sai]):
                    sai, melhor = i, razao
        if sai is None:
            raise ValueError("ilimitado")
        p = T[sai][entra]
        T[sai] = [x / p for x in T[sai]]
        for i in range(n):
            if i != sai and T[i][entra] != 0:
                f = T[i][entra]
                T[i] = [x - f * y for x, y in zip(T[i], T[sai])]
        f = obj[entra]
        obj = [x - f * y for x, y in zip(obj, T[sai])]
        base[sai] = entra
        pivos += 1
    x = [zero] * m
    for i, j in enumerate(base):
        if j < m:
            x[j] = T[i][-1]
    y = [obj[m + i] for i in range(n)]   # preços duais = custos reduzidos das folgas
    return obj[-1], x, y, pivos


def resolver_jogo(A, exato=True):
    """O valor e as estratégias ótimas (linha, coluna) do jogo de soma zero A (payoff para a LINHA), pelo simplex.
    Devolve (valor, p_linha, q_coluna, pivôs)."""
    conv = Fraction if exato else float
    A = [[conv(x) for x in linha] for linha in A]
    zero, um = conv(0), conv(1)
    menor = min(min(linha) for linha in A)
    desloc = (um - menor) if menor <= 0 else zero
    B = [[x + desloc for x in linha] for linha in A]
    n, m = len(B), len(B[0])
    val, w, u, pivos = simplex_max(B, [um] * n, [um] * m, zero=zero)
    v_desl = um / val
    q = [wj * v_desl for wj in w]
    p = [ui * v_desl for ui in u]
    return v_desl - desloc, p, q, pivos


def valor_contra(A, p, q):
    """p·A·q, o payoff esperado da linha."""
    tot = 0
    for i, pi in enumerate(p):
        for j, qj in enumerate(q):
            tot += pi * A[i][j] * qj
    return tot


def dualidade(A, p, q):
    """(min_j (pA)_j, max_i (Aq)_i): no equilíbrio os dois são o valor (maxmin = minmax)."""
    n, m = len(A), len(A[0])
    pior_linha = min(sum(p[i] * A[i][j] for i in range(n)) for j in range(m))
    melhor_coluna = max(sum(A[i][j] * q[j] for j in range(m)) for i in range(n))
    return pior_linha, melhor_coluna


# --- pôquer de Kuhn completo (J=1, Q=2, K=3; cada um põe 1; aposta de 1) ---

P1_ACOES = ("aposta", "passa-desiste", "passa-paga")        # por carta do jogador 1
P2_ACOES = tuple(product(("desiste", "paga"), ("passa", "aposta")))  # por carta: (contra aposta, contra passe)


def _payoff_kuhn(c1, c2, a1, a2):
    """Payoff do JOGADOR 1 numa distribuição (c1, c2), com a ação a1 do jogador 1 e o par a2 = (contra aposta, contra passe) do 2."""
    ganha = 1 if c1 > c2 else -1
    contra_aposta, contra_passe = a2
    if a1 == "aposta":
        return 1 if contra_aposta == "desiste" else 2 * ganha
    if contra_passe == "passa":
        return ganha
    return -1 if a1 == "passa-desiste" else 2 * ganha


def kuhn_forma_normal():
    """A matriz 27×64 do pôquer de Kuhn: linhas = estratégias puras do jogador 1 (uma ação por carta), colunas = do jogador 2
    (um par por carta); entrada = média exata (Fraction) sobre as 6 distribuições. Devolve (A, linhas, colunas)."""
    linhas = list(product(P1_ACOES, repeat=3))
    colunas = list(product(P2_ACOES, repeat=3))
    A = []
    for s1 in linhas:
        linha = []
        for s2 in colunas:
            tot = Fraction(0)
            for c1 in (1, 2, 3):
                for c2 in (1, 2, 3):
                    if c1 != c2:
                        tot += Fraction(_payoff_kuhn(c1, c2, s1[c1 - 1], s2[c2 - 1]), 6)
            linha.append(tot)
        A.append(linha)
    return A, linhas, colunas


def comportamento(estrategias, pesos, carta, pos, acao):
    """A probabilidade de comportamento: a massa das estratégias puras que, com a `carta`, tomam `acao` na posição `pos`
    (pos = None para o jogador 1; 0 = contra aposta, 1 = contra passe, para o jogador 2)."""
    tot = 0
    for s, w in zip(estrategias, pesos):
        a = s[carta - 1] if pos is None else s[carta - 1][pos]
        if a == acao or (pos is None and acao == "passa" and a.startswith("passa")):
            tot += w
    return tot


def jogo_lcg(linhas=4, colunas=5, semente=112):
    """A fixture da Parte 112 (escrita no pré-registro): entradas (x mod 11) − 5, x pelo LCG x ← (1103515245x + 12345) mod 2³¹, linha por linha."""
    x, A = semente, []
    for _ in range(linhas):
        linha = []
        for _ in range(colunas):
            x = (1103515245 * x + 12345) % 2147483648
            linha.append(x % 11 - 5)
        A.append(linha)
    return A
