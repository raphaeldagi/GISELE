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
ERROS_P309, TESTES_P309 = 53, 113


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
          " -> synthai.SynthaiExploradora (P295: explora o bandido por amostragem de Thompson, sozinha)")
    print(f"Regressao: {ok}/{total} resultados publicados reproduzidos; falhas = {falhas}")


PARTES = {1: _parte_1, 2: _parte_2, 3: _parte_3, 4: _parte_4, 5: _parte_5, 6: _parte_6, 7: _parte_7, 8: _parte_8, 9: _parte_9, 10: _parte_10, 11: _parte_11, 12: _parte_12, 13: _parte_13, 14: _parte_14, 15: _parte_15, 16: _parte_16, 17: _parte_17, 18: _parte_18, 19: _parte_19, 20: _parte_20, 21: _parte_21, 22: _parte_22, 23: _parte_23}


if __name__ == "__main__":
    # python3 calculos.py           -> todas as partes (é assim que resultados.txt é gerado)
    # python3 calculos.py 9 10      -> só as partes pedidas, para desenvolver mais rápido
    import sys
    for _k in [int(x) for x in sys.argv[1:]] or sorted(PARTES):
        PARTES[_k]()
    _unificacao()
