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
ERROS_P849, TESTES_P849 = 0, 0


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


ERROS_P879, TESTES_P879 = 0, 0


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

ERROS_P909, TESTES_P909 = 0, 0


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


ERROS_P939, TESTES_P939 = 0, 0


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


ERROS_P969, TESTES_P969 = 0, 0


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


ERROS_P999, TESTES_P999 = 0, 0


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


ERROS_P1029, TESTES_P1029 = 0, 0


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


PARTES = {1: _parte_1, 2: _parte_2, 3: _parte_3, 4: _parte_4, 5: _parte_5, 6: _parte_6, 7: _parte_7, 8: _parte_8, 9: _parte_9, 10: _parte_10, 11: _parte_11, 12: _parte_12, 13: _parte_13, 14: _parte_14, 15: _parte_15, 16: _parte_16, 17: _parte_17, 18: _parte_18, 19: _parte_19, 20: _parte_20, 21: _parte_21, 22: _parte_22, 23: _parte_23, 24: _parte_24, 25: _parte_25, 26: _parte_26, 27: _parte_27, 28: _parte_28, 29: _parte_29, 30: _parte_30, 31: _parte_31, 32: _parte_32, 33: _parte_33, 34: _parte_34, 35: _parte_35, 36: _parte_36, 37: _parte_37, 38: _parte_38, 39: _parte_39, 40: _parte_40, 41: _parte_41, 42: _parte_42, 43: _parte_43, 44: _parte_44, 45: _parte_45, 46: _parte_46, 47: _parte_47, 48: _parte_48, 49: _parte_49, 50: _parte_50, 51: _parte_51, 52: _parte_52}


if __name__ == "__main__":
    # python3 calculos.py           -> todas as partes (é assim que resultados.txt é gerado)
    # python3 calculos.py 9 10      -> só as partes pedidas, para desenvolver mais rápido
    import sys
    for _k in [int(x) for x in sys.argv[1:]] or sorted(PARTES):
        PARTES[_k]()
    _unificacao()
