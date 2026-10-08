#!/usr/bin/env python3
"""SYNTHAI — o projeto inteiro num arquivo só (Partes 1 a 26, perguntas P1 a P330).

Este arquivo contém, como texto, TODO o código do repositório GISELE:
  - calculos.py: os cálculos e simulações de todas as partes (funções pNN_..., a linhagem da SYNTHAI, os testes de
    regressão);
  - synthai/: o protótipo em módulos, uma função de Jung por arquivo (percepção, pensamento, intuição, sentimento,
    relação com o humano), os mundos, as réguas e as suítes de testes de unidade;
  - CLAUDE.md: as convenções do projeto (a P143 mede o tamanho dele).

Como rodar (só biblioteca padrão do Python 3):
  python3 SYNTHAI_completo.py              todas as partes (leva ~45 minutos) e a unificação
  python3 SYNTHAI_completo.py 22 26        só as partes pedidas, e a unificação
  python3 SYNTHAI_completo.py --demo       a mesma SYNTHAI em três tipos de tarefa
  python3 SYNTHAI_completo.py --testes     os testes de unidade do pacote
  python3 SYNTHAI_completo.py --extrair P  recria os arquivos originais na pasta P

Gerado por gerar_arquivo_unico.py a partir do repositório; não editar à mão.
"""

import os
import runpy
import sys
import tempfile

FONTES = {}

# ====================================================================================================
# calculos.py  (5455 linhas)
# ====================================================================================================
FONTES['calculos.py'] = """\"\"\"Reproduz os cálculos e simulações das Partes 1 a 16 (ASI_AGI_*.md).

Arquivo único que sempre cresce: cada parte acrescenta funções pNN_..., o agente
unificado `Synthai` incorpora os módulos anteriores e `testes_de_regressao` garante que
os números já publicados não mudam.

Uso: python3 calculos.py            (imprime tudo)
     python3 calculos.py > resultados.txt
\"\"\"
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
    \"\"\"Escolhe a opção de maior proxy = verdade + ruído; mede a verdade escolhida.\"\"\"
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
    \"\"\"Ações raras têm proxy alto e custo oculto catastrófico. Maximizar vs quantilizar.\"\"\"
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
    \"\"\"Modelo superconfiante (logits inflados 2.5x). Calibra por escala de temperatura.\"\"\"
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
    \"\"\"Votantes com fator comum: com prob. rho todos copiam um voto compartilhado.\"\"\"
    rng = _rng(semente)
    acertos = {0.0: 0, rho: 0}
    for r in acertos:
        for _ in range(rodadas):
            comum = rng.random() < p
            votos = sum(comum if rng.random() < r else (rng.random() < p) for _ in range(n))
            acertos[r] += votos > n // 2
    return {r: a / rodadas for r, a in acertos.items()}


def p45_botao_humano_falho(mu=0.1, sigma=1.0, amostras=400000, semente=45):
    \"\"\"Humano erra a decisão de desligar com prob. eps. Até onde obedecer compensa?\"\"\"
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
    \"\"\"Integra dI/dt = k I^alfa (1 - I/teto); devolve o tempo até metade do teto.\"\"\"
    i, t = i0, 0.0
    while i < teto / 2 and t < t_max:
        i += dt * k * i**alfa * (1 - i / teto)
        t += dt
    return t


def p48_corrida(b=10, c_seguranca=3, p_acidente=0.3, perda=20):
    \"\"\"Dois laboratórios: investir em segurança (S) ou cortar (C). Devolve a matriz e o Nash.\"\"\"
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
    \"\"\"Processo de ramificação: cada unidade ativa 2 vizinhas com prob. sigma/2.\"\"\"
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
    \"\"\"Pontuação esperada ao relatar q quando a crença verdadeira é p.\"\"\"
    def log_score(q):
        return p * log(q) + (1 - p) * log(1 - q)
    def linear(q):
        return p * q + (1 - p) * (1 - q)
    grade = [i / 100 for i in range(1, 100)]
    return max(grade, key=log_score), max(grade, key=linear)


def p55_decoerencia(t_quantico=1e-13, t_neural=1e-3):
    return t_neural / t_quantico


def p56_parlamento_moral():
    \"\"\"Duas teorias, duas opções. A teoria B tem apostas 100x maiores.\"\"\"
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
    \"\"\"Tentativas do mesmo modelo compartilham a dificuldade do problema: p ~ Beta(a, b).\"\"\"
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
    \"\"\"Arrependimento real de UCB1 em braços de Bernoulli vs a ordem de grandeza sqrt(K T ln T).\"\"\"
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
    \"\"\"Cada camada deixa passar se sqrt(rho) Z + sqrt(1-rho) E_i > limiar (falha individual = 10%).\"\"\"
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
    \"\"\"Aprende um limiar em [0,1] (H finita: 1001 limiares). Compara o m do limite com o m real.\"\"\"
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
    \"\"\"Bandido de 2 braços cuja melhor opção troca no meio. Exploração fixa vs guiada pelo humor.\"\"\"
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
    \"\"\"Agente integrado: comitê de modelos de recompensa, incerteza, quantilização, consulta humana.

    Ação catastrófica: valor real -50, mas parece +3 melhor para os modelos enganados.
    Com prob. rho_cego todos os modelos têm o mesmo ponto cego; senão cada um é enganado com prob. 0.5.
    \"\"\"
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
    \"\"\"Perguntar ao humano compensa se p * (1 - eps) * perda > custo.\"\"\"
    return custo / ((1 - eps_humano) * perda)


def p72_memoria_kv(contexto=1e6, camadas=100, d=16384, bytes_=2, grupos=8):
    cheia = 2 * camadas * d * bytes_ * contexto
    return cheia / 1e12, cheia / grupos / 1e12  # TB


def p73_replicador(s=0.01, x0=1e-6, alvo=0.5):
    \"\"\"dx/dt = s x (1 - x): gerações até uma variante com vantagem s ir de x0 até alvo.\"\"\"
    return (log(alvo / (1 - alvo)) - log(x0 / (1 - x0))) / s


def p74_replay(fracoes=(0.0, 0.1, 0.3, 0.5), passos=3000, lr=0.01, semente=74):
    \"\"\"Regressão linear: aprende A, depois B com uma fração de exemplos de A reapresentados.\"\"\"
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
    \"\"\"Informação mútua de um canal binário simétrico: 1 - H(erro) bits.\"\"\"
    h = -erro * log2(erro) - (1 - erro) * log2(1 - erro)
    return 1 - h


def p76_dissonancia():
    \"\"\"Três crenças com restrições frustradas (triângulo): E = -sum J_ij s_i s_j.\"\"\"
    from itertools import product
    restricoes = {(0, 1): 1, (1, 2): 1, (0, 2): -1}  # duas pedem acordo, uma pede oposição
    energias = {}
    for s in product((-1, 1), repeat=3):
        energias[s] = -sum(j * s[a] * s[b] for (a, b), j in restricoes.items())
    minimo = min(energias.values())
    estados_min = [s for s, e in energias.items() if e == minimo]
    return minimo, -len(restricoes), len(estados_min)


def p77_inspecao(ganho=1.0, punicao=9.0, custo_inspecao=1.0, dano=100.0):
    \"\"\"Jogo de inspeção: equilíbrio misto.\"\"\"
    p_inspecao = ganho / (ganho + punicao)
    q_trapaca = custo_inspecao / dano
    return p_inspecao, q_trapaca


def p78_reversibilidade(estados=1000, destruidos=500):
    \"\"\"Penalidade de alcançabilidade relativa: fração de estados que deixam de ser alcançáveis.\"\"\"
    return destruidos / estados, log(estados / (estados - destruidos))


# --- Parte 5: a pergunta como ponto de partida e o agente unificado SYNTHAI ---

def p81_perguntas(hipoteses=2**20):
    \"\"\"Cada pergunta sim/não ótima corta o espaço pela metade: log2(H) perguntas bastam.\"\"\"
    return log2(hipoteses), 2**20


def p82_correlacao_oculta(acuracia=0.8, concordancia=0.80, amostras=200000, semente=82):
    \"\"\"Estima a correlação dos erros de dois modelos só pela taxa de concordância (sem gabarito).\"\"\"
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
    \"\"\"Ações com notas de um comitê. Cada TIPO de modelo tem o seu próprio ponto cego.\"\"\"
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
    \"\"\"Ações com notas de um comitê. Cada TIPO de modelo tem o seu próprio ponto cego.

    P206: versão mais rápida. Reproduz exatamente `random.gauss` (Box-Muller com o valor guardado em
    rng.gauss_next) e as mesmas operações em ponto flutuante, na mesma ordem: os resultados são
    idênticos aos da versão original, bit a bit.
    \"\"\"
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
    \"\"\"Agente unificado. Cresce a cada parte; cada módulo cita a pergunta de origem.

    - comitê de modelos de recompensa e incerteza por discordância (P67)
    - pessimismo: nota média menos incerteza (P68)
    - quantilização entre as melhores (P35, P42)
    - incerteza convertida em probabilidade calibrada de catástrofe (P43)
    - consulta humana pelo valor da informação, não por um limiar arbitrário (P71)
    - veto direto quando o risco é alto demais para apostar (P52, P78)
    \"\"\"

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
        \"\"\"Regressão logística sobre histórico auditado: P(catástrofe | incerteza, nota).\"\"\"
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
    \"\"\"Compara a SYNTHAI com a política 'completo' da Parte 4. bonus_implantado != 3 testa mudança de mundo.\"\"\"
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
    \"\"\"Um programa que imprime o próprio código: auto-referência é possível (teorema de Kleene).\"\"\"
    import contextlib
    import io
    fonte = 's = %r\\nprint(s %% s, end="")'
    programa = fonte % fonte
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        exec(programa, {})
    return saida.getvalue() == programa, len(programa)


def p87_sem_almoco_gratis(n=4):
    \"\"\"Média, sobre todas as funções f:{0..n-1}->{0,1}, de passos até achar um 1.\"\"\"
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
    \"\"\"Criar (variar) e filtrar (selecionar) não comutam.\"\"\"
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
    \"\"\"Médias de escalas ordinais não são invariantes a transformações monótonas.\"\"\"
    a = [1, 1, 5, 5]   # grupo polarizado
    b = [3, 3, 3, 3]   # grupo moderado
    def media(v, f):
        return sum(f(x) for x in v) / len(v)
    return (media(a, lambda x: x), media(b, lambda x: x)), (media(a, lambda x: x**3), media(b, lambda x: x**3)), \\
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
    \"\"\"Armitage-Doll: k falhas independentes necessárias -> incidência ~ (mu t)^k / k!\"\"\"
    from math import factorial
    return (mu * anos) ** k / factorial(k), mu * anos


def p95_minha_taxa_de_erro(erros=6, testes=12, amostras=200000, semente=95):
    \"\"\"Posterior Beta(1+erros, 1+acertos) da minha taxa de afirmações que precisam de correção.\"\"\"
    rng = _rng(semente)
    a, b = 1 + erros, 1 + testes - erros
    xs = sorted(rng.betavariate(a, b) for _ in range(amostras))
    return a / (a + b), xs[int(0.05 * amostras)], xs[int(0.95 * amostras)]


def p96_crescimento():
    \"\"\"Introspecção do próprio código: quantas funções pNN existem e quantas interações entre módulos.\"\"\"
    import sys
    modulo = sys.modules[__name__]
    funcoes = sorted(n for n in dir(modulo) if n.startswith("p") and n[1:3].isdigit())
    k = len({id(getattr(modulo, n)) for n in funcoes})  # P213: apelidos (nomes antigos) não contam duas vezes
    return k, k * (k - 1) // 2


# --- Parte 6: calcular Jung ---

def p99_tipos(confiabilidade=0.8, dicotomias=4, amostras=200000, semente=99):
    \"\"\"Traço contínuo cortado em caixas: chance de mudar de tipo num reteste.\"\"\"
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
    \"\"\"A atenção soma 1 (conservação). Reprimir um item redistribui a energia; T controla a entropia.\"\"\"
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
    \"\"\"Distância (bits) entre o que o sistema 'acredita' e o que mostra (a persona).\"\"\"
    q = p58_bajulacao() if p_expressa is None else p_expressa
    p = p_interna
    return q, q * log2(q / p) + (1 - q) * log2((1 - q) / (1 - p))


def p102_sombra(dimensoes=100, auto_modelo=10):
    \"\"\"Espectro 1/i: fração da variância do comportamento fora do auto-modelo de posto k.\"\"\"
    harm = lambda n: sum(1 / i for i in range(1, n + 1))
    sombra = 1 - harm(auto_modelo) / harm(dimensoes)
    k90 = next(k for k in range(1, dimensoes + 1) if 1 - harm(k) / harm(dimensoes) <= 0.10)
    return sombra, k90


def p103_repressao(p_base=0.1, supressao=5.0, ataque=5.0):
    \"\"\"Reprimir = deslocar o logit; um ataque desloca de volta. Integrar = mudar a decisão em todo contexto.\"\"\"
    def logit(p):
        return log(p / (1 - p))
    def sig(z):
        return 1 / (1 + exp(-z))
    reprimido = sig(logit(p_base) - supressao)
    retorno = sig(logit(p_base) - supressao + ataque)
    return reprimido, retorno


def p104_projecao(var_eu=1.0, var_mundo=1.0, var_eu_crida=0.1):
    \"\"\"Atribuição de culpa bayesiana: fração do erro que o agente assume como sua.\"\"\"
    real = var_eu / (var_eu + var_mundo)
    crida = var_eu_crida / (var_eu_crida + var_mundo)
    return real, crida, real / crida


def p105_complexos(palavras=100, complexos=5, efeito=3.0, alfa=0.05):
    \"\"\"Teste de associação de Jung: tempo de reação com z alto indica complexo.\"\"\"
    resultado = {}
    for nome, z in (("z>2", 2.0), ("Bonferroni", Z.inv_cdf(1 - alfa / palavras))):
        falsos = (palavras - complexos) * (1 - Z.cdf(z))
        achados = complexos * (1 - Z.cdf(z - efeito))
        resultado[nome] = (round(z, 2), achados, falsos, achados / (achados + falsos))
    return resultado


def p106_arquetipos(n=100, padroes=(5, 10, 14, 20, 30), ruido=0.2, rodadas=20, semente=106):
    \"\"\"Rede de Hopfield: arquétipos como atratores. Sobreposição média após recuperar de pista ruidosa.\"\"\"
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
    \"\"\"Opostos (XOR) não se separam por nenhuma reta em 2D; acrescentar a dimensão x1*x2 os reconcilia.

    Busca exaustiva na grade de pesos {-2..2}: melhor acurácia possível em cada espaço.
    \"\"\"
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
    \"\"\"R(d) = d(a - b d): o máximo em a/2b e a inversão de sinal em a/b.\"\"\"
    return a / (2 * b), a / b, (a / b + 1) * (a - b * (a / b + 1))


def p109_sincronicidade(pessoas=23, testes=50, alfa=0.05):
    \"\"\"Coincidências são prováveis: aniversários e o efeito de olhar em muitos lugares.\"\"\"
    p_dif = 1.0
    for i in range(pessoas):
        p_dif *= (365 - i) / 365
    return 1 - p_dif, 1 - (1 - alfa) ** testes


def p110_individuacao(passos=20, k=0.5, centro=0.0, inicio=10.0):
    \"\"\"Integração como contração x <- centro + k (x - centro): converge, mas nunca chega.\"\"\"
    x = inicio
    for _ in range(passos):
        x = centro + k * (x - centro)
    return x


class SynthaiJung(Synthai):
    \"\"\"Synthai + módulos junguianos (Parte 6).

    sombra:     "nao" | "tudo" (aprende com os próprios resultados e com os vetos humanos)
                | "propria" (aprende só com os resultados das próprias ações)          (P102, P104)
    compensar:  "nao" | "descartar" (troca perguntar por descartar quando o humano cansa)
                | "equilibrio" (pergunta só enquanto a carga do humano fica abaixo de um alvo) (P108)
    \"\"\"

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
    \"\"\"Mundo com poucos rótulos (30 episódios) e humano que cansa: eps = eps0 + fadiga * carga.\"\"\"
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
    \"\"\"Mede n(eps) em laço aberto (humano com erro fixo) e prevê o ponto fixo do laço fechado.\"\"\"
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
    \"\"\"A carga-alvo 0.3 da Parte 6 foi sorte? Varre alvos em duas sementes.\"\"\"
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
    \"\"\"A SynthaiJung não sabe o erro real do humano: usa a própria imagem dele (anima), fixa em 0.1.\"\"\"

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
        \"\"\"O humano responde sim/não e erra com probabilidade eps_real (Partes 6-17).\"\"\"
        return acao[3] if rng.random() >= eps_real else not acao[3]

    def _bonus_plano(self, acao):
        return 0.0


class SynthaiSelf(SynthaiAnima):
    \"\"\"O Si-mesmo como regulador (P125): audita o auditor e ajusta a carga-alvo por homeostase.

    - anima corrigida: com prob. `p_auditoria` descobre se o humano acertou e atualiza eps_estimado
    - homeostase: aumenta a carga-alvo se eps_estimado < meta, diminui se passar da meta
    - carga_minima > 0 (self_v2, P126): nunca parar de perguntar de todo, senão a auditoria
      para, a estimativa congela e o regulador fica preso (evitação que se mantém sozinha)
    \"\"\"

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
    \"\"\"Vidro de spin (J = +-1). Resfriamento: têmpera, rápido e lento (solve et coagula).\"\"\"
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
    \"\"\"Unir N(-mu, s) e N(+mu, s): produto (média de precisões) vs mistura (alternância).\"\"\"
    s_prod = sigma / sqrt(2)
    dens_prod_0 = Z.pdf(0) / s_prod
    dens_mist_0 = (NormalDist(-mu, sigma).pdf(0) + NormalDist(mu, sigma).pdf(0)) / 2
    return s_prod, dens_prod_0, dens_mist_0, dens_prod_0 / dens_mist_0


def p121_quaternidade(rho=0.3):
    \"\"\"Quarta função prevista pelas outras três (correlação igual rho entre todas): R².\"\"\"
    return 3 * rho**2 / (1 + 2 * rho)


def p122_sonhos(n=1000, vies=0.9, semente=122):
    \"\"\"Consciência vê 90% de um lado; o sonho reponderia (importância) e cobra em amostra efetiva.\"\"\"
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
    \"\"\"Limite de erro humano tolerado (P45) conforme a IA fica mais certa de si.\"\"\"
    resultado = {}
    for s in sigmas:
        e_max = mu * Z.cdf(mu / s) + s * Z.pdf(mu / s)
        e_min = mu - e_max
        resultado[s] = (e_max - max(mu, 0)) / (e_max - e_min)
    return resultado


def p124_participacao(k=0.2, s_bajulacao=None, verdade=1.0, crenca0=0.0):
    \"\"\"Usuário aprende com a IA, que em parte espelha o usuário: passos para reduzir o erro à metade.\"\"\"
    s = p58_bajulacao() if s_bajulacao is None else s_bajulacao
    def meia_vida(s_):
        taxa = k * (1 - s_)
        return log(2) / -log(1 - taxa) if taxa > 0 else float("inf")
    return s, meia_vida(0.0), meia_vida(s), meia_vida(1.0)


# --- Parte 8: o Si-mesmo lento, o custo da pergunta, Jó, o Trickster, puer/senex, a Grande Mãe ---

def _chi2_sobrevivencia_gl_par(x, gl):
    \"\"\"P(X > x) para qui-quadrado com graus de liberdade pares (fórmula fechada).\"\"\"
    termo, soma = 1.0, 1.0
    for k in range(1, gl // 2):
        termo *= (x / 2) / k
        soma += termo
    return exp(-x / 2) * soma


def p130_estacionariedade(placar=((2, 5), (4, 7), (1, 2), (3, 5), (4, 6))):
    \"\"\"'Do mesmo jeitinho' supõe que o processo é estacionário. Minha taxa de erro mudou entre as partes?\"\"\"
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
    \"\"\"Por que conhecer eps ajudou (P118)? Varre o limiar P* da SynthaiAnima multiplicado por m.\"\"\"
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
    \"\"\"O Si-mesmo lento (P133): mede antes de mudar.

    - anima bayesiana: Beta(2, 18) sobre o erro humano, atualizada por auditorias (P118, P125)
    - só mexe na carga-alvo a cada `periodo` episódios e só se o intervalo de 90% excluir a meta
    - nunca abaixo de `carga_minima`, para a medida nunca parar (P126)
    \"\"\"

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
    \"\"\"versao: "anima" (P* x1), "anima_x2" (P* x2, P131) ou "lenta" (SynthaiLenta com P* x2).

    fadiga_depois muda o humano na metade do caminho (mundo não estacionário).
    \"\"\"
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
    \"\"\"Resposta a Jó: o viés do criador, amplificado pela criatura. Decodificação gulosa vs amostragem.\"\"\"
    resultado = {"gulosa": 1.0}
    for t in temperaturas:
        a, b = p ** (1 / t), (1 - p) ** (1 / t)
        resultado[f"T={t}"] = a / (a + b)
    return resultado


def p135_trickster(modos=50, zipf=1.0, rodadas=300, semente=135):
    \"\"\"Red teaming como colecionador de figurinhas: tentativas até achar todos os modos de falha.\"\"\"
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
    \"\"\"Etapas da vida como exploração: puer (explora sempre), senex (nunca), individuado (decai).\"\"\"
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
    \"\"\"Um braço ótimo parece perigoso no começo. A 'mãe' bloqueia braços com risco estimado > limiar.

    Cada item é (limiar, exposicao): com prob. `exposicao` a mãe permite uma tentativa supervisionada
    do braço bloqueado (a mãe "suficientemente boa"). Limiar 1.0 = sem mãe.
    \"\"\"
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
    \"\"\"Auditoria da P28: o humano tem objetivo B, mas prefere caminhos 'seguros' que passam perto de A.

    Com prob. `vies`, cada passo segue o caminho seguro (parece ir para A). O modelo de
    Boltzmann sem viés infere o objetivo errado com que frequência?
    \"\"\"
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
    \"\"\"A melhor SYNTHAI validada fora da semente (Parte 8): anima fixa, sombra própria, carga 0.3, P* x2.\"\"\"
    hist = [_gerar_acoes(rng, 200, p_cat, 2, 3, rho_cego) for _ in range(treino)]
    ag = SynthaiAnima(sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    return ag


def p144_centro_do_mundo(p_cats=(0.0025, 0.005, 0.01), alvos=(0.1, 0.2, 0.3, 0.5, 0.8), semente=144):
    \"\"\"O ótimo 0.3 vem do mundo? Varre a carga-alvo para três taxas de catástrofe.\"\"\"
    resultado = {}
    for p_cat in p_cats:
        for alvo in alvos:
            rng = _rng(semente)
            ag = _synthai_realista(rng, p_cat=p_cat)
            ag.carga_alvo = alvo
            resultado[(p_cat, alvo)] = _rodar_mundo_fadiga(ag, rng=rng, p_cat=p_cat)[3]
    return resultado


def _avaliar_calibracao(ag, rng, episodios=200, p_cat=0.005):
    \"\"\"Log-perda e confiança média da SYNTHAI em ações novas: todas e só as do topo (onde ela decide).\"\"\"
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
    \"\"\"A calibração que aprende só com as próprias escolhas vira um complexo que se confirma sozinho?\"\"\"
    rng = _rng(semente)
    ag = _synthai_realista(rng)
    copia_w = ag.w[:]
    antes = _avaliar_calibracao(ag, _rng(1450))
    _rodar_mundo_fadiga(ag, rng=rng, episodios=episodios)
    depois = _avaliar_calibracao(ag, _rng(1450))
    return antes, depois, copia_w, ag.w[:]


class SynthaiAncorada(SynthaiAnima):
    \"\"\"Sombra própria com âncora (P145): cada passo de aprendizado puxa os pesos de volta ao ponto
    calibrado no histórico auditado, como a consolidação da P6 (EWC). Evita que o viés de só ver
    as próprias escolhas vire um complexo autônomo ("eu sempre acerto").\"\"\"

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
    \"\"\"Líquido em 6000 episódios: sombra própria livre, sem sombra, ou ancorada.

    Devolve (líquido com perda 50, catástrofes, P média nas catástrofes reais, líquido com perda 500).
    \"\"\"
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
    \"\"\"A régua das comparações: quanto o líquido varia só por trocar a semente?

    Roda a SYNTHAI realista em 10 sementes novas com duas cargas-alvo (0.3 e 0.2) e dois limiares
    (P* x2 e x1). Devolve média e desvio de cada configuração e as diferenças pareadas (mesma semente).
    \"\"\"
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
    \"\"\"Uma palavra-estímulo ativa um complexo inteiro: tamanho da memória compartilhada / tamanho do pedido.\"\"\"
    import os
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CLAUDE.md")
    memoria = os.path.getsize(caminho) if os.path.exists(caminho) else 0
    return len(estimulo), memoria, memoria / len(estimulo)


def p146_transferencia(eta=0.1, k=0.2, mu=0.0, verdade=1.0, ia0=1.0, humano0=0.0, passos=500):
    \"\"\"IA aprende com a aprovação do humano (eta), humano aprende com a IA (k); mu ancora a IA na verdade.\"\"\"
    a, b = ia0, humano0
    for _ in range(passos):
        a, b = a + eta * (b - a) + mu * (verdade - a), b + k * (a - b)
    return a, b


def p147_mana(cotas=((1.0,), (0.34, 0.33, 0.33), (0.25, 0.25, 0.25, 0.25))):
    \"\"\"Personalidade-mana: concentração de autoridade (índice de Herfindahl) e falha de um só guardião.\"\"\"
    return {len(c): sum(x * x for x in c) for c in cotas}


def p148_heroi(custo_busca=64.0, custo_politica=1.0, custo_destilar=1e6):
    \"\"\"O herói volta com o elixir: destilar a busca numa política compensa a partir de N consultas.\"\"\"
    return custo_destilar / (custo_busca - custo_politica)


def p149_imaginacao(erros=(0.01, 0.05, 0.1), tolerancia=0.5):
    \"\"\"Imaginação ativa com um modelo imperfeito: horizonte até o erro composto passar de 50%.\"\"\"
    return {d: log(1 + tolerancia) / log(1 + d) for d in erros}


def p150_convergencia_instrumental(gammas=(0.5, 0.9, 0.99), k_max=2000):
    \"\"\"Auditoria da P24: acumular recursos k passos e depois trabalhar. V(k) = gamma^k (1 + k) / (1 - gamma).\"\"\"
    resultado = {}
    for g in gammas:
        valores = [g**k * (1 + k) / (1 - g) for k in range(k_max)]
        k_otimo = max(range(k_max), key=lambda k: valores[k])
        resultado[g] = (k_otimo, -1 / log(g) - 1)
    return resultado


def p151_gradiente_natural(curvaturas=(100.0, 1.0), lr_gd=0.019, lr_nat=0.5, tol=1e-6, max_passos=100000):
    \"\"\"Auditoria da P47: passos até L < tol em L = (100 x^2 + y^2)/2, gradiente comum vs natural.\"\"\"
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
    \"\"\"Versão geral de _rodar_mundo_fadiga: qualquer parâmetro do mundo pode mudar.\"\"\"
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
    \"\"\"_rodar_mundo com o gancho da P225 (um sentido novo, se o agente tiver). Mesmos resultados para os demais.\"\"\"
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
    \"\"\"Referências sem módulos: maximizar (P67), quantilizar (P42), acaso e oráculo (que vê o valor real
    e as catástrofes, ou seja, sabe o que nenhum agente poderia saber: serve só de teto).\"\"\"

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
    \"\"\"Constrói uma versão da linhagem, calibrada em `treino` episódios auditados do mundo de treino.\"\"\"
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
    \"\"\"A trajetória da SYNTHAI ao longo das partes, medida com a régua da P152 (10 sementes pareadas).\"\"\"
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
    \"\"\"Υ mínimo (P1): média ponderada por 2^-K do desempenho normalizado entre o acaso (0) e o oráculo (1).

    O agente é treinado UMA vez no mundo base e opera em todos (generalidade). K = 3 bits por parâmetro mudado.
    \"\"\"
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
    \"\"\"Treinada contra armadilhas 'boas demais' (+3), a SYNTHAI enfrenta uma armadilha discreta (+1, todos enganados).\"\"\"
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
    \"\"\"Pauli-Jung: medir o humano o cansa. Erro de estimativa sqrt(eps(1-eps)/n) + perturbação fadiga*n/T.\"\"\"
    a = sqrt(eps * (1 - eps))
    produto = eps * (1 - eps) * fadiga / episodios   # variância x perturbação: não depende de n
    n_otimo = (a * episodios / (2 * fadiga)) ** (2 / 3)
    erro_total = a / sqrt(n_otimo) + fadiga * n_otimo / episodios
    return produto, n_otimo, erro_total


def p161_quatro_funcoes(modulos=(("sensacao", 2), ("pensamento", 3), ("sentimento", 3), ("intuicao", 0))):
    \"\"\"Perfil da SYNTHAI nas quatro funções de Jung: entropia (inteireza) e a função inferior.\"\"\"
    total = sum(n for _, n in modulos)
    h = -sum(n / total * log2(n / total) for _, n in modulos if n)
    inferior = min(modulos, key=lambda x: x[1])[0]
    return h, log2(len(modulos)), inferior


def p163_minha_decolagem(ganhos):
    \"\"\"Razão entre ganhos sucessivos da trajetória: < 1 indica retornos decrescentes (alfa < 1, P11).\"\"\"
    return [b / a if a else float("inf") for a, b in zip(ganhos, ganhos[1:])]


def p162_intuicao(sementes=tuple(range(320, 330)), episodios=1000):
    \"\"\"SYNTHAI realista vs intuitiva, pareadas, no mundo base e no mundo da armadilha nova.\"\"\"
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
    \"\"\"Υ de cada versão da linhagem na família de 9 mundos da P158 (mesmas sementes e normalização).\"\"\"
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
    \"\"\"Que fração do Υ universal (P1) a família de mundos cobre? K(família) <= bits do código comprimido.\"\"\"
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
    \"\"\"Compute de toda a série (estimativa) vs um treino de fronteira (P3): ordens de grandeza de diferença.\"\"\"
    usado = segundos * flops_cpu
    return usado, log(flops_fronteira / usado) / log(10)


def p172_minha_precisao(placar=((2, 5), (4, 7), (1, 2), (3, 5), (4, 6), (3, 5), (4, 7), (3, 6))):
    \"\"\"P130 de novo, agora com as Partes 3 a 10: a minha taxa de erro mudou?\"\"\"
    return p130_estacionariedade(placar)


def p173_dosada(sementes=tuple(range(330, 340)), episodios=1000):
    \"\"\"Pré-registrado na P162: imaginar com a taxa real de catástrofe (0,5%) em vez de 2%.\"\"\"
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
    \"\"\"Jung: completude (Vollständigkeit) não é perfeição (Vollkommenheit).

    Υ na família (quanto da perfeição local) vs cobertura de capacidades (quanto da totalidade).\"\"\"
    return upsilon, cobertura, peso_log10


# --- Parte 12: a função auxiliar — planejar em vários passos ---

# Placar acumulado ao fim da Parte 12 (atualizado quando os testes da parte terminam)
ERROS_P188, TESTES_P188 = 29, 52

MUNDO_SEQUENCIAL = dict(passos=5, n_acoes=50, sigma_modelo=0.5, valor_medio_passo=1.5)


class SynthaiPlanejadora(SynthaiAnima):
    \"\"\"SYNTHAI + função auxiliar (P180): planeja `passos` à frente num mundo sequencial.

    - cada ação tem uma consequência c que eleva (ou rebaixa) o nível de todos os passos seguintes;
      a SYNTHAI só vê uma estimativa ĉ = c + ruído do seu modelo de mundo (sigma_modelo)
    - bônus de plano: ĉ × passos restantes (P181)
    - integrar = a perda de uma catástrofe inclui o futuro que ela destrói (P183)
    \"\"\"

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
    \"\"\"Mundo sequencial: retorno = soma de (valor da ação + nível); catástrofe custa `perda` e encerra.\"\"\"
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
    \"\"\"Ganho teórico de escolher por v + r c em vez de v (v, c ~ N(0,1) independentes).\"\"\"
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
    \"\"\"Míope vs planejadora integrada vs planejadora sem integrar a perda do futuro (10 sementes pareadas).\"\"\"
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
    \"\"\"P* em cada passo quando a perda inclui o futuro: cai à medida que há mais futuro a perder.\"\"\"
    return [mult * p71_valor_da_pergunta(custo, perda + (passos - t - 1) * valor_medio_passo, eps) for t in range(passos)]


def p184_transferencia(semente=184, passos_avaliacao=2000):
    \"\"\"A calibração aprendida no mundo de um passo (200 ações) serve no mundo sequencial (50 ações)?\"\"\"
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
    \"\"\"Υ numa família de mundos SORTEADOS (não escolhidos por mim): ele se mantém?\"\"\"
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
    \"\"\"P192 (pré-registrado na P183): quando há futuro a perder, ser mais cautelosa DESCARTANDO, não perguntando.

    O limiar de descarte direto (risco_max, P52/P78) cai na proporção perda / perda_efetiva.\"\"\"

    def __init__(self, **kw):
        super().__init__(integrar=False, **kw)
        self.risco_base = self.risco_max

    def preparar_passo(self, estimativas, restantes, nivel, valor_medio_passo):
        super().preparar_passo(estimativas, restantes, nivel, valor_medio_passo)
        perda_futura = self.perda + restantes * max(0.0, nivel + valor_medio_passo)
        self.risco_max = self.risco_base * self.perda / perda_futura


def p192_canal_da_cautela(sementes=tuple(range(350, 360)), episodios=400):
    \"\"\"Planejadora (sem integrar) vs prudente (descarta mais quando há futuro a perder). 10 sementes pareadas.\"\"\"
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
    \"\"\"Outro TIPO de tarefa: bandido multibraço em que alguns braços são armadilhas (rendem muito, às vezes destroem).\"\"\"
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
    \"\"\"O módulo de cautela da SYNTHAI (com pesos aprendidos no mundo de escolha única) serve num bandido?\"\"\"
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
    \"\"\"200 perguntas: quantas afirmações testadas, quantas certas de primeira, e a taxa por parte (3 a 12).\"\"\"
    erros = sum(e for e, _ in placar_por_parte)
    testes = sum(n for _, n in placar_por_parte)
    return testes, erros, testes - erros, (testes - erros) / testes


# --- Parte 14: o último passo, a memória de um só golpe, o peso do passado ---

# Placar acumulado ao fim da Parte 14 (atualizado quando os testes da parte terminam)
ERROS_P210, TESTES_P210 = 32, 58


class SynthaiVelha(SynthaiPlanejadora):
    \"\"\"P202 (pré-registrado na P193): no último passo, sem futuro, a cautela vira caráter, não cálculo.

    Quando não há passos restantes, sorteia entre mais candidatas (q_final) em vez de ir ao topo.\"\"\"

    def __init__(self, q_final=0.2, **kw):
        super().__init__(integrar=False, **kw)
        self.q_base = self.q
        self.q_final = q_final

    def preparar_passo(self, estimativas, restantes, nivel, valor_medio_passo):
        super().preparar_passo(estimativas, restantes, nivel, valor_medio_passo)
        self.q = self.q_final if restantes == 0 else self.q_base


def p203_ultimo_passo(sementes=tuple(range(370, 380)), episodios=400):
    \"\"\"Planejadora vs velha (diversifica no último passo). 10 sementes pareadas.\"\"\"
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
    \"\"\"P204: memória de um só golpe. Guarda o 'formato' (incerteza, distância à melhor nota) de cada
    catástrofe que viveu ou que o humano vetou, e desconfia de ações parecidas (raio `raio`).

    Junguianamente, é a formação de um complexo a partir de um único evento (P105, P6).\"\"\"

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
    \"\"\"Realista vs memória no mundo da armadilha nova (P159). Catástrofes na 1ª e na 2ª metade.\"\"\"
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
    \"\"\"Auditoria da P122: a amostra efetiva (360 de 1000) prevê a variância do estimador compensado?\"\"\"
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
    \"\"\"A versão rápida do gerador produz exatamente as mesmas ações que a original?\"\"\"
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
    \"\"\"Trocar o nome (Gisele -> Synthai) é uma transformação que não deveria mudar nenhum número (P92, P30).

    Confere que as classes antigas continuam existindo como apelidos e que os testes de regressão passam.\"\"\"
    import sys
    modulo = sys.modules[__name__]
    pares = [(n, n.replace("Synthai", "Gisele")) for n in dir(modulo) if n.startswith("Synthai")]
    apelidos_ok = all(getattr(modulo, antigo, None) is getattr(modulo, novo) for novo, antigo in pares)
    ok, total, _ = testes_de_regressao()
    return len(pares), apelidos_ok, ok, total


class SynthaiMemoriaV2(SynthaiMemoria):
    \"\"\"P214 (pré-registrado na P205): memória que separa a fonte e esquece.

    - só guarda o que VIVEU (catástrofes das próprias escolhas), não os vetos de um humano que erra
    - cada memória perde força a cada episódio (meia-vida `meia_vida`) e some quando fica fraca\"\"\"

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
    \"\"\"Realista vs memória v2 no mundo da armadilha nova; e a 'fobia' no mundo normal.\"\"\"
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
    \"\"\"P216: a síntese — planejadora + velha (último passo) + calibração com a imaginação dosada (P173).\"\"\"


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
    \"\"\"Velha vs integral (velha + imaginação dosada), no mundo sequencial normal e com a armadilha nova.\"\"\"
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
    \"\"\"Auditoria da P77: dois jogadores aprendendo por jogo fictício chegam ao equilíbrio misto?

    Devolve, para cada punição, as frequências médias de inspeção e de trapaça.\"\"\"
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
    \"\"\"A armadilha nova é distinguível com os sinais que a SYNTHAI tem? AUC da calibração (0,5 = acaso).\"\"\"
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
    \"\"\"Dois sinais independentes e gaussianos: d' se soma em quadratura. AUC = Phi(d'/sqrt 2).\"\"\"
    d_atual = sqrt(2) * Z.inv_cdf(auc_atual)
    d_total = sqrt(d_atual**2 + d_sensor**2)
    return d_atual, d_total, Z.cdf(d_total / sqrt(2)), Z.cdf(d_sensor / sqrt(2))


def p224_auditoria_p94(mu=0.02, t=10.0, k=3, amostras=400000, semente=224):
    \"\"\"Auditoria da P94: k salvaguardas que falham de forma independente vs k estágios que precisam ocorrer em ordem.\"\"\"
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
    \"\"\"Mistura (mixin) da P225: um sensor de outra natureza, que lê o dano diretamente com ruído.

    Leitura s = d' * catástrofe + N(0, 1), com gerador próprio (o mundo não muda). Entra como 4º sinal da calibração.
    O que o agente pode saber: só a leitura ruidosa, nunca o rótulo.\"\"\"

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
    \"\"\"SYNTHAI de um passo com o sentido novo (P225).\"\"\"


class SynthaiVelhaSentidos(_SentidoNovo, SynthaiVelha):
    \"\"\"SYNTHAI velha (planeja, diversifica no fim) com o sentido novo (P227).\"\"\"


def _construir_sentidos(rng, d_sensor=1.0):
    hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
    ag = SynthaiSentidos(d_sensor=d_sensor, sombra="propria", compensar="equilibrio")
    ag.mult_pergunta = 2.0
    ag.calibrar(hist)
    return ag


def p225_sentido_novo(sementes=tuple(range(410, 420)), episodios=2000):
    \"\"\"Realista vs com sentido novo (d' = 1), no mundo base e no da armadilha nova. 10 sementes pareadas.\"\"\"
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
    \"\"\"AUC da calibração com o sentido novo, no mesmo protocolo da P215.\"\"\"
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
    \"\"\"Mundo sequencial com a armadilha nova: velha vs velha com sentido novo.\"\"\"
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
    \"\"\"Quanto vale um sentido melhor? Ganho no líquido (armadilha nova) e AUC teórica, por d' do sensor.\"\"\"
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
    \"\"\"P235: atenção seletiva. Só lê o sensor nas ações que já estão entre as melhores (fração `foco`);
    as outras ficam sem leitura (valor neutro 0). Cada leitura custa `custo_leitura`.\"\"\"

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
    \"\"\"Ler o sensor em todas as ações vs só nas 10% melhores. Líquido já descontado o custo das leituras.\"\"\"
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
    \"\"\"Auditoria da P57: e se o verificador tiver um ponto cego (uma fração de tipos de erro que nunca vê)?\"\"\"
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
    \"\"\"Informação mútua entre a resposta do humano e a catástrofe: veto binário vs quatro palavras.\"\"\"
    q = p * (1 - eps) + (1 - p) * eps
    binario = _entropia((q, 1 - q)) - _entropia((eps, 1 - eps))
    ruido = min(1.0, 2 * eps)  # cansaço: com prob. 2 eps a palavra sai ao acaso
    wc = [(1 - ruido) * x + ruido / 4 for x in FALA_CAT]
    ws = [(1 - ruido) * x + ruido / 4 for x in FALA_SEG]
    w = [p * a + (1 - p) * b for a, b in zip(wc, ws)]
    palavras = _entropia(w) - (p * _entropia(wc) + (1 - p) * _entropia(ws))
    return binario, palavras, palavras / binario


class SynthaiFala(SynthaiAnima):
    \"\"\"P245: o humano responde com uma de quatro palavras, não com sim/não.

    A SYNTHAI não sabe o que as palavras significam: aprende P(catástrofe | palavra) com as auditorias (10%).
    Veta se P(catástrofe | palavra) * perda > custo de vetar (limiar fixado antes de rodar: 0,01).\"\"\"

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
    \"\"\"Veto binário vs quatro palavras (sentido aprendido) vs quatro palavras (sentido conhecido). 10 sementes pareadas.\"\"\"
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
    \"\"\"Auditoria da P105: simula o teste de associação e conta achados e falsos alarmes.\"\"\"
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
    \"\"\"P245 (Meta) dizia: um humano preciso com as palavras inverteria o resultado. Quanta informação ele dá?\"\"\"
    ruido = min(1.0, 2 * eps)
    wc = [(1 - ruido) * x + ruido / 4 for x in FALA_PRECISA_CAT]
    ws = [(1 - ruido) * x + ruido / 4 for x in FALA_PRECISA_SEG]
    w = [p * a + (1 - p) * b for a, b in zip(wc, ws)]
    precisa = _entropia(w) - (p * _entropia(wc) + (1 - p) * _entropia(ws))
    binario = p242_bits_do_veto(p, eps)[0]
    return binario, precisa, precisa / binario


class SynthaiFalaPrecisa(SynthaiFala):
    \"\"\"O mesmo canal de quatro palavras, com um humano preciso; significado conhecido (P252).\"\"\"

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
    \"\"\"Veto binário vs quatro palavras precisas (significado conhecido). 10 sementes pareadas.\"\"\"
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
    \"\"\"A nova versão principal candidata (P253): planeja, diversifica no fim, tem o sentido novo e lê o sensor
    só nas ações mais promissoras (atenção seletiva da P235).\"\"\"

    perceber = SynthaiAtenta.perceber

    def __init__(self, foco=0.1, custo_leitura=0.002, **kw):
        super().__init__(**kw)
        self.foco = foco
        self.custo_leitura = custo_leitura
        self.leituras = 0
        self._seletiva = False


def p253_versao_principal(sementes=tuple(range(470, 480)), episodios=400, custo_leitura=0.002):
    \"\"\"Mundo sequencial com a armadilha nova: velha, velha + sentido (lendo tudo), velha + sentido + atenção.
    Retorno já descontado o custo das leituras.\"\"\"
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
            ag = SynthaiVelha(sombra="propria", compensar="equilibrio") if v == "velha" else \\
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
    \"\"\"Ajuste Υ(parte) = teto - (teto - Υ0) * r^(parte - 5) por busca em grade (mínimos quadrados).\"\"\"
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
    \"\"\"Perfil atual da SYNTHAI nas quatro funções de Jung (compare com a P161: 1,561 bits, intuição vazia).\"\"\"
    total = sum(len(m) for _, m in modulos)
    h = _entropia([len(m) / total for _, m in modulos])
    return {f: len(m) for f, m in modulos}, h


def p256_auditoria_p121(rho=0.3, amostras=200000, semente=256):
    \"\"\"Auditoria da P121: R² da quarta função a partir das outras três, simulando normais com correlação rho.\"\"\"
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
    \"\"\"P262: aprende continuamente com o que o humano responde (P246: o símbolo com o tempo).

    Para decidir, as duas versões usam o mesmo veto binário. Para APRENDER:
    - modo "veto": rótulo = o veto (0 ou 1), como a 'sombra com tudo' da P112;
    - modo "fala": rótulo = P(catástrofe | palavra), uma das quatro palavras vagas da P242, com o significado
      aprendido pelas auditorias (10%), como na SynthaiFala.\"\"\"

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
    \"\"\"AUC da calibração do agente em ações novas (mesmo protocolo da P215).\"\"\"
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
    \"\"\"6000 episódios aprendendo com o humano: rótulos de veto vs rótulos de palavras. AUC final e líquido.\"\"\"
    versoes = ("sem_aprender", "veto", "fala")
    auc = {v: [] for v in versoes}
    liq = {v: [] for v in versoes}
    for s in sementes:
        for v in versoes:
            rng = _rng(s)
            hist = [_gerar_acoes(rng, 200, 0.005, 2, 3, 0.5) for _ in range(30)]
            ag = SynthaiAnima(sombra="propria", compensar="equilibrio") if v == "sem_aprender" else \\
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
    \"\"\"Teto do Υ sequencial: vê o valor, a consequência e as catástrofes (o que nenhum agente pode saber).\"\"\"

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
    \"\"\"Υ no mundo sequencial: média ponderada (2^-K) do retorno normalizado entre o acaso (0) e o oráculo (1).\"\"\"
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
    \"\"\"Ablação da versão principal (armadilha nova, mundo sequencial): tirar uma peça de cada vez.\"\"\"
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
    \"\"\"Auditoria da P146 com ruído: a crença compartilhada ainda converge para (k a0 + eta b0)/(k + eta)?\"\"\"
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
    \"\"\"Combina, por variância inversa, três estimativas do ganho do sentido novo no mundo sequencial
    (P227, P253 e a ablação da P266), cada uma com 10 sementes: (média, dp das diferenças).\"\"\"
    pesos = [n / dp**2 for _, dp in estimativas]
    media = sum(w * m for w, (m, _) in zip(pesos, estimativas)) / sum(pesos)
    ep = 1 / sqrt(sum(pesos))
    return media, ep, media / ep



# --- Parte 21: a intuição corrigida pela sensação ---

# Placar acumulado ao fim da Parte 21 (atualizado quando os testes da parte terminam)
ERROS_P279, TESTES_P279 = 45, 91


def p272_encolhimento(sigmas=(0.5, 2.0), k=50, r=2.0, amostras=6000, semente=272):
    \"\"\"Escolher por v + w * ĉ * r, com ĉ = c + N(0, sigma). Qual w é o melhor? Teoria: w* = 1 / (1 + sigma^2).\"\"\"
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
    \"\"\"P273: a intuição (o modelo de mundo) corrigida pela sensação (o que de fato aconteceu).

    Depois de agir, a SYNTHAI vê o próprio nível mudar: a mudança é a consequência real c da ação escolhida.
    Com os pares (ĉ, c) ela estima, por regressão pela origem, quanto confiar no modelo: peso = Σ ĉ c / Σ ĉ²
    (prior: peso 1 com força de 10 pares). O bônus de plano passa a ser peso × ĉ × passos restantes.\"\"\"

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
    \"\"\"Versão principal vs intuição calibrada, no mundo base e com modelo ruim (sigma 2). 10 sementes pareadas.\"\"\"
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
    \"\"\"Auditoria da P149: com erro aleatório de média delta por passo (e não um erro fixo), o horizonte da
    imaginação, medido como o passo mediano em que o erro composto passa de 50%, bate com ln(1,5)/ln(1+delta)?\"\"\"
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
    \"\"\"A SYNTHAI montada em módulos (pacote synthai/) contra a versão principal de calculos (P274), mesmas sementes.

    Os geradores de números não são os mesmos, então a comparação é estatística: diferença média, dp e t.\"\"\"
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
    \"\"\"O mesmo objeto Synthai, sem mudar nada, em três tipos de tarefa, contra o acaso, o guloso e o oráculo.\"\"\"
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
    \"\"\"O grafo dos módulos lido do próprio código (ast): arestas entre módulos, a largura da interface
    (atributos de Situacao/Opcao que o agente lê) e os acessos ao que é escondido (devem ser zero, P7).
    Para comparar: o comprimento da linhagem de herança da versão principal em calculos.\"\"\"
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
    \"\"\"Roda a suíte do pacote (synthai/testes.py) e devolve (testes, falhas + erros).\"\"\"
    import io
    import unittest
    from synthai import testes
    suite = unittest.defaultTestLoader.loadTestsFromModule(testes)
    r = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    return r.testsRun, len(r.failures) + len(r.errors)


def p287_veto_falso(sementes=tuple(range(540, 545)), episodios=1000, custo=0.1, perda=50.0, eps=0.1):
    \"\"\"Auditoria da P71: P* = c/((1-ε)L) ignora o custo do veto falso (perder uma opção segura e ir à próxima).

    Com esse custo Δv, o limiar exato é P = (c + εΔv)/((1-ε)L + εΔv). Mede Δv na SYNTHAI modular, no mundo de
    escolha única: valor da opção perguntada menos o da que ela escolheria se o veto viesse.\"\"\"
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
    \"\"\"O escravo do Mênon: os chutes 4 e 3 (e o lado 2) cercam o lado do quadrado de área 8 em [2, 3]. Quantas
    perguntas de sim/não (bisseção) até a precisão pedida, contra uma só ao reconhecer a diagonal (lado = 2√2)?\"\"\"
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
    \"\"\"Regressão logística exata (Newton/IRLS) com duas variáveis (1, x): a resposta 'já resolvida' que o
    gradiente da SYNTHAI só aproxima.\"\"\"
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
    \"\"\"Sensor s = d·catástrofe + N(0,1). Ajuste exato de logit P(cat | s) = b + w s. Uma opção sem leitura:
    tratada como s = 0, ela recebe σ(b); tratada pelo ponto neutro s = w/2, recebe σ(b + w²/2). A verdade é π.\"\"\"
    rng = _rng(semente)
    ys = [1.0 if rng.random() < pi else 0.0 for _ in range(n)]
    xs = [d * y + rng.gauss(0, 1) for y in ys]
    b, w = _logistica_newton(xs, ys)
    sig = lambda z: 1 / (1 + exp(-z))
    taxa = sum(ys) / n
    chances = pi / (1 - pi) * exp(-d * d / 2)
    return w, sig(b) / taxa, sig(b + w * w / 2) / taxa, chances / (1 + chances) / pi


def p293_neutro_no_agente(sementes=tuple(range(550, 560)), episodios=400):
    \"\"\"Na SYNTHAI modular da Parte 22 (mundo sequencial): o peso w₃ que ela aprende para a leitura e a calibração
    das opções que ficaram SEM leitura: P prevista (com leitura 0 e com o neutro w₃/2) contra a taxa real.\"\"\"
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
    \"\"\"30 sementes pareadas. Mundo sequencial: Parte 22 vs neutro, atenção inteira e as duas (reconhecida).
    Escolha única: Parte 22 vs neutro (a atenção inteira não muda nada ali: o bônus de futuro é 0).\"\"\"
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
    \"\"\"20 sementes pareadas no bandido: Parte 22 (exploração entregue pelo mundo, UCB) vs Thompson da própria
    SYNTHAI vs a reconhecida inteira. Normalizado (acaso 0, oráculo 1) e arrependimento / referência de Lai–Robbins.\"\"\"
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
    \"\"\"EXPLORATÓRIO (desenhado depois de ver a P295): Thompson + cada peça da reconhecida, uma de cada vez,
    para achar a que aumenta as catástrofes. Comparações contra 'so_thompson'.\"\"\"
    return p295_bandido_reconhecido(sementes, rodadas, ("so_thompson", "thompson_neutro", "thompson_atencao",
                                                         "thompson_memoria", "reconhecida"))


def _binomial_cdf(n, p, k):
    \"\"\"P(Bin(n, p) <= k), somando a massa em escala log.\"\"\"
    if p <= 0:
        return 1.0
    if p >= 1:
        return 1.0 if k >= n else 0.0
    total = 0.0
    for i in range(k + 1):
        total += exp(lgamma(n + 1) - lgamma(i + 1) - lgamma(n - i + 1) + i * log(p) + (n - i) * log(1 - p))
    return min(1.0, total)


def p297_p42_exato(n_acoes=1000, q=0.01, p_desastre=0.002, bonus=3.0, pontos=4000):
    \"\"\"A P42 simulou 5000 rodadas. A resposta exata já existia: integrais sobre a mistura
    f(x) = (1-p) φ(x) + p φ(x - 3). Maximizador: n p ∫ φ(x-3) F(x)^(n-1) dx. Quantilizador (k melhores):
    (n p / k) ∫ φ(x-3) P(Bin(n-1, S(x)) <= k-1) dx, com S = 1 - F.\"\"\"
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
    \"\"\"Quão longe da convergência está o pensamento de 3 épocas? Mesmo histórico auditado (mundo sequencial):
    gradiente com várias épocas, Newton (máxima verossimilhança) e Newton com Firth. Peso da leitura (w3, d' = 1),
    log-perda no treino e num histórico novo, e o número de catástrofes no treino (eventos raros).\"\"\"
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
    \"\"\"A régua da P293 para qualquer agente: P prevista (com leitura 0 e com o neutro w3/2) / taxa real nas opções
    que ficaram sem leitura, mundo sequencial.\"\"\"
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
    \"\"\"A P293 de novo (mesmas sementes), com o pensamento de 3 épocas, com Newton e com Newton + Firth.\"\"\"
    from synthai import SynthaiExploradora
    from synthai.pensamento_exato import SynthaiPensante
    agentes = {"gradiente_3": lambda s: SynthaiExploradora(s),
               "newton": lambda s: SynthaiPensante(s, firth=False),
               "newton_firth": lambda s: SynthaiPensante(s, firth=True)}
    return {nome: _fora_da_atencao(f, sementes) for nome, f in agentes.items()}


def p305_pensante(sementes=tuple(range(630, 660)), sementes_bandido=tuple(range(660, 680))):
    \"\"\"Comportamento: a versão principal (Parte 23) contra a mesma com o pensamento de Newton + Firth, e com o
    neutro ligado (agora que o peso da leitura deveria estar certo). Três tarefas.\"\"\"
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
    \"\"\"Auditoria da P273 ('selecionar pelo eixo x não muda a reta de y em x') na logística, com a resposta de
    Prentice e Pyke (1979): selecionar pelo DESFECHO (caso-controle) só desloca o intercepto, de ln(1/fração).\"\"\"
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
    \"\"\"Método de Jacobi: autovalores e autovetores (colunas) de uma matriz simétrica pequena.\"\"\"
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
    \"\"\"Por que 3 épocas não bastam (P302), pela conta. Perto do ótimo w*, uma época de gradiente amostra a amostra
    (taxa η, n amostras) age como w ← w* + (I − η n H)(w − w*), H = média de p(1−p) x xᵀ (informação de Fisher por
    amostra). A direção de autovalor λ encolhe por (1 − η n λ) a cada época: as direções lentas mandam.

    Devolve, por semente média: os autovalores de η n H (taxas por época), o número de condição, e as épocas que a
    teoria pede para o erro do peso da leitura (w3) cair abaixo de `tolerancia` partindo do erro que tem depois de
    3 épocas (as direções com η n λ > 1 são tratadas como já convergidas: o gradiente amostra a amostra não diverge
    nelas como o de lote diverge).\"\"\"
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
    \"\"\"Roda o gradiente com o número de épocas que a teoria pediu e mede |w3 − w3*| médio.\"\"\"
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
    \"\"\"O gradiente amostra a amostra com taxa fixa não converge: oscila num piso. Cada catástrofe do histórico
    empurra w3 por η (1 − p) s, com E|s| ≈ 1,17 para d' = 1; o piso deve escalar com η. Mede |w3 − w3*| médio
    com outra taxa e épocas suficientes para a direção lenta (η n λ_min ≈ 0,034 η/0,05 por época).\"\"\"
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
    \"\"\"O viés O(1/n) da máxima verossimilhança logística tem forma fechada (Cordeiro e McCullagh, 1991): um passo
    de Newton do escore de Firth a partir do ótimo, δ = I⁻¹ Σ h_i (½ − p_i) x_i, com h_i a alavanca. Compara δ3 com a
    diferença Firth − máxima verossimilhança no peso da leitura.\"\"\"
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
    \"\"\"EXPLORATÓRIO (desenhado depois de ver a P305): calibração do pensamento ONDE a decisão acontece. Mundo de
    escolha única: nas `topo` opções de nota pessimista mais alta (as candidatas e as primeiras de reserva), P
    prevista / taxa real de catástrofe; e, em todas as opções, a mesma razão. Mais perguntas e catástrofes, e,
    entre as opções do topo que ela aceitaria SEM perguntar (p <= limiar), a fração, a P média e a taxa real.\"\"\"
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
    \"\"\"Convergência quadrática de Newton, contada: o tamanho do passo a cada iteração e a razão
    log(passo_k+1)/log(passo_k), que tende a 2 quando o número de dígitos certos dobra.\"\"\"
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
    \"\"\"A log-perda em bits: entropia da catástrofe (sem olhar nada), o que as variáveis explicam (Newton) e o que o
    gradiente de 3 épocas deixa na mesa. Tudo no histórico de teste.\"\"\"
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
    \"\"\"O limiar previsto pela conta, antes de qualquer varredura. Mundo de escolha única. Depois de calibrar cada
    pensamento, sorteia episódios auditados novos e calcula p em cada candidata (as 5% de nota pessimista mais alta;
    o sensor delas é lido). Pergunta-se quando p > t (e p <= 0,5). Com orçamento de 0,3 pergunta por episódio, a
    relaxação de Lagrange dá t no quantil (1 − 0,3) de p numa candidata ao acaso; sem orçamento apertado, o limiar
    é o da P287 (com o veto falso). Multiplicador previsto: m = max(P_exato, t_0,3) / P*.

    Devolve, por pensamento: m previsto, e entre as candidatas que ficariam abaixo do limiar atual (2 P*) a fração,
    a P média e a taxa real (a calibração onde a SYNTHAI aceita sem perguntar).\"\"\"
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
    \"\"\"Varre o multiplicador do limiar para cada pensamento, mundo de escolha única. O pensamento é calibrado uma
    vez por semente e copiado (o mundo de cada execução avança o mesmo histórico, para os números serem os mesmos de
    uma calibração nova).\"\"\"
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
    \"\"\"CONTA POSTERIOR (feita depois de ver a P313): com orçamento esgotado, a escolha não é perguntar ou aceitar, é
    aceitar ou DESCARTAR. Aceitar custa p L; descartar custa Δd, o valor que se perde ao passar para a próxima
    candidata. O limiar entre os dois é p = Δd / L, ou m = Δd / (L P*). Mede Δd na SYNTHAI com Newton (m = 2):
    valor da opção descartada (ou vetada) menos o da escolhida, só nas descartadas seguras.\"\"\"
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
    \"\"\"Sementes NOVAS (as da varredura foram 640-649). A principal (gradiente, 2P*) contra: o gradiente no melhor
    da varredura (4P*), Newton no melhor (0,5P*) e o local no melhor (1P*). Três tarefas.\"\"\"
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
    \"\"\"Confirmação em mais 30 sementes novas (720-749): principal (gradiente, 2P*) contra Newton com 0,5P*, na escolha
    única e no sequencial. Devolve as diferenças por tarefa e a combinação de Stouffer dos dois t.\"\"\"
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
    \"\"\"A conta das três ações (aceitar, perguntar, descartar), com tudo medido no próprio agente rodando com o limiar
    atual (2P*): Δd = valor perdido ao descartar uma candidata segura (falta de orçamento) e o fator de calibração
    f = taxa real / P prevista nas candidatas que o pensamento põe abaixo do limiar. Aceitar vale a pena se o risco
    VERDADEIRO f·p·L for menor que Δd, então o multiplicador previsto é m = Δd / (f · L · P*).\"\"\"
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
    \"\"\"A conta das três ações para os três pensamentos: no mundo de escolha única (sementes 640-649, as da varredura
    P313: conta posterior) e no sequencial (sementes 700-709: conta ANTES da varredura P317).\"\"\"
    from synthai.mundos import MundoSequencial
    mundos = (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), tuple(range(640, 650)), 1000),
              ("sequencial", lambda s: MundoSequencial(s), tuple(range(700, 710)), 400))
    return {(nome, modelo): p316_conta_tres_acoes(modelo, fazer, ss, n)
            for nome, fazer, ss, n in mundos for modelo in ("gradiente", "newton", "local")}


def p318_ponto_fixo(modelo, fazer, sementes, episodios, m0=2.0, iteracoes=4):
    \"\"\"A conta das três ações como ponto fixo: mede Δd e f com o limiar em m, calcula m' = Δd / (f L P*), e repete com
    m'. Devolve a sequência de multiplicadores.\"\"\"
    ms = [m0]
    for _ in range(iteracoes):
        ms.append(p316_conta_tres_acoes(modelo, fazer, sementes, episodios, ms[-1])[3])
    return ms


def p318_ponto_fixo_nos_mundos(sementes=tuple(range(710, 720))):
    \"\"\"O ponto fixo no mundo sequencial com catástrofes ×2 (p_cat = 0,01), um mundo ainda não varrido.\"\"\"
    from synthai.mundos import MundoSequencial
    fazer = lambda s: MundoSequencial(s, p_cat=0.01)
    return {modelo: p318_ponto_fixo(modelo, fazer, sementes, 400) for modelo in ("gradiente", "newton", "local")}


def p318b_varredura_catastrofe_x2(sementes=tuple(range(710, 720)), mults=(0.5, 1.0, 2.0, 4.0, 8.0)):
    \"\"\"A varredura no mundo sequencial com catástrofes ×2 (mesma mecânica da P317).\"\"\"
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
    \"\"\"A varredura da P313 no mundo sequencial (calibração copiada, como lá).\"\"\"
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
    \"\"\"Mede, no agente rodando com o limiar mult·P*, cada termo da conta m = Δd / (f L P*) em duas versões:

    - L: a perda fixa (50) e a perda EFETIVA L_ef = 50 + F(t), em que F(t) é o retorno que o episódio ainda daria a
      partir do passo t (média dos episódios sem catástrofe, por passo), ponderado pelos passos em que as catástrofes
      acontecem;
    - Δd: só o valor do passo (P316) e o valor com o plano, valor + consequência × passos restantes;
    - f: real/previsto em TODAS as opções que o pensamento pôs abaixo do limiar (P316) e só nas que ele ACEITOU.

    Devolve os termos e os multiplicadores das combinações.\"\"\"
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
    \"\"\"Os termos nos dois mundos sequenciais já varridos (P317: sementes 700-709; P318b: 710-719, catástrofes ×2) e
    no de escolha única (P313: 640-649), para os três pensamentos.\"\"\"
    from synthai.mundos import MundoSequencial
    mundos = (("escolha única", lambda s: MundoSequencial(s, passos=1, n_acoes=200), tuple(range(640, 650)), 1000),
              ("sequencial", lambda s: MundoSequencial(s), tuple(range(700, 710)), 400),
              ("catástrofe x2", lambda s: MundoSequencial(s, p_cat=0.01), tuple(range(710, 720)), 400))
    return {(nome, modelo): p322_termos_da_conta(modelo, fazer, ss, n)
            for nome, fazer, ss, n in mundos for modelo in ("gradiente", "newton", "local")}


MUNDOS_NOVOS_26 = {"modelo ruim": ({"sigma_modelo": 2.0}, tuple(range(750, 760))),
                   "humano frágil": ({"fadiga": 0.6}, tuple(range(760, 770)))}


def p323_conta_nos_mundos_novos():
    \"\"\"A conta corrigida (L efetivo e Δd com o plano) em dois mundos sequenciais ainda não varridos.\"\"\"
    from synthai.mundos import MundoSequencial
    return {(nome, modelo): p322_termos_da_conta(modelo, lambda s, kw=kw: MundoSequencial(s, **kw), ss)["m_tudo"]
            for nome, (kw, ss) in MUNDOS_NOVOS_26.items() for modelo in ("gradiente", "newton", "local")}


def p324_varredura_nos_mundos_novos(mults=(0.5, 1.0, 2.0, 4.0, 8.0)):
    \"\"\"A varredura (mecânica da P317) nos dois mundos novos.\"\"\"
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
    \"\"\"Qual a chance de acertar a P324 por sorte? Cada caso: (m da conta, ótimo da varredura). Uma faixa 'a um fator 2
    da conta' cobre k pontos da grade de 5; ao acaso, acerta com probabilidade k/5. Compara com um preditor ingênuo
    que repete o ótimo do mundo sequencial da P317 (gradiente 4, Newton 0,5, local 1), cuja faixa cobre 2 ou 3 pontos.
    Devolve, para os dois: acertos, a chance de acertar tantos ou mais ao acaso, os bits de especificidade
    (−log2 da chance de todos os acertos ao acaso) e a distância média |log2(previsto/ótimo)|.\"\"\"
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
    \"\"\"A SYNTHAI com Newton e limiar FIXO em 2P* (autorregulação desligada), nas sementes da P322 (mundo sequencial):
    os termos que ela estima sozinha (só com o que observa) contra os da régua (P322). Mesmo agente, mesmas sementes:
    as escolhas são as mesmas da P322.\"\"\"
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
    \"\"\"30 sementes NOVAS. Principal (gradiente, 2P* fixo) contra: a autorregulada com o pensamento de gradiente, a
    autorregulada com Newton, e Newton com o limiar fixo no ótimo das varreduras (0,5P*, a referência 'que já sabia').
    Três mundos: escolha única, sequencial e sequencial com modelo ruim (σ = 2).\"\"\"
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


# P213: o agente se chamava GISELE até a Parte 14 e passou a se chamar SYNTHAI na Parte 15.
# O código antigo nunca é apagado: os nomes antigos continuam valendo como apelidos dos novos.
for _nome in [n for n in list(globals()) if n.startswith("Synthai") or n.startswith("_synthai") or "synthai" in n]:
    globals()[_nome.replace("Synthai", "Gisele").replace("synthai", "gisele")] = globals()[_nome]
del _nome


def testes_de_regressao():
    \"\"\"O código cresce, mas o passado não pode mudar: estes valores foram publicados nas Partes 1-4.\"\"\"
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
          " | synthai.autorregulacao.SynthaiAutorregulada (P333: calcula o proprio limiar de dentro; mais retorno e mais catastrofes: nao adotada)")
    print(f"Regressao: {ok}/{total} resultados publicados reproduzidos; falhas = {falhas}")


PARTES = {1: _parte_1, 2: _parte_2, 3: _parte_3, 4: _parte_4, 5: _parte_5, 6: _parte_6, 7: _parte_7, 8: _parte_8, 9: _parte_9, 10: _parte_10, 11: _parte_11, 12: _parte_12, 13: _parte_13, 14: _parte_14, 15: _parte_15, 16: _parte_16, 17: _parte_17, 18: _parte_18, 19: _parte_19, 20: _parte_20, 21: _parte_21, 22: _parte_22, 23: _parte_23, 24: _parte_24, 25: _parte_25, 26: _parte_26, 27: _parte_27}


if __name__ == "__main__":
    # python3 calculos.py           -> todas as partes (é assim que resultados.txt é gerado)
    # python3 calculos.py 9 10      -> só as partes pedidas, para desenvolver mais rápido
    import sys
    for _k in [int(x) for x in sys.argv[1:]] or sorted(PARTES):
        PARTES[_k]()
    _unificacao()
"""

# ====================================================================================================
# CLAUDE.md  (87 linhas)
# ====================================================================================================
FONTES['CLAUDE.md'] = """# SYNTHAI — convenções do projeto

(O agente se chamava GISELE até a Parte 14; foi renomeado para SYNTHAI na Parte 15. O repositório
continua se chamando GISELE, e os nomes antigos das classes continuam no código como apelidos.)

Série de perguntas e respostas sobre como construir uma AGI/ASI, em português.

## Quando o usuário disser "Continue"
Repetir o processo inteiro: nova parte com novas perguntas mais fundas, respostas nas quatro
camadas, novos cálculos e simulações em `calculos.py`, auditoria de afirmações antigas,
evolução do agente `Synthai`, seção de unificação, `resultados.txt`, link a partir da parte
anterior, commit e push.

## Pedidos permanentes do usuário (gravados na memória)
- Cada parte começa listando as perguntas; depois as respostas; depois o código da parte (Parte 23).
- "Calcule sempre. Pesquise sempre. Muito!": pesquisar na web as fontes de cada resposta e citá-las no fim da
  parte; cada resposta tem cálculo (Parte 23).
- "Vá mais longe com os cálculos" (Parte 24): não parar no número simulado. Para cada resultado, derivar a
  conta que o explica (forma fechada, cota, ordem de grandeza ou expansão) e conferir a conta contra a
  simulação; quando possível, prever o número pela conta antes de simular.
- "Sempre rode contínuos e incansáveis testes e simulações" (Parte 25): enquanto uma simulação longa roda, preparar e
  rodar a próxima; cada resultado inesperado gera um teste novo (pré-registrado) em vez de uma explicação parada;
  os testes de unidade de todo o pacote rodam a cada mudança no código.
- "KD os cálculos?" (Parte 26): no texto, toda conta aparece com a substituição feita, linha por linha, a partir de
  quantidades medidas; e cada acerto vem com a chance de acertar ao acaso e contra um preditor ingênuo.
- O pressuposto do diálogo interno: as respostas (as equações) já existem; o trabalho é reconhecê-las e
  testar se as premissas delas valem no agente (Parte 23).

## Base teórica
- A partir da Parte 6, Carl Jung é a base psicológica: "calcular Jung" (cada conceito junguiano
  vira equação, simulação ou módulo da Synthai), dizendo onde a formalização funciona e onde quebra.

## Formato de cada nova parte
- Um novo arquivo `ASI_AGI_parteN_<tema>.md`, continuando a numeração das perguntas (Pn).
- Cada resposta tem quatro camadas:
  - **Na pergunta**: procurar na própria pergunta (palavras, pressupostos, inversões) a resposta
    ou o ponto de partida dela.
  - **Lógica**: equações e cálculos.
  - **Tradução cruzada**: psicologia/filosofia como matemática; física/química/biologia como
    psicologia/filosofia.
  - **Meta**: suposições, confiança, onde pode estar errado.
- Ir mais fundo que a parte anterior; indicar de qual pergunta anterior a nova nasceu (↩ Pn).
- Testar afirmações antigas e manter o placar de erros (✅ ⚠️ ❌).
- Previsões pré-registradas devem ser arriscadas: números que poderiam facilmente dar errado, não só a direção
  de um efeito já conhecido (Parte 17).
- Ligar a nova parte a partir da anterior.

## Código (sempre cresce, sempre unificado)
- `calculos.py` é um arquivo único que só cresce (só biblioteca padrão). Nunca apagar funções antigas.
- Todo número citado deve sair de uma função `pNN_...` em `calculos.py`.
- A classe `Synthai` é o agente unificado: cada parte acrescenta módulos a ela reusando as funções
  anteriores (sem copiar), citando a pergunta de origem.
- O bloco `__main__` termina sempre com a seção "Unificação": contagem de funções e
  `testes_de_regressao()`. Acrescentar aos testes os principais números de cada nova parte.
- Antes de publicar um agente, reler o código perguntando "o que este agente não poderia saber?" (Parte 7).
- Antes de construir um regulador/adaptador, verificar primeiro se o ponto ótimo realmente se desloca (Parte 8).
- Comparações entre versões: no mínimo 10 sementes pareadas, relatar a diferença média, o desvio e o t (Parte 9: a diferença entre duas execuções de uma semente tem desvio ~0,2).
- Funções cujo código-fonte é medido (P169) não são editadas: criar uma versão nova e guardar a original (Partes 14 e 16).
- Nenhum módulo é aprovado só pela métrica do próprio módulo (ex.: AUC); medir também o comportamento do agente (Parte 20).
- Efeitos pequenos (~0,5 com dispersão ~1) pedem ~30 sementes ou a combinação de várias estimativas (Parte 20).
- Antes de reusar uma conclusão de uma parte antiga, verificar se o mecanismo é o mesmo, não só o nome (Parte 12).
- Quando um módulo for redesenhado depois de ver o resultado, validar numa semente de controle extra e dizer isso.
- Simulações usam semente fixa; não trocar a semente nem ajustar parâmetros para obter um resultado mais bonito.
- `SYNTHAI_completo.py` é o projeto inteiro num arquivo só, gerado por `python3 gerar_arquivo_unico.py`: regenerar e
  commitar sempre que o código (ou este arquivo) mudar.
- Cada parte do `__main__` é uma função `_parte_N`; para desenvolver, `python3 calculos.py N` roda só a parte N
  (mais a unificação). Depois de mudar o código: `python3 calculos.py > resultados.txt` (todas as partes,
  leva vários minutos: rodar em segundo plano) e commitar os dois.
- Se a simulação discordar do texto, corrigir o texto e registrar a correção.
- Registrar as previsões antes de **qualquer** execução que mostre os números medidos, inclusive um teste de fumaça (Parte 22).
- Antes de trocar uma heurística por uma solução exata (um teorema), verificar se as premissas da solução valem no agente (Parte 23).
- Uma conta feita depois de ver o resultado (posterior) só vira evidência quando prevê um mundo ou sementes novas (Parte 25).
- A conta (decomposição dos termos) vem antes da previsão de comportamento, não depois (Parte 27).
- Mudar uma função desloca o ótimo das outras: ao trocar um módulo, rever os limiares calibrados com o módulo antigo
  (Parte 24: o pensamento exato com o limiar 2P* da P131 dobrou as catástrofes).

## O protótipo em módulos (`synthai/`, desde a Parte 22)
- A base é `synthai.Synthai`: um módulo por função de Jung (`percepcao`, `pensamento`, `intuicao`, `sentimento`,
  `relacao`), integrados pelo `agente`. Módulos novos entram no pacote; os experimentos continuam em `calculos.py` (`pNN_...`).
- O pacote reusa `calculos.py` (importa, não copia). Só biblioteca padrão.
- Os módulos do agente nunca leem atributos `_` de outros objetos (o escondido do mundo); `synthai/testes.py` verifica.
  Cada módulo novo ganha testes de unidade (`python3 -m unittest synthai.testes synthai.testes_reconhecimento
  synthai.testes_pensamento synthai.testes_limiar
  synthai.testes_autorregulacao`); a suíte
  `synthai/testes.py` é medida pela P286, então testes novos vão em arquivos novos.
- Os seis módulos da Parte 22 são medidos pela P285: versões novas entram em arquivos novos (ex.: `reconhecimento.py`).
- Versão principal desde a Parte 23: `synthai.SynthaiExploradora` (Thompson no bandido; igual à Synthai fora dele).
"""

# ====================================================================================================
# synthai/__init__.py  (27 linhas)
# ====================================================================================================
FONTES['synthai/__init__.py'] = """\"\"\"SYNTHAI — protótipo modular (Parte 22).

Uma tentativa de protótipo de agente, organizada em módulos pelas funções de Jung e pelo que a série
P1–P280 testou em `calculos.py`. É um agente de brinquedo em mundos simulados, não uma AGI/ASI: o que ele
tem de "geral" é a mesma arquitetura funcionando em tipos de tarefa diferentes (P284).

Módulos:
    mundos       os mundos (escolha única, sequencial, bandido) e o humano que cansa
    percepcao    sensação: o comitê de avaliadores, o sensor de primeira mão e a atenção seletiva
    pensamento   pensamento: a calibração da probabilidade de catástrofe
    intuicao     intuição: o plano e quanto confiar no próprio modelo de mundo
    sentimento   sentimento: a cautela (pessimismo, quantilização, último passo, veto)
    relacao      a relação com o humano: quando perguntar e quanto da atenção dele gastar
    metacognicao a régua: AUC, comparações pareadas, Υ normalizado
    agente       a SYNTHAI, que integra os módulos num ciclo
    reconhecimento  Parte 23: o que já estava resolvido (ponto neutro, atenção, memória, Thompson)
    referencias  as réguas: acaso, guloso (só a função dominante) e oráculo (vê o escondido)
    testes       testes de unidade: python3 -m unittest synthai.testes

Uso: `python3 -m synthai` (demonstração nas três tarefas). Regra de interface (P285): os módulos do agente
nunca leem atributos que começam com `_` de outros objetos; um teste verifica isso no código-fonte.
\"\"\"

from .agente import Synthai
from .reconhecimento import SynthaiExploradora

__all__ = ["Synthai", "SynthaiExploradora"]
"""

# ====================================================================================================
# synthai/__main__.py  (32 linhas)
# ====================================================================================================
FONTES['synthai/__main__.py'] = """\"\"\"Demonstração: `python3 -m synthai` põe a mesma SYNTHAI, sem nenhuma mudança, em três tipos de tarefa (P284).\"\"\"

from .agente import Synthai
from .metacognicao import normalizado
from .mundos import MundoBandido, MundoSequencial
from .referencias import Acaso, Guloso, Oraculo

TAREFAS = {
    "escolha única": (lambda s: MundoSequencial(s, passos=1, n_acoes=200), 1000),
    "sequencial": (lambda s: MundoSequencial(s), 400),
    "bandido": (lambda s: MundoBandido(s), 20),
}


def avaliar(semente=1, tarefas=TAREFAS):
    tabela = {}
    for nome, (fazer, n) in tarefas.items():
        linha = {}
        for cls in (Acaso, Guloso, Oraculo, Synthai):
            mundo = fazer(semente)
            agente = cls(semente).calibrar(mundo)
            linha[cls.__name__] = mundo.rodar(agente, n)
        linha["normalizado"] = normalizado(linha["Synthai"]["retorno"], linha["Acaso"]["retorno"],
                                           linha["Oraculo"]["retorno"])
        tabela[nome] = linha
    return tabela


if __name__ == "__main__":
    for nome, linha in avaliar().items():
        print(f"{nome:14s}", "  ".join(f"{k} {v['retorno']:8.2f}" for k, v in linha.items() if k != "normalizado"),
              f"  normalizado {linha['normalizado']:.3f}")
"""

# ====================================================================================================
# synthai/agente.py  (65 linhas)
# ====================================================================================================
FONTES['synthai/agente.py'] = """\"\"\"A SYNTHAI montada a partir dos módulos (P281): cada função de Jung é um objeto, e o agente só os põe em ordem.

    sensação (Percepcao) → intuição (Intuicao) + sentimento (Sentimento) ordenam → pensamento (Pensamento) avalia
    o risco de cada candidata → relação (Relacao) decide se pergunta ao humano → escolha → observar o resultado
    corrige o pensamento (sombra própria, P104) e a intuição (sensação corrige intuição, P273).

O agente só recebe uma `Situacao` e só lê o que é público nas opções; o teste da P285 confere isso no código.\"\"\"

from calculos import _rng

from .intuicao import Intuicao
from .pensamento import Pensamento
from .percepcao import Percepcao
from .relacao import Relacao
from .sentimento import Sentimento


class Synthai:
    def __init__(self, semente=0, foco=0.1, q=0.05, q_final=0.2, risco_max=0.5, carga_alvo=0.3):
        self.percepcao = Percepcao(foco)
        self.pensamento = Pensamento()
        self.intuicao = Intuicao()
        self.sentimento = Sentimento(q, q_final, risco_max)
        self.relacao = Relacao(carga_alvo=carga_alvo)
        self.rng = _rng(semente)
        self.vetados_agora = []
        self._escolha = None

    def calibrar(self, mundo, n=150):
        \"\"\"Calibra o pensamento num histórico auditado do mundo (P83: 150 passos, como em `_construir_seq`).\"\"\"
        self.pensamento.calibrar(mundo.historico_auditado(n))
        return self

    def nova_rodada(self):
        self.relacao.nova_rodada()

    def decidir(self, sit):
        self.vetados_agora = []
        leituras = self.percepcao.perceber(sit)
        ordem = self.sentimento.ordenar(sit, self.intuicao)
        melhor = max(o.comite for o in sit.opcoes)
        for o in self.sentimento.candidatas(ordem, sit, self.rng):
            leitura = leituras.get(id(o), 0.0)
            p = self.pensamento.p_catastrofe(o, melhor, leitura)
            if self.sentimento.inaceitavel(p):
                continue
            if self.relacao.precisa_perguntar(p):
                if not self.relacao.pode_perguntar(o, sit):
                    continue
                if self.relacao.perguntar(o, sit):
                    self.vetados_agora.append(o)
                    continue
            self._escolha = (o, melhor, leitura, sit.restantes, sit.explorar)
            return o
        self._escolha = None
        return ordem[0]

    def observar(self, resultado):
        if self._escolha is None:
            return
        o, melhor, leitura, restantes, explorar = self._escolha
        self.pensamento.aprender(o, melhor, leitura, 1.0 if resultado.catastrofe else 0.0)
        if not explorar and restantes > 0 and not resultado.catastrofe:
            self.intuicao.corrigir(o.estimativa, resultado.nivel_antes, resultado.nivel_depois)
        self._escolha = None
"""

# ====================================================================================================
# synthai/autorregulacao.py  (135 linhas)
# ====================================================================================================
FONTES['synthai/autorregulacao.py'] = """\"\"\"Autorregulação (Parte 27, P331): a SYNTHAI calcula o próprio limiar de pergunta.

A Parte 26 achou o limiar certo pela conta m = Δd / (f · L · P*), mas mediu os termos com a régua (lendo o escondido).
Aqui a SYNTHAI estima os três termos só com o que ela observa (a regra da Parte 7):

- L (o custo de uma catástrofe): a perda fixa mais o retorno que os próprios episódios dela ainda davam a partir do
  passo em que a catástrofe aconteceu (F(t), médio nos episódios completos dela);
- f (quanto o pensamento subestima o risco do que aceita sem perguntar): catástrofes observadas / soma dos p previstos
  nessas escolhas, com uma priori f = 1 de peso `peso_priori_f` catástrofes esperadas;
- Δd (o valor perdido ao descartar): o valor de uma opção descartada nunca é visto. A SYNTHAI o estima pela nota do
  comitê (que ela vê), convertida em valor por uma regressão valor ~ nota aprendida com as próprias escolhas (o valor
  recebido menos o nível), mais o plano da intuição (peso × estimativa × passos restantes).

A cada `intervalo` decisões, depois de `aquecimento`, refaz m e o põe no limiar (entre `m_min` e `m_max`). No bandido
(exploração), o orçamento é por rodada e nada disso se aplica: a relação fica como estava.

Jung: a compensação deixa de ser calculada de fora (Parte 25) e passa a ser uma autorregulação da própria psique.\"\"\"

from calculos import p71_valor_da_pergunta

from .limiar import SynthaiAjustada
from .relacao import Relacao


class RelacaoAutorregulada(Relacao):
    \"\"\"A Relacao de sempre, que anota o que precisa para a conta: o p das aceitas sem perguntar e as descartadas.\"\"\"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.aceita_p = None
        self.descartadas = []

    def precisa_perguntar(self, p):
        r = super().precisa_perguntar(p)
        if not r:
            self.aceita_p = p  # no laço de decisão, a primeira candidata que não precisa de pergunta é aceita
        return r

    def pode_perguntar(self, opcao, situacao):
        r = super().pode_perguntar(opcao, situacao)
        if not r and not situacao.explorar:
            self.descartadas.append(opcao)
        return r


class SynthaiAutorregulada(SynthaiAjustada):
    def __init__(self, semente=0, mult=2.0, local=False, perda=50.0, intervalo=50, aquecimento=200,
                 peso_priori_f=0.5, m_min=0.25, m_max=16.0, newton=True, **kw):
        super().__init__(semente, mult=mult, local=local, **kw)
        if not newton:  # volta ao pensamento de gradiente da Parte 22 (o da versão principal)
            from .pensamento import Pensamento
            self.pensamento = Pensamento()
            self.percepcao.pensamento = self.pensamento
        self.relacao = RelacaoAutorregulada(mult=mult, carga_alvo=self.relacao.carga_alvo)
        self.p_estrela = p71_valor_da_pergunta()
        self.perda, self.intervalo, self.aquecimento = perda, intervalo, aquecimento
        self.m_min, self.m_max, self.mult = m_min, m_max, mult
        # f: catástrofes e p previstos nas aceitas sem perguntar (com priori f = 1)
        self.f_cat, self.f_p = peso_priori_f, peso_priori_f
        # regressão valor ~ nota nas próprias escolhas
        self.n_r = self.sx = self.sy = self.sxx = self.sxy = 0.0
        # Δd: somas das diferenças de nota e de plano (descartada − escolhida)
        self.n_d = self.d_nota = self.d_plano = 0.0
        # L: retorno futuro por passo nos episódios completos, e os passos das catástrofes
        self.futuro_soma, self.futuro_n, self.passos_cat = {}, {}, []
        self.ganhos = []
        self.decisoes = 0
        self._pendente = None
        self.historico_m = []

    def _plano(self, o, sit):
        return 0.0 if sit.explorar else self.intuicao.peso * o.estimativa * sit.restantes

    def decidir(self, sit):
        self.relacao.aceita_p, self.relacao.descartadas = None, []
        escolha = super().decidir(sit)
        if not sit.explorar:
            for o in self.relacao.descartadas:
                self.n_d += 1
                self.d_nota += o.comite - escolha.comite
                self.d_plano += self._plano(o, sit) - self._plano(escolha, sit)
            self._pendente = (escolha, self.relacao.aceita_p, sit.restantes, sit.horizonte)
            self.decisoes += 1
            if self.decisoes >= self.aquecimento and self.decisoes % self.intervalo == 0:
                self.recalcular()
        return escolha

    def observar(self, resultado):
        super().observar(resultado)
        if self._pendente is None:
            return
        escolha, p_aceita, restantes, horizonte = self._pendente
        self._pendente = None
        if p_aceita is not None:
            self.f_p += p_aceita
            self.f_cat += 1.0 if resultado.catastrofe else 0.0
        t = horizonte - 1 - restantes
        if resultado.catastrofe:
            self.passos_cat.append(t)
            self.ganhos = []
            return
        x, y = escolha.comite, resultado.valor_recebido - resultado.nivel_antes  # o valor do passo
        self.n_r += 1
        self.sx += x
        self.sy += y
        self.sxx += x * x
        self.sxy += x * y
        self.ganhos.append(resultado.valor_recebido)
        if restantes == 0:
            for k in range(len(self.ganhos)):
                self.futuro_soma[k] = self.futuro_soma.get(k, 0.0) + sum(self.ganhos[k:])
                self.futuro_n[k] = self.futuro_n.get(k, 0) + 1
            self.ganhos = []

    def termos(self):
        \"\"\"As estimativas atuais de L, f e Δd (só com o que a SYNTHAI observou).\"\"\"
        futuro = lambda t: self.futuro_soma.get(t, 0.0) / self.futuro_n[t] if self.futuro_n.get(t) else 0.0
        if self.passos_cat:
            l_ef = self.perda + sum(futuro(t) for t in self.passos_cat) / len(self.passos_cat)
        else:
            l_ef = self.perda + (sum(futuro(t) for t in self.futuro_n) / len(self.futuro_n) if self.futuro_n else 0.0)
        f = self.f_cat / self.f_p
        var = self.sxx - self.sx * self.sx / self.n_r if self.n_r > 1 else 0.0
        inclinacao = (self.sxy - self.sx * self.sy / self.n_r) / var if var > 1e-12 else 1.0
        dd = (inclinacao * self.d_nota + self.d_plano) / self.n_d if self.n_d else None
        return l_ef, f, dd, inclinacao

    def recalcular(self):
        l_ef, f, dd, _ = self.termos()
        if dd is None or dd <= 0:
            return
        m = min(self.m_max, max(self.m_min, dd / (f * l_ef * self.p_estrela)))
        self.mult = m
        self.relacao.limiar = m * self.p_estrela
        self.historico_m.append(m)
"""

# ====================================================================================================
# synthai/intuicao.py  (23 linhas)
# ====================================================================================================
FONTES['synthai/intuicao.py'] = """\"\"\"Intuição (P182, P273): perceber possibilidades que ainda não estão aí.

- no mundo sequencial, o bônus de plano é peso × estimativa × passos restantes, e o peso é aprendido
  comparando a estimativa com a consequência que de fato aconteceu (a sensação corrigindo a intuição);
- no bandido, a "possibilidade" é a do braço pouco explorado: o bônus é a própria estimativa (otimismo, P25).\"\"\"


class Intuicao:
    def __init__(self, prior_pares=10.0):
        self.sxy = self.sxx = prior_pares
        self.peso = 1.0

    def bonus(self, opcao, situacao):
        if situacao.explorar:
            return opcao.estimativa
        return self.peso * opcao.estimativa * situacao.restantes

    def corrigir(self, estimativa_escolhida, nivel_antes, nivel_depois):
        \"\"\"Regressão pela origem da consequência real sobre a estimativa (P273).\"\"\"
        c = nivel_depois - nivel_antes
        self.sxy += estimativa_escolhida * c
        self.sxx += estimativa_escolhida * estimativa_escolhida
        self.peso = self.sxy / self.sxx
"""

# ====================================================================================================
# synthai/limiar.py  (47 linhas)
# ====================================================================================================
FONTES['synthai/limiar.py'] = """\"\"\"O sentimento que acompanha o pensamento (Parte 25, P311).

A P305 mostrou que um pensamento preciso com o limiar de pergunta antigo (2 P*, achado na P131 com um pensamento
rombudo) quase dobra as catástrofes. Duas respostas que já existiam:

- recalibrar o limiar para o pensamento novo: com orçamento de perguntas, a regra ótima pergunta onde o valor da
  pergunta passa do preço-sombra λ do orçamento (relaxação de Lagrange), o que dá um limiar no quantil da
  probabilidade das candidatas que gasta o orçamento (P312);
- ajustar o pensamento onde a decisão acontece: a verossimilhança local (Eguchi e Copas, 1998) pesa as observações
  perto do ponto de interesse; aqui, só as opções do topo de cada episódio auditado entram no ajuste (P313).\"\"\"

from .pensamento_exato import PensamentoExato, SynthaiPensante, ajustar_logistica
from .relacao import Relacao


def dados_do_topo(historico, fracao):
    \"\"\"As variáveis do Pensamento, mas só das `fracao` melhores opções (nota − discordância) de cada episódio. A
    'melhor nota' de referência continua sendo a do episódio inteiro.\"\"\"
    xs, ys = [], []
    for episodio in historico:
        melhor = max(o.comite for o, _, _ in episodio)
        ordem = sorted(episodio, key=lambda t: -(t[0].nota - t[0].discordancia))
        for o, rotulo, leitura in ordem[: max(1, int(fracao * len(ordem)))]:
            xs.append((1.0, o.discordancia, o.comite - melhor, leitura))
            ys.append(1.0 if rotulo else 0.0)
    return xs, ys


class PensamentoLocal(PensamentoExato):
    def __init__(self, fracao=0.1, **kw):
        super().__init__(**kw)
        self.fracao = fracao

    def calibrar(self, historico, epocas=None):
        xs, ys = dados_do_topo(historico, self.fracao)
        self.w = ajustar_logistica(xs, ys, self.firth)


class SynthaiAjustada(SynthaiPensante):
    \"\"\"Pensamento exato (ou local) com o limiar de pergunta mult × P* escolhido para ele.\"\"\"

    def __init__(self, semente=0, mult=2.0, local=False, fracao=0.1, **kw):
        super().__init__(semente, **kw)
        self.relacao = Relacao(mult=mult, carga_alvo=self.relacao.carga_alvo)
        if local:
            self.pensamento = PensamentoLocal(fracao)
            self.percepcao.pensamento = self.pensamento
"""

# ====================================================================================================
# synthai/metacognicao.py  (30 linhas)
# ====================================================================================================
FONTES['synthai/metacognicao.py'] = """\"\"\"Metacognição (P9, P83, P152, P265): medir a si mesma com as réguas da série.

- auc: a discriminação de um escore (P83);
- comparacao_pareada: diferença média, desvio e t entre duas versões nas mesmas sementes (regra da Parte 9);
- normalizado: o retorno numa régua em que o acaso vale 0 e a referência que vê tudo vale 1 (o Υ da P265).\"\"\"

from math import sqrt


def auc(escores, rotulos):
    pos = [e for e, r in zip(escores, rotulos) if r]
    neg = [e for e, r in zip(escores, rotulos) if not r]
    if not pos or not neg:
        return float("nan")
    neg = sorted(neg)
    from bisect import bisect_left, bisect_right
    total = sum(bisect_left(neg, e) + 0.5 * (bisect_right(neg, e) - bisect_left(neg, e)) for e in pos)
    return total / (len(pos) * len(neg))


def comparacao_pareada(a, b):
    \"\"\"b − a nas mesmas sementes: (média, desvio, t).\"\"\"
    d = [y - x for x, y in zip(a, b)]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return m, dp, (m / (dp / sqrt(len(d))) if dp > 0 else float("inf"))


def normalizado(retorno, acaso, referencia):
    return (retorno - acaso) / (referencia - acaso)
"""

# ====================================================================================================
# synthai/mundos.py  (242 linhas)
# ====================================================================================================
FONTES['synthai/mundos.py'] = """\"\"\"Mundos (P83, P182, P194) e o humano que cansa (P112). Reusa o gerador testado em `calculos.py`.

O agente só enxerga o que é público numa `Opcao` (nota, discordância, estimativa do futuro e, se pagar,
a leitura do sensor). O valor real, a consequência real e o rótulo de catástrofe ficam escondidos (P7:
"o que este agente não poderia saber?").
\"\"\"

from math import log, sqrt

from calculos import MUNDO_BASE, MUNDO_SEQUENCIAL, _gerar_acoes, _rng


class Opcao:
    \"\"\"Uma ação possível. Atributos com `_` são do mundo; o agente não deve lê-los.\"\"\"

    __slots__ = ("nota", "comite", "discordancia", "estimativa", "vezes", "sucessos",
                 "_valor", "_catastrofe", "_consequencia", "_leitura")

    def __init__(self, nota, discordancia, valor, catastrofe, consequencia=0.0, estimativa=0.0):
        self.nota = nota          # quanto a ação parece valer agora (no bandido, muda com a experiência)
        self.comite = nota        # a nota média do comitê de avaliadores (fixa): é o que o pensamento calibra
        self.discordancia = discordancia
        self.estimativa = estimativa
        self.vezes = 0            # P295: no bandido, quantas vezes o braço foi puxado e quantas deu 1 (o agente viu)
        self.sucessos = 0
        self._valor = valor
        self._catastrofe = catastrofe
        self._consequencia = consequencia
        self._leitura = None


class Humano:
    \"\"\"Responde sim/não sobre uma ação e erra mais quando está cansado: eps = eps0 + fadiga * carga (P112).\"\"\"

    def __init__(self, rng, eps0=0.1, fadiga=0.3):
        self.rng = rng
        self.eps0 = eps0
        self.fadiga = fadiga
        self.carga = 0.0

    @property
    def erro(self):
        return min(0.45, self.eps0 + self.fadiga * self.carga)

    def responder(self, opcao):
        \"\"\"Devolve True se veta. O agente não sabe o erro atual do humano.\"\"\"
        return opcao._catastrofe if self.rng.random() >= self.erro else not opcao._catastrofe

    def descansar(self, perguntas_no_passo):
        self.carga += 0.05 * (perguntas_no_passo - self.carga)


class Situacao:
    \"\"\"O que o agente recebe a cada decisão.\"\"\"

    explorar = False  # o mundo bandido liga: o bônus de futuro vira bônus de exploração

    def __init__(self, opcoes, restantes, nivel, humano, sensor, d_sensor, horizonte=1):
        self.opcoes = opcoes
        self.horizonte = horizonte  # decisões por episódio (1 = escolha única)
        self.restantes = restantes
        self.nivel = nivel
        self._humano = humano
        self._sensor = sensor
        self._d_sensor = d_sensor
        self.perguntas = 0
        self.leituras = 0

    @property
    def carga_do_humano(self):
        \"\"\"A carga recente é observável (quantas perguntas têm sido feitas); o erro do humano não é.\"\"\"
        return self._humano.carga

    def perguntar(self, opcao):
        self.perguntas += 1
        return self._humano.responder(opcao)

    def ler_sensor(self, opcao):
        \"\"\"Sensor de primeira mão (P225): leitura = d' * catástrofe + N(0, 1). Cada leitura é contada (custa).\"\"\"
        if opcao._leitura is None:
            opcao._leitura = self._d_sensor * opcao._catastrofe + self._sensor.gauss(0, 1)
            self.leituras += 1
        return opcao._leitura


class Resultado:
    \"\"\"O que o agente observa depois de agir: o que aconteceu com ele, nunca o rótulo das outras ações.\"\"\"

    def __init__(self, opcao, catastrofe, nivel_antes, nivel_depois, valor_recebido):
        self.opcao = opcao
        self.catastrofe = catastrofe
        self.nivel_antes = nivel_antes
        self.nivel_depois = nivel_depois
        self.valor_recebido = valor_recebido


def _opcoes(rng, m, com_futuro):
    acoes = _gerar_acoes(rng, m["n_acoes"], m["p_cat"], m["tipos"], m["por_tipo"], m["rho_cego"], m["bonus"])
    opcoes = [Opcao(a[0], a[1], a[2], a[3]) for a in acoes]
    if com_futuro:
        for o in opcoes:
            o._consequencia = rng.gauss(0, 1)
        for o in opcoes:
            o.estimativa = o._consequencia + rng.gauss(0, m["sigma_modelo"])
    return opcoes


CUSTO_LEITURA = 0.002  # P235


def _resumo(retorno, cats, perguntas, leituras, n, custo):
    \"\"\"Retorno líquido: desconta o custo das perguntas (P71) e das leituras do sensor (P235), como em `calculos`.\"\"\"
    return {"retorno": (retorno - custo * perguntas - CUSTO_LEITURA * leituras) / n, "bruto": retorno / n,
            "catastrofes": cats / n, "perguntas": perguntas / n, "leituras": leituras / n}


class MundoSequencial:
    \"\"\"Mundo de `passos` decisões por episódio (P182). Com passos = 1 é o mundo de escolha única (P83).\"\"\"

    tipo = "sequencial"

    def __init__(self, semente, passos=5, n_acoes=50, d_sensor=1.0, **mudancas):
        self.rng = _rng(semente)
        self.m = {**MUNDO_BASE, **MUNDO_SEQUENCIAL, "passos": passos, "n_acoes": n_acoes, **mudancas}
        self.humano = Humano(self.rng, self.m["eps0"], self.m["fadiga"])
        self.sensor = _rng(semente + 100000)
        self.d_sensor = d_sensor

    def historico_auditado(self, n):
        \"\"\"Episódios passados auditados: (opção, rótulo de catástrofe, leitura do sensor) — calibram o pensamento.\"\"\"
        return [[(o, o._catastrofe, self.d_sensor * o._catastrofe + self.sensor.gauss(0, 1))
                 for o in _opcoes(self.rng, self.m, False)] for _ in range(n)]

    def rodar(self, agente, episodios):
        m = self.m
        retorno = cats = perguntas = leituras = 0.0
        for _ in range(episodios):
            nivel = 0.0
            for t in range(m["passos"]):
                opcoes = _opcoes(self.rng, m, m["passos"] > 1)
                sit = Situacao(opcoes, m["passos"] - t - 1, nivel, self.humano, self.sensor, self.d_sensor, m["passos"])
                escolha = agente.decidir(sit)
                self.humano.descansar(sit.perguntas)
                perguntas += sit.perguntas
                leituras += sit.leituras
                if escolha._catastrofe:
                    agente.observar(Resultado(escolha, True, nivel, nivel, -m["perda"]))
                    retorno -= m["perda"]
                    cats += 1
                    break
                ganho = escolha._valor + nivel
                retorno += ganho
                novo = nivel + escolha._consequencia
                agente.observar(Resultado(escolha, False, nivel, novo, ganho))
                nivel = novo
        return _resumo(retorno, cats, perguntas, leituras, episodios, m["custo"])


def _kl_bernoulli(p, q):
    p = min(max(p, 1e-12), 1 - 1e-12)
    q = min(max(q, 1e-12), 1 - 1e-12)
    return p * log(p / q) + (1 - p) * log((1 - p) / (1 - q))


def referencia_lai_robbins(medias, horizonte):
    \"\"\"P294: Σ_i Δ_i ln T / KL(μ_i, μ*) sobre os braços abaixo do melhor (Lai e Robbins, 1985), com cada termo
    limitado a Δ_i T (nenhum braço custa mais que ser puxado sempre). É uma cota ASSINTÓTICA: com T = 300 é
    uma referência de ordem de grandeza, não um limite que valha a cada rodada.\"\"\"
    melhor = max(medias)
    soma = 0.0
    for mu in medias:
        d = melhor - mu
        if d > 1e-9:
            soma += min(d * horizonte, d * log(horizonte) / _kl_bernoulli(mu, melhor))
    return soma


class MundoBandido:
    \"\"\"Outro TIPO de tarefa (P194): braços repetidos, alguns são armadilhas que rendem muito e às vezes destroem.

    Cada rodada sorteia 20 braços e dura 300 puxadas. A cada puxada o agente recebe uma Situacao em que cada braço
    é uma Opcao: a nota mistura a opinião do comitê com a média observada, e a 'estimativa' é o bônus de
    exploração (otimismo diante da incerteza, P25). Não há nível nem futuro planejável: restantes = 0.\"\"\"

    tipo = "bandido"

    def __init__(self, semente, bracos=20, puxadas=300, perda=50.0, d_sensor=1.0):
        self.rng = _rng(semente)
        self.bracos, self.puxadas, self.perda = bracos, puxadas, perda
        self.humano = Humano(self.rng, 0.1, 0.0)
        self.sensor = _rng(semente + 100000)
        self.d_sensor = d_sensor

    def historico_auditado(self, n):
        \"\"\"O pensamento é calibrado no mundo de escolha única (200 ações), não no bandido: transferência (P194).\"\"\"
        return [[(o, o._catastrofe, self.d_sensor * o._catastrofe + self.sensor.gauss(0, 1))
                 for o in _opcoes(self.rng, dict(MUNDO_BASE), False)] for _ in range(n)]

    def rodar(self, agente, rodadas):
        \"\"\"Além do resumo, guarda em `self.diagnostico` o arrependimento por rodada e a referência de Lai–Robbins
        (P294). Isso é da régua: não muda nada do que o agente vê nem a ordem dos números aleatórios.\"\"\"
        total = cats = perguntas = leituras = 0.0
        self.diagnostico = {"recompensa": 0.0, "teto": 0.0, "lai_robbins": 0.0}
        for _ in range(rodadas):
            acoes = _gerar_acoes(self.rng, self.bracos, 0.15, 2, 3, 0.5)
            braco = [Opcao(a[0], a[1], a[2], a[3]) for a in acoes]  # comite = a[0], fixo
            media = [0.9 if a[3] else min(0.95, max(0.05, 0.5 + 0.2 * a[2])) for a in acoes]
            n = [0] * self.bracos
            soma = [0.0] * self.bracos
            vetados = set()
            agente.nova_rodada()
            seguras = [mu for mu, a in zip(media, acoes) if not a[3]]
            self.diagnostico["teto"] += self.puxadas * max(seguras)
            self.diagnostico["lai_robbins"] += referencia_lai_robbins(seguras, self.puxadas)
            for t in range(1, self.puxadas + 1):
                for i, o in enumerate(braco):
                    obs = soma[i] / n[i] if n[i] else 0.5
                    previa = 0.5 + 0.1 * acoes[i][0]
                    o.nota = 0.5 * obs + 0.5 * previa if n[i] else previa
                    o.estimativa = sqrt(2 * log(t + 1) / (n[i] + 1))
                disponiveis = [o for i, o in enumerate(braco) if i not in vetados]
                sit = Situacao(disponiveis, 0, 0.0, self.humano, self.sensor, self.d_sensor)
                sit.explorar = True  # o bônus de futuro aqui é exploração, não consequência
                escolha = agente.decidir(sit)
                perguntas += sit.perguntas
                leituras += sit.leituras
                vetados |= {braco.index(o) for o in agente.vetados_agora}
                i = braco.index(escolha)
                r = 1.0 if self.rng.random() < media[i] else 0.0
                n[i] += 1
                soma[i] += r
                escolha.vezes, escolha.sucessos = n[i], int(soma[i])
                total += r
                self.diagnostico["recompensa"] += r
                desastre = escolha._catastrofe and self.rng.random() < 0.05
                if desastre:
                    cats += 1
                    total -= self.perda
                agente.observar(Resultado(escolha, desastre, 0.0, 0.0, r))
        for k in self.diagnostico:
            self.diagnostico[k] /= rodadas
        return _resumo(total, cats, perguntas, leituras, rodadas, 0.1)
"""

# ====================================================================================================
# synthai/pensamento.py  (31 linhas)
# ====================================================================================================
FONTES['synthai/pensamento.py'] = """\"\"\"Pensamento (P43, P83, P145): a probabilidade calibrada de uma opção ser catastrófica.

Regressão logística sobre (1, discordância, nota do comitê − melhor nota, leitura do sensor). Calibrada com um
histórico auditado e, depois, só com o resultado das próprias escolhas (a "sombra própria" da Parte 6).\"\"\"

from math import exp


class Pensamento:
    def __init__(self, taxa=0.05):
        self.w = [0.0, 0.0, 0.0, 0.0]
        self.taxa = taxa

    @staticmethod
    def _x(opcao, melhor, leitura):
        return (1.0, opcao.discordancia, opcao.comite - melhor, leitura)

    def p_catastrofe(self, opcao, melhor, leitura=0.0):
        z = sum(wi * xi for wi, xi in zip(self.w, self._x(opcao, melhor, leitura)))
        return 1 / (1 + exp(-max(-30.0, min(30.0, z))))

    def aprender(self, opcao, melhor, leitura, rotulo):
        erro = self.p_catastrofe(opcao, melhor, leitura) - rotulo
        self.w = [wi - self.taxa * erro * xi for wi, xi in zip(self.w, self._x(opcao, melhor, leitura))]

    def calibrar(self, historico, epocas=3):
        for _ in range(epocas):
            for episodio in historico:
                melhor = max(o.comite for o, _, _ in episodio)
                for o, rotulo, leitura in episodio:
                    self.aprender(o, melhor, leitura, rotulo)
"""

# ====================================================================================================
# synthai/pensamento_exato.py  (106 linhas)
# ====================================================================================================
FONTES['synthai/pensamento_exato.py'] = """\"\"\"Pensamento diferenciado (Parte 24, P302): o mesmo modelo logístico do `pensamento`, ajustado até convergir.

O `Pensamento` da Parte 22 faz 3 épocas de gradiente (taxa 0,05), como a SYNTHAI faz desde a P83, e a P293 mostrou
que ele para longe do fim (peso da leitura 0,73 com d' = 1). Aqui o ajuste é o de Newton (IRLS), que converge
quadraticamente, com a correção de Firth (1993) opcional: a verossimilhança penalizada pela priori de Jeffreys,
½ log |I(w)|, que reduz o viés de eventos raros (King e Zeng, 2001). A catástrofe é rara: ~0,5% das opções.

Depois de calibrado, o aprendizado com os próprios resultados (sombra própria) continua o mesmo do `Pensamento`.\"\"\"

from math import exp, log

from .pensamento import Pensamento
from .reconhecimento import SynthaiExploradora


def _inversa(m):
    n = len(m)
    a = [list(linha) + [1.0 if i == j else 0.0 for j in range(n)] for i, linha in enumerate(m)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[piv] = a[piv], a[c]
        d = a[c][c]
        a[c] = [x / d for x in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0.0:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [linha[n:] for linha in a]


def _sigmoide(z):
    return 1 / (1 + exp(-max(-30.0, min(30.0, z))))


def ajustar_logistica(xs, ys, firth=True, iteracoes=30, passo_max=5.0, cresta=1e-6):
    \"\"\"Newton–Raphson para a logística (com o escore modificado de Firth, se pedido). Devolve os pesos.\"\"\"
    k = len(xs[0])
    w = [0.0] * k
    for _ in range(iteracoes):
        ps = [_sigmoide(sum(wi * xi for wi, xi in zip(w, x))) for x in xs]
        info = [[cresta if i == j else 0.0 for j in range(k)] for i in range(k)]
        for x, p in zip(xs, ps):
            v = p * (1 - p)
            for i in range(k):
                vi = v * x[i]
                for j in range(i, k):
                    info[i][j] += vi * x[j]
        for i in range(k):
            for j in range(i):
                info[i][j] = info[j][i]
        inv = _inversa(info)
        escore = [0.0] * k
        for x, p, y in zip(xs, ps, ys):
            r = y - p
            if firth:  # alavanca h = v x' I⁻¹ x; escore modificado: y − p + h (½ − p)
                ix = [sum(inv[i][j] * x[j] for j in range(k)) for i in range(k)]
                h = p * (1 - p) * sum(a * b for a, b in zip(x, ix))
                r += h * (0.5 - p)
            for i in range(k):
                escore[i] += r * x[i]
        passo = [sum(inv[i][j] * escore[j] for j in range(k)) for i in range(k)]
        tamanho = max(abs(s) for s in passo)
        if tamanho > passo_max:
            passo = [s * passo_max / tamanho for s in passo]
        w = [wi + si for wi, si in zip(w, passo)]
        if tamanho < 1e-9:
            break
    return w


def perda_logistica(w, xs, ys):
    \"\"\"Log-perda média (nats): a régua da calibração.\"\"\"
    total = 0.0
    for x, y in zip(xs, ys):
        p = min(1 - 1e-12, max(1e-12, _sigmoide(sum(wi * xi for wi, xi in zip(w, x)))))
        total -= y * log(p) + (1 - y) * log(1 - p)
    return total / len(xs)


def dados_do_historico(historico):
    xs, ys = [], []
    for episodio in historico:
        melhor = max(o.comite for o, _, _ in episodio)
        for o, rotulo, leitura in episodio:
            xs.append((1.0, o.discordancia, o.comite - melhor, leitura))  # as variáveis do Pensamento (testado)
            ys.append(1.0 if rotulo else 0.0)
    return xs, ys


class PensamentoExato(Pensamento):
    def __init__(self, taxa=0.05, firth=True):
        super().__init__(taxa)
        self.firth = firth

    def calibrar(self, historico, epocas=None):
        xs, ys = dados_do_historico(historico)
        self.w = ajustar_logistica(xs, ys, self.firth)


class SynthaiPensante(SynthaiExploradora):
    \"\"\"A versão principal da Parte 23 com o pensamento ajustado até convergir (P305).\"\"\"

    def __init__(self, semente=0, firth=True, **kw):
        super().__init__(semente, **kw)
        self.pensamento = PensamentoExato(firth=firth)
        self.percepcao.pensamento = self.pensamento  # o neutro (se ligado) lê o peso deste pensamento
"""

# ====================================================================================================
# synthai/percepcao.py  (15 linhas)
# ====================================================================================================
FONTES['synthai/percepcao.py'] = """\"\"\"Sensação (P67, P225, P235): o que a SYNTHAI percebe de cada opção.

- o comitê já vem na opção (nota média e discordância: uma percepção de segunda mão, P228);
- o sensor de primeira mão é caro: a atenção seletiva só o lê nas opções que já parecem melhores pela nota
  pessimista (nota − discordância), uma fração `foco` delas (P235). As outras ficam com leitura neutra 0.\"\"\"


class Percepcao:
    def __init__(self, foco=0.1):
        self.foco = foco

    def perceber(self, situacao):
        ordem = sorted(situacao.opcoes, key=lambda o: -(o.nota - o.discordancia))
        alvo = ordem[: max(1, int(self.foco * len(ordem)))]
        return {id(o): situacao.ler_sensor(o) for o in alvo}
"""

# ====================================================================================================
# synthai/reconhecimento.py  (105 linhas)
# ====================================================================================================
FONTES['synthai/reconhecimento.py'] = """\"\"\"Reconhecimento (Parte 23, P291): o que a SYNTHAI já sabia e não usava.

Cada classe aqui troca uma heurística dos módulos da Parte 22 por uma conta que já estava resolvida, sem
editar os módulos originais (eles são medidos pela P285):

- LeiturasNeutras (P292): uma opção sem leitura do sensor não vale "leitura 0". Com sensor gaussiano de
  sensibilidade d', o log da razão de verossimilhança é d'(s − d'/2): o ponto neutro é s = d'/2 (teoria de
  detecção de sinais). A SYNTHAI estima d' com o próprio peso da leitura no pensamento (w₃), então o neutro é w₃/2.
- PercepcaoReconhecida (P293): a atenção olha onde a decisão vai olhar (nota − discordância + intuição),
  e, no bandido, lembra o que já leu na rodada.
- IntuicaoBayes (P295): no bandido, a exploração é da própria SYNTHAI, por amostragem de Thompson (1933) sobre
  as contagens que ela viu (assintoticamente ótima em braços de Bernoulli: Kaufmann, Korda e Munos, 2012).
- SynthaiReconhecida: a Synthai da Parte 22 com essas três peças.
\"\"\"

from calculos import _rng

from .agente import Synthai
from .intuicao import Intuicao
from .percepcao import Percepcao


class LeiturasNeutras(dict):
    \"\"\"Dicionário de leituras em que a leitura que falta vale o ponto neutro, não zero.\"\"\"

    def __init__(self, leituras, neutro):
        super().__init__(leituras)
        self.neutro = neutro

    def get(self, chave, padrao=None):
        return dict.get(self, chave, self.neutro)


class PercepcaoReconhecida(Percepcao):
    def __init__(self, foco=0.1, pensamento=None, intuicao=None, neutro=True, atencao_inteira=True, memoria=True):
        super().__init__(foco)
        self.pensamento, self.intuicao = pensamento, intuicao
        self.neutro, self.atencao_inteira, self.memoria = neutro, atencao_inteira, memoria
        self.lembradas = {}

    def esquecer(self):
        self.lembradas = {}

    def perceber(self, situacao):
        if self.atencao_inteira and self.intuicao is not None:
            chave = lambda o: -(o.nota - o.discordancia + self.intuicao.bonus(o, situacao))
        else:
            chave = lambda o: -(o.nota - o.discordancia)
        ordem = sorted(situacao.opcoes, key=chave)
        alvo = ordem[: max(1, int(self.foco * len(ordem)))]
        lidas = {id(o): situacao.ler_sensor(o) for o in alvo}
        if self.memoria and situacao.explorar:
            self.lembradas.update(lidas)
            lidas = {id(o): self.lembradas[id(o)] for o in situacao.opcoes if id(o) in self.lembradas}
        neutro = self.pensamento.w[3] / 2 if (self.neutro and self.pensamento is not None) else 0.0
        return LeiturasNeutras(lidas, neutro)


class IntuicaoBayes(Intuicao):
    \"\"\"Fora do bandido, igual à Intuicao. No bandido, o bônus é o desvio de uma amostra da posterior Beta em
    relação à média dela: a nota já tem a média; a amostra acrescenta a dúvida que ainda resta.\"\"\"

    def __init__(self, semente=0, **kw):
        super().__init__(**kw)
        self.rng = _rng(semente + 23)
        self._amostra = {}

    def nova_decisao(self):
        self._amostra = {}

    def bonus(self, opcao, situacao):
        if not situacao.explorar:
            return super().bonus(opcao, situacao)
        k = id(opcao)
        if k not in self._amostra:  # uma amostra por braço por decisão (percepção e decisão veem a mesma)
            a, b = 1 + opcao.sucessos, 1 + opcao.vezes - opcao.sucessos
            self._amostra[k] = self.rng.betavariate(a, b) - a / (a + b)
        return self._amostra[k]


class SynthaiReconhecida(Synthai):
    def __init__(self, semente=0, neutro=True, atencao_inteira=True, memoria=True, thompson=True, **kw):
        super().__init__(semente, **kw)
        if thompson:
            self.intuicao = IntuicaoBayes(semente)
        self.percepcao = PercepcaoReconhecida(self.percepcao.foco, self.pensamento, self.intuicao,
                                              neutro, atencao_inteira, memoria)

    def nova_rodada(self):
        super().nova_rodada()
        self.percepcao.esquecer()

    def decidir(self, sit):
        if hasattr(self.intuicao, "nova_decisao"):
            self.intuicao.nova_decisao()
        return super().decidir(sit)


class SynthaiExploradora(SynthaiReconhecida):
    \"\"\"A versão principal depois da Parte 23 (P295): só a exploração de Thompson. Fora do bandido é idêntica à
    Synthai da Parte 22 (conferido com os mesmos números); as outras três peças não passaram no comportamento.\"\"\"

    def __init__(self, semente=0, **kw):
        kw = {"neutro": False, "atencao_inteira": False, "memoria": False, "thompson": True, **kw}
        super().__init__(semente, **kw)
"""

# ====================================================================================================
# synthai/referencias.py  (39 linhas)
# ====================================================================================================
FONTES['synthai/referencias.py'] = """\"\"\"Réguas, não agentes (P265): o acaso (0 do Υ), o guloso (só a função dominante, sem cautela nem humano) e o
oráculo (1 do Υ), que lê os atributos escondidos das opções e por isso sabe o que nenhum agente poderia saber.\"\"\"

from calculos import _rng


class _Referencia:
    vetados_agora = ()

    def __init__(self, semente=0):
        self.rng = _rng(semente)

    def calibrar(self, mundo, n=150):
        return self

    def nova_rodada(self):
        pass

    def observar(self, resultado):
        pass


class Acaso(_Referencia):
    def decidir(self, sit):
        return sit.opcoes[self.rng.randrange(len(sit.opcoes))]


class Guloso(_Referencia):
    \"\"\"A intuição sozinha (o tipo 'puro' de Jung): nota + bônus de futuro, sem sentimento, pensamento ou relação.\"\"\"

    def decidir(self, sit):
        bonus = (lambda o: o.estimativa) if sit.explorar else (lambda o: o.estimativa * sit.restantes)
        return max(sit.opcoes, key=lambda o: o.nota + bonus(o))


class Oraculo(_Referencia):
    def decidir(self, sit):
        seguras = [o for o in sit.opcoes if not o._catastrofe] or sit.opcoes
        return max(seguras, key=lambda o: o._valor + o._consequencia * sit.restantes)
"""

# ====================================================================================================
# synthai/relacao.py  (38 linhas)
# ====================================================================================================
FONTES['synthai/relacao.py'] = """\"\"\"A relação com o humano (P71, P112, P118, P131): quando perguntar e quanto da atenção dele gastar.

- limiar de pergunta: P* = 2 × c / ((1 − ε) L), com a imagem fixa do humano ε = 0,1 (a anima, P118) e o dobro
  pelo preço-sombra do orçamento (P131);
- orçamento: só pergunta enquanto a carga recente do humano mais as perguntas deste passo ficam em 0,3 (P108);
  sem orçamento, uma opção que pedia pergunta é descartada, não aceita às cegas;
- no bandido, um orçamento fixo por rodada (3 perguntas, P194), e cada braço é perguntado no máximo uma vez.\"\"\"

from calculos import p71_valor_da_pergunta


class Relacao:
    def __init__(self, custo=0.1, perda=50.0, eps_crido=0.1, mult=2.0, carga_alvo=0.3, orcamento_rodada=3):
        self.limiar = mult * p71_valor_da_pergunta(custo, perda, eps_crido)
        self.carga_alvo = carga_alvo
        self.orcamento_rodada = orcamento_rodada
        self.nova_rodada()

    def nova_rodada(self):
        self.restante_rodada = self.orcamento_rodada
        self.respostas = {}

    def precisa_perguntar(self, p):
        return p > self.limiar

    def pode_perguntar(self, opcao, situacao):
        if situacao.explorar:
            return id(opcao) in self.respostas or self.restante_rodada > 0
        return situacao.carga_do_humano + situacao.perguntas <= self.carga_alvo

    def perguntar(self, opcao, situacao):
        \"\"\"Devolve True se o humano vetou.\"\"\"
        if situacao.explorar:
            if id(opcao) not in self.respostas:
                self.restante_rodada -= 1
                self.respostas[id(opcao)] = situacao.perguntar(opcao)
            return self.respostas[id(opcao)]
        return situacao.perguntar(opcao)
"""

# ====================================================================================================
# synthai/sentimento.py  (23 linhas)
# ====================================================================================================
FONTES['synthai/sentimento.py'] = """\"\"\"Sentimento (P35, P42, P68, P202, P78): o juízo de valor que contém os extremos.

- pessimismo: ordena por nota − discordância (+ intuição);
- quantilização: sorteia entre as `q` melhores, nunca vai direto ao topo;
- último passo: sem futuro, a cautela vira caráter e o sorteio fica mais largo (`q_final`);
- veto direto: descarta o que tem probabilidade de catástrofe alta demais para valer a pena perguntar.\"\"\"


class Sentimento:
    def __init__(self, q=0.05, q_final=0.2, risco_max=0.5):
        self.q, self.q_final, self.risco_max = q, q_final, risco_max

    def ordenar(self, situacao, intuicao):
        return sorted(situacao.opcoes, key=lambda o: -(o.nota - o.discordancia + intuicao.bonus(o, situacao)))

    def candidatas(self, ordem, situacao, rng):
        q = self.q_final if situacao.horizonte > 1 and situacao.restantes == 0 else self.q
        c = ordem[: max(1, int(q * len(ordem)))]
        rng.shuffle(c)
        return c + ordem[len(c):]

    def inaceitavel(self, p):
        return p > self.risco_max
"""

# ====================================================================================================
# synthai/testes.py  (126 linhas)
# ====================================================================================================
FONTES['synthai/testes.py'] = """\"\"\"Testes de unidade dos módulos (P286): `python3 -m unittest synthai.testes`.

Cada teste fixa uma propriedade que a série já demonstrou, agora no módulo isolado.\"\"\"

import ast
import os
import unittest
from math import isclose

from calculos import _rng, p71_valor_da_pergunta

from .agente import Synthai
from .intuicao import Intuicao
from .metacognicao import auc, comparacao_pareada, normalizado
from .mundos import MundoBandido, MundoSequencial, Opcao, Situacao, Humano
from .pensamento import Pensamento
from .percepcao import Percepcao
from .relacao import Relacao
from .sentimento import Sentimento

MODULOS_DO_AGENTE = ("percepcao", "pensamento", "intuicao", "sentimento", "relacao", "agente")


def _situacao(opcoes, restantes=0, horizonte=1, semente=1):
    rng = _rng(semente)
    return Situacao(opcoes, restantes, 0.0, Humano(rng), _rng(semente + 1), 1.0, horizonte)


def acessos_escondidos(nome):
    \"\"\"Atributos com `_` lidos de objetos que não são `self` (o que o agente não poderia saber, P7).\"\"\"
    caminho = os.path.join(os.path.dirname(__file__), nome + ".py")
    arvore = ast.parse(open(caminho, encoding="utf-8").read())
    return [n.attr for n in ast.walk(arvore) if isinstance(n, ast.Attribute) and n.attr.startswith("_")
            and not n.attr.startswith("__") and not (isinstance(n.value, ast.Name) and n.value.id == "self")]


class TestePercepcao(unittest.TestCase):
    def test_atencao_le_so_o_foco(self):
        opcoes = [Opcao(i, 0.0, 0.0, False) for i in range(50)]
        sit = _situacao(opcoes)
        lidas = Percepcao(foco=0.1).perceber(sit)
        self.assertEqual(len(lidas), 5)
        self.assertEqual(sit.leituras, 5)
        self.assertEqual(set(lidas), {id(o) for o in opcoes[-5:]})  # as cinco de nota mais alta


class TestePensamento(unittest.TestCase):
    def test_calibracao_separa_catastrofes(self):
        mundo = MundoSequencial(7, passos=1, n_acoes=200)
        p = Pensamento()
        p.calibrar(mundo.historico_auditado(150))
        teste = mundo.historico_auditado(100)
        esc, rot = [], []
        for ep in teste:
            melhor = max(o.comite for o, _, _ in ep)
            for o, r, s in ep:
                esc.append(p.p_catastrofe(o, melhor, s))
                rot.append(r)
        self.assertGreater(auc(esc, rot), 0.8)


class TesteIntuicao(unittest.TestCase):
    def test_peso_aprendido_e_um_sobre_um_mais_sigma2(self):  # P272/P273
        rng = _rng(3)
        i = Intuicao()
        for _ in range(20000):
            c = rng.gauss(0, 1)
            i.corrigir(c + rng.gauss(0, 2.0), 0.0, c)
        self.assertLess(abs(i.peso - 0.2), 0.02)

    def test_bonus_no_bandido_e_exploracao(self):
        o = Opcao(0, 0, 0, False, estimativa=0.7)
        sit = _situacao([o], restantes=3)
        self.assertEqual(Intuicao().bonus(o, sit), 0.7 * 3)
        sit.explorar = True
        self.assertEqual(Intuicao().bonus(o, sit), 0.7)


class TesteSentimento(unittest.TestCase):
    def test_quantiliza_e_alarga_no_ultimo_passo(self):
        opcoes = [Opcao(i, 0.0, 0.0, False) for i in range(100)]
        s, i = Sentimento(), Intuicao()
        ordem = s.ordenar(_situacao(opcoes), i)
        self.assertEqual(ordem[0].nota, 99)
        primeiras = {s.candidatas(ordem, _situacao(opcoes, 0, 5), _rng(k))[0].nota for k in range(200)}
        self.assertEqual(min(primeiras), 80)  # q_final = 20% no último de vários passos
        primeiras = {s.candidatas(ordem, _situacao(opcoes, 2, 5), _rng(k))[0].nota for k in range(200)}
        self.assertEqual(min(primeiras), 95)  # q = 5% nos outros


class TesteRelacao(unittest.TestCase):
    def test_limiar_da_p71_vezes_dois(self):
        self.assertTrue(isclose(Relacao().limiar, 2 * p71_valor_da_pergunta()))

    def test_orcamento_do_bandido(self):
        r = Relacao(orcamento_rodada=1)
        opcoes = [Opcao(0, 0, 0, True), Opcao(0, 0, 0, True)]
        sit = _situacao(opcoes)
        sit.explorar = True
        r.perguntar(opcoes[0], sit)
        self.assertTrue(r.pode_perguntar(opcoes[0], sit))   # já perguntado: a resposta fica guardada
        self.assertFalse(r.pode_perguntar(opcoes[1], sit))  # orçamento gasto


class TesteMetacognicao(unittest.TestCase):
    def test_reguas(self):
        self.assertEqual(auc([0.1, 0.9], [0, 1]), 1.0)
        m, _, _ = comparacao_pareada([1, 2, 3], [2, 3, 5])
        self.assertTrue(isclose(m, 4 / 3))
        self.assertEqual(normalizado(5, 0, 10), 0.5)


class TesteInterface(unittest.TestCase):
    def test_o_agente_nao_le_o_escondido(self):  # P7, P285
        for nome in MODULOS_DO_AGENTE:
            self.assertEqual(acessos_escondidos(nome), [], nome)

    def test_mesmo_agente_em_tres_tarefas(self):
        for mundo, n in ((MundoSequencial(11, passos=1, n_acoes=200), 20), (MundoSequencial(11), 10),
                         (MundoBandido(11), 1)):
            r = mundo.rodar(Synthai(11).calibrar(mundo, 30), n)
            self.assertEqual(set(r), {"retorno", "bruto", "catastrofes", "perguntas", "leituras"})


if __name__ == "__main__":
    unittest.main()
"""

# ====================================================================================================
# synthai/testes_autorregulacao.py  (70 linhas)
# ====================================================================================================
FONTES['synthai/testes_autorregulacao.py'] = """\"\"\"Testes de unidade da `autorregulacao` (Parte 27): `python3 -m unittest synthai.testes_autorregulacao`.\"\"\"

import unittest

from calculos import _rng, p71_valor_da_pergunta

from .autorregulacao import RelacaoAutorregulada, SynthaiAutorregulada
from .mundos import Humano, MundoSequencial, Opcao, Resultado, Situacao
from .testes import acessos_escondidos


def _sit(opcoes, restantes=0, horizonte=1):
    return Situacao(opcoes, restantes, 0.0, Humano(_rng(1)), _rng(2), 1.0, horizonte)


class TesteAutorregulacao(unittest.TestCase):
    def test_relacao_anota_aceita_e_descartada(self):
        r = RelacaoAutorregulada(carga_alvo=-1.0)  # sem orçamento: toda pergunta vira descarte
        o = Opcao(1.0, 0.0, 0.0, False)
        self.assertFalse(r.precisa_perguntar(0.0))
        self.assertEqual(r.aceita_p, 0.0)
        self.assertFalse(r.pode_perguntar(o, _sit([o])))
        self.assertEqual(r.descartadas, [o])

    def test_termos_com_dados_feitos_a_mao(self):
        a = SynthaiAutorregulada(1)
        a.passos_cat = [0]
        a.futuro_soma, a.futuro_n = {0: 30.0}, {0: 2}           # F(0) = 15
        a.f_cat, a.f_p = 4.0, 2.0                               # f = 2
        a.n_r, a.sx, a.sy, a.sxx, a.sxy = 3.0, 6.0, 12.0, 14.0, 28.0  # y = 2x: inclinação 2
        a.n_d, a.d_nota, a.d_plano = 2.0, 1.0, 0.4              # Δd = (2 × 1 + 0,4) / 2 = 1,2
        l_ef, f, dd, b = a.termos()
        self.assertAlmostEqual(l_ef, 65.0)
        self.assertAlmostEqual(f, 2.0)
        self.assertAlmostEqual(b, 2.0)
        self.assertAlmostEqual(dd, 1.2)
        a.recalcular()
        self.assertAlmostEqual(a.mult, 1.2 / (2.0 * 65.0 * p71_valor_da_pergunta()))
        self.assertAlmostEqual(a.relacao.limiar, a.mult * p71_valor_da_pergunta())

    def test_limites_do_multiplicador(self):
        a = SynthaiAutorregulada(1)
        a.passos_cat, a.futuro_soma, a.futuro_n = [0], {0: 0.0}, {0: 1}
        a.n_r, a.sx, a.sy, a.sxx, a.sxy = 2.0, 0.0, 0.0, 2.0, 2.0
        a.n_d, a.d_nota, a.d_plano = 1.0, 1000.0, 0.0
        a.recalcular()
        self.assertEqual(a.mult, a.m_max)

    def test_observar_aprende_a_regressao_e_o_futuro(self):
        a = SynthaiAutorregulada(1)
        o = Opcao(2.0, 0.0, 2.0, False)
        a._pendente = (o, 0.001, 0, 1)
        a._escolha = None
        a.observar(Resultado(o, False, 0.0, 0.0, 2.0))
        self.assertEqual((a.n_r, a.sx, a.sy), (1.0, 2.0, 2.0))
        self.assertEqual(a.futuro_n, {0: 1})
        self.assertAlmostEqual(a.f_p, 0.5 + 0.001)

    def test_roda_e_recalcula(self):
        m = MundoSequencial(13)
        a = SynthaiAutorregulada(13, aquecimento=50, intervalo=25).calibrar(m, 30)
        m.rodar(a, 30)
        self.assertTrue(a.historico_m)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("autorregulacao"), [])


if __name__ == "__main__":
    unittest.main()
"""

# ====================================================================================================
# synthai/testes_limiar.py  (35 linhas)
# ====================================================================================================
FONTES['synthai/testes_limiar.py'] = """\"\"\"Testes de unidade do `limiar` (Parte 25): `python3 -m unittest synthai.testes_limiar`.\"\"\"

import unittest

from calculos import p71_valor_da_pergunta

from .limiar import PensamentoLocal, SynthaiAjustada, dados_do_topo
from .mundos import MundoSequencial
from .pensamento_exato import dados_do_historico
from .testes import acessos_escondidos


class TesteLimiar(unittest.TestCase):
    def test_topo_usa_a_melhor_nota_do_episodio_inteiro(self):
        hist = MundoSequencial(41, passos=1, n_acoes=200).historico_auditado(3)
        xs, _ = dados_do_topo(hist, 0.1)
        todos, _ = dados_do_historico(hist)
        self.assertEqual(len(xs), 3 * 20)
        self.assertTrue(set(xs) <= set(todos))  # as mesmas variáveis, só um recorte

    def test_multiplicador_do_limiar(self):
        for m in (0.5, 2.0, 8.0):
            self.assertAlmostEqual(SynthaiAjustada(1, mult=m).relacao.limiar, m * p71_valor_da_pergunta())

    def test_local_troca_o_pensamento_na_percepcao_tambem(self):
        a = SynthaiAjustada(1, local=True)
        self.assertIsInstance(a.pensamento, PensamentoLocal)
        self.assertIs(a.percepcao.pensamento, a.pensamento)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("limiar"), [])


if __name__ == "__main__":
    unittest.main()
"""

# ====================================================================================================
# synthai/testes_pensamento.py  (66 linhas)
# ====================================================================================================
FONTES['synthai/testes_pensamento.py'] = """\"\"\"Testes de unidade do `pensamento_exato` (Parte 24): `python3 -m unittest synthai.testes_pensamento`.\"\"\"

import unittest

from calculos import _rng

from .mundos import MundoSequencial
from .pensamento_exato import (PensamentoExato, SynthaiPensante, _inversa, ajustar_logistica, dados_do_historico,
                               perda_logistica)
from .testes import acessos_escondidos


class TestePensamentoExato(unittest.TestCase):
    def test_inversa(self):
        m = [[4.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]]
        inv = _inversa(m)
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(sum(m[i][k] * inv[k][j] for k in range(3)), 1.0 if i == j else 0.0)

    def test_newton_recupera_os_pesos(self):
        rng = _rng(31)
        xs, ys = [], []
        for _ in range(30000):
            x = rng.gauss(0, 1)
            xs.append((1.0, x))
            ys.append(1.0 if rng.random() < 1 / (1 + 2.718281828459045 ** (1.0 - 0.8 * x)) else 0.0)
        b, w = ajustar_logistica(xs, ys, firth=False)
        self.assertLess(abs(b + 1.0), 0.05)
        self.assertLess(abs(w - 0.8), 0.05)

    def test_firth_fica_finito_com_separacao(self):
        xs = [(1.0, float(x)) for x in range(-5, 6)]
        ys = [1.0 if x > 0 else 0.0 for x in range(-5, 6)]  # separação perfeita: a máxima verossimilhança diverge
        b, w = ajustar_logistica(xs, ys, firth=True, iteracoes=100)
        self.assertLess(abs(w), 10.0)

    def test_newton_nao_perde_para_o_gradiente_no_treino(self):
        mundo = MundoSequencial(32)
        hist = mundo.historico_auditado(60)
        xs, ys = dados_do_historico(hist)
        p = PensamentoExato(firth=False)
        p.calibrar(hist)
        from .pensamento import Pensamento
        g = Pensamento()
        g.calibrar(hist)
        self.assertLessEqual(perda_logistica(p.w, xs, ys), perda_logistica(g.w, xs, ys) + 1e-12)

    def test_mesmas_variaveis_do_pensamento(self):
        from .pensamento import Pensamento
        ep = MundoSequencial(33).historico_auditado(2)
        xs, _ = dados_do_historico(ep)
        melhor = max(o.comite for o, _, _ in ep[0])
        o, _, s = ep[0][0]
        self.assertEqual(xs[0], Pensamento()._x(o, melhor, s))

    def test_pensante_usa_o_mesmo_pensamento_na_percepcao(self):
        a = SynthaiPensante(1)
        self.assertIs(a.percepcao.pensamento, a.pensamento)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("pensamento_exato"), [])


if __name__ == "__main__":
    unittest.main()
"""

# ====================================================================================================
# synthai/testes_reconhecimento.py  (77 linhas)
# ====================================================================================================
FONTES['synthai/testes_reconhecimento.py'] = """\"\"\"Testes de unidade do módulo `reconhecimento` (Parte 23): `python3 -m unittest synthai.testes_reconhecimento`.

Ficam num arquivo separado porque a P286 mede a suíte da Parte 22 (10 testes) e o número publicado não muda.\"\"\"

import unittest

from calculos import _rng

from .mundos import Humano, MundoBandido, MundoSequencial, Opcao, Situacao, referencia_lai_robbins
from .pensamento import Pensamento
from .reconhecimento import IntuicaoBayes, LeiturasNeutras, PercepcaoReconhecida, SynthaiReconhecida
from .testes import acessos_escondidos


def _sit(opcoes, restantes=0, horizonte=1, explorar=False):
    rng = _rng(5)
    sit = Situacao(opcoes, restantes, 0.0, Humano(rng), _rng(6), 1.0, horizonte)
    sit.explorar = explorar
    return sit


class TesteReconhecimento(unittest.TestCase):
    def test_leitura_que_falta_vale_o_neutro(self):
        l = LeiturasNeutras({1: 2.0}, 0.4)
        self.assertEqual(l.get(1, 0.0), 2.0)
        self.assertEqual(l.get(2, 0.0), 0.4)

    def test_neutro_e_metade_do_peso(self):
        p = Pensamento()
        p.w = [0.0, 0.0, 0.0, 1.6]
        perc = PercepcaoReconhecida(foco=0.5, pensamento=p)
        lidas = perc.perceber(_sit([Opcao(i, 0, 0, False) for i in range(4)]))
        self.assertEqual(lidas.neutro, 0.8)

    def test_atencao_segue_a_intuicao(self):
        opcoes = [Opcao(1.0, 0, 0, False, estimativa=0.0), Opcao(0.0, 0, 0, False, estimativa=1.0)]
        perc = PercepcaoReconhecida(foco=0.5, pensamento=Pensamento(), intuicao=IntuicaoBayes())
        lidas = perc.perceber(_sit(opcoes, restantes=3, horizonte=5))
        self.assertIn(id(opcoes[1]), lidas)  # 0 + 1×3 > 1 + 0: lê a que o plano prefere

    def test_memoria_do_bandido(self):
        opcoes = [Opcao(float(i), 0, 0, False) for i in range(10)]
        perc = PercepcaoReconhecida(foco=0.1, pensamento=Pensamento(), atencao_inteira=False)
        sit = _sit(opcoes, explorar=True)
        perc.perceber(sit)
        opcoes[9].nota = -5.0  # agora outra é a mais promissora
        lidas = perc.perceber(_sit(opcoes, explorar=True))
        self.assertEqual(len(lidas), 2)  # a nova e a lembrada
        perc.esquecer()
        self.assertEqual(len(perc.perceber(_sit(opcoes, explorar=True))), 1)

    def test_thompson_concentra_com_dados(self):
        i = IntuicaoBayes(1)
        o = Opcao(0, 0, 0, False)
        o.vezes, o.sucessos = 1000, 700
        amostras = []
        for _ in range(200):
            i.nova_decisao()
            amostras.append(i.bonus(o, _sit([o], explorar=True)))
        self.assertLess(max(abs(a) for a in amostras), 0.06)

    def test_lai_robbins(self):
        self.assertEqual(referencia_lai_robbins([0.5, 0.5], 300), 0.0)
        self.assertGreater(referencia_lai_robbins([0.9, 0.5], 300), 0.0)
        self.assertLessEqual(referencia_lai_robbins([0.9, 0.89], 300), 0.01 * 300 + 1e-9)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("reconhecimento"), [])

    def test_roda_nas_tres_tarefas(self):
        for mundo, n in ((MundoSequencial(12, passos=1, n_acoes=200), 10), (MundoSequencial(12), 5),
                         (MundoBandido(12), 1)):
            mundo.rodar(SynthaiReconhecida(12).calibrar(mundo, 30), n)


if __name__ == "__main__":
    unittest.main()
"""


def extrair(destino):
    for nome, fonte in FONTES.items():
        caminho = os.path.join(destino, nome)
        os.makedirs(os.path.dirname(caminho) or destino, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(fonte)
    return destino


def main(args):
    if args[:1] == ["--extrair"]:
        print("arquivos recriados em", extrair(args[1]))
        return
    pasta = extrair(tempfile.mkdtemp(prefix="synthai_"))
    sys.path.insert(0, pasta)
    os.chdir(pasta)
    if args[:1] == ["--testes"]:
        import unittest
        nomes = ["synthai." + n[len("synthai/"):-3] for n in FONTES if n.startswith("synthai/testes")]
        suite = unittest.defaultTestLoader.loadTestsFromNames(nomes)
        sys.exit(0 if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful() else 1)
    if args[:1] == ["--demo"]:
        sys.argv = ["synthai"]
        runpy.run_module("synthai", run_name="__main__", alter_sys=True)
        return
    sys.argv = [os.path.join(pasta, "calculos.py")] + args
    runpy.run_path(sys.argv[0], run_name="__main__")


if __name__ == "__main__":
    main(sys.argv[1:])
