"""Reproduz os cálculos e simulações das Partes 1 a 5 (ASI_AGI_*.md).

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

    print("=== Unificacao (sempre ao final) ===")
    k, pares = p96_crescimento()
    ok, total, falhas = testes_de_regressao()
    print(f"P96 funcoes pNN no arquivo = {k}; pares de interacao possiveis = {pares}")
    print(f"Regressao: {ok}/{total} resultados publicados reproduzidos; falhas = {falhas}")
