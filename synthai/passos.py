"""O tamanho do passo numa quadrática anisotrópica (Parte 136).

Reescrita offline, só biblioteca padrão, das ideias seguras de dois módulos recebidos que nenhuma parte tinha usado:
`externos/pacote_v015/objetivos_cognitivos.py` (a quadrática SPD com condição κ, autovalores em progressão geométrica de 1 a κ,
base ortonormal sorteada) e `externos/pacote3/inovacao_guiada.py` (o passo de secante 0,8·(s·s)/(s·y) com proteção, a média
exponencial do gradiente e o limite da norma do deslocamento). Os originais usam numpy e um módulo `recursiva_paraconsistente`
que não veio no pacote; aqui não há nem um nem outro. E um auditor de CAPACIDADES para tudo o que é recebido: rede, processo,
código dinâmico e desserialização (o `security_audit_ast_v2` da Parte 111 só olha a rede).
"""
import ast
import math
import random


# --- a quadrática de objetivos_cognitivos.py ---

def _gram_schmidt(colunas):
    base = []
    for v in colunas:
        w = list(v)
        for b in base:
            p = sum(wi * bi for wi, bi in zip(w, b))
            w = [wi - p * bi for wi, bi in zip(w, b)]
        n = math.sqrt(sum(wi * wi for wi in w))
        base.append([wi / n for wi in w])
    return base


def quadratica_anisotropica(dimensao=8, condicao=10.0, semente=31001):
    """Devolve (A, autovalores, Q): A = Q diag(λ) Qᵀ, λ_i = κ^{i/(d-1)} (de 1 a κ), Q ortonormal por Gram-Schmidt de uma
    matriz gaussiana com a semente dada. Q é uma lista de vetores-coluna (Q[i] é o autovetor de λ_i)."""
    rng = random.Random(semente)
    Q = _gram_schmidt([[rng.gauss(0.0, 1.0) for _ in range(dimensao)] for _ in range(dimensao)])
    lam = [condicao ** (i / (dimensao - 1)) for i in range(dimensao)]
    A = [[sum(lam[k] * Q[k][i] * Q[k][j] for k in range(dimensao)) for j in range(dimensao)] for i in range(dimensao)]
    return A, lam, Q


def custo(A, x, alvo):
    d = [xi - ai for xi, ai in zip(x, alvo)]
    return sum(d[i] * sum(A[i][j] * d[j] for j in range(len(d))) for i in range(len(d)))


def gradiente(A, x, alvo):
    d = [xi - ai for xi, ai in zip(x, alvo)]
    return [2.0 * sum(A[i][j] * d[j] for j in range(len(d))) for i in range(len(d))]


# --- os passos de inovacao_guiada.py ---

def passo_secante(s, y, fallback, fator=0.8, minimo=0.002, maximo=0.4):
    """O passo de Barzilai-Borwein do texto recebido: fator·(s·s)/(s·y), recortado em [mínimo, máximo]; sem curvatura
    observável (s·s ≤ 1e-12 ou s·y ≤ 1e-10) devolve o fallback. Devolve (passo, válido)."""
    if s is None:
        return fallback, False
    ss = sum(a * a for a in s)
    sy = sum(a * b for a, b in zip(s, y))
    if not (math.isfinite(ss) and math.isfinite(sy)) or ss <= 1e-12 or sy <= 1e-10:
        return fallback, False
    return min(maximo, max(minimo, fator * ss / sy)), True


def descer(A, x0, alvo, T, metodo="fixo", passo=0.05, fator=0.8, beta=0.6, sigma=0.0, semente=0, limite=None):
    """Descida do gradiente com T passos. metodo: 'fixo' (passo constante), 'secante' (o passo de BB do texto, com o passo
    fixo como fallback no primeiro) ou 'media' (direção = média exponencial do gradiente com peso beta no atual).
    sigma: ruído gaussiano somado ao gradiente. limite: norma máxima do deslocamento (o 'limite_tangente'). Devolve a lista
    dos custos (T + 1 valores, o inicial primeiro)."""
    rng = random.Random(semente)
    x = list(x0)
    custos = [custo(A, x, alvo)]
    x_ant = g_ant = media = None
    for _ in range(T):
        g = gradiente(A, x, alvo)
        if sigma:
            g = [gi + sigma * rng.gauss(0.0, 1.0) for gi in g]
        eta, direcao = passo, g
        if metodo == "secante":
            s = None if x_ant is None else [a - b for a, b in zip(x, x_ant)]
            y = None if g_ant is None else [a - b for a, b in zip(g, g_ant)]
            eta, _ = passo_secante(s, y, passo, fator)
        elif metodo == "media":
            media = list(g) if media is None else [beta * a + (1 - beta) * b for a, b in zip(g, media)]
            direcao = media
        delta = [-eta * di for di in direcao]
        if limite is not None:
            n = math.sqrt(sum(di * di for di in delta))
            if n > limite:
                delta = [di * limite / n for di in delta]
        x_ant, g_ant = x, g
        x = [xi + di for xi, di in zip(x, delta)]
        custos.append(custo(A, x, alvo))
    return custos


def razao_fixo_fechada(lam, coordenadas, passo, T):
    """A forma fechada da descida de passo fixo numa quadrática: na base própria, a coordenada c_i é multiplicada por
    (1 - 2ηλ_i) a cada passo (a hessiana de dᵀAd é 2A), e o custo é Σ λ_i c_i². Devolve f_T / f_0."""
    f0 = sum(l * c * c for l, c in zip(lam, coordenadas))
    fT = sum(l * c * c * (1 - 2 * passo * l) ** (2 * T) for l, c in zip(lam, coordenadas))
    return fT / f0


def coordenadas_proprias(Q, x, alvo):
    d = [xi - ai for xi, ai in zip(x, alvo)]
    return [sum(q[i] * d[i] for i in range(len(d))) for q in Q]


def variancia_media_exponencial(beta, n=200000, semente=0):
    """Variância estacionária da média exponencial m ← βg + (1-β)m de ruído branco de variância 1, medida em n passos
    (descartando os 1000 primeiros). A forma fechada é β/(2-β)."""
    rng = random.Random(semente)
    m, soma, soma2, k = 0.0, 0.0, 0.0, 0
    for t in range(n):
        m = beta * rng.gauss(0.0, 1.0) + (1 - beta) * m
        if t >= 1000:
            soma += m
            soma2 += m * m
            k += 1
    media = soma / k
    return soma2 / k - media * media


# --- o auditor de capacidades ---

_PROCESSO = {("subprocess", None), ("os", "system"), ("os", "popen"), ("os", "fork"), ("os", "forkpty"), ("os", "spawnl"),
             ("os", "spawnv"), ("os", "spawnve"), ("os", "execv"), ("os", "execve"), ("os", "execl"), ("os", "execvp"),
             ("multiprocessing", None), ("pty", "spawn")}
_DINAMICO = {"eval", "exec", "compile", "__import__"}
_DESSERIALIZAR = {("pickle", "load"), ("pickle", "loads"), ("marshal", "loads"), ("marshal", "load"), ("dill", None),
                  ("shelve", "open")}
_IMPORTLIB = {"exec_module", "import_module", "spec_from_file_location", "load_module"}
_REDE_MODULOS = {"requests", "httpx", "aiohttp", "socket", "http", "ftplib", "smtplib", "urllib.request", "websocket",
                 "telnetlib", "paramiko", "nltk"}


def _nome_pontuado(no):
    partes = []
    while isinstance(no, ast.Attribute):
        partes.append(no.attr)
        no = no.value
    if isinstance(no, ast.Name):
        partes.append(no.id)
        return ".".join(reversed(partes))
    return None


def auditar_capacidades(fonte):
    """Lê a árvore sintática (SEM executar) e devolve {categoria: [achados]} para quatro capacidades: 'rede' (import de módulo
    de rede), 'processo' (import de subprocess/multiprocessing, chamada os.system/fork/exec*), 'dinamico' (chamada a
    eval/exec/compile/__import__ e importlib.exec_module & cia.) e 'desserializacao' (pickle.load(s), marshal, shelve).
    Conta USO (import, chamada), não MENÇÃO (uma string com 'subprocess' não conta: a regra da Parte 109). Um fonte que não
    é Python válido devolve {'nao_analisavel': [mensagem]}."""
    try:
        arvore = ast.parse(fonte)
    except SyntaxError as e:
        return {"nao_analisavel": [f"linha {e.lineno}: {e.msg}"]}
    achados = {"rede": set(), "processo": set(), "dinamico": set(), "desserializacao": set()}
    for no in ast.walk(arvore):
        modulos = []
        if isinstance(no, ast.Import):
            modulos = [a.name for a in no.names]
        elif isinstance(no, ast.ImportFrom) and no.module:
            modulos = [no.module] + [no.module + "." + a.name for a in no.names]
        for m in modulos:
            raiz = m.split(".")[0]
            if m in _REDE_MODULOS or (raiz in _REDE_MODULOS and raiz != "urllib"):
                achados["rede"].add("import:" + m)
            if raiz in ("subprocess", "multiprocessing"):
                achados["processo"].add("import:" + m)
            if raiz in ("pickle", "marshal", "dill", "shelve"):
                achados["desserializacao"].add("import:" + m)
        if isinstance(no, ast.Call):
            nome = _nome_pontuado(no.func)
            if nome is None:
                continue
            partes = nome.split(".")
            if nome in _DINAMICO:
                achados["dinamico"].add("chamada:" + nome)
            if partes[-1] in _IMPORTLIB:
                achados["dinamico"].add("chamada:" + nome)
            if len(partes) >= 2:
                base, fim = partes[0], partes[-1]
                if (base, None) in _PROCESSO or (base, fim) in _PROCESSO:
                    achados["processo"].add("chamada:" + nome)
                if (base, fim) in _DESSERIALIZAR or (base, None) in _DESSERIALIZAR:
                    achados["desserializacao"].add("chamada:" + nome)
    return {k: sorted(v) for k, v in achados.items() if v}
