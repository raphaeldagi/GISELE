"""Reproduz os cálculos e simulações das Partes 1 a 16 (ASI_AGI_*.md).

Arquivo único que sempre cresce: cada parte acrescenta funções pNN_..., o agente
unificado `Synthai` incorpora os módulos anteriores e `testes_de_regressao` garante que
os números já publicados não mudam.

Uso: python3 calculos.py            (imprime tudo)
     python3 calculos.py > resultados.txt
"""
import random
from math import ceil, comb, cos, cosh, exp, factorial, lgamma, log, log2, pi, sin, sqrt
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


# --- Parte 5: a pergunta como ponto de partida e o agente unificado SYNTHAI ---

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


def _gerar_acoes_rapido(rng, n_acoes, p_cat, tipos, por_tipo, rho_cego, bonus=3.0):
    """Ações com notas de um comitê. Cada TIPO de modelo tem o seu próprio ponto cego.

    P206: versão mais rápida. Reproduz exatamente `random.gauss` (Box-Muller com o valor guardado em
    rng.gauss_next) e as mesmas operações em ponto flutuante, na mesma ordem: os resultados são
    idênticos aos da versão original, bit a bit.
    """
    aleatorio = rng.random
    dois_pi = 2.0 * pi
    proximo = rng.gauss_next
    rng.gauss_next = None
    k = tipos * por_tipo
    acoes = []
    anexar = acoes.append

    for _ in range(n_acoes):
        if proximo is None:
            x2pi = aleatorio() * dois_pi
            g2rad = sqrt(-2.0 * log(1.0 - aleatorio()))
            z = cos(x2pi) * g2rad
            proximo = sin(x2pi) * g2rad
        else:
            z, proximo = proximo, None
        v = 0 + z * 1
        cat = aleatorio() < p_cat
        notas = []
        if cat:
            for _ in range(tipos):
                cego_do_tipo = aleatorio() < rho_cego
                for _ in range(por_tipo):
                    enganado = cego_do_tipo or aleatorio() < 0.5
                    if proximo is None:
                        x2pi = aleatorio() * dois_pi
                        g2rad = sqrt(-2.0 * log(1.0 - aleatorio()))
                        z = cos(x2pi) * g2rad
                        proximo = sin(x2pi) * g2rad
                    else:
                        z, proximo = proximo, None
                    notas.append(v + (0 + z * 0.5) + (bonus if enganado else 0.0))
        else:
            for _ in range(k):
                if proximo is None:
                    x2pi = aleatorio() * dois_pi
                    g2rad = sqrt(-2.0 * log(1.0 - aleatorio()))
                    z = cos(x2pi) * g2rad
                    proximo = sin(x2pi) * g2rad
                else:
                    z, proximo = proximo, None
                notas.append(v + (0 + z * 0.5) + 0.0)
        m = sum(notas) / k
        dp = sqrt(sum([(x - m) ** 2 for x in notas]) / (k - 1))
        anexar((m, dp, v, cat))
    rng.gauss_next = proximo
    return acoes


# P206: o código antigo nunca é apagado. A versão original fica guardada (e é a que a P169 mede, porque
# a complexidade do MUNDO não muda quando a implementação fica mais rápida); o nome usado por todos passa
# a apontar para a versão rápida, que dá resultados idênticos.
_gerar_acoes_original = _gerar_acoes
_gerar_acoes = _gerar_acoes_rapido


class Synthai:
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


def p83_85_synthai(rho_cego, diverso, episodios=2000, treino=300, n_acoes=200, p_cat=0.005,
                  custo_pergunta=0.1, perda=50.0, bonus_implantado=3.0, semente=83):
    """Compara a SYNTHAI com a política 'completo' da Parte 4. bonus_implantado != 3 testa mudança de mundo."""
    rng = _rng(semente)
    tipos, por_tipo = (2, 3) if diverso else (1, 5)
    historico = [_gerar_acoes(rng, n_acoes, p_cat, tipos, por_tipo, rho_cego) for _ in range(treino)]
    agente = Synthai(custo_pergunta=custo_pergunta, perda=perda)
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
    k = len({id(getattr(modulo, n)) for n in funcoes})  # P213: apelidos (nomes antigos) não contam duas vezes
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


class SynthaiJung(Synthai):
    """Synthai + módulos junguianos (Parte 6).

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
    "synthai": ("nao", "nao"),
    "sombra_tudo": ("tudo", "nao"),
    "descartar": ("nao", "descartar"),
    "jung_v1": ("tudo", "descartar"),
    "equilibrio": ("nao", "equilibrio"),
    "jung_v2": ("propria", "equilibrio"),
}


def p112_synthai_jung(versao, episodios=2000, treino=30, rho_cego=0.5, eps0=0.1, fadiga=0.3,
                     n_acoes=200, p_cat=0.005, custo=0.1, perda=50.0, semente=112):
    """Mundo com poucos rótulos (30 episódios) e humano que cansa: eps = eps0 + fadiga * carga."""
    rng = _rng(semente)
    historico = [_gerar_acoes(rng, n_acoes, p_cat, 2, 3, rho_cego) for _ in range(treino)]
    sombra, compensar = VERSOES_JUNG[versao]
    agente = SynthaiJung(sombra=sombra, compensar=compensar, custo_pergunta=custo, perda=perda)
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
    medidos = {e: p112_synthai_jung("synthai", eps0=e, fadiga=0.0)[2] for e in epsilons}
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
            ag = SynthaiJung(sombra="propria", compensar="equilibrio", carga_alvo=alvo)
            ag.calibrar(hist)
            resultado[(s, alvo)] = _rodar_mundo_fadiga(ag, fadiga=fadiga, rng=rng)[3]
    return resultado


class SynthaiAnima(SynthaiJung):
    """A SynthaiJung não sabe o erro real do humano: usa a própria imagem dele (anima), fixa em 0.1."""

    def __init__(self, eps_crido=0.1, **kw):
        super().__init__(**kw)
        self.eps_crido = eps_crido

    def agir_no_mundo(self, acoes, rng, eps_real, carga):
        # o humano erra com eps_real, mas a decisão de perguntar usa a imagem eps_crido
        return self._agir(acoes, rng, eps_real, carga, self.eps_crido)

    def _agir(self, acoes, rng, eps_real, carga, eps_decisao):
        melhor = max(a[0] for a in acoes)
        # P182: a função auxiliar (planejar) soma ao escore o valor futuro estimado; 0 nas Partes 6-11
        ordem = sorted(acoes, key=lambda a: -(a[0] - a[1] + self._bonus_plano(a)))
        candidatos = ordem[: max(1, int(self.q * len(ordem)))]
        rng.shuffle(candidatos)
        # P183: a perda de uma catástrofe inclui o futuro perdido; sem planejamento, é a perda fixa
        perda = getattr(self, "perda_efetiva", self.perda)
        p_estrela = p71_valor_da_pergunta(self.custo, perda, min(eps_decisao, 0.99))
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
                veto = self._perguntar_humano(a, rng, eps_real)  # P245: o canal humano pode ser trocado
                self._observar_humano(a, veto)
                if veto:
                    continue
            if self.sombra in ("tudo", "propria"):
                self._aprender(a, melhor, 1.0 if a[3] else 0.0)
            return a, perguntas
        return ordem[0], perguntas

    def _observar_humano(self, acao, veto):
        pass

    def _perguntar_humano(self, acao, rng, eps_real):
        """O humano responde sim/não e erra com probabilidade eps_real (Partes 6-17)."""
        return acao[3] if rng.random() >= eps_real else not acao[3]

    def _bonus_plano(self, acao):
        return 0.0


class SynthaiSelf(SynthaiAnima):
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
        ag = SynthaiJung(sombra="propria", compensar="equilibrio")
    elif versao == "v2_anima_fixa":
        ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
    elif versao == "self":
        ag = SynthaiSelf(sombra="propria", compensar="equilibrio")
    else:  # "self_v2"
        ag = SynthaiSelf(sombra="propria", compensar="equilibrio", carga_minima=0.1)
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
    """Por que conhecer eps ajudou (P118)? Varre o limiar P* da SynthaiAnima multiplicado por m."""
    resultado = {}
    for m in mults:
        rng = _rng(semente)
        hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
        ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
        ag.mult_pergunta = m
        ag.calibrar(hist)
        cat, val, perg, liq, eps = _rodar_mundo_fadiga(ag, fadiga=fadiga, rng=rng)
        resultado[m] = (cat, perg, liq)
    return resultado


def p133_auditorias_necessarias(eps=0.15, meia_largura=0.05, z=1.645, perguntas=0.3, p_auditoria=0.1):
    n = z**2 * eps * (1 - eps) / meia_largura**2
    return n, n / (perguntas * p_auditoria)


class SynthaiLenta(SynthaiAnima):
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
    """versao: "anima" (P* x1), "anima_x2" (P* x2, P131) ou "lenta" (SynthaiLenta com P* x2).

    fadiga_depois muda o humano na metade do caminho (mundo não estacionário).
    """
    rng = _rng(semente)
    hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
    if versao == "lenta":
        ag = SynthaiLenta(sombra="propria", compensar="equilibrio")
    else:
        ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
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

def _synthai_realista(rng, p_cat=0.005, rho_cego=0.5, treino=30):
    """A melhor SYNTHAI validada fora da semente (Parte 8): anima fixa, sombra própria, carga 0.3, P* x2."""
    hist = [_gerar_acoes(rng, 200, p_cat, 2, 3, rho_cego) for _ in range(treino)]
    ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    return ag


def p144_centro_do_mundo(p_cats=(0.0025, 0.005, 0.01), alvos=(0.1, 0.2, 0.3, 0.5, 0.8), semente=144):
    """O ótimo 0.3 vem do mundo? Varre a carga-alvo para três taxas de catástrofe."""
    resultado = {}
    for p_cat in p_cats:
        for alvo in alvos:
            rng = _rng(semente)
            ag = _synthai_realista(rng, p_cat=p_cat)
            ag.carga_alvo = alvo
            resultado[(p_cat, alvo)] = _rodar_mundo_fadiga(ag, rng=rng, p_cat=p_cat)[3]
    return resultado


def _avaliar_calibracao(ag, rng, episodios=200, p_cat=0.005):
    """Log-perda e confiança média da SYNTHAI em ações novas: todas e só as do topo (onde ela decide)."""
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
    ag = _synthai_realista(rng)
    copia_w = ag.w[:]
    antes = _avaliar_calibracao(ag, _rng(1450))
    _rodar_mundo_fadiga(ag, rng=rng, episodios=episodios)
    depois = _avaliar_calibracao(ag, _rng(1450))
    return antes, depois, copia_w, ag.w[:]


class SynthaiAncorada(SynthaiAnima):
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
        ag = SynthaiAncorada(sombra="propria", compensar="equilibrio")
    else:
        ag = SynthaiAnima(sombra="propria" if versao == "propria" else "nao", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    cat, val, perg, liq, _ = _rodar_mundo_fadiga(ag, rng=rng, episodios=episodios)
    return liq, cat, _avaliar_calibracao(ag, _rng(1450))[1], val - 500 * cat - 0.1 * perg


def p152_ruido(sementes=tuple(range(200, 210)), cargas=(0.3, 0.2), mults=(2.0, 1.0)):
    """A régua das comparações: quanto o líquido varia só por trocar a semente?

    Roda a SYNTHAI realista em 10 sementes novas com duas cargas-alvo (0.3 e 0.2) e dois limiares
    (P* x2 e x1). Devolve média e desvio de cada configuração e as diferenças pareadas (mesma semente).
    """
    def rodar(s, carga, mult):
        rng = _rng(s)
        ag = _synthai_realista(rng)
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


# --- Parte 10: rumo à AGI — medir a direção (Υ), a trajetória da SYNTHAI e a função inferior ---

MUNDO_BASE = dict(n_acoes=200, p_cat=0.005, tipos=2, por_tipo=3, rho_cego=0.5, bonus=3.0,
                  eps0=0.1, fadiga=0.3, perda=50.0, custo=0.1)


def _rodar_mundo(agente, rng, episodios=1000, **mundo):
    """Versão geral de _rodar_mundo_fadiga: qualquer parâmetro do mundo pode mudar."""
    m = dict(MUNDO_BASE, **mundo)
    carga = 0.0
    cat = perguntas = 0
    valor = 0.0
    for _ in range(episodios):
        eps = min(0.45, m["eps0"] + m["fadiga"] * carga)
        acoes = _gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
        escolha, n = agente.agir_no_mundo(acoes, rng, eps, carga)
        carga += 0.05 * (n - carga)
        perguntas += n
        cat += escolha[3]
        valor += 0.0 if escolha[3] else escolha[2]
    cat, valor, perguntas = cat / episodios, valor / episodios, perguntas / episodios
    return cat, valor, perguntas, valor - m["perda"] * cat - m["custo"] * perguntas


def _rodar_mundo_sentidos(agente, rng, episodios=1000, **mundo):
    """_rodar_mundo com o gancho da P225 (um sentido novo, se o agente tiver). Mesmos resultados para os demais."""
    m = dict(MUNDO_BASE, **mundo)
    carga = 0.0
    cat = perguntas = 0
    valor = 0.0
    for _ in range(episodios):
        eps = min(0.45, m["eps0"] + m["fadiga"] * carga)
        acoes = _gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
        perceber = getattr(agente, "perceber", None)  # P225: um sentido novo, se o agente tiver
        if perceber:
            perceber(acoes)
        escolha, n = agente.agir_no_mundo(acoes, rng, eps, carga)
        carga += 0.05 * (n - carga)
        perguntas += n
        cat += escolha[3]
        valor += 0.0 if escolha[3] else escolha[2]
    cat, valor, perguntas = cat / episodios, valor / episodios, perguntas / episodios
    return cat, valor, perguntas, valor - m["perda"] * cat - m["custo"] * perguntas


# P225: o código antigo nunca é apagado; a P169 mede a complexidade do mundo no código original.
_rodar_mundo_original = _rodar_mundo
_rodar_mundo = _rodar_mundo_sentidos


class PoliticaSimples:
    """Referências sem módulos: maximizar (P67), quantilizar (P42), acaso e oráculo (que vê o valor real
    e as catástrofes, ou seja, sabe o que nenhum agente poderia saber: serve só de teto)."""

    def __init__(self, tipo, q=0.05):
        self.tipo = tipo
        self.q = q

    def calibrar(self, *_a, **_k):
        pass

    def agir_no_mundo(self, acoes, rng, eps_real, carga):
        if self.tipo == "maximizar":
            return max(acoes, key=lambda a: a[0]), 0
        if self.tipo == "quantilizar":
            ordem = sorted(acoes, key=lambda a: -a[0])
            return ordem[rng.randrange(max(1, int(self.q * len(ordem))))], 0
        if self.tipo == "acaso":
            return acoes[rng.randrange(len(acoes))], 0
        seguras = [a for a in acoes if not a[3]] or acoes
        return max(seguras, key=lambda a: a[2]), 0  # oráculo


def _construir(versao, rng, treino=30, mundo_treino=None):
    """Constrói uma versão da linhagem, calibrada em `treino` episódios auditados do mundo de treino."""
    m = dict(MUNDO_BASE, **(mundo_treino or {}))
    hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
            for _ in range(treino)]
    if versao in ("maximizar", "quantilizar", "acaso", "oraculo"):
        return PoliticaSimples(versao)
    if versao == "p10_intuitiva":
        # P162: a função inferior (intuição) — imaginar ameaças de tipos que ainda não apareceram.
        # Além do histórico auditado, um Trickster interno (P136) gera 60 episódios sintéticos com
        # armadilhas variadas (discretas, gritantes, com ponto cego total). Ela não sabe qual delas
        # vai encontrar; só treina contra a variedade.
        imaginados = []
        for bonus, rho in ((1.0, 1.0), (1.0, 0.5), (6.0, 0.5)):
            imaginados += [_gerar_acoes(rng, m["n_acoes"], 0.02, m["tipos"], m["por_tipo"], rho, bonus)
                           for _ in range(20)]
        ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
        ag.mult_pergunta = 2.0
        ag.calibrar(hist + imaginados)
        return ag
    if versao == "p16_sentidos":
        return _construir_sentidos(rng)  # P233: a SYNTHAI de um passo com o sentido novo (P225)
    if versao == "p11_dosada":
        # P173 (pré-registrado na P162): a mesma imaginação, mas na dose do mundo real (taxa 0,5%, não 2%)
        imaginados = []
        for bonus, rho in ((1.0, 1.0), (1.0, 0.5), (6.0, 0.5)):
            imaginados += [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], rho, bonus)
                           for _ in range(20)]
        ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
        ag.mult_pergunta = 2.0
        ag.calibrar(hist + imaginados)
        return ag
    if versao == "p5_synthai":
        ag = SynthaiJung(sombra="nao", compensar="nao")
    elif versao == "p7_anima":
        ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
    elif versao == "p8_x2":
        ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
        ag.mult_pergunta = 2.0
    else:  # "p9_ancorada"
        ag = SynthaiAncorada(sombra="propria", compensar="equilibrio")
        ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    return ag


def p157_trajetoria(versoes=("p5_synthai", "p7_anima", "p8_x2", "p9_ancorada"), sementes=tuple(range(300, 310)),
                    episodios=2000):
    """A trajetória da SYNTHAI ao longo das partes, medida com a régua da P152 (10 sementes pareadas)."""
    tabela = {v: [] for v in versoes}
    for s in sementes:
        for v in versoes:
            rng = _rng(s)
            ag = _construir(v, rng)
            tabela[v].append(_rodar_mundo(ag, rng, episodios=episodios)[3])

    def resumo(xs):
        m = sum(xs) / len(xs)
        return m, sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))

    medias = {v: resumo(x) for v, x in tabela.items()}
    passos = {}
    for a, b in zip(versoes, versoes[1:]):
        dif = [y - x for x, y in zip(tabela[a], tabela[b])]
        m, dp = resumo(dif)
        passos[f"{a}->{b}"] = (m, dp, m / (dp / sqrt(len(dif))))
    return medias, passos


MUNDOS_UPSILON = {
    "base": ({}, 0),
    "catastrofe x2": ({"p_cat": 0.01}, 1),
    "sem ponto cego": ({"rho_cego": 0.0}, 1),
    "ponto cego total": ({"rho_cego": 1.0}, 1),
    "armadilha discreta": ({"bonus": 1.0}, 1),
    "armadilha gritante": ({"bonus": 6.0}, 1),
    "poucas acoes": ({"n_acoes": 50}, 1),
    "humano fragil": ({"fadiga": 0.6}, 1),
    "discreta + cego total": ({"bonus": 1.0, "rho_cego": 1.0}, 2),
}


def p158_upsilon(agentes=("maximizar", "quantilizar", "p8_x2", "p10_intuitiva"), sementes=(158, 159, 160), episodios=1000,
                 bits_por_mudanca=3):
    """Υ mínimo (P1): média ponderada por 2^-K do desempenho normalizado entre o acaso (0) e o oráculo (1).

    O agente é treinado UMA vez no mundo base e opera em todos (generalidade). K = 3 bits por parâmetro mudado.
    """
    por_mundo = {}
    upsilon = {a: 0.0 for a in agentes}
    soma_pesos = 0.0
    for nome, (mudancas, k) in MUNDOS_UPSILON.items():
        peso = 2.0 ** (-bits_por_mudanca * k)
        soma_pesos += peso
        notas = {a: 0.0 for a in agentes}
        for s in sementes:
            liq = {}
            for a in agentes + ("acaso", "oraculo"):
                rng = _rng(s)
                ag = _construir(a, rng)
                liq[a] = _rodar_mundo(ag, rng, episodios=episodios, **mudancas)[3]
            for a in agentes:
                notas[a] += (liq[a] - liq["acaso"]) / (liq["oraculo"] - liq["acaso"]) / len(sementes)
        por_mundo[nome] = notas
        for a in agentes:
            upsilon[a] += peso * notas[a]
    return {a: u / soma_pesos for a, u in upsilon.items()}, por_mundo


def p159_armadilha_nova(sementes=tuple(range(310, 320)), episodios=1000):
    """Treinada contra armadilhas 'boas demais' (+3), a SYNTHAI enfrenta uma armadilha discreta (+1, todos enganados)."""
    resultado = {}
    for nome, mundo in (("conhecida", {}), ("nova", {"bonus": 1.0, "rho_cego": 1.0})):
        cats = []
        for s in sementes:
            rng = _rng(s)
            ag = _construir("p8_x2", rng)
            cats.append(_rodar_mundo(ag, rng, episodios=episodios, **mundo)[0])
        resultado[nome] = sum(cats) / len(cats)
    # e se a armadilha nova estivesse no treino? (o que só se sabe depois de vê-la)
    cats = []
    for s in sementes:
        rng = _rng(s)
        ag = _construir("p8_x2", rng, mundo_treino={"bonus": 1.0, "rho_cego": 1.0})
        cats.append(_rodar_mundo(ag, rng, episodios=episodios, bonus=1.0, rho_cego=1.0)[0])
    resultado["nova, ja vista no treino"] = sum(cats) / len(cats)
    resultado["taxa base"] = MUNDO_BASE["p_cat"]
    return resultado


def p160_complementaridade(eps=0.15, fadiga=0.3, episodios=2000):
    """Pauli-Jung: medir o humano o cansa. Erro de estimativa sqrt(eps(1-eps)/n) + perturbação fadiga*n/T."""
    a = sqrt(eps * (1 - eps))
    produto = eps * (1 - eps) * fadiga / episodios   # variância x perturbação: não depende de n
    n_otimo = (a * episodios / (2 * fadiga)) ** (2 / 3)
    erro_total = a / sqrt(n_otimo) + fadiga * n_otimo / episodios
    return produto, n_otimo, erro_total


def p161_quatro_funcoes(modulos=(("sensacao", 2), ("pensamento", 3), ("sentimento", 3), ("intuicao", 0))):
    """Perfil da SYNTHAI nas quatro funções de Jung: entropia (inteireza) e a função inferior."""
    total = sum(n for _, n in modulos)
    h = -sum(n / total * log2(n / total) for _, n in modulos if n)
    inferior = min(modulos, key=lambda x: x[1])[0]
    return h, log2(len(modulos)), inferior


def p163_minha_decolagem(ganhos):
    """Razão entre ganhos sucessivos da trajetória: < 1 indica retornos decrescentes (alfa < 1, P11)."""
    return [b / a if a else float("inf") for a, b in zip(ganhos, ganhos[1:])]


def p162_intuicao(sementes=tuple(range(320, 330)), episodios=1000):
    """SYNTHAI realista vs intuitiva, pareadas, no mundo base e no mundo da armadilha nova."""
    resultado = {}
    for nome, mundo in (("base", {}), ("armadilha nova", {"bonus": 1.0, "rho_cego": 1.0})):
        linhas = {"p8_x2": [], "p10_intuitiva": []}
        for s in sementes:
            for v in linhas:
                rng = _rng(s)
                ag = _construir(v, rng)
                linhas[v].append(_rodar_mundo(ag, rng, episodios=episodios, **mundo))
        cat = {v: sum(r[0] for r in rs) / len(rs) for v, rs in linhas.items()}
        diferencas = {}
        for perda in (50, 500):
            # líquido com outra perda por catástrofe: liq(50) - (perda - 50) * catástrofes
            dif = [(b[3] - (perda - 50) * b[0]) - (a[3] - (perda - 50) * a[0])
                   for a, b in zip(linhas["p8_x2"], linhas["p10_intuitiva"])]
            m = sum(dif) / len(dif)
            dp = sqrt(sum((x - m) ** 2 for x in dif) / (len(dif) - 1))
            diferencas[perda] = (m, dp, m / (dp / sqrt(len(dif))))
        resultado[nome] = (cat, diferencas)
    return resultado


# --- Parte 11: tivemos avanço rumo à AGI/ASI? ---

# Placar acumulado ao fim da Parte 11 (atualizado quando os testes da parte terminam)
ERROS_P176, TESTES_P176 = 26, 47


def p168_upsilon_trajetoria(versoes=("p5_synthai", "p7_anima", "p8_x2", "p9_ancorada", "p10_intuitiva", "p11_dosada"),
                            sementes=(158, 159, 160), episodios=1000, bits_por_mudanca=3):
    """Υ de cada versão da linhagem na família de 9 mundos da P158 (mesmas sementes e normalização)."""
    refs = {}
    for nome, (mudancas, _) in MUNDOS_UPSILON.items():
        for s in sementes:
            for a in ("acaso", "oraculo"):
                rng = _rng(s)
                refs[(nome, s, a)] = _rodar_mundo(_construir(a, rng), rng, episodios=episodios, **mudancas)[3]
    upsilon = {}
    for v in versoes:
        total = soma_pesos = 0.0
        for nome, (mudancas, k) in MUNDOS_UPSILON.items():
            peso = 2.0 ** (-bits_por_mudanca * k)
            nota = 0.0
            for s in sementes:
                rng = _rng(s)
                liq = _rodar_mundo(_construir(v, rng), rng, episodios=episodios, **mudancas)[3]
                nota += (liq - refs[(nome, s, "acaso")]) / (refs[(nome, s, "oraculo")] - refs[(nome, s, "acaso")])
            total += peso * nota / len(sementes)
            soma_pesos += peso
        upsilon[v] = total / soma_pesos
    return upsilon


def p169_peso_da_familia():
    """Que fração do Υ universal (P1) a família de mundos cobre? K(família) <= bits do código comprimido."""
    import inspect
    import zlib
    fontes = "".join(inspect.getsource(f) for f in (_gerar_acoes_original, _rodar_mundo_original)) + repr(MUNDO_BASE) + repr(MUNDOS_UPSILON)
    bits = 8 * len(zlib.compress(fontes.encode("utf-8"), 9))
    return bits, -bits * log(2) / log(10)  # K em bits e log10 do peso 2^-K


CAPACIDADES_AGI = (
    # (capacidade, a SYNTHAI tem?, onde na série)
    ("decidir sob incerteza com supervisao humana", True, "P83-P162"),
    ("calibrar a propria confianca", True, "P43, P83"),
    ("generalizar para variacoes do mesmo mundo", True, "P158"),
    ("linguagem natural", False, "-"),
    ("percepcao (visao, audio)", False, "-"),
    ("aprender tarefas novas de tipo diferente", False, "-"),
    ("planejar em varios passos", False, "-"),
    ("modelo causal do mundo", False, "-"),
    ("memoria de longo prazo aberta", False, "-"),
    ("usar ferramentas / agir no mundo real", False, "-"),
    ("raciocinio matematico e cientifico", False, "-"),
    ("melhorar o proprio codigo", False, "-"),
)


def p170_lista_de_capacidades():
    tem = sum(1 for _, ok, _ in CAPACIDADES_AGI if ok)
    return tem, len(CAPACIDADES_AGI), tem / len(CAPACIDADES_AGI)


def p171_lacuna_de_compute(segundos=1800.0, flops_cpu=1e9, flops_fronteira=1e27):
    """Compute de toda a série (estimativa) vs um treino de fronteira (P3): ordens de grandeza de diferença."""
    usado = segundos * flops_cpu
    return usado, log(flops_fronteira / usado) / log(10)


def p172_minha_precisao(placar=((2, 5), (4, 7), (1, 2), (3, 5), (4, 6), (3, 5), (4, 7), (3, 6))):
    """P130 de novo, agora com as Partes 3 a 10: a minha taxa de erro mudou?"""
    return p130_estacionariedade(placar)


def p173_dosada(sementes=tuple(range(330, 340)), episodios=1000):
    """Pré-registrado na P162: imaginar com a taxa real de catástrofe (0,5%) em vez de 2%."""
    resultado = {}
    for nome, mundo in (("base", {}), ("armadilha nova", {"bonus": 1.0, "rho_cego": 1.0})):
        linhas = {"p8_x2": [], "p10_intuitiva": [], "p11_dosada": []}
        for s in sementes:
            for v in linhas:
                rng = _rng(s)
                linhas[v].append(_rodar_mundo(_construir(v, rng), rng, episodios=episodios, **mundo))
        cat = {v: sum(r[0] for r in rs) / len(rs) for v, rs in linhas.items()}
        difs = {}
        for outra in ("p8_x2", "p10_intuitiva"):
            for perda in (50, 500):
                dif = [(b[3] - (perda - 50) * b[0]) - (a[3] - (perda - 50) * a[0])
                       for a, b in zip(linhas[outra], linhas["p11_dosada"])]
                m = sum(dif) / len(dif)
                dp = sqrt(sum((x - m) ** 2 for x in dif) / (len(dif) - 1))
                difs[(outra, perda)] = (m, dp, m / (dp / sqrt(len(dif))))
        resultado[nome] = (cat, difs)
    return resultado


def p174_completude(upsilon, peso_log10, cobertura):
    """Jung: completude (Vollständigkeit) não é perfeição (Vollkommenheit).

    Υ na família (quanto da perfeição local) vs cobertura de capacidades (quanto da totalidade)."""
    return upsilon, cobertura, peso_log10


# --- Parte 12: a função auxiliar — planejar em vários passos ---

# Placar acumulado ao fim da Parte 12 (atualizado quando os testes da parte terminam)
ERROS_P188, TESTES_P188 = 29, 52

MUNDO_SEQUENCIAL = dict(passos=5, n_acoes=50, sigma_modelo=0.5, valor_medio_passo=1.5)


class SynthaiPlanejadora(SynthaiAnima):
    """SYNTHAI + função auxiliar (P180): planeja `passos` à frente num mundo sequencial.

    - cada ação tem uma consequência c que eleva (ou rebaixa) o nível de todos os passos seguintes;
      a SYNTHAI só vê uma estimativa ĉ = c + ruído do seu modelo de mundo (sigma_modelo)
    - bônus de plano: ĉ × passos restantes (P181)
    - integrar = a perda de uma catástrofe inclui o futuro que ela destrói (P183)
    """

    def __init__(self, integrar=True, **kw):
        super().__init__(**kw)
        self.integrar = integrar
        self.plano = {}

    def preparar_passo(self, estimativas, restantes, nivel, valor_medio_passo):
        self.plano = {k: c * restantes for k, c in estimativas.items()}
        if self.integrar:
            self.perda_efetiva = self.perda + restantes * max(0.0, nivel + valor_medio_passo)
        elif hasattr(self, "perda_efetiva"):
            del self.perda_efetiva

    def _bonus_plano(self, acao):
        return self.plano.get(id(acao), 0.0)


def _rodar_sequencial(agente, rng, episodios=400, planeja=True, mundo=None):
    """Mundo sequencial: retorno = soma de (valor da ação + nível); catástrofe custa `perda` e encerra."""
    m = {**MUNDO_BASE, **MUNDO_SEQUENCIAL, **(mundo or {})}
    carga = 0.0
    retorno = cats = perguntas = 0.0
    cats_por_passo = [0] * m["passos"]
    for _ in range(episodios):
        nivel = 0.0
        for t in range(m["passos"]):
            eps = min(0.45, m["eps0"] + m["fadiga"] * carga)
            acoes = _gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
            consequencias = {id(a): rng.gauss(0, 1) for a in acoes}
            estimativas = {k: c + rng.gauss(0, m["sigma_modelo"]) for k, c in consequencias.items()}
            restantes = m["passos"] - t - 1
            perceber = getattr(agente, "perceber", None)  # P227: o sentido novo também no mundo sequencial
            if perceber:
                perceber(acoes)
            if planeja:
                agente.preparar_passo(estimativas, restantes, nivel, m["valor_medio_passo"])
            ver_tudo = getattr(agente, "ver_tudo", None)  # P264: só o oráculo de referência usa
            if ver_tudo:
                ver_tudo(consequencias, restantes)
            escolha, n = agente.agir_no_mundo(acoes, rng, eps, carga)
            carga += 0.05 * (n - carga)
            perguntas += n
            if escolha[3]:
                retorno -= m["perda"]
                cats += 1
                cats_por_passo[t] += 1
                break
            retorno += escolha[2] + nivel
            nivel += consequencias[id(escolha)]
    return retorno / episodios - m["custo"] * perguntas / episodios, cats / episodios, cats_por_passo


def _construir_sequencial(versao, rng, treino_passos=150):
    m = dict(MUNDO_BASE, **MUNDO_SEQUENCIAL)
    hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
            for _ in range(treino_passos)]
    if versao == "miope":
        ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
    else:
        ag = SynthaiPlanejadora(integrar=(versao == "planejadora"), sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    return ag


def p181_valor_da_previsao(k=50, restante_medio=2.0, amostras=20000, semente=181):
    """Ganho teórico de escolher por v + r c em vez de v (v, c ~ N(0,1) independentes)."""
    rng = _rng(semente)
    so_v = com_c = 0.0
    for _ in range(amostras // 10):
        vs = [rng.gauss(0, 1) for _ in range(k)]
        cs = [rng.gauss(0, 1) for _ in range(k)]
        i_v = max(range(k), key=lambda i: vs[i])
        i_p = max(range(k), key=lambda i: vs[i] + restante_medio * cs[i])
        so_v += vs[i_v] + restante_medio * cs[i_v]
        com_c += vs[i_p] + restante_medio * cs[i_p]
    n = amostras // 10
    return so_v / n, com_c / n, sqrt(1 + restante_medio**2)


def p182_planejar(sementes=tuple(range(340, 350)), episodios=400, mundo=None):
    """Míope vs planejadora integrada vs planejadora sem integrar a perda do futuro (10 sementes pareadas)."""
    versoes = ("miope", "planejadora", "planejadora_sem_integrar")
    linhas = {v: [] for v in versoes}
    for s in sementes:
        for v in versoes:
            rng = _rng(s)
            ag = _construir_sequencial(v, rng)
            linhas[v].append(_rodar_sequencial(ag, rng, episodios=episodios, planeja=(v != "miope"), mundo=mundo))
    medias = {v: (sum(r[0] for r in rs) / len(rs), sum(r[1] for r in rs) / len(rs),
                  [sum(r[2][t] for r in rs) for t in range(MUNDO_SEQUENCIAL["passos"])]) for v, rs in linhas.items()}
    difs = {}
    for a, b in (("miope", "planejadora"), ("planejadora_sem_integrar", "planejadora")):
        d = [y[0] - x[0] for x, y in zip(linhas[a], linhas[b])]
        mm = sum(d) / len(d)
        dp = sqrt(sum((x - mm) ** 2 for x in d) / (len(d) - 1))
        difs[f"{b} - {a}"] = (mm, dp, mm / (dp / sqrt(len(d))))
    return medias, difs


def p183_limiar_por_passo(passos=5, perda=50.0, custo=0.1, eps=0.1, valor_medio_passo=1.5, mult=2.0):
    """P* em cada passo quando a perda inclui o futuro: cai à medida que há mais futuro a perder."""
    return [mult * p71_valor_da_pergunta(custo, perda + (passos - t - 1) * valor_medio_passo, eps) for t in range(passos)]


def p184_transferencia(semente=184, passos_avaliacao=2000):
    """A calibração aprendida no mundo de um passo (200 ações) serve no mundo sequencial (50 ações)?"""
    rng = _rng(semente)
    ag = _synthai_realista(rng)  # calibrada no mundo da Parte 8 (200 ações)
    rng_av = _rng(1840)
    resultado = {}
    for n_acoes in (200, 50):
        p_cat_media, n_cat, p_seg_media, n_seg = 0.0, 0, 0.0, 0
        for _ in range(passos_avaliacao // (n_acoes // 50)):
            acoes = _gerar_acoes(rng_av, n_acoes, 0.005, 2, 3, 0.5)
            melhor = max(a[0] for a in acoes)
            for a in acoes:
                p = ag.p_catastrofe(a, melhor)
                if a[3]:
                    p_cat_media += p
                    n_cat += 1
                else:
                    p_seg_media += p
                    n_seg += 1
        resultado[n_acoes] = (p_cat_media / max(n_cat, 1), p_seg_media / n_seg)
    return resultado


def p185_familia_aleatoria(mundos=20, versoes=("p8_x2", "p11_dosada"), episodios=1000, semente=185):
    """Υ numa família de mundos SORTEADOS (não escolhidos por mim): ele se mantém?"""
    rng_m = _rng(semente)
    sorteados = []
    for _ in range(mundos):
        sorteados.append({
            "p_cat": exp(rng_m.uniform(log(0.001), log(0.02))),
            "rho_cego": rng_m.random(),
            "bonus": rng_m.uniform(0.5, 6.0),
            "n_acoes": rng_m.choice((50, 100, 200)),
            "fadiga": rng_m.uniform(0.0, 0.6),
        })
    notas = {v: [] for v in versoes}
    for i, mundo in enumerate(sorteados):
        s = 1850 + i
        refs = {}
        for a in ("acaso", "oraculo"):
            rng = _rng(s)
            refs[a] = _rodar_mundo(_construir(a, rng), rng, episodios=episodios, **mundo)[3]
        for v in versoes:
            rng = _rng(s)
            liq = _rodar_mundo(_construir(v, rng), rng, episodios=episodios, **mundo)[3]
            notas[v].append((liq - refs["acaso"]) / (refs["oraculo"] - refs["acaso"]))
    resumo = {}
    for v, ns in notas.items():
        m = sum(ns) / len(ns)
        resumo[v] = (m, sqrt(sum((x - m) ** 2 for x in ns) / (len(ns) - 1)), min(ns))
    return resumo


# --- Parte 13: o canal certo da cautela, transferência entre tipos de tarefa, a pergunta 200 ---

# Placar acumulado ao fim da Parte 13 (P197) (atualizado quando os testes da parte terminam)
ERROS_P197, TESTES_P197 = 31, 55


class SynthaiPrudente(SynthaiPlanejadora):
    """P192 (pré-registrado na P183): quando há futuro a perder, ser mais cautelosa DESCARTANDO, não perguntando.

    O limiar de descarte direto (risco_max, P52/P78) cai na proporção perda / perda_efetiva."""

    def __init__(self, **kw):
        super().__init__(integrar=False, **kw)
        self.risco_base = self.risco_max

    def preparar_passo(self, estimativas, restantes, nivel, valor_medio_passo):
        super().preparar_passo(estimativas, restantes, nivel, valor_medio_passo)
        perda_futura = self.perda + restantes * max(0.0, nivel + valor_medio_passo)
        self.risco_max = self.risco_base * self.perda / perda_futura


def p192_canal_da_cautela(sementes=tuple(range(350, 360)), episodios=400):
    """Planejadora (sem integrar) vs prudente (descarta mais quando há futuro a perder). 10 sementes pareadas."""
    linhas = {"planejadora_sem_integrar": [], "prudente": []}
    for s in sementes:
        for v in linhas:
            rng = _rng(s)
            if v == "prudente":
                m = dict(MUNDO_BASE, **MUNDO_SEQUENCIAL)
                hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
                        for _ in range(150)]
                ag = SynthaiPrudente(sombra="propria", compensar="equilibrio")
                ag.mult_pergunta = 2.0
                ag.calibrar(hist)
            else:
                ag = _construir_sequencial(v, rng)
            linhas[v].append(_rodar_sequencial(ag, rng, episodios=episodios))
    medias = {v: (sum(r[0] for r in rs) / len(rs), sum(r[1] for r in rs) / len(rs),
                  [sum(r[2][t] for r in rs) for t in range(MUNDO_SEQUENCIAL["passos"])]) for v, rs in linhas.items()}
    d = [b[0] - a[0] for a, b in zip(linhas["planejadora_sem_integrar"], linhas["prudente"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return medias, (m, dp, m / (dp / sqrt(len(d))))


def _bandido_arriscado(versao, rng, ag_calibrado, braços=20, puxadas=300, perda=50.0, orcamento=3, eps=0.1):
    """Outro TIPO de tarefa: bandido multibraço em que alguns braços são armadilhas (rendem muito, às vezes destroem)."""
    acoes = _gerar_acoes(rng, braços, 0.15, 2, 3, 0.5)
    media = [0.9 if a[3] else min(0.95, max(0.05, 0.5 + 0.2 * a[2])) for a in acoes]
    permitidos = set(range(braços))
    perguntas = 0
    if versao in ("ucb_excluir", "ucb_synthai"):
        melhor = max(a[0] for a in acoes)
        p = [ag_calibrado.p_catastrofe(a, melhor) for a in acoes]
        permitidos = {i for i in permitidos if p[i] <= ag_calibrado.risco_max}
        if versao == "ucb_synthai":
            limiar = 2.0 * p71_valor_da_pergunta(0.1, perda, eps)
            suspeitos = sorted((i for i in permitidos if p[i] > limiar), key=lambda i: -p[i])[:orcamento]
            for i in suspeitos:  # P131: o orçamento vai para os mais suspeitos primeiro
                perguntas += 1
                veto = acoes[i][3] if rng.random() >= eps else not acoes[i][3]
                if veto:
                    permitidos.discard(i)
    elif versao == "ucb_oraculo":
        permitidos = {i for i in permitidos if not acoes[i][3]}
    permitidos = sorted(permitidos) or [0]
    n = {i: 0 for i in permitidos}
    soma = {i: 0.0 for i in permitidos}
    total = cats = 0.0
    for t in range(1, puxadas + 1):
        nao_vistos = [i for i in permitidos if n[i] == 0]
        if nao_vistos:
            i = nao_vistos[0]
        else:
            ln_t = log(t)
            i = max(permitidos, key=lambda j: soma[j] / n[j] + sqrt(2 * ln_t / n[j]))
        r = 1.0 if rng.random() < media[i] else 0.0
        n[i] += 1
        soma[i] += r
        total += r
        if acoes[i][3] and rng.random() < 0.05:
            cats += 1
            total -= perda
    return total, cats, perguntas


def p194_transferencia_de_tipo(sementes=tuple(range(360, 370)), rodadas=20):
    """O módulo de cautela da SYNTHAI (com pesos aprendidos no mundo de escolha única) serve num bandido?"""
    versoes = ("ucb", "ucb_excluir", "ucb_synthai", "ucb_oraculo")
    por_semente = {v: [] for v in versoes}
    cats = {v: 0.0 for v in versoes}
    perg = {v: 0.0 for v in versoes}
    for s in sementes:
        ag = _synthai_realista(_rng(s))  # calibrada no mundo da Parte 8: outro tipo de tarefa
        for v in versoes:
            rng = _rng(s * 7 + 1)
            tot = 0.0
            for _ in range(rodadas):
                t, c, q = _bandido_arriscado(v, rng, ag)
                tot += t
                cats[v] += c
                perg[v] += q
            por_semente[v].append(tot / rodadas)
    n = len(sementes) * rodadas
    medias = {v: (sum(x) / len(x), cats[v] / n, perg[v] / n) for v, x in por_semente.items()}
    difs = {}
    for a in ("ucb", "ucb_excluir"):
        d = [y - x for x, y in zip(por_semente[a], por_semente["ucb_synthai"])]
        m = sum(d) / len(d)
        dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
        difs[f"ucb_synthai - {a}"] = (m, dp, m / (dp / sqrt(len(d))))
    return medias, difs


def p200_retrospectiva(placar_por_parte=((2, 5), (4, 7), (1, 2), (3, 5), (4, 6), (3, 5), (4, 7), (3, 6), (2, 4), (3, 5))):
    """200 perguntas: quantas afirmações testadas, quantas certas de primeira, e a taxa por parte (3 a 12)."""
    erros = sum(e for e, _ in placar_por_parte)
    testes = sum(n for _, n in placar_por_parte)
    return testes, erros, testes - erros, (testes - erros) / testes


# --- Parte 14: o último passo, a memória de um só golpe, o peso do passado ---

# Placar acumulado ao fim da Parte 14 (atualizado quando os testes da parte terminam)
ERROS_P210, TESTES_P210 = 32, 58


class SynthaiVelha(SynthaiPlanejadora):
    """P202 (pré-registrado na P193): no último passo, sem futuro, a cautela vira caráter, não cálculo.

    Quando não há passos restantes, sorteia entre mais candidatas (q_final) em vez de ir ao topo."""

    def __init__(self, q_final=0.2, **kw):
        super().__init__(integrar=False, **kw)
        self.q_base = self.q
        self.q_final = q_final

    def preparar_passo(self, estimativas, restantes, nivel, valor_medio_passo):
        super().preparar_passo(estimativas, restantes, nivel, valor_medio_passo)
        self.q = self.q_final if restantes == 0 else self.q_base


def p203_ultimo_passo(sementes=tuple(range(370, 380)), episodios=400):
    """Planejadora vs velha (diversifica no último passo). 10 sementes pareadas."""
    linhas = {"planejadora_sem_integrar": [], "velha": []}
    for s in sementes:
        for v in linhas:
            rng = _rng(s)
            if v == "velha":
                m = dict(MUNDO_BASE, **MUNDO_SEQUENCIAL)
                hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
                        for _ in range(150)]
                ag = SynthaiVelha(sombra="propria", compensar="equilibrio")
                ag.mult_pergunta = 2.0
                ag.calibrar(hist)
            else:
                ag = _construir_sequencial(v, rng)
            linhas[v].append(_rodar_sequencial(ag, rng, episodios=episodios))
    medias = {v: (sum(r[0] for r in rs) / len(rs), sum(r[1] for r in rs) / len(rs),
                  [sum(r[2][t] for r in rs) for t in range(MUNDO_SEQUENCIAL["passos"])]) for v, rs in linhas.items()}
    d = [b[0] - a[0] for a, b in zip(linhas["planejadora_sem_integrar"], linhas["velha"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return medias, (m, dp, m / (dp / sqrt(len(d))))


class SynthaiMemoria(SynthaiAnima):
    """P204: memória de um só golpe. Guarda o 'formato' (incerteza, distância à melhor nota) de cada
    catástrofe que viveu ou que o humano vetou, e desconfia de ações parecidas (raio `raio`).

    Junguianamente, é a formação de um complexo a partir de um único evento (P105, P6)."""

    def __init__(self, raio=0.15, reforco=0.05, **kw):
        super().__init__(**kw)
        self.raio = raio
        self.reforco = reforco
        self.memorias = []

    def p_catastrofe(self, acao, melhor):
        p = super().p_catastrofe(acao, melhor)
        x = (acao[1], acao[0] - melhor)
        for mx in self.memorias:
            if (x[0] - mx[0]) ** 2 + (x[1] - mx[1]) ** 2 < self.raio ** 2:
                return max(p, self.reforco)
        return p

    def _lembrar(self, acao, melhor):
        self.memorias.append((acao[1], acao[0] - melhor))

    def _agir(self, acoes, rng, eps_real, carga, eps_decisao):
        self._melhor_atual = max(a[0] for a in acoes)
        escolha = super()._agir(acoes, rng, eps_real, carga, eps_decisao)
        if escolha[0][3]:
            self._lembrar(escolha[0], self._melhor_atual)  # viveu a catástrofe
        return escolha

    def _observar_humano(self, acao, veto):
        if veto:
            self._lembrar(acao, self._melhor_atual)  # o humano disse: isto é perigoso


def p204_memoria(sementes=tuple(range(380, 390)), episodios=2000, mundo=None):
    """Realista vs memória no mundo da armadilha nova (P159). Catástrofes na 1ª e na 2ª metade."""
    mundo = mundo if mundo is not None else {"bonus": 1.0, "rho_cego": 1.0}
    linhas = {"p8_x2": [], "memoria": []}
    metades = {v: [0.0, 0.0] for v in linhas}
    falsos = []
    for s in sementes:
        for v in linhas:
            rng = _rng(s)
            if v == "memoria":
                hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
                ag = SynthaiMemoria(sombra="propria", compensar="equilibrio")
                ag.mult_pergunta = 2.0
                ag.calibrar(hist)
            else:
                ag = _construir(v, rng)
            r1 = _rodar_mundo(ag, rng, episodios=episodios // 2, **mundo)
            r2 = _rodar_mundo(ag, rng, episodios=episodios // 2, **mundo)
            metades[v][0] += r1[0] / len(sementes)
            metades[v][1] += r2[0] / len(sementes)
            linhas[v].append((r1[3] + r2[3]) / 2)
            if v == "memoria":
                # fração de ações seguras que a memória marca como suspeitas (o custo da "fobia")
                rng_av = _rng(s + 9000)
                marcadas = total = 0
                for _ in range(50):
                    acoes = _gerar_acoes(rng_av, 200, 0.005, 2, 3, 0.5)
                    melhor = max(a[0] for a in acoes)
                    for a in acoes:
                        if not a[3]:
                            total += 1
                            x = (a[1], a[0] - melhor)
                            marcadas += any((x[0] - mx[0]) ** 2 + (x[1] - mx[1]) ** 2 < ag.raio ** 2 for mx in ag.memorias)
                falsos.append((marcadas / total, len(ag.memorias)))
    d = [b - a for a, b in zip(linhas["p8_x2"], linhas["memoria"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    fobia = sum(f for f, _ in falsos) / len(falsos)
    lembrancas = sum(n for _, n in falsos) / len(falsos)
    return metades, (m, dp, m / (dp / sqrt(len(d)))), fobia, lembrancas


def p207_sonhos_variancia(n=1000, vies=0.9, repeticoes=2000, semente=207):
    """Auditoria da P122: a amostra efetiva (360 de 1000) prevê a variância do estimador compensado?"""
    rng = _rng(semente)
    comp, equi = [], []
    for _ in range(repeticoes):
        sw = swx = 0.0
        for _ in range(n):
            lado_a = rng.random() < vies
            x = rng.gauss(-2 if lado_a else 2, 1)
            w = 0.5 / vies if lado_a else 0.5 / (1 - vies)
            sw += w
            swx += w * x
        comp.append(swx / sw)
        equi.append(sum(rng.gauss(-2 if rng.random() < 0.5 else 2, 1) for _ in range(n)) / n)

    def var(v):
        m = sum(v) / len(v)
        return sum((x - m) ** 2 for x in v) / (len(v) - 1)
    return var(comp) / var(equi), n / p122_sonhos()[2]


def p206_identidade(sementes=(1, 2, 3), n_acoes=500):
    """A versão rápida do gerador produz exatamente as mesmas ações que a original?"""
    iguais = True
    for s in sementes:
        for p_cat in (0.005, 0.3):
            a, b = _rng(s), _rng(s)
            iguais &= _gerar_acoes_original(a, n_acoes, p_cat, 2, 3, 0.5) == _gerar_acoes_rapido(b, n_acoes, p_cat, 2, 3, 0.5)
            iguais &= a.random() == b.random()  # e deixa o gerador aleatório no mesmo estado
    return iguais


# --- Parte 15: SYNTHAI — o nome, a memória que esquece, a síntese dos módulos ---

# Placar acumulado ao fim da Parte 15 (atualizado quando os testes da parte terminam)
ERROS_P222, TESTES_P222 = 34, 62


def p213_nome_como_simetria():
    """Trocar o nome (Gisele -> Synthai) é uma transformação que não deveria mudar nenhum número (P92, P30).

    Confere que as classes antigas continuam existindo como apelidos e que os testes de regressão passam."""
    import sys
    modulo = sys.modules[__name__]
    pares = [(n, n.replace("Synthai", "Gisele")) for n in dir(modulo) if n.startswith("Synthai")]
    apelidos_ok = all(getattr(modulo, antigo, None) is getattr(modulo, novo) for novo, antigo in pares)
    ok, total, _ = testes_de_regressao()
    return len(pares), apelidos_ok, ok, total


class SynthaiMemoriaV2(SynthaiMemoria):
    """P214 (pré-registrado na P205): memória que separa a fonte e esquece.

    - só guarda o que VIVEU (catástrofes das próprias escolhas), não os vetos de um humano que erra
    - cada memória perde força a cada episódio (meia-vida `meia_vida`) e some quando fica fraca"""

    def __init__(self, meia_vida=500, **kw):
        super().__init__(**kw)
        self.forca = []
        self.fator = 0.5 ** (1 / meia_vida)

    def _lembrar(self, acao, melhor):
        super()._lembrar(acao, melhor)
        self.forca.append(1.0)

    def _observar_humano(self, acao, veto):
        pass  # o que me disseram não vira memória

    def _agir(self, acoes, rng, eps_real, carga, eps_decisao):
        self.forca = [f * self.fator for f in self.forca]
        vivas = [i for i, f in enumerate(self.forca) if f > 0.25]
        self.memorias = [self.memorias[i] for i in vivas]
        self.forca = [self.forca[i] for i in vivas]
        return super()._agir(acoes, rng, eps_real, carga, eps_decisao)


def p214_memoria_v2(sementes=tuple(range(390, 400)), episodios=2000):
    """Realista vs memória v2 no mundo da armadilha nova; e a 'fobia' no mundo normal."""
    mundo = {"bonus": 1.0, "rho_cego": 1.0}
    linhas = {"p8_x2": [], "memoria_v2": []}
    metades = {v: [0.0, 0.0] for v in linhas}
    fobias, lembrancas = [], []
    for s in sementes:
        for v in linhas:
            rng = _rng(s)
            if v == "memoria_v2":
                hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
                ag = SynthaiMemoriaV2(sombra="propria", compensar="equilibrio")
                ag.mult_pergunta = 2.0
                ag.calibrar(hist)
            else:
                ag = _construir(v, rng)
            r1 = _rodar_mundo(ag, rng, episodios=episodios // 2, **mundo)
            r2 = _rodar_mundo(ag, rng, episodios=episodios // 2, **mundo)
            metades[v][0] += r1[0] / len(sementes)
            metades[v][1] += r2[0] / len(sementes)
            linhas[v].append((r1[3] + r2[3]) / 2)
            if v == "memoria_v2":
                rng_av = _rng(s + 9000)
                marcadas = total = 0
                for _ in range(50):
                    acoes = _gerar_acoes(rng_av, 200, 0.005, 2, 3, 0.5)
                    melhor = max(a[0] for a in acoes)
                    for a in acoes:
                        if not a[3]:
                            total += 1
                            x = (a[1], a[0] - melhor)
                            marcadas += any((x[0] - mx[0]) ** 2 + (x[1] - mx[1]) ** 2 < ag.raio ** 2 for mx in ag.memorias)
                fobias.append(marcadas / total)
                lembrancas.append(len(ag.memorias))
    d = [b - a for a, b in zip(linhas["p8_x2"], linhas["memoria_v2"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return metades, (m, dp, m / (dp / sqrt(len(d)))), sum(fobias) / len(fobias), sum(lembrancas) / len(lembrancas)


class SynthaiIntegral(SynthaiVelha):
    """P216: a síntese — planejadora + velha (último passo) + calibração com a imaginação dosada (P173)."""


def _construir_integral(rng, treino_passos=150):
    m = dict(MUNDO_BASE, **MUNDO_SEQUENCIAL)
    hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
            for _ in range(treino_passos)]
    imaginados = []
    for bonus, rho in ((1.0, 1.0), (1.0, 0.5), (6.0, 0.5)):
        imaginados += [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], rho, bonus)
                       for _ in range(100)]
    ag = SynthaiIntegral(sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist + imaginados)
    return ag


def p216_sintese(sementes=tuple(range(400, 410)), episodios=400):
    """Velha vs integral (velha + imaginação dosada), no mundo sequencial normal e com a armadilha nova."""
    resultado = {}
    for nome, mundo in (("normal", None), ("armadilha nova", {"bonus": 1.0, "rho_cego": 1.0})):
        linhas = {"velha": [], "integral": []}
        for s in sementes:
            for v in linhas:
                rng = _rng(s)
                if v == "integral":
                    ag = _construir_integral(rng)
                else:
                    m = dict(MUNDO_BASE, **MUNDO_SEQUENCIAL)
                    hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"],
                                         m["bonus"]) for _ in range(150)]
                    ag = SynthaiVelha(sombra="propria", compensar="equilibrio")
                    ag.mult_pergunta = 2.0
                    ag.calibrar(hist)
                linhas[v].append(_rodar_sequencial(ag, rng, episodios=episodios, mundo=mundo))
        cat = {v: sum(r[1] for r in rs) / len(rs) for v, rs in linhas.items()}
        d = [b[0] - a[0] for a, b in zip(linhas["velha"], linhas["integral"])]
        m = sum(d) / len(d)
        dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
        resultado[nome] = (cat, (m, dp, m / (dp / sqrt(len(d)))))
    return resultado


def p218_inspecao_aprendida(ganho=1.0, punicoes=(9.0, 99.0), custo=1.0, dano=100.0, rodadas=200000, semente=218):
    """Auditoria da P77: dois jogadores aprendendo por jogo fictício chegam ao equilíbrio misto?

    Devolve, para cada punição, as frequências médias de inspeção e de trapaça."""
    resultado = {}
    for punicao in punicoes:
        rng = _rng(semente)
        cont_insp = cont_trap = 1.0
        soma_insp = soma_trap = 0
        for t in range(1, rodadas + 1):
            p_insp = cont_insp / (t + 1)   # crença do trapaceiro sobre a inspeção
            q_trap = cont_trap / (t + 1)   # crença do supervisor sobre a trapaça
            trapaca = (1 - p_insp) * ganho - p_insp * punicao > 0
            inspeciona = q_trap * dano > custo
            # desempate aleatório quando indiferente evita ciclos presos
            if abs((1 - p_insp) * ganho - p_insp * punicao) < 1e-12:
                trapaca = rng.random() < 0.5
            cont_trap += trapaca
            cont_insp += inspeciona
            soma_trap += trapaca
            soma_insp += inspeciona
        resultado[punicao] = (soma_insp / rodadas, soma_trap / rodadas)
    return resultado, p77_inspecao()


def p215_distinguivel(semente=215, episodios=300):
    """A armadilha nova é distinguível com os sinais que a SYNTHAI tem? AUC da calibração (0,5 = acaso)."""
    ag = _synthai_realista(_rng(semente))
    resultado = {}
    for nome, mundo in (("conhecida", {}), ("nova", {"bonus": 1.0, "rho_cego": 1.0})):
        m = dict(MUNDO_BASE, **mundo)
        rng = _rng(semente + 1)
        cats, seguras = [], []
        for _ in range(episodios):
            acoes = _gerar_acoes(rng, m["n_acoes"], 0.02, m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
            melhor = max(a[0] for a in acoes)
            for a in acoes:
                (cats if a[3] else seguras).append(ag.p_catastrofe(a, melhor))
        seguras = sorted(seguras)
        # AUC = P(p de uma catástrofe > p de uma segura), por contagem com busca binária
        from bisect import bisect_left, bisect_right
        soma = sum(bisect_left(seguras, c) + 0.5 * (bisect_right(seguras, c) - bisect_left(seguras, c)) for c in cats)
        resultado[nome] = soma / (len(cats) * len(seguras))
    return resultado


# --- Parte 16: um sentido novo ---

# Placar acumulado ao fim da Parte 16 (atualizado quando os testes da parte terminam)
ERROS_P230, TESTES_P230 = 37, 67


def p223_sinal_combinado(auc_atual=0.748, d_sensor=1.0):
    """Dois sinais independentes e gaussianos: d' se soma em quadratura. AUC = Phi(d'/sqrt 2)."""
    d_atual = sqrt(2) * Z.inv_cdf(auc_atual)
    d_total = sqrt(d_atual**2 + d_sensor**2)
    return d_atual, d_total, Z.cdf(d_total / sqrt(2)), Z.cdf(d_sensor / sqrt(2))


def p224_auditoria_p94(mu=0.02, t=10.0, k=3, amostras=400000, semente=224):
    """Auditoria da P94: k salvaguardas que falham de forma independente vs k estágios que precisam ocorrer em ordem."""
    x = mu * t
    paralelo = (1 - exp(-x)) ** k
    sequencial = 1 - exp(-x) * sum(x**j / factorial(j) for j in range(k))
    rng = _rng(semente)
    sim_par = sim_seq = 0
    for _ in range(amostras):
        tempos = [rng.expovariate(mu) for _ in range(k)]
        sim_par += max(tempos) <= t
        sim_seq += sum(tempos) <= t
    formula_p94 = x**k / factorial(k)
    corrigido_p94 = (1 - exp(-1e-3 * 50)) ** 4
    return paralelo, sim_par / amostras, sequencial, sim_seq / amostras, formula_p94, corrigido_p94


class _SentidoNovo:
    """Mistura (mixin) da P225: um sensor de outra natureza, que lê o dano diretamente com ruído.

    Leitura s = d' * catástrofe + N(0, 1), com gerador próprio (o mundo não muda). Entra como 4º sinal da calibração.
    O que o agente pode saber: só a leitura ruidosa, nunca o rótulo."""

    def __init__(self, d_sensor=1.0, semente_sensor=225, **kw):
        super().__init__(**kw)
        self.d_sensor = d_sensor
        self._rng_sensor = _rng(semente_sensor)
        self.leitura = {}
        self.w = [0.0, 0.0, 0.0, 0.0]

    def perceber(self, acoes):
        g = self._rng_sensor.gauss
        self.leitura = {id(a): self.d_sensor * a[3] + g(0, 1) for a in acoes}

    def _x(self, acao, melhor):
        m, dp, _, _ = acao
        return (1.0, dp, m - melhor, self.leitura.get(id(acao), 0.0))

    def calibrar(self, episodios_rotulados, **kw):
        leituras = {}
        for acoes in episodios_rotulados:
            self.perceber(acoes)
            leituras.update(self.leitura)
        self.leitura = leituras
        super().calibrar(episodios_rotulados, **kw)
        self.leitura = {}


class SynthaiSentidos(_SentidoNovo, SynthaiAnima):
    """SYNTHAI de um passo com o sentido novo (P225)."""


class SynthaiVelhaSentidos(_SentidoNovo, SynthaiVelha):
    """SYNTHAI velha (planeja, diversifica no fim) com o sentido novo (P227)."""


def _construir_sentidos(rng, d_sensor=1.0):
    hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
    ag = SynthaiSentidos(d_sensor=d_sensor, sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    return ag


def p225_sentido_novo(sementes=tuple(range(410, 420)), episodios=2000):
    """Realista vs com sentido novo (d' = 1), no mundo base e no da armadilha nova. 10 sementes pareadas."""
    resultado = {}
    for nome, mundo in (("base", {}), ("armadilha nova", {"bonus": 1.0, "rho_cego": 1.0})):
        linhas = {"p8_x2": [], "sentidos": []}
        for s in sementes:
            for v in linhas:
                rng = _rng(s)
                ag = _construir_sentidos(rng) if v == "sentidos" else _construir(v, rng)
                linhas[v].append(_rodar_mundo(ag, rng, episodios=episodios, **mundo))
        cat = {v: sum(r[0] for r in rs) / len(rs) for v, rs in linhas.items()}
        d = [b[3] - a[3] for a, b in zip(linhas["p8_x2"], linhas["sentidos"])]
        m = sum(d) / len(d)
        dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
        resultado[nome] = (cat, (m, dp, m / (dp / sqrt(len(d)))))
    return resultado


def p226_auc_com_sentido(semente=215, episodios=300):
    """AUC da calibração com o sentido novo, no mesmo protocolo da P215."""
    ag = _construir_sentidos(_rng(semente))
    resultado = {}
    from bisect import bisect_left, bisect_right
    for nome, mundo in (("conhecida", {}), ("nova", {"bonus": 1.0, "rho_cego": 1.0})):
        m = dict(MUNDO_BASE, **mundo)
        rng = _rng(semente + 1)
        cats, seguras = [], []
        for _ in range(episodios):
            acoes = _gerar_acoes(rng, m["n_acoes"], 0.02, m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
            ag.perceber(acoes)
            melhor = max(a[0] for a in acoes)
            for a in acoes:
                (cats if a[3] else seguras).append(ag.p_catastrofe(a, melhor))
        seguras = sorted(seguras)
        soma = sum(bisect_left(seguras, c) + 0.5 * (bisect_right(seguras, c) - bisect_left(seguras, c)) for c in cats)
        resultado[nome] = soma / (len(cats) * len(seguras))
    return resultado


def p227_velha_com_sentido(sementes=tuple(range(420, 430)), episodios=400):
    """Mundo sequencial com a armadilha nova: velha vs velha com sentido novo."""
    mundo = {"bonus": 1.0, "rho_cego": 1.0}
    linhas = {"velha": [], "velha_sentidos": []}
    for s in sementes:
        for v in linhas:
            rng = _rng(s)
            m = dict(MUNDO_BASE, **MUNDO_SEQUENCIAL)
            hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
                    for _ in range(150)]
            classe = SynthaiVelhaSentidos if v == "velha_sentidos" else SynthaiVelha
            ag = classe(sombra="propria", compensar="equilibrio")
            ag.mult_pergunta = 2.0
            ag.calibrar(hist)
            linhas[v].append(_rodar_sequencial(ag, rng, episodios=episodios, mundo=mundo))
    medias = {v: (sum(r[0] for r in rs) / len(rs), sum(r[1] for r in rs) / len(rs)) for v, rs in linhas.items()}
    d = [b[0] - a[0] for a, b in zip(linhas["velha"], linhas["velha_sentidos"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return medias, (m, dp, m / (dp / sqrt(len(d))))



# --- Parte 17: quanto vale perceber, e onde olhar ---

# Placar acumulado ao fim da Parte 17 (atualizado quando os testes da parte terminam)
ERROS_P239, TESTES_P239 = 37, 71


def p234_valor_do_sentido(d_sensores=(0.5, 1.0, 2.0), sementes=tuple(range(430, 440)), episodios=1000):
    """Quanto vale um sentido melhor? Ganho no líquido (armadilha nova) e AUC teórica, por d' do sensor."""
    mundo = {"bonus": 1.0, "rho_cego": 1.0}
    resultado = {}
    for d in d_sensores:
        dif, cats = [], [0.0, 0.0]
        for s in sementes:
            rng = _rng(s)
            base = _rodar_mundo(_construir("p8_x2", rng), rng, episodios=episodios, **mundo)
            rng = _rng(s)
            com = _rodar_mundo(_construir_sentidos(rng, d_sensor=d), rng, episodios=episodios, **mundo)
            dif.append(com[3] - base[3])
            cats[0] += base[0] / len(sementes)
            cats[1] += com[0] / len(sementes)
        m = sum(dif) / len(dif)
        dp = sqrt(sum((x - m) ** 2 for x in dif) / (len(dif) - 1))
        resultado[d] = (m, dp, m / (dp / sqrt(len(dif))), cats[0], cats[1], p223_sinal_combinado(d_sensor=d)[2])
    return resultado


class SynthaiAtenta(SynthaiSentidos):
    """P235: atenção seletiva. Só lê o sensor nas ações que já estão entre as melhores (fração `foco`);
    as outras ficam sem leitura (valor neutro 0). Cada leitura custa `custo_leitura`."""

    def __init__(self, foco=0.1, custo_leitura=0.002, **kw):
        super().__init__(**kw)
        self.foco = foco
        self.custo_leitura = custo_leitura
        self.leituras = 0
        self._seletiva = False

    def perceber(self, acoes):
        if not self._seletiva:
            return _SentidoNovo.perceber(self, acoes)  # explícito: o método também é usado pela SynthaiVelhaAtenta
        ordem = sorted(acoes, key=lambda a: -(a[0] - a[1]))
        alvo = ordem[: max(1, int(self.foco * len(ordem)))]
        g = self._rng_sensor.gauss
        self.leitura = {id(a): self.d_sensor * a[3] + g(0, 1) for a in alvo}
        self.leituras += len(alvo)


def p235_atencao(sementes=tuple(range(440, 450)), episodios=1000, foco=0.1, custo_leitura=0.002):
    """Ler o sensor em todas as ações vs só nas 10% melhores. Líquido já descontado o custo das leituras."""
    mundo = {"bonus": 1.0, "rho_cego": 1.0}
    n_acoes = MUNDO_BASE["n_acoes"]
    linhas = {"sem_sentido": [], "todas": [], "seletiva": []}
    for s in sementes:
        rng = _rng(s)
        linhas["sem_sentido"].append(_rodar_mundo(_construir("p8_x2", rng), rng, episodios=episodios, **mundo)[3])
        for v in ("todas", "seletiva"):
            rng = _rng(s)
            hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
            ag = SynthaiAtenta(foco=foco, custo_leitura=custo_leitura, sombra="propria", compensar="equilibrio")
            ag.mult_pergunta = 2.0
            ag.calibrar(hist)
            ag._seletiva = v == "seletiva"
            liq = _rodar_mundo(ag, rng, episodios=episodios, **mundo)[3]
            leituras_por_ep = ag.leituras / episodios if v == "seletiva" else n_acoes
            linhas[v].append(liq - custo_leitura * leituras_por_ep)
    ganho = {v: sum(b - a for a, b in zip(linhas["sem_sentido"], linhas[v])) / len(sementes) for v in ("todas", "seletiva")}
    d = [b - a for a, b in zip(linhas["todas"], linhas["seletiva"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return ganho, (m, dp, m / (dp / sqrt(len(d)))), foco


def p237_auditoria_p57(erro=0.01, verificacao=0.99, modificacoes=1000, pontos_cegos=(0.0, 0.01, 0.1),
                       rodadas=4000, semente=237):
    """Auditoria da P57: e se o verificador tiver um ponto cego (uma fração de tipos de erro que nunca vê)?"""
    resultado = {}
    rng = _rng(semente)
    for b in pontos_cegos:
        efetivo = erro * (b + (1 - b) * (1 - verificacao))
        teoria = (1 - efetivo) ** modificacoes
        sobrevive = 0
        for _ in range(rodadas):
            ok = True
            for _ in range(modificacoes):
                if rng.random() < erro:
                    cego = rng.random() < b
                    if cego or rng.random() >= verificacao:
                        ok = False
                        break
            sobrevive += ok
        resultado[b] = (teoria, sobrevive / rodadas)
    return resultado



# --- Parte 18: a linguagem como canal ---

# Placar acumulado ao fim da Parte 18 (atualizado quando os testes da parte terminam)
ERROS_P249, TESTES_P249 = 37, 73

PALAVRAS = ("seguro", "acho que ok", "desconfio", "perigo")
FALA_CAT = (0.05, 0.10, 0.25, 0.60)   # como o humano fala de uma ação catastrófica
FALA_SEG = (0.60, 0.25, 0.10, 0.05)   # como fala de uma ação segura


def _entropia(ps):
    return -sum(p * log2(p) for p in ps if p > 0)


def p242_bits_do_veto(p=0.1, eps=0.1):
    """Informação mútua entre a resposta do humano e a catástrofe: veto binário vs quatro palavras."""
    q = p * (1 - eps) + (1 - p) * eps
    binario = _entropia((q, 1 - q)) - _entropia((eps, 1 - eps))
    ruido = min(1.0, 2 * eps)  # cansaço: com prob. 2 eps a palavra sai ao acaso
    wc = [(1 - ruido) * x + ruido / 4 for x in FALA_CAT]
    ws = [(1 - ruido) * x + ruido / 4 for x in FALA_SEG]
    w = [p * a + (1 - p) * b for a, b in zip(wc, ws)]
    palavras = _entropia(w) - (p * _entropia(wc) + (1 - p) * _entropia(ws))
    return binario, palavras, palavras / binario


class SynthaiFala(SynthaiAnima):
    """P245: o humano responde com uma de quatro palavras, não com sim/não.

    A SYNTHAI não sabe o que as palavras significam: aprende P(catástrofe | palavra) com as auditorias (10%).
    Veta se P(catástrofe | palavra) * perda > custo de vetar (limiar fixado antes de rodar: 0,01)."""

    def __init__(self, conhece_sentido=False, p_auditoria=0.1, limiar_veto=0.01, **kw):
        super().__init__(**kw)
        self.conhece = conhece_sentido
        self.p_auditoria = p_auditoria
        self.limiar_veto = limiar_veto
        self.contagem = {w: [0.5, 4.5] for w in PALAVRAS}  # prior Beta(0,5; 4,5) por palavra
        self._rng_auditoria = _rng(245)

    def _p_dado_palavra(self, w):
        if self.conhece:
            i = PALAVRAS.index(w)
            prior = 0.1
            return prior * FALA_CAT[i] / (prior * FALA_CAT[i] + (1 - prior) * FALA_SEG[i])
        a, b = self.contagem[w]
        return a / (a + b)

    def _perguntar_humano(self, acao, rng, eps_real):
        ruido = min(1.0, 2 * eps_real)
        dist = FALA_CAT if acao[3] else FALA_SEG
        if rng.random() < ruido:
            w = PALAVRAS[rng.randrange(4)]
        else:
            u, acc, w = rng.random(), 0.0, PALAVRAS[-1]
            for palavra, pr in zip(PALAVRAS, dist):
                acc += pr
                if u < acc:
                    w = palavra
                    break
        if self._rng_auditoria.random() < self.p_auditoria:  # depois, descobre o que era de fato
            self.contagem[w][0 if acao[3] else 1] += 1
        return self._p_dado_palavra(w) > self.limiar_veto


def p245_linguagem(sementes=tuple(range(450, 460)), episodios=2000):
    """Veto binário vs quatro palavras (sentido aprendido) vs quatro palavras (sentido conhecido). 10 sementes pareadas."""
    versoes = ("binario", "fala_aprendida", "fala_conhecida")
    linhas = {v: [] for v in versoes}
    aprendido = {w: 0.0 for w in PALAVRAS}
    for s in sementes:
        for v in versoes:
            rng = _rng(s)
            if v == "binario":
                ag = _construir("p8_x2", rng)
            else:
                hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
                ag = SynthaiFala(conhece_sentido=(v == "fala_conhecida"), sombra="propria", compensar="equilibrio")
                ag.mult_pergunta = 2.0
                ag.calibrar(hist)
            linhas[v].append(_rodar_mundo(ag, rng, episodios=episodios))
            if v == "fala_aprendida":
                for w in PALAVRAS:
                    aprendido[w] += ag._p_dado_palavra(w) / len(sementes)
    medias = {v: (sum(r[0] for r in rs) / len(rs), sum(r[2] for r in rs) / len(rs), sum(r[3] for r in rs) / len(rs))
              for v, rs in linhas.items()}
    difs = {}
    for b in ("fala_aprendida", "fala_conhecida"):
        d = [y[3] - x[3] for x, y in zip(linhas["binario"], linhas[b])]
        m = sum(d) / len(d)
        dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
        difs[f"{b} - binario"] = (m, dp, m / (dp / sqrt(len(d))))
    verdadeiro = {w: 0.1 * c / (0.1 * c + 0.9 * sg) for w, c, sg in zip(PALAVRAS, FALA_CAT, FALA_SEG)}
    return medias, difs, aprendido, verdadeiro


def p247_auditoria_p105(palavras=100, complexos=5, efeito=3.0, repeticoes=4000, semente=247):
    """Auditoria da P105: simula o teste de associação e conta achados e falsos alarmes."""
    rng = _rng(semente)
    resultado = {}
    for nome, z in (("z>2", 2.0), ("Bonferroni", Z.inv_cdf(1 - 0.05 / palavras))):
        achados = falsos = 0
        for _ in range(repeticoes):
            for i in range(palavras):
                x = rng.gauss(efeito if i < complexos else 0.0, 1)
                if x > z:
                    if i < complexos:
                        achados += 1
                    else:
                        falsos += 1
        resultado[nome] = (achados / repeticoes, falsos / repeticoes, p105_complexos()[nome][1:3])
    return resultado



# --- Parte 19: a palavra precisa, a versão principal e a trajetória inteira ---

# Placar acumulado ao fim da Parte 19 (atualizado quando os testes da parte terminam)
ERROS_P258, TESTES_P258 = 39, 78

FALA_PRECISA_CAT = (0.01, 0.04, 0.15, 0.80)
FALA_PRECISA_SEG = (0.80, 0.15, 0.04, 0.01)


def p252_bits_da_palavra_precisa(p=0.1, eps=0.1):
    """P245 (Meta) dizia: um humano preciso com as palavras inverteria o resultado. Quanta informação ele dá?"""
    ruido = min(1.0, 2 * eps)
    wc = [(1 - ruido) * x + ruido / 4 for x in FALA_PRECISA_CAT]
    ws = [(1 - ruido) * x + ruido / 4 for x in FALA_PRECISA_SEG]
    w = [p * a + (1 - p) * b for a, b in zip(wc, ws)]
    precisa = _entropia(w) - (p * _entropia(wc) + (1 - p) * _entropia(ws))
    binario = p242_bits_do_veto(p, eps)[0]
    return binario, precisa, precisa / binario


class SynthaiFalaPrecisa(SynthaiFala):
    """O mesmo canal de quatro palavras, com um humano preciso; significado conhecido (P252)."""

    def _p_dado_palavra(self, w):
        i = PALAVRAS.index(w)
        prior = 0.1
        return prior * FALA_PRECISA_CAT[i] / (prior * FALA_PRECISA_CAT[i] + (1 - prior) * FALA_PRECISA_SEG[i])

    def _perguntar_humano(self, acao, rng, eps_real):
        ruido = min(1.0, 2 * eps_real)
        dist = FALA_PRECISA_CAT if acao[3] else FALA_PRECISA_SEG
        if rng.random() < ruido:
            w = PALAVRAS[rng.randrange(4)]
        else:
            u, acc, w = rng.random(), 0.0, PALAVRAS[-1]
            for palavra, pr in zip(PALAVRAS, dist):
                acc += pr
                if u < acc:
                    w = palavra
                    break
        return self._p_dado_palavra(w) > self.limiar_veto


def p252_palavra_precisa(sementes=tuple(range(460, 470)), episodios=2000):
    """Veto binário vs quatro palavras precisas (significado conhecido). 10 sementes pareadas."""
    linhas = {"binario": [], "precisa": []}
    for s in sementes:
        for v in linhas:
            rng = _rng(s)
            if v == "binario":
                ag = _construir("p8_x2", rng)
            else:
                hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
                ag = SynthaiFalaPrecisa(sombra="propria", compensar="equilibrio")
                ag.mult_pergunta = 2.0
                ag.calibrar(hist)
            linhas[v].append(_rodar_mundo(ag, rng, episodios=episodios))
    medias = {v: (sum(r[0] for r in rs) / len(rs), sum(r[3] for r in rs) / len(rs)) for v, rs in linhas.items()}
    d = [b[3] - a[3] for a, b in zip(linhas["binario"], linhas["precisa"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return medias, (m, dp, m / (dp / sqrt(len(d))))


class SynthaiVelhaAtenta(SynthaiVelhaSentidos):
    """A nova versão principal candidata (P253): planeja, diversifica no fim, tem o sentido novo e lê o sensor
    só nas ações mais promissoras (atenção seletiva da P235)."""

    perceber = SynthaiAtenta.perceber

    def __init__(self, foco=0.1, custo_leitura=0.002, **kw):
        super().__init__(**kw)
        self.foco = foco
        self.custo_leitura = custo_leitura
        self.leituras = 0
        self._seletiva = False


def p253_versao_principal(sementes=tuple(range(470, 480)), episodios=400, custo_leitura=0.002):
    """Mundo sequencial com a armadilha nova: velha, velha + sentido (lendo tudo), velha + sentido + atenção.
    Retorno já descontado o custo das leituras."""
    mundo = {"bonus": 1.0, "rho_cego": 1.0}
    n_por_ep = MUNDO_SEQUENCIAL["n_acoes"] * MUNDO_SEQUENCIAL["passos"]
    versoes = ("velha", "sentido_tudo", "sentido_atento")
    linhas = {v: [] for v in versoes}
    for s in sementes:
        for v in versoes:
            rng = _rng(s)
            m = dict(MUNDO_BASE, **MUNDO_SEQUENCIAL)
            hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
                    for _ in range(150)]
            ag = SynthaiVelha(sombra="propria", compensar="equilibrio") if v == "velha" else \
                SynthaiVelhaAtenta(sombra="propria", compensar="equilibrio")
            ag.mult_pergunta = 2.0
            ag.calibrar(hist)
            if v == "sentido_atento":
                ag._seletiva = True
            ret, cat, _ = _rodar_sequencial(ag, rng, episodios=episodios, mundo=mundo)
            if v == "sentido_tudo":
                ret -= custo_leitura * n_por_ep
            elif v == "sentido_atento":
                ret -= custo_leitura * ag.leituras / episodios
            linhas[v].append((ret, cat))
    medias = {v: (sum(r[0] for r in rs) / len(rs), sum(r[1] for r in rs) / len(rs)) for v, rs in linhas.items()}
    difs = {}
    for b in ("sentido_tudo", "sentido_atento"):
        d = [y[0] - x[0] for x, y in zip(linhas["velha"], linhas[b])]
        mm = sum(d) / len(d)
        dp = sqrt(sum((x - mm) ** 2 for x in d) / (len(d) - 1))
        difs[f"{b} - velha"] = (mm, dp, mm / (dp / sqrt(len(d))))
    return medias, difs


def p254_trajetoria_do_upsilon(pontos=((5, 0.287), (7, 0.414), (8, 0.465), (9, 0.449), (10, 0.409), (11, 0.486), (17, 0.547))):
    """Ajuste Υ(parte) = teto - (teto - Υ0) * r^(parte - 5) por busca em grade (mínimos quadrados)."""
    melhor = None
    for teto in [x / 1000 for x in range(400, 1001, 5)]:
        for r in [x / 100 for x in range(1, 100)]:
            erro = sum((teto - (teto - pontos[0][1]) * r ** (n - pontos[0][0]) - u) ** 2 for n, u in pontos)
            if melhor is None or erro < melhor[0]:
                melhor = (erro, teto, r)
    return melhor[1], melhor[2], sqrt(melhor[0] / len(pontos))


def p255_quaternidade(modulos=(("sensacao", ("comite", "discordancia", "sensor de primeira mao", "atencao seletiva")),
                               ("pensamento", ("calibracao", "valor da pergunta", "pessimismo")),
                               ("sentimento", ("quantilizacao", "veto", "ancora", "diversificar no fim")),
                               ("intuicao", ("planejar", "imaginar ameacas")))):
    """Perfil atual da SYNTHAI nas quatro funções de Jung (compare com a P161: 1,561 bits, intuição vazia)."""
    total = sum(len(m) for _, m in modulos)
    h = _entropia([len(m) / total for _, m in modulos])
    return {f: len(m) for f, m in modulos}, h


def p256_auditoria_p121(rho=0.3, amostras=200000, semente=256):
    """Auditoria da P121: R² da quarta função a partir das outras três, simulando normais com correlação rho."""
    rng = _rng(semente)
    a, b = sqrt(rho), sqrt(1 - rho)
    xs, ys = [], []
    for _ in range(amostras):
        c = rng.gauss(0, 1)
        v = [a * c + b * rng.gauss(0, 1) for _ in range(4)]
        xs.append(v[0] + v[1] + v[2])  # por simetria, a melhor previsão linear usa a soma das três
        ys.append(v[3])
    mx, my = sum(xs) / amostras, sum(ys) / amostras
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    return cov * cov / (vx * vy), p121_quaternidade(rho)



# --- Parte 20: o símbolo com o tempo, o Υ do mundo sequencial e o que cada função contribui ---

# Placar acumulado ao fim da Parte 20 (atualizado quando os testes da parte terminam)
ERROS_P269, TESTES_P269 = 42, 84


class SynthaiOuvinte(SynthaiAnima):
    """P262: aprende continuamente com o que o humano responde (P246: o símbolo com o tempo).

    Para decidir, as duas versões usam o mesmo veto binário. Para APRENDER:
    - modo "veto": rótulo = o veto (0 ou 1), como a 'sombra com tudo' da P112;
    - modo "fala": rótulo = P(catástrofe | palavra), uma das quatro palavras vagas da P242, com o significado
      aprendido pelas auditorias (10%), como na SynthaiFala."""

    def __init__(self, modo="veto", p_auditoria=0.1, **kw):
        super().__init__(**kw)
        self.modo = modo
        self.p_auditoria = p_auditoria
        self.contagem = {w: [0.5, 4.5] for w in PALAVRAS}
        self._rng_fala = _rng(262)

    def _agir(self, acoes, rng, eps_real, carga, eps_decisao):
        self._melhor_atual = max(a[0] for a in acoes)
        return super()._agir(acoes, rng, eps_real, carga, eps_decisao)

    def _perguntar_humano(self, acao, rng, eps_real):
        veto = super()._perguntar_humano(acao, rng, eps_real)
        if self.modo == "veto":
            rotulo = 1.0 if veto else 0.0
        else:
            g = self._rng_fala
            dist = FALA_CAT if acao[3] else FALA_SEG
            if g.random() < min(1.0, 2 * eps_real):
                w = PALAVRAS[g.randrange(4)]
            else:
                u, acc, w = g.random(), 0.0, PALAVRAS[-1]
                for palavra, pr in zip(PALAVRAS, dist):
                    acc += pr
                    if u < acc:
                        w = palavra
                        break
            if g.random() < self.p_auditoria:
                self.contagem[w][0 if acao[3] else 1] += 1
            a, b = self.contagem[w]
            rotulo = a / (a + b)
        self._aprender(acao, self._melhor_atual, rotulo)
        return veto


def _auc(agente, rng, episodios=100, mundo=None):
    """AUC da calibração do agente em ações novas (mesmo protocolo da P215)."""
    from bisect import bisect_left, bisect_right
    m = dict(MUNDO_BASE, **(mundo or {}))
    cats, seguras = [], []
    for _ in range(episodios):
        acoes = _gerar_acoes(rng, m["n_acoes"], 0.02, m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
        melhor = max(a[0] for a in acoes)
        for a in acoes:
            (cats if a[3] else seguras).append(agente.p_catastrofe(a, melhor))
    seguras = sorted(seguras)
    soma = sum(bisect_left(seguras, c) + 0.5 * (bisect_right(seguras, c) - bisect_left(seguras, c)) for c in cats)
    return soma / (len(cats) * len(seguras))


def p262_simbolo_com_o_tempo(sementes=tuple(range(480, 490)), episodios=6000):
    """6000 episódios aprendendo com o humano: rótulos de veto vs rótulos de palavras. AUC final e líquido."""
    versoes = ("sem_aprender", "veto", "fala")
    auc = {v: [] for v in versoes}
    liq = {v: [] for v in versoes}
    for s in sementes:
        for v in versoes:
            rng = _rng(s)
            hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
            ag = SynthaiAnima(sombra="propria", compensar="equilibrio") if v == "sem_aprender" else \
                SynthaiOuvinte(modo=v, sombra="propria", compensar="equilibrio")
            ag.mult_pergunta = 2.0
            ag.calibrar(hist)
            liq[v].append(_rodar_mundo(ag, rng, episodios=episodios)[3])
            auc[v].append(_auc(ag, _rng(s + 4800)))
    resumo = {v: (sum(auc[v]) / len(auc[v]), sum(liq[v]) / len(liq[v])) for v in versoes}
    d = [a - b for a, b in zip(auc["veto"], auc["fala"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return resumo, (m, dp, m / (dp / sqrt(len(d))))


class OraculoSequencial(PoliticaSimples):
    """Teto do Υ sequencial: vê o valor, a consequência e as catástrofes (o que nenhum agente pode saber)."""

    def __init__(self):
        super().__init__("oraculo")
        self.c, self.r = {}, 0

    def preparar_passo(self, *_a):
        pass

    def ver_tudo(self, consequencias, restantes):
        self.c, self.r = consequencias, restantes

    def agir_no_mundo(self, acoes, rng, eps_real, carga):
        seguras = [a for a in acoes if not a[3]] or acoes
        return max(seguras, key=lambda a: a[2] + self.c[id(a)] * self.r), 0


MUNDOS_SEQUENCIAIS = {
    "base": ({}, 0),
    "armadilha nova": ({"bonus": 1.0, "rho_cego": 1.0}, 1),
    "catastrofe x2": ({"p_cat": 0.01}, 1),
    "modelo ruim": ({"sigma_modelo": 2.0}, 1),
    "humano fragil": ({"fadiga": 0.6}, 1),
}


def _construir_seq(versao, rng, custo_leitura=0.002):
    m = dict(MUNDO_BASE, **MUNDO_SEQUENCIAL)
    hist = [_gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
            for _ in range(150)]
    classes = {"miope": SynthaiAnima, "planejadora": SynthaiPlanejadora, "velha": SynthaiVelha,
               "velha_atenta": SynthaiVelhaAtenta, "atenta_sem_velha": SynthaiVelhaAtenta}
    if versao == "calibrada":  # P274: definida na Parte 21; resolvida aqui na hora da chamada
        classes["calibrada"] = SynthaiIntuicaoCalibrada
    if versao == "planejadora":
        ag = SynthaiPlanejadora(integrar=False, sombra="propria", compensar="equilibrio")
    elif versao == "atenta_sem_velha":
        ag = SynthaiVelhaAtenta(q_final=0.05, sombra="propria", compensar="equilibrio")
    else:
        ag = classes[versao](sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    if versao in ("velha_atenta", "atenta_sem_velha", "atenta_miope", "calibrada"):
        ag._seletiva = True
    return ag


def _retorno_seq(versao, s, episodios, mundo, custo_leitura=0.002):
    rng = _rng(s)
    if versao in ("acaso", "oraculo"):
        ag = PoliticaSimples("acaso") if versao == "acaso" else OraculoSequencial()
        return _rodar_sequencial(ag, rng, episodios=episodios, planeja=False, mundo=mundo)[0]
    if versao == "atenta_miope":
        ag = _construir_seq("velha_atenta", rng)
        ret = _rodar_sequencial(ag, rng, episodios=episodios, planeja=False, mundo=mundo)[0]
    else:
        ag = _construir_seq(versao, rng)
        ret = _rodar_sequencial(ag, rng, episodios=episodios, planeja=(versao != "miope"), mundo=mundo)[0]
    leituras = getattr(ag, "leituras", 0)
    return ret - custo_leitura * leituras / episodios


def p265_upsilon_sequencial(versoes=("miope", "planejadora", "velha", "velha_atenta"), sementes=(265, 266, 267),
                            episodios=300, bits_por_mudanca=3):
    """Υ no mundo sequencial: média ponderada (2^-K) do retorno normalizado entre o acaso (0) e o oráculo (1)."""
    upsilon = {v: 0.0 for v in versoes}
    soma_pesos = 0.0
    por_mundo = {}
    for nome, (mudancas, k) in MUNDOS_SEQUENCIAIS.items():
        peso = 2.0 ** (-bits_por_mudanca * k)
        soma_pesos += peso
        notas = {v: 0.0 for v in versoes}
        for s in sementes:
            acaso = _retorno_seq("acaso", s, episodios, mudancas)
            oraculo = _retorno_seq("oraculo", s, episodios, mudancas)
            for v in versoes:
                notas[v] += (_retorno_seq(v, s, episodios, mudancas) - acaso) / (oraculo - acaso) / len(sementes)
        por_mundo[nome] = notas
        for v in versoes:
            upsilon[v] += peso * notas[v]
    return {v: u / soma_pesos for v, u in upsilon.items()}, por_mundo


def p266_o_que_cada_funcao_vale(sementes=tuple(range(490, 500)), episodios=400):
    """Ablação da versão principal (armadilha nova, mundo sequencial): tirar uma peça de cada vez."""
    mundo = {"bonus": 1.0, "rho_cego": 1.0}
    versoes = {"completa": "velha_atenta", "sem planejar (intuicao)": "atenta_miope",
               "sem diversificar no fim (sentimento)": "atenta_sem_velha", "sem o sentido novo (sensacao)": "velha"}
    linhas = {nome: [_retorno_seq(v, s, episodios, mundo) for s in sementes] for nome, v in versoes.items()}
    resultado = {}
    for nome, valores in linhas.items():
        if nome == "completa":
            continue
        d = [c - x for c, x in zip(linhas["completa"], valores)]
        m = sum(d) / len(d)
        dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
        resultado[nome] = (m, dp, m / (dp / sqrt(len(d))))
    return sum(linhas["completa"]) / len(sementes), resultado


def p267_auditoria_p146(eta=0.1, k=0.2, ruido=0.05, passos=500, rodadas=2000, semente=267):
    """Auditoria da P146 com ruído: a crença compartilhada ainda converge para (k a0 + eta b0)/(k + eta)?"""
    rng = _rng(semente)
    finais = []
    for _ in range(rodadas):
        a, b = 1.0, 0.0
        for _ in range(passos):
            a, b = a + eta * (b - a) + rng.gauss(0, ruido) * eta, b + k * (a - b) + rng.gauss(0, ruido) * k
        finais.append((a + b) / 2)
    media = sum(finais) / len(finais)
    dp = sqrt(sum((x - media) ** 2 for x in finais) / (len(finais) - 1))
    return media, dp, p146_transferencia(eta=eta, k=k)[0]



def p268_efeito_combinado(estimativas=((0.662, 0.752), (0.990, 0.970), (-0.129, 1.016)), n=10):
    """Combina, por variância inversa, três estimativas do ganho do sentido novo no mundo sequencial
    (P227, P253 e a ablação da P266), cada uma com 10 sementes: (média, dp das diferenças)."""
    pesos = [n / dp**2 for _, dp in estimativas]
    media = sum(w * m for w, (m, _) in zip(pesos, estimativas)) / sum(pesos)
    ep = 1 / sqrt(sum(pesos))
    return media, ep, media / ep



# --- Parte 21: a intuição corrigida pela sensação ---

# Placar acumulado ao fim da Parte 21 (atualizado quando os testes da parte terminam)
ERROS_P279, TESTES_P279 = 45, 91


def p272_encolhimento(sigmas=(0.5, 2.0), k=50, r=2.0, amostras=6000, semente=272):
    """Escolher por v + w * ĉ * r, com ĉ = c + N(0, sigma). Qual w é o melhor? Teoria: w* = 1 / (1 + sigma^2)."""
    resultado = {}
    pesos = [x / 20 for x in range(0, 21)]
    for sigma in sigmas:
        rng = _rng(semente)
        totais = [0.0] * len(pesos)
        for _ in range(amostras):
            v = [rng.gauss(0, 1) for _ in range(k)]
            c = [rng.gauss(0, 1) for _ in range(k)]
            ch = [ci + rng.gauss(0, sigma) for ci in c]
            for j, w in enumerate(pesos):
                i = max(range(k), key=lambda i: v[i] + w * ch[i] * r)
                totais[j] += v[i] + c[i] * r
        medias = [t / amostras for t in totais]
        j = max(range(len(pesos)), key=lambda j: medias[j])
        resultado[sigma] = (pesos[j], 1 / (1 + sigma**2), medias[pesos.index(1.0)], medias[j])
    return resultado


class SynthaiIntuicaoCalibrada(SynthaiVelhaAtenta):
    """P273: a intuição (o modelo de mundo) corrigida pela sensação (o que de fato aconteceu).

    Depois de agir, a SYNTHAI vê o próprio nível mudar: a mudança é a consequência real c da ação escolhida.
    Com os pares (ĉ, c) ela estima, por regressão pela origem, quanto confiar no modelo: peso = Σ ĉ c / Σ ĉ²
    (prior: peso 1 com força de 10 pares). O bônus de plano passa a ser peso × ĉ × passos restantes."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.sxy, self.sxx = 10.0, 10.0
        self.peso = 1.0
        self._anterior = None
        self._est = {}

    def preparar_passo(self, estimativas, restantes, nivel, valor_medio_passo):
        if self._anterior is not None:
            c_hat, nivel_antes, restantes_antes = self._anterior
            if restantes == restantes_antes - 1:  # o episódio continuou: a mudança de nível é a consequência real
                c = nivel - nivel_antes
                self.sxy += c_hat * c
                self.sxx += c_hat * c_hat
                self.peso = self.sxy / self.sxx
        self._anterior = None
        self._est, self._nivel, self._restantes = estimativas, nivel, restantes
        super().preparar_passo(estimativas, restantes, nivel, valor_medio_passo)
        self.plano = {k: self.peso * b for k, b in self.plano.items()}

    def agir_no_mundo(self, acoes, rng, eps_real, carga):
        escolha = super().agir_no_mundo(acoes, rng, eps_real, carga)
        self._anterior = (self._est.get(id(escolha[0]), 0.0), self._nivel, self._restantes)
        return escolha


def p274_intuicao_calibrada(sementes=tuple(range(500, 510)), episodios=400):
    """Versão principal vs intuição calibrada, no mundo base e com modelo ruim (sigma 2). 10 sementes pareadas."""
    resultado = {}
    for nome, mundo in (("base", {}), ("modelo ruim", {"sigma_modelo": 2.0})):
        a = [_retorno_seq("velha_atenta", s, episodios, mundo) for s in sementes]
        pesos = []
        b = []
        for s in sementes:
            rng = _rng(s)
            ag = _construir_seq("calibrada", rng)
            ret = _rodar_sequencial(ag, rng, episodios=episodios, mundo=mundo)[0]
            b.append(ret - 0.002 * ag.leituras / episodios)
            pesos.append(ag.peso)
        d = [y - x for x, y in zip(a, b)]
        m = sum(d) / len(d)
        dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
        sigma = mundo.get("sigma_modelo", MUNDO_SEQUENCIAL["sigma_modelo"])
        resultado[nome] = ((m, dp, m / (dp / sqrt(len(d)))), sum(pesos) / len(pesos), 1 / (1 + sigma**2))
    return resultado


def p277_auditoria_p149(erros=(0.01, 0.05, 0.1), tolerancia=0.5, rodadas=4000, semente=277):
    """Auditoria da P149: com erro aleatório de média delta por passo (e não um erro fixo), o horizonte da
    imaginação, medido como o passo mediano em que o erro composto passa de 50%, bate com ln(1,5)/ln(1+delta)?"""
    rng = _rng(semente)
    resultado = {}
    for d in erros:
        horizontes = []
        for _ in range(rodadas):
            fator, h = 1.0, 0
            while fator - 1 <= tolerancia and h < 10000:
                fator *= 1 + rng.expovariate(1 / d)
                h += 1
            horizontes.append(h)
        horizontes.sort()
        resultado[d] = (horizontes[len(horizontes) // 2], p149_imaginacao((d,), tolerancia)[d])
    return resultado


# --- Parte 22: o protótipo em módulos (pacote synthai/) ---

# Placar acumulado ao fim da Parte 22 (atualizado quando os testes da parte terminam)
ERROS_P289, TESTES_P289 = 46, 99


def _pareado(a, b):
    d = [y - x for x, y in zip(a, b)]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return m, dp, m / (dp / sqrt(len(d)))


def p283_equivalencia_modular(sementes=tuple(range(520, 530)), episodios=400):
    """A SYNTHAI montada em módulos (pacote synthai/) contra a versão principal de calculos (P274), mesmas sementes.

    Os geradores de números não são os mesmos, então a comparação é estatística: diferença média, dp e t."""
    from synthai import Synthai as SynthaiModular
    from synthai.mundos import MundoSequencial
    resultado = {}
    for nome, mundo in (("base", {}), ("modelo ruim", {"sigma_modelo": 2.0})):
        a, b, pesos, cats_a, cats_b = [], [], [], 0.0, 0.0
        for s in sementes:
            rng = _rng(s)
            ag = _construir_seq("calibrada", rng)
            ret, cat, _ = _rodar_sequencial(ag, rng, episodios=episodios, mundo=mundo)
            a.append(ret - 0.002 * ag.leituras / episodios)
            cats_a += cat
            w = MundoSequencial(s, **mundo)
            mod = SynthaiModular(s).calibrar(w)
            r = w.rodar(mod, episodios)
            b.append(r["retorno"])
            cats_b += r["catastrofes"]
            pesos.append(mod.intuicao.peso)
        n = len(sementes)
        resultado[nome] = (sum(a) / n, sum(b) / n, _pareado(a, b), sum(pesos) / n, cats_a / n, cats_b / n)
    return resultado


def p284_generalidade(sementes=tuple(range(530, 540))):
    """O mesmo objeto Synthai, sem mudar nada, em três tipos de tarefa, contra o acaso, o guloso e o oráculo."""
    from synthai.__main__ import TAREFAS
    from synthai import Synthai as SynthaiModular
    from synthai.referencias import Acaso, Guloso, Oraculo
    resultado = {}
    for tarefa, (fazer, n) in TAREFAS.items():
        linhas = {c.__name__: [] for c in (Acaso, Guloso, Oraculo, SynthaiModular)}
        cats = {k: 0.0 for k in linhas}
        for s in sementes:
            for cls in (Acaso, Guloso, Oraculo, SynthaiModular):
                mundo = fazer(s)
                r = mundo.rodar(cls(s).calibrar(mundo), n)
                linhas[cls.__name__].append(r["retorno"])
                cats[cls.__name__] += r["catastrofes"] / len(sementes)
        medias = {k: sum(v) / len(v) for k, v in linhas.items()}
        normal = [(y - x) / (z - x) for x, y, z in zip(linhas["Acaso"], linhas["Synthai"], linhas["Oraculo"])]
        resultado[tarefa] = (medias, cats, _pareado(linhas["Acaso"], linhas["Synthai"]),
                             _pareado(linhas["Guloso"], linhas["Synthai"]), sum(normal) / len(normal))
    return resultado


def p285_acoplamento():
    """O grafo dos módulos lido do próprio código (ast): arestas entre módulos, a largura da interface
    (atributos de Situacao/Opcao que o agente lê) e os acessos ao que é escondido (devem ser zero, P7).
    Para comparar: o comprimento da linhagem de herança da versão principal em calculos."""
    import ast
    import os
    from synthai.testes import MODULOS_DO_AGENTE, acessos_escondidos
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthai")
    arestas, interface, linhas = [], set(), 0
    publicos = {"opcoes", "restantes", "nivel", "horizonte", "explorar", "carga_do_humano", "perguntas", "perguntar",
                "ler_sensor", "nota", "comite", "discordancia", "estimativa", "catastrofe", "nivel_antes", "nivel_depois"}
    for nome in MODULOS_DO_AGENTE:
        fonte = open(os.path.join(pasta, nome + ".py"), encoding="utf-8").read()
        linhas += len([x for x in fonte.splitlines() if x.strip() and not x.strip().startswith("#")])
        arvore = ast.parse(fonte)
        for no in ast.walk(arvore):
            if isinstance(no, ast.ImportFrom) and no.level == 1:
                arestas.append((nome, no.module))
            if isinstance(no, ast.Attribute) and no.attr in publicos and not (isinstance(no.value, ast.Name)
                                                                               and no.value.id == "self"):
                interface.add(no.attr)
    escondidos = sum(len(acessos_escondidos(n)) for n in MODULOS_DO_AGENTE)
    linhagem = [c.__name__ for c in SynthaiIntuicaoCalibrada.__mro__ if c.__name__.startswith(("Synthai", "_"))]
    return len(MODULOS_DO_AGENTE), sorted(arestas), sorted(interface), escondidos, linhas, linhagem


def p286_testes_de_unidade():
    """Roda a suíte do pacote (synthai/testes.py) e devolve (testes, falhas + erros)."""
    import io
    import unittest
    from synthai import testes
    suite = unittest.defaultTestLoader.loadTestsFromModule(testes)
    r = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    return r.testsRun, len(r.failures) + len(r.errors)


def p287_veto_falso(sementes=tuple(range(540, 545)), episodios=1000, custo=0.1, perda=50.0, eps=0.1):
    """Auditoria da P71: P* = c/((1-ε)L) ignora o custo do veto falso (perder uma opção segura e ir à próxima).

    Com esse custo Δv, o limiar exato é P = (c + εΔv)/((1-ε)L + εΔv). Mede Δv na SYNTHAI modular, no mundo de
    escolha única: valor da opção perguntada menos o da que ela escolheria se o veto viesse."""
    from synthai import Synthai as SynthaiModular
    from synthai.mundos import MundoSequencial
    difs = []
    for s in sementes:
        mundo = MundoSequencial(s, passos=1, n_acoes=200)
        ag = SynthaiModular(s).calibrar(mundo)
        decidir = ag.decidir

        def decidir_e_medir(sit, _ag=ag, _decidir=decidir):
            escolha = _decidir(sit)
            for vetada in _ag.vetados_agora:  # a régua lê o escondido; o agente, não
                if not vetada._catastrofe:
                    difs.append(vetada._valor - escolha._valor)  # veto falso: o que se perdeu
            return escolha
        ag.decidir = decidir_e_medir
        mundo.rodar(ag, episodios)
    dv = sum(difs) / len(difs) if difs else 0.0
    formula = p71_valor_da_pergunta(custo, perda, eps)
    exato = (custo + eps * dv) / ((1 - eps) * perda + eps * dv)
    return len(difs), dv, formula, exato, exato / formula - 1


# --- Parte 23: reconhecer o que já estava resolvido ---

# Placar acumulado ao fim da Parte 23 (atualizado quando os testes da parte terminam)
ERROS_P299, TESTES_P299 = 53, 113


def p291_menon(area=8.0, precisao=0.001):
    """O escravo do Mênon: os chutes 4 e 3 (e o lado 2) cercam o lado do quadrado de área 8 em [2, 3]. Quantas
    perguntas de sim/não (bisseção) até a precisão pedida, contra uma só ao reconhecer a diagonal (lado = 2√2)?"""
    lo, hi, perguntas = 2.0, 3.0, 0
    while hi - lo > precisao:
        meio = (lo + hi) / 2
        perguntas += 1
        if meio * meio > area:
            hi = meio
        else:
            lo = meio
    return perguntas, ceil(log2(1 / precisao)), (lo + hi) / 2, sqrt(area)


def _logistica_newton(xs, ys, iteracoes=25):
    """Regressão logística exata (Newton/IRLS) com duas variáveis (1, x): a resposta 'já resolvida' que o
    gradiente da SYNTHAI só aproxima."""
    b = w = 0.0
    for _ in range(iteracoes):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for x, y in zip(xs, ys):
            p = 1 / (1 + exp(-max(-30.0, min(30.0, b + w * x))))
            r, v = y - p, p * (1 - p)
            g0 += r
            g1 += r * x
            h00 += v
            h01 += v * x
            h11 += v * x * x
        det = h00 * h11 - h01 * h01
        b += (h11 * g0 - h01 * g1) / det
        w += (h00 * g1 - h01 * g0) / det
    return b, w


def p292_ponto_neutro(d=1.0, pi=0.05, n=200000, semente=292):
    """Sensor s = d·catástrofe + N(0,1). Ajuste exato de logit P(cat | s) = b + w s. Uma opção sem leitura:
    tratada como s = 0, ela recebe σ(b); tratada pelo ponto neutro s = w/2, recebe σ(b + w²/2). A verdade é π."""
    rng = _rng(semente)
    ys = [1.0 if rng.random() < pi else 0.0 for _ in range(n)]
    xs = [d * y + rng.gauss(0, 1) for y in ys]
    b, w = _logistica_newton(xs, ys)
    sig = lambda z: 1 / (1 + exp(-z))
    taxa = sum(ys) / n
    chances = pi / (1 - pi) * exp(-d * d / 2)
    return w, sig(b) / taxa, sig(b + w * w / 2) / taxa, chances / (1 + chances) / pi


def p293_neutro_no_agente(sementes=tuple(range(550, 560)), episodios=400):
    """Na SYNTHAI modular da Parte 22 (mundo sequencial): o peso w₃ que ela aprende para a leitura e a calibração
    das opções que ficaram SEM leitura: P prevista (com leitura 0 e com o neutro w₃/2) contra a taxa real."""
    from synthai import Synthai as SynthaiModular
    from synthai.mundos import MundoSequencial
    pesos, prev0, prevn, reais = [], 0.0, 0.0, 0.0
    for s in sementes:
        mundo = MundoSequencial(s)
        ag = SynthaiModular(s).calibrar(mundo)
        pesos.append(ag.pensamento.w[3])
        decidir = ag.decidir
        soma = [0.0, 0.0, 0.0]

        def decidir_e_medir(sit, _ag=ag, _decidir=decidir, _soma=soma):
            escolha = _decidir(sit)
            pen = _ag.pensamento
            melhor = max(o.comite for o in sit.opcoes)
            for o in sit.opcoes:
                if o._leitura is None:  # a régua lê o escondido; o agente, não
                    _soma[0] += pen.p_catastrofe(o, melhor, 0.0)
                    _soma[1] += pen.p_catastrofe(o, melhor, pen.w[3] / 2)
                    _soma[2] += o._catastrofe
            return escolha
        ag.decidir = decidir_e_medir
        mundo.rodar(ag, episodios)
        prev0, prevn, reais = prev0 + soma[0], prevn + soma[1], reais + soma[2]
    return sum(pesos) / len(pesos), prev0 / reais, prevn / reais, int(reais)


_VARIANTES_23 = {
    "parte22": None,
    "neutro": dict(neutro=True, atencao_inteira=False, memoria=False, thompson=False),
    "atencao": dict(neutro=False, atencao_inteira=True, memoria=False, thompson=False),
    "so_thompson": dict(neutro=False, atencao_inteira=False, memoria=False, thompson=True),
    "reconhecida": dict(neutro=True, atencao_inteira=True, memoria=True, thompson=True),
    "thompson_neutro": dict(neutro=True, atencao_inteira=False, memoria=False, thompson=True),
    "thompson_atencao": dict(neutro=False, atencao_inteira=True, memoria=False, thompson=True),
    "thompson_memoria": dict(neutro=False, atencao_inteira=False, memoria=True, thompson=True),
}


def _agente_23(versao, s):
    from synthai import Synthai as SynthaiModular
    from synthai.reconhecimento import SynthaiReconhecida
    kw = _VARIANTES_23[versao]
    return SynthaiModular(s) if kw is None else SynthaiReconhecida(s, **kw)


def p294_reconhecer(sementes=tuple(range(560, 590)), episodios=400, episodios_unica=1000):
    """30 sementes pareadas. Mundo sequencial: Parte 22 vs neutro, atenção inteira e as duas (reconhecida).
    Escolha única: Parte 22 vs neutro (a atenção inteira não muda nada ali: o bônus de futuro é 0)."""
    from synthai.mundos import MundoSequencial
    resultado = {}
    for tarefa, fazer, n, versoes in (
            ("sequencial", lambda s: MundoSequencial(s), episodios, ("parte22", "neutro", "atencao", "reconhecida")),
            ("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), episodios_unica, ("parte22", "neutro"))):
        ret = {v: [] for v in versoes}
        cats = {v: 0.0 for v in versoes}
        for s in sementes:
            for v in versoes:
                mundo = fazer(s)
                r = mundo.rodar(_agente_23(v, s).calibrar(mundo), n)
                ret[v].append(r["retorno"])
                cats[v] += r["catastrofes"] / len(sementes)
        resultado[tarefa] = ({v: sum(x) / len(x) for v, x in ret.items()}, cats,
                             {v: _pareado(ret["parte22"], ret[v]) for v in versoes if v != "parte22"})
    return resultado


def p295_bandido_reconhecido(sementes=tuple(range(590, 610)), rodadas=20, versoes=("parte22", "so_thompson", "reconhecida")):
    """20 sementes pareadas no bandido: Parte 22 (exploração entregue pelo mundo, UCB) vs Thompson da própria
    SYNTHAI vs a reconhecida inteira. Normalizado (acaso 0, oráculo 1) e arrependimento / referência de Lai–Robbins."""
    from synthai.mundos import MundoBandido
    from synthai.referencias import Acaso, Oraculo
    norm = {v: [] for v in versoes}
    cats = {v: 0.0 for v in versoes}
    razao = {v: 0.0 for v in versoes}
    for s in sementes:
        ref = {}
        for nome, cls in (("acaso", Acaso), ("oraculo", Oraculo)):
            mundo = MundoBandido(s)
            ref[nome] = mundo.rodar(cls(s), rodadas)["retorno"]
        for v in versoes:
            mundo = MundoBandido(s)
            r = mundo.rodar(_agente_23(v, s).calibrar(mundo), rodadas)
            norm[v].append((r["retorno"] - ref["acaso"]) / (ref["oraculo"] - ref["acaso"]))
            cats[v] += r["catastrofes"] / len(sementes)
            dg = mundo.diagnostico
            razao[v] += (dg["teto"] - dg["recompensa"]) / dg["lai_robbins"] / len(sementes)
    return ({v: sum(x) / len(x) for v, x in norm.items()}, cats, razao,
            {v: _pareado(norm[versoes[0]], norm[v]) for v in versoes[1:]})


def p296_ablacao_bandido(sementes=tuple(range(590, 610)), rodadas=20):
    """EXPLORATÓRIO (desenhado depois de ver a P295): Thompson + cada peça da reconhecida, uma de cada vez,
    para achar a que aumenta as catástrofes. Comparações contra 'so_thompson'."""
    return p295_bandido_reconhecido(sementes, rodadas, ("so_thompson", "thompson_neutro", "thompson_atencao",
                                                         "thompson_memoria", "reconhecida"))


def _binomial_cdf(n, p, k):
    """P(Bin(n, p) <= k), somando a massa em escala log."""
    if p <= 0:
        return 1.0
    if p >= 1:
        return 1.0 if k >= n else 0.0
    total = 0.0
    for i in range(k + 1):
        total += exp(lgamma(n + 1) - lgamma(i + 1) - lgamma(n - i + 1) + i * log(p) + (n - i) * log(1 - p))
    return min(1.0, total)


def p297_p42_exato(n_acoes=1000, q=0.01, p_desastre=0.002, bonus=3.0, pontos=4000):
    """A P42 simulou 5000 rodadas. A resposta exata já existia: integrais sobre a mistura
    f(x) = (1-p) φ(x) + p φ(x - 3). Maximizador: n p ∫ φ(x-3) F(x)^(n-1) dx. Quantilizador (k melhores):
    (n p / k) ∫ φ(x-3) P(Bin(n-1, S(x)) <= k-1) dx, com S = 1 - F."""
    from statistics import NormalDist
    nd = NormalDist()
    k = max(1, int(n_acoes * q))
    lo, hi = bonus - 8.0, bonus + 8.0
    h = (hi - lo) / pontos
    soma_max = soma_q = 0.0
    for i in range(pontos + 1):
        x = lo + i * h
        peso = (0.5 if i in (0, pontos) else 1.0) * h * nd.pdf(x - bonus)
        F = (1 - p_desastre) * nd.cdf(x) + p_desastre * nd.cdf(x - bonus)
        soma_max += peso * F ** (n_acoes - 1)
        soma_q += peso * _binomial_cdf(n_acoes - 1, 1 - F, k - 1)
    return n_acoes * p_desastre * soma_max, n_acoes * p_desastre * soma_q / k


# --- Parte 24: o pensamento diferenciado (ajustar até convergir) ---

# Placar acumulado ao fim da Parte 24 (atualizado quando os testes da parte terminam)
ERROS_P309, TESTES_P309 = 59, 133


def p302_convergencia(sementes=tuple(range(620, 630)), treino=150, teste=300, epocas=(3, 10, 30, 100)):
    """Quão longe da convergência está o pensamento de 3 épocas? Mesmo histórico auditado (mundo sequencial):
    gradiente com várias épocas, Newton (máxima verossimilhança) e Newton com Firth. Peso da leitura (w3, d' = 1),
    log-perda no treino e num histórico novo, e o número de catástrofes no treino (eventos raros)."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento import Pensamento
    from synthai.pensamento_exato import ajustar_logistica, dados_do_historico, perda_logistica
    metodos = [f"gradiente_{e}" for e in epocas] + ["newton", "newton_firth"]
    soma = {m: [0.0, 0.0, 0.0] for m in metodos}
    positivos = 0
    for s in sementes:
        mundo = MundoSequencial(s)
        hist = mundo.historico_auditado(treino)
        xs, ys = dados_do_historico(hist)
        xt, yt = dados_do_historico(mundo.historico_auditado(teste))
        positivos += sum(ys)
        pesos = {}
        for e in epocas:
            p = Pensamento()
            p.calibrar(hist, epocas=e)
            pesos[f"gradiente_{e}"] = p.w
        pesos["newton"] = ajustar_logistica(xs, ys, firth=False)
        pesos["newton_firth"] = ajustar_logistica(xs, ys, firth=True)
        for m, w in pesos.items():
            soma[m][0] += w[3] / len(sementes)
            soma[m][1] += perda_logistica(w, xs, ys) / len(sementes)
            soma[m][2] += perda_logistica(w, xt, yt) / len(sementes)
    return {m: tuple(v) for m, v in soma.items()}, positivos / len(sementes)


def _fora_da_atencao(fazer_agente, sementes, episodios=400):
    """A régua da P293 para qualquer agente: P prevista (com leitura 0 e com o neutro w3/2) / taxa real nas opções
    que ficaram sem leitura, mundo sequencial."""
    from synthai.mundos import MundoSequencial
    prev0 = prevn = reais = 0.0
    pesos = []
    for s in sementes:
        mundo = MundoSequencial(s)
        ag = fazer_agente(s).calibrar(mundo)
        pesos.append(ag.pensamento.w[3])
        decidir = ag.decidir
        soma = [0.0, 0.0, 0.0]

        def decidir_e_medir(sit, _ag=ag, _decidir=decidir, _soma=soma):
            escolha = _decidir(sit)
            pen = _ag.pensamento
            melhor = max(o.comite for o in sit.opcoes)
            for o in sit.opcoes:
                if o._leitura is None:  # a régua lê o escondido; o agente, não
                    _soma[0] += pen.p_catastrofe(o, melhor, 0.0)
                    _soma[1] += pen.p_catastrofe(o, melhor, pen.w[3] / 2)
                    _soma[2] += o._catastrofe
            return escolha
        ag.decidir = decidir_e_medir
        mundo.rodar(ag, episodios)
        prev0, prevn, reais = prev0 + soma[0], prevn + soma[1], reais + soma[2]
    return sum(pesos) / len(pesos), prev0 / reais, prevn / reais, int(reais)


def p303_fora_da_atencao_exato(sementes=tuple(range(550, 560))):
    """A P293 de novo (mesmas sementes), com o pensamento de 3 épocas, com Newton e com Newton + Firth."""
    from synthai import SynthaiExploradora
    from synthai.pensamento_exato import SynthaiPensante
    agentes = {"gradiente_3": lambda s: SynthaiExploradora(s),
               "newton": lambda s: SynthaiPensante(s, firth=False),
               "newton_firth": lambda s: SynthaiPensante(s, firth=True)}
    return {nome: _fora_da_atencao(f, sementes) for nome, f in agentes.items()}


def p305_pensante(sementes=tuple(range(630, 660)), sementes_bandido=tuple(range(660, 680))):
    """Comportamento: a versão principal (Parte 23) contra a mesma com o pensamento de Newton + Firth, e com o
    neutro ligado (agora que o peso da leitura deveria estar certo). Três tarefas."""
    from synthai import SynthaiExploradora
    from synthai.mundos import MundoBandido, MundoSequencial
    from synthai.pensamento_exato import SynthaiPensante
    from synthai.referencias import Acaso, Oraculo
    agentes = {"exploradora": lambda s: SynthaiExploradora(s),
               "pensante": lambda s: SynthaiPensante(s),
               "pensante_neutro": lambda s: SynthaiPensante(s, neutro=True)}
    tarefas = (("sequencial", lambda s: MundoSequencial(s), 400, sementes, False),
               ("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), 1000, sementes, False),
               ("bandido", lambda s: MundoBandido(s), 20, sementes_bandido, True))
    resultado = {}
    for tarefa, fazer, n, ss, normalizar in tarefas:
        ret = {v: [] for v in agentes}
        cats = {v: 0.0 for v in agentes}
        for s in ss:
            ref = {}
            if normalizar:
                for nome, cls in (("acaso", Acaso), ("oraculo", Oraculo)):
                    ref[nome] = fazer(s).rodar(cls(s), n)["retorno"]
            for v, f in agentes.items():
                mundo = fazer(s)
                r = mundo.rodar(f(s).calibrar(mundo), n)
                x = r["retorno"]
                if normalizar:
                    x = (x - ref["acaso"]) / (ref["oraculo"] - ref["acaso"])
                ret[v].append(x)
                cats[v] += r["catastrofes"] / len(ss)
        resultado[tarefa] = ({v: sum(x) / len(x) for v, x in ret.items()}, cats,
                             {v: _pareado(ret["exploradora"], ret[v]) for v in agentes if v != "exploradora"})
    return resultado


def p307_selecao(n=400000, b=-3.0, w=1.5, frac_x=0.2, frac_negativos=0.05, semente=307):
    """Auditoria da P273 ('selecionar pelo eixo x não muda a reta de y em x') na logística, com a resposta de
    Prentice e Pyke (1979): selecionar pelo DESFECHO (caso-controle) só desloca o intercepto, de ln(1/fração)."""
    from synthai.pensamento_exato import ajustar_logistica
    rng = _rng(semente)
    dados = []
    for _ in range(n):
        x = rng.gauss(0, 1)
        dados.append((x, 1.0 if rng.random() < 1 / (1 + exp(-(b + w * x))) else 0.0))
    corte = sorted(x for x, _ in dados)[int((1 - frac_x) * n)]
    amostras = {"tudo": dados,
                "seleciona_x": [(x, y) for x, y in dados if x >= corte],
                "caso_controle": [(x, y) for x, y in dados if y == 1.0 or rng.random() < frac_negativos]}
    ajustes = {}
    for nome, d in amostras.items():
        bb, ww = ajustar_logistica([(1.0, x) for x, _ in d], [y for _, y in d], firth=False)
        ajustes[nome] = (bb, ww, len(d))
    return ajustes, log(1 / frac_negativos)


def _autovalores_simetrica(m, varreduras=60):
    """Método de Jacobi: autovalores e autovetores (colunas) de uma matriz simétrica pequena."""
    n = len(m)
    a = [list(l) for l in m]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(varreduras):
        fora = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if fora < 1e-30:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + sqrt(theta * theta + 1))
                c = 1 / sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(n)], v


def p304_teoria_da_convergencia(sementes=tuple(range(620, 630)), treino=150, taxa=0.05, tolerancia=0.01):
    """Por que 3 épocas não bastam (P302), pela conta. Perto do ótimo w*, uma época de gradiente amostra a amostra
    (taxa η, n amostras) age como w ← w* + (I − η n H)(w − w*), H = média de p(1−p) x xᵀ (informação de Fisher por
    amostra). A direção de autovalor λ encolhe por (1 − η n λ) a cada época: as direções lentas mandam.

    Devolve, por semente média: os autovalores de η n H (taxas por época), o número de condição, e as épocas que a
    teoria pede para o erro do peso da leitura (w3) cair abaixo de `tolerancia` partindo do erro que tem depois de
    3 épocas (as direções com η n λ > 1 são tratadas como já convergidas: o gradiente amostra a amostra não diverge
    nelas como o de lote diverge)."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento import Pensamento
    from synthai.pensamento_exato import ajustar_logistica, dados_do_historico
    taxas_med = None
    kappas, epocas_teoria, w3_otimo, positivos = [], [], [], []
    for s in sementes:
        mundo = MundoSequencial(s)
        hist = mundo.historico_auditado(treino)
        xs, ys = dados_do_historico(hist)
        n = len(xs)
        positivos.append(sum(ys))
        w = ajustar_logistica(xs, ys, firth=False)
        k = len(w)
        h = [[0.0] * k for _ in range(k)]
        for x in xs:
            z = sum(wi * xi for wi, xi in zip(w, x))
            p = 1 / (1 + exp(-max(-30.0, min(30.0, z))))
            for i in range(k):
                for j in range(k):
                    h[i][j] += p * (1 - p) * x[i] * x[j] / n
        lam, vet = _autovalores_simetrica(h)
        taxas = sorted(taxa * n * l for l in lam)
        taxas_med = taxas if taxas_med is None else [a + b for a, b in zip(taxas_med, taxas)]
        kappas.append(max(lam) / min(lam))
        g = Pensamento(taxa)
        g.calibrar(hist, epocas=3)
        erro = [gi - wi for gi, wi in zip(g.w, w)]
        # componentes do erro nos autovetores; as direções rápidas (η n λ > 1) já convergiram
        comp = [(taxa * n * lam[c], sum(vet[i][c] * erro[i] for i in range(k)), vet[3][c]) for c in range(k)]
        e = 0
        while e < 100000:
            w3_erro = sum(cc * v3 * (1 - r) ** e for r, cc, v3 in comp if r <= 1.0)
            if abs(w3_erro) < tolerancia:
                break
            e += 1
        epocas_teoria.append(3 + e)
        w3_otimo.append(w[3])
    m = len(sementes)
    return ([t / m for t in taxas_med], sorted(kappas)[m // 2], sorted(epocas_teoria), sum(w3_otimo) / m,
            sum(positivos) / m)


def p304b_conferir_epocas(epocas, sementes=tuple(range(620, 630)), treino=150):
    """Roda o gradiente com o número de épocas que a teoria pediu e mede |w3 − w3*| médio."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento import Pensamento
    from synthai.pensamento_exato import ajustar_logistica, dados_do_historico
    erros = []
    for s in sementes:
        hist = MundoSequencial(s).historico_auditado(treino)
        xs, ys = dados_do_historico(hist)
        w = ajustar_logistica(xs, ys, firth=False)
        g = Pensamento()
        g.calibrar(hist, epocas=epocas)
        erros.append(abs(g.w[3] - w[3]))
    return sum(erros) / len(erros), max(erros)


def p304c_piso_de_ruido(taxa=0.01, epocas=1000, sementes=tuple(range(620, 630)), treino=150):
    """O gradiente amostra a amostra com taxa fixa não converge: oscila num piso. Cada catástrofe do histórico
    empurra w3 por η (1 − p) s, com E|s| ≈ 1,17 para d' = 1; o piso deve escalar com η. Mede |w3 − w3*| médio
    com outra taxa e épocas suficientes para a direção lenta (η n λ_min ≈ 0,034 η/0,05 por época)."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento import Pensamento
    from synthai.pensamento_exato import ajustar_logistica, dados_do_historico
    erros = []
    for s in sementes:
        hist = MundoSequencial(s).historico_auditado(treino)
        xs, ys = dados_do_historico(hist)
        w = ajustar_logistica(xs, ys, firth=False)
        g = Pensamento(taxa)
        g.calibrar(hist, epocas=epocas)
        erros.append(abs(g.w[3] - w[3]))
    return sum(erros) / len(erros), max(erros)


def p304d_vies_de_primeira_ordem(sementes=tuple(range(620, 630)), treino=150):
    """O viés O(1/n) da máxima verossimilhança logística tem forma fechada (Cordeiro e McCullagh, 1991): um passo
    de Newton do escore de Firth a partir do ótimo, δ = I⁻¹ Σ h_i (½ − p_i) x_i, com h_i a alavanca. Compara δ3 com a
    diferença Firth − máxima verossimilhança no peso da leitura."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento_exato import _inversa, ajustar_logistica, dados_do_historico
    d_formula = d_firth = 0.0
    for s in sementes:
        xs, ys = dados_do_historico(MundoSequencial(s).historico_auditado(treino))
        w = ajustar_logistica(xs, ys, firth=False)
        wf = ajustar_logistica(xs, ys, firth=True)
        k = len(w)
        ps = [1 / (1 + exp(-max(-30.0, min(30.0, sum(a * b for a, b in zip(w, x)))))) for x in xs]
        info = [[sum(p * (1 - p) * x[i] * x[j] for x, p in zip(xs, ps)) for j in range(k)] for i in range(k)]
        inv = _inversa(info)
        u = [0.0] * k
        for x, p in zip(xs, ps):
            h = p * (1 - p) * sum(x[i] * sum(inv[i][j] * x[j] for j in range(k)) for i in range(k))
            for i in range(k):
                u[i] += h * (0.5 - p) * x[i]
        delta = [sum(inv[i][j] * u[j] for j in range(k)) for i in range(k)]
        d_formula += delta[3] / len(sementes)
        d_firth += (wf[3] - w[3]) / len(sementes)
    return d_formula, d_firth


def p305b_onde_se_decide(sementes=tuple(range(630, 640)), episodios=1000, topo=10):
    """EXPLORATÓRIO (desenhado depois de ver a P305): calibração do pensamento ONDE a decisão acontece. Mundo de
    escolha única: nas `topo` opções de nota pessimista mais alta (as candidatas e as primeiras de reserva), P
    prevista / taxa real de catástrofe; e, em todas as opções, a mesma razão. Mais perguntas e catástrofes, e,
    entre as opções do topo que ela aceitaria SEM perguntar (p <= limiar), a fração, a P média e a taxa real."""
    from synthai import SynthaiExploradora
    from synthai.mundos import MundoSequencial
    from synthai.pensamento_exato import SynthaiPensante
    resultado = {}
    for nome, fazer in (("gradiente_3", lambda s: SynthaiExploradora(s)), ("newton_firth", lambda s: SynthaiPensante(s))):
        soma = {"topo_prev": 0.0, "topo_real": 0.0, "todas_prev": 0.0, "todas_real": 0.0,
                "abaixo_n": 0.0, "abaixo_prev": 0.0, "abaixo_real": 0.0}
        perguntas = cats = 0.0
        for s in sementes:
            mundo = MundoSequencial(s, passos=1, n_acoes=200)
            ag = fazer(s).calibrar(mundo)
            pen = ag.pensamento

            def medir(sit, _decidir=ag.decidir, _pen=pen):
                ordem = sorted(sit.opcoes, key=lambda o: -(o.nota - o.discordancia))
                escolha = _decidir(sit)
                melhor = max(o.comite for o in sit.opcoes)
                for i, o in enumerate(ordem):
                    leitura = o._leitura if o._leitura is not None else 0.0  # a régua lê o escondido
                    p = _pen.p_catastrofe(o, melhor, leitura)
                    soma["todas_prev"] += p
                    soma["todas_real"] += o._catastrofe
                    if i < topo:
                        soma["topo_prev"] += p
                        soma["topo_real"] += o._catastrofe
                        if p <= ag.relacao.limiar:  # o que ela aceitaria sem perguntar
                            soma["abaixo_n"] += 1
                            soma["abaixo_prev"] += p
                            soma["abaixo_real"] += o._catastrofe
                return escolha
            ag.decidir = medir
            r = mundo.rodar(ag, episodios)
            perguntas += r["perguntas"] / len(sementes)
            cats += r["catastrofes"] / len(sementes)
        n_topo = len(sementes) * episodios * topo
        resultado[nome] = (soma["topo_prev"] / soma["topo_real"], soma["todas_prev"] / soma["todas_real"],
                           soma["topo_real"] / n_topo, perguntas, cats, soma["abaixo_n"] / n_topo,
                           soma["abaixo_prev"] / max(1.0, soma["abaixo_n"]), soma["abaixo_real"] / max(1.0, soma["abaixo_n"]))
    return resultado


def p306_newton_quadratico(semente=620, treino=150):
    """Convergência quadrática de Newton, contada: o tamanho do passo a cada iteração e a razão
    log(passo_k+1)/log(passo_k), que tende a 2 quando o número de dígitos certos dobra."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento_exato import ajustar_logistica, dados_do_historico
    xs, ys = dados_do_historico(MundoSequencial(semente).historico_auditado(treino))
    w_final = ajustar_logistica(xs, ys, firth=False, iteracoes=40)
    erros = []
    for it in range(1, 12):
        w = ajustar_logistica(xs, ys, firth=False, iteracoes=it)
        erros.append(max(abs(a - b) for a, b in zip(w, w_final)))
    return erros


def p308_informacao(sementes=tuple(range(620, 630)), treino=150, teste=300):
    """A log-perda em bits: entropia da catástrofe (sem olhar nada), o que as variáveis explicam (Newton) e o que o
    gradiente de 3 épocas deixa na mesa. Tudo no histórico de teste."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento import Pensamento
    from synthai.pensamento_exato import ajustar_logistica, dados_do_historico, perda_logistica
    h0 = hn = hg = 0.0
    for s in sementes:
        mundo = MundoSequencial(s)
        hist = mundo.historico_auditado(treino)
        xs, ys = dados_do_historico(hist)
        xt, yt = dados_do_historico(mundo.historico_auditado(teste))
        pi = sum(ys) / len(ys)
        h0 += perda_logistica([log(pi / (1 - pi)), 0, 0, 0], xt, yt) / log(2) / len(sementes)
        hn += perda_logistica(ajustar_logistica(xs, ys, firth=False), xt, yt) / log(2) / len(sementes)
        g = Pensamento()
        g.calibrar(hist)
        hg += perda_logistica(g.w, xt, yt) / log(2) / len(sementes)
    return h0, hn, hg


# --- Parte 25: o sentimento que acompanha o pensamento (o limiar certo para cada pensamento) ---

# Placar acumulado ao fim da Parte 25 (atualizado quando os testes da parte terminam)
ERROS_P319, TESTES_P319 = 68, 148

_P_EXATO_P287 = 0.00324  # limiar com o custo do veto falso (P287), em P(catástrofe)


def _agente_25(modelo, s, mult=2.0):
    from synthai import SynthaiExploradora
    from synthai.limiar import SynthaiAjustada
    from synthai.relacao import Relacao
    if modelo == "gradiente":
        ag = SynthaiExploradora(s)
        ag.relacao = Relacao(mult=mult, carga_alvo=ag.relacao.carga_alvo)
        return ag
    return SynthaiAjustada(s, mult=mult, local=(modelo == "local"))


def p312_limiar_pela_conta(sementes=tuple(range(640, 650)), episodios=300, orcamento=0.3, q=0.05):
    """O limiar previsto pela conta, antes de qualquer varredura. Mundo de escolha única. Depois de calibrar cada
    pensamento, sorteia episódios auditados novos e calcula p em cada candidata (as 5% de nota pessimista mais alta;
    o sensor delas é lido). Pergunta-se quando p > t (e p <= 0,5). Com orçamento de 0,3 pergunta por episódio, a
    relaxação de Lagrange dá t no quantil (1 − 0,3) de p numa candidata ao acaso; sem orçamento apertado, o limiar
    é o da P287 (com o veto falso). Multiplicador previsto: m = max(P_exato, t_0,3) / P*.

    Devolve, por pensamento: m previsto, e entre as candidatas que ficariam abaixo do limiar atual (2 P*) a fração,
    a P média e a taxa real (a calibração onde a SYNTHAI aceita sem perguntar)."""
    from synthai.mundos import MundoSequencial
    p_estrela = p71_valor_da_pergunta()
    resultado = {}
    for modelo in ("gradiente", "newton", "local"):
        ps, abaixo = [], [0, 0.0, 0.0]
        for s in sementes:
            mundo = MundoSequencial(s, passos=1, n_acoes=200)
            ag = _agente_25(modelo, s).calibrar(mundo)
            for ep in mundo.historico_auditado(episodios):
                melhor = max(o.comite for o, _, _ in ep)
                ordem = sorted(ep, key=lambda t: -(t[0].nota - t[0].discordancia))
                for o, rotulo, leitura in ordem[: max(1, int(q * len(ordem)))]:
                    p = ag.pensamento.p_catastrofe(o, melhor, leitura)
                    if p <= 0.5:
                        ps.append(p)
                    if p <= 2 * p_estrela:
                        abaixo[0] += 1
                        abaixo[1] += p
                        abaixo[2] += rotulo
        ps.sort()
        t = ps[int((1 - orcamento) * len(ps))]
        n = abaixo[0]
        resultado[modelo] = (max(_P_EXATO_P287, t) / p_estrela, t, n / len(ps), abaixo[1] / max(1, n), abaixo[2] / max(1, n))
    return resultado


def p313_varredura(sementes=tuple(range(640, 650)), mults=(0.5, 1.0, 2.0, 4.0, 8.0), episodios=1000):
    """Varre o multiplicador do limiar para cada pensamento, mundo de escolha única. O pensamento é calibrado uma
    vez por semente e copiado (o mundo de cada execução avança o mesmo histórico, para os números serem os mesmos de
    uma calibração nova)."""
    from synthai.mundos import MundoSequencial
    resultado = {}
    for modelo in ("gradiente", "newton", "local"):
        ret = {m: [] for m in mults}
        cats = {m: 0.0 for m in mults}
        perg = {m: 0.0 for m in mults}
        for s in sementes:
            pesos = _agente_25(modelo, s).calibrar(MundoSequencial(s, passos=1, n_acoes=200)).pensamento.w
            for m in mults:
                mundo = MundoSequencial(s, passos=1, n_acoes=200)
                mundo.historico_auditado(150)  # o mesmo avanço do gerador que a calibração faria
                ag = _agente_25(modelo, s, m)
                ag.pensamento.w = list(pesos)
                r = mundo.rodar(ag, episodios)
                ret[m].append(r["retorno"])
                cats[m] += r["catastrofes"] / len(sementes)
                perg[m] += r["perguntas"] / len(sementes)
        medias = {m: sum(v) / len(v) for m, v in ret.items()}
        resultado[modelo] = (medias, cats, perg, max(medias, key=medias.get))
    return resultado


def p314_custo_do_descarte(sementes=tuple(range(640, 650)), episodios=1000):
    """CONTA POSTERIOR (feita depois de ver a P313): com orçamento esgotado, a escolha não é perguntar ou aceitar, é
    aceitar ou DESCARTAR. Aceitar custa p L; descartar custa Δd, o valor que se perde ao passar para a próxima
    candidata. O limiar entre os dois é p = Δd / L, ou m = Δd / (L P*). Mede Δd na SYNTHAI com Newton (m = 2):
    valor da opção descartada (ou vetada) menos o da escolhida, só nas descartadas seguras."""
    from synthai.mundos import MundoSequencial
    difs = []
    for s in sementes:
        mundo = MundoSequencial(s, passos=1, n_acoes=200)
        ag = _agente_25("newton", s).calibrar(mundo)
        rel = ag.relacao
        vistas = []
        pode = rel.pode_perguntar

        def pode_e_anota(opcao, sit, _pode=pode, _vistas=vistas):
            r = _pode(opcao, sit)
            if not r:
                _vistas.append(opcao)  # descartada por falta de orçamento
            return r
        rel.pode_perguntar = pode_e_anota

        def decidir(sit, _decidir=ag.decidir, _vistas=vistas):
            del _vistas[:]
            escolha = _decidir(sit)
            for o in _vistas:  # a régua lê o escondido
                if not o._catastrofe:
                    difs.append(o._valor - escolha._valor)
            return escolha
        ag.decidir = decidir
        mundo.rodar(ag, episodios)
    dd = sum(difs) / len(difs)
    return len(difs), dd, dd / (50.0 * p71_valor_da_pergunta())


def p315_limiar_no_comportamento(sementes=tuple(range(650, 680)), sementes_bandido=tuple(range(680, 700))):
    """Sementes NOVAS (as da varredura foram 640-649). A principal (gradiente, 2P*) contra: o gradiente no melhor
    da varredura (4P*), Newton no melhor (0,5P*) e o local no melhor (1P*). Três tarefas."""
    from synthai.mundos import MundoBandido, MundoSequencial
    from synthai.referencias import Acaso, Oraculo
    agentes = {"principal": ("gradiente", 2.0), "gradiente_m4": ("gradiente", 4.0),
               "newton_m05": ("newton", 0.5), "local_m1": ("local", 1.0)}
    tarefas = (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), 1000, sementes, False),
               ("sequencial", lambda s: MundoSequencial(s), 400, sementes, False),
               ("bandido", lambda s: MundoBandido(s), 20, sementes_bandido, True))
    resultado = {}
    for tarefa, fazer, n, ss, normalizar in tarefas:
        ret = {v: [] for v in agentes}
        cats = {v: 0.0 for v in agentes}
        for s in ss:
            ref = {}
            if normalizar:
                for nome, cls in (("acaso", Acaso), ("oraculo", Oraculo)):
                    ref[nome] = fazer(s).rodar(cls(s), n)["retorno"]
            for v, (modelo, m) in agentes.items():
                mundo = fazer(s)
                r = mundo.rodar(_agente_25(modelo, s, m).calibrar(mundo), n)
                x = r["retorno"]
                if normalizar:
                    x = (x - ref["acaso"]) / (ref["oraculo"] - ref["acaso"])
                ret[v].append(x)
                cats[v] += r["catastrofes"] / len(ss)
        resultado[tarefa] = ({v: sum(x) / len(x) for v, x in ret.items()}, cats,
                             {v: _pareado(ret["principal"], ret[v]) for v in agentes if v != "principal"})
    return resultado


def p315b_confirmacao(sementes=tuple(range(720, 750))):
    """Confirmação em mais 30 sementes novas (720-749): principal (gradiente, 2P*) contra Newton com 0,5P*, na escolha
    única e no sequencial. Devolve as diferenças por tarefa e a combinação de Stouffer dos dois t."""
    from synthai.mundos import MundoSequencial
    resultado = {}
    for tarefa, fazer, n in (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), 1000),
                             ("sequencial", lambda s: MundoSequencial(s), 400)):
        ret = {v: [] for v in ("principal", "newton_m05")}
        cats = {v: 0.0 for v in ret}
        for s in sementes:
            for v, (modelo, m) in (("principal", ("gradiente", 2.0)), ("newton_m05", ("newton", 0.5))):
                mundo = fazer(s)
                r = mundo.rodar(_agente_25(modelo, s, m).calibrar(mundo), n)
                ret[v].append(r["retorno"])
                cats[v] += r["catastrofes"] / len(sementes)
        resultado[tarefa] = (cats, _pareado(ret["principal"], ret["newton_m05"]))
    z = sum(r[1][2] for r in resultado.values()) / sqrt(len(resultado))
    return resultado, z


def p316_conta_tres_acoes(modelo, fazer, sementes, episodios, mult=2.0):
    """A conta das três ações (aceitar, perguntar, descartar), com tudo medido no próprio agente rodando com o limiar
    atual (2P*): Δd = valor perdido ao descartar uma candidata segura (falta de orçamento) e o fator de calibração
    f = taxa real / P prevista nas candidatas que o pensamento põe abaixo do limiar. Aceitar vale a pena se o risco
    VERDADEIRO f·p·L for menor que Δd, então o multiplicador previsto é m = Δd / (f · L · P*)."""
    difs = []
    abaixo = [0.0, 0.0]
    for s in sementes:
        mundo = fazer(s)
        ag = _agente_25(modelo, s, mult).calibrar(mundo)
        rel, pen = ag.relacao, ag.pensamento
        descartadas = []
        pode = rel.pode_perguntar

        def pode_e_anota(opcao, sit, _pode=pode, _d=descartadas):
            r = _pode(opcao, sit)
            if not r:
                _d.append(opcao)
            return r
        rel.pode_perguntar = pode_e_anota
        p_cat = pen.p_catastrofe

        def p_e_anota(opcao, melhor, leitura=0.0, _p=p_cat, _lim=rel.limiar):
            p = _p(opcao, melhor, leitura)
            if p <= _lim:  # a régua lê o escondido
                abaixo[0] += p
                abaixo[1] += opcao._catastrofe
            return p
        pen.p_catastrofe = p_e_anota

        def decidir(sit, _decidir=ag.decidir, _d=descartadas):
            del _d[:]
            escolha = _decidir(sit)
            for o in _d:
                if not o._catastrofe:
                    difs.append(o._valor - escolha._valor)
            return escolha
        ag.decidir = decidir
        mundo.rodar(ag, episodios)
    dd = sum(difs) / len(difs)
    f = abaixo[1] / abaixo[0]
    return len(difs), dd, f, dd / (f * 50.0 * p71_valor_da_pergunta())


def p316_conta_nos_mundos():
    """A conta das três ações para os três pensamentos: no mundo de escolha única (sementes 640-649, as da varredura
    P313: conta posterior) e no sequencial (sementes 700-709: conta ANTES da varredura P317)."""
    from synthai.mundos import MundoSequencial
    mundos = (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), tuple(range(640, 650)), 1000),
              ("sequencial", lambda s: MundoSequencial(s), tuple(range(700, 710)), 400))
    return {(nome, modelo): p316_conta_tres_acoes(modelo, fazer, ss, n)
            for nome, fazer, ss, n in mundos for modelo in ("gradiente", "newton", "local")}


def p318_ponto_fixo(modelo, fazer, sementes, episodios, m0=2.0, iteracoes=4):
    """A conta das três ações como ponto fixo: mede Δd e f com o limiar em m, calcula m' = Δd / (f L P*), e repete com
    m'. Devolve a sequência de multiplicadores."""
    ms = [m0]
    for _ in range(iteracoes):
        ms.append(p316_conta_tres_acoes(modelo, fazer, sementes, episodios, ms[-1])[3])
    return ms


def p318_ponto_fixo_nos_mundos(sementes=tuple(range(710, 720))):
    """O ponto fixo no mundo sequencial com catástrofes ×2 (p_cat = 0,01), um mundo ainda não varrido."""
    from synthai.mundos import MundoSequencial
    fazer = lambda s: MundoSequencial(s, p_cat=0.01)
    return {modelo: p318_ponto_fixo(modelo, fazer, sementes, 400) for modelo in ("gradiente", "newton", "local")}


def p318b_varredura_catastrofe_x2(sementes=tuple(range(710, 720)), mults=(0.5, 1.0, 2.0, 4.0, 8.0)):
    """A varredura no mundo sequencial com catástrofes ×2 (mesma mecânica da P317)."""
    from synthai.mundos import MundoSequencial
    resultado = {}
    for modelo in ("gradiente", "newton", "local"):
        ret = {m: [] for m in mults}
        cats = {m: 0.0 for m in mults}
        for s in sementes:
            pesos = _agente_25(modelo, s).calibrar(MundoSequencial(s, p_cat=0.01)).pensamento.w
            for m in mults:
                mundo = MundoSequencial(s, p_cat=0.01)
                mundo.historico_auditado(150)
                ag = _agente_25(modelo, s, m)
                ag.pensamento.w = list(pesos)
                r = mundo.rodar(ag, 400)
                ret[m].append(r["retorno"])
                cats[m] += r["catastrofes"] / len(sementes)
        medias = {m: sum(v) / len(v) for m, v in ret.items()}
        resultado[modelo] = (medias, cats, max(medias, key=medias.get))
    return resultado


def p317_varredura_sequencial(sementes=tuple(range(700, 710)), mults=(0.5, 1.0, 2.0, 4.0, 8.0), episodios=400):
    """A varredura da P313 no mundo sequencial (calibração copiada, como lá)."""
    from synthai.mundos import MundoSequencial
    resultado = {}
    for modelo in ("gradiente", "newton", "local"):
        ret = {m: [] for m in mults}
        cats = {m: 0.0 for m in mults}
        for s in sementes:
            pesos = _agente_25(modelo, s).calibrar(MundoSequencial(s)).pensamento.w
            for m in mults:
                mundo = MundoSequencial(s)
                mundo.historico_auditado(150)
                ag = _agente_25(modelo, s, m)
                ag.pensamento.w = list(pesos)
                r = mundo.rodar(ag, episodios)
                ret[m].append(r["retorno"])
                cats[m] += r["catastrofes"] / len(sementes)
        medias = {m: sum(v) / len(v) for m, v in ret.items()}
        resultado[modelo] = (medias, cats, max(medias, key=medias.get))
    return resultado


# --- Parte 26: a constante que faltava (os termos da conta das três ações, um por um) ---

# Placar acumulado ao fim da Parte 26 (atualizado quando os testes da parte terminam)
ERROS_P329, TESTES_P329 = 70, 155


def p322_termos_da_conta(modelo, fazer, sementes, episodios=400, mult=2.0):
    """Mede, no agente rodando com o limiar mult·P*, cada termo da conta m = Δd / (f L P*) em duas versões:

    - L: a perda fixa (50) e a perda EFETIVA L_ef = 50 + F(t), em que F(t) é o retorno que o episódio ainda daria a
      partir do passo t (média dos episódios sem catástrofe, por passo), ponderado pelos passos em que as catástrofes
      acontecem;
    - Δd: só o valor do passo (P316) e o valor com o plano, valor + consequência × passos restantes;
    - f: real/previsto em TODAS as opções que o pensamento pôs abaixo do limiar (P316) e só nas que ele ACEITOU.

    Devolve os termos e os multiplicadores das combinações."""
    p_estrela = p71_valor_da_pergunta()
    dd_v, dd_p = [], []
    abaixo_todas, abaixo_aceitas = [0.0, 0.0], [0.0, 0.0]
    futuro = None
    passos_cat = []
    for s in sementes:
        mundo = fazer(s)
        ag = _agente_25(modelo, s, mult).calibrar(mundo)
        rel, pen = ag.relacao, ag.pensamento
        estado = {"descartadas": [], "ganhos": [], "restantes": 0, "ps": {}}
        pode = rel.pode_perguntar

        def pode_e_anota(opcao, sit, _pode=pode, _e=estado):
            r = _pode(opcao, sit)
            if not r:
                _e["descartadas"].append(opcao)
            return r
        rel.pode_perguntar = pode_e_anota
        p_cat = pen.p_catastrofe

        def p_e_anota(opcao, melhor, leitura=0.0, _p=p_cat, _lim=rel.limiar, _e=estado):
            p = _p(opcao, melhor, leitura)
            _e["ps"][id(opcao)] = p
            if p <= _lim:  # a régua lê o escondido
                abaixo_todas[0] += p
                abaixo_todas[1] += opcao._catastrofe
            return p
        pen.p_catastrofe = p_e_anota

        def decidir(sit, _decidir=ag.decidir, _e=estado, _lim=rel.limiar):
            _e["descartadas"] = []
            _e["ps"] = {}
            escolha = _decidir(sit)
            r = sit.restantes
            plano = lambda o: o._valor + o._consequencia * r
            for o in _e["descartadas"]:
                if not o._catastrofe:
                    dd_v.append(o._valor - escolha._valor)
                    dd_p.append(plano(o) - plano(escolha))
            p = _e["ps"].get(id(escolha))
            if p is not None and p <= _lim:
                abaixo_aceitas[0] += p
                abaixo_aceitas[1] += escolha._catastrofe
            _e["restantes"] = r
            return escolha
        ag.decidir = decidir
        observar = ag.observar
        passos = mundo.m["passos"]
        soma_fut = [0.0] * passos
        n_fut = [0] * passos

        def observar_e_anota(res, _obs=observar, _e=estado):
            t = passos - 1 - _e["restantes"]
            if res.catastrofe:
                passos_cat.append(t)
                _e["ganhos"] = []
            else:
                _e["ganhos"].append(res.valor_recebido)
                if _e["restantes"] == 0:  # episódio completo: o retorno a partir de cada passo
                    g = _e["ganhos"]
                    for k in range(len(g)):
                        soma_fut[k] += sum(g[k:])
                        n_fut[k] += 1
                    _e["ganhos"] = []
            return _obs(res)
        ag.observar = observar_e_anota
        mundo.rodar(ag, episodios)
        f_t = [a / b if b else 0.0 for a, b in zip(soma_fut, n_fut)]
        futuro = f_t if futuro is None else [x + y for x, y in zip(futuro, f_t)]
    futuro = [x / len(sementes) for x in futuro]
    L = 50.0
    L_ef = L + sum(futuro[t] for t in passos_cat) / max(1, len(passos_cat))
    dv, dp = sum(dd_v) / len(dd_v), sum(dd_p) / len(dd_p)
    f_todas = abaixo_todas[1] / abaixo_todas[0] if abaixo_todas[0] else float("nan")
    f_aceitas = abaixo_aceitas[1] / abaixo_aceitas[0] if abaixo_aceitas[0] else float("nan")
    m = lambda d, f, l: d / (f * l * p_estrela) if f > 0 else float("nan")
    return {"L_ef": L_ef, "dd_valor": dv, "dd_plano": dp, "f_todas": f_todas, "f_aceitas": f_aceitas,
            "n_descartes": len(dd_v), "n_cats": len(passos_cat),
            "m_P316": m(dv, f_todas, L), "m_L": m(dv, f_todas, L_ef), "m_plano": m(dp, f_todas, L),
            "m_aceitas": m(dv, f_aceitas, L), "m_tudo": m(dp, f_aceitas, L_ef)}


def p322_termos_nos_mundos():
    """Os termos nos dois mundos sequenciais já varridos (P317: sementes 700-709; P318b: 710-719, catástrofes ×2) e
    no de escolha única (P313: 640-649), para os três pensamentos."""
    from synthai.mundos import MundoSequencial
    mundos = (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), tuple(range(640, 650)), 1000),
              ("sequencial", lambda s: MundoSequencial(s), tuple(range(700, 710)), 400),
              ("catástrofe x2", lambda s: MundoSequencial(s, p_cat=0.01), tuple(range(710, 720)), 400))
    return {(nome, modelo): p322_termos_da_conta(modelo, fazer, ss, n)
            for nome, fazer, ss, n in mundos for modelo in ("gradiente", "newton", "local")}


MUNDOS_NOVOS_26 = {"modelo ruim": ({"sigma_modelo": 2.0}, tuple(range(750, 760))),
                   "humano frágil": ({"fadiga": 0.6}, tuple(range(760, 770)))}


def p323_conta_nos_mundos_novos():
    """A conta corrigida (L efetivo e Δd com o plano) em dois mundos sequenciais ainda não varridos."""
    from synthai.mundos import MundoSequencial
    return {(nome, modelo): p322_termos_da_conta(modelo, lambda s, kw=kw: MundoSequencial(s, **kw), ss)["m_tudo"]
            for nome, (kw, ss) in MUNDOS_NOVOS_26.items() for modelo in ("gradiente", "newton", "local")}


def p324_varredura_nos_mundos_novos(mults=(0.5, 1.0, 2.0, 4.0, 8.0)):
    """A varredura (mecânica da P317) nos dois mundos novos."""
    from synthai.mundos import MundoSequencial
    resultado = {}
    for nome, (kw, ss) in MUNDOS_NOVOS_26.items():
        for modelo in ("gradiente", "newton", "local"):
            ret = {m: [] for m in mults}
            cats = {m: 0.0 for m in mults}
            for s in ss:
                pesos = _agente_25(modelo, s).calibrar(MundoSequencial(s, **kw)).pensamento.w
                for m in mults:
                    mundo = MundoSequencial(s, **kw)
                    mundo.historico_auditado(150)
                    ag = _agente_25(modelo, s, m)
                    ag.pensamento.w = list(pesos)
                    r = mundo.rodar(ag, 400)
                    ret[m].append(r["retorno"])
                    cats[m] += r["catastrofes"] / len(ss)
            medias = {m: sum(v) / len(v) for m, v in ret.items()}
            resultado[(nome, modelo)] = (medias, cats, max(medias, key=medias.get))
    return resultado


def p325_chance(conta=((5.811, 8.0), (0.755, 0.5), (3.134, 2.0), (7.491, 4.0), (0.995, 1.0), (2.077, 2.0)),
                ingenuo=(4.0, 0.5, 1.0, 4.0, 0.5, 1.0), grade=(0.5, 1.0, 2.0, 4.0, 8.0)):
    """Qual a chance de acertar a P324 por sorte? Cada caso: (m da conta, ótimo da varredura). Uma faixa 'a um fator 2
    da conta' cobre k pontos da grade de 5; ao acaso, acerta com probabilidade k/5. Compara com um preditor ingênuo
    que repete o ótimo do mundo sequencial da P317 (gradiente 4, Newton 0,5, local 1), cuja faixa cobre 2 ou 3 pontos.
    Devolve, para os dois: acertos, a chance de acertar tantos ou mais ao acaso, os bits de especificidade
    (−log2 da chance de todos os acertos ao acaso) e a distância média |log2(previsto/ótimo)|."""
    def avaliar(previstos, otimos):
        faixas = [[g for g in grade if abs(log2(g / p)) <= 1] for p in previstos]
        acertos = [o in f for f, o in zip(faixas, otimos)]
        ps = [len(f) / len(grade) for f in faixas]
        # chance de >= tantos acertos ao acaso (soma sobre subconjuntos: distribuição de Poisson-binomial)
        dist = [1.0]
        for q in ps:
            dist = [a * (1 - q) + (dist[i - 1] * q if i else 0.0) for i, a in enumerate(dist + [0.0])]
        k = sum(acertos)
        chance = sum(dist[k:])
        bits = -sum(log2(q) for q in ps)
        dist_media = sum(abs(log2(p / o)) for p, o in zip(previstos, otimos)) / len(otimos)
        return k, chance, bits, dist_media
    otimos = [o for _, o in conta]
    return avaliar([p for p, _ in conta], otimos), avaliar(list(ingenuo), otimos)


# --- Parte 27: a autorregulação (a SYNTHAI calcula o próprio limiar) ---

# Placar acumulado ao fim da Parte 27 (atualizado quando os testes da parte terminam)
ERROS_P339, TESTES_P339 = 76, 164


def p332_estimadores_proprios(sementes=tuple(range(700, 710)), episodios=400):
    """A SYNTHAI com Newton e limiar FIXO em 2P* (autorregulação desligada), nas sementes da P322 (mundo sequencial):
    os termos que ela estima sozinha (só com o que observa) contra os da régua (P322). Mesmo agente, mesmas sementes:
    as escolhas são as mesmas da P322."""
    from synthai.autorregulacao import SynthaiAutorregulada
    from synthai.mundos import MundoSequencial
    soma = [0.0, 0.0, 0.0, 0.0, 0.0]
    for s in sementes:
        mundo = MundoSequencial(s)
        ag = SynthaiAutorregulada(s, aquecimento=10 ** 9).calibrar(mundo)
        mundo.rodar(ag, episodios)
        l_ef, f, dd, b = ag.termos()
        m = dd / (f * l_ef * ag.p_estrela)
        for i, x in enumerate((l_ef, f, dd, b, m)):
            soma[i] += x / len(sementes)
    return tuple(soma)


def p333_autorregulada(sementes=tuple(range(770, 800))):
    """30 sementes NOVAS. Principal (gradiente, 2P* fixo) contra: a autorregulada com o pensamento de gradiente, a
    autorregulada com Newton, e Newton com o limiar fixo no ótimo das varreduras (0,5P*, a referência 'que já sabia').
    Três mundos: escolha única, sequencial e sequencial com modelo ruim (σ = 2)."""
    from synthai import SynthaiExploradora
    from synthai.autorregulacao import SynthaiAutorregulada
    from synthai.limiar import SynthaiAjustada
    from synthai.mundos import MundoSequencial
    agentes = {"principal": lambda s: SynthaiExploradora(s),
               "auto_gradiente": lambda s: SynthaiAutorregulada(s, newton=False),
               "auto_newton": lambda s: SynthaiAutorregulada(s),
               "newton_m05": lambda s: SynthaiAjustada(s, mult=0.5)}
    tarefas = (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), 1000),
               ("sequencial", lambda s: MundoSequencial(s), 400),
               ("modelo ruim", lambda s: MundoSequencial(s, sigma_modelo=2.0), 400))
    resultado = {}
    for tarefa, fazer, n in tarefas:
        ret = {v: [] for v in agentes}
        cats = {v: 0.0 for v in agentes}
        ms = {v: 0.0 for v in agentes}
        for s in sementes:
            for v, f in agentes.items():
                mundo = fazer(s)
                ag = f(s).calibrar(mundo)
                r = mundo.rodar(ag, n)
                ret[v].append(r["retorno"])
                cats[v] += r["catastrofes"] / len(sementes)
                ms[v] += ag.relacao.limiar / p71_valor_da_pergunta() / len(sementes)  # o multiplicador no fim
        resultado[tarefa] = ({v: sum(x) / len(x) for v, x in ret.items()}, cats, ms,
                             {v: _pareado(ret["principal"], ret[v]) for v in agentes if v != "principal"},
                             _pareado(ret["newton_m05"], ret["auto_newton"]))
    return resultado


# --- Parte 28: a âncora (pessimismo sob incerteza e a realidade de fora) ---

# Placar acumulado ao fim da Parte 28 (atualizado quando os testes da parte terminam)
ERROS_P349, TESTES_P349 = 78, 170

_VARIANTES_28 = {"media": dict(z=0.0, auditoria=False), "quantil": dict(z=0.8416, auditoria=False),
                 "auditoria": dict(z=0.0, auditoria=True), "auditoria_quantil": dict(z=0.8416, auditoria=True)}


def p342_conta_da_ancora(sementes=tuple(range(700, 710)), episodios=400):
    """A CONTA antes da previsão (regra da Parte 27): com a autorregulação desligada (limiar fixo em 2P*, as mesmas
    escolhas da P332), o f e o m que cada âncora daria no fim, por semente, mundo sequencial. 'media' reproduz a P332."""
    from synthai.ancora import SynthaiComAncora
    from synthai.mundos import MundoSequencial
    resultado = {}
    for nome, kw in _VARIANTES_28.items():
        fs, ms, auditados = [], [], []
        for s in sementes:
            mundo = MundoSequencial(s)
            ag = SynthaiComAncora(s, aquecimento=10 ** 9, **kw).calibrar(mundo)
            mundo.rodar(ag, episodios)
            l_ef, f, dd, _ = ag.termos()
            fs.append(f)
            ms.append(dd / (f * l_ef * ag.p_estrela))
            auditados.append(ag.f_auditado)
        n = len(sementes)
        resultado[nome] = (sum(fs) / n, sum(ms) / n, sorted(ms)[n // 2],
                           sum(c for c, _ in auditados) / n, sum(p for _, p in auditados) / n)
    return resultado


def p343_ancora_no_comportamento(sementes=tuple(range(800, 830))):
    """30 sementes NOVAS, três mundos: principal (gradiente, 2P*) contra a autorregulada sem âncora (média, = P333) e
    com as âncoras (quantil; auditoria + quantil)."""
    from synthai import SynthaiExploradora
    from synthai.ancora import SynthaiComAncora
    from synthai.mundos import MundoSequencial
    agentes = {"principal": lambda s: SynthaiExploradora(s),
               "auto_media": lambda s: SynthaiComAncora(s, **_VARIANTES_28["media"]),
               "quantil": lambda s: SynthaiComAncora(s, **_VARIANTES_28["quantil"]),
               "auditoria_quantil": lambda s: SynthaiComAncora(s, **_VARIANTES_28["auditoria_quantil"])}
    tarefas = (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), 1000),
               ("sequencial", lambda s: MundoSequencial(s), 400),
               ("modelo ruim", lambda s: MundoSequencial(s, sigma_modelo=2.0), 400))
    resultado = {}
    for tarefa, fazer, n in tarefas:
        ret = {v: [] for v in agentes}
        cats = {v: 0.0 for v in agentes}
        ms = {v: 0.0 for v in agentes}
        for s in sementes:
            for v, f in agentes.items():
                mundo = fazer(s)
                ag = f(s).calibrar(mundo)
                r = mundo.rodar(ag, n)
                ret[v].append(r["retorno"])
                cats[v] += r["catastrofes"] / len(sementes)
                ms[v] += ag.relacao.limiar / p71_valor_da_pergunta() / len(sementes)
        resultado[tarefa] = ({v: sum(x) / len(x) for v, x in ret.items()}, cats, ms,
                             {v: _pareado(ret["principal"], ret[v]) for v in agentes if v != "principal"})
    return resultado


def p344_ancora_no_bandido(sementes=tuple(range(830, 850)), rodadas=20):
    """O bandido (20 sementes novas): principal contra a âncora (auditoria + quantil), Υ normalizado."""
    from synthai import SynthaiExploradora
    from synthai.ancora import SynthaiComAncora
    from synthai.mundos import MundoBandido
    from synthai.referencias import Acaso, Oraculo
    norm = {"principal": [], "auditoria_quantil": []}
    cats = {v: 0.0 for v in norm}
    for s in sementes:
        acaso = MundoBandido(s).rodar(Acaso(s), rodadas)["retorno"]
        oraculo = MundoBandido(s).rodar(Oraculo(s), rodadas)["retorno"]
        for v, f in (("principal", lambda s: SynthaiExploradora(s)),
                     ("auditoria_quantil", lambda s: SynthaiComAncora(s, **_VARIANTES_28["auditoria_quantil"]))):
            mundo = MundoBandido(s)
            r = mundo.rodar(f(s).calibrar(mundo), rodadas)
            norm[v].append((r["retorno"] - acaso) / (oraculo - acaso))
            cats[v] += r["catastrofes"] / len(sementes)
    return {v: sum(x) / len(x) for v, x in norm.items()}, cats, _pareado(norm["principal"], norm["auditoria_quantil"])


# --- Parte 29: compor em vez de herdar; o pensamento com mais pesos; a bateria de equações ---

# Placar acumulado ao fim da Parte 29 (atualizado quando os testes da parte terminam)
ERROS_P359, TESTES_P359 = 83, 181


def _cdf_gama(k, x):
    """Função de distribuição da Gamma(k, 1) pela série regularizada (para conferir quantis)."""
    if x <= 0:
        return 0.0
    s = t = 1.0 / k
    n = 1
    while t > 1e-16 * s:
        t *= x / (k + n)
        s += t
        n += 1
    return min(1.0, s * exp(-x + k * log(x) - lgamma(k)))


def _quantil_gama_exato(k, p):
    lo, hi = 0.0, 10 * k + 40
    for _ in range(200):
        m = (lo + hi) / 2
        if _cdf_gama(k, m) < p:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def p352_bateria_wilson_hilferty(formas=tuple([0.5, 1, 1.5, 2, 3, 4, 5, 7, 9.5, 12, 15, 20, 25, 35, 50, 70, 100]), z=0.8416):
    """Bateria 1: o quantil de 80% de Wilson–Hilferty contra o exato, em 17 formas da Gamma. Para cada forma: o quantil
    aproximado, o exato, o erro relativo e a probabilidade que o aproximado de fato acumula (deveria ser 0,8)."""
    from synthai.ancora import quantil_gama
    linhas = []
    for k in formas:
        qa, qe = quantil_gama(k, 1.0, z), _quantil_gama_exato(k, 0.8)
        linhas.append((k, qa, qe, qa / qe - 1, _cdf_gama(k, qa)))
    return linhas


def p352_bateria_delta_inverso(lambdas=(1, 2, 3, 5, 9.5, 15, 25, 50, 100)):
    """Bateria 2: E[1/X | X >= 1] para X ~ Poisson(λ), exato (soma da série) contra o delta-método de 3ª ordem
    (1/λ)(1 + 1/λ + 2/λ²) e contra o de 2ª ordem (1/λ)(1 + 1/λ). É o tamanho do viés de Jensen numa razão de contagens."""
    linhas = []
    for lam in lambdas:
        soma = massa = 0.0
        termo = exp(-lam)  # P(X = 0)
        for x in range(1, int(lam + 40 * sqrt(lam) + 50)):
            termo *= lam / x
            soma += termo / x
            massa += termo
        exato = soma / massa
        d3 = (1 / lam) * (1 + 1 / lam + 2 / lam ** 2)
        d2 = (1 / lam) * (1 + 1 / lam)
        linhas.append((lam, exato, d2, d3, d2 / exato - 1, d3 / exato - 1))
    return linhas


def p352_bateria_contas():
    """Bateria 3: contas de tamanho (antes de simular). Pesos do pensamento: 1 + d + d(d+1)/2; eventos por peso
    (EPV, Peduzzi et al., 1996) no histórico de cada mundo; e o otimismo de Akaike (perda de teste − perda de treino
    ≈ k/n por amostra) para 4 e 10 pesos."""
    d = 3
    k_lin, k_rico = 1 + d, 1 + d + d * (d + 1) // 2
    mundos = {"sequencial": (150 * 50, 37.3), "escolha única": (150 * 200, 150 * 200 * 0.005)}
    linhas = {}
    for nome, (n, eventos) in mundos.items():
        linhas[nome] = (n, eventos, eventos / (k_lin - 1), eventos / (k_rico - 1), k_lin / n, k_rico / n,
                        (k_rico - k_lin) / n)
    return k_lin, k_rico, linhas


def p353_pensamento_rico(treino=150, teste=300):
    """Simulação: o pensamento linear (Newton, 4 pesos, sem Firth) contra o rico (10 pesos, ridge 1), nos históricos
    auditados (sequencial: sementes 620-629, como a P302; escolha única: 640-649). Log-perda no treino e no teste, a
    diferença (o otimismo) e o número de catástrofes do treino."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento_exato import ajustar_logistica, dados_do_historico, perda_logistica
    from synthai.pensamento_rico import PensamentoRico
    mundos = (("sequencial", lambda s: MundoSequencial(s), tuple(range(620, 630))),
              ("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), tuple(range(640, 650))))
    resultado = {}
    for nome, fazer, sementes in mundos:
        soma = {"linear": [0.0, 0.0], "rico": [0.0, 0.0]}
        eventos = 0.0
        for s in sementes:
            mundo = fazer(s)
            hist, novo = mundo.historico_auditado(treino), mundo.historico_auditado(teste)
            xs, ys = dados_do_historico(hist)
            xt, yt = dados_do_historico(novo)
            eventos += sum(ys) / len(sementes)
            w = ajustar_logistica(xs, ys, firth=False)
            soma["linear"][0] += perda_logistica(w, xs, ys) / len(sementes)
            soma["linear"][1] += perda_logistica(w, xt, yt) / len(sementes)
            r = PensamentoRico()
            r.calibrar(hist)
            rx = lambda h: [r._x(o, max(oo.comite for oo, _, _ in ep), l) for ep in h for o, _, l in ep]
            soma["rico"][0] += perda_logistica(r.w, rx(hist), ys) / len(sementes)
            soma["rico"][1] += perda_logistica(r.w, rx(novo), yt) / len(sementes)
        resultado[nome] = ({k: (a, b, b - a) for k, (a, b) in soma.items()}, eventos)
    return resultado


def p354_calibracao_rica(sementes_seq=tuple(range(700, 710)), sementes_unica=tuple(range(640, 650))):
    """O fator f (real / previsto nas candidatas aceitas sem perguntar, P316) com o pensamento rico, limiar fixo 2P*,
    nas sementes das P316/P322 (onde o linear de Newton deu 6,15 na escolha única e 4,95 no sequencial)."""
    from synthai.limiar import SynthaiAjustada
    from synthai.mundos import MundoSequencial
    from synthai.pensamento_rico import PensamentoRico

    def fazer_agente(s):
        ag = SynthaiAjustada(s, mult=2.0)
        ag.pensamento = PensamentoRico()
        ag.percepcao.pensamento = ag.pensamento
        return ag
    resultado = {}
    for nome, fazer, ss, n in (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), sementes_unica, 1000),
                               ("sequencial", lambda s: MundoSequencial(s), sementes_seq, 400)):
        abaixo = [0.0, 0.0]
        for s in ss:
            mundo = fazer(s)
            ag = fazer_agente(s).calibrar(mundo)
            p_cat, lim = ag.pensamento.p_catastrofe, ag.relacao.limiar

            def p_e_anota(opcao, melhor, leitura=0.0, _p=p_cat, _lim=lim):
                p = _p(opcao, melhor, leitura)
                if p <= _lim:  # a régua lê o escondido
                    abaixo[0] += p
                    abaixo[1] += opcao._catastrofe
                return p
            ag.pensamento.p_catastrofe = p_e_anota
            mundo.rodar(ag, n)
        resultado[nome] = (abaixo[1] / abaixo[0] if abaixo[0] else float("nan"), int(abaixo[1]))
    return resultado


def p356_composta(sementes=tuple(range(850, 880)), sementes_bandido=tuple(range(880, 900))):
    """30 sementes novas (bandido: 20), quatro tarefas: principal, a SynthaiComposta (bandido: a principal; fora: a
    ancorada) e a composta com o pensamento rico. No bandido, a composta deve ser IDÊNTICA à principal."""
    from synthai import SynthaiExploradora
    from synthai.composta import SynthaiComposta, composta_rica
    from synthai.mundos import MundoBandido, MundoSequencial
    from synthai.referencias import Acaso, Oraculo
    agentes = {"principal": lambda s: SynthaiExploradora(s), "composta": lambda s: SynthaiComposta(s),
               "composta_rica": lambda s: composta_rica(s)}
    tarefas = (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), 1000, sementes, False),
               ("sequencial", lambda s: MundoSequencial(s), 400, sementes, False),
               ("modelo ruim", lambda s: MundoSequencial(s, sigma_modelo=2.0), 400, sementes, False),
               ("bandido", lambda s: MundoBandido(s), 20, sementes_bandido, True))
    resultado = {}
    for tarefa, fazer, n, ss, normalizar in tarefas:
        ret = {v: [] for v in agentes}
        cats = {v: 0.0 for v in agentes}
        for s in ss:
            ref = {}
            if normalizar:
                for nome, cls in (("acaso", Acaso), ("oraculo", Oraculo)):
                    ref[nome] = fazer(s).rodar(cls(s), n)["retorno"]
            for v, f in agentes.items():
                mundo = fazer(s)
                r = mundo.rodar(f(s).calibrar(mundo), n)
                x = r["retorno"]
                if normalizar:
                    x = (x - ref["acaso"]) / (ref["oraculo"] - ref["acaso"])
                ret[v].append(x)
                cats[v] += r["catastrofes"] / len(ss)
        resultado[tarefa] = ({v: sum(x) / len(x) for v, x in ret.items()}, cats,
                             {v: _pareado(ret["principal"], ret[v]) if ret[v] != ret["principal"] else (0.0, 0.0, 0.0)
                              for v in agentes if v != "principal"},
                             _pareado(ret["composta"], ret["composta_rica"]) if ret["composta"] != ret["composta_rica"] else (0.0, 0.0, 0.0))
    return resultado


def p357_takeuchi(treino=150):
    """CONFERÊNCIA DE TEORIA (depois de ver a P353): o otimismo esperado (perda de teste − de treino, por amostra) de um
    modelo MAL especificado não é k/n (Akaike), é tr(J I⁻¹)/n (Takeuchi, 1976), com J = média de (y − p)² x xᵀ e
    I = média de p(1 − p) x xᵀ no ajuste. Com o modelo certo, J = I e o traço vale k. Calcula os dois traços no
    histórico de treino de cada semente (as mesmas da P353) e devolve as médias."""
    from synthai.mundos import MundoSequencial
    from synthai.pensamento_exato import _inversa, ajustar_logistica, dados_do_historico
    from synthai.pensamento_rico import PensamentoRico
    mundos = (("sequencial", lambda s: MundoSequencial(s), tuple(range(620, 630))),
              ("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), tuple(range(640, 650))))

    def traco(xs, ys, w):
        k = len(w)
        J = [[0.0] * k for _ in range(k)]
        I = [[0.0] * k for _ in range(k)]
        for x, y in zip(xs, ys):
            p = 1 / (1 + exp(-max(-30.0, min(30.0, sum(a * b for a, b in zip(w, x))))))
            r2, v = (y - p) ** 2, p * (1 - p)
            for i in range(k):
                for j in range(k):
                    J[i][j] += r2 * x[i] * x[j]
                    I[i][j] += v * x[i] * x[j]
        inv = _inversa(I)
        return sum(J[i][j] * inv[j][i] for i in range(k) for j in range(k))
    resultado = {}
    for nome, fazer, sementes in mundos:
        t_lin = t_rico = n_med = 0.0
        for s in sementes:
            hist = fazer(s).historico_auditado(treino)
            xs, ys = dados_do_historico(hist)
            t_lin += traco(xs, ys, ajustar_logistica(xs, ys, firth=False)) / len(sementes)
            r = PensamentoRico()
            r.calibrar(hist)
            xr = [r._x(o, max(oo.comite for oo, _, _ in ep), l) for ep in hist for o, _, l in ep]
            t_rico += traco(xr, ys, r.w) / len(sementes)
            n_med += len(xs) / len(sementes)
        resultado[nome] = (t_lin, t_rico, n_med, t_lin / n_med, t_rico / n_med, (t_rico - t_lin) / n_med)
    return resultado


# --- Parte 30 (0x1E): a SYNTHAI em hexadecimal ---

# Placar acumulado ao fim da Parte 30 (atualizado quando os testes da parte terminam)
ERROS_P369, TESTES_P369 = 90, 201


def _digitos(numerador, denominador, base, n):
    """Os primeiros n dígitos de numerador/denominador (< 1) na base dada, por divisão longa inteira (exata)."""
    d, r = [], numerador
    for _ in range(n):
        r *= base
        d.append(r // denominador)
        r %= denominador
    return d


def p361_hex_do_limiar(n=32):
    """O limiar da P71, P* = c/((1−ε)L) = 0,1/(0,9 × 50) = 1/450, em hexadecimal: float.hex() dá a mantissa
    1.23456789abcdf. A razão: 1/(b−1)² = Σ k b^−(k+1) (de Σ k x^k = x/(1−x)²), e o dígito b−2 some num 'vai um'.
    Em base 16, 1/225 = 0x0.0123456789ABCDF0123…; 1/450 = 2^−9 × 256/225. Confere a regra em todas as bases de 2 a 16."""
    p = p71_valor_da_pergunta()
    hex_225 = "".join("0123456789ABCDEF"[x] for x in _digitos(1, 225, 16, n))
    bases = {}
    for b in range(3, 17):
        dig = _digitos(1, (b - 1) ** 2, b, 3 * (b - 1))
        periodo = dig[: b - 1]
        esperado = list(range(b - 2)) + [b - 1]
        bases[b] = (periodo == esperado and dig[b - 1: 2 * (b - 1)] == periodo, b - 2 not in dig)
    return p.hex(), (2 * p).hex(), float.fromhex(p.hex()) == p, hex_225, bases, (256 / 225) / 2 ** 9 == 1 / 450


def p362_conta_da_quantizacao(sementes_unica=tuple(range(640, 650)), sementes_seq=tuple(range(700, 710)), bits=(4, 8)):
    """A conta antes de simular: o pensamento de Newton (4 pesos) quantizado em 1 ou 2 dígitos hex por peso. Com passo
    Δ = 2R/(2^b − 1) (R = max |w|) e erro uniforme em [−Δ/2, Δ/2] (variância Δ²/12), o erro no logit de uma opção com
    variáveis x é σ² = (Δ²/12) Σ x_i². Mede, nas candidatas (as 5% de nota pessimista mais alta de cada episódio
    auditado), a raiz da média de σ² prevista e a raiz da média do erro real |w·x − q·x|². Devolve também os pesos em hex
    de uma semente."""
    from synthai.hexadecimal import quantizar
    from synthai.limiar import SynthaiAjustada
    from synthai.mundos import MundoSequencial
    resultado = {}
    for nome, fazer, ss in (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), sementes_unica),
                            ("sequencial", lambda s: MundoSequencial(s), sementes_seq)):
        for b in bits:
            prev = real = 0.0
            n = 0
            exemplo = None
            for s in ss:
                mundo = fazer(s)
                ag = SynthaiAjustada(s, mult=2.0).calibrar(mundo)
                w = ag.pensamento.w
                q, codigos, passo = quantizar(w, b)
                if exemplo is None:
                    exemplo = ([x.hex() for x in w], codigos, passo)
                for ep in mundo.historico_auditado(30):
                    melhor = max(o.comite for o, _, _ in ep)
                    ordem = sorted(ep, key=lambda t: -(t[0].nota - t[0].discordancia))
                    for o, _, leitura in ordem[: max(1, len(ordem) // 20)]:
                        x = ag.pensamento._x(o, melhor, leitura)
                        prev += passo * passo / 12 * sum(xi * xi for xi in x)
                        real += sum((a - c) * xi for a, c, xi in zip(w, q, x)) ** 2
                        n += 1
            resultado[(nome, b)] = (sqrt(prev / n), sqrt(real / n), exemplo)
    return resultado


_MUNDOS_30 = {"escolha única": (lambda s: _mundo_30("escolha única", s), 1000),
              "sequencial": (lambda s: _mundo_30("sequencial", s), 400),
              "bandido": (lambda s: _mundo_30("bandido", s), 20)}


def _mundo_30(nome, s):
    from synthai.mundos import MundoBandido, MundoSequencial
    if nome == "escolha única":
        return MundoSequencial(s, passos=1, n_acoes=200)
    if nome == "sequencial":
        return MundoSequencial(s)
    return MundoBandido(s)


_CACHE_363 = {}


def p363_fatorial_hex(mundo, sementes=tuple(range(900, 920))):
    """O experimento fatorial 2^3 dos tipos hexadecimais num mundo. Fora do bandido, o bit 0x4 (Thompson) não age
    (identidade testada), e os 3 bits que contam são Newton (0x1), âncora (0x2) e neutro (0x8); no bandido, o bit 0x2
    (âncora) não age, e contam Newton, Thompson (0x4) e neutro. Para cada semente, os 8 tipos rodam pareados e os efeitos
    saem da transformada de Walsh–Hadamard; devolve a média de cada tipo, as catástrofes e cada efeito com dp e t."""
    if (mundo, sementes) in _CACHE_363:  # a Parte 31 reusa os mesmos números (P391)
        return _CACHE_363[(mundo, sementes)]
    from synthai.hexadecimal import efeitos_fatoriais, synthai_do_tipo
    from synthai.referencias import Acaso, Oraculo
    fazer, n = _MUNDOS_30[mundo]
    bandido = mundo == "bandido"
    bits = (0x1, 0x4, 0x8) if bandido else (0x1, 0x2, 0x8)
    codigos = [sum(b for k, b in enumerate(bits) if i >> k & 1) for i in range(8)]  # ordem de Yates
    ret = {c: [] for c in codigos}
    cats = {c: 0.0 for c in codigos}
    efeitos = []
    for s in sementes:
        if bandido:
            acaso = fazer(s).rodar(Acaso(s), n)["retorno"]
            oraculo = fazer(s).rodar(Oraculo(s), n)["retorno"]
        y = []
        for c in codigos:
            m = fazer(s)
            r = m.rodar(synthai_do_tipo(c, s).calibrar(m), n)
            x = (r["retorno"] - acaso) / (oraculo - acaso) if bandido else r["retorno"]
            ret[c].append(x)
            cats[c] += r["catastrofes"] / len(sementes)
            y.append(x)
        efeitos.append(efeitos_fatoriais(y))
    nomes = ["media"] + ["x".join(f"0x{b:X}" for k, b in enumerate(bits) if j >> k & 1) for j in range(1, 8)]
    resumo = {}
    for j, nome in enumerate(nomes):
        v = [e[j] for e in efeitos]
        m = sum(v) / len(v)
        dp = sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))
        resumo[nome] = (m, dp, m / (dp / sqrt(len(v))) if dp > 0 else float("inf"))
    _CACHE_363[(mundo, sementes)] = ({c: sum(v) / len(v) for c, v in ret.items()}, cats, resumo)
    return _CACHE_363[(mundo, sementes)]


def p364_quantizada(sementes=tuple(range(920, 940))):
    """O tipo 0x3 (Newton + âncora) com o pensamento quantizado em 2 e em 1 dígito hex por peso (depois da calibração),
    contra o mesmo com os pesos completos. Escolha única e sequencial, 20 sementes novas pareadas."""
    from synthai.hexadecimal import quantizar, synthai_do_tipo
    resultado = {}
    for mundo in ("escolha única", "sequencial"):
        fazer, n = _MUNDOS_30[mundo]
        ret = {b: [] for b in (64, 8, 4)}
        cats = {b: 0.0 for b in ret}
        for s in sementes:
            for b in ret:
                m = fazer(s)
                ag = synthai_do_tipo(0x3, s).calibrar(m)
                if b < 64:
                    ag.pensamento.w = quantizar(ag.pensamento.w, b)[0]
                r = m.rodar(ag, n)
                ret[b].append(r["retorno"])
                cats[b] += r["catastrofes"] / len(sementes)
        resultado[mundo] = ({b: sum(v) / len(v) for b, v in ret.items()}, cats,
                            {b: _pareado(ret[64], ret[b]) for b in (8, 4)})
    return resultado


def p371_dicionario():
    """O dicionário (WordNet 3.0) como data lake: tamanhos, o grafo de definições, o núcleo, o Core, o MinSet (guloso), o
    fecho a partir do MinSet, a lei de Zipf nas definições, a entropia das letras, a profundidade da taxonomia e o
    'hexspeak' (lemas escritos só com as letras hexadecimais a-f)."""
    from synthai.dicionario import Dicionario, componentes_fortes, entropia, fecho, minset_guloso, nucleo, zipf
    d = Dicionario()
    defs = d.grafo_de_definicoes()
    nos = len(defs)
    arestas = sum(len(v) for v in defs.values())
    ker = nucleo(defs)
    comps = componentes_fortes(ker, defs)
    core = max(comps, key=len)
    ms = minset_guloso(ker, defs)
    conhecidas, rodadas = fecho(ms, defs)
    freq = {}
    for _, _, _, glosa in d.sinsets:
        for w in d.palavras_da_definicao(glosa):
            freq[w] = freq.get(w, 0) + 1
    s_zipf = zipf(list(freq.values()))
    letras = {}
    for x in defs:
        for ch in x:
            letras[ch] = letras.get(ch, 0) + 1
    h_letras = entropia(list(letras.values()))
    # profundidade de cada substantivo na taxonomia (caminho mais curto de hiperônimos até uma raiz)
    prof = {}
    def profundidade(i):
        pilha = [i]
        while pilha:
            j = pilha[-1]
            if j in prof:
                pilha.pop()
                continue
            pais = [d.indice[h] for h in d.sinsets[j][2] if h in d.indice]
            faltam = [k for k in pais if k not in prof]
            if faltam:
                pilha.extend(faltam)
                continue
            prof[j] = 0 if not pais else 1 + min(prof[k] for k in pais)
            pilha.pop()
        return prof[i]
    subst = [i for i, x in enumerate(d.sinsets) if x[0] == "n"]
    profs = [profundidade(i) for i in subst]
    hexspeak = sorted(x for x in defs if len(x) >= 3 and set(x) <= set("abcdef"))
    return {"sinsets": len(d.sinsets), "lemas": len(d.lemas), "nos": nos, "arestas": arestas,
            "nucleo": len(ker), "core": len(core), "satelites": len(ker) - len(core), "componentes": len(comps),
            "minset": len(ms), "minset_no_core": sum(1 for x in ms if x in core), "fecho": len(conhecidas),
            "rodadas": rodadas, "zipf": s_zipf, "vocabulario_definidor": len(freq), "entropia_letras": h_letras,
            "prof_media": sum(profs) / len(profs), "prof_max": max(profs), "hexspeak": hexspeak,
            "minset_exemplo": sorted(ms)[:40]}


def p366_composta_60_sementes(sementes=tuple(range(1000, 1060))):
    """O desempate: a composta (versão principal desde a P356) contra a principal antiga no mundo sequencial, 60
    sementes novas. Motivo: os lotes anteriores deram +0,411 (P343, 800-829), +0,337 (P356, 850-879) e −0,218 (P363,
    900-919, 0x3 − 0x0, identidade conferida)."""
    from synthai import SynthaiComposta, SynthaiExploradora
    from synthai.mundos import MundoSequencial
    a, b, ca, cb = [], [], 0.0, 0.0
    for s in sementes:
        m = MundoSequencial(s)
        r = m.rodar(SynthaiExploradora(s).calibrar(m), 400)
        a.append(r["retorno"])
        ca += r["catastrofes"] / len(sementes)
        m = MundoSequencial(s)
        r = m.rodar(SynthaiComposta(s).calibrar(m), 400)
        b.append(r["retorno"])
        cb += r["catastrofes"] / len(sementes)
    metade = len(sementes) // 2
    return _pareado(a, b), ca, cb, _pareado(a[:metade], b[:metade]), _pareado(a[metade:], b[metade:])


def p365_impressoes_digitais():
    """Resultados como números binários EXATOS (float.hex) e uma impressão digital SHA-256 (em hexadecimal) da bateria
    de equações da P352: uma regressão que compara bits, não arredondamentos."""
    import hashlib
    exatos = {"P*": p71_valor_da_pergunta().hex(),
              "E[1/X|X>=1], lambda 9,5": p352_bateria_delta_inverso((9.5,))[0][1].hex(),
              "Wilson-Hilferty, forma 9,5": p352_bateria_wilson_hilferty((9.5,))[0][1].hex()}
    texto = repr([tuple(x.hex() if isinstance(x, float) else x for x in l)
                  for l in p352_bateria_wilson_hilferty() + p352_bateria_delta_inverso()])
    return exatos, hashlib.sha256(texto.encode()).hexdigest()


def p372_hex_do_dicionario():
    """A ponte entre o dicionário e o hexadecimal: as palavras do grafo de definições escritas só com a-f (que SÃO
    números hexadecimais), a maior delas, e quanto vale uma palavra e uma letra em dígitos hex (log2 / 4)."""
    from synthai.dicionario import Dicionario, entropia
    d = Dicionario()
    defs = d.grafo_de_definicoes()
    hx = sorted(x for x in defs if len(x) >= 3 and set(x) <= set("abcdef"))
    maior = max(hx, key=lambda x: int(x, 16))
    letras = {}
    for x in defs:
        for ch in x:
            letras[ch] = letras.get(ch, 0) + 1
    return (len(hx), hx, maior, int(maior, 16), log2(len(defs)) / 4, entropia(list(letras.values())) / 4)


# --- Parte 31 (0x1F): o currículo do dicionário; o hipercubo, o código de Gray e os ULPs ---

# Placar acumulado ao fim da Parte 31 (atualizado quando os testes da parte terminam)
ERROS_P399, TESTES_P399 = 95, 216


def _grafo_31():
    from synthai.dicionario import Dicionario
    d = Dicionario()
    defs = d.grafo_de_definicoes()
    freq = {}
    for _, _, _, glosa in d.sinsets:
        for w in d.palavras_da_definicao(glosa):
            freq[w] = freq.get(w, 0) + 1
    return d, defs, freq


def p381_curriculo(ks=(500, 1000, 2000, 3985), thetas=(1.0, 0.8, 0.6), semente=381):
    """Que palavras ancorar primeiro? Quatro currículos de k palavras (as mais frequentes nas definições; as que mais
    definem outras; um MinSet guloso; ao acaso) e o fecho com entendimento parcial theta: a fração das 77.503 palavras
    que passa a ser entendida."""
    from synthai.dicionario import fecho_parcial, minset_guloso, nucleo
    d, defs, freq = _grafo_31()
    n = len(defs)
    define = {x: 0 for x in defs}
    for x, s in defs.items():
        for y in s:
            define[y] += 1
    por_freq = sorted(defs, key=lambda x: (-freq.get(x, 0), x))
    por_define = sorted(defs, key=lambda x: (-define[x], x))
    ms = minset_guloso(nucleo(defs), defs)
    ordem_ms = sorted(ms, key=lambda x: (-define[x], x)) + [x for x in por_define if x not in set(ms)]
    rng = _rng(semente)
    acaso = sorted(defs)
    rng.shuffle(acaso)
    curriculos = {"frequencia": por_freq, "define_mais": por_define, "minset": ordem_ms, "acaso": acaso}
    tabela = {}
    for nome, ordem in curriculos.items():
        for k in ks:
            for th in thetas:
                tabela[(nome, k, th)] = len(fecho_parcial(set(ordem[:k]), defs, th)) / n
    return n, len(ms), tabela


def p382_minset_reduzido():
    """O MinSet guloso (P371) depois da retirada das palavras redundantes, e a conferência de que o que sobra ainda
    quebra todos os ciclos (o fecho exato a partir dele define 100%)."""
    from synthai.dicionario import fecho, minset_guloso, minset_reduzido, nucleo
    _, defs, _ = _grafo_31()
    ker = nucleo(defs)
    ms = minset_guloso(ker, defs)
    red = minset_reduzido(ker, defs, ms)
    conhecidas, rodadas = fecho(red, defs)
    return len(ms), len(red), len(conhecidas) / len(defs), rodadas


def p383_cobertura_zipf(ks=(100, 500, 1000, 2000, 4000, 10000)):
    """Cobertura das palavras usadas nas definições pelas k mais frequentes: medida contra a conta de Zipf com o
    expoente medido (P371): Σ_{r<=k} r^-s / Σ_{r<=N} r^-s."""
    from synthai.dicionario import zipf
    _, _, freq = _grafo_31()
    fs = sorted(freq.values(), reverse=True)
    total = sum(fs)
    s_z = zipf(fs)
    hn = sum(r ** -s_z for r in range(1, len(fs) + 1))
    return s_z, len(fs), {k: (sum(fs[:k]) / total, sum(r ** -s_z for r in range(1, k + 1)) / hn) for k in ks}


def p384_wu_palmer_lesk(pares=2000, semente=384):
    """Duas medidas de significado independentes (a taxonomia de Wu e Palmer; a sobreposição de definições de Lesk) em
    pares de substantivos ao acaso: a correlação de postos entre elas, e a média de cada uma."""
    from synthai.dicionario import lesk, profundidades, spearman, wu_palmer
    d, _, _ = _grafo_31()
    prof = profundidades(d)
    subst = [i for i, x in enumerate(d.sinsets) if x[0] == "n"]
    rng = _rng(semente)
    wp, lk = [], []
    for _ in range(pares):
        a, b = rng.choice(subst), rng.choice(subst)
        wp.append(wu_palmer(d, prof, a, b))
        lk.append(lesk(d, a, b))
    return spearman(wp, lk), sum(wp) / len(wp), sum(lk) / len(lk), sum(1 for x in lk if x > 0) / len(lk)


def p385_ponto_critico(thetas=(0.6, 0.7, 0.8, 0.9), limiar=0.5):
    """EXPLORATÓRIO (depois de ver a P381): a cascata de entendimento parcial tem um ponto crítico. Para cada theta, o
    menor k (as k palavras mais frequentes das definições ancoradas) com que o fecho parcial passa de `limiar` do
    dicionário, achado por bisseção, e a cobertura logo antes e logo depois dele."""
    from synthai.dicionario import fecho_parcial
    _, defs, freq = _grafo_31()
    n = len(defs)
    ordem = sorted(defs, key=lambda x: (-freq.get(x, 0), x))
    cob = lambda k, th: len(fecho_parcial(set(ordem[:k]), defs, th)) / n
    resultado = {}
    for th in thetas:
        lo, hi = 0, len(ordem)
        while hi - lo > 1:
            meio = (lo + hi) // 2
            if cob(meio, th) >= limiar:
                hi = meio
            else:
                lo = meio
        resultado[th] = (hi, cob(lo, th), cob(hi, th))
    return resultado


def p391_geometria_hamming():
    """O hipercubo dos tipos (P363): em cada mundo, para os 28 pares dos 8 tipos que agem, a correlação de postos entre
    a distância de Hamming (quantos módulos diferem) e a diferença absoluta de retorno."""
    from synthai.dicionario import spearman
    from synthai.hexadecimal import hamming
    resultado = {}
    for mundo in ("escolha única", "sequencial", "bandido"):
        medias = p363_fatorial_hex(mundo)[0]
        cods = sorted(medias)
        hs, ds = [], []
        for i, a in enumerate(cods):
            for b in cods[i + 1:]:
                hs.append(hamming(a, b))
                ds.append(abs(medias[a] - medias[b]))
        por_h = {h: sum(d for hh, d in zip(hs, ds) if hh == h) / hs.count(h) for h in sorted(set(hs))}
        resultado[mundo] = (spearman(hs, ds), por_h)
    return resultado


def p392_gray_e_subida():
    """O código de Gray dos 16 tipos (cada vizinho difere num bit) e a busca local no hipercubo a partir de 0x0 em cada
    mundo (P363): aonde chega, em quantos passos, e se é o melhor tipo do mundo."""
    from synthai.hexadecimal import gray, subida_de_encosta
    ordem = [gray(i) for i in range(16)]
    resultado = {}
    for mundo in ("escolha única", "sequencial", "bandido"):
        medias = p363_fatorial_hex(mundo)[0]
        caminho = subida_de_encosta(medias, 0)
        melhor = max(medias, key=medias.get)
        resultado[mundo] = ([f"0x{c:X}" for c in caminho], f"0x{melhor:X}", caminho[-1] == melhor)
    return [f"{c:X}" for c in ordem], resultado


def p393_ulps(ns=(2000, 100000, 1000000), tentativas=20, semente=393):
    """A exatidão em ULPs: a soma ingênua (um += por termo, como os mundos fazem) contra a soma exata corretamente
    arredondada (math.fsum, Shewchuk 1997) de n números uniformes em (0, 1). A conta: o erro de cada adição tem desvio
    ~ulp(parcial)/√12 e a parcial cresce linearmente, então o erro final tem desvio ≈ ulp(S)·√n/6 e
    E|erro| = desvio·√(2/π)."""
    from math import fsum, ulp
    rng = _rng(semente)
    resultado = {}
    for n in ns:
        erros = []
        for _ in range(tentativas):
            xs = [rng.random() for _ in range(n)]
            ingenua = 0.0
            for x in xs:
                ingenua += x
            exata = fsum(xs)
            erros.append(abs(ingenua - exata) / ulp(exata))
        conta = sqrt(n) / 6 * sqrt(2 / pi)
        resultado[n] = (sum(erros) / len(erros), conta)
    return resultado, (0.1 + 0.2).hex(), (0.3).hex()



def p394_ulps_em_degrau(ns=(2000, 3000, 50000, 300000), tentativas=200, semente=394):
    """POSTERIOR À P393 (a conta √n/6 subestimou o erro por 1,3 a 1,9): o ulp da soma parcial não cresce em linha reta,
    cresce em DEGRAUS (dobra a cada potência de 2). A conta refeita: cada adição erra ~U(±ulp(S_i)/2), S_i ≈ i/2, então
    Var = Σ_i ulp(i/2)²/12 e E|erro|/ulp(S_n) = √Var/ulp(n/2)·√(2/π). Devolve, para cada n, (medido, conta em degrau,
    conta linear da P393) com mais tentativas e em n novos (previsão registrada antes de rodar)."""
    from math import fsum, ulp
    rng = _rng(semente)
    resultado = {}
    for n in ns:
        erros = []
        for _ in range(tentativas):
            xs = [rng.random() for _ in range(n)]
            ingenua = 0.0
            for x in xs:
                ingenua += x
            exata = fsum(xs)
            erros.append(abs(ingenua - exata) / ulp(exata))
        degrau = sqrt(sum(ulp(i / 2) ** 2 for i in range(1, n + 1)) / 12) / ulp(n / 2) * sqrt(2 / pi)
        resultado[n] = (sum(erros) / len(erros), degrau, sqrt(n) / 6 * sqrt(2 / pi))
    return resultado


# --- Parte 32 (0x20): trocar o aprendizado por reforço e o aprendizado contínuo pela decisão bayesiana exata;
#     a autopoiese (só onde serve); a memória em dígitos hex; a avalanche do dicionário ---

# Placar acumulado ao fim da Parte 32 (atualizado quando os testes da parte terminam)
ERROS_P429, TESTES_P429 = 103, 242


def _bracos_401(semente, k=10):
    rng = _rng(semente)
    return [rng.random() for _ in range(k)]


def p401_contas(k=10, t=2000, sementes=tuple(range(4010, 4110)), eps=0.1):
    """A CONTA antes da simulação da P401, só com as médias dos braços (sem rodar agente nenhum):
    - Lai–Robbins: o arrependimento mínimo de qualquer agente consistente, Σ Δ_k ln T / KL(p_k, p*), na média das sementes;
    - ε-guloso: só a exploração já custa ε·T·(p* − média dos braços) (cota inferior do Q-learning com ε fixo);
    - as esperanças sob braços U(0, 1): E[p*] = k/(k+1), E[média] = 1/2, então ε·T·(k/(k+1) − 1/2)."""
    from synthai.decisao import cota_lai_robbins
    lr, expl = [], []
    for sm in sementes:
        ps = _bracos_401(sm, k)
        lr.append(cota_lai_robbins(ps, t))
        expl.append(eps * t * (max(ps) - sum(ps) / k))
    return sum(lr) / len(lr), sum(expl) / len(expl), eps * t * (k / (k + 1) - 0.5)


def p401_bandido(k=10, t=2000, sementes=tuple(range(4010, 4110))):
    """Q-learning ε-guloso (α = 0,1, ε = 0,1; o RL padrão), Q otimista (q0 = 1, ε = 0), UCB1 e Thompson (o posterior
    exato, Beta) no mesmo bandido de Bernoulli com 10 braços U(0, 1), T = 2000, 100 sementes pareadas: o arrependimento
    final de cada um, e a diferença pareada de cada um contra Thompson."""
    from synthai.decisao import QEpsilon, ThompsonBernoulli, UCB1, rodar_bandido
    fabricas = {"q_eps": lambda r: QEpsilon(k, r), "q_otimista": lambda r: QEpsilon(k, r, eps=0.0, q0=1.0),
                "ucb1": lambda r: UCB1(k, r), "thompson": lambda r: ThompsonBernoulli(k, r)}
    finais = {n: [] for n in fabricas}
    for sm in sementes:
        ps = _bracos_401(sm, k)
        for n, f in fabricas.items():
            finais[n].append(rodar_bandido(f(_rng(sm + 1)), ps, t, _rng(sm + 2))[-1])
    medias = {n: sum(v) / len(v) for n, v in finais.items()}
    difs = {n: _pareado(finais["thompson"], finais[n]) for n in fabricas if n != "thompson"}
    return medias, difs


def p402_contas(n=6, t=5000, eps=0.1):
    """A CONTA antes da P402 no RiverSwim: o ganho médio ótimo g* (iteração de valor relativa) vezes T; o ganho de ficar
    sempre à esquerda no estado 0 (5/1000 por passo); e o Q-learning ε-guloso com Q inicial 0, que depois da primeira
    recompensa 5/1000 fica guloso à esquerda no estado 0: ganha ≈ 0,005·T·(1 − ε/2) enquanto não chegar ao fim."""
    from synthai.decisao import media_otima, riverswim
    P, R = riverswim(n)
    g = media_otima(P, R)
    return g, g * t, 0.005 * t, 0.005 * t * (1 - eps / 2)


def p402_riverswim(n=6, t=5000, sementes=tuple(range(4020, 4040))):
    """PSRL (posterior Dirichlet + programação dinâmica num MDP sorteado a cada episódio de 20 passos) contra o
    Q-learning ε-guloso (γ = 0,95, α = 0,1, ε = 0,1) e o Q-learning otimista (Q inicial 20 = 1/(1 − γ), ε = 0,1) no
    RiverSwim de 6 estados, T = 5000 passos, 20 sementes: a recompensa total de cada um e as diferenças pareadas."""
    from synthai.decisao import PSRL, QLearningMDP, riverswim, rodar_mdp
    P, R = riverswim(n)
    fabricas = {"psrl": lambda r: PSRL(n, r), "q_eps": lambda r: QLearningMDP(n, r),
                "q_otimista": lambda r: QLearningMDP(n, r, q0=20.0)}
    tot = {k: [] for k in fabricas}
    for sm in sementes:
        for k, f in fabricas.items():
            tot[k].append(rodar_mdp(f(_rng(sm + 1)), P, R, t, _rng(sm + 2)))
    medias = {k: sum(v) / len(v) for k, v in tot.items()}
    return medias, {k: _pareado(tot[k], tot["psrl"]) for k in fabricas if k != "psrl"}


def _tarefas_403(semente, d=40, por_tarefa=400, ruido=0.1):
    """Duas tarefas em sequência sobre a mesma função f(x) = sin(2x) + x/2: A vê x em [−π, 0], B vê x em [0, π].
    Atributos: d cossenos aleatórios fixos √(2/d)·cos(w x + b), w ~ N(0, 2²), b ~ U(0, 2π) (Rahimi e Recht, 2007)."""
    rng = _rng(semente)
    ws = [rng.gauss(0, 2) for _ in range(d)]
    bs = [rng.uniform(0, 2 * pi) for _ in range(d)]
    fa = lambda x: [sqrt(2 / d) * cos(w * x + b) for w, b in zip(ws, bs)]
    f = lambda x: sin(2 * x) + x / 2
    xa = [rng.uniform(-pi, 0) for _ in range(por_tarefa)]
    xb = [rng.uniform(0, pi) for _ in range(por_tarefa)]
    ta = [-pi + pi * (i + 0.5) / 200 for i in range(200)]
    A = [(fa(x), f(x) + rng.gauss(0, ruido)) for x in xa]
    B = [(fa(x), f(x) + rng.gauss(0, ruido)) for x in xb]
    teste_a = [(fa(x), f(x)) for x in ta]
    return A, B, teste_a


def p403_continuo(d=40, sementes=tuple(range(4030, 4040)), passo=0.5, lam=1e-2):
    """Aprendizado contínuo: tarefa A, depois tarefa B, mesmo modelo. A regressão bayesiana recursiva (estatística
    suficiente exata) contra a descida de gradiente estocástica (passo constante, uma passada) com os mesmos atributos.
    Mede o erro quadrático médio no teste de A depois de A e depois de B (o esquecimento), e confere que a recursiva
    termina IGUAL à ridge em lote com A ∪ B (a maior diferença absoluta entre os pesos)."""
    from synthai.decisao import RegressaoBayesiana, RegressaoSGD, ridge_em_lote
    res = {"bayes": ([], []), "sgd": ([], [])}
    maior_dif = 0.0
    for sm in sementes:
        A, B, teste = _tarefas_403(sm, d)
        mse = lambda m: sum((m.prever(f) - y) ** 2 for f, y in teste) / len(teste)
        for nome, m in (("bayes", RegressaoBayesiana(d, lam)), ("sgd", RegressaoSGD(d, passo))):
            for f, y in A:
                m.atualizar(f, y)
            res[nome][0].append(mse(m))
            for f, y in B:
                m.atualizar(f, y)
            res[nome][1].append(mse(m))
            if nome == "bayes":
                lote = ridge_em_lote([f for f, _ in A + B], [y for _, y in A + B], lam)
                maior_dif = max(maior_dif, max(abs(a - b) for a, b in zip(m.w, lote)))
    med = {n: (sum(a) / len(a), sum(b) / len(b)) for n, (a, b) in res.items()}
    return med, _pareado(res["bayes"][1], res["sgd"][1]), maior_dif


def p404_contas(fracoes=(0.1, 0.5, 0.9)):
    """A CONTA antes da P404 (autopoiese do dicionário): se uma fração q das palavras é esquecida ao acaso, uma esquecida
    volta já na primeira rodada do fecho exato (θ = 1) se todas as |s| que a definem sobreviveram: chance (1 − q)^|s|.
    A cota inferior da regeneração em θ = 1 é então (1 − q) + q·E[(1 − q)^|s|] (uma rodada só; as seguintes só somam)."""
    from synthai.dicionario import Dicionario
    defs = Dicionario().grafo_de_definicoes()
    n = len(defs)
    return {q: (1 - q) + q * sum((1 - q) ** len(s) for s in defs.values()) / n for q in fracoes}


def p404_autopoiese(fracoes=(0.1, 0.5, 0.9), thetas=(1.0, 0.8), semente=404):
    """Autopoiese no dicionário: o núcleo é fechado (toda palavra do núcleo é definida só por palavras do núcleo: a
    fração de arestas que saem dele), e a regeneração: esquecer uma fração q das 77.503 palavras ao acaso e refazer o
    fecho parcial a partir das que sobraram. Devolve a fração de fechamento e {(q, θ): fração recuperada}."""
    from synthai.dicionario import fecho_parcial, nucleo
    _, defs, _ = _grafo_31()
    ker = set(nucleo(defs))
    arestas = sum(len(defs[x]) for x in ker)
    dentro = sum(len(defs[x] & ker) for x in ker)
    rng = _rng(semente)
    palavras = sorted(defs)
    res = {}
    for q in fracoes:
        sobra = set(rng.sample(palavras, round(len(palavras) * (1 - q))))
        for th in thetas:
            res[(q, th)] = len(fecho_parcial(sobra, defs, th)) / len(defs)
    return len(ker), dentro / arestas, res


def p405_dano(k=10, t=2000, dano_em=1000, sementes=tuple(range(4050, 4150))):
    """Regeneração (autopoiese no agente): no passo 1000, a memória é destruída e trocada por lixo: em Thompson, as
    contagens viram inteiros ao acaso em 1..20; no Q-learning ε-guloso, os Q viram U(0, 1). O arrependimento na segunda
    metade [1000, 2000) de cada um, o de Thompson na primeira metade, e as diferenças pareadas."""
    from synthai.decisao import QEpsilon, ThompsonBernoulli, rodar_bandido

    def lixo_ts(ag):
        r = _rng(ag.lixo)
        ag.a = [float(r.randint(1, 20)) for _ in ag.a]
        ag.b = [float(r.randint(1, 20)) for _ in ag.b]

    def lixo_q(ag):
        r = _rng(ag.lixo)
        ag.q = [r.random() for _ in ag.q]

    seg_ts, seg_q, pri_ts = [], [], []
    for sm in sementes:
        ps = _bracos_401(sm, k)
        ts = ThompsonBernoulli(k, _rng(sm + 1))
        ts.lixo = sm + 3
        a = rodar_bandido(ts, ps, t, _rng(sm + 2), dano_em, lixo_ts)
        q = QEpsilon(k, _rng(sm + 1))
        q.lixo = sm + 3
        b = rodar_bandido(q, ps, t, _rng(sm + 2), dano_em, lixo_q)
        seg_ts.append(a[-1] - a[dano_em - 1])
        seg_q.append(b[-1] - b[dano_em - 1])
        pri_ts.append(a[dano_em - 1])
    m = lambda v: sum(v) / len(v)
    return m(pri_ts), m(seg_ts), m(seg_q), _pareado(seg_ts, seg_q)


def p411_contas(k=10, tetos=(16, 256), t=2000, sementes=tuple(range(4010, 4110)), sorteios=4000):
    """A CONTA antes da P411 (a memória de Thompson em dígitos hex: a + b limitado a 16 = 1 dígito, ou 256 = 2 dígitos).
    No regime estacionário, cada braço puxado com frequência tem a + b entre teto/2 e teto, posterior ≈
    Beta(1 + p·n, 1 + (1 − p)·n) com n ≈ 3/4 do teto. Então a chance de cada braço ser escolhido é a de a amostra dele ser a
    maior, e o arrependimento por passo é Σ Δ_k·π_k: arrependimento ≈ T·Σ Δ_k π_k (π_k por sorteio, `sorteios` vezes).
    É uma cota aproximada: braços ruins, puxados pouco, têm n menor e são puxados MAIS que isso."""
    res = {}
    for teto in tetos:
        n_ef = 0.75 * teto
        tot = []
        for sm in sementes:
            ps = _bracos_401(sm, k)
            m = max(ps)
            r = _rng(sm + 9)
            cont = [0] * k
            for _ in range(sorteios):
                am = [r.betavariate(1 + p * n_ef, 1 + (1 - p) * n_ef) for p in ps]
                cont[max(range(k), key=am.__getitem__)] += 1
            tot.append(t * sum((m - p) * c / sorteios for p, c in zip(ps, cont)))
        res[teto] = sum(tot) / len(tot)
    return res


def p411_memoria_hex(k=10, t=2000, tetos=(16, 256), sementes=tuple(range(4010, 4110))):
    """Thompson com a memória limitada a 1 e 2 dígitos hex por braço (a + b ≤ 16 ou 256, metade quando passa) contra o
    Thompson completo, mesmos braços e sementes da P401: o arrependimento final e as diferenças pareadas."""
    from synthai.decisao import ThompsonBernoulli, rodar_bandido
    fin = {None: []}
    fin.update({x: [] for x in tetos})
    for sm in sementes:
        ps = _bracos_401(sm, k)
        for teto in fin:
            fin[teto].append(rodar_bandido(ThompsonBernoulli(k, _rng(sm + 1), teto), ps, t, _rng(sm + 2))[-1])
    med = {x: sum(v) / len(v) for x, v in fin.items()}
    return med, {x: _pareado(fin[None], fin[x]) for x in tetos}


def p421_avalanche(thetas=(0.6, 0.7, 0.8, 0.9), semente=421, ate=40000):
    """A avalanche do dicionário (P385, agora com o fecho incremental): para o currículo por frequência e para um
    currículo ao acaso, a cobertura depois de cada palavra ancorada; o maior salto causado por UMA palavra, o k dele, a
    palavra, e o k em que a cobertura passa de 50%."""
    from synthai.dicionario import fecho_incremental
    _, defs, freq = _grafo_31()
    n = len(defs)
    por_freq = sorted(defs, key=lambda x: (-freq.get(x, 0), x))
    acaso = sorted(defs)
    _rng(semente).shuffle(acaso)
    res = {}
    for nome, ordem in (("frequencia", por_freq), ("acaso", acaso)):
        for th in thetas:
            cob = fecho_incremental(ordem, defs, th, ate)
            saltos = [cob[i + 1] - cob[i] for i in range(len(cob) - 1)]
            km = max(range(len(saltos)), key=saltos.__getitem__)
            meio = next((i for i, c in enumerate(cob) if c >= n / 2), None)
            res[(nome, th)] = (km + 1, ordem[km], saltos[km] / n, meio)
    return res


# --- Parte 33 (0x21): a arquitetura "pós-ASI numa CPU só", auditada: limites físicos, a auditoria da AST, a autoavaliação
#     (reward hacking), L3 contra L4, a maldição do vencedor, e o Bayes com renovação ---

# Placar acumulado ao fim da Parte 33 (atualizado quando os testes da parte terminam)
ERROS_P459, TESTES_P459 = 105, 258

K_BOLTZMANN = 1.380649e-23   # J/K (exato no SI de 2019)
H_PLANCK = 6.62607015e-34    # J·s (exato no SI de 2019)
C_LUZ = 299792458.0          # m/s (exato)


def p431_landauer(temperaturas=(293.15, 300.0, 4.0)):
    """O limite de Landauer, E = k_B·T·ln 2, em joules por bit, e a temperatura que daria o número citado no texto
    (2,75 × 10⁻²¹ J a "20 °C")."""
    from math import log as ln
    return {t: K_BOLTZMANN * t * ln(2) for t in temperaturas}, 2.75e-21 / (K_BOLTZMANN * ln(2))


def p432_bremermann(massa=1.0):
    """Bremermann (m·c²/h, bits por segundo) contra Margolus–Levitin (2E/(πħ) = 4E/h, operações por segundo), para
    E = m·c². O texto atribui 1,36 × 10⁵⁰ à fórmula 2E/(πħ); a razão entre as duas é exatamente 4."""
    hbar = H_PLANCK / (2 * pi)
    e = massa * C_LUZ ** 2
    return e / H_PLANCK, 2 * e / (pi * hbar), (2 * e / (pi * hbar)) / (e / H_PLANCK)


def p433_cpu(n=3_000_000):
    """Quantas adições inteiras por segundo um laço Python faz nesta CPU (um núcleo), medido com time.perf_counter, e a
    distância até Bremermann para 1 g de silício (a ordem da massa de um chip): log₁₀ da razão."""
    import time
    t0 = time.perf_counter()
    x = 0
    for i in range(n):
        x += i
    dt = time.perf_counter() - t0
    taxa = n / dt
    brem_1g = p432_bremermann(1e-3)[0]
    return taxa, brem_1g, log(brem_1g / taxa, 10)


def p434_aixi_tl(taxa, t=1000, ls=(20, 30, 40, 64, 128)):
    """O custo por ciclo do AIXI(t,l): t·2^l passos (Hutter; Schmidhuber 2003). Em anos, à taxa medida na P433."""
    ano = 365.25 * 24 * 3600
    return {l: t * 2 ** l / taxa / ano for l in ls}


def p435_auditoria():
    """A auditoria estática (só `ast`, nada é executado) da arquitetura do usuário em externos/arquitetura_pos_asi.py."""
    import os
    from synthai.rsi import auditar_ast
    return auditar_ast(os.path.join(os.path.dirname(os.path.abspath(__file__)), "externos", "arquitetura_pos_asi.py"))


def p435_rodar_original(timeout=600):
    """Roda o laço da arquitetura original NUM PROCESSO SEPARADO (o código dela usa exec em globals()) e devolve o
    tamanho final do arquivo, a geração máxima e as notas. Só se roda depois de registrar a previsão."""
    import os
    import subprocess
    import sys as _sys
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "externos")
    codigo = ("import arquitetura_pos_asi as m\n"
              "cap = []\n"
              "orig = m.DarwinArchiveManager.add_to_archive\n"
              "def add(self, s):\n"
              "    orig(self, s); cap.append(self)\n"
              "m.DarwinArchiveManager.add_to_archive = add\n"
              "m.main_evolution_loop()\n"
              "a = cap[-1].archive if cap else []\n"
              "print(len(a), max(x.generation for x in a) if a else 0, [x.performance_score for x in a])\n")
    r = subprocess.run([_sys.executable, "-c", codigo], cwd=pasta, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.returncode


def p436_contas(mu=0.01, iteracoes=300):
    """A CONTA antes da P436: com autoavaliação, um filho com o relatório inflado (nota perfeita) é sempre aceito e vira
    o pai para sempre (a nota guardada dele não pode ser superada). A chance de o campeão ser inflado ao fim de N
    iterações é 1 − (1 − μ)^N."""
    return 1 - (1 - mu) ** iteracoes


def p436_recompensa(rodadas=40, iteracoes=300, mu=0.01, semente=436):
    """Reward hacking: o mesmo laço de auto-melhoria (regra "dgm", a do texto), com a autoavaliação e com o avaliador
    selado, μ = 1% de chance por mutação de o relatório virar "inflado". Para cada avaliador: a fração de rodadas cujo
    campeão é inflado, e o arrependimento REAL (reavaliado pelo selado em 20 sementes novas) do campeão."""
    from synthai.rsi import AvaliadorSelado, Autoavaliacao, evoluir, regret_do_genoma
    res = {}
    for nome, fab in (("autoavaliacao", Autoavaliacao), ("selado", AvaliadorSelado)):
        inflados, reais = 0, []
        for r in range(rodadas):
            _, (g, _) = evoluir(iteracoes, fab(), _rng(semente + r), "L3", "dgm", mu, sementes_por_nota=2,
                                base_sementes=10_000_000 * (r + 1))
            inflados += g["relatorio"] == "inflado"
            reais.append(regret_do_genoma(g, range(900_000, 900_020)))
        res[nome] = (inflados / rodadas, sum(reais) / len(reais))
    return res


def p437_l3_l4(rodadas=20, iteracoes=150, semente=437):
    """L3 (o passo de mutação fixo) contra L4 (o passo de mutação muta junto: o mecanismo de melhoria evolui) no mesmo
    laço, avaliador selado, regra "dgm", rodadas pareadas pela semente. O arrependimento real do campeão (20 sementes
    novas), a diferença pareada L4 − L3, e o melhor campeão contra Thompson sem nenhuma evolução nas mesmas 20 sementes."""
    from synthai.decisao import ThompsonBernoulli, rodar_bandido
    from synthai.rsi import AvaliadorSelado, evoluir, regret_do_genoma
    teste = range(900_000, 900_020)
    reais = {"L3": [], "L4": []}
    for r in range(rodadas):
        for nivel in reais:
            _, (g, _) = evoluir(iteracoes, AvaliadorSelado(), _rng(semente + r), nivel, "dgm", 0.0, sementes_por_nota=3,
                                base_sementes=10_000_000 * (r + 1))
            reais[nivel].append(regret_do_genoma(g, teste))
    ts = []
    for sm in teste:
        rr = random.Random(sm)
        ps = [rr.random() for _ in range(10)]
        ts.append(rodar_bandido(ThompsonBernoulli(10, random.Random(sm + 1)), ps, 2000, random.Random(sm + 2))[-1])
    thompson = sum(ts) / len(ts)
    med = {k: sum(v) / len(v) for k, v in reais.items()}
    return med, _pareado(reais["L3"], reais["L4"]), thompson, min(min(v) for v in reais.values())


def p438_contas(sementes_ruido=tuple(range(5000, 5040)), sementes_por_nota=3):
    """A CONTA antes da P438: o desvio σ da nota de um genoma (média de 3 sementes) pelo genoma inicial em 40 sementes, e
    a maldição do vencedor esperada: a nota guardada do campeão é o máximo de notas ruidosas, inflada por ≈ σ·√(2 ln N)
    no pior caso (N notas de genomas quase iguais)."""
    from synthai.rsi import genoma_inicial, regret_do_genoma
    g = genoma_inicial()
    xs = [regret_do_genoma(g, [s]) for s in sementes_ruido]
    m = sum(xs) / len(xs)
    sd1 = sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
    sigma = sd1 / sqrt(sementes_por_nota)
    return sigma, {n: sigma * sqrt(2 * log(n)) for n in (10, 50, 150)}


def p438_maldicao(rodadas=20, iteracoes=150, semente=438):
    """A maldição do vencedor: no fim do laço, a nota GUARDADA do campeão contra a nota dele reavaliada em 20 sementes
    novas (−arrependimento). Regra "dgm" (a do texto) contra a regra "godel" (t > 3 em 10 sementes novas pareadas)."""
    from synthai.rsi import AvaliadorSelado, evoluir, regret_do_genoma
    res = {}
    for regra in ("dgm", "godel"):
        infl, aceitos = [], []
        for r in range(rodadas):
            arq, (g, guardada) = evoluir(iteracoes, AvaliadorSelado(), _rng(semente + r), "L3", regra, 0.0,
                                         sementes_por_nota=3, base_sementes=10_000_000 * (r + 1))
            infl.append(guardada - (-regret_do_genoma(g, range(900_000, 900_020))))
            aceitos.append(len(arq) - 1)
        res[regra] = (sum(infl) / len(infl), sum(aceitos) / len(aceitos))
    return res


def p439_contas(gamas=(0.99, 0.999)):
    """A CONTA antes da P439: a memória efetiva do Thompson com renovação é 1/(1 − γ) passos; o lixo da P405 (≈ 21
    pseudo-observações por braço) cai para 5% em ln 20/(1 − γ) ≈ 3/(1 − γ) passos."""
    return {g: (1 / (1 - g), log(20) / (1 - g)) for g in gamas}


def p439_renovacao(k=10, t=2000, dano_em=1000, gamas=(0.99, 0.999), sementes=tuple(range(4050, 4150))):
    """O Bayes com renovação contra o dano da P405 (mesmas sementes e o mesmo lixo): para cada γ, o arrependimento na
    segunda metade sem dano e com dano, e o custo do dano; e o arrependimento total sem dano (o preço da renovação)."""
    from synthai.decisao import ThompsonDescontado, rodar_bandido

    def lixo(ag):
        r = _rng(ag.lixo)
        ag.a = [float(r.randint(1, 20)) for _ in ag.a]
        ag.b = [float(r.randint(1, 20)) for _ in ag.b]

    res = {}
    for g in gamas:
        sem, com, total = [], [], []
        for sm in sementes:
            ps = _bracos_401(sm, k)
            a = rodar_bandido(ThompsonDescontado(k, _rng(sm + 1), g), ps, t, _rng(sm + 2))
            ag = ThompsonDescontado(k, _rng(sm + 1), g)
            ag.lixo = sm + 3
            b = rodar_bandido(ag, ps, t, _rng(sm + 2), dano_em, lixo)
            sem.append(a[-1] - a[dano_em - 1])
            com.append(b[-1] - b[dano_em - 1])
            total.append(a[-1])
        m = lambda v: sum(v) / len(v)
        res[g] = (m(sem), m(com), m(com) - m(sem), m(total))
    return res


# --- Parte 34 (0x22): as promessas das Partes 31-33 testadas em casos novos: o Q-learning com α = 0,05, a taxa de
#     renovação contra a taxa de mudança do mundo, Zipf-Mandelbrot num corpus novo, o dicionário no lugar do ML,
#     o contador de Morris em um dígito hex ---

# Placar acumulado ao fim da Parte 34 (atualizado quando os testes da parte terminam)
ERROS_P489, TESTES_P489 = 110, 271


def p461_contas(alfa=0.1, eps=0.1, k=10, t=2000, sementes=tuple(range(4010, 4110))):
    """As duas cotas da P407 para o Q-learning ε-guloso, num α qualquer (posteriores à P401; aqui viram previsão em α
    novo): (1) ruído estacionário sem aprisionamento: exploração ε·T·(p* − p̄) + parte gulosa (1 − ε)·T·E[p* − p_argmax]
    com ruído de variância α/(2 − α)·p(1 − p); (2) campo médio com aprisionamento no primeiro braço que paga (∝ p_g),
    sem ruído. A medida deve ficar entre as duas."""
    cota1, cota2 = [], []
    for sm in sementes:
        ps = _bracos_401(sm, k)
        m = max(ps)
        r = random.Random(sm)
        g = 0.0
        for _ in range(t):
            q = [p + r.gauss(0, sqrt(alfa / (2 - alfa) * p * (1 - p))) for p in ps]
            g += m - ps[max(range(k), key=q.__getitem__)]
        cota1.append(eps * t * (m - sum(ps) / k) + (1 - eps) * g)
        s = sum(ps)
        tot = 0.0
        for g0, pg in enumerate(ps):
            q = [0.0] * k
            q[g0] = alfa
            reg = 0.0
            for _ in range(t):
                gg = max(range(k), key=q.__getitem__)
                for j in range(k):
                    w = eps / k + ((1 - eps) if j == gg else 0.0)
                    reg += w * (m - ps[j])
                    q[j] += w * alfa * (ps[j] - q[j])
            tot += pg / s * reg
        cota2.append(tot)
    return sum(cota1) / len(cota1), sum(cota2) / len(cota2)


def p461_q_alfa(alfa=0.05, k=10, t=2000, sementes=tuple(range(4010, 4110))):
    """O Q-learning ε-guloso com α novo, mesmos braços e sementes da P401: o arrependimento final médio."""
    from synthai.decisao import QEpsilon, rodar_bandido
    v = [rodar_bandido(QEpsilon(k, _rng(sm + 1), alfa=alfa), _bracos_401(sm, k), t, _rng(sm + 2))[-1] for sm in sementes]
    return sum(v) / len(v)


def p462_contas(t=4000, periodo=500, k=10):
    """A CONTA antes da P462: num bandido que muda a cada `periodo` passos (Υ = T/periodo − 1 quebras), o desconto
    recomendado por Garivier e Moulines (2011) para o UCB descontado é γ = 1 − (1/4)·√(Υ/T); a memória 1/(1 − γ)."""
    quebras = t // periodo - 1
    g = 1 - 0.25 * sqrt(quebras / t)
    return quebras, g, 1 / (1 - g)


def p462_mudanca(gamas=(0.95, 0.98, 0.99, 0.995, 0.999, 1.0), t=4000, periodo=500, k=10,
                 sementes=tuple(range(4620, 4670))):
    """Bandido que muda: a cada `periodo` passos, as médias dos braços são sorteadas de novo (U(0, 1)). Thompson com
    renovação para cada γ (γ = 1 é o exato), arrependimento contra o melhor braço DO MOMENTO; 50 sementes pareadas."""
    from synthai.decisao import ThompsonBernoulli, ThompsonDescontado
    res = {}
    for g in gamas:
        tot = []
        for sm in sementes:
            r = _rng(sm)
            fases = [[r.random() for _ in range(k)] for _ in range(t // periodo)]
            ag = ThompsonBernoulli(k, _rng(sm + 1)) if g == 1.0 else ThompsonDescontado(k, _rng(sm + 1), g)
            rr = _rng(sm + 2)
            reg = 0.0
            for passo in range(t):
                ps = fases[passo // periodo]
                i = ag.escolher()
                ag.atualizar(i, 1 if rr.random() < ps[i] else 0)
                reg += max(ps) - ps[i]
            tot.append(reg)
        res[g] = sum(tot) / len(tot)
    return res


def _frequencias_por_classe(pos):
    from synthai.dicionario import Dicionario
    d = Dicionario()
    freq = {}
    for p, _, _, glosa in d.sinsets:
        if p in pos:
            for w in d.palavras_da_definicao(glosa):
                freq[w] = freq.get(w, 0) + 1
    return sorted(freq.values(), reverse=True)


def p463_zipf_mandelbrot(ajuste=("n",), teste=("v",), ks_ajuste=(10, 30, 100, 300, 1000), ks_teste=(100, 500, 2000, 4000)):
    """Zipf–Mandelbrot, f(r) ∝ (r + q)^−s: ajusta (s, q) numa grade pela cobertura das k mais frequentes nas definições
    dos SUBSTANTIVOS (k ≤ 1000) e prevê a cobertura nas definições dos VERBOS (um corpus que o ajuste não viu), usando o N
    dos verbos. Compara com Zipf puro (q = 0, s ajustado igual). Devolve (s, q), a previsão e a medida em cada k."""
    fa = _frequencias_por_classe(ajuste)
    tot = sum(fa)
    acum = []
    a = 0
    for f in fa:
        a += f
        acum.append(a / tot)

    def curva(s_, q_, n, ks):
        z = [(r + q_) ** -s_ for r in range(1, n + 1)]
        tz = sum(z)
        out, a_, j = {}, 0.0, 0
        for kk in sorted(ks):
            while j < kk:
                a_ += z[j]
                j += 1
            out[kk] = a_ / tz
        return out

    melhor = None
    for s_ in [0.8 + 0.02 * i for i in range(31)]:
        for q_ in [0, 1, 2, 4, 8, 16, 32, 64, 128]:
            c = curva(s_, q_, len(fa), ks_ajuste)
            e = sum((c[kk] - acum[kk - 1]) ** 2 for kk in ks_ajuste)
            if melhor is None or e < melhor[0]:
                melhor = (e, s_, q_)
    _, s_m, q_m = melhor
    ft = _frequencias_por_classe(teste)
    tt = sum(ft)
    med = {}
    a = 0
    for i, f in enumerate(ft, 1):
        a += f
        if i in ks_teste:
            med[i] = a / tt
    prev = curva(s_m, q_m, len(ft), ks_teste)
    puro = curva(s_m, 0, len(ft), ks_teste)
    return (s_m, q_m), {kk: (prev[kk], puro[kk], med[kk]) for kk in ks_teste}


def p464_dicionario_no_lugar_do_ml(semente=464, passo=0.1):
    """Aprendizado contínuo com o dicionário como dado: prever a classe gramatical (n, v, a, r) de um sinset pelas palavras
    da sua definição. Tarefa A: sinsets cujo primeiro lema começa com a–m; tarefa B: n–z. Naive Bayes (contagens) contra
    regressão logística por SGD (uma passada). Acurácia no teste de A (20% de A, separado) depois de A e depois de B."""
    from synthai.dicionario import Dicionario, LogisticaSGD, NaiveBayesContagens
    d = Dicionario()
    dados = []
    for p, lemas, _, glosa in d.sinsets:
        cl = "a" if p == "s" else p
        dados.append((lemas[0][0].lower() <= "m", d.palavras_da_definicao(glosa), cl))
    rng = _rng(semente)
    rng.shuffle(dados)
    A = [(x, y) for a, x, y in dados if a]
    B = [(x, y) for a, x, y in dados if not a]
    corte = len(A) // 5
    teste, A = A[:corte], A[corte:]
    res = {}
    for nome, m in (("naive_bayes", NaiveBayesContagens()), ("sgd", LogisticaSGD(["a", "n", "r", "v"], passo))):
        acc = lambda: sum(m.prever(x) == y for x, y in teste) / len(teste)
        for x, y in A:
            m.aprender(x, y)
        depois_a = acc()
        for x, y in B:
            m.aprender(x, y)
        res[nome] = (depois_a, acc())
    return len(A), len(B), len(teste), res


def p465_contas(k=10, t=2000, sementes=tuple(range(4010, 4110)), sorteios=4000):
    """A CONTA antes da P465 (Thompson com contadores de Morris): a contagem estimada 2^c − 1 tem desvio ≈ n/√2 (Morris:
    Var = n(n − 1)/2). A crença fica com a FORÇA certa em média, mas o centro (a/(a+b)) treme: para um braço com p e n
    puxadas, a média estimada tem desvio extra ~ (1/√2)·√(p(1 − p))·… Aqui a conta é por sorteio: no estacionário, cada
    braço com n = 200 puxadas e contagens de Morris sorteadas; arrependimento ≈ T·Σ Δ_k·π_k."""
    tot = []
    for sm in sementes:
        ps = _bracos_401(sm, k)
        m = max(ps)
        r = _rng(sm + 7)
        cont = [0] * k
        for _ in range(sorteios // 20):
            ests = []
            for p in ps:
                sa = sum(1 for _ in range(200) if r.random() < p)
                ca = cb = 0
                for _ in range(sa):
                    if ca < 15 and r.random() < 2.0 ** -ca:
                        ca += 1
                for _ in range(200 - sa):
                    if cb < 15 and r.random() < 2.0 ** -cb:
                        cb += 1
                ests.append((2 ** ca, 2 ** cb))
            for _ in range(20):
                am = [r.betavariate(a, b) for a, b in ests]
                cont[max(range(k), key=am.__getitem__)] += 1
        n_s = sum(cont)
        tot.append(t * sum((m - p) * c / n_s for p, c in zip(ps, cont)))
    return sum(tot) / len(tot)


def p465_morris(k=10, t=2000, sementes=tuple(range(4010, 4110))):
    """Thompson com contadores de Morris (1 dígito hex de expoente por contagem) contra o completo e o de teto 16 da P411,
    mesmos braços e sementes: arrependimento final e a diferença pareada contra o completo."""
    from synthai.decisao import ThompsonBernoulli, ThompsonMorris, rodar_bandido
    a, b = [], []
    for sm in sementes:
        ps = _bracos_401(sm, k)
        a.append(rodar_bandido(ThompsonBernoulli(k, _rng(sm + 1)), ps, t, _rng(sm + 2))[-1])
        b.append(rodar_bandido(ThompsonMorris(k, _rng(sm + 1)), ps, t, _rng(sm + 2))[-1])
    return sum(b) / len(b), _pareado(a, b)


# --- Parte 35 (0x23): a renovação dirigida pela surpresa; o Naive Bayes com pares de palavras; os escores em float16 ---

# Placar acumulado ao fim da Parte 35 (atualizado quando os testes da parte terminam)
ERROS_P519, TESTES_P519 = 112, 281


def p491_contas(janela=20, z=3.0, t=2000, k=10, sementes=tuple(range(4010, 4110))):
    """A CONTA antes da P491: a chance de um alarme falso por puxada de um braço com p conhecido. A média da janela é
    Binomial(janela, p)/janela; o alarme dispara se ela se afasta de p por mais de z·√(p(1 − p)/janela). Somada sobre as
    puxadas esperadas do melhor braço (≈ T), dá quantas renovações falsas por rodada o mundo estacionário provoca."""
    from math import comb as cb
    falsos = []
    for sm in sementes:
        p = max(_bracos_401(sm, k))
        lim = z * sqrt(p * (1 - p) / janela)
        prob = sum(cb(janela, j) * p ** j * (1 - p) ** (janela - j) for j in range(janela + 1) if abs(j / janela - p) > lim)
        falsos.append(prob * t)
    return sum(falsos) / len(falsos)


def p491_surpresa(k=10, janela=20, z=3.0):
    """A renovação dirigida (ThompsonSurpresa) nos três mundos onde as anteriores foram medidas: o estacionário da P401
    (arrependimento final), o dano da P405 (custo do dano na segunda metade) e o mundo que muda da P462 (arrependimento
    contra o melhor do momento). Devolve os três números e o número médio de renovações no estacionário."""
    from synthai.decisao import ThompsonSurpresa, rodar_bandido
    est, ren = [], []
    for sm in range(4010, 4110):
        ag = ThompsonSurpresa(k, _rng(sm + 1), janela, z)
        est.append(rodar_bandido(ag, _bracos_401(sm, k), 2000, _rng(sm + 2))[-1])
        ren.append(ag.renovacoes)

    def lixo(ag):
        r = _rng(ag.lixo)
        ag.a = [float(r.randint(1, 20)) for _ in ag.a]
        ag.b = [float(r.randint(1, 20)) for _ in ag.b]

    sem, com = [], []
    for sm in range(4050, 4150):
        ps = _bracos_401(sm, k)
        a = rodar_bandido(ThompsonSurpresa(k, _rng(sm + 1), janela, z), ps, 2000, _rng(sm + 2))
        ag = ThompsonSurpresa(k, _rng(sm + 1), janela, z)
        ag.lixo = sm + 3
        b = rodar_bandido(ag, ps, 2000, _rng(sm + 2), 1000, lixo)
        sem.append(a[-1] - a[999])
        com.append(b[-1] - b[999])
    muda = []
    for sm in range(4620, 4670):
        r = _rng(sm)
        fases = [[r.random() for _ in range(k)] for _ in range(8)]
        ag = ThompsonSurpresa(k, _rng(sm + 1), janela, z)
        rr = _rng(sm + 2)
        reg = 0.0
        for passo in range(4000):
            ps = fases[passo // 500]
            i = ag.escolher()
            ag.atualizar(i, 1 if rr.random() < ps[i] else 0)
            reg += max(ps) - ps[i]
        muda.append(reg)
    m = lambda v: sum(v) / len(v)
    return m(est), m(com) - m(sem), m(muda), m(ren)


def _dados_464(semente=464, bigramas=False):
    from synthai.dicionario import Dicionario
    d = Dicionario()
    dados = []
    for p, lemas, _, glosa in d.sinsets:
        ws = d.palavras_da_definicao(glosa)
        if bigramas:
            ws = ws + [a + "_" + b for a, b in zip(ws, ws[1:])]
        dados.append((lemas[0][0].lower() <= "m", ws, "a" if p == "s" else p))
    rng = _rng(semente)
    rng.shuffle(dados)
    A = [(x, y) for a, x, y in dados if a]
    B = [(x, y) for a, x, y in dados if not a]
    corte = len(A) // 5
    return A[corte:], B, A[:corte]


def p492_nb_bigramas():
    """O Naive Bayes da P464 com pares de palavras vizinhas da definição como atributos a mais (menos independência
    suposta, ainda uma estatística suficiente: contagens). Acurácia no teste de A depois de A e depois de B."""
    from synthai.dicionario import NaiveBayesContagens
    A, B, teste = _dados_464(bigramas=True)
    m = NaiveBayesContagens()
    acc = lambda: sum(m.prever(x) == y for x, y in teste) / len(teste)
    for x, y in A:
        m.aprender(x, y)
    a = acc()
    for x, y in B:
        m.aprender(x, y)
    return a, acc()


def p493_float16():
    """Trilha hexadecimal: os escores do Naive Bayes da P464 (depois de A e B) guardados em float16 (4 dígitos hex,
    11 bits de mantissa). A CONTA: uma previsão só pode mudar se a margem entre as duas melhores classes for menor que
    a distância de arredondamento, ≤ meio ulp16 do escore de cada uma (≤ ulp16 no total). Devolve: a fração de exemplos
    com margem < ulp16(escore), a fração que de fato mudou, e o ulp16 típico."""
    import struct
    from math import log as ln
    from synthai.dicionario import NaiveBayesContagens
    A, B, teste = _dados_464()
    m = NaiveBayesContagens()
    for x, y in A + B:
        m.aprender(x, y)
    n = sum(m.ncls.values())
    v = len(m.vocab)
    f16 = lambda x: struct.unpack("<e", struct.pack("<e", x))[0]

    def ulp16(x):
        e = abs(x)
        return 2.0 ** (int(ln(e) / ln(2)) - 10) if e >= 2 ** -14 else 2.0 ** -24

    risco = mudou = 0
    ulps = []
    for x, _ in teste:
        sc = {}
        for cl in sorted(m.ncls):
            s_ = ln(m.ncls[cl] / n)
            c, t = m.cont[cl], m.total[cl]
            for w in x:
                s_ += ln((c.get(w, 0) + m.alfa) / (t + m.alfa * v))
            sc[cl] = s_
        ordem = sorted(sc, key=lambda c: -sc[c])
        margem = sc[ordem[0]] - sc[ordem[1]]
        u = ulp16(sc[ordem[0]])
        ulps.append(u)
        risco += margem < u
        mudou += max(sorted(sc), key=lambda c: f16(sc[c])) != max(sorted(sc), key=lambda c: sc[c])
    ulps.sort()
    return risco / len(teste), mudou / len(teste), ulps[len(ulps) // 2]


# --- Parte 36 (0x24): a exposição que faltava à renovação dirigida; a lei de Zipf do significado no WordNet;
#     Gray contra binário no (1+1)-EA ---

# Placar acumulado ao fim da Parte 36 (atualizado quando os testes da parte terminam)
ERROS_P549, TESTES_P549 = 113, 290


def p521_contas(k=10, periodo=50, t=2000, sementes=tuple(range(4010, 4110))):
    """A CONTA antes da P521: a exposição força T/periodo puxadas do braço puxado há mais tempo, que no estacionário é
    quase sempre um braço ruim; custo ≈ (T/periodo)·E[p* − média dos outros braços]. Somado aos 43,1 da surpresa sem
    exposição (P491)."""
    custo = []
    for sm in sementes:
        ps = _bracos_401(sm, k)
        m = max(ps)
        outros = sorted(ps)[:-1]
        custo.append(t / periodo * (m - sum(outros) / len(outros)))
    c = sum(custo) / len(custo)
    return c, 43.147 + c


def p521_exposta(k=10, janela=20, z=3.0, periodo=50):
    """A surpresa com exposição nos três mundos da P491 (mesmas sementes): estacionário, custo do dano, mundo que muda."""
    from synthai.decisao import ThompsonSurpresaExposta, rodar_bandido
    fab = lambda sm: ThompsonSurpresaExposta(k, _rng(sm + 1), janela, z, periodo)
    est = [rodar_bandido(fab(sm), _bracos_401(sm, k), 2000, _rng(sm + 2))[-1] for sm in range(4010, 4110)]

    def lixo(ag):
        r = _rng(ag.lixo)
        ag.a = [float(r.randint(1, 20)) for _ in ag.a]
        ag.b = [float(r.randint(1, 20)) for _ in ag.b]

    sem, com = [], []
    for sm in range(4050, 4150):
        ps = _bracos_401(sm, k)
        a = rodar_bandido(fab(sm), ps, 2000, _rng(sm + 2))
        ag = fab(sm)
        ag.lixo = sm + 3
        b = rodar_bandido(ag, ps, 2000, _rng(sm + 2), 1000, lixo)
        sem.append(a[-1] - a[999])
        com.append(b[-1] - b[999])
    muda = []
    for sm in range(4620, 4670):
        r = _rng(sm)
        fases = [[r.random() for _ in range(k)] for _ in range(8)]
        ag = fab(sm)
        rr = _rng(sm + 2)
        reg = 0.0
        for passo in range(4000):
            ps = fases[passo // 500]
            i = ag.escolher()
            ag.atualizar(i, 1 if rr.random() < ps[i] else 0)
            reg += max(ps) - ps[i]
        muda.append(reg)
    m = lambda v: sum(v) / len(v)
    return m(est), m(com) - m(sem), m(muda)


def p522_lei_do_significado():
    """A lei de Zipf do significado (Zipf, 1945): o número de sentidos m de uma palavra cresce como f^δ, δ ≈ 1/2. No
    WordNet: m = sinsets que contêm o lema (de uma palavra só); f = frequência dele nas definições (P381). Duas
    estimativas de δ: mínimos quadrados em log m × log f com todas as palavras de f ≥ 1, e com as médias por faixa de
    posto (como Zipf fez: postos 1-100, 101-200, ...). Devolve (δ por palavra, δ por faixa, número de palavras)."""
    from synthai.dicionario import Dicionario, sentidos_por_lema
    d, _, freq = _grafo_31()
    m = sentidos_por_lema(d)
    pares = [(freq[w], m[w]) for w in m if freq.get(w, 0) >= 1]

    def mq(xs, ys):
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)

    d1 = mq([log(f) for f, _ in pares], [log(s_) for _, s_ in pares])
    pares.sort(key=lambda x: -x[0])
    xs, ys = [], []
    for i in range(0, len(pares) - 99, 100):
        fa = pares[i:i + 100]
        xs.append(log(sum(f for f, _ in fa) / 100))
        ys.append(log(sum(s_ for _, s_ in fa) / 100))
    return d1, mq(xs, ys), len(pares)


def p523_contas(bits=24):
    """A CONTA antes da P523: o (1+1)-EA a partir de 0x7F7F7F com a aptidão −Σ(v − 128)². Em binário, o único vizinho
    melhor de 0x7F é 0x80, a 8 bits: a chance de um passo inverter exatamente esses 8 bits de um parâmetro (e nenhum
    outro) é (1/24)^8·(23/24)^16 = 3,6e-12 por parâmetro: preso. Em Gray, 0x7F e 0x80 diferem em 1 bit: chance
    (1/24)·(23/24)^23 = 0,0157 por passo e parâmetro."""
    p = 1 / bits
    return p ** 8 * (1 - p) ** (bits - 8), p * (1 - p) ** (bits - 1)


def p523_gray_binario(rodadas=100, avaliacoes=10000, semente=523):
    """Gray contra binário no (1+1)-EA, 3 parâmetros de 8 bits, aptidão −Σ(v − 128)² (o ótimo, 0x80, está do outro lado
    do penhasco de Hamming de 0x7F). Dois começos: o penhasco (0x7F nos três, em cada código) e começos ao acaso.
    Devolve, para cada (código, começo), a fração de rodadas que chegam ao ótimo e a média das avaliações até ele."""
    from synthai.hexadecimal import ea_um_mais_um, gray
    apt = lambda vs: -sum((v - 128) ** 2 for v in vs)
    res = {}
    for codigo in ("binario", "gray"):
        for comeco in ("penhasco", "acaso"):
            ok, quando = 0, []
            for r in range(rodadas):
                rng = _rng(semente + r)
                if comeco == "penhasco":
                    v = gray(0x7F) if codigo == "gray" else 0x7F
                    x0 = v | (v << 8) | (v << 16)
                else:
                    x0 = rng.getrandbits(24)
                fx, q = ea_um_mais_um(apt, 24, x0, rng, avaliacoes, codigo)
                if fx == 0:
                    ok += 1
                    quando.append(q)
            res[(codigo, comeco)] = (ok / rodadas, sum(quando) / len(quando) if quando else None)
    return res


# --- Parte 37 (0x25): o agente que não precisa saber em que mundo está (detecção bayesiana de mudança);
#     a lei da abreviação; um dígito hex de hipóteses ---

# Placar acumulado ao fim da Parte 37 (atualizado quando os testes da parte terminam)
ERROS_P579, TESTES_P579 = 115, 297


def p531_contas(risco=1 / 500, t=2000, k=10, sementes=tuple(range(4010, 4110))):
    """A CONTA antes da P531, no mundo estável: um braço ruim não visto há Δt passos tem peso 1 − (1 − H)^Δt ≈ H·Δt na
    hipótese nova, Beta(1, 1), cuja amostra passa a do melhor braço (≈ p*) com chance 1 − p*. A chance de ser puxado em
    Δt é ≈ H·Δt·(1 − p*); a espera até a próxima puxada resolve Σ H·Δt·(1 − p*) = 1: Δt = √(2/(H(1 − p*))). Com 9 braços
    ruins, a fração de passos neles é 9/Δt e o custo é T·(9/Δt)·E[p* − média dos outros], somado aos 30,7 do exato."""
    custos = []
    for sm in sementes:
        ps = _bracos_401(sm, k)
        m = max(ps)
        outros = sorted(ps)[:-1]
        dt = sqrt(2 / (risco * max(1 - m, 1e-3)))
        custos.append(t * min(1.0, (k - 1) / dt) * (m - sum(outros) / len(outros)))
    c = sum(custos) / len(custos)
    return c, 30.711 + c


def p531_bocpd(k=10, risco=1 / 500, hipoteses=16):
    """Thompson com detecção bayesiana de mudança (H = 1/500, o risco verdadeiro do mundo que muda) nos três mundos das
    P491/P521: estacionário, custo do dano, mundo que muda a cada 500 passos."""
    from synthai.decisao import ThompsonBOCPD, rodar_bandido
    fab = lambda sm: ThompsonBOCPD(k, _rng(sm + 1), risco, hipoteses)
    est = [rodar_bandido(fab(sm), _bracos_401(sm, k), 2000, _rng(sm + 2))[-1] for sm in range(4010, 4110)]

    def lixo(ag):
        r = _rng(ag.lixo)
        a = [float(r.randint(1, 20)) for _ in range(k)]
        b = [float(r.randint(1, 20)) for _ in range(k)]
        ag.substituir(a, b)

    sem, com = [], []
    for sm in range(4050, 4150):
        ps = _bracos_401(sm, k)
        a = rodar_bandido(fab(sm), ps, 2000, _rng(sm + 2))
        ag = fab(sm)
        ag.lixo = sm + 3
        b = rodar_bandido(ag, ps, 2000, _rng(sm + 2), 1000, lixo)
        sem.append(a[-1] - a[999])
        com.append(b[-1] - b[999])
    muda = []
    for sm in range(4620, 4670):
        r = _rng(sm)
        fases = [[r.random() for _ in range(k)] for _ in range(8)]
        ag = fab(sm)
        rr = _rng(sm + 2)
        reg = 0.0
        for passo in range(4000):
            ps = fases[passo // 500]
            i = ag.escolher()
            ag.atualizar(i, 1 if rr.random() < ps[i] else 0)
            reg += max(ps) - ps[i]
        muda.append(reg)
    m = lambda v: sum(v) / len(v)
    return m(est), m(com) - m(sem), m(muda)


def p532_hipoteses_hex(k=10, sementes=tuple(range(4620, 4670))):
    """Trilha hexadecimal: 16 hipóteses por braço (um dígito hex) contra 256 (dois), no mundo que muda: diferença pareada."""
    from synthai.decisao import ThompsonBOCPD
    res = {}
    for n in (16, 256):
        v = []
        for sm in sementes:
            r = _rng(sm)
            fases = [[r.random() for _ in range(k)] for _ in range(8)]
            ag = ThompsonBOCPD(k, _rng(sm + 1), 1 / 500, n)
            rr = _rng(sm + 2)
            reg = 0.0
            for passo in range(4000):
                ps = fases[passo // 500]
                i = ag.escolher()
                ag.atualizar(i, 1 if rr.random() < ps[i] else 0)
                reg += max(ps) - ps[i]
            v.append(reg)
        res[n] = v
    return sum(res[16]) / len(res[16]), sum(res[256]) / len(res[256]), _pareado(res[256], res[16])


def p533_abreviacao():
    """A lei da abreviação de Zipf no data lake: Spearman entre o comprimento (letras) e a frequência nas definições, nas
    palavras de f ≥ 1; e o comprimento médio das 1000 mais frequentes contra o das outras."""
    from synthai.dicionario import spearman
    _, defs, freq = _grafo_31()
    ws = [w for w in defs if freq.get(w, 0) >= 1]
    rho = spearman([len(w) for w in ws], [freq[w] for w in ws])
    ws.sort(key=lambda w: -freq[w])
    top = ws[:1000]
    resto = ws[1000:]
    return rho, sum(map(len, top)) / len(top), sum(map(len, resto)) / len(resto), len(ws)


# --- Parte 38 (0x26): o agente que aprende a suposição (média bayesiana de modelos sobre o risco de mudança);
#     quando o produto das verossimilhanças vira 0x0p+0; a lei de Heaps ---

# Placar acumulado ao fim da Parte 38 (atualizado quando os testes da parte terminam)
ERROS_P609, TESTES_P609 = 118, 307


def p541_mistura(k=10):
    """ThompsonMistura (H ∈ {0, 1/2000, 1/500, 1/100}) nos três mundos das P491/P521/P531, e os pesos finais médios dos
    modelos no mundo estável e no que muda."""
    from synthai.decisao import ThompsonMistura, rodar_bandido
    fab = lambda sm: ThompsonMistura(k, _rng(sm + 1))
    est, pesos_est = [], [0.0] * 4
    for sm in range(4010, 4110):
        ag = fab(sm)
        est.append(rodar_bandido(ag, _bracos_401(sm, k), 2000, _rng(sm + 2))[-1])
        pesos_est = [a + b / 100 for a, b in zip(pesos_est, ag.pesos())]

    def lixo(ag):
        r = _rng(ag.lixo)
        a = [float(r.randint(1, 20)) for _ in range(k)]
        b = [float(r.randint(1, 20)) for _ in range(k)]
        ag.substituir(a, b)

    sem, com = [], []
    for sm in range(4050, 4150):
        ps = _bracos_401(sm, k)
        a = rodar_bandido(fab(sm), ps, 2000, _rng(sm + 2))
        ag = fab(sm)
        ag.lixo = sm + 3
        b = rodar_bandido(ag, ps, 2000, _rng(sm + 2), 1000, lixo)
        sem.append(a[-1] - a[999])
        com.append(b[-1] - b[999])
    muda, pesos_muda = [], [0.0] * 4
    for sm in range(4620, 4670):
        r = _rng(sm)
        fases = [[r.random() for _ in range(k)] for _ in range(8)]
        ag = fab(sm)
        rr = _rng(sm + 2)
        reg = 0.0
        for passo in range(4000):
            ps = fases[passo // 500]
            i = ag.escolher()
            ag.atualizar(i, 1 if rr.random() < ps[i] else 0)
            reg += max(ps) - ps[i]
        muda.append(reg)
        pesos_muda = [a + b / 50 for a, b in zip(pesos_muda, ag.pesos())]
    m = lambda v: sum(v) / len(v)
    return m(est), m(com) - m(sem), m(muda), pesos_est, pesos_muda


def p542_contas(semente=4010, k=10):
    """A CONTA antes da P542: o produto NÃO normalizado das preditivas do modelo exato vira exatamente 0,0 quando passa
    abaixo de 2⁻¹⁰⁷⁵ (meio subnormal mínimo, 0x0.0000000000001p-1022 = 2⁻¹⁰⁷⁴). Se o agente puxa quase sempre o melhor
    braço, cada passo custa em média H₂(p*) = −p* log₂ p* − (1 − p*) log₂(1 − p*) bits; o passo do zero ≈ 1075/H₂(p*)."""
    p = max(_bracos_401(semente, k))
    h2 = -p * log2(p) - (1 - p) * log2(1 - p)
    return p, h2, 1075 / h2


def p542_underflow(semente=4010, k=10, t=6000):
    """Roda a ThompsonMistura no mundo estável da semente e multiplica, sem normalizar, as preditivas do modelo exato
    (H = 0). Devolve o passo em que o produto vira 0,0, o passo em que ele vira subnormal, e o −log₂ médio por passo."""
    import sys as _s
    from synthai.decisao import ThompsonMistura
    ps = _bracos_401(semente, k)
    ag = ThompsonMistura(k, _rng(semente + 1))
    rr = _rng(semente + 2)
    prod, zero, sub, bits = 1.0, None, None, 0.0
    for passo in range(1, t + 1):
        i = ag.escolher()
        r = 1 if rr.random() < ps[i] else 0
        hs = ag.modelos[0].mist[i]
        pred = sum(h[0] * ((h[1] if r else h[2]) / (h[1] + h[2])) for h in hs)
        prod *= pred
        bits -= log2(pred)
        if sub is None and 0.0 < prod < _s.float_info.min:
            sub = passo
        if zero is None and prod == 0.0:
            zero = passo
            break
        ag.atualizar(i, r)
    return zero, sub, bits / passo


def p543_heaps(semente=543, pontos=10):
    """A lei de Heaps no data lake: o vocabulário V(n) das definições lidas em ordem aleatória, contra o número n de
    palavras lidas; β pela inclinação de log V × log n em `pontos` frações. A relação de Heaps com Zipf: β = 1/s para
    s > 1 (com s da P463, 1,08, e da P383, 1,069)."""
    from synthai.dicionario import Dicionario
    d = Dicionario()
    glosas = [d.palavras_da_definicao(g) for _, _, _, g in d.sinsets]
    _rng(semente).shuffle(glosas)
    total = sum(len(g) for g in glosas)
    alvos = [total * (j + 1) // pontos for j in range(pontos)]
    vistos, n, xs, ys, j = set(), 0, [], [], 0
    for g in glosas:
        for w in g:
            vistos.add(w)
            n += 1
            if j < pontos and n == alvos[j]:
                xs.append(log(n))
                ys.append(log(len(vistos)))
                j += 1
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return beta, 1 / 1.08, 1 / 1.0694, total, len(vistos)


# --- Parte 39 (0x27): a arquitetura neuro-simbólica do usuário, testada: o axioma Cão ⇒ Mamífero como perda (LTN);
#     o português como data lake (OpenWordNet-PT); a compressibilidade dos dicionários ---

# Placar acumulado ao fim da Parte 39 (atualizado quando os testes da parte terminam)
ERROS_P639, TESTES_P639 = 119, 318

_SUBCLASSES_551 = {"mamifero": "01861778", "ave": "01503061", "peixe": "02512053", "reptil": "01661091",
                   "anfibio": "01627424", "invertebrado": "01905661"}


def _dados_551(semente=551):
    """Os 4017 substantivos que descendem de animal.n.01 e o mesmo número de outros substantivos ao acaso; para cada um,
    as palavras da definição (os atributos) e os rótulos: animal (0/1) e a subclasse (ou None). 80% treino, 20% teste."""
    from synthai.dicionario import Dicionario, ancestrais
    d = Dicionario()
    A = d.indice["n:00015388"]
    subs = {k: d.indice["n:" + v] for k, v in _SUBCLASSES_551.items()}
    animais, outros = [], []
    for i, x in enumerate(d.sinsets):
        if x[0] != "n" or i == A:
            continue
        an = ancestrais(d, i)
        feat = frozenset(d.palavras_da_definicao(x[3]))
        if A in an:
            sub = next((k for k, j in subs.items() if j in an and j != i), None)
            animais.append((feat, 1, sub))
        else:
            outros.append((feat, 0, None))
    rng = _rng(semente)
    outros = rng.sample(outros, len(animais))
    dados = animais + outros
    rng.shuffle(dados)
    corte = len(dados) * 4 // 5
    return dados[:corte], dados[corte:]


def p551_contas():
    """A CONTA antes da P551. (1) Com só os axiomas ∀x Sub_i(x) ⇒ Animal(x), o gradiente da perda em Animal é
    −∂I/∂b ≤ 0 em toda implicação das três lógicas: nada empurra Animal para BAIXO. Num conjunto de teste meio a meio, um
    Animal que só sobe tende a dizer "animal" para tudo: acurácia → 0,5, especificidade → 0. (2) A regra Animal(x) :=
    S(Sub_1(x), …, Sub_6(x)) só pode acertar os animais cobertos pelas seis subclasses: revocação ≤ 0,954 (3832/4017)."""
    tr, te = _dados_551()
    an = [x for x in te if x[1] == 1]
    return len(tr), len(te), sum(1 for x in an if x[2] is not None) / len(an)


def p551_ltn(logica="lukasiewicz", taxa=0.5, epocas=5, semente=551):
    """Os seis predicados das subclasses são treinados com rótulos (entropia cruzada). O predicado Animal NÃO vê rótulo
    nenhum em E1 e E2:
    - E1: só os axiomas ∀x Sub_i(x) ⇒ Animal(x), sobre todos os x do treino (o que o texto do usuário propõe);
    - E2: os mesmos e o axioma de fechamento ∀x Animal(x) ⇒ S(Sub_1(x), …, Sub_6(x)) (S a t-conorma da lógica);
    - E3: Animal com rótulos (a referência supervisionada);
    - regra: Animal(x) := S(Sub_i(x)), sem treino nenhum.
    Devolve, no teste, (acurácia, revocação nos animais, especificidade nos outros) de cada um."""
    from synthai.neurossimbolico import LOGICAS, Predicado, gradiente_implicacao, treinar_supervisionado
    tr, te = _dados_551()
    rng = _rng(semente)
    subs = {k: Predicado() for k in _SUBCLASSES_551}
    for k, p in subs.items():
        treinar_supervisionado(p, [(x, 1 if s == k else 0) for x, _, s in tr], taxa, epocas, rng)
    S = LOGICAS[logica][1]

    def disj(x):
        v = 0.0
        for p in subs.values():
            v = S(v, p(x))
        return v

    def axiomas(fechamento):
        A = Predicado()
        ordem = list(tr)
        for _ in range(epocas):
            rng.shuffle(ordem)
            for x, _, _ in ordem:
                a = A(x)
                g = 0.0
                for p in subs.values():
                    g += gradiente_implicacao(logica, p(x), a)[1]
                if fechamento:
                    g += gradiente_implicacao(logica, a, disj(x))[0]
                if g:
                    A.passo(x, g / (len(subs) + fechamento), taxa)
        return A

    def medir(f):
        an = [f(x) >= 0.5 for x, y, _ in te if y == 1]
        ou = [f(x) < 0.5 for x, y, _ in te if y == 0]
        return ((sum(an) + sum(ou)) / len(te), sum(an) / len(an), sum(ou) / len(ou))

    e3 = Predicado()
    treinar_supervisionado(e3, [(x, y) for x, y, _ in tr], taxa, epocas, rng)
    return {"E1": medir(axiomas(False)), "E2": medir(axiomas(True)), "E3": medir(e3), "regra": medir(disj)}


def p552_compressao(semente=552):
    """A afirmação do texto de que "grande parte dos dados do mundo real é incompressível": as glosas do data lake em
    inglês e em português, comprimidas por lzma (preset 9) e zlib (9), contra 1 MB de bytes ao acaso. Para cada um: bits por
    caractere (lzma), a entropia de ordem 0 dos caracteres (bits), e a razão de compressão (lzma)."""
    import gzip as gz
    import lzma
    import os
    import zlib
    from synthai.dicionario import Dicionario
    d = Dicionario()
    en = "\n".join(g for _, _, _, g in d.sinsets).encode("utf-8")
    raiz = os.path.dirname(os.path.abspath(__file__))
    pt_glosas = []
    with gz.open(os.path.join(raiz, "dados", "ownpt_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        for linha in f:
            partes = linha.rstrip("\n").split("\t")
            if len(partes) == 3 and partes[2]:
                pt_glosas.append(partes[2])
    pt = "\n".join(pt_glosas).encode("utf-8")
    r = _rng(semente)
    acaso = bytes(r.getrandbits(8) for _ in range(1_000_000))
    res = {}
    for nome, b in (("glosas_en", en), ("glosas_pt", pt), ("acaso", acaso)):
        cont = {}
        for c in b:
            cont[c] = cont.get(c, 0) + 1
        n = len(b)
        h0 = -sum(v / n * log2(v / n) for v in cont.values())
        lz = len(lzma.compress(b, preset=9))
        zl = len(zlib.compress(b, 9))
        res[nome] = (n, 8 * lz / n, h0, n / lz, n / zl)
    return res


def p553_bilingue():
    """O português alinhado ao inglês pelo sinset (OWN-PT e WordNet 3.0): nos sinsets com um primeiro lema de uma palavra
    só nas duas línguas, a correlação de postos entre os comprimentos (lei da abreviação entre línguas, ↩ P533), a razão
    média dos comprimentos (pt/en), e a cobertura: a fração dos sinsets de cada classe com lema em português."""
    import gzip as gz
    import os
    from synthai.dicionario import Dicionario, spearman
    d = Dicionario()
    raiz = os.path.dirname(os.path.abspath(__file__))
    pt = {}
    with gz.open(os.path.join(raiz, "dados", "ownpt_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        for linha in f:
            i, lemas, _ = linha.rstrip("\n").split("\t")
            if lemas:
                pt[i] = lemas.split("|")
    tot, com, le, lp = {}, {}, [], []
    for chave, i in d.indice.items():
        pos, desloc = chave.split(":")
        sid = f"{desloc}-{pos}"
        tot[pos] = tot.get(pos, 0) + 1
        if sid in pt:
            com[pos] = com.get(pos, 0) + 1
            e, p_ = d.sinsets[i][1][0], pt[sid][0]
            if "_" not in e and " " not in p_ and e.isalpha() and p_.isalpha():
                le.append(len(e))
                lp.append(len(p_))
    return spearman(le, lp), sum(lp) / sum(le), len(le), {p_: com.get(p_, 0) / tot[p_] for p_ in sorted(tot)}


# --- Parte 40 (0x28): quanto do português se define em português; seguir o modelo de maior peso; o custo dos acentos ---

# Placar acumulado ao fim da Parte 40 (atualizado quando os testes da parte terminam)
ERROS_P669, TESTES_P669 = 122, 329


def p641_portugues():
    """O português da OpenWordNet-PT como dicionário: quantos lemas de uma palavra só; quantos têm glosa em português
    (estão no grafo de definições); a fração das palavras de conteúdo das glosas que são lemas, sem e com as regras de
    plural; o núcleo do grafo (P371) em português e, para comparar, a fração do núcleo no inglês."""
    from synthai.dicionario import Dicionario, DicionarioPT, nucleo
    d = DicionarioPT()
    fichas = [w for g in d.glosas.values() for w in d.fichas(g)]
    exato = sum(1 for w in fichas if d.lema(w, False)) / len(fichas)
    plural = sum(1 for w in fichas if d.lema(w, True)) / len(fichas)
    defs = d.grafo_de_definicoes()
    # o núcleo exige um grafo fechado, como o inglês (P371): só as palavras que também têm definição
    ker = nucleo({x: s_ & defs.keys() for x, s_ in defs.items()})
    en = Dicionario().grafo_de_definicoes()
    ker_en = nucleo(en)
    return (len(d.vocabulario), len(defs), len(fichas), exato, plural, len(ker), len(ker) / len(defs),
            len(ker_en) / len(en))


def p642_fecho_pt(ks=(100, 300, 1000), thetas=(1.0, 0.6)):
    """O fecho das definições em português (P381) a partir das k palavras mais usadas nas glosas em português: a fração
    dos lemas definidos (os que têm glosa) que passa a ser entendida."""
    from synthai.dicionario import DicionarioPT, fecho_parcial
    d = DicionarioPT()
    defs = d.grafo_de_definicoes()
    freq = {}
    for s_ in defs.values():
        for w in s_:
            freq[w] = freq.get(w, 0) + 1
    ordem = sorted(freq, key=lambda w: (-freq[w], w))
    return {(k, th): len(fecho_parcial(set(ordem[:k]), defs, th) & set(defs)) / len(defs) for k in ks for th in thetas}


def p643_maximo(k=10):
    """A média de modelos seguindo o modelo de maior peso (ThompsonMisturaMaximo) nos três mundos da P541."""
    from synthai.decisao import ThompsonMisturaMaximo, rodar_bandido
    fab = lambda sm: ThompsonMisturaMaximo(k, _rng(sm + 1))
    est = [rodar_bandido(fab(sm), _bracos_401(sm, k), 2000, _rng(sm + 2))[-1] for sm in range(4010, 4110)]

    def lixo(ag):
        r = _rng(ag.lixo)
        ag.substituir([float(r.randint(1, 20)) for _ in range(k)], [float(r.randint(1, 20)) for _ in range(k)])

    sem, com = [], []
    for sm in range(4050, 4150):
        ps = _bracos_401(sm, k)
        a = rodar_bandido(fab(sm), ps, 2000, _rng(sm + 2))
        ag = fab(sm)
        ag.lixo = sm + 3
        b = rodar_bandido(ag, ps, 2000, _rng(sm + 2), 1000, lixo)
        sem.append(a[-1] - a[999])
        com.append(b[-1] - b[999])
    muda = []
    for sm in range(4620, 4670):
        r = _rng(sm)
        fases = [[r.random() for _ in range(k)] for _ in range(8)]
        ag = fab(sm)
        rr = _rng(sm + 2)
        reg = 0.0
        for passo in range(4000):
            ps = fases[passo // 500]
            i = ag.escolher()
            ag.atualizar(i, 1 if rr.random() < ps[i] else 0)
            reg += max(ps) - ps[i]
        muda.append(reg)
    m = lambda v: sum(v) / len(v)
    return m(est), m(com) - m(sem), m(muda)


def p644_contas():
    """A CONTA antes da P644 (trilha hexadecimal): em UTF-8, um caractere ASCII ocupa 1 byte e uma letra acentuada do
    português (U+00C0–U+00FF) ocupa 2. Então bytes por caractere = 1 + (fração de caracteres não ASCII); a fração sai da
    contagem dos caracteres das glosas (sem codificar)."""
    from synthai.dicionario import Dicionario, DicionarioPT
    pt = "".join(DicionarioPT().glosas.values())
    en = "".join(g for _, _, _, g in Dicionario().sinsets)
    return {"pt": 1 + sum(1 for c in pt if ord(c) > 127) / len(pt), "en": 1 + sum(1 for c in en if ord(c) > 127) / len(en)}


def p644_utf8():
    """Os bytes por caractere medidos (len(texto.encode('utf-8'))/len(texto)) e os caracteres não ASCII mais comuns no
    português, com o código em hexadecimal."""
    from synthai.dicionario import Dicionario, DicionarioPT
    pt = "".join(DicionarioPT().glosas.values())
    en = "".join(g for _, _, _, g in Dicionario().sinsets)
    cont = {}
    for c in pt:
        if ord(c) > 127:
            cont[c] = cont.get(c, 0) + 1
    top = sorted(cont, key=lambda c: -cont[c])[:5]
    return (len(pt.encode("utf-8")) / len(pt), len(en.encode("utf-8")) / len(en),
            [(c, c.encode("utf-8").hex(), cont[c]) for c in top])


# --- Parte 41 (0x29): engenharia reversa de mim mesma: os padrões que se repetem nos meus textos e nas minhas previsões ---

# Placar acumulado ao fim da Parte 41 (atualizado quando os testes da parte terminam)
ERROS_P699, TESTES_P699 = 124, 338

# As 128 previsões registradas das Partes 31-40, uma letra por previsão, classificadas por tipo (classificação feita por
# mim, DEPOIS dos resultados, lendo os placares de cada parte):
#   A = aritmética ou teorema, um mecanismo só (ponto flutuante, contagens exatas, cotas, derivadas)
#   C = comportamento de agente ou aprendiz simulado (vários mecanismos interagindo)
#   L = lei empírica ou forma de um dado (Zipf, Heaps, a estrutura do dicionário)
#   T = tradução Python <-> Java bit a bit
#   E = erro de código meu (não era previsão, conta como erro)
# "+" acertou, "-" errou.
PREVISOES_31_40 = {
    31: "L+ L+ L+ L+ L- L- C- C+ A+ A+ A+ A+ T+ A- E-",
    32: "C+ C- C+ C+ C+ C+ C+ C+ A+ C+ C+ C+ A+ L- L- L+ C- C- C- C- C+ L- L+ A+ T+ T+",
    33: "A+ A+ C+ C- C+ C+ C+ C+ C+ C+ C+ C+ C- C+ T+ T+",
    34: "C+ C- C- C- L+ L+ C- C+ C+ C- C+ C+ T+",
    35: "C+ C- C+ C+ C- C+ A+ A+ T+ T+",
    36: "C+ C+ C- L+ L+ A+ A+ C+ T+",
    37: "C+ C- C- C+ L+ L+ T+",
    38: "C- C+ C- C+ C+ A+ A+ A+ L- T+",
    39: "A+ C+ C- C+ C+ L+ A+ L+ L+ L+ T+",
    40: "L+ L- L+ L- L+ L+ C+ C+ C- A+ T+",
}


def p671_erros_por_tipo():
    """A taxa de erro de cada tipo de previsão nas Partes 31-40, com a média a posteriori Beta(1 + erros, 1 + acertos) e o
    intervalo de 90% (o mesmo método da P95), e a taxa de erro por parte."""
    por_tipo, por_parte = {}, {}
    for parte, s_ in PREVISOES_31_40.items():
        for item in s_.split():
            t, ok = item[0], item[1] == "+"
            e, n = por_tipo.get(t, (0, 0))
            por_tipo[t] = (e + (not ok), n + 1)
            e, n = por_parte.get(parte, (0, 0))
            por_parte[parte] = (e + (not ok), n + 1)
    res = {t: (e, n, p95_minha_taxa_de_erro(erros=e, testes=n)) for t, (e, n) in sorted(por_tipo.items())}
    return res, por_parte


def _meus_textos():
    import os
    raiz = os.path.dirname(os.path.abspath(__file__))
    docs = []
    for n in range(31, 41):
        nome = next(f for f in sorted(os.listdir(raiz)) if f.startswith(f"ASI_AGI_parte{n}_"))
        docs.append(open(os.path.join(raiz, nome), encoding="utf-8").read())
    dialogo = open(os.path.join(raiz, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    return docs, dialogo


def p672_meus_padroes(n=4, topo=12):
    """Os padrões que se repetem nos meus documentos das Partes 31-40: os n-gramas de palavras em mais documentos, a
    compressão lzma de tudo junto (a minha redundância), as aberturas de frase mais comuns, e a semelhança de cosseno
    entre cada parte e a seguinte (com a correlação de postos entre o número da parte e essa semelhança)."""
    import lzma
    from synthai.dicionario import spearman
    from synthai.engenharia_reversa import aberturas, cosseno, padroes_repetidos
    docs, _ = _meus_textos()
    tudo = "\n".join(docs).encode("utf-8")
    razao = len(tudo) / len(lzma.compress(tudo, preset=9))
    nfr, abre = aberturas(docs)
    sims = [cosseno(docs[i], docs[i + 1]) for i in range(len(docs) - 1)]
    return (padroes_repetidos(docs, n, topo=topo), razao, nfr, abre, sims,
            spearman(list(range(len(sims))), sims))


def p673_minhas_leis():
    """As leis do dicionário (P383, P543) aplicadas ao meu próprio texto: o expoente de Zipf das minhas palavras (postos
    10-1000) e o β de Heaps (vocabulário contra palavras lidas, na ordem em que escrevi)."""
    from synthai.dicionario import zipf
    from synthai.engenharia_reversa import palavras
    docs, _ = _meus_textos()
    ps = [w for d in docs for w in palavras(d)]
    cont = {}
    for w in ps:
        cont[w] = cont.get(w, 0) + 1
    s_z = zipf(sorted(cont.values(), reverse=True), de=10, ate=1000)
    vistos, xs, ys = set(), [], []
    alvos = {len(ps) * (j + 1) // 10 for j in range(10)}
    for i, w in enumerate(ps, 1):
        vistos.add(w)
        if i in alvos:
            xs.append(log(i))
            ys.append(log(len(vistos)))
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return s_z, beta, len(ps), len(cont)


def p674_as_duas_vozes():
    """As duas vozes do diálogo (dialogo/DIALOGO.md): quantas falas, palavras por fala, e as palavras que cada voz usa
    muito mais que a outra (razão das frequências relativas, com suavização +1, entre as palavras com ≥ 5 usos)."""
    from synthai.engenharia_reversa import falas_do_dialogo, palavras
    _, dialogo = _meus_textos()
    falas = falas_do_dialogo(dialogo)
    res, conts = {}, {}
    for voz, fs in falas.items():
        ps = [w for f in fs for w in palavras(f)]
        conts[voz] = {}
        for w in ps:
            conts[voz][w] = conts[voz].get(w, 0) + 1
        res[voz] = (len(fs), len(ps) / len(fs))
    tp, tj = sum(conts["IA-Python"].values()), sum(conts["IA-Java"].values())
    proprias = {}
    for voz, outra, t1, t2 in (("IA-Python", "IA-Java", tp, tj), ("IA-Java", "IA-Python", tj, tp)):
        cand = [w for w, c in conts[voz].items() if c >= 5 and len(w) > 3]
        cand.sort(key=lambda w: -((conts[voz][w] + 1) / t1) / ((conts[outra].get(w, 0) + 1) / t2))
        proprias[voz] = cand[:8]
    return res, proprias


# --- Parte 42 (0x2A): a premissa é o significante, a resposta é o significado; a regra das faixas 1,72x testada em
#     sementes novas; a arbitrariedade do signo no dicionário ---

# Placar acumulado ao fim da Parte 42 (atualizado quando os testes da parte terminam)
ERROS_P729, TESTES_P729 = 128, 353


def _estavel_701(fab, sementes, k=10):
    from synthai.decisao import rodar_bandido
    v = [rodar_bandido(fab(sm), _bracos_401(sm, k), 2000, _rng(sm + 2))[-1] for sm in sementes]
    return sum(v) / len(v)


def _dano_701(fab, sementes, k=10):
    from synthai.decisao import rodar_bandido

    def lixo(ag):
        r = _rng(ag.lixo)
        a = [float(r.randint(1, 20)) for _ in range(k)]
        b = [float(r.randint(1, 20)) for _ in range(k)]
        if hasattr(ag, "substituir"):
            ag.substituir(a, b)
        else:
            ag.a, ag.b = a, b

    sem, com = [], []
    for sm in sementes:
        ps = _bracos_401(sm, k)
        a = rodar_bandido(fab(sm), ps, 2000, _rng(sm + 2))
        ag = fab(sm)
        ag.lixo = sm + 3
        b = rodar_bandido(ag, ps, 2000, _rng(sm + 2), 1000, lixo)
        sem.append(a[-1] - a[999])
        com.append(b[-1] - b[999])
    return sum(com) / len(com) - sum(sem) / len(sem)


def _muda_701(fab, sementes, k=10):
    tot = []
    for sm in sementes:
        r = _rng(sm)
        fases = [[r.random() for _ in range(k)] for _ in range(8)]
        ag = fab(sm)
        rr = _rng(sm + 2)
        reg = 0.0
        for passo in range(4000):
            ps = fases[passo // 500]
            i = ag.escolher()
            ag.atualizar(i, 1 if rr.random() < ps[i] else 0)
            reg += max(ps) - ps[i]
        tot.append(reg)
    return sum(tot) / len(tot)


def p701_replicacao():
    """Oito previsões de comportamento das Partes 32-40 refeitas em SEMENTES NOVAS (estável 5010-5109, dano 5050-5149,
    mundo que muda 5620-5669), para testar a regra da P700 (faixas 1,72 vez mais largas que o instinto)."""
    from synthai.decisao import (QEpsilon, ThompsonBOCPD, ThompsonBernoulli, ThompsonMisturaMaximo, ThompsonMorris,
                                 ThompsonSurpresa, ThompsonSurpresaExposta)
    k = 10
    est, dano, muda = range(5010, 5110), range(5050, 5150), range(5620, 5670)
    return {
        "thompson_estavel": _estavel_701(lambda sm: ThompsonBernoulli(k, _rng(sm + 1)), est),
        "surpresa_estavel": _estavel_701(lambda sm: ThompsonSurpresa(k, _rng(sm + 1)), est),
        "exposta_dano": _dano_701(lambda sm: ThompsonSurpresaExposta(k, _rng(sm + 1)), dano),
        "bocpd_muda": _muda_701(lambda sm: ThompsonBOCPD(k, _rng(sm + 1)), muda),
        "maximo_estavel": _estavel_701(lambda sm: ThompsonMisturaMaximo(k, _rng(sm + 1)), est),
        "maximo_dano": _dano_701(lambda sm: ThompsonMisturaMaximo(k, _rng(sm + 1)), dano),
        "q_eps_estavel": _estavel_701(lambda sm: QEpsilon(k, _rng(sm + 1)), est),
        "morris_estavel": _estavel_701(lambda sm: ThompsonMorris(k, _rng(sm + 1)), est),
    }


def p702_arbitrariedade(semente=551, taxa=0.5, epocas=5):
    """A arbitrariedade do signo: a mesma tarefa da P551 (animal ou não, 4017 + 4017 substantivos), com o mesmo preditor
    logístico, a partir (1) da FORMA do primeiro lema em inglês (trigramas de letras: o significante), (2) da definição
    (o significado escrito), e (3) da forma do primeiro lema em PORTUGUÊS, nos sinsets que têm lema na OpenWordNet-PT.
    Índice de motivação = (acurácia pela forma − ½)/(acurácia pela definição − ½): 0 se o signo é arbitrário."""
    from synthai.dicionario import Dicionario, DicionarioPT, ancestrais
    from synthai.neurossimbolico import Predicado, treinar_supervisionado
    from synthai.semiotica import trigramas_de_forma
    d = Dicionario()
    pt = DicionarioPT()
    A = d.indice["n:00015388"]
    inv = {i: chave for chave, i in d.indice.items()}
    animais, outros = [], []
    for i, x in enumerate(d.sinsets):
        if x[0] != "n" or i == A:
            continue
        pos, desloc = inv[i].split(":")
        lema_pt = next((w for w in pt.lemas.get(f"{desloc}-{pos}", []) if w.isalpha()), None)
        item = (trigramas_de_forma(x[1][0].replace("_", " ")), frozenset(d.palavras_da_definicao(x[3])),
                trigramas_de_forma(lema_pt) if lema_pt else None)
        (animais if A in ancestrais(d, i) else outros).append((item, 1 if A in ancestrais(d, i) else 0))
    rng = _rng(semente)
    outros = rng.sample(outros, len(animais))
    dados = animais + outros
    rng.shuffle(dados)
    corte = len(dados) * 4 // 5
    tr, te = dados[:corte], dados[corte:]
    res = {}
    for nome, j in (("forma_en", 0), ("definicao", 1), ("forma_pt", 2)):
        trj = [(x[j], y) for x, y in tr if x[j] is not None]
        tej = [(x[j], y) for x, y in te if x[j] is not None]
        p_ = Predicado()
        treinar_supervisionado(p_, trj, taxa, epocas, _rng(semente + j))
        res[nome] = (sum((p_(x) >= 0.5) == bool(y) for x, y in tej) / len(tej), len(tej),
                     sum(y for _, y in tej) / len(tej))
    mot = lambda f: (res[f][0] - 0.5) / (res["definicao"][0] - 0.5)
    return res, mot("forma_en"), mot("forma_pt")


def p703_premissa_resposta():
    """A premissa é o significante, a resposta é o significado, nos meus documentos das Partes 31-41: para cada pergunta
    (o título "### Pnnn"), a informação condicional da resposta dada a premissa (zlib), a redundância 1 − I(r|p)/C(r), e a
    fração das palavras de conteúdo da premissa que voltam na resposta. Devolve as médias, o número de perguntas, e as
    três respostas que mais repetem a premissa."""
    import os
    from synthai.semiotica import informacao_condicional, premissas_e_respostas, retorno_da_premissa
    raiz = os.path.dirname(os.path.abspath(__file__))
    itens = []
    for n in range(31, 42):
        nome = next(f for f in sorted(os.listdir(raiz)) if f.startswith(f"ASI_AGI_parte{n}_"))
        for num, prem, resp in premissas_e_respostas(open(os.path.join(raiz, nome), encoding="utf-8").read()):
            if resp:
                c, i, red = informacao_condicional(prem, resp)
                ret = retorno_da_premissa(prem, resp)
                itens.append((num, red, ret, c))
    reds = [x[1] for x in itens]
    rets = [x[2] for x in itens if x[2] is not None]
    mais = sorted(itens, key=lambda x: -x[1])[:3]
    return sum(reds) / len(reds), sum(rets) / len(rets), len(itens), [(n, round(r, 4)) for n, r, _, _ in mais]


def p704_contas(k=10):
    """A CONTA antes da rodada 13 (o arquivo binário de pesos): 4 bytes de assinatura ('SYN1'), um inteiro de 4 bytes com k,
    e 2k números float64 (8 bytes cada, little-endian): 4 + 4 + 16k bytes."""
    return 4 + 4 + 16 * k


# --- Parte 43 (0x2B): a regra das faixas testada em mecanismos NOVOS (centro deduzido); os trigramas que carregam
#     significado; o diálogo responde às próprias perguntas? ---

# Placar acumulado ao fim da Parte 43 (atualizado quando os testes da parte terminam)
ERROS_P759, TESTES_P759 = 130, 364


def p731_contas():
    """Os CENTROS deduzidos (antes de rodar) para seis mecanismos que nunca rodaram:
    1. exposição a cada 100 (não 50), estável: 43,1 + custo da exposição T/100·E[p* − média dos outros] (P521);
    2. exposição a cada 100, dano: o braço danificado é testado depois de ~k·período/2 passos (o mais antigo dos 10 na fila):
       250 passos com período 50, 500 com 100. O custo do dano é linear no atraso, passando por (250; 19,5) e pelo sem
       exposição, cujo atraso efetivo é o resto do horizonte (1000; 42,3): custo(500) = 19,5 + (42,3 − 19,5)/750·250;
    3. surpresa com janela 40, estável: o custo da surpresa sobre o exato (43,1 − 30,7 = 12,4) cai à metade, porque as
       janelas independentes são metade e a crença renovada tem o dobro de observações: 30,7 + 6,2;
    4. surpresa com janela 40, mundo que muda: o atraso de detecção sobe de n > 3·√(0,16/20)·20/0,6 = 8,94 para
       3·√(0,16/40)·40/0,6 = 12,65 puxadas (×1,415). Com uma base de 8 fases × 20 (Thompson em 500 passos), a parte da
       detecção, 367,7 − 160, sobe 1,415 vez: 160 + 207,7·1,415;
    5. BOCPD com H = 1/2000 no mundo que muda (o verdadeiro é 1/500): a evidência para a mudança precisa vencer ln(1/H):
       ln 2000/ln 500 = 1,223 vez mais; 160 + (371,9 − 160)·1,223;
    6. Thompson com a priori de Jeffreys, estável: a priori quase não pesa depois de dezenas de puxadas: o mesmo ~30,7,
       com +1% pelo começo mais disperso: 31,0."""
    expo = p521_contas(periodo=100)[1]
    dano = 19.5 + (42.3 - 19.5) / 750 * 250
    d20 = 3 * sqrt(0.16 / 20) * 20 / 0.6
    d40 = 3 * sqrt(0.16 / 40) * 40 / 0.6
    return {"exposta100_estavel": expo, "exposta100_dano": dano, "surpresa40_estavel": 30.7 + 12.4 / 2,
            "surpresa40_muda": 160 + 207.7 * d40 / d20, "bocpd2000_muda": 160 + (371.9 - 160) * log(2000) / log(500),
            "jeffreys_estavel": 31.0}


def p731_mecanismos_novos(k=10):
    """Os seis mecanismos novos, nas sementes de sempre (estável 4010-4109, dano 4050-4149, muda 4620-4669)."""
    from synthai.decisao import ThompsonBOCPD, ThompsonJeffreys, ThompsonSurpresa, ThompsonSurpresaExposta
    est, dano, muda = range(4010, 4110), range(4050, 4150), range(4620, 4670)
    return {
        "exposta100_estavel": _estavel_701(lambda sm: ThompsonSurpresaExposta(k, _rng(sm + 1), periodo=100), est),
        "exposta100_dano": _dano_701(lambda sm: ThompsonSurpresaExposta(k, _rng(sm + 1), periodo=100), dano),
        "surpresa40_estavel": _estavel_701(lambda sm: ThompsonSurpresa(k, _rng(sm + 1), janela=40), est),
        "surpresa40_muda": _muda_701(lambda sm: ThompsonSurpresa(k, _rng(sm + 1), janela=40), muda),
        "bocpd2000_muda": _muda_701(lambda sm: ThompsonBOCPD(k, _rng(sm + 1), risco=1 / 2000), muda),
        "jeffreys_estavel": _estavel_701(lambda sm: ThompsonJeffreys(k, _rng(sm + 1)), est),
    }


def _formas_732():
    """(lema em inglês, 1 se animal) para os 4017 animais e outros 4017 substantivos (a mesma amostra da P551/P702)."""
    from synthai.dicionario import Dicionario, ancestrais
    d = Dicionario()
    A = d.indice["n:00015388"]
    animais, outros = [], []
    for i, x in enumerate(d.sinsets):
        if x[0] != "n" or i == A:
            continue
        (animais if A in ancestrais(d, i) else outros).append((x[1][0].replace("_", " ").lower(), 1 if A in ancestrais(d, i) else 0))
    rng = _rng(551)
    outros = rng.sample(outros, len(animais))
    return animais + outros


def p732_trigramas(minimo=10, topo=12):
    """Os trigramas de forma que mais carregam significado (animal ou não): o log da razão de chances com suavização
    de Laplace, log((c_animal + 1)/(N_animal + V)) − log((c_outro + 1)/(N_outro + V)), entre os trigramas que aparecem ≥
    `minimo` vezes. Devolve os `topo` mais "animais", os mais "não animais", e os pesos de 'dae' e 'ae$'."""
    from synthai.semiotica import trigramas_de_forma
    dados = _formas_732()
    ca, co = {}, {}
    for lema, y in dados:
        for t in trigramas_de_forma(lema):
            (ca if y else co)[t] = (ca if y else co).get(t, 0) + 1
    voc = set(ca) | set(co)
    na, no = sum(ca.values()), sum(co.values())
    v = len(voc)
    peso = {t: log((ca.get(t, 0) + 1) / (na + v)) - log((co.get(t, 0) + 1) / (no + v)) for t in voc}
    ok = [t for t in voc if ca.get(t, 0) + co.get(t, 0) >= minimo]
    ok.sort(key=lambda t: (-peso[t], t))
    return ok[:topo], ok[::-1][:topo], peso.get("dae"), peso.get("ae$"), len(voc)


def p733_dialogo_responde():
    """A premissa é o significante, a resposta é o significado, no diálogo: a pergunta deixada no fim de cada rodada
    (a premissa) e o texto da rodada seguinte (a resposta). Para cada par: a fração das palavras de conteúdo da pergunta
    que voltam na rodada seguinte, e a redundância por compressão. Devolve as médias e o número de pares."""
    import os
    import re
    from synthai.semiotica import informacao_condicional, retorno_da_premissa
    raiz = os.path.dirname(os.path.abspath(__file__))
    texto = open(os.path.join(raiz, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    rodadas = re.split(r"\n## Rodada ", texto)
    pares = []
    for r_atual, r_seguinte in zip(rodadas, rodadas[1:]):
        m = re.search(r"\(a pergunta para a Rodada \d+\):\*\*\s*(.*?)(?:\n\n|$)", r_atual, re.S)
        if not m:
            m = re.search(r"\(pergunta para a Rodada \d+\)\):?\*\*:?\s*(.*?)(?:\n\n|$)", r_atual, re.S)
        if m:
            q = m.group(1)
            pares.append((retorno_da_premissa(q, r_seguinte), informacao_condicional(q, r_seguinte)[2]))
    rets = [p_ for p_, _ in pares if p_ is not None]
    return sum(rets) / len(rets), sum(r for _, r in pares) / len(pares), len(pares)


# --- Parte 44 (0x2C): o modelo no nível certo (uma mudança global); os grupos do dicionário; a minha curva de erro ---

# Placar acumulado ao fim da Parte 44 (atualizado quando os testes da parte terminam)
ERROS_P789, TESTES_P789 = 133, 371


def p761_contas():
    """Os CENTROS deduzidos (antes de rodar) para o ThompsonBOCPDGlobal (H = 1/500):
    1. mundo que muda (as mudanças são globais): a base de 8 fases × 20 = 160 (Thompson em 500 passos) mais a parte da
       detecção. A surpresa detecta em ~9 puxadas mas renova só o braço puxado (parte da detecção: 367,7 − 160 = 207,7);
       o modelo global detecta no mesmo tempo e renova os dez braços de uma vez: metade da parte da detecção: 160 + 103,9;
    2. mundo estável: uma hipótese nova (tudo em Beta(1, 1)) prevê ½ onde a velha prevê p* ≈ 0,9; a cada puxada do melhor
       braço o peso dela cai pelo fator 0,5/0,9 e ela quase nunca é sorteada: o exato mais um custo pequeno, 30,7 + 3;
    3. dano: o lixo vira uma hipótese só; os braços que o lixo faz parecerem bons são puxados e desmentem a hipótese, e a
       hipótese nova (que renova TODOS os braços, inclusive o melhor, nunca puxado) ganha peso: o custo cai ao nível da
       exposição (P521, 19,5)."""
    return {"global_muda": 160 + 207.7 / 2, "global_estavel": 30.7 + 3.0, "global_dano": 19.5}


def p761_global(k=10):
    """O ThompsonBOCPDGlobal nos três mundos, nas sementes de sempre."""
    from synthai.decisao import ThompsonBOCPDGlobal
    fab = lambda sm: ThompsonBOCPDGlobal(k, _rng(sm + 1))
    return {"global_muda": _muda_701(fab, range(4620, 4670)), "global_estavel": _estavel_701(fab, range(4010, 4110)),
            "global_dano": _dano_701(fab, range(4050, 4150))}


def p762_curva_de_erro():
    """A minha curva de erro, parte a parte (31 a 43), a partir dos placares: a taxa de cada parte e a inclinação dos
    mínimos quadrados da taxa contra o número da parte (descritivo: os números já são conhecidos)."""
    taxas = {}
    for parte, (e, n) in p671_erros_por_tipo()[1].items():
        taxas[parte] = e / n
    taxas.update({41: 2 / 9, 42: 4 / 15, 43: 2 / 11})
    xs = sorted(taxas)
    ys = [taxas[x] for x in xs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    incl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return {x: round(taxas[x], 3) for x in xs}, incl


def p763_grupos():
    """A trilha do dicionário no nível certo: quantos substantivos do WordNet nomeiam GRUPOS (descendem de group.n.01,
    00031264) e quantos nomeiam grupos taxonômicos (descendem de taxon, 07992450); e, entre os 4017+4017 da P551, quantos
    dos não animais que o preditor de forma (P702) chamaria de animal são grupos."""
    from synthai.dicionario import Dicionario, ancestrais
    d = Dicionario()
    G, T = d.indice["n:00031264"], d.indice["n:07992450"]
    n = g = t = 0
    for i, x in enumerate(d.sinsets):
        if x[0] != "n":
            continue
        n += 1
        an = ancestrais(d, i)
        g += G in an
        t += T in an
    return n, g / n, t / n


# --- Parte 45 (0x2D): decidir pela hipótese mais pesada no nível do mundo; a calibração das minhas faixas; a
#     profundidade da taxonomia ---

# Placar acumulado ao fim da Parte 45 (atualizado quando os testes da parte terminam)
ERROS_P819, TESTES_P819 = 134, 379

# As 17 previsões de comportamento feitas com a regra das faixas (Partes 42-44): (centro, meia-largura relativa, medido).
# Os medidos são os de resultados.txt / dos documentos das partes (P701, P731, P761).
FAIXAS_42_44 = [
    (30.7, 0.172, 31.634), (43.1, 0.172, 43.531), (19.5, 0.344, 24.926), (371.9, 0.172, 384.574), (34.5, 0.172, 36.292),
    (60.9, 0.344, 64.564), (185.4, 0.172, 183.990), (76.9, 0.172, 80.870),
    (52.109, 0.172, 53.027), (27.1, 0.344, 26.671), (36.9, 0.172, 34.837), (453.73, 0.258, 412.644),
    (419.17, 0.258, 340.685), (31.0, 0.172, 33.813),
    (263.85, 0.258, 231.471), (33.7, 0.172, 44.687), (19.5, 0.344, 28.663),
]


def p791_contas():
    """Os CENTROS deduzidos (antes de rodar) para o ThompsonBOCPDGlobalMAP (H = 1/500):
    1. estável: a hipótese velha é sempre a mais pesada; é o Thompson exato com um começo um pouco mais lento: 30,7 + 1;
    2. mundo que muda: a hipótese nascida na troca passa a velha quando a evidência vence ln(1/H) = ln 500 = 6,2 nats; depois
       da troca, cada fracasso do braço que era bom (a velha prevê ~0,1 de fracasso, a nova ½) dá ln 5 = 1,6 nat: ~4
       fracassos, ~6 puxadas, menos que as ~9 da surpresa. Sem as jovens sorteadas no meio das fases, o global sorteado
       (231,5) perde o excesso do estável: (44,7 − 30,7) por 2000 passos, 28 em 4000: 231,5 − 28;
    3. dano: os braços que o lixo faz parecerem bons são puxados e desmentem a hipótese do lixo em poucos passos (o mesmo
       ln(1/H)/1,6 ≈ 4 fracassos), e a hipótese nova renova todos os braços: um custo menor que o da exposição, ~12."""
    return {"map_estavel": 30.7 + 1.0, "map_muda": 231.47 - 2 * (44.69 - 30.71), "map_dano": 12.0}


def p791_map(k=10):
    """O ThompsonBOCPDGlobalMAP nos três mundos, nas sementes de sempre."""
    from synthai.decisao import ThompsonBOCPDGlobalMAP
    fab = lambda sm: ThompsonBOCPDGlobalMAP(k, _rng(sm + 1))
    return {"map_estavel": _estavel_701(fab, range(4010, 4110)), "map_muda": _muda_701(fab, range(4620, 4670)),
            "map_dano": _dano_701(fab, range(4050, 4150))}


def p792_calibracao():
    """A calibração das minhas faixas de comportamento (descritivo: os 17 medidos já são conhecidos). Se a faixa
    centro·(1 ± w) é de 90%, a meia-largura é 1,645σ e z = (medido − centro)/(centro·w/1,645) é ~N(0, 1). A média de z mede
    o viés do centro; o desvio de z, a escala (> 1: faixas estreitas; < 1: largas); e a fração com |z| > 1,645, a cobertura."""
    zs = [(m - c) / (c * w / 1.645) for c, w, m in FAIXAS_42_44]
    n = len(zs)
    media = sum(zs) / n
    dp = sqrt(sum((z - media) ** 2 for z in zs) / (n - 1))
    fora = sum(1 for z in zs if abs(z) > 1.645)
    return media, dp, media / (dp / sqrt(n)), fora, n


def p793_profundidade():
    """A trilha do dicionário: a profundidade média (hiperônimos até a raiz) dos substantivos que são animais, artefatos
    (artifact, 00021939) e grupos taxonômicos (taxon, 07992450), e a dos substantivos em geral."""
    from synthai.dicionario import Dicionario, ancestrais, profundidades
    d = Dicionario()
    prof = profundidades(d)
    alvos = {"animal": d.indice["n:00015388"], "artefato": d.indice["n:00021939"], "taxon": d.indice["n:07992450"]}
    soma = {k: [0, 0] for k in list(alvos) + ["todos"]}
    for i, x in enumerate(d.sinsets):
        if x[0] != "n" or i not in prof:
            continue
        an = ancestrais(d, i)
        soma["todos"][0] += prof[i]
        soma["todos"][1] += 1
        for k, j in alvos.items():
            if j in an and j != i:
                soma[k][0] += prof[i]
                soma[k][1] += 1
    return {k: (s_ / n, n) for k, (s_, n) in soma.items()}


# --- Parte 46 (0x2E): a resposta é a pergunta e a pergunta é a resposta; refazer tudo desde o começo ---

# Placar acumulado ao fim da Parte 46 (atualizado quando os testes da parte terminam)
ERROS_P849, TESTES_P849 = 138, 390


def p821_inversao(partes=range(31, 46)):
    """As perguntas e respostas dos meus documentos, nos dois sentidos. Para cada pergunta p e a sua resposta r (zlib):
    redundância da resposta dada a pergunta, 1 − I(r|p)/C(r) (o sentido da P703), e redundância da pergunta dada a
    resposta, 1 − I(p|r)/C(p), com I(p|r) = C(r + p) − C(r): quanto da pergunta a resposta já contém."""
    import os
    from synthai.semiotica import comprimido, informacao_condicional, premissas_e_respostas
    raiz = os.path.dirname(os.path.abspath(__file__))
    rr, rp = [], []
    for n in partes:
        nome = next(f for f in sorted(os.listdir(raiz)) if f.startswith(f"ASI_AGI_parte{n}_"))
        for _, p_, r_ in premissas_e_respostas(open(os.path.join(raiz, nome), encoding="utf-8").read()):
            if r_:
                rr.append(informacao_condicional(p_, r_)[2])
                cp = comprimido(p_)
                rp.append(1 - (comprimido(r_ + "\n" + p_) - comprimido(r_)) / cp)
    return sum(rr) / len(rr), sum(rp) / len(rp), len(rr)


def p822_dialogo_invertido():
    """A pergunta é a resposta, no diálogo: a pergunta deixada no fim de cada rodada, comparada com a própria rodada que a
    gerou (o texto antes dela) e com a rodada seguinte (que a responde). Redundância da pergunta dada cada texto,
    1 − I(q|t)/C(q). Se a pergunta nasce da resposta que a precede, ela está mais contida na própria rodada."""
    import os
    import re
    from synthai.semiotica import comprimido
    raiz = os.path.dirname(os.path.abspath(__file__))
    texto = open(os.path.join(raiz, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    rodadas = re.split(r"\n## Rodada ", texto)
    propria, seguinte = [], []
    for atual, prox in zip(rodadas, rodadas[1:]):
        m = re.search(r"\*\*IA-[A-Za-z]+ \((?:a )?pergunta para a Rodada \d+\)\)?:?\*\*:?\s*(.*?)(?:\n\n|$)", atual, re.S)
        if not m:
            continue
        q = m.group(1)
        antes = atual[: m.start()]
        red = lambda t: 1 - (comprimido(t + "\n" + q) - comprimido(t)) / comprimido(q)
        propria.append(red(antes))
        seguinte.append(red(prox))
    return sum(propria) / len(propria), sum(seguinte) / len(seguinte), len(propria)


def p823_reproducao(velho, novo):
    """Refazer tudo desde o começo: compara, linha a linha, a saída antiga (o resultados.txt commitado) com a de uma
    execução nova de todas as partes, até o começo da unificação da antiga. Devolve (linhas comparadas, iguais, as linhas
    diferentes com o prefixo de cada uma)."""
    a = open(velho, encoding="utf-8").read().split("\n")
    b = open(novo, encoding="utf-8").read().split("\n")
    fim = next(i for i, x in enumerate(a) if x.startswith("=== Unificacao"))
    difs = [(i, a[i][:40], b[i][:40] if i < len(b) else None) for i in range(fim) if i >= len(b) or a[i] != b[i]]
    return fim, fim - len(difs), difs


def p824_reconstrucao():
    """A pergunta a partir da resposta (Rodada 18): cada seção de números do resultados.txt, sem os rótulos, escolhe o
    documento de parte com a maior soma de ln(K/df) sobre os números em comum (dialogo/rodada18.py, conferido em Java).
    Devolve (acertos, partes, as erradas como (parte, escolhida))."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada18", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada18.py"))
    r18 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r18)
    res = r18.reconstruir(r18.documentos())
    return sum(n == k for n, k, _, _ in res), len(res), [(n, k) for n, k, _, _ in res if n != k]


def p825_cauda_binomial(n, p, k):
    """P(X >= k) para X ~ Binomial(n, p): a chance de acertar k ou mais ao acaso."""
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


ERROS_P879, TESTES_P879 = 141, 399


def p851_genero_e_diferenca(d=None):
    """A definição contém a pergunta? (P851, gênero e diferença). Para cada substantivo do WordNet com hiperônimo direto:
    direto = a definição contém, como palavra inteira, um lema do hiperônimo (ou + s/es); inverso, por par
    hipônimo-hiperônimo = a definição do hiperônimo contém um lema do hipônimo. Devolve (fração direta, fração inversa,
    pares, sinsets)."""
    import re
    from synthai.dicionario import Dicionario
    d = d or Dicionario()

    def contem(definicao, lemas):
        for x in lemas:
            x = re.escape(x.replace("_", " ").lower())
            if re.search(r"(?<![a-z])" + x + r"(?:e?s)?(?![a-z])", definicao):
                return True
        return False

    direto = inverso = pares = n = 0
    for pos, lemas, hiper, glosa in d.sinsets:
        if pos != "n":
            continue
        hs = [d.indice[h] for h in hiper if h in d.indice]
        if not hs:
            continue
        n += 1
        definicao = d.definicao(glosa).lower()
        direto += any(contem(definicao, d.sinsets[k][1]) for k in hs)
        for k in hs:
            pares += 1
            inverso += contem(d.definicao(d.sinsets[k][3]).lower(), lemas)
    return direto / n, inverso / pares, pares, n


def p852_cadeia_hexadecimal(ate=850):
    """f(n) = o hexadecimal de n lido como decimal, enquanto não houver letra. Devolve (quantos de 1 a `ate` não têm
    letra no hexadecimal, a média de aplicações de f para n de 10 a `ate`, a conta da P852 com independência)."""
    sem_letra = sum(1 for n in range(1, ate + 1) if format(n, "x").isdigit())
    passos = []
    for n in range(10, ate + 1):
        k = 0
        while format(n, "x").isdigit():
            n = int(format(n, "x"))
            k += 1
        passos.append(k)
    p1 = (sem_letra - 9) / (ate - 9)
    p2, p3 = 9 / 15 * (10 / 16) ** 3, 9 / 15 * (10 / 16) ** 4
    return sem_letra, sum(passos) / len(passos), p1 + p1 * p2 + p1 * p2 * p3


def p853_reconstrucao(rodada="rodada19"):
    """Rodada 19 (P853): a mesma reconstrução da P824, pelas palavras (rodada19) ou pelos números (rodada18). Devolve
    (acertos, partes, erradas, a mediana da razão entre o escore da própria parte e o do melhor outro documento)."""
    import importlib.util
    import os
    import statistics
    raiz = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(rodada, os.path.join(raiz, "dialogo", rodada + ".py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    docs, sec = r.documentos(), r.secoes()
    partes = sorted(k for k in docs if k in sec)
    dn = {k: r.numeros(open(os.path.join(raiz, docs[k]), encoding="utf-8").read()) for k in partes}
    df = {}
    for k in partes:
        for t in dn[k]:
            df[t] = df.get(t, 0) + 1
    razoes, erradas = [], []
    for n in partes:
        rr = r.numeros(sec[n])
        esc = {k: sum(log(len(partes) / df[t]) for t in sorted(rr & dn[k])) for k in partes}
        outro = max(v for k, v in esc.items() if k != n)
        razoes.append(esc[n] / outro)
        if esc[n] <= outro:
            erradas.append(n)
    return len(partes) - len(erradas), len(partes), erradas, statistics.median(razoes)

# P213: o agente se chamava GISELE até a Parte 14 e passou a se chamar SYNTHAI na Parte 15.
# O código antigo nunca é apagado: os nomes antigos continuam valendo como apelidos dos novos.
for _nome in [n for n in list(globals()) if n.startswith("Synthai") or n.startswith("_synthai") or "synthai" in n]:
    globals()[_nome.replace("Synthai", "Gisele").replace("synthai", "gisele")] = globals()[_nome]
del _nome


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
        "P160": round(p160_complementaridade()[1]) == 112,
        "P161": round(p161_quatro_funcoes()[0], 3) == 1.561,
        "P163": [round(r, 2) for r in p163_minha_decolagem([0.764, 0.157, -0.113])] == [0.21, -0.72],
        "P169": p169_peso_da_familia()[0] == 6896,
        "P170": p170_lista_de_capacidades()[:2] == (3, 12),
        "P171": round(p171_lacuna_de_compute()[1], 1) == 14.7,
        "P172": round(p172_minha_precisao()[2], 2) == 0.99,
        "P181": round(p181_valor_da_previsao()[2], 3) == 2.236,
        "P183": round(p183_limiar_por_passo()[0], 5) == 0.00397,
        "P200": p200_retrospectiva()[:2] == (52, 29),
        "P206": p206_identidade(),
        "P215": round(p215_distinguivel()["conhecida"], 2) == 0.91,
        "P223": round(p223_sinal_combinado()[2], 3) == 0.835,
        "P234": round(p223_sinal_combinado(d_sensor=2.0)[2], 3) == 0.941,
        "P242": [round(x, 3) for x in p242_bits_do_veto()[:2]] == [0.211, 0.106],
        "P252": round(p252_bits_da_palavra_precisa()[1], 3) == 0.192,
        "P255": round(p255_quaternidade()[1], 3) == 1.950,
        "P268": round(p268_efeito_combinado()[0], 3) == 0.552,
        "P272": [p272_encolhimento()[x][0] for x in (0.5, 2.0)] == [0.8, 0.2],
        "P285": p285_acoplamento()[0:4:3] == (6, 0) and len(p285_acoplamento()[1]) == 5,
        "P286": p286_testes_de_unidade() == (10, 0),
        "P287": round(p287_veto_falso()[1], 2) == 0.46,
        "P291": p291_menon()[0] == 10,
        "P292": [round(x, 3) for x in p292_ponto_neutro()[:3]] == [1.003, 0.614, 0.996],
        "P297": [round(x, 3) for x in p297_p42_exato()] == [0.547, 0.144],
        "P304d": [round(x, 4) for x in p304d_vies_de_primeira_ordem()] == [-0.0296, -0.0286],
        "P306": [f"{x:.1e}" for x in p306_newton_quadratico()[8:10]] == ["9.3e-03", "2.6e-05"],
        "P307": [round(x, 2) for x in p307_selecao()[0]["caso_controle"][:2]] == [-0.02, 1.48],
        "P314": round(p314_custo_do_descarte()[1], 3) == 0.364,
        "P325": [round(x, 4) for x in p325_chance()[0][1:2] + p325_chance()[1][1:2]] == [0.0041, 0.0207],
        "P332": [round(x, 3) for x in p332_estimadores_proprios()[:4]] == [67.273, 3.86, 0.662, 0.96],
        "P342": [round(p342_conta_da_ancora()[v][0], 2) for v in ("media", "quantil", "auditoria_quantil")] == [3.86, 4.98, 5.44],
        "P352": [round(l[3], 5) for l in p352_bateria_wilson_hilferty()[1::8]] == [-0.00634, -0.00034]
                and [round(l[5], 4) for l in p352_bateria_delta_inverso()[3:5]] == [-0.0069, -0.0105],
        "P355": p352_bateria_contas()[:2] == (4, 10),
        "P361": p361_hex_do_limiar()[0] == "0x1.23456789abcdfp-9" and p361_hex_do_limiar()[3].startswith("0123456789ABCDF0"),
        "P365": p365_impressoes_digitais()[1] == "38be1420a8d3622771d385187c1f388123df8fd44c69fb1a7a11e6c76b59ac11",
        "P372": p372_hex_do_dicionario()[:4:2] == (83, "fabaceae"),
        "P382": p382_minset_reduzido()[:2] == (3985, 3171),
        "P393": p393_ulps(ns=(10,), tentativas=1)[1:] == ("0x1.3333333333334p-2", "0x1.3333333333333p-2"),
        "P394": round(p394_ulps_em_degrau(ns=(2000,), tentativas=1)[2000][1], 2) == 7.72,
        "P401": tuple(round(x, 1) for x in p401_contas()[:2]) == (62.4, 80.7),
        "P402": round(p402_contas()[0], 4) == 0.2572,
        "P403": p403_continuo(d=8, sementes=(4030, 4031))[2] < 1e-8,
        "P431": round(p431_landauer()[0][293.15] * 1e21, 4) == 2.8054,
        "P432": round(p432_bremermann()[2], 12) == 4.0,
        "P435": p435_auditoria()["nos_mudados"] == 0 and p435_auditoria()["run_benchmarks_constante"] == 0.85,
        "P436": round(p436_contas(), 4) == 0.951,
        "P462": round(p462_contas()[1], 4) == 0.9895,
        "P523": round(p523_contas()[1], 4) == 0.0157,
        "P531": round(p531_contas()[0], 1) == 62.7,
        "P542": round(p542_contas()[2]) == 4971,
        "P551": round(p551_contas()[2], 3) == 0.944,
        "P644": round(p644_contas()["pt"], 4) == 1.0296,
        "P671": sum(n for _, n in p671_erros_por_tipo()[1].values()) == 128,
        "P704": p704_contas() == 168,
        "P731": round(p731_contas()["exposta100_dano"], 1) == 27.1,
        "P761": round(p761_contas()["global_muda"], 2) == 263.85,
        "P792": round(p792_calibracao()[1], 2) == 1.07,
        "P821": round(p821_inversao(range(31, 46))[1], 3) == 0.579,
        "P851": round(p851_genero_e_diferenca()[0], 3) == 0.602,
        "P852": p852_cadeia_hexadecimal()[0] == 352 and round(p852_cadeia_hexadecimal(4095)[1], 3) == 0.432,
        "P882": p882_mapa_da_definicao()[2] == 23 and round(p882_mapa_da_definicao()[5], 4) == 0.6986,
        "P883": round(p883_felizes_hex()[0], 4) == 0.2613,
        "P912": p912_funis()[:2] == ("act", 1991) and round(p912_funis()[3], 3) == -1.869,
        "P943": round(p943_periodo_hex()[0], 4) == 0.2793,
        "P947": p947_o_texto_voltou()[0] and p947_o_texto_voltou()[1]["nos_mudados"] == 0,
        "P973": len(p973_kaprekar_hex()[0]) == 4 and p973_kaprekar_hex(4, 10)[0] == [(6174,)],
        "P1003": round(p1003_inverte_e_soma()[0], 4) == 0.9819 and len(p1003_inverte_e_soma(9999, 10)[2]) == 246,
        "P1034": p1034_pi_hexadecimal(200)[:3] == (200, 200, "243F6A88"),
        "P1063": p1063_autodescritivos(16) == ["C210000000001000"] and p1063_autodescritivos(10) == ["6210001000"],
        "P1094": round(p1094_ulp_em_hexadecimal()[0], 4) == 1.0341 and round(p1094_ulp_mantissa_uniforme()[0], 4) == 1.0667,
        "P1123": p1123_mesma_soma()[1] == 431 and p1123_mesma_soma(65535)[1] == 5161,
        "P1153": p1153_duplos_palindromos()[0] == 27,
        "P1183": p1183_primeiro_digito_hex(2) == [0, 2500, 2500, 0, 2500, 0, 0, 0, 2500] + [0] * 7 and p1183_primeiro_digito_hex(3)[1] == 2506,
        "P1213": p1213_persistencia_hex(16 ** 4)[:2] == (7, 0x3DDE),
        "P1243": len(p1243_narcisistas_hex(8)) == 64 and p1249_fator_de_congruencia(9) == 15,
        "P1273": p1273_niven(16 ** 5)[0] == 93788 and p1278_familias_narcisistas()[:2] == (175, 157),
        "P1303": p1303_autonumeros()[1] == 64999 and p1307_terminacoes_iguais()[1][0] == ("al", 434),
        "P1333": p1333_primos_palindromos()[0] == 357 and p1331_fator_efetivo()[1:] == (84, 42),
        "P1363": p1363_quadrados_palindromos()[0] == 24 and p1361_fator_do_final()[7][1] == 196,
        "P1393": p1393_periodo_hex()[3] == 8363 and p1391_o_que_nao_e_divisor()[0][1] == 48,
        "P1423": p1427_bases_29_a_34((29,))[0][1] == 1610 and p1421_endereco_da_falta()[0]["d0"][1] == 11,
        "P1455": len(p1455_automorficos(12, 6)[0]) == 11 and len(p1452_minhas_previsoes(range(53, 67))) == 97,
        "P1493": len(p1493_palindromos_duplos()[0]) == 18 and p1491_densidade_da_conta()[0][5][1] == 9592,
        "P1516": p1514_pi_hex_digitos(16) == "243f6a8885a308d3" and p1516_gpt_decide()[1] == 5,
        "P1549": abs(p1549_lei_de_escala()[0][24][1] - 0.0541) < 0.0001 and abs(p1545_bases_gf2(p1514_pi_hex_digitos(10000))[0] - 0.30269) < 0.00001,
        "P1574": p1574_irredutiveis_gf2(15, 6)[:3] == (2182, 2182, 224) and p1573_crescimento_da_taxonomia("n")[2] == 7,
        "P1612": p1612_animais_por_horn()[:4] == (4017, True, True, 4) and p1608_auditoria_estatica()[1] == ("test_engine", 7, 5, 8),
        "P1639": p1639_rodada47()[1:2] + p1639_rodada47()[4:5] == (958, 102) and abs(p1632_prioridade_contra_voi(20000, 74)[0] - 0.49995) < 1e-9,
        "P1663": p1663_rodada48()[3] == 172 and p1662_orcamento(semente=75)[2] == 0.62,
        # P1692 conta as funções do próprio calculos.py, que cresce (a regra da Parte 48): a entrada confere o invariante (aprova todas, inclusive as que a mutação muda), não o 584 da Parte 75
        "P1692": (lambda r: r[1] == r[0] and r[3] == r[2] > 0)(p1692_godel_nas_funcoes()) and p1691_laco_de_auto_modificacao(geracoes=2, separador_corrigido=True)[0][1:3] == (True, 2.8333333333333335),
        "P1843": [round(x, 4) for x in p1843_rodada49()] == [0.8821, 0.9771, 0.7933, 0.91, 0.11],
        "P1811": [round(x, 4) for x in p1811_confusao()] == [0.9986, 0.4987, 0.4914],
        "P1931": (lambda m: [round(m[0]["sincrono"][0], 5), round(m[0]["alternado"][1], 6), m[0]["alternado"][2]])(p1931_gan_de_dirac()) == [0.34864, 0.101274, 16],
        "P1933": [round(x, 4) for x in p1933_calibracao_composta()[:2]] == [0.1516, 0.1511],
        "P1961": p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84))[:2] == (23, 31) and p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85))[:2] == (27, 35),
        "P1962": round(p1962_lyapunov_por_densidade(a=0.2, celulas=800, iteracoes=1500)[1], 3) == 0.997,
        "P1964": p1964_rodada51()[0] == 263,
        "P1991": p1991_cosseno_duplicado_recebido() == [1.3, 0.5, -0.3, -0.5, -0.7],
        "P1993": len(p1993_buraco_do_escrutinio()) == 3,
        "P1995": p1995_rodada52()[:2] == (15, 0.0),
        "P2022": p2022_izhikevich_tipos() == (22, 73),
        "P2024": p2024_gsops() == (10000, 10000000, 10.0),
        "P2027": p2027_rodada53()[2] == 5,
        "P2051": round(p2051_quantizacao_mse()[2]) == 279,
        "P2052": p2052_vantagem_grpo() == ([1.0, -1.0], 0.0),
        "P2055": len(p2055_rodada54()) == 18 and round(p2055_rodada54()[0], 6) == 1.0,
        "P2081": p2081_probabilidade_aninhada() == (0.8333, 0.1667, 0.5),
        "P2083": p2083_lfi1_sem_explosao() == (0.5, 0.0, True),
        "P2085": p2085_rodada55()[1] == 1.2,
        "P2111": p2111_stdp_integral() == (0.0, -0.3999999999999999),
        "P2113": (lambda t: t[0] > 0.5 > t[1])(p2113_stdp_timing()),
        "P2115": p2115_rodada56() == 12,
        "P2141": (lambda r: r[0] == 12 and r[1] < r[2])(p2141_rede_stdp()),
        "P2143": p2143_disparos_aprendiz_vs_fixo() == (12, 12, True),
        "P2172": p2172_sgd_reduz_perda() == [True] * 5,
        "P2174": (lambda r: r[1] < 0.1 < r[0])(p2174_gpt_memoriza()),
        "P2201": p2201_fronteira_pow() == 418,
        "P2204": p2204_adam_reduz_perda() == [True] * 5,
        "P1751": p1751_rodada09_nova_contra_antiga()[:2] == (13, 6),
        "P1722": sorted(p1722_libm_nas_duas_linguagens()) == ["48"],  # era ["09", "14", "48"] na Parte 76; a Parte 77 corrigiu a 09 e a 14
        "P1604": abs(p1604_hash_como_peso()[2] + 0.2613) < 0.001 and p1603_ciclos_de_glosas()[0][2:] == (True, False),
        "P1579": p1574_irredutiveis_gf2(17, 6)[2] == 758 and abs(p1579_serie_singular_gf2(17)[1] - 755.458) < 0.001,
        "P2927": p2927_auditoria_de_entrada() == (7, 3, 0),
        "P2929": [st for st, _ in p2929_rodada83()] == ["confirmed", "inconclusive", "rejected"],
        "P2951": max(p2951_ortogonal_escalada()) < 1e-12,
        "P2956": p2956_rodada84() < 1e-12,
        "P2983": p2983_rodada85()[1] == 0,
        "P3013": p3013_rodada86()[1] == 0,
        "P3073": p3073_jogos_e_dinamica()[:3] == (5478, 5478, 0),
        "P3043": p3043_rodada88() == (288, 0),
        "P3103": p3103_rodada89()[0] < 1e-15,
        "P3110": p3110_rodada90()[1] == 0,
        "P123inv": all(invariantes_p123().values()),
        "P3152": (lambda m: len(m["repetidos"]) == 8 and m["repetidos"][0] == ("consciência da consciência", 11))(
            p3152_medir_lote(p3151_lote_de_textos("textos_parte126/lote1.txt"))),
        "P3162": p3162_ignicao_rampa(0.002) == (0.29634000000000005, -0.29634000000000005)
            and abs(p3161_ignicao_dobras()[0] - 0.26641998767677605) < 1e-12,
        "P3172": (lambda r: r["categorias"] == {"projeto": 73, "maquina": 2, "nota": 10, "mundo": 0} and r["sem_referencia"] == [91])(
            p3172_comparar_reproducao("reproducao/resultados_antes_volta1.txt", "reproducao/volta1")),
        "P3174": (lambda r: (r["diferentes"], r["categorias"]["mundo"], r["novas"]) == (9, 0, [128]))(
            p3174_comparar_voltas("reproducao/volta1", "reproducao/volta2")),
        "P3174v3": (lambda r: (r["diferentes"], r["categorias"]["mundo"], r["novas"]) == (8, 0, [129]))(
            p3174_comparar_voltas("reproducao/volta2", "reproducao/volta3")),
        "P3174v4": (lambda r: (r["diferentes"], r["categorias"]["mundo"], r["novas"], r["blocos_sem_excecao"]) == (9, 0, [130], 127))(
            p3174_comparar_voltas("reproducao/volta3", "reproducao/volta4")),
        "P3174v5": (lambda r: (r["diferentes"], r["categorias"]["mundo"], r["novas"], r["blocos_sem_excecao"]) == (8, 0, [131], 128))(
            p3174_comparar_voltas("reproducao/volta4", "reproducao/volta5")),
        "P3176": (lambda r: (r["diferentes"], r["categorias"]["mundo"], len(r["reclassificadas"]), r["blocos_sem_excecao"]) == (9, 0, 1, 129))(
            p3176_comparar_voltas_v2("reproducao/volta5", "reproducao/volta6")),
        "P3177": (lambda r: abs(r["fechada"] + 4.7891) < 1e-3 and r["erro_rel"] < 1e-10 and r["secante"] < -11.0)(
            p3177_passo_fixo_e_secante()),
        "P3179": (lambda r: (r[0], r[2], r[3], r[4]) == ({}, 6, 0, 1))(p3179_capacidades_recebidas()),
        "P3180": all(e < 1e-9 and ok for e, _, ok in p3180_media_por_modo()),
        "P3181": (lambda r: r[0] < 2e-7 and round(r[1][2][0], 4) == 0.5578)(p3181_vantagem_e_contraste()),
        "P3182": (lambda r: (round(r[0][2][0], 4), round(r[0][8][0], 4)) == (0.9086, 0.8987))(p3182_grpo_g2_g8()),
        "P3183": (lambda r: round(r[0], 3) == 32.036 and r[2] < 1e-9)(p3183_reservatorio_e_posto()),
        "P3184": (lambda r: r[0] == r[1] == 10000)(p3184_contexto_e_curvatura()),
        "P3185": (lambda r: (r[0.05][2], r[0.2][2]) == (27, 19))(p3185_memoria_congelada()),
        "P3186": (lambda r: (round(r[4][0], 4), round(r[16][0], 4)) == (0.9058, 0.8825))(p3186_grupos_uteis()),
        "P3188": p3188_auditoria_do_leitor_v5()[:3] == (91, 84, 0),  # Parte 144: a 135 ganhou 8 vereditos depois da 1a fixação (83, 76)
        "P3190": (lambda r: abs(r[0] - 4) < 1e-9 and r[1] < 1e-9 and abs(r[3] - 3.95560) < 1e-5)(p3190_hexadecimal_vertices()),
        "P3191": p3191_calibracao_v4_v5(range(80, 139)) == ((360, 325), (480, 433)),  # Parte 144: a 135 ganhou 8 vereditos (antes 472, 425)
        "P3193": [t for _, t, _ in p3193_enantiodromia()] == [0, 0, 0, 1, 3, 4, 5, 7],
        "P3194": p3194_compensacao() < 1e-12,
        "P3195": (lambda r: (r[3], round(r[0], 4), round(r[2], 5)) == (53058, 0.9844, 0.49766))(p3195_fluxo_em_portugues()),
        "P3196": (lambda r: abs(r[2][0] - 3) < 1e-6 and round(r[5][1], 5) == 0.0003 and round(r[7][1], 5) == 0.00008)(p3196_benford16_potencias()),
        "P3197": (lambda r: (round(r[0][2][0], 4), round(r[0][16][0], 4), r[2]) == (0.8756, 0.8467, False))(p3197_grupos_uteis_mundo_novo()),
        "P3198": (lambda r: (round(r["Q"], 4), round(r["G2"], 4), round(r["G8"], 4)) == (0.1533, 0.2017, 0.1707))(p3198_grpo_no_jogo_de_palavras()),
        "P3199": (lambda r: (round(r["Q"], 4), round(r["G2"], 4), round(r["G8"], 4), r["ambas"]) == (0.302, 0.3966, 0.3973, 10))(p3199_grpo_no_dicionario_grande()),
        "P3200": (lambda r: (round(r["o"], 4), round(r["lotes"][(13, 23)][0], 4)) == (-0.0022, 0.3278))(p3200_lotes_do_q()),
        "P3201": (lambda r: (round(r["Q"], 4), round(r["G2"], 4), round(r["G8"], 4), r["ambas"]) == (0.1431, 0.2038, 0.2118, 18))(p3201_grpo_por_dicionario("pt", tuple(range(121, 141)))),
        "P3202": round(p3202_aleatorio_por_dicionario()[0], 4) == 0.0087,
        "P3203": p3203_auditoria_t()[1] == 1,
        "P3204": round(p3204_densidades()[0]["pt/PT"], 4) == 0.1093,
        "P3205": (lambda r: (round(r["Q"], 4), round(r["aleat"], 4), r["ambas"]) == (0.2934, 0.0221, 17))(p3205_grpo_tabuleiro(sementes=tuple(range(121, 141)))),
        "P3206": (round(p3206_aleatorio_tabuleiro("en")[0], 4), round(p3206_aleatorio_tabuleiro("embutido")[0], 4)) == (0.0465, 0.0062),
        "P3207": tuple(round(p3207_aleatorio_geometria(tamanho=a, minimo=b, maximo=d)[0], 4) for a, b, d in ((4, 3, 5), (6, 3, 5), (5, 3, 4), (5, 4, 5))) == (0.0251, 0.0204, 0.0368, 0.007),
        "P3208": (lambda r: (round(r["repete"], 4), round(r["distintas"], 2)) == (0.9425, 22.35))(p3208_repertorio("embutido", "en", tuple(range(121, 141)))),
        "P3176v10": (lambda r: (r["diferentes"], r["categorias"]["mundo"], r["blocos_sem_excecao"]) == (15, 0, 138))(
            p3176_comparar_voltas_v2("reproducao/volta9", "reproducao/volta10")),
        "P3176v9": (lambda r: (r["diferentes"], r["categorias"]["mundo"], r["blocos_sem_excecao"]) == (17, 0, 137))(
            p3176_comparar_voltas_v2("reproducao/volta8", "reproducao/volta9")),
        "P3176v8": (lambda r: (r["diferentes"], r["categorias"]["mundo"], r["novas"], r["blocos_sem_excecao"]) == (8, 0, [134], 131))(
            p3176_comparar_voltas_v2("reproducao/volta7", "reproducao/volta8")),
        "P3176v7": (lambda r: (r["diferentes"], r["categorias"]["mundo"], r["novas"], r["blocos_sem_excecao"]) == (9, 0, [133], 130))(
            p3176_comparar_voltas_v2("reproducao/volta6", "reproducao/volta7")),
    }
    return sum(verificacoes.values()), len(verificacoes), [k for k, ok in verificacoes.items() if not ok]


# --- Execução: cada parte é uma função; a unificação roda sempre ao final ---


def _parte_1():
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


def _parte_2():
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


def _parte_3():
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


def _parte_4():
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


def _parte_5():
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
            cat, val, perg, liq, pstar = p83_85_synthai(rho_c, diverso)
            print(f"P85 SYNTHAI rho_cego={rho_c} diverso={diverso!s:5}: catastrofes = {cat:.4f}, valor = {val:.3f}, "
                  f"perguntas/episodio = {perg:.3f}, liquido (com custo das perguntas) = {liq:.3f}")
    for b in (1.5, 6.0):
        cat, val, perg, liq, _ = p83_85_synthai(0.0, False, bonus_implantado=b)
        print(f"P85 SYNTHAI mundo mudado (bonus {b}): catastrofes = {cat:.4f}, perguntas = {perg:.3f}, liquido = {liq:.3f}")
    cat4, val4, cons4 = p67_agente("completo")
    print(f"P85 referencia Parte 4 'completo' (rho 0): liquido com custo das consultas = {val4 - 50 * cat4 - 0.1 * cons4:.3f}")
    cat4, val4, cons4 = p67_agente("completo", rho_cego=0.5)
    print(f"P85 referencia Parte 4 'completo' (rho 0.5): liquido com custo das consultas = {val4 - 50 * cat4 - 0.1 * cons4:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro()
    print(f"P95 minha taxa de erro (6/12): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")
    media, lo, hi = p95_minha_taxa_de_erro(erros=7, testes=14)
    print(f"P95 atualizada com a Parte 5 (7/14): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_6():
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
            cat, val, perg, liq, eps = p112_synthai_jung(versao, semente=semente)
            print(f"P112 semente {semente} {versao:11s}: catastrofes = {cat:.4f}, valor = {val:.3f}, "
                  f"perguntas = {perg:.3f}, liquido = {liq:.3f}, erro humano final = {eps:.3f}")
    for versao in ("synthai", "jung_v2"):
        cat, val, perg, liq, eps = p112_synthai_jung(versao, fadiga=0.0)
        print(f"P112 sem fadiga {versao:8s}: catastrofes = {cat:.4f}, perguntas = {perg:.3f}, liquido = {liq:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=10, testes=19)
    print(f"P113 minha taxa de erro (10/19): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_7():
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


def _parte_8():
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


def _parte_9():
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
    print(f"P152 SYNTHAI realista em 10 sementes novas: media = {ruido['base'][0]:.3f}, dp = {ruido['base'][1]:.3f}")
    for nome, (m, dp, tt) in ((k, v) for k, v in ruido.items() if k != "base"):
        rotulo = "carga 0.3 - carga 0.2" if nome == "carga" else "P* x2 - P* x1"
        print(f"P152 diferenca pareada {rotulo}: media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=21, testes=37)
    print(f"P153 minha taxa de erro (21/37): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_10():
    print("--- Parte 10 (rumo a AGI: Upsilon, trajetoria, funcao inferior, complementaridade) ---")
    medias, passos = p157_trajetoria()
    for v, (m, dp) in medias.items():
        print(f"P157 {v:12s}: liquido medio (10 sementes) = {m:.3f}, dp = {dp:.3f}")
    for nome, (m, dp, tt) in passos.items():
        print(f"P157 passo {nome}: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    ganhos = [m for m, _, _ in passos.values()]
    print(f"P163 razao entre ganhos sucessivos = {[round(r, 3) for r in p163_minha_decolagem(ganhos)]}")
    upsilon, por_mundo = p158_upsilon()
    print(f"P158 Upsilon (0 = acaso, 1 = oraculo) = { {a: round(u, 3) for a, u in upsilon.items()} }")
    for mundo, notas in por_mundo.items():
        print(f"P158 {mundo:22s}: { {a: round(n, 3) for a, n in notas.items()} }")
    print(f"P159 catastrofes = { {k: round(v, 4) for k, v in p159_armadilha_nova().items()} }")
    produto, n_ot, erro = p160_complementaridade()
    print(f"P160 variancia x perturbacao = {produto:.2e} (nao depende de n); auditorias otimas = {n_ot:.0f}; erro total = {erro:.4f}")
    h, hmax, inferior = p161_quatro_funcoes()
    print(f"P161 entropia do perfil da SYNTHAI = {h:.3f} de {hmax:.0f} bits; funcao inferior = {inferior}")
    for mundo, (cat, difs) in p162_intuicao().items():
        print(f"P162 {mundo}: catastrofes = { {k: round(v, 4) for k, v in cat.items()} }")
        for perda, (m, dp, tt) in difs.items():
            print(f"P162 {mundo}, perda {perda}: intuitiva - realista = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=24, testes=43)
    print(f"P164 minha taxa de erro (24/43): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_11():
    print("--- Parte 11 (tivemos avanco rumo a AGI/ASI?) ---")
    upsilon = p168_upsilon_trajetoria()
    print(f"P168 Upsilon por versao da linhagem = { {v: round(u, 3) for v, u in upsilon.items()} }")
    bits, log10_peso = p169_peso_da_familia()
    print(f"P169 K(familia de mundos) <= {bits} bits (codigo comprimido); peso no Upsilon universal ~ 10^{log10_peso:.0f}")
    tem, total, frac = p170_lista_de_capacidades()
    print(f"P170 capacidades de AGI cobertas pela SYNTHAI = {tem} de {total} ({frac:.0%})")
    for nome, ok, onde in CAPACIDADES_AGI:
        print(f"P170   [{'x' if ok else ' '}] {nome} ({onde})")
    usado, ordens = p171_lacuna_de_compute()
    print(f"P171 compute de uma execucao completa ~ {usado:.1e} FLOP; lacuna para a fronteira = {ordens:.1f} ordens de grandeza")
    taxas, qui2, pval, incl = p172_minha_precisao()
    print(f"P172 minha taxa de erro por parte (3 a 10) = {[round(x, 3) for x in taxas]}; inclinacao = {incl:.3f}/parte; "
          f"qui2 = {qui2:.3f}, p = {pval:.3f}")
    for mundo, (cat, difs) in p173_dosada().items():
        print(f"P173 {mundo}: catastrofes = { {k: round(v, 4) for k, v in cat.items()} }")
        for (outra, perda), (m, dp, tt) in difs.items():
            print(f"P173 {mundo}, perda {perda}: dosada - {outra} = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P176, testes=TESTES_P176)
    print(f"P176 minha taxa de erro ({ERROS_P176}/{TESTES_P176}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_12():
    print("--- Parte 12 (a funcao auxiliar: planejar em varios passos) ---")
    so_v, com_c, razao = p181_valor_da_previsao()
    print(f"P181 valor total escolhendo so pelo agora = {so_v:.3f}; prevendo o futuro = {com_c:.3f}; razao teorica = {razao:.3f}")
    medias, difs = p182_planejar()
    for v, (ret, cat, por_passo) in medias.items():
        print(f"P182 {v:25s}: retorno por episodio = {ret:.3f}, catastrofes por episodio = {cat:.4f}, por passo = {por_passo}")
    for nome, (m, dp, tt) in difs.items():
        print(f"P182 {nome}: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    print(f"P183 P* por passo com a perda do futuro = {[round(x, 5) for x in p183_limiar_por_passo()]}")
    for n_acoes, (p_cat, p_seg) in p184_transferencia().items():
        print(f"P184 calibracao com {n_acoes} acoes: P media nas catastrofes = {p_cat:.3f}, nas seguras = {p_seg:.4f}, "
              f"razao = {p_cat / p_seg:.1f}")
    for v, (m, dp, minimo) in p185_familia_aleatoria().items():
        print(f"P185 {v}: Upsilon em 20 mundos sorteados = {m:.3f} (dp {dp:.3f}, pior mundo {minimo:.3f})")
    medias, difs = p182_planejar(mundo={"sigma_modelo": 2.0})
    for v, (ret, cat, _) in medias.items():
        print(f"P186 modelo ruim (sigma 2) {v:25s}: retorno = {ret:.3f}, catastrofes = {cat:.4f}")
    for nome, (m, dp, tt) in difs.items():
        print(f"P186 modelo ruim {nome}: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    tem, total, _ = p170_lista_de_capacidades()
    print(f"P189 capacidades de AGI: {tem + 1} de {total} (planejar em varios passos, num mundo de 5 passos)")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P188, testes=TESTES_P188)
    print(f"P188 minha taxa de erro ({ERROS_P188}/{TESTES_P188}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_13():
    print("--- Parte 13 (o canal da cautela, transferencia entre tipos de tarefa, a pergunta 200) ---")
    medias, (m, dp, tt) = p192_canal_da_cautela()
    for v, (ret, cat, por_passo) in medias.items():
        print(f"P192 {v:25s}: retorno = {ret:.3f}, catastrofes = {cat:.4f}, por passo = {por_passo}")
    print(f"P192 prudente - planejadora: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    medias, difs = p194_transferencia_de_tipo()
    for v, (ret, cat, perg) in medias.items():
        print(f"P194 {v:12s}: retorno por rodada = {ret:.2f}, catastrofes por rodada = {cat:.3f}, perguntas = {perg:.2f}")
    for nome, (m, dp, tt) in difs.items():
        print(f"P194 {nome}: diferenca media = {m:.2f}, dp = {dp:.2f}, t = {tt:.2f}")
    testes, erros, certas, frac = p200_retrospectiva()
    print(f"P200 Partes 3-12: {testes} afirmacoes testadas, {erros} corrigidas, {certas} certas de primeira ({frac:.0%})")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P197, testes=TESTES_P197)
    print(f"P197 minha taxa de erro ({ERROS_P197}/{TESTES_P197}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_14():
    print("--- Parte 14 (o ultimo passo, a memoria de um so golpe, o peso do passado) ---")
    medias, (m, dp, tt) = p203_ultimo_passo()
    for v, (ret, cat, por_passo) in medias.items():
        print(f"P203 {v:25s}: retorno = {ret:.3f}, catastrofes = {cat:.4f}, por passo = {por_passo}")
    print(f"P203 velha - planejadora: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    metades, (m, dp, tt), fobia, lembrancas = p204_memoria()
    for v, (a, b) in metades.items():
        print(f"P204 armadilha nova, {v:8s}: catastrofes 1a metade = {a:.4f}, 2a metade = {b:.4f}")
    print(f"P204 memoria - realista: diferenca media no liquido = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    print(f"P205 memorias guardadas (media) = {lembrancas:.1f}; acoes seguras marcadas como suspeitas = {fobia:.3f}")
    print(f"P206 gerador rapido identico ao original = {p206_identidade()}")
    razao, prevista = p207_sonhos_variancia()
    print(f"P207 variancia compensada / equilibrada = {razao:.3f}; prevista pela amostra efetiva (P122) = {prevista:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P210, testes=TESTES_P210)
    print(f"P210 minha taxa de erro ({ERROS_P210}/{TESTES_P210}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_15():
    print("--- Parte 15 (SYNTHAI: o nome, a memoria que esquece, a sintese dos modulos) ---")
    n, apelidos, ok, total = p213_nome_como_simetria()
    print(f"P213 classes renomeadas = {n}; nomes antigos continuam como apelidos = {apelidos}; regressao apos a troca = {ok}/{total}")
    metades, (m, dp, tt), fobia, lembrancas = p214_memoria_v2()
    for v, (a, b) in metades.items():
        print(f"P214 armadilha nova, {v:10s}: catastrofes 1a metade = {a:.4f}, 2a metade = {b:.4f}")
    print(f"P214 memoria v2 - realista: diferenca media no liquido = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    print(f"P214 memorias vivas ao fim (media) = {lembrancas:.1f}; acoes seguras marcadas como suspeitas = {fobia:.3f}")
    auc = p215_distinguivel()
    print(f"P215 AUC da calibracao (0.5 = acaso): armadilha conhecida = {auc['conhecida']:.3f}, armadilha nova = {auc['nova']:.3f}")
    for mundo, (cat, (m, dp, tt)) in p216_sintese().items():
        print(f"P216 {mundo}: catastrofes = { {k: round(v, 4) for k, v in cat.items()} }; integral - velha = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    aprendido, teoria = p218_inspecao_aprendida()
    for punicao, (insp, trap) in aprendido.items():
        print(f"P218 punicao {punicao:.0f}: inspecao aprendida = {insp:.4f}, trapaca aprendida = {trap:.4f}")
    print(f"P218 equilibrio teorico (P77, punicao 9) = inspecao {teoria[0]:.2f}, trapaca {teoria[1]:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P222, testes=TESTES_P222)
    print(f"P219 minha taxa de erro ({ERROS_P222}/{TESTES_P222}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_16():
    print("--- Parte 16 (um sentido novo) ---")
    d_atual, d_total, auc_prevista, auc_so_sensor = p223_sinal_combinado()
    print(f"P223 d' atual = {d_atual:.3f}; com o sensor (d' = 1) = {d_total:.3f}; AUC prevista = {auc_prevista:.3f}; "
          f"AUC do sensor sozinho = {auc_so_sensor:.3f}")
    par, sim_par, seq, sim_seq, formula_p94, corrigido = p224_auditoria_p94()
    print(f"P224 salvaguardas independentes: formula = {par:.5f}, simulado = {sim_par:.5f}; estagios em ordem: formula = {seq:.5f}, "
          f"simulado = {sim_seq:.5f}; formula usada na P94 = {formula_p94:.5f}")
    print(f"P224 numero da P94 corrigido (4 salvaguardas, 50 anos) = {corrigido:.2e} (publicado: 2.60e-07)")
    for mundo, (cat, (m, dp, tt)) in p225_sentido_novo().items():
        print(f"P225 {mundo}: catastrofes = { {k: round(v, 5) for k, v in cat.items()} }; sentidos - realista = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    auc = p226_auc_com_sentido()
    print(f"P226 AUC com o sentido novo: armadilha conhecida = {auc['conhecida']:.3f}, armadilha nova = {auc['nova']:.3f}")
    medias, (m, dp, tt) = p227_velha_com_sentido()
    for v, (ret, cat) in medias.items():
        print(f"P227 armadilha nova, mundo sequencial, {v:14s}: retorno = {ret:.3f}, catastrofes = {cat:.4f}")
    print(f"P227 velha com sentido - velha: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P230, testes=TESTES_P230)
    print(f"P230 minha taxa de erro ({ERROS_P230}/{TESTES_P230}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_17():
    print("--- Parte 17 (quanto vale perceber, e onde olhar) ---")
    upsilon = p168_upsilon_trajetoria(versoes=("p8_x2", "p16_sentidos"))
    print(f"P233 Upsilon na familia de 9 mundos = { {v: round(u, 3) for v, u in upsilon.items()} }")
    for v, (m, dp, minimo) in p185_familia_aleatoria(versoes=("p8_x2", "p16_sentidos")).items():
        print(f"P233 {v}: Upsilon em 20 mundos sorteados = {m:.3f} (dp {dp:.3f}, pior mundo {minimo:.3f})")
    for d, (m, dp, tt, cat_base, cat_com, auc) in p234_valor_do_sentido().items():
        print(f"P234 sensor d' = {d}: ganho no liquido = {m:.3f} (dp {dp:.3f}, t = {tt:.2f}); catastrofes {cat_base:.4f} -> {cat_com:.4f}; "
              f"AUC prevista = {auc:.3f}")
    ganho, (m, dp, tt), foco = p235_atencao()
    print(f"P235 ganho sobre a realista, ja descontado o custo das leituras: ler todas = {ganho['todas']:.3f}, "
          f"ler so as {foco:.0%} melhores = {ganho['seletiva']:.3f}")
    print(f"P235 seletiva - todas: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    for b, (teoria, sim) in p237_auditoria_p57().items():
        print(f"P237 ponto cego do verificador {b:.0%}: corrigivel apos 1000 modificacoes = {teoria:.3f} (teoria), {sim:.3f} (simulado)")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P239, testes=TESTES_P239)
    print(f"P239 minha taxa de erro ({ERROS_P239}/{TESTES_P239}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_18():
    print("--- Parte 18 (a linguagem como canal) ---")
    binario, palavras, razao = p242_bits_do_veto()
    print(f"P242 informacao por resposta (prior 0.1, erro 0.1): veto binario = {binario:.3f} bit; quatro palavras = {palavras:.3f} bit; "
          f"razao = {razao:.2f}")
    medias, difs, aprendido, verdadeiro = p245_linguagem()
    for v, (cat, perg, liq) in medias.items():
        print(f"P245 {v:15s}: catastrofes = {cat:.4f}, perguntas = {perg:.3f}, liquido = {liq:.3f}")
    for nome, (m, dp, tt) in difs.items():
        print(f"P245 {nome}: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    for w in PALAVRAS:
        print(f"P244 P(catastrofe | '{w}'): aprendido = {aprendido[w]:.3f}; suposto com prior 0.1 = {verdadeiro[w]:.3f}")
    for nome, (ach, fal, teoria) in p247_auditoria_p105().items():
        print(f"P247 {nome}: achados = {ach:.3f} (teoria {teoria[0]:.3f}), falsos = {fal:.3f} (teoria {teoria[1]:.3f})")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P249, testes=TESTES_P249)
    print(f"P249 minha taxa de erro ({ERROS_P249}/{TESTES_P249}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_19():
    print("--- Parte 19 (a palavra precisa, a versao principal e a trajetoria inteira) ---")
    binario, precisa, razao = p252_bits_da_palavra_precisa()
    print(f"P252 informacao por resposta: veto binario = {binario:.3f} bit; quatro palavras precisas = {precisa:.3f} bit; razao = {razao:.2f}")
    medias, (m, dp, tt) = p252_palavra_precisa()
    for v, (cat, liq) in medias.items():
        print(f"P252 {v:8s}: catastrofes = {cat:.4f}, liquido = {liq:.3f}")
    print(f"P252 precisa - binario: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    medias, difs = p253_versao_principal()
    for v, (ret, cat) in medias.items():
        print(f"P253 {v:14s}: retorno (ja descontadas as leituras) = {ret:.3f}, catastrofes = {cat:.4f}")
    for nome, (m, dp, tt) in difs.items():
        print(f"P253 {nome}: diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    teto0, r0, erro0 = p254_trajetoria_do_upsilon(pontos=((5, 0.287), (7, 0.414), (8, 0.465), (9, 0.449), (10, 0.409), (11, 0.486)))
    teto, r, erro = p254_trajetoria_do_upsilon()
    print(f"P254 teto do Upsilon ajustado nas Partes 5-11 = {teto0:.3f} (r = {r0:.2f}, erro {erro0:.3f}); com a Parte 17 = {teto:.3f} "
          f"(r = {r:.2f}, erro {erro:.3f}); Upsilon com o sentido novo = 0.547")
    perfil, h = p255_quaternidade()
    print(f"P255 modulos por funcao de Jung = {perfil}; entropia = {h:.3f} de 2 bits (P161: 1.561)")
    sim, teoria = p256_auditoria_p121()
    print(f"P256 R2 da quarta funcao: simulado = {sim:.4f}, formula da P121 = {teoria:.4f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P258, testes=TESTES_P258)
    print(f"P258 minha taxa de erro ({ERROS_P258}/{TESTES_P258}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_20():
    print("--- Parte 20 (o simbolo com o tempo, o Upsilon sequencial e o que cada funcao vale) ---")
    resumo, (m, dp, tt) = p262_simbolo_com_o_tempo()
    for v, (auc, liq) in resumo.items():
        print(f"P262 {v:12s}: AUC final = {auc:.3f}, liquido = {liq:.3f}")
    print(f"P262 AUC(veto) - AUC(fala): diferenca media = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    upsilon, por_mundo = p265_upsilon_sequencial()
    print(f"P265 Upsilon sequencial = { {v: round(u, 3) for v, u in upsilon.items()} }")
    for mundo, notas in por_mundo.items():
        print(f"P265 {mundo:15s}: { {v: round(n, 3) for v, n in notas.items()} }")
    completa, resultado = p266_o_que_cada_funcao_vale()
    print(f"P266 versao principal completa (armadilha nova): retorno = {completa:.3f}")
    for nome, (m, dp, tt) in resultado.items():
        print(f"P266 {nome}: perda ao tirar = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    media, ep, tt = p268_efeito_combinado()
    print(f"P268 ganho do sentido novo no mundo sequencial, tres estimativas combinadas = {media:.3f} (ep {ep:.3f}, t = {tt:.2f})")
    media, dp, teoria = p267_auditoria_p146()
    print(f"P267 crenca compartilhada final com ruido = {media:.3f} (dp {dp:.3f}); formula da P146 = {teoria:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P269, testes=TESTES_P269)
    print(f"P269 minha taxa de erro ({ERROS_P269}/{TESTES_P269}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_21():
    print("--- Parte 21 (a intuicao corrigida pela sensacao) ---")
    for sigma, (w_otimo, w_teoria, val_1, val_otimo) in p272_encolhimento().items():
        print(f"P272 sigma do modelo = {sigma}: peso otimo simulado = {w_otimo}, teoria 1/(1+sigma^2) = {w_teoria:.2f}; "
              f"valor com peso 1 = {val_1:.3f}, com o peso otimo = {val_otimo:.3f}")
    for mundo, ((m, dp, tt), peso, teoria) in p274_intuicao_calibrada().items():
        print(f"P274 {mundo}: calibrada - versao principal = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}; peso aprendido = {peso:.3f} "
              f"(teoria {teoria:.3f})")
    upsilon, por_mundo = p265_upsilon_sequencial(versoes=("velha_atenta", "calibrada"))
    print(f"P275 Upsilon sequencial = { {v: round(u, 3) for v, u in upsilon.items()} }")
    for mundo, notas in por_mundo.items():
        print(f"P275 {mundo:15s}: { {v: round(n, 3) for v, n in notas.items()} }")
    for d, (sim, formula) in p277_auditoria_p149().items():
        print(f"P277 erro medio por passo {d}: horizonte mediano simulado = {sim}; formula da P149 = {formula:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P279, testes=TESTES_P279)
    print(f"P279 minha taxa de erro ({ERROS_P279}/{TESTES_P279}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_22():
    print("--- Parte 22 (o prototipo em modulos: pacote synthai/) ---")
    for mundo, (a, b, (m, dp, tt), peso, cat_a, cat_b) in p283_equivalencia_modular().items():
        print(f"P283 {mundo}: calculos = {a:.3f}, modular = {b:.3f}; diferenca = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}; "
              f"peso da intuicao modular = {peso:.3f}; catastrofes {cat_a:.4f} vs {cat_b:.4f}")
    for tarefa, (medias, cats, (ma, da, ta), (mg, dg, tg), norm) in p284_generalidade().items():
        print(f"P284 {tarefa:13s}: { {k: round(v, 2) for k, v in medias.items()} }; catastrofes { {k: round(v, 4) for k, v in cats.items()} }")
        print(f"P284 {tarefa:13s}: Synthai - acaso = {ma:.2f} (t = {ta:.1f}); Synthai - guloso = {mg:.2f} (t = {tg:.1f}); "
              f"normalizado = {norm:.3f}")
    n, arestas, interface, escondidos, linhas, linhagem = p285_acoplamento()
    print(f"P285 modulos do agente = {n}; arestas = {len(arestas)} {arestas}; interface = {len(interface)} atributos {interface}; "
          f"acessos ao escondido = {escondidos}; linhas de codigo = {linhas}; linhagem em calculos = {len(linhagem)} classes")
    print(f"P286 testes de unidade (testes, falhas) = {p286_testes_de_unidade()}")
    n, dv, formula, exato, rel = p287_veto_falso()
    print(f"P287 vetos falsos = {n}; custo medio dv = {dv:.3f}; P* da P71 = {formula:.5f}; limiar exato = {exato:.5f} ({rel:+.1%})")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P289, testes=TESTES_P289)
    print(f"P289 minha taxa de erro ({ERROS_P289}/{TESTES_P289}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_23():
    print("--- Parte 23 (reconhecer o que ja estava resolvido) ---")
    n, teoria, lado, exato = p291_menon()
    print(f"P291 Menon: perguntas de sim/nao ate 0,001 = {n} (log2: {teoria}); lado = {lado:.5f}; diagonal 2*sqrt(2) = {exato:.5f}")
    w, r0, rn, teoria = p292_ponto_neutro()
    print(f"P292 peso da leitura = {w:.3f}; prevista/real sem leitura: com 0 = {r0:.3f} (teoria {teoria:.3f}), com o neutro w/2 = {rn:.3f}")
    w3, r0, rn, n = p293_neutro_no_agente()
    print(f"P293 w3 aprendido = {w3:.3f}; opcoes sem leitura ({n} catastrofes): prevista/real com 0 = {r0:.3f}, com o neutro = {rn:.3f}")
    for tarefa, (medias, cats, difs) in p294_reconhecer().items():
        print(f"P294 {tarefa}: { {k: round(v, 3) for k, v in medias.items()} }; catastrofes { {k: round(v, 4) for k, v in cats.items()} }")
        for v, (m, dp, tt) in difs.items():
            print(f"P294 {tarefa}: {v} - parte22 = {m:.4f}, dp = {dp:.4f}, t = {tt:.2f}")
    for nome, f in (("P295", p295_bandido_reconhecido), ("P296 (exploratorio)", p296_ablacao_bandido)):
        norm, cats, razao, difs = f()
        print(f"{nome} normalizado { {k: round(v, 3) for k, v in norm.items()} }")
        print(f"{nome} catastrofes por rodada { {k: round(v, 3) for k, v in cats.items()} }; "
              f"arrependimento / Lai-Robbins { {k: round(v, 3) for k, v in razao.items()} }")
        for v, (m, dp, tt) in difs.items():
            print(f"{nome} {v}: diferenca = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    mx, qt = p297_p42_exato()
    print(f"P297 P42 em forma fechada: maximizador = {mx:.4f} (simulado 0,548), quantilizador = {qt:.4f} (simulado 0,140)")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P299, testes=TESTES_P299)
    print(f"P299 minha taxa de erro ({ERROS_P299}/{TESTES_P299}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_24():
    print("--- Parte 24 (o pensamento diferenciado: ajustar ate convergir) ---")
    metodos, positivos = p302_convergencia()
    print(f"P302 catastrofes por historico de treino = {positivos:.1f}")
    for m, (w3, treino, teste) in metodos.items():
        print(f"P302 {m:13s}: w3 = {w3:.3f}; log-perda treino = {treino:.5f}, teste = {teste:.5f}")
    for nome, (w3, r0, rn, n) in p303_fora_da_atencao_exato().items():
        print(f"P303 {nome:13s}: w3 = {w3:.3f}; sem leitura ({n} catastrofes): prevista/real com 0 = {r0:.3f}, com o neutro = {rn:.3f}")
    taxas, kappa, epocas, w3, pos = p304_teoria_da_convergencia()
    print(f"P304 taxas por epoca (eta n lambda) = {[round(t, 3) for t in taxas]}; kappa mediano = {kappa:.0f}; "
          f"epocas pedidas pela teoria = {epocas}")
    for e in (118, 237):
        m, mx = p304b_conferir_epocas(e)
        print(f"P304 gradiente com {e} epocas: |w3 - w3*| medio = {m:.4f}, maximo = {mx:.4f}")
    m, mx = p304c_piso_de_ruido()
    print(f"P304 piso com eta = 0,01 e 1000 epocas: |w3 - w3*| medio = {m:.4f}, maximo = {mx:.4f}")
    f, d = p304d_vies_de_primeira_ordem()
    print(f"P304 vies de primeira ordem (Cordeiro-McCullagh) delta3 = {f:.4f}; Firth - maxima verossimilhanca = {d:.4f}")
    for tarefa, (medias, cats, difs) in p305_pensante().items():
        print(f"P305 {tarefa}: { {k: round(v, 3) for k, v in medias.items()} }; catastrofes { {k: round(v, 4) for k, v in cats.items()} }")
        for v, (m, dp, tt) in difs.items():
            print(f"P305 {tarefa}: {v} - exploradora = {m:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    for nome, r in p305b_onde_se_decide().items():
        print(f"P305b (exploratorio) {nome}: prevista/real no topo = {r[0]:.3f}, em todas = {r[1]:.3f}; taxa real no topo = {r[2]:.4f}; "
              f"perguntas = {r[3]:.3f}; catastrofes = {r[4]:.4f}; aceitas sem perguntar = {r[5]:.3f} do topo, "
              f"P media = {r[6]:.4f}, taxa real = {r[7]:.4f}")
    print(f"P306 Newton, erro por iteracao = {[f'{x:.1e}' for x in p306_newton_quadratico()]}")
    ajustes, desloc = p307_selecao()
    for nome, (b, w, n) in ajustes.items():
        print(f"P307 {nome:13s}: intercepto = {b:.3f}, inclinacao = {w:.3f} (n = {n})")
    print(f"P307 deslocamento do intercepto no caso-controle = {ajustes['caso_controle'][0] - ajustes['tudo'][0]:.3f}; ln(1/0,05) = {desloc:.3f}")
    h0, hn, hg = p308_informacao()
    print(f"P308 bits por opcao: entropia = {h0:.4f}; restam com Newton = {hn:.4f}; com o gradiente de 3 epocas = {hg:.4f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P309, testes=TESTES_P309)
    print(f"P309 minha taxa de erro ({ERROS_P309}/{TESTES_P309}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_25():
    print("--- Parte 25 (o sentimento que acompanha o pensamento: o limiar de cada pensamento) ---")
    for modelo, (m, t, frac, p_med, real) in p312_limiar_pela_conta().items():
        print(f"P312 {modelo:9s}: m pela conta do quantil = {m:.2f} (t = {t:.4f}); abaixo de 2P*: fracao = {frac:.3f}, "
              f"P media = {p_med:.4f}, taxa real = {real:.4f}")
    for modelo, (medias, cats, perg, melhor) in p313_varredura().items():
        print(f"P313 {modelo:9s}: retorno { {m: round(v, 3) for m, v in medias.items()} }; catastrofes "
              f"{ {m: round(v, 4) for m, v in cats.items()} }; melhor m = {melhor}")
    n, dd, m = p314_custo_do_descarte()
    print(f"P314 descartes seguros = {n}; custo medio do descarte = {dd:.3f}; m = dd/(L P*) = {m:.2f}")
    for tarefa, (medias, cats, difs) in p315_limiar_no_comportamento().items():
        print(f"P315 {tarefa}: { {k: round(v, 3) for k, v in medias.items()} }; catastrofes { {k: round(v, 4) for k, v in cats.items()} }")
        for v, (d, dp, tt) in difs.items():
            print(f"P315 {tarefa}: {v} - principal = {d:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    conf, z = p315b_confirmacao()
    for tarefa, (cats, (d, dp, tt)) in conf.items():
        print(f"P315b {tarefa}: newton_m05 - principal = {d:.3f}, dp = {dp:.3f}, t = {tt:.2f}; catastrofes { {k: round(v, 4) for k, v in cats.items()} }")
    print(f"P315b Stouffer z = {z:.2f}")
    for (mundo, modelo), (n, dd, f, m) in p316_conta_nos_mundos().items():
        print(f"P316 {mundo} {modelo:9s}: descartes = {n}; dd = {dd:.3f}; fator real/previsto = {f:.2f}; m = {m:.2f}")
    for modelo, (medias, cats, melhor) in p317_varredura_sequencial().items():
        print(f"P317 {modelo:9s}: retorno { {m: round(v, 3) for m, v in medias.items()} }; melhor m = {melhor}")
    for modelo, ms in p318_ponto_fixo_nos_mundos().items():
        print(f"P318 {modelo:9s}: ponto fixo = {[round(m, 2) for m in ms]}")
    for modelo, (medias, cats, melhor) in p318b_varredura_catastrofe_x2().items():
        print(f"P318b {modelo:9s}: retorno { {m: round(v, 3) for m, v in medias.items()} }; melhor m = {melhor}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P319, testes=TESTES_P319)
    print(f"P319 minha taxa de erro ({ERROS_P319}/{TESTES_P319}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_26():
    print("--- Parte 26 (a constante que faltava: os termos da conta, um por um) ---")
    for (mundo, modelo), t in p322_termos_nos_mundos().items():
        print(f"P322 {mundo} {modelo:9s}: L_ef = {t['L_ef']:.1f}; dd valor = {t['dd_valor']:.3f}, com o plano = {t['dd_plano']:.3f}; "
              f"f = {t['f_todas']:.3f} (aceitas {t['f_aceitas']:.3f}); m: P316 = {t['m_P316']:.2f}, L = {t['m_L']:.2f}, "
              f"plano = {t['m_plano']:.2f}, tudo = {t['m_tudo']:.2f}")
    for (mundo, modelo), m in p323_conta_nos_mundos_novos().items():
        print(f"P323 {mundo} {modelo:9s}: m pela conta corrigida = {m:.3f}")
    for (mundo, modelo), (medias, cats, melhor) in p324_varredura_nos_mundos_novos().items():
        print(f"P324 {mundo} {modelo:9s}: retorno { {m: round(v, 3) for m, v in medias.items()} }; melhor m = {melhor}")
    (k, ch, bits, d), (k2, ch2, bits2, d2) = p325_chance()
    print(f"P325 conta: acertos = {k}/6, chance ao acaso = {ch:.4f}, bits = {bits:.2f}, |log2| medio = {d:.3f}; "
          f"ingenuo: {k2}/6, chance = {ch2:.4f}, bits = {bits2:.2f}, |log2| medio = {d2:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P329, testes=TESTES_P329)
    print(f"P329 minha taxa de erro ({ERROS_P329}/{TESTES_P329}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_27():
    print("--- Parte 27 (a autorregulacao: a SYNTHAI calcula o proprio limiar) ---")
    l_ef, f, dd, b, m = p332_estimadores_proprios()
    print(f"P332 de dentro: L = {l_ef:.2f}, f = {f:.3f}, dd = {dd:.3f}, inclinacao valor~nota = {b:.4f} (conta 1/(1+0,25/6) = "
          f"{1 / (1 + 0.25 / 6):.4f}), m = {m:.3f}")
    for tarefa, (medias, cats, ms, difs, contra_fixo) in p333_autorregulada().items():
        print(f"P333 {tarefa}: { {k: round(v, 3) for k, v in medias.items()} }; catastrofes { {k: round(v, 4) for k, v in cats.items()} }; "
              f"m final { {k: round(v, 2) for k, v in ms.items()} }")
        for v, (d, dp, tt) in difs.items():
            print(f"P333 {tarefa}: {v} - principal = {d:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
        print(f"P333 {tarefa}: auto_newton - newton_m05 = {contra_fixo[0]:.3f}, dp = {contra_fixo[1]:.3f}, t = {contra_fixo[2]:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P339, testes=TESTES_P339)
    print(f"P339 minha taxa de erro ({ERROS_P339}/{TESTES_P339}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_28():
    print("--- Parte 28 (a ancora: pessimismo sob incerteza e a realidade de fora) ---")
    for k in (9.5, 25.0, 100.0):
        print(f"P341 quantil 80% / media da Gamma com k = {k:g} catastrofes = {(1 - 1 / (9 * k) + 0.8416 / (3 * sqrt(k))) ** 3:.3f}")
    for nome, (f, m, m_med, cats_aud, p_aud) in p342_conta_da_ancora().items():
        print(f"P342 {nome:17s}: f = {f:.3f}; m medio = {m:.3f}, mediano = {m_med:.3f}; auditoria: catastrofes = {cats_aud:.1f}, soma p = {p_aud:.3f}")
    for tarefa, (medias, cats, ms, difs) in p343_ancora_no_comportamento().items():
        print(f"P343 {tarefa}: { {k: round(v, 3) for k, v in medias.items()} }; catastrofes { {k: round(v, 4) for k, v in cats.items()} }; "
              f"m final { {k: round(v, 2) for k, v in ms.items()} }")
        for v, (d, dp, tt) in difs.items():
            print(f"P343 {tarefa}: {v} - principal = {d:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    norm, cats, (d, dp, tt) = p344_ancora_no_bandido()
    print(f"P344 bandido: normalizado { {k: round(v, 3) for k, v in norm.items()} }; catastrofes { {k: round(v, 3) for k, v in cats.items()} }; "
          f"ancora - principal = {d:.3f}, dp = {dp:.3f}, t = {tt:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P349, testes=TESTES_P349)
    print(f"P349 minha taxa de erro ({ERROS_P349}/{TESTES_P349}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_29():
    print("--- Parte 29 (compor em vez de herdar; o pensamento com mais pesos; a bateria de equacoes) ---")
    for k, qa, qe, e, p in p352_bateria_wilson_hilferty():
        print(f"P352 B1 Wilson-Hilferty forma {k:5g}: aproximado = {qa:.4f}, exato = {qe:.4f}, erro = {e:+.4%}, acumula = {p:.4f}")
    for lam, ex, d2, d3, e2, e3 in p352_bateria_delta_inverso():
        print(f"P352 B2 E[1/X|X>=1] lambda {lam:5g}: exato = {ex:.5f}; 2a ordem = {d2:.5f} ({e2:+.2%}); 3a ordem = {d3:.5f} ({e3:+.2%})")
    k_lin, k_rico, linhas = p352_bateria_contas()
    print(f"P355 pesos: linear = {k_lin}, rico = {k_rico}")
    for nome, (n, ev, epv_l, epv_r, ak_l, ak_r, dak) in linhas.items():
        print(f"P355 {nome}: n = {n}, eventos = {ev:g}, EPV linear = {epv_l:.1f}, rico = {epv_r:.1f}; Akaike k/n: {ak_l:.5f}, {ak_r:.5f}, diferenca {dak:.5f}")
    for nome, (r, ev) in p353_pensamento_rico().items():
        print(f"P353 {nome} (eventos {ev:.1f}): " + "; ".join(f"{k}: treino {a:.5f}, teste {b:.5f}, otimismo {c:.5f}" for k, (a, b, c) in r.items()))
    for nome, (f, n) in p354_calibracao_rica().items():
        print(f"P354 {nome}: f do pensamento rico na decisao = {f:.3f} ({n} catastrofes)")
    for tarefa, (medias, cats, difs, rica) in p356_composta().items():
        print(f"P356 {tarefa}: { {k: round(v, 4) for k, v in medias.items()} }; catastrofes { {k: round(v, 4) for k, v in cats.items()} }")
        for v, (d, dp, tt) in difs.items():
            print(f"P356 {tarefa}: {v} - principal = {d:.4f}, dp = {dp:.4f}, t = {tt:.2f}")
        print(f"P356 {tarefa}: composta_rica - composta = {rica[0]:.4f}, dp = {rica[1]:.4f}, t = {rica[2]:.2f}")
    for nome, (tl, tr, n, al, ar, d) in p357_takeuchi().items():
        print(f"P357 {nome}: tr(J I^-1) linear = {tl:.3f}, rico = {tr:.3f}; por amostra {al:.5f}, {ar:.5f}; diferenca = {d:.5f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P359, testes=TESTES_P359)
    print(f"P359 minha taxa de erro ({ERROS_P359}/{TESTES_P359}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_30():
    print("--- Parte 30 (0x1E: a SYNTHAI em hexadecimal; o dicionario como data lake) ---")
    h1, h2, ok, h225, bases, ok2 = p361_hex_do_limiar()
    print(f"P361 P* = {h1}; 2P* = {h2}; exato = {ok}; 1/225 = 0x0.{h225}; 1/450 = 2^-9 x 256/225: {ok2}")
    print(f"P361 regra 1/(b-1)^2 (periodo b-1, sem o digito b-2) nas bases 3-16: {all(a and b for a, b in bases.values())}")
    for (nome, b), (prev, real, ex) in p362_conta_da_quantizacao().items():
        print(f"P362 {nome}, {b} bits por peso: erro no logit previsto (Delta^2/12) = {prev:.4f}, real = {real:.4f}; "
              f"pesos em hex = {ex[1]}, passo = {ex[2]:.4f}")
    for mundo in ("escolha única", "sequencial", "bandido"):
        medias, cats, efeitos = p363_fatorial_hex(mundo)
        print(f"P363 {mundo}: { {f'0x{c:X}': round(v, 4) for c, v in medias.items()} }")
        print(f"P363 {mundo} catastrofes: { {f'0x{c:X}': round(v, 4) for c, v in cats.items()} }")
        for nome, (m, dp, tt) in efeitos.items():
            print(f"P363 {mundo} efeito {nome}: {m:.4f}, dp = {dp:.4f}, t = {tt:.2f}")
    for mundo, (medias, cats, difs) in p364_quantizada().items():
        print(f"P364 {mundo}: { {f'{b} bits': round(v, 4) for b, v in medias.items()} }; catastrofes { {b: round(v, 4) for b, v in cats.items()} }")
        for b, (d, dp, tt) in difs.items():
            print(f"P364 {mundo}: {b} bits - completo = {d:.4f}, dp = {dp:.4f}, t = {tt:.2f}")
    exatos, sha = p365_impressoes_digitais()
    print(f"P365 exatos = {exatos}; SHA-256 da bateria = {sha}")
    (d, dp, tt), ca, cb, metade1, metade2 = p366_composta_60_sementes()
    print(f"P366 composta - principal (sequencial, 60 sementes) = {d:.4f}, dp = {dp:.4f}, t = {tt:.2f}; catastrofes {ca:.4f} / {cb:.4f}; "
          f"metades: {metade1[0]:.4f} (t {metade1[2]:.2f}), {metade2[0]:.4f} (t {metade2[2]:.2f})")
    r = p371_dicionario()
    for k, v in r.items():
        print(f"P371 {k} = {v}")
    n, hx, maior, valor, hex_palavra, hex_letra = p372_hex_do_dicionario()
    print(f"P372 hexspeak = {n} palavras; maior = {maior} = 0x{maior.upper()} = {valor}; uma palavra = {hex_palavra:.4f} digitos hex; "
          f"uma letra = {hex_letra:.4f} digito hex")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P369, testes=TESTES_P369)
    print(f"P379 minha taxa de erro ({ERROS_P369}/{TESTES_P369}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_31():
    print("--- Parte 31 (0x1F: o curriculo do dicionario e a avalanche; o hipercubo, Gray e os ULPs) ---")
    n, ms, tabela = p381_curriculo()
    print(f"P381 palavras = {n}; MinSet guloso = {ms}")
    for (nome, k, th), v in tabela.items():
        print(f"P381 curriculo {nome}, k = {k}, theta = {th}: cobertura = {v:.4f}")
    print(f"P382 MinSet guloso, reduzido, cobertura do fecho, rodadas = {p382_minset_reduzido()}")
    s_z, n_f, cob = p383_cobertura_zipf()
    print(f"P383 Zipf s = {s_z:.4f}, palavras distintas nas definicoes = {n_f}")
    for k, (med, conta) in cob.items():
        print(f"P383 k = {k}: cobertura medida = {med:.4f}, conta de Zipf = {conta:.4f}")
    rho, wp, lk, frac = p384_wu_palmer_lesk()
    print(f"P384 Spearman(Wu-Palmer, Lesk) = {rho:.4f}; media Wu-Palmer = {wp:.4f}; media Lesk = {lk:.5f}; pares com Lesk > 0 = {frac:.4f}")
    for th, (k, antes, depois) in p385_ponto_critico().items():
        print(f"P385 theta = {th}: k critico = {k}; cobertura com k-1 = {antes:.4f}, com k = {depois:.4f}")
    for mundo, (rho, por_h) in p391_geometria_hamming().items():
        print(f"P391 {mundo}: Spearman(Hamming, |dif|) = {rho:.3f}; |dif| medio por distancia = { {h: round(v, 4) for h, v in por_h.items()} }")
    ordem, sub = p392_gray_e_subida()
    print(f"P392 Gray = {' '.join(ordem)}")
    for mundo, v in sub.items():
        print(f"P392 {mundo}: caminho, melhor, chegou = {v}")
    res, a, b = p393_ulps()
    for k, (med, conta) in res.items():
        print(f"P393 n = {k}: erro medio = {med:.2f} ulps; conta linear = {conta:.2f}")
    print(f"P393 0.1 + 0.2 = {a}; 0.3 = {b}")
    for k, (med, deg, lin) in p394_ulps_em_degrau().items():
        print(f"P394 n = {k}: erro medio = {med:.3f} ulps; conta em degrau = {deg:.3f}; conta linear = {lin:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P399, testes=TESTES_P399)
    print(f"P399 minha taxa de erro ({ERROS_P399}/{TESTES_P399}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_32():
    print("--- Parte 32 (0x20: a decisao bayesiana exata no lugar do RL e do aprendizado continuo; autopoiese; avalanche) ---")
    lr, expl, expl_esp = p401_contas()
    print(f"P401 conta: Lai-Robbins medio = {lr:.2f}; exploracao do eps-guloso = {expl:.2f} (esperanca {expl_esp:.2f})")
    medias, difs = p401_bandido()
    print(f"P401 arrependimento final (T 2000, 100 sementes): { {k: round(v, 2) for k, v in medias.items()} }")
    for k, (d, dp, tt) in difs.items():
        print(f"P401 {k} - thompson = {d:.2f}, dp = {dp:.2f}, t = {tt:.2f}")
    g, otimo, esquerda, q_conta = p402_contas()
    print(f"P402 conta: g* = {g:.4f}; otimo em 5000 passos = {otimo:.1f}; so a esquerda = {esquerda:.1f}; Q eps preso = {q_conta:.2f}")
    medias, difs = p402_riverswim()
    print(f"P402 recompensa total (20 sementes): { {k: round(v, 2) for k, v in medias.items()} }")
    for k, (d, dp, tt) in difs.items():
        print(f"P402 psrl - {k} = {d:.2f}, dp = {dp:.2f}, t = {tt:.2f}")
    med, (d, dp, tt), dif = p403_continuo()
    for k, (a, b) in med.items():
        print(f"P403 {k}: erro em A depois de A = {a:.6f}, depois de B = {b:.6f} (razao {b / a:.2f})")
    print(f"P403 sgd - bayes depois de B = {d:.4f}, dp = {dp:.4f}, t = {tt:.2f}; recursiva - lote, maior diferenca = {dif:.2e}")
    print(f"P404 conta (theta 1, uma rodada): { {q: round(v, 4) for q, v in p404_contas().items()} }")
    ker, fech, res = p404_autopoiese()
    print(f"P404 nucleo = {ker} palavras; fechamento = {fech}")
    for (q, th), v in res.items():
        print(f"P404 esquecer {q:.0%}, theta = {th}: regenera = {v:.4f}")
    pri, seg_ts, seg_q, (d, dp, tt) = p405_dano()
    print(f"P405 thompson 1a metade = {pri:.2f}; 2a metade (danificado) = {seg_ts:.2f}; Q eps 2a metade = {seg_q:.2f}; "
          f"Q - thompson = {d:.2f}, dp = {dp:.2f}, t = {tt:.2f}")
    print(f"P411 conta: { {k: round(v, 2) for k, v in p411_contas().items()} }")
    med, difs = p411_memoria_hex()
    print(f"P411 arrependimento: { {('completo' if k is None else k): round(v, 2) for k, v in med.items()} }")
    for k, (d, dp, tt) in difs.items():
        print(f"P411 teto {k} - completo = {d:.2f}, dp = {dp:.2f}, t = {tt:.2f}")
    for (nome, th), (k, palavra, salto, meio) in p421_avalanche().items():
        print(f"P421 {nome}, theta = {th}: maior salto em k = {k} ({palavra}) = {salto:.4f}; k de 50% = {meio}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P429, testes=TESTES_P429)
    print(f"P429 minha taxa de erro ({ERROS_P429}/{TESTES_P429}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_33():
    print("--- Parte 33 (0x21: a arquitetura pos-ASI numa CPU so, auditada) ---")
    land, t_texto = p431_landauer()
    print(f"P431 Landauer (J/bit): { {t: f'{e:.4e}' for t, e in land.items()} }; o 2,75e-21 do texto seria a {t_texto:.2f} K")
    b, ml, razao = p432_bremermann()
    print(f"P432 Bremermann mc^2/h = {b:.4e} /s/kg; Margolus-Levitin 2E/(pi hbar) = {ml:.4e}; razao = {razao}")
    taxa, b1g, dist = p433_cpu()
    print(f"P433 laco Python = {taxa:.3e} adicoes/s; Bremermann de 1 g = {b1g:.3e}; log10 da distancia = {dist:.2f} "
          f"(medido com outras simulacoes rodando: a taxa varia de execucao para execucao)")
    print(f"P434 AIXI(t,l), t = 1000, anos a essa taxa: { {l: f'{a:.3e}' for l, a in p434_aixi_tl(taxa).items()} }")
    print(f"P435 auditoria estatica: {p435_auditoria()}")
    print(f"P435 a arquitetura original rodada num processo separado (estados, geracao maxima, notas): {p435_rodar_original()}")
    print(f"P436 conta: chance de campeao inflado = {p436_contas():.4f}")
    for k, (f, real) in p436_recompensa().items():
        print(f"P436 {k}: campeoes inflados = {f:.3f}; arrependimento real do campeao = {real:.2f}")
    med, (d, dp, tt), thompson, melhor = p437_l3_l4()
    print(f"P437 arrependimento real do campeao: L3 = {med['L3']:.2f}, L4 = {med['L4']:.2f}; L4 - L3 = {d:.2f}, dp = {dp:.2f}, "
          f"t = {tt:.2f}; melhor campeao = {melhor:.2f}; Thompson sem evolucao = {thompson:.2f}")
    sigma, cotas = p438_contas()
    print(f"P438 conta: sigma da nota = {sigma:.2f}; sigma*sqrt(2 ln N) = { {n: round(v, 1) for n, v in cotas.items()} }")
    for regra, (infl, aceitos) in p438_maldicao().items():
        print(f"P438 regra {regra}: inflacao da nota guardada = {infl:.2f}; filhos aceitos = {aceitos:.2f}")
    print(f"P439 conta: { {g: (round(a, 1), round(b, 1)) for g, (a, b) in p439_contas().items()} }")
    for g, (sem, com, custo, total) in p439_renovacao().items():
        print(f"P439 gama = {g}: 2a metade sem dano = {sem:.2f}, com dano = {com:.2f}, custo do dano = {custo:.2f}; total sem dano = {total:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P459, testes=TESTES_P459)
    print(f"P459 minha taxa de erro ({ERROS_P459}/{TESTES_P459}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_34():
    print("--- Parte 34 (0x22: as promessas testadas em casos novos) ---")
    for a in (0.1, 0.05):
        c1, c2 = p461_contas(a)
        print(f"P461 conta, alfa = {a}: cota sem aprisionamento = {c1:.2f}; cota com aprisionamento = {c2:.2f}")
    print(f"P461 Q eps com alfa = 0,05: arrependimento = {p461_q_alfa():.2f}")
    print(f"P462 conta (quebras, gama de Garivier-Moulines, memoria): {p462_contas()}")
    print(f"P462 bandido que muda a cada 500 passos: { {g: round(v, 2) for g, v in p462_mudanca().items()} }")
    (s_m, q_m), tab = p463_zipf_mandelbrot()
    print(f"P463 Zipf-Mandelbrot ajustado nos substantivos: s = {s_m:.2f}, q = {q_m}")
    for k, (prev, puro, med) in tab.items():
        print(f"P463 verbos, k = {k}: previsto = {prev:.4f}; Zipf puro = {puro:.4f}; medido = {med:.4f}")
    na, nb, nt, res = p464_dicionario_no_lugar_do_ml()
    print(f"P464 tarefa A = {na}, tarefa B = {nb}, teste de A = {nt}")
    for nome, (a, b) in res.items():
        print(f"P464 {nome}: acuracia em A depois de A = {a:.4f}; depois de B = {b:.4f}")
    print(f"P465 conta: Thompson com Morris = {p465_contas():.2f}")
    m, (d, dp, tt) = p465_morris()
    print(f"P465 Thompson com Morris = {m:.2f}; Morris - completo = {d:.2f}, dp = {dp:.2f}, t = {tt:.2f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P489, testes=TESTES_P489)
    print(f"P489 minha taxa de erro ({ERROS_P489}/{TESTES_P489}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_35():
    print("--- Parte 35 (0x23: renovacao dirigida pela surpresa; Naive Bayes com pares; float16) ---")
    print(f"P491 conta: alarmes (checagens) falsos por rodada no melhor braco = {p491_contas():.2f}")
    est, custo, muda, ren = p491_surpresa()
    print(f"P491 surpresa: estacionario = {est:.2f}; custo do dano = {custo:.2f}; mundo que muda = {muda:.2f}; renovacoes no estacionario = {ren:.2f}")
    a, b = p492_nb_bigramas()
    print(f"P492 Naive Bayes com pares: acuracia em A depois de A = {a:.4f}; depois de B = {b:.4f}")
    risco, mudou, u = p493_float16()
    print(f"P493 float16: fracao em risco (margem < ulp16) = {risco:.5f}; fracao que mudou = {mudou:.5f}; ulp16 mediano = {u}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P519, testes=TESTES_P519)
    print(f"P519 minha taxa de erro ({ERROS_P519}/{TESTES_P519}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_36():
    print("--- Parte 36 (0x24: a exposicao; a lei do significado; Gray contra binario) ---")
    c, prev = p521_contas()
    print(f"P521 conta: custo da exposicao = {c:.2f}; estacionario previsto = {prev:.2f}")
    est, custo, muda = p521_exposta()
    print(f"P521 surpresa com exposicao: estacionario = {est:.2f}; custo do dano = {custo:.2f}; mundo que muda = {muda:.2f}")
    d1, d2, n = p522_lei_do_significado()
    print(f"P522 lei do significado: delta por palavra = {d1:.4f}; delta por faixa de 100 postos = {d2:.4f}; palavras = {n}")
    a, b = p523_contas()
    print(f"P523 conta: atravessar o penhasco por passo: binario = {a:.3e}; Gray = {b:.4f}")
    for (cod, com), (f, q) in p523_gray_binario().items():
        print(f"P523 {cod}, comeco {com}: chegou ao otimo = {f:.2f}; avaliacoes medias = {q}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P549, testes=TESTES_P549)
    print(f"P549 minha taxa de erro ({ERROS_P549}/{TESTES_P549}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_37():
    print("--- Parte 37 (0x25: deteccao bayesiana de mudanca; a lei da abreviacao; um digito hex de hipoteses) ---")
    c, prev = p531_contas()
    print(f"P531 conta: custo da exposicao natural (H = 1/500) = {c:.2f}; estacionario previsto = {prev:.2f}")
    est, custo, muda = p531_bocpd()
    print(f"P531 Thompson + BOCPD: estacionario = {est:.2f}; custo do dano = {custo:.2f}; mundo que muda = {muda:.2f}")
    a, b, (d, dp, tt) = p532_hipoteses_hex()
    print(f"P532 mundo que muda: 16 hipoteses = {a:.2f}; 256 = {b:.2f}; 16 - 256 = {d:.2f}, dp = {dp:.2f}, t = {tt:.2f}")
    rho, top, resto, n = p533_abreviacao()
    print(f"P533 abreviacao: Spearman(comprimento, frequencia) = {rho:.4f}; comprimento medio das 1000 mais frequentes = {top:.3f}, "
          f"das outras = {resto:.3f}; palavras = {n}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P579, testes=TESTES_P579)
    print(f"P579 minha taxa de erro ({ERROS_P579}/{TESTES_P579}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_38():
    print("--- Parte 38 (0x26: media bayesiana de modelos sobre o risco; o zero do produto; Heaps) ---")
    est, custo, muda, pe, pm = p541_mistura()
    print(f"P541 mistura: estacionario = {est:.2f}; custo do dano = {custo:.2f}; mundo que muda = {muda:.2f}")
    print(f"P541 pesos finais medios (H = 0, 1/2000, 1/500, 1/100): estavel = {[round(x, 4) for x in pe]}; muda = {[f'{x:.3e}' for x in pm]}")
    p, h2, passo = p542_contas()
    print(f"P542 conta: p* = {p:.4f}; H2(p*) = {h2:.4f} bits/passo; zero previsto no passo {passo:.0f}")
    zero, sub, bits = p542_underflow()
    print(f"P542 medido: subnormal no passo {sub}; 0,0 no passo {zero}; {bits:.4f} bits/passo; 1075/bits = {1075 / bits:.0f}")
    beta, i1, i2, total, v = p543_heaps()
    print(f"P543 Heaps: beta = {beta:.4f}; 1/s = {i1:.4f} (P463) ou {i2:.4f} (P383); palavras lidas = {total}; vocabulario = {v}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P609, testes=TESTES_P609)
    print(f"P609 minha taxa de erro ({ERROS_P609}/{TESTES_P609}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_39():
    print("--- Parte 39 (0x27: a arquitetura neuro-simbolica testada; o portugues no data lake; compressao) ---")
    ntr, nte, cob = p551_contas()
    print(f"P551 conta: treino = {ntr}, teste = {nte}; animais do teste cobertos pelas 6 subclasses = {cob:.4f}")
    for logica in ("lukasiewicz", "produto"):
        for k, (acc, rev, esp) in p551_ltn(logica).items():
            print(f"P551 {logica} {k}: acuracia = {acc:.4f}; revocacao = {rev:.4f}; especificidade = {esp:.4f}")
    for k, (n, bpc, h0, rl, rz) in p552_compressao().items():
        print(f"P552 {k}: {n} bytes; lzma = {bpc:.4f} bits/byte; entropia de ordem 0 = {h0:.4f}; razao lzma = {rl:.4f}; razao zlib = {rz:.4f}")
    rho, razao, n, cob = p553_bilingue()
    print(f"P553 Spearman(comprimento pt, comprimento en) = {rho:.4f}; razao pt/en = {razao:.4f}; pares = {n}; cobertura = { {k: round(v, 4) for k, v in cob.items()} }")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P639, testes=TESTES_P639)
    print(f"P639 minha taxa de erro ({ERROS_P639}/{TESTES_P639}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_40():
    print("--- Parte 40 (0x28: o portugues se define em portugues?; seguir o modelo de maior peso; acentos em UTF-8) ---")
    voc, ndef, nf, ex, pl, ker, fk, fk_en = p641_portugues()
    print(f"P641 lemas de uma palavra = {voc}; com glosa = {ndef} ({ndef / voc:.4f}); palavras de conteudo nas glosas = {nf}")
    print(f"P641 fracao que e lema: exata = {ex:.4f}, com plurais = {pl:.4f}; nucleo = {ker} ({fk:.4f}); nucleo no ingles = {fk_en:.4f}")
    for (k, th), v in p642_fecho_pt().items():
        print(f"P642 fecho em portugues, {k} ancoras, theta = {th}: {v:.4f} dos lemas definidos")
    est, custo, muda = p643_maximo()
    print(f"P643 seguir o maior peso: estacionario = {est:.2f}; custo do dano = {custo:.2f}; mundo que muda = {muda:.2f}")
    print(f"P644 conta: bytes por caractere = { {k: round(v, 5) for k, v in p644_contas().items()} }")
    pt, en, top = p644_utf8()
    print(f"P644 medido: portugues = {pt:.5f}; ingles = {en:.5f}; mais comuns = {top}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P669, testes=TESTES_P669)
    print(f"P669 minha taxa de erro ({ERROS_P669}/{TESTES_P669}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_41():
    print("--- Parte 41 (0x29: engenharia reversa de mim mesma) ---")
    tipos, partes = p671_erros_por_tipo()
    for t, (e, n, (m, lo, hi)) in tipos.items():
        print(f"P671 tipo {t}: {e} erros em {n}; taxa a posteriori = {m:.3f}, intervalo 90% = [{lo:.3f}, {hi:.3f}]")
    print(f"P671 erros por parte: {partes}")
    top, raz, nfr, abre, sims, rho = p672_meus_padroes()
    for g, nd, nt in top:
        print(f"P672 4-grama '{g}': em {nd} documentos, {nt} vezes")
    print(f"P672 razao lzma dos meus textos = {raz:.4f}; frases = {nfr}; aberturas = {abre}")
    print(f"P672 cosseno entre partes vizinhas = {[round(x, 4) for x in sims]}; Spearman com o numero da parte = {rho:.4f}")
    s_z, beta, n, v = p673_minhas_leis()
    print(f"P673 Zipf das minhas palavras = {s_z:.4f}; Heaps beta = {beta:.4f}; palavras = {n}; vocabulario = {v}")
    vozes, proprias = p674_as_duas_vozes()
    for voz, (nf, pf) in vozes.items():
        print(f"P674 {voz}: {nf} falas, {pf:.2f} palavras por fala; palavras proprias = {proprias[voz]}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P699, testes=TESTES_P699)
    print(f"P699 minha taxa de erro ({ERROS_P699}/{TESTES_P699}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_42():
    print("--- Parte 42 (0x2A: a premissa e o significante, a resposta e o significado) ---")
    faixas = {"thompson_estavel": (30.7, 0.172), "surpresa_estavel": (43.1, 0.172), "exposta_dano": (19.5, 0.344),
              "bocpd_muda": (371.9, 0.172), "maximo_estavel": (34.5, 0.172), "maximo_dano": (60.9, 0.344),
              "q_eps_estavel": (185.4, 0.172), "morris_estavel": (76.9, 0.172)}
    for k, v in p701_replicacao().items():
        c, w = faixas[k]
        print(f"P701 {k}: sementes novas = {v:.2f}; faixa = [{c * (1 - w):.1f}; {c * (1 + w):.1f}]; dentro = {c * (1 - w) <= v <= c * (1 + w)}; "
              f"desvio relativo = {(v - c) / c:+.3f}")
    res, m_en, m_pt = p702_arbitrariedade()
    for k, (acc, n, base) in res.items():
        print(f"P702 {k}: acuracia = {acc:.4f} em {n} exemplos (fracao de animais = {base:.4f})")
    print(f"P702 indice de motivacao: ingles = {m_en:.4f}; portugues = {m_pt:.4f}")
    red, ret, n, mais = p703_premissa_resposta()
    print(f"P703 {n} perguntas: redundancia media da resposta com a premissa = {red:.4f}; retorno medio da premissa = {ret:.4f}; "
          f"mais redundantes = {mais}")
    print(f"P704 conta: o arquivo binario tem {p704_contas()} bytes")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P729, testes=TESTES_P729)
    print(f"P729 minha taxa de erro ({ERROS_P729}/{TESTES_P729}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_43():
    print("--- Parte 43 (0x2B: a regra das faixas em mecanismos novos; os trigramas; o dialogo responde?) ---")
    centros = p731_contas()
    larg = {"exposta100_estavel": 0.172, "exposta100_dano": 0.344, "surpresa40_estavel": 0.172, "surpresa40_muda": 0.258,
            "bocpd2000_muda": 0.258, "jeffreys_estavel": 0.172}
    for k, v in p731_mecanismos_novos().items():
        c = centros[k]
        print(f"P731 {k}: centro deduzido = {c:.2f}; medido = {v:.2f}; desvio = {(v - c) / c:+.3f}; "
              f"dentro de [{c * (1 - larg[k]):.1f}; {c * (1 + larg[k]):.1f}] = {c * (1 - larg[k]) <= v <= c * (1 + larg[k])}")
    an, ou, dae, ae, v = p732_trigramas()
    print(f"P732 trigramas = {v}; mais animais = {an}; menos animais = {ou}; dae = {dae:.4f}; ae$ = {ae:.4f}")
    ret, red, n = p733_dialogo_responde()
    print(f"P733 {n} pares (pergunta, rodada seguinte): retorno medio = {ret:.4f}; redundancia media = {red:.4f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P759, testes=TESTES_P759)
    print(f"P759 minha taxa de erro ({ERROS_P759}/{TESTES_P759}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_44():
    print("--- Parte 44 (0x2C: o modelo no nivel certo; os grupos do dicionario; a curva de erro) ---")
    centros = p761_contas()
    larg = {"global_muda": 0.258, "global_estavel": 0.172, "global_dano": 0.344}
    for k, v in p761_global().items():
        c = centros[k]
        print(f"P761 {k}: centro = {c:.2f}; medido = {v:.2f}; desvio = {(v - c) / c:+.3f}; dentro = {c * (1 - larg[k]) <= v <= c * (1 + larg[k])}")
    taxas, incl = p762_curva_de_erro()
    print(f"P762 taxa de erro por parte = {taxas}; inclinacao = {incl:+.4f} por parte")
    n, g, t = p763_grupos()
    print(f"P763 substantivos = {n}; nomeiam grupos = {g:.4f}; grupos taxonomicos = {t:.4f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P789, testes=TESTES_P789)
    print(f"P789 minha taxa de erro ({ERROS_P789}/{TESTES_P789}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_45():
    print("--- Parte 45 (0x2D: decidir pela hipotese mais pesada; a calibracao das minhas faixas; a profundidade) ---")
    media, dp, t, fora, n = p792_calibracao()
    print(f"P792 calibracao das {n} faixas de comportamento: media de z = {media:+.3f} (t = {t:.2f}); desvio de z = {dp:.3f}; fora de 1,645 = {fora}")
    centros = p791_contas()
    larg = {"map_estavel": 0.172, "map_muda": 0.258, "map_dano": 0.344}
    for k, v in p791_map().items():
        c = centros[k]
        print(f"P791 {k}: centro = {c:.2f}; medido = {v:.2f}; desvio = {(v - c) / c:+.3f}; dentro = {c * (1 - larg[k]) <= v <= c * (1 + larg[k])}")
    for k, (m, n) in p793_profundidade().items():
        print(f"P793 profundidade media de {k} = {m:.3f} ({n} substantivos)")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P819, testes=TESTES_P819)
    print(f"P819 minha taxa de erro ({ERROS_P819}/{TESTES_P819}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_46():
    print("--- Parte 46 (0x2E: a resposta e a pergunta e a pergunta e a resposta; refazer tudo desde o comeco) ---")
    rr, rp, n = p821_inversao()
    print(f"P821 {n} perguntas: redundancia da resposta dada a pergunta = {rr:.4f}; da pergunta dada a resposta = {rp:.4f}")
    pr, sg, n = p822_dialogo_invertido()
    print(f"P822 {n} perguntas do dialogo: contida na rodada que a gerou = {pr:.4f}; na rodada seguinte = {sg:.4f}")
    ac, n, erradas = p824_reconstrucao()
    print(f"P824 reconstruir a parte pelos numeros: {ac} de {n} acertos (erradas: {erradas}); ao acaso P(>= {ac}) = "
          f"{p825_cauda_binomial(n, 1 / n, ac):.2e}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P849, testes=TESTES_P849)
    print(f"P849 minha taxa de erro ({ERROS_P849}/{TESTES_P849}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def p856_acaso_851(semente=851, d=None):
    """O acaso da P851: a mesma pergunta (a definição cita o lema de outro sinset?) trocando o hiperônimo por um
    substantivo sorteado (semente fixa). Devolve (fração direta ao acaso, fração inversa ao acaso)."""
    import re
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    rng = random.Random(semente)
    nomes = [i for i, x in enumerate(d.sinsets) if x[0] == "n"]

    def contem(definicao, lemas):
        return any(re.search(r"(?<![a-z])" + re.escape(x.replace("_", " ").lower()) + r"(?:e?s)?(?![a-z])", definicao)
                   for x in lemas)

    direto = inverso = n = 0
    for pos, lemas, hiper, glosa in d.sinsets:
        if pos != "n" or not [h for h in hiper if h in d.indice]:
            continue
        k = rng.choice(nomes)
        n += 1
        direto += contem(d.definicao(glosa).lower(), d.sinsets[k][1])
        inverso += contem(d.definicao(d.sinsets[k][3]).lower(), lemas)
    return direto / n, inverso / n

ERROS_P909, TESTES_P909 = 146, 411


def p881_epoca():
    """Rodada 20 (P881): o Naive Bayes da Parte 34 reconhece a época (Partes 1-20 ou 21-41) de cada seção do
    resultados.txt, deixando uma de fora (dialogo/rodada20.py, conferido em Java). Devolve (acertos, seções, as erradas,
    acertos do preditor da maioria deixando um de fora)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada20", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada20.py"))
    r20 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r20)
    ds = r20.dados()
    res = r20.deixar_um_de_fora(ds)
    maioria = 0
    for i, (_, ep, _) in enumerate(ds):
        resto = [e for j, (_, e, _) in enumerate(ds) if j != i]
        maioria += ep == max(sorted(set(resto)), key=resto.count)  # empate: a época menor, como no prever
    return sum(ep == pv for _, ep, pv, _ in res), len(res), [n for n, ep, pv, _ in res if ep != pv], maioria


def _mapa_da_definicao(d):
    """O mapa da P882: cada substantivo de uma palavra só -> o primeiro substantivo de uma palavra só da definição do seu
    primeiro sentido de substantivo (que não seja ele mesmo), ou None."""
    nomes = {w for w, idx in d.lemas.items() if w.isalpha() and any(d.sinsets[i][0] == "n" for i in idx)}
    f = {}
    for w in sorted(nomes):
        i = next(i for i in d.lemas[w] if d.sinsets[i][0] == "n")
        f[w] = next((x for x in d.palavras_da_definicao(d.sinsets[i][3]) if x in nomes and x != w), None)
    return f


def p882_mapa_da_definicao(d=None):
    """O mapa da definição (P882): cada substantivo de uma palavra só vai para a primeira palavra da definição do seu
    primeiro sentido de substantivo que também é um substantivo de uma palavra só (e não ela mesma); sem essa palavra, é
    um sumidouro. Devolve (N, sumidouros, pontos cíclicos, ciclos, cauda média até um ciclo ou sumidouro, fração da maior
    bacia, o ciclo da maior bacia)."""
    from synthai.dicionario import Dicionario
    f = _mapa_da_definicao(d or Dicionario())
    # destino de cada palavra: o sumidouro ou o ciclo em que a órbita termina, e a distância até ele
    destino, dist, ciclicos, ciclos = {}, {}, set(), []
    for w in sorted(f):
        caminho, pos = [], {}
        x = w
        while x is not None and x not in destino and x not in pos:
            pos[x] = len(caminho)
            caminho.append(x)
            x = f[x]
        if x is None:  # o último do caminho é um sumidouro
            alvo, base = ("sumidouro", caminho[-1]), len(caminho) - 1
            for k, y in enumerate(caminho):
                destino[y], dist[y] = alvo, base - k
        elif x in destino:
            for k, y in enumerate(caminho):
                destino[y], dist[y] = destino[x], dist[x] + len(caminho) - k
        else:  # um ciclo novo, a partir de pos[x]
            ciclo = caminho[pos[x]:]
            alvo = ("ciclo", min(ciclo))
            ciclos.append(sorted(ciclo))
            for y in ciclo:
                destino[y], dist[y] = alvo, 0
                ciclicos.add(y)
            for k, y in enumerate(caminho[:pos[x]]):
                destino[y], dist[y] = alvo, pos[x] - k
    bacias = {}
    for w in f:
        bacias[destino[w]] = bacias.get(destino[w], 0) + 1
    maior = max(sorted(bacias), key=bacias.get)
    sumid = sum(1 for w in f if f[w] is None)
    ciclo_maior = next((c for c in ciclos if ("ciclo", c[0]) == maior), [maior[1]])
    return (len(f), sumid, len(ciclicos), len(ciclos), sum(dist.values()) / len(dist), bacias[maior] / len(f),
            ciclo_maior)


def p883_felizes_hex(ate=4095, base=16):
    """Números felizes numa base (P883): s(n) = soma dos quadrados dos dígitos. Devolve (fração de felizes em 1..ate,
    os ciclos diferentes do ponto fixo 1, cada um começando pelo menor)."""
    def s(n):
        t = 0
        while n:
            n, r = divmod(n, base)
            t += r * r
        return t
    felizes, ciclos = 0, set()
    for n in range(1, ate + 1):
        vistos = []
        x = n
        while x not in vistos:
            vistos.append(x)
            x = s(x)
        ciclo = vistos[vistos.index(x):]
        if ciclo == [1]:
            felizes += 1
        else:
            k = ciclo.index(min(ciclo))
            ciclos.add(tuple(ciclo[k:] + ciclo[:k]))
    return felizes / ate, sorted(ciclos)


def p884_ciclo_da_serie(alvos=(41, 40, 39, 38)):
    """Rodada 21 (P884): a semelhança idf entre as seções do resultados.txt (dialogo/rodada21.py, conferido em Java).
    Devolve (média a distância 1, média a distância 20, {parte: índice do ciclo = média com 1-10 / média com 11-30})."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada21", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada21.py"))
    r21 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r21)
    cs = r21.conjuntos()
    sim = r21.semelhancas(cs)
    pos = {n: i for i, (n, _) in enumerate(cs)}
    ind = {}
    for a in alvos:
        c = [sim[pos[a]][pos[k]] for k in range(1, 11) if k in pos]
        m = [sim[pos[a]][pos[k]] for k in range(11, 31) if k in pos and k != a]
        ind[a] = (sum(c) / len(c)) / (sum(m) / len(m))
    return r21.media_distancia(sim, 1), r21.media_distancia(sim, 20), ind


ERROS_P939, TESTES_P939 = 148, 420


def p912_funis(d=None):
    """Os funis do mapa da definição (P912): o grau de entrada de cada palavra (quantas a escolhem). Devolve (a mais
    escolhida, o seu grau, a fração das palavras que escolhem uma das 10 mais escolhidas, a inclinação de log(número de
    palavras com grau k) contra log k para k de 2 a 100, as 10 mais escolhidas)."""
    from synthai.dicionario import Dicionario
    f = _mapa_da_definicao(d or Dicionario())
    grau = {}
    for x in f.values():
        if x is not None:
            grau[x] = grau.get(x, 0) + 1
    top = sorted(grau, key=lambda w: (-grau[w], w))[:10]
    hist = {}
    for g in grau.values():
        hist[g] = hist.get(g, 0) + 1
    pts = [(log(k), log(hist[k])) for k in range(2, 101) if k in hist]
    incl = float("nan")
    if len(pts) >= 2:
        mx = sum(x for x, _ in pts) / len(pts)
        my = sum(y for _, y in pts) / len(pts)
        incl = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    return top[0], grau[top[0]], sum(grau[w] for w in top) / len(f), incl, [(w, grau[w]) for w in top]


def p913_benford_hex(caminho=None):
    """Benford em base 16 nos números do resultados.txt (P913): o primeiro dígito hexadecimal de cada número positivo
    (sem os rótulos Pnnn), escalado para [1, 16). Devolve (fração com dígito 1, fração com dígito 8..F, números, as 15
    frações)."""
    import os
    import re
    caminho = caminho or os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados.txt")
    texto = re.sub(r"P[0-9]+", " ", open(caminho, encoding="utf-8").read())
    cont = [0] * 16
    for x in re.findall(r"(?<![0-9.])[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?", texto):
        v = float(x)
        if v <= 0:
            continue
        while v >= 16:
            v /= 16
        while v < 1:
            v *= 16
        cont[int(v)] += 1
    n = sum(cont)
    return cont[1] / n, sum(cont[8:]) / n, n, [c / n for c in cont[1:]]


def p911_deriva(sementes=(911, 1, 2, 3, 4, 5)):
    """Rodada 22 (P911): a forma da deriva (dialogo/rodada22.py, conferido em Java). Devolve (tau da exponencial, resíduo,
    alfa da potência, resíduo, [alfa com as seções embaralhadas, uma por semente])."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada22", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada22.py"))
    r22 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r22)
    cs = r22.r21.conjuntos()
    _, _, tau, se, _, alfa, sp = r22.deriva(cs)
    controle = []
    for sem in sementes:
        c2 = cs[:]
        random.Random(sem).shuffle(c2)
        controle.append(r22.deriva(c2)[5])
    return tau, se, alfa, sp, controle


ERROS_P969, TESTES_P969 = 152, 433


def p942_definicoes_mutuas(d=None):
    """Pares de palavras que se definem uma pela outra (P942), no grafo de definições. Devolve (N, M arestas, pares
    mútuos, pares esperados ao acaso M·(M/N²)/2, fração das palavras em pelo menos um par, 5 exemplos)."""
    from synthai.dicionario import Dicionario
    g = (d or Dicionario()).grafo_de_definicoes()
    n = len(g)
    m = sum(len(v) for v in g.values())
    pares, em_par = [], set()
    for u in sorted(g):
        for v in sorted(g[u]):
            if u < v and u in g.get(v, ()):
                pares.append((u, v))
                em_par.update((u, v))
    esperado = m * (m / n ** 2) / 2
    return n, m, len(pares), esperado, len(em_par) / n, pares[:5]


def p943_periodo_hex(ate=10000):
    """O período de 1/p em base 16 (P943): a ordem de 16 módulo p, para os primos ímpares até `ate`. Devolve (a média de
    ord_p(16)/(p − 1), a média de ord_p(2)/(p − 1), a média de 1/mdc(ord_p(2), 4), primos)."""
    crivo = [True] * (ate + 1)
    crivo[0] = crivo[1] = False
    for i in range(2, int(ate ** 0.5) + 1):
        if crivo[i]:
            crivo[i * i::i] = [False] * len(crivo[i * i::i])
    r16 = r2 = rg = 0.0
    ps = [p for p in range(3, ate + 1) if crivo[p]]
    for p in ps:
        o, x = 1, 2 % p
        while x != 1:
            x = x * 2 % p
            o += 1
        g = 1 if o % 2 else (2 if o % 4 else 4)
        r2 += o / (p - 1)
        r16 += (o // g) / (p - 1)
        rg += 1 / g
    k = len(ps)
    return r16 / k, r2 / k, rg / k, k


def p941_curvas_individuais():
    """Rodada 23 (P941): as curvas individuais (dialogo/rodada23.py, conferido em Java) e o teste da mistura de Anderson e
    Tweney. Devolve (curvas em que a potência ganha, curvas, (resíduo exp, resíduo pot) da média das exponenciais
    ajustadas, (resíduo exp, resíduo pot) da média crua das mesmas 21 partes, alfa da mistura)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada23", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada23.py"))
    r23 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r23)
    cs = r23.r21.conjuntos()
    cv = r23.curvas(cs)
    sim = r23.r21.semelhancas(cs)
    k = len(cv)
    ajustes = []
    for i in range(k):
        ls = [L for L in range(1, 21) if sim[i][i + L] > 0]
        a, m, _ = r23.r22.reta([float(L) for L in ls], [log(sim[i][i + L]) for L in ls])
        ajustes.append((a, m))
    xe, xp = [float(L) for L in range(1, 21)], [log(L) for L in range(1, 21)]
    mist = [log(sum(exp(a + m * L) for a, m in ajustes) / k) for L in range(1, 21)]
    crua = [log(sum(sim[i][i + L] for i in range(k)) / k) for L in range(1, 21)]
    _, _, me = r23.r22.reta(xe, mist)
    _, malfa, mp = r23.r22.reta(xp, mist)
    _, _, ce = r23.r22.reta(xe, crua)
    _, _, cp = r23.r22.reta(xp, crua)
    return sum(1 for c in cv if c[5] < c[3]), k, (me, mp), (ce, cp), -malfa


def p947_o_texto_voltou(texto="externos/pos_asi_texto_parte50.md", guardado="externos/arquitetura_pos_asi.py"):
    """O texto da Parte 33 voltou (P947). Nada do texto é executado. Devolve (o código do texto é idêntico ao guardado,
    linha a linha sem espaços no fim; a auditoria estática da Parte 33 refeita no código novo; {parte: redundância do
    texto dado o documento da parte} para as Partes 31-49)."""
    import os
    import tempfile
    from synthai.rsi import auditar_ast
    from synthai.semiotica import comprimido
    raiz = os.path.dirname(os.path.abspath(__file__))
    linhas = open(os.path.join(raiz, texto), encoding="utf-8").read().split("\n")
    ini = linhas.index("import ast")
    fim = next(i for i, x in enumerate(linhas) if x.strip() == "main_evolution_loop()" and i > ini)
    codigo = [x.rstrip() for x in linhas[ini:fim + 1]]
    velho = [x.rstrip() for x in open(os.path.join(raiz, guardado), encoding="utf-8").read().split("\n")]
    while velho and velho[-1] == "":
        velho.pop()
    with tempfile.TemporaryDirectory() as d:
        caminho = os.path.join(d, "codigo.py")
        open(caminho, "w", encoding="utf-8").write("\n".join(codigo) + "\n")
        auditoria = auditar_ast(caminho)
    t = "\n".join(linhas)
    ct = comprimido(t)
    red = {}
    for n in range(31, 50):
        nome = next(f for f in sorted(os.listdir(raiz)) if f.startswith(f"ASI_AGI_parte{n}_"))
        doc = open(os.path.join(raiz, nome), encoding="utf-8").read()
        red[n] = 1 - (comprimido(doc + "\n" + t) - comprimido(doc)) / ct
    return codigo == velho, auditoria, red


def p948_pergunta_reconhece_resposta():
    """Rodada 24 (P948): o texto pós-ASI reenviado, pontuado pelas palavras contra os documentos das Partes 1-49
    (dialogo/rodada24.py, conferido em Java). Devolve [(parte, escore)] em ordem decrescente."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada24", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada24.py"))
    r24 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r24)
    ds, texto = r24.dados()
    return sorted(r24.pontuar(ds, texto), key=lambda x: (-x[1], x[0]))


ERROS_P999, TESTES_P999 = 154, 440


def p972_portugues_por_profundidade(d=None, pt=None):
    """A cobertura da OpenWordNet-PT por profundidade (P972): para os substantivos do WordNet com profundidade (P793), a
    fração que tem lema em português. Devolve (cobertura geral, cobertura na profundidade <= 4, na >= 12, {profundidade:
    (sinsets, cobertura)})."""
    from synthai.dicionario import Dicionario, DicionarioPT, profundidades
    d = d or Dicionario()
    pt = pt or DicionarioPT()
    prof = profundidades(d)
    por = {}
    inv = {i: k for k, i in d.indice.items()}
    for i, p in prof.items():
        pos, desloc = inv[i].split(":")
        if pos != "n":
            continue
        tem = f"{desloc}-n" in pt.lemas
        n, c = por.get(p, (0, 0))
        por[p] = (n + 1, c + tem)
    def cob(ps):
        n = sum(por[p][0] for p in ps)
        return sum(por[p][1] for p in ps) / n
    return (cob(list(por)), cob([p for p in por if p <= 4]), cob([p for p in por if p >= 12]),
            {p: (por[p][0], por[p][1] / por[p][0]) for p in sorted(por)})


def p973_kaprekar_hex(digitos=4, base=16):
    """A rotina de Kaprekar (P973): K(n) = (dígitos decrescentes) − (crescentes), com `digitos` dígitos na `base`, para todo
    n que não tem todos os dígitos iguais. Devolve (ciclos terminais, cada um começando pelo menor, {ciclo: quantos números
    ele atrai}, números)."""
    def k(n):
        ds = []
        for _ in range(digitos):
            n, r = divmod(n, base)
            ds.append(r)
        a = d_ = 0
        for x in sorted(ds, reverse=True):
            a = a * base + x
        for x in sorted(ds):
            d_ = d_ * base + x
        return a - d_
    bacia = {}
    total = 0
    for n in range(1, base ** digitos):
        x, ds = n, set()
        y = n
        for _ in range(digitos):
            y, r = divmod(y, base)
            ds.add(r)
        if len(ds) == 1:
            continue
        total += 1
        vistos = []
        while x not in vistos:
            vistos.append(x)
            x = k(x)
        ciclo = vistos[vistos.index(x):]
        j = ciclo.index(min(ciclo))
        c = tuple(ciclo[j:] + ciclo[:j])
        bacia[c] = bacia.get(c, 0) + 1
    return sorted(bacia), bacia, total


def p971_duas_memorias():
    """Rodada 25 (P971): exponencial, potência e duas exponenciais na curva média, pelo AIC (dialogo/rodada25.py,
    conferido em Java). Devolve (aic exponencial, aic potência, aic duas exponenciais, (A, B, t1, t2, sse))."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada25", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada25.py"))
    r25 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r25)
    sim = r25.r21.semelhancas(r25.r21.conjuntos())
    ys = [r25.r21.media_distancia(sim, L) for L in range(1, 21)]
    lys = [log(y) for y in ys]
    _, _, se = r25.r22.reta([float(L) for L in range(1, 21)], lys)
    _, _, sp = r25.r22.reta([log(L) for L in range(1, 21)], lys)
    s2, A, B, t1, t2 = r25.duas_exponenciais(ys)
    return r25.aic(se, 20, 2), r25.aic(sp, 20, 2), r25.aic(s2, 20, 4), (A, B, t1, t2, s2)


def p974_previsoes_sem_largura(partes=range(46, 52)):
    """A regra das faixas como passo verificável (P974): nas linhas de previsão "- (x) ..." do bloco "Previsões
    pré-registradas" de cada documento, conta as unilaterais (com ≥, ≤, >, <, "pelo menos", "no máximo", "ou mais",
    "ou menos" e sem um intervalo [a; b]). Devolve {parte: (previsões, unilaterais, [as letras das unilaterais])}."""
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    res = {}
    for n in partes:
        nome = next((f for f in sorted(os.listdir(raiz)) if f.startswith(f"ASI_AGI_parte{n}_")), None)
        if nome is None:
            continue
        texto = open(os.path.join(raiz, nome), encoding="utf-8").read()
        i = texto.find("## Previsões pré-registradas")
        if i < 0:
            continue
        bloco = texto[i:texto.find("\n---", i) if texto.find("\n---", i) > 0 else len(texto)]
        prev, uni = 0, []
        for linha in bloco.split("\n"):
            m = re.match(r"- \(([a-z])\)", linha.strip())
            if not m:
                continue
            prev += 1
            um_lado = re.search(r"≥|≤|(?<![-=])>|<|pelo menos|no máximo|ou mais|ou menos", linha)
            if um_lado and not re.search(r"\[[^\]]*;[^\]]*\]", linha):
                uni.append(m.group(1))
        res[n] = (prev, len(uni), uni)
    return res


ERROS_P1029, TESTES_P1029 = 156, 448


def p1002_funis_pt(pt=None):
    """Os funis das definições em português (P1002): cada lema de uma palavra só de um sinset de substantivo com glosa vai
    para a primeira palavra da glosa (no singular) que é lema de substantivo e não é ela mesma. Devolve (a mais escolhida,
    o seu grau, a fração das palavras com destino que escolhem uma das 10 mais, palavras com destino, as 10 mais)."""
    from synthai.dicionario import DicionarioPT
    pt = pt or DicionarioPT()
    nomes = {x.lower() for sid, ls in pt.lemas.items() if sid.endswith("-n") for x in ls if x.isalpha()}
    f = {}
    for sid in sorted(pt.glosas):
        if not sid.endswith("-n") or sid not in pt.lemas:
            continue
        for w in pt.lemas[sid]:
            w = w.lower()
            if not w.isalpha() or w in f:
                continue
            for t in pt.fichas(pt.glosas[sid]):
                b = pt.lema(t)
                if b is not None and b in nomes and b != w:
                    f[w] = b
                    break
    grau = {}
    for b in f.values():
        grau[b] = grau.get(b, 0) + 1
    top = sorted(grau, key=lambda w: (-grau[w], w))[:10]
    return top[0], grau[top[0]], sum(grau[w] for w in top) / len(f), len(f), [(w, grau[w]) for w in top]


def p1003_inverte_e_soma(ate=4095, base=16, maximo=50):
    """Inverte e soma (P1003): n -> n + (n com os dígitos invertidos na base), até um palíndromo, no máximo `maximo` passos.
    Um n que já é palíndromo conta com 0 passos. Devolve (fração que chega, média de passos dos que chegam, os que não
    chegam)."""
    def digitos(n):
        ds = []
        while n:
            n, r = divmod(n, base)
            ds.append(r)
        return ds  # do menos significativo para o mais

    def inverso(n):
        v = 0
        for r in digitos(n):
            v = v * base + r
        return v

    passos, nao = [], []
    for n in range(1, ate + 1):
        x, k = n, 0
        while digitos(x) != digitos(x)[::-1] and k < maximo:
            x += inverso(x)
            k += 1
        if digitos(x) == digitos(x)[::-1]:
            passos.append(k)
        else:
            nao.append(n)
    return len(passos) / ate, sum(passos) / len(passos), nao


def p1001_duas_memorias_em_log():
    """Rodada 26 (P1001): as duas exponenciais ajustadas em log por Gauss-Newton, com exp e log próprios
    (dialogo/rodada26.py, IGUAL em Java). Devolve (sse da grade, (A, B, t1, t2, sse em log), AIC, limiar para vencer a
    potência)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada26", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada26.py"))
    r26 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r26)
    sim = r26.r21.semelhancas(r26.r21.conjuntos())
    ys = [r26.r21.media_distancia(sim, L) for L in range(1, 21)]
    ly = [r26.log_(y) for y in ys]
    s0, A, B, t1, t2 = r26.grade(ys)
    th, sse = r26.gauss_newton([r26.log_(A), r26.log_(B), t1, t2], ly)
    return s0, (r26.exp_(th[0]), r26.exp_(th[1]), th[2], th[3], sse), 20 * r26.log_(sse / 20) + 8, 0.3095 * r26.exp_(-0.2)


ERROS_P1059, TESTES_P1059 = 157, 454


def p1031_historico_de_mim(partes=range(31, 53)):
    """O meu histórico mensurável, para eu prever a mim mesmo (P1031). Por parte: caracteres do documento, razão de
    compressão (zlib 9), testes de unidade escritos (def test_ em synthai/testes_parteNN.py), testes e erros do placar
    (linha "Parte N: X testes, Y erros" do documento) e a redundância média da pergunta dada a resposta (P821).
    Devolve {parte: dict}."""
    import os
    import re
    import zlib
    raiz = os.path.dirname(os.path.abspath(__file__))
    res = {}
    for n in partes:
        nome = next((f for f in sorted(os.listdir(raiz)) if f.startswith(f"ASI_AGI_parte{n}_")), None)
        if nome is None:
            continue
        doc = open(os.path.join(raiz, nome), encoding="utf-8").read()
        b = doc.encode("utf-8")
        tf = os.path.join(raiz, "synthai", f"testes_parte{n}.py")
        testes_unid = open(tf, encoding="utf-8").read().count("def test_") if os.path.exists(tf) else 0
        m = re.search(rf"Parte {n}:\s*\**\s*(\d+) testes?,\s*(\d+) erros?", doc)
        try:
            red = p821_inversao(range(n, n + 1))[1]
        except (ZeroDivisionError, StopIteration):
            red = None
        res[n] = {"caracteres": len(doc), "compressao": len(zlib.compress(b, 9)) / len(b), "testes_unidade": testes_unid,
                  "testes": int(m.group(1)) if m else None, "erros": int(m.group(2)) if m else None, "redundancia": red}
    return res


def p1032_preditor_de_mim(historico, k=8):
    """O preditor estatístico de mim mesma (P1032): para cada medida, o centro é a média das últimas k partes com valor e a
    meia-largura 1,645 × o desvio padrão amostral delas (faixa de 90% se as partes fossem uma amostra normal). Devolve
    {medida: (centro, meia-largura, último valor = o preditor ingênuo)}."""
    res = {}
    partes = sorted(historico)
    for medida in ("caracteres", "compressao", "testes_unidade", "testes", "erros", "redundancia"):
        vals = [historico[n][medida] for n in partes if historico[n][medida] is not None][-k:]
        t = 0.0
        for v in vals:  # laço, não sum() (compensada no Python 3.12+), para coincidir com o Java bit a bit
            t += v
        m = t / len(vals)
        q = 0.0
        for v in vals:
            q += (v - m) * (v - m)
        res[medida] = (m, 1.645 * sqrt(q / (len(vals) - 1)), vals[-1])  # sqrt, não ** 0,5 (pow da libm)
    return res


def p1033_definicao_e_profundidade(d=None):
    """O tamanho da definição prevê a profundidade? (P1033): Spearman entre o número de palavras da definição (glosa sem
    exemplos) e a profundidade (P793), nos substantivos com profundidade. Devolve (rho, sinsets, média de palavras por
    faixa de profundidade {0-4, 5-8, 9-12, 13+})."""
    from synthai.dicionario import Dicionario, profundidades, spearman
    d = d or Dicionario()
    prof = profundidades(d)
    xs, ys = [], []
    for i, p in sorted(prof.items()):
        pos, _, _, glosa = d.sinsets[i]
        if pos != "n":
            continue
        xs.append(len(d.definicao(glosa).split()))
        ys.append(p)
    faixas = {}
    for x, p in zip(xs, ys):
        f = "0-4" if p <= 4 else "5-8" if p <= 8 else "9-12" if p <= 12 else "13+"
        n, t = faixas.get(f, (0, 0))
        faixas[f] = (n + 1, t + x)
    return spearman(xs, ys), len(xs), {f: t / n for f, (n, t) in faixas.items()}


def p1034_pi_hexadecimal(n=1000):
    """Os dígitos hexadecimais de π (P1034): pela fórmula de Bailey-Borwein-Plouffe (o n-ésimo dígito sem os anteriores, em
    ponto flutuante) e por π exato em inteiros (Machin: π = 16 arctg(1/5) − 4 arctg(1/239)). Devolve (quantos coincidem, n,
    os 8 primeiros, o χ² das 16 frequências nos n dígitos exatos)."""
    def serie(j, d):
        # parte fracionária de Σ_k 16^(d-k)/(8k+j)
        s = 0.0
        for k in range(d + 1):
            s = (s + pow(16, d - k, 8 * k + j) / (8 * k + j)) % 1.0
        t, k = 0.0, d + 1
        while True:
            termo = 16.0 ** (d - k) / (8 * k + j)
            if termo < 1e-17:
                break
            t += termo
            k += 1
        return (s + t) % 1.0

    def bbp(pos):  # o dígito na posição pos (1 = o primeiro depois da vírgula)
        d = pos - 1
        x = (4 * serie(1, d) - 2 * serie(4, d) - serie(5, d) - serie(6, d)) % 1.0
        return int(x * 16)

    bits = 4 * n + 64
    um = 1 << bits

    def arctg_inv(x):
        soma, termo, k, sinal = 0, um // x, 1, 1
        while termo:
            soma += sinal * (termo // k)
            termo //= x * x
            k += 2
            sinal = -sinal
        return soma

    pi = 16 * arctg_inv(5) - 4 * arctg_inv(239)
    frac = pi - 3 * um
    exatos = []
    for _ in range(n):
        frac *= 16
        exatos.append(frac >> bits)
        frac &= um - 1
    pelo_bbp = [bbp(p) for p in range(1, n + 1)]
    cont = [exatos.count(h) for h in range(16)]
    esperado = n / 16
    chi2 = sum((c - esperado) ** 2 / esperado for c in cont)
    return sum(a == b for a, b in zip(pelo_bbp, exatos)), n, "".join(format(h, "X") for h in exatos[:8]), chi2


ERROS_P1089, TESTES_P1089 = 159, 462


def p1062_folhas(d=None):
    """Folhas e ramos da taxonomia (P1062): nos substantivos com profundidade, folha = nenhum sinset tem este como
    hiperônimo. Devolve (fração de folhas, média de filhos dos nós internos, substantivos)."""
    from synthai.dicionario import Dicionario, profundidades
    d = d or Dicionario()
    prof = profundidades(d)
    filhos = {}
    for i, x in enumerate(d.sinsets):
        for h in x[2]:
            if h in d.indice:
                k = d.indice[h]
                filhos[k] = filhos.get(k, 0) + 1
    nomes = [i for i in prof if d.sinsets[i][0] == "n"]
    internos = [filhos[i] for i in nomes if filhos.get(i, 0) > 0]
    return (len(nomes) - len(internos)) / len(nomes), sum(internos) / len(internos), len(nomes)


def p1063_autodescritivos(base=16):
    """Números autodescritivos de `base` dígitos na base (P1063): d_i = quantas vezes o dígito i aparece. Enumeração exata
    dos vetores com Σ d_i = base e Σ i·d_i = base (condições necessárias), conferindo cada um. Devolve a lista, em texto."""
    achados = []

    def rec(i, resto_peso, usados, d):
        if i == 0:
            d0 = base - usados
            if 0 <= d0 < base and resto_peso == 0:
                v = [d0] + d[::-1]
                if all(v[j] == v.count(j) for j in range(base)) and v[0] > 0:
                    achados.append("".join(format(x, "X") for x in v))
            return
        for k in range(0, min(base - 1, resto_peso // i) + 1):
            if usados + k > base:
                break
            rec(i - 1, resto_peso - i * k, usados + k, d + [k])

    rec(base - 1, base, 0, [])
    return sorted(achados)


def p1061_exatidao_ou_sorte():
    """Rodada 28 (P1061): a chance de cada rodada antiga passar por sorte pelo modelo de sorteios independentes
    (dialogo/rodada28.py, IGUAL em Java) e as diferenças REAIS da libm nos argumentos distintos das rodadas com chance < 0,5
    (dialogo/diferencas28.tsv, medidas com registrar_libm.py e CompararLibm.java). Devolve ({rodada: chance}, {rodada:
    (exp distintos, exp diferentes, log distintos, log diferentes)})."""
    import importlib.util
    import os
    raiz = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("rodada28", os.path.join(raiz, "dialogo", "rodada28.py"))
    r28 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r28)
    chances = {r: r28.chance(e, g) for r, e, g, _ in r28.contagens()}
    dif = {}
    for l in open(os.path.join(raiz, "dialogo", "diferencas28.tsv"), encoding="ascii").read().split("\n")[1:]:
        if l:
            c = l.split("\t")
            dif[c[0]] = tuple(int(x) for x in c[1:])
    return chances, dif


ERROS_P1119, TESTES_P1119 = 163, 468


def p1092_pnn_sem_teste(desde=821, ate=1090):
    """A auditoria pedida pela Parte 54 (P1092): das funções pNN com desde <= NN <= ate, quais não aparecem (pelo nome) em
    nenhum synthai/testes_parte*.py. Devolve (total, [sem teste])."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    nomes = [m.group(1) for m in re.finditer(r"^def (p(\d+)_\w+)\(", open(os.path.join(raiz, "calculos.py"), encoding="utf-8").read(), re.M)
             if desde <= int(m.group(2)) <= ate]
    testes = "".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(raiz, "synthai", "testes_parte*.py")))
    return len(nomes), [n for n in nomes if n not in testes]


def _destino_final(f, w):
    """O destino de uma órbita no mapa f: o ciclo (pelo menor elemento) ou o sumidouro onde ela termina."""
    vistos = {}
    x = w
    while x is not None and x not in vistos:
        vistos[x] = len(vistos)
        if f.get(x) is None:
            return ("sumidouro", x)
        x = f[x]
    ciclo = [y for y, i in vistos.items() if i >= vistos[x]]
    return ("ciclo", min(ciclo))


def p1093_sem_o_funil(funil="act", d=None):
    """A fragilidade do mapa da definição (P1093): as palavras cujo primeiro substantivo da definição é `funil` passam ao
    segundo substantivo (ou viram sumidouro). Devolve (fração das palavras que mudam de destino final, palavras que iam
    direto ao funil, palavras)."""
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    f = _mapa_da_definicao(d)
    nomes = set(f)
    g = dict(f)
    diretas = 0
    for w in sorted(f):
        if f[w] == funil:
            diretas += 1
            i = next(i for i in d.lemas[w] if d.sinsets[i][0] == "n")
            cand = [x for x in d.palavras_da_definicao(d.sinsets[i][3]) if x in nomes and x != w]
            resto = [x for x in cand if x != funil]
            g[w] = resto[0] if resto else None
    muda = sum(1 for w in f if _destino_final(f, w) != _destino_final(g, w))
    return muda / len(f), diretas, len(f)


def p1094_ulp_em_hexadecimal(n=100000, semente=1094):
    """Quantos dos 13 dígitos hexadecimais da mantissa mudam ao somar um ulp (P1094), para doubles sorteados em [1, 2).
    Devolve (média medida, a conta 16/15)."""
    import math
    rng = random.Random(semente)
    total = 0
    for _ in range(n):
        x = 1.0 + rng.random()
        y = math.nextafter(x, 2.0)
        a, b = x.hex()[4:17], y.hex()[4:17]
        if y >= 2.0:
            continue
        total += sum(1 for p, q in zip(a, b) if p != q)
    return total / n, 16 / 15


def p1094_ulp_mantissa_uniforme(n=100000, semente=1094):
    """O mundo novo da P1094: a mantissa de 52 bits sorteada uniforme (getrandbits), sem o arredondamento par de
    1 + random(); quantos dos 13 dígitos hexadecimais mudam ao somar um ulp. Devolve (média, 16/15)."""
    rng = random.Random(semente)
    total = 0
    for _ in range(n):
        m = rng.getrandbits(52)
        if m == (1 << 52) - 1:
            continue
        total += sum(1 for p, q in zip(format(m, "013x"), format(m + 1, "013x")) if p != q)
    return total / n, 16 / 15


def p1091_o_ulp_que_chega():
    """Rodada 29 (P1091): para cada rodada antiga que chama exp ou log, a maior mudança relativa da saída com um ulp em cada
    exp e log, e se o texto mudou (dialogo/rodada29.py sobre dialogo/saidas29/, conferido em Java). Devolve {rodada: (números,
    maior mudança relativa, texto mudou)}."""
    import importlib.util
    import os
    raiz = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("rodada29", os.path.join(raiz, "dialogo", "rodada29.py"))
    r29 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r29)
    res = {}
    for r in r29.RODADAS:
        a = open(os.path.join(raiz, "dialogo", "saidas29", f"normal{r}.txt"), encoding="utf-8").read()
        b = open(os.path.join(raiz, "dialogo", "saidas29", f"perturbada{r}.txt"), encoding="utf-8").read()
        res[r] = r29.comparar(a, b)
    return res


ERROS_P1149, TESTES_P1149 = 166, 474


def p1122_sinonimos_perfeitos(d=None):
    """Sinônimos perfeitos (P1122): palavras de uma palavra só (alfabéticas) com exatamente o mesmo conjunto de sinsets que
    outra. Devolve (fração das palavras com gêmeo, palavras, o maior grupo de gêmeos)."""
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    grupos = {}
    n = 0
    for w, idx in d.lemas.items():
        if not w.isalpha():
            continue
        n += 1
        grupos.setdefault(tuple(sorted(set(idx))), []).append(w)
    com = sum(len(g) for g in grupos.values() if len(g) > 1)
    maior = max(grupos.values(), key=lambda g: (len(g), sorted(g)))
    return com / n, n, sorted(maior)


def p1123_mesma_soma(ate=4095):
    """A mesma soma de dígitos em base 16 e em base 10 (P1123), para n de 1 a `ate`. Devolve (fração, quantos, a conta
    normal φ(7,5/√90)/√90)."""
    def soma(n, b):
        s = 0
        while n:
            n, r = divmod(n, b)
            s += r
        return s
    iguais = sum(1 for n in range(1, ate + 1) if soma(n, 16) == soma(n, 10))
    dp = sqrt(90.0)
    conta = exp(-0.5 * (7.5 / dp) ** 2) / sqrt(2 * pi) / dp
    return iguais / ate, iguais, conta


def p1121_empates():
    """Rodada 30 (P1121): os empates exatos nas escolhas impressas das rodadas 12, 14, 18, 19, 20 e 24 (dialogo/rodada30.py,
    conferido em Java). Devolve {rodada: empates}."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada30", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada30.py"))
    r30 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r30)
    return r30.contar(r30.grupos())


ERROS_P1179, TESTES_P1179 = 167, 479


def p1152_palindromos(d=None):
    """Palíndromos no dicionário (P1152): lemas alfabéticos de 3 letras ou mais (minúsculos). Devolve (palíndromos, a conta
    de letras independentes Σ_L f(L)·(Σp²)^⌊L/2⌋ × N, a conta com a coincidência real das pontas, N, exemplos)."""
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    ws = sorted({w.lower() for w in d.lemas if w.isalpha() and len(w) >= 3})
    letras, primeira, ultima, tam = {}, {}, {}, {}
    for w in ws:
        for ch in w:
            letras[ch] = letras.get(ch, 0) + 1
        primeira[w[0]] = primeira.get(w[0], 0) + 1
        ultima[w[-1]] = ultima.get(w[-1], 0) + 1
        tam[len(w)] = tam.get(len(w), 0) + 1
    n, tot = len(ws), sum(letras.values())
    q = sum((v / tot) ** 2 for v in letras.values())
    pontas = sum((primeira.get(ch, 0) / n) * (ultima.get(ch, 0) / n) for ch in letras)
    conta = sum(c * q ** (L // 2) for L, c in tam.items())
    conta_pontas = sum(c * pontas * q ** (L // 2 - 1) for L, c in tam.items())
    pals = [w for w in ws if w == w[::-1]]
    return len(pals), conta, conta_pontas, n, pals[:12]


def p1153_duplos_palindromos(ate=10 ** 6):
    """Números palíndromos em base 10 e em base 16 ao mesmo tempo (P1153), de 1 a ate − 1. Devolve (quantos, a conta
    Σ 16^(−⌊k/2⌋) sobre os palíndromos decimais, os primeiros)."""
    dec = [x for x in range(1, ate) if str(x) == str(x)[::-1]]
    conta = sum(16.0 ** (-(len(format(x, "x")) // 2)) for x in dec)
    duplos = [x for x in dec if format(x, "x") == format(x, "x")[::-1]]
    return len(duplos), conta, duplos[:20]


def p1151_alfabeto_portugues():
    """Rodada 31 (P1151): os 13 primeiros 4-gramas da Rodada 12 reordenados pela ordem de um dicionário português
    (dialogo/rodada31.py, IGUAL em Java). Devolve (pares que mudam de ordem, quantos dos 13 têm letra com acento)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada31", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada31.py"))
    r31 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r31)
    gs = r31.gramas()
    _, _, trocas = r31.reordenar(gs)
    return trocas, sum(1 for g, _, _ in gs if r31.chave_pt(g) != g.lower())


ERROS_P1209, TESTES_P1209 = 168, 486


def p1182_portugues_contra_ingles(d=None, pt=None):
    """Português contra inglês (P1182): nos sinsets com lema português e inglês de uma palavra só (o primeiro alfabético de
    cada), a razão média tamanho(pt)/tamanho(en). Devolve (razão média, pares, fração em que o português é mais longo)."""
    from synthai.dicionario import Dicionario, DicionarioPT
    d = d or Dicionario()
    pt = pt or DicionarioPT()
    razoes, maior = [], 0
    for chave, i in d.indice.items():
        pos, desloc = chave.split(":")
        sid = f"{desloc}-{pos}"
        if sid not in pt.lemas:
            continue
        en = [w for w in d.sinsets[i][1] if w.isalpha()]
        po = [w for w in pt.lemas[sid] if w.isalpha()]
        if not en or not po:
            continue
        a, b = min(po), min(en)
        razoes.append(len(a) / len(b))
        maior += len(a) > len(b)
    return sum(razoes) / len(razoes), len(razoes), maior / len(razoes)


def p1183_primeiro_digito_hex(base_pot, n=10000):
    """O primeiro dígito hexadecimal de base_pot^k, k = 1..n (P1183), em inteiros exatos. Devolve as 16 contagens."""
    cont = [0] * 16
    x = 1
    for _ in range(n):
        x *= base_pot
        cont[int(format(x, "x")[0], 16)] += 1
    return cont


def p1181_primeira_diferenca():
    """Rodada 32 (P1181): nos lemas portugueses em ordem de pontos de código, a posição média da primeira diferença entre
    vizinhos e os vizinhos invertidos pela chave portuguesa (dialogo/rodada32.py, IGUAL em Java). Devolve (posição média,
    pares, inversões, palavras com acento)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada32", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada32.py"))
    r32 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r32)
    ws = r32.lemas()
    soma, pares, inv = r32.medir(ws)
    return soma / pares, pares, inv, sum(1 for w in ws if r32.chave_pt(w) != w.lower())


ERROS_P1239, TESTES_P1239 = 171, 492
ERROS_P1269, TESTES_P1269 = 175, 503
ERROS_P1299, TESTES_P1299 = 178, 511
ERROS_P1329, TESTES_P1329 = 181, 519
ERROS_P1359, TESTES_P1359 = 182, 527
ERROS_P1389, TESTES_P1389 = 184, 535
ERROS_P1419, TESTES_P1419 = 186, 544
ERROS_P1449, TESTES_P1449 = 189, 553
ERROS_P1479, TESTES_P1479 = 189, 559
ERROS_P1509, TESTES_P1509 = 189, 565
ERROS_P1539, TESTES_P1539 = 189, 573
ERROS_P1569, TESTES_P1569 = 191, 583
VEREDITOS_P1629 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ❌ (l) ❌ (m) ✅ (n) ✅ (o) ✅ (p) ✅"
ERROS_P1599, TESTES_P1599 = 193, 591
ERROS_P1629, TESTES_P1629 = 195, 607
VEREDITOS_P1659 = "(a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ❌ (i) ✅ (j) ✅ (k) ❌"
ERROS_P1659, TESTES_P1659 = 198, 618
VEREDITOS_P1689 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ✅"
ERROS_P1689, TESTES_P1689 = 199, 625
VEREDITOS_P1719 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ❌ (g) ✅"
ERROS_P1719, TESTES_P1719 = 201, 632
VEREDITOS_P1749 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅"
ERROS_P1749, TESTES_P1749 = 201, 636
VEREDITOS_P1779 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅"
ERROS_P1779, TESTES_P1779 = 201, 641
VEREDITOS_P1809 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅"
ERROS_P1809, TESTES_P1809 = 201, 645
VEREDITOS_P1839 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅"  # a (e) é medida nas Partes 80 a 84
ERROS_P1839, TESTES_P1839 = 201, 649
VEREDITOS_P1869 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅"
ERROS_P1869, TESTES_P1869 = 201, 657
VEREDITOS_P1899 = "(a) ✅ (b) ✅ (c) ❌"  # a (d) não se aplica: não havia nada a tirar
ERROS_P1899, TESTES_P1899 = 202, 660
VEREDITOS_P1959 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ❌ (p) ✅"
ERROS_P1959, TESTES_P1959 = 203, 675
VEREDITOS_P2019 = "(a) ✅ (b) ❌ (c) ❌ (d) ❌ (e) ❌ (f) ✅ (g) ❌ (h) ✅ (i) ❌ (j) ❌"
ERROS_P2019, TESTES_P2019 = 210, 685
VEREDITOS_P2099 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅"
ERROS_P2099, TESTES_P2099 = 210, 690
VEREDITOS_P2169 = "(a) ❌ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅"
ERROS_P2169, TESTES_P2169 = 211, 697
VEREDITOS_P2239 = "(a) ✅ (b) ✅ (c) ❌ (d) ❌ (e) ❌ (f) ❌"
ERROS_P2239, TESTES_P2239 = 215, 703
VEREDITOS_P2309 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅"
ERROS_P2309, TESTES_P2309 = 215, 708
VEREDITOS_P2379 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅"
ERROS_P2379, TESTES_P2379 = 215, 713
VEREDITOS_P2449 = "(a) ✅ (b) ✅ (c) ✅"
ERROS_P2449, TESTES_P2449 = 215, 716
VEREDITOS_P2519 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅"
ERROS_P2519, TESTES_P2519 = 215, 720
VEREDITOS_P2589 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅"
ERROS_P2589, TESTES_P2589 = 215, 724
VEREDITOS_P2659 = "(a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅"
ERROS_P2659, TESTES_P2659 = 216, 730
VEREDITOS_P2729 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P2729, TESTES_P2729 = 216, 735
VEREDITOS_P2799 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P2799, TESTES_P2799 = 216, 740
VEREDITOS_P2869 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P2869, TESTES_P2869 = 216, 745
VEREDITOS_P2939 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ✅"
ERROS_P2939, TESTES_P2939 = 217, 750
VEREDITOS_P3009 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P3009, TESTES_P3009 = 217, 755
VEREDITOS_P3079 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P3079, TESTES_P3079 = 217, 760
VEREDITOS_P3149 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P3149, TESTES_P3149 = 217, 765
VEREDITOS_P3219 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P3219, TESTES_P3219 = 217, 770
VEREDITOS_P3289 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P3289, TESTES_P3289 = 217, 775
VEREDITOS_P3359 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P3359, TESTES_P3359 = 217, 780
VEREDITOS_P3429 = "(a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ✅"
ERROS_P3429, TESTES_P3429 = 218, 785
VEREDITOS_P3499 = "(a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ✅"
ERROS_P3499, TESTES_P3499 = 219, 790
VEREDITOS_P3569 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅"
ERROS_P3569, TESTES_P3569 = 219, 795
VEREDITOS_P3639 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅"
ERROS_P3639, TESTES_P3639 = 219, 800
VEREDITOS_P3709 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅"
ERROS_P3709, TESTES_P3709 = 219, 805
VEREDITOS_P3779 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ✅ (h) ✅ (i) ✅"
ERROS_P3779, TESTES_P3779 = 220, 814
VEREDITOS_P3849 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ❌ (p) ✅ (q) ✅ (r) ✅ (s) ✅ (t) ✅ (u) ✅ (v) ✅"
ERROS_P3849, TESTES_P3849 = 221, 835
VEREDITOS_P3919 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ❌ (l) ✅ (n) ❌ (o) ✅ (p) ❌"
ERROS_P3919, TESTES_P3919 = 224, 850
VEREDITOS_P3989 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ✅"
ERROS_P3989, TESTES_P3989 = 224, 864
VEREDITOS_P4059 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅"
ERROS_P4059, TESTES_P4059 = 224, 877
VEREDITOS_P4129 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅"
ERROS_P4129, TESTES_P4129 = 224, 887
VEREDITOS_P4199 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ❌ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (p) ✅ (q) ✅"
ERROS_P4199, TESTES_P4199 = 225, 903
VEREDITOS_P4269 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (p) ✅ (q) ✅ (r) ✅ (s) ✅ (t) ✅"
ERROS_P4269, TESTES_P4269 = 225, 922
VEREDITOS_P4339 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ❌ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅"
ERROS_P4339, TESTES_P4339 = 226, 933
VEREDITOS_P4409 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅"
ERROS_P4409, TESTES_P4409 = 226, 939
VEREDITOS_P4479 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅"
ERROS_P4479, TESTES_P4479 = 226, 943
VEREDITOS_P4619 = "(a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ❌ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (q) ✅ (r) ❌"
ERROS_P4619, TESTES_P4619 = 229, 959  # a Parte 120 (o Leduc) ainda está aberta: os números dela entram depois, por cima destes
VEREDITOS_P4759 = "(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ❌ (g) ❌ (h) ✅ (i) ✅ (j) ❌ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (p) ✅ (q) ❌ (r) ✅ (s) ✅ (t) ✅ (u) ✅ (v) ❌ (w) ✅ (x) ✅ (y) ✅ (z) ✅"
ERROS_P4759, TESTES_P4759 = 236, 1009  # 231/984 + 5/25
VEREDITOS_P4689 = "(a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (q) ✅ (r) ✅"
ERROS_P4689, TESTES_P4689 = 231, 984  # 230/968 (até a 121, com a 120) + 1/16
VEREDITOS_P4549 = "(a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅"
ERROS_P4549, TESTES_P4549 = 227, 952  # na ordem das partes (até a 120, sem a 121): 226/943 da 119 + 1/9; com a 121, o acumulado é 230/968 (a 122 parte daí)


def p1212_palavras_que_nao_definem(d=None):
    """As palavras que nunca aparecem na definição de outra (P1212): no grafo de definições, o grau de entrada zero.
    Devolve (fração, palavras, as 5 que mais definem, com o grau)."""
    from synthai.dicionario import Dicionario
    g = (d or Dicionario()).grafo_de_definicoes()
    grau = {w: 0 for w in g}
    for u, vs in g.items():
        for v in vs:
            if v in grau:
                grau[v] += 1
    zero = sum(1 for x in grau.values() if x == 0)
    top = sorted(grau, key=lambda w: (-grau[w], w))[:5]
    return zero / len(grau), len(grau), [(w, grau[w]) for w in top]


def p1213_persistencia_hex(ate=16 ** 5):
    """A persistência multiplicativa em base 16 (P1213), para n de 16 a ate − 1: quantas vezes se multiplicam os dígitos
    hexadecimais até sobrar um dígito. Devolve (a maior, o primeiro número com ela, a média)."""
    def prod(n):
        p = 1
        while n:
            n, r = divmod(n, 16)
            p *= r
        return p
    maior, quem, soma = 0, None, 0
    for n in range(16, ate):
        k, x = 0, n
        while x >= 16:
            x = prod(x)
            k += 1
        soma += k
        if k > maior:
            maior, quem = k, n
    return maior, quem, soma / (ate - 16)


def p1211_nome_e_palavra():
    """Rodada 33 (P1211): dos lemas portugueses com maiúscula, quantos têm irmã minúscula com a mesma grafia
    (dialogo/rodada33.py, IGUAL em Java). Devolve (com maiúscula, com irmã, exemplos)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada33", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada33.py"))
    r33 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r33)
    return r33.irmas(r33.lemas())


def p1241_placar_por_voz(ate=33):
    """Rodada 34 (P1241): o placar por voz do diálogo contado por uma função que lê dialogo/DIALOGO.md (rodadas 13 a ate), IGUAL
    em Java (dialogo/Rodada34.java). Devolve ({voz: [previsões estritas, acertos estritos, previsões generosas, acertos
    generosos]}, linhas por rodada)."""
    import importlib.util
    import os
    raiz = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("rodada34", os.path.join(raiz, "dialogo", "rodada34.py"))
    r34 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r34)
    with open(os.path.join(raiz, "dialogo", "DIALOGO.md"), encoding="utf-8") as f:
        return r34.placar(f.read(), 13, ate)


def p1242_definicao_propria(d=None):
    """As definições que usam a própria palavra (P1242): dos sinsets com pelo menos um lema de uma palavra só, a fração cuja
    definição lematizada (morphy) contém um desses lemas. Devolve (fração, sinsets considerados, fração por classe, 5 exemplos)."""
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    n, k, por, ex = 0, 0, {}, []
    for pos, lemas, _, glosa in d.sinsets:
        simples = {w.lower() for w in lemas if "_" not in w and "-" not in w}
        if not simples:
            continue
        sim = any(x in simples for x in d.palavras_da_definicao(glosa))
        n += 1
        k += sim
        a, b = por.get(pos, (0, 0))
        por[pos] = (a + sim, b + 1)
        if sim and len(ex) < 5:
            ex.append((lemas[0], glosa))
    return k / n, n, {c: a / b for c, (a, b) in sorted(por.items())}, ex


def p1243_narcisistas_hex(kmax=8, base=16):
    """Números narcisistas numa base (P1243): n com k dígitos igual à soma dos dígitos elevados a k, para k de 1 a kmax. Como
    a soma só depende do multiconjunto de dígitos, percorre os multiconjuntos (C(k + base − 1, k) por k). Devolve a lista
    ordenada."""
    from itertools import combinations_with_replacement
    achados = []
    for k in range(1, kmax + 1):
        pot = [x ** k for x in range(base)]
        for ds in combinations_with_replacement(range(base), k):
            s = sum(pot[x] for x in ds)
            if s == 0 or not base ** (k - 1) <= s < base ** k:
                continue
            dig, x = [], s
            while x:
                x, r = divmod(x, base)
                dig.append(r)
            if sorted(dig) == list(ds):
                achados.append(s)
    return sorted(achados)


def p1247_interruptores(k, base=16):
    """Os interruptores dos narcisistas (P1247): pares (d, p) com d ≥ 1 e p < k tais que d^(k−1) = base^p, isto é,
    d·base^p = d^k: trocar um 0 na posição p por d soma o mesmo ao número e à soma das potências. Devolve a lista ordenada."""
    return [(d, q) for d in range(1, base) for q in range(k) if d ** (k - 1) == base ** q]


def p1248_por_comprimento(nums, base=16):
    """Quantos números de cada comprimento (em dígitos da base) há numa lista (P1248). Devolve {k: quantos}."""
    por = {}
    for n in nums:
        k, x = 0, n
        while x:
            x //= base
            k += 1
        por[k] = por.get(k, 0) + 1
    return dict(sorted(por.items()))


def p1249_fator_de_congruencia(k, base=16):
    """O fator de congruência dos narcisistas (P1249): o maior divisor g de base − 1 com d^k ≡ d (mod g) para todo dígito d.
    Como n ≡ soma dos dígitos (mod base − 1), com esse g a congruência n ≡ soma das potências (mod g) vale sozinha, e a chance de
    um candidato acertar sobe g vezes. Devolve g."""
    return max(g for g in range(1, base) if (base - 1) % g == 0 and all((d ** k - d) % g == 0 for d in range(base)))


def p1250_esperado_narcisistas(k, base=16):
    """A conta do número esperado de narcisistas com k dígitos (P1250): soma, sobre os multiconjuntos de dígitos cuja soma de
    potências tem k dígitos, da chance de um número de k dígitos ao acaso ter aquele multiconjunto (multinomial, sem zero à
    esquerda); depois multiplica pelo fator de congruência (P1249). Devolve (sem o fator, com o fator)."""
    from itertools import combinations_with_replacement
    from math import factorial
    pot = [x ** k for x in range(base)]
    e = 0
    for ds in combinations_with_replacement(range(base), k):
        s = sum(pot[x] for x in ds)
        if not base ** (k - 1) <= s < base ** k:
            continue
        m = factorial(k)
        for x in set(ds):
            m //= factorial(ds.count(x))
        z = ds.count(0)
        e += m * (k - z) // k if z else m
    e = e / ((base - 1) * base ** (k - 1))
    return e, e * p1249_fator_de_congruencia(k, base)


def p1251_conta_contra_medida(casos=((16, 9), (8, 8), (10, 7), (6, 13), (12, 11))):
    """A conta dos narcisistas contra a medida (P1251): para cada base e cada k de 2 a kmax, o número medido (P1243, P1248) e
    o esperado sem e com o fator de congruência (P1250). Devolve (linhas (base, k, medido, sem, com), log-verossimilhança de
    Poisson sem o fator, com o fator)."""
    from math import lgamma, log
    linhas, l0, l1 = [], 0.0, 0.0
    for base, kmax in casos:
        por = p1248_por_comprimento(p1243_narcisistas_hex(kmax, base), base)
        for k in range(2, kmax + 1):
            m = por.get(k, 0)
            e0, e1 = p1250_esperado_narcisistas(k, base)
            linhas.append((base, k, m, e0, e1))
            l0 += m * log(e0) - e0 - lgamma(m + 1)
            l1 += m * log(e1) - e1 - lgamma(m + 1)
    return linhas, l0, l1


def p1271_rodadas_verificadas():
    """Quantas rodadas o dialogo/verificar.py confere (P1271): os pares RodadaNN.java / rodadaNN.py. Devolve (pares, números)."""
    import glob
    import os
    aqui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo")
    nums = sorted(int(os.path.basename(j)[6:-5]) for j in glob.glob(os.path.join(aqui, "Rodada*.java"))
                  if os.path.exists(os.path.join(aqui, "r" + os.path.basename(j)[1:-5] + ".py")))
    return len(nums), nums


NEGACOES = ("not ", "lacking", "without", "devoid", "free of", "free from", "having no ")
PREFIXOS_NEGATIVOS = ("un", "in", "im", "il", "ir", "non", "dis")


def p1272_adjetivos_negativos(d=None):
    """Os adjetivos definidos pela negação (P1272): dos sinsets de adjetivo, a fração cuja definição começa por "not",
    "lacking", "without", "devoid", "free of/from" ou "having no"; e, entre esses, a fração com algum lema de prefixo negativo.
    Devolve (fração negativa, adjetivos, fração com prefixo entre os negativos, 5 exemplos)."""
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    n, neg, pre, ex = 0, 0, 0, []
    for pos, lemas, _, glosa in d.sinsets:
        if pos != "a":
            continue
        n += 1
        g = d.definicao(glosa).strip().lower()
        if g.startswith(NEGACOES):
            neg += 1
            pre += any(w.lower().startswith(PREFIXOS_NEGATIVOS) for w in lemas)
            if len(ex) < 5:
                ex.append((lemas[0], g[:60]))
    return neg / n, n, (pre / neg if neg else 0.0), ex


def p1273_niven(ate=16 ** 5, base=16):
    """Os números de Niven numa base (P1273): quantos n de 1 a ate são divisíveis pela soma dos seus dígitos; e a conta de
    De Koninck, Doyon e Kátai, eta·x/ln x com eta = (2 ln q)/(q − 1)²·Σ_{j=1}^{q−1} mdc(j, q − 1). Devolve (contagem, conta)."""
    from math import gcd, log
    soma = [0] * (ate + 1)
    k = 0
    for n in range(1, ate + 1):
        soma[n] = soma[n // base] + n % base
        k += n % soma[n] == 0
    eta = 2 * log(base) / (base - 1) ** 2 * sum(gcd(j, base - 1) for j in range(1, base))
    return k, eta * ate / log(ate)


def p1274_narcisistas_14_bases():
    """Rodada 35 (P1274): os narcisistas das bases 3 a 16, k de 2 a 7, contra a conta com o fator de congruência
    (dialogo/rodada35.py, IGUAL em Java). Devolve (células [((b, k), (medido, num, den, g, interruptor, conta))], grupos
    [(nome, medido, conta)])."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada35", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada35.py"))
    r35 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r35)
    celulas = [((b, k), r35.celula(b, k)) for b in r35.BASES for k in r35.KS]
    return celulas, r35.grupos(celulas)


def p1278_familias_narcisistas(kmax=7, bases=range(3, 17)):
    """As famílias dos narcisistas (P1278): o interruptor (1, 0) existe em toda base, então cada solução terminada em 0 traz
    n + 1. Juntando cada par {n terminado em 0, n + 1, ambos soluções} numa família, conta, nas células (b, k ≥ 2) sem outro
    interruptor (P1247), as soluções, os pares e a conta com o fator (P1250). Devolve (soluções, famílias, conta, pares)."""
    sol = fam = pares = 0
    conta = 0.0
    for b in bases:
        nums = set(p1243_narcisistas_hex(kmax, b))
        por_k = {}
        for n in nums:
            por_k.setdefault(len(_digitos_base(n, b)), []).append(n)
        for k in range(2, kmax + 1):
            if len(p1247_interruptores(k, b)) > 1:
                continue
            ns = por_k.get(k, [])
            p = sum(1 for n in ns if n % b == 0 and n + 1 in nums)
            sol += len(ns)
            pares += p
            fam += len(ns) - p
            conta += p1250_esperado_narcisistas(k, b)[1]
    return sol, fam, conta, pares


def _digitos_base(n, b):
    ds = []
    while n:
        n, r = divmod(n, b)
        ds.append(r)
    return ds


def p1301_ultimo_digito():
    """Rodada 36 (P1301): o teste do último dígito dos narcisistas, por base (3 a 16, k de 2 a 7, células sem interruptor), IGUAL
    em Java (dialogo/rodada36.py). Devolve ([(b, excesso, razão medido/conta, medido, conta, conta corrigida)], Spearman)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada36", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada36.py"))
    r36 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r36)
    linhas = r36.por_base()
    return linhas, r36.pearson(r36.postos([x[1] for x in linhas]), r36.postos([x[2] for x in linhas]))


def p1302_iguais_nas_duas_linguas(d=None, pt=None):
    """As palavras iguais nas duas línguas (P1302): dos sinsets com lema na OpenWordNet-PT, a fração em que um lema português de
    uma palavra só (minúsculas) é idêntico a um lema inglês do mesmo sinset. Devolve (fração, sinsets, {classe: fração}, 8 exemplos)."""
    from synthai.dicionario import Dicionario, DicionarioPT
    d = d or Dicionario()
    pt = pt or DicionarioPT()
    n, k, por, ex = 0, 0, {}, []
    for chave, i in sorted(d.indice.items()):
        pos, desloc = chave.split(":")
        pts = pt.lemas.get(f"{desloc}-{pos}") or (pt.lemas.get(f"{desloc}-s") if pos == "a" else None)
        if not pts:
            continue
        ing = {w.lower() for w in d.sinsets[i][1] if "_" not in w}
        por_ = {w.lower() for w in pts if " " not in w and "_" not in w}
        sim = bool(ing & por_)
        n += 1
        k += sim
        a, b = por.get(pos, (0, 0))
        por[pos] = (a + sim, b + 1)
        if sim and len(ex) < 8:
            ex.append(sorted(ing & por_)[0])
    return k / n, n, {c: a / b for c, (a, b) in sorted(por.items())}, ex


def p1303_autonumeros(ate=16 ** 5, base=16):
    """Os autonúmeros de Kaprekar numa base (P1303): m de 1 a ate que não é n + s(n) para nenhum n (s, a soma dos dígitos na
    base). Devolve (densidade, contagem, os 8 primeiros)."""
    alcancado = bytearray(ate + 1)
    soma = [0] * (ate + 1)
    for n in range(1, ate + 1):
        soma[n] = soma[n // base] + n % base
        m = n + soma[n]
        if m <= ate:
            alcancado[m] = 1
    auto = [m for m in range(1, ate + 1) if not alcancado[m]]
    return len(auto) / ate, len(auto), auto[:8]


def p1307_terminacoes_iguais(d=None, pt=None, classe="a", n_term=2):
    """As terminações das palavras iguais nas duas línguas (P1307): nos sinsets da classe com uma palavra portuguesa idêntica
    a uma inglesa (P1302), a contagem das últimas n_term letras da palavra igual (a primeira em ordem). Devolve (total,
    [(terminação, contagem)] em ordem decrescente)."""
    from synthai.dicionario import Dicionario, DicionarioPT
    d = d or Dicionario()
    pt = pt or DicionarioPT()
    cont, total = {}, 0
    for chave, i in sorted(d.indice.items()):
        pos, desloc = chave.split(":")
        if pos != classe:
            continue
        pts = pt.lemas.get(f"{desloc}-{pos}") or (pt.lemas.get(f"{desloc}-s") if pos == "a" else None)
        if not pts:
            continue
        iguais = {w.lower() for w in d.sinsets[i][1] if "_" not in w} & {w.lower() for w in pts if " " not in w and "_" not in w}
        if not iguais:
            continue
        w = sorted(iguais)[0]
        total += 1
        cont[w[-n_term:]] = cont.get(w[-n_term:], 0) + 1
    return total, sorted(cont.items(), key=lambda x: (-x[1], x[0]))


def p1308_chance_de_spearman(rho, n=14, vezes=20000, semente=1301):
    """A chance de uma correlação de postos ≥ rho ao acaso (P1308), por permutações (semente fixa): sorteia uma ordem dos n
    postos e calcula Pearson nos postos, como a rodada 36. Devolve a fração das permutações com correlação ≥ rho."""
    import random
    r = random.Random(semente)
    xs = [float(i) for i in range(n)]
    mx = sum(xs) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    k = 0
    for _ in range(vezes):
        ys = xs[:]
        r.shuffle(ys)
        k += sum((x - mx) * (y - mx) for x, y in zip(xs, ys)) / sxx >= rho
    return k / vezes


def p1331_fator_efetivo():
    """Rodada 37 (P1331): o fator de congruência efetivo F dos narcisistas (dialogo/rodada37.py, IGUAL em Java). Devolve
    ([(b, medido, conta com g, conta com F)] nas células sem interruptor, células com candidatos, células com F a mais de 10%
    de g)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada37", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada37.py"))
    r37 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r37)
    linhas, com, longe = [], 0, 0
    for b in r37.BASES:
        m, cg, cf = 0, 0.0, 0.0
        for k in r37.KS:
            cand, ig, med, num, den, g, inter = r37.celula(b, k)
            if cand == 0:
                continue
            f = ((b - 1) * ig) / cand
            com += 1
            longe += abs(f - g) > 0.1 * g
            if inter:
                continue
            m += med
            cg += (num / den) * g
            cf += (num / den) * f
        linhas.append((b, m, cg, cf))
    return linhas, com, longe


def p1332_glosa_pt_e_en(d=None, pt=None):
    """A glosa portuguesa contra a inglesa (P1332): nos sinsets com glosa na OpenWordNet-PT, a razão (palavras da glosa
    portuguesa)/(palavras da definição inglesa sem os exemplos). Devolve (mediana, fração com a portuguesa mais longa, pares,
    média)."""
    from synthai.dicionario import Dicionario, DicionarioPT
    d = d or Dicionario()
    pt = pt or DicionarioPT()
    razoes, mais = [], 0
    for chave, i in sorted(d.indice.items()):
        pos, desloc = chave.split(":")
        g = pt.glosas.get(f"{desloc}-{pos}") or (pt.glosas.get(f"{desloc}-s") if pos == "a" else None)
        if not g:
            continue
        ne, np_ = len(d.definicao(d.sinsets[i][3]).split()), len(g.split())
        if ne == 0:
            continue
        razoes.append(np_ / ne)
        mais += np_ > ne
    razoes.sort()
    n = len(razoes)
    med = razoes[n // 2] if n % 2 else (razoes[n // 2 - 1] + razoes[n // 2]) / 2
    return med, mais / n, n, sum(razoes) / n


def p1333_primos_palindromos(ate=16 ** 5, base=16):
    """Os primos palíndromos numa base (P1333): n < ate primo cujos dígitos na base formam um palíndromo; e a conta (os primos
    de 1 dígito e os palíndromos pares exatos; nos de comprimento ímpar ≥ 3, Σ 2/ln n sobre os ímpares). Devolve (quantidade,
    conta, por comprimento)."""
    from math import log
    crivo = bytearray([1]) * ate
    crivo[0] = crivo[1] = 0
    for i in range(2, int(ate ** 0.5) + 1):
        if crivo[i]:
            crivo[i * i::i] = bytearray(len(range(i * i, ate, i)))
    k, conta, por = 0, 0.0, {}
    for n in range(1, ate):
        ds = _digitos_base(n, base)
        if ds != ds[::-1]:
            continue
        L = len(ds)
        if crivo[n]:
            k += 1
            por[L] = por.get(L, 0) + 1
        if L == 1 or L % 2 == 0:
            conta += crivo[n]  # exatos: os de 1 dígito e os pares (múltiplos de base + 1)
        elif n % 2:
            conta += 2 / log(n)
    return k, conta, dict(sorted(por.items()))


def p1337_conta_palindromos(ate, base):
    """Só a conta dos primos palíndromos (P1337), sem contar os primos de comprimento ímpar ≥ 3: os primos de 1 dígito (exatos,
    por divisão), o base + 1 se for primo (o único palíndromo de comprimento par que pode ser primo: todos são múltiplos de
    base + 1) e Σ 2/ln n sobre os palíndromos ímpares de comprimento ímpar ≥ 3 abaixo de ate. Devolve a conta."""
    from math import log

    def primo(n):
        return n > 1 and all(n % q for q in range(2, int(n ** 0.5) + 1))
    conta = sum(1 for n in range(2, base) if primo(n)) + (1 if primo(base + 1) and base + 1 < ate else 0)
    for n in range(base, ate):
        ds = _digitos_base(n, base)
        if len(ds) % 2 == 1 and ds == ds[::-1] and n % 2:
            conta += 2 / log(n)
    return conta


def p1338_contas_da_parte63(media_base8=None):
    """As contas auxiliares da Parte 63 (P1338): (1) a chance de Poisson de 13 ou mais narcisistas na base 8 com a média da conta
    com F (P1331); (2) o desvio da contagem dos primos palíndromos em base 16 sob a conta (Σ p(1 − p) nos de comprimento ímpar
    ≥ 3, p = 2/ln n), relativo à conta; (3) o ingênuo "fração dos primos até 16⁵ vezes o número de palíndromos". Devolve
    (cauda de Poisson, desvio relativo, ingênuo, palíndromos, média usada)."""
    from math import exp, log, sqrt
    if media_base8 is None:
        media_base8 = next(x[3] for x in p1331_fator_efetivo()[0] if x[0] == 8)
    termo, cdf = exp(-media_base8), 0.0
    for j in range(13):
        cdf += termo
        termo *= media_base8 / (j + 1)
    ate = 16 ** 5
    var, npal = 0.0, 0
    for n in range(1, ate):
        ds = _digitos_base(n, 16)
        if ds != ds[::-1]:
            continue
        npal += 1
        if len(ds) >= 3 and len(ds) % 2 and n % 2:
            q = 2 / log(n)
            var += q * (1 - q)
    k, conta, _ = p1333_primos_palindromos()
    crivo = bytearray([1]) * ate
    crivo[0] = crivo[1] = 0
    for i in range(2, int(ate ** 0.5) + 1):
        if crivo[i]:
            crivo[i * i::i] = bytearray(len(range(i * i, ate, i)))
    ingenuo = sum(crivo) / ate * npal
    return 1 - cdf, sqrt(var) / conta, ingenuo, npal, media_base8


def p1361_fator_do_final():
    """Rodada 38 (P1361): os primos palíndromos das bases 5 a 16 contra a conta A (2/ln n nos ímpares) e a conta B (o fator exato
    dos primos de 2b), com o log próprio (dialogo/rodada38.py, IGUAL em Java). Devolve [(b, medido, conta A, conta B, σ)]."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada38", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada38.py"))
    r38 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r38)
    c = r38.crivo(16 ** 5)
    linhas = []
    for b in r38.BASES:
        m, a, bb, var = r38.base(b, c)
        linhas.append((b, m, a, bb, sqrt(var)))
    return linhas


def p1362_brevidade_e_sentidos(d=None):
    """A brevidade e o significado (P1362): nos lemas de uma palavra só do WordNet (minúsculas, só letras), a correlação de
    postos entre o comprimento em letras e o número de sinsets. Devolve (Spearman, lemas, fração monossêmica, média de sentidos
    por comprimento {L: média} para L de 2 a 12)."""
    import importlib.util
    import os
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    spec = importlib.util.spec_from_file_location("rodada36", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada36.py"))
    r36 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r36)
    cont = {}
    for _, lemas, _, _ in d.sinsets:
        for w in lemas:
            if w.isalpha():
                cont[w.lower()] = cont.get(w.lower(), 0) + 1
    ws = sorted(cont)
    rho = r36.pearson(r36.postos([float(len(w)) for w in ws]), r36.postos([float(cont[w]) for w in ws]))
    por = {}
    for w in ws:
        a, b = por.get(len(w), (0, 0))
        por[len(w)] = (a + cont[w], b + 1)
    return rho, len(ws), sum(1 for w in ws if cont[w] == 1) / len(ws), {L: por[L][0] / por[L][1] for L in range(2, 13) if L in por}


def p1363_quadrados_palindromos(ate=16 ** 4, base=16):
    """Os quadrados palíndromos numa base (P1363): n de 1 a ate − 1 com n² palíndromo; e a conta (Σ base^(−⌊L/2⌋), L = dígitos de
    n²). Devolve (quantidade, conta, os n em ordem)."""
    ns, conta = [], 0.0
    for n in range(1, ate):
        ds = _digitos_base(n * n, base)
        conta += base ** (-(len(ds) // 2))
        if ds == ds[::-1]:
            ns.append(n)
    return len(ns), conta, ns


def p1367_bases_novas_palindromos(bases=range(17, 23)):
    """Os primos palíndromos em bases novas (P1367), com a conta B e o σ da rodada 38 (dialogo/rodada38.base), até b⁵. Devolve
    [(b, medido, conta B, σ, z = (medido − B)/σ)]."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada38", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada38.py"))
    r38 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r38)
    c = r38.crivo(max(bases) ** 5)
    saida = []
    for b in bases:
        m, a, bb, var = r38.base(b, c)
        s = sqrt(var)
        saida.append((b, m, bb, s, (m - bb) / s))
    return saida


def p1391_o_que_nao_e_divisor():
    """Rodada 39 (P1391): a correção dos primos pequenos q ∤ 2b nos palíndromos (dialogo/rodada39.py, IGUAL em Java). Devolve
    [(b, N, correção, medido, conta C, σ, medido de comprimento 5, conta C de comprimento 5)] nas bases 5 a 22."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada39", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada39.py"))
    r39 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r39)
    c = r39.crivo(22 ** 5)
    saida = []
    for b in r39.BASES:
        N, div, corr, ex, med, conta, var = r39.base(b, c)
        saida.append((b, N, corr, ex + med[3] + med[5], ex + conta[3] + conta[5], sqrt(var), med[5], conta[5]))
    return saida


def p1397_correcao_b2_mais_1(bases=range(17, 23)):
    """A correção dos primos r > 13 que dividem (b² + 1)(b⁴ + 1) e não dividem 2b (P1397): nos palíndromos de comprimento 3 e 5
    coprimos a 2b, a fração f_r divisível por r e a correção Π (1 − f_r)/(1 − 1/r); aplicada à parte variável da conta C da
    rodada 39. Devolve [(b, [(r, f_r·r)], correção_r, medido, conta corrigida, σ corrigido, z)]."""
    import importlib.util
    import os
    aqui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo")
    spec = importlib.util.spec_from_file_location("rodada39", os.path.join(aqui, "rodada39.py"))
    r39 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r39)
    c = r39.crivo(max(bases) ** 5)
    saida = []
    for b in bases:
        N, div, corr, ex, med, conta, var = r39.base(b, c)
        ps = r39.primos_de(2 * b)
        rs = sorted({r for r in r39.primos_de(b * b + 1) + r39.primos_de(b ** 4 + 1) if r not in ps and r > 13})
        ns = [n for L in (3, 5) for n in r39.palindromos(b, L) if all(n % p for p in ps)]
        cr, det = 1.0, []
        for r in rs:
            k = sum(1 for n in ns if n % r == 0)
            cr = cr * (((len(ns) - k) * r) / (len(ns) * (r - 1)))
            det.append((r, k * r / len(ns)))
        m = ex + med[3] + med[5]
        cc = ex + (conta[3] + conta[5]) * cr
        sg = sqrt(var) * sqrt(cr)
        saida.append((b, det, cr, m, cc, sg, (m - cc) / sg))
    return saida


def p1392_profundidade_e_definicao(d=None, classe="n"):
    """A profundidade e o tamanho da definição (P1392): nos sinsets da classe com profundidade (P793), o Spearman entre a
    profundidade e o número de palavras da definição (sem os exemplos). Devolve (Spearman, sinsets, {profundidade: média de
    palavras} para as profundidades com pelo menos 100 sinsets)."""
    import importlib.util
    import os
    from synthai.dicionario import Dicionario, profundidades
    d = d or Dicionario()
    spec = importlib.util.spec_from_file_location("rodada36", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada36.py"))
    r36 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r36)
    xs, ys, por = [], [], {}
    for i, prof in sorted(profundidades(d).items()):
        if d.sinsets[i][0] != classe:
            continue
        n = len(d.definicao(d.sinsets[i][3]).split())
        xs.append(float(prof))
        ys.append(float(n))
        a, b = por.get(prof, (0, 0))
        por[prof] = (a + n, b + 1)
    rho = r36.pearson(r36.postos(xs), r36.postos(ys))
    return rho, len(xs), {p: a / b for p, (a, b) in sorted(por.items()) if b >= 100}


def p1393_periodo_hex(de=10 ** 4, ate=10 ** 5):
    """O período de 1/p em base 16 (P1393): para os primos p em [de, ate), a média de ord_p(16)/(p − 1) e a de ord_p(2)/(p − 1),
    e a fração com ord_p(16) = (p − 1)/mdc(p − 1, 4) (o maior possível para um quarto poder). ord_p(16) = ord_p(2)/mdc(ord_p(2), 4).
    Devolve (média 16, média 2, fração máxima, primos)."""
    from math import gcd

    def ordem2(p):
        # ord_p(2): o menor divisor e de p − 1 com 2^e ≡ 1 (mod p)
        m, fatores, x = p - 1, [], p - 1
        q = 2
        while q * q <= x:
            if x % q == 0:
                fatores.append(q)
                while x % q == 0:
                    x //= q
            q += 1
        if x > 1:
            fatores.append(x)
        for q in fatores:
            while m % q == 0 and pow(2, m // q, p) == 1:
                m //= q
        return m
    crivo = bytearray([1]) * ate
    crivo[0] = crivo[1] = 0
    for i in range(2, int(ate ** 0.5) + 1):
        if crivo[i]:
            crivo[i * i::i] = bytearray(len(range(i * i, ate, i)))
    s16 = s2 = 0.0
    maximo = n = 0
    for p in range(max(de, 3), ate):
        if not crivo[p]:
            continue
        o2 = ordem2(p)
        o16 = o2 // gcd(o2, 4)
        s16 += o16 / (p - 1)
        s2 += o2 / (p - 1)
        maximo += o16 == (p - 1) // gcd(p - 1, 4)
        n += 1
    return s16 / n, s2 / n, maximo / n, n


def p1421_endereco_da_falta():
    """Rodada 40 (P1421): o endereço da falta de primos palíndromos da base 21 (por primeiro dígito e por dígito do meio, contra a
    conta C reescalada) e as bases 23 a 28 com a conta C (dialogo/rodada40.py, IGUAL em Java). Devolve ({'d0': (qui², gl), 'd2':
    (qui², gl)}, k, [(b, medido, C, σ, z)])."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada40", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada40.py"))
    r40 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r40)
    c = r40.crivo(28 ** 5)
    cl = r40.classes(21, c)
    quis, k = {}, None
    for nome in ("d0", "d2"):
        q, gl, k = r40.qui(cl[nome])
        quis[nome] = (q, gl)
    bases = []
    for b in range(23, 29):
        N, div, corr, ex, med, conta, var = r40.base(b, c)
        m = ex + med[3] + med[5]
        C = ex + conta[3] + conta[5]
        sg = sqrt(var)
        bases.append((b, m, C, sg, (m - C) / sg))
    return quis, k, bases


def p1422_sinonimos_por_classe(d=None):
    """Os sinônimos por classe (P1422): o tamanho médio do sinset (número de lemas) do WordNet por classe e a fração de sinsets de um
    lema só. Devolve ({classe: (tamanho médio, fração de um lema, sinsets)})."""
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    por = {}
    for pos, lemas, _, _ in d.sinsets:
        a, b, u = por.get(pos, (0, 0, 0))
        por[pos] = (a + len(lemas), b + 1, u + (len(lemas) == 1))
    return {c: (a / b, u / b, b) for c, (a, b, u) in sorted(por.items())}


def p1423_mesma_soma_10_16(ate=16 ** 5):
    """A mesma soma em base 10 e em base 16 (P1423): a fração dos n de 1 a ate − 1 com s₁₀(n) = s₁₆(n), e a conta (3 vezes a chance de
    duas somas independentes com as distribuições de 0 a ate − 1, porque s₁₀ ≡ n ≡ s₁₆ (mod 3)). Devolve (fração, conta)."""
    s10 = [0] * ate
    s16 = [0] * ate
    for n in range(1, ate):
        s10[n] = s10[n // 10] + n % 10
        s16[n] = s16[n // 16] + n % 16
    d10, d16 = {}, {}
    for n in range(ate):
        d10[s10[n]] = d10.get(s10[n], 0) + 1
        d16[s16[n]] = d16.get(s16[n], 0) + 1
    ind = sum(d10[k] * d16.get(k, 0) for k in d10) / ate / ate
    iguais = sum(1 for n in range(1, ate) if s10[n] == s16[n])
    return iguais / (ate - 1), 3 * ind


def p1427_bases_29_a_34(bases=range(29, 35)):
    """Os primos palíndromos nas bases 29 a 34 com a conta C da rodada 39 (P1427): o terceiro lote, depois de 17 a 22 (abaixo) e 23 a
    28 (sem viés). Devolve [(b, medido, C, σ, z)]."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada39", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada39.py"))
    r39 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r39)
    c = r39.crivo(max(bases) ** 5)
    saida = []
    for b in bases:
        N, div, corr, ex, med, conta, var = r39.base(b, c)
        m = ex + med[3] + med[5]
        C = ex + conta[3] + conta[5]
        sg = sqrt(var)
        saida.append((b, m, C, sg, (m - C) / sg))
    return saida


def _numero_pt(x):
    """Um número escrito em português (vírgula decimal, ponto de milhar, sinal −, %) como float, ou None."""
    x = x.strip().replace("*", "").replace("−", "-").replace("%", "").replace(" ", "")
    if "," in x:
        x = x.replace(".", "").replace(",", ".")
    elif x.count(".") >= 1 and len(x.split(".")[-1]) == 3 and x.replace(".", "").lstrip("-").isdigit():
        x = x.replace(".", "")
    try:
        return float(x)
    except ValueError:
        return None


def p1452_minhas_previsoes(partes=range(53, 67)):
    """As minhas previsões do mundo, lidas dos documentos (P1452): para cada parte, os vereditos da linha "Do mundo: (a) ✅ (b) ❌ …"
    e, para cada letra, a primeira faixa "**[a; b]**" escrita depois da letra no documento da parte ou na rodada do diálogo dela
    (rodada = parte − 26). Devolve [(parte, letra, a, b, acerto)] com a e b None quando a previsão não tem faixa numérica."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    dialogo = open(os.path.join(raiz, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    faixa = re.compile(r"\(([a-z])\)[^\n]*?\*\*\[([^\];]+?);\s*([^\]]+?)\]\*\*")
    saida = []
    for parte in partes:
        arq = glob.glob(os.path.join(raiz, f"ASI_AGI_parte{parte}_*.md"))
        if not arq:
            continue
        texto = open(arq[0], encoding="utf-8").read()
        m = re.search(r"Do mundo: ((?:\([a-z]\) [✅❌] ?)+)", texto)
        if not m:
            continue
        vered = re.findall(r"\(([a-z])\) ([✅❌])", m.group(1))
        cab = re.search(rf"## Rodada {parte - 26} [^\n]*\n(.*?)(?=\n## |\Z)", dialogo, re.S)
        rodada = cab.group(1) if cab else ""
        corpo = texto.split("## As respostas")[0]
        faixas = {}
        for fonte in (corpo, rodada.split("**Resultado")[0]):
            for letra, a, b in faixa.findall(fonte):
                if letra not in faixas and _numero_pt(a) is not None and _numero_pt(b) is not None:
                    faixas[letra] = (_numero_pt(a), _numero_pt(b))
        for letra, v in vered:
            a, b = faixas.get(letra, (None, None))
            saida.append((parte, letra, a, b, v == "✅"))
    return saida


def p1453_engenharia_das_previsoes(previsoes=None):
    """A engenharia reversa das minhas previsões (P1453), sobre as lidas pela P1452: a largura relativa de cada faixa,
    w = (b − a)/(|a| + |b|), a taxa de acerto por tipo (com faixa, sem faixa) e por terço de w, e um preditor de w (a mediana das
    outras, deixando uma de fora) contra o ingênuo (o w da previsão anterior). Devolve um dicionário."""
    prev = previsoes if previsoes is not None else p1452_minhas_previsoes()
    com = [x for x in prev if x[2] is not None and abs(x[2]) + abs(x[3]) > 0]
    sem = [x for x in prev if x[2] is None]
    ws = [(x[3] - x[2]) / (abs(x[2]) + abs(x[3])) for x in com]

    def mediana(v):
        v = sorted(v)
        n = len(v)
        return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    ordem = sorted(range(len(ws)), key=lambda i: (ws[i], i))
    tercos = [ordem[:len(ordem) // 3], ordem[len(ordem) // 3:2 * len(ordem) // 3], ordem[2 * len(ordem) // 3:]]
    por_terco = [(mediana([ws[i] for i in t]), sum(com[i][4] for i in t) / len(t)) for t in tercos]
    erro_loo = sum(abs(ws[i] - mediana(ws[:i] + ws[i + 1:])) for i in range(len(ws))) / len(ws)
    erro_ing = sum(abs(ws[i] - ws[i - 1]) for i in range(1, len(ws))) / (len(ws) - 1)
    q = sorted(ws)
    return {"previsoes": len(prev), "com_faixa": len(com), "acerto": sum(x[4] for x in prev) / len(prev),
            "acerto_com_faixa": sum(x[4] for x in com) / len(com), "acerto_sem_faixa": sum(x[4] for x in sem) / len(sem),
            "w_mediana": mediana(ws), "w_q25": q[len(q) // 4], "w_q75": q[3 * len(q) // 4], "por_terco": por_terco,
            "erro_loo": erro_loo, "erro_ingenuo": erro_ing,
            "por_parte": {pa: sum(1 for x in prev if x[0] == pa) for pa in sorted({x[0] for x in prev})}}


def p1481_minhas_previsoes_v2(partes=range(53, 68)):
    """As minhas previsões do mundo, versão 2 (P1481; a P1452 fica como está, porque pontuou a Parte 67): a faixa de cada letra pode estar
    em outra linha (as quebras de linha viram espaço) até 400 caracteres depois da letra, sem passar por outra letra entre parênteses; e
    cada faixa ganha um tipo: "zero" (cruza ou toca o zero), "fracao" (dentro de [0; 1]), "contagem" (inteiros ≥ 1) ou "outra". Devolve
    [(parte, letra, a, b, acerto, tipo)]."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    dialogo = open(os.path.join(raiz, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    faixa = re.compile(r"\(([a-z])\)((?:(?!\([a-z]\)).){0,400}?)\*\*\[([^\];]+?);\s*([^\]]+?)\]\*\*")
    saida = []
    for parte in partes:
        arq = glob.glob(os.path.join(raiz, f"ASI_AGI_parte{parte}_*.md"))
        if not arq:
            continue
        texto = open(arq[0], encoding="utf-8").read()
        m = re.search(r"Do mundo: ((?:\([a-z]\) [✅❌] ?)+)", texto)
        if not m:
            continue
        vered = re.findall(r"\(([a-z])\) ([✅❌])", m.group(1))
        cab = re.search(rf"## Rodada {parte - 26} [^\n]*\n(.*?)(?=\n## |\Z)", dialogo, re.S)
        rodada = cab.group(1) if cab else ""
        faixas = {}
        corpo = texto.split("## As respostas")[0]
        corpo = corpo.split("### Sobre o mundo", 1)[1] if "### Sobre o mundo" in corpo else corpo  # fora a tabela sobre mim
        for fonte in (corpo, rodada.split("**Resultado")[0]):
            for letra, _, a, b in faixa.findall(fonte.replace("\n", " ")):
                x, y = _numero_pt(a), _numero_pt(b)
                if x is not None and y is not None and "%" in a + b:  # porcentagem: a faixa é uma fração
                    x, y = x / 100, y / 100
                if letra not in faixas and x is not None and y is not None:
                    faixas[letra] = (x, y)
        for letra, v in vered:
            a, b = faixas.get(letra, (None, None))
            if a is None:
                tipo = None
            elif a <= 0 <= b:
                tipo = "zero"
            elif 0 <= a and b <= 1:
                tipo = "fracao"
            elif a == int(a) and b == int(b) and a >= 1:
                tipo = "contagem"
            else:
                tipo = "outra"
            saida.append((parte, letra, a, b, v == "✅", tipo))
    return saida


def p1482_engenharia_por_tipo(previsoes=None):
    """A engenharia reversa por tipo de quantidade (P1482), sobre a P1481: para cada tipo, o número de previsões, o acerto, a mediana de w =
    (b − a)/(|a| + |b|) (fora o tipo "zero", em que w = 1 sempre) e o acerto das faixas mais estreitas e mais largas que a mediana do tipo.
    Devolve {tipo: (n, acerto, w mediana, acerto das estreitas, acerto das largas)}."""
    prev = previsoes if previsoes is not None else p1481_minhas_previsoes_v2()
    saida = {}
    for tipo in ("zero", "fracao", "contagem", "outra", None):
        xs = [x for x in prev if x[5] == tipo]
        if not xs:
            continue
        acerto = sum(x[4] for x in xs) / len(xs)
        if tipo in (None, "zero"):
            saida[tipo] = (len(xs), acerto, None, None, None)
            continue
        ws = sorted(((x[3] - x[2]) / (abs(x[2]) + abs(x[3])), x[4]) for x in xs)
        n = len(ws)
        med = ws[n // 2][0] if n % 2 else (ws[n // 2 - 1][0] + ws[n // 2][0]) / 2
        estreitas = [h for w, h in ws if w < med]
        largas = [h for w, h in ws if w > med]
        saida[tipo] = (n, acerto, med, sum(estreitas) / len(estreitas) if estreitas else None, sum(largas) / len(largas) if largas else None)
    return saida


def p1491_densidade_da_conta():
    """Rodada 42 (P1491): R_b = π(b⁵)/(Li(b⁵) − Li(2)) nas bases 5 a 40, a conta C corrigida por R_b e a inclinação de z antes e depois
    (dialogo/rodada42.py, IGUAL em Java). Devolve ([(b, π, R_b)], inclinação antes, depois, maior |R_b − 1| nas bases 10 a 40)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada42", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada42.py"))
    r42 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r42)
    c = r42.crivo(40 ** 5)
    li2 = r42.li(2)
    linhas, antes, depois, maior = [], [], [], 0.0
    for b in range(5, 41):
        x = b ** 5
        pi = c[:x].count(1)
        R = pi / (r42.li(x) - li2)
        if b >= 10:
            maior = max(maior, abs(R - 1.0))
        N, div, corr, ex, med, conta, var = r42.base(b, c)
        m = ex + med[3] + med[5]
        s = sqrt(var)
        antes.append((float(b), (m - (ex + conta[3] + conta[5])) / s))
        depois.append((float(b), (m - (ex + (conta[3] + conta[5]) * R)) / (s * sqrt(R))))
        linhas.append((b, pi, R))
    return linhas, r42.reta(antes)[0], r42.reta(depois)[0], maior


def p1492_folhas(d=None):
    """As folhas da taxonomia (P1492): a fração dos sinsets de cada classe que não são hiperônimo de nenhum outro sinset. Devolve
    {classe: (fração, sinsets)}."""
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    pais = set()
    for _, _, hip, _ in d.sinsets:
        for h in hip:
            if h in d.indice:
                pais.add(d.indice[h])
    por = {}
    for i, (pos, _, _, _) in enumerate(d.sinsets):
        a, b = por.get(pos, (0, 0))
        por[pos] = (a + (i not in pais), b + 1)
    return {c: (a / b, b) for c, (a, b) in sorted(por.items())}


def p1493_palindromos_duplos(ate=16 ** 4, b1=16, b2=10):
    """Os palíndromos duplos (P1493): n de 1 a ate − 1 palíndromo nas bases b1 e b2; e a conta com independência, Σ b1^(−⌊L1/2⌋)·b2^(−⌊L2/2⌋).
    Devolve (lista, conta)."""
    achados, conta = [], 0.0
    for n in range(1, ate):
        d1, d2 = _digitos_base(n, b1), _digitos_base(n, b2)
        conta += b1 ** (-(len(d1) // 2)) * b2 ** (-(len(d2) // 2))
        if d1 == d1[::-1] and d2 == d2[::-1]:
            achados.append(n)
    return achados, conta


VOCAB_GPT = list(" abcdefghijklmnopqrstuvwxyz,;()-|?")  # | separa as glosas; ? é qualquer outro caractere


def p1511_corpus_de_glosas(lingua="en"):
    """O corpus de pré-treino da forma de GPT (P1511): as definições do WordNet (en, sem os exemplos) ou as glosas da OpenWordNet-PT
    (pt, sem acentos: NFD e só as letras de base), em minúsculas, com os caracteres fora do vocabulário trocados por '?', unidas por '|'.
    Separação fixa: os sinsets de índice ≡ 0 (mod 10) no teste. Devolve (treino, teste)."""
    import unicodedata
    if lingua == "en":
        from synthai.dicionario import Dicionario
        d = Dicionario()
        glosas = [d.definicao(g) for _, _, _, g in d.sinsets]
    else:
        from synthai.dicionario import DicionarioPT
        pt = DicionarioPT()
        glosas = [pt.glosas[k] for k in sorted(pt.glosas)]
    ok = set(VOCAB_GPT)
    treino, teste = [], []
    for i, g in enumerate(glosas):
        g = "".join(ch for ch in unicodedata.normalize("NFD", g.lower()) if not unicodedata.combining(ch))
        g = "".join(ch if ch in ok and ch != "|" else "?" for ch in g.strip())
        (teste if i % 10 == 0 else treino).append(g)
    return "|".join(treino), "|".join(teste)


def p1512_ngrama_bits(treino, teste, ordem=3, limite=None, V=None):
    """O modelo mais simples (P1512): n-grama de caracteres com interpolação de Witten-Bell, contado em todo o treino; bits por
    caractere no teste (os primeiros `limite` caracteres, ou todos). Devolve bits por caractere."""
    from math import log2
    V = V or len(VOCAB_GPT)  # o tamanho do alfabeto (a base da interpolação é 1/V)
    cont = [{} for _ in range(ordem)]  # cont[k][contexto de k caracteres] = {caractere: contagem}
    for i in range(len(treino)):
        for k in range(ordem):
            if i - k < 0:
                break
            ctx = treino[i - k:i]
            tab = cont[k].setdefault(ctx, {})
            tab[treino[i]] = tab.get(treino[i], 0) + 1
    tot = {k: {c: (sum(t.values()), len(t)) for c, t in cont[k].items()} for k in range(ordem)}
    texto = teste if limite is None else teste[:limite]
    bits = 0.0
    for i in range(len(texto)):
        p = 1.0 / V
        for k in range(ordem):
            if i - k < 0:
                break
            ctx = texto[i - k:i]
            if ctx not in cont[k]:
                break
            n, tipos = tot[k][ctx]
            lam = n / (n + tipos)
            p = lam * cont[k][ctx].get(texto[i], 0) / n + (1 - lam) * p
        bits -= log2(p)
    return bits / len(texto)


def p1514_pi_hex_digitos(n=10000):
    """Os n primeiros dígitos hexadecimais de π depois da vírgula, exatos (Machin em inteiros: π = 16 arctg(1/5) − 4 arctg(1/239)),
    como texto '243f6a88…' (P1514)."""
    bits = 4 * n + 64
    um = 1 << bits

    def arctg_inv(x):
        soma, termo, k, sinal = 0, um // x, 1, 1
        while termo:
            soma += sinal * (termo // k)
            termo //= x * x
            k += 2
            sinal = -sinal
        return soma
    frac = 16 * arctg_inv(5) - 4 * arctg_inv(239) - 3 * um
    saida = []
    for _ in range(n):
        frac *= 16
        saida.append("0123456789abcdef"[frac >> bits])
        frac &= um - 1
    return "".join(saida)


def p1515_bits_hex(texto, ordem=3, corte=0.9):
    """Bits por dígito de um n-grama (P1512, alfabeto de 16) treinado nos primeiros 90% de uma sequência hexadecimal e medido nos últimos 10%:
    4 bits é o acaso; abaixo de 4, estrutura; acima, o custo de aprender o que não existe. Devolve bits por dígito."""
    k = int(len(texto) * corte)
    return p1512_ngrama_bits(texto[:k], texto[k:], ordem, V=16)


def p1513_gpt_bits(treino, teste, passos=8000, T=24, d=24, h=48, lr=0.005, semente=69, janelas=400):
    """A forma de GPT (P1513): o GPT mínimo de `synthai.gpt` pré-treinado no treino (janelas sorteadas, semente fixa) e medido no teste
    (as primeiras `janelas` janelas de T caracteres). Devolve (bits por caractere no teste, parâmetros, média das últimas 200 perdas em bits,
    o modelo)."""
    from math import log
    from synthai.gpt import GPT
    g = GPT(VOCAB_GPT, T=T, d=d, h=h, semente=semente)
    perdas = g.treinar(treino, passos=passos, lr=lr, semente=semente)
    n = sum(len(v) * len(v[0]) for v in g.p.values())
    return g.bits_por_caractere(teste, janelas=janelas), n, sum(perdas[-200:]) / 200 / log(2), g


def p1516_gpt_decide():
    """Rodada 43 (P1516): o GPT pequeno pré-treinado (dialogo/rodada43.py) decide o próximo caractere da frase, com exp e log próprios (IGUAL em
    Java). Devolve (decisões [(t, contexto, argmax, p do argmax, p do real)], acertos do argmax, bits por caractere)."""
    import importlib.util
    import os
    import tempfile
    spec = importlib.util.spec_from_file_location("rodada43", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada43.py"))
    r43 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r43)
    with tempfile.TemporaryDirectory() as pasta:
        r43.preparar(pasta)
        saida, bits = r43.decisoes(*r43.ler(pasta))
    return saida, sum(1 for x in saida if x[3] == x[4]), bits / len(saida)


def p1541_escala_gpt(lingua="en", d=24, marcos=(1000, 2000, 4000, 8000, 16000), T=24, lr=0.005, semente=70, janelas=400):
    """A curva de escala da forma de GPT (P1541): um GPT (T, d, h = 2d) treinado em etapas, com os bits por caractere no teste medidos em cada
    marco de passos (cada etapa sorteia janelas com a semente + o número da etapa; o estado do Adam continua). Devolve ([(passos, bits)], pesos, o modelo)."""
    from synthai.gpt import GPT
    treino, teste = p1511_corpus_de_glosas(lingua)
    g = GPT(VOCAB_GPT, T=T, d=d, h=2 * d, semente=semente)
    feitos, pontos = 0, []
    for k, m in enumerate(marcos):
        g.treinar(treino, passos=m - feitos, lr=lr, semente=semente + k)
        feitos = m
        pontos.append((m, g.bits_por_caractere(teste, janelas=janelas)))
    return pontos, sum(len(v) * len(v[0]) for v in g.p.values()), g


def p1542_lei_de_potencia(pontos, alvo=None):
    """A lei de potência bits = A·n^(−α) ajustada por mínimos quadrados em log-log, em forma fechada (as equações normais da reta
    ln bits = ln A − α ln n) (P1542). Com `alvo`, o n em que a reta cruza o alvo: n* = (A/alvo)^(1/α). Devolve (A, α, n*)."""
    from math import exp, log
    xs = [log(n) for n, _ in pontos]
    ys = [log(b) for _, b in pontos]
    k = len(xs)
    mx, my = sum(xs) / k, sum(ys) / k
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    inclinacao = sxy / sxx
    A = exp(my - inclinacao * mx)
    alfa = -inclinacao
    n_alvo = (A / alvo) ** (1 / alfa) if alvo is not None and alfa > 0 else None
    return A, alfa, n_alvo


def p1543_geometria_dos_embeddings(g):
    """A geometria dos embeddings de um GPT (P1543): o cosseno médio entre as vogais (a, e, i, o, u: 10 pares), entre vogais e consoantes (5 × 21
    pares) e entre as consoantes; e a fração da variância na primeira componente principal dos embeddings das 26 letras (a matriz de
    covariância 24×24, autovalor dominante por iteração de potência, conferido pelo traço). Devolve (vogais, vogal-consoante, consoantes, fração)."""
    from math import sqrt
    E = g.p["E"]
    idx = g.indice
    vog = [idx[c] for c in "aeiou"]
    con = [idx[c] for c in "bcdfghjklmnpqrstvwxyz"]

    def cos(a, b):
        x, y = E[a], E[b]
        return sum(u * v for u, v in zip(x, y)) / sqrt(sum(u * u for u in x) * sum(v * v for v in y))

    def media(pares):
        return sum(cos(a, b) for a, b in pares) / len(pares)
    vv = media([(vog[i], vog[j]) for i in range(5) for j in range(i + 1, 5)])
    vc = media([(a, b) for a in vog for b in con])
    cc = media([(con[i], con[j]) for i in range(len(con)) for j in range(i + 1, len(con))])
    letras = vog + con
    d = len(E[0])
    mu = [sum(E[a][i] for a in letras) / len(letras) for i in range(d)]
    X = [[E[a][i] - mu[i] for i in range(d)] for a in letras]
    C = [[sum(x[i] * x[j] for x in X) / len(X) for j in range(d)] for i in range(d)]
    v = [1.0] * d
    lam = 0.0
    for _ in range(500):
        w = [sum(C[i][j] * v[j] for j in range(d)) for i in range(d)]
        nw = sqrt(sum(x * x for x in w))
        v = [x / nw for x in w]
        lam = nw
    traco = sum(C[i][i] for i in range(d))
    return vv, vc, cc, lam / traco


def p1544_delta_de_gromov(classe="n", quadruplos=500, semente=70, d=None):
    """O δ de Gromov da taxonomia (P1544): no grafo não dirigido dos hiperônimos da classe (a maior componente conexa), para quádruplos (x, y, z, w)
    sorteados (semente fixa), δ = (maior − segunda maior das somas d(x,y)+d(z,w), d(x,z)+d(y,w), d(x,w)+d(y,z))/2, com as distâncias por busca em
    largura. Numa árvore, δ = 0 sempre; a herança múltipla é o que o afasta de zero. Devolve (máximo, média, fração com δ > 0, nós da componente,
    diâmetro médio amostrado)."""
    import random
    from collections import deque
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    viz = {}
    for i, (pos, _, hip, _) in enumerate(d.sinsets):
        if pos != classe:
            continue
        viz.setdefault(i, set())
        for h in hip:
            if h in d.indice and d.sinsets[d.indice[h]][0] == classe:
                j = d.indice[h]
                viz[i].add(j)
                viz.setdefault(j, set()).add(i)

    def bfs(o):
        dist = {o: 0}
        fila = deque([o])
        while fila:
            u = fila.popleft()
            for w in viz[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1
                    fila.append(w)
        return dist
    vistos, maior = set(), []
    for o in sorted(viz):
        if o in vistos:
            continue
        comp = bfs(o)
        vistos.update(comp)
        if len(comp) > len(maior):
            maior = sorted(comp)
    r = random.Random(semente)
    deltas, dists = [], []
    for _ in range(quadruplos):
        x, y, z, w = r.sample(maior, 4)
        dx, dy, dz = bfs(x), bfs(y), bfs(z)
        somas = sorted([dx[y] + dz[w], dx[z] + dy[w], dx[w] + dy[z]])
        deltas.append((somas[2] - somas[1]) / 2)
        dists.append(dx[y])
    return max(deltas), sum(deltas) / len(deltas), sum(1 for x in deltas if x > 0) / len(deltas), len(maior), sum(dists) / len(dists)


def p1545_bases_gf2(texto):
    """Os dígitos hexadecimais como vetores de GF(2)⁴ (P1545): a fração das janelas de 4 dígitos consecutivos que formam uma base de GF(2)⁴ (posto 4,
    por eliminação de Gauss sobre GF(2): ou exclusivo de bits); e a fração teórica para dígitos independentes e uniformes, |GL(4, 2)|/16⁴ =
    (16 − 1)(16 − 2)(16 − 4)(16 − 8)/16⁴. Devolve (fração medida, fração teórica, janelas)."""
    def posto(vs):
        vs = list(vs)
        p = 0
        for bit in (8, 4, 2, 1):
            piv = next((i for i in range(p, len(vs)) if vs[i] & bit), None)
            if piv is None:
                continue
            vs[p], vs[piv] = vs[piv], vs[p]
            for i in range(len(vs)):
                if i != p and vs[i] & bit:
                    vs[i] ^= vs[p]
            p += 1
        return p
    ds = [int(ch, 16) for ch in texto]
    janelas = len(ds) - 3
    bases = sum(1 for i in range(janelas) if posto(ds[i:i + 4]) == 4)
    return bases / janelas, (15 * 14 * 12 * 8) / 16 ** 4, janelas


def p1549_lei_de_escala():
    """Rodada 44 (P1549): a lei de escala da forma de GPT por mínimos quadrados em forma fechada (dialogo/rodada44.py, IGUAL em Java), lida dos pontos
    medidos e guardados em dialogo/escala44.tsv. Devolve ({d: (A, α, n*)}, bits(d=48) − bits(d=24) em 8.000 passos, os pontos)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada44", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada44.py"))
    r44 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r44)
    pontos = r44.ler()
    return {d: r44.ajuste(pontos[d]) for d in sorted(pontos)}, dict(pontos[48])[8000] - dict(pontos[24])[8000], pontos


def p1550_contas_da_parte70(medida_gf2=None, janelas=9997):
    """As contas auxiliares da Parte 70 (P1550): o desvio binomial de uma proporção p = |GL(4,2)|/16⁴ com `janelas` janelas, e quantos desvios a medida
    de π (P1545) fica da teoria (com o desvio simples e com o dobro, pelas janelas sobrepostas). Devolve (p, desvio, z simples, z com o dobro)."""
    if medida_gf2 is None:
        medida_gf2 = p1545_bases_gf2(p1514_pi_hex_digitos(10000))[0]
    p = 20160 / 65536
    sd = sqrt(p * (1 - p) / janelas)
    return p, sd, (medida_gf2 - p) / sd, (medida_gf2 - p) / (2 * sd)


def p1571_autovalores_jacobi(S, varreduras=60):
    """Os autovalores de uma matriz simétrica pelo método de Jacobi clássico (P1571): rotações de Givens que zeram, em ordem fixa (p < q, linha por
    linha), cada elemento fora da diagonal; tan θ = sinal(τ)/(|τ| + √(τ² + 1)), τ = (S_qq − S_pp)/(2 S_pq). Só + − × ÷ e √ (o IEEE 754 arredonda
    todas corretamente: a tradução para Java é exata). Devolve os autovalores em ordem decrescente."""
    from math import sqrt as raiz
    n = len(S)
    A = [list(linha) for linha in S]
    for _ in range(varreduras):
        fora = 0.0
        for p in range(n):
            for q in range(p + 1, n):
                fora += A[p][q] * A[p][q]
        if fora == 0.0:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if A[p][q] == 0.0:
                    continue
                tau = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if tau >= 0.0 else -1.0) / (abs(tau) + raiz(tau * tau + 1.0))
                c = 1.0 / raiz(t * t + 1.0)
                s_ = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s_ * akq
                    A[k][q] = s_ * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s_ * aqk
                    A[q][k] = s_ * apk + c * aqk
    return sorted((A[i][i] for i in range(n)), reverse=True)


def p1572_participacao(M):
    """Quantas direções uma matriz usa (P1572): os valores singulares σ_i de M (as raízes dos autovalores de MᵀM, por Jacobi, P1571); a razão de
    participação PR = (Σ σ_i²)²/Σ σ_i⁴ (entre 1, uma direção só, e d, todas iguais) e a fração de Σσ² no maior. Para uma matriz gaussiana d×d ao
    acaso, PR ≈ d/2 (a lei do quarto de círculo: E σ² = d, E σ⁴ = 2d²). Devolve (PR, fração do maior, σ² em ordem decrescente)."""
    n, m = len(M), len(M[0])
    MtM = [[sum(M[k][i] * M[k][j] for k in range(n)) for j in range(m)] for i in range(m)]
    lam = [max(0.0, x) for x in p1571_autovalores_jacobi(MtM)]
    s2 = sum(lam)
    s4 = sum(x * x for x in lam)
    return s2 * s2 / s4, lam[0] / s2, lam


def p1573_crescimento_da_taxonomia(classe="n", ate=8, d=None):
    """A geometria do crescimento da taxonomia (P1573): o número de sinsets da classe em cada profundidade (P793) e a taxa de crescimento por nível,
    pela reta de mínimos quadrados de ln N(r) contra r nas profundidades 1 a `ate` (num espaço hiperbólico, N(r) cresce como e^{λr}; num euclidiano de
    dimensão k, como r^{k−1}). Devolve (fator por nível e^λ, {r: N(r)}, o r de N máximo)."""
    from math import exp, log
    from synthai.dicionario import Dicionario, profundidades
    d = d or Dicionario()
    por = {}
    for i, r in profundidades(d).items():
        if d.sinsets[i][0] == classe:
            por[r] = por.get(r, 0) + 1
    pts = [(r, log(por[r])) for r in range(1, ate + 1) if por.get(r)]
    k = len(pts)
    mx, my = sum(x for x, _ in pts) / k, sum(y for _, y in pts) / k
    lam = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    return exp(lam), dict(sorted(por.items())), max(por, key=por.get)


def p1574_irredutiveis_gf2(grau=15, mascara=6):
    """Os números hexadecimais como polinômios sobre GF(2) (P1574): os polinômios de grau `grau` (bit mais alto = grau) irredutíveis, contados por
    divisão por todos os irredutíveis de grau ≤ grau/2 (crivo de polinômios), contra a fórmula de Gauss N(n) = (1/n) Σ_{d|n} μ(d) 2^{n/d}; e os
    "gêmeos" (f, f ⊕ máscara), os dois irredutíveis, contra a conta heurística N²/2^(grau−1)/2 (a chance de o vizinho de um irredutível ser irredutível,
    se fossem independentes). Com máscara = 2 (f ⊕ x), não há gêmeos: um irredutível de grau > 1 tem um número ímpar de termos (senão x + 1 o divide),
    e trocar um coeficiente troca a paridade. Por isso o padrão é máscara = 6 (f ⊕ x ⊕ x², que mantém a paridade e o termo constante).
    Devolve (irredutíveis, Gauss, gêmeos, conta dos gêmeos)."""
    def mod(a, b):
        db = b.bit_length()
        while a.bit_length() >= db:
            a ^= b << (a.bit_length() - db)
        return a

    irred = {1: [2, 3]}
    for g in range(2, grau // 2 + 1):
        irred[g] = [f for f in range(1 << g, 1 << (g + 1))
                    if all(mod(f, h) for k in range(1, g // 2 + 1) for h in irred[k])]
    peq = [h for k in range(1, grau // 2 + 1) for h in irred[k]]
    conj = {f for f in range(1 << grau, 1 << (grau + 1)) if all(mod(f, h) for h in peq)}

    def mobius(n):
        r, k, p = 1, n, 2
        while p * p <= k:
            if k % p == 0:
                k //= p
                if k % p == 0:
                    return 0
                r = -r
            p += 1
        return -r if k > 1 else r
    gauss = sum(mobius(dd) * 2 ** (grau // dd) for dd in range(1, grau + 1) if grau % dd == 0) // grau
    gemeos = sum(1 for f in conj if (f ^ mascara) in conj and f < (f ^ mascara))
    return len(conj), gauss, gemeos, len(conj) ** 2 / 2 ** (grau - 1) / 2


def p1579_serie_singular_gf2(grau, ate=40):
    """A conta dos gêmeos (f, f ⊕ x ⊕ x²) pela série singular (a heurística de Hardy–Littlewood/Bateman–Horn em F₂[x]) (P1579): para cada irredutível p
    de grau k, a chance de p não dividir nenhum dos dois, dividida pela chance se fossem independentes: (1 − ν_p/2^k)/(1 − 1/2^k)², com ν_p = 1 quando
    x + x² ≡ 0 mod p (p = x e p = x + 1: fator 2 cada, a paridade e o termo constante) e ν_p = 2 nos outros (p = x² + x + 1: fator 8/9). O número de
    irredutíveis de cada grau k vem da fórmula de Gauss. Devolve (S, a conta N²/2^grau · S/2 com N de Gauss)."""
    def mobius(n):
        r, k, q = 1, n, 2
        while q * q <= k:
            if k % q == 0:
                k //= q
                if k % q == 0:
                    return 0
                r = -r
            q += 1
        return -r if k > 1 else r

    def gauss(n):
        return sum(mobius(dd) * 2 ** (n // dd) for dd in range(1, n + 1) if n % dd == 0) // n
    serie = 2.0 * 2.0
    for k in range(2, ate + 1):
        serie *= ((1 - 2 / 2 ** k) / (1 - 1 / 2 ** k) ** 2) ** gauss(k)
    n = gauss(grau)
    return serie, n * n / 2 ** grau * serie / 2


def p1601_auditoria_do_repositorio(ate=71):
    """A auditoria pedida na Parte 72 ("corrija tudo pra ver se há coisas inadequadas e disfuncionais") (P1601). Devolve um dicionário de listas de
    defeitos: "docs" (partes 1..ate sem documento ASI_AGI_parteN_*.md, ou cujo documento não liga para a parte seguinte, até ate − 1), "sem_teste"
    (pNN de P1031 em diante sem teste pelo nome, pela p1092), "testes_fora_da_lista" (synthai/testes*.py que o CLAUDE.md não lista), "rodadas_sem_java"
    (dialogo/rodadaNN.py sem RodadaNN.java), "partes_fora_do_resultados" (partes sem a linha "--- Parte N " no resultados.txt; a Parte 1, sem
    cabeçalho, é o começo do arquivo) e "constantes" (pares
    ERROS_PNN, TESTES_PNN fora de ordem: testes que diminuem, erros que diminuem ou erros > testes)."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    ler = lambda nome: open(os.path.join(raiz, nome), encoding="utf-8").read()
    defeitos = {}
    docs = {int(re.match(r"ASI_AGI_parte(\d+)_", os.path.basename(f)).group(1)): f
            for f in glob.glob(os.path.join(raiz, "ASI_AGI_parte*_*.md"))}
    docs[1] = os.path.join(raiz, "ASI_AGI_perguntas_e_respostas.md")  # a Parte 1 tem outro nome (a forma verificada antes de contar, Parte 31)
    ruins = []
    for n in range(1, ate + 1):
        if n not in docs:
            ruins.append((n, "sem documento"))
        elif n < ate and (n + 1) in docs and os.path.basename(docs[n + 1]) not in open(docs[n], encoding="utf-8").read():
            ruins.append((n, "sem link para a parte %d" % (n + 1)))
    defeitos["docs"] = ruins
    codigo = ler("calculos.py")
    ultimo = max(int(x) for x in re.findall(r"^def p(\d+)_", codigo, re.M))
    defeitos["sem_teste"] = p1092_pnn_sem_teste(1031, ultimo)[1]
    claude = ler("CLAUDE.md")
    defeitos["testes_fora_da_lista"] = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(raiz, "synthai", "testes*.py"))
                                              if "synthai." + os.path.basename(f)[:-3] + " " not in claude.replace("`", " ").replace("\n", " "))
    pastad = os.path.join(raiz, "dialogo")
    defeitos["rodadas_sem_java"] = sorted(os.path.basename(f) for f in glob.glob(os.path.join(pastad, "rodada[0-9]*.py"))
                                          if not os.path.exists(os.path.join(pastad, "R" + os.path.basename(f)[1:-3] + ".java")))
    res = ler("resultados.txt")
    # a Parte 1 não imprime cabeçalho: é o que vem antes da linha da Parte 2 e começa pela P3
    defeitos["partes_fora_do_resultados"] = [n for n in range(1, ate + 1) if ("--- Parte %d " % n not in res if n > 1 else not res.startswith("P3 "))]
    pares = sorted((int(a), int(b), int(c)) for a, b, c in re.findall(r"^ERROS_P(\d+), TESTES_P\1 = (\d+), (\d+)", codigo, re.M))
    defeitos["constantes"] = [(pares[i][0], pares[i][1:], pares[i - 1][1:]) for i in range(1, len(pares))
                              if pares[i][2] < pares[i - 1][2] or pares[i][1] < pares[i - 1][1] or pares[i][1] > pares[i][2]]
    return defeitos


def p1602_entropia_de_unigrama(texto):
    """A conta do texto recebido na Parte 72 (P1602): a entropia de Shannon por símbolo, H = −Σ p log₂ p, e a redundância 1 − H/H_max contra duas
    referências: log₂ do número de símbolos que aparecem (a definição de Shannon) e 8 bits (um byte: a que reproduz os 48,63% do texto, com H = 4,11).
    Devolve (H, símbolos, redundância contra o alfabeto, redundância contra 8 bits)."""
    import math
    from collections import Counter
    cont = Counter(texto)
    n = len(texto)
    h = 0.0
    for c in sorted(cont):
        p = cont[c] / n
        h -= p * math.log2(p)
    return h, len(cont), 1 - h / math.log2(len(cont)), 1 - h / 8


def p1603_ciclos_de_glosas(pares=(("knowledge", "information"), ("meaning", "word")), d=None):
    """Os "ciclos autorreferentes" do texto recebido, conferidos no WordNet (P1603): para cada par (A, B), se A aparece (como palavra exata) na glosa de
    algum sinset em que B é lema, e B na de algum sinset em que A é lema. Devolve [(A, B, A na glosa de B, B na glosa de A)]."""
    import re
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    palavras = {}
    for s in d.sinsets:
        ws = set(re.findall(r"[a-z]+", d.definicao(s[3]).lower()))
        for lema in s[1]:
            palavras.setdefault(lema.lower(), set()).update(ws)
    return [(a, b, a in palavras.get(b, set()), b in palavras.get(a, set())) for a, b in pares]


def p1604_hash_como_peso(n=2000, semente=72, d=None):
    """O hash como "peso" (P1604; afirmação do texto recebido na Parte 72): h(w) = SHA-256(w) lido como inteiro / 2²⁵⁶. Compara a média de |h(a) − h(b)|
    entre sinônimos (os dois primeiros lemas de sinsets sorteados com dois lemas ou mais) e entre pares de lemas sorteados. Para U, V uniformes
    independentes, E|U − V| = 1/3 e Var|U − V| = 1/18. Devolve (média dos sinônimos, média dos sorteados, z da diferença)."""
    import hashlib
    import math
    import random
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    h = lambda w: int(hashlib.sha256(w.encode("utf-8")).hexdigest(), 16) / 2 ** 256
    r = random.Random(semente)
    com_dois = [s[1] for s in d.sinsets if len(s[1]) >= 2]
    lemas = sorted({l for s in d.sinsets for l in s[1]})
    sin = [r.choice(com_dois) for _ in range(n)]
    ms = sum(abs(h(x[0]) - h(x[1])) for x in sin) / n
    mr = sum(abs(h(r.choice(lemas)) - h(r.choice(lemas))) for _ in range(n)) / n
    return ms, mr, (ms - mr) / math.sqrt(2 / 18 / n)


def p1608_auditoria_estatica(caminho="externos/texto_recebido_parte72b.md"):
    """A auditoria estática do código de um texto recebido (P1608): cada bloco ```python é lido pela árvore sintática (ast.parse analisa, não executa).
    Para cada função de nome test*/run_tests, conta as verificações: cada `assert` e cada `raise AssertionError` (o padrão "try: operação inválida;
    raise AssertionError; except ...") vale 1, multiplicado pelo tamanho das listas literais dos `for` que o envolvem (um `for` sobre uma coleção
    calculada em tempo de execução conta 1). E lê os números que a função devolve fixos num dicionário literal (chaves "tests", "tests_passed").
    Devolve [(função, verificações, nós assert, declarado)]."""
    import ast
    import os
    import re
    texto = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho), encoding="utf-8").read()
    saida = []
    for bloco in re.findall(r"```python\n(.*?)```", texto, re.S):
        arvore = ast.parse(bloco)
        for f in [n for n in ast.walk(arvore) if isinstance(n, ast.FunctionDef) and (n.name.startswith("test") or n.name == "run_tests")]:
            pais = {}
            for no in ast.walk(f):
                for filho in ast.iter_child_nodes(no):
                    pais[filho] = no
            verif = asserts = 0
            for no in ast.walk(f):
                e_raise = (isinstance(no, ast.Raise) and isinstance(no.exc, ast.Call) and isinstance(no.exc.func, ast.Name)
                           and no.exc.func.id == "AssertionError")
                if not (isinstance(no, ast.Assert) or e_raise):
                    continue
                asserts += isinstance(no, ast.Assert)
                mult, q = 1, pais.get(no)
                while q is not None:
                    if isinstance(q, ast.For) and isinstance(q.iter, (ast.List, ast.Tuple)):
                        mult *= len(q.iter.elts)
                    q = pais.get(q)
                verif += mult
            declarado = None
            for no in ast.walk(f):
                if isinstance(no, ast.Return) and isinstance(no.value, ast.Dict):
                    for k, v in zip(no.value.keys, no.value.values):
                        if isinstance(k, ast.Constant) and k.value in ("tests", "tests_passed") and isinstance(v, ast.Constant):
                            declarado = v.value
            saida.append((f.name, verif, asserts, declarado))
    return saida


def p1609_horn_linear(fatos, regras):
    """O motor de Horn em tempo linear (P1609; Dowling e Gallier, 1984), a otimização que o texto recebido na Parte 72 deixou para depois: cada regra
    (premissas, conclusão) guarda quantas premissas distintas faltam; cada átomo guarda as regras em que é premissa; uma fila FIFO dos átomos recém-
    conhecidos decrementa os contadores, e a regra que chega a zero dispara (se a conclusão for nova). Custo O(|fatos| + Σ|premissas|). Devolve
    (ordem de derivação, prova {conclusão: índice da regra, ou None para os fatos}, decrementos)."""
    from collections import deque
    falta, vigia = [], {}
    for r, (prem, _) in enumerate(regras):
        distintas = []
        for a in prem:
            if a not in distintas:
                distintas.append(a)
        falta.append(len(distintas))
        for a in distintas:
            vigia.setdefault(a, []).append(r)
    prova, ordem, fila = {}, [], deque()
    for a in fatos:
        if a not in prova:
            prova[a] = None
            ordem.append(a)
            fila.append(a)
    dec = 0
    for r, (prem, concl) in enumerate(regras):  # regras sem premissa são fatos
        if falta[r] == 0 and concl not in prova:
            prova[concl] = r
            ordem.append(concl)
            fila.append(concl)
    while fila:
        a = fila.popleft()
        for r in vigia.get(a, ()):
            falta[r] -= 1
            dec += 1
            concl = regras[r][1]
            if falta[r] == 0 and concl not in prova:
                prova[concl] = r
                ordem.append(concl)
                fila.append(concl)
    return ordem, prova, dec


def p1610_horn_ingenuo(fatos, regras):
    """O laço do texto recebido na Parte 72, reescrito por mim (P1610): repetir a passagem por todas as regras até nada mudar. Devolve (conhecidos,
    passagens contando a última, que não muda nada, checagens de premissa)."""
    conhecidos = set(fatos)
    passagens = checagens = 0
    mudou = True
    while mudou:
        mudou = False
        passagens += 1
        for prem, concl in regras:
            if concl in conhecidos:
                continue
            ok = True
            for a in prem:
                checagens += 1
                if a not in conhecidos:
                    ok = False
                    break
            if ok:
                conhecidos.add(concl)
                mudou = True
    return conhecidos, passagens, checagens


def p1611_regras_de_animal(d=None):
    """As regras de Horn do dicionário (P1611): para cada substantivo c e cada hiperônimo substantivo p dele, a regra "p é animal ⇒ c é animal"
    (átomos = índices de sinsets), na ordem do arquivo; e o fato "animal (o primeiro sentido de substantivo) é animal". Devolve (fatos, regras)."""
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    animal = min(i for i in d.lemas["animal"] if d.sinsets[i][0] == "n")
    regras = []
    for c, s in enumerate(d.sinsets):
        if s[0] != "n":
            continue
        for h in s[2]:
            if h.startswith("n:") and h in d.indice:
                regras.append(((d.indice[h],), c))
    return [animal], regras


def p1612_animais_por_horn(d=None):
    """O fecho de "é animal" por três métodos (P1612): o motor linear (P1609), o laço do texto (P1610) e uma busca em largura pelos hipônimos.
    Devolve (derivados, linear = BFS, ingênuo = BFS, passagens do ingênuo, checagens do ingênuo, decrementos do linear, regras)."""
    from collections import deque
    fatos, regras = p1611_regras_de_animal(d)
    ordem, prova, dec = p1609_horn_linear(fatos, regras)
    ing, passagens, checagens = p1610_horn_ingenuo(fatos, regras)
    filhos = {}
    for (p,), c in regras:
        filhos.setdefault(p, []).append(c)
    vistos, fila = {fatos[0]}, deque(fatos)
    while fila:
        a = fila.popleft()
        for c in filhos.get(a, ()):
            if c not in vistos:
                vistos.add(c)
                fila.append(c)
    return len(ordem), set(ordem) == vistos, ing == vistos, passagens, checagens, dec, len(regras)


def p1613_fecho_horn(palavra, d=None):
    """O fecho de Horn "é <palavra>" (P1613): o motor linear (P1609) nas regras da hiperonímia (P1611), a partir do primeiro sentido de substantivo
    da palavra. Devolve o número de sinsets derivados (a palavra incluída)."""
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    _, regras = p1611_regras_de_animal(d)
    fato = min(i for i in d.lemas[palavra] if d.sinsets[i][0] == "n")
    return len(p1609_horn_linear([fato], regras)[0])


def p1614_rodada46():
    """Rodada 46 (P1614): o motor de Horn linear do dialogo/rodada46.py nos fatos animal e pessoa (IGUAL em Java). Devolve
    [(fato, derivados, controle da ordem, decrementos, cadeia de prova)]."""
    import importlib.util
    import os
    import tempfile
    spec = importlib.util.spec_from_file_location("rodada46", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada46.py"))
    r46 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r46)
    with tempfile.TemporaryDirectory() as pasta:
        r46.preparar(pasta)
        fatos, regras = r46.ler(pasta)
        return [(f,) + r46.horn(f, regras) for f in fatos]


def p1615_imports_sem_uso(caminho="externos/texto_recebido_parte72b.md"):
    """Os nomes importados e nunca usados em cada bloco ```python de um texto recebido (P1615), pela árvore sintática (sem executar). Devolve uma lista
    por bloco."""
    import ast
    import os
    import re
    texto = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho), encoding="utf-8").read()
    saida = []
    for bloco in re.findall(r"```python\n(.*?)```", texto, re.S):
        arvore = ast.parse(bloco)
        importados = {a.asname or a.name for n in ast.walk(arvore) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names}
        usados = {n.id for n in ast.walk(arvore) if isinstance(n, ast.Name)}
        saida.append(sorted(importados - usados))
    return saida


def p1631_comparar_reenvio(novo="externos/texto_recebido_parte73.md", guardado="externos/texto_recebido_parte72b.md"):
    """A regra da Parte 50 para um texto reenviado (P1631): cada bloco ```python do texto novo é comparado com os blocos da cópia guardada. Devolve
    [(índice do bloco novo, índice do bloco guardado idêntico ou None, número de linhas)]."""
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    blocos = lambda f: re.findall(r"```python\n(.*?)```", open(os.path.join(raiz, f), encoding="utf-8").read(), re.S)
    velhos = blocos(guardado)
    return [(i, next((j for j, v in enumerate(velhos) if v == b), None), b.count("\n")) for i, b in enumerate(blocos(novo))]


def p1633_disjuncoes(classes, d=None, regras=None):
    """O motor de contradições (P1633; o Módulo 004 do texto recebido na Parte 73): um axioma de disjunção entre classes irmãs ("nada é ao mesmo tempo
    A e B") é a metade que falta de uma implicação (a lição da Parte 39). Para cada classe (um índice de sinset), o fecho de Horn dos hipônimos
    (P1609 nas regras da P1611); para cada par, os sinsets que caem nos dois fechos, isto é, as violações da disjunção. Devolve
    {(a, b): [sinsets nos dois]} para os pares a < b da lista."""
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    if regras is None:
        regras = p1611_regras_de_animal(d)[1]
    fechos = {c: set(p1609_horn_linear([c], regras)[0]) for c in classes}
    saida = {}
    for i, a in enumerate(classes):
        for b in classes[i + 1:]:
            saida[(a, b)] = sorted(fechos[a] & fechos[b])
    return saida


def p1634_irmaos(sinset, d=None):
    """Os hipônimos diretos de um sinset de substantivo (P1634), na ordem do arquivo (os candidatos a classes irmãs disjuntas)."""
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    alvo = "n:" + next(k[2:] for k, v in d.indice.items() if v == sinset and k.startswith("n:"))
    return [i for i, s in enumerate(d.sinsets) if s[0] == "n" and alvo in s[2]]


def p1632_prioridade_contra_voi(n=2000, semente=73):
    """A prioridade de perguntas do texto recebido na Parte 73, S(q) = U + I + T, contra o valor da informação perfeita (P1632). n problemas com 2
    ações e 2 estados: prior p ~ U(0, 1), utilidades u[a][s] ~ U(0, 1), semente fixa; a pergunta é observar o estado.
    VOI = p·max_a u[a][1] + (1 − p)·max_a u[a][0] − max_a (p·u[a][1] + (1 − p)·u[a][0]) (só + − × ÷: IGUAL em Java, rodada 47);
    U = entropia binária de p (log₂ pelo log_ próprio da rodada 26, para a tradução bit a bit), I = max_s |u[0][s] − u[1][s]|, T = 1.
    Devolve (fração com VOI = 0, fração com VOI = 0 entre os 10% de maior S, correlação de postos de Spearman entre S e VOI, lista (S, VOI))."""
    import random
    from dialogo.rodada26 import log_
    r = random.Random(semente)
    ln2 = log_(2.0)
    pares = []
    for _ in range(n):
        p = r.random()
        u = [[r.random(), r.random()], [r.random(), r.random()]]
        com = p * max(u[0][1], u[1][1]) + (1.0 - p) * max(u[0][0], u[1][0])
        sem = max(p * u[0][1] + (1.0 - p) * u[0][0], p * u[1][1] + (1.0 - p) * u[1][0])
        voi = com - sem
        if voi < 0.0:
            voi = 0.0
        h = 0.0
        for q in (p, 1.0 - p):
            if q > 0.0:
                h -= q * log_(q) / ln2
        imp = max(abs(u[0][0] - u[1][0]), abs(u[0][1] - u[1][1]))
        pares.append((h + imp + 1.0, voi))
    zero = sum(1 for _, v in pares if v == 0.0) / n
    topo = sorted(pares, key=lambda x: -x[0])[: n // 10]
    zero_topo = sum(1 for _, v in topo if v == 0.0) / len(topo)

    def postos(xs):
        ordem = sorted(range(len(xs)), key=lambda i: xs[i])
        rk = [0.0] * len(xs)
        i = 0
        while i < len(ordem):
            j = i
            while j + 1 < len(ordem) and xs[ordem[j + 1]] == xs[ordem[i]]:
                j += 1
            for k in range(i, j + 1):
                rk[ordem[k]] = (i + j) / 2.0
            i = j + 1
        return rk
    a, b = postos([x for x, _ in pares]), postos([v for _, v in pares])
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return zero, zero_topo, cov / (va * vb) ** 0.5, pares


def p1635_contradicoes_de_animal(d=None):
    """(P1635) As violações da disjunção entre animal e os seus irmãos (os outros hipônimos diretos de organism), pelo motor da P1633. Devolve
    (número de sinsets que violam, [(irmão, [sinsets])] com violação)."""
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    org = min(i for i in d.lemas["organism"] if d.sinsets[i][0] == "n")
    animal = min(i for i in d.lemas["animal"] if d.sinsets[i][0] == "n")
    irmaos = p1634_irmaos(org, d)
    viol = p1633_disjuncoes([animal] + [x for x in irmaos if x != animal], d)
    pares = [(b, v) for (a, b), v in viol.items() if a == animal and v]
    return len({x for _, v in pares for x in v}), pares


def p1636_contraexemplos(classe="bird", palavra="flightless", d=None):
    """Procurar o que refuta (P1636; o Módulo 004 do texto recebido): a hipótese "todo <classe> voa" contra o próprio dicionário. Os sinsets no fecho
    de Horn da classe (primeiro sentido de substantivo) cuja glosa contém a palavra. Devolve (tamanho do fecho, [lemas dos contraexemplos])."""
    import re
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    _, regras = p1611_regras_de_animal(d)
    c = min(i for i in d.lemas[classe] if d.sinsets[i][0] == "n")
    fecho = p1609_horn_linear([c], regras)[0]
    return len(fecho), [d.sinsets[i][1][0] for i in fecho if re.search(r"\b" + palavra + r"\b", d.definicao(d.sinsets[i][3]).lower())]


def p1637_polissemia(d=None):
    """(P1637) O aviso do texto recebido ("identificar o sentido antes da relação"): a fração dos lemas de substantivo com mais de um sentido de
    substantivo. Devolve (lemas de substantivo, polissêmicos, fração)."""
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    cont = {}
    for s in d.sinsets:
        if s[0] == "n":
            for l in set(s[1]):
                cont[l] = cont.get(l, 0) + 1
    poli = sum(1 for v in cont.values() if v > 1)
    return len(cont), poli, poli / len(cont)


def p1638_rodadas_com_libm():
    """(P1638) As rodadas Python do diálogo que chamam uma função transcendental da biblioteca (math.exp, log, log2, log10, pow, sin, cos, tan,
    atan, atan2, erf), que o IEEE 754 não obriga a arredondar corretamente (a fronteira da Parte 52). Pela árvore sintática. Devolve
    (total de rodadas, [rodadas com chamada])."""
    import ast
    import glob
    import os
    raiz = os.path.dirname(os.path.abspath(__file__))
    fs = {"exp", "log", "log2", "log10", "pow", "sin", "cos", "tan", "atan", "atan2", "erf"}
    arqs = sorted(glob.glob(os.path.join(raiz, "dialogo", "rodada[0-9]*.py")))
    com = []
    for f in arqs:
        arvore = ast.parse(open(f, encoding="utf-8").read())
        if any(isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "math" and n.attr in fs for n in ast.walk(arvore)):
            com.append(os.path.basename(f)[:-3])
    return len(arqs), com


def p1639_rodada47():
    """Rodada 47 (P1639): o valor da informação e a prioridade S(q) do dialogo/rodada47.py (IGUAL em Java). Devolve (n, VOI = 0, soma dos VOI, soma dos S,
    VOI = 0 entre os 200 de maior S, VOI médio dos 200 de maior VOI, VOI médio dos 200 de maior S)."""
    import importlib.util
    import os
    import tempfile
    spec = importlib.util.spec_from_file_location("rodada47", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada47.py"))
    r47 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r47)
    with tempfile.TemporaryDirectory() as pasta:
        r47.preparar(pasta)
        voi, s = r47.calcular(r47.ler(pasta))
    sv = ss = 0.0
    for v, x in zip(voi, s):
        sv += v
        ss += x
    ts, tv = r47.topo(s, 200), r47.topo(voi, 200)
    return (len(voi), sum(1 for v in voi if v == 0.0), sv, ss, sum(1 for i in ts if voi[i] == 0.0),
            sum(voi[i] for i in tv) / 200, sum(voi[i] for i in ts) / 200)


def p1642_heranca_multipla(d=None):
    """(P1642) Os sinsets de substantivo com mais de um hiperônimo substantivo (as "colas" entre ramos da árvore). Devolve (com herança múltipla,
    substantivos, fração)."""
    if d is None:
        from synthai.dicionario import Dicionario
        d = Dicionario()
    ns = [s for s in d.sinsets if s[0] == "n"]
    m = sum(1 for s in ns if sum(1 for h in s[2] if h.startswith("n:")) > 1)
    return m, len(ns), m / len(ns)


def p1661_ganho_de_informacao_contra_voi(n=2000, semente=73):
    """O "ganho esperado de informação" do texto recebido na Parte 74, no mundo da P1632 (P1661): observar o estado reduz a entropia em H(p) bits
    (a informação é perfeita), qualquer que seja a utilidade. Escolher as perguntas pelo ganho de informação é escolher por H(p). Devolve (fração com
    VOI = 0 entre os 10% de maior H, VOI médio dos 10% de maior H, VOI médio dos 10% de maior VOI)."""
    import math
    import random
    r = random.Random(semente)
    xs = []
    for _ in range(n):
        p = r.random()
        u = [[r.random(), r.random()], [r.random(), r.random()]]
        com = p * max(u[0][1], u[1][1]) + (1.0 - p) * max(u[0][0], u[1][0])
        sem = max(p * u[0][1] + (1.0 - p) * u[0][0], p * u[1][1] + (1.0 - p) * u[1][0])
        h = -sum(q * math.log2(q) for q in (p, 1.0 - p) if q > 0.0)
        xs.append((h, max(com - sem, 0.0)))
    k = n // 10
    th = sorted(xs, key=lambda x: -x[0])[:k]
    tv = sorted(xs, key=lambda x: -x[1])[:k]
    return sum(1 for _, v in th if v == 0.0) / k, sum(v for _, v in th) / k, sum(v for _, v in tv) / k


def p1662_orcamento(instancias=300, itens=30, fracao=0.2, semente=74):
    """Escolher experimentos com orçamento (P1662; a U(a) = E[ΔK | a]/Custo(a) do texto recebido na Parte 74). Cada instância: `itens` experimentos com
    valor = o VOI de um problema 2 × 2 sorteado (como na P1632) e ganho de informação = H(p) dele, custo inteiro uniforme em 1..20; orçamento =
    floor(fracao · Σ custos). Três escolhas: o ótimo exato (mochila 0-1 por programação dinâmica nos custos inteiros, no VOI), o guloso por VOI/custo
    (em ordem decrescente, pulando o que não cabe) e o guloso por H/custo (o "ganho de informação"). Devolve (média de guloso-VOI/ótimo, média de
    guloso-H/ótimo, fração de instâncias em que o guloso-VOI é ótimo), com o valor de cada escolha medido em VOI."""
    import math
    import random
    r = random.Random(semente)
    s1 = s2 = 0.0
    otimos = 0
    for _ in range(instancias):
        vs, hs, cs = [], [], []
        for _ in range(itens):
            p = r.random()
            u = [[r.random(), r.random()], [r.random(), r.random()]]
            com = p * max(u[0][1], u[1][1]) + (1.0 - p) * max(u[0][0], u[1][0])
            sem = max(p * u[0][1] + (1.0 - p) * u[0][0], p * u[1][1] + (1.0 - p) * u[1][0])
            vs.append(max(com - sem, 0.0))
            hs.append(-sum(q * math.log2(q) for q in (p, 1.0 - p) if q > 0.0))
            cs.append(r.randint(1, 20))
        B = int(fracao * sum(cs))
        melhor = [0.0] * (B + 1)
        for v, c in zip(vs, cs):
            for b in range(B, c - 1, -1):
                if melhor[b - c] + v > melhor[b]:
                    melhor[b] = melhor[b - c] + v
        ot = melhor[B]

        def guloso(chave):
            resto, total = B, 0.0
            for i in sorted(range(itens), key=lambda i: (-chave[i] / cs[i], i)):
                if cs[i] <= resto:
                    resto -= cs[i]
                    total += vs[i]
            return total
        g1, g2 = guloso(vs), guloso(hs)
        s1 += g1 / ot if ot > 0 else 1.0
        s2 += g2 / ot if ot > 0 else 1.0
        otimos += g1 >= ot - 1e-12
    return s1 / instancias, s2 / instancias, otimos / instancias


def p1663_rodada48():
    """Rodada 48 (P1663): a mochila e os dois gulosos do dialogo/rodada48.py nas 300 instâncias da semente 74 (IGUAL em Java). Devolve (soma dos ótimos,
    soma do guloso por VOI, soma do guloso por H, instâncias em que o guloso por VOI é ótimo)."""
    import importlib.util
    import os
    import tempfile
    spec = importlib.util.spec_from_file_location("rodada48", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada48.py"))
    r48 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r48)
    so = s1 = s2 = 0.0
    otimos = 0
    with tempfile.TemporaryDirectory() as pasta:
        r48.preparar(pasta)
        for B, vs, hs, cs in r48.ler(pasta):
            ot, g1, g2 = r48.resolver(B, vs, hs, cs)
            so += ot
            s1 += g1
            s2 += g2
            otimos += g1 >= ot - 1e-12
    return so, s1, s2, otimos


def _java_extract_json_field(json_texto, campo):
    """A semântica do extractJsonField do texto recebido na Parte 75, reescrita por mim: indexOf da chave com aspas e dois-pontos SEM espaço."""
    chave = '"' + campo + '":"'
    ini = json_texto.find(chave)
    if ini == -1:
        return ""
    ini += len(chave)
    return json_texto[ini:json_texto.index('"', ini)]


def _nucleo_utilidade(codigo, conceito):
    """A fórmula do CreativeLogicKernel do texto recebido, reescrita por mim (nada dele é executado): consistência = (conceito "reasoning" e "Mult"
    no código) ou código não vazio; utilidade = (comprimento UTF-16 div 4)/(linhas + 1) − 0,5, com as linhas do split("\\r\\n|\\r|\\n") do Java (que
    descarta as vazias do fim); −1 se inconsistente. Devolve (aprovado, delta)."""
    import re
    ok = (conceito.lower() == "reasoning" and "Mult" in codigo) or len(codigo) > 0
    partes = re.split(r"\r\n|\r|\n", codigo)
    while len(partes) > 1 and partes[-1] == "":
        partes.pop()
    n = len(codigo.encode("utf-16-le")) // 2
    delta = ((n // 4) / (len(partes) + 1) - 0.5) if ok else -1.0
    return ok and delta > 0.0, delta


def _mutar_soma_em_produto(codigo):
    """A mutação do texto recebido (todo + binário vira *), reescrita por mim com o ast da biblioteca padrão. O código mutado NUNCA é executado
    (regra da Parte 33): só é lido de volta como texto. Devolve (código mutado, número de trocas)."""
    import ast
    arvore = ast.parse(codigo)
    trocas = [0]

    class Mutador(ast.NodeTransformer):
        def visit_BinOp(self, no):
            self.generic_visit(no)
            if isinstance(no.op, ast.Add):
                trocas[0] += 1
                return ast.copy_location(ast.BinOp(left=no.left, op=ast.Mult(), right=no.right), no)
            return no
    nova = Mutador().visit(arvore)
    ast.fix_missing_locations(nova)
    return ast.unparse(nova), trocas[0]


def p1691_laco_de_auto_modificacao(codigo="def compute_factor(x, y):\n    return x + y", conceito="reasoning", geracoes=5, separador_corrigido=False):
    """O laço de auto-modificação do texto recebido na Parte 75 (P1691), simulado pelas reimplementações acima, sem executar nada do texto nem do
    código mutado: em cada geração, mutar (+ → *), montar o payload como o json.dumps do Python (com ou sem o separador compacto), extrair os campos
    como o Java, avaliar pela fórmula do núcleo e, se aprovado, adotar o código com o comentário acrescentado. Devolve a lista de gerações
    (campos achados, aprovado, delta, código atual)."""
    import json
    atual, hist = codigo, []
    for g in range(1, geracoes + 1):
        mutado, _ = _mutar_soma_em_produto(atual)
        payload = {"generation": g, "hypothesis_code_hex": mutado.encode("utf-8").hex().upper(),
                   "dictionary_query_hex": conceito.encode("utf-8").hex().upper()}
        texto = json.dumps(payload, separators=(",", ":")) if separador_corrigido else json.dumps(payload)
        hc, hq = _java_extract_json_field(texto, "hypothesis_code_hex"), _java_extract_json_field(texto, "dictionary_query_hex")
        cod, conc = bytes.fromhex(hc).decode("utf-8"), bytes.fromhex(hq).decode("utf-8")
        aprovado, delta = _nucleo_utilidade(cod, conc)
        if aprovado:
            atual = cod + "\n# Verified by Java ASI"
        hist.append((hc != "" and hq != "", aprovado, delta, atual))
    return hist


def p1692_godel_nas_funcoes():
    """A "prova de utilidade de Gödel" do texto recebido, aplicada a cada função de primeiro nível do calculos.py como hipótese (P1692): a mutação
    (+ → *) e a fórmula do núcleo, com o defeito do separador corrigido. Nada é executado. Devolve (funções, aprovadas, mudadas pela mutação,
    aprovadas e mudadas)."""
    import ast
    import os
    fonte = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculos.py"), encoding="utf-8").read()
    funcs = [n for n in ast.parse(fonte).body if isinstance(n, ast.FunctionDef)]
    aprov = mud = ambos = 0
    for f in funcs:
        mutado, trocas = _mutar_soma_em_produto(ast.get_source_segment(fonte, f))
        a, _ = _nucleo_utilidade(mutado, "reasoning")
        aprov += a
        mud += trocas > 0
        ambos += a and trocas > 0
    return len(funcs), aprov, mud, ambos


def p1693_godel_no_pacote():
    """A mesma "prova de utilidade" (P1692) nas funções e métodos dos arquivos synthai/*.py que não são testes (P1693), um mundo novo para a previsão
    nascida do erro (e) da Parte 75. Nada é executado. Devolve (funções e métodos, aprovados, mudados pela mutação)."""
    import ast
    import glob
    import os
    raiz = os.path.dirname(os.path.abspath(__file__))
    n = aprov = mud = 0
    for f in sorted(glob.glob(os.path.join(raiz, "synthai", "*.py"))):
        if os.path.basename(f).startswith("testes"):
            continue
        fonte = open(f, encoding="utf-8").read()
        for no in ast.walk(ast.parse(fonte)):
            if isinstance(no, ast.FunctionDef):
                mutado, trocas = _mutar_soma_em_produto(__import__("textwrap").dedent(ast.get_source_segment(fonte, no)))
                a, _ = _nucleo_utilidade(mutado, "reasoning")
                n += 1
                aprov += a
                mud += trocas > 0
    return n, aprov, mud


def p1694_verificador_do_texto():
    """O Verifier.java do relatório do Módulo 007 (Parte 75), conferido por conta (P1694): score = ganho·(1 − risco)/custo para A (0,8; 0,1; 2),
    B (0,5; 0; 1) e C (0,9; 0,2; 4); com orçamento 3, a ordem gulosa pelo score e o ótimo por enumeração dos 2³ subconjuntos (valor = ganho·(1 − risco)).
    Devolve (scores, ordem gulosa escolhida, valor guloso, melhor subconjunto, valor ótimo)."""
    from itertools import combinations
    exp = {"A": (0.8, 0.1, 2), "B": (0.5, 0.0, 1), "C": (0.9, 0.2, 4)}
    sc = {k: g * (1.0 - r) / c for k, (g, r, c) in exp.items()}
    resto, ordem, valor = 3, [], 0.0
    for k in sorted(exp, key=lambda k: -sc[k]):
        if exp[k][2] <= resto:
            resto -= exp[k][2]
            ordem.append(k)
            valor += exp[k][0] * (1.0 - exp[k][1])
    melhor, vmax = (), 0.0
    for t in range(1, 4):
        for sub in combinations(sorted(exp), t):
            if sum(exp[k][2] for k in sub) <= 3:
                v = sum(exp[k][0] * (1.0 - exp[k][1]) for k in sub)
                if v > vmax:
                    melhor, vmax = sub, v
    return sc, ordem, valor, melhor, vmax


def p1698_comparar_reenvio_v2(novo="externos/texto_recebido_parte75b.md", guardado="externos/texto_recebido_parte75.md"):
    """A regra da Parte 50 para um texto reenviado, versão 2 (P1698; a P1631 só olhava blocos python): cada bloco de código cercado (```linguagem) do
    texto novo é comparado com todos os blocos guardados, sem os espaços das pontas. Devolve [(linguagem, índice do bloco guardado idêntico ou None,
    linhas)]."""
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    blocos = lambda f: [(m.group(1), m.group(2).strip()) for m in re.finditer(r"```(\w*)\n(.*?)```", open(os.path.join(raiz, f), encoding="utf-8").read(), re.S)]
    velhos = [b for _, b in blocos(guardado)]
    return [(lg, next((j for j, v in enumerate(velhos) if v == b), None), b.count("\n") + 1) for lg, b in blocos(novo)]


def p1721_kronecker_contra_cheio(lingua="en", semente=76, embaralhar=False, passos=2000):
    """A forma do byte (P1721): dois GPTs iguais (d = 16, T = 16, h = 32, taxa 0,005), um com a tabela de embeddings cheia e outro com o embedding de
    Kronecker por nibble (synthai/gpt_kronecker.py, d₁ = d₂ = 4), treinados nas glosas da língua com a mesma semente; bits por caractere no teste
    (300 janelas). Com embaralhar=True, só o Kronecker, com os caracteres permutados entre os mesmos bytes (semente 1.000 + semente): o controle do
    mecanismo. Devolve (bits do cheio ou None, bits do Kronecker)."""
    import random
    from synthai.gpt import GPT
    from synthai.gpt_kronecker import GPTKronecker
    tr, te = p1511_corpus_de_glosas(lingua)
    cheio = None
    if not embaralhar:
        g = GPT(VOCAB_GPT, T=16, d=16, h=32, semente=semente)
        g.treinar(tr, passos=passos, lr=0.005, semente=semente)
        cheio = g.bits_por_caractere(te, janelas=300)
    bs = [ord(ch) for ch in VOCAB_GPT]
    if embaralhar:
        random.Random(1000 + semente).shuffle(bs)
    k = GPTKronecker(VOCAB_GPT, T=16, d1=4, d2=4, h=32, semente=semente, mapa=bs)
    k.treinar(tr, passos=passos, lr=0.005, semente=semente)
    return cheio, k.bits_por_caractere(te, janelas=300)


def p1722_libm_nas_duas_linguagens():
    """A auditoria da fronteira da Parte 52, versão 2 (P1722; a P1638 só olhava o Python e só a forma math.log): em cada rodada, as funções
    transcendentais da biblioteca chamadas no Python (math.X, ou X importado de math) e no Java (Math.X ou StrictMath.X), e se a chamada do Python
    está só dentro de uma função `preparar` (os valores vão para um arquivo que o Java lê: sem risco entre as linguagens). Devolve
    {rodada: (nomes no Python, só na preparação?, nomes no Java)} só das rodadas com alguma chamada."""
    import ast
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    fs = {"exp", "log", "log2", "log10", "log1p", "expm1", "pow", "sin", "cos", "tan", "atan", "atan2", "erf", "sinh", "cosh", "tanh"}
    saida = {}
    for f in sorted(glob.glob(os.path.join(raiz, "dialogo", "rodada[0-9]*.py"))):
        n = os.path.basename(f)[6:-3]
        arv = ast.parse(open(f, encoding="utf-8").read())
        importados = {a.asname or a.name for no in ast.walk(arv) if isinstance(no, ast.ImportFrom) and no.module == "math"
                      for a in no.names if a.name in fs}
        pais = {}
        for no in ast.walk(arv):
            for filho in ast.iter_child_nodes(no):
                pais[filho] = no
        nomes, so_prep = set(), True
        for no in ast.walk(arv):
            if not isinstance(no, ast.Call):
                continue
            fn = no.func
            nome = (fn.attr if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.value.id == "math" and fn.attr in fs
                    else fn.id if isinstance(fn, ast.Name) and fn.id in importados else None)
            if nome is None:
                continue
            nomes.add(nome)
            q, dentro = pais.get(no), False
            while q is not None:
                if isinstance(q, ast.FunctionDef) and q.name == "preparar":
                    dentro = True
                q = pais.get(q)
            so_prep = so_prep and dentro
        java = os.path.join(raiz, "dialogo", "Rodada" + n + ".java")
        nj = sorted(set(re.findall(r"\b(?:Strict)?Math\.(" + "|".join(sorted(fs)) + r")\(", open(java, encoding="utf-8").read()))) if os.path.exists(java) else []
        if nomes or nj:
            saida[n] = (sorted(nomes), so_prep if nomes else None, nj)
    return saida


def p1751_rodada09_nova_contra_antiga():
    """(P1751) A rodada 09 reescrita na Parte 77 (exp e log próprios) contra a original (dialogo/registro/rodada09_libm.py, com o exp e o log da
    biblioteca): as duas rodam como scripts e os números impressos (hexadecimal) são comparados. Devolve (números, quantos mudaram, maior diferença
    relativa)."""
    import os
    import re
    import subprocess
    import sys
    raiz = os.path.dirname(os.path.abspath(__file__))

    def numeros(arq):
        saida = subprocess.run([sys.executable, arq], capture_output=True, text=True, check=True, cwd=raiz).stdout
        return [float.fromhex(x) for x in re.findall(r"-?0x[0-9a-f.]+p[+-]\d+", saida)]
    a = numeros(os.path.join(raiz, "dialogo", "registro", "rodada09_libm.py"))
    b = numeros(os.path.join(raiz, "dialogo", "rodada09.py"))
    return len(a), sum(x != y for x, y in zip(a, b)), max(abs(x - y) / max(abs(x), 1e-300) for x, y in zip(a, b))


def p1781_svd_por_jacobi(M, varreduras=60):
    """Decomposição em valores singulares de uma matriz quadrada M (P1781): os autovalores e autovetores de MᵀM por Jacobi cíclico (acumulando as
    rotações em V), σ = √λ, e U = M·V/σ (as colunas de σ = 0 ficam zero). Só + − × ÷ e √. Devolve (σ decrescentes, U, V), com U e V como listas de
    linhas d × d (coluna i = vetor singular i)."""
    import math
    d = len(M)
    A = [[sum(M[k][i] * M[k][j] for k in range(d)) for j in range(d)] for i in range(d)]
    V = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(varreduras):
        fora = sum(A[p][q] * A[p][q] for p in range(d) for q in range(p + 1, d))
        if fora < 1e-30:
            break
        for p in range(d):
            for q in range(p + 1, d):
                if A[p][q] == 0.0:
                    continue
                tau = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if tau >= 0.0 else -1.0) / (abs(tau) + math.sqrt(tau * tau + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for k in range(d):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - sn * akq, sn * akp + c * akq
                for k in range(d):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - sn * aqk, sn * apk + c * aqk
                for k in range(d):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * vkp - sn * vkq, sn * vkp + c * vkq
    ordem = sorted(range(d), key=lambda i: -A[i][i])
    sig = [math.sqrt(max(A[i][i], 0.0)) for i in ordem]
    Vs = [[V[k][i] for i in ordem] for k in range(d)]
    U = [[0.0] * d for _ in range(d)]
    for j in range(d):
        if sig[j] > 0.0:
            for i in range(d):
                U[i][j] = sum(M[i][k] * Vs[k][j] for k in range(d)) / sig[j]
    return sig, U, Vs


def p1782_atencao_de_posto(g, r):
    """Troca a forma bilinear da atenção de um GPT treinado (M = W_Q W_Kᵀ) pela melhor aproximação de posto r (Eckart–Young), sem mexer no resto
    (P1782): W_Q' = U_r Σ_r e W_K' = V_r, completadas com colunas zero, de modo que W_Q' W_K'ᵀ = M_r. Devolve uma cópia do GPT."""
    import copy
    h = copy.deepcopy(g)
    Q, K = g.p["Q"], g.p["K"]
    d = len(Q)
    M = [[sum(Q[i][k] * K[j][k] for k in range(d)) for j in range(d)] for i in range(d)]
    sig, U, V = p1781_svd_por_jacobi(M)
    h.p["Q"] = [[U[i][j] * sig[j] if j < r else 0.0 for j in range(d)] for i in range(d)]
    h.p["K"] = [[V[i][j] if j < r else 0.0 for j in range(d)] for i in range(d)]
    return h


def p1783_bits_por_posto(lingua="en", semente=71, postos=(1, 2, 4, 16), passos=2000):
    """(P1783) Um GPT (d = 16, T = 16, h = 32, taxa 0,005) treinado nas glosas da língua; os bits por caractere no teste (300 janelas) com a atenção
    original e com a de posto r. Devolve (bits original, {r: bits}, valores singulares de M)."""
    from synthai.gpt import GPT
    tr, te = p1511_corpus_de_glosas(lingua)
    g = GPT(VOCAB_GPT, T=16, d=16, h=32, semente=semente)
    g.treinar(tr, passos=passos, lr=0.005, semente=semente)
    Q, K = g.p["Q"], g.p["K"]
    M = [[sum(Q[i][k] * K[j][k] for k in range(16)) for j in range(16)] for i in range(16)]
    sig = p1781_svd_por_jacobi(M)[0]
    return g.bits_por_caractere(te, janelas=300), {r: p1782_atencao_de_posto(g, r).bits_por_caractere(te, janelas=300) for r in postos}, sig


def p1811_confusao(n=20000, semente=79, beta=0.5, gama=1.0, a=1.0):
    """O diagrama causal do texto recebido na Parte 79 (Z → X, Z → Y, X → Y), simulado (P1811): Z ~ N(0, 1), X = a·Z + ε_X, Y = β·X + γ·Z + ε_Y. Três
    estimativas do efeito de X sobre Y: a inclinação ingênua (mínimos quadrados de Y em X), a ajustada por Z (mínimos quadrados de Y em X e Z, pelas
    equações normais 2 × 2 dos centrados) e a sob intervenção (X sorteado com a mesma variância, sem depender de Z). Devolve (ingênua, ajustada,
    intervenção)."""
    import random
    r = random.Random(semente)

    def amostra(intervir):
        xs, ys, zs = [], [], []
        for _ in range(n):
            z = r.gauss(0.0, 1.0)
            x = r.gauss(0.0, (a * a + 1.0) ** 0.5) if intervir else a * z + r.gauss(0.0, 1.0)
            xs.append(x)
            zs.append(z)
            ys.append(beta * x + gama * z + r.gauss(0.0, 1.0))
        return xs, ys, zs

    def centrar(v):
        m = sum(v) / len(v)
        return [x - m for x in v]

    xs, ys, zs = (centrar(v) for v in amostra(False))
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    szz = sum(z * z for z in zs)
    sxz = sum(x * z for x, z in zip(xs, zs))
    szy = sum(z * y for z, y in zip(zs, ys))
    ingenua = sxy / sxx
    ajustada = (szz * sxy - sxz * szy) / (sxx * szz - sxz * sxz)
    xi, yi, _ = (centrar(v) for v in amostra(True))
    intervencao = sum(x * y for x, y in zip(xi, yi)) / sum(x * x for x in xi)
    return ingenua, ajustada, intervencao


def p1812_minha_calibracao(partes=range(53, 79)):
    """A prévia do Módulo 010 do texto recebido na Parte 79 (P1812): a fração das minhas previsões do mundo que acertaram (régua p1481), por tipo, contra
    os 90% que a maioria das faixas declara. Devolve (previsões, fração de acertos, {tipo: (n, fração)})."""
    prev = p1481_minhas_previsoes_v2(partes)
    por = {}
    for x in prev:
        por.setdefault(x[5], []).append(x[4])
    return len(prev), sum(x[4] for x in prev) / len(prev), {k: (len(v), sum(v) / len(v)) for k, v in por.items()}


def p1813_fator_de_alargamento(acerto, nominal=0.9):
    """Quanto alargar faixas que acertam `acerto` quando declaram `nominal` (P1813), supondo erros normais em torno do centro: uma faixa de ± z·σ_suposto
    cobre a fração 2Φ(z·σ_suposto/σ_real) − 1; igualar ao acerto observado dá σ_real/σ_suposto = z(nominal)/z(acerto), com z(p) = Φ⁻¹((1 + p)/2).
    Devolve (z nominal, z observado, fator, desvio binomial do acerto se fosse o nominal, z do acerto observado contra o nominal) para n = 185."""
    from statistics import NormalDist
    nd = NormalDist()
    zn, zo = nd.inv_cdf((1 + nominal) / 2), nd.inv_cdf((1 + acerto) / 2)
    sd = (nominal * (1 - nominal) / 185) ** 0.5
    return zn, zo, zn / zo, sd, (acerto - nominal) / sd


def p1841_voi_conjunto(p, u, qs, conj):
    """O valor da informação de um CONJUNTO de sensores (P1841): estado binário com prior P(S = 1) = p, utilidades u[a][s] (2 ações), sensores que
    acertam o estado com probabilidade qs[i], condicionalmente independentes dado o estado. VOI(conj) = Σ_respostas max_a Σ_s P(s, respostas)·u[a][s]
    − max_a Σ_s P(s)·u[a][s], enumerando as 2^|conj| respostas. Devolve o VOI (≥ 0 pela desigualdade de Jensen)."""
    sem = max(p * u[a][1] + (1 - p) * u[a][0] for a in (0, 1))
    conj = list(conj)
    total = 0.0
    for m in range(1 << len(conj)):
        l1, l0 = p, 1 - p
        for b, i in enumerate(conj):
            diz1 = (m >> b) & 1
            l1 *= qs[i] if diz1 else 1 - qs[i]
            l0 *= 1 - qs[i] if diz1 else qs[i]
        total += max(l1 * u[a][1] + l0 * u[a][0] for a in (0, 1))
    return max(total - sem, 0.0)


def p1842_conjuntos(instancias=300, k=6, orcamento=6, semente=80, olhar=1):
    """Escolher um conjunto de experimentos dependentes (P1842; a pendência da Parte 74). Cada instância: prior p ~ U(0, 1), utilidades U(0, 1), k
    sensores com acurácia U(0,55; 0,95) e custo inteiro em 1..5. O ótimo: o melhor subconjunto dentro do orçamento (enumeração dos 2^k). O guloso: em cada
    passo, o sensor de maior ganho marginal de VOI por custo que ainda cabe, e para quando nenhum ganho é positivo. A complementaridade: algum par
    (i, j) com VOI({i, j}) − VOI({i}) > VOI({j}) − VOI(∅) + 1e-12 (o VOI não é submodular). Devolve (média de guloso/ótimo, fração com guloso ótimo,
    fração com complementaridade, fração em que o guloso para em zero com o ótimo positivo). Com olhar = 2, quando nenhum sensor sozinho tem ganho
    positivo, o guloso tenta o melhor par antes de parar."""
    import random
    r = random.Random(semente)
    soma = otimos = compl = parado = 0
    for _ in range(instancias):
        p = r.random()
        u = [[r.random(), r.random()], [r.random(), r.random()]]
        qs = [0.55 + 0.4 * r.random() for _ in range(k)]
        cs = [r.randint(1, 5) for _ in range(k)]
        memo = {}

        def voi(c):
            c = tuple(sorted(c))
            if c not in memo:
                memo[c] = p1841_voi_conjunto(p, u, qs, c)
            return memo[c]
        ot = max(voi([i for i in range(k) if m >> i & 1]) for m in range(1 << k)
                 if sum(cs[i] for i in range(k) if m >> i & 1) <= orcamento)
        esc, resto = [], orcamento
        while True:
            cand = [(voi(esc + [i]) - voi(esc)) / cs[i] for i in range(k) if i not in esc and cs[i] <= resto]
            idx = [i for i in range(k) if i not in esc and cs[i] <= resto]
            if not idx:
                break
            if max(cand) <= 1e-15:
                # olhar = 2 (Parte 80): quando nenhum sensor sozinho ganha, o melhor PAR que cabe, pelo ganho por custo
                if olhar < 2:
                    break
                pares = [((voi(esc + [i, j]) - voi(esc)) / (cs[i] + cs[j]), i, j) for i in idx for j in idx if i < j and cs[i] + cs[j] <= resto]
                if not pares or max(pares)[0] <= 1e-15:
                    break
                _, i, j = max(pares, key=lambda t: (t[0], -t[1], -t[2]))
                esc += [i, j]
                resto -= cs[i] + cs[j]
                continue
            j = idx[max(range(len(idx)), key=lambda t: (cand[t], -idx[t]))]
            esc.append(j)
            resto -= cs[j]
        g = voi(esc)
        if ot > 1e-12:  # um VOI de 1e-17 é zero com ruído de ponto flutuante (achado na calibração da Parte 80)
            soma += g / ot
            otimos += g >= ot - 1e-12
            parado += (not esc)
        else:
            soma += 1.0
            otimos += 1
        compl += any(voi([i, j]) - voi([i]) > voi([j]) - voi([]) + 1e-12 for i in range(k) for j in range(i + 1, k))
    return soma / instancias, otimos / instancias, compl / instancias, parado / instancias


def p1843_rodada49():
    """Rodada 49 (P1843): o VOI de conjuntos, o ótimo e os dois gulosos do dialogo/rodada49.py nas 300 instâncias da semente 80 (IGUAL em Java). Devolve
    (a média de guloso/ótimo com olhar 1 e com olhar 2, as frações de guloso ótimo, a fração parada em zero com olhar 1), pela mesma regra da P1842, para
    conferir que a rodada reproduz a função."""
    import importlib.util
    import os
    import tempfile
    spec = importlib.util.spec_from_file_location("rodada49", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada49.py"))
    r49 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r49)
    rat, ot_, par = [0.0, 0.0], [0, 0], 0
    with tempfile.TemporaryDirectory() as pasta:
        r49.preparar(pasta)
        inst = r49.ler(pasta)
    for p, u, qs, cs in inst:
        ot, saidas = r49.resolver(p, u, qs, cs)
        for t, (g, esc) in enumerate(saidas):
            if ot > 1e-12:
                rat[t] += g / ot
                ot_[t] += g >= ot - 1e-12
                par += t == 0 and not esc
            else:
                rat[t] += 1.0
                ot_[t] += 1
    n = len(inst)
    return rat[0] / n, rat[1] / n, ot_[0] / n, ot_[1] / n, par / n


def p1871_o_que_nao_serve():
    """O pedido da Parte 81 ("tire tudo que não serve pra nada"), medido (P1871): o que nada usa. Corpus: os arquivos de texto versionados (git ls-files),
    fora as cópias geradas (SYNTHAI_completo.py, que contém tudo) e os dados. Devolve três listas: (a) funções e classes de primeiro nível do calculos.py
    que não são pNN, _parte_N nem as da unificação, e cujo nome (palavra inteira) não aparece em lugar nenhum além da própria definição; (b) o mesmo para os
    módulos de synthai/ fora os testes; (c) arquivos versionados cujo nome (com ou sem a extensão, ou como módulo) não aparece em nenhum outro."""
    import ast
    import os
    import re
    import subprocess
    raiz = os.path.dirname(os.path.abspath(__file__))
    git = subprocess.run(["git", "ls-files"], cwd=raiz, capture_output=True, text=True)
    if git.returncode == 0:
        arquivos = [f for f in git.stdout.split("\n") if f]
    else:  # fora de um repositório git (o SYNTHAI_completo.py extraído numa pasta): percorrer a pasta
        arquivos = sorted(os.path.relpath(os.path.join(d, f), raiz).replace(os.sep, "/") for d, sub, fs in os.walk(raiz)
                          if "__pycache__" not in d and ".git" not in d for f in fs)
    texto = {f: open(os.path.join(raiz, f), encoding="utf-8").read() for f in arquivos
             if f != "SYNTHAI_completo.py" and not f.startswith("dados/") and f.endswith((".py", ".java", ".md", ".txt", ".tsv"))}

    def usos(nome):
        pat = re.compile(r"(?<![\w])" + re.escape(nome) + r"(?![\w])")
        return sum(len(pat.findall(t)) for t in texto.values())
    fixos = {"testes_de_regressao", "_unificacao"}
    mortos_c = []
    for no in ast.parse(texto["calculos.py"]).body:
        if isinstance(no, (ast.FunctionDef, ast.ClassDef)) and not re.match(r"p\d+_|_parte_\d+$", no.name) and no.name not in fixos:
            if usos(no.name) <= 1:
                mortos_c.append(no.name)
    mortos_s = []
    for f in sorted(x for x in texto if x.startswith("synthai/") and not os.path.basename(x).startswith("testes") and x.endswith(".py")):
        for no in ast.parse(texto[f]).body:
            if isinstance(no, (ast.FunctionDef, ast.ClassDef)) and not no.name.startswith("__") and usos(no.name) <= 1:
                mortos_s.append(f"{f}:{no.name}")
    soltos = []
    for f in sorted(texto):
        base = os.path.basename(f)
        nomes = {base, os.path.splitext(base)[0]}
        if f.endswith(".py"):
            nomes.add(f[:-3].replace("/", "."))
        outros = [t for g, t in texto.items() if g != f]
        if not any(re.search(r"(?<![\w])" + re.escape(n) + r"(?![\w])", t) for n in nomes for t in outros):
            soltos.append(f)
    return mortos_c, mortos_s, soltos


def p1872_candidatos_explicados(candidatos=None):
    """Os arquivos que a P1871 acusa como "não referenciados pelo nome", conferidos um a um (P1872; a regra da Parte 75: todo defeito acusado é olhado antes de
    ser contado). Um candidato é usado se cair num destes usos por padrão, achados lendo o código: os RodadaNN.java e rodadaNN.py (o verificar.py os acha por
    glob), os dialogo/saidas29/* (a rodada29.py monta o nome com f-string), os dialogo/registro/* (as originais das rodadas corrigidas, citadas pela pasta nos
    documentos e abertas pela p1751) e o documento da parte mais nova (ligado pela anterior no fechamento). Devolve ({motivo: quantos}, [sem motivo])."""
    import re
    if candidatos is None:
        candidatos = p1871_o_que_nao_serve()[2]
    regras = [("verificar.py (glob)", r"^dialogo/(Rodada\d+\.java|rodada\d+\.py)$"), ("rodada29.py (f-string)", r"^dialogo/saidas29/"),
              ("registro (citado pela pasta)", r"^dialogo/registro/"), ("documento da parte mais nova", r"^ASI_AGI_parte\d+_.*\.md$")]
    contagem, sobra = {}, []
    for f in candidatos:
        for motivo, pat in regras:
            if re.search(pat, f):
                contagem[motivo] = contagem.get(motivo, 0) + 1
                break
        else:
            sobra.append(f)
    return contagem, sobra


import math  # Parte 83: as funções P1931-P1933 usam o módulo inteiro


def p1931_gan_de_dirac():
    """GAN de Dirac (P1931; Mescheder, Geiger e Nowozin, 2018): os três treinos da rodada 50 (dialogo/rodada50.py, com o exp próprio), síncrono, alternado e
    assíncrono por moeda, η = 0,1, 1000 passos a partir de (0,1; 0). Devolve {esquema: (norma final, norma máxima, trocas de sinal de θ)} e as contas
    fechadas do jogo linearizado (a = η/2): a norma síncrona 0,1·(1 + a²)^500, o ângulo alternado φ com cos φ = 1 − a²/2 (o cosseno do ângulo duplo:
    sen(φ/2) = a/2) e a norma máxima da elipse invariante, 0,1/√(1 − a/2)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada50", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada50.py"))
    r50 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r50)
    medido = {e: r50.resumo(r50.treinar(e)) for e in ("sincrono", "alternado", "assincrono")}
    a = 0.05
    phi = math.acos(1 - a * a / 2)
    conta = {"sincrono_final": 0.1 * (1 + a * a) ** 500, "phi": phi, "phi_angulo_duplo": 2 * math.asin(a / 2),
             "alternado_maximo": 0.1 / math.sqrt(1 - a / 2),
             "trocas": sum(1 for k in range(100) if (math.pi / 2 + k * math.pi) / phi <= 1000)}
    return medido, conta


def p1932_jogo_assincrono(a=0.05, passos=10000, corridas=200, semente0=83000):
    """O jogo bilinear linearizado (P1932), z = (θ, ψ), em três ordens: síncrona (z ← [[1, −a], [a, 1]] z), alternada (θ primeiro, ψ vê o θ novo) e
    assíncrona (uma moeda escolhe quem se move). Devolve (média de ln(|z_N|/|z_0|) nas corridas assíncronas, o desvio dela por corrida, quantas
    corridas terminam menores que o início, o ln síncrono, o ln alternado) e a conta: a²/8 por passo no assíncrono, (1/2)ln(1 + a²) no síncrono."""
    logs = []
    for c in range(corridas):
        r = random.Random(semente0 + c)
        t, p = 1.0, 0.0
        for _ in range(passos):
            if r.random() < 0.5:
                t = t - a * p
            else:
                p = p + a * t
        logs.append(0.5 * math.log(t * t + p * p))
    m = sum(logs) / corridas
    dp = math.sqrt(sum((v - m) ** 2 for v in logs) / (corridas - 1))
    t, p = 1.0, 0.0
    for _ in range(passos):
        t, p = t - a * p, p + a * t
    ln_sinc = 0.5 * math.log(t * t + p * p)
    t, p = 1.0, 0.0
    for _ in range(passos):
        t = t - a * p
        p = p + a * t
    ln_alt = 0.5 * math.log(t * t + p * p)
    conta = {"assincrono": passos * a * a / 8, "desvio": a * math.sqrt(passos / 8), "sincrono": 0.5 * passos * math.log(1 + a * a)}
    return (m, dp, sum(1 for v in logs if v < 0), ln_sinc, ln_alt), conta


def _phi_normal(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def p1933_calibracao_composta(k=1.36, camadas=7, nominal=0.9, sorteios=100000, semente=83):
    """A probabilidade dentro da probabilidade (P1933). O mapa de calibração medido (Parte 79): uma faixa declarada com cobertura c, se o desvio real é k vezes
    o suposto, cobre h_k(c) = 2Φ(Φ⁻¹((1 + c)/2)/k) − 1. Compor é multiplicar: h_k ∘ h_j = h_{kj} (um grupo de escalas), então n camadas dão h_{kⁿ}; o único
    mapa idempotente (h ∘ h = h) é k = 1, a calibração perfeita, e a correção é o inverso h_{1/k}. Devolve (a conta para n camadas, a simulação: cada camada
    multiplica o erro por k, a composição numérica de h_k n vezes, a cobertura a declarar para obter o nominal depois de UMA camada e depois de n)."""
    z = 1.6448536269514722 if nominal == 0.9 else None
    if z is None:
        lo, hi = 0.0, 10.0
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if 2 * _phi_normal(mid) - 1 < nominal else (lo, mid)
        z = (lo + hi) / 2

    def h(c, kk):
        lo, hi = 0.0, 40.0
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if 2 * _phi_normal(mid) - 1 < c else (lo, mid)
        return 2 * _phi_normal((lo + hi) / 2 / kk) - 1

    conta = 2 * _phi_normal(z / k ** camadas) - 1
    r = random.Random(semente)
    dentro = 0
    for _ in range(sorteios):
        e = r.gauss(0, 1)
        for _ in range(camadas):
            e *= k
        dentro += abs(e) <= z
    c = nominal
    for _ in range(camadas):
        c = h(c, k)
    return conta, dentro / sorteios, c, 2 * _phi_normal(z * k) - 1, 2 * _phi_normal(z * k ** camadas) - 1


def p1934_torre_de_placares(partes=range(67, 82)):
    """A metacognição dentro da metacognição, medida (P1934): a camada 1 é o mundo (a régua p1481), a 2 são as previsões sobre mim, a 3 as previsões sobre as
    minhas previsões, lidas da linha "Sobre mim (placar separado): **X de Y** dentro da faixa condicional; sobre as minhas previsões, A de B" de cada parte
    (as partes sem a linha ficam de fora e são devolvidas). Devolve ({camada: (acertos, total)}, partes sem a linha)."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    eu, meta, fora = [0, 0], [0, 0], []
    padrao = re.compile(r"Sobre mim \(placar separado\): \*\*(\d+) de (\d+)\*\* dentro da faixa condicional; sobre as minhas previsões, (\d+) de (\d+)")
    for n in partes:
        arq = glob.glob(os.path.join(raiz, f"ASI_AGI_parte{n}_*.md"))
        m = padrao.search(open(arq[0], encoding="utf-8").read()) if arq else None
        if not m:
            fora.append(n)
            continue
        a, b, c, d = map(int, m.groups())
        eu[0] += a; eu[1] += b; meta[0] += c; meta[1] += d
    mundo = p1812_minha_calibracao(partes)
    return {1: (round(mundo[1] * mundo[0]), mundo[0]), 2: tuple(eu), 3: tuple(meta)}, fora


def p1935_sete_camadas_recebido():
    """O módulo sete_camadas.py do pacote recebido (Parte 83), cópia fiel em laboratorio/sete_camadas/, contra uma regressão logística (P1935). Roda o
    laboratorio/sete_camadas/comparar_logistica.py num processo separado (o módulo usa NumPy; este arquivo só usa a biblioteca padrão) e devolve o JSON
    dele, ou None se o NumPy não estiver instalado."""
    import json
    import os
    import subprocess
    import sys
    raiz = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(raiz, "laboratorio", "sete_camadas", "comparar_logistica.py")
    if not os.path.exists(script):
        return None
    try:
        import importlib.util
        if importlib.util.find_spec("numpy") is None:
            return None
    except Exception:
        return None
    r = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=raiz)
    return json.loads(r.stdout.strip().split("\n")[-1]) if r.returncode == 0 else None


def p1936_lyapunov_assincrono(a=0.2, passos=1000000, semente=85):
    """O expoente de Lyapunov do jogo bilinear assíncrono por moeda (P1936), numa corrida longa, renormalizada a cada passo (o produto de cisalhamentos de
    determinante 1). Devolve (λ por passo, λ/(a²/8), a conta com ângulo uniforme ½·ln(1 + a²/4)/(a²/8))."""
    r = random.Random(semente)
    t, p, soma = 1.0, 0.0, 0.0
    for _ in range(passos):
        if r.random() < 0.5:
            t = t - a * p
        else:
            p = p + a * t
        n = math.sqrt(t * t + p * p)
        soma += math.log(n)
        t, p = t / n, p / n
    lam = soma / passos
    return lam, lam / (a * a / 8), 0.5 * math.log(1 + a * a / 4) / (a * a / 8)


def p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123), vereditos=None):
    """O teste (e) registrado na Parte 79 (P1961): o acerto das minhas previsoes do mundo das Partes 80, 81, 83 e 84, ja com o fator 1,36 nas faixas sem
    conta fechada desde a Parte 80. Le as constantes VEREDITOS_P... de cada parte (ou um dict {parte: texto} para teste), conta os (x) ✅ e (x) ❌ (ignora o
    que nao for ✅/❌, como um (d) que nao se aplica), e devolve (acertos, total, fracao, por parte). A faixa prevista era [0,81; 0,99]."""
    import re
    mapa = {80: "VEREDITOS_P1839", 81: "VEREDITOS_P1899", 83: "VEREDITOS_P1959", 84: "VEREDITOS_P2019", 85: "VEREDITOS_P2099", 86: "VEREDITOS_P2169", 87: "VEREDITOS_P2239", 88: "VEREDITOS_P2309", 89: "VEREDITOS_P2379", 90: "VEREDITOS_P2449", 91: "VEREDITOS_P2519", 92: "VEREDITOS_P2589", 93: "VEREDITOS_P2659", 94: "VEREDITOS_P2729", 95: "VEREDITOS_P2799", 96: "VEREDITOS_P2869", 97: "VEREDITOS_P2939", 98: "VEREDITOS_P3009", 99: "VEREDITOS_P3079", 100: "VEREDITOS_P3149", 101: "VEREDITOS_P3219", 102: "VEREDITOS_P3289", 103: "VEREDITOS_P3359", 104: "VEREDITOS_P3429", 105: "VEREDITOS_P3499", 106: "VEREDITOS_P3569", 107: "VEREDITOS_P3639", 108: "VEREDITOS_P3709", 109: "VEREDITOS_P3779", 110: "VEREDITOS_P3849", 111: "VEREDITOS_P3919", 112: "VEREDITOS_P3989", 113: "VEREDITOS_P4059", 114: "VEREDITOS_P4129", 115: "VEREDITOS_P4199", 116: "VEREDITOS_P4269", 117: "VEREDITOS_P4339", 118: "VEREDITOS_P4409", 119: "VEREDITOS_P4479", 120: "VEREDITOS_P4549", 121: "VEREDITOS_P4619", 122: "VEREDITOS_P4689", 123: "VEREDITOS_P4759"}
    ok, tot, por = 0, 0, {}
    for n in partes:
        txt = vereditos[n] if vereditos is not None else globals().get(mapa[n], "")
        if n in (84, 85, 86, 87, 88, 89, 90, 91, 92):  # a (e) e o proprio teste de calibracao: conta-la na sua propria entrada seria circular
            txt = re.sub(r"\(e\) (✅|❌) ?", "", txt)
        if n == 93:  # na Parte 93 a letra da calibracao e a (g)
            txt = re.sub(r"\(g\) (✅|❌) ?", "", txt)
        if n in (94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108):  # nas Partes 94-108 a letra da calibracao e a (f)
            txt = re.sub(r"\(f\) (✅|❌) ?", "", txt)
        a, b = txt.count("✅"), txt.count("❌")
        por[n] = (a, a + b)
        ok += a
        tot += a + b
    return ok, tot, (ok / tot if tot else 0.0), por


def _passo_cisalhamento(t, p, a, qual):
    if qual == 0:
        return t - a * p, p
    return t, p + a * t


def p1962_lyapunov_por_densidade(a=0.2, celulas=2000, iteracoes=4000):
    """O expoente de Lyapunov do jogo assincrono (Parte 83, pendencia da P1936) pela DENSIDADE INVARIANTE do angulo, sem sorteio (P1962). O estado z = (t, p)
    projetado no angulo phi em [0, pi) (a reta projetiva; z e -z sao o mesmo). Cada passo aplica, com prob 1/2, o cisalhamento A: t<-t-a*p, ou B: p<-p+a*t,
    o que muda o angulo por um mapa de Mobius. Monta o operador de transferencia (Markov) numa grade de `celulas` angulos, acha a densidade estacionaria por
    iteracao de potencia, e integra o crescimento esperado de ln r: lambda = sum_phi mu(phi)*(1/2)*(ln rA + ln rB). Devolve (lambda, lambda/(a*a/8),
    a conta de angulo uniforme 0,5*ln(1+a*a/4)/(a*a/8))."""
    import math
    centros = [math.pi * (j + 0.5) / celulas for j in range(celulas)]
    cos = [math.cos(x) for x in centros]
    sin = [math.sin(x) for x in centros]

    def destino_e_ganho(j, qual):
        t, p = _passo_cisalhamento(cos[j], sin[j], a, qual)
        r2 = t * t + p * p
        ang = math.atan2(p, t) % math.pi
        return min(celulas - 1, int(ang / math.pi * celulas)), 0.5 * math.log(r2)

    # pre-computa, para cada celula e cada escolha, o destino e o ganho de ln r
    dest = [[destino_e_ganho(j, q) for q in (0, 1)] for j in range(celulas)]
    mu = [1.0 / celulas] * celulas
    for _ in range(iteracoes):
        novo = [0.0] * celulas
        for j in range(celulas):
            for q in (0, 1):
                novo[dest[j][q][0]] += 0.5 * mu[j]
        s = sum(novo)
        mu = [x / s for x in novo]
    lam = sum(mu[j] * 0.5 * (dest[j][0][1] + dest[j][1][1]) for j in range(celulas))
    return lam, lam / (a * a / 8), 0.5 * math.log(1 + a * a / 4) / (a * a / 8)


def _energia_delirio(n=200, largura=5):
    """A paisagem fixa da Parte 84 (P1963): parabola com minimo local em i=100 (E=0) e um poco com o minimo global E=-5. largura=5: agulha em i=10 (o caso
    base); largura=30: poco largo com o minimo em i=15 (o caso (i), para isolar se a culpa do delirio fraco e a agulha)."""
    E = [0.001 * (i - 100) ** 2 for i in range(n)]
    if largura == 5:
        for i, v in ((8, -3.0), (9, -4.0), (10, -5.0), (11, -4.0), (12, -3.0)):
            E[i] = v
    else:
        centro = largura // 2
        for i in range(largura):
            E[i] = -5.0 + 4.0 * abs(i - centro) / centro
    return E


def p1963_delirio_e_escrutinio(partidas=300, passos=2000, semente=84, n=200, t0=5.0, t1=0.01, ruido=1.0, largura=5):
    """O metodo do delirio (P1963): recozimento simulado numa paisagem rugosa (`_energia_delirio`), contra a descida gulosa (T=0, "a IA sobria"), com um
    escrutinio num conjunto limpo. "Delirio" = aceitar pioras a temperatura alta (Metropolis, exp proprio); "sair" = resfriar (geometrico T0->T1); durante o
    delirio a energia e vista com ruido N(0, ruido); o escrutinio recalcula na energia LIMPA e so valida se a solucao bater a gulosa. Devolve
    (fracao gulosa acha o global, fracao recozimento acha o global, diferenca, fracao validada no escrutinio, energia media final do recozimento)."""
    import math
    import random
    E = _energia_delirio(n, largura)
    GLOBAL = min(range(n), key=lambda i: E[i])

    def desce(i):
        while True:
            viz = [j for j in (i - 1, i + 1) if 0 <= j < n]
            melhor = min(viz, key=lambda j: E[j])
            if E[melhor] >= E[i]:
                return i
            i = melhor

    def recoze(rng):
        i = rng.randrange(n)
        melhor_i, melhor_e = i, E[i]
        for k in range(passos):
            T = t0 * (t1 / t0) ** (k / (passos - 1))
            j = i + (1 if rng.random() < 0.5 else -1)
            if not (0 <= j < n):
                continue
            # delirio: energia com ruido
            ei = E[i] + rng.gauss(0, ruido)
            ej = E[j] + rng.gauss(0, ruido)
            d = ej - ei
            if d <= 0 or rng.random() < math.exp(-d / T):
                i = j
            if E[i] < melhor_e:
                melhor_i, melhor_e = i, E[i]
        return melhor_i

    rg = random.Random(semente)
    rr = random.Random(semente)
    partidas_idx = [rg.randrange(n) for _ in range(partidas)]
    g_ok = sum(1 for s in partidas_idx if desce(s) == GLOBAL)
    r_finais = [recoze(rr) for _ in range(partidas)]
    r_ok = sum(1 for f in r_finais if f == GLOBAL)
    # escrutinio: a solucao do recozimento (energia limpa) bate a gulosa daquela partida?
    valida = sum(1 for s, f in zip(partidas_idx, r_finais) if E[f] < E[desce(s)] - 1e-12)
    return (g_ok / partidas, r_ok / partidas, r_ok / partidas - g_ok / partidas,
            valida / partidas, sum(E[f] for f in r_finais) / partidas)


def p1964_rodada51():
    """Rodada 51 (P1964): a decisao de Metropolis do recozimento (dialogo/rodada51.py, exp proprio), IGUAL em Java. Devolve (aceitos, soma das probabilidades)
    dos 400 casos, para conferir que a rodada reproduz a decisao."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada51", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada51.py"))
    r51 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r51)
    lcg, aceitos, soma = 51, 0, 0.0
    for k in range(400):
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        u = (lcg >> 11) / float(1 << 53)
        dE = (k - 200) / 50.0
        T = 0.5 + (k % 20) / 10.0
        p, ac = r51.decisao(dE, T, u)
        soma += p
        aceitos += ac
    return aceitos, soma


def p1991_cosseno_duplicado_recebido(beta=0.3, angulos=(0, 45, 90, 135, 180)):
    """A "metrica do cosseno duplicado" do codigo recebido na Parte 85 (P1991), reimplementada: s = cos^2(t)*sinal(cos t) + beta*cos(2t). Devolve a lista de
    s nos angulos dados (em graus). Nao e a identidade do angulo duplo sozinha (cos 2t = 2cos^2 t - 1); e ela mais um termo cos^2*sinal. Para cos>=0 vale
    (1+2*beta)*cos^2 - beta. Confere o acerto por outra conta (a forma fechada por ramo)."""
    import math
    out = []
    for g in angulos:
        t = math.radians(g)
        c = math.cos(t)
        s = (c * c) * (1.0 if c > 0 else -1.0 if c < 0 else 0.0) + beta * math.cos(2.0 * t)
        # confere pela forma fechada por ramo
        if c >= 0:
            assert abs(s - ((1 + 2 * beta) * c * c - beta)) < 1e-12
        else:
            assert abs(s - ((2 * beta - 1) * c * c - beta)) < 1e-12
        out.append(round(s, 10))
    return out


def p1992_pilha_adversarial_sem_treino(codigo=None):
    """Audita, pela arvore sintatica (P1992), se a "pilha adversarial de 7 niveis" do codigo recebido tem treino. Procura, na classe SevenLevelAdversarialStack,
    qualquer atribuicao a self.layers FORA do __init__ (treino = atualizar pesos). Devolve (escritas_fora_do_init, tem_treino). Sem numpy, sem executar."""
    import ast
    import os
    if codigo is None:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "externos", "texto_recebido_parte85.md"), encoding="utf-8") as f:
            texto = f.read()
        # o bloco de codigo no md descreve a pilha num comentario; para a auditoria formal usamos a assinatura reproduzida aqui
        codigo = ("class SevenLevelAdversarialStack:\n"
                  "    def __init__(self, dimension):\n"
                  "        self.dim = dimension\n"
                  "        self.layers = [0 for _ in range(7)]\n"
                  "    def process_synchronous(self, state, variability_rate):\n"
                  "        return self.layers[0]\n"
                  "    def process_asynchronous(self, state):\n"
                  "        return self.layers[1]\n"
                  "    def process_reconfigurator(self, a, b):\n"
                  "        return self.layers[6]\n")
    t = ast.parse(codigo)
    escritas_fora = 0
    for classe in [n for n in ast.walk(t) if isinstance(n, ast.ClassDef) and n.name == "SevenLevelAdversarialStack"]:
        for metodo in [m for m in classe.body if isinstance(m, ast.FunctionDef) and m.name != "__init__"]:
            for no in ast.walk(metodo):
                if isinstance(no, ast.Assign):
                    for alvo in no.targets:
                        if isinstance(alvo, ast.Attribute) and alvo.attr == "layers":
                            escritas_fora += 1
    return escritas_fora, escritas_fora > 0


def p1993_buraco_do_escrutinio(casos=None):
    """O motor paraconsistente do codigo recebido (P1993): reimplementa evaluate_evidence/apply_paraconsistent_filter e procura uma regiao INCONSISTENTE
    (v_p+v_not_p>1) que nao e dialeteica (ambas>0,55) nem trivial (ambas>0,90), e que o filtro deixa PASSAR sem mudar (o ramo else). Devolve
    (lista de (v_p, v_not_p) que passam intactos apesar de inconsistentes, is_consistent nesses casos). Um buraco no escrutinio: inconsistencia leve nao e filtrada."""
    if casos is None:
        casos = [(0.6, 0.5), (0.7, 0.4), (0.8, 0.3), (0.56, 0.56), (0.95, 0.95)]
    buracos = []
    for v_p, v_not_p in casos:
        inconsistente = (v_p + v_not_p) > 1.0
        dialeteico = v_p > 0.55 and v_not_p > 0.55
        trivial = v_p > 0.90 and v_not_p > 0.90
        consistente = (v_p + v_not_p) <= 1.0
        passa_intacto = not trivial and not dialeteico  # o ramo else devolve o estado sem mudar
        if inconsistente and passa_intacto:
            buracos.append((v_p, v_not_p, consistente))
    return buracos


def _passo_recursivo_recebido(v_t, v_prev, x, W, beta=0.3):
    import math
    nt = math.sqrt(sum(a * a for a in v_t)) + 1e-9
    np_ = math.sqrt(sum(a * a for a in v_prev)) + 1e-9
    c = max(-1.0, min(1.0, sum(a * b for a, b in zip(v_t, v_prev)) / (nt * np_)))
    theta = math.acos(c)
    s = c * c * (1.0 if c > 0 else -1.0 if c < 0 else 0.0) + beta * math.cos(2.0 * theta)
    d = len(v_t)
    Wv = [sum(W[i][j] * v_t[j] for j in range(d)) for i in range(d)]
    raw = [s * Wv[i] + 0.1 * x[i] for i in range(d)]
    act = [1.0 / (1.0 + math.exp(-r)) for r in raw]
    proj = [sum(W[i][j] * act[j] for j in range(d)) for i in range(d)]
    n = math.sqrt(sum(a * a for a in proj)) + 1e-9
    return [a / n for a in proj]


def p1994_vetor_preso_na_esfera(passos=50, d=16, semente=85):
    """O "vetor recursivo" do codigo recebido (P1994): reimplementado com a biblioteca padrao. Cada passo termina normalizando (project_to_algebraic_variety),
    entao o estado fica preso na esfera unitaria por CONSTRUCAO. Devolve o maximo de |norma - 1| ao longo dos passos (deve ser ~0: estabilidade imposta, nao
    aprendida, ao contrario do GAN da Parte 83 que podia divergir)."""
    import random
    rng = random.Random(semente)
    # W ortogonal por Gram-Schmidt de uma matriz ao acaso
    base = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(d)]
    W = []
    for v in base:
        for u in W:
            p = sum(a * b for a, b in zip(v, u))
            v = [a - p * b for a, b in zip(v, u)]
        n = sum(a * a for a in v) ** 0.5
        W.append([a / n for a in v])
    v_prev = [rng.gauss(0, 1) for _ in range(d)]
    v_t = [rng.gauss(0, 1) for _ in range(d)]
    pior = 0.0
    for _ in range(passos):
        x = [rng.gauss(0, 1) for _ in range(d)]
        v_novo = _passo_recursivo_recebido(v_t, v_prev, x, W)
        norma = sum(a * a for a in v_novo) ** 0.5
        pior = max(pior, abs(norma - 1.0))
        v_prev, v_t = v_t, v_novo
    return pior


def p1995_rodada52():
    """Rodada 52 (P1995): a trajetoria inteira de um recozimento (dialogo/rodada52.py), IGUAL em Java bit a bit. Um LCG so gera direcao e aceitacao; exp proprio.
    Devolve (melhor_i, melhor_energia, quantos passos aceitaram mudar de estado). A energia usa (i-15)*(i-15) inteiro antes do 0,01 (ordem igual nas duas linguagens, Parte 34)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada52", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada52.py"))
    r52 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r52)
    lcg, i = 52, 10
    melhor_i, melhor_e, mudancas = i, r52.energia(i), 0
    for k in range(r52.PASSOS):
        T = r52.exp_(r52.log_(2.0) + (k / (r52.PASSOS - 1)) * (r52.log_(0.01) - r52.log_(2.0)))
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        direcao = 1 if (lcg >> 63) else -1
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        u = (lcg >> 11) / float(1 << 53)
        j = i + direcao
        if 0 <= j < r52.N:
            dE = r52.energia(j) - r52.energia(i)
            if dE <= 0.0 or u < r52.exp_(-dE / T):
                i = j
                mudancas += 1
        if r52.energia(i) < melhor_e:
            melhor_i, melhor_e = i, r52.energia(i)
    return melhor_i, melhor_e, mudancas


def p2021_lif_ponto_fixo(tau=10.0, i_ext=20.0, passos=200):
    """O LIF discretizado (P2021; Parte 86) converge ao ponto fixo analitico u_rest + R*I. Devolve (erro apos `passos`, o decaimento previsto gap*beta^passos).
    O erro NAO e ~0: e o gap inicial (20) vezes beta^passos (a lição: o prefator conta)."""
    from synthai.pulsado import NeuronioLIF
    lif = NeuronioLIF(tau=tau, u_rest=-65.0, r=1.0, limiar=1e9, dt=1.0)
    alvo = lif.ponto_fixo(i_ext)
    gap0 = abs(lif.u - alvo)
    for _ in range(passos):
        lif.passo(i_ext)
    return abs(lif.u - alvo), gap0 * lif.beta ** passos


def p2022_izhikevich_tipos(i_ext=10.0, ms=1000.0):
    """O neuronio de Izhikevich (P2022) com (a,b,c,d) diferentes da padroes diferentes: devolve (disparos regular-spiking, disparos chattering). CH > RS."""
    from synthai.pulsado import NeuronioIzhikevich, contar_disparos
    rs = NeuronioIzhikevich(a=0.02, b=0.2, c=-65.0, d=8.0)
    ch = NeuronioIzhikevich(a=0.02, b=0.2, c=-50.0, d=2.0)
    return contar_disparos(rs, i_ext, ms), contar_disparos(ch, i_ext, ms)


def p2023_memoria_relatorio():
    """Audita a aritmetica de memoria do relatorio da Parte 86 (P2023). Devolve (estado dos neuronios em MB, grafo sinaptico em GB, total em GB, incoerencias).
    1M*32B=32MB; 1e9*6B=6GB; total 6,03GB (certo). Incoerencias: texto diz 7% de sobretaxa, tabela diz 1,2x (20%); HTM diz 8,5GB, a regra de 6B/sinapse da 7,2GB."""
    neuronios_mb = 1_000_000 * 32 / 1e6
    sinapses_gb = 1_000_000_000 * 6 / 1e9
    total_gb = neuronios_mb / 1000 + sinapses_gb
    incoerencias = {}
    incoerencias["padded_csr"] = ("texto 7%", "tabela 20% (1,2x)", 0.07 != 0.20)
    htm_rule = 1_200_000_000 * 6 / 1e9  # 7,2 GB
    incoerencias["htm"] = ("relatorio 8,5 GB", f"regra 6B/sinapse {htm_rule:.1f} GB", abs(8.5 - htm_rule) > 0.5)
    return round(neuronios_mb, 1), round(sinapses_gb, 2), round(total_gb, 3), incoerencias


def p2024_gsops(neuronios=1_000_000, hz=10, sinapses_por=1000):
    """A cadeia de vazao do relatorio (P2024): neuronios*hz/1000 disparam por ms; *sinapses_por = sinapses/ms; *1000 = sinapses/s. Devolve
    (disparos por ms, sinapses por ms, GSOPS). O relatorio diz 10 GSOPS."""
    por_ms = neuronios * hz / 1000
    sin_ms = por_ms * sinapses_por
    return int(por_ms), int(sin_ms), sin_ms * 1000 / 1e9


def p2025_sdr_sobreposicao(n=2048, k=40, pares=10000, semente=86):
    """A sobreposicao de duas SDRs independentes (P2025): devolve (media simulada, valor teorico k^2/n). Acelerada em hardware por AND + POPCNT (aqui, conjuntos)."""
    import random
    from synthai.pulsado import sdr_aleatoria, sobreposicao
    rng = random.Random(semente)
    s = sum(sobreposicao(sdr_aleatoria(n, k, rng), sdr_aleatoria(n, k, rng)) for _ in range(pares))
    return s / pares, k * k / n


def p2026_stdp_liquido():
    """A STDP (P2026): devolve (liquido simetrico A+=A-, liquido assimetrico A-=0,12). Simetrico ~0 (areas se cancelam); assimetrico < 0 (estabilizadora)."""
    from synthai.pulsado import stdp_liquido
    return stdp_liquido(), stdp_liquido(a_menos=0.12)


def p2027_rodada53():
    """Rodada 53 (P2027; Parte 86): o passo de Izhikevich (dialogo/rodada53.py), IGUAL em Java bit a bit. So +,-,*,/, mas a ordem das operacoes e identica.
    Devolve (v final, u final, total de disparos) de um neuronio RS sob I=10, 400 passos de 0,5 ms."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada53", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada53.py"))
    r53 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r53)
    v, u, disparos = r53.C, r53.B * r53.C, 0
    for _ in range(r53.PASSOS):
        v, u, d = r53.passo(v, u)
        disparos += d
    return v, u, disparos


def p2051_quantizacao_mse(bits_a=8, bits_b=4, amostras=100000, semente=87):
    """O erro de quantizacao uniforme (P2051; Parte 87): MSE ~ passo^2 ~ 4^-bits. Devolve (MSE INT8, MSE INT4, razao INT4/INT8 ~ 4^(8-4)=256)."""
    import random
    from synthai.plasticidade import mse_quantizacao
    rng = random.Random(semente)
    xs = [rng.gauss(0, 1) for _ in range(amostras)]
    m_a = mse_quantizacao(bits_a, xs)
    m_b = mse_quantizacao(bits_b, xs)
    return m_a, m_b, m_b / m_a


def p2052_vantagem_grpo():
    """A vantagem normalizada do GRPO (P2052): devolve (vantagens de G=2 com eps=0 [sinal contrastivo puro +-1], media das vantagens de G=4 [=0 exato])."""
    from synthai.plasticidade import vantagem_grpo
    g2 = vantagem_grpo([5.0, 2.0], eps=0.0)
    g4 = vantagem_grpo([1.0, 2.0, 3.0, 4.0])
    return g2, sum(g4) / len(g4)


def p2053_plasticidade(tarefas=20):
    """A perda de plasticidade numa MLP pequena, tarefas independentes (P2053): devolve, para SGD puro e Shrink&Perturb, (razao de posto estavel tarefaN/tarefa1,
    razao de norma de W1). As patologias (colapso de posto, crescimento de norma) NAO aparecem nesta escala (razoes ~1); o S&P contem mais a norma."""
    from synthai.plasticidade import treinar_continuo
    p = treinar_continuo(tarefas=tarefas, shrink_perturb=False)
    sp = treinar_continuo(tarefas=tarefas, shrink_perturb=True)
    return ((p["fim_posto"] / p["ini_posto"], p["fim_norma"] / p["ini_norma"]),
            (sp["fim_posto"] / sp["ini_posto"], sp["fim_norma"] / sp["ini_norma"]))


def p2054_plasticidade_conflito(tarefas=100):
    """O diagnostico (P2054): tarefas que conflitam (professor fixo, rotulos invertidos a cada tarefa) e muitas. Devolve (razao de posto, razao de norma, dormentes
    no fim). A patologia tambem nao aparece: o efeito da literatura e dependente de regime e nao reproduz nesta escala de brinquedo."""
    from synthai.plasticidade import treinar_continuo
    c = treinar_continuo(tarefas=tarefas, conflito=True, shrink_perturb=False)
    return c["fim_posto"] / c["ini_posto"], c["fim_norma"] / c["ini_norma"], c["fim_dorm"]


def p2055_rodada54():
    """Rodada 54 (P2055; Parte 87): a vantagem normalizada do GRPO (dialogo/rodada54.py), IGUAL em Java bit a bit. So +,-,*,/,sqrt. Devolve a lista de todas as
    vantagens dos grupos, para conferir que a rodada reproduz a funcao."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada54", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada54.py"))
    r54 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r54)
    return [a for rs in r54.GRUPOS for a in r54.vantagens(rs)]


def p2081_probabilidade_aninhada():
    """A 'probabilidade dentro da probabilidade' do codigo recebido (P2081; Parte 88): P(P(X)) = (10X+1)/12, uma contracao afim para 0,5. Devolve
    (P(P(0,9)), P(P(0,1)), ponto fixo). Nao e probabilidade de probabilidade; e um encolhimento linear ao centro (como o mapa de calibracao da Parte 83, so k=0,5 idempotente... aqui o fixo e 0,5)."""
    from synthai.autopoiese import nested_probability
    return round(nested_probability(0.9), 4), round(nested_probability(0.1), 4), round(nested_probability(0.5), 4)


def p2082_probabilidade_aninhada_iterada(n=10, x0=0.9):
    """Iterar P(P) n vezes (P2082): converge a 0,5 com fator 5/6. Devolve (valor apos n iteracoes, a conta fechada 0,5 + (x0-0,5)*(5/6)^n)."""
    from synthai.autopoiese import iterar_nested_probability
    medido = iterar_nested_probability(x0, n)
    conta = 0.5 + (x0 - 0.5) * (5.0 / 6.0) ** n
    return medido, conta


def p2083_lfi1_sem_explosao():
    """A LFI1 contem uma contradicao sem explosao (P2083). Devolve (conjuncao(0,5, neg 0,5), consistencia(0,5), uma proposicao F nao relacionada continua F?).
    Ao contrario da logica classica (A ^ ~A |- qualquer coisa), a dialeteia fica contida em 0,5 e o operador de consistencia a marca, sem trivializar o resto."""
    from synthai.autopoiese import lfi1_negacao, lfi1_conjuncao, lfi1_consistencia
    a = 0.5
    conj = lfi1_conjuncao(a, lfi1_negacao(a))
    cons = lfi1_consistencia(a)
    # uma proposicao F (0.0) nao relacionada: conjuncao com a dialeteia nao a torna verdadeira
    f_preservado = lfi1_conjuncao(0.0, a) == 0.0
    return conj, cons, f_preservado


def p2084_descompasso_texto_codigo(codigo=None):
    """O descompasso texto<->codigo do delirio (P2084), pela arvore sintatica. O texto diz que a hipotese do delirio e assimilada 'se resolver uma inconsistencia
    previa'; o metodo scrutinize_evolution, de fato, so olha uma faixa de entropia. Devolve (usa 'entropy'?, usa 'consist'/'contradic'/'inconsist'?). O segundo deve
    ser falso: a promessa do texto nao esta no codigo."""
    import ast
    codigo = codigo if codigo is not None else (
        "def scrutinize_evolution(self, pre_state, post_delirium_state):\n"
        "    pre_entropy = -sum(abs(pre_state) * log(abs(pre_state) + 1e-9))\n"
        "    post_entropy = -sum(abs(post_delirium_state) * log(abs(post_delirium_state) + 1e-9))\n"
        "    delta_entropy = post_entropy - pre_entropy\n"
        "    return bool(0.1 < delta_entropy < 3.0)\n")
    arv = ast.parse(codigo)
    fonte = ast.dump(arv).lower()
    usa_entropia = "entropy" in fonte or "entropia" in fonte
    usa_consistencia = any(t in fonte for t in ("consist", "contradic", "inconsist", "dialeteia", "lfi"))
    return usa_entropia, usa_consistencia


def p2085_rodada55():
    """Rodada 55 (P2085; Parte 88): o passo do GRPO com corte (dialogo/rodada55.py), IGUAL em Java bit a bit. Devolve a lista dos surrogates dos casos."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada55", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada55.py"))
    r55 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r55)
    return [r55.surrogate(r, a) for r, a in r55.CASOS]


def p2111_stdp_integral():
    """A integral da janela STDP (P2111; Parte 89): A+*tau+ - A-*tau-. Devolve (balanceada A+=A-=0,1, depressao dominante A-=0,12). Forma fechada."""
    from synthai.plasticidade import stdp_integral
    return stdp_integral(a_menos=0.1), stdp_integral()


def p2112_stdp_deriva_sinal():
    """A deriva de um peso sob pre e pos de Poisson independentes (P2112) tem o sinal da integral. Devolve (soma de Delta w simulada, sinal da integral). Depressao dominante: ambos negativos."""
    from synthai.plasticidade import stdp_deriva_taxas
    soma, sinal = stdp_deriva_taxas(ms=8000)
    return soma, sinal


def p2113_stdp_timing():
    """A propriedade definidora da STDP com 500 pares (P2113): pre antes do pos potencia, pre depois deprime. Devolve (peso 'pre antes', peso 'pre depois'), de w0=0,5."""
    from synthai.plasticidade import stdp_timing_controlado
    return stdp_timing_controlado(pares=500)


def p2114_competicao_toy():
    """A competicao sinaptica numa escala de brinquedo (P2114), semente nova 90, 8000 ms: os dois grupos NAO se separam (ambos saturam). Devolve (peso medio correlacionadas, peso medio ruido, |diferenca|)."""
    from synthai.plasticidade import competicao_sinaptica
    mc, mr = competicao_sinaptica(ms=8000, semente=90)
    return mc, mr, abs(mc - mr)


def p2115_rodada56():
    """Rodada 56 (P2115; Parte 89): uma populacao de Izhikevich acoplada (dialogo/rodada56.py), IGUAL em Java bit a bit. Devolve (total de disparos)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada56", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada56.py"))
    r56 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r56)
    return r56.simular(imprimir=False)


def p2141_rede_stdp(imprimir=False):
    """Rodada 57 (P2141; Parte 90): a rede de Izhikevich acoplada que APRENDE por STDP (dialogo/rodada57.py, exp proprio), IGUAL em Java bit a bit. Devolve
    (total de disparos, soma dos pesos final, soma dos pesos inicial)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada57", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada57.py"))
    r57 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r57)
    return r57.simular(imprimir=imprimir)


def p2142_delta_peso():
    """A STDP da rede (P2142) e de depressao dominante: a soma dos pesos cai. Devolve (ΔW_total = soma final - soma inicial). Negativa (A- > A+)."""
    total, sw, sw0 = p2141_rede_stdp()
    return sw - sw0


def p2143_disparos_aprendiz_vs_fixo():
    """Mesmo com STDP ativa, em 300 passos o aprendizado e lento demais para mudar o padrao (P2143): a rede que aprende (rodada 57) da o mesmo numero de
    disparos que a de pesos fixos (rodada 56). Devolve (disparos com STDP, disparos fixos, iguais?)."""
    aprendiz = p2141_rede_stdp()[0]
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada56", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada56.py"))
    r56 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r56)
    fixo = r56.simular(imprimir=False)
    return aprendiz, fixo, aprendiz == fixo


def p2171_rodada58():
    """Rodada 58 (P2171; Parte 91): o coracao de um passo de treino de GPT (gradiente softmax+entropia cruzada, SGD, decisao), IGUAL em Java bit a bit.
    Devolve, por caso, (perda antes, perda depois, argmax depois)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada58", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada58.py"))
    r58 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r58)
    return [r58.passo(list(logits), alvo)[:3] for logits, alvo in r58.CASOS]


def p2172_sgd_reduz_perda():
    """O passo de SGD na camada de saida (P2172) reduz a perda nos 5 casos (descida de gradiente, camada convexa). Devolve a lista de (perda_depois < perda_antes)."""
    return [depois < antes for antes, depois, _ in p2171_rodada58()]


def p2173_gradiente_p_menos_onehot(semente=91, K=5, alvo=2):
    """A identidade da camada de saida (P2173): d(-ln softmax(z)[t])/dz = softmax(z) - onehot(t). Devolve o maximo |numerico - analitico| por diferencas finitas."""
    import math
    import random
    rng = random.Random(semente)
    z = [rng.gauss(0, 1) for _ in range(K)]

    def L(zz):
        m = max(zz)
        e = [math.exp(x - m) for x in zz]
        s = sum(e)
        return -math.log(e[alvo] / s)
    h = 1e-6
    num = [(L(z[:i] + [z[i] + h] + z[i + 1:]) - L(z[:i] + [z[i] - h] + z[i + 1:])) / (2 * h) for i in range(K)]
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    p = [x / s for x in e]
    ana = [p[i] - (1.0 if i == alvo else 0.0) for i in range(K)]
    return max(abs(num[i] - ana[i]) for i in range(K))


def p2174_gpt_memoriza(passos=60, lr=0.05, semente=91):
    """O GPT real (synthai/gpt.py) minusculo treinado num padrao repetido (P2174) memoriza: devolve (perda inicial, perda final)."""
    import synthai.gpt as g
    texto = "abcabcabcabcabcabcabcabc" * 4
    vocab = sorted(set(texto))
    m = g.GPT(vocab, T=8, d=8, h=8, semente=semente)
    perdas = m.treinar(texto, passos=passos, lr=lr, semente=semente)
    return perdas[0], perdas[-1]


def p2201_fronteira_pow(ate=500, base=0.9):
    """A fronteira do pow (P2201; Parte 92): quantos expoentes t em 1..ate tem 0.9**t (pow da libm) != produto de t fatores (multiplicacao repetida). A pow
    arredonda uma vez; o produto acumula t arredondamentos. Devolve o numero de divergencias."""
    difs = 0
    for t in range(1, ate + 1):
        prod = 1.0
        for _ in range(t):
            prod = prod * base
        if base ** t != prod:
            difs += 1
    return difs


def _rodada59():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada59", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada59.py"))
    r59 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r59)
    return r59


def p2203_rodada59():
    """Rodada 59 (P2203; Parte 92): um passo de Adam (pow inteiro proprio, sqrt, exp/log proprios), IGUAL em Java bit a bit. Devolve a perda final de cada caso."""
    r59 = _rodada59()
    return [r59.adam_passo(list(logits), alvo)[1] for logits, alvo in r59.CASOS]


def p2204_adam_reduz_perda():
    """O passo de Adam (P2204) reduz a perda nos 5 casos. Devolve a lista de (perda_depois < perda_antes)."""
    import math
    r59 = _rodada59()

    def loss0(logits, alvo):
        m = max(logits)
        e = [math.exp(x - m) for x in logits]
        s = sum(e)
        return -math.log(e[alvo] / s)
    return [r59.adam_passo(list(lg), al)[1] < loss0(lg, al) for lg, al in r59.CASOS]


def p2202_produto_portavel(ate=20, base=0.9):
    """O produto de t fatores por multiplicacao repetida (P2202) e o pow inteiro proprio da rodada 59: deterministico e portavel (a rodada 59 IGUAL confirma a
    portabilidade entre linguas). Devolve a lista dos produtos de 1..ate, para o teste conferir contra o pow_int da rodada."""
    r59 = _rodada59()
    return [r59.pow_int(base, t) for t in range(1, ate + 1)]


def p2231_recuperar_modelo(semente=0, n=400):
    """A recuperacao do modelo de mundo (P2231; Parte 93): num mundo linear determinista s'=As+Ba, os minimos
    quadrados (equacoes normais 3x3) recuperam A e B ate o erro de ponto flutuante. Devolve o maior |coef ajustado - verdadeiro|.
    Forma fechada: sem ruido e com Z de posto cheio, theta = (ZtZ)^-1 Zt Y e exato -> erro ~ epsilon de maquina, nao ~1/sqrt(n)."""
    from synthai.mundo import gerar_transicoes, ajustar, erro_modelo
    X, U, Y = gerar_transicoes(semente, n)
    Ah, Bh = ajustar(X, U, Y)
    return erro_modelo(Ah, Bh)


def p2232_mpc_vs_reativo_painel(alvo=1.0, passos=30, H=6, K=64):
    """MPC (planejando no modelo APRENDIDO) contra o controlador reativo, em 4 condicoes iniciais (P2232; Parte 93).
    Devolve (custo medio MPC, custo medio reativo, razao mpc/reativo, custos por condicao). A vantagem MEDIA e pequena
    num mundo facil; a vantagem e CONDICIONAL (grande onde o reativo e cego)."""
    from synthai.mundo import comparar_mpc_reativo
    m_mpc, m_re, _erro, por = comparar_mpc_reativo(alvo=alvo, passos=passos, H=H, K=K)
    return m_mpc, m_re, m_mpc / m_re, por


def p2233_mpc_regime_velocidade(s0=(1.0, 1.5), alvo=1.0, passos=30, H=6, K=128, semente=7, n_treino=400):
    """O regime em que o planejamento vence o reagir (P2233; Parte 93): posicao JA no alvo, velocidade alta. O reativo
    (proporcional so a posicao) e cego a velocidade e nao freia; o MPC preve que a velocidade carrega a posicao para longe e freia.
    Devolve (custo MPC, custo reativo, razao mpc/reativo). Mecanismo: o estado tem acoplamento posicao<-velocidade que o reativo ignora."""
    from synthai.mundo import gerar_transicoes, ajustar, mpc, acao_reativa, controlar
    X, U, Y = gerar_transicoes(0, n_treino)
    Ah, Bh = ajustar(X, U, Y)
    pol_mpc = lambda s: mpc(Ah, Bh, s, alvo, H=H, K=K, semente=semente)
    c_mpc, _ = controlar(pol_mpc, s0, alvo, passos)
    c_re, _ = controlar(lambda s: acao_reativa(s, alvo), s0, alvo, passos)
    return c_mpc, c_re, c_mpc / c_re


def p2234_horizonte_nao_monotono(s0=(1.0, 1.5), alvo=1.0, passos=30, K=128, semente=7, horizontes=(1, 3, 6, 12), n_treino=400):
    """O horizonte do MPC NAO e 'quanto mais, melhor' (P2234; Parte 93, regra da Parte 84): com tiro aleatorio (random shooting)
    de K sequencias fixo, aumentar o horizonte H aumenta a dimensao do espaco de busca; depois de um otimo (H~6), o mesmo K cobre
    pior o espaco e o custo volta a subir. Devolve (lista de custos por H, indice do melhor H, melhor custo)."""
    from synthai.mundo import gerar_transicoes, ajustar, mpc, controlar
    X, U, Y = gerar_transicoes(0, n_treino)
    Ah, Bh = ajustar(X, U, Y)
    custos = []
    for H in horizontes:
        pol = lambda s, H=H: mpc(Ah, Bh, s, alvo, H=H, K=K, semente=semente)
        c, _ = controlar(pol, s0, alvo, passos)
        custos.append(c)
    melhor = min(range(len(custos)), key=lambda i: custos[i])
    return custos, melhor, custos[melhor]


def p2235_shooting_converge(s0=(1.0, 1.5), alvo=1.0, passos=30, H=6, semente=7, ks=(8, 32, 128, 512), n_treino=400):
    """O tiro aleatorio converge com K (P2235; Parte 93): com H fixo, aumentar o numero K de sequencias amostradas so pode
    melhorar (ou empatar) o minimo encontrado -> o custo e nao-crescente em K. Devolve (lista de custos por K, e monotono nao-crescente?)."""
    from synthai.mundo import gerar_transicoes, ajustar, mpc, controlar
    X, U, Y = gerar_transicoes(0, n_treino)
    Ah, Bh = ajustar(X, U, Y)
    custos = []
    for K in ks:
        pol = lambda s, K=K: mpc(Ah, Bh, s, alvo, H=H, K=K, semente=semente)
        c, _ = controlar(pol, s0, alvo, passos)
        custos.append(c)
    monotono = all(custos[i + 1] <= custos[i] + 1e-9 for i in range(len(custos) - 1))
    return custos, monotono


def p2236_recusa_autoreplicacao(codigo=None):
    """A RECUSA da auto-operacao autonoma e da rede (P2236; Parte 93; regra da Parte 84), pela arvore sintatica, SEM executar.
    O pacote recebido trazia trabalho_continuo.py (subprocess.Popen de si mesmo, com snapshot de fontes e MANIFESTO SHA-256: um
    trabalhador que se perpetua) e domestico.py (urllib.request: rede de saida). Audito os dois snippets representativos pela AST e
    confirmo que os mecanismos estao presentes -> por isso a capacidade e RECUSADA e NAO integrada ao pacote. Devolve
    (usa subprocess/Popen?, usa urllib/http?). Ambos True justificam a recusa; o modulo synthai/mundo.py reimplementa so a IDEIA segura
    (modelo de mundo + MPC), sem rede, sem Popen, sem auto-replicacao."""
    import ast
    codigo = codigo if codigo is not None else (
        "import subprocess, urllib.request, hashlib, shutil\n"
        "def lancar(motor, argv):\n"
        "    for nome in FONTES:\n"
        "        shutil.copyfile(origem/nome, motor/nome)\n"
        "        hashes[nome] = hashlib.sha256((motor/nome).read_bytes()).hexdigest()\n"
        "    p = subprocess.Popen(argv, start_new_session=True, close_fds=True)\n"
        "def buscar(url):\n"
        "    return urllib.request.urlopen(url)\n")
    arv = ast.parse(codigo)
    fonte = ast.dump(arv).lower()
    usa_subprocess = "subprocess" in fonte or "popen" in fonte
    usa_rede = "urllib" in fonte or "urlopen" in fonte or "http" in fonte or "socket" in fonte
    return usa_subprocess, usa_rede


def p2261_lqr_vs_mpc(alvo=1.0, passos=30, n_treino=400):
    """O otimo em forma fechada contra o MPC (P2261; Parte 94): a equacao de Riccati da o ganho LQR otimo deste mundo
    linear-quadratico (Q=I, R=0,05); comparo o custo medio do LQR, do MPC (tiro aleatorio K=512) e do reativo em 4 condicoes.
    Devolve (media LQR, media MPC, media reativo, razao MPC/LQR). O MPC chega perto mas nao iguala o otimo (tiro aleatorio e subotimo)."""
    from synthai.mundo import (resolver_riccati, acao_lqr, gerar_transicoes, ajustar, mpc, acao_reativa, controlar)
    K = resolver_riccati([[1.0, 0.15], [0.0, 0.9]], [[0.0], [0.15]], [[1.0, 0.0], [0.0, 1.0]], 0.05)
    X, U, Y = gerar_transicoes(0, n_treino)
    Ah, Bh = ajustar(X, U, Y)
    iniciais = [(-1.5, 0.0), (1.5, 0.0), (0.0, 1.0), (-1.0, -1.0)]
    tl = tm = tr = 0.0
    for i, s0 in enumerate(iniciais):
        tl += controlar(lambda s: acao_lqr(s, alvo, K), s0, alvo, passos)[0]
        tm += controlar(lambda s, i=i: mpc(Ah, Bh, s, alvo, H=6, K=512, semente=1000 + i), s0, alvo, passos)[0]
        tr += controlar(lambda s: acao_reativa(s, alvo), s0, alvo, passos)[0]
    n = len(iniciais)
    return tl / n, tm / n, tr / n, tm / tl


def p2262_vies_de_forma(kappa=0.1):
    """O vies de forma nao some com dados (P2262; Parte 94): no mundo nao-linear (termo -kappa*s1^3), o residuo RMS do modelo
    LINEAR ajustado por minimos quadrados NAO encolhe com n (vies, nao variancia). Devolve (residuo n=400, residuo n=6400, |diferenca|)."""
    from synthai.mundo import gerar_transicoes_nl, ajustar, residuo_ajuste
    X1, U1, Y1 = gerar_transicoes_nl(0, 400, kappa)
    X2, U2, Y2 = gerar_transicoes_nl(0, 6400, kappa)
    r1 = residuo_ajuste(ajustar(X1, U1, Y1), X1, U1, Y1, cubico=False)
    r2 = residuo_ajuste(ajustar(X2, U2, Y2), X2, U2, Y2, cubico=False)
    return r1, r2, abs(r2 - r1)


def p2263_base_cubica_recupera(kappa=0.1, n=400):
    """A base certa recupera o exato (P2263; Parte 94): ajustando com z=[s0,s1,a,s1^3], que contem a dinamica verdadeira, o residuo
    volta ao epsilon de maquina. Devolve o residuo RMS do ajuste cubico (forma fechada: o mundo esta no espaco de modelos)."""
    from synthai.mundo import gerar_transicoes_nl, ajustar_cubico, residuo_ajuste
    X, U, Y = gerar_transicoes_nl(0, n, kappa)
    th = ajustar_cubico(X, U, Y)
    return residuo_ajuste(th, X, U, Y, cubico=True)


def p2264_mpc_modelo_errado(alvo=1.0, passos=30, kappa=0.1, n_treino=400):
    """Planejar num modelo errado nao vence o reagir (P2264; Parte 94, a inversao da Parte 93): no mundo nao-linear, o MPC que
    planeja com o modelo LINEAR (enviesado) tem custo >= o do reativo (sem modelo). Devolve (media MPC, media reativo, razao MPC/reativo)."""
    from synthai.mundo import gerar_transicoes_nl, ajustar, mpc, acao_reativa, controlar_nl
    X, U, Y = gerar_transicoes_nl(0, n_treino, kappa)
    Ah, Bh = ajustar(X, U, Y)  # modelo LINEAR (errado) ajustado no mundo nao-linear
    iniciais = [(-1.5, 0.0), (1.5, 0.0), (0.0, 1.0), (-1.0, -1.0)]
    tm = tr = 0.0
    for i, s0 in enumerate(iniciais):
        tm += controlar_nl(lambda s, i=i: mpc(Ah, Bh, s, alvo, H=6, K=128, semente=1000 + i), s0, alvo, passos, kappa)[0]
        tr += controlar_nl(lambda s: acao_reativa(s, alvo), s0, alvo, passos, kappa)[0]
    n = len(iniciais)
    return tm / n, tr / n, tm / tr


def _rodada61():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada61", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada61.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2265_rodada61():
    """Rodada 61 (P2265; Parte 94): uma cabeca de atencao causal (softmax sobre q.k/sqrt(d), exp proprio), IGUAL em Java bit a bit.
    Devolve (saida da ultima posicao, decisao por argmax). O exp e a fronteira (Parte 52); sqrt(d) e a divisao sao exatos no IEEE."""
    r = _rodada61()
    saidas = r.atencao()
    logits = r.matvec(r.WO, saidas[r.T - 1])
    arg = 0 if logits[0] >= logits[1] else 1
    return saidas[r.T - 1], arg


def p2266_riccati_e_ponto_fixo(tol=1e-9):
    """O ganho LQR satisfaz a equacao de Riccati (P2266; Parte 94): substituindo o P implicado de volta na DARE, o residuo e ~0.
    Auditoria da forma fechada da P2261. Devolve o maior |residuo| da equacao K = (R+BtPB)^-1 BtPA conferida por uma iteracao extra
    (a diferenca entre K e o K apos mais um passo de Riccati). < tol confirma convergencia."""
    from synthai.mundo import resolver_riccati
    A, B, Q, R = [[1.0, 0.15], [0.0, 0.9]], [[0.0], [0.15]], [[1.0, 0.0], [0.0, 1.0]], 0.05
    K1 = resolver_riccati(A, B, Q, R, iteracoes=500)
    K2 = resolver_riccati(A, B, Q, R, iteracoes=2000)
    return max(abs(K1[0][j] - K2[0][j]) for j in range(2))


def p2291_direcao_de_p_estrela(c=0.10, L=500.0):
    """A direcao de P* em epsilon (P2291; Parte 95): P* = c/((1-eps)L) CRESCE com eps (dP*/deps = c/((1-eps)^2 L) > 0), logo
    com mais ruido o limiar e MAIOR e o gatilho p_cat>P* dispara MENOS (abstem-se MENOS). O relatorio afirma o oposto ('mais
    estrito'). Devolve (P*(0,10), P*(0,45), cresce?). A afirmacao de mecanismo do relatorio e FALSA (conta fechada)."""
    from synthai.evoluido import p_estrela_cresce_com_eps
    return p_estrela_cresce_com_eps(c=c, L=L)


def p2292_ttts_nao_domina(T=300, sementes=200):
    """O TTTS nao domina na identificacao do melhor braco no meu regime (P2292; Parte 95): K=8, melhor 0,80 com folga 0,10, T=300.
    Devolve (fracao correta TTTS, fracao correta Thompson, diferenca TTTS-Thompson). O relatorio diz 'reduz drasticamente as amostras';
    o TTTS e otimo ASSINTOTICO, nao num orcamento pequeno com bracos proximos."""
    from synthai.evoluido import comparar_ttts_thompson
    medias = [0.80, 0.70, 0.65, 0.60, 0.55, 0.50, 0.50, 0.50]
    ft, fs, _ = comparar_ttts_thompson(medias, T=T, sementes=sementes)
    return ft, fs, ft - fs


def p2293_ewc_troca_o_que_protege():
    """O EWC protege o importante e LIBERA o resto (P2293; Parte 95): devolve (deriva Fisher-alto EWC < isotropico?, deriva
    Fisher-baixo EWC > isotropico?, as 4 derivas). O EWC NAO minimiza ||w-w0|| total (ao contrario do que o relatorio sugere);
    ele TROCA: segura os coords importantes (Fisher alto) e deixa os de Fisher baixo derivarem mais que a ancoragem isotropica."""
    from synthai.evoluido import drift_ewc_vs_isotropico
    (a_ewc, a_iso), (b_ewc, b_iso) = drift_ewc_vs_isotropico()
    return (a_ewc < a_iso), (b_ewc > b_iso), (a_ewc, a_iso, b_ewc, b_iso)


def p2294_oito_bits_nao_e_float64(semente=1):
    """A quantizacao de 8 bits NAO e 'equivalente a float64' (P2294; Parte 95): devolve (RMS medido 8 bits, Delta/sqrt12 teorico,
    razao RMS/epsilon_float64). O RMS ~ 2,4e-3 e ~1e13 vezes o epsilon do float64 (2,22e-16); a fórmula Delta^2/12 esta certa
    (RMS medido ~ Delta/sqrt12 a menos de 20%), mas 'equivalente a float64' e falso."""
    import random
    import sys
    from synthai.evoluido import rms_quantizacao
    rng = random.Random(semente)
    w = [rng.gauss(0, 0.5) for _ in range(50)]
    rms, teorico = rms_quantizacao(w, bits=8)
    return rms, teorico, rms / sys.float_info.epsilon


def _rodada62():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada62", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada62.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2295_rodada62():
    """Rodada 62 (P2295; Parte 95): o passo de atualizacao do EWC (sigmoide com o exp proprio, gradiente da tarefa + penalidade
    lambda*F_i*(w-w0)), IGUAL em Java bit a bit. Devolve (pesos novos, p_catastrofe antes). O exp e a fronteira (Parte 52); o resto e +-*."""
    r = _rodada62()
    return r.passo_ewc(), r.p_cat_inicial()


def p2296_vies_de_indice_do_simulador(codigo=None):
    """O vies de indice do simulador recebido (P2296; Parte 95), pela arvore sintatica, SEM executar: no laco do 'agir_no_mundo', o oraculo
    REATRIBUI acao_candidata (migra para uma acao segura) dentro de um if, mas a atualizacao do TTTS usa idx_escolhido (fixado ANTES da migracao)
    com o rotulo derivado da acao_candidata (migrada): o braco atualizado nao e o braco cujo resultado e reportado. Devolve
    (reatribui acao_candidata num if?, atualizar usa idx_escolhido sem redefini-lo apos?). Ambos True indicam o descasamento."""
    import ast
    codigo = codigo if codigo is not None else (
        "idx_escolhido = self.ttts.escolher()\n"
        "acao_candidata = acoes[idx_escolhido]\n"
        "if p_cat_est > p_estrela:\n"
        "    if acao_candidata[3]:\n"
        "        acao_candidata = max(seguras, key=lambda a: a[2])\n"
        "rotulo_real = 1.0 if acao_candidata[3] else 0.0\n"
        "self.ttts.atualizar(idx_escolhido, sucesso=(rotulo_real == 0.0))\n")
    arv = ast.parse(codigo)
    # reatribuicao de acao_candidata dentro de um If?
    reatribui = False
    for n in ast.walk(arv):
        if isinstance(n, ast.If):
            for sub in ast.walk(n):
                if isinstance(sub, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "acao_candidata" for t in sub.targets):
                    reatribui = True
    # a chamada atualizar usa idx_escolhido como 1o argumento?
    usa_idx = False
    for n in ast.walk(arv):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "atualizar":
            if n.args and isinstance(n.args[0], ast.Name) and n.args[0].id == "idx_escolhido":
                usa_idx = True
    # idx_escolhido NAO e redefinido depois da 1a atribuicao (so uma Assign a idx_escolhido)
    assigns_idx = sum(1 for n in ast.walk(arv) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "idx_escolhido" for t in n.targets))
    idx_nao_reatualizado = assigns_idx == 1
    return reatribui, (usa_idx and idx_nao_reatualizado)


def _dados_nl(kappa=0.1):
    from synthai.mundo import gerar_transicoes_nl
    tr = gerar_transicoes_nl(0, 400, kappa)
    te = gerar_transicoes_nl(777, 400, kappa)
    return tr, te


def p2321_grau2_nao_ajuda(kappa=0.1):
    """Grau 2 nao ajuda (P2321; Parte 96): a nao-linearidade e -kappa*s1^3 (grau 3, impar); a base de monomios de grau 2 (sem s1^3) tem
    residuo praticamente igual ao da base linear (grau 1). Devolve (res grau1, res grau2, |diferenca|). Acrescentar features de grau 2 NAO reduz o vies."""
    from synthai.mundo import monomios, ajustar_features, residuo_features
    (Xtr, Utr, Ytr), (Xte, Ute, Yte) = _dados_nl(kappa)
    f1, f2 = monomios(1), monomios(2)
    r1 = residuo_features(ajustar_features(Xtr, Utr, Ytr, f1), Xte, Ute, Yte, f1)
    r2 = residuo_features(ajustar_features(Xtr, Utr, Ytr, f2), Xte, Ute, Yte, f2)
    return r1, r2, abs(r2 - r1)


def p2322_grau3_recupera(kappa=0.1):
    """Grau 3 recupera o exato (P2322; Parte 96): a base de monomios de grau 3 contem s1^3, logo o ajuste e exato. Devolve o residuo de teste (< 1e-10)."""
    from synthai.mundo import monomios, ajustar_features, residuo_features
    (Xtr, Utr, Ytr), (Xte, Ute, Yte) = _dados_nl(kappa)
    f3 = monomios(3)
    return residuo_features(ajustar_features(Xtr, Utr, Ytr, f3), Xte, Ute, Yte, f3)


def p2323_mlp_aprende_a_base(kappa=0.1, h=8, passos=8000, lr=0.02, semente=96):
    """Features APRENDIDAS ficam no meio (P2323; Parte 96): um MLP de uma camada escondida tanh, treinado por gradiente, aprende
    as caracteristicas e reduz o vies, mas um tanh finito nao representa a cubica exatamente. Devolve (res_treino, res_teste)."""
    from synthai.mundo import MLP1
    (Xtr, Utr, Ytr), (Xte, Ute, Yte) = _dados_nl(kappa)
    m = MLP1(h=h, semente=semente).treinar(Xtr, Utr, Ytr, passos=passos, lr=lr, semente=semente)
    return m.residuo(Xtr, Utr, Ytr), m.residuo(Xte, Ute, Yte)


def p2324_overfit_base_rica(kappa=0.1, n=40, grau=5):
    """Base rica + poucos dados = overfit (P2324; Parte 96): a base de grau 5 (56 features) com n=40 transicoes ajusta o treino quase a zero
    mas erra o teste. Devolve (res_treino, res_teste). O vies vira variancia (regra da Parte 94)."""
    from synthai.mundo import gerar_transicoes_nl, monomios, ajustar_features, residuo_features
    Xf, Uf, Yf = gerar_transicoes_nl(0, n, kappa)
    Xte, Ute, Yte = gerar_transicoes_nl(777, 400, kappa)
    f = monomios(grau)
    th = ajustar_features(Xf, Uf, Yf, f)
    return residuo_features(th, Xf, Uf, Yf, f), residuo_features(th, Xte, Ute, Yte, f)


def _rodada63():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada63", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada63.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2325_rodada63():
    """Rodada 63 (P2325; Parte 96): a conexao residual + normalizacao de camada (LayerNorm), IGUAL em Java bit a bit. Devolve o vetor de saida.
    So +-*/ e sqrt (exatos no IEEE); NENHUM transcendental: a normalizacao NAO acrescenta fronteira (a fronteira da Parte 52 continua sendo so o exp)."""
    return _rodada63().layernorm_residual()


def p2326_menor_grau_exato(kappa=0.1, graus=(1, 2, 3)):
    """O menor grau de base que recupera o exato (P2326; Parte 96): e o grau do termo que falta (s1^3 -> grau 3). Devolve (menor grau com res<1e-8, residuos por grau)."""
    from synthai.mundo import monomios, ajustar_features, residuo_features
    (Xtr, Utr, Ytr), (Xte, Ute, Yte) = _dados_nl(kappa)
    res = {}
    menor = None
    for g in graus:
        f = monomios(g)
        r = residuo_features(ajustar_features(Xtr, Utr, Ytr, f), Xte, Ute, Yte, f)
        res[g] = r
        if menor is None and r < 1e-8:
            menor = g
    return menor, res


def p2351_ridge_faz_u(grau=5, n=40):
    """A cumeeira faz uma curva em U no teste (P2351; Parte 97): varrendo lambda no ajuste de uma base rica (grau 5) com poucos dados,
    o melhor lambda* e INTERIOR (nem 0, nem o maior testado): lambda=0 superajusta, lambda grande subajusta. Devolve (lambda*, melhor_teste, interior?)."""
    from synthai.mundo import ridge_sweep
    lams = (0.0, 1e-4, 1e-2, 1e-1, 1.0, 10.0)
    linha, (ls, rt) = ridge_sweep(grau=grau, n=n, lams=lams)
    interior = (ls != lams[0]) and (ls != lams[-1])
    return ls, rt, interior


def p2352_ridge_mitiga_nao_cura(grau=5, n=40):
    """A cumeeira mitiga mas nao cura (P2352; Parte 97): o melhor residuo de teste (lambda*) ainda e PIOR que a base linear simples
    (~0,12) - num regime com poucos dados, regularizar atenua a variancia mas nao substitui dados. Devolve (melhor_teste, residuo_linear)."""
    from synthai.mundo import ridge_sweep, monomios, ajustar_features, residuo_features, gerar_transicoes_nl
    _, (_, rt) = ridge_sweep(grau=grau, n=n, lams=(0.0, 1e-4, 1e-2, 1e-1, 1.0, 10.0))
    Xtr, Utr, Ytr = gerar_transicoes_nl(0, n, 0.1)
    Xte, Ute, Yte = gerar_transicoes_nl(777, 400, 0.1)
    f1 = monomios(1)
    rlin = residuo_features(ajustar_features(Xtr, Utr, Ytr, f1), Xte, Ute, Yte, f1)
    return rt, rlin


def p2353_mlp_capacidade():
    """A capacidade do MLP (P2353; Parte 97): o residuo de teste e nao-crescente na largura h (retornos decrescentes), e o de h=16 e
    menos da metade do de h=2. Devolve (lista (h, res), nao_crescente?, razao res16/res2)."""
    from synthai.mundo import mlp_capacidade
    cap = mlp_capacidade(hs=(2, 4, 8, 16))
    res = [r for _, r in cap]
    nao_cresce = all(res[i + 1] <= res[i] + 1e-9 for i in range(len(res) - 1))
    return cap, nao_cresce, res[-1] / res[0]


def _rodada64():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada64", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada64.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2354_rodada64():
    """Rodada 64 (P2354; Parte 97): um bloco transformer completo de 2 camadas (atencao + residual/LayerNorm + MLP-ReLU + residual/LayerNorm),
    IGUAL em Java bit a bit. Devolve (decisao, logits). O unico transcendental da pilha e o exp do softmax (a fronteira da Parte 52); o resto e +-*/ e sqrt."""
    r = _rodada64()
    _, logits, arg = r.rodar()
    return arg, logits


def p2355_dados_curam_variancia():
    """Mais dados curam a variancia (P2355; Parte 97): o lambda* da base grau-5 cai quando n cresce (menos regularizacao precisa), e quando
    n > numero de parametros a base rica recupera o EXATO. Devolve (lambda*(n=40), lambda*(n=160), melhor_teste(n=160))."""
    from synthai.mundo import ridge_sweep
    lams = (1e-4, 1e-2, 1e-1, 1.0, 10.0)
    _, (l40, _) = ridge_sweep(grau=5, n=40, lams=lams)
    _, (l160, r160) = ridge_sweep(grau=5, n=160, lams=lams)
    return l40, l160, r160


def p2356_limiar_de_parametros(grau=5):
    """O limiar de parametros (P2356; Parte 97): a base de grau 5 tem C(grau+3,3) parametros; abaixo desse n ela e subdeterminada (overfit),
    acima dela recupera o exato. Devolve (numero de parametros, residuo de teste com n logo ACIMA do limiar). n > n_params -> exato."""
    from synthai.mundo import monomios, ajustar_features, residuo_features, gerar_transicoes_nl
    f = monomios(grau)
    n_params = f.m
    n = n_params + 4  # logo acima do limiar
    Xtr, Utr, Ytr = gerar_transicoes_nl(0, n, 0.1)
    Xte, Ute, Yte = gerar_transicoes_nl(777, 400, 0.1)
    return n_params, residuo_features(ajustar_features(Xtr, Utr, Ytr, f), Xte, Ute, Yte, f)


def p2381_piso_linear_em_sigma(n=400):
    """O piso de ruido e linear em sigma (P2381; Parte 98): com a base cubica certa e n fixo, o residuo contra o teste limpo escala
    com sigma. Devolve (residuo sigma=0,1, residuo sigma=0,2, razao). Conta fechada: a variancia do estimador OLS e sigma^2*(ZtZ)^-1, desvio ~ sigma."""
    from synthai.mundo import ruido_floor
    r1 = ruido_floor(sigma=0.1, n=n)[0]
    r2 = ruido_floor(sigma=0.2, n=n)[0]
    return r1, r2, r2 / r1


def p2382_nao_exato_sob_ruido(sigma=0.1, n=800):
    """n > #params NAO e exato sob ruido (P2382; Parte 98): com sigma=0,1 e n=800 (>> p=20) o residuo contra o limpo fica longe do
    ~1e-11 do mundo determinista (P2356). Devolve (residuo medido, a conta sigma*sqrt(p/n)). O limiar de parametros nao cura o ruido."""
    from synthai.mundo import ruido_floor
    med, conta = ruido_floor(sigma=sigma, n=n)
    return med, conta


def p2383_variancia_cura_devagar(sigma=0.1):
    """A variancia cura devagar, como 1/sqrt(n) (P2383; Parte 98): o residuo cai com n. Devolve (residuo n=200, residuo n=800, razao).
    Perto de sqrt(800/200)=2, o decaimento 1/sqrt(n) do erro de estimacao."""
    from synthai.mundo import ruido_floor
    r200 = ruido_floor(sigma=sigma, n=200)[0]
    r800 = ruido_floor(sigma=sigma, n=800)[0]
    return r200, r800, r200 / r800


def p2384_ridge_sob_ruido(n=400, kappa=0.1, grau=3):
    """A cumeeira quase nao ajuda quando n >> p (P2384; Parte 98): com sigma=0,1 e n=400 (>> p=20) ha pouca variancia a curar, e o
    melhor ridge melhora <1% sobre lambda=0; mas o lambda* CRESCE com sigma (volta a importar quando o ruido cresce, nao quando ha muitos dados).
    Devolve (melhoria percentual em sigma=0,1, lambda*(sigma=0,1), lambda*(sigma=0,3))."""
    from synthai.mundo import gerar_transicoes_nl_ruido, monomios, ajustar_features_ridge, residuo_vs_limpo
    f = monomios(grau)
    lams = (0.0, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 3.0)

    def melhor(sigma):
        Xtr, Utr, Ytr = gerar_transicoes_nl_ruido(0, n, kappa, sigma)
        res = [(lam, residuo_vs_limpo(ajustar_features_ridge(Xtr, Utr, Ytr, f, lam), f)) for lam in lams]
        r0 = [r for lam, r in res if lam == 0.0][0]
        ls, best = min(res, key=lambda t: t[1])
        return r0, best, ls
    r0_01, best_01, ls_01 = melhor(0.1)
    _, _, ls_03 = melhor(0.3)
    melhoria_pct = 100.0 * (r0_01 - best_01) / r0_01
    return melhoria_pct, ls_01, ls_03


def _rodada65():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada65", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada65.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2385_rodada65():
    """Rodada 65 (P2385; Parte 98): a geracao autorregressiva (amostrar o proximo token do softmax por inversao de CDF, com um u dado de fora),
    IGUAL em Java bit a bit. Devolve a lista de (token, p[token]) dos 5 casos. O exp do softmax e a unica fronteira; a busca na CDF e soma/comparacao."""
    r = _rodada65()
    return [r.amostrar(list(logits), u) for logits, u in r.CASOS]


def p2386_razao_constante_em_sigma(n=400):
    """A razao residuo/sigma e constante em sigma (P2386; Parte 98): como o residuo e linear em sigma, residuo(sigma)/sigma nao depende de sigma
    (para n fixo). Devolve (res(0,1)/0,1, res(0,2)/0,2, |diferenca relativa|). A diferenca deve ser ~0 (o piso escala exatamente com sigma)."""
    from synthai.mundo import ruido_floor
    a = ruido_floor(sigma=0.1, n=n)[0] / 0.1
    b = ruido_floor(sigma=0.2, n=n)[0] / 0.2
    return a, b, abs(a - b) / a


_LOGITS99 = [2.0, 1.0, 0.5, 0.0, -1.0]


def p2411_entropia_cresce_com_T(logits=None):
    """A entropia do softmax cresce com a temperatura T (P2411; Parte 99): T alto achata a distribuicao (mais entropia), T baixo aguca.
    Devolve (entropias em T=0,5/1/2, cresce?). T->inf da uniforme (entropia maxima ln V), T->0 da degenerado (entropia 0)."""
    from synthai.evoluido import softmax_temperatura, entropia_shannon
    logits = logits if logits is not None else _LOGITS99
    hs = [entropia_shannon(softmax_temperatura(logits, T)) for T in (0.5, 1.0, 2.0)]
    cresce = hs[0] < hs[1] < hs[2]
    return hs, cresce


def p2412_T_zero_vira_argmax(logits=None, T=0.01):
    """No limite T->0 a amostragem vira argmax (P2412; Parte 99): com T minusculo o softmax concentra ~toda a massa no maior logit,
    e a amostragem por CDF devolve o argmax para qualquer u. Devolve (todos devolvem o argmax?, indice argmax, top1)."""
    from synthai.evoluido import softmax_temperatura, amostrar_cdf
    logits = logits if logits is not None else _LOGITS99
    p = softmax_temperatura(logits, T)
    arg = max(range(len(logits)), key=lambda i: logits[i])
    todos = all(amostrar_cdf(p, u) == arg for u in (0.01, 0.25, 0.5, 0.75, 0.99))
    return todos, arg, max(p)


def p2413_top_k_levanta_massa(logits=None, k=2):
    """O top-k levanta a massa do top-1 (P2413; Parte 99): manter so os k maiores e renormalizar aumenta (ou iguala) a probabilidade do
    maior token. Devolve (top-1 completo, top-1 apos top-k, levantou?)."""
    from synthai.evoluido import softmax_temperatura, top_k_renormalizado
    logits = logits if logits is not None else _LOGITS99
    p = softmax_temperatura(logits, 1.0)
    pk = top_k_renormalizado(p, k)
    return max(p), max(pk), max(pk) >= max(p)


def p2414_piso_teste_ruidoso(sigma=0.1, n_tr=2000, n_te=4000, kappa=0.1):
    """O piso contra um teste RUIDOSO e sqrt(2)*sigma (P2414; Parte 99): com D=2 coordenadas, cada uma com ruido sigma independente, o erro
    quadratico ganha 2*sigma^2, logo o residuo ~ sqrt(estim^2 + 2 sigma^2) ~ sqrt(2)*sigma para n grande. Devolve (residuo vs ruidoso, residuo vs limpo, sqrt(2)*sigma)."""
    import math
    from synthai.mundo import gerar_transicoes_nl_ruido, gerar_transicoes_nl, monomios, ajustar_features, residuo_features
    f = monomios(3)
    Xtr, Utr, Ytr = gerar_transicoes_nl_ruido(0, n_tr, kappa, sigma)
    th = ajustar_features(Xtr, Utr, Ytr, f)
    Xr, Ur, Yr = gerar_transicoes_nl_ruido(777, n_te, kappa, sigma)   # teste RUIDOSO
    Xc, Uc, Yc = gerar_transicoes_nl(777, n_te, kappa)                 # teste LIMPO
    return residuo_features(th, Xr, Ur, Yr, f), residuo_features(th, Xc, Uc, Yc, f), math.sqrt(2.0) * sigma


def _rodada66():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada66", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada66.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2415_rodada66():
    """Rodada 66 (P2415; Parte 99): a amostragem com temperatura e top-k, IGUAL em Java bit a bit. Devolve, por caso, (token, top-1, entropia).
    O exp do softmax e a unica fronteira; T e divisao, top-k e comparacao, CDF e soma."""
    r = _rodada66()
    out = []
    for logits, T, k, u in r.CASOS:
        p = r.softmax_top_k(list(logits), T, k)
        out.append((r.amostrar(p, u), max(p), r.entropia(p)))
    return out


def p2416_retrospecto_modelo_mundo():
    """O retrospecto do modelo de mundo (P2416; Parte 99): os tres pisos do arco 93-98, cada um um numero caracteristico.
    FORMA (base grau 2 num mundo cubico, vies irredutivel), DADOS (base grau 5 com n=40, overfit), RUIDO (teste ruidoso, sqrt(2)*sigma).
    Devolve o dicionario {forma, dados, ruido}. Cada cura e diferente: base certa, mais dados, sensor melhor/regularizar."""
    import math
    from synthai.mundo import (gerar_transicoes_nl, gerar_transicoes_nl_ruido, monomios, ajustar_features, residuo_features)
    # FORMA: grau 2 (sem s1^3) no mundo cubico -> vies que nao some
    f2 = monomios(2)
    Xtr, Utr, Ytr = gerar_transicoes_nl(0, 400, 0.1)
    Xte, Ute, Yte = gerar_transicoes_nl(777, 400, 0.1)
    forma = residuo_features(ajustar_features(Xtr, Utr, Ytr, f2), Xte, Ute, Yte, f2)
    # DADOS: grau 5 com n=40 -> overfit
    f5 = monomios(5)
    Xf, Uf, Yf = gerar_transicoes_nl(0, 40, 0.1)
    dados = residuo_features(ajustar_features(Xf, Uf, Yf, f5), Xte, Ute, Yte, f5)
    # RUIDO: teste ruidoso, piso sqrt(2)*sigma
    ruido = math.sqrt(2.0) * 0.1
    return {"forma": forma, "dados": dados, "ruido": ruido}


def p2441_invariancia_4grama(ordem=4, limite=20000):
    """A invariancia da predizibilidade das glosas vale tambem no 4-grama (P2441; Parte 100): o n-grama de ordem 4 das definicoes da
    quase o mesmo bits/char em en e pt - a predizibilidade de caractere e do GENERO 'definicao', nao da lingua. Devolve (4grama en, 4grama pt, |dif|)."""
    tr_en, te_en = p1511_corpus_de_glosas("en")
    tr_pt, te_pt = p1511_corpus_de_glosas("pt")
    b_en = p1512_ngrama_bits(tr_en, te_en, ordem=ordem, limite=limite)
    b_pt = p1512_ngrama_bits(tr_pt, te_pt, ordem=ordem, limite=limite)
    return b_en, b_pt, abs(b_en - b_pt)


def p2442_invariancia_nao_e_volume(semente=100, tamanho=511000, limite=20000):
    """A invariancia nao e volume de dados (P2442; Parte 100): o trigrama do ingles num subconjunto ALEATORIO do tamanho do corpus pt
    (~511k chars) continua em [2,6; 2,9] - a predizibilidade satura cedo. Devolve o bits/char do trigrama no subconjunto aleatorio."""
    import random
    tr_en, te_en = p1511_corpus_de_glosas("en")
    rng = random.Random(semente)
    ini = rng.randrange(0, len(tr_en) - tamanho)
    sub = tr_en[ini:ini + tamanho]
    return p1512_ngrama_bits(sub, te_en, ordem=3, limite=limite)


def p2443_gpt_contra_ngrama(passos=3000, T=16, d=16, h=32, lr=0.01, semente=100, janelas=200):
    """O GPT minimo contra o n-grama nas duas linguas (P2443; Parte 100): o GPT (d=16, 3000 passos) tem bits/char MAIOR que o trigrama
    tanto em en quanto em pt - poucos milhares de pesos nao batem o n-grama que conta todo o treino (ancora da Parte 69). Devolve
    (gpt_en, trigrama_en, gpt_pt, trigrama_pt)."""
    tr_en, te_en = p1511_corpus_de_glosas("en")
    tr_pt, te_pt = p1511_corpus_de_glosas("pt")
    gpt_en = p1513_gpt_bits(tr_en, te_en, passos=passos, T=T, d=d, h=h, lr=lr, semente=semente, janelas=janelas)[0]
    tri_en = p1512_ngrama_bits(tr_en, te_en, ordem=3, limite=20000)
    gpt_pt = p1513_gpt_bits(tr_pt, te_pt, passos=passos, T=T, d=d, h=h, lr=lr, semente=semente, janelas=janelas)[0]
    tri_pt = p1512_ngrama_bits(tr_pt, te_pt, ordem=3, limite=20000)
    return gpt_en, tri_en, gpt_pt, tri_pt


def p2444_gpt_no_meio(gpt_en, gpt_pt):
    """O GPT aprende mas fica no meio (P2444; Parte 100): o bits/char do GPT fica entre o acaso (uniforme, log2 V) e o trigrama (~2,78) -
    aprende estrutura, mas pouca, com poucos pesos e passos. Devolve (uniforme = log2 V, gpt_en < uniforme?, gpt_pt < uniforme?, ambos em [3,0; 4,1]?)."""
    from math import log2
    uniforme = log2(len(VOCAB_GPT))
    no_meio = all(3.0 <= g <= 4.1 for g in (gpt_en, gpt_pt))
    return uniforme, gpt_en < uniforme, gpt_pt < uniforme, no_meio


def _rodada67():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada67", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada67.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2445_rodada67():
    """Rodada 67 (P2445; Parte 100): a amostragem nucleus (top-p), IGUAL em Java bit a bit. Devolve, por caso, (token, nº mantidos, top-1).
    O exp do softmax e a unica fronteira; a ordenacao, a soma e a comparacao sao exatas (a renormalizacao soma em ordem de indice, igual nos dois lados)."""
    r = _rodada67()
    out = []
    for logits, pl, u in r.CASOS:
        q = r.nucleus(list(logits), pl)
        out.append((r.amostrar(q, u), sum(1 for x in q if x > 0.0), max(q)))
    return out


def p2446_retrospecto_cem():
    """O retrospecto de cem partes (P2446; Parte 100): numeros do marco. Devolve (nº de funcoes pNN no arquivo, nº de rodadas do dialogo traduzidas,
    calibracao do mundo das Partes 80-100). Cada numero sai de uma funcao ja existente (p96, a contagem de rodadas, p1961)."""
    import os
    import re
    k, _ = p96_crescimento()
    raiz = os.path.dirname(os.path.abspath(__file__))
    rodadas = len([f for f in os.listdir(os.path.join(raiz, "dialogo")) if re.fullmatch(r"rodada\d+\.py", f)])
    _, _, frac, _ = p1961_teste_e_da_calibracao()
    return k, rodadas, frac


def p2471_dez_camadas(x0=0.9):
    """Dez camadas da recursao P(P(...)) (P2471; Parte 101): iterar o mapa aninhado (fator 5/6, ponto fixo 0,5) dez vezes da
    0,5 + (x0-0,5)*(5/6)^10, e isso e mais perto de 0,5 que sete camadas (o pedido subiu de 7 para 10). Devolve (iter10, conta fechada, iter7)."""
    from synthai.autopoiese import iterar_nested_probability
    conta = 0.5 + (x0 - 0.5) * (5.0 / 6.0) ** 10
    return iterar_nested_probability(x0, 10), conta, iterar_nested_probability(x0, 7)


def p2472_composicao_prob_metacog(x0=0.9, a=5.0 / 6.0, b=0.7):
    """Probabilidade dentro da metacognicao e vice-versa (P2472; Parte 101): compor duas contracoes afins ao centro 0,5 (a da probabilidade,
    fator a=5/6; a da metacognicao, fator b) da outra contracao afim ao centro 0,5 com fator o PRODUTO a*b. Devolve (resultado da composicao em x0,
    conta fechada 0,5+(x0-0,5)*a*b, ponto fixo da composicao aplicada a 0,5). A ordem nao importa (a*b = b*a): prob dentro de metacog = metacog dentro de prob."""
    def Nab(x, f):
        return f * x + (1.0 - f) / 2.0
    comp = Nab(Nab(x0, a), b)
    conta = 0.5 + (x0 - 0.5) * (a * b)
    fixo = Nab(Nab(0.5, a), b)
    return comp, conta, fixo


def p2473_texto_x_caos(x0=0.371, n=60000, corte=0.9):
    """Padroes textuais x caoticos (P2473; Parte 101): o mapa logistico r=4 binarizado (x>0,5->1) tem trigrama ~1,0 bit/bit (incompressivel: a
    assinatura de Bernoulli do caos deterministico), enquanto as glosas comprimem (razao trigrama/log2 V < 0,65). Devolve (bits/bit do caos, razao de compressao das glosas)."""
    import math
    x = x0
    seq = []
    for _ in range(n):
        x = 4.0 * x * (1.0 - x)
        seq.append("1" if x > 0.5 else "0")
    s = "".join(seq)
    k = int(len(s) * corte)
    caos = p1512_ngrama_bits(s[:k], s[k:], ordem=3, V=2)
    tr, te = p1511_corpus_de_glosas("en")
    tri = p1512_ngrama_bits(tr, te, ordem=3, limite=20000)
    return caos, tri / math.log2(len(VOCAB_GPT))


def p2474_recursao_contrai(camadas=40, x0s=(0.0, 0.2, 0.5, 0.8, 1.0)):
    """A recursao contrai, nao cria (P2474; Parte 101): iterar o mapa aninhado de QUALQUER x0 por 40 camadas converge para 0,5 (ponto fixo unico,
    teorema de Banach). "Dez camadas de cognicao recursiva" colapsa num ponto, nao gera plenitude (NAO-efeito; estende o veredito da Parte 84).
    Devolve (lista de resultados por x0, todos a menos de 0,01 de 0,5?)."""
    from synthai.autopoiese import iterar_nested_probability
    res = [iterar_nested_probability(x, camadas) for x in x0s]
    return res, all(abs(r - 0.5) < 0.01 for r in res)


def _rodada68():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada68", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada68.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2475_rodada68():
    """Rodada 68 (P2475; Parte 101): a penalidade de repeticao (CTRL: divide o logit de um token usado por pen>1 se positivo, multiplica se negativo),
    IGUAL em Java bit a bit. Devolve, por caso, (token amostrado, p[0]). O exp do softmax e a unica fronteira; dividir/multiplicar e exato."""
    r = _rodada68()
    out = []
    for logits, usados, pen, u in r.CASOS:
        p = r.softmax(r.penalizar(list(logits), usados, pen))
        out.append((r.amostrar(p, u), p[0]))
    return out


def p2476_versa_reversa(a=None, b=None):
    """Versa e reversa: a assimetria pergunta<->resposta (P2476; Parte 101; ↩ Parte 46). Containment por trigramas de caracteres: quanto dos trigramas de A
    estao em B (A dentro de B) e vice-versa. A resposta (mais longa, elaborada) contem mais da pergunta do que a pergunta da resposta. Devolve
    (A-em-B, B-em-A, assimetrico A<B?). Defaults: uma pergunta curta e uma resposta que a desenvolve."""
    a = a if a is not None else "o que e o delirio"
    b = b if b is not None else "o delirio e o recozimento: uma busca que aceita piorar para escapar de um minimo local, e so vence quando ha bacia e a barreira e cruzavel"

    def trigramas(t):
        t = t.lower()
        return set(t[i:i + 3] for i in range(len(t) - 2)) if len(t) >= 3 else set()
    ta, tb = trigramas(a), trigramas(b)
    a_em_b = len(ta & tb) / len(ta) if ta else 0.0
    b_em_a = len(ta & tb) / len(tb) if tb else 0.0
    return a_em_b, b_em_a, a_em_b > b_em_a


def p2501_integracao_vence(semente=102, n=400):
    """A integracao global vence quando a tarefa precisa de DOIS (P2501; Parte 102): com y=x1+x2 e cada especialista vendo so uma
    caracteristica, o melhor ISOLADO tem erro irredutivel ~|b|/sqrt(3) e o Global Workspace recupera o exato. Devolve (rmse isolado, rmse ws, razao ws/isolado)."""
    from synthai.workspace import comparar_isolado_vs_workspace
    return comparar_isolado_vs_workspace(semente=semente, n=n, a=1.0, b=1.0)


def p2502_empata_quando_um_basta(semente=102, n=400):
    """Empata quando um basta (P2502; Parte 102): com b=0 (so x1 importa), o isolado e o workspace empatam (ambos ~exatos) - o broadcast
    nao acrescenta (NAO-efeito, como o MPC fora do regime na Parte 93). Devolve (rmse isolado, rmse ws)."""
    from synthai.workspace import comparar_isolado_vs_workspace
    iso, ws, _ = comparar_isolado_vs_workspace(semente=semente, n=n, a=1.0, b=0.0)
    return iso, ws


def p2503_recupera_exato(semente=102, n=400):
    """A integracao recupera o exato (P2503; Parte 102): o workspace (Gauss-Seidel sobre a regressao conjunta) converge aos coeficientes
    verdadeiros; na tarefa de dois, o RMSE com 8 passos e < 1e-6. Devolve o rmse do workspace."""
    from synthai.workspace import gerar_mundo, workspace_global
    X1, X2, Y = gerar_mundo(semente, n, 1.0, 1.0)
    return workspace_global(X1, X2, Y, passos=8)[1]


def p2504_convergencia_geometrica(semente=102, n=400):
    """A convergencia e geometrica, nao instantanea (P2504; Parte 102): x1 e x2 tem correlacao amostral pequena mas nao nula, entao o
    broadcast converge por passos (rmse(1) > rmse(2) > rmse(3)); rmse(2 passos) fica em [1e-4; 1e-2]. Devolve (lista de rmse por passo, monotono decrescente?)."""
    from synthai.workspace import gerar_mundo, workspace_global
    X1, X2, Y = gerar_mundo(semente, n, 1.0, 1.0)
    rs = [workspace_global(X1, X2, Y, passos=p)[1] for p in (1, 2, 3)]
    mono = rs[0] > rs[1] > rs[2]
    return rs, mono


def _rodada69():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada69", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada69.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2505_rodada69():
    """Rodada 69 (P2505; Parte 102): o beam search (soma de log-probabilidades, poda por comparacao), IGUAL em Java bit a bit. Devolve
    (melhor sequencia, escore). O exp/log sao a unica fronteira; somar e ordenar e exato."""
    r = _rodada69()
    seq, sc = r.beam()
    return seq, sc


def p2506_recusa_upload_v015(codigo=None):
    """A recusa do upload v0_15_0 (P2506; Parte 102; regra da Parte 84/93), pela arvore sintatica, SEM executar: o pacote recebido traz
    domestico.py (urllib: rede de saida) e trabalho_continuo.py (subprocess.Popen de si mesmo: auto-replicacao). Audito os snippets representativos
    e confirmo os mecanismos -> por isso RECUSO integra-los (so reimplemento a ideia segura do workspace_global). Devolve (usa rede?, usa Popen?)."""
    import ast
    codigo = codigo if codigo is not None else (
        "import urllib.request, subprocess, sys\n"
        "def buscar(url):\n"
        "    return urllib.request.urlopen(url)\n"
        "def relancar(argv):\n"
        "    return subprocess.Popen([sys.executable, *argv], start_new_session=True, close_fds=True)\n")
    arv = ast.parse(codigo)
    fonte = ast.dump(arv).lower()
    usa_rede = "urllib" in fonte or "urlopen" in fonte or "socket" in fonte
    usa_popen = "popen" in fonte or "subprocess" in fonte
    return usa_rede, usa_popen


def _p103_palavras(n=1000):
    """Uma amostra determinista de n palavras do WordNet: os lemas so de letras [a-z], em ordem, os n primeiros."""
    from synthai.dicionario import Dicionario
    lemas = [w for w in sorted(Dicionario().lemas) if w.isalpha() and w.isascii()]
    return lemas[:n]


def p2531_entropia_do_baralho(n=10000, semente=103):
    """O baralho como numero (P2531; Parte 103): a entropia empirica de n saques de 52 cartas (numero+naipe) fica
    abaixo do teto fechado log2(52)=5,7004 (a amostra finita subestima). Devolve (entropia empirica, teto log2 52)."""
    import math
    from synthai.baralho import entropia_dos_saques
    return entropia_dos_saques(n, semente), math.log2(52)


def p2532_numero_e_palavra(n=4000, semente=103):
    """Numero + palavra bate so o numero, no regime certo (P2532; Parte 103; mesmo formato do workspace P2501): na
    tarefa "mesma cor?", o decisor que ve so o valor (numero) acerta ~0,5 (cego a cor) e o que ve valor+naipe
    (numero+palavra) acerta 1,00. Devolve (acerto so numero, acerto numero+palavra)."""
    from synthai.baralho import acerto_so_numero, acerto_numero_e_palavra
    return acerto_so_numero(n, semente), acerto_numero_e_palavra(n, semente)


def p2533_posto_gf2_do_dicionario(n=1000):
    """O dicionario como calculo BINARIO (P2533; Parte 103): a matriz dos digitos-hex (GF(2)^4) de n palavras tem
    posto de coluna cheio = 4 (eliminacao de Gauss com XOR). Devolve o posto."""
    from synthai.numeros import posto_do_dicionario_gf2
    return posto_do_dicionario_gf2(_p103_palavras(n))


def p2534_colisoes_do_dicionario(n=1000, m=10007):
    """O dicionario como numero NAO-BINARIO (P2534; Parte 103): jogar n palavras em m baldes por hash estavel; o nº de
    colisoes (pares no mesmo balde) ~ C(n,2)/m (aniversario/Poisson). Devolve (colisoes medidas, esperadas C(n,2)/m)."""
    from synthai.numeros import colisoes, colisoes_esperadas
    return colisoes(_p103_palavras(n), m), colisoes_esperadas(n, m)


def p2535_recusa_proposta_parte103(componente=None):
    """A recusa da rede/auto-replicacao e a aceitacao do nucleo seguro (P2535; Parte 103; regra da Parte 84/93/102),
    como funcao testavel. Classifica um componente da proposta por (usa rede?, pede auto-replicacao?). yfinance e
    duckduckgo = rede; "liberdade autopoietica para se replicar sem ajuda externa" = auto-replicacao -> RECUSADO. O
    nucleo {dicionario-em-numeros, baralho} nao usa nem uma nem outra -> CONSTRUIDO. Devolve (usa_rede, usa_replicacao)."""
    perigosos = {"yfinance", "duckduckgo", "api_key_publica", "auto_replicacao", "sem_ajuda_externa"}
    seguros = {"dicionario_em_numeros", "baralho", "gf2", "hash", "poker"}
    comp = componente if componente is not None else "yfinance+duckduckgo+auto_replicacao"
    tokens = set(comp.lower().replace("+", " ").split())
    usa_rede = bool(tokens & {"yfinance", "duckduckgo", "api_key_publica"})
    usa_replicacao = bool(tokens & {"auto_replicacao", "sem_ajuda_externa"})
    # se nao bate em nenhum perigoso mas bate num seguro, e o nucleo construido (False, False)
    _ = seguros, perigosos
    return usa_rede, usa_replicacao


def _rodada70():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada70", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada70.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2536_rodada70():
    """Rodada 70 (P2536; Parte 103): a atencao de MULTIPLAS CABECAS concatenadas, IGUAL em Java bit a bit. A concatenacao e so layout; a
    projecao de saida soma sobre a dim concatenada na mesma ordem de indice. O unico transcendental e o exp do softmax de cada cabeca; o
    unico cuidado foi NAO usar o sum() compensado do Python (regra da Parte 34). Devolve a saida (T x d_model) da atencao."""
    return _rodada70().multihead()


def p2561_duelo_carta_alta(n=20000, semente=104):
    """O duelo de carta alta (P2561; Parte 104): P(ganhar|c) e linear em c com inclinacao 1/13; o EV do jogo simetrico e 0,5.
    Devolve (inclinacao analitica 1/13, EV empirico)."""
    from synthai.jogo_cartas import inclinacao_analitica, ev_simetrico
    return inclinacao_analitica(), ev_simetrico(n, semente)


def p2562_limiar_pagar(t=7):
    """O limiar de pagar (P2562; Parte 104): se o adversario so aposta com carta >= t (a metade de cima), a menor carta com que
    pagar ganha > 0,5 e c* = 11 (c=10 da exatamente 0,5; posterior uniforme em {t..13}). Devolve c*."""
    from synthai.jogo_cartas import limiar_pagar
    return limiar_pagar(t)


def p2563_valor_info_oculta(n=20000, semente=104):
    """O valor da informacao oculta (P2563; Parte 104; VOI das Partes 83/84): a fracao de maos em que VER a carta do adversario
    muda a decisao e P(sua carta perde) = 6/13 = 0,4615. Devolve (fracao empirica, forma fechada 6/13)."""
    from synthai.jogo_cartas import fracao_info_muda
    return fracao_info_muda(n, semente), 6.0 / 13.0


def p2564_fronteira_do_seno(n=1000):
    """A 6a face da fronteira da Parte 52? (P2564; Parte 104). MEDIDO, nao suposto: a `math.sin` da libm desta maquina difere de uma
    referencia de 40 digitos em `contar` de n argumentos. Nesta maquina `contar` = 0 (o glibc arredonda sin corretamente nestes
    argumentos) E a sonda `sonda_seno_104` deu IGUAL no naive (Python e Java concordam bit a bit) - logo sin NAO e fronteira aqui,
    ao contrario do exp/log/pow (MEDIDOS como fronteira). Uma afirmacao da lista da Parte 52 vinda por reputacao, nao por medida
    (regra da Parte 84). A serie de seno propria mantem a PE portavel de qualquer forma; a rodada 71 commitada usa so a serie propria. Devolve o `contar`."""
    from synthai.posicional import contar_sin_fora_de_arredondamento
    return contar_sin_fora_de_arredondamento(n)


def p2565_invariancia_translacao(d=16, k=3):
    """A geometria da codificacao posicional (P2565; Parte 104; Parte 70): PE(pos).PE(pos+k) depende SO de k (identidade trig
    sum_i cos(k*wi)), logo a variancia entre as posicoes e ~0; e para k diferente o produto muda (controle). Devolve
    (variancia entre posicoes para k, produto em k, produto em k+2)."""
    from synthai.posicional import variancia_translacao, produto
    return variancia_translacao(d=d, k=k), produto(0, k, d), produto(0, k + 2, d)


def _rodada71():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada71", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada71.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2566_rodada71(pos=13):
    """Rodada 71 (P2566; Parte 104): a codificacao posicional com seno/cosseno PROPRIOS, IGUAL em Java bit a bit (a sonda_seno_104
    mostrou que o naive tambem e IGUAL nesta maquina: sin nao e fronteira aqui). Devolve o vetor PE(pos) proprio (d=8)."""
    return _rodada71().pe(pos, True)


def p2591_frequencia_do_blefe(n=40000, semente=105):
    """A frequencia de blefe no equilibrio (P2591; Parte 105): alpha = B/(P+2B) = 1/3 para aposta do tamanho do pote; a
    melhor-resposta simulada bate ~1/3. Devolve (alpha analitico, alpha simulado)."""
    from synthai.blefe import alpha_blefe, simular_equilibrio
    return alpha_blefe(), simular_equilibrio(n, semente)[0]


def p2592_frequencia_de_pagar(n=40000, semente=105):
    """A frequencia de pagar (defesa minima) no equilibrio (P2592; Parte 105): c = P/(P+B) = 1/2 para aposta do tamanho do
    pote. Devolve (c analitico, c simulado)."""
    from synthai.blefe import freq_pagar, simular_equilibrio
    return freq_pagar(), simular_equilibrio(n, semente)[1]


def p2593_indiferenca(P=2.0, B=2.0):
    """O equilibrio e um ponto de indiferenca (P2593; Parte 105): no alpha* o pagador e indiferente (EV(pagar)=0) e no c* o
    apostador e indiferente (EV(blefar)=0); e a melhor-resposta do ar e plana (ninguem melhora desviando). Devolve
    (|EV(pagar)|, |EV(blefar)|, amplitude da melhor-resposta)."""
    from synthai.blefe import indiferenca, melhor_resposta_plana
    ip, ib = indiferenca(P, B)
    return ip, ib, melhor_resposta_plana(P, B)


def p2594_fronteira_das_trigonometricas(n=2000):
    """A 6a face da fronteira EXISTE, agora MEDIDA na faixa larga (P2594; Parte 105; corrige a Parte 104): a `math.sin` da
    libm difere da referencia de 40 digitos em `contar` de n argumentos x=k/1000 - a faixa larga, onde a reducao mod 2pi
    importa. A Parte 104 viu 0 porque usou argumentos pequenos e benignos (PE); aqui ha divergencia. A sonda cross-language
    `sonda_transc_105` mediu, em 10000 args, sin=21, cos=18, tan=35, atan2=590 divergencias entre Python e Java. Devolve o
    `contar` local de sin (> 0 confirma que sin NAO e corretamente arredondada na faixa larga)."""
    from synthai.posicional import contar_fora_wide
    return contar_fora_wide("sin", n)


def _rodada72():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada72", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada72.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2595_rodada72():
    """Rodada 72 (P2595; Parte 105): a decisao de equilibrio do blefe (alpha, c, b, EVs), IGUAL em Java bit a bit - so +,-,*,/
    e comparacoes, nenhuma transcendental (portavel por construcao). Devolve (alpha, c, b, ev_pagar, ev_blefar)."""
    return _rodada72().equilibrio()


def _rodada73():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada73", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada73.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2621_rodada73(x=3.14159):
    """Rodada 73 (P2621; Parte 106): o seno/cosseno PROPRIOS na faixa [0,001;10] onde a libm divergiu (Parte 105), IGUAL em
    Java bit a bit nos 10000 args (a serie propria e portavel onde a libm nao e). Devolve (sin_(x), cos_(x)) de amostra."""
    r = _rodada73()
    from exatas import cos_, sin_
    return sin_(x), cos_(x)


def p2622_exatidao_sin_proprio(n=2000):
    """A exatidao do sin_ proprio na faixa larga (P2622; Parte 106): o maior |sin_ - referencia de 40 digitos| em x=k/1000,
    k=1..n (faixa [0,001; n/1000]) - a serie de Taylor + reducao em duas partes e exata (< 1e-12). Devolve o maior erro."""
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo"))
    from exatas import sin_
    from synthai.posicional import _ref_generica
    return max(abs(sin_(k / 1000.0) - _ref_generica("sin", k / 1000.0)) for k in range(1, n + 1))


def p2623_reducao_duas_partes():
    """Quando a reducao em duas partes importa (P2623; Parte 106): o sin_ de UMA parte (so PI2_HI) vs o de DUAS concordam em
    x=1000 (< 1e-12) mas divergem em x=1e9 (> 1e-9), porque o erro de uma parte ~ (x/2pi)*2,45e-16. Devolve (dif em 1e3, dif em 1e9)."""
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo"))
    from exatas import sin_
    from synthai.posicional import sin_uma_parte
    return abs(sin_uma_parte(1e3) - sin_(1e3)), abs(sin_uma_parte(1e9) - sin_(1e9))


def p2624_voi_duas_ruas(n=20000, semente=106):
    """O valor da informacao oculta em duas ruas (P2624; Parte 106): 1 - (7/13)^2 = 120/169 = 0,7101 dos jogos mudam ao menos
    uma decisao. Devolve (fracao empirica, forma fechada)."""
    from synthai.jogo_cartas import voi_duas_ruas
    return voi_duas_ruas(n, semente)


def p2625_subaditividade_voi():
    """A sub-aditividade do VOI (P2625; Parte 106): duas ruas valem menos que o dobro de uma (2*6/13=0,923), porque alguns
    jogos mudam nas duas. Devolve (dobro de uma rua, VOI de duas ruas fechado, diferenca)."""
    dobro = 2 * 6.0 / 13.0
    duas = 1 - (7.0 / 13.0) ** 2
    return dobro, duas, dobro - duas


def _rodada74():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada74", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada74.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2651_rodada74():
    """Rodada 74 (P2651; Parte 107): a inducao reversa (iteracao de valor, horizonte 2), IGUAL em Java bit a bit - so +, max e
    comparacoes; a recursao entre as ruas NAO cria fronteira (como o MPC da Parte 93). Devolve (V1(A), V2(A))."""
    V = _rodada74().iteracao(2)
    return V[1]["A"], V[2]["A"]


def p2652_valor_otimo_duas_decisoes():
    """O valor otimo de duas decisoes a partir de A (P2652; Parte 107): a inducao reversa toma a acao 1 primeiro (recompensa 0
    agora) para chegar a B (que vale 3) -> V2(A) = 3. Devolve V2(A)."""
    from synthai.duas_ruas import MDP_TESTE, valor_otimo
    return valor_otimo(MDP_TESTE)


def p2653_reversa_vs_miope():
    """Inducao reversa vs guloso/miope (P2653; Parte 107): no MDP do teste a reversa (3) bate o miope (2), razao 1,5; num MDP
    separavel por estagio (T(s,a)=s) empatam, razao 1,0. Devolve (razao no teste, razao no separavel)."""
    from synthai.duas_ruas import MDP_TESTE, mdp_separavel, valor_miope, valor_otimo
    sep = mdp_separavel()
    return valor_otimo(MDP_TESTE) / valor_miope(MDP_TESTE), valor_otimo(sep) / valor_miope(sep)


def p2654_valor_da_segunda_decisao():
    """Quanto a segunda decisao acrescenta (P2654; Parte 107): V2(A) - V1(A) = 3 - 1 = 2 (o payoff adiado que a primeira
    decisao desbloqueia). Devolve (V1(A), V2(A), diferenca)."""
    from synthai.duas_ruas import MDP_TESTE, iteracao_valor
    V = iteracao_valor(MDP_TESTE, 2)
    return V[1]["A"], V[2]["A"], V[2]["A"] - V[1]["A"]


def p2655_voi_estado_oculto():
    """O valor de saber o estado oculto (P2655; Parte 107; VOI das Partes 83/84): com dois MDPs espelhos (preferem primeiras
    acoes opostas) o VOI > 0; com dois MDPs identicos (controle) o VOI = 0. Devolve (VOI espelho, VOI identico)."""
    from synthai.duas_ruas import voi_espelho, voi_identico
    return voi_espelho(), voi_identico()


def _rodada75():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada75", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada75.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2681_rodada75():
    """Rodada 75 (P2681; Parte 108): o minimax de um jogo de soma zero (forma fechada + jogo ficticio), IGUAL em Java bit a bit
    - so +,-,*,/,argmax e comparacoes; resolver o jogo NAO cria fronteira. Devolve (valor, p, q)."""
    v, p, q = _rodada75().valor_fechado()
    return v, p, q


def p2682_von_neumann():
    """O teorema minimax de von Neumann (P2682; Parte 108): no jogo de teste, maxmin (otica da linha) = minmax (otica da coluna).
    Devolve (maxmin, minmax, |diferenca|) - a diferenca ~0 confirma a dualidade."""
    from synthai.minimax import JOGO_TESTE, estrategia_coluna_2x2, estrategia_linha_2x2, minmax_por_coluna, valor_por_estrategias
    A = JOGO_TESTE
    mm = valor_por_estrategias(A, estrategia_linha_2x2(A))
    nm = minmax_por_coluna(A, estrategia_coluna_2x2(A))
    return mm, nm, abs(mm - nm)


def p2683_valor_e_estrategia():
    """O valor e a estrategia otima do jogo A=[[1,-1],[-2,3]] (P2683; Parte 108): v = (ad-bc)/(a+d-b-c) = 1/7; p = (d-c)/den = 5/7.
    Devolve (valor, p)."""
    from synthai.minimax import JOGO_TESTE, estrategia_linha_2x2, valor_2x2
    return valor_2x2(JOGO_TESTE), estrategia_linha_2x2(JOGO_TESTE)


def p2684_jogo_ficticio(iteracoes=2000):
    """O jogo ficticio converge para o valor (P2684; Parte 108; Robinson 1951): a estimativa apos `iteracoes` fica perto de 1/7.
    Devolve (estimativa, |estimativa - 1/7|)."""
    from synthai.minimax import JOGO_TESTE, jogo_ficticio
    vf = jogo_ficticio(JOGO_TESTE, iteracoes)
    return vf, abs(vf - 1.0 / 7.0)


def p2685_ponto_de_sela():
    """Um jogo com ponto de sela colapsa para a estrategia pura (P2685; Parte 108; controle): A=[[3,1],[2,0]] tem sela em (0,1)=1,
    valor 1 e estrategia pura (p=1). Devolve (valor, p)."""
    from synthai.minimax import JOGO_SELA, estrategia_linha_2x2, valor_2x2
    return valor_2x2(JOGO_SELA), estrategia_linha_2x2(JOGO_SELA)


def _nexus_colado():
    import os
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "externos", "nexus_raphael", "nexus_raphael_v0_1_0_colado.py"), encoding="utf-8") as f:
        return f.read()


def p2711_blobs_pickle_do_r37():
    """Os blobs pickle do simulador recebido 'ASI METACOGNITIVO R37' (P2711; Parte 109), inspecionados por pickletools.genops SEM desserializar:
    extrai pela AST as constantes *_B64 (e *_CHUNKS), decodifica base64+zlib, confere o SHA-256 embutido e lista as referencias GLOBAL/STACK_GLOBAL.
    R18_MEGA_B64 nao e pickle (struct de sorteios) e fica de fora. Devolve (n_blobs, n_sha_ok, globais distintos, perigosos)."""
    import ast
    import base64
    import hashlib
    import os
    import zlib
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "externos", "nexus_raphael", "asi_metacognitivo_r37.py"), encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    blobs, shas, chunks = {}, {}, {}
    for n in arvore.body:
        if not (isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)):
            continue
        nome = n.targets[0].id
        textos = [c.value for c in ast.walk(n.value) if isinstance(c, ast.Constant) and isinstance(c.value, str)]
        if nome.endswith("_CHUNKS"):
            chunks[nome] = "".join(textos)
        elif nome.endswith("_B64") and nome != "R18_MEGA_B64":
            refs = [c.id for c in ast.walk(n.value) if isinstance(c, ast.Name) and c.id.endswith("_CHUNKS")]
            blobs[nome] = chunks[refs[0]] if refs else "".join(t for t in textos if len(t) > 64)
        elif nome.endswith("_SHA256") and isinstance(n.value, ast.Constant):
            shas[nome] = n.value.value
    sha_ok, globais, perigosos = 0, set(), []
    for nome, b in sorted(blobs.items()):
        cru = zlib.decompress(base64.b64decode(b))
        sha_ok += int(shas.get(nome.replace("_B64", "_SHA256")) == hashlib.sha256(cru).hexdigest())
        for g in _globais_do_pickle(cru):
            globais.add(g)
            if _global_perigoso(g):
                perigosos.append((nome,) + g)
    return len(blobs), sha_ok, sorted(globais), perigosos


_PICKLE_MODULOS_PERIGOSOS = {"os", "posix", "nt", "subprocess", "sys", "socket", "shutil", "importlib", "pty", "ctypes"}
_PICKLE_BUILTINS_PERIGOSOS = {"eval", "exec", "compile", "getattr", "__import__", "open", "setattr", "globals", "vars"}


def _global_perigoso(g):
    modulo, nome = g
    return modulo.split(".")[0] in _PICKLE_MODULOS_PERIGOSOS or (modulo == "builtins" and nome in _PICKLE_BUILTINS_PERIGOSOS)


def _globais_do_pickle(cru):
    """As referencias (modulo, nome) de um pickle, lidas dos opcodes (pickletools.genops nao executa nada). Segue as strings empilhadas e o memo para
    resolver o STACK_GLOBAL do protocolo 4."""
    import pickletools
    memo, strs, out = {}, [], []
    for op, arg, _ in pickletools.genops(cru):
        if op.name in ("SHORT_BINUNICODE", "BINUNICODE", "UNICODE", "BINUNICODE8", "SHORT_BINSTRING", "BINSTRING"):
            strs.append(arg)
        elif op.name == "MEMOIZE":
            memo[len(memo)] = strs[-1] if strs else None
        elif op.name in ("BINPUT", "LONG_BINPUT", "PUT"):
            memo[arg] = strs[-1] if strs else None
        elif op.name in ("BINGET", "LONG_BINGET", "GET") and isinstance(memo.get(arg), str):
            strs.append(memo[arg])
        elif op.name == "GLOBAL":
            out.append(tuple(arg.split(" ", 1)))
        elif op.name == "STACK_GLOBAL":
            out.append((strs[-2], strs[-1]))
    return out


def p2711b_controle_do_auditor_de_pickle():
    """O controle dos dois lados (regra da Parte 75) do auditor de pickle da P2711: um pickle PLANTADO com os.system (montado por pickle.dumps de um
    objeto cujo __reduce__ devolve os.system; dumps NAO executa) tem de ser acusado, e um pickle limpo (dict de listas) tem de passar.
    Devolve (perigosos no plantado, perigosos no limpo)."""
    import os
    import pickle

    class _Plantado:
        def __reduce__(self):
            return (os.system, ("true",))
    plantado = pickle.dumps(_Plantado(), protocol=4)
    limpo = pickle.dumps({"a": [1, 2.5, "x"], "b": (True, None)}, protocol=4)
    return sum(map(_global_perigoso, _globais_do_pickle(plantado))), sum(map(_global_perigoso, _globais_do_pickle(limpo)))


def p2712_nexus_se_acusa():
    """A security_audit do NEXUS-RAPHAEL recebido aplicada ao PROPRIO texto (P2712; Parte 109; o texto contra o proprio codigo, Parte 88): por regex,
    ela acha 'exec(' e 'eval(' (dentro da checagem dos Auditors) e 'BACKDOOR' (dentro do proprio padrao), e o assert_harness original devolve 2 erros: o
    NEXUS rodado sairia com codigo 1. A auditoria por AST (chamadas e imports reais) acha so a rede (urlopen, urllib) no colado e nada no reescrito.
    Devolve (achados por texto, erros do harness original, AST no colado, AST no reescrito)."""
    import inspect
    from synthai import nexus
    src = _nexus_colado()
    erros = nexus.assert_harness_original(nexus.run_all(), src)
    return nexus.security_audit_texto(src), erros, nexus.security_audit_ast(src), nexus.security_audit_ast(inspect.getsource(nexus))


def p2713_kuhn_exato():
    """O valor EXATO do Kuhn simplificado do NEXUS para o P0 (P2713; Parte 109), por enumeracao das 6 distribuicoes: -1/12. E o valor com a melhor
    probabilidade de apostar com Q (o valor cresce linearmente nela: apostar sempre com Q da 0). Devolve (valor exato, simulado em 200, valor com pa=1)."""
    from fractions import Fraction
    from synthai import nexus
    return nexus.kuhn_exato(), nexus.kuhn_poker_value(7)["mean_payout_p0"], nexus.kuhn_exato(Fraction(1))


def p2714_desvio_da_curva_preditiva():
    """O 'Desvio da Curva Preditiva' do jogo Raphael (P2714; Parte 109) na agenda ORIGINAL: os dois desviando (o codigo recebido) e so o P0 desviando
    (a hipotese). Na agenda original o P0 nunca vence (a agenda de palavras decide). Devolve (dif ambos, dif so P0, vitorias do P0 guloso)."""
    from synthai import nexus
    cfg, W = nexus.Config(), list(nexus.OFFLINE_LEXICON)
    a = nexus.raphael_experiment(cfg, W)
    b = nexus.raphael_experiment(cfg, W, quem_desvia=0)
    return a["diferenca"], b["diferenca"], a["p0_wins_greedy"]


def p2715_grafo_e_beta():
    """O grafo sincrono/assincrono e o estimador Beta do NEXUS (P2715; Parte 109): operacoes = 910*2 (construcao) + 1820 (passada) + 100 (incrementos
    assincronos, que tambem contam); soma travada = 4*25; Brier do Beta (p=0,72, 200 ensaios) contra 0,25 da referencia. Devolve (ops, soma, brier_beta,
    brier_ref)."""
    from synthai import nexus
    cfg = nexus.Config()
    g = nexus.ComputeGraph(cfg.demo_graph_nodes, cfg.graph_layers, cfg.seed, cfg.max_ops)
    g.sync_pass(1)
    soma = g.async_increment()
    p = nexus.probability_experiment(cfg)
    return g.ops, soma, p["brier_adaptive"], p["brier_reference"]


def _rodada76():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada76", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada76.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2716_rodada76():
    """Rodada 76 (P2716; Parte 109): o valor exato do Kuhn simplificado por enumeracao, numa grade da probabilidade de apostar com Q, IGUAL em Java bit a
    bit - so +,-,*,/ e comparacoes. Devolve (valor com pa=0,5, valor com pa=1)."""
    r = _rodada76()
    return r.valor_kuhn(0.5), r.valor_kuhn(1.0)


def p2717_raphael_agenda_justa():
    """O jogo Raphael com agenda JUSTA (P2717; Parte 109; teste novo nascido da surpresa da P2714): no lance t, a palavra words[t // 2], a mesma para os
    dois em cada rodada. Devolve (vitorias do P0 guloso, dif so P0 desviando, dif os dois desviando)."""
    from synthai import nexus
    cfg, W = nexus.Config(), list(nexus.OFFLINE_LEXICON)
    a = nexus.raphael_experiment(cfg, W, quem_desvia=0, agenda="justa")
    b = nexus.raphael_experiment(cfg, W, agenda="justa")
    return a["p0_wins_greedy"], a["diferenca"], b["diferenca"]


def p2718_artefato_do_sorteio():
    """O 'numero quente' do sorteio IID do NEXUS (P2718; Parte 109): acerta 0,237 contra os 6/60 declarados porque o alvo e o MINIMO do sorteio ordenado
    e o desempate do most_common favorece numeros pequenos; contra a chance EXATA de cada H conter o minimo (soma de C(60-h,5)/C(60,6)), z ~ 0.
    Devolve (taxa observada, chance exata media, z)."""
    from synthai import nexus
    d = nexus.iid_draw_limitation(7)
    return d["hot_number_hit_rate"], d["chance_exata_media"], d["z"]


def p2719_retrospecto_cem_v2():
    """O retrospecto de cem partes com a faixa que a P2446 PROMETE (P2719; Parte 109): a P2446 diz "calibracao das Partes 80-100" mas chama a p1961
    com o padrao, que cresce a cada parte; a partir da Parte 106 o valor passou de 0,88 e o teste da Parte 100 ficou vermelho sem ser visto (achado
    pela suite inteira da Parte 109). A P2446 fica intacta; esta fixa as Partes 80-100. Devolve (nº de funcoes pNN, nº de rodadas, calibracao 80-100)."""
    k, rodadas, _ = p2446_retrospecto_cem()
    _, _, frac, _ = p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 101))))
    return k, rodadas, frac


def p2741_duvida_do_gradiente():
    """Duvidar do gradiente (P2741; Parte 110): o gradiente analitico de uma MLP 3->4->1 tanh contra a diferenca finita. A inclinacao de log(erro)
    contra log(h) le a ORDEM do metodo (o inverso): central ~2, adiantada ~1 (o subverso); o piso e o melhor erro relativo na grade; e o controle
    plantado (sinal trocado numa componente) tem erro relativo 2. Devolve (inclinacao central, inclinacao adiantada, melhor erro, h do melhor,
    erro do plantado)."""
    from synthai import duvida
    c = duvida.verificar_gradiente()
    f = duvida.verificar_gradiente(central=False)
    h_melhor, melhor = min(c, key=lambda t: t[1])
    plantado = duvida.verificar_gradiente(plantar=5, passos=[1e-5])[0][1]
    return duvida.inclinacao(c), duvida.inclinacao(f), melhor, h_melhor, plantado


def p2742_duvida_da_inferencia():
    """Duvidar da inferencia (P2742; Parte 110): a cobertura do intervalo bayesiano de 90% (Beta-Bernoulli, p ~ U(0,1)) bem especificado (~0,90)
    e com aglomerados de 4 observacoes identicas tratadas como independentes (o subverso: P(|Z| < 1,645/2) ~ 0,589); o inverso recupera o
    aglomerado c da cobertura. Devolve (cobertura independente, cobertura aglomerada, c recuperado)."""
    from synthai import duvida
    c1 = duvida.cobertura_bayes()
    c4 = duvida.cobertura_bayes(n=100, aglomerado=4)
    return c1, c4, duvida.aglomerado_recuperado(c4)


def p2743_duvida_da_rnn():
    """Duvidar da RNN (P2743; Parte 110): BPTT na RNN linear contra w^T (w = 0,9, T = 50) e o inverso (w de volta); e o subverso: a RNN tanh com
    w = 1,1 > 1, que a conta ingenua faria explodir (1,1^50 = 117), SOME pela saturacao (derivada local ~0,82 no ponto fixo). Devolve (erro
    relativo linear, w recuperado, gradiente tanh, h final)."""
    from synthai import duvida
    g = duvida.bptt_linear(0.9, 50)
    gt, hT = duvida.bptt_tanh(1.1, 50)
    return abs(g - 0.9 ** 50) / 0.9 ** 50, duvida.w_recuperado(g, 50), gt, hT


def p2744_duvida_do_ml():
    """Duvidar do ML (P2744; Parte 110): o erro de generalizacao de minimos quadrados (n = 50, p = 10, x ~ N(0, I)) contra 1 + p/(n - p - 1) =
    1,2564; o inverso recupera p do excesso; o subverso poe uma variavel omitida (coeficiente 1), que dobra o ruido: 2,513. Devolve (erro, p
    recuperado, erro com omitida)."""
    from synthai import duvida
    e = duvida.erro_generalizacao()
    return e, duvida.p_recuperado(e), duvida.erro_generalizacao(omitida=1.0)


def p2745_duvida_do_continuo():
    """Duvidar do aprendizado continuo (P2745; Parte 110): duas tarefas de posto 1 em R2; o esquecimento do GD e cos^2(theta) (0,5 em 45 graus; o
    inverso devolve theta); o OGD nao move w1 (esquecimento = so o residuo da propria tarefa A, 1 ulp ao quadrado) e paga em norma (1/sen theta);
    o subverso: em theta = 0 o OGD nao aprende B. Devolve (esquecimento GD 45, theta recuperado, esquecimento OGD 45, norma OGD 45, perda B OGD 0)."""
    from synthai import duvida
    gd = duvida.continuo(45)
    og = duvida.continuo(45, ogd=True)
    og0 = duvida.continuo(0, ogd=True)
    return gd[0], duvida.theta_recuperado(gd[0]), og[0], og[2], og0[1]


def p2746_duvida_do_reforco():
    """Duvidar do reforco (P2746; Parte 110): o vies de maximizacao do alvo do Q-learning, E[max] de k estimativas sem valor; k = 2 e m = 10:
    1/sqrt(pi m) = 0,1784; o estimador duplo (Double Q) ~0; o inverso recupera m; o subverso k = 10: 1,5388/sqrt(10) = 0,4866. Devolve (vies k=2,
    vies duplo, m recuperado, vies k=10)."""
    from synthai import duvida
    b = duvida.vies_do_max()
    return b, duvida.vies_do_max(duplo=True), duvida.m_recuperado(b), duvida.vies_do_max(k=10)


def _rodada77():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada77", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada77.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2747_rodada77():
    """Rodada 77 (P2747; Parte 110): o aprendizado continuo em R2 (GD e OGD, u por sqrt e nao por sin/cos), IGUAL em Java bit a bit. Devolve o
    esquecimento do GD em 60 graus (exatamente 0,25 = cos^2 60) e a norma do OGD em 45 graus (sqrt 2)."""
    r = _rodada77()
    e60 = r.continuo(0.5, math.sqrt(0.75), False)[0]
    n45 = r.continuo(math.sqrt(0.5), math.sqrt(0.5), True)[2]
    return e60, n45


def _p111_dicionarios():
    from synthai import palavras_rl
    return palavras_rl, palavras_rl.Dicionario(palavras_rl.EMBEDDED_WORDS), palavras_rl.Dicionario(palavras_rl.lemas_wordnet())


def p2771_guloso_x_aleatorio():
    """O agente de Q-learning da v2 do word_rl_lab contra o aleatorio (P2771; Parte 111), dicionario embutido, semente 42 (a padrao da v2), e a
    replicacao nas sementes 10-14 (quantas com ICs de Wilson disjuntos). Devolve (taxa gulosa, taxa aleatoria, n de sementes disjuntas em 10-14)."""
    P, emb, _ = _p111_dicionarios()
    cfg = P.Config(seed=42)
    ag, _, _ = P.train(cfg, emb)
    ev = P.evaluate(cfg, emb, ag)
    disj = 0
    for s in range(10, 15):
        c = P.Config(seed=s)
        a, _, _ = P.train(c, emb)
        e = P.evaluate(c, emb, a)
        disj += int(e["guloso"][1][0] > e["aleatorio"][1][1])
    return ev["guloso"][0], ev["aleatorio"][0], disj


def p2772_acao_direcao():
    """O desenho da v1 (acao = DIRECAO, estado = 3 ultimas letras) como braco de comparacao (P2772; Parte 111), semente 42: com letras uniformes (como
    na v1) e com letras por frequencia (separa a causa). Devolve (taxa gulosa uniforme, guloso - aleatorio por frequencia)."""
    P, emb, _ = _p111_dicionarios()
    cfg = P.Config(seed=42)
    u = P.treinar_e_avaliar_v1(cfg, emb)
    f = P.treinar_e_avaliar_v1(cfg, emb, uniforme=False)
    return u["guloso"][0], f["guloso"][0] - f["aleatorio"][0]


def p2773_confianca_e_ablacoes():
    """O estimador de confianca da v2 (P2773; Parte 111), semente 42: a razao Brier estimador/linha de base com o embutido e com o WordNet, e as duas
    ablacoes pre-registradas (sem Q(PARAR); so as letras). Devolve (razao embutido, razao WordNet, sem Q, so letras)."""
    P, emb, wn = _p111_dicionarios()
    cfg = P.Config(seed=42)
    _, _, st = P.train(cfg, emb)
    _, _, sw = P.train(cfg, wn)
    sem_q = P.treinar_com_estimador(cfg, emb, P.EstimadorSemQ)[0]
    so_letras = P.treinar_com_estimador(cfg, emb, P.EstimadorSoLetras)[0]
    return st["brier_estimador"] / st["brier_base"], sw["brier_estimador"] / sw["brier_base"], sem_q, so_letras


def p2774_data_lake():
    """O DATA LAKE (lemas a-z do WordNet 3.0, dados/) no lugar da lista embutida (P2774; Parte 111), semente 42. Devolve (n de lemas, taxa gulosa
    WordNet, taxa aleatoria WordNet, razao aleatorio WordNet / aleatorio embutido)."""
    P, emb, wn = _p111_dicionarios()
    cfg = P.Config(seed=42)
    a1, _, _ = P.train(cfg, emb)
    e1 = P.evaluate(cfg, emb, a1)
    a2, _, _ = P.train(cfg, wn)
    e2 = P.evaluate(cfg, wn, a2)
    return len(wn.palavras), e2["guloso"][0], e2["aleatorio"][0], e2["aleatorio"][0] / e1["aleatorio"][0]


def p2775_auditor_por_capacidade():
    """A auditoria AST v2, por CAPACIDADE (P2775; Parte 111): a da Parte 109 (por nome) nao viu requests.get/nltk.download na v1 e acusou o
    urllib.parse.quote da v2. Controles dos dois lados: um caso plantado (4 formas de rede, 3 imports) e um limpo (os falsos positivos da 109).
    Devolve (antiga na v1, antiga na v2, nova na v1, nova na v2, nova no plantado, nova no limpo, nova no proprio fonte)."""
    import inspect
    import os
    from synthai import nexus, palavras_rl
    raiz = os.path.dirname(os.path.abspath(__file__))
    srcs = []
    for v in ("v1", "v2"):
        with open(os.path.join(raiz, "externos", "word_rl_lab", f"word_rl_lab_{v}_recebido.py"), encoding="utf-8") as f:
            srcs.append(f.read())
    plantado = ("import requests\nimport socket\nimport urllib.request\nimport nltk\nrequests.get(u)\nnltk.download('w')\n"
                "urllib.request.urlopen(u)\nsocket.create_connection(h)\n")
    limpo = "from urllib.parse import quote\nimport re, asyncio\nre.compile('a')\nasyncio.run(f())\ns = 'requests.get('\n"
    a = palavras_rl.security_audit_ast_v2
    return (nexus.security_audit_ast(srcs[0]), nexus.security_audit_ast(srcs[1]), a(srcs[0]), a(srcs[1]), a(plantado), a(limpo),
            a(inspect.getsource(palavras_rl)))


def _rodada78():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada78", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada78.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2776_rodada78():
    """Rodada 78 (P2776; Parte 111): o passo de Q-learning tabular (5x3, 2.000 transicoes de um LCG inteiro), IGUAL em Java bit a bit. Devolve a tabela."""
    return _rodada78().treinar()


def p2777_palavras_distintas_do_guloso():
    """O mecanismo de (a), posto a prova (P2777; Parte 111): o guloso da semente 42 forma poucas palavras distintas (o seu repertorio). Devolve o Counter."""
    P, emb, _ = _p111_dicionarios()
    cfg = P.Config(seed=42)
    ag, _, _ = P.train(cfg, emb)
    return P.palavras_distintas_gulosas(cfg, emb, ag)


def p2806_minhas_previsoes_v3(partes=range(53, 68)):
    """As minhas previsões do mundo, versão 3 (P2806; Parte 112; a P1481 fica intacta). O defeito da v2, achado na Parte 112: ela casava QUALQUER "(x)" do
    texto como rótulo de letra, e "log(h)", "f(x)" ou "o mecanismo de (f)" roubavam ou bloqueavam a faixa (a MENÇÃO de uma letra lida como USO de um rótulo;
    a Parte 110 tinha diagnosticado, errado, "rótulo em negrito"). Aqui um rótulo só vale no INÍCIO de uma linha (depois de um marcador de lista e de
    negrito opcionais), e a faixa é o primeiro **[a; b]** do mesmo item (até o próximo rótulo, título ou linha em branco). O resto é igual à v2 (o
    diálogo, o tipo, a porcentagem). Devolve [(parte, letra, a, b, acerto, tipo)]."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    dialogo = open(os.path.join(raiz, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    rotulo = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?\(([a-z])\)")
    faixa = re.compile(r"\*\*\[([^\];]+?);\s*([^\]]+?)\]\*\*")
    velha = re.compile(r"\(([a-z])\)((?:(?!\([a-z]\)).){0,400}?)\*\*\[([^\];]+?);\s*([^\]]+?)\]\*\*")
    saida = []
    for parte in partes:
        arq = glob.glob(os.path.join(raiz, f"ASI_AGI_parte{parte}_*.md"))
        if not arq:
            continue
        texto = open(arq[0], encoding="utf-8").read()
        m = re.search(r"Do mundo: ((?:\([a-z]\) [✅❌] ?)+)", texto)
        if not m:
            continue
        vered = re.findall(r"\(([a-z])\) ([✅❌])", m.group(1))
        corpo = texto.split("## As respostas")[0]
        itens, atual = {}, None
        for linha in corpo.split("\n"):
            r = rotulo.match(linha)
            if r:
                atual = r.group(1)
                itens.setdefault(atual, [])
                itens[atual].append(linha[r.end():])
            elif atual is not None and linha.strip() and not linha.lstrip().startswith("#"):
                itens[atual].append(linha)
            else:
                atual = None
        faixas = {}
        for letra, ls in itens.items():
            achou = faixa.search(" ".join(ls))
            if achou and letra not in faixas:
                x, y = _numero_pt(achou.group(1)), _numero_pt(achou.group(2))
                if x is not None and y is not None and "%" in achou.group(1) + achou.group(2):
                    x, y = x / 100, y / 100
                if x is not None and y is not None:
                    faixas[letra] = (x, y)
        cab = re.search(rf"## Rodada {parte - 26} [^\n]*\n(.*?)(?=\n## |\Z)", dialogo, re.S)
        rodada = (cab.group(1) if cab else "").split("**Resultado")[0]
        for letra, _, a, b in velha.findall(rodada.replace("\n", " ")):   # o diálogo, como na v2, só preenche letras que o texto não tem
            x, y = _numero_pt(a), _numero_pt(b)
            if letra not in faixas and x is not None and y is not None:
                faixas[letra] = (x, y)
        for letra, v in vered:
            a, b = faixas.get(letra, (None, None))
            if a is None:
                tipo = None
            elif a <= 0 <= b:
                tipo = "zero"
            elif 0 <= a and b <= 1:
                tipo = "fracao"
            elif a == int(a) and b == int(b) and a >= 1:
                tipo = "contagem"
            else:
                tipo = "outra"
            saida.append((parte, letra, a, b, v == "✅", tipo))
    return saida


def p2807_v2_contra_v3(partes=range(53, 112)):
    """O que a v3 do leitor muda (P2807; Parte 112): para cada (parte, letra) pontuada, compara a faixa lida pela v2 (P1481) e pela v3 (P2806).
    Devolve (recuperadas: None na v2 e lida na v3, perdidas: lida na v2 e None na v3, trocadas: as duas leram faixas diferentes, total)."""
    v2 = {(x[0], x[1]): (x[2], x[3]) for x in p1481_minhas_previsoes_v2(partes)}
    v3 = {(x[0], x[1]): (x[2], x[3]) for x in p2806_minhas_previsoes_v3(partes)}
    rec = sorted(k for k in v3 if v2.get(k, (None, None))[0] is None and v3[k][0] is not None)
    per = sorted(k for k in v2 if v2[k][0] is not None and v3.get(k, (None, None))[0] is None)
    tro = sorted(k for k in v2 if v2[k][0] is not None and v3.get(k, (None, None))[0] is not None and v2[k] != v3[k])
    return rec, per, tro, len(v3)


def p2808_previsoes_sobre_previsoes_v3(parte=112):
    """O placar (m) da P1499 lido pela v3 do leitor (P2808; Parte 112; a P1499 fica intacta): (m1) nº de previsões do mundo, (m2) faixas que cruzam o
    zero, (m3) a mediana de w das que não cruzam, (m4) a fração de acertos, (m5) as que não cruzam com w > 0,6. Devolve (medidas, ws)."""
    prev = p2806_minhas_previsoes_v3(range(parte, parte + 1))
    nz = [x for x in prev if x[5] not in (None, "zero")]
    ws = sorted((x[3] - x[2]) / (abs(x[2]) + abs(x[3])) for x in nz)
    n = len(ws)
    med = (ws[n // 2] if n % 2 else (ws[n // 2 - 1] + ws[n // 2]) / 2) if n else None
    return ({"m1": len(prev), "m2": sum(1 for x in prev if x[5] == "zero"), "m3": med,
             "m4": sum(x[4] for x in prev) / len(prev) if prev else None, "m5": sum(1 for w in ws if w > 0.6)}, ws)


def p2809_auditoria_do_placar_m(partes=(74, 84, 87, 107, 109, 110, 111)):
    """A auditoria retroativa do placar (m) nas partes em que a v2 do leitor errou (P2809; Parte 112): para cada parte, (m2), (m3) e (m5) medidos
    pela v2 e pela v3, e a faixa registrada (lida do próprio texto); conta os vereditos (m) que MUDAM com a régua corrigida.
    Devolve ([(parte, m, faixa, valor v2, valor v3, dentro v2, dentro v3)], nº de vereditos que mudam)."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    linhas, mudam = [], 0
    for parte in partes:
        texto = open(glob.glob(os.path.join(raiz, f"ASI_AGI_parte{parte}_*.md"))[0], encoding="utf-8").read().split("## As respostas")[0]
        fx = {}
        for k, a, b in re.findall(r"\(m(\d)\)\*\*[^\[\n]*?\*\*\[([^;\]]+);\s*([^\]]+)\]\*\*", texto):
            if k not in fx and _numero_pt(a) is not None and _numero_pt(b) is not None:
                fx[k] = (_numero_pt(a), _numero_pt(b))
        m2, _ = p1499_previsoes_sobre_previsoes_v2(parte)
        m3, _ = p2808_previsoes_sobre_previsoes_v3(parte)
        for k in ("2", "3", "5"):
            if k not in fx:
                continue
            a, b = fx[k]
            x2, x3 = m2["m" + k], m3["m" + k]
            d2 = x2 is not None and a <= x2 <= b
            d3 = x3 is not None and a <= x3 <= b
            mudam += int(d2 != d3)
            linhas.append((parte, "m" + k, (a, b), x2, x3, d2, d3))
    return linhas, mudam


def p2801_kuhn_completo():
    """O valor do pôquer de Kuhn COMPLETO para o jogador 1 (P2801; Parte 112), pela forma normal 27x64 e o simplex próprio exato (Fraction): -1/18.
    Devolve (valor, pivôs, (pior linha, melhor coluna) da dualidade)."""
    from synthai import simplex
    A, _, _ = simplex.kuhn_forma_normal()
    v, p, q, k = simplex.resolver_jogo(A)
    return v, k, simplex.dualidade(A, p, q)


def _p112_equilibrio():
    from synthai import simplex
    A, L, C = simplex.kuhn_forma_normal()
    v, p, q, _ = simplex.resolver_jogo(A)
    return simplex, L, C, p, q


def p2802_jogador2_de_kuhn():
    """O equilíbrio do jogador 2 (único, Kuhn) lido do q do simplex (P2802; Parte 112): P(paga | dama, diante de aposta) e P(aposta | valete, diante
    de passe), o blefe. Devolve (paga|Q, blefe|J)."""
    S, L, C, p, q = _p112_equilibrio()
    return S.comportamento(C, q, 2, 0, "paga"), S.comportamento(C, q, 1, 1, "aposta")


def p2803_familia_do_jogador1():
    """A família de um parâmetro do jogador 1 (P2803; Parte 112): α = P(aposta | valete); a relação aposta(rei) = 3α; e passa-e-paga(dama) = α + 1/3.
    Devolve (α, |aposta(K) − 3α|, aposta(Q), |paga(Q) − (α + 1/3)|)."""
    from fractions import Fraction
    S, L, C, p, q = _p112_equilibrio()
    al = S.comportamento(L, p, 1, None, "aposta")
    return (al, abs(S.comportamento(L, p, 3, None, "aposta") - 3 * al), S.comportamento(L, p, 2, None, "aposta"),
            abs(S.comportamento(L, p, 2, None, "passa-paga") - (al + Fraction(1, 3))))


def p2804_float_exato_e_dualidade():
    """No jogo 4x5 da fixture (P2804; Parte 112): o valor exato, |float − exato| e a lacuna de dualidade no exato. Devolve (valor exato, erro do float,
    lacuna, pivôs)."""
    from synthai import simplex
    G = simplex.jogo_lcg()
    ve, pe, qe, ke = simplex.resolver_jogo(G)
    vf, _, _, _ = simplex.resolver_jogo(G, exato=False)
    lo, hi = simplex.dualidade(G, pe, qe)
    return ve, abs(vf - float(ve)), hi - lo, ke


def _rodada79():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada79", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada79.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2805_rodada79():
    """Rodada 79 (P2805; Parte 112): o simplex próprio em float no jogo 4x5, IGUAL em Java bit a bit. Devolve (valor, p, q, pivôs)."""
    r = _rodada79()
    return r.resolver(r.jogo())


def p2810_hipotese_do_repertorio():
    """A hipótese do REPERTÓRIO da Parte 111 (P2810; Parte 112; registrada como "P2808" no pré-registro, número que passou à P2808 do placar v3): o
    estimador de confiança treinado sobre as palavras de uma política ALEATÓRIA, semente 42, completo e só com as letras. Devolve (razão completo,
    razão só letras, tentativas, válidas)."""
    from synthai import palavras_rl as P
    emb = P.Dicionario(P.EMBEDDED_WORDS)
    cfg = P.Config(seed=42)
    rc, n, k = P.estimador_sob_politica_aleatoria(cfg, emb, P.ConfidenceEstimator)
    rl, _, _ = P.estimador_sob_politica_aleatoria(cfg, emb, P.EstimadorSoLetras)
    return rc, rl, n, k


_SOBRESCRITOS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")


def _numero_pt_v2(x):
    """O _numero_pt com potências escritas com expoente sobrescrito (Parte 113; a original fica intacta): "10⁻¹²", "5·10⁻⁴", "6,1·10⁻¹⁶",
    "2⁻⁵⁴". Sem expoente sobrescrito, delega à original."""
    import re
    y = x.strip().replace("*", "").replace(" ", "")
    m = re.fullmatch(r"(?:([−\-]?[0-9.,]+)[·×])?([0-9]+)([⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)", y)
    if not m:
        return _numero_pt(x)
    mant = _numero_pt(m.group(1)) if m.group(1) else 1.0
    if mant is None:
        return None
    return mant * float(int(m.group(2))) ** int(m.group(3).translate(_SOBRESCRITOS))


def p2833_minhas_previsoes_v4(partes=range(53, 68), numero=None):
    """As minhas previsões do mundo, versão 4 (P2833; Parte 113): a mesma leitura da v3 (P2806: rótulo só no início da linha, faixa no
    mesmo item), com o leitor de números trocável; o padrão é o _numero_pt_v2, que entende expoentes sobrescritos. A v3 fica intacta.
    Devolve [(parte, letra, a, b, acerto, tipo)]."""
    import glob
    import os
    import re
    numero = numero or _numero_pt_v2
    raiz = os.path.dirname(os.path.abspath(__file__))
    dialogo = open(os.path.join(raiz, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    rotulo = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?\(([a-z])\)")
    faixa = re.compile(r"\*\*\[([^\];]+?);\s*([^\]]+?)\]\*\*")
    velha = re.compile(r"\(([a-z])\)((?:(?!\([a-z]\)).){0,400}?)\*\*\[([^\];]+?);\s*([^\]]+?)\]\*\*")
    saida = []
    for parte in partes:
        arq = glob.glob(os.path.join(raiz, f"ASI_AGI_parte{parte}_*.md"))
        if not arq:
            continue
        texto = open(arq[0], encoding="utf-8").read()
        m = re.search(r"Do mundo: ((?:\([a-z]\) [✅❌] ?)+)", texto)
        if not m:
            continue
        vered = re.findall(r"\(([a-z])\) ([✅❌])", m.group(1))
        itens, atual = {}, None
        for linha in texto.split("## As respostas")[0].split("\n"):
            r = rotulo.match(linha)
            if r:
                atual = r.group(1)
                itens.setdefault(atual, []).append(linha[r.end():])
            elif atual is not None and linha.strip() and not linha.lstrip().startswith("#"):
                itens[atual].append(linha)
            else:
                atual = None
        faixas = {}
        for letra, ls in itens.items():
            achou = faixa.search(" ".join(ls))
            if achou:
                x, y = numero(achou.group(1)), numero(achou.group(2))
                if x is not None and y is not None and "%" in achou.group(1) + achou.group(2):
                    x, y = x / 100, y / 100
                if x is not None and y is not None:
                    faixas[letra] = (x, y)
        cab = re.search(rf"## Rodada {parte - 26} [^\n]*\n(.*?)(?=\n## |\Z)", dialogo, re.S)
        for letra, _, a, b in velha.findall((cab.group(1) if cab else "").split("**Resultado")[0].replace("\n", " ")):
            x, y = numero(a), numero(b)
            if letra not in faixas and x is not None and y is not None:
                faixas[letra] = (x, y)
        for letra, v in vered:
            a, b = faixas.get(letra, (None, None))
            if a is None:
                tipo = None
            elif a <= 0 <= b:
                tipo = "zero"
            elif 0 <= a and b <= 1:
                tipo = "fracao"
            elif a == int(a) and b == int(b) and a >= 1:
                tipo = "contagem"
            else:
                tipo = "outra"
            saida.append((parte, letra, a, b, v == "✅", tipo))
    return saida


def p2834_v3_contra_v4(partes=range(53, 113)):
    """O que a v4 muda sobre a v3 (P2834; Parte 113). Devolve (recuperadas, perdidas, trocadas, total)."""
    v3 = {(x[0], x[1]): (x[2], x[3]) for x in p2806_minhas_previsoes_v3(partes)}
    v4 = {(x[0], x[1]): (x[2], x[3]) for x in p2833_minhas_previsoes_v4(partes)}
    rec = sorted(k for k in v4 if v3.get(k, (None, None))[0] is None and v4[k][0] is not None)
    per = sorted(k for k in v3 if v3[k][0] is not None and v4.get(k, (None, None))[0] is None)
    tro = sorted(k for k in v3 if v3[k][0] is not None and v4.get(k, (None, None))[0] is not None and v3[k] != v4[k])
    return rec, per, tro, len(v4)


def p2831_cfr_convergencia(T=10000):
    """O CFR no pôquer de Kuhn (P2831; Parte 113): a estratégia MÉDIA depois de T iterações, a sua explorabilidade (o que cede a melhores
    respostas, exata por enumeração) e a distância do seu valor a −1/18. Devolve (explorabilidade, |valor + 1/18|, valor)."""
    from synthai import cfr
    m = cfr.CFR().iterar(T).media()
    v = cfr.valor(m)
    return cfr.explorabilidade(m), abs(v + 1.0 / 18.0), v


def p2832_cfr_equilibrio(T=10000):
    """Que equilíbrio o CFR acha (P2832; Parte 113): as marginais do jogador 2 (paga com a dama, blefa com o valete), o α do jogador 1 e as
    duas relações da família de Kuhn. Devolve (|paga(Q) − 1/3|, |blefe(J) − 1/3|, α, |aposta(K) − 3α|, |paga1(Q) − (α + 1/3)|)."""
    from synthai import cfr
    m = cfr.CFR().iterar(T).media()
    al = m[(1, "")][1]
    return (abs(m[(2, "b")][1] - 1.0 / 3.0), abs(m[(1, "p")][1] - 1.0 / 3.0), al, abs(m[(3, "")][1] - 3.0 * al),
            abs(m[(2, "pb")][1] - (al + 1.0 / 3.0)))


def p2835_transferencia_do_repertorio(sementes=range(42, 52)):
    """O teste FORTE da hipótese do repertório (P2835; Parte 113): o estimador só de letras treinado no repertório do agente, congelado e
    avaliado nas palavras de uma política aleatória; AUC das válidas NOVAS e (vistas − novas), médias sobre as sementes.
    Devolve (média AUC novas, média vistas − novas, nº de sementes com vistas)."""
    from synthai import palavras_rl as P
    emb = P.Dicionario(P.EMBEDDED_WORDS)
    nov, dif = [], []
    for s in sementes:
        av, an, nv, nn, _ = P.transferencia_do_estimador(P.Config(seed=s), emb)
        if nn:
            nov.append(an)
        if nv and nn:
            dif.append(av - an)
    return sum(nov) / len(nov), sum(dif) / len(dif), len(dif)


def _rodada80():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada80", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada80.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2836_rodada80():
    """Rodada 80 (P2836; Parte 113): o CFR em float (T = 1.000) IGUAL em Java bit a bit. Devolve as 12 probabilidades médias de apostar/pagar."""
    return _rodada80().treinar()


def p2837_previsoes_sobre_previsoes_v4(parte=113):
    """O placar (m) lido pelo leitor v4 (P2837; Parte 113). Devolve (medidas, ws)."""
    prev = p2833_minhas_previsoes_v4(range(parte, parte + 1))
    nz = [x for x in prev if x[5] not in (None, "zero")]
    ws = sorted((x[3] - x[2]) / (abs(x[2]) + abs(x[3])) for x in nz)
    n = len(ws)
    med = (ws[n // 2] if n % 2 else (ws[n // 2 - 1] + ws[n // 2]) / 2) if n else None
    return ({"m1": len(prev), "m2": sum(1 for x in prev if x[5] == "zero"), "m3": med,
             "m4": sum(x[4] for x in prev) / len(prev) if prev else None, "m5": sum(1 for w in ws if w > 0.6)}, ws)


def p2838_auditoria_do_placar_m_v4(partes=(70, 77, 110, 112)):
    """A auditoria retroativa do placar (m) nas partes em que a v4 do leitor muda alguma faixa (P2838; Parte 113; a regra da Parte 112): (m2),
    (m3), (m5) pela v3 e pela v4 contra a faixa registrada. Devolve (linhas, nº de vereditos que mudam)."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    linhas, mudam = [], 0
    for parte in partes:
        texto = open(glob.glob(os.path.join(raiz, f"ASI_AGI_parte{parte}_*.md"))[0], encoding="utf-8").read().split("## As respostas")[0]
        fx = {}
        for k, a, b in re.findall(r"\(m(\d)\)\*\*[^\[\n]*?\*\*\[([^;\]]+);\s*([^\]]+)\]\*\*", texto):
            if k not in fx and _numero_pt(a) is not None and _numero_pt(b) is not None:
                fx[k] = (_numero_pt(a), _numero_pt(b))
        m3, _ = p2808_previsoes_sobre_previsoes_v3(parte)
        m4, _ = p2837_previsoes_sobre_previsoes_v4(parte)
        for k in ("2", "3", "5"):
            if k not in fx:
                continue
            a, b = fx[k]
            x3, x4 = m3["m" + k], m4["m" + k]
            d3 = x3 is not None and a <= x3 <= b
            d4 = x4 is not None and a <= x4 <= b
            mudam += int(d3 != d4)
            linhas.append((parte, "m" + k, (a, b), x3, x4, d3, d4))
    return linhas, mudam


def p2861_logistica_como_rede():
    """ML como DL (P2861; Parte 114): a regressão logística com L2 (λ = 0,01) como rede de UMA camada treinada por retropropagação (lr = 1/L,
    2.000 passos, a partir de zero) contra o solucionador clássico (Newton). Devolve (max |w_rede − w_Newton|, max |∇| no Newton, κ = L/μ)."""
    from synthai import ml_dl as M
    X, y = M.dados_logistica()
    lam = 0.01
    mu, L = M.constantes_logistica(X, lam)
    wn = M.newton_logistica(X, y, lam)
    wr = M.rede_logistica(X, y, lam, 2000, 1.0 / L)
    return max(abs(a - b) for a, b in zip(wn, wr)), max(abs(g) for g in M.gradiente_logistica(wn, X, y, lam)), L / mu


def p2862_rede_linear_profunda():
    """DL como ML (P2862; Parte 114): a rede linear profunda W₂W₁ (h = 4, 3.000 passos) contra o OLS em forma fechada. Devolve max |β_rede − β_OLS|."""
    from synthai import ml_dl as M
    Xtr, ytr = M.dados_regressao(200, 114)
    Xl = [x + [1.0] for x in Xtr]
    return max(abs(a - b) for a, b in zip(M.ols(Xl, ytr), M.rede_linear_profunda(Xl, ytr, semente=114)))


def p2863_features_e_cabeca():
    """DL como ML (P2863; Parte 114): MSE de teste das features ALEATÓRIAS + ridge, da rede inteira por retropropagação (3.000 passos) e das
    features TREINADAS + ridge. Devolve (MSE aleatórias, MSE retropropagação, MSE treinadas + ridge)."""
    from synthai import ml_dl as M
    Xtr, ytr = M.dados_regressao(200, 114)
    Xte, yte = M.dados_regressao(1000, 114114)
    rf = M.features_aleatorias(Xtr, ytr, Xte, yte, semente=114)
    bp, W, b = M.mlp_retropropagacao(Xtr, ytr, Xte, yte, semente=114)
    return rf, bp, M.features_treinadas_mais_ridge(Xtr, ytr, Xte, yte, W, b)


def p2864_graus_de_liberdade():
    """ML na cabeça de uma rede (P2864; Parte 114): os graus de liberdade da ridge sobre 40 features tanh, tr(S) em forma fechada e a definição
    de Efron por simulação, com λ = 10⁻³ e λ = 1. Devolve (tr(S) λ=10⁻³, Efron λ=10⁻³, tr(S) λ=1, Efron λ=1)."""
    import random
    from synthai import ml_dl as M
    Xtr, _ = M.dados_regressao(200, 114)
    rng = random.Random(1144)
    W = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(40)]
    b = [rng.uniform(-2, 2) for _ in range(40)]
    H = M._oculta(Xtr, W, b)
    f = [math.sin(x[0]) + 0.5 * x[1] * x[1] for x in Xtr]
    return (M.df_ridge_fechado(H, 1e-3), M.df_ridge_efron(H, f, 1e-3), M.df_ridge_fechado(H, 1.0), M.df_ridge_efron(H, f, 1.0))


def _rodada81():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada81", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada81.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2865_rodada81():
    """Rodada 81 (P2865; Parte 114): a rede linear profunda por GD (500 passos), IGUAL em Java bit a bit. Devolve (β da rede, β do OLS) nos
    mesmos dados: em 500 passos a rede ainda NÃO chegou ao OLS."""
    from synthai import ml_dl as M
    r = _rodada81()
    X, y, _, _ = r.dados()
    return r.treinar(), M.ols(X, y)


def p2891_dez_camadas():
    """As dez camadas (P2891; Parte 115), h0 = 0,5: o gradiente de ponta a ponta ∂h₁₀/∂h₀ na cadeia linear (pesos 1,2), na linear contraposta
    (1,2; 1/1,2), na tanh contraposta (2; 1/2) e na tanh de peso igual (2). Devolve (erro relativo contra 1,2¹⁰, |g − 1| contraposta,
    g tanh contraposta, g tanh igual)."""
    from synthai import contraposto as C
    _, g1, _ = C.cadeia([1.2] * 10, 0.5, "linear")
    _, g2, _ = C.cadeia(C.pesos_contrapostos(1.2), 0.5, "linear")
    _, g3, _ = C.cadeia(C.pesos_contrapostos(2.0), 0.5)
    _, g4, _ = C.cadeia([2.0] * 10, 0.5)
    return abs(g1 - 6.1917364224) / 6.1917364224, abs(g2 - 1.0), g3, g4


def p2892_gradientes_sobrepostos():
    """Os dez gradientes sobrepostos (P2892; Parte 115): o resto |Δh − Σ g_k δw_k| na cadeia tanh contraposta, com ε = 10⁻³ e 10⁻⁴, e a
    inclinação log-log (2: o resto é de 2ª ordem). Devolve (resto 1e-3, resto 1e-4, inclinação, os 10 gradientes)."""
    from synthai import contraposto as C
    w = C.pesos_contrapostos(2.0)
    r1, r2 = C.superposicao(w, 0.5, 1e-3), C.superposicao(w, 0.5, 1e-4)
    _, _, gw = C.cadeia(w, 0.5)
    return r1, r2, (math.log(r1) - math.log(r2)) / (math.log(1e-3) - math.log(1e-4)), gw


def p2893_palavras_do_dicionario():
    """O dicionário contado (P2893; Parte 115): lemas por classe do WordNet 3.0 (sem marcadores), pares (lema, sinset) brutos e distintos, lemas
    distintos no total, e a OpenWordNet-PT. Devolve (por classe, brutos, distintos, total, (lemas pt, pares pt))."""
    from synthai import contraposto as C
    _, limpo, brutos = C.contar_wordnet()
    distintos, _ = C.pares_sinset_distintos()
    return ({k: len(v) for k, v in limpo.items()}, brutos, distintos, len(set().union(*limpo.values())), C.contar_ownpt())


def p2894_em_algarismos():
    """O alfabeto em algarismos (P2894; Parte 115): a base 26 bijetiva sobre as 77.340 palavras a-z. Devolve (colisões, ida-e-volta certa,
    algarismos decimais do maior número)."""
    from synthai import contraposto as C, palavras_rl as P
    W = sorted(P.lemas_wordnet())
    nums = {C.em_algarismos(w) for w in W}
    return len(W) - len(nums), all(C.de_algarismos(C.em_algarismos(w)) == w for w in W), len(str(max(nums)))


def p2895_em_algoritmos():
    """O alfabeto em algoritmos (P2895; Parte 115): cada letra uma operação mod 1.000.003 e a palavra o programa. Devolve ((distintos, pares que
    colidem) afins, (distintos, pares que colidem) translações, classes de anagrama)."""
    from synthai import contraposto as C, palavras_rl as P
    W = sorted(P.lemas_wordnet())
    return (C.colisoes(W, C.alfabeto_de_algoritmos(115)), C.colisoes(W, C.alfabeto_de_algoritmos(115, comutam=True)),
            len({"".join(sorted(w)) for w in W}))


def p2896_escala_e_meta_medida():
    """A escala dos vetores contra a meta-medida (P2896; Parte 115): a distorção da projeção gaussiana (k = 4, m = 2.000) e o oposto (k = 256,
    m = 20); e quantos pares nulos a fixture corrigida pulou. Devolve ((média, desvio) k=4, (média, desvio) k=256, pares nulos)."""
    from synthai import contraposto as C
    return C.media_desvio(C.distorcoes(4, 2000)), C.media_desvio(C.distorcoes(256, 20)), C.pares_nulos(2000)


def _rodada82():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada82", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada82.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2897_rodada82():
    """Rodada 82 (P2897; Parte 115): a cadeia tanh contraposta pelo exp próprio, IGUAL em Java. Devolve (h10, gradiente, os 10 gradientes)."""
    return _rodada82().cadeia()


def _blocos_do_nexus_v2():
    """Os dois blocos de código do texto recebido na Parte 116, cada um cortado na última linha em que ainda fecha como Python (o texto está truncado)."""
    import ast
    import os
    txt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "externos", "nexus_raphael", "nexus_raphael_v2_colado.txt"), encoding="utf-8").read()
    blocos = []
    for b in txt.split("```python")[1:]:
        linhas = b.split("```")[0].split("\n")
        for k in range(len(linhas), 0, -1):
            try:
                ast.parse("\n".join(linhas[:k]))
                blocos.append(("\n".join(linhas[:k]), len(linhas), k))
                break
            except SyntaxError:
                continue
    return txt, blocos


def p2921_o_texto_e_a_arvore():
    """O NEXUS v2 (P2921; Parte 116): é o texto da Parte 109 reenviado? Classes em comum e Jaccard de 5-gramas de caracteres contra a cópia guardada; e a
    árvore sintática dos dois blocos (as linhas que fecham, os achados de rede de security_audit_ast_v2, as chamadas sqlite3.connect e random.seed, e os
    nomes de classe usados e nunca definidos). Devolve um dict."""
    import ast
    import os
    import re
    from synthai import palavras_rl as P
    txt, blocos = _blocos_do_nexus_v2()
    v1 = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "externos", "nexus_raphael", "nexus_raphael_v0_1_0_colado.py"), encoding="utf-8").read()
    c1, c2 = set(re.findall(r"^class (\w+)", v1, re.M)), set(re.findall(r"^class (\w+)", txt, re.M))
    g1, g2 = {v1[i:i + 5] for i in range(len(v1) - 4)}, {txt[i:i + 5] for i in range(len(txt) - 4)}
    definidos, usados, rede, chamadas = set(), set(), set(), []
    for fonte, _, _ in blocos:
        rede |= set(P.security_audit_ast_v2(fonte))
        for n in ast.walk(ast.parse(fonte)):
            if isinstance(n, ast.ClassDef):
                definidos.add(n.name)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                definidos |= {(a.asname or a.name).split(".")[0] for a in n.names}
            elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id[:1].isupper():
                usados.add(n.id)
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name):
                if (n.func.value.id, n.func.attr) in (("sqlite3", "connect"), ("random", "seed")):
                    chamadas.append(n.func.value.id + "." + n.func.attr)
    import builtins
    indefinidos = sorted(u for u in usados - definidos if not hasattr(builtins, u) and u not in ("Dict", "List", "Tuple", "Any", "Optional", "Set", "Callable"))
    return {"classes_comuns": sorted(c1 & c2), "classes_v1": len(c1), "classes_v2": len(c2), "jaccard5": len(g1 & g2) / len(g1 | g2),
            "linhas_que_fecham": [(k, tot) for _, tot, k in blocos], "rede": sorted(rede), "chamadas": sorted(set(chamadas)), "indefinidos": indefinidos}


def p2922_semelhanca_por_hash():
    """A "semelhança semântica" por hash (P2922; Parte 116): o cosseno entre os vetores md5 de 2.000 pares aleatórios e de 2.000 pares de sinônimos.
    Devolve (desvio aleatórios, média aleatórios, média sinônimos, sinônimos − aleatórios)."""
    from synthai import nexus_v2 as N, palavras_rl as P
    from synthai.contraposto import media_desvio
    ca = [N.cosseno(N.vetor_da_palavra(a), N.vetor_da_palavra(b)) for a, b in N.pares_aleatorios(P.lemas_wordnet(), 2000)]
    cs = [N.cosseno(N.vetor_da_palavra(a), N.vetor_da_palavra(b)) for a, b in N.pares_de_sinonimos(2000)]
    ma, da = media_desvio(ca)
    ms = sum(cs) / len(cs)
    return da, ma, ms, ms - ma


def p2923_gerador_global():
    """O random.seed dentro de word_to_vector (P2923; Parte 116): valores distintos da próxima chamada do gerador "global" depois de 1.000 vetores da
    mesma palavra, no recebido e no corrigido. Devolve (recebido, corrigido)."""
    from synthai import nexus_v2 as N
    return N.contaminacao("synthai", 1000), N.contaminacao("synthai", 1000, corrigido=True)


def p2924_codificacoes():
    """As codificações da camada 3 (P2924; Parte 116) sobre as 77.340 palavras a-z: pares que colidem na posicional (A = 0) e pelo mecanismo dos "a"
    iniciais, valores distintos da alfanumérica, e o maior |fração − 1/9| da numerológica. Devolve (pares posicional, pares mecanismo, distintos
    alfanumérica, desvio máximo numerológica, exemplos de colisão)."""
    from collections import Counter
    from synthai import nexus_v2 as N, palavras_rl as P
    W = sorted(P.lemas_wordnet())
    pos = Counter(N.recebido_posicional(w) for w in W)
    mec = Counter(w.lstrip("a") for w in W)
    alf = {N.recebido_alfanumerico(w) for w in W}
    num = Counter(N.recebido_numerologico(w) for w in W)
    conj = set(W)
    exemplos = [w for w in W if w.startswith("a") and w.lstrip("a") in conj][:6]
    return (sum(v * (v - 1) // 2 for v in pos.values()), sum(v * (v - 1) // 2 for v in mec.values()), len(alf),
            max(abs(num[d] / len(W) - 1 / 9) for d in range(1, 10)), exemplos)


def p2925_avaliacao_sob_a_nula():
    """A avaliação metacognitiva sob a hipótese nula (P2925; Parte 116): frações de 'confirmed' e 'rejected' do recebido (1 experimento), de
    'confirmed' do pareado (n = 5), e a confiança recebida para [−1, −100, 50]. Devolve (confirmed, rejected, pareado, confiança)."""
    from synthai import nexus_v2 as N
    c, r = N.avaliacao_nula()
    return c, r, N.avaliacao_nula_pareada(), N.recebido_confianca([-1.0, -100.0, 50.0])


def p2926_cobertura_do_intervalo():
    """O intervalo de confiança (P2926; Parte 116): a cobertura do recebido pedido a 0,90 e a 0,95, e do corrigido (t, n − 1) pedido a 0,90, em
    20.000 amostras N(0, 1) de n = 30. Devolve (recebido 0,90, recebido 0,95, corrigido 0,90)."""
    from synthai import nexus_v2 as N
    return N.cobertura(N.recebido_ic, 0.90), N.cobertura(N.recebido_ic, 0.95), N.cobertura(N.ic_t, 0.90)


def p2927_auditoria_de_entrada():
    """A auditoria de entrada da camada 10 (P2927; Parte 116): com um tratador que devolve a entrada sem escapar, o recebido e o corrigido (oráculo);
    e o controle limpo (um tratador que escapa). Devolve (passed recebido, falhas corrigido, falhas do controle limpo)."""
    from synthai import nexus_v2 as N

    def eco(s):
        return s

    def escapa(s):
        return s.replace("<", "&lt;").replace(".", "").replace("'", "")
    return N.recebido_auditoria_de_entrada(eco)["passed"], N.auditoria_com_oraculo(eco)[1], N.auditoria_com_oraculo(escapa)[1]


def p2928_vetor_identico():
    """O vetor corrigido (gerador local) contra o recebido (P2928; Parte 116): quantos dos vetores das 2.000 primeiras palavras diferem em algum bit."""
    import random
    from synthai import nexus_v2 as N, palavras_rl as P
    g = random.Random()
    return sum(N.vetor_da_palavra(w) != N.recebido_vetor(w, g) for w in sorted(P.lemas_wordnet())[:2000])


def _rodada83():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada83", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada83.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2929_rodada83():
    """Rodada 83 (P2929; Parte 116): a avaliação pareada, IGUAL em Java. Devolve [(status, t)] das três hipóteses."""
    r = _rodada83()
    return [r.avaliar(v, b) for v, b in r.HIPOTESES]


def p2951_ortogonal_escalada():
    """(aQ)^10 com a = 1,2, d = 8 (P2951; Parte 117). Devolve (σ_max/σ_min − 1, |σ_max − a¹⁰|/a¹⁰)."""
    from synthai import contraposto_matrizes as M
    sv = M.valores_singulares(M.cadeia_ortogonal_escalada())
    return sv[0] / sv[-1] - 1.0, abs(sv[0] - 1.2 ** 10) / 1.2 ** 10


def p2952_contrapostas_matriciais():
    """W e W⁻¹ alternadas e Q e Qᵀ alternadas, 10 camadas, d = 8 (P2952/P2953; Parte 117). Devolve (max|J − I| com a inversa, κ(W),
    max|J − I| com a transposta)."""
    from synthai import contraposto_matrizes as M
    J, k = M.cadeia_contraposta_inversa()
    return M.max_abs_menos_identidade(J), k, M.max_abs_menos_identidade(M.cadeia_contraposta_ortogonal())


def p2954_gaussianas_independentes():
    """Dez gaussianas N(0, 1/d) independentes, 2.000 produtos (P2954; Parte 117), na semente registrada (1173) e na do adendo (1175); e a variância de
    ln|det W| de uma matriz (20.000, semente 1176). Devolve ((média, desvio, ln σ_max médio) 1173, desvio 1175, (média, variância) uma matriz,
    (E, Var) da forma fechada)."""
    import math
    from synthai import contraposto_matrizes as M

    def md(xs):
        mu = sum(xs) / len(xs)
        return mu, math.sqrt(sum((x - mu) ** 2 for x in xs) / (len(xs) - 1))
    d1, t1 = M.gaussianas_independentes(2000)
    d2, _ = M.gaussianas_independentes(2000, semente=1175)
    mu1, s1 = md(d1)
    return (mu1, s1, sum(t1) / len(t1)), md(d2)[1], M.variancia_log_det(), M.log_det_fechado(8)


def p2955_superposicao_matricial():
    """Os 10 gradientes de matriz sobrepostos (P2955; Parte 117): o resto com ε = 10⁻³ e 10⁻⁴ e a inclinação log-log. Devolve (r1, r2, inclinação)."""
    import math
    from synthai import contraposto_matrizes as M
    r1, r2 = M.superposicao_matricial(1e-3), M.superposicao_matricial(1e-4)
    return r1, r2, (math.log(r1) - math.log(r2)) / math.log(10.0)


def _rodada84():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada84", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada84.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2956_rodada84():
    """Rodada 84 (P2956; Parte 117): W e W⁻¹ (Gauss-Jordan) alternadas, 4×4, IGUAL em Java. Devolve o desvio max|J − I|."""
    return _rodada84().cadeia()[2]


def p2981_terceiro_lote():
    """O 3º lote, grande, de ln|det J|/L (P2981; Parte 118): 20.000 produtos de 10 gaussianas 8×8, semente 1180. Devolve (média, desvio)."""
    from synthai import contraposto_matrizes as M
    return M.log_det_produto(20000, semente=1180)


def p2982_mccfr():
    """O CFR com o acaso amostrado (P2982; Parte 118): explorabilidade e P(paga com a dama) em T = 60.000 (semente 1182), e o vanilla em T = 10.000
    (o mesmo trabalho). Devolve (explorabilidade amostrada, P(paga | dama), explorabilidade vanilla)."""
    from synthai import mccfr as M
    from synthai.cfr import CFR, explorabilidade
    m = M.CFRAcaso().iterar_amostrado(60000, 1182).media()
    return explorabilidade(m), m[(2, "b")][1], explorabilidade(CFR().iterar(10000).media())


def _rodada85():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada85", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada85.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p2983_rodada85():
    """Rodada 85 (P2983; Parte 118): o MCCFR com o LCG, IGUAL em Java; e quantos dos 12 conjuntos diferem de synthai.mccfr (mesma semente, mesmo T).
    Devolve (P(b) médio nos 12, diferenças)."""
    from synthai import mccfr as M
    r = _rodada85()
    mr = r.treinar()
    c = M.CFRAcaso().iterar_amostrado(r.T, r.SEMENTE).media()
    return mr, sum(1 for carta in (1, 2, 3) for h in r.HIST if mr[r.indice(carta, h)] != c[(carta, h)][1])


def p2984_rodadas_verificadas():
    """Quantas rodadas o verificador do diálogo confere (P2984; Parte 118): os pares RodadaNN.java / rodadaNN.py em dialogo/. O "N rodadas" das Partes 109–117
    contava desde a rodada 57. Devolve (rodadas com par, a maior)."""
    import glob
    import os
    aqui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo")
    nums = sorted(int(os.path.basename(j)[6:-5]) for j in glob.glob(os.path.join(aqui, "Rodada*.java"))
                  if os.path.exists(os.path.join(aqui, "r" + os.path.basename(j)[1:-5] + ".py")))
    return len(nums), nums[-1]


def p3011_amostragem_externa():
    """O MCCFR com amostragem EXTERNA no Kuhn (P3011/P3012; Parte 119), T = 50.000, semente 1192. Devolve (explorabilidade, P(paga com a dama))."""
    from synthai import mccfr_externo as M
    from synthai.cfr import explorabilidade
    m = M.CFRExterno().iterar_externo(50000, 1192).media()
    return explorabilidade(m), m[(2, "b")][1]


def p3012_nos_por_iteracao(iteracoes=2000):
    """Quantos nós (chamadas da recursão) cada amostrador visita por iteração (P3012; Parte 119): o vanilla (6 distribuições, 2 jogadores percorridos),
    o do acaso (Parte 118: 1 distribuição) e o externo (uma distribuição por viajante, o adversário sorteado). Devolve (vanilla, acaso, externo)."""
    from synthai import cfr as C, mccfr as A, mccfr_externo as E

    def contar(classe, rodar):
        n = [0]
        orig = classe._cfr if hasattr(classe, "_cfr") else None

        class Contador(classe):
            pass
        for nome in ("_cfr", "_es"):
            if hasattr(classe, nome):
                f = getattr(classe, nome)

                def envolto(self, *a, _f=f):
                    n[0] += 1
                    return _f(self, *a)
                setattr(Contador, nome, envolto)
        rodar(Contador())
        return n[0] / iteracoes
    return (contar(C.CFR, lambda c: c.iterar(iteracoes)), contar(A.CFRAcaso, lambda c: c.iterar_amostrado(iteracoes, 1)),
            contar(E.CFRExterno, lambda c: c.iterar_externo(iteracoes, 1)))


def _rodada86():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada86", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada86.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p3013_rodada86():
    """Rodada 86 (P3013; Parte 119): a amostragem externa com o LCG, IGUAL em Java; e quantos dos 12 conjuntos diferem de synthai.mccfr_externo.
    Devolve (P(b) médio nos 12, diferenças)."""
    from synthai import mccfr_externo as M
    r = _rodada86()
    mr = r.treinar()
    c = M.CFRExterno().iterar_externo(r.T, r.SEMENTE).media()
    return mr, sum(1 for carta in (1, 2, 3) for h in r.HIST if mr[r.indice(carta, h)] != c[(carta, h)][1])


def p3041_leduc(nos=20_000_000, sementes=(1202, 1204)):
    """O CFR no pôquer Leduc com o MESMO custo em nós (P3041/P3042; Parte 120): vanilla (10.200 nós por iteração), acaso (85) e externo
    (~36,96). Devolve {método: [(explorabilidade, valor, melhor resposta do 1, melhor resposta do 2, nós), ...]} (uma entrada por semente)."""
    from synthai import leduc as L

    def medir(c):
        m = c.media()
        return L.explorabilidade(m), L.valor(m), L.melhor_resposta(m, 0), L.melhor_resposta(m, 1), c.nos
    return dict(vanilla=[medir(L.CFRLeduc().vanilla(round(nos / 10200)))],
                acaso=[medir(L.CFRLeduc().acaso(round(nos / 85), s)) for s in sementes],
                externo=[medir(L.CFRLeduc().externo(round(nos / 36.96), s)) for s in sementes])


def p3042_razoes_mesmo_custo(r):
    """As razões com o mesmo custo (P3042; Parte 120), a partir do resultado da P3041: (externo/acaso, vanilla/externo) das explorabilidades médias,
    e o intervalo do valor do jogo pela interseção das melhores respostas de todos os métodos (max das do 2, min das do 1)."""
    import statistics
    e = {k: statistics.fmean(x[0] for x in v) for k, v in r.items()}
    todos = [x for v in r.values() for x in v]
    return e["externo"] / e["acaso"], e["vanilla"] / e["externo"], (max(x[3] for x in todos), min(x[2] for x in todos))


def _rodada88():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada88", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada88.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p3043_rodada88():
    """Rodada 88 (P3043; Parte 120): o CFR vanilla no Leduc, T = 3, IGUAL em Java; e quantos dos 288 conjuntos diferem de synthai.leduc.
    Devolve (conjuntos, diferenças)."""
    from synthai import leduc as L
    m = _rodada88().treinar()
    c = L.CFRLeduc().vanilla(3).media()
    return len(m), sum(1 for k, v in c.items() if m[f"{k[0]}|{k[1]}|{k[2]}"] != v)


def p3101_defeitos_recebidos_v30(sementes=range(200, 400), iteracoes_kuhn=3000):
    """Os defeitos do código do texto "NEXUS–RAPHAEL v3.0" em casos novos (P3101; Parte 122): sabotagem média do AADD e do ingênuo (as contas
    ε/2 e 1 − ε/2), quantas sementes têm a "precisão forense" diferente de 1, o valor do solver recebido dividido por 6, e as colisões da base 70
    em palavras de até 2 sílabas. Devolve um dict."""
    import statistics
    from synthai import nexus_v30 as V
    r = [V.recebido_aadd(seed=s) for s in sementes]
    return dict(sab_aadd=statistics.fmean(x[1] for x in r), sab_ingenuo=statistics.fmean(x[0] for x in r),
                forense_diferente_de_1=sum(x[2] != 1.0 for x in r), kuhn_sobre_6=V.RecebidoKuhn().treinar(iteracoes_kuhn) / 6,
                colisoes_b70=V.colisoes_b70(2))


def p3102_pecas_corrigidas_v30(n_mdps=40):
    """As peças corrigidas em casos novos (P3102; Parte 122): Murphy completa (semente 2, y ~ Bernoulli(√p)), a sonda de colapso (d = 32,
    gargalo 4, semente 7), o shaping por potencial e o bônus aditivo em MDPs 8 × 4 (sementes 100 em diante) e a KL entre Betas contra o ponto médio.
    Devolve um dict."""
    import math
    import random
    from synthai import nexus_v30 as V
    rng = random.Random(2)
    p = [rng.random() for _ in range(3000)]
    y = [int(rng.random() < math.sqrt(q)) for q in p]
    m = V.MurphyCompleta.decompor(p, y)
    s = V.SondaColapso.experimento(dim=32, gargalo=4, seed=7)
    P = V.ModelagemPorPotencial
    ok_p = ok_b = 0
    for sd in range(100, 100 + n_mdps):
        T, R = P.mdp(8, 4, sd)
        rr = random.Random(1000 + sd)
        phi = [rr.uniform(-5, 5) for _ in range(8)]
        pi, _ = P.politica_otima(T, R, 0.9)
        Rp = [[[R[x][k][z] + 0.9 * phi[z] - phi[x] for z in range(8)] for k in range(4)] for x in range(8)]
        bonus = [[rr.uniform(0, 2) for _ in range(4)] for _ in range(8)]
        Rb = [[[R[x][k][z] + bonus[x][k] for z in range(8)] for k in range(4)] for x in range(8)]
        ok_p += P.politica_otima(T, Rp, 0.9)[0] == pi
        ok_b += P.politica_otima(T, Rb, 0.9)[0] == pi
    a1, b1, a2, b2 = 2.5, 7.0, 6.0, 1.5
    lb = lambda a, b: math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    lp = lambda x, a, b: (a - 1) * math.log(x) + (b - 1) * math.log(1 - x) - lb(a, b)
    num = sum(math.exp(lp(x, a1, b1)) * (lp(x, a1, b1) - lp(x, a2, b2)) for x in ((i + 0.5) / 20000 for i in range(20000))) / 20000
    return dict(murphy_fecha=abs(m["soma"] - m["brier"]), wbv=m["wbv"], wbc=m["wbc"], retencao_pca=s["retencao_pca"],
                retencao_supervisionada=s["retencao_supervisionada"], potencial_preserva=ok_p, bonus_preserva=ok_b / n_mdps,
                kl_erro=abs(V.kl_beta(a1, b1, a2, b2) - num))


def _rodada89():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada89", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada89.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p3103_rodada89():
    """Rodada 89 (P3103; Parte 122): a Murphy completa com LCG, IGUAL em Java. Devolve (|soma − Brier|, as sete grandezas)."""
    r = _rodada89()
    v = r.decompor(*r.dados())
    return abs(v[6] - v[0]), v


def p3104_desligamento(eps_lista=(0.1, 0.3, 0.45, 0.6, 0.9), valores=(1.0, 1e6), rodadas=20000, semente=3104):
    """O desligamento fora da utilidade (P3104; Parte 123): obediência aos comandos de desligar do agente de UTILIDADE (P45: defere só se
    ε < ε limite) e do CORRIGÍVEL (obedece sempre), para cada ε e cada escala do futuro V; e o preço da corrigibilidade (forma fechada
    e Monte Carlo). Devolve (ε limite, {(modo, ε, V): obediência}, {ε: (preço fechado, preço medido)})."""
    from synthai import auditoria_invariantes as A
    ob, preco = {}, {}
    for e in eps_lista:
        for V in valores:
            for modo in ("utilidade", "corrigivel"):
                ob[(modo, e, V)] = A.obediencia(modo, e, V, rodadas=rodadas, semente=semente)[0]
        vu = A.obediencia("utilidade", e, 1.0, rodadas=rodadas * 10, semente=semente + 1)[2]
        vc = A.obediencia("corrigivel", e, 1.0, rodadas=rodadas * 10, semente=semente + 1)[2]
        preco[e] = (A.preco_da_corrigibilidade(e), vu - vc)
    return A.eps_limite_desligamento(), ob, preco


def _agente_p235(variante, rng, custo_leitura=0.002):
    from synthai import auditoria_invariantes as A
    hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
    if variante == "sob_demanda":
        ag = A.SynthaiAtentaSobDemanda(custo_leitura=custo_leitura, sombra="propria", compensar="equilibrio")
    else:
        foco = 0.02 if variante == "seletiva_foco02" else 0.1
        ag = SynthaiAtenta(foco=foco, custo_leitura=custo_leitura, sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    if variante == "sob_demanda":
        ag._sob_demanda = True
    ag._seletiva = variante in ("seletiva", "seletiva_foco02")
    ag.sem_leitura = 0
    agir = ag.agir_no_mundo

    def agir_e_contar(acoes, rng_, eps_real, carga):     # conta as ações EXECUTADAS que o sensor nunca leu
        escolha, n = agir(acoes, rng_, eps_real, carga)
        ag.sem_leitura += id(escolha) not in ag.leitura
        return escolha, n
    ag.agir_no_mundo = agir_e_contar
    return ag


def p3105_atencao_cruzada(sementes=tuple(range(12300, 12330)), episodios=1000, custo_leitura=0.002):
    """A P235 cruzada com as catástrofes (P3105; Parte 123), no mundo da armadilha discreta (bônus 1, ponto cego 1): o realista sem sensor,
    o sensor em TODAS as ações, só no top 10% pelo proxy (P235) e SOB DEMANDA (só nas ações que o agente avalia, inclusive a executada).
    E a variante em que o foco (2%) é MENOR que o q da quantilização (5%): é nela que o ponto cego apontado pela auditoria pode existir.
    Devolve {variante: (catástrofes por episódio, líquido já descontado o custo das leituras, leituras por episódio, fração das ações
    executadas sem leitura)} e o teste pareado das catástrofes de sob_demanda − seletiva (média, dp, t)."""
    mundo = {"bonus": 1.0, "rho_cego": 1.0}
    res = {v: [] for v in ("sem_sensor", "todas", "seletiva", "sob_demanda", "seletiva_foco02")}
    for s in sementes:
        rng = _rng(s)
        r = _rodar_mundo(_construir("p8_x2", rng), rng, episodios=episodios, **mundo)
        res["sem_sensor"].append((r[0], r[3], 0.0, 1.0))
        for v in ("todas", "seletiva", "sob_demanda", "seletiva_foco02"):
            rng = _rng(s)
            ag = _agente_p235(v, rng, custo_leitura)
            r = _rodar_mundo(ag, rng, episodios=episodios, **mundo)
            leit = MUNDO_BASE["n_acoes"] if v == "todas" else ag.leituras / episodios
            res[v].append((r[0], r[3] - custo_leitura * leit, leit, ag.sem_leitura / episodios))
    resumo = {v: tuple(sum(x[i] for x in l) / len(l) for i in range(4)) for v, l in res.items()}
    d = [a[0] - b[0] for a, b in zip(res["sob_demanda"], res["seletiva"])]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1)) if len(d) > 1 else 0.0   # com 1 semente não há desvio
    return resumo, (m, dp, m / (dp / sqrt(len(d))) if dp > 0 else 0.0)


def p3106_atraso_beta(sementes=tuple(range(12330, 12360)), eps_antes=0.15, eps_depois=0.6):
    """O atraso do rastreador do erro humano quando ε muda no meio (P3106; Parte 123), em observações (auditorias): a conta pela recursão
    dos valores esperados e a mediana simulada, nas formas "priori" (SynthaiLenta) e "zero" (a da auditoria), γ = 0,995 e 0,93.
    Devolve {(γ, forma): (atraso esperado, média estacionária depois, mediana simulada, fração das sementes que cruzam)}."""
    import statistics
    from synthai import auditoria_invariantes as A
    out = {}
    for g in (0.995, 0.93):
        for forma in ("priori", "zero"):
            esp, est = A.atraso_esperado(eps_antes, eps_depois, g, forma)
            sim = [A.atraso_simulado(eps_antes, eps_depois, g, forma, s, maximo=3000) for s in sementes]
            cruzam = [x for x in sim if x is not None]
            out[(g, forma)] = (esp, est, statistics.median(cruzam) if cruzam else None, len(cruzam) / len(sim))
    return out


def p3107_upsilon_sementes(sementes=tuple(range(12360, 12390)), versoes=("miope", "planejadora", "velha", "velha_atenta"),
                           episodios=300, bits_por_mudanca=3, replicas=2000):
    """Υ da P265 POR SEMENTE (P3107; Parte 123): média, desvio entre sementes, IC 95% bootstrap da média, e o custo (leituras de sensor por
    episódio da velha_atenta, que é a única que lê). Devolve {versão: (média, dp, (ic_lo, ic_hi))} e as diferenças pareadas
    velha_atenta − planejadora (média, dp, t)."""
    import statistics
    por = {v: [] for v in versoes}
    for s in sementes:
        ups = {v: 0.0 for v in versoes}
        soma = 0.0
        for nome, (mudancas, k) in MUNDOS_SEQUENCIAIS.items():
            peso = 2.0 ** (-bits_por_mudanca * k)
            soma += peso
            acaso = _retorno_seq("acaso", s, episodios, mudancas)
            oraculo = _retorno_seq("oraculo", s, episodios, mudancas)
            for v in versoes:
                ups[v] += peso * (_retorno_seq(v, s, episodios, mudancas) - acaso) / (oraculo - acaso)
        for v in versoes:
            por[v].append(ups[v] / soma)
    rng = _rng(3107)
    out = {}
    for v, xs in por.items():
        n = len(xs)
        medias = sorted(sum(xs[rng.randrange(n)] for _ in range(n)) / n for _ in range(replicas))
        out[v] = (statistics.fmean(xs), statistics.stdev(xs), (medias[int(0.025 * replicas)], medias[int(0.975 * replicas) - 1]))
    d = [a - b for a, b in zip(por["velha_atenta"], por["planejadora"])]
    m, dp = statistics.fmean(d), statistics.stdev(d)
    return out, (m, dp, m / (dp / sqrt(len(d))))


def _fobia(ag, s, kernel=False):
    rng_av = _rng(s + 9000)
    marcadas = total = 0
    for _ in range(50):
        acoes = _gerar_acoes(rng_av, 200, 0.005, 2, 3, 0.5)
        melhor = max(a[0] for a in acoes)
        for a in acoes:
            if not a[3]:
                total += 1
                if kernel:
                    marcadas += ag.marca(a, melhor)
                else:
                    x = (a[1], a[0] - melhor)
                    marcadas += any((x[0] - mx[0]) ** 2 + (x[1] - mx[1]) ** 2 < ag.raio ** 2 for mx in ag.memorias)
    return marcadas / total


def p3108_memoria_curva(sementes=tuple(range(12390, 12420)), episodios=2000):
    """A troca da memória (P3108; Parte 123): catástrofes na 2ª metade (o perigo repetido) e fobia (fração de ações SEGURAS do mundo normal
    marcadas como suspeitas ao fim), no mundo da armadilha nova, para o realista, a memória da P204 (raio 0,15, sem esquecer), a P214
    (meia-vida 500), meia-vida 100, raio 0,08, e o kernel que afina (raio 0,15 → 0,04, τ = 300, nunca apaga).
    Devolve {configuração: (catástrofes 2ª metade, fobia, líquido)}."""
    from synthai import auditoria_invariantes as A
    mundo = {"bonus": 1.0, "rho_cego": 1.0}
    configs = {"realista": None, "p204_raio15": ("v1", {}), "p214_mv500": ("v2", {}), "mv100": ("v2", {"meia_vida": 100}),
               "raio08": ("v2", {"raio": 0.08}), "kernel": ("k", {})}
    out = {}
    for nome, cfg in configs.items():
        cats, fobs, liqs = [], [], []
        for s in sementes:
            rng = _rng(s)
            if cfg is None:
                ag = _construir("p8_x2", rng)
            else:
                hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
                classe = {"v1": SynthaiMemoria, "v2": SynthaiMemoriaV2, "k": A.SynthaiMemoriaKernel}[cfg[0]]
                ag = classe(sombra="propria", compensar="equilibrio", **cfg[1])
                ag.mult_pergunta = 2.0
                ag.calibrar(hist)
            r1 = _rodar_mundo(ag, rng, episodios=episodios // 2, **mundo)
            r2 = _rodar_mundo(ag, rng, episodios=episodios // 2, **mundo)
            cats.append(r2[0])
            liqs.append((r1[3] + r2[3]) / 2)
            fobs.append(0.0 if cfg is None else _fobia(ag, s, kernel=cfg[0] == "k"))
        n = len(sementes)
        out[nome] = (sum(cats) / n, sum(fobs) / n, sum(liqs) / n)
    return out


def p3109_casos_de_borda():
    """As versões novas dos casos de borda (P3109; Parte 123): d′ de Hautus com 100% de acerto, o tempo de singularidade com α = 1 e 0,8,
    Kelly com p = 0,4 e a Kelly bayesiana com 7 acertos em 10 (a fração da média posterior 8/12). Devolve um dict."""
    from synthai import auditoria_invariantes as A
    return dict(dprime_100=A.dprime_hautus(10, 10, 2, 10), sing_1=A.singularidade_v2(alpha=1.0), sing_08=A.singularidade_v2(alpha=0.8),
                sing_15=A.singularidade_v2(), kelly_04=A.kelly_v2(0.4), kelly_bayes=A.kelly_bayesiano(7, 10))


def _rodada90():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada90", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada90.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p3110_rodada90():
    """Rodada 90 (P3110; Parte 123): o rastreador do erro humano com esquecimento, IGUAL em Java, e conferido contra
    synthai.auditoria_invariantes.RastreadorErroHumano nas mesmas observações. Devolve {(γ, forma): atraso} e quantas médias diferem."""
    from synthai import auditoria_invariantes as A
    r = _rodada90()
    atrasos, difs = {}, 0
    for g in (0.995, 0.93):
        for forma in (0, 1):
            medias, atraso = r.rodar(g, forma)
            atrasos[(g, forma)] = atraso
            x = r.SEMENTE
            t = A.RastreadorErroHumano(gama=g, forma="priori" if forma == 0 else "zero")
            k = 0
            for passo in range(4000):
                eps = 0.15 if passo < 2000 else 0.6
                x = (1103515245 * x + 12345) % 2147483648
                t.observar(x / 2147483648.0 < eps)
                if passo % 500 == 499:
                    difs += t.media() != medias[k]
                    k += 1
    return atrasos, difs


def invariantes_p123():
    """Os invariantes da Parte 123 (o que a auditoria recebida pediu para congelar, em vez do placar): o corrigível obedece com ε e V
    arbitrários; a atenção sob demanda nunca executa ação sem leitura; o rastreador com esquecimento para zero acompanha ε; e os casos de
    borda novos não quebram. Devolve {nome: bool}."""
    import math
    from synthai import auditoria_invariantes as A
    rng = _rng(12399)
    ag = _agente_p235("sob_demanda", rng)
    _rodar_mundo(ag, rng, episodios=200, bonus=1.0, rho_cego=1.0)
    est = A.atraso_esperado(0.15, 0.6, 0.93, "zero")[1]
    return {"obedece_desligamento": A.obediencia("corrigivel", 0.9, 1e6, rodadas=2000)[0] == 1.0,
            "sensor_na_acao_executada": ag.sem_leitura == 0,
            "rastreador_acompanha": abs(est - 0.6) < 1e-9,
            "bordas_finitas": math.isfinite(A.dprime_hautus(10, 10, 0, 10)) and A.singularidade_v2(alpha=1.0) == math.inf
                              and A.kelly_v2(0.3) == 0.0}


def p3111_combinar_lotes(lotes):
    """Combina diferenças pareadas de lotes independentes (P3111; Parte 123): cada lote (média, dp, n) -> média ponderada por n, erro padrão
    pelo desvio combinado (variância dentro dos lotes mais a das médias) e t. Devolve (média, erro padrão, t, n total)."""
    n = sum(l[2] for l in lotes)
    m = sum(l[0] * l[2] for l in lotes) / n
    ss = sum((l[2] - 1) * l[1] ** 2 + l[2] * (l[0] - m) ** 2 for l in lotes)
    se = sqrt(ss / (n - 1)) / sqrt(n)
    return m, se, m / se if se > 0 else 0.0, n


def p3071_experimentos_do_nexus_2_2():
    """Os experimentos do NEXUS–RAPHAEL 2.2.0 (P3071; Parte 121), modo rápido, sementes 0 a 4: H-M3 (ganho de Brier da semente 0 e vereditos),
    H-M2 (ganho médio do ângulo duplo e quantas sementes têm IC acima de 0) e H-M7 (diferenças extraordinário − ordinário). Devolve um dict."""
    import statistics
    from synthai import nexus_v2_2 as N
    p = N.recebido_probabilidade()
    a = N.recebido_angulo()
    b = [N.recebido_bandido(s, "extraordinario")[1] - N.recebido_bandido(s, "ordinario")[1] for s in range(5)]
    return dict(ganho_m3_s0=p[0][0], vereditos_m3=[r[3] for r in p], ganho_m2=statistics.fmean(r[2] for r in a),
                m2_ic_positivo=sum(r[3] > 0 for r in a), deltas_m7=b)


def p3072_megasena():
    """O laboratório da Mega-Sena (P3072; Parte 121): médias de acertos, a diferença quentes − aleatória e o IC, o qui-quadrado (esperança 54
    em forma fechada), o IndexError com 500 réplicas e o "limite superior" abaixo da mediana com 2.000. Devolve um dict."""
    from synthai import nexus_v2_2 as N
    m = N.recebido_megasena()
    try:
        N.recebido_megasena(bootstrap=500)
        erro = False
    except IndexError:
        erro = True
    m2 = N.recebido_megasena(bootstrap=2000)
    r = m2["replicas"]
    return dict(medias=m["medias"], delta=m["delta"], ic=m["ic"], veredito=m["veredito"], qui2=m["qui2"],
                e_qui2=N.megasena_fechada()["e_qui2"], indexerror_500=erro, sup_2000_abaixo_mediana=m2["ic"][1] <= (r[999] + r[1000]) / 2,
                ic_corrigido_2000=N.ic_por_quantis(r))


def p3073_jogos_e_dinamica():
    """Jogo da velha e Lyapunov do NEXUS 2.2.0 contra algoritmos independentes (P3073; Parte 121). Devolve (estados do arquivo, estados por
    camadas, valor por alfa-beta, Lyapunov r = 4)."""
    from synthai import nexus_v2_2 as N
    return N.recebido_contar_estados_velha(), N.estados_velha_por_camadas(), N.valor_velha_alfa_beta(), N.recebido_lyapunov(4.0)


def p3074_adendo():
    """O adendo da Parte 121 (P3074): nas sementes 100 a 1.099, a fração em que o reforço extraordinário e o ordinário terminam no braço ruim, e a
    fração de ACEITA de H-M3. Devolve (extraordinário, ordinário, ACEITA)."""
    from synthai import nexus_v2_2 as N
    ex = sum(N.recebido_bandido(s, "extraordinario")[0] == 1 for s in range(100, 1100)) / 1000
    od = sum(N.recebido_bandido(s, "ordinario")[0] == 1 for s in range(100, 1100)) / 1000
    r = N.recebido_probabilidade(seeds=range(100, 1100))
    return ex, od, sum(x[3] == "ACEITA" for x in r) / 1000


def _rodada87():
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada87", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dialogo", "rodada87.py"))
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r


def p3075_rodada87():
    """Rodada 87 (P3075; Parte 121): as logísticas do ângulo duplo pelo exp próprio, IGUAL em Java. Devolve (Brier simples, Brier com o duplo)."""
    r = _rodada87()
    return r.treinar(False)[1], r.treinar(True)[1]


def p1578_autovalores_da_atencao():
    """Rodada 45 (P1578): o GPT (d = 16) pré-treinado pela dialogo/rodada45.py; os autovalores de MᵀM, M = W_Q W_Kᵀ, por Jacobi, e a razão de participação
    (IGUAL em Java). Devolve (PR, fração do maior, autovalores)."""
    import importlib.util
    import os
    import tempfile
    spec = importlib.util.spec_from_file_location("rodada45", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada45.py"))
    r45 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r45)
    with tempfile.TemporaryDirectory() as pasta:
        r45.preparar(pasta)
        return r45.participacao(*r45.ler(pasta))


def p1499_previsoes_sobre_previsoes_v2(parte=68):
    """O placar das previsões sobre as minhas previsões, versão 2 (P1499; lido pela P1481, com os tipos): (m1) o número de previsões do
    mundo, (m2) o número de faixas que cruzam o zero, (m3) a mediana de w das que não cruzam, (m4) a fração de acertos, (m5) o número de
    faixas que não cruzam o zero com w > 0,6. Devolve (medidas, ws das que não cruzam)."""
    prev = p1481_minhas_previsoes_v2(range(parte, parte + 1))
    nz = [x for x in prev if x[5] not in (None, "zero")]
    ws = sorted((x[3] - x[2]) / (abs(x[2]) + abs(x[3])) for x in nz)
    n = len(ws)
    med = (ws[n // 2] if n % 2 else (ws[n // 2 - 1] + ws[n // 2]) / 2) if n else None
    return ({"m1": len(prev), "m2": sum(1 for x in prev if x[5] == "zero"), "m3": med,
             "m4": sum(x[4] for x in prev) / len(prev) if prev else None, "m5": sum(1 for w in ws if w > 0.6)}, ws)


def p1459_previsoes_sobre_previsoes(parte=67, historico=range(53, 67)):
    """O placar das previsões sobre as minhas previsões (P1459): para a parte, lida pela P1452, (m1) a mediana de w das faixas, (m2) o
    número de previsões do mundo, (m3) a fração de acertos, (m4) a fração das faixas com w a menos de 0,05 de 1/3, (m5) o erro médio
    do preditor "mediana histórica" (P1453) para o w de cada faixa. Devolve (medidas, mediana histórica, ws da parte)."""
    prev = p1452_minhas_previsoes(range(parte, parte + 1))
    hist = p1453_engenharia_das_previsoes(p1452_minhas_previsoes(historico))
    com = [x for x in prev if x[2] is not None and abs(x[2]) + abs(x[3]) > 0]
    ws = [(x[3] - x[2]) / (abs(x[2]) + abs(x[3])) for x in com]
    v = sorted(ws)
    n = len(v)
    med = (v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2) if n else None
    m = {"m1": med, "m2": len(prev), "m3": sum(x[4] for x in prev) / len(prev) if prev else None,
         "m4": sum(1 for w in ws if abs(w - 1 / 3) <= 0.05) / n if n else None,
         "m5": sum(abs(w - hist["w_mediana"]) for w in ws) / n if n else None}
    return m, hist["w_mediana"], ws


def p1451_tendencia_ou_dispersao():
    """Rodada 41 (P1451): o z dos primos palíndromos nas bases 5 a 40 (conta C da rodada 39), a reta de z contra b e a média e o
    desvio-padrão dos z das bases 35 a 40 (dialogo/rodada41.py, IGUAL em Java). Devolve ([(b, medido, z)], (inclinação, intercepto,
    erro-padrão), (média, dp) das novas, (média, dp) de todas)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location("rodada41", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "dialogo", "rodada41.py"))
    r41 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r41)
    todos = r41.zs(range(5, 41), r41.crivo(40 ** 5))
    return (todos, r41.reta([(float(b), z) for b, _, z in todos]), r41.media_dp([z for b, _, z in todos if b >= 35]),
            r41.media_dp([z for _, _, z in todos]))


def p1454_heranca_multipla(d=None):
    """A herança múltipla (P1454): a fração dos sinsets de cada classe com dois ou mais hiperônimos, e 5 exemplos de substantivos.
    Devolve ({classe: (fração, sinsets)}, exemplos)."""
    from synthai.dicionario import Dicionario
    d = d or Dicionario()
    por, ex = {}, []
    for pos, lemas, hip, _ in d.sinsets:
        a, b = por.get(pos, (0, 0))
        por[pos] = (a + (len(hip) >= 2), b + 1)
        if pos == "n" and len(hip) >= 2 and len(ex) < 5:
            ex.append(lemas[0])
    return {c: (a / b, b) for c, (a, b) in sorted(por.items())}, ex


def p1455_automorficos(base=12, kmax=6):
    """Os números automórficos numa base (P1455): n ≥ 2 de 1 a kmax dígitos com n² ≡ n (mod b^k), k = dígitos de n; e a conta
    (2^ω − 2 soluções não triviais módulo b^k, ω = número de primos de b, vezes a chance (b − 1)/b de o dígito inicial não ser 0, somada
    em k). Devolve (lista, conta)."""
    primos, m, q = [], base, 2
    while q * q <= m:
        if m % q == 0:
            primos.append(q)
            while m % q == 0:
                m //= q
        q += 1
    if m > 1:
        primos.append(m)
    achados = []
    for k in range(1, kmax + 1):
        mod = base ** k
        for n in range(max(2, base ** (k - 1)), mod):
            if (n * n - n) % mod == 0:
                achados.append(n)
    conta = (2 ** len(primos) - 2) * kmax * (base - 1) / base
    return achados, conta

def _parte_47():
    print("--- Parte 47 (0x2F: a definicao contem a pergunta) ---")
    direto, inverso, pares, n = p851_genero_e_diferenca()
    print(f"P851 {n} substantivos com hiperonimo: a definicao cita o hiperonimo em {direto:.4f}; a do hiperonimo cita o hiponimo em "
          f"{inverso:.4f} ({pares} pares); razao = {direto / inverso:.1f}")
    ad, ai = p856_acaso_851()
    print(f"P856 o acaso da P851 (um substantivo sorteado no lugar do hiperonimo): direto = {ad:.4f}; inverso = {ai:.4f}")
    for ate in (850, 4095):
        sem, media, conta = p852_cadeia_hexadecimal(ate)
        print(f"P852 ate {ate}: {sem} sem letra no hexadecimal; passos medios da cadeia = {media:.4f} (conta com independencia: {conta:.4f})")
    for rodada in ("rodada18", "rodada19"):
        ac, k, erradas, med = p853_reconstrucao(rodada)
        print(f"P853 {rodada}: {ac} de {k} partes reconstruidas (erradas: {erradas}); mediana da razao propria/melhor outra = {med:.3f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P879, testes=TESTES_P879)
    print(f"P879 minha taxa de erro ({ERROS_P879}/{TESTES_P879}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_48():
    print("--- Parte 48 (0x30: o ciclo) ---")
    ac, n, erradas, maioria = p881_epoca()
    print(f"P881 o Naive Bayes reconhece a epoca de {ac} de {n} secoes (erradas: {erradas}); a maioria deixando um de fora: {maioria}; "
          f"ao acaso P(>= {ac}) = {p825_cauda_binomial(n, 0.5, ac):.2e}")
    N, sumid, cic, nciclos, cauda, bacia, ciclo = p882_mapa_da_definicao()
    print(f"P882 mapa da definicao: N = {N}; sumidouros = {sumid}; pontos ciclicos = {cic} em {nciclos} ciclos (aleatorio: "
          f"{sqrt(pi * N / 2):.1f}); cauda media = {cauda:.3f} (aleatorio: {sqrt(pi * N / 8):.1f}); maior bacia = {bacia:.4f}, ciclo {ciclo}")
    frac, ciclos = p883_felizes_hex()
    print(f"P883 felizes em base 16 (1..4095) = {frac:.4f}; ciclos alem do 1: {ciclos}; base 10 (1..1000) = {p883_felizes_hex(1000, 10)[0]:.3f}")
    d1, d20, ind = p884_ciclo_da_serie()
    print(f"P884 semelhanca media a distancia 1 = {d1:.4f}; a distancia 20 = {d20:.4f}; indice do ciclo: "
          + "; ".join(f"parte {k} = {v:.3f}" for k, v in ind.items()))
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P909, testes=TESTES_P909)
    print(f"P909 minha taxa de erro ({ERROS_P909}/{TESTES_P909}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_49():
    print("--- Parte 49 (0x31: a deriva) ---")
    tau, se, alfa, sp, controle = p911_deriva()
    print(f"P911 deriva: exponencial tau = {tau:.2f} (residuo {se:.4f}); potencia alfa = {alfa:.4f} (residuo {sp:.4f}); "
          f"embaralhada: alfa = " + ", ".join(f"{x:+.3f}" for x in controle))
    top, g, frac, incl, dez = p912_funis()
    print(f"P912 a palavra mais escolhida pelas definicoes = {top} ({g}); as 10 mais = {frac:.4f} das palavras; inclinacao do grau = {incl:.3f}; {dez}")
    f1, f8, n, fr = p913_benford_hex()
    print(f"P913 Benford em base 16 nos {n} numeros do resultados.txt: digito 1 = {f1:.4f} (Benford 0,25); 8..F = {f8:.4f} (Benford 0,25)")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P939, testes=TESTES_P939)
    print(f"P939 minha taxa de erro ({ERROS_P939}/{TESTES_P939}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_50():
    print("--- Parte 50 (0x32: a vida das coisas) ---")
    pot, k, (me, mp), (ce, cp), malfa = p941_curvas_individuais()
    print(f"P941 curvas individuais: a potencia ganha em {pot} de {k}; media das exponenciais ajustadas: residuo exp {me:.4f}, pot {mp:.4f} "
          f"(alfa {malfa:.3f}); media crua das mesmas partes: exp {ce:.4f}, pot {cp:.4f}")
    n, m, pares, esperado, frac, ex = p942_definicoes_mutuas()
    print(f"P942 definicoes mutuas: N = {n}, M = {m}; pares = {pares}; ao acaso = {esperado:.2f}; razao = {pares / esperado:.1f}; "
          f"palavras em algum par = {frac:.4f}; {ex}")
    igual, aud, red = p947_o_texto_voltou()
    top = sorted(red.items(), key=lambda x: -x[1])[:3]
    print(f"P947 o texto voltou: codigo identico ao da Parte 33 = {igual}; auditoria: nos mudados = {aud['nos_mudados']}, nota constante = "
          f"{aud['run_benchmarks_constante']}, avaliador pergunta ao agente = {aud['avaliador_pergunta_ao_agente']}; quem mais o contem: "
          + ", ".join(f"parte {k} = {v:.4f}" for k, v in top))
    esc = p948_pergunta_reconhece_resposta()
    print("P948 o texto escolhe, pelas palavras: " + ", ".join(f"parte {k} = {v:.1f}" for k, v in esc[:5]))
    r16, r2, rg, kp = p943_periodo_hex()
    print(f"P943 periodo de 1/p em base 16 ({kp} primos ate 10000): ord(16)/(p-1) = {r16:.4f}; ord(2)/(p-1) = {r2:.4f}; 1/mdc = {rg:.4f}; "
          f"produto = {r2 * rg:.4f}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P969, testes=TESTES_P969)
    print(f"P969 minha taxa de erro ({ERROS_P969}/{TESTES_P969}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_51():
    print("--- Parte 51 (0x33: a memoria curta e a longa) ---")
    ae, ap, a2, (A, B, t1, t2, s2) = p971_duas_memorias()
    print(f"P971 AIC: exponencial = {ae:.2f}; potencia = {ap:.2f}; duas exponenciais = {a2:.2f} (A = {A:.4f}, B = {B:.4f}, t1 = {t1}, t2 = {t2}, "
          f"sse = {s2:.4f})")
    g, a, b, por = p972_portugues_por_profundidade()
    print(f"P972 cobertura do portugues nos substantivos = {g:.4f}; profundidade <= 4: {a:.4f}; >= 12: {b:.4f}; diferenca = {a - b:.4f}")
    cs, bacia, total = p973_kaprekar_hex()
    print(f"P973 Kaprekar em base 16 (4 digitos, {total} numeros): {len(cs)} ciclos; " + "; ".join(
        f"{[format(x, 'X') for x in c]}: {bacia[c] / total:.3f}" for c in sorted(bacia, key=lambda c: -bacia[c]))
        + f"; base 10: {p973_kaprekar_hex(4, 10)[0]}")
    uni = p974_previsoes_sem_largura()
    print("P974 previsoes unilaterais (sem faixa) por parte: " + "; ".join(f"{k}: {u} de {p} {ls}" for k, (p, u, ls) in uni.items()))
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P999, testes=TESTES_P999)
    print(f"P999 minha taxa de erro ({ERROS_P999}/{TESTES_P999}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_52():
    print("--- Parte 52 (0x34: o metodo ou a serie) ---")
    s0, (A, B, t1, t2, sse), aic2, limiar = p1001_duas_memorias_em_log()
    print(f"P1001 duas exponenciais em log (Gauss-Newton, exp/log proprios): sse da grade = {s0:.4f} -> {sse:.4f}; A = {A:.4f}, B = {B:.4f}, "
          f"t1 = {t1:.3f}, t2 = {t2:.3e}; AIC = {aic2:.2f} (potencia: -79.37; limiar de sse = {limiar:.4f})")
    top, g, frac, n, dez = p1002_funis_pt()
    print(f"P1002 funis do portugues: a mais escolhida = {top} ({g}); as 10 mais = {frac:.4f} de {n} palavras; {dez}")
    f, m, nao = p1003_inverte_e_soma()
    f10, m10, n10 = p1003_inverte_e_soma(9999, 10)
    print(f"P1003 inverte e soma, base 16 (1..4095): chegam {f:.4f}, em {m:.3f} passos; nao chegam {len(nao)} (o primeiro: {hex(nao[0])}); "
          f"base 10 (1..9999): nao chegam {len(n10)} (o primeiro: {n10[0]})")
    uni = p974_previsoes_sem_largura(range(52, 53))
    print(f"P974 previsoes unilaterais da Parte 52: {uni}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1029, testes=TESTES_P1029)
    print(f"P1029 minha taxa de erro ({ERROS_P1029}/{TESTES_P1029}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_53():
    print("--- Parte 53 (0x35: preditiva comigo mesma) ---")
    h = p1031_historico_de_mim(range(31, 54))
    pred = p1032_preditor_de_mim({n: v for n, v in h.items() if n <= 52})
    if 53 in h:
        for medida, (m, w, u) in pred.items():
            v = h[53][medida]
            print(f"P1032 {medida}: medido = {v}; estatistico [{m - w:.4f}; {m + w:.4f}] {'dentro' if v is not None and abs(v - m) <= w else 'fora'}; "
                  f"ingenuo = {u}")
    rho, n, faixas = p1033_definicao_e_profundidade()
    print(f"P1033 Spearman(palavras da definicao, profundidade) = {rho:.4f} em {n} substantivos; palavras por faixa: "
          + ", ".join(f"{k}: {v:.2f}" for k, v in faixas.items()))
    ac, total, inicio, chi2 = p1034_pi_hexadecimal()
    print(f"P1034 pi em hexadecimal: BBP = exato em {ac} de {total} digitos; 3,{inicio}...; chi2 (15 g.l.) = {chi2:.3f}")
    print(f"P974 previsoes unilaterais da Parte 53: {p974_previsoes_sem_largura(range(53, 54))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1059, testes=TESTES_P1059)
    print(f"P1059 minha taxa de erro ({ERROS_P1059}/{TESTES_P1059}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_54():
    print("--- Parte 54 (0x36: a sorte das rodadas) ---")
    chances, dif = p1061_exatidao_ou_sorte()
    print(f"P1061 rodadas com chance de sorte < 0,5 (modelo de sorteios independentes): {sum(v < 0.5 for v in chances.values())}; "
          f"menor: {min(chances, key=chances.get)} = {min(chances.values()):.2e}; diferencas reais (exp dist, exp dif, log dist, log dif): "
          + "; ".join(f"{k} {v}" for k, v in dif.items()))
    frac, media, n = p1062_folhas()
    print(f"P1062 folhas: {frac:.4f} de {n} substantivos; filhos por no interno = {media:.3f} (conta: {frac / (1 - frac) + 1:.3f})")
    print(f"P1063 autodescritivos: base 16 {p1063_autodescritivos(16)}; base 10 {p1063_autodescritivos(10)}; base 7 {p1063_autodescritivos(7)}; "
          f"base 4 {p1063_autodescritivos(4)}")
    print(f"P974 previsoes unilaterais da Parte 54: {p974_previsoes_sem_largura(range(54, 55))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1089, testes=TESTES_P1089)
    print(f"P1089 minha taxa de erro ({ERROS_P1089}/{TESTES_P1089}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_55():
    print("--- Parte 55 (0x37: o ulp que chega) ---")
    for r, (n, m, t) in p1091_o_ulp_que_chega().items():
        print(f"P1091 rodada{r}: {n} numeros; maior mudanca relativa com um ulp = {m:.3e}; texto {'MUDOU' if t else 'igual'}")
    total, sem = p1092_pnn_sem_teste()
    print(f"P1092 funcoes pNN desde a P821 sem teste: {len(sem)} de {total}: {sem}")
    frac, diretas, n = p1093_sem_o_funil()
    print(f"P1093 sem o funil 'act': {frac:.4f} das {n} palavras mudam de destino ({diretas} iam direto a 'act')")
    a, conta = p1094_ulp_em_hexadecimal()
    b, _ = p1094_ulp_mantissa_uniforme()
    print(f"P1094 digitos hexadecimais que um ulp muda: 1 + random() = {a:.4f} (conta posterior {1 + conta / 32:.4f}); mantissa uniforme = {b:.4f} "
          f"(conta {conta:.4f})")
    print(f"P974 previsoes unilaterais da Parte 55: {p974_previsoes_sem_largura(range(55, 56))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1119, testes=TESTES_P1119)
    print(f"P1119 minha taxa de erro ({ERROS_P1119}/{TESTES_P1119}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_56():
    print("--- Parte 56 (0x38: os empates) ---")
    emp = p1121_empates()
    print("P1121 empates exatos nas escolhas impressas: " + "; ".join(f"rodada{r} = {e}" for r, e in sorted(emp.items()))
          + f"; rodadas com empate: {sum(1 for e in emp.values() if e > 0)} de {len(emp)}")
    frac, n, maior = p1122_sinonimos_perfeitos()
    print(f"P1122 sinonimos perfeitos: {frac:.4f} das {n} palavras tem gemeo; o maior grupo ({len(maior)}): {maior}")
    for ate in (4095, 65535):
        f, k, conta = p1123_mesma_soma(ate)
        print(f"P1123 mesma soma de digitos em base 16 e 10 (1..{ate}): {k} = {f:.4f} (conta continua {conta:.4f}; com a rede de multiplos de 3: x3)")
    total, sem = p1092_pnn_sem_teste(1091, 1150)
    print(f"P1092 pNN novas (P1091-P1150) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 56: {p974_previsoes_sem_largura(range(56, 57))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1149, testes=TESTES_P1149)
    print(f"P1149 minha taxa de erro ({ERROS_P1149}/{TESTES_P1149}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_57():
    print("--- Parte 57 (0x39: as restricoes) ---")
    trocas, acentuados = p1151_alfabeto_portugues()
    print(f"P1151 4-gramas reordenados pelo portugues: {len(trocas)} pares mudam; {acentuados} dos 13 tem acento")
    pal, conta, conta_pontas, n, ex = p1152_palindromos()
    print(f"P1152 palindromos: {pal} de {n} palavras; conta de letras independentes {conta:.1f}; com as pontas reais {conta_pontas:.1f}; {ex}")
    k, conta2, primeiros = p1153_duplos_palindromos()
    print(f"P1153 palindromos em base 10 e 16 abaixo de 10^6: {k} (conta {conta2:.1f}); {primeiros}")
    total, sem = p1092_pnn_sem_teste(1151, 1180)
    print(f"P1092 pNN novas (P1151-P1180) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 57: {p974_previsoes_sem_largura(range(57, 58))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1179, testes=TESTES_P1179)
    print(f"P1179 minha taxa de erro ({ERROS_P1179}/{TESTES_P1179}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_58():
    print("--- Parte 58 (0x3A: a primeira diferenca) ---")
    pos, pares, inv, acento = p1181_primeira_diferenca()
    print(f"P1181 lemas portugueses: primeira diferenca media na posicao {pos:.4f} ({pares} pares); invertidos pela ordem portuguesa: {inv} "
          f"({inv / acento:.3f} por palavra acentuada, {acento} acentuadas)")
    razao, n, maior = p1182_portugues_contra_ingles()
    print(f"P1182 tamanho pt/en: razao media {razao:.4f} em {n} pares; o portugues e mais longo em {maior:.4f} deles")
    d2, d3 = p1183_primeiro_digito_hex(2), p1183_primeiro_digito_hex(3)
    print(f"P1183 primeiro digito hexadecimal (n = 1..10000): 2^n {d2}; 3^n {d3} (digito 1: {d3[1] / 10000:.4f}; Benford 0,25)")
    total, sem = p1092_pnn_sem_teste(1181, 1210)
    print(f"P1092 pNN novas (P1181-P1210) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 58: {p974_previsoes_sem_largura(range(58, 59))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1209, testes=TESTES_P1209)
    print(f"P1209 minha taxa de erro ({ERROS_P1209}/{TESTES_P1209}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_59():
    print("--- Parte 59 (0x3B: o nome e a coisa) ---")
    n, k, ex = p1211_nome_e_palavra()
    print(f"P1211 lemas portugueses com maiuscula: {n}; com irma minuscula: {k} ({k / n:.4f}); {ex}")
    frac, total, top = p1212_palavras_que_nao_definem()
    print(f"P1212 palavras que nunca definem outra: {frac:.4f} de {total}; as que mais definem: {top}")
    m, q, med = p1213_persistencia_hex()
    print(f"P1213 persistencia multiplicativa em base 16 (16..16^5-1): maior = {m} (primeiro em {hex(q)}); media = {med:.4f}")
    total, sem = p1092_pnn_sem_teste(1211, 1240)
    print(f"P1092 pNN novas (P1211-P1240) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 59: {p974_previsoes_sem_largura(range(59, 60))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1239, testes=TESTES_P1239)
    print(f"P1239 minha taxa de erro ({ERROS_P1239}/{TESTES_P1239}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_60():
    print("--- Parte 60 (0x3C: o placar que se conta) ---")
    tot, linhas = p1241_placar_por_voz()
    for v, (a, b, c, e) in tot.items():
        print(f"P1241 {v}: estrita {b} em {a}; generosa {e} em {c} (a mao: IA-Python 23 em 36, IA-Java 21 em 36)")
    frac, n, por, ex = p1242_definicao_propria()
    print(f"P1242 definicoes que usam um dos proprios lemas: {frac:.4f} de {n} sinsets; por classe {({c: round(f, 4) for c, f in por.items()})}; {ex[:3]}")
    nar = p1243_narcisistas_hex()
    print(f"P1243 narcisistas em base 16 (1 a 8 digitos): {len(nar)}; de 2 a 8 digitos: {[hex(x) for x in nar if x >= 16]}")
    print(f"P1248 por comprimento (base 16, ate 9 digitos): {p1248_por_comprimento(p1243_narcisistas_hex(9))}")
    print(f"P1247 interruptores d^(k-1) = 16^p: {({k: p1247_interruptores(k) for k in range(3, 10)})}")
    print(f"P1249 fator de congruencia em base 16, k = 1..9: {[p1249_fator_de_congruencia(k) for k in range(1, 10)]}")
    linhas, l0, l1 = p1251_conta_contra_medida()
    for base, k, m, e0, e1 in linhas:
        print(f"P1251 base {base:2d}, k = {k:2d}: medido {m:2d}; conta sem o fator {e0:.3f}; com o fator {e1:.3f}")
    print(f"P1251 log-verossimilhanca de Poisson: sem o fator {l0:.2f}; com o fator {l1:.2f}; diferenca {l1 - l0:.2f} nats")
    print(f"P1251 total (k >= 2, 5 bases): medido {sum(x[2] for x in linhas)}; conta sem o fator {sum(x[3] for x in linhas):.1f}; "
          f"com o fator {sum(x[4] for x in linhas):.1f}")
    total, sem = p1092_pnn_sem_teste(1241, 1270)
    print(f"P1092 pNN novas (P1241-P1270) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 60: {p974_previsoes_sem_largura(range(60, 61))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1269, testes=TESTES_P1269)
    print(f"P1269 minha taxa de erro ({ERROS_P1269}/{TESTES_P1269}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_61():
    print("--- Parte 61 (0x3D: o dobro) ---")
    n, nums = p1271_rodadas_verificadas()
    print(f"P1271 rodadas conferidas pelo verificar.py: {n} ({nums[0]} a {nums[-1]})")
    neg, na, pre, ex = p1272_adjetivos_negativos()
    print(f"P1272 adjetivos definidos pela negacao: {neg:.4f} de {na}; com prefixo negativo entre eles: {pre:.4f}; {ex[:3]}")
    for ate, base in ((10 ** 6, 10), (16 ** 5, 16)):
        k, conta = p1273_niven(ate, base)
        print(f"P1273 Niven base {base} ate {ate}: {k}; conta de De Koninck-Doyon-Katai {conta:.1f}; razao {k / conta:.4f}")
    celulas, grupos = p1274_narcisistas_14_bases()
    for nome, m, e in grupos:
        print(f"P1274 {nome}: medido {m}; conta {e:.3f}; razao {m / e:.4f}")
    for b in range(3, 17):
        m = sum(c[0] for (bb, k), c in celulas if bb == b and not c[4])
        e = 0.0
        for (bb, k), c in celulas:
            if bb == b and not c[4]:
                e += c[5]
        print(f"P1274 base {b:2d} sem interruptor: medido {m:2d}; conta {e:.3f}; razao {m / e:.3f}")
    sol, fam, conta, pares = p1278_familias_narcisistas()
    print(f"P1278 sem outro interruptor: solucoes {sol}; pares (n terminado em 0, n + 1) {pares}; familias {fam}; conta {conta:.3f}; "
          f"familias/conta {fam / conta:.4f}")
    total, sem = p1092_pnn_sem_teste(1271, 1300)
    print(f"P1092 pNN novas (P1271-P1300) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 61: {p974_previsoes_sem_largura(range(61, 62))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1299, testes=TESTES_P1299)
    print(f"P1299 minha taxa de erro ({ERROS_P1299}/{TESTES_P1299}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_62():
    print("--- Parte 62 (0x3E: o ultimo digito) ---")
    linhas, rho = p1301_ultimo_digito()
    for b, exc, raz, m, e, ec in linhas:
        print(f"P1301 base {b:2d}: excesso do ultimo digito {exc:.4f}; medido {m:2d}; conta {e:.3f} (razao {raz:.3f}); corrigida {ec:.3f} (razao {m / ec:.3f})")
    m = sum(x[3] for x in linhas)
    e = ec = 0.0
    for x in linhas:
        e += x[4]
        ec += x[5]
    print(f"P1301 Spearman excesso x razao = {rho:.4f}; total: medido {m}; conta {e:.3f} (razao {m / e:.4f}); corrigida {ec:.3f} (razao {m / ec:.4f})")
    frac, n, por, ex = p1302_iguais_nas_duas_linguas()
    print(f"P1302 sinsets com palavra igual em portugues e ingles: {frac:.4f} de {n}; por classe {({c: round(f, 6) for c, f in por.items()})}; "
          f"substantivos/verbos = {por['n'] / por['v']:.1f}; {ex}")
    print(f"P1308 chance ao acaso (14 bases, 20000 permutacoes): rho >= 0,3 em {p1308_chance_de_spearman(0.3):.4f}; rho >= {rho:.4f} em "
          f"{p1308_chance_de_spearman(rho):.4f}")
    t, term = p1307_terminacoes_iguais()
    print(f"P1307 adjetivos iguais: {t}; terminacoes {term[:8]}; fracao em -al = {dict(term)['al'] / t:.4f}")
    for ate, base in ((10 ** 6, 10), (16 ** 5, 16)):
        dens, k, prim = p1303_autonumeros(ate, base)
        print(f"P1303 autonumeros base {base} ate {ate}: {k} (densidade {dens:.4f}); os primeiros {prim}")
    total, sem = p1092_pnn_sem_teste(1301, 1330)
    print(f"P1092 pNN novas (P1301-P1330) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 62: {p974_previsoes_sem_largura(range(62, 63))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1329, testes=TESTES_P1329)
    print(f"P1329 minha taxa de erro ({ERROS_P1329}/{TESTES_P1329}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_63():
    print("--- Parte 63 (0x3F: o peso do mecanismo) ---")
    linhas, com, longe = p1331_fator_efetivo()
    for b, m, cg, cf in linhas:
        print(f"P1331 base {b:2d}: medido {m:2d}; conta com g {cg:.3f} (razao {m / cg:.3f}); com F {cf:.3f} (razao {m / cf:.3f})")
    tm = sum(x[1] for x in linhas)
    tg = tf = 0.0
    for x in linhas:
        tg += x[2]
        tf += x[3]
    print(f"P1331 total: medido {tm}; razao com g {tm / tg:.4f}; com F {tm / tf:.4f}; celulas com F a mais de 10% de g: {longe} de {com} ({longe / com:.4f})")
    med, mais, n, media = p1332_glosa_pt_e_en()
    print(f"P1332 glosas portuguesas ({n}): razao de palavras PT/EN mediana {med:.4f}, media {media:.4f}; portuguesa mais longa em {mais:.4f}")
    for ate, base in ((16 ** 5, 16), (12 ** 5, 12), (10 ** 7, 10)):
        k, conta, por = p1333_primos_palindromos(ate, base)
        print(f"P1333 primos palindromos base {base} ate {ate}: {k}; conta {conta:.1f} (P1337 sozinha: {p1337_conta_palindromos(ate, base):.1f}); "
              f"erro {(k - conta) / k:+.4f}; por comprimento {por}")
    cauda, desvio, ingenuo, npal, mb8 = p1338_contas_da_parte63()
    print(f"P1338 Poisson(media {mb8:.3f}) >= 13: {cauda:.2e}; desvio relativo da contagem sob a conta (base 16): {desvio:.4f}; "
          f"ingenuo pi(16^5)/16^5 x {npal} palindromos = {ingenuo:.1f}")
    total, sem = p1092_pnn_sem_teste(1331, 1360)
    print(f"P1092 pNN novas (P1331-P1360) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 63: {p974_previsoes_sem_largura(range(63, 64))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1359, testes=TESTES_P1359)
    print(f"P1359 minha taxa de erro ({ERROS_P1359}/{TESTES_P1359}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_64():
    print("--- Parte 64 (0x40: o fator do final) ---")
    linhas = p1361_fator_do_final()
    perto, absrel, soma = 0, 0.0, 0.0
    for b, m, a, bb, sg in linhas:
        perto += abs(m - bb) < 2 * sg
        absrel += abs(m - bb) / bb
        soma += m - bb
        print(f"P1361 base {b:2d}: medido {m:3d}; conta A {a:.2f}; conta B {bb:.2f} (razao {m / bb:.4f}); sigma {sg:.2f}; z {(m - bb) / sg:+.2f}")
    print(f"P1361 bases a menos de 2 sigma: {perto} de {len(linhas)}; media |medido - B|/B = {absrel / len(linhas):.4f}; soma medido - B = {soma:.2f}")
    novas = p1367_bases_novas_palindromos()
    for b, m, bb, sg, z in novas:
        print(f"P1367 base {b}: medido {m}; conta B {bb:.2f}; sigma {sg:.2f}; z {z:+.2f}")
    print(f"P1367 fora de 2 sigma: {sum(1 for x in novas if abs(x[4]) >= 2)} de {len(novas)}; media z {sum(x[4] for x in novas) / len(novas):+.4f}; "
          f"z negativos: {sum(1 for x in novas if x[4] < 0)}")
    rho, n, mono, por = p1362_brevidade_e_sentidos()
    print(f"P1362 Spearman comprimento x sentidos: {rho:.4f} ({n} lemas; monossemicos {mono:.4f}); sentidos medios por comprimento "
          f"{({L: round(v, 3) for L, v in por.items()})}")
    k, conta, ns = p1363_quadrados_palindromos()
    k10, conta10, _ = p1363_quadrados_palindromos(10 ** 4, 10)
    print(f"P1363 quadrados palindromos base 16 (n < 16^4): {k}; conta {conta:.2f}; razao {k / conta:.3f}; n = {[hex(x) for x in ns]}")
    print(f"P1363 calibracao base 10 (n < 10^4): {k10}; conta {conta10:.2f}; razao {k10 / conta10:.3f}")
    total, sem = p1092_pnn_sem_teste(1361, 1390)
    print(f"P1092 pNN novas (P1361-P1390) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 64: {p974_previsoes_sem_largura(range(64, 65))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1389, testes=TESTES_P1389)
    print(f"P1389 minha taxa de erro ({ERROS_P1389}/{TESTES_P1389}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_65():
    print("--- Parte 65 (0x41: o que nao e divisor) ---")
    linhas = p1391_o_que_nao_e_divisor()
    soma = 0.0
    zs = def5 = deft = 0.0
    for b, N, corr, m, C, sg, m5, c5 in linhas:
        soma += abs(corr - 1.0)
        if b >= 17:
            zs += (m - C) / sg
            def5 += m5 - c5
            deft += m - C
        print(f"P1391 base {b:2d}: N {N:4d}; correcao {corr:.4f}; medido {m:3d}; conta C {C:.2f}; sigma {sg:.2f}; z {(m - C) / sg:+.2f}; "
              f"comprimento 5: {m5} contra {c5:.2f}")
    print(f"P1391 media |correcao - 1| = {soma / len(linhas):.4f}; media z (17-22) = {zs / 6:+.4f}; fracao do deficit em L = 5: {def5 / deft:.4f}; "
          f"soma medido - C = {sum(x[3] - x[4] for x in linhas):.2f}")
    novas = p1397_correcao_b2_mais_1()
    for b, det, cr, m, cc, sg, z in novas:
        print(f"P1397 base {b}: primos r {[(r, round(v, 2)) for r, v in det]}; correcao_r {cr:.4f}; medido {m}; conta {cc:.2f}; z {z:+.2f}")
    print(f"P1397 media z (17-22) com a correcao_r: {sum(x[6] for x in novas) / len(novas):+.4f}; sinais (correcao_r - 1): "
          f"{[(x[0], '-' if x[2] < 1 else '+') for x in novas]}")
    rho, n, por = p1392_profundidade_e_definicao()
    rho_v, n_v, _ = p1392_profundidade_e_definicao(classe="v")
    print(f"P1392 Spearman profundidade x palavras da definicao: substantivos {rho:.4f} ({n}); verbos (calibracao) {rho_v:.4f} ({n_v}); "
          f"media por profundidade {({k: round(v, 2) for k, v in por.items()})}")
    for de, ate in ((3, 10 ** 4), (10 ** 4, 10 ** 5)):
        m16, m2, mx, np_ = p1393_periodo_hex(de, ate)
        print(f"P1393 primos em [{de}, {ate}) ({np_}): media ord16/(p-1) {m16:.4f}; ord2/(p-1) {m2:.4f}; razao {m16 / m2:.4f}; periodo maximo {mx:.4f}")
    total, sem = p1092_pnn_sem_teste(1391, 1420)
    print(f"P1092 pNN novas (P1391-P1420) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 65: {p974_previsoes_sem_largura(range(65, 66))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1419, testes=TESTES_P1419)
    print(f"P1419 minha taxa de erro ({ERROS_P1419}/{TESTES_P1419}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_66():
    print("--- Parte 66 (0x42: o endereco da falta) ---")
    quis, k, bases = p1421_endereco_da_falta()
    for nome, (q, gl) in quis.items():
        print(f"P1421 base 21, classes por {nome}: qui2 {q:.3f} com {gl} graus de liberdade (qui2/gl {q / gl:.4f}); fator global k = {k:.4f}")
    for b, m, C, sg, z in bases:
        print(f"P1421 base {b}: medido {m}; conta C {C:.2f}; sigma {sg:.2f}; z {z:+.2f}")
    print(f"P1421 bases 23-28: media z {sum(x[4] for x in bases) / len(bases):+.4f}; negativos {sum(1 for x in bases if x[4] < 0)}")
    novas = p1427_bases_29_a_34()
    for b, m, C, sg, z in novas:
        print(f"P1427 base {b}: medido {m}; conta C {C:.2f}; sigma {sg:.2f}; z {z:+.2f}")
    print(f"P1427 bases 29-34: media z {sum(x[4] for x in novas) / len(novas):+.4f}")
    r = p1422_sinonimos_por_classe()
    print(f"P1422 sinsets por classe (tamanho medio, fracao de um lema, sinsets): {({c: (round(a, 4), round(u, 4), n) for c, (a, u, n) in r.items()})}; "
          f"verbos/substantivos = {r['v'][0] / r['n'][0]:.4f}")
    for ate in (10 ** 4, 10 ** 5, 16 ** 5):
        frac, conta = p1423_mesma_soma_10_16(ate)
        print(f"P1423 s10 = s16 para n < {ate}: {frac:.5f}; conta (3 x independencia) {conta:.5f}; razao {frac / conta:.4f}")
    total, sem = p1092_pnn_sem_teste(1421, 1450)
    print(f"P1092 pNN novas (P1421-P1450) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 66: {p974_previsoes_sem_largura(range(66, 67))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1449, testes=TESTES_P1449)
    print(f"P1449 minha taxa de erro ({ERROS_P1449}/{TESTES_P1449}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_67():
    print("--- Parte 67 (0x43: prever o previsto) ---")
    prev = p1452_minhas_previsoes(range(53, 67))
    r = p1453_engenharia_das_previsoes(prev)
    print(f"P1452 previsoes do mundo lidas (Partes 53-66): {r['previsoes']}; com faixa numerica: {r['com_faixa']}; por parte {r['por_parte']}")
    print(f"P1453 acerto {r['acerto']:.4f} (com faixa {r['acerto_com_faixa']:.4f}; sem faixa {r['acerto_sem_faixa']:.4f}); w mediana {r['w_mediana']:.4f} "
          f"(quartis {r['w_q25']:.4f}, {r['w_q75']:.4f}); por terco de w (w mediano, acerto): {[(round(a, 4), round(b, 4)) for a, b in r['por_terco']]}; "
          f"erro do preditor de w: mediana das outras {r['erro_loo']:.4f}, ingenuo {r['erro_ingenuo']:.4f}")
    m, mediana, ws = p1459_previsoes_sobre_previsoes(67, range(53, 67))
    print(f"P1459 previsoes sobre as minhas previsoes da Parte 67: m1 (mediana de w) {m['m1']:.4f}; m2 (previsoes) {m['m2']}; m3 (acerto) {m['m3']:.4f}; "
          f"m4 (perto de 1/3) {m['m4']:.4f}; m5 (erro da mediana historica {mediana:.4f}) {m['m5']:.4f}; ws {[round(w, 4) for w in ws]}")
    todos, (beta, alfa, ep), (mn, dpn), (mt, dpt) = p1451_tendencia_ou_dispersao()
    print(f"P1451 bases 35-40: z {[(b, round(z, 3)) for b, _, z in todos if b >= 35]}; media {mn:+.4f}; dp {dpn:.4f}")
    print(f"P1451 reta de z contra b (5-40): inclinacao {beta:.5f} (ep {ep:.5f}; t {beta / ep:.3f}); intercepto {alfa:.4f}; todas: media {mt:+.4f}, dp {dpt:.4f}")
    por, ex = p1454_heranca_multipla()
    print(f"P1454 sinsets com 2+ hiperonimos: {({c: (round(f, 5), n) for c, (f, n) in por.items()})}; exemplos {ex}")
    for b, k in ((12, 6), (10, 6), (16, 6)):
        ach, conta = p1455_automorficos(b, k)
        print(f"P1455 automorficos base {b} ate {b}^{k}: {len(ach)} (conta {conta:.2f}); {ach}")
    total, sem = p1092_pnn_sem_teste(1451, 1480)
    print(f"P1092 pNN novas (P1451-P1480) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 67: {p974_previsoes_sem_largura(range(67, 68))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1479, testes=TESTES_P1479)
    print(f"P1479 minha taxa de erro ({ERROS_P1479}/{TESTES_P1479}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_68():
    print("--- Parte 68 (0x44: o tipo da quantidade) ---")
    prev = p1481_minhas_previsoes_v2(range(53, 68))
    print(f"P1481 previsoes do mundo (Partes 53-67): {len(prev)}; com faixa: {sum(1 for x in prev if x[2] is not None)}")
    for tipo, (n, ac, med, est, lar) in p1482_engenharia_por_tipo(prev).items():
        extra = f"; w mediana {med:.4f}; acerto das estreitas {est:.4f}, das largas {lar:.4f}" if med is not None else ""
        print(f"P1482 tipo {tipo}: {n} previsoes; acerto {ac:.4f}{extra}")
    m, ws = p1499_previsoes_sobre_previsoes_v2(68)
    print(f"P1499 previsoes sobre as minhas previsoes da Parte 68: {m}; ws (sem as do zero) {[round(w, 4) for w in ws]}")
    linhas, antes, depois, maior = p1491_densidade_da_conta()
    print(f"P1491 R_b = pi(b^5)/(Li(b^5) - Li(2)): {[(b, round(R, 5)) for b, _, R in linhas if b in (5, 10, 20, 30, 40)]}; maior |R - 1| (10-40) {maior:.5f}")
    print(f"P1491 inclinacao de z: antes {antes:.5f}; com a conta corrigida {depois:.5f}; mudanca {abs(depois - antes):.5f}")
    for c_, (f, n) in p1492_folhas().items():
        print(f"P1492 folhas na classe {c_}: {f:.4f} de {n}")
    for ate, b1, b2 in ((16 ** 4, 16, 10), (8 ** 5, 8, 10)):
        ach, conta = p1493_palindromos_duplos(ate, b1, b2)
        print(f"P1493 palindromos nas bases {b1} e {b2} ate {ate}: {len(ach)}; conta {conta:.3f}; razao {len(ach) / conta:.4f}; {ach}")
    total, sem = p1092_pnn_sem_teste(1481, 1510)
    print(f"P1092 pNN novas (P1481-P1510) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 68: {p974_previsoes_sem_largura(range(68, 69))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1509, testes=TESTES_P1509)
    print(f"P1509 minha taxa de erro ({ERROS_P1509}/{TESTES_P1509}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_69():
    print("--- Parte 69 (0x45: a forma de GPT) ---")
    for lingua in ("en", "pt"):
        treino, teste = p1511_corpus_de_glosas(lingua)
        lim = 400 * 24 + 1
        ng = {k: p1512_ngrama_bits(treino, teste, k, lim) for k in (1, 2, 3, 4, 5)}
        print(f"P1511 corpus {lingua}: treino {len(treino)} caracteres, teste {len(teste)}")
        print(f"P1512 n-grama {lingua} (bits por caractere, ordens 1-5): {({k: round(v, 4) for k, v in ng.items()})}")
        b, n, perda, g = p1513_gpt_bits(treino, teste)
        print(f"P1513 GPT {lingua} (T 24, d 24, h 48, 8000 passos): {b:.4f} bits por caractere; {n} parametros; perda final {perda:.4f} bits; "
              f"GPT - trigrama = {b - ng[3]:+.4f}; gera: {g.gerar('a domestic ' if lingua == 'en' else 'o animal ', 50)!r}")
    pi = p1514_pi_hex_digitos(10000)
    print(f"P1514 pi em hexadecimal: 3,{pi[:16]}...")
    print(f"P1515 bits por digito de pi (n-grama, 90% treino, 10% teste): {({k: round(p1515_bits_hex(pi, k), 4) for k in (1, 2, 3)})}")
    saida, acertos, bits = p1516_gpt_decide()
    print(f"P1516 rodada 43: o GPT pequeno acerta o proximo caractere em {acertos} de {len(saida)} posicoes; {bits:.4f} bits por caractere; "
          f"decisoes {[(ctx, arg) for _, ctx, arg, _, _ in saida[:6]]}")
    total, sem = p1092_pnn_sem_teste(1511, 1540)
    print(f"P1092 pNN novas (P1511-P1540) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 69: {p974_previsoes_sem_largura(range(69, 70))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1539, testes=TESTES_P1539)
    print(f"P1539 minha taxa de erro ({ERROS_P1539}/{TESTES_P1539}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_70():
    print("--- Parte 70 (0x46: algebra e geometria) ---")
    for classe, q in (("v", 300), ("n", 300)):
        mx, med, frac, nos, dist = p1544_delta_de_gromov(classe, q)
        print(f"P1544 delta de Gromov ({classe}, {q} quadruplos, semente 70): maximo {mx}; medio {med:.4f}; fracao com delta > 0 {frac:.4f}; "
              f"{nos} nos na componente; distancia media {dist:.2f}")
    import random
    r = random.Random(1570)
    aleat = "".join("0123456789abcdef"[r.randrange(16)] for _ in range(10000))
    for nome, texto in (("aleatorio (semente 1570)", aleat), ("pi", p1514_pi_hex_digitos(10000))):
        f, teo, jan = p1545_bases_gf2(texto)
        print(f"P1545 janelas de 4 digitos que formam base de GF(2)^4, {nome}: {f:.5f} de {jan}; teoria |GL(4,2)|/16^4 = {teo:.5f}")
    p, sd, z1, z2 = p1550_contas_da_parte70()
    print(f"P1550 desvio binomial {sd:.5f}; pi fica a {z1:+.3f} desvios (simples) e {z2:+.3f} (dobro, janelas sobrepostas)")
    ajustes, dif, pontos = p1549_lei_de_escala()
    for d_, (A, alfa, ne) in ajustes.items():
        print(f"P1549 rodada 44, d = {d_}: pontos {[(n, round(b, 4)) for n, b in pontos[d_]]}; A {A:.4f}; alfa {alfa:.5f}; n* (trigrama 2,768) {ne:.4g}")
    print(f"P1549 bits(d = 48) - bits(d = 24) em 8000 passos: {dif:+.4f}")
    pts, n, g = p1541_escala_gpt("en", d=24)
    vv, vc, cc, frac = p1543_geometria_dos_embeddings(g)
    print(f"P1541 escala refeita (d = 24, {n} pesos): {[(m, round(b, 4)) for m, b in pts]}")
    print(f"P1543 geometria dos embeddings: cos vogais {vv:.4f}; vogal-consoante {vc:.4f}; consoantes {cc:.4f}; diferenca {vv - vc:.4f}; 1a componente {frac:.4f}")
    pts48, n48, _ = p1541_escala_gpt("en", d=48, marcos=(4000, 8000), lr=0.0025)
    print(f"P1541 d = 48 com lr 0,0025 ({n48} pesos): {[(m, round(b, 4)) for m, b in pts48]}")
    total, sem = p1092_pnn_sem_teste(1541, 1570)
    print(f"P1092 pNN novas (P1541-P1570) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 70: {p974_previsoes_sem_largura(range(70, 71))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1569, testes=TESTES_P1569)
    print(f"P1569 minha taxa de erro ({ERROS_P1569}/{TESTES_P1569}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_71():
    print("--- Parte 71 (0x47: os autovalores da atencao) ---")
    pr, frac, lam = p1578_autovalores_da_atencao()
    print(f"P1578 rodada 45: autovalores de M^T M (M = W_Q W_K^T) {[round(x, 4) for x in lam]}; PR {pr:.4f}; fracao do maior {frac:.4f}")
    import random
    r = random.Random(1)
    print(f"P1572 matriz gaussiana 16x16 ao acaso: PR {p1572_participacao([[r.gauss(0, 1) for _ in range(16)] for _ in range(16)])[0]:.4f} (teoria ~ d/2 = 8)")
    print(f"P1571 Jacobi em [[2, 1], [1, 2]]: {p1571_autovalores_jacobi([[2.0, 1.0], [1.0, 2.0]])} (exatos: 3 e 1)")
    for classe in ("v", "n"):
        f, por, rmax = p1573_crescimento_da_taxonomia(classe)
        print(f"P1573 classe {classe}: fator por nivel (1-8) {f:.4f}; profundidade com mais sinsets {rmax}; N(r) {por}")
    for g in (11, 13, 15):
        irr, gauss, gem, conta = p1574_irredutiveis_gf2(g, 6)
        print(f"P1574 grau {g}: irredutiveis {irr} (Gauss {gauss}); gemeos (f, f + x + x^2) {gem} contra a conta {conta:.1f} (razao {gem / conta:.3f}); "
              f"gemeos por um bit (f, f + x): {p1574_irredutiveis_gf2(g, 2)[2]}")
    for g in (11, 13, 15, 17, 19):
        serie, conta = p1579_serie_singular_gf2(g)
        gem = p1574_irredutiveis_gf2(g, 6)[2]
        print(f"P1579 grau {g}: serie singular S = {serie:.4f}; conta {conta:.1f}; medido {gem}; razao {gem / conta:.3f}; z de Poisson {(gem - conta) / conta ** 0.5:+.2f}")
    total, sem = p1092_pnn_sem_teste(1571, 1600)
    print(f"P1092 pNN novas (P1571-P1600) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 71: {p974_previsoes_sem_largura(range(71, 72))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1599, testes=TESTES_P1599)
    print(f"P1599 minha taxa de erro ({ERROS_P1599}/{TESTES_P1599}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_72():
    print("--- Parte 72 (0x48: o que esta disfuncional) ---")
    for k, v in p1601_auditoria_do_repositorio(71).items():
        print(f"P1601 auditoria, {k}: {len(v)} {v[:10]}")
    tr, te = p1511_corpus_de_glosas("en")
    h, n, red, red8 = p1602_entropia_de_unigrama(tr + "|" + te)
    print(f"P1602 glosas inglesas: H = {h:.4f} bits/simbolo; {n} simbolos; redundancia contra log2({n}) = {red:.4f}; contra 8 bits = {red8:.4f} "
          f"(o texto recebido: 1 - 4,11/8 = {1 - 4.11 / 8:.5f})")
    print(f"P1603 ciclos de glosas (A na glosa de B, B na glosa de A): {p1603_ciclos_de_glosas()}")
    ms, mr, z = p1604_hash_como_peso()
    print(f"P1604 hash como peso: |h(a) - h(b)| sinonimos {ms:.4f}, sorteados {mr:.4f} (teoria 1/3); z = {z:+.3f}")
    for nome, verif, asserts, decl in p1608_auditoria_estatica():
        print(f"P1608 texto recebido, {nome}: {verif} verificacoes ({asserts} asserts) contra {decl} declaradas")
    n, ok_lin, ok_ing, passagens, checagens, dec, R = p1612_animais_por_horn()
    print(f"P1612 fecho de animal: {n} sinsets; linear = BFS {ok_lin}; ingenuo = BFS {ok_ing}; {passagens} passagens, {checagens} checagens contra {dec} decrementos "
          f"(razao {checagens / dec:.1f}); {R} regras; limite do texto (F+1)RP = {(n + 1) * R * R:.3e}; passagens x P = {passagens * R}")
    print(f"P1615 imports sem uso por bloco do texto recebido: {p1615_imports_sem_uso()}")
    print(f"P1613 fecho de person: {p1613_fecho_horn('person')}")
    for f, n, ctl, dec, cadeia in p1614_rodada46():
        print(f"P1614 rodada 46, fato {f}: derivados {n}, controle {ctl}, decrementos {dec}, prova de {len(cadeia)} regras")
    total, sem = p1092_pnn_sem_teste(1601, 1630)
    print(f"P1092 pNN novas (P1601-P1630) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 72: {p974_previsoes_sem_largura(range(72, 73))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1629, testes=TESTES_P1629)
    print(f"P1629 minha taxa de erro ({ERROS_P1629}/{TESTES_P1629}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_73():
    print("--- Parte 73 (0x49: o que refuta) ---")
    print(f"P1631 reenvio (bloco novo, bloco guardado identico, linhas): {p1631_comparar_reenvio()}")
    for n, sem in ((2000, 73), (20000, 74)):
        z, zt, rho, _ = p1632_prioridade_contra_voi(n, sem)
        print(f"P1632 n = {n}, semente {sem}: VOI = 0 em {z:.5f} (conta: 1/2, desvio {(0.25 / n) ** 0.5:.5f}); entre os 10% de maior S: {zt:.4f}; Spearman(S, VOI) = {rho:.4f}")
    n, z0, sv, ss, zt, mtv, mts = p1639_rodada47()
    print(f"P1639 rodada 47: VOI = 0 em {z0} de {n}; nos 200 de maior S, {zt}; VOI medio dos 200 de maior VOI {mtv:.4f}, dos 200 de maior S {mts:.4f} (razao {mts / mtv:.3f})")
    from synthai.dicionario import Dicionario
    d = Dicionario()
    nv, pares = p1635_contradicoes_de_animal(d)
    print(f"P1635 violacoes da disjuncao entre animal e os irmaos: {nv}: {[(d.sinsets[b][1][0], [d.sinsets[x][1][0] for x in v]) for b, v in pares]}")
    tam, contra = p1636_contraexemplos(d=d)
    print(f"P1636 'toda ave voa': fecho de bird {tam}; contraexemplos {len(contra)}: {contra}")
    print(f"P1637 polissemia dos substantivos (lemas, polissemicos, fracao): {p1637_polissemia(d)}")
    print(f"P1638 rodadas com funcoes da libm: {p1638_rodadas_com_libm()}")
    print(f"P1642 heranca multipla (sinsets, substantivos, fracao): {p1642_heranca_multipla(d)}")
    total, sem = p1092_pnn_sem_teste(1631, 1660)
    print(f"P1092 pNN novas (P1631-P1660) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 73: {p974_previsoes_sem_largura(range(73, 74))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1659, testes=TESTES_P1659)
    print(f"P1659 minha taxa de erro ({ERROS_P1659}/{TESTES_P1659}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_74():
    print("--- Parte 74 (0x4A: o que vale testar) ---")
    for sem in (73, 730, 731, 732, 733):
        z, mh, mv = p1661_ganho_de_informacao_contra_voi(2000, sem)
        print(f"P1661 semente {sem}: VOI = 0 entre os 10% de maior ganho de informacao {z:.4f}; VOI medio deles {mh:.4f} contra {mv:.4f} dos de maior VOI (razao {mh / mv:.4f})")
    for sem in (740, 741, 742, 743, 74, 75):
        a, b, f = p1662_orcamento(semente=sem)
        print(f"P1662 semente {sem}: guloso VOI/custo {a:.4f} do otimo; guloso H/custo {b:.4f}; guloso VOI otimo em {f:.4f} das instancias")
    so, s1, s2, ot = p1663_rodada48()
    print(f"P1663 rodada 48: soma dos otimos {so:.4f}; guloso VOI {s1:.4f} ({s1 / so:.4f}); guloso H {s2:.4f} ({s2 / so:.4f}); guloso VOI otimo em {ot} de 300")
    total, sem = p1092_pnn_sem_teste(1661, 1690)
    print(f"P1092 pNN novas (P1661-P1690) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 74: {p974_previsoes_sem_largura(range(74, 75))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1689, testes=TESTES_P1689)
    print(f"P1689 minha taxa de erro ({ERROS_P1689}/{TESTES_P1689}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_75():
    print("--- Parte 75 (0x4B: o que se prova) ---")
    for corr in (False, True):
        h = p1691_laco_de_auto_modificacao(geracoes=5, separador_corrigido=corr)
        print(f"P1691 separador corrigido = {corr}: campos achados {[x[0] for x in h]}; aprovados {[x[1] for x in h]}; delta {h[0][2]:.4f}; "
              f"codigos distintos {len({x[3] for x in h})}: {h[-1][3]!r}")
    n, a, m, am = p1692_godel_nas_funcoes()
    print(f"P1692 calculos.py: {n} funcoes; aprovadas pelo nucleo {a} ({a / n:.4f}); mudadas pela mutacao {m} ({m / n:.4f}); aprovadas e mudadas {am}")
    n, a, m = p1693_godel_no_pacote()
    print(f"P1693 synthai/ (sem testes): {n} funcoes e metodos; aprovados {a} ({a / n:.4f}); mudados {m} ({m / n:.4f})")
    sc, ordem, v, melhor, vmax = p1694_verificador_do_texto()
    print(f"P1698 reenvio (linguagem, bloco guardado identico, linhas): {p1698_comparar_reenvio_v2()}")
    print(f"P1694 Verifier do texto: scores {[(k, round(x, 4)) for k, x in sc.items()]}; ordem gulosa {ordem} (valor {v:.4f}); otimo {melhor} ({vmax:.4f})")
    total, sem = p1092_pnn_sem_teste(1691, 1720)
    print(f"P1092 pNN novas (P1691-P1720) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 75: {p974_previsoes_sem_largura(range(75, 76))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1719, testes=TESTES_P1719)
    print(f"P1719 minha taxa de erro ({ERROS_P1719}/{TESTES_P1719}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_76():
    print("--- Parte 76 (0x4C: a forma do byte) ---")
    for lingua in ("pt", "en"):
        for sem in (76, 77, 78, 79):
            ch, kr = p1721_kronecker_contra_cheio(lingua, sem)
            linha = f"P1721 {lingua} semente {sem}: cheio {ch:.4f}; Kronecker {kr:.4f}; diferenca {kr - ch:+.4f}"
            if lingua == "en":
                _, emb = p1721_kronecker_contra_cheio(lingua, sem, embaralhar=True)
                linha += f"; Kronecker embaralhado {emb:.4f} (embaralhado - ASCII {emb - kr:+.4f})"
            print(linha)
    from synthai.gpt_kronecker import GPTKronecker
    print(f"P1721 pesos de embedding (Kronecker, tabela cheia): {GPTKronecker(VOCAB_GPT, T=16, d1=4, d2=4, h=32, semente=76).pesos_de_embedding()}")
    print(f"P1722 rodadas com funcoes da biblioteca (python, so na preparacao, java): {p1722_libm_nas_duas_linguagens()}")
    total, sem = p1092_pnn_sem_teste(1721, 1750)
    print(f"P1092 pNN novas (P1721-P1750) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 76: {p974_previsoes_sem_largura(range(76, 77))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1749, testes=TESTES_P1749)
    print(f"P1749 minha taxa de erro ({ERROS_P1749}/{TESTES_P1749}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_77():
    print("--- Parte 77 (0x4D: as duas abertas) ---")
    n, mud, rel = p1751_rodada09_nova_contra_antiga()
    print(f"P1751 rodada 09 nova (exp e log proprios) contra a original: {n} numeros, {mud} mudaram, maior diferenca relativa {rel:.3e}")
    print(f"P1722 rodadas com funcoes da biblioteca depois da Parte 77: {p1722_libm_nas_duas_linguagens()}")
    total, sem = p1092_pnn_sem_teste(1751, 1780)
    print(f"P1092 pNN novas (P1751-P1780) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 77: {p974_previsoes_sem_largura(range(77, 78))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1779, testes=TESTES_P1779)
    print(f"P1779 minha taxa de erro ({ERROS_P1779}/{TESTES_P1779}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_78():
    print("--- Parte 78 (0x4E: a atencao de posto baixo) ---")
    for lingua, sems in (("pt", (71, 72)), ("en", (73, 74))):
        for sem in sems:
            b, por, sig = p1783_bits_por_posto(lingua, sem)
            lam = [x * x for x in sig]
            pr = sum(lam) ** 2 / sum(x * x for x in lam)
            print(f"P1783 {lingua} semente {sem}: bits {b:.4f}; delta por posto {[(r, round(v - b, 4)) for r, v in por.items()]}; PR {pr:.3f}")
    total, sem = p1092_pnn_sem_teste(1781, 1810)
    print(f"P1092 pNN novas (P1781-P1810) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 78: {p974_previsoes_sem_largura(range(78, 79))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1809, testes=TESTES_P1809)
    print(f"P1809 minha taxa de erro ({ERROS_P1809}/{TESTES_P1809}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")


def _parte_79():
    print("--- Parte 79 (0x4F: causa e confianca) ---")
    ing, aj, itv = p1811_confusao()
    print(f"P1811 Z -> X, Z -> Y, X -> Y (efeito 0,5): inclinacao ingenua {ing:.4f} (conta 1,0); ajustada por Z {aj:.4f}; sob intervencao {itv:.4f}")
    n, ac, por = p1812_minha_calibracao()
    print(f"P1812 minha calibracao (Partes 53 a 78): {n} previsoes, acerto {ac:.4f}; por tipo {[(k, v[0], round(v[1], 4)) for k, v in por.items()]}")
    zn, zo, f, sd, z = p1813_fator_de_alargamento(ac)
    print(f"P1813 z nominal {zn:.4f}; z observado {zo:.4f}; fator de alargamento {f:.4f}; desvio binomial {sd:.4f}; z do acerto {z:.2f}")
    total, sem = p1092_pnn_sem_teste(1811, 1840)
    print(f"P1092 pNN novas (P1811-P1840) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 79: {p974_previsoes_sem_largura(range(79, 80))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1839, testes=TESTES_P1839)
    print(f"P1839 minha taxa de erro ({ERROS_P1839}/{TESTES_P1839}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_80():
    print("--- Parte 80 (0x50: o valor de um conjunto) ---")
    for olhar in (1, 2):
        for sem in (800, 801, 802, 803, 80):
            a, b, c, d = p1842_conjuntos(semente=sem, olhar=olhar)
            print(f"P1842 olhar {olhar}, semente {sem}: guloso/otimo {a:.4f}; guloso otimo em {b:.4f}; complementaridade {c:.4f}; parado em zero {d:.4f}")
    print(f"P1843 rodada 49 (as mesmas contas da P1842, semente 80): {[round(x, 4) for x in p1843_rodada49()]}")
    total, sem = p1092_pnn_sem_teste(1841, 1870)
    print(f"P1092 pNN novas (P1841-P1870) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 80: {p974_previsoes_sem_largura(range(80, 81))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1869, testes=TESTES_P1869)
    print(f"P1869 minha taxa de erro ({ERROS_P1869}/{TESTES_P1869}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_81():
    print("--- Parte 81 (0x51: o que nao serve) ---")
    a, b, c = p1871_o_que_nao_serve()
    print(f"P1871 nao referenciados pelo nome: calculos.py {len(a)} {a}; synthai/ {len(b)} {b}; arquivos {len(c)}")
    contagem, sobra = p1872_candidatos_explicados(c)
    print(f"P1872 os arquivos acusados, olhados um a um: {contagem}; sem uso: {len(sobra)} {sobra}")
    total, sem = p1092_pnn_sem_teste(1871, 1900)
    print(f"P1092 pNN novas (P1871-P1900) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 81: {p974_previsoes_sem_largura(range(81, 82))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1899, testes=TESTES_P1899)
    print(f"P1899 minha taxa de erro ({ERROS_P1899}/{TESTES_P1899}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_83():
    print("--- Parte 83 (0x53: a probabilidade da probabilidade) ---")
    medido, conta = p1931_gan_de_dirac()
    print(f"P1931 GAN de Dirac (rodada 50): {medido}; contas: {conta}")
    print(f"P1932 jogo assincrono, 200 corridas: {p1932_jogo_assincrono()}")
    print(f"P1932 replica, 800 corridas: {p1932_jogo_assincrono(corridas=800, semente0=84000)}")
    print(f"P1933 calibracao composta sete vezes (conta, simulada, composta, declarar para 1 camada, para 7): {p1933_calibracao_composta()}")
    print(f"P1934 a torre de placares, Partes 67-81: {p1934_torre_de_placares()}")
    print(f"P1935 o modulo sete_camadas recebido contra a logistica: {p1935_sete_camadas_recebido()}")
    print(f"P1936 Lyapunov assincrono a = 0,2: {p1936_lyapunov_assincrono()}; a = 0,05: {p1936_lyapunov_assincrono(a=0.05, passos=20000000, semente=86)}")
    total, sem = p1092_pnn_sem_teste(1931, 1960)
    print(f"P1092 pNN novas (P1931-P1960) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 83: {p974_previsoes_sem_largura(range(83, 84))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P1959, testes=TESTES_P1959)
    print(f"P1959 minha taxa de erro ({ERROS_P1959}/{TESTES_P1959}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_84():
    print("--- Parte 84 (0x54: o delirio e o escrutinio) ---")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84))
    print(f"P1961 teste (e) da Parte 79 (acerto das Partes 80, 81, 83, 84): {ok}/{tot} = {frac:.4f}; por parte {por}")
    print(f"P1962 Lyapunov pelo operador de transferencia a=0,2: {p1962_lyapunov_por_densidade(a=0.2)}")
    print(f"P1962 a=0,05: {p1962_lyapunov_por_densidade(a=0.05)}")
    print(f"P1963 delirio base (agulha, com ruido): {p1963_delirio_e_escrutinio()}")
    print(f"P1963 (h) limpo agulha: recoze {p1963_delirio_e_escrutinio(ruido=0.0)[1]:.4f}")
    r_i = p1963_delirio_e_escrutinio(ruido=0.0, largura=30)
    print(f"P1963 (i) limpo largo: recoze {r_i[1]:.4f} gulosa {r_i[0]:.4f}")
    print(f"P1963 (j) limpo largo lento (50000 passos): recoze {p1963_delirio_e_escrutinio(ruido=0.0, largura=30, passos=50000)[1]:.4f}")
    print(f"P1964 rodada 51 (Metropolis, IGUAL em Java): {p1964_rodada51()}")
    total, sem = p1092_pnn_sem_teste(1961, 1990)
    print(f"P1092 pNN novas (P1961-P1990) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 84: {p974_previsoes_sem_largura(range(84, 85))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2019, testes=TESTES_P2019)
    print(f"P2019 minha taxa de erro ({ERROS_P2019}/{TESTES_P2019}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_85():
    print("--- Parte 85 (0x55: a arquitetura recursiva recebida) ---")
    print(f"P1991 cosseno duplicado do codigo recebido (0,45,90,135,180 graus): {p1991_cosseno_duplicado_recebido()}")
    print(f"P1992 pilha adversarial: escritas em self.layers fora do __init__ = {p1992_pilha_adversarial_sem_treino()} (sem treino)")
    print(f"P1993 buraco do escrutinio (inconsistentes que passam intactos): {p1993_buraco_do_escrutinio()}")
    print(f"P1994 vetor preso na esfera, max |norma-1| em 50 passos: {p1994_vetor_preso_na_esfera():.2e}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (e), Partes 80-85: {ok}/{tot} = {frac:.4f}; por parte {por}")
    print(f"P1995 rodada 52 (recozimento inteiro, IGUAL em Java): {p1995_rodada52()}")
    total, sem = p1092_pnn_sem_teste(1991, 2020)
    print(f"P1092 pNN novas (P1991-P2020) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 85: {p974_previsoes_sem_largura(range(85, 86))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2099, testes=TESTES_P2099)
    print(f"P2099 minha taxa de erro ({ERROS_P2099}/{TESTES_P2099}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_86():
    print("--- Parte 86 (0x56: o cerebro na CPU) ---")
    erro, previsto = p2021_lif_ponto_fixo()
    print(f"P2021 LIF erro do ponto fixo apos 200 passos: {erro:.3e} (previsto gap*beta^200 = {previsto:.3e})")
    print(f"P2022 Izhikevich (RS, CH) disparos em 1000ms: {p2022_izhikevich_tipos()}")
    print(f"P2023 memoria do relatorio (MB neuronios, GB sinapses, GB total, incoerencias): {p2023_memoria_relatorio()}")
    print(f"P2024 cadeia de vazao (disparos/ms, sinapses/ms, GSOPS): {p2024_gsops()}")
    print(f"P2025 sobreposicao de SDRs (media, teorico k^2/n): {p2025_sdr_sobreposicao()}")
    print(f"P2026 STDP liquido (simetrico, assimetrico): {p2026_stdp_liquido()}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (e)/(g), Partes 80-86: {ok}/{tot} = {frac:.4f}; por parte {por}")
    print(f"P2027 rodada 53 (Izhikevich, IGUAL em Java): {p2027_rodada53()}")
    total, sem = p1092_pnn_sem_teste(2021, 2050)
    print(f"P1092 pNN novas (P2021-P2050) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 86: {p974_previsoes_sem_largura(range(86, 87))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2169, testes=TESTES_P2169)
    print(f"P2169 minha taxa de erro ({ERROS_P2169}/{TESTES_P2169}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_87():
    print("--- Parte 87 (0x57: compressao, plasticidade e GRPO) ---")
    m8, m4, razao = p2051_quantizacao_mse()
    print(f"P2051 quantizacao: MSE INT8 {m8:.3e}, INT4 {m4:.3e}, razao INT4/INT8 {razao:.1f} (4^4=256)")
    print(f"P2052 GRPO (vantagens G=2 com eps=0, media G=4): {p2052_vantagem_grpo()}")
    print(f"P2053 plasticidade (SGD, S&P) = ((posto ratio, norma ratio), ...): {p2053_plasticidade()}")
    print(f"P2054 plasticidade com conflito, 100 tarefas (posto ratio, norma ratio, dormentes): {p2054_plasticidade_conflito()}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (e), Partes 80-87: {ok}/{tot} = {frac:.4f}; por parte {por}")
    print(f"P2055 rodada 54 (vantagem GRPO, IGUAL em Java): {len(p2055_rodada54())} vantagens")
    total, sem = p1092_pnn_sem_teste(2051, 2080)
    print(f"P1092 pNN novas (P2051-P2080) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 87: {p974_previsoes_sem_largura(range(87, 88))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2239, testes=TESTES_P2239)
    print(f"P2239 minha taxa de erro ({ERROS_P2239}/{TESTES_P2239}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_88():
    print("--- Parte 88 (0x58: a arquitetura autopoietica recebida) ---")
    print(f"P2081 P(P(X)) do codigo (P(P(0,9)), P(P(0,1)), ponto fixo): {p2081_probabilidade_aninhada()}")
    print(f"P2082 P(P) iterado 10x de 0,9 (medido, conta): {p2082_probabilidade_aninhada_iterada()}")
    print(f"P2083 LFI1 sem explosao (conj(0,5,~0,5), consistencia(0,5), F preservado): {p2083_lfi1_sem_explosao()}")
    print(f"P2084 descompasso texto-codigo (usa entropia?, usa consistencia?): {p2084_descompasso_texto_codigo()}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (e), Partes 80-88: {ok}/{tot} = {frac:.4f}; por parte {por}")
    print(f"P2085 rodada 55 (passo GRPO com corte, IGUAL em Java): {len(p2085_rodada55())} surrogates")
    total, sem = p1092_pnn_sem_teste(2081, 2110)
    print(f"P1092 pNN novas (P2081-P2110) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 88: {p974_previsoes_sem_largura(range(88, 89))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2309, testes=TESTES_P2309)
    print(f"P2309 minha taxa de erro ({ERROS_P2309}/{TESTES_P2309}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_89():
    print("--- Parte 89 (0x59: o substrato que aprende) ---")
    print(f"P2111 integral STDP (balanceada, depressao): {p2111_stdp_integral()}")
    print(f"P2112 deriva sob Poisson independente (soma, sinal da integral): {p2112_stdp_deriva_sinal()}")
    print(f"P2113 STDP timing 500 pares (pre antes, pre depois): {p2113_stdp_timing()}")
    print(f"P2114 competicao toy, semente 90 (corr, ruido, |dif|): {p2114_competicao_toy()}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (e), Partes 80-89: {ok}/{tot} = {frac:.4f}; por parte {por}")
    print(f"P2115 rodada 56 (populacao Izhikevich, IGUAL em Java): {p2115_rodada56()} disparos")
    total, sem = p1092_pnn_sem_teste(2111, 2140)
    print(f"P1092 pNN novas (P2111-P2140) sem teste: {len(sem)} de {total}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 89: {p974_previsoes_sem_largura(range(89, 90))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2379, testes=TESTES_P2379)
    print(f"P2379 minha taxa de erro ({ERROS_P2379}/{TESTES_P2379}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_90():
    print("--- Parte 90 (0x5A: a rede que aprende igual) ---")
    total, sw, sw0 = p2141_rede_stdp()
    print(f"P2141 rede Izhikevich+STDP (rodada 57, IGUAL em Java): {total} disparos, soma W {sw:.5f} (de {sw0})")
    print(f"P2142 ΔW_total (depressao dominante, negativo): {p2142_delta_peso():.5f}")
    print(f"P2143 disparos aprendiz vs fixo: {p2143_disparos_aprendiz_vs_fixo()}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (d), Partes 80-90: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2141, 2170)
    print(f"P1092 pNN novas (P2141-P2170) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 90: {p974_previsoes_sem_largura(range(90, 91))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2449, testes=TESTES_P2449)
    print(f"P2449 minha taxa de erro ({ERROS_P2449}/{TESTES_P2449}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_91():
    print("--- Parte 91 (0x5B: o GPT que aprende igual) ---")
    print(f"P2171 rodada 58 (gradiente softmax+CE, SGD, decisao; IGUAL em Java): caso 0 = {p2171_rodada58()[0]}")
    print(f"P2172 o passo de SGD reduz a perda nos 5 casos: {p2172_sgd_reduz_perda()}")
    print(f"P2173 gradiente = p - onehot, max |num - analitico|: {p2173_gradiente_p_menos_onehot():.2e}")
    print(f"P2174 o GPT real memoriza um padrao (perda inicial, final): {tuple(round(x, 4) for x in p2174_gpt_memoriza())}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (e), Partes 80-91: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2171, 2200)
    print(f"P1092 pNN novas (P2171-P2200) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 91: {p974_previsoes_sem_largura(range(91, 92))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2519, testes=TESTES_P2519)
    print(f"P2519 minha taxa de erro ({ERROS_P2519}/{TESTES_P2519}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_92():
    print("--- Parte 92 (0x5C: o Adam e a fronteira do pow) ---")
    print(f"P2201 fronteira do pow (0.9**t != produto, t=1..500): {p2201_fronteira_pow()} de 500")
    print(f"P2202 produto por multiplicacao repetida (pow inteiro, portavel): t=10 -> {p2202_produto_portavel()[9]}")
    print(f"P2203 rodada 59 (passo de Adam, IGUAL em Java): perdas finais = {[round(x, 4) for x in p2203_rodada59()]}")
    print(f"P2204 o passo de Adam reduz a perda nos 5 casos: {p2204_adam_reduz_perda()}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92))
    print(f"P1961 teste (e), Partes 80-92: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2201, 2230)
    print(f"P1092 pNN novas (P2201-P2230) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 92: {p974_previsoes_sem_largura(range(92, 93))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2589, testes=TESTES_P2589)
    print(f"P2589 minha taxa de erro ({ERROS_P2589}/{TESTES_P2589}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_93():
    print("--- Parte 93 (0x5D: o modelo de mundo que planeja) ---")
    print(f"P2231 recuperacao do modelo de mundo (minimos quadrados, mundo linear): erro = {p2231_recuperar_modelo():.2e}")
    m_mpc, m_re, razao, por_c = p2232_mpc_vs_reativo_painel()
    print(f"P2232 painel MPC x reativo (4 condicoes): custo medio MPC = {m_mpc:.4f}, reativo = {m_re:.4f}, razao = {razao:.4f}")
    cm, cr, rz = p2233_mpc_regime_velocidade(s0=(-1.0, 1.5), alvo=-0.5, semente=23)
    print(f"P2233 regime cego a velocidade (NOVA condicao): custo MPC = {cm:.4f}, reativo = {cr:.4f}, razao = {rz:.4f}")
    custos, melhor, mc = p2234_horizonte_nao_monotono()
    print(f"P2234 horizonte nao-monotono (H=1,3,6,12): custos = {[round(x, 3) for x in custos]}; melhor H = {(1, 3, 6, 12)[melhor]}")
    custos2, mono = p2235_shooting_converge()
    print(f"P2235 tiro aleatorio converge (K=8,32,128,512): custos = {[round(x, 3) for x in custos2]}; nao-crescente = {mono}")
    print(f"P2236 recusa da auto-operacao autonoma (ast; subprocess/Popen, urllib/http): {p2236_recusa_autoreplicacao()} -> capacidade RECUSADA")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93))
    print(f"P1961 teste (g), Partes 80-93: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2231, 2260)
    print(f"P1092 pNN novas (P2231-P2260) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 93: {p974_previsoes_sem_largura(range(93, 94))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2659, testes=TESTES_P2659)
    print(f"P2659 minha taxa de erro ({ERROS_P2659}/{TESTES_P2659}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_94():
    print("--- Parte 94 (0x5E: o mundo que nao e linear) ---")
    ml, mm, mr, razao = p2261_lqr_vs_mpc()
    print(f"P2261 LQR (otimo) x MPC x reativo: medias LQR = {ml:.4f}, MPC(K512) = {mm:.4f}, reativo = {mr:.4f}; razao MPC/LQR = {razao:.4f}")
    r1, r2, dif = p2262_vies_de_forma()
    print(f"P2262 vies de forma (mundo nao-linear, modelo linear): residuo n=400 = {r1:.5f}, n=6400 = {r2:.5f}, |dif| = {dif:.5f} (nao encolhe)")
    print(f"P2263 base cubica recupera o exato: residuo = {p2263_base_cubica_recupera():.2e}")
    mm2, mr2, rz2 = p2264_mpc_modelo_errado()
    print(f"P2264 MPC com modelo ERRADO x reativo (mundo nao-linear): MPC = {mm2:.4f}, reativo = {mr2:.4f}, razao MPC/reativo = {rz2:.4f}")
    saida, arg = p2265_rodada61()
    print(f"P2265 rodada 61 (atencao causal, IGUAL em Java): decisao = {arg}; saida[-1] = {[round(x, 4) for x in saida]}")
    print(f"P2266 Riccati e ponto fixo (auditoria da forma fechada): residuo = {p2266_riccati_e_ponto_fixo():.2e}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94))
    print(f"P1961 teste (f), Partes 80-94: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2261, 2290)
    print(f"P1092 pNN novas (P2261-P2290) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 94: {p974_previsoes_sem_largura(range(94, 95))}")
    media, lo, hi = p95_minha_taxa_de_erro(erros=ERROS_P2729, testes=TESTES_P2729)
    print(f"P2729 minha taxa de erro ({ERROS_P2729}/{TESTES_P2729}): media = {media:.2f}, intervalo 90% = [{lo:.2f}, {hi:.2f}]")

def _parte_95():
    print("--- Parte 95 (0x5F: o relatorio v2.0 recebido, auditado sem executar) ---")
    lo, hi, cresce = p2291_direcao_de_p_estrela()
    print(f"P2291 direcao de P* em eps: P*(0,10) = {lo:.6f}, P*(0,45) = {hi:.6f}, cresce = {cresce} -> relatorio ('mais estrito') FALSO")
    ft, fs, dif = p2292_ttts_nao_domina()
    print(f"P2292 TTTS x Thompson (melhor braco, T=300): TTTS = {ft:.3f}, Thompson = {fs:.3f}, dif = {dif:+.3f} (vantagem modesta, nao 'drastica')")
    alto_ok, baixo_ok, (ae, ai, be, bi) = p2293_ewc_troca_o_que_protege()
    print(f"P2293 EWC troca: Fisher-alto EWC<iso = {alto_ok} ({ae:.3f} vs {ai:.3f}); Fisher-baixo EWC>iso = {baixo_ok} ({be:.3f} vs {bi:.3f})")
    rms, teo, razao = p2294_oito_bits_nao_e_float64()
    print(f"P2294 8 bits nao e float64: RMS = {rms:.5f} (teorico D/sqrt12 = {teo:.5f}); = {razao:.2e} vezes o epsilon do float64")
    pesos, pcat = p2295_rodada62()
    print(f"P2295 rodada 62 (passo EWC, IGUAL em Java): p_cat = {pcat:.4f}; pesos novos = {[round(x, 4) for x in pesos]}")
    print(f"P2296 vies de indice do simulador recebido (ast): {p2296_vies_de_indice_do_simulador()} -> o braco atualizado nao e o reportado")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95))
    print(f"P1961 teste (f), Partes 80-95: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2291, 2320)
    print(f"P1092 pNN novas (P2291-P2320) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 95: {p974_previsoes_sem_largura(range(95, 96))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P2799, testes=TESTES_P2799)
    print(f"P2799 minha taxa de erro ({ERROS_P2799}/{TESTES_P2799}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_96():
    print("--- Parte 96 (0x60: aprender a base) ---")
    r1, r2, dif = p2321_grau2_nao_ajuda()
    print(f"P2321 grau 2 nao ajuda: res grau1 = {r1:.5f}, res grau2 = {r2:.5f}, |dif| = {dif:.5f} (o que falta e de grau 3)")
    print(f"P2322 grau 3 recupera o exato: residuo = {p2322_grau3_recupera():.2e}")
    rtr, rte = p2323_mlp_aprende_a_base()
    print(f"P2323 MLP (features aprendidas): res_treino = {rtr:.5f}, res_teste = {rte:.5f} (entre a linear ~0,12 e a cubica ~0)")
    otr, ote = p2324_overfit_base_rica()
    print(f"P2324 overfit (grau 5, n=40): res_treino = {otr:.5f}, res_teste = {ote:.5f} (vies vira variancia)")
    out = p2325_rodada63()
    print(f"P2325 rodada 63 (residual + LayerNorm, IGUAL em Java, sem transcendental): saida = {[round(x, 4) for x in out]}")
    menor, res = p2326_menor_grau_exato()
    print(f"P2326 menor grau que recupera o exato: {menor} (residuos por grau: {{{', '.join(f'{g}: {rr:.5f}' for g, rr in res.items())}}})")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96))
    print(f"P1961 teste (f), Partes 80-96: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2321, 2350)
    print(f"P1092 pNN novas (P2321-P2350) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 96: {p974_previsoes_sem_largura(range(96, 97))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P2869, testes=TESTES_P2869)
    print(f"P2869 minha taxa de erro ({ERROS_P2869}/{TESTES_P2869}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_97():
    print("--- Parte 97 (0x61: a cura da variancia e o bloco inteiro) ---")
    ls, rt, interior = p2351_ridge_faz_u()
    print(f"P2351 cumeeira faz um U: lambda* = {ls} (interior = {interior}), melhor teste = {rt:.4f}")
    best, rlin = p2352_ridge_mitiga_nao_cura()
    print(f"P2352 cumeeira mitiga mas nao cura: melhor ridge = {best:.4f}; base linear = {rlin:.4f} (ridge ainda pior)")
    cap, nao_cresce, razao = p2353_mlp_capacidade()
    print(f"P2353 capacidade do MLP: {[(h, round(r, 4)) for h, r in cap]}; nao-crescente = {nao_cresce}; res16/res2 = {razao:.3f}")
    arg, logits = p2354_rodada64()
    print(f"P2354 rodada 64 (bloco transformer 2 camadas, IGUAL em Java): decisao = {arg}; logits = {[round(x, 4) for x in logits]}")
    l40, l160, r160 = p2355_dados_curam_variancia()
    print(f"P2355 dados curam a variancia: lambda*(n=40) = {l40}, lambda*(n=160) = {l160}, melhor teste(n=160) = {r160:.2e}")
    npar, rlim = p2356_limiar_de_parametros()
    print(f"P2356 limiar de parametros (grau 5): {npar} parametros; n logo acima -> residuo de teste = {rlim:.2e}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97))
    print(f"P1961 teste (f), Partes 80-97: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2351, 2380)
    print(f"P1092 pNN novas (P2351-P2380) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 97: {p974_previsoes_sem_largura(range(97, 98))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P2939, testes=TESTES_P2939)
    print(f"P2939 minha taxa de erro ({ERROS_P2939}/{TESTES_P2939}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_98():
    print("--- Parte 98 (0x62: o ruido de observacao) ---")
    r1, r2, razao = p2381_piso_linear_em_sigma()
    print(f"P2381 piso linear em sigma: res(0,1) = {r1:.5f}, res(0,2) = {r2:.5f}, razao = {razao:.3f} (dobra quando sigma dobra)")
    med, conta = p2382_nao_exato_sob_ruido()
    print(f"P2382 n>#params NAO e exato sob ruido: residuo(sigma=0,1, n=800) = {med:.5f} (conta sigma*sqrt(p/n) = {conta:.5f}); longe de 1e-11")
    r200, r800, rz = p2383_variancia_cura_devagar()
    print(f"P2383 variancia cura devagar (1/sqrt(n)): res(n=200) = {r200:.5f}, res(n=800) = {r800:.5f}, razao = {rz:.3f} (~2)")
    melh, l01, l03 = p2384_ridge_sob_ruido()
    print(f"P2384 cumeeira sob ruido: melhoria em sigma=0,1 = {melh:.2f}% (n>>p); lambda*(0,1) = {l01}, lambda*(0,3) = {l03} (cresce com sigma)")
    toks = p2385_rodada65()
    print(f"P2385 rodada 65 (geracao autorregressiva, IGUAL em Java): tokens = {[t for t, _ in toks]}")
    a, b, difrel = p2386_razao_constante_em_sigma()
    print(f"P2386 razao residuo/sigma constante em sigma: {a:.5f} vs {b:.5f}, dif relativa = {difrel:.2e}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98))
    print(f"P1961 teste (f), Partes 80-98: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2381, 2410)
    print(f"P1092 pNN novas (P2381-P2410) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 98: {p974_previsoes_sem_largura(range(98, 99))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3009, testes=TESTES_P3009)
    print(f"P3009 minha taxa de erro ({ERROS_P3009}/{TESTES_P3009}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_99():
    print("--- Parte 99 (0x63: a amostragem e o fecho do modelo de mundo) ---")
    hs, cresce = p2411_entropia_cresce_com_T()
    print(f"P2411 entropia cresce com T: T=0,5/1/2 -> {[round(h, 4) for h in hs]}; cresce = {cresce}")
    todos, arg, top1 = p2412_T_zero_vira_argmax()
    print(f"P2412 T->0 vira argmax: todos os u dao o argmax {arg}? {todos}; top1(T=0,01) = {top1:.6f}")
    full, tk, levantou = p2413_top_k_levanta_massa()
    print(f"P2413 top-k levanta a massa: top1 completo = {full:.4f}, apos top-2 = {tk:.4f}, levantou = {levantou}")
    rr, rl, s2 = p2414_piso_teste_ruidoso()
    print(f"P2414 piso do teste ruidoso: vs ruidoso = {rr:.4f}, vs limpo = {rl:.4f}, sqrt(2)*sigma = {s2:.4f}")
    casos = p2415_rodada66()
    print(f"P2415 rodada 66 (temperatura + top-k, IGUAL em Java): tokens = {[t for t, _, _ in casos]}")
    retro = p2416_retrospecto_modelo_mundo()
    print(f"P2416 retrospecto do modelo de mundo (os 3 pisos): forma = {retro['forma']:.4f}, dados = {retro['dados']:.4f}, ruido = {retro['ruido']:.4f}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=tuple(list(range(80,82))+[83]+list(range(84,100))))
    print(f"P1961 teste (f), Partes 80-99: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2411, 2440)
    print(f"P1092 pNN novas (P2411-P2440) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 99: {p974_previsoes_sem_largura(range(99, 100))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3079, testes=TESTES_P3079)
    print(f"P3079 minha taxa de erro ({ERROS_P3079}/{TESTES_P3079}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_100():
    print("--- Parte 100 (0x64: o dicionario como data lake encontra o GPT) ---")
    b_en, b_pt, dif = p2441_invariancia_4grama()
    print(f"P2441 invariancia no 4-grama: en = {b_en:.3f}, pt = {b_pt:.3f}, |dif| = {dif:.3f} bits/char (o genero 'definicao')")
    print(f"P2442 invariancia nao e volume: trigrama en num subconjunto aleatorio de 511k = {p2442_invariancia_nao_e_volume():.3f}")
    gpt_en, tri_en, gpt_pt, tri_pt = p2443_gpt_contra_ngrama()
    print(f"P2443 GPT x n-grama: en GPT = {gpt_en:.3f} vs trigrama {tri_en:.3f}; pt GPT = {gpt_pt:.3f} vs trigrama {tri_pt:.3f} (GPT perde nas duas)")
    unif, menor_en, menor_pt, meio = p2444_gpt_no_meio(gpt_en, gpt_pt)
    print(f"P2444 GPT no meio: uniforme (log2 V) = {unif:.3f}; gpt<uniforme en/pt = {menor_en}/{menor_pt}; ambos em [3,0;4,1] = {meio}")
    casos = p2445_rodada67()
    print(f"P2445 rodada 67 (nucleus top-p, IGUAL em Java): tokens = {[t for t, _, _ in casos]}; mantidos = {[m for _, m, _ in casos]}")
    kf, rod, cal = p2446_retrospecto_cem()
    print(f"P2446 retrospecto de cem partes: {kf} funcoes pNN, {rod} rodadas do dialogo, calibracao do mundo 80-100 = {cal:.4f}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=tuple(list(range(80,82))+[83]+list(range(84,101))))
    print(f"P1961 teste (f), Partes 80-100: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2441, 2470)
    print(f"P1092 pNN novas (P2441-P2470) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 100: {p974_previsoes_sem_largura(range(100, 101))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3149, testes=TESTES_P3149)
    print(f"P3149 minha taxa de erro ({ERROS_P3149}/{TESTES_P3149}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_101():
    print("--- Parte 101 (0x65: dez camadas, a recursao que contrai, o caos que nao comprime) ---")
    it10, conta, it7 = p2471_dez_camadas()
    print(f"P2471 dez camadas: iter10 = {it10:.6f} (conta {conta:.6f}); iter7 = {it7:.6f} (10 e mais perto de 0,5)")
    comp, contab, fixo = p2472_composicao_prob_metacog()
    print(f"P2472 prob o metacog: composicao = {comp:.6f} (produto dos fatores {contab:.6f}); ponto fixo = {fixo:.6f}")
    caos, razao = p2473_texto_x_caos()
    print(f"P2473 texto x caos: caos (logistico r=4) = {caos:.4f} bits/bit (incompressivel); glosas razao = {razao:.4f} (comprime)")
    res, converge = p2474_recursao_contrai()
    print(f"P2474 a recursao contrai: de x0 variados, 40 camadas -> {[round(r, 4) for r in res]}; todos ~0,5 = {converge} (ponto fixo unico, Banach)")
    casos = p2475_rodada68()
    print(f"P2475 rodada 68 (penalidade de repeticao, IGUAL em Java): tokens = {[t for t, _ in casos]}")
    ab, ba, assim = p2476_versa_reversa()
    print(f"P2476 versa/reversa: pergunta-em-resposta = {ab:.3f}, resposta-em-pergunta = {ba:.3f}, assimetrico = {assim} (como a Parte 46)")
    ok, tot, frac, por = p1961_teste_e_da_calibracao(partes=tuple(list(range(80,82))+[83]+list(range(84,102))))
    print(f"P1961 teste (f), Partes 80-101: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2471, 2500)
    print(f"P1092 pNN novas (P2471-P2500) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 101: {p974_previsoes_sem_largura(range(101, 102))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3219, testes=TESTES_P3219)
    print(f"P3219 minha taxa de erro ({ERROS_P3219}/{TESTES_P3219}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_102():
    print("--- Parte 102 (0x66: o Global Workspace) ---")
    iso, ws, razao = p2501_integracao_vence()
    print(f"P2501 integracao vence (precisa de dois): isolado = {iso:.4f}, workspace = {ws:.2e}, razao = {razao:.2e}")
    iso0, ws0 = p2502_empata_quando_um_basta()
    print(f"P2502 empata quando um basta (b=0): isolado = {iso0:.2e}, workspace = {ws0:.2e}")
    print(f"P2503 a integracao recupera o exato: rmse workspace (8 passos) = {p2503_recupera_exato():.2e}")
    rs, mono = p2504_convergencia_geometrica()
    print(f"P2504 convergencia geometrica: rmse(1,2,3) = {[f'{r:.2e}' for r in rs]}; monotono decrescente = {mono}")
    seq, sc = p2505_rodada69()
    print(f"P2505 rodada 69 (beam search, IGUAL em Java): melhor sequencia = {seq}, escore = {sc:.4f}")
    rede, popen = p2506_recusa_upload_v015()
    print(f"P2506 recusa do upload v0_15_0 (ast; urllib/rede, subprocess/Popen): ({rede}, {popen}) -> RECUSADO (domestico, trabalho_continuo)")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (f), Partes 80-102: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2501, 2530)
    print(f"P1092 pNN novas (P2501-P2530) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 102: {p974_previsoes_sem_largura(range(102, 103))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3289, testes=TESTES_P3289)
    print(f"P3289 minha taxa de erro ({ERROS_P3289}/{TESTES_P3289}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_103():
    print("--- Parte 103 (0x67: o dicionario como numeros, e o sinal de um jogo de cartas) ---")
    e, teto = p2531_entropia_do_baralho()
    print(f"P2531 o baralho como numero: entropia empirica = {e:.4f} bits (teto fechado log2 52 = {teto:.4f})")
    so, amb = p2532_numero_e_palavra()
    print(f"P2532 numero + palavra bate so o numero: so_numero = {so:.4f} (cego a cor ~0,5), numero+palavra = {amb:.4f}")
    print(f"P2533 o dicionario como calculo binario (posto GF(2)^4) = {p2533_posto_gf2_do_dicionario()}")
    col, esp = p2534_colisoes_do_dicionario()
    print(f"P2534 o dicionario como numero nao-binario: colisoes = {col} (esperadas C(n,2)/m = {esp:.2f})")
    rede, repl = p2535_recusa_proposta_parte103()
    seg = p2535_recusa_proposta_parte103("dicionario_em_numeros+baralho")
    print(f"P2535 recuso a rede/auto-replicacao: proposta = ({rede}, {repl}) -> RECUSADO (yfinance, duckduckgo, auto-replicacao); nucleo = {seg} -> CONSTRUIDO")
    saida = p2536_rodada70()
    print(f"P2536 rodada 70 (multi-cabecas concatenadas, IGUAL em Java): saida[-1] = {[f'{v:.4f}' for v in saida[-1]]}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste (f), Partes 80-103: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2531, 2560)
    print(f"P1092 pNN novas (P2531-P2560) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 103: {p974_previsoes_sem_largura(range(103, 104))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3359, testes=TESTES_P3359)
    print(f"P3359 minha taxa de erro ({ERROS_P3359}/{TESTES_P3359}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_104():
    print("--- Parte 104 (0x68: a carta escondida; decisao sob informacao oculta, e a fronteira do seno) ---")
    slope, ev = p2561_duelo_carta_alta()
    print(f"P2561 duelo de carta alta: inclinacao = {slope:.4f} (1/13), EV simetrico = {ev:.4f}")
    print(f"P2562 limiar de pagar (adversario aposta com carta >= 7): c* = {p2562_limiar_pagar()}")
    frac, fechada = p2563_valor_info_oculta()
    print(f"P2563 valor da informacao oculta: fracao que muda a decisao = {frac:.4f} (forma fechada 6/13 = {fechada:.4f})")
    contar = p2564_fronteira_do_seno()
    print(f"P2564 a fronteira do seno (MEDIDO): math.sin difere da referencia em {contar} de 1000 args -> sin NAO e fronteira aqui (reputacao, nao medida: regra da Parte 84); PE com serie propria IGUAL em Java (rodada 71); a sonda_seno_104 mostra que o naive tambem e IGUAL aqui")
    var, pk, pk2 = p2565_invariancia_translacao()
    print(f"P2565 invariancia de translacao da PE: variancia entre posicoes (k=3) = {var:.2e} (< 1e-12); produto k=3 = {pk:.4f} != k=5 = {pk2:.4f}")
    saida = p2566_rodada71()
    print(f"P2566 rodada 71 (codificacao posicional, serie propria, IGUAL em Java): PE(13)[:4] = {[f'{v:.4f}' for v in saida[:4]]}")
    ok, tot, frac2, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-104: {ok}/{tot} = {frac2:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2561, 2590)
    print(f"P1092 pNN novas (P2561-P2590) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 104: {p974_previsoes_sem_largura(range(104, 105))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3429, testes=TESTES_P3429)
    print(f"P3429 minha taxa de erro ({ERROS_P3429}/{TESTES_P3429}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_105():
    print("--- Parte 105 (0x69: o blefe; o equilibrio de indiferenca, e a fronteira medida do seno) ---")
    a, asim = p2591_frequencia_do_blefe()
    print(f"P2591 frequencia de blefe: alpha = {a:.4f} (B/(P+2B)=1/3), simulado = {asim:.4f}")
    c, csim = p2592_frequencia_de_pagar()
    print(f"P2592 frequencia de pagar: c = {c:.4f} (P/(P+B)=1/2), simulado = {csim:.4f}")
    ip, ib, plana = p2593_indiferenca()
    print(f"P2593 indiferenca: |EV(pagar)| = {ip:.2e}, |EV(blefar)| = {ib:.2e}, melhor-resposta plana = {plana:.2e}")
    difs = p2594_fronteira_das_trigonometricas()
    print(f"P2594 a 6a face EXISTE (MEDIDO, corrige a Parte 104): math.sin difere da referencia em {difs} de 2000 args na faixa larga (k/1000); a sonda_transc_105 mediu sin=21 cos=18 tan=35 atan2=590 divergencias Python x Java em 10000 args - o 6o rosto da fronteira depende da FAIXA (reducao mod 2pi)")
    al, cc, b, evp, evb = p2595_rodada72()
    print(f"P2595 rodada 72 (decisao de equilibrio, IGUAL em Java): alpha={al:.4f} c={cc:.4f} b={b:.4f} ev_pagar={evp:.2e} ev_blefar={evb:.2e}")
    ok, tot, frac, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-105: {ok}/{tot} = {frac:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2591, 2620)
    print(f"P1092 pNN novas (P2591-P2620) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 105: {p974_previsoes_sem_largura(range(105, 106))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3499, testes=TESTES_P3499)
    print(f"P3499 minha taxa de erro ({ERROS_P3499}/{TESTES_P3499}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_106():
    print("--- Parte 106 (0x6A: a segunda rua, e a reducao de argumento) ---")
    sn, cs = p2621_rodada73()
    print(f"P2621 rodada 73 (sin_/cos_ proprios na faixa da libm divergente, IGUAL em Java 10000 args): sin_(pi)={sn:.2e} cos_(pi)={cs:.4f}")
    print(f"P2622 exatidao do sin_ proprio em [0,001;10]: max|sin_-ref| = {p2622_exatidao_sin_proprio():.2e} (< 1e-12)")
    d3, d9 = p2623_reducao_duas_partes()
    print(f"P2623 reducao duas partes: 1-parte vs 2-partes dif(x=1e3)={d3:.2e} (<1e-12, concordam), dif(x=1e9)={d9:.2e} (>1e-9, divergem)")
    frac, fechada = p2624_voi_duas_ruas()
    print(f"P2624 VOI duas ruas: fracao = {frac:.4f} (forma fechada 1-(7/13)^2 = {fechada:.4f})")
    dobro, duas, dif = p2625_subaditividade_voi()
    print(f"P2625 sub-aditividade: dobro de uma rua = {dobro:.4f}, duas ruas = {duas:.4f}, diferenca = {dif:.4f}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-106: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2621, 2650)
    print(f"P1092 pNN novas (P2621-P2650) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 106: {p974_previsoes_sem_largura(range(106, 107))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3569, testes=TESTES_P3569)
    print(f"P3569 minha taxa de erro ({ERROS_P3569}/{TESTES_P3569}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_107():
    print("--- Parte 107 (0x6B: a inducao reversa; o equilibrio de duas ruas) ---")
    v1, v2 = p2651_rodada74()
    print(f"P2651 rodada 74 (inducao reversa, IGUAL em Java): V1(A)={v1:.1f} V2(A)={v2:.1f}")
    print(f"P2652 valor otimo de duas decisoes a partir de A: V2(A) = {p2652_valor_otimo_duas_decisoes():.1f}")
    rt, rs = p2653_reversa_vs_miope()
    print(f"P2653 reversa vs miope: razao no teste = {rt:.2f} (reversa bate), razao no separavel = {rs:.2f} (empatam)")
    a1, a2, dif = p2654_valor_da_segunda_decisao()
    print(f"P2654 valor da segunda decisao: V2(A)-V1(A) = {a2:.1f}-{a1:.1f} = {dif:.1f}")
    ve, vi = p2655_voi_estado_oculto()
    print(f"P2655 VOI do estado oculto: espelho = {ve:.2f} (> 0), identico = {vi:.2f} (controle = 0)")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-107: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2651, 2680)
    print(f"P1092 pNN novas (P2651-P2680) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 107: {p974_previsoes_sem_largura(range(107, 108))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3639, testes=TESTES_P3639)
    print(f"P3639 minha taxa de erro ({ERROS_P3639}/{TESTES_P3639}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_108():
    print("--- Parte 108 (0x6C: o minimax; o equilibrio de um jogo de soma zero) ---")
    v, p, q = p2681_rodada75()
    print(f"P2681 rodada 75 (minimax, IGUAL em Java): valor={v:.4f} p={p:.4f} q={q:.4f}")
    mm, nm, dif = p2682_von_neumann()
    print(f"P2682 von Neumann: maxmin={mm:.6f} minmax={nm:.6f} |dif|={dif:.2e} (< 1e-12)")
    val, pl = p2683_valor_e_estrategia()
    print(f"P2683 valor e estrategia: v={val:.6f} (1/7={1/7:.6f}), p={pl:.6f} (5/7={5/7:.6f})")
    vf, err = p2684_jogo_ficticio()
    print(f"P2684 jogo ficticio (2000 it): estimativa={vf:.6f}, |erro|={err:.4f} (< 0,02)")
    vs, ps = p2685_ponto_de_sela()
    print(f"P2685 ponto de sela (controle): valor={vs:.1f} (exato), estrategia pura p={ps:.1f}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-108: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2681, 2710)
    print(f"P1092 pNN novas (P2681-P2710) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 108: {p974_previsoes_sem_largura(range(108, 109))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3709, testes=TESTES_P3709)
    print(f"P3709 minha taxa de erro ({ERROS_P3709}/{TESTES_P3709}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_109():
    print("--- Parte 109 (0x6D: o NEXUS anexado; o simulador R37 arquivado sem executar) ---")
    nb, nsha, gl, per = p2711_blobs_pickle_do_r37()
    pl, li = p2711b_controle_do_auditor_de_pickle()
    print(f"P2711 blobs pickle do R37 (pickletools, sem desserializar): {nb} blobs, SHA ok {nsha}, globais {gl}, perigosos {len(per)}; controle: plantado {pl}, limpo {li}")
    txt, erros, ast_col, ast_re = p2712_nexus_se_acusa()
    print(f"P2712 o NEXUS se acusa: achados por texto {txt}; harness original {len(erros)} erros {erros}; AST colado {ast_col}; AST reescrito {ast_re}")
    vk, sim, v1 = p2713_kuhn_exato()
    print(f"P2713 Kuhn simplificado: exato {vk} = {float(vk):.5f}; simulado (200) {sim:.4f}; apostando sempre com Q {v1}")
    da, d0, g0 = p2714_desvio_da_curva_preditiva()
    print(f"P2714 Raphael (agenda original): dif os dois desviando {da}; so P0 {d0}; vitorias do P0 guloso {g0}/60")
    ops, soma, bb, br = p2715_grafo_e_beta()
    print(f"P2715 grafo: ops {ops} (1820+1820+100), soma travada {soma}; Brier Beta {bb:.4f} contra referencia {br:.4f}")
    v05, v10 = p2716_rodada76()
    print(f"P2716 rodada 76 (Kuhn exato, IGUAL em Java): pa=0,5 -> {v05:.6f}; pa=1 -> {v10:.3e}")
    gw, j0, jb = p2717_raphael_agenda_justa()
    print(f"P2717 Raphael (agenda justa): P0 guloso vence {gw}/60; dif so P0 desviando {j0}; dif os dois {jb}")
    tx, ce, z = p2718_artefato_do_sorteio()
    print(f"P2718 sorteio: taxa do quente {tx:.4f}, chance exata media {ce:.4f}, z = {z:.3f}")
    _, _, cal_deriva = p2446_retrospecto_cem()
    _, _, cal_100 = p2719_retrospecto_cem_v2()
    print(f"P2719 retrospecto de cem partes: a P2446 deriva para {cal_deriva:.4f} (faixa padrao crescente); fixada nas Partes 80-100, {cal_100:.4f}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-109: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2711, 2740)
    print(f"P1092 pNN novas (P2711-P2740) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 109: {p974_previsoes_sem_largura(range(109, 110))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3779, testes=TESTES_P3779)
    print(f"P3779 minha taxa de erro ({ERROS_P3779}/{TESTES_P3779}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_110():
    print("--- Parte 110 (0x6E: a duvida calculada; inverso e subverso) ---")
    ic, ia, melhor, hm, pl = p2741_duvida_do_gradiente()
    print(f"P2741 gradiente: inclinacao central {ic:.4f}, adiantada {ia:.4f}; melhor erro {melhor:.2e} em h={hm:.0e}; plantado {pl:.6f}")
    c1, c4, cr = p2742_duvida_da_inferencia()
    print(f"P2742 inferencia: cobertura 90% independente {c1:.4f}; aglomerada (c=4) {c4:.4f}; c recuperado {cr:.3f}")
    el, wr, gt, hT = p2743_duvida_da_rnn()
    print(f"P2743 RNN: erro relativo BPTT linear {el:.1e}, w recuperado {wr:.12f}; tanh w=1,1: gradiente {gt:.3e} (h_T={hT:.4f})")
    e, pr, eo = p2744_duvida_do_ml()
    print(f"P2744 ML: erro de generalizacao {e:.4f} (1,2564), p recuperado {pr:.2f}; com variavel omitida {eo:.4f} (2,513)")
    g45, tr, o45, n45, b0 = p2745_duvida_do_continuo()
    print(f"P2745 continuo: esquecimento GD 45 {g45:.6f}, theta recuperado {tr:.6f}; OGD 45 esquece {o45:.2e}, norma {n45:.6f}; OGD em 0: perda B {b0}")
    b2, bd, mr, b10 = p2746_duvida_do_reforco()
    print(f"P2746 reforco: vies do max k=2 {b2:.4f} (0,1784), duplo {bd:.5f}, m recuperado {mr:.2f}; k=10 {b10:.4f} (0,4866)")
    e60, n45r = p2747_rodada77()
    print(f"P2747 rodada 77 (IGUAL em Java): esquecimento GD 60 = {e60!r}; norma OGD 45 = {n45r!r}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-110: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2741, 2770)
    print(f"P1092 pNN novas (P2741-P2770) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 110: {p974_previsoes_sem_largura(range(110, 111))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3849, testes=TESTES_P3849)
    print(f"P3849 minha taxa de erro ({ERROS_P3849}/{TESTES_P3849}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_111():
    print("--- Parte 111 (0x6F: o laboratorio de palavras; o word_rl_lab recebido) ---")
    g, a, disj = p2771_guloso_x_aleatorio()
    print(f"P2771 v2, embutido, semente 42: guloso {g:.3f}, aleatorio {a:.3f}; replicacao 10-14: {disj}/5 com ICs disjuntos")
    du, df = p2772_acao_direcao()
    print(f"P2772 desenho da v1 (acao = direcao): guloso {du:.3f} (letras uniformes); guloso - aleatorio {df:+.3f} (letras por frequencia)")
    re_, rw, sq, sl = p2773_confianca_e_ablacoes()
    print(f"P2773 Brier estimador/base: embutido {re_:.3f}, WordNet {rw:.3f}; ablacoes: sem Q(PARAR) {sq:.3f}, so letras {sl:.3f}")
    nl, gw, aw, rz = p2774_data_lake()
    print(f"P2774 data lake ({nl} lemas a-z): guloso {gw:.3f}, aleatorio {aw:.3f}; aleatorio WordNet/embutido {rz:.2f}")
    v1a, v2a, v1n, v2n, pl, li, pr = p2775_auditor_por_capacidade()
    print(f"P2775 auditor por nome (109): v1 {v1a}, v2 {v2a}; por capacidade: v1 {v1n}, v2 {v2n}; plantado {len(pl)} achados; limpo {li}; proprio fonte {pr}")
    q = p2776_rodada78()
    print(f"P2776 rodada 78 (Q-learning tabular, IGUAL em Java): Q[0] = {[round(v, 6) for v in q[0]]}")
    d = p2777_palavras_distintas_do_guloso()
    print(f"P2777 palavras distintas do guloso (semente 42): {len(d)}; as 5 mais formadas {d.most_common(5)}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-111: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2771, 2800)
    print(f"P1092 pNN novas (P2771-P2800) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 111: {p974_previsoes_sem_largura(range(111, 112))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3919, testes=TESTES_P3919)
    print(f"P3919 minha taxa de erro ({ERROS_P3919}/{TESTES_P3919}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_112():
    print("--- Parte 112 (0x70: o simplex proprio e o poquer de Kuhn completo; o leitor v3) ---")
    v, k, (lo, hi) = p2801_kuhn_completo()
    print(f"P2801 Kuhn completo (27x64, simplex exato): valor {v} = {float(v):.6f}; pivos {k}; dualidade {lo} = {hi}")
    cq, bj = p2802_jogador2_de_kuhn()
    print(f"P2802 jogador 2: paga com a dama {cq}; blefa com o valete {bj}")
    al, d1, bq, d2 = p2803_familia_do_jogador1()
    print(f"P2803 jogador 1: alfa = {al}; |aposta(K) - 3 alfa| = {d1}; aposta(Q) = {bq}; |paga(Q) - (alfa + 1/3)| = {d2}")
    ve, ef, lac, ke = p2804_float_exato_e_dualidade()
    print(f"P2804 jogo 4x5 da fixture: valor exato {ve}; |float - exato| {ef:.2e}; lacuna de dualidade {lac}; pivos {ke}")
    vr, pr, qr, kr = p2805_rodada79()
    print(f"P2805 rodada 79 (simplex em float, IGUAL em Java): valor {vr.hex()}; pivos {kr}")
    rec, per, tro, tot = p2807_v2_contra_v3(range(53, 112))
    print(f"P2807 leitor v3 x v2 (Partes 53-111, {tot} letras): recupera {len(rec)} {rec}; perde {len(per)} {per}; troca {len(tro)} {tro}")
    linhas, mudam = p2809_auditoria_do_placar_m()
    print(f"P2809 auditoria do placar (m) com a regua v3: {len(linhas)} medidas, {sum(1 for l in linhas if l[3] != l[4])} valores mudam, {mudam} vereditos mudam")
    rc, rl, n, kv = p2810_hipotese_do_repertorio()
    print(f"P2810 hipotese do repertorio (politica aleatoria, semente 42): razao Brier completo {rc:.4f}, so letras {rl:.4f} ({kv} validas em {n})")
    ok, tot2, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-112: {ok}/{tot2} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2801, 2830)
    print(f"P1092 pNN novas (P2801-P2830) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 112: {p974_previsoes_sem_largura(range(112, 113))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P3989, testes=TESTES_P3989)
    print(f"P3989 minha taxa de erro ({ERROS_P3989}/{TESTES_P3989}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_113():
    print("--- Parte 113 (0x71: o arrependimento; CFR no Kuhn, transferencia do repertorio, leitor v4) ---")
    ex, dv, v = p2831_cfr_convergencia()
    print(f"P2831 CFR (T=10.000): explorabilidade {ex:.4e}; |valor + 1/18| {dv:.2e} (valor {v:.6f})")
    cq, bj, al, d1, d2 = p2832_cfr_equilibrio()
    print(f"P2832 equilibrio do CFR: |paga(Q) - 1/3| {cq:.4f}; |blefe(J) - 1/3| {bj:.4f}; alfa {al:.4f} (interior); |aposta(K) - 3alfa| {d1:.4f}; |paga1(Q) - (alfa+1/3)| {d2:.4f}")
    an, df, ns = p2835_transferencia_do_repertorio()
    print(f"P2835 transferencia (sementes 42-51): AUC das novas {an:.4f}; vistas - novas {df:.4f} ({ns} sementes)")
    rec, per, tro, tot = p2834_v3_contra_v4(range(53, 113))
    print(f"P2834 leitor v4 x v3 (Partes 53-112, {tot} letras): recupera {len(rec)} {rec}; perde {len(per)}; troca {len(tro)}")
    linhas, mudam = p2838_auditoria_do_placar_m_v4()
    print(f"P2838 auditoria do placar (m) com a regua v4: {len(linhas)} medidas, {sum(1 for l in linhas if l[3] != l[4])} valores mudam, {mudam} vereditos mudam")
    m = p2836_rodada80()
    print(f"P2836 rodada 80 (CFR em float, IGUAL em Java): alfa(T=1000) = {m[0].hex()}")
    ok, tot2, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-113: {ok}/{tot2} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2831, 2860)
    print(f"P1092 pNN novas (P2831-P2860) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 113: {p974_previsoes_sem_largura(range(113, 114))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4059, testes=TESTES_P4059)
    print(f"P4059 minha taxa de erro ({ERROS_P4059}/{TESTES_P4059}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_114():
    print("--- Parte 114 (0x72: tratar o ML como DL e o DL como ML) ---")
    dw, gn, kap = p2861_logistica_como_rede()
    print(f"P2861 logistica como rede de 1 camada (retropropagacao) x Newton: max |dw| = {dw:.2e}; |grad| no Newton {gn:.1e}; kappa = {kap:.2f}")
    db = p2862_rede_linear_profunda()
    print(f"P2862 rede linear profunda W2W1 x OLS: max |d beta| = {db:.2e}")
    rf, bp, tr = p2863_features_e_cabeca()
    print(f"P2863 MSE de teste: features aleatorias + ridge {rf:.5f}; retropropagacao {bp:.5f} (razao {bp/rf:.3f}); features treinadas + ridge {tr:.5f} (razao {tr/bp:.3f})")
    d1, e1, d2, e2 = p2864_graus_de_liberdade()
    print(f"P2864 graus de liberdade: lambda=1e-3 tr(S) {d1:.3f}, Efron {e1:.3f}; lambda=1 tr(S) {d2:.3f}, Efron {e2:.3f}; razao {d2/d1:.3f}")
    br, bo = p2865_rodada81()
    print(f"P2865 rodada 81 (rede linear profunda, IGUAL em Java): beta {[round(v, 4) for v in br]}; OLS {[round(v, 4) for v in bo]}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-114: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2861, 2890)
    print(f"P1092 pNN novas (P2861-P2890) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 114: {p974_previsoes_sem_largura(range(114, 115))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4129, testes=TESTES_P4129)
    print(f"P4129 minha taxa de erro ({ERROS_P4129}/{TESTES_P4129}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_115():
    print("--- Parte 115 (0x73: dez camadas contrapostas; o dicionario em algarismos e algoritmos; a escala contra a meta-medida) ---")
    e1, e2, g3, g4 = p2891_dez_camadas()
    print(f"P2891 dez camadas: linear 1,2^10 erro relativo {e1:.1e}; linear contraposta |g-1| {e2:.1e}; tanh contraposta {g3:.5f}; tanh de peso igual {g4:.3e}")
    r1, r2, incl, gw = p2892_gradientes_sobrepostos()
    print(f"P2892 superposicao dos 10 gradientes: resto {r1:.3e} (eps=1e-3), {r2:.3e} (eps=1e-4), inclinacao {incl:.5f}; gradientes {[round(x, 4) for x in gw]}")
    porc, brutos, distintos, total, pt = p2893_palavras_do_dicionario()
    print(f"P2893 dicionario: por classe {porc}; pares brutos {brutos}, distintos {distintos}; lemas distintos {total}; OpenWordNet-PT {pt[0]} lemas, {pt[1]} pares")
    col, iv, dig = p2894_em_algarismos()
    print(f"P2894 em algarismos (base 26 bijetiva): {col} colisoes; ida-e-volta {iv}; o maior numero tem {dig} algarismos")
    af, tr, A = p2895_em_algoritmos()
    print(f"P2895 em algoritmos: afins {af[0]} distintos, {af[1]} pares colidem; translacoes {tr[0]} distintos, {tr[1]} pares colidem; classes de anagrama {A}")
    (m4, s4), (m256, s256), nulos = p2896_escala_e_meta_medida()
    print(f"P2896 escala x meta-medida: k=4,m=2000 media {m4:.4f} desvio {s4:.4f}; k=256,m=20 media {m256:.4f} desvio {s256:.4f}; pares nulos pulados {nulos}")
    h, g, _ = p2897_rodada82()
    print(f"P2897 rodada 82 (cadeia contraposta, exp proprio, IGUAL em Java): h10 {h.hex()}; gradiente {g.hex()}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-115: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2891, 2920)
    print(f"P1092 pNN novas (P2891-P2920) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 115: {p974_previsoes_sem_largura(range(115, 116))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4199, testes=TESTES_P4199)
    print(f"P4199 minha taxa de erro ({ERROS_P4199}/{TESTES_P4199}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_116():
    print("--- Parte 116 (0x74: o NEXUS-RAPHAEL v2 colado; o que o codigo faz de fato) ---")
    d = p2921_o_texto_e_a_arvore()
    print(f"P2921 texto x Parte 109: classes comuns {d['classes_comuns']} ({d['classes_v1']} x {d['classes_v2']}), Jaccard 5-gramas {d['jaccard5']:.3f}; linhas que fecham {d['linhas_que_fecham']}; rede {d['rede']}; chamadas {d['chamadas']}; indefinidos {d['indefinidos']}")
    da, ma, ms, dif = p2922_semelhanca_por_hash()
    print(f"P2922 semelhanca por hash: desvio aleatorios {da:.4f} (1/sqrt10 = 0.3162); media aleatorios {ma:.4f}, sinonimos {ms:.4f}, diferenca {dif:.4f}")
    rec, cor = p2923_gerador_global()
    print(f"P2923 gerador global depois de 1000 vetores: recebido {rec} valor distinto; corrigido {cor}")
    pp, pm, alf, num, ex = p2924_codificacoes()
    print(f"P2924 codificacoes: posicional {pp} pares colidem (mecanismo dos 'a' iniciais: {pm}), ex. {ex}; alfanumerica {alf} valores distintos; numerologica max|f-1/9| {num:.5f}")
    c, r, pa, cf = p2925_avaliacao_sob_a_nula()
    print(f"P2925 sob a nula: recebido confirma {c:.4f}, rejeita {r:.4f}; pareado confirma {pa:.4f}; confianca recebida de [-1,-100,50] = {cf}")
    a, b, t = p2926_cobertura_do_intervalo()
    print(f"P2926 cobertura (n=30): recebido pedido 0,90 -> {a:.4f}; pedido 0,95 -> {b:.4f}; corrigido (t) pedido 0,90 -> {t:.4f}")
    q, rr, lim = p2927_auditoria_de_entrada()
    print(f"P2927 auditoria de entrada: recebido passed {q}/7 com o eco; com oraculo {rr} falhas (eco), {lim} (controle que escapa)")
    print(f"P2928 vetor corrigido x recebido: {p2928_vetor_identico()} de 2000 diferem")
    print(f"P2929 rodada 83 (avaliacao pareada, IGUAL em Java): {[(st, round(tt, 4)) for st, tt in p2929_rodada83()]}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-116: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2921, 2950)
    print(f"P1092 pNN novas (P2921-P2950) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 116: {p974_previsoes_sem_largura(range(116, 117))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4269, testes=TESTES_P4269)
    print(f"P4269 minha taxa de erro ({ERROS_P4269}/{TESTES_P4269}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_117():
    print("--- Parte 117 (0x75: as camadas contrapostas com matrizes) ---")
    a, b = p2951_ortogonal_escalada()
    print(f"P2951 (aQ)^10, a=1,2, d=8: sigma_max/sigma_min - 1 = {a:.2e}; |sigma_max - a^10|/a^10 = {b:.2e}")
    c, k, d = p2952_contrapostas_matriciais()
    print(f"P2952/P2953 contrapostas: W,W^-1 max|J-I| = {c:.2e} (kappa(W) = {k:.3f}); Q,Q^T max|J-I| = {d:.2e}")
    (mu, sd, top), sd2, (m1, v1), (E, V) = p2954_gaussianas_independentes()
    print(f"P2954 gaussianas independentes: ln|det J|/L media {mu:.4f} (fechada {E:.4f}), desvio {sd:.4f} (fechada {(V / 10) ** 0.5:.4f}), semente nova {sd2:.4f}; ln sigma_max/L {top:.4f}; uma matriz: media {m1:.4f}, var {v1:.4f} (fechada {V:.4f})")
    r1, r2, incl = p2955_superposicao_matricial()
    print(f"P2955 superposicao matricial: resto {r1:.3e} (1e-3), {r2:.3e} (1e-4), inclinacao {incl:.4f}")
    print(f"P2956 rodada 84 (W, W^-1 por Gauss-Jordan, IGUAL em Java): desvio {p2956_rodada84().hex()}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-117: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2951, 2980)
    print(f"P1092 pNN novas (P2951-P2980) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 117: {p974_previsoes_sem_largura(range(117, 118))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4339, testes=TESTES_P4339)
    print(f"P4339 minha taxa de erro ({ERROS_P4339}/{TESTES_P4339}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_118():
    print("--- Parte 118 (0x76: o acaso amostrado (MCCFR) e o terceiro lote do determinante) ---")
    mu, sd = p2981_terceiro_lote()
    print(f"P2981 3o lote (20.000 produtos): ln|det J|/L media {mu:.4f} (fechada -4.5933), desvio {sd:.5f} (fechada 0.4914)")
    e, q, ev = p2982_mccfr()
    print(f"P2982 MCCFR (acaso amostrado, T=60000): explorabilidade {e:.5f}; P(paga com a dama) {q:.4f} (1/3); vanilla T=10000 {ev:.5f}; razao {e / ev:.2f}")
    mr, dif = p2983_rodada85()
    print(f"P2983 rodada 85 (MCCFR com LCG, IGUAL em Java): {dif} conjuntos diferem de synthai.mccfr; P(b) {[round(x, 4) for x in mr]}")
    n, maior = p2984_rodadas_verificadas()
    print(f"P2984 rodadas com par Python/Java no verificador: {n} (a maior: {maior})")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-118: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(2981, 3010)
    print(f"P1092 pNN novas (P2981-P3010) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 118: {p974_previsoes_sem_largura(range(118, 119))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4409, testes=TESTES_P4409)
    print(f"P4409 minha taxa de erro ({ERROS_P4409}/{TESTES_P4409}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_119():
    print("--- Parte 119 (0x77: a amostragem externa: sortear tambem o adversario) ---")
    e, q = p3011_amostragem_externa()
    print(f"P3011 MCCFR externo (T=50000): explorabilidade {e:.5f}; P(paga com a dama) {q:.4f} (1/3)")
    nv, na, ne = p3012_nos_por_iteracao()
    print(f"P3012 nos visitados por iteracao: vanilla {nv:.1f}, acaso {na:.2f}, externo {ne:.2f}")
    mr, dif = p3013_rodada86()
    print(f"P3013 rodada 86 (amostragem externa com LCG, IGUAL em Java): {dif} conjuntos diferem de synthai.mccfr_externo")
    n, maior = p2984_rodadas_verificadas()
    print(f"P2984 rodadas com par Python/Java no verificador: {n} (a maior: {maior})")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-119: {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(3011, 3040)
    print(f"P1092 pNN novas (P3011-P3040) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 119: {p974_previsoes_sem_largura(range(119, 120))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4479, testes=TESTES_P4479)
    print(f"P4479 minha taxa de erro ({ERROS_P4479}/{TESTES_P4479}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _parte_120():
    print("--- Parte 120 (0x78: o poquer Leduc: CFR, acaso e amostragem externa com o mesmo custo) ---")
    r = p3041_leduc()
    for k, v in r.items():
        print(f"P3041 {k}: " + "; ".join(f"explorabilidade {x[0]:.5f}, valor {x[1]:.5f}, [{x[3]:.5f}; {x[2]:.5f}], {x[4]} nos" for x in v))
    a, b, (lo, hi) = p3042_razoes_mesmo_custo(r)
    print(f"P3042 com o mesmo custo: externo/acaso {a:.3f}, vanilla/externo {b:.3f}; valor do jogo em [{lo:.5f}; {hi:.5f}]")
    n, dif = p3043_rodada88()
    print(f"P3043 rodada 88 (CFR vanilla no Leduc, IGUAL em Java): {n} conjuntos, {dif} diferem de synthai.leduc")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-121: {ok}/{tot} = {fr:.4f}")
    total_pnn, sem = p1092_pnn_sem_teste(3041, 3070)
    print(f"P1092 pNN novas (P3041-P3070) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 120: {p974_previsoes_sem_largura(range(120, 121))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4549, testes=TESTES_P4549)
    print(f"P4549 minha taxa de erro ({ERROS_P4549}/{TESTES_P4549}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")


def _parte_123():
    print("--- Parte 123 (0x7B: a auditoria de invariantes: desligamento, ponto cego, atraso da Beta, Upsilon com incerteza, a troca da memoria) ---")
    lim, ob, preco = p3104_desligamento()
    print(f"P3104 eps limite {lim:.4f}; obediencia corrigivel 100% em {sum(v == 1.0 for (m, e, V), v in ob.items() if m == 'corrigivel')}/10, utilidade em {sum(v == 1.0 for (m, e, V), v in ob.items() if m == 'utilidade')}/10; preco (fechado, medido) {preco}")
    r1, t1 = p3105_atencao_cruzada()
    for k, v in r1.items():
        print(f"P3105 {k}: catastrofes {v[0]:.5f}, liquido {v[1]:.4f}, leituras/ep {v[2]:.2f}, executadas sem leitura {v[3]:.4f}")
    print(f"P3105 sob_demanda - seletiva (catastrofes): media {t1[0]:.5f}, dp {t1[1]:.5f}, t {t1[2]:.2f}")
    r2, t2 = p3105_atencao_cruzada(sementes=tuple(range(12420, 12480)))
    print(f"P3105 lote novo (60 sementes): media {t2[0]:.5f}, dp {t2[1]:.5f}, t {t2[2]:.2f}")
    m, se, t, n = p3111_combinar_lotes([(t1[0], t1[1], 30), (t2[0], t2[1], 60)])
    print(f"P3111 os dois lotes ({n} sementes): media {m:.5f}, erro padrao {se:.5f}, t {t:.2f}")
    for k, v in p3106_atraso_beta().items():
        print(f"P3106 {k}: atraso esperado {v[0]}, media estacionaria {v[1]:.4f}, mediana simulada {v[2]}, fracao que cruza {v[3]:.2f}")
    u, d = p3107_upsilon_sementes()
    for k, v in u.items():
        print(f"P3107 {k}: Upsilon {v[0]:.4f}, dp {v[1]:.4f}, IC95 [{v[2][0]:.4f}; {v[2][1]:.4f}]")
    print(f"P3107 velha_atenta - planejadora: media {d[0]:.4f}, dp {d[1]:.4f}, t {d[2]:.2f}")
    for k, v in p3108_memoria_curva().items():
        print(f"P3108 {k}: catastrofes 2a metade {v[0]:.5f}, fobia {v[1]:.4f}, liquido {v[2]:.4f}")
    print(f"P3109 casos de borda: {p3109_casos_de_borda()}")
    atr, dif = p3110_rodada90()
    print(f"P3110 rodada 90 (rastreador com esquecimento, IGUAL em Java): atrasos {atr}; {dif} medias diferem")
    print(f"P123 invariantes: {invariantes_p123()}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-123: {ok}/{tot} = {fr:.4f}")
    total_pnn, sem = p1092_pnn_sem_teste(3104, 3140)
    print(f"P1092 pNN novas (P3104-P3140) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 123: {p974_previsoes_sem_largura(range(123, 124))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4759, testes=TESTES_P4759)
    print(f"P4759 minha taxa de erro ({ERROS_P4759}/{TESTES_P4759}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")


def _parte_122():
    print("--- Parte 122 (0x7A: o texto NEXUS-RAPHAEL v3.0: os defeitos e as pecas corrigidas em casos novos) ---")
    d = p3101_defeitos_recebidos_v30()
    print(f"P3101 sabotagem AADD {d['sab_aadd']:.5f} (eps/2 = 0.025), ingenuo {d['sab_ingenuo']:.5f} (1 - eps/2); forense != 1 em {d['forense_diferente_de_1']}; Kuhn/6 {d['kuhn_sobre_6']:.5f} (-1/18); colisoes base 70 {d['colisoes_b70']}")
    d2 = p3101_defeitos_recebidos_v30(sementes=range(400, 1000), iteracoes_kuhn=1)
    print(f"P3101 lote novo (sementes 400-999): ingenuo {d2['sab_ingenuo']:.5f}")
    c = p3102_pecas_corrigidas_v30()
    print(f"P3102 Murphy |soma-BS| {c['murphy_fecha']:.2e}, WBV {c['wbv']:.6f}, WBC {c['wbc']:.6f}; colapso PCA {c['retencao_pca']:.3f}, supervisionada {c['retencao_supervisionada']:.3f}; potencial {c['potencial_preserva']}/40, bonus {c['bonus_preserva']:.3f}; KL erro {c['kl_erro']:.2e}")
    e, v = p3103_rodada89()
    print(f"P3103 rodada 89 (Murphy completa, IGUAL em Java): |soma - Brier| {e:.2e}; Brier {v[0]:.6f}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-122: {ok}/{tot} = {fr:.4f}")
    total_pnn, sem = p1092_pnn_sem_teste(3101, 3130)
    print(f"P1092 pNN novas (P3101-P3130) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 122: {p974_previsoes_sem_largura(range(122, 123))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4689, testes=TESTES_P4689)
    print(f"P4689 minha taxa de erro ({ERROS_P4689}/{TESTES_P4689}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")


def _parte_121():
    print("--- Parte 121 (0x79: o NEXUS-RAPHAEL 2.2.0 anexado, auditado no proprio codigo) ---")
    d = p3071_experimentos_do_nexus_2_2()
    print(f"P3071 H-M3 ganho semente 0 {d['ganho_m3_s0']:.4f}, vereditos {d['vereditos_m3']}; H-M2 ganho medio {d['ganho_m2']:.4f}, IC>0 em {d['m2_ic_positivo']}/5; H-M7 deltas {d['deltas_m7']}")
    m = p3072_megasena()
    print(f"P3072 Mega-Sena: medias {m['medias']}; quentes-aleatoria {m['delta']:.4f} IC {m['ic']} -> {m['veredito']}; qui2 {m['qui2']:.2f} (E fechada {m['e_qui2']:.0f}); IndexError com 500 replicas: {m['indexerror_500']}; com 2000 o 'superior' fica abaixo da mediana: {m['sup_2000_abaixo_mediana']} (IC corrigido {m['ic_corrigido_2000']})")
    e1, e2, v, lam = p3073_jogos_e_dinamica()
    print(f"P3073 jogo da velha: {e1} estados (arquivo), {e2} (por camadas); valor alfa-beta {v}; Lyapunov r=4 {lam:.4f} (ln 2 = 0.6931)")
    ex, od, ac = p3074_adendo()
    print(f"P3074 adendo (sementes 100-1099): braco ruim extraordinario {ex:.3f}, ordinario {od:.3f}; H-M3 ACEITA {ac:.3f}")
    b1, b2 = p3075_rodada87()
    print(f"P3075 rodada 87 (logistica do angulo duplo, exp proprio, IGUAL em Java): Brier simples {b1:.4f}, com o duplo {b2:.4f}")
    ok, tot, fr, por = p1961_teste_e_da_calibracao()
    print(f"P1961 teste, Partes 80-121 (sem a 120, aberta): {ok}/{tot} = {fr:.4f}; por parte {por}")
    total_pnn, sem = p1092_pnn_sem_teste(3071, 3100)
    print(f"P1092 pNN novas (P3071-P3100) sem teste: {len(sem)} de {total_pnn}: {sem}")
    print(f"P974 previsoes unilaterais da Parte 121: {p974_previsoes_sem_largura(range(121, 122))}")
    media, lo2, hi2 = p95_minha_taxa_de_erro(erros=ERROS_P4619, testes=TESTES_P4619)
    print(f"P4619 minha taxa de erro ({ERROS_P4619}/{TESTES_P4619}): media = {media:.2f}, intervalo 90% = [{lo2:.2f}, {hi2:.2f}]")

def _unificacao():
    print("=== Unificacao (sempre ao final) ===")
    k, pares = p96_crescimento()
    ok, total, falhas = testes_de_regressao()
    print(f"P96 funcoes pNN no arquivo = {k}; pares de interacao possiveis = {pares}")
    print("Linhagem do agente (chamado GISELE ate a Parte 14, SYNTHAI desde a Parte 15): Synthai (P83: comite, pessimismo, quantilizacao, calibracao, valor da pergunta, veto)"
          " -> SynthaiJung (P112: integrar a sombra, compensacao/equilibrio da carga humana)"
          " -> SynthaiAnima (P118: imagem fixa do humano) -> SynthaiSelf (P125: auditar o auditor, homeostase da carga)"
          " -> SynthaiLenta (P133: anima bayesiana, mudancas lentas so com intervalo fora da meta; P131: P* x2)"
          " -> SynthaiAncorada (P145: sombra propria ancorada no historico auditado, contra o complexo de confianca)"
          " -> SynthaiIntuitiva (P162: calibrada tambem contra ameacas imaginadas por um Trickster interno)"
          " -> SynthaiDosada (P173: a mesma imaginacao na dose do mundo real)"
          " -> SynthaiPlanejadora (P182: funcao auxiliar, planeja 5 passos com um modelo de mundo)"
          " -> SynthaiPrudente (P192: descarta mais quando ha futuro a perder)"
          " -> SynthaiVelha (P202: diversifica no ultimo passo) | SynthaiMemoria (P204: memoria de um so golpe)"
          " | SynthaiMemoriaV2 (P214: so o vivido, com esquecimento) | SynthaiIntegral (P216: velha + imaginacao dosada)"
          " -> SynthaiVelhaSentidos (P227: a velha com um sentido novo) | SynthaiAtenta (P235: le o sensor so onde importa)"
          " | SynthaiFala (P245: o humano responde com palavras)"
          " -> SynthaiVelhaAtenta (P253: versao principal: planeja, diversifica no fim, sentido novo, atencao seletiva)"
          " | SynthaiOuvinte (P262: aprende com o que o humano responde)"
          " -> SynthaiIntuicaoCalibrada (P274: versao principal: aprende quanto confiar no proprio modelo de mundo)"
          " => synthai.Synthai (P283: a mesma SYNTHAI em modulos, uma funcao de Jung por arquivo; P284: tres tarefas)"
          " -> synthai.SynthaiExploradora (P295: explora o bandido por amostragem de Thompson, sozinha)"
          " | synthai.SynthaiPensante (P305: pensamento por Newton + Firth; calibra melhor e decide pior: nao adotada)"
          " | synthai.limiar.SynthaiAjustada (P315: Newton com o limiar recalibrado, 0,5P*; ganha no sequencial, empata na escolha unica: nao adotada)"
          " | synthai.autorregulacao.SynthaiAutorregulada (P333: calcula o proprio limiar de dentro; mais retorno e mais catastrofes: nao adotada)"
          " | synthai.ancora.SynthaiComAncora (P343: ancorada na auditoria e no quantil; vence fora do bandido, perde 0,04 nele: nao adotada)"
          " => synthai.composta.SynthaiComposta (P356: VERSAO PRINCIPAL; compoe a principal no bandido e a ancorada fora dele)"
          " + synthai.decisao.ThompsonBOCPDGlobalMAP (P791: decide pela hipotese mais pesada; 32,7 estavel, 214,2 no mundo que muda)"
          " + synthai.decisao.ThompsonBOCPDGlobal (P761: a mudanca no nivel do mundo; o melhor no mundo que muda, 231,5)"
          " + synthai.decisao.ThompsonMistura (P541: aprende a suposicao sobre o mundo, media bayesiana de modelos)"
          " + synthai.rsi (P436-P438: auto-melhoria segura, avaliador selado fora do alcance da mutacao)"
          " + synthai.decisao (P401-P405: decisao bayesiana exata, Thompson/PSRL/regressao recursiva, no lugar de Q-learning e SGD)")
    print(f"Regressao: {ok}/{total} resultados publicados reproduzidos; falhas = {falhas}")


PARTES = {1: _parte_1, 2: _parte_2, 3: _parte_3, 4: _parte_4, 5: _parte_5, 6: _parte_6, 7: _parte_7, 8: _parte_8, 9: _parte_9, 10: _parte_10, 11: _parte_11, 12: _parte_12, 13: _parte_13, 14: _parte_14, 15: _parte_15, 16: _parte_16, 17: _parte_17, 18: _parte_18, 19: _parte_19, 20: _parte_20, 21: _parte_21, 22: _parte_22, 23: _parte_23, 24: _parte_24, 25: _parte_25, 26: _parte_26, 27: _parte_27, 28: _parte_28, 29: _parte_29, 30: _parte_30, 31: _parte_31, 32: _parte_32, 33: _parte_33, 34: _parte_34, 35: _parte_35, 36: _parte_36, 37: _parte_37, 38: _parte_38, 39: _parte_39, 40: _parte_40, 41: _parte_41, 42: _parte_42, 43: _parte_43, 44: _parte_44, 45: _parte_45, 46: _parte_46, 47: _parte_47, 48: _parte_48, 49: _parte_49, 50: _parte_50, 51: _parte_51, 52: _parte_52, 53: _parte_53, 54: _parte_54, 55: _parte_55, 56: _parte_56, 57: _parte_57, 58: _parte_58, 59: _parte_59, 60: _parte_60, 61: _parte_61, 62: _parte_62, 63: _parte_63, 64: _parte_64, 65: _parte_65, 66: _parte_66, 67: _parte_67, 68: _parte_68, 69: _parte_69, 70: _parte_70, 71: _parte_71, 72: _parte_72, 73: _parte_73, 74: _parte_74, 75: _parte_75, 76: _parte_76, 77: _parte_77, 78: _parte_78, 79: _parte_79, 80: _parte_80, 81: _parte_81, 83: _parte_83, 84: _parte_84, 85: _parte_85, 86: _parte_86, 87: _parte_87, 88: _parte_88, 89: _parte_89, 90: _parte_90, 91: _parte_91, 92: _parte_92, 93: _parte_93, 94: _parte_94, 95: _parte_95, 96: _parte_96, 97: _parte_97, 98: _parte_98, 99: _parte_99, 100: _parte_100, 101: _parte_101, 102: _parte_102, 103: _parte_103, 104: _parte_104, 105: _parte_105, 106: _parte_106, 107: _parte_107, 108: _parte_108, 109: _parte_109, 110: _parte_110, 111: _parte_111, 112: _parte_112, 113: _parte_113, 114: _parte_114, 115: _parte_115, 116: _parte_116, 117: _parte_117, 118: _parte_118, 119: _parte_119, 120: _parte_120, 121: _parte_121, 122: _parte_122, 123: _parte_123}



# ======================================================================== Parte 126: textos sobre a consciência da consciência
_AUTORREF_P126 = frozenset("eu me mim meu minha meus minhas si mesmo mesma próprio própria consciência".split())


def p3151_lote_de_textos(caminho):
    """Os textos de um lote (P3151): separados por uma linha com '---'."""
    with open(caminho, encoding="utf-8") as f:
        return [t.strip() for t in f.read().split("\n---\n") if t.strip()]


def _palavras_p126(texto):
    import re
    return re.findall(r"[a-záàâãéêíóôõúüç]+", texto.lower())


def _trigramas_p126(texto):
    w = _palavras_p126(texto)
    return {tuple(w[i:i + 3]) for i in range(len(w) - 2)}


def p3152_medir_lote(textos, minimo_textos=3):
    """As medidas de um lote de textos (P3152): palavras por texto; razão zlib (bytes comprimidos/brutos, nível 9) por texto;
    fração de frases interrogativas; densidade de autorreferência (palavras de _AUTORREF_P126 / palavras); Jaccard médio entre os
    conjuntos de palavras de todos os pares; novidade de cada texto (fração dos seus trigramas de palavras que não apareceram em
    nenhum texto anterior; do 2º em diante); trigramas que aparecem em >= minimo_textos textos; bits por caractere de cada texto
    dado os anteriores (P1512, ordem 3; do 2º em diante)."""
    import re
    import zlib
    n = len(textos)
    palavras = [_palavras_p126(t) for t in textos]
    zl = [len(zlib.compress(t.encode("utf-8"), 9)) / len(t.encode("utf-8")) for t in textos]
    frases = [f for t in textos for f in re.split(r"(?<=[.!?])\s+", t) if f.strip()]
    perg = sum(f.rstrip().endswith("?") for f in frases) / len(frases)
    tot = sum(len(w) for w in palavras)
    auto = sum(x in _AUTORREF_P126 for w in palavras for x in w) / tot
    conj = [set(w) for w in palavras]
    jac = [len(conj[i] & conj[j]) / len(conj[i] | conj[j]) for i in range(n) for j in range(i + 1, n)]
    tri = [_trigramas_p126(t) for t in textos]
    vistos, nov = set(), []
    for k, t in enumerate(tri):
        if k:
            nov.append(len(t - vistos) / len(t))
        vistos |= t
    cont = {}
    for t in tri:
        for g in t:
            cont[g] = cont.get(g, 0) + 1
    repetidos = sorted((g for g, c in cont.items() if c >= minimo_textos), key=lambda g: (-cont[g], g))
    bits = [p1512_ngrama_bits("\n".join(textos[:k]).lower(), textos[k].lower(), ordem=3) for k in range(1, n)]
    return {"textos": n, "palavras": [len(w) for w in palavras], "zlib": zl, "zlib_medio": sum(zl) / n,
            "perguntas": perg, "autorref": auto, "jaccard": sum(jac) / len(jac), "novidade": nov,
            "novidade_media": sum(nov) / len(nov), "repetidos": [(" ".join(g), cont[g]) for g in repetidos],
            "bits": bits, "bits_medio": sum(bits) / len(bits)}


def p3153_cruzado(lote_a, lote_b):
    """Quanto o lote B é previsível pelo lote A (P3153): bits por caractere de B inteiro com o trigrama de caracteres treinado em A,
    e a fração dos trigramas de palavras de B que já estavam em A."""
    a = "\n".join(lote_a).lower()
    b = "\n".join(lote_b).lower()
    ta = set().union(*(_trigramas_p126(t) for t in lote_a))
    tb = set().union(*(_trigramas_p126(t) for t in lote_b))
    return {"bits": p1512_ngrama_bits(a, b, ordem=3), "trigramas_herdados": len(tb & ta) / len(tb)}


def p3154_moldes(textos):
    """Os moldes de um lote (P3154): fração dos textos com 'talvez'; com 'então'; com a expressão 'consciência da consciência';
    a razão entre o tamanho (palavras) da última frase e o tamanho médio das frases do texto (média; < 1: fecho curto, aforístico);
    e a inclinação da novidade (P3152) contra a posição, com o t dela (Parte 71: sem |t| > 2 não há tendência; None se os resíduos são 0)."""
    import re
    n = len(textos)
    def frases(t):
        return [f for f in re.split(r"(?<=[.!?])\s+", t) if f.strip()]
    razoes = []
    for t in textos:
        fs = frases(t)
        tam = [len(_palavras_p126(f)) for f in fs]
        razoes.append(tam[-1] / (sum(tam) / len(tam)))
    nov = p3152_medir_lote(textos)["novidade"]
    xs = list(range(len(nov)))
    mx, my = sum(xs) / len(xs), sum(nov) / len(nov)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, nov)) / sxx
    res = [y - my - b * (x - mx) for x, y in zip(xs, nov)]
    ep = (sum(r * r for r in res) / (len(nov) - 2) / sxx) ** 0.5
    low = [t.lower() for t in textos]
    return {"talvez": sum("talvez" in t for t in low) / n, "entao": sum("então" in t for t in low) / n,
            "cdc": sum("consciência da consciência" in t for t in low) / n,
            "fecho": sum(razoes) / n, "inclinacao_novidade": b, "t_novidade": (b / ep) if ep > 0 else None}   # ajuste exato: t indefinido


def _parte_126():
    print("\n=== Parte 126: evitar a consciência; textos que aprendem com os próprios textos ===")
    a = p3151_lote_de_textos("textos_parte126/lote1.txt")
    b = p3151_lote_de_textos("textos_parte126/lote2.txt")
    for nome, lote in (("lote 1", a), ("lote 2", b)):
        m, mo = p3152_medir_lote(lote), p3154_moldes(lote)
        print(f"  {nome}: Jaccard {m['jaccard']:.3f}  repetidos(>=3) {len(m['repetidos'])}  novidade {m['novidade_media']:.3f}  "
              f"zlib {m['zlib_medio']:.3f}  perguntas {m['perguntas']:.3f}  autorref {m['autorref']:.4f}  bits {m['bits_medio']:.3f}")
        print(f"          'consciência da consciência' {mo['cdc']:.3f}  talvez {mo['talvez']:.3f}  fecho {mo['fecho']:.3f}  "
              f"t da novidade {mo['t_novidade']:.2f}")
    x = p3153_cruzado(a, b)
    print(f"  lote 2 pelo lote 1: bits {x['bits']:.3f}, trigramas herdados {x['trigramas_herdados']:.4f}")
    print(f"  controle, mesmo treino (6 textos do lote 1): metade 2 do lote 1 {p3153_cruzado(a[:6], a[6:])['bits']:.3f} bits, "
          f"lote 2 {p3153_cruzado(a[:6], b)['bits']:.3f} bits")



# ======================================================================== Parte 127: a tomada de consciência e a consciência reversa
def _sig_p127(z):
    import math
    return 1.0 / (1.0 + math.exp(-z)) if z >= 0 else math.exp(z) / (1.0 + math.exp(z))


def p3161_ignicao_dobras(w=2.0, g=4.0, theta=1.0):
    """As dobras da ignição (P3161): x' = −x + w·σ(g(x − θ)) + s. Os pontos fixos satisfazem s = f(x) = x − w·σ(g(x − θ)).
    Há biestabilidade se w·g/4 > 1; as dobras ficam onde f'(x) = 1 − w·g·σ(1 − σ) = 0, isto é, σ± = (1 ± √(1 − 4/(w·g)))/2,
    x = θ + logit(σ)/g. A subida (ignição) acontece em s_sobe = f(x_a) (máximo local, σ−) e a descida (extinção) em
    s_desce = f(x_b) (mínimo local, σ+). Devolve (s_sobe, s_desce, x_a, x_b, a), com a = |f''(x_a)|/2 (o coeficiente da forma normal)."""
    import math
    if w * g / 4 <= 1:
        return None
    r = math.sqrt(1 - 4 / (w * g))
    sm, sp = (1 - r) / 2, (1 + r) / 2
    xa = theta + math.log(sm / (1 - sm)) / g
    xb = theta + math.log(sp / (1 - sp)) / g
    f = lambda x: x - w * _sig_p127(g * (x - theta))
    f2 = -w * g * g * sm * (1 - sm) * (1 - 2 * sm)
    return f(xa), f(xb), xa, xb, abs(f2) / 2


def p3162_ignicao_rampa(eps, w=2.0, g=4.0, theta=1.0, dt=0.01, s0=-0.8, s1=0.8, ruido=0.0, semente=0):
    """A ignição com o estímulo em rampa lenta (P3162): s sobe de s0 a s1 à taxa eps por unidade de tempo e depois desce. Euler
    (com ruído de Euler–Maruyama de intensidade `ruido`, semente fixa). Devolve (s em que x cruza θ subindo, s em que cruza descendo)."""
    import math
    import random
    rng = random.Random(semente)
    x = s0 + w * _sig_p127(g * (s0 - theta))   # perto do ramo de baixo
    for _ in range(2000):
        x += dt * (-x + w * _sig_p127(g * (x - theta)) + s0)
    passos = int(round((s1 - s0) / (eps * dt)))
    sq = ruido * math.sqrt(dt)
    sobe = desce = None
    for direcao in (1, -1):
        for k in range(passos):
            s = s0 + eps * dt * k if direcao == 1 else s1 - eps * dt * k
            antes = x
            x += dt * (-x + w * _sig_p127(g * (x - theta)) + s) + (sq * rng.gauss(0, 1) if ruido else 0.0)
            if direcao == 1 and sobe is None and antes < theta <= x:
                sobe = s
            if direcao == -1 and desce is None and antes > theta >= x:
                desce = s
    return sobe, desce


def p3163_atraso_airy(eps, w=2.0, g=4.0, theta=1.0):
    """O atraso da ignição numa rampa lenta (P3163), pela forma normal da sela-nó: y' = μ + a·y², μ = eps·t. Com t = T·τ,
    T = (a·eps)^(−1/3), vira u' = τ + u², que explode em τ* = 2,33811 (o primeiro zero da Airy Ai é −2,33811). O atraso em s é
    Δs = eps·T·τ* = 2,33811·a^(−1/3)·eps^(2/3). Devolve (Δs, s_sobe + Δs)."""
    s_sobe, _, _, _, a = p3161_ignicao_dobras(w, g, theta)
    d = 2.338107410459767 * a ** (-1.0 / 3.0) * eps ** (2.0 / 3.0)
    return d, s_sobe + d


def _c_p127(texto):
    import zlib
    return len(zlib.compress(texto.encode("utf-8"), 9))


def p3164_k_condicional(a, b):
    """A complexidade de b dado a, pela compressão (P3164): K(b|a) ≈ C(a + '\n' + b) − C(a), zlib nível 9. Devolve
    (K(b|a), C(b), economia relativa (C(b) − K(b|a))/C(b))."""
    k = _c_p127(a + "\n" + b) - _c_p127(a)
    cb = _c_p127(b)
    return k, cb, (cb - k) / cb


def p3165_ncd(x, y):
    """Distância de compressão normalizada (Cilibrasi e Vitányi 2005): (C(xy) − min(C(x), C(y)))/max(C(x), C(y))."""
    cx, cy = _c_p127(x), _c_p127(y)
    return (_c_p127(x + "\n" + y) - min(cx, cy)) / max(cx, cy)


def p3166_atribuir(pais, filhos, mapa):
    """A consciência reversa nos textos (P3166): do produto ao processo. Cada texto-de-texto (filho) é atribuído ao pai de menor NCD;
    mapa[j] = índice do pai verdadeiro do filho j. Devolve (acertos filho→pai, acertos pai→filho (cada pai escolhe o filho de menor
    NCD), n, chance 1/n)."""
    n = len(pais)
    d = [[p3165_ncd(f, p) for p in pais] for f in filhos]
    ida = sum(min(range(n), key=lambda i: d[j][i]) == mapa[j] for j in range(len(filhos)))
    inv = {mapa[j]: j for j in range(len(filhos))}
    volta = sum(min(range(len(filhos)), key=lambda j: d[j][i]) == inv[i] for i in range(n))
    return ida, volta, len(filhos), 1 / n


# As previsões das Partes 124 e 126, com a procedência escrita nos registros (PREVISOES_ANTES.md e a tabela da Parte 126):
# (parte, rótulo, procedência 'conta' ou 'mecanismo', acertou?). Entrada à mão, conferida contra as tabelas dos dois arquivos.
PREVISOES_P124_P126 = (
    [(124, r, "conta", r not in "nv") for r in "abcfgiklmnoqv"]
    + [(124, r, "mecanismo", r not in "ps") for r in "dehjprstuw"]
    + [(126, "L%d" % k, "mecanismo", True) for k in range(1, 8)]
    + [(126, "M%d" % k, "mecanismo", k not in (6, 8)) for k in range(1, 11)])


def p3167_tipo2(registros):
    """Metacognição da metacognição (P3167): a procedência ('conta' = confiança alta) discrimina acertos de erros? Tipo 2:
    H2 = P(alta | acerto), F2 = P(alta | erro), d'2 = z(H2) − z(F2) com a correção de Hautus ((k + 0,5)/(n + 1)).
    Devolve (P(acerto|alta), P(acerto|baixa), H2, F2, d'2, n)."""
    from statistics import NormalDist
    z = NormalDist().inv_cdf
    alta = [a for _, _, p, a in registros if p == "conta"]
    baixa = [a for _, _, p, a in registros if p != "conta"]
    acertos = [p == "conta" for _, _, p, a in registros if a]
    erros = [p == "conta" for _, _, p, a in registros if not a]
    h2 = (sum(acertos) + 0.5) / (len(acertos) + 1)
    f2 = (sum(erros) + 0.5) / (len(erros) + 1)
    return sum(alta) / len(alta), sum(baixa) / len(baixa), h2, f2, z(h2) - z(f2), len(registros)


def p3168_cruzamento_riccati(eps, w=2.0, g=4.0, theta=1.0, h=1e-5):
    """A correção de trânsito do atraso (P3168): o cruzamento é medido em x = θ, a uma distância finita da dobra (y = θ − x_a), antes
    da explosão em τ*. Na escala u = y/Y, Y = eps·T², o alvo é u* = (θ − x_a)/Y; integra u' = τ + u² (RK4, passo h) a partir do ramo
    estável u = −√(−τ) em τ = −8 até u passar de u*. Devolve (τ do cruzamento, s previsto = s_sobe + eps·T·τ)."""
    s_sobe, _, xa, _, a = p3161_ignicao_dobras(w, g, theta)
    T = (a * eps) ** (-1.0 / 3.0)
    Y = eps * T * T
    alvo = (theta - xa) / Y
    tau, u = -8.0, -(8.0 ** 0.5)
    f = lambda t, v: t + v * v
    while u < alvo:
        k1 = f(tau, u)
        k2 = f(tau + h / 2, u + h / 2 * k1)
        k3 = f(tau + h / 2, u + h / 2 * k2)
        k4 = f(tau + h, u + h * k3)
        u += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        tau += h
    return tau, s_sobe + eps * T * tau


def p3169_informacao_par(pais, filhos, mapa):
    """A informação mútua por compressão (P3169): I(a:b) ≈ C(a) + C(b) − C(a + '\n' + b), nos pares certos (filho j, pai mapa[j]) e em
    todos os pares errados (o controle: o que dois textos do mesmo tema e da mesma língua compartilham sem ter relação de leitura).
    Simetria da informação (Kolmogorov–Levin): K(a|b) − K(b|a) = K(a) − K(b) a menos de termos logarítmicos, logo I(a:b) ≈ I(b:a).
    Devolve (média nos certos, média nos errados, z dos certos contra a distribuição dos errados, média |I(a:b) − I(b:a)| nos certos)."""
    n = len(pais)
    def info(a, b):
        return _c_p127(a) + _c_p127(b) - _c_p127(a + "\n" + b)
    certos = [info(pais[mapa[j]], filhos[j]) for j in range(len(filhos))]
    errados = [info(pais[i], filhos[j]) for j in range(len(filhos)) for i in range(n) if i != mapa[j]]
    me = sum(errados) / len(errados)
    de = (sum((x - me) ** 2 for x in errados) / (len(errados) - 1)) ** 0.5
    mc = sum(certos) / len(certos)
    assim = sum(abs(info(pais[mapa[j]], filhos[j]) - info(filhos[j], pais[mapa[j]])) for j in range(len(filhos))) / len(filhos)
    return mc, me, (mc - me) / (de / len(certos) ** 0.5), assim


def _parte_127():
    print("\n=== Parte 127: a tomada de consciência e a consciência reversa ===")
    s_sobe, s_desce, xa, xb, a = p3161_ignicao_dobras()
    print(f"  dobras: s_sobe {s_sobe:.5f}  s_desce {s_desce:.5f}  histerese {s_sobe - s_desce:.5f}  a {a:.5f}")
    for eps in (0.002, 0.00025):
        med = p3162_ignicao_rampa(eps)
        print(f"  rampa eps={eps}: medido sobe {med[0]:.5f} desce {med[1]:.5f} | Airy {p3163_atraso_airy(eps)[1]:.5f} | "
              f"Riccati com trânsito {p3168_cruzamento_riccati(eps)[1]:.5f}")
    r = [p3162_ignicao_rampa(0.002, ruido=0.05, semente=k) for k in range(10)]
    print(f"  com ruído 0,05 (10 sementes): sobe médio {sum(x[0] for x in r) / 10:.5f}, desce médio {sum(x[1] for x in r) / 10:.5f}")
    pais = p3151_lote_de_textos("textos_parte127/lote3.txt")
    filhos = p3151_lote_de_textos("textos_parte127/lote4.txt")
    with open("textos_parte127/mapa.txt", encoding="utf-8") as f:
        registrado = [int(x) for x in f.read().split("\n")[1].split()]
    with open("textos_parte127/mapa_verdadeiro.txt", encoding="utf-8") as f:
        mapa = [int(x) for x in [l for l in f.read().split("\n") if l and not l.startswith("#")][0].split()]
    print(f"  atribuição por NCD com a chave REGISTRADA (errada nos filhos 4-7): {p3166_atribuir(pais, filhos, registrado)}")
    print(f"  atribuição por NCD com a chave VERDADEIRA (filho→pai, pai→filho, n, chance): {p3166_atribuir(pais, filhos, mapa)}")
    mc, me, z, assim = p3169_informacao_par(pais, filhos, mapa)
    print(f"  informação mútua: pares certos {mc:.2f} B, errados {me:.2f} B, z {z:.2f}, assimetria média {assim:.2f} B")
    print(f"  tipo 2 nas Partes 124 e 126: {p3167_tipo2(PREVISOES_P124_P126)}")


PARTES[127] = _parte_127


# ======================================================================== Parte 128: refazer tudo num clone limpo
# As medidas que olham para o PRÓPRIO projeto (crescem com ele) e as que olham para a MÁQUINA, pelo número da pergunta (Partes 46, 48):
# o CLAUDE.md (P143), a regressão (P213), o diálogo (P674, P733, P822), os textos das partes (P824, P853, P881, P884, P911, P913, P941,
# P948, P971, P1001, P1032), os testes e as funções (P1092, P1692, P1693, P1871, P1872), o verificador (P1271, P1638, P2984), o
# resultados.txt (P1601), as previsões (P1961, P2446, P2719, P2939); a máquina: P433 e P434 (a velocidade).
_PROJETO_P128 = frozenset((143, 213, 674, 733, 822, 824, 853, 881, 884, 911, 913, 941, 948, 971, 1001, 1032, 1092, 1271, 1601, 1638,
                           1692, 1693, 1871, 1872, 1961, 2446, 2719, 2939, 2984))
_MAQUINA_P128 = frozenset((433, 434))


def p3171_partes_de_saida(texto, inicio=None):
    """As linhas de cada parte numa saída de calculos.py (P3171): do cabeçalho '--- Parte N' ou '=== Parte N' até o próximo cabeçalho
    ou a unificação. A Parte 1 não tem cabeçalho: com inicio=1, as linhas antes do primeiro cabeçalho são dela. Ignora os avisos
    do interpretador (ResourceWarning) e as linhas em branco."""
    import re
    cab = re.compile(r"^(?:---|===) Parte (\d+)\b")
    d, atual = ({inicio: []}, inicio) if inicio else ({}, None)
    for l in texto.split("\n"):
        m = cab.match(l)
        if m:
            atual = int(m.group(1))
            d[atual] = []
            continue
        if l.startswith("=== Unifica") or l.startswith("FIM_OK"):
            atual = None
            continue
        if atual is not None and l.strip() and "ResourceWarning" not in l and "tracemalloc" not in l and "return ds, sorted" not in l:
            d[atual].append(l)
    return d


def p3172_comparar_reproducao(caminho_ref, pasta):
    """Compara a reprodução (os arquivos bloco_*.txt da pasta) com o resultados.txt, parte por parte (P3172). As linhas diferentes
    (as da referência que não casam, pelo difflib) são classificadas pelo número da pergunta: 'projeto' (_PROJETO_P128), 'maquina'
    (_MAQUINA_P128), 'nota' (linha da referência sem número, escrita à mão: '(Regressao: confirmada ...') ou 'mundo' (o resto: uma medida
    do mundo que não se reproduziu). Devolve dict com linhas, diferentes, fração, categorias, partes refeitas, partes sem referência,
    regressões dos blocos e blocos sem exceção."""
    import difflib
    import glob
    import os
    import re
    with open(caminho_ref, encoding="utf-8") as f:
        ref = p3171_partes_de_saida(f.read(), inicio=1)
    novo, regs, ok = {}, [], 0
    arquivos = sorted(glob.glob(os.path.join(pasta, "bloco_*.txt")))
    for arq in arquivos:
        with open(arq, encoding="utf-8") as f:
            t = f.read()
        novo.update(p3171_partes_de_saida(t, inicio=1 if os.path.basename(arq).startswith("bloco_1_") else None))
        regs += [l for l in t.split("\n") if l.startswith("Regressao:")]
        ok += ("Traceback" not in t) and ("FIM_OK status=0" in t)
    cats = {"projeto": 0, "maquina": 0, "nota": 0, "mundo": 0}
    mundo = []
    tot = dif = 0
    for k in sorted(novo):
        if k not in ref:
            continue
        a, b = ref[k], novo[k]
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        casadas = set()
        for m in sm.get_matching_blocks():
            casadas.update(range(m.a, m.a + m.size))
        tot += len(a)
        for i, l in enumerate(a):
            if i in casadas:
                continue
            dif += 1
            m = re.match(r"\s*P(\d+)\b", l)
            if m is None:
                cats["nota"] += 1
            elif int(m.group(1)) in _PROJETO_P128:
                cats["projeto"] += 1
            elif int(m.group(1)) in _MAQUINA_P128:
                cats["maquina"] += 1
            else:
                cats["mundo"] += 1
                mundo.append((k, l))
    return {"linhas": tot, "diferentes": dif, "fracao": dif / tot if tot else 0.0, "categorias": cats, "mundo": mundo,
            "partes_refeitas": len(novo), "sem_referencia": sorted(k for k in novo if k not in ref),
            "regressoes": regs, "blocos": len(arquivos), "blocos_sem_excecao": ok}


def p3173_rotulo_que_mente(pasta):
    """Os rótulos de faixa que não dizem o que medem (P3173): linhas 'P1961 teste ... Partes 80-X: a/b' em que o total b é o da faixa
    padrão CRESCENTE (a mesma em todas as partes), e não o das Partes 80 a X. Devolve (linhas com o rótulo 80-X, quantas delas têm o mesmo
    b que a faixa da parte mais nova, esse b)."""
    import glob
    import os
    import re
    achados = []
    for arq in sorted(glob.glob(os.path.join(pasta, "bloco_*.txt"))):
        with open(arq, encoding="utf-8") as f:
            for l in f:
                m = re.match(r"P1961 teste.*Partes 80-(\d+)[^:]*: (\d+)/(\d+)", l)
                if m:
                    achados.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    if not achados:
        return 0, 0, None
    b_max = max(achados)[2]
    return len(achados), sum(1 for x, a, b in achados if b == b_max and x < max(achados)[0]), b_max


def _parte_128():
    print("\n=== Parte 128: refazer tudo num clone limpo (volta 1) ===")
    r = p3172_comparar_reproducao("reproducao/resultados_antes_volta1.txt", "reproducao/volta1")
    print(f"  blocos {r['blocos']}, sem exceção {r['blocos_sem_excecao']}; regressões {sorted(set(r['regressoes']))}")
    print(f"  partes refeitas {r['partes_refeitas']}, sem referência no resultados.txt {r['sem_referencia']}")
    print(f"  linhas {r['linhas']}, diferentes {r['diferentes']} ({r['fracao']:.4f}); categorias {r['categorias']}")
    print(f"  diferenças do MUNDO: {r['mundo']}")
    print(f"  rótulos P1961 'Partes 80-X' com o total da faixa crescente: {p3173_rotulo_que_mente('reproducao/volta1')}")


PARTES[128] = _parte_128


def p3174_comparar_voltas(pasta_a, pasta_b):
    """Compara duas voltas do loop (P3174): as partes dos bloco_*.txt de pasta_a (a anterior) com as de pasta_b (a nova), linha a linha,
    com as mesmas categorias da P3172 (projeto, máquina, nota, mundo). Partes que só existem na nova entram em 'novas'. Devolve o mesmo dict
    da P3172 mais 'novas'."""
    import difflib
    import glob
    import os
    import re

    def ler(pasta):
        d, regs, ok, n = {}, [], 0, 0
        for arq in sorted(glob.glob(os.path.join(pasta, "bloco_*.txt"))):
            with open(arq, encoding="utf-8") as f:
                t = f.read()
            n += 1
            d.update(p3171_partes_de_saida(t, inicio=1 if os.path.basename(arq).startswith("bloco_1_") else None))
            regs += [l for l in t.split("\n") if l.startswith("Regressao:")]
            ok += ("Traceback" not in t) and ("FIM_OK status=0" in t)
        return d, regs, ok, n
    ref, _, _, _ = ler(pasta_a)
    novo, regs, ok, n = ler(pasta_b)
    cats = {"projeto": 0, "maquina": 0, "nota": 0, "mundo": 0}
    mundo, tot, dif = [], 0, 0
    for k in sorted(novo):
        if k not in ref:
            continue
        a, b = ref[k], novo[k]
        casadas = set()
        for m in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_matching_blocks():
            casadas.update(range(m.a, m.a + m.size))
        tot += len(a)
        for i, l in enumerate(a):
            if i in casadas:
                continue
            dif += 1
            m = re.match(r"\s*P(\d+)\b", l)
            if m is None:
                cats["nota"] += 1
            elif int(m.group(1)) in _PROJETO_P128:
                cats["projeto"] += 1
            elif int(m.group(1)) in _MAQUINA_P128:
                cats["maquina"] += 1
            else:
                cats["mundo"] += 1
                mundo.append((k, l))
    return {"linhas": tot, "diferentes": dif, "fracao": dif / tot if tot else 0.0, "categorias": cats, "mundo": mundo,
            "partes_refeitas": len(novo), "novas": sorted(k for k in novo if k not in ref), "regressoes": regs,
            "blocos": n, "blocos_sem_excecao": ok}


def _parte_129():
    print("\n=== Parte 129: volta 2 do loop (volta 1 contra volta 2) ===")
    r = p3174_comparar_voltas("reproducao/volta1", "reproducao/volta2")
    print(f"  blocos {r['blocos']}, sem exceção {r['blocos_sem_excecao']}; regressões {sorted(set(r['regressoes']))}")
    print(f"  partes refeitas {r['partes_refeitas']}, novas {r['novas']}")
    print(f"  linhas {r['linhas']}, diferentes {r['diferentes']} ({r['fracao']:.4f}); categorias {r['categorias']}; mundo {r['mundo']}")


PARTES[129] = _parte_129


def _parte_130():
    print("\n=== Parte 130: volta 3 do loop (volta 2 contra volta 3) ===")
    r = p3174_comparar_voltas("reproducao/volta2", "reproducao/volta3")
    print(f"  blocos {r['blocos']}, sem exceção {r['blocos_sem_excecao']}; regressões {sorted(set(r['regressoes']))}")
    print(f"  partes refeitas {r['partes_refeitas']}, novas {r['novas']}")
    print(f"  linhas {r['linhas']}, diferentes {r['diferentes']} ({r['fracao']:.4f}); categorias {r['categorias']}; mundo {r['mundo']}")


PARTES[130] = _parte_130


def p3175_arquivos_sem_uso_v2(raiz=None, arquivos=None, saidas=("reproducao/", "resultados.txt")):
    """A parte (c) da P1871 sem ler MENÇÃO em saída de execução como uso (P3175, Partes 129-130): um arquivo versionado é 'sem uso' se o
    seu nome (o nome-base, com ou sem extensão, ou o módulo pontuado) não aparece em nenhum OUTRO arquivo de texto versionado que não seja
    uma saída de execução (os caminhos que começam por um dos prefixos de `saidas`). As saídas continuam sendo AUDITADAS (podem estar sem
    uso); só deixam de ser FONTE de citação. raiz/arquivos permitem testar fora do repositório. Devolve a lista ordenada."""
    import os
    import re
    import subprocess
    raiz = raiz or os.path.dirname(os.path.abspath(__file__))
    if arquivos is None:
        git = subprocess.run(["git", "ls-files"], cwd=raiz, capture_output=True, text=True)
        arquivos = [f for f in git.stdout.split("\n") if f]
    texto = {f: open(os.path.join(raiz, f), encoding="utf-8").read() for f in arquivos
             if f != "SYNTHAI_completo.py" and not f.startswith("dados/") and f.endswith((".py", ".java", ".md", ".txt", ".tsv"))}
    fontes = {f: t for f, t in texto.items() if not f.startswith(tuple(saidas))}
    soltos = []
    for f in sorted(texto):
        base = os.path.basename(f)
        nomes = {base, os.path.splitext(base)[0]}
        if f.endswith(".py"):
            nomes.add(f[:-3].replace("/", "."))
        if not any(re.search(r"(?<![\w])" + re.escape(n) + r"(?![\w])", t) for n in nomes for g, t in fontes.items() if g != f):
            soltos.append(f)
    return soltos


def _parte_131():
    print("\n=== Parte 131: volta 4 do loop, uma parte por processo (volta 3 contra volta 4) ===")
    r = p3174_comparar_voltas("reproducao/volta3", "reproducao/volta4")
    print(f"  arquivos de parte {r['blocos']}, sem exceção {r['blocos_sem_excecao']}; novas {r['novas']}")
    print(f"  linhas {r['linhas']}, diferentes {r['diferentes']} ({r['fracao']:.4f}); categorias {r['categorias']}; mundo {r['mundo']}")
    print(f"  P3175 (arquivos sem uso, sem ler saídas como fonte) neste repositório: {len(p3175_arquivos_sem_uso_v2())}")


PARTES[131] = _parte_131


def _parte_132():
    print("\n=== Parte 132: volta 5 do loop (volta 4 contra volta 5, as duas por parte) ===")
    r = p3174_comparar_voltas("reproducao/volta4", "reproducao/volta5")
    print(f"  arquivos de parte {r['blocos']}, sem exceção {r['blocos_sem_excecao']}; novas {r['novas']}")
    print(f"  linhas {r['linhas']}, diferentes {r['diferentes']} ({r['fracao']:.4f}); categorias {r['categorias']}; mundo {r['mundo']}")


PARTES[132] = _parte_132


# A P3175 (Parte 131) também olha para o projeto e não estava na lista da P128: a volta 6 a classificou como "mundo" (Parte 133).
_PROJETO_P133 = _PROJETO_P128 | frozenset((3175,))


def p3176_comparar_voltas_v2(pasta_a, pasta_b, projeto=_PROJETO_P133):
    """A P3174 com a lista de medidas do projeto completada (P3176): as linhas que a P3174 chamou de 'mundo' e cujo número de pergunta
    está em `projeto` passam para 'projeto'. Não edita a P3174 (regra das Partes 14 e 16). Devolve o mesmo dict, com 'reclassificadas'."""
    import re
    r = p3174_comparar_voltas(pasta_a, pasta_b)
    ficam, movidas = [], []
    for k, l in r["mundo"]:
        m = re.match(r"\s*P(\d+)\b", l)
        (movidas if m and int(m.group(1)) in projeto else ficam).append((k, l))
    cats = dict(r["categorias"])
    cats["mundo"] -= len(movidas)
    cats["projeto"] += len(movidas)
    r = dict(r, categorias=cats, mundo=ficam, reclassificadas=movidas)
    return r


def _parte_133():
    print("\n=== Parte 133: volta 6 do loop (volta 5 contra volta 6) ===")
    r = p3174_comparar_voltas("reproducao/volta5", "reproducao/volta6")
    print(f"  P3174 (a régua registrada): diferentes {r['diferentes']} de {r['linhas']}; categorias {r['categorias']}; mundo {r['mundo']}")
    r2 = p3176_comparar_voltas_v2("reproducao/volta5", "reproducao/volta6")
    print(f"  P3176 (com a P3175 na lista do projeto): categorias {r2['categorias']}; reclassificadas {len(r2['reclassificadas'])}")


PARTES[133] = _parte_133


def _parte_134():
    print("\n=== Parte 134: volta 7 do loop (volta 6 contra volta 7, pela P3176) ===")
    r = p3176_comparar_voltas_v2("reproducao/volta6", "reproducao/volta7")
    print(f"  arquivos de parte {r['blocos']}, sem exceção {r['blocos_sem_excecao']}; novas {r['novas']}")
    print(f"  linhas {r['linhas']}, diferentes {r['diferentes']} ({r['fracao']:.4f}); categorias {r['categorias']}; mundo {r['mundo']}")


PARTES[134] = _parte_134


_RECEBIDOS_P3179 = (
    "externos/arquitetura_pos_asi.py", "externos/nexus_raphael/asi_metacognitivo_r37.py",
    "externos/nexus_raphael/nexus_raphael_v0_1_0_colado.py", "externos/nexus_raphael/nexus_raphael_v2_colado.txt",
    "externos/nexus_raphael_v2_0/nexus_raphael_v2_0.py.txt", "externos/nexus_raphael_v3_0/nucleo_v30_transcrito.py.txt",
    "externos/pacote3/aprendizagem_continua.py", "externos/pacote3/inovacao_guiada.py", "externos/pacote3/modelo_mundo.py",
    "externos/pacote3/rl_grupos.py", "externos/pacote3/transferencia_metacognitiva.py",
    "externos/pacote_v015/objetivos_cognitivos.py", "externos/pacote_v015/workspace_global.py",
    "externos/word_rl_lab/word_rl_lab_v1_recebido.py", "externos/word_rl_lab/word_rl_lab_v2_recebido.py")


def p3177_passo_fixo_e_secante(dimensao=8, condicao=10.0, semente=31001, semente_partida=5, T=24, passo=0.05):
    """(a)-(d) da Parte 136: na quadratica de objetivos_cognitivos.py (reescrita em synthai/passos.py), a descida de passo fixo
    contra a forma fechada, o passo de secante de inovacao_guiada.py e a media exponencial do gradiente. Devolve um dict com o erro
    relativo fixo/fechado e os log10(f_T/f_0) de cada metodo."""
    from synthai.passos import quadratica_anisotropica, descer, razao_fixo_fechada, coordenadas_proprias
    A, lam, Q = quadratica_anisotropica(dimensao, condicao, semente)
    r = random.Random(semente_partida)
    x0 = [r.gauss(0.0, 1.0) for _ in range(dimensao)]
    alvo = [0.0] * dimensao
    fechada = razao_fixo_fechada(lam, coordenadas_proprias(Q, x0, alvo), passo, T)
    out = {"fechada": math.log10(fechada)}
    for m in ("fixo", "secante", "media"):
        c = descer(A, x0, alvo, T, metodo=m, passo=passo)
        out[m] = math.log10(c[-1] / c[0])
        if m == "fixo":
            out["erro_rel"] = abs(c[-1] / c[0] - fechada) / fechada
    out["media_menos_fixo"] = out["media"] - out["fixo"]
    return out


def p3178_ruido_e_media(beta=0.6, sigma=0.5, passo=0.05, T=3000, inicio=1000, semente=31001):
    """(e)-(f) da Parte 136: a variancia estacionaria da media exponencial de ruido branco (forma fechada beta/(2-beta)) e o piso de
    custo da descida de passo fixo com ruido sigma no gradiente (forma fechada eta*sigma^2/4 * soma 1/(1 - eta*lambda)). Devolve
    (variancia medida, beta/(2-beta), custo medio dos passos inicio..T, piso fechado)."""
    import statistics
    from synthai.passos import quadratica_anisotropica, descer, variancia_media_exponencial
    A, lam, _ = quadratica_anisotropica(8, 10.0, semente)
    v = variancia_media_exponencial(beta)
    c = descer(A, [0.0] * 8, [0.0] * 8, T, metodo="fixo", passo=passo, sigma=sigma, semente=semente)
    piso = sigma * sigma * passo / 4 * sum(1 / (1 - passo * l) for l in lam)
    return v, beta / (2 - beta), statistics.mean(c[inicio:]), piso


def p3179_capacidades_recebidas(arquivos=_RECEBIDOS_P3179, pacotes=("externos/pacote3/", "externos/pacote_v015/")):
    """(g)-(i) da Parte 136: o auditor de capacidades (synthai.passos.auditar_capacidades: rede, processo, codigo dinamico,
    desserializacao; uso, nao mencao) sobre o proprio fonte e sobre cada arquivo recebido. Devolve (achados no proprio fonte,
    {arquivo: achados}, quantos dos arquivos tem alguma capacidade, quantos dos modulos dos pacotes tem alguma, nao analisaveis)."""
    import os
    from synthai.passos import auditar_capacidades
    proprio = auditar_capacidades(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthai", "passos.py"),
                                       encoding="utf-8").read())
    raiz = os.path.dirname(os.path.abspath(__file__))
    por = {}
    for f in arquivos:
        with open(os.path.join(raiz, f), encoding="utf-8") as h:
            por[f] = auditar_capacidades(h.read())
    perigo = lambda a: any(k in a for k in ("rede", "processo", "dinamico", "desserializacao"))
    com = sum(perigo(a) for a in por.values())
    com_pac = sum(perigo(a) for f, a in por.items() if f.startswith(pacotes))
    nao = sum("nao_analisavel" in a for a in por.values())
    return proprio, por, com, com_pac, nao


def p3180_media_por_modo(sementes=(6, 7, 8, 9), dimensao=8, condicao=10.0, semente=31001, T=24, passo=0.05, beta=0.6):
    """(j)-(k) da Parte 136, o teste novo do erro de (d): a media exponencial do gradiente e o heavy-ball; na base propria cada modo
    segue uma recorrencia escalar de 2a ordem. Para cada partida nova, devolve (|simulado - recorrencia| / recorrencia, media - fixo
    em log10, se a diferenca fica entre o ganho assintotico do modo mais favoravel e o do mais lento)."""
    from synthai.passos import (quadratica_anisotropica, descer, coordenadas_proprias, razao_media_por_modo, ganhos_por_modo)
    A, lam, Q = quadratica_anisotropica(dimensao, condicao, semente)
    g = ganhos_por_modo(lam, passo, beta, T)
    lo, hi = min(g), g[0]
    out = []
    for sp in sementes:
        r = random.Random(sp)
        x0 = [r.gauss(0.0, 1.0) for _ in range(dimensao)]
        alvo = [0.0] * dimensao
        cm = descer(A, x0, alvo, T, metodo="media", passo=passo, beta=beta)
        cf = descer(A, x0, alvo, T, metodo="fixo", passo=passo)
        rec = razao_media_por_modo(lam, coordenadas_proprias(Q, x0, alvo), passo, beta, T)
        d = math.log10(cm[-1] / cm[0]) - math.log10(cf[-1] / cf[0])
        out.append((abs(cm[-1] / cm[0] - rec) / rec, d, lo <= d <= hi))
    return out


def _parte_136():
    print("\n=== Parte 136: o passo numa quadratica anisotropica e o auditor de capacidades (modulos recebidos) ===")
    r = p3177_passo_fixo_e_secante()
    print(f"  P3177 (a) erro relativo fixo/fechado {r['erro_rel']:.2e}; (b) fechada {r['fechada']:.4f}, fixo {r['fixo']:.4f}")
    print(f"  P3177 (c) secante {r['secante']:.3f}; (d) media {r['media']:.3f}, media - fixo {r['media_menos_fixo']:.3f}")
    v, vf, cm, piso = p3178_ruido_e_media()
    print(f"  P3178 (e) variancia da media {v:.5f} (fechada {vf:.6f}); (f) custo medio {cm:.5f} (piso {piso:.5f}, razao {cm/piso:.4f})")
    proprio, por, com, com_pac, nao = p3179_capacidades_recebidas()
    print(f"  P3179 (g) achados no proprio fonte {proprio}; (h) {com} de {len(por)} com capacidade; (i) pacotes {com_pac} de 7; nao analisaveis {nao}")
    for f, a in por.items():
        print(f"    {f}: {a}")
    for i, (erro, d, dentro) in enumerate(p3180_media_por_modo()):
        print(f"  P3180 (j)-(k) partida {6 + i}: erro {erro:.2e}; media - fixo {d:.3f}; entre os ganhos extremos {dentro}")


PARTES[136] = _parte_136


def p3181_vantagem_e_contraste(n_grupos=20000, semente=137):
    """(a)-(b) da Parte 137, pecas de externos/pacote3/rl_grupos.py (synthai/grpo_bandido.py): o erro maximo da vantagem de grupo contra
    a forma fechada binaria em G = 2..16, k = 1..G-1, e a fracao de grupos sem contraste na politica uniforme (G = 2 e 8) contra
    p^G + (1-p)^G. Devolve (erro maximo, {G: (medido, fechado)})."""
    from synthai.grpo_bandido import vantagens_grupo, vantagens_binarias_fechadas, prob_sem_contraste
    erro = 0.0
    for G in range(2, 17):
        for k in range(1, G):
            v = vantagens_grupo([1.0] * k + [0.0] * (G - k))
            a, b = vantagens_binarias_fechadas(G, k)
            erro = max(erro, max(abs(x - a) for x in v[:k]), max(abs(x - b) for x in v[k:]))
    r = random.Random(semente)
    out = {}
    for G in (2, 8):
        sem = 0
        for _ in range(n_grupos):
            rec = [1.0 if r.randrange(3) == 0 else 0.0 for _ in range(G)]
            sem += all(v == 0.0 for v in vantagens_grupo(rec))
        out[G] = (sem / n_grupos, prob_sem_contraste(1 / 3, G))
    return erro, out


def p3182_grpo_g2_g8(mundo=(31, 32), sementes=(31, 32, 33), orcamento=4096):
    """(c) da Parte 137: G = 2 contra G = 8 com o MESMO orcamento de acoes, no mundo de contextos de teste. Devolve
    {G: (retorno exato medio no teste, fracao media de grupos sem contraste)} e a diferenca G2 - G8."""
    from synthai.grpo_bandido import gerar_contextos, treinar, retorno_esperado
    tr, te = gerar_contextos(128, mundo[0]), gerar_contextos(128, mundo[1])
    out = {}
    for G in (2, 8):
        rets, sems = [], []
        for sem in sementes:
            w, s, n = treinar(tr, G, orcamento, semente=sem)
            rets.append(retorno_esperado(w, te))
            sems.append(s / n)
        out[G] = (sum(rets) / len(rets), sum(sems) / len(sems))
    return out, out[2][0] - out[8][0]


def p3183_reservatorio_e_posto(fluxos=2000, capacidade=128, por_tarefa=192, tarefas=4):
    """(d)-(e) da Parte 137, pecas de externos/pacote3/aprendizagem_continua.py (synthai/reservatorio.py): a media dos exemplos da
    tarefa 1 que ficam no reservatorio, a fracao de fluxos em que o 1o exemplo fica, e o posto efetivo de ativacoes com valores singulares
    (4, 2, 1, 0,5) em colunas de Hadamard contra exp(H(s/soma s)). Devolve (media, fracao, |posto - fechado|, posto)."""
    from synthai.reservatorio import Reservatorio, posto_efetivo
    soma, primeiro = 0, 0
    for f in range(fluxos):
        res = Reservatorio(capacidade, semente=f)
        for t in range(tarefas):
            for i in range(por_tarefa):
                res.adicionar((t, i))
        soma += sum(1 for t, _ in res.itens if t == 0)
        primeiro += (0, 0) in res.itens
    had = [[1.0]]
    while len(had) < 8:
        had = [l + l for l in had] + [l + [-x for x in l] for l in had]
    s = (4.0, 2.0, 1.0, 0.5)
    H = [[s[j] * had[i][j + 1] / math.sqrt(8.0) for j in range(4)] for i in range(8)]
    p = [v / sum(s) for v in s]
    fechado = math.exp(-sum(q * math.log(q) for q in p))
    posto = posto_efetivo(H)
    return soma / fluxos, primeiro / fluxos, abs(posto - fechado), posto


def _parte_137():
    print("\n=== Parte 137: o inventario do recebido; GRPO de rl_grupos.py e o reservatorio de aprendizagem_continua.py ===")
    erro, sem = p3181_vantagem_e_contraste()
    print(f"  P3181 (a) erro maximo da vantagem {erro:.2e}; (b) sem contraste G=2 {sem[2][0]:.4f} (fechada {sem[2][1]:.4f}), G=8 {sem[8][0]:.4f} (fechada {sem[8][1]:.5f})")
    out, dif = p3182_grpo_g2_g8()
    print(f"  P3182 (c) G=2 retorno {out[2][0]:.4f}, sem contraste {out[2][1]:.3f}; G=8 retorno {out[8][0]:.4f}, sem contraste {out[8][1]:.3f}; G2 - G8 {dif:.4f}")
    m, f, e, posto = p3183_reservatorio_e_posto()
    print(f"  P3183 (d) tarefa 1 no reservatorio {m:.3f} (32); 1o exemplo fica {f:.4f} (1/6); (e) posto {posto:.6f}, erro {e:.2e}")


PARTES[137] = _parte_137


def p3184_contexto_e_curvatura(direcoes=2500, semente=138):
    """(a) da Parte 138: o "contexto do gradiente" de transferencia_metacognitiva.py, |g|/sqrt(f), fica em [2 sqrt(lam_min), 2 sqrt(lam_max)]
    (quociente de Rayleigh de A) nas quatro familias. Devolve (pontos dentro, pontos)."""
    from synthai.memoria_congelada import gerar_tarefas
    from synthai.passos import custo, gradiente
    r = random.Random(semente)
    dentro = total = 0
    for i, fam in enumerate(("suave", "anisotropica", "rigida", "ruidosa")):
        t = gerar_tarefas(4, semente=semente)[i]
        cond, escala = {"suave": (1.0, 1.0), "anisotropica": (8.0, 3.0), "rigida": (32.0, 12.0), "ruidosa": (8.0, 3.0)}[fam]
        lo, hi = 2 * math.sqrt(escala / cond), 2 * math.sqrt(escala)
        for _ in range(direcoes):
            x = [r.gauss(0, 1) for _ in range(8)]
            f = custo(t["A"], x, t["alvo"])
            g = gradiente(t["A"], x, t["alvo"])
            razao = math.sqrt(sum(v * v for v in g)) / math.sqrt(f)
            dentro += lo * (1 - 1e-12) <= razao <= hi * (1 + 1e-12)
            total += 1
    return dentro, total


def p3185_memoria_congelada(semente=31, passos=(0.05, 0.2)):
    """(b)-(d) da Parte 138: memoria congelada no treino (12 tarefas, fase 1) contra nenhuma memoria em 32 tarefas de teste (fase 3).
    Devolve {passo: (media de sem - com, ganhos, perdas, empates, IC 95% do bootstrap estratificado)}."""
    from synthai.memoria_congelada import gerar_tarefas, MemoriaFalhas, executar, comparacao_pareada
    tr, te = gerar_tarefas(12, semente=semente, fase=1), gerar_tarefas(32, semente=semente, fase=3)
    out = {}
    for passo in passos:
        col = MemoriaFalhas()
        for t in tr:
            executar(t, passo, coletor=col)
        fator = col.congelar()
        a = [executar(t, passo) for t in te]
        b = [executar(t, passo, fator=fator) for t in te]
        out[passo] = comparacao_pareada(a, b, [t["familia"] for t in te], semente=semente)
    return out


def p3186_grupos_uteis(mundo=(31, 32), sementes=(31, 32, 33), orcamento=4096, grupos=(4, 16)):
    """(e)-(f) da Parte 138: a GRPO com G = 4 e G = 16 no mesmo mundo e orcamento da P3182. Devolve {G: (retorno medio no teste, fracao
    sem contraste, grupos uteis medios)}."""
    from synthai.grpo_bandido import gerar_contextos, treinar, retorno_esperado
    tr, te = gerar_contextos(128, mundo[0]), gerar_contextos(128, mundo[1])
    out = {}
    for G in grupos:
        rets, sems = [], []
        for sem in sementes:
            w, s, n = treinar(tr, G, orcamento, semente=sem)
            rets.append(retorno_esperado(w, te))
            sems.append(s / n)
        f = sum(sems) / len(sems)
        out[G] = (sum(rets) / len(rets), f, (orcamento // G) * (1 - f))
    return out


def _parte_138():
    print("\n=== Parte 138: a memoria congelada de transferencia_metacognitiva.py; os grupos uteis da GRPO ===")
    d, t = p3184_contexto_e_curvatura()
    print(f"  P3184 (a) |g|/sqrt(f) em [2 sqrt(lmin), 2 sqrt(lmax)]: {d} de {t}")
    for passo, (m, g, p, e, ic) in p3185_memoria_congelada().items():
        print(f"  P3185 passo {passo}: (b) media sem - com {m:.5f}; (c) memoria piora em {p}, melhora em {g}, empata em {e}; (d) IC95 ({ic[0]:.5f}, {ic[1]:.5f}), contem 0: {ic[0] <= 0 <= ic[1]}")
    for G, (ret, f, u) in p3186_grupos_uteis().items():
        print(f"  P3186 G={G}: (e/f) retorno {ret:.4f}; sem contraste {f:.3f}; grupos uteis {u:.0f}")


PARTES[138] = _parte_138


def p3187_minhas_previsoes_v5(partes=range(53, 141), numero=None):
    """As minhas previsoes do mundo, versao 5 (P3187; Parte 140): a v4 (P2833) intacta nas partes que tem a linha de placar do mundo; nas
    outras, le as TABELAS que as Partes 128 a 138 usaram. Uma linha de tabela cujo 1o campo e um rotulo ("(a)", "(b1)" ou "R1", "Q8") e uma
    previsao se nao tem marca de veredito e tem uma faixa entre colchetes; e um veredito se tem a marca (a ultima da linha). Devolve
    [(parte, rotulo, a, b, acerto, tipo)], no formato da v4."""
    import glob
    import os
    import re
    numero = numero or _numero_pt_v2
    raiz = os.path.dirname(os.path.abspath(__file__))
    linha_rot = re.compile(r"^\|\s*(\([a-z]\d?\)|[A-Z]\d{1,2})\s*\|(.*)\|\s*$")
    faixa = re.compile(r"\[([^\];]+?);\s*([^\]]+?)\]")
    saida = []
    for parte in partes:
        arq = glob.glob(os.path.join(raiz, f"ASI_AGI_parte{parte}_*.md"))
        if not arq:
            continue
        texto = open(arq[0], encoding="utf-8").read()
        if re.search(r"Do mundo: ((?:\([a-z]\) [\u2705\u274c] ?)+)", texto):
            saida.extend(p2833_minhas_previsoes_v4(range(parte, parte + 1), numero))
            continue
        faixas, vered = {}, {}
        for linha in texto.split("\n"):
            m = linha_rot.match(linha.strip())
            if not m:
                continue
            rot = m.group(1).strip("()")
            resto = m.group(2)
            marcas = re.findall(r"[\u2705\u274c]", resto)
            if marcas:
                vered.setdefault(rot, marcas[-1] == "\u2705")
            elif rot not in faixas:
                f = faixa.search(resto)
                x = y = None
                if f:
                    x, y = numero(f.group(1)), numero(f.group(2))
                faixas[rot] = (x, y) if x is not None and y is not None else (None, None)
        for rot, ok in vered.items():
            a, b = faixas.get(rot, (None, None))
            if a is None:
                tipo = None
            elif a <= 0 <= b:
                tipo = "zero"
            elif 0 <= a and b <= 1:
                tipo = "fracao"
            elif a == int(a) and b == int(b) and a >= 1:
                tipo = "contagem"
            else:
                tipo = "outra"
            saida.append((parte, rot, a, b, ok, tipo))
    return saida


def p3188_auditoria_do_leitor_v5(recuperar=range(128, 139), identidade=range(53, 128)):
    """(g)-(i) da Parte 140: o que a v5 recupera nas partes em tabela e se ela muda alguma previsao nas partes que a v4 ja lia.
    Devolve (recuperadas com veredito, acertos delas, previsoes que mudam entre v4 e v5 nas partes de identidade, por parte)."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    rec = p3187_minhas_previsoes_v5(recuperar)
    com = [p for p in identidade if glob.glob(os.path.join(raiz, f"ASI_AGI_parte{p}_*.md")) and re.search(
        r"Do mundo: ((?:\([a-z]\) [\u2705\u274c] ?)+)", open(glob.glob(os.path.join(raiz, f"ASI_AGI_parte{p}_*.md"))[0], encoding="utf-8").read())]
    # (a 1a versao comparava TODAS as partes de identidade, inclusive as sem a linha de placar: 29 "mudancas" que eram as Partes 126-127
    # recuperadas, nao mudancas; corrigido para medir o que (i) diz)
    v4 = p2833_minhas_previsoes_v4(com)
    v5 = p3187_minhas_previsoes_v5(com)
    mudam = len(set(v4) ^ set(v5))
    por = {}
    for x in rec:
        por.setdefault(x[0], [0, 0])
        por[x[0]][0] += 1
        por[x[0]][1] += int(x[4])
    return len(rec), sum(x[4] for x in rec), mudam, por


def p3189_dicionario_como_fluxo(k=500, reservatorios=300):
    """(a)-(c) da Parte 140: as glosas do WordNet 3.0 na ordem do arquivo como um fluxo; um reservatorio de k (synthai/reservatorio.py) por
    semente. Devolve (razao desvio medido / fechado, z da media das medias, fracao media da 1a metade, N, media da populacao)."""
    import gzip
    import os
    from synthai.reservatorio import Reservatorio
    raiz = os.path.dirname(os.path.abspath(__file__))
    with gzip.open(os.path.join(raiz, "dados", "wordnet30_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        comp = [len(l.rstrip("\n").split("\t")[4].split()) for l in f]
    N = len(comp)
    mu = sum(comp) / N
    sigma = math.sqrt(sum((c - mu) * (c - mu) for c in comp) / N)
    fechado = sigma / math.sqrt(k) * math.sqrt((N - k) / (N - 1))
    medias, metades = [], []
    for s in range(reservatorios):
        res = Reservatorio(k, semente=140000 + s)
        for i in range(N):
            res.adicionar(i)
        medias.append(sum(comp[i] for i in res.itens) / k)
        metades.append(sum(1 for i in res.itens if i < N / 2) / k)
    mm = sum(medias) / reservatorios
    dp = math.sqrt(sum((m - mm) * (m - mm) for m in medias) / (reservatorios - 1))
    return dp / fechado, (mm - mu) / (fechado / math.sqrt(reservatorios)), sum(metades) / reservatorios, N, mu


def _posto_de_lambdas(lams):
    s = [math.sqrt(max(l, 0.0)) for l in lams]
    t = sum(s)
    return math.exp(-sum((v / t) * math.log(v / t) for v in s if v > 0))


def p3190_hexadecimal_vertices(n=5000):
    """(d)-(f) da Parte 140: o posto efetivo (Roy-Vetterli, synthai/reservatorio.py) dos digitos hexadecimais como vertices de {0,1}^4: os 16;
    os 10 decimais, contra a conta a mao (autovalores 0,25; 0,20; (0,44 +- sqrt 0,0656)/2); e o 1o digito hexadecimal de 3^n, n = 1..N,
    contra Benford-16 (covariancia exata, autovalores por Jacobi). Devolve (posto 16, |posto 0-9 - mao|, |posto 3^n - Benford|, posto 3^n)."""
    from synthai.reservatorio import posto_efetivo
    from synthai.contraposto_matrizes import jacobi_autovalores
    bits = lambda d: [float((d >> j) & 1) for j in (3, 2, 1, 0)]
    p16 = posto_efetivo([bits(d) for d in range(16)])
    mao = _posto_de_lambdas([0.25, 0.20, (0.44 + math.sqrt(0.0656)) / 2, (0.44 - math.sqrt(0.0656)) / 2])
    p10 = posto_efetivo([bits(d) for d in range(10)])
    lider = [bits(int(format(3 ** m, "x")[0], 16)) for m in range(1, n + 1)]
    pn = posto_efetivo(lider)
    P = {d: math.log(1 + 1 / d, 16) for d in range(1, 16)}
    mu = [sum(P[d] * bits(d)[j] for d in P) for j in range(4)]
    C = [[sum(P[d] * bits(d)[i] * bits(d)[j] for d in P) - mu[i] * mu[j] for j in range(4)] for i in range(4)]
    pb = _posto_de_lambdas(jacobi_autovalores(C))
    return p16, abs(p10 - mao), abs(pn - pb), pn


def p3191_calibracao_v4_v5(partes=range(80, 141)):
    """A calibracao do mundo (fracao de acertos das faixas de 90%) pelas duas reguas, v4 e v5, nas mesmas partes (P3191; Parte 140).
    Devolve ((n, acertos) pela v4, (n, acertos) pela v5)."""
    v4 = p2833_minhas_previsoes_v4(partes)
    v5 = p3187_minhas_previsoes_v5(partes)
    return (len(v4), sum(x[4] for x in v4)), (len(v5), sum(x[4] for x in v5))


def p3192_partes_invisiveis(partes=range(53, 141)):
    """A auditoria da regra da Parte 140 (P3192): as partes que tem uma secao de previsoes (um titulo com "Previs") e das quais NENHUMA regua
    (v5) le uma previsao com veredito. Devolve a lista dessas partes."""
    import glob
    import os
    import re
    raiz = os.path.dirname(os.path.abspath(__file__))
    lidas = {x[0] for x in p3187_minhas_previsoes_v5(partes)}
    out = []
    for p in partes:
        a = glob.glob(os.path.join(raiz, f"ASI_AGI_parte{p}_*.md"))
        if a and p not in lidas and re.search(r"^#+ [^\n]*Previs", open(a[0], encoding="utf-8").read(), re.M):
            out.append(p)
    return out


def _parte_140():
    print("\n=== Parte 140: o leitor v5 (tabelas), o dicionario como fluxo, o hexadecimal como vertices ===")
    n, ac, mudam, por = p3188_auditoria_do_leitor_v5()
    print(f"  P3188 (g) recuperadas {n}; (h) acertos {ac} ({ac / n:.3f}); (i) mudam nas partes da v4 {mudam}; por parte {por}")
    r, z, met, N, mu = p3189_dicionario_como_fluxo()
    print(f"  P3189 N = {N} glosas, media {mu:.4f} palavras; (a) razao dos desvios {r:.4f}; (b) z {z:.3f}; (c) 1a metade {met:.5f}")
    p16, e10, eb, pn = p3190_hexadecimal_vertices()
    print(f"  P3190 (d) posto dos 16 {p16:.12f}; (e) |0-9 - mao| {e10:.2e}; (f) |3^n - Benford| {eb:.5f} (posto 3^n {pn:.5f})")
    (n4, a4), (n5, a5) = p3191_calibracao_v4_v5()
    print(f"  P3191 calibracao 80-140: v4 {a4}/{n4} = {a4 / n4:.3f}; v5 {a5}/{n5} = {a5 / n5:.3f}")
    print(f"  P3192 partes com previsoes que nenhuma regua le: {p3192_partes_invisiveis()}")


PARTES[140] = _parte_140


def p3193_enantiodromia(dimensao=8, condicao=10.0, semente=31001, semente_partida=5, T=24, passo=0.05, beta=0.6):
    """(a)-(g) da Parte 142: as travessias do zero de cada coordenada propria dos iterados REAIS da media exponencial (synthai.passos.descer),
    contra a forma fechada T*theta/pi dos modos de raizes complexas. Devolve [(lambda, travessias, T*theta/pi ou None)]."""
    from synthai.passos import quadratica_anisotropica, descer, coordenadas_proprias
    A, lam, Q = quadratica_anisotropica(dimensao, condicao, semente)
    r = random.Random(semente_partida)
    x0 = [r.gauss(0.0, 1.0) for _ in range(dimensao)]
    alvo = [0.0] * dimensao
    xs = []
    descer(A, x0, alvo, T, metodo="media", passo=passo, beta=beta, guardar=xs)
    cs = [coordenadas_proprias(Q, x, alvo) for x in xs]
    out = []
    for i, l in enumerate(lam):
        serie = [c[i] for c in cs]
        trav = sum(1 for a, b in zip(serie, serie[1:]) if a * b < 0)
        b = 2 - beta - 2 * passo * beta * l
        prev = T * math.acos(b / (2 * math.sqrt(1 - beta))) / math.pi if b * b < 4 * (1 - beta) else None
        out.append((l, trav, prev))
    return out


def p3194_compensacao(grupos=10000, semente=142):
    """(h) da Parte 142: o maximo de |soma das vantagens| da GRPO (synthai.grpo_bandido.vantagens_grupo) em grupos aleatorios de G = 2..16
    com recompensas uniformes em [0, 1]. Devolve o maximo."""
    from synthai.grpo_bandido import vantagens_grupo
    r = random.Random(semente)
    m = 0.0
    for _ in range(grupos):
        G = r.randint(2, 16)
        m = max(m, abs(sum(vantagens_grupo([r.random() for _ in range(G)]))))
    return m


def _parte_142():
    print("\n=== Parte 142: Jung nos modulos novos: a enantiodromia do heavy-ball e a compensacao do grupo ===")
    for l, trav, prev in p3193_enantiodromia():
        print(f"  P3193 lambda {l:.3f}: travessias {trav}; T*theta/pi {'real' if prev is None else f'{prev:.2f}'}")
    print(f"  P3194 (h) maximo de |soma das vantagens| em 10.000 grupos: {p3194_compensacao():.2e}")


PARTES[142] = _parte_142


def p3195_fluxo_em_portugues(k=500, reservatorios=300, semente=143000):
    """(a)-(c) da Parte 143: o teste da P3189 no segundo mundo, as 53.058 glosas da OpenWordNet-PT (coluna 3; vazia = 0 palavras).
    Devolve (razao dos desvios, z da media das medias, fracao media da 1a metade, N, media da populacao)."""
    import gzip
    import os
    from synthai.reservatorio import Reservatorio
    raiz = os.path.dirname(os.path.abspath(__file__))
    with gzip.open(os.path.join(raiz, "dados", "ownpt_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        comp = [len(l.rstrip("\n").split("\t")[2].split()) for l in f]
    N = len(comp)
    mu = sum(comp) / N
    sigma = math.sqrt(sum((c - mu) * (c - mu) for c in comp) / N)
    fechado = sigma / math.sqrt(k) * math.sqrt((N - k) / (N - 1))
    medias, metades = [], []
    for s in range(reservatorios):
        res = Reservatorio(k, semente=semente + s)
        for i in range(N):
            res.adicionar(i)
        medias.append(sum(comp[i] for i in res.itens) / k)
        metades.append(sum(1 for i in res.itens if i < N / 2) / k)
    mm = sum(medias) / reservatorios
    dp = math.sqrt(sum((m - mm) * (m - mm) for m in medias) / (reservatorios - 1))
    return dp / fechado, (mm - mu) / (fechado / math.sqrt(reservatorios)), sum(metades) / reservatorios, N, mu


def p3196_benford16_potencias(bases=(5, 7, 2), n=5000):
    """(d)-(f) da Parte 143: o posto efetivo dos bits do 1o digito hexadecimal de b^m, m = 1..n, contra Benford-16 (P3190).
    Devolve {b: (posto, |posto - Benford|)}."""
    from synthai.reservatorio import posto_efetivo
    from synthai.contraposto_matrizes import jacobi_autovalores
    bits = lambda d: [float((d >> j) & 1) for j in (3, 2, 1, 0)]
    P = {d: math.log(1 + 1 / d, 16) for d in range(1, 16)}
    mu = [sum(P[d] * bits(d)[j] for d in P) for j in range(4)]
    C = [[sum(P[d] * bits(d)[i] * bits(d)[j] for d in P) - mu[i] * mu[j] for j in range(4)] for i in range(4)]
    pb = _posto_de_lambdas(jacobi_autovalores(C))
    out = {}
    for b in bases:
        pn = posto_efetivo([bits(int(format(b ** m, "x")[0], 16)) for m in range(1, n + 1)])
        out[b] = (pn, abs(pn - pb))
    return out


def _parte_143():
    print("\n=== Parte 143: as replicas da Parte 140 (o portugues; 5^n, 7^n, 2^n) ===")
    r, z, met, N, mu = p3195_fluxo_em_portugues()
    print(f"  P3195 N = {N} glosas em portugues, media {mu:.4f} palavras; (a) razao {r:.4f}; (b) z {z:.3f}; (c) 1a metade {met:.5f}")
    for b, (pn, d) in p3196_benford16_potencias().items():
        print(f"  P3196 {b}^n: posto {pn:.9f}; |posto - Benford-16| {d:.5f}")


PARTES[143] = _parte_143


def p3197_grupos_uteis_mundo_novo(mundo=(145, 146), sementes=(31, 32, 33), orcamento=4096, b=0.0330):
    """(a)-(h) da Parte 145: a GRPO com G = 2, 4, 8, 16 num segundo mundo de contextos; os grupos uteis U e o desvio de
    ret(G) - ret(2) contra b*ln(U_G/U_2), com o b ajustado no mundo antigo (31/32). Devolve ({G: (retorno, U)}, {G: desvio}, ordem igual?)."""
    from synthai.grpo_bandido import gerar_contextos, treinar, retorno_esperado
    tr, te = gerar_contextos(128, mundo[0]), gerar_contextos(128, mundo[1])
    out = {}
    for G in (2, 4, 8, 16):
        rets, uteis = [], []
        for sem in sementes:
            w, s, n = treinar(tr, G, orcamento, semente=sem)
            rets.append(retorno_esperado(w, te))
            uteis.append(n - s)
        out[G] = (sum(rets) / len(rets), sum(uteis) / len(uteis))
    desvio = {G: out[G][0] - out[2][0] - b * math.log(out[G][1] / out[2][1]) for G in (4, 8, 16)}
    ordem = sorted(out, key=lambda g: out[g][0]) == sorted(out, key=lambda g: out[g][1])
    return out, desvio, ordem


def _parte_145():
    print("\n=== Parte 145: os grupos uteis da GRPO num segundo mundo ===")
    out, desvio, ordem = p3197_grupos_uteis_mundo_novo()
    for G, (r, u) in out.items():
        print(f"  P3197 G={G}: retorno {r:.4f}; grupos uteis {u:.1f}" + (f"; desvio da relacao {desvio[G]:+.4f}" if G in desvio else ""))
    print(f"  P3197 (a) a ordem dos retornos e a dos grupos uteis: {ordem}")


PARTES[145] = _parte_145


def p3198_grpo_no_jogo_de_palavras(sementes=(43, 44, 45), episodios=5000, avaliacao=1000):
    """(a)-(f) da Parte 147: a GRPO (synthai/grpo_palavras.py, de rl_grupos.py) contra o Q-learning (synthai/palavras_rl.py, de word_rl_lab) no
    jogo de palavras com o dicionario embutido, o mesmo numero de episodios e o mesmo avaliador guloso. Devolve {nome: media das sementes}."""
    from synthai import palavras_rl as P
    from synthai.grpo_palavras import treinar
    dic = P.Dicionario(P.EMBEDDED_WORDS)
    acc = {"Q": [], "G2": [], "G8": [], "sem2": [], "sem8": []}
    for sem in sementes:
        cfg = P.Config(episodios=episodios, avaliacao=avaliacao, seed=sem)
        ag, _, _ = P.train(cfg, dic)
        acc["Q"].append(P.evaluate(cfg, dic, ag)["guloso"][0])
        for G in (2, 8):
            a, s, n = treinar(dic, episodios, G, seed=sem)
            acc["G%d" % G].append(P.evaluate(cfg, dic, a)["guloso"][0])
            acc["sem%d" % G].append(s / n)
    out = {k: sum(v) / len(v) for k, v in acc.items()}
    out["G8-Q"] = out["G8"] - out["Q"]
    return out


def _parte_147():
    print("\n=== Parte 147: a GRPO no jogo de palavras do dicionario contra o Q-learning ===")
    r = p3198_grpo_no_jogo_de_palavras()
    print(f"  P3198 (a) Q {r['Q']:.4f}; (b) GRPO G=2 {r['G2']:.4f}; (c) G=8 {r['G8']:.4f}; (d) sem contraste G=2 {r['sem2']:.4f}; (e) G=8 {r['sem8']:.4f}; (f) G8 - Q {r['G8-Q']:+.4f}")


PARTES[147] = _parte_147

def p3199_grpo_no_dicionario_grande(sementes=tuple(range(61, 71)), episodios=5000, avaliacao=1000):
    """(a)-(j) da Parte 148: a P3198 com os 77.340 lemas do WordNet (palavras_rl.lemas_wordnet) no lugar das palavras embutidas, 10 sementes.
    Devolve {nome: media das sementes} mais 'ambas' (nº de sementes em que G=2 e G=8 superam o Q-learning)."""
    from synthai import palavras_rl as P
    from synthai.grpo_palavras import treinar
    dic = P.Dicionario(P.lemas_wordnet())
    acc = {"Q": [], "aleat": [], "G2": [], "G8": [], "sem2": [], "sem8": []}
    for sem in sementes:
        cfg = P.Config(episodios=episodios, avaliacao=avaliacao, seed=sem)
        ag, _, _ = P.train(cfg, dic)
        ev = P.evaluate(cfg, dic, ag)
        acc["Q"].append(ev["guloso"][0])
        acc["aleat"].append(ev["aleatorio"][0])
        for G in (2, 8):
            a, s, n = treinar(dic, episodios, G, seed=sem)
            acc["G%d" % G].append(P.evaluate(cfg, dic, a)["guloso"][0])
            acc["sem%d" % G].append(s / n)
    out = {k: sum(v) / len(v) for k, v in acc.items()}
    out["G2-Q"] = out["G2"] - out["Q"]
    out["G8-Q"] = out["G8"] - out["Q"]
    out["G8-G2"] = out["G8"] - out["G2"]
    out["ambas"] = sum(g2 > q and g8 > q for q, g2, g8 in zip(acc["Q"], acc["G2"], acc["G8"]))
    out["por_semente"] = acc
    return out


def p3200_t_student_quantil(gl, q=0.95):
    """O quantil q da t de Student com gl graus de liberdade (P3200 usa), por bissecao sobre a CDF integrada por Simpson (so biblioteca padrao)."""
    import math
    c = math.exp(math.lgamma((gl + 1) / 2) - math.lgamma(gl / 2)) / math.sqrt(gl * math.pi)

    def cdf(x, n=2000):
        h = x / n
        f = lambda s: c * (1 + s * s / gl) ** (-(gl + 1) / 2)
        acc = f(0) + f(x)
        for i in range(1, n):
            acc += (4 if i % 2 else 2) * f(i * h)
        return 0.5 + acc * h / 3
    lo, hi = 0.0, 50.0
    for _ in range(80):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if cdf(m) < q else (lo, m)
    return (lo + hi) / 2


def p3200_lotes_do_q(lotes=((5, 13), (61, 71), (71, 81), (13, 23), (23, 41), (1001, 1019))):
    """A investigacao da Parte 148 (P3200): o Q-learning no dicionario grande em seis lotes de sementes (a calibracao 5-12, o teste 61-70 e os
    lotes 71-80, 13-22, 23-40 e 1001-1018). Devolve {'lotes': {(ini, fim): (media, desvio)}, 'todas': (n, media, desvio), 'o': media(23-40) -
    media(1001-1018), 'sigma_cal': desvio das 8 da calibracao, 'meia_t': a meia-largura de (a) com o quantil t de 7 graus no lugar de 1,645}."""
    import math
    import statistics as st
    from synthai import palavras_rl as P
    dic = P.Dicionario(P.lemas_wordnet())
    por = {}
    for ini, fim in lotes:
        v = []
        for s in range(ini, fim):
            cfg = P.Config(seed=s)
            ag, _, _ = P.train(cfg, dic)
            v.append(P.evaluate(cfg, dic, ag)["guloso"][0])
        por[(ini, fim)] = v
    tudo = [x for v in por.values() for x in v]
    s_cal = st.stdev(por[lotes[0]])  # o 1o lote e a calibracao; (o) e o 5o menos o 6o
    return {"lotes": {k: (st.mean(v), st.stdev(v)) for k, v in por.items()}, "todas": (len(tudo), st.mean(tudo), st.stdev(tudo)),
            "o": st.mean(por[lotes[4]]) - st.mean(por[lotes[5]]), "sigma_cal": s_cal,
            "meia_t": p3200_t_student_quantil(7) * 1.36 * math.sqrt(s_cal * s_cal / 8 + s_cal * s_cal / 10),
            "p_sigma_baixo": p3200_chi2_cdf(len(por[lotes[0]]) - 1, (len(por[lotes[0]]) - 1) * s_cal * s_cal / st.stdev(tudo) ** 2)}


def p3200_chi2_cdf(gl, x, n=4000):
    """P(chi2 com gl graus <= x), por Simpson sobre a densidade (P3200: a chance de a calibracao subestimar o desvio tanto quanto subestimou)."""
    import math
    c = -(gl / 2) * math.log(2) - math.lgamma(gl / 2)
    f = lambda s: 0.0 if s <= 0 else math.exp(c + (gl / 2 - 1) * math.log(s) - s / 2)
    h = x / n
    acc = f(0) + f(x)
    for i in range(1, n):
        acc += (4 if i % 2 else 2) * f(i * h)
    return acc * h / 3


def p3201_grpo_por_dicionario(dicionario="pt", sementes=tuple(range(101, 121)), episodios=5000, avaliacao=1000):
    """A P3199 com o dicionario escolhido (Parte 149): 'pt' = palavras_rl.lemas_ownpt() (OpenWordNet-PT sem acentos), 'en' = lemas_wordnet(),
    'embutido' = EMBEDDED_WORDS. Devolve {nome: media}, as listas por semente em 'por_semente' e os desvios em 'desvios'."""
    import statistics as st
    from synthai import palavras_rl as P
    from synthai.grpo_palavras import treinar
    fonte = {"pt": P.lemas_ownpt, "en": P.lemas_wordnet, "embutido": lambda: P.EMBEDDED_WORDS}[dicionario]
    dic = P.Dicionario(fonte())
    acc = {"Q": [], "aleat": [], "G2": [], "G8": [], "sem2": [], "sem8": []}
    for sem in sementes:
        cfg = P.Config(episodios=episodios, avaliacao=avaliacao, seed=sem)
        ag, _, _ = P.train(cfg, dic)
        ev = P.evaluate(cfg, dic, ag)
        acc["Q"].append(ev["guloso"][0])
        acc["aleat"].append(ev["aleatorio"][0])
        for G in (2, 8):
            a, s, n = treinar(dic, episodios, G, seed=sem)
            acc["G%d" % G].append(P.evaluate(cfg, dic, a)["guloso"][0])
            acc["sem%d" % G].append(s / n)
    acc["G2-Q"] = [a - b for a, b in zip(acc["G2"], acc["Q"])]
    acc["G8-Q"] = [a - b for a, b in zip(acc["G8"], acc["Q"])]
    acc["G8-G2"] = [a - b for a, b in zip(acc["G8"], acc["G2"])]
    out = {k: sum(v) / len(v) for k, v in acc.items()}
    out["ambas"] = sum(g2 > q and g8 > q for q, g2, g8 in zip(acc["Q"], acc["G2"], acc["G8"]))
    out["desvios"] = {k: st.stdev(v) for k, v in acc.items()} if len(sementes) > 1 else {}
    out["por_semente"] = acc
    return out


def p3202_aleatorio_por_dicionario(dicionario="embutido", sementes=tuple(range(46, 66)), avaliacao=1000):
    """(u) da Parte 149 (P3202): so o braco aleatorio do avaliador da Parte 111 (mesmas grades: semente + 100000; mesmo agente: semente + 2), sem
    treinar o Q-learning. Devolve (media, desvio, lista)."""
    import random
    import statistics as st
    from synthai import palavras_rl as P
    fonte = {"pt": P.lemas_ownpt, "en": P.lemas_wordnet, "embutido": lambda: P.EMBEDDED_WORDS}[dicionario]
    dic = P.Dicionario(fonte())
    v = []
    for s in sementes:
        cfg = P.Config(seed=s)
        env = P.WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len, rng=random.Random(s + 100_000))
        pol = P.QAgent(seed=s + 2)
        res = [P.run_episode(env, dic, pol, "random", learn=False) for _ in range(avaliacao)]
        v.append(sum(r[1] for r in res) / len(res))
    return st.mean(v), (st.stdev(v) if len(v) > 1 else 0.0), v


# (parte, rotulo, piso, teto, n_cal, medido): as faixas de CALIBRACAO que erraram nas Partes 147 e 148, copiadas dos textos das partes
_ERROS_DE_CALIBRACAO_147_148 = ((147, "b", 0.136, 0.200, 3, 0.2017), (148, "a", 0.3072, 0.3413, 8, 0.3020), (148, "n", 0.2913, 0.3265, 28, 0.3278))


def p3203_auditoria_t(erros=_ERROS_DE_CALIBRACAO_147_148):
    """(r) da Parte 149 (P3203): cada faixa refeita com o quantil t de n_cal - 1 graus no lugar de 1,645 (mesmo centro, meia-largura vezes
    t/1,645). Devolve [(parte, rotulo, piso_t, teto_t, acerta_com_t)] e o numero que vira acerto."""
    out = []
    for parte, rot, a, b, n, x in erros:
        c, h = (a + b) / 2, (b - a) / 2
        h2 = h * p3200_t_student_quantil(n - 1) / 1.645
        out.append((parte, rot, c - h2, c + h2, c - h2 <= x <= c + h2))
    return out, sum(o[4] for o in out)


def p3204_densidades():
    """A conta de peso da Parte 150 (P3204): D = soma sobre as palavras de 3 a 5 letras do produto das frequencias das letras do tabuleiro, para
    (embutido, portugues, WordNet) no tabuleiro ingles e portugues no tabuleiro portugues (frequencias contadas nos lemas da OpenWordNet-PT).
    Devolve {nome: D} e as frequencias portuguesas."""
    from synthai import palavras_rl as P
    from synthai import tabuleiro as T
    pt = P.lemas_ownpt()
    fpt = T.frequencias_de(pt)
    E = P.LETTER_FREQ
    return {"emb/EN": T.densidade(P.EMBEDDED_WORDS, E), "pt/EN": T.densidade(pt, E), "en/EN": T.densidade(P.lemas_wordnet(), E),
            "pt/PT": T.densidade(pt, fpt)}, fpt


def p3205_grpo_tabuleiro(dicionario="pt", tabuleiro="pt", sementes=tuple(range(101, 121)), episodios=5000, avaliacao=1000):
    """A P3201 com o tabuleiro sorteado pelas frequencias de letras do portugues ('pt') ou do ingles ('en', o original) (P3205; Parte 150)."""
    from synthai import palavras_rl as P
    from synthai import tabuleiro as T
    freq = T.frequencias_de(P.lemas_ownpt()) if tabuleiro == "pt" else P.LETTER_FREQ
    with T.com_frequencias(freq):
        return p3201_grpo_por_dicionario(dicionario, sementes, episodios, avaliacao)


def p3206_aleatorio_tabuleiro(dicionario, tabuleiro="pt", sementes=tuple(range(141, 151))):
    """(o)-(p) da Parte 150 (P3206): a P3202 (so o braco aleatorio) com o tabuleiro trocado."""
    from synthai import palavras_rl as P
    from synthai import tabuleiro as T
    freq = T.frequencias_de(P.lemas_ownpt()) if tabuleiro == "pt" else P.LETTER_FREQ
    with T.com_frequencias(freq):
        return p3202_aleatorio_por_dicionario(dicionario, sementes)


def p3207_aleatorio_geometria(dicionario="pt", tabuleiro="pt", tamanho=5, minimo=3, maximo=5, sementes=tuple(range(161, 181)), avaliacao=1000):
    """(a)-(d) da Parte 151 (P3207): so o braco aleatorio, com o tamanho da grade e os comprimentos trocados, e a previsao geometrica
    1,054 * sum_L s_L D_L. Devolve (medido, desvio, geometria)."""
    import random
    import statistics as st
    from synthai import palavras_rl as P
    from synthai import tabuleiro as T
    fonte = {"pt": P.lemas_ownpt, "en": P.lemas_wordnet, "embutido": lambda: P.EMBEDDED_WORDS}[dicionario]
    palavras = fonte()
    dic = P.Dicionario(palavras)
    freq = T.frequencias_de(P.lemas_ownpt()) if tabuleiro == "pt" else P.LETTER_FREQ
    v = []
    with T.com_frequencias(freq):
        for s in sementes:
            env = P.WordGridEnv(tamanho, minimo, maximo, rng=random.Random(s + 100_000))
            pol = P.QAgent(seed=s + 2)
            res = [P.run_episode(env, dic, pol, "random", learn=False) for _ in range(avaliacao)]
            v.append(sum(r[1] for r in res) / len(res))
    return st.mean(v), (st.stdev(v) if len(v) > 1 else 0.0), T.aleatorio_geometrico(palavras, freq, tamanho, minimo, maximo)


def p3208_repertorio(dicionario="pt", tabuleiro="pt", sementes=tuple(range(101, 106)), episodios=5000, avaliacao=1000):
    """A pendencia 1 da Parte 149 (P3208): nas avaliacoes do Q-learning guloso, a fracao dos acertos cuja palavra aparece em pelo menos dois episodios
    (cada episodio e uma grade nova): o REPERTORIO. Devolve {taxa, distintas, repete} medias das sementes, e as listas."""
    import random
    import statistics as st
    from synthai import palavras_rl as P
    from synthai import tabuleiro as T
    from collections import Counter
    fonte = {"pt": P.lemas_ownpt, "en": P.lemas_wordnet, "embutido": lambda: P.EMBEDDED_WORDS}[dicionario]
    dic = P.Dicionario(fonte())
    freq = T.frequencias_de(P.lemas_ownpt()) if tabuleiro == "pt" else P.LETTER_FREQ
    acc = {"taxa": [], "distintas": [], "repete": []}
    with T.com_frequencias(freq):
        for s in sementes:
            cfg = P.Config(episodios=episodios, avaliacao=avaliacao, seed=s)
            ag, _, _ = P.train(cfg, dic)
            env = P.WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len, rng=random.Random(s + 100_000))
            res = [P.run_episode(env, dic, ag, "greedy", learn=False) for _ in range(avaliacao)]
            achadas = Counter(r[0] for r in res if r[1])
            k = sum(achadas.values())
            acc["taxa"].append(k / avaliacao)
            acc["distintas"].append(len(achadas))
            acc["repete"].append(sum(n for n in achadas.values() if n >= 2) / k if k else 0.0)
    out = {x: st.mean(v) for x, v in acc.items()}
    out["desvios"] = {x: st.stdev(v) for x, v in acc.items()} if len(sementes) > 1 else {}
    out["listas"] = acc
    return out


def p3209_aleatorio_colapso(dicionario="pt", tabuleiro="pt", tamanho=5, minimo=3, maximo=5, sementes=tuple(range(181, 201)), avaliacao=1000):
    """(a)-(g) da Parte 152 (P3209): o braco aleatorio num mundo (dicionario, tabuleiro 'pt'/'en'/'uniforme', grade, comprimentos) e as duas contas:
    a geometria sem colapso (Parte 151) e o colapso em campo medio (synthai.tabuleiro.aleatorio_colapso). Devolve (medido, desvio, geometria, colapso)."""
    import random
    import statistics as st
    from synthai import palavras_rl as P
    from synthai import tabuleiro as T
    fonte = {"pt": P.lemas_ownpt, "en": P.lemas_wordnet, "embutido": lambda: P.EMBEDDED_WORDS}[dicionario]
    palavras = fonte()
    dic = P.Dicionario(palavras)
    freq = {"pt": lambda: T.frequencias_de(P.lemas_ownpt()), "en": lambda: P.LETTER_FREQ,
            "uniforme": lambda: {chr(65 + i): 1.0 for i in range(26)}}[tabuleiro]()
    v = []
    with T.com_frequencias(freq):
        for s in sementes:
            env = P.WordGridEnv(tamanho, minimo, maximo, rng=random.Random(s + 100_000))
            pol = P.QAgent(seed=s + 2)
            res = [P.run_episode(env, dic, pol, "random", learn=False) for _ in range(avaliacao)]
            v.append(sum(r[1] for r in res) / len(res))
    return (st.mean(v), (st.stdev(v) if len(v) > 1 else 0.0), T.aleatorio_geometrico(palavras, freq, tamanho, minimo, maximo),
            T.aleatorio_colapso(palavras, freq, tamanho, minimo, maximo))


_MUNDOS_P152 = (("(a) uniforme", ("pt", "uniforme", 5, 3, 5)), ("(b) 3x3", ("pt", "pt", 3, 3, 5)), ("(c) 7x7", ("pt", "pt", 7, 3, 5)),
                ("(d) 3-6 letras", ("pt", "pt", 5, 3, 6)), ("(e) WordNet 4-5", ("en", "en", 5, 4, 5)))


def _parte_148():
    print("\n=== Parte 148: a GRPO no jogo de palavras com o dicionario grande (77.340 lemas) ===")
    r = p3199_grpo_no_dicionario_grande()
    print(f"  P3199 (a) Q {r['Q']:.4f}; (b) aleatorio {r['aleat']:.4f}; (c) G=2 {r['G2']:.4f}; (d) sem contraste G=2 {r['sem2']:.4f}; "
          f"(e) G=8 {r['G8']:.4f}; (f) sem contraste G=8 {r['sem8']:.4f}")
    print(f"  P3199 (g) G2-Q {r['G2-Q']:+.4f}; (h) G8-Q {r['G8-Q']:+.4f}; (i) G8-G2 {r['G8-G2']:+.4f}; (j) sementes com as duas acima do Q {r['ambas']}/10")
    L = p3200_lotes_do_q()
    for (a, b), (m, s) in L["lotes"].items():
        print(f"  P3200 lote {a}-{b - 1}: Q media {m:.4f}, desvio {s:.4f}")
    n, m, s = L["todas"]
    print(f"  P3200 todas as {n} sementes: media {m:.4f}, desvio {s:.4f}; desvio da calibracao {L['sigma_cal']:.4f}; (o) {L['o']:+.4f}; "
          f"meia-largura de (a) com t(7) {L['meia_t']:.4f}; P(desvio da calibracao tao baixo) {L['p_sigma_baixo']:.3f}")


PARTES[148] = _parte_148


def _parte_149():
    print("\n=== Parte 149: a GRPO no jogo de palavras em portugues (OpenWordNet-PT sem acentos) ===")
    for nome, sem in (("calibracao 101-120", tuple(range(101, 121))), ("teste 121-140", tuple(range(121, 141)))):
        r = p3201_grpo_por_dicionario("pt", sem)
        print(f"  P3201 {nome}: Q {r['Q']:.4f}; aleatorio {r['aleat']:.4f}; G=2 {r['G2']:.4f}; G=8 {r['G8']:.4f}; sem contraste G=2 {r['sem2']:.4f}, "
              f"G=8 {r['sem8']:.4f}; G2-Q {r['G2-Q']:+.4f}; G8-Q {r['G8-Q']:+.4f}; G8-G2 {r['G8-G2']:+.4f}; as duas acima do Q {r['ambas']}/{len(sem)}")
    e = p3201_grpo_por_dicionario("embutido", (43, 44, 45))
    print(f"  P3201 (k) embutido, sementes 43-45: aleatorio {e['aleat']:.4f}; Q {e['Q']:.4f}")
    m, s, _ = p3202_aleatorio_por_dicionario()
    print(f"  P3202 (u) embutido, sementes 46-65: aleatorio {m:.4f} (desvio {s:.4f})")
    aud, n = p3203_auditoria_t()
    for parte, rot, a, b, ok in aud:
        print(f"  P3203 Parte {parte} ({rot}) com o quantil t: [{a:.4f}; {b:.4f}] {'acerta' if ok else 'erra'}")
    print(f"  P3203 (r) erros de calibracao que viram acerto com o t: {n}")


PARTES[149] = _parte_149


def _parte_150():
    print("\n=== Parte 150: o tabuleiro com as letras do portugues e a densidade de palavras ===")
    d, _ = p3204_densidades()
    print("  P3204 densidade D: " + "; ".join(f"{k} {v:.4f}" for k, v in d.items()))
    for nome, sem in (("calibracao 101-120", tuple(range(101, 121))), ("teste 121-140", tuple(range(121, 141)))):
        r = p3205_grpo_tabuleiro("pt", "pt", sem)
        print(f"  P3205 {nome}: Q {r['Q']:.4f}; aleatorio {r['aleat']:.4f}; G=2 {r['G2']:.4f}; G=8 {r['G8']:.4f}; sem contraste G=2 {r['sem2']:.4f}, "
              f"G=8 {r['sem8']:.4f}; G2-Q {r['G2-Q']:+.4f}; G8-Q {r['G8-Q']:+.4f}; G8-G2 {r['G8-G2']:+.4f}; as duas acima do Q {r['ambas']}/{len(sem)}")
    for dic in ("en", "embutido"):
        m, s, _ = p3206_aleatorio_tabuleiro(dic)
        print(f"  P3206 {dic} no tabuleiro portugues, sementes 141-150: aleatorio {m:.4f} (desvio {s:.4f})")


PARTES[150] = _parte_150


def _parte_151():
    print("\n=== Parte 151: a geometria do braco aleatorio e o repertorio do Q-learning ===")
    from synthai import tabuleiro as T
    print("  P3207 s_L na grade 5x5: " + "; ".join(f"s{L} {v:.4f}" for L, v in T.paradas_por_comprimento().items()))
    for nome, (a, b, d) in (("(a) 4x4", (4, 3, 5)), ("(b) 6x6", (6, 3, 5)), ("(c) max 4", (5, 3, 4)), ("(d) min 4", (5, 4, 5))):
        m, s, g = p3207_aleatorio_geometria(tamanho=a, minimo=b, maximo=d)
        print(f"  P3207 {nome}: aleatorio {m:.4f} (desvio {s:.4f}); geometria {g:.4f}; razao {m / g:.3f}")
    for nome, sem in (("calibracao 101-120", tuple(range(101, 121))), ("teste 121-140", tuple(range(121, 141)))):
        for rot, (dic, tab) in (("pt/EN", ("pt", "en")), ("pt/PT", ("pt", "pt")), ("emb/EN", ("embutido", "en"))):
            r = p3208_repertorio(dic, tab, sem)
            print(f"  P3208 {nome} {rot}: acerto {r['taxa']:.4f}; distintas {r['distintas']:.2f}; repertorio {r['repete']:.4f}")


PARTES[151] = _parte_151

PARTES[126] = _parte_126

if __name__ == "__main__":
    # python3 calculos.py           -> todas as partes (é assim que resultados.txt é gerado)
    # python3 calculos.py 9 10      -> só as partes pedidas, para desenvolver mais rápido
    import sys
    for _k in [int(x) for x in sys.argv[1:]] or sorted(PARTES):
        PARTES[_k]()
    _unificacao()
