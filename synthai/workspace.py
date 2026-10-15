"""Parte 102: um Global Workspace (GWT) minimo em biblioteca padrao — reimplementacao da IDEIA de workspace_global.py (recebida,
auditada por AST, NAO executada): varios modulos especialistas propoem, um vence por SALIENCIA (quanto reduz o residuo), e a sua
contribuicao e TRANSMITIDA (broadcast) a todos no proximo passo. A pergunta: a integracao global bate os especialistas ISOLADOS
quando a tarefa precisa combinar dois? So +-*/; sem rede, sem threads, sem Popen; deterministico (semente fixa)."""

import math
import random


def _ols_1d(xs, ys):
    """Minimos quadrados de uma reta y = c*x (sem intercepto) por forma fechada: c = sum(x*y)/sum(x*x)."""
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    return sxy / sxx if sxx else 0.0


def gerar_mundo(semente, n, a=1.0, b=1.0):
    """n amostras (x1, x2) ~ U(-1,1) e alvo y = a*x1 + b*x2. Devolve (X1, X2, Y)."""
    rng = random.Random(semente)
    X1 = [rng.uniform(-1, 1) for _ in range(n)]
    X2 = [rng.uniform(-1, 1) for _ in range(n)]
    Y = [a * X1[i] + b * X2[i] for i in range(n)]
    return X1, X2, Y


def _rmse(pred, Y):
    return math.sqrt(sum((p - y) ** 2 for p, y in zip(pred, Y)) / len(Y))


def especialista_isolado(Xvis, Y):
    """Um especialista que so VE a sua caracteristica: ajusta y = c*xvis e preve. Devolve (predicoes, rmse)."""
    c = _ols_1d(Xvis, Y)
    pred = [c * x for x in Xvis]
    return pred, _rmse(pred, Y)


def workspace_global(X1, X2, Y, passos=8):
    """O Global Workspace: dois especialistas (A ve x1, B ve x2) refinam por turnos o RESIDUO transmitido no quadro-negro.
    Turno: o especialista ajusta a SUA caracteristica ao residuo atual (y - broadcast), soma a sua contribuicao ao broadcast, e
    transmite o novo residuo. E a descida por coordenadas (Gauss-Seidel) sobre a regressao conjunta — a integracao recupera o que
    nenhum ve sozinho. Devolve (predicoes, rmse, numero de passos ate convergir)."""
    n = len(Y)
    broadcast = [0.0] * n     # o quadro-negro: a estimativa comum de y
    c1 = c2 = 0.0
    ult = None
    convergiu = passos
    for t in range(passos):
        # especialista A: ajusta x1 ao residuo (y - parte de B)
        resid_a = [Y[i] - c2 * X2[i] for i in range(n)]
        c1 = _ols_1d(X1, resid_a)
        # especialista B: ajusta x2 ao residuo (y - parte de A)
        resid_b = [Y[i] - c1 * X1[i] for i in range(n)]
        c2 = _ols_1d(X2, resid_b)
        broadcast = [c1 * X1[i] + c2 * X2[i] for i in range(n)]
        r = _rmse(broadcast, Y)
        if ult is not None and abs(ult - r) < 1e-12:
            convergiu = t + 1
            break
        ult = r
    return broadcast, _rmse(broadcast, Y), convergiu


def comparar_isolado_vs_workspace(semente=102, n=400, a=1.0, b=1.0):
    """Compara o melhor especialista ISOLADO com o Global Workspace. Devolve (rmse melhor isolado, rmse workspace, razao ws/isolado).
    Quando a tarefa precisa das DUAS caracteristicas (a,b != 0), o isolado tem erro irredutivel (~|b|/sqrt3 para x2~U(-1,1)) e o
    workspace recupera o exato; quando uma basta (b=0), empatam."""
    X1, X2, Y = gerar_mundo(semente, n, a, b)
    _, r_a = especialista_isolado(X1, Y)
    _, r_b = especialista_isolado(X2, Y)
    melhor_iso = min(r_a, r_b)
    _, r_ws, _ = workspace_global(X1, X2, Y)
    return melhor_iso, r_ws, (r_ws / melhor_iso if melhor_iso else 0.0)
