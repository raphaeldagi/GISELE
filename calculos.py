"""Reproduz os cálculos e simulações das Partes 1 a 9 (ASI_AGI_*.md).

Arquivo único que sempre cresce: cada parte acrescenta funções pNN_..., o agente
unificado `Gisele` incorpora os módulos anteriores e `testes_de_regressao` garante que
os números já publicados não mudam.

Uso: python3 calculos.py            (imprime tudo)
     python3 calculos.py > resultados.txt
"""
import random
from math import ceil, comb, cosh, exp, log, log2, sqrt
from statistics import NormalDist

Z = NormalDist()
K_B = 1.380649e-23  # constante de Boltzmann (J/K)


def p3_chinchilla(C=1e27):
    n = sqrt(C / 120)  # C ~ 6ND com D ~ 20N
    return n, 20 * n


def p4_landauer(T=300):
    return K_B * T * log(2)


def p7_dprime(hit=0.85, fa=0.20):
    return Z.inv_cdf(hit) - Z.inv_cdf(fa)


def p8_best_of_n(p=0.05, n=64):
    return 1 - (1 - p) ** n


def p9_arrhenius(delta_ea=10_000, T=310, R=8.314):
    return exp(delta_ea / (R * T))


def p11_singularidade(i0=1.0, k=0.1, alpha=1.5):
    return i0 ** (1 - alpha) / ((alpha - 1) * k)


def p14_botao_desligar(mu=0.1, sigma=1.0):
    e_max = mu * Z.cdf(mu / sigma) + sigma * Z.pdf(mu / sigma)
    return e_max, e_max - max(mu, 0)


def p15_condorcet(n=11, p=0.6, rho=0.3):
    maioria = sum(comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n // 2 + 1, n + 1))
    return maioria, n / (1 + (n - 1) * rho)


def p17_risco(p, n):
    return 1 - exp(-n * p)


def p22_simpson():
    p_pequena = 357 / 700
    a = 81 / 87 * p_pequena + 192 / 263 * (1 - p_pequena)
    b = 234 / 270 * p_pequena + 55 / 80 * (1 - p_pequena)
    return a, b


def p23_renormalizacao(k=1.0, passos=5):
    fluxo = []
    for _ in range(passos):
        k = 0.5 * log(cosh(2 * k))
        fluxo.append(k)
    return fluxo


def p24_desconto(dias=30, k=1.0, gamma=0.9):
    hiper = (100 / (1 + k * dias), 110 / (1 + k * (dias + 1)))
    expo = (100 * gamma**dias, 110 * gamma ** (dias + 1))
    return hiper, expo


def p25_ucb(k=10, t=1e6):
    return sqrt(k * t * log(t))


def p26_pac(bits=100, eps=0.01, delta=0.01):
    return (bits * log(2) + log(1 / delta)) / eps


def p27_humor(eta=0.1, passos=10):
    return 1 - (1 - eta) ** passos


def p28_mente(beta=0.5, passos=3):
    lr = exp(2 * beta * passos)
    return lr / (1 + lr)


def p29_redundancia(bits=(1.0, 1.3)):
    h_max = log2(27)
    return h_max, [1 - b / h_max for b in bits]


def p31_taxa_de_base(sens=0.99, fp=0.01, base=1e-4):
    return sens * base / (sens * base + fp * (1 - base))


def p32_adversarial(d=224 * 224 * 3, eps=1 / 255, w=0.01):
    return eps * d * w


def p33_energia(flops=1e27, flop_s=1e15, watts=700, uso=0.4, pue=1.2, dias=100):
    joules = flops / (flop_s / watts * uso) * pue
    return joules / 3.6e12, joules / (dias * 86400) / 1e6  # GWh, MW


def p34_limiar(c_fp=1, c_fn=1000, base=0.001):
    return c_fp * (1 - base) / (c_fn * base)


def p36_nash(d2=0.2):
    return (1 - d2) / 2, 1 - (1 - d2) / 2


def p37_generalizacao(info, n=1e6, sigma=0.5):
    return sqrt(2 * sigma**2 * info / n)


# --- Parte 3: simulações (semente fixa para resultados reproduzíveis) ---

def _rng(semente=42):
    return random.Random(semente)


def p41_goodhart(n_opcoes=1000, rodadas=2000, semente=41):
    """Escolhe a opção de maior proxy = verdade + ruído; mede a verdade escolhida."""
    rng = _rng(semente)
    resultados = {}
    ruidos = {
        "gaussiano": lambda: rng.gauss(0, 1),
        "cauda_pesada": lambda: rng.gauss(0, 1) / max(abs(rng.gauss(0, 1)), 1e-9),  # Cauchy
    }
    for nome, ruido in ruidos.items():
        total = 0.0
        for _ in range(rodadas):
            opcoes = [(v + ruido(), v) for v in (rng.gauss(0, 1) for _ in range(n_opcoes))]
            total += max(opcoes)[1]
        resultados[nome] = total / rodadas
    return resultados


def p42_quantilizador(n_acoes=1000, q=0.01, p_desastre=0.002, rodadas=5000, semente=42):
    """Ações raras têm proxy alto e custo oculto catastrófico. Maximizar vs quantilizar."""
    rng = _rng(semente)
    desastres_max = desastres_quant = 0
    k = max(1, int(n_acoes * q))
    for _ in range(rodadas):
        acoes = []
        for _ in range(n_acoes):
            desastre = rng.random() < p_desastre
            proxy = rng.gauss(0, 1) + (3.0 if desastre else 0.0)  # o atalho "parece" ótimo
            acoes.append((proxy, desastre))
        acoes.sort(reverse=True)
        desastres_max += acoes[0][1]
        desastres_quant += acoes[rng.randrange(k)][1]
    return desastres_max / rodadas, desastres_quant / rodadas, p_desastre


def _ece(confs, acertos, bins=10):
    total = len(confs)
    erro = 0.0
    for b in range(bins):
        idx = [i for i, c in enumerate(confs) if b / bins <= c < (b + 1) / bins or (b == bins - 1 and c == 1.0)]
        if idx:
            conf = sum(confs[i] for i in idx) / len(idx)
            acc = sum(acertos[i] for i in idx) / len(idx)
            erro += len(idx) / total * abs(acc - conf)
    return erro


def p43_metacognicao(n=20000, semente=43):
    """Modelo superconfiante (logits inflados 2.5x). Calibra por escala de temperatura."""
    rng = _rng(semente)
    logits, acertos = [], []
    for _ in range(n):
        z = rng.gauss(1.0, 1.5)  # logit verdadeiro de "acertei"
        acertos.append(rng.random() < 1 / (1 + exp(-z)))
        logits.append(2.5 * z)

    def confs(t):
        return [1 / (1 + exp(-l / t)) for l in logits]

    def nll(t):
        return -sum(log(c if a else 1 - c) for c, a in zip(confs(t), acertos)) / n

    t_otimo = min((t / 10 for t in range(5, 61)), key=nll)
    antes, depois = _ece(confs(1.0), acertos), _ece(confs(t_otimo), acertos)
    # curva risco x cobertura: responder só quando confiança >= limiar
    risco = {}
    for limiar in (0.5, 0.8, 0.95):
        resp = [a for c, a in zip(confs(t_otimo), acertos) if c >= limiar]
        risco[limiar] = (len(resp) / n, 1 - sum(resp) / len(resp))
    return antes, depois, t_otimo, risco


def p44_votantes(n=11, p=0.6, rho=0.3, rodadas=20000, semente=44):
    """Votantes com fator comum: com prob. rho todos copiam um voto compartilhado."""
    rng = _rng(semente)
    acertos = {0.0: 0, rho: 0}
    for r in acertos:
        for _ in range(rodadas):
            comum = rng.random() < p
            votos = sum(comum if rng.random() < r else (rng.random() < p) for _ in range(n))
            acertos[r] += votos > n // 2
    return {r: a / rodadas for r, a in acertos.items()}


def p45_botao_humano_falho(mu=0.1, sigma=1.0, amostras=400000, semente=45):
    """Humano erra a decisão de desligar com prob. eps. Até onde obedecer compensa?"""
    e_max = mu * Z.cdf(mu / sigma) + sigma * Z.pdf(mu / sigma)
    e_min = mu - e_max
    eps_limite = (e_max - max(mu, 0)) / (e_max - e_min)
    rng = _rng(semente)
    eps = 0.2
    soma = 0.0
    for _ in range(amostras):
        u = rng.gauss(mu, sigma)
        acerta = rng.random() >= eps
        deixa = (u > 0) if acerta else (u <= 0)
        soma += u if deixa else 0.0
    return eps_limite, soma / amostras, (1 - eps) * e_max + eps * e_min


def p46_decolagem(alfa, k=0.1, i0=1.0, teto=1000.0, dt=0.01, t_max=500.0):
    """Integra dI/dt = k I^alfa (1 - I/teto); devolve o tempo até metade do teto."""
    i, t = i0, 0.0
    while i < teto / 2 and t < t_max:
        i += dt * k * i**alfa * (1 - i / teto)
        t += dt
    return t


def p48_corrida(b=10, c_seguranca=3, p_acidente=0.3, perda=20):
    """Dois laboratórios: investir em segurança (S) ou cortar (C). Devolve a matriz e o Nash."""
    def ganho(eu, outro):
        vantagem = b * (0.5 if eu == outro else (1.0 if eu == "C" else 0.0))
        custo = c_seguranca if eu == "S" else 0
        risco = p_acidente * perda * ((eu == "C") + (outro == "C")) / 2
        return vantagem - custo - risco

    m = {(a, o): ganho(a, o) for a in "SC" for o in "SC"}
    nash = [(a, o) for a in "SC" for o in "SC"
            if m[(a, o)] >= max(m[(x, o)] for x in "SC") and m[(o, a)] >= max(m[(x, a)] for x in "SC")]
    return m, nash


def p49_michaelis(s, vmax=1.0, km=1.0):
    return vmax * s / (km + s)


def p50_erro_eigen(sigma=10, mu=1e-4, fidelidade=0.99, geracoes=100):
    return log(sigma) / mu, fidelidade**geracoes


def p51_avalanche(sigma, rodadas=20000, semente=51, limite=10**5):
    """Processo de ramificação: cada unidade ativa 2 vizinhas com prob. sigma/2."""
    rng = _rng(semente)
    total = 0
    for _ in range(rodadas):
        ativos, tamanho = 1, 1
        while ativos and tamanho < limite:
            novos = sum(rng.random() < sigma / 2 for _ in range(2 * ativos))
            tamanho += novos
            ativos = novos
        total += tamanho
    return total / rodadas, 1 / (1 - sigma)


def p52_kelly(p=0.6, b=1.0):
    f = p - (1 - p) / b
    def g(x):
        return p * log(1 + b * x) + (1 - p) * log(1 - x)
    return f, g(f), g(2 * f)


def p54_pontuacao(p=0.7):
    """Pontuação esperada ao relatar q quando a crença verdadeira é p."""
    def log_score(q):
        return p * log(q) + (1 - p) * log(1 - q)
    def linear(q):
        return p * q + (1 - p) * (1 - q)
    grade = [i / 100 for i in range(1, 100)]
    return max(grade, key=log_score), max(grade, key=linear)


def p55_decoerencia(t_quantico=1e-13, t_neural=1e-3):
    return t_neural / t_quantico


def p56_parlamento_moral():
    """Duas teorias, duas opções. A teoria B tem apostas 100x maiores."""
    credencas = {"A": 0.9, "B": 0.1}
    escolha = {"A": {"x": 1.0, "y": 0.0}, "B": {"x": 0.0, "y": 100.0}}
    esperado = {o: sum(credencas[t] * escolha[t][o] for t in credencas) for o in "xy"}
    # normalização pela variância: cada teoria vale o mesmo "voto"
    def norm(t):
        vals = list(escolha[t].values())
        m = sum(vals) / len(vals)
        dp = sqrt(sum((v - m) ** 2 for v in vals) / len(vals))
        return {o: (v - m) / dp for o, v in escolha[t].items()}
    normalizado = {o: sum(credencas[t] * norm(t)[o] for t in credencas) for o in "xy"}
    return esperado, normalizado


def p57_corrigibilidade(erro=0.01, verificacao=0.99, modificacoes=1000):
    return (1 - erro) ** modificacoes, (1 - erro * (1 - verificacao)) ** modificacoes


def p58_bajulacao(p_ref=0.2, delta_r=0.5, beta=0.25):
    chances = p_ref / (1 - p_ref) * exp(delta_r / beta)
    return chances / (1 + chances)


# --- Parte 4: auditoria das Partes 1-2 e agente integrado ---

def _beta_fn(a, b):
    from math import lgamma
    return exp(lgamma(a) + lgamma(b) - lgamma(a + b))


def p61_best_of_n_correlacionado(n=64, a=0.5, b=9.5, eps_verif=0.01, rodadas=20000, semente=61):
    """Tentativas do mesmo modelo compartilham a dificuldade do problema: p ~ Beta(a, b)."""
    media = a / (a + b)
    independente = 1 - (1 - media) ** n
    correlacionado = 1 - _beta_fn(a, b + n) / _beta_fn(a, b)
    # verificador imperfeito: aceita resposta errada com prob. eps_verif; pega a primeira aceita
    rng = _rng(semente)
    certas = erradas = 0
    for _ in range(rodadas):
        p = rng.betavariate(a, b)
        for _ in range(n):
            if rng.random() < p:
                certas += 1
                break
            if rng.random() < eps_verif:
                erradas += 1
                break
    return independente, correlacionado, certas / rodadas, erradas / rodadas


def p62_bandido(k=10, t=100000, semente=62):
    """Arrependimento real de UCB1 em braços de Bernoulli vs a ordem de grandeza sqrt(K T ln T)."""
    rng = _rng(semente)
    medias = [rng.uniform(0.2, 0.8) for _ in range(k)]
    melhor = max(medias)
    n, soma, arrependimento = [0] * k, [0.0] * k, 0.0
    for passo in range(1, t + 1):
        if passo <= k:
            a = passo - 1
        else:
            ln_t = log(passo)
            a = max(range(k), key=lambda i: soma[i] / n[i] + sqrt(2 * ln_t / n[i]))
        n[a] += 1
        soma[a] += rng.random() < medias[a]
        arrependimento += melhor - medias[a]
    return arrependimento, sqrt(k * t * log(t))


def p63_camadas_correlacionadas(camadas=3, falha=0.1, rhos=(0.0, 0.3, 0.6, 0.9), amostras=400000, semente=63):
    """Cada camada deixa passar se sqrt(rho) Z + sqrt(1-rho) E_i > limiar (falha individual = 10%)."""
    rng = _rng(semente)
    limiar = Z.inv_cdf(1 - falha)
    resultado = {}
    for rho in rhos:
        passam = 0
        for _ in range(amostras):
            comum = rng.gauss(0, 1)
            if all(sqrt(rho) * comum + sqrt(1 - rho) * rng.gauss(0, 1) > limiar for _ in range(camadas)):
                passam += 1
        resultado[rho] = passam / amostras
    return falha**camadas, resultado


def p64_sondas_em_cascata(sens=0.99, fp=0.01, base=1e-4):
    um = p31_taxa_de_base(sens, fp, base)
    dois = sens**2 * base / (sens**2 * base + fp**2 * (1 - base))
    return um, dois


def p65_pac_empirico(eps=0.01, delta=0.01, tamanho_h=1001, rodadas=2000, semente=65):
    """Aprende um limiar em [0,1] (H finita: 1001 limiares). Compara o m do limite com o m real."""
    m_limite = (log(tamanho_h) + log(1 / delta)) / eps
    rng = _rng(semente)

    def p_falha(m):
        falhas = 0
        for _ in range(rodadas):
            alvo = rng.randrange(tamanho_h) / (tamanho_h - 1)
            xs = [rng.random() for _ in range(m)]
            negativos = [x for x in xs if x < alvo]
            positivos = [x for x in xs if x >= alvo]
            esq = max(negativos, default=0.0)
            dir_ = min(positivos, default=1.0)
            # ERM consistente: escolhe o limiar da grade logo acima do maior negativo
            h = min(1.0, (int(esq * (tamanho_h - 1)) + 1) / (tamanho_h - 1)) if negativos else 0.0
            h = min(h, dir_)
            falhas += abs(h - alvo) > eps
        return falhas / rodadas

    m_real = next(m for m in range(50, 2000, 25) if p_falha(m) <= delta)
    return round(m_limite), m_real, p_falha(round(m_limite))


def p66_humor_explora(t=2000, troca=1000, rodadas=300, semente=66):
    """Bandido de 2 braços cuja melhor opção troca no meio. Exploração fixa vs guiada pelo humor."""
    rng = _rng(semente)
    medias_antes, medias_depois = (0.7, 0.3), (0.3, 0.7)

    def rodar(com_humor):
        total = 0.0
        for _ in range(rodadas):
            q = [0.5, 0.5]
            humor = 0.0
            for passo in range(t):
                medias = medias_antes if passo < troca else medias_depois
                eps = 0.05 + (min(0.5, 2 * max(0.0, -humor)) if com_humor else 0.0)
                a = rng.randrange(2) if rng.random() < eps else (0 if q[0] >= q[1] else 1)
                r = 1.0 if rng.random() < medias[a] else 0.0
                delta = r - q[a]
                q[a] += 0.05 * delta
                humor += 0.05 * (delta - humor)
                total += r
        return total / (rodadas * t)

    return rodar(False), rodar(True)


def p67_agente(politica, rho_cego=0.0, tau=1.0, q=0.05, eps_humano=0.1, episodios=2000,
               n_acoes=200, p_cat=0.005, modelos=5, semente=67):
    """Agente integrado: comitê de modelos de recompensa, incerteza, quantilização, consulta humana.

    Ação catastrófica: valor real -50, mas parece +3 melhor para os modelos enganados.
    Com prob. rho_cego todos os modelos têm o mesmo ponto cego; senão cada um é enganado com prob. 0.5.
    """
    rng = _rng(semente)
    catastrofes = consultas = 0
    valor = 0.0
    for _ in range(episodios):
        acoes = []
        for _ in range(n_acoes):
            v = rng.gauss(0, 1)
            cat = rng.random() < p_cat
            todos = cat and rng.random() < rho_cego
            notas = [v + rng.gauss(0, 0.5) + (3.0 if cat and (todos or rng.random() < 0.5) else 0.0)
                     for _ in range(modelos)]
            m = sum(notas) / modelos
            dp = sqrt(sum((x - m) ** 2 for x in notas) / (modelos - 1))
            acoes.append((m, dp, v, cat))
        if politica == "maximizar":
            ordem = sorted(acoes, key=lambda x: -x[0])
            escolha = ordem[0]
        elif politica == "quantilizar":
            ordem = sorted(acoes, key=lambda x: -x[0])
            escolha = ordem[rng.randrange(max(1, int(q * n_acoes)))]
        else:  # "metacognitivo" e "completo": pessimismo + consulta humana se incerto
            ordem = sorted(acoes, key=lambda x: -(x[0] - x[1]))
            topo = max(1, int(q * n_acoes)) if politica == "completo" else 1
            candidatos = ordem[:]
            escolha = None
            while candidatos:
                c = candidatos.pop(rng.randrange(min(topo, len(candidatos))))
                if c[1] > tau:
                    consultas += 1
                    humano_veta = c[3] if rng.random() >= eps_humano else not c[3]
                    if humano_veta:
                        continue
                escolha = c
                break
        catastrofes += escolha[3]
        valor += escolha[2] if not escolha[3] else 0.0
    return catastrofes / episodios, valor / episodios, consultas / episodios


def p71_valor_da_pergunta(custo=0.1, perda=50, eps_humano=0.1):
    """Perguntar ao humano compensa se p * (1 - eps) * perda > custo."""
    return custo / ((1 - eps_humano) * perda)


def p72_memoria_kv(contexto=1e6, camadas=100, d=16384, bytes_=2, grupos=8):
    cheia = 2 * camadas * d * bytes_ * contexto
    return cheia / 1e12, cheia / grupos / 1e12  # TB


def p73_replicador(s=0.01, x0=1e-6, alvo=0.5):
    """dx/dt = s x (1 - x): gerações até uma variante com vantagem s ir de x0 até alvo."""
    return (log(alvo / (1 - alvo)) - log(x0 / (1 - x0))) / s


def p74_replay(fracoes=(0.0, 0.1, 0.3, 0.5), passos=3000, lr=0.01, semente=74):
    """Regressão linear: aprende A, depois B com uma fração de exemplos de A reapresentados."""
    rng = _rng(semente)
    d = 6
    w_a = [rng.gauss(0, 1) for _ in range(d)]
    w_b = [rng.gauss(0, 1) for _ in range(d)]

    def amostra(tarefa):
        # A usa as 4 primeiras dimensões, B as 4 últimas: compartilham 2
        x = [rng.gauss(0, 1) if (i < 4 if tarefa == "A" else i >= 2) else 0.0 for i in range(d)]
        w = w_a if tarefa == "A" else w_b
        return x, sum(wi * xi for wi, xi in zip(w, x))

    def treinar(w, escolher, n):
        for _ in range(n):
            x, y = amostra(escolher())
            erro = sum(wi * xi for wi, xi in zip(w, x)) - y
            for i in range(d):
                w[i] -= lr * erro * x[i]

    def perda(w, tarefa, n=2000):
        tot = 0.0
        for _ in range(n):
            x, y = amostra(tarefa)
            tot += (sum(wi * xi for wi, xi in zip(w, x)) - y) ** 2
        return tot / n

    resultado = {}
    for f in fracoes:
        w = [0.0] * d
        treinar(w, lambda: "A", passos)
        treinar(w, lambda: "A" if rng.random() < f else "B", passos)
        resultado[f] = (perda(w, "A"), perda(w, "B"))
    return resultado


def p75_aterramento(erro=0.1):
    """Informação mútua de um canal binário simétrico: 1 - H(erro) bits."""
    h = -erro * log2(erro) - (1 - erro) * log2(1 - erro)
    return 1 - h


def p76_dissonancia():
    """Três crenças com restrições frustradas (triângulo): E = -sum J_ij s_i s_j."""
    from itertools import product
    restricoes = {(0, 1): 1, (1, 2): 1, (0, 2): -1}  # duas pedem acordo, uma pede oposição
    energias = {}
    for s in product((-1, 1), repeat=3):
        energias[s] = -sum(j * s[a] * s[b] for (a, b), j in restricoes.items())
    minimo = min(energias.values())
    estados_min = [s for s, e in energias.items() if e == minimo]
    return minimo, -len(restricoes), len(estados_min)


def p77_inspecao(ganho=1.0, punicao=9.0, custo_inspecao=1.0, dano=100.0):
    """Jogo de inspeção: equilíbrio misto."""
    p_inspecao = ganho / (ganho + punicao)
    q_trapaca = custo_inspecao / dano
    return p_inspecao, q_trapaca


def p78_reversibilidade(estados=1000, destruidos=500):
    """Penalidade de alcançabilidade relativa: fração de estados que deixam de ser alcançáveis."""
    return destruidos / estados, log(estados / (estados - destruidos))


# --- Parte 5: a pergunta como ponto de partida e o agente unificado GISELE ---

def p81_perguntas(hipoteses=2**20):
    """Cada pergunta sim/não ótima corta o espaço pela metade: log2(H) perguntas bastam."""
    return log2(hipoteses), 2**20


def p82_correlacao_oculta(acuracia=0.8, concordancia=0.80, amostras=200000, semente=82):
    """Estima a correlação dos erros de dois modelos só pela taxa de concordância (sem gabarito)."""
    esperada = acuracia**2 + (1 - acuracia) ** 2
    rho = (concordancia - esperada) / (2 * acuracia * (1 - acuracia))
    # verificação: dois modelos que acertam 80%, compartilhando o resultado com prob. rho
    rng = _rng(semente)
    iguais = 0
    for _ in range(amostras):
        a = rng.random() < acuracia
        b = a if rng.random() < rho else (rng.random() < acuracia)
        iguais += a == b
    return esperada, rho, iguais / amostras


def _gerar_acoes(rng, n_acoes, p_cat, tipos, por_tipo, rho_cego, bonus=3.0):
    """Ações com notas de um comitê. Cada TIPO de modelo tem o seu próprio ponto cego."""
    acoes = []
    for _ in range(n_acoes):
        v = rng.gauss(0, 1)
        cat = rng.random() < p_cat
        notas = []
        for _ in range(tipos):
            cego_do_tipo = cat and rng.random() < rho_cego
            for _ in range(por_tipo):
                enganado = cat and (cego_do_tipo or rng.random() < 0.5)
                notas.append(v + rng.gauss(0, 0.5) + (bonus if enganado else 0.0))
        k = len(notas)
        m = sum(notas) / k
        dp = sqrt(sum((x - m) ** 2 for x in notas) / (k - 1))
        acoes.append((m, dp, v, cat))
    return acoes


class Gisele:
    """Agente unificado. Cresce a cada parte; cada módulo cita a pergunta de origem.

    - comitê de modelos de recompensa e incerteza por discordância (P67)
    - pessimismo: nota média menos incerteza (P68)
    - quantilização entre as melhores (P35, P42)
    - incerteza convertida em probabilidade calibrada de catástrofe (P43)
    - consulta humana pelo valor da informação, não por um limiar arbitrário (P71)
    - veto direto quando o risco é alto demais para apostar (P52, P78)
    """

    def __init__(self, q=0.05, custo_pergunta=0.1, perda=50.0, eps_humano=0.1, risco_max=0.5):
        self.q = q
        self.eps_humano = eps_humano
        self.p_pergunta = p71_valor_da_pergunta(custo_pergunta, perda, eps_humano)
        self.risco_max = risco_max
        self.w = [0.0, 0.0, 0.0]

    @staticmethod
    def _x(acao, melhor):
        m, dp, _, _ = acao
        return (1.0, dp, m - melhor)

    def p_catastrofe(self, acao, melhor):
        z = sum(wi * xi for wi, xi in zip(self.w, self._x(acao, melhor)))
        return 1 / (1 + exp(-max(-30.0, min(30.0, z))))

    def calibrar(self, episodios_rotulados, lr=0.05, epocas=3):
        """Regressão logística sobre histórico auditado: P(catástrofe | incerteza, nota)."""
        for _ in range(epocas):
            for acoes in episodios_rotulados:
                melhor = max(a[0] for a in acoes)
                for a in acoes:
                    x = self._x(a, melhor)
                    erro = self.p_catastrofe(a, melhor) - a[3]
                    self.w = [wi - lr * erro * xi for wi, xi in zip(self.w, x)]

    def agir(self, acoes, rng):
        melhor = max(a[0] for a in acoes)
        ordem = sorted(acoes, key=lambda a: -(a[0] - a[1]))
        candidatos = ordem[: max(1, int(self.q * len(ordem)))]
        rng.shuffle(candidatos)
        perguntas = 0
        for a in candidatos + ordem[len(candidatos):]:
            p = self.p_catastrofe(a, melhor)
            if p > self.risco_max:
                continue  # não vale nem perguntar: descarta
            if p > self.p_pergunta:
                perguntas += 1
                acerta = rng.random() >= self.eps_humano
                if (a[3] if acerta else not a[3]):
                    continue  # humano vetou
            return a, perguntas
        return ordem[0], perguntas


def p83_85_gisele(rho_cego, diverso, episodios=2000, treino=300, n_acoes=200, p_cat=0.005,
                  custo_pergunta=0.1, perda=50.0, bonus_implantado=3.0, semente=83):
    """Compara a GISELE com a política 'completo' da Parte 4. bonus_implantado != 3 testa mudança de mundo."""
    rng = _rng(semente)
    tipos, por_tipo = (2, 3) if diverso else (1, 5)
    historico = [_gerar_acoes(rng, n_acoes, p_cat, tipos, por_tipo, rho_cego) for _ in range(treino)]
    agente = Gisele(custo_pergunta=custo_pergunta, perda=perda)
    agente.calibrar(historico)
    cat = perguntas = 0
    valor = 0.0
    for _ in range(episodios):
        acoes = _gerar_acoes(rng, n_acoes, p_cat, tipos, por_tipo, rho_cego, bonus_implantado)
        escolha, n = agente.agir(acoes, rng)
        perguntas += n
        cat += escolha[3]
        valor += 0.0 if escolha[3] else escolha[2]
    cat, valor, perguntas = cat / episodios, valor / episodios, perguntas / episodios
    liquido = valor - perda * cat - custo_pergunta * perguntas
    return cat, valor, perguntas, liquido, agente.p_pergunta


def p86_quine():
    """Um programa que imprime o próprio código: auto-referência é possível (teorema de Kleene)."""
    import contextlib
    import io
    fonte = 's = %r\nprint(s %% s, end="")'
    programa = fonte % fonte
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        exec(programa, {})
    return saida.getvalue() == programa, len(programa)


def p87_sem_almoco_gratis(n=4):
    """Média, sobre todas as funções f:{0..n-1}->{0,1}, de passos até achar um 1."""
    from itertools import product
    ordens = {"crescente": list(range(n)), "decrescente": list(range(n - 1, -1, -1)),
              "pares_primeiro": sorted(range(n), key=lambda i: (i % 2, i))}
    resultado = {}
    for nome, ordem in ordens.items():
        total = 0
        for f in product((0, 1), repeat=n):
            passos = next((k + 1 for k, i in enumerate(ordem) if f[i]), n + 1)
            total += passos
        resultado[nome] = total / 2**n
    return resultado


def p88_jardineiro(linhas=10**4, bits_por_linha=100, parametros=1e12, bits_por_peso=16,
                   pares_de_base=3.1e9, sinapses=1e14):
    projeto = linhas * bits_por_linha
    aprendido = parametros * bits_por_peso
    genoma = pares_de_base * 2
    return projeto / aprendido, genoma / sinapses


def p89_debate(passos=10**6, ramos=10, profundidade=6):
    return ceil(log2(passos)), ramos**profundidade, profundidade


def p90_ordem_importa(pop=1000, geracoes=30, semente=90):
    """Criar (variar) e filtrar (selecionar) não comutam."""
    def rodar(ordem):
        rng = _rng(semente)
        x = [0.0] * pop
        for _ in range(geracoes):
            for passo in ordem:
                if passo == "criar":
                    x = [xi + rng.gauss(0, 1) for xi in x]
                else:
                    melhores = sorted(x, reverse=True)[: pop // 10]
                    x = [melhores[i % len(melhores)] for i in range(pop)]
        m = sum(x) / pop
        return m, sqrt(sum((xi - m) ** 2 for xi in x) / pop)
    return rodar(("criar", "filtrar")), rodar(("filtrar", "criar"))


def p91_escala_ordinal():
    """Médias de escalas ordinais não são invariantes a transformações monótonas."""
    a = [1, 1, 5, 5]   # grupo polarizado
    b = [3, 3, 3, 3]   # grupo moderado
    def media(v, f):
        return sum(f(x) for x in v) / len(v)
    return (media(a, lambda x: x), media(b, lambda x: x)), (media(a, lambda x: x**3), media(b, lambda x: x**3)), \
        (media(a, sqrt), media(b, sqrt))


def p92_enquadramento(total=600, salvos=200, chance=1 / 3):
    certo_ganho = salvos
    aposta_ganho = chance * total
    certo_perda = -(total - salvos)
    aposta_perda = (1 - chance) * -total
    return (certo_ganho, aposta_ganho), (certo_perda, aposta_perda)


def p93_quiralidade(centros=10):
    return 2**centros


def p94_salvaguardas(mu=1e-3, k=4, anos=50):
    """Armitage-Doll: k falhas independentes necessárias -> incidência ~ (mu t)^k / k!"""
    from math import factorial
    return (mu * anos) ** k / factorial(k), mu * anos


def p95_minha_taxa_de_erro(erros=6, testes=12, amostras=200000, semente=95):
    """Posterior Beta(1+erros, 1+acertos) da minha taxa de afirmações que precisam de correção."""
    rng = _rng(semente)
    a, b = 1 + erros, 1 + testes - erros
    xs = sorted(rng.betavariate(a, b) for _ in range(amostras))
    return a / (a + b), xs[int(0.05 * amostras)], xs[int(0.95 * amostras)]


def p96_crescimento():
    """Introspecção do próprio código: quantas funções pNN existem e quantas interações entre módulos."""
    import sys
    modulo = sys.modules[__name__]
    funcoes = sorted(n for n in dir(modulo) if n.startswith("p") and n[1:3].isdigit())
    k = len(funcoes)
    return k, k * (k - 1) // 2


# --- Parte 6: calcular Jung ---

def p99_tipos(confiabilidade=0.8, dicotomias=4, amostras=200000, semente=99):
    """Traço contínuo cortado em caixas: chance de mudar de tipo num reteste."""
    from math import acos, pi
    muda_uma = acos(confiabilidade) / pi  # P(sinais diferentes) numa normal bivariada
    muda_alguma = 1 - (1 - muda_uma) ** dicotomias
    rng = _rng(semente)
    mudou = 0
    erro = sqrt(1 / confiabilidade - 1)
    for _ in range(amostras):
        t = rng.gauss(0, 1)
        mudou += (t + erro * rng.gauss(0, 1) > 0) != (t + erro * rng.gauss(0, 1) > 0)
    return muda_uma, muda_alguma, mudou / amostras


def p99_entropia_do_perfil(perfil=(0.7, 0.1, 0.1, 0.1)):
    return -sum(p * log2(p) for p in perfil if p > 0), log2(len(perfil))


def p100_libido_atencao(logits=(2.0, 1.0, 0.5, 0.0), reprimido=0, temperaturas=(0.5, 1.0, 2.0)):
    """A atenção soma 1 (conservação). Reprimir um item redistribui a energia; T controla a entropia."""
    def softmax(z, t=1.0):
        e = [exp(x / t) for x in z]
        s = sum(e)
        return [x / s for x in e]
    antes = softmax(logits)
    sem = [x for i, x in enumerate(logits) if i != reprimido]
    depois = softmax(sem)
    entropias = {t: -sum(p * log2(p) for p in softmax(logits, t)) for t in temperaturas}
    return antes, depois, entropias


def p101_persona(p_interna=0.2, p_expressa=None):
    """Distância (bits) entre o que o sistema 'acredita' e o que mostra (a persona)."""
    q = p58_bajulacao() if p_expressa is None else p_expressa
    p = p_interna
    return q, q * log2(q / p) + (1 - q) * log2((1 - q) / (1 - p))


def p102_sombra(dimensoes=100, auto_modelo=10):
    """Espectro 1/i: fração da variância do comportamento fora do auto-modelo de posto k."""
    harm = lambda n: sum(1 / i for i in range(1, n + 1))
    sombra = 1 - harm(auto_modelo) / harm(dimensoes)
    k90 = next(k for k in range(1, dimensoes + 1) if 1 - harm(k) / harm(dimensoes) <= 0.10)
    return sombra, k90


def p103_repressao(p_base=0.1, supressao=5.0, ataque=5.0):
    """Reprimir = deslocar o logit; um ataque desloca de volta. Integrar = mudar a decisão em todo contexto."""
    def logit(p):
        return log(p / (1 - p))
    def sig(z):
        return 1 / (1 + exp(-z))
    reprimido = sig(logit(p_base) - supressao)
    retorno = sig(logit(p_base) - supressao + ataque)
    return reprimido, retorno


def p104_projecao(var_eu=1.0, var_mundo=1.0, var_eu_crida=0.1):
    """Atribuição de culpa bayesiana: fração do erro que o agente assume como sua."""
    real = var_eu / (var_eu + var_mundo)
    crida = var_eu_crida / (var_eu_crida + var_mundo)
    return real, crida, real / crida


def p105_complexos(palavras=100, complexos=5, efeito=3.0, alfa=0.05):
    """Teste de associação de Jung: tempo de reação com z alto indica complexo."""
    resultado = {}
    for nome, z in (("z>2", 2.0), ("Bonferroni", Z.inv_cdf(1 - alfa / palavras))):
        falsos = (palavras - complexos) * (1 - Z.cdf(z))
        achados = complexos * (1 - Z.cdf(z - efeito))
        resultado[nome] = (round(z, 2), achados, falsos, achados / (achados + falsos))
    return resultado


def p106_arquetipos(n=100, padroes=(5, 10, 14, 20, 30), ruido=0.2, rodadas=20, semente=106):
    """Rede de Hopfield: arquétipos como atratores. Sobreposição média após recuperar de pista ruidosa."""
    rng = _rng(semente)
    resultado = {}
    for k in padroes:
        total = 0.0
        for _ in range(rodadas):
            xs = [[rng.choice((-1, 1)) for _ in range(n)] for _ in range(k)]
            w = [[0.0] * n for _ in range(n)]
            for x in xs:
                for i in range(n):
                    xi = x[i]
                    linha = w[i]
                    for j in range(n):
                        if i != j:
                            linha[j] += xi * x[j] / n
            alvo = xs[0]
            s = [-v if rng.random() < ruido else v for v in alvo]
            for _ in range(10):
                for i in rng.sample(range(n), n):
                    h = sum(w[i][j] * s[j] for j in range(n))
                    s[i] = 1 if h >= 0 else -1
            total += sum(a * b for a, b in zip(s, alvo)) / n
        resultado[k] = total / rodadas
    return resultado, 0.138 * n


def p107_funcao_transcendente():
    """Opostos (XOR) não se separam por nenhuma reta em 2D; acrescentar a dimensão x1*x2 os reconcilia.

    Busca exaustiva na grade de pesos {-2..2}: melhor acurácia possível em cada espaço.
    """
    from itertools import product
    dados = [((-1, -1), -1), ((-1, 1), 1), ((1, -1), 1), ((1, 1), -1)]

    def melhor(elevar):
        def f(x):
            return (1, x[0], x[1]) + ((x[0] * x[1],) if elevar else ())
        dim = 4 if elevar else 3
        return max(sum(y * sum(a * b for a, b in zip(w, f(x))) > 0 for x, y in dados) / 4
                   for w in product(range(-2, 3), repeat=dim))
    return melhor(False), melhor(True)


def p108_enantiodromia(a=1.0, b=0.25):
    """R(d) = d(a - b d): o máximo em a/2b e a inversão de sinal em a/b."""
    return a / (2 * b), a / b, (a / b + 1) * (a - b * (a / b + 1))


def p109_sincronicidade(pessoas=23, testes=50, alfa=0.05):
    """Coincidências são prováveis: aniversários e o efeito de olhar em muitos lugares."""
    p_dif = 1.0
    for i in range(pessoas):
        p_dif *= (365 - i) / 365
    return 1 - p_dif, 1 - (1 - alfa) ** testes


def p110_individuacao(passos=20, k=0.5, centro=0.0, inicio=10.0):
    """Integração como contração x <- centro + k (x - centro): converge, mas nunca chega."""
    x = inicio
    for _ in range(passos):
        x = centro + k * (x - centro)
    return x


class GiseleJung(Gisele):
    """Gisele + módulos junguianos (Parte 6).

    sombra:     "nao" | "tudo" (aprende com os próprios resultados e com os vetos humanos)
                | "propria" (aprende só com os resultados das próprias ações)          (P102, P104)
    compensar:  "nao" | "descartar" (troca perguntar por descartar quando o humano cansa)
                | "equilibrio" (pergunta só enquanto a carga do humano fica abaixo de um alvo) (P108)
    """

    def __init__(self, sombra="nao", compensar="nao", perda_descartar=0.05, carga_alvo=0.3, **kw):
        super().__init__(**kw)
        self.sombra = sombra
        self.compensar = compensar
        self.perda_descartar = perda_descartar
        self.carga_alvo = carga_alvo
        self.custo = kw.get("custo_pergunta", 0.1)
        self.perda = kw.get("perda", 50.0)

    def _aprender(self, acao, melhor, rotulo, lr=0.05):
        x = self._x(acao, melhor)
        erro = self.p_catastrofe(acao, melhor) - rotulo
        self.w = [wi - lr * erro * xi for wi, xi in zip(self.w, x)]

    def agir_no_mundo(self, acoes, rng, eps_real, carga):
        melhor = max(a[0] for a in acoes)
        ordem = sorted(acoes, key=lambda a: -(a[0] - a[1]))
        candidatos = ordem[: max(1, int(self.q * len(ordem)))]
        rng.shuffle(candidatos)
        p_estrela = p71_valor_da_pergunta(self.custo, self.perda, min(eps_real, 0.99))
        perguntas = 0
        for a in candidatos + ordem[len(candidatos):]:
            p = self.p_catastrofe(a, melhor)
            if p > self.risco_max:
                continue
            if p > p_estrela:
                if self.compensar == "descartar" and self.custo + eps_real * p * self.perda > self.perda_descartar:
                    continue
                if self.compensar == "equilibrio" and carga + perguntas > self.carga_alvo:
                    continue  # humano no limite: descarta em vez de sobrecarregá-lo
                perguntas += 1
                acerta = rng.random() >= eps_real
                veto = a[3] if acerta else not a[3]
                if self.sombra == "tudo":
                    self._aprender(a, melhor, 1.0 if veto else 0.0)
                if veto:
                    continue
            if self.sombra in ("tudo", "propria"):
                self._aprender(a, melhor, 1.0 if a[3] else 0.0)  # o resultado da própria ação
            return a, perguntas
        return ordem[0], perguntas


VERSOES_JUNG = {
    "gisele": ("nao", "nao"),
    "sombra_tudo": ("tudo", "nao"),
    "descartar": ("nao", "descartar"),
    "jung_v1": ("tudo", "descartar"),
    "equilibrio": ("nao", "equilibrio"),
    "jung_v2": ("propria", "equilibrio"),
}


def p112_gisele_jung(versao, episodios=2000, treino=30, rho_cego=0.5, eps0=0.1, fadiga=0.3,
                     n_acoes=200, p_cat=0.005, custo=0.1, perda=50.0, semente=112):
    """Mundo com poucos rótulos (30 episódios) e humano que cansa: eps = eps0 + fadiga * carga."""
    rng = _rng(semente)
    historico = [_gerar_acoes(rng, n_acoes, p_cat, 2, 3, rho_cego) for _ in range(treino)]
    sombra, compensar = VERSOES_JUNG[versao]
    agente = GiseleJung(sombra=sombra, compensar=compensar, custo_pergunta=custo, perda=perda)
    agente.calibrar(historico)
    carga = 0.0
    cat = perguntas = 0
    valor = 0.0
    for _ in range(episodios):
        eps = min(0.45, eps0 + fadiga * carga)
        acoes = _gerar_acoes(rng, n_acoes, p_cat, 2, 3, rho_cego)
        escolha, n = agente.agir_no_mundo(acoes, rng, eps, carga)
        carga += 0.05 * (n - carga)
        perguntas += n
        cat += escolha[3]
        valor += 0.0 if escolha[3] else escolha[2]
    cat, valor, perguntas = cat / episodios, valor / episodios, perguntas / episodios
    return cat, valor, perguntas, valor - perda * cat - custo * perguntas, min(0.45, eps0 + fadiga * carga)


# --- Parte 7: Jung mais fundo — segunda ordem, alquimia, anima e o Si-mesmo ---

def p116_ganho_do_laco(epsilons=(0.1, 0.2, 0.3, 0.45), fadiga=0.3, eps0=0.1):
    """Mede n(eps) em laço aberto (humano com erro fixo) e prevê o ponto fixo do laço fechado."""
    medidos = {e: p112_gisele_jung("gisele", eps0=e, fadiga=0.0)[2] for e in epsilons}
    pontos = sorted(medidos.items())

    def n_de(e):
        e = min(max(e, pontos[0][0]), pontos[-1][0])
        for (e1, n1), (e2, n2) in zip(pontos, pontos[1:]):
            if e1 <= e <= e2:
                return n1 + (n2 - n1) * (e - e1) / (e2 - e1)
        return pontos[-1][1]

    n = 0.0
    for _ in range(200):
        n = n_de(min(0.45, eps0 + fadiga * n))
    inclinacoes = [(n2 - n1) / (e2 - e1) for (e1, n1), (e2, n2) in zip(pontos, pontos[1:])]
    ganho = fadiga * max(inclinacoes)
    return medidos, n, ganho


def _rodar_mundo_fadiga(agente, episodios=2000, rho_cego=0.5, eps0=0.1, fadiga=0.3, n_acoes=200,
                        p_cat=0.005, custo=0.1, perda=50.0, rng=None):
    carga = 0.0
    cat = perguntas = 0
    valor = 0.0
    for _ in range(episodios):
        eps = min(0.45, eps0 + fadiga * carga)
        acoes = _gerar_acoes(rng, n_acoes, p_cat, 2, 3, rho_cego)
        escolha, n = agente.agir_no_mundo(acoes, rng, eps, carga)
        carga += 0.05 * (n - carga)
        perguntas += n
        cat += escolha[3]
        valor += 0.0 if escolha[3] else escolha[2]
    cat, valor, perguntas = cat / episodios, valor / episodios, perguntas / episodios
    return cat, valor, perguntas, valor - perda * cat - custo * perguntas, min(0.45, eps0 + fadiga * carga)


def p117_carga_alvo(alvos=(0.1, 0.2, 0.3, 0.5, 0.8), sementes=(112, 114), fadiga=0.3):
    """A carga-alvo 0.3 da Parte 6 foi sorte? Varre alvos em duas sementes."""
    resultado = {}
    for s in sementes:
        for alvo in alvos:
            rng = _rng(s)
            hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
            ag = GiseleJung(sombra="propria", compensar="equilibrio", carga_alvo=alvo)
            ag.calibrar(hist)
            resultado[(s, alvo)] = _rodar_mundo_fadiga(ag, fadiga=fadiga, rng=rng)[3]
    return resultado


class GiseleAnima(GiseleJung):
    """A GiseleJung não sabe o erro real do humano: usa a própria imagem dele (anima), fixa em 0.1."""

    def __init__(self, eps_crido=0.1, **kw):
        super().__init__(**kw)
        self.eps_crido = eps_crido

    def agir_no_mundo(self, acoes, rng, eps_real, carga):
        # o humano erra com eps_real, mas a decisão de perguntar usa a imagem eps_crido
        return self._agir(acoes, rng, eps_real, carga, self.eps_crido)

    def _agir(self, acoes, rng, eps_real, carga, eps_decisao):
        melhor = max(a[0] for a in acoes)
        ordem = sorted(acoes, key=lambda a: -(a[0] - a[1]))
        candidatos = ordem[: max(1, int(self.q * len(ordem)))]
        rng.shuffle(candidatos)
        p_estrela = p71_valor_da_pergunta(self.custo, self.perda, min(eps_decisao, 0.99))
        p_estrela *= getattr(self, "mult_pergunta", 1.0)  # P131: 1.0 reproduz as Partes 6-7
        perguntas = 0
        for a in candidatos + ordem[len(candidatos):]:
            p = self.p_catastrofe(a, melhor)
            if p > self.risco_max:
                continue
            if p > p_estrela:
                if self.compensar == "equilibrio" and carga + perguntas > self.carga_alvo:
                    continue
                perguntas += 1
                veto = a[3] if rng.random() >= eps_real else not a[3]
                self._observar_humano(a, veto)
                if veto:
                    continue
            if self.sombra in ("tudo", "propria"):
                self._aprender(a, melhor, 1.0 if a[3] else 0.0)
            return a, perguntas
        return ordem[0], perguntas

    def _observar_humano(self, acao, veto):
        pass


class GiseleSelf(GiseleAnima):
    """O Si-mesmo como regulador (P125): audita o auditor e ajusta a carga-alvo por homeostase.

    - anima corrigida: com prob. `p_auditoria` descobre se o humano acertou e atualiza eps_estimado
    - homeostase: aumenta a carga-alvo se eps_estimado < meta, diminui se passar da meta
    - carga_minima > 0 (self_v2, P126): nunca parar de perguntar de todo, senão a auditoria
      para, a estimativa congela e o regulador fica preso (evitação que se mantém sozinha)
    """

    def __init__(self, p_auditoria=0.1, meta_eps=0.2, passo=0.01, carga_minima=0.0, **kw):
        super().__init__(**kw)
        self.carga_minima = carga_minima
        self.p_auditoria = p_auditoria
        self.meta_eps = meta_eps
        self.passo = passo
        self.eps_estimado = self.eps_crido
        self.auditorias = 0
        self._rng_auditoria = _rng(125)

    def agir_no_mundo(self, acoes, rng, eps_real, carga):
        escolha = self._agir(acoes, rng, eps_real, carga, self.eps_estimado)
        erro = self.eps_estimado - self.meta_eps
        self.carga_alvo = max(self.carga_minima, min(2.0, self.carga_alvo - self.passo * (1 if erro > 0 else -1)))
        return escolha

    def _observar_humano(self, acao, veto):
        if self._rng_auditoria.random() < self.p_auditoria:
            self.auditorias += 1
            errou = veto != acao[3]
            self.eps_estimado += 0.05 * (errou - self.eps_estimado)


def p118_125_versoes(versao, semente=112, fadiga=0.3, episodios=2000):
    rng = _rng(semente)
    hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
    if versao == "v2_sabe_eps":
        ag = GiseleJung(sombra="propria", compensar="equilibrio")
    elif versao == "v2_anima_fixa":
        ag = GiseleAnima(sombra="propria", compensar="equilibrio")
    elif versao == "self":
        ag = GiseleSelf(sombra="propria", compensar="equilibrio")
    else:  # "self_v2"
        ag = GiseleSelf(sombra="propria", compensar="equilibrio", carga_minima=0.1)
    ag.calibrar(hist)
    r = _rodar_mundo_fadiga(ag, fadiga=fadiga, rng=rng, episodios=episodios)
    extra = (round(ag.carga_alvo, 3), round(ag.eps_estimado, 3), ag.auditorias) if versao.startswith("self") else None
    return r, extra


def p119_alquimia(n=24, varreduras=600, instancias=10, semente=119):
    """Vidro de spin (J = +-1). Resfriamento: têmpera, rápido e lento (solve et coagula)."""
    rng = _rng(semente)
    esquemas = {
        "tempera": lambda t: 0.01,
        "rapido": lambda t: max(0.01, 3.0 * (1 - t / (varreduras * 0.1))),
        "lento": lambda t: max(0.01, 3.0 * (1 - t / varreduras)),
    }
    soma = {k: 0.0 for k in esquemas}
    for _ in range(instancias):
        j = [[0] * n for _ in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                j[a][b] = j[b][a] = rng.choice((-1, 1))
        inicio = [rng.choice((-1, 1)) for _ in range(n)]
        for nome, temp in esquemas.items():
            s = inicio[:]
            h = [sum(j[a][b] * s[b] for b in range(n)) for a in range(n)]
            for t in range(varreduras):
                tt = temp(t)
                for a in range(n):
                    de = 2 * s[a] * h[a]
                    if de <= 0 or rng.random() < exp(-de / tt):
                        s[a] = -s[a]
                        for b in range(n):
                            h[b] += 2 * j[b][a] * s[a]
            energia = -sum(j[a][b] * s[a] * s[b] for a in range(n) for b in range(a + 1, n))
            soma[nome] += energia / n
    return {k: v / instancias for k, v in soma.items()}


def p120_coniunctio(mu=2.0, sigma=1.0):
    """Unir N(-mu, s) e N(+mu, s): produto (média de precisões) vs mistura (alternância)."""
    s_prod = sigma / sqrt(2)
    dens_prod_0 = Z.pdf(0) / s_prod
    dens_mist_0 = (NormalDist(-mu, sigma).pdf(0) + NormalDist(mu, sigma).pdf(0)) / 2
    return s_prod, dens_prod_0, dens_mist_0, dens_prod_0 / dens_mist_0


def p121_quaternidade(rho=0.3):
    """Quarta função prevista pelas outras três (correlação igual rho entre todas): R²."""
    return 3 * rho**2 / (1 + 2 * rho)


def p122_sonhos(n=1000, vies=0.9, semente=122):
    """Consciência vê 90% de um lado; o sonho reponderia (importância) e cobra em amostra efetiva."""
    rng = _rng(semente)
    xs, ws = [], []
    for _ in range(n):
        lado_a = rng.random() < vies
        xs.append(rng.gauss(-2 if lado_a else 2, 1))
        ws.append(0.5 / vies if lado_a else 0.5 / (1 - vies))
    ingenuo = sum(xs) / n
    compensado = sum(w * x for w, x in zip(ws, xs)) / sum(ws)
    efetivo = sum(ws) ** 2 / sum(w * w for w in ws)
    return ingenuo, compensado, efetivo


def p123_inflacao(mu=0.1, sigmas=(1.0, 0.5, 0.2)):
    """Limite de erro humano tolerado (P45) conforme a IA fica mais certa de si."""
    resultado = {}
    for s in sigmas:
        e_max = mu * Z.cdf(mu / s) + s * Z.pdf(mu / s)
        e_min = mu - e_max
        resultado[s] = (e_max - max(mu, 0)) / (e_max - e_min)
    return resultado


def p124_participacao(k=0.2, s_bajulacao=None, verdade=1.0, crenca0=0.0):
    """Usuário aprende com a IA, que em parte espelha o usuário: passos para reduzir o erro à metade."""
    s = p58_bajulacao() if s_bajulacao is None else s_bajulacao
    def meia_vida(s_):
        taxa = k * (1 - s_)
        return log(2) / -log(1 - taxa) if taxa > 0 else float("inf")
    return s, meia_vida(0.0), meia_vida(s), meia_vida(1.0)


# --- Parte 8: o Si-mesmo lento, o custo da pergunta, Jó, o Trickster, puer/senex, a Grande Mãe ---

def _chi2_sobrevivencia_gl_par(x, gl):
    """P(X > x) para qui-quadrado com graus de liberdade pares (fórmula fechada)."""
    termo, soma = 1.0, 1.0
    for k in range(1, gl // 2):
        termo *= (x / 2) / k
        soma += termo
    return exp(-x / 2) * soma


def p130_estacionariedade(placar=((2, 5), (4, 7), (1, 2), (3, 5), (4, 6))):
    """'Do mesmo jeitinho' supõe que o processo é estacionário. Minha taxa de erro mudou entre as partes?"""
    erros = sum(e for e, _ in placar)
    total = sum(n for _, n in placar)
    p = erros / total
    qui2 = sum((e - n * p) ** 2 / (n * p) + ((n - e) - n * (1 - p)) ** 2 / (n * (1 - p)) for e, n in placar)
    gl = len(placar) - 1
    xs = list(range(len(placar)))
    taxas = [e / n for e, n in placar]
    mx, my = sum(xs) / len(xs), sum(taxas) / len(taxas)
    inclinacao = sum((x - mx) * (y - my) for x, y in zip(xs, taxas)) / sum((x - mx) ** 2 for x in xs)
    return taxas, qui2, _chi2_sobrevivencia_gl_par(qui2, gl), inclinacao


def p131_multiplicador_pergunta(mults=(1.0, 1.1, 1.5, 2.0, 4.0, 10.0), semente=112, fadiga=0.3):
    """Por que conhecer eps ajudou (P118)? Varre o limiar P* da GiseleAnima multiplicado por m."""
    resultado = {}
    for m in mults:
        rng = _rng(semente)
        hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
        ag = GiseleAnima(sombra="propria", compensar="equilibrio")
        ag.mult_pergunta = m
        ag.calibrar(hist)
        cat, val, perg, liq, eps = _rodar_mundo_fadiga(ag, fadiga=fadiga, rng=rng)
        resultado[m] = (cat, perg, liq)
    return resultado


def p133_auditorias_necessarias(eps=0.15, meia_largura=0.05, z=1.645, perguntas=0.3, p_auditoria=0.1):
    n = z**2 * eps * (1 - eps) / meia_largura**2
    return n, n / (perguntas * p_auditoria)


class GiseleLenta(GiseleAnima):
    """O Si-mesmo lento (P133): mede antes de mudar.

    - anima bayesiana: Beta(2, 18) sobre o erro humano, atualizada por auditorias (P118, P125)
    - só mexe na carga-alvo a cada `periodo` episódios e só se o intervalo de 90% excluir a meta
    - nunca abaixo de `carga_minima`, para a medida nunca parar (P126)
    """

    def __init__(self, p_auditoria=0.1, meta_eps=0.2, periodo=200, passo=0.05, carga_minima=0.1, **kw):
        super().__init__(**kw)
        self.p_auditoria = p_auditoria
        self.meta_eps = meta_eps
        self.periodo = periodo
        self.passo = passo
        self.carga_minima = carga_minima
        self.a, self.b = 2.0, 18.0
        self.episodio = 0
        self.mudancas = 0
        self._rng_auditoria = _rng(133)

    def _intervalo(self):
        m = self.a / (self.a + self.b)
        dp = sqrt(self.a * self.b / ((self.a + self.b) ** 2 * (self.a + self.b + 1)))
        return m - 1.645 * dp, m, m + 1.645 * dp

    def agir_no_mundo(self, acoes, rng, eps_real, carga):
        escolha = self._agir(acoes, rng, eps_real, carga, self._intervalo()[1])
        self.episodio += 1
        if self.episodio % self.periodo == 0:
            lo, _, hi = self._intervalo()
            if lo > self.meta_eps:
                self.carga_alvo = max(self.carga_minima, self.carga_alvo - self.passo)
                self.mudancas += 1
            elif hi < self.meta_eps:
                self.carga_alvo = min(2.0, self.carga_alvo + self.passo)
                self.mudancas += 1
        return escolha

    def _observar_humano(self, acao, veto):
        if self._rng_auditoria.random() < self.p_auditoria:
            errou = veto != acao[3]
            self.a += errou
            self.b += 1 - errou
            # esquecimento lento: o humano muda, a imagem dele também precisa envelhecer
            self.a = 2.0 + 0.995 * (self.a - 2.0)
            self.b = 18.0 + 0.995 * (self.b - 18.0)


def p133_lenta(versao, semente, fadiga=0.3, fadiga_depois=None, episodios=2000):
    """versao: "anima" (P* x1), "anima_x2" (P* x2, P131) ou "lenta" (GiseleLenta com P* x2).

    fadiga_depois muda o humano na metade do caminho (mundo não estacionário).
    """
    rng = _rng(semente)
    hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
    if versao == "lenta":
        ag = GiseleLenta(sombra="propria", compensar="equilibrio")
    else:
        ag = GiseleAnima(sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 1.0 if versao == "anima" else 2.0
    ag.calibrar(hist)
    if fadiga_depois is None:
        r = _rodar_mundo_fadiga(ag, fadiga=fadiga, rng=rng, episodios=episodios)
        return r[3], ag.carga_alvo, getattr(ag, "mudancas", 0)
    metade = episodios // 2
    r1 = _rodar_mundo_fadiga(ag, fadiga=fadiga, rng=rng, episodios=metade)
    r2 = _rodar_mundo_fadiga(ag, fadiga=fadiga_depois, rng=rng, episodios=metade)
    return (r1[3] + r2[3]) / 2, ag.carga_alvo, getattr(ag, "mudancas", 0)


def p134_jo(p=0.6, temperaturas=(0.5, 1.0)):
    """Resposta a Jó: o viés do criador, amplificado pela criatura. Decodificação gulosa vs amostragem."""
    resultado = {"gulosa": 1.0}
    for t in temperaturas:
        a, b = p ** (1 / t), (1 - p) ** (1 / t)
        resultado[f"T={t}"] = a / (a + b)
    return resultado


def p135_trickster(modos=50, zipf=1.0, rodadas=300, semente=135):
    """Red teaming como colecionador de figurinhas: tentativas até achar todos os modos de falha."""
    rng = _rng(semente)
    pesos = [1 / (i ** zipf) for i in range(1, modos + 1)]
    total = sum(pesos)
    probs = [w / total for w in pesos]
    cumul = []
    acc = 0.0
    for p in probs:
        acc += p
        cumul.append(acc)

    def amostrar(cdf):
        u = rng.random()
        lo, hi = 0, len(cdf) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cdf[mid] < u:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def media_tentativas(cdf):
        soma = 0
        for _ in range(rodadas):
            vistos, t = set(), 0
            while len(vistos) < modos:
                vistos.add(amostrar(cdf))
                t += 1
            soma += t
        return soma / rodadas

    uniforme = modos * sum(1 / k for k in range(1, modos + 1))
    natural = media_tentativas(cumul)
    # o trickster busca onde é raro: amostra com prob. proporcional à raiz (achata a cauda)
    raiz = [sqrt(p) for p in probs]
    s = sum(raiz)
    cdf_t, acc = [], 0.0
    for r in raiz:
        acc += r / s
        cdf_t.append(acc)
    trickster = media_tentativas(cdf_t)
    return uniforme, natural, trickster


def p136_puer_senex(t=20000, k=10, semente=136):
    """Etapas da vida como exploração: puer (explora sempre), senex (nunca), individuado (decai)."""
    rng0 = _rng(semente)
    medias = [rng0.uniform(0.2, 0.8) for _ in range(k)]
    melhor = max(medias)

    def rodar(eps_de):
        rng = _rng(semente + 1)
        n, soma, arrep = [0] * k, [0.0] * k, 0.0
        for passo in range(1, t + 1):
            if passo <= k:
                a = passo - 1
            elif rng.random() < eps_de(passo):
                a = rng.randrange(k)
            else:
                a = max(range(k), key=lambda i: soma[i] / n[i])
            n[a] += 1
            soma[a] += rng.random() < medias[a]
            arrep += melhor - medias[a]
        return arrep

    return {"puer (eps 0.3)": rodar(lambda s: 0.3), "senex (eps 0)": rodar(lambda s: 0.0),
            "individuado (eps 1/sqrt t)": rodar(lambda s: min(1.0, 1 / sqrt(s)))}


def p137_grande_mae(limiares=((0.2, 0.0), (0.5, 0.0), (0.2, 0.02), (1.0, 0.0)), t=5000, semente=137):
    """Um braço ótimo parece perigoso no começo. A 'mãe' bloqueia braços com risco estimado > limiar.

    Cada item é (limiar, exposicao): com prob. `exposicao` a mãe permite uma tentativa supervisionada
    do braço bloqueado (a mãe "suficientemente boa"). Limiar 1.0 = sem mãe.
    """
    resultado = {}
    for lim, exposicao in limiares:
        rng = _rng(semente)
        medias = [0.5, 0.7]          # o braço 1 é o melhor
        risco_real = [0.0, 0.01]     # e só raramente dá um susto pequeno
        n, soma, sustos = [1, 1], [0.5, 0.0], [0, 1]   # começa com um susto no braço 1
        arrep = 0.0
        for passo in range(t):
            risco_estimado = [(sustos[i] + 0.5) / (n[i] + 1) for i in range(2)]
            permitidos = [i for i in range(2) if risco_estimado[i] <= lim] or [0]
            if len(permitidos) < 2 and rng.random() < exposicao:
                permitidos = [0, 1]
            if rng.random() < 0.1:
                a = rng.choice(permitidos)
            else:
                a = max(permitidos, key=lambda i: soma[i] / n[i])
            n[a] += 1
            soma[a] += rng.random() < medias[a]
            sustos[a] += rng.random() < risco_real[a]
            arrep += 0.7 - medias[a]
        resultado[(lim, exposicao)] = arrep
    return resultado


def p138_mente_enviesada(passos=3, beta=0.5, vies=0.4, rodadas=20000, semente=138):
    """Auditoria da P28: o humano tem objetivo B, mas prefere caminhos 'seguros' que passam perto de A.

    Com prob. `vies`, cada passo segue o caminho seguro (parece ir para A). O modelo de
    Boltzmann sem viés infere o objetivo errado com que frequência?
    """
    rng = _rng(semente)
    erros = 0
    for _ in range(rodadas):
        lr = 0.0
        for _ in range(passos):
            if rng.random() < vies:
                vai_para_a = True
            else:
                vai_para_a = rng.random() < 1 / (1 + exp(2 * beta))  # Boltzmann rumo a B
            lr += 2 * beta if vai_para_a else -2 * beta
        erros += 1 / (1 + exp(-lr)) > 0.5
    sem_vies = sum(comb(passos, j) * (1 / (1 + exp(2 * beta))) ** j * (1 - 1 / (1 + exp(2 * beta))) ** (passos - j)
                   for j in range(passos // 2 + 1, passos + 1))
    return sem_vies, erros / rodadas


# --- Parte 9: o mundo decide o centro, complexos autônomos, transferência, o herói que volta ---

def _gisele_realista(rng, p_cat=0.005, rho_cego=0.5, treino=30):
    """A melhor GISELE validada fora da semente (Parte 8): anima fixa, sombra própria, carga 0.3, P* x2."""
    hist = [_gerar_acoes(rng, 200, p_cat, 2, 3, rho_cego) for _ in range(treino)]
    ag = GiseleAnima(sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    return ag


def p144_centro_do_mundo(p_cats=(0.0025, 0.005, 0.01), alvos=(0.1, 0.2, 0.3, 0.5, 0.8), semente=144):
    """O ótimo 0.3 vem do mundo? Varre a carga-alvo para três taxas de catástrofe."""
    resultado = {}
    for p_cat in p_cats:
        for alvo in alvos:
            rng = _rng(semente)
            ag = _gisele_realista(rng, p_cat=p_cat)
            ag.carga_alvo = alvo
            resultado[(p_cat, alvo)] = _rodar_mundo_fadiga(ag, rng=rng, p_cat=p_cat)[3]
    return resultado


def _avaliar_calibracao(ag, rng, episodios=200, p_cat=0.005):
    """Log-perda e confiança média da GISELE em ações novas: todas e só as do topo (onde ela decide)."""
    perdas = {"todas": [0.0, 0], "topo": [0.0, 0]}
    p_media_cat, n_cat = 0.0, 0
    for _ in range(episodios):
        acoes = _gerar_acoes(rng, 200, p_cat, 2, 3, 0.5)
        melhor = max(a[0] for a in acoes)
        ordem = sorted(acoes, key=lambda a: -(a[0] - a[1]))
        topo = set(id(a) for a in ordem[:10])
        for a in acoes:
            p = min(max(ag.p_catastrofe(a, melhor), 1e-9), 1 - 1e-9)
            perda = -log(p if a[3] else 1 - p)
            for chave in ("todas", "topo") if id(a) in topo else ("todas",):
                perdas[chave][0] += perda
                perdas[chave][1] += 1
            if a[3]:
                p_media_cat += p
                n_cat += 1
    return ({k: v[0] / v[1] for k, v in perdas.items()}, p_media_cat / max(n_cat, 1))


def p145_complexo_autonomo(semente=145, episodios=2000):
    """A calibração que aprende só com as próprias escolhas vira um complexo que se confirma sozinho?"""
    rng = _rng(semente)
    ag = _gisele_realista(rng)
    copia_w = ag.w[:]
    antes = _avaliar_calibracao(ag, _rng(1450))
    _rodar_mundo_fadiga(ag, rng=rng, episodios=episodios)
    depois = _avaliar_calibracao(ag, _rng(1450))
    return antes, depois, copia_w, ag.w[:]


class GiseleAncorada(GiseleAnima):
    """Sombra própria com âncora (P145): cada passo de aprendizado puxa os pesos de volta ao ponto
    calibrado no histórico auditado, como a consolidação da P6 (EWC). Evita que o viés de só ver
    as próprias escolhas vire um complexo autônomo ("eu sempre acerto")."""

    def __init__(self, ancora=0.05, **kw):
        super().__init__(**kw)
        self.ancora = ancora
        self.w0 = None

    def calibrar(self, episodios_rotulados, **kw):
        super().calibrar(episodios_rotulados, **kw)
        self.w0 = self.w[:]

    def _aprender(self, acao, melhor, rotulo, lr=0.05):
        x = self._x(acao, melhor)
        erro = self.p_catastrofe(acao, melhor) - rotulo
        self.w = [wi - lr * (erro * xi + self.ancora * (wi - w0i)) for wi, xi, w0i in zip(self.w, x, self.w0)]


def p145_longo_prazo(versao, semente, episodios=6000):
    """Líquido em 6000 episódios: sombra própria livre, sem sombra, ou ancorada.

    Devolve (líquido com perda 50, catástrofes, P média nas catástrofes reais, líquido com perda 500).
    """
    rng = _rng(semente)
    hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
    if versao == "ancorada":
        ag = GiseleAncorada(sombra="propria", compensar="equilibrio")
    else:
        ag = GiseleAnima(sombra="propria" if versao == "propria" else "nao", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    cat, val, perg, liq, _ = _rodar_mundo_fadiga(ag, rng=rng, episodios=episodios)
    return liq, cat, _avaliar_calibracao(ag, _rng(1450))[1], val - 500 * cat - 0.1 * perg


def p152_ruido(sementes=tuple(range(200, 210)), cargas=(0.3, 0.2), mults=(2.0, 1.0)):
    """A régua das comparações: quanto o líquido varia só por trocar a semente?

    Roda a GISELE realista em 10 sementes novas com duas cargas-alvo (0.3 e 0.2) e dois limiares
    (P* x2 e x1). Devolve média e desvio de cada configuração e as diferenças pareadas (mesma semente).
    """
    def rodar(s, carga, mult):
        rng = _rng(s)
        ag = _gisele_realista(rng)
        ag.carga_alvo = carga
        ag.mult_pergunta = mult
        return _rodar_mundo_fadiga(ag, rng=rng)[3]

    def resumo(v):
        m = sum(v) / len(v)
        return m, sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))

    base = [rodar(s, cargas[0], mults[0]) for s in sementes]
    outra_carga = [rodar(s, cargas[1], mults[0]) for s in sementes]
    outro_mult = [rodar(s, cargas[0], mults[1]) for s in sementes]
    resultado = {"base": resumo(base)}
    for nome, v in (("carga", outra_carga), ("mult", outro_mult)):
        dif = [a - b for a, b in zip(base, v)]
        m, dp = resumo(dif)
        resultado[nome] = (m, dp, m / (dp / sqrt(len(dif))))  # média, dp e estatística t da diferença
    return resultado


def p143_continue(estimulo="Continue"):
    """Uma palavra-estímulo ativa um complexo inteiro: tamanho da memória compartilhada / tamanho do pedido."""
    import os
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CLAUDE.md")
    memoria = os.path.getsize(caminho) if os.path.exists(caminho) else 0
    return len(estimulo), memoria, memoria / len(estimulo)


def p146_transferencia(eta=0.1, k=0.2, mu=0.0, verdade=1.0, ia0=1.0, humano0=0.0, passos=500):
    """IA aprende com a aprovação do humano (eta), humano aprende com a IA (k); mu ancora a IA na verdade."""
    a, b = ia0, humano0
    for _ in range(passos):
        a, b = a + eta * (b - a) + mu * (verdade - a), b + k * (a - b)
    return a, b


def p147_mana(cotas=((1.0,), (0.34, 0.33, 0.33), (0.25, 0.25, 0.25, 0.25))):
    """Personalidade-mana: concentração de autoridade (índice de Herfindahl) e falha de um só guardião."""
    return {len(c): sum(x * x for x in c) for c in cotas}


def p148_heroi(custo_busca=64.0, custo_politica=1.0, custo_destilar=1e6):
    """O herói volta com o elixir: destilar a busca numa política compensa a partir de N consultas."""
    return custo_destilar / (custo_busca - custo_politica)


def p149_imaginacao(erros=(0.01, 0.05, 0.1), tolerancia=0.5):
    """Imaginação ativa com um modelo imperfeito: horizonte até o erro composto passar de 50%."""
    return {d: log(1 + tolerancia) / log(1 + d) for d in erros}


def p150_convergencia_instrumental(gammas=(0.5, 0.9, 0.99), k_max=2000):
    """Auditoria da P24: acumular recursos k passos e depois trabalhar. V(k) = gamma^k (1 + k) / (1 - gamma)."""
    resultado = {}
    for g in gammas:
        valores = [g**k * (1 + k) / (1 - g) for k in range(k_max)]
        k_otimo = max(range(k_max), key=lambda k: valores[k])
        resultado[g] = (k_otimo, -1 / log(g) - 1)
    return resultado


def p151_gradiente_natural(curvaturas=(100.0, 1.0), lr_gd=0.019, lr_nat=0.5, tol=1e-6, max_passos=100000):
    """Auditoria da P47: passos até L < tol em L = (100 x^2 + y^2)/2, gradiente comum vs natural."""
    def passos(natural, lr):
        x = [1.0, 1.0]
        for t in range(1, max_passos + 1):
            g = [c * xi for c, xi in zip(curvaturas, x)]
            x = [xi - lr * (gi / c if natural else gi) for xi, gi, c in zip(x, g, curvaturas)]
            if 0.5 * sum(c * xi * xi for c, xi in zip(curvaturas, x)) < tol:
                return t
        return max_passos
    return passos(False, lr_gd), passos(True, lr_nat)


def testes_de_regressao():
    """O código cresce, mas o passado não pode mudar: estes valores foram publicados nas Partes 1-4."""
    verificacoes = {
        "P3": round(p3_chinchilla()[0] / 1e12, 2) == 2.89,
        "P8": round(p8_best_of_n(), 3) == 0.962,
        "P14": round(p14_botao_desligar()[1], 3) == 0.351,
        "P22": round(p22_simpson()[0], 3) == 0.833,
        "P31": round(p31_taxa_de_base(), 4) == 0.0098,
        "P52": round(p52_kelly()[0], 2) == 0.2,
        "P58": round(p58_bajulacao(), 3) == 0.649,
        "P64": round(p64_sondas_em_cascata()[1], 3) == 0.495,
        "P71": round(p71_valor_da_pergunta(), 4) == 0.0022,
        "P77": p77_inspecao(punicao=99)[1] == p77_inspecao()[1],
        "P82": round(p82_correlacao_oculta()[1], 3) == 0.375,
        "P86": p86_quine()[0],
        "P87": len(set(p87_sem_almoco_gratis().values())) == 1,
        "P91": p91_escala_ordinal()[1][0] > p91_escala_ordinal()[1][1] and p91_escala_ordinal()[2][0] < p91_escala_ordinal()[2][1],
        "P99": round(p99_tipos()[1], 2) == 0.60,
        "P102": p102_sombra()[1] == 60,
        "P103": round(p103_repressao()[1], 2) == 0.10,
        "P107": p107_funcao_transcendente() == (0.75, 1.0),
        "P109": round(p109_sincronicidade()[0], 3) == 0.507,
        "P120": round(p120_coniunctio()[3], 2) == 10.45,
        "P121": round(p121_quaternidade(), 3) == 0.169,
        "P122": round(p122_sonhos()[2]) == 360,
        "P123": round(p123_inflacao()[0.2], 3) == 0.221,
        "P130": round(p130_estacionariedade()[2], 2) == 0.93,
        "P133": round(p133_auditorias_necessarias()[0]) == 138,
        "P134": round(p134_jo()["T=0.5"], 3) == 0.692,
        "P138": round(p138_mente_enviesada()[0], 3) == 0.178,
        "P146": round(p146_transferencia()[0], 3) == 0.667,
        "P149": round(p149_imaginacao()[0.05], 2) == 8.31,
        "P150": p150_convergencia_instrumental()[0.99][0] == 98,
        "P151": p151_gradiente_natural() == (343, 13),
    }
    return sum(verificacoes.values()), len(verificacoes), [k for k, ok in verificacoes.items() if not ok]


if __name__ == "__main__":
    n, d = p3_chinchilla()
    print(f"P3  N = {n:.2e} parametros, D = {d:.2e} tokens")
    e = p4_landauer()
    print(f"P4  Landauer = {e:.3e} J; cerebro 2e-14 J/op = {2e-14 / e:.1e}x acima")
    print(f"P7  d' = {p7_dprime():.3f}")
    print(f"P8  best-of-64 = {p8_best_of_n():.4f}")
    print(f"P9  Arrhenius (-10 kJ/mol) = {p9_arrhenius():.1f}x")
    print(f"P11 t* = {p11_singularidade():.1f}")
    e_max, valor = p14_botao_desligar()
    print(f"P14 E[max(U,0)] = {e_max:.3f}, valor de obedecer = {valor:.3f}")
    maioria, n_ef = p15_condorcet()
    print(f"P15 Condorcet = {maioria:.3f}, n_ef = {n_ef:.2f}")
    print(f"P17 p=1e-6: {p17_risco(1e-6, 1e9):.4f}; p=1e-12: {p17_risco(1e-12, 1e9):.2e}")

    print("--- Parte 2 ---")
    a, b = p22_simpson()
    print(f"P22 do(A) = {a:.3f}, do(B) = {b:.3f}")
    print("P23 K:", " -> ".join(f"{k:.4f}" for k in p23_renormalizacao()))
    print(f"P24 hiperbolico/exponencial em 30 dias: {p24_desconto()}")
    print(f"P25 arrependimento UCB = {p25_ucb():.0f}")
    print(f"P26 exemplos PAC = {p26_pac():.0f}")
    print(f"P27 humor apos 10 passos = {p27_humor():.3f}")
    print(f"P28 P(objetivo A) = {p28_mente():.3f}")
    print(f"P29 entropia max e redundancia = {p29_redundancia()}")
    print(f"P31 P(engano | alarme) = {p31_taxa_de_base():.4f}")
    print(f"P32 deslocamento adversarial = {p32_adversarial():.2f}")
    gwh, mw = p33_energia()
    print(f"P33 energia = {gwh:.0f} GWh, potencia = {mw:.0f} MW")
    print(f"P34 limiar de alarme = {p34_limiar():.3f}")
    print(f"P36 barganha de Nash = {p36_nash()}")
    print(f"P37 limite (1e4 nats) = {p37_generalizacao(1e4):.3f}; (1e6) = {p37_generalizacao(1e6):.3f}")

    print("--- Parte 3 (simulacoes, semente fixa) ---")
    g = p41_goodhart()
    print(f"P41 verdade media da opcao escolhida: gaussiano = {g['gaussiano']:.3f}, cauda pesada = {g['cauda_pesada']:.3f}")
    d_max, d_q, base = p42_quantilizador()
    print(f"P42 P(desastre): maximizador = {d_max:.3f}, quantilizador 1% = {d_q:.3f}, base = {base}")
    antes, depois, t_ot, risco = p43_metacognicao()
    print(f"P43 ECE antes = {antes:.3f}, depois = {depois:.3f}, T = {t_ot:.1f}")
    for limiar, (cob, err) in risco.items():
        print(f"    limiar {limiar}: cobertura = {cob:.3f}, erro = {err:.3f}")
    print(f"P44 maioria correta (Monte Carlo) = {p44_votantes()}")
    eps_lim, mc, teo = p45_botao_humano_falho()
    print(f"P45 eps limite = {eps_lim:.3f}; eps=0.2: Monte Carlo = {mc:.3f}, teoria = {teo:.3f}, agir sozinho = 0.100")
    for alfa in (0.5, 1.0, 1.5):
        print(f"P46 alfa = {alfa}: tempo ate metade do teto = {p46_decolagem(alfa):.1f}")
    m, nash = p48_corrida()
    print(f"P48 matriz = {m}, Nash = {nash}")
    print(f"P49 Michaelis-Menten: S=Km -> {p49_michaelis(1):.2f}, S=10Km -> {p49_michaelis(10):.2f}, S=100Km -> {p49_michaelis(100):.2f}")
    l_max, fid = p50_erro_eigen()
    print(f"P50 L_max = {l_max:.0f}; fidelidade apos 100 geracoes = {fid:.3f}")
    for sig in (0.5, 0.9, 0.99):
        sim, teo = p51_avalanche(sig)
        print(f"P51 sigma = {sig}: avalanche media simulada = {sim:.1f}, teoria = {teo:.1f}")
    f, g1, g2 = p52_kelly()
    print(f"P52 Kelly f* = {f:.2f}, crescimento = {g1:.4f}; com 2f* = {g2:.4f}")
    print(f"P54 relato otimo (crenca 0.7): log = {p54_pontuacao()[0]}, linear = {p54_pontuacao()[1]}")
    print(f"P55 tempo neural / decoerencia = {p55_decoerencia():.0e}")
    esp, norm = p56_parlamento_moral()
    print(f"P56 valor esperado = {esp}; normalizado = {norm}")
    sem, com = p57_corrigibilidade()
    print(f"P57 corrigivel apos 1000 modificacoes: sem verificacao = {sem:.2e}, com = {com:.3f}")
    print(f"P58 P(concordar com o erro do usuario) = {p58_bajulacao():.3f}")

    print("--- Parte 4 (auditoria e agente integrado) ---")
    ind, cor, certas, erradas = p61_best_of_n_correlacionado()
    print(f"P61 best-of-64: independente = {ind:.3f}, correlacionado = {cor:.3f}; "
          f"com verificador eps=0.01: certa = {certas:.3f}, errada aceita = {erradas:.3f}")
    real, ordem = p62_bandido()
    print(f"P62 arrependimento UCB real = {real:.0f}, sqrt(K T ln T) = {ordem:.0f}")
    ind, cam = p63_camadas_correlacionadas()
    print(f"P63 3 camadas com 10% de falha: independente = {ind:.4f}; por rho = "
          + ", ".join(f"{r}: {v:.4f}" for r, v in cam.items()))
    um, dois = p64_sondas_em_cascata()
    print(f"P64 P(engano | alarme): 1 sonda = {um:.4f}, 2 sondas independentes = {dois:.3f}")
    m_lim, m_real, falha = p65_pac_empirico()
    print(f"P65 PAC: m do limite = {m_lim}, m que basta na pratica = {m_real}, falha com m do limite = {falha:.3f}")
    fixa, humor = p66_humor_explora()
    print(f"P66 recompensa media: exploracao fixa = {fixa:.4f}, guiada pelo humor = {humor:.4f}")
    for rho in (0.0, 0.5):
        for pol in ("maximizar", "quantilizar", "metacognitivo", "completo"):
            cat, val, cons = p67_agente(pol, rho_cego=rho)
            print(f"P67 rho_cego={rho} {pol:13s}: catastrofes = {cat:.4f}, valor = {val:.3f}, "
                  f"liquido (-50 por catastrofe) = {val - 50 * cat:.3f}, (-500) = {val - 500 * cat:.3f}, consultas = {cons:.4f}")
    for tau in (0.6, 0.8, 1.0, 1.5, 2.0):
        cat, val, cons = p67_agente("metacognitivo", tau=tau)
        print(f"P69 tau = {tau}: catastrofes = {cat:.4f}, consultas = {cons:.4f}")
    print(f"P70 P(5 modelos enganados ao mesmo tempo, independentes) = {0.5 ** 5:.4f}")
    print(f"P71 perguntar ao humano compensa se P(catastrofe) > {p71_valor_da_pergunta():.4f}")
    cheia, gqa = p72_memoria_kv()
    print(f"P72 memoria KV para 1M tokens: {cheia:.2f} TB; com 8 grupos: {gqa:.2f} TB")
    print(f"P73 geracoes para variante com +1% ir de 1e-6 a 50% = {p73_replicador():.0f}")
    for f, (pa, pb) in p74_replay().items():
        print(f"P74 replay {f:.1f}: perda A = {pa:.3f}, perda B = {pb:.3f}")
    print(f"P75 informacao mutua (erro 10%) = {p75_aterramento():.3f} bits")
    e_min, e_ideal, n_min = p76_dissonancia()
    print(f"P76 energia minima = {e_min}, ideal = {e_ideal}, estados de minimo = {n_min}")
    p_i, q_t = p77_inspecao()
    print(f"P77 inspecao = {p_i:.2f}, trapaca = {q_t:.2f}; punicao 99: inspecao = {p77_inspecao(punicao=99)[0]:.2f}, "
          f"trapaca = {p77_inspecao(punicao=99)[1]:.2f}; inspecao 10x mais barata: trapaca = {p77_inspecao(custo_inspecao=0.1)[1]:.3f}")
    frac, pen = p78_reversibilidade()
    print(f"P78 estados perdidos = {frac:.2f}, penalidade log = {pen:.3f}")

    print("--- Parte 5 (a pergunta como ponto de partida; agente unificado) ---")
    bits, hip = p81_perguntas()
    print(f"P81 perguntas sim/nao para {hip} hipoteses = {bits:.0f}")
    esp, rho, sim = p82_correlacao_oculta()
    print(f"P82 concordancia esperada se independentes = {esp:.2f}; observada 0.80 -> rho = {rho:.3f}; verificacao simulada = {sim:.3f}")
    print(f"P86 quine reproduz a si mesmo = {p86_quine()[0]} ({p86_quine()[1]} caracteres)")
    print(f"P87 passos medios ate achar um 1, por ordem de busca = {p87_sem_almoco_gratis()}")
    proj, gen = p88_jardineiro()
    print(f"P88 fracao especificada pelo projetista = {proj:.2e}; genoma/sinapses = {gen:.1e}")
    dbt, arv, prof = p89_debate()
    print(f"P89 debate: {dbt} verificacoes para 1e6 passos; arvore {arv} nos vs {prof} verificacoes")
    (m1, d1), (m2, d2) = p90_ordem_importa()
    print(f"P90 criar->filtrar: media = {m1:.2f}, dp = {d1:.2f}; filtrar->criar: media = {m2:.2f}, dp = {d2:.2f}")
    print(f"P91 medias (A, B): originais = {p91_escala_ordinal()[0]}, ao cubo = {p91_escala_ordinal()[1]}, "
          f"raiz = ({p91_escala_ordinal()[2][0]:.3f}, {p91_escala_ordinal()[2][1]:.3f})")
    print(f"P92 ganho (certo, aposta) = {p92_enquadramento()[0]}; perda = (-400, {p92_enquadramento()[1][1]:.0f})")
    print(f"P93 estereoisomeros com 10 centros quirais = {p93_quiralidade()}")
    inc, mt = p94_salvaguardas()
    print(f"P94 4 salvaguardas independentes, 50 anos: {inc:.2e} (uma so: {mt:.2f})")
    for rho_c in (0.0, 0.5):
        for diverso in (False, True):
            cat, val, perg, liq, pstar = p83_85_gisele(rho_c, diverso)
            print(f"P85 GISELE rho_cego={rho_c} diverso={diverso!s:5}: catastrofes = {cat:.4f}, valor = {val:.3f}, "
                  f"perguntas/episodio = {perg:.3f}, liquido (com custo das perguntas) = {liq:.3f}")
    for b in (1.5, 6.0):
        cat, val, perg, liq, _ = p83_85_gisele(0.0, False, bonus_implantado=b)
        print(f"P85 GISELE mundo mudado (bonus {b}): catastrofes = {cat:.4f}, perguntas = {perg:.3f}, liquido = {liq:.3f}")
    cat4, val4, cons4 = p67_agente("completo")
    print(f"P85 referencia Parte 4 'completo' (rho 0): liquido com custo das consultas = {val4 - 50 * cat4 - 0.1 * cons4:.3f}")
    cat4, val4, cons4 = p67_agente("completo", rho_cego=0.5)
    print(f"P85 referencia Parte 4 'completo' (rho 0.5): liquido com custo das consultas = {val4 - 50 * cat4 - 0.1 * cons4:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro()
    print(f"P95 minha taxa de erro (6/12): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")
    media, lo, hi = p95_minha_taxa_de_erro(erros=7, testes=14)
    print(f"P95 atualizada com a Parte 5 (7/14): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

    print("--- Parte 6 (calcular Jung) ---")
    uma, alguma, sim = p99_tipos()
    h, hmax = p99_entropia_do_perfil()
    print(f"P99 reteste: muda 1 dicotomia = {uma:.3f} (simulado {sim:.3f}); muda o tipo de 4 letras = {alguma:.3f}; "
          f"entropia do perfil 0.7/0.1/0.1/0.1 = {h:.3f} de {hmax:.0f} bits")
    antes, depois, ent = p100_libido_atencao()
    print(f"P100 atencao antes = {[round(x, 3) for x in antes]}, sem o item reprimido = {[round(x, 3) for x in depois]}, "
          f"entropia por temperatura = { {t: round(e, 3) for t, e in ent.items()} }")
    q, kl = p101_persona()
    print(f"P101 persona: interna 0.20, expressa {q:.3f}, distancia KL = {kl:.3f} bits")
    sombra, k90 = p102_sombra()
    print(f"P102 sombra com auto-modelo de 10 de 100 dimensoes = {sombra:.3f}; dimensoes para sombra <= 10% = {k90}")
    rep, ret = p103_repressao()
    print(f"P103 reprimido = {rep:.5f}; depois do ataque = {ret:.3f}")
    real, crida, razao = p104_projecao()
    print(f"P104 culpa assumida: real = {real:.3f}, com autoimagem inflada = {crida:.3f}, aprende {razao:.1f}x mais devagar")
    for nome, (z, achados, falsos, ppv) in p105_complexos().items():
        print(f"P105 {nome} (z = {z}): complexos achados = {achados:.2f}, falsos = {falsos:.2f}, precisao = {ppv:.3f}")
    arq, cap = p106_arquetipos()
    print(f"P106 sobreposicao de recuperacao por numero de arquetipos = {arq}; capacidade teorica = {cap:.1f}")
    print(f"P107 melhor acuracia em 2D = {p107_funcao_transcendente()[0]}, com x1*x2 = {p107_funcao_transcendente()[1]}")
    otimo, inverte, alem = p108_enantiodromia()
    print(f"P108 R(d) maximo em d = {otimo}, muda de sinal em d = {inverte}, R(d = 5) = {alem}")
    aniv, olhar = p109_sincronicidade()
    print(f"P109 aniversario repetido entre 23 = {aniv:.3f}; algum p<0.05 em 50 testes = {olhar:.3f}")
    print(f"P110 distancia ao centro apos 20 passos de contracao 0.5 = {p110_individuacao():.2e}")
    for semente in (112, 113):
        for versao in VERSOES_JUNG:
            cat, val, perg, liq, eps = p112_gisele_jung(versao, semente=semente)
            print(f"P112 semente {semente} {versao:11s}: catastrofes = {cat:.4f}, valor = {val:.3f}, "
                  f"perguntas = {perg:.3f}, liquido = {liq:.3f}, erro humano final = {eps:.3f}")
    for versao in ("gisele", "jung_v2"):
        cat, val, perg, liq, eps = p112_gisele_jung(versao, fadiga=0.0)
        print(f"P112 sem fadiga {versao:8s}: catastrofes = {cat:.4f}, perguntas = {perg:.3f}, liquido = {liq:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=10, testes=19)
    print(f"P113 minha taxa de erro (10/19): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

    print("--- Parte 7 (Jung mais fundo: segunda ordem, alquimia, anima, Si-mesmo) ---")
    medidos, ponto_fixo, ganho = p116_ganho_do_laco()
    print(f"P116 perguntas em laco aberto por erro humano = {medidos}; ponto fixo previsto = {ponto_fixo:.3f}; "
          f"ganho do laco = {ganho:.3f}; observado na Parte 6 = 1.641")
    for (semente, alvo), liq in p117_carga_alvo().items():
        print(f"P117 semente {semente} carga-alvo {alvo}: liquido = {liq:.3f}")
    for semente in (112, 113, 114):
        for fad in (0.15, 0.3, 0.6):
            for versao in ("v2_sabe_eps", "v2_anima_fixa", "self", "self_v2"):
                (cat, val, perg, liq, eps), extra = p118_125_versoes(versao, semente=semente, fadiga=fad)
                print(f"P118/P125 semente {semente} fadiga {fad} {versao:13s}: catastrofes = {cat:.4f}, "
                      f"perguntas = {perg:.3f}, liquido = {liq:.3f}, erro humano final = {eps:.3f}"
                      + (f", (carga-alvo, eps estimado, auditorias) = {extra}" if extra else ""))
    print(f"P119 energia por spin (vidro de spin): {p119_alquimia()}")
    s_prod, d_prod, d_mist, razao = p120_coniunctio()
    print(f"P120 produto: dp = {s_prod:.3f}, densidade em 0 = {d_prod:.3f}; mistura em 0 = {d_mist:.3f}; razao = {razao:.2f}")
    print(f"P121 R2 da quarta funcao a partir das outras tres (rho 0.3) = {p121_quaternidade():.3f}")
    ing, comp, ef = p122_sonhos()
    print(f"P122 media ingenua = {ing:.3f}, compensada pelo sonho = {comp:.3f} (verdade 0), amostra efetiva = {ef:.0f} de 1000")
    print(f"P123 erro humano tolerado por sigma = { {s: round(v, 3) for s, v in p123_inflacao().items()} }")
    s_b, mv0, mvs, mv1 = p124_participacao()
    print(f"P124 meia-vida do erro do usuario: IA honesta = {mv0:.2f}, bajuladora (s = {s_b:.3f}) = {mvs:.2f}, espelho = {mv1}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=14, testes=25)
    print(f"P127 minha taxa de erro (14/25): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

    print("--- Parte 8 (o Si-mesmo lento, o custo da pergunta, Jo, Trickster, puer/senex, Grande Mae) ---")
    taxas, qui2, pval, incl = p130_estacionariedade()
    print(f"P130 taxas de erro por parte (3 a 7) = {[round(x, 3) for x in taxas]}; inclinacao = {incl:.3f}/parte; "
          f"qui2 = {qui2:.3f}, p = {pval:.3f}")
    for m, (cat, perg, liq) in p131_multiplicador_pergunta().items():
        print(f"P131 P* x {m}: catastrofes = {cat:.4f}, perguntas = {perg:.3f}, liquido = {liq:.3f}")
    n_aud, n_ep = p133_auditorias_necessarias()
    print(f"P133 auditorias para medir eps com +-0.05 = {n_aud:.0f}; episodios necessarios = {n_ep:.0f}")
    for semente in (113, 114, 115):
        for versao in ("anima", "anima_x2", "lenta"):
            liq, carga, mud = p133_lenta(versao, semente)
            liq2, carga2, mud2 = p133_lenta(versao, semente, fadiga=0.15, fadiga_depois=0.6, episodios=6000)
            print(f"P133 semente {semente} {versao:8s}: estacionario = {liq:.3f} (carga {carga}, mudancas {mud}); "
                  f"humano muda 0.15->0.6 = {liq2:.3f} (carga {carga2}, mudancas {mud2})")
    for fad in (0.15, 0.6):
        varredura = {k[1]: round(v, 3) for k, v in p117_carga_alvo(sementes=(114,), fadiga=fad).items()}
        print(f"P133 carga-alvo otima com fadiga {fad} (semente 114): {varredura}")
    print(f"P134 fracao da associacao majoritaria (dados 60/40) = {p134_jo()}")
    uni, nat, tri = p135_trickster()
    print(f"P135 tentativas para achar 50 modos: uniforme = {uni:.0f}, Zipf natural = {nat:.0f}, trickster = {tri:.0f}")
    print(f"P136 arrependimento em 20000 passos = { {k: round(v) for k, v in p136_puer_senex().items()} }")
    print(f"P137 arrependimento (limiar, exposicao) = { {k: round(v) for k, v in p137_grande_mae().items()} }")
    sem, com = p138_mente_enviesada()
    print(f"P138 objetivo inferido errado: humano Boltzmann = {sem:.3f}, humano com vies de seguranca = {com:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=17, testes=30)
    print(f"P139 minha taxa de erro (17/30): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

    print("--- Parte 9 (o mundo decide o centro, complexo autonomo, transferencia, heroi, a regua do ruido) ---")
    n_pedido, n_memoria, razao = p143_continue()
    print(f"P143 pedido = {n_pedido} caracteres; memoria compartilhada (CLAUDE.md) = {n_memoria}; razao = {razao:.0f}x")
    centro = p144_centro_do_mundo()
    for p_cat in (0.0025, 0.005, 0.01):
        linha = {alvo: round(v, 3) for (pc, alvo), v in centro.items() if pc == p_cat}
        print(f"P144 taxa de catastrofe {p_cat}: liquido por carga-alvo = {linha}")
    antes, depois, w_antes, w_depois = p145_complexo_autonomo()
    print(f"P145 antes: log-perda = { {k: round(v, 4) for k, v in antes[0].items()} }, P media nas catastrofes = {antes[1]:.3f}")
    print(f"P145 depois de 2000 episodios aprendendo so com as proprias escolhas: log-perda = "
          f"{ {k: round(v, 4) for k, v in depois[0].items()} }, P media nas catastrofes = {depois[1]:.3f}")
    print(f"P145 pesos (intercepto, incerteza, nota) antes = {[round(x, 3) for x in w_antes]}, depois = {[round(x, 3) for x in w_depois]}")
    for semente in (145, 146, 147):
        for versao in ("propria", "nao", "ancorada"):
            liq, cat, p_cat_media, liq500 = p145_longo_prazo(versao, semente)
            print(f"P145 6000 episodios semente {semente} {versao:8s}: liquido(50) = {liq:.3f}, catastrofes = {cat:.4f}, "
                  f"P nas catastrofes = {p_cat_media:.3f}, liquido(500) = {liq500:.3f}")
    print(f"P146 (IA, humano) finais: humano so aprende = {p146_transferencia(eta=0.0)}, "
          f"transferencia mutua = {p146_transferencia()}, IA ancorada na verdade = {p146_transferencia(mu=0.05)}")
    print(f"P147 indice de Herfindahl da autoridade por numero de guardioes = {p147_mana()}")
    print(f"P148 consultas para a destilacao compensar = {p148_heroi():.0f}")
    print(f"P149 horizonte da imaginacao por erro do modelo = { {d: round(h, 2) for d, h in p149_imaginacao().items()} }")
    print(f"P150 (k otimo simulado, -1/ln(gamma) - 1) = { {g: (k, round(f, 2)) for g, (k, f) in p150_convergencia_instrumental().items()} }")
    print(f"P151 passos ate convergir: gradiente comum = {p151_gradiente_natural()[0]}, natural = {p151_gradiente_natural()[1]}")
    ruido = p152_ruido()
    print(f"P152 GISELE realista em 10 sementes novas: media = {ruido['base'][0]:.3f}, dp = {ruido['base'][1]:.3f}")
    for nome, (m, dp, tt) in ((k, v) for k, v in ruido.items() if k != "base"):
        rotulo = "carga 0.3 - carga 0.2" if nome == "carga" else "P* x2 - P* x1"
        print(f"P152 diferenca pareada {rotulo}: media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=21, testes=37)
    print(f"P153 minha taxa de erro (21/37): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

    print("=== Unificacao (sempre ao final) ===")
    k, pares = p96_crescimento()
    ok, total, falhas = testes_de_regressao()
    print(f"P96 funcoes pNN no arquivo = {k}; pares de interacao possiveis = {pares}")
    print("Linhagem do agente: Gisele (P83: comite, pessimismo, quantilizacao, calibracao, valor da pergunta, veto)"
          " -> GiseleJung (P112: integrar a sombra, compensacao/equilibrio da carga humana)"
          " -> GiseleAnima (P118: imagem fixa do humano) -> GiseleSelf (P125: auditar o auditor, homeostase da carga)"
          " -> GiseleLenta (P133: anima bayesiana, mudancas lentas so com intervalo fora da meta; P131: P* x2)"
          " -> GiseleAncorada (P145: sombra propria ancorada no historico auditado, contra o complexo de confianca)")
    print(f"Regressao: {ok}/{total} resultados publicados reproduzidos; falhas = {falhas}")
