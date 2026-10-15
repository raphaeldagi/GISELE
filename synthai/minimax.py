"""O minimax de von Neumann (Parte 108): o equilíbrio de um jogo de soma zero. Offline, só biblioteca padrão. Dois caminhos:
a FÓRMULA FECHADA do jogo 2×2 sem sela, e o JOGO FICTÍCIO (fictitious play: cada jogador joga a melhor resposta ao
histórico médio do outro; Robinson 1951 prova que a média converge ao valor). Só +, −, ×, ÷, argmax e comparações —
nenhuma transcendental, portável por construção (Parte 52)."""

JOGO_TESTE = [[1.0, -1.0], [-2.0, 3.0]]     # sem sela -> mistura, valor 1/7
JOGO_SELA = [[3.0, 1.0], [2.0, 0.0]]         # sela em (0,1) = 1


def tem_sela(A):
    """Devolve o valor da sela (maxmin = minmax) se houver ponto de sela puro, senão None."""
    maxmin = max(min(linha) for linha in A)
    minmax = min(max(A[i][j] for i in range(len(A))) for j in range(len(A[0])))
    return maxmin if maxmin == minmax else None


def valor_2x2(A):
    """O valor de um jogo 2×2 de soma zero por forma fechada: se há sela, é ela; senão v = (ad − bc)/(a+d−b−c)."""
    s = tem_sela(A)
    if s is not None:
        return s
    (a, b), (c, d) = A
    return (a * d - b * c) / (a + d - b - c)


def estrategia_linha_2x2(A):
    """A estratégia ótima do jogador de linha (prob da linha 0): sela -> pura (1 ou 0); senão p = (d − c)/(a+d−b−c)."""
    s = tem_sela(A)
    if s is not None:
        # joga puro a linha cujo mínimo é o maxmin
        return 1.0 if min(A[0]) >= min(A[1]) else 0.0
    (a, b), (c, d) = A
    return (d - c) / (a + d - b - c)


def valor_por_estrategias(A, p):
    """maxmin pela ótica da linha: com a linha jogando (p, 1−p), o adversário escolhe a coluna de menor payoff para a linha.
    Devolve esse mínimo garantido (que, na p ótima, é o valor)."""
    col0 = p * A[0][0] + (1 - p) * A[1][0]
    col1 = p * A[0][1] + (1 - p) * A[1][1]
    return min(col0, col1)


def estrategia_coluna_2x2(A):
    """A estratégia ótima do jogador de coluna (prob da coluna 0): q = (d − b)/(a+d−b−c) (sem sela)."""
    s = tem_sela(A)
    if s is not None:
        return 1.0 if max(A[0][0], A[1][0]) <= max(A[0][1], A[1][1]) else 0.0
    (a, b), (c, d) = A
    return (d - b) / (a + d - b - c)


def minmax_por_coluna(A, q):
    """minmax pela ótica da coluna: com a coluna jogando (q, 1−q), a linha escolhe a de maior payoff; devolve esse máximo."""
    lin0 = q * A[0][0] + (1 - q) * A[0][1]
    lin1 = q * A[1][0] + (1 - q) * A[1][1]
    return max(lin0, lin1)


def jogo_ficticio(A, iteracoes=2000):
    """Jogo fictício (Robinson): cada jogador joga a melhor resposta à frequência histórica do outro; o valor é estimado pela
    média de (maxmin do histórico da linha, minmax do histórico da coluna)/2 — converge ao valor. Só somas, argmax, comparações.
    Devolve a estimativa do valor."""
    m, n = len(A), len(A[0])
    cont_lin = [0] * m   # quantas vezes a linha jogou cada ação
    cont_col = [0] * n
    # payoff acumulado da coluna se a linha jogar o histórico (para a coluna escolher a melhor resposta) e vice-versa
    ganho_col = [0.0] * n   # payoff para a LINHA de cada coluna, contra o histórico da linha
    ganho_lin = [0.0] * m
    cont_lin[0] += 1        # início arbitrário
    for j in range(n):
        ganho_col[j] += A[0][j]
    v_sup, v_inf = [], []
    for _ in range(iteracoes):
        # coluna: melhor resposta = coluna de MENOR ganho para a linha
        jc = 0
        for j in range(1, n):
            if ganho_col[j] < ganho_col[jc]:
                jc = j
        cont_col[jc] += 1
        for i in range(m):
            ganho_lin[i] += A[i][jc]
        # linha: melhor resposta = linha de MAIOR ganho para a linha
        il = 0
        for i in range(1, m):
            if ganho_lin[i] > ganho_lin[il]:
                il = i
        cont_lin[il] += 1
        for j in range(n):
            ganho_col[j] += A[il][j]
        t_lin = sum(cont_lin)
        t_col = sum(cont_col)
        v_sup.append(max(ganho_lin) / t_col)   # cota superior do valor
        v_inf.append(min(ganho_col) / t_lin)   # cota inferior
    return (v_sup[-1] + v_inf[-1]) / 2.0
