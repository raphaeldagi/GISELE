"""Compressão, GRPO e perda de plasticidade (Parte 87), biblioteca padrão. Reimplementa as peças testáveis do relatório recebido: o operador de quantização
uniforme, a vantagem normalizada do GRPO, e uma MLP de uma camada oculta treinada numa sequência de tarefas para medir a perda de plasticidade (posto
estável das ativações, neurônios dormentes, norma dos pesos) com e sem Shrink&Perturb."""

import math
import random


def quantizar(x, bits, lo, hi):
    """Quantizacao uniforme: s = (hi-lo)/(2^bits - 1); q = round((x-lo)/s); devolve o valor de-quantizado lo + q*s (saturado)."""
    niveis = (1 << bits) - 1
    s = (hi - lo) / niveis
    q = round((x - lo) / s)
    q = max(0, min(niveis, q))
    return lo + q * s


def mse_quantizacao(bits, amostras, lo=-4.0, hi=4.0):
    return sum((x - quantizar(x, bits, lo, hi)) ** 2 for x in amostras) / len(amostras)


def vantagem_grpo(recompensas, eps=1e-8):
    """A vantagem normalizada do GRPO: (r_i - media)/(desvio populacional + eps)."""
    g = len(recompensas)
    media = sum(recompensas) / g
    var = sum((r - media) ** 2 for r in recompensas) / g
    desvio = math.sqrt(var)
    return [(r - media) / (desvio + eps) for r in recompensas]


def _relu(x):
    return x if x > 0 else 0.0


def posto_estavel(colunas):
    """Posto estavel ||A||_F^2 / ||A||_2^2 de uma matriz dada como lista de linhas (amostras x unidades). ||A||_2^2 = maior autovalor de A^T A por iteracao
    de potencia. Proxy do posto efetivo, so com +,-,*,/ e sqrt."""
    n_lin = len(colunas)
    d = len(colunas[0])
    # A^T A (d x d)
    gram = [[sum(colunas[r][i] * colunas[r][j] for r in range(n_lin)) for j in range(d)] for i in range(d)]
    fro2 = sum(gram[i][i] for i in range(d))  # ||A||_F^2 = traco(A^T A)
    if fro2 <= 1e-18:
        return 0.0
    # maior autovalor de gram por iteracao de potencia
    v = [1.0] * d
    for _ in range(100):
        w = [sum(gram[i][j] * v[j] for j in range(d)) for i in range(d)]
        n = math.sqrt(sum(a * a for a in w))
        if n < 1e-18:
            return 0.0
        v = [a / n for a in w]
    Av = [sum(gram[i][j] * v[j] for j in range(d)) for i in range(d)]
    lam = sum(v[i] * Av[i] for i in range(d))
    return fro2 / lam if lam > 1e-18 else 0.0


def treinar_continuo(tarefas=20, d_in=10, d_oculta=20, amostras=40, passos=50, taxa=0.1,
                     shrink_perturb=False, sp_shrink=0.9, sp_ruido=0.01, semente=87, conflito=False):
    """Uma MLP de 1 camada oculta (ReLU) + saida linear, treinada por SGD numa sequencia de tarefas de classificacao binaria aleatorias. Mede, na tarefa 1 e
    na ultima: posto estavel das ativacoes ocultas, fracao de unidades dormentes (ReLU sempre zero na amostra), e norma de W1. Com shrink_perturb, aplica
    W <- sp_shrink*W + ruido no inicio de cada tarefa (a regra do relatorio). Devolve {posto1, postoN, dorm1, dormN, norma1, normaN}."""
    rng = random.Random(semente)
    W1 = [[rng.gauss(0, 1.0 / math.sqrt(d_in)) for _ in range(d_in)] for _ in range(d_oculta)]
    W2 = [rng.gauss(0, 1.0 / math.sqrt(d_oculta)) for _ in range(d_oculta)]
    medidas = {}

    def ativacoes(X):
        return [[_relu(sum(W1[h][k] * x[k] for k in range(d_in))) for h in range(d_oculta)] for x in X]

    def medir(X, rotulo):
        H = ativacoes(X)
        posto = posto_estavel(H)
        dorm = sum(1 for h in range(d_oculta) if all(H[r][h] <= 1e-12 for r in range(len(X)))) / d_oculta
        norma = math.sqrt(sum(W1[h][k] ** 2 for h in range(d_oculta) for k in range(d_in)))
        medidas[rotulo + "posto"] = posto
        medidas[rotulo + "dorm"] = dorm
        medidas[rotulo + "norma"] = norma

    for t in range(tarefas):
        if shrink_perturb and t > 0:
            for h in range(d_oculta):
                for k in range(d_in):
                    W1[h][k] = sp_shrink * W1[h][k] + rng.gauss(0, sp_ruido)
                W2[h] = sp_shrink * W2[h] + rng.gauss(0, sp_ruido)
        # tarefa t: professor aleatorio (independente) ou, com conflito, professor fixo com rotulos invertidos a cada tarefa
        if conflito:
            if t == 0:
                treinar_continuo._wstar = [rng.gauss(0, 1) for _ in range(d_in)]
            wstar = treinar_continuo._wstar
            flip = (t % 2 == 1)
        else:
            wstar = [rng.gauss(0, 1) for _ in range(d_in)]
            flip = False
        X = [[rng.gauss(0, 1) for _ in range(d_in)] for _ in range(amostras)]
        y = [(0.0 if flip else 1.0) if sum(wstar[k] * x[k] for k in range(d_in)) > 0 else (1.0 if flip else 0.0) for x in X]
        if t == 0:
            medir(X, "ini_")
        for _ in range(passos):
            for xi, yi in zip(X, y):
                h = [_relu(sum(W1[hh][k] * xi[k] for k in range(d_in))) for hh in range(d_oculta)]
                pred = sum(W2[hh] * h[hh] for hh in range(d_oculta))
                err = pred - yi
                for hh in range(d_oculta):
                    if h[hh] > 0:
                        for k in range(d_in):
                            W1[hh][k] -= taxa * err * W2[hh] * xi[k]
                    W2[hh] -= taxa * err * h[hh]
        if t == tarefas - 1:
            medir(X, "fim_")
    return medidas


# ---- Parte 89: o substrato pulsado que aprende (STDP com competicao sinaptica) ----

def stdp_integral(a_mais=0.1, a_menos=0.12, tau_mais=20.0, tau_menos=20.0):
    """A integral da janela STDP: A+*tau+ - A-*tau- (a deriva esperada por par pre-pos, em taxas independentes). Forma fechada (Kempter/Gerstner/van Hemmen 1999)."""
    return a_mais * tau_mais - a_menos * tau_menos


def competicao_sinaptica(n_corr=10, n_ruido=40, ms=5000, dt=1.0, taxa_hz=20.0, w0=0.5, wmax=1.0,
                         a_mais=0.008, a_menos=0.0088, tau=20.0, limiar=1.0, tau_m=20.0, semente=89):
    """Um neuronio LIF com n_corr sinapses CORRELACIONADAS (disparam junto com um sinal comum) e n_ruido sinapses INDEPENDENTES (Poisson), com STDP de pares e
    limites [0, wmax], depressao dominante (A-*tau- > A+*tau+). Resultado classico (Song-Miller-Abbott 2000): as correlacionadas vencem, as independentes decaem.
    Devolve (peso medio final correlacionadas, peso medio final independentes). So biblioteca padrao."""
    import math
    import random
    rng = random.Random(semente)
    n = n_corr + n_ruido
    w = [w0] * n
    u = 0.0
    beta = math.exp(-dt / tau_m)
    p = taxa_hz * dt / 1000.0  # prob. de disparo por passo
    ult_pre = [-1e9] * n       # ultimo disparo pre de cada sinapse
    ult_pos = -1e9             # ultimo disparo pos
    passos = int(ms / dt)
    for k in range(passos):
        t = k * dt
        sinal = rng.random() < p   # o sinal comum das correlacionadas
        pre = []
        for i in range(n):
            if i < n_corr:
                disparou = sinal  # correlacionadas seguem o sinal comum
            else:
                disparou = rng.random() < p
            if disparou:
                pre.append(i)
                ult_pre[i] = t
        # integra as entradas ponderadas
        entrada = sum(w[i] for i in pre)
        u = beta * u + entrada
        # STDP pre->pos (depressao: pre chega, olha o ultimo pos; se pos foi antes, Dt<0 deprime)
        for i in pre:
            dt_pp = ult_pos - t  # <= 0
            if ult_pos > -1e8:
                w[i] = max(0.0, w[i] - a_menos * math.exp(dt_pp / tau))
        disparo_pos = u >= limiar
        if disparo_pos:
            ult_pos = t
            u = 0.0
            # STDP pos (potenciacao: para cada pre recente, Dt = t - ult_pre > 0 potencia)
            for i in range(n):
                d = t - ult_pre[i]
                if 0 <= d < 5 * tau:
                    w[i] = min(wmax, w[i] + a_mais * math.exp(-d / tau))
    mc = sum(w[:n_corr]) / n_corr
    mr = sum(w[n_corr:]) / n_ruido
    return mc, mr


def stdp_timing_controlado(dt_par=5.0, pares=200, w0=0.5, a_mais=0.01, a_menos=0.011, tau=20.0):
    """A propriedade definidora da STDP (robusta, independente de regime): uma sinapse cujo pre precede o pos (dt=+dt_par) POTENCIA; cujo pre segue o pos
    (dt=-dt_par) DEPRIME. Aplica `pares` pares com cada temporizacao e devolve (peso final 'pre antes', peso final 'pre depois'). Confere o sinal da janela."""
    from synthai.pulsado import stdp_delta
    w_antes = w0
    w_depois = w0
    for _ in range(pares):
        w_antes += stdp_delta(dt_par, a_mais, a_menos, tau, tau)    # dt>0: potencia
        w_depois += stdp_delta(-dt_par, a_mais, a_menos, tau, tau)  # dt<0: deprime
    return w_antes, w_depois


def stdp_deriva_taxas(r_pre=20.0, r_pos=20.0, ms=20000, dt=1.0, a_mais=0.1, a_menos=0.12, tau=20.0, semente=89):
    """A deriva de um peso sob pre e pos de Poisson INDEPENDENTES, a taxas r_pre e r_pos (Hz). A conta (Kempter et al.): a deriva por par e proporcional a
    A+*tau+ - A-*tau-, entao negativa quando a depressao domina. Devolve (soma de Delta w simulada, sinal da integral). So biblioteca padrao."""
    import math
    import random
    rng = random.Random(semente)
    p_pre = r_pre * dt / 1000.0
    p_pos = r_pos * dt / 1000.0
    pre_spikes = []
    pos_spikes = []
    passos = int(ms / dt)
    for k in range(passos):
        t = k * dt
        if rng.random() < p_pre:
            pre_spikes.append(t)
        if rng.random() < p_pos:
            pos_spikes.append(t)
    # soma dos Delta w de todos os pares dentro de +-5 tau
    total = 0.0
    j0 = 0
    for tpos in pos_spikes:
        for tpre in pre_spikes:
            d = tpos - tpre  # dt = t_pos - t_pre; d>0 => pre antes => potencia
            if abs(d) < 5 * tau:
                total += a_mais * math.exp(-d / tau) if d > 0 else -a_menos * math.exp(d / tau)
    integral = a_mais * tau - a_menos * tau
    return total, (1 if integral > 0 else -1 if integral < 0 else 0)
