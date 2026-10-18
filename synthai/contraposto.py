"""As três contas da Parte 115 (biblioteca padrão).

1. DEZ CAMADAS CONTRAPOSTAS e DEZ GRADIENTES SOBREPOSTOS. Uma cadeia escalar h_k = φ(w_k·h_{k−1}) de 10 camadas. "Contrapostas": os pesos
   alternam a e 1/a, cada camada desfazendo a escala da anterior. O gradiente de ponta a ponta é o produto das 10 derivadas locais
   w_k·φ′(·) (a retropropagação). "Sobrepostos": os 10 gradientes ∂h₁₀/∂w_k, um por camada, se SOMAM na variação de primeira ordem quando
   os 10 pesos mudam juntos (Δh ≈ Σ g_k·δw_k, o princípio da superposição do diferencial); o resto é de 2ª ordem.
2. O DICIONÁRIO CONTADO, em ALGARISMOS e em ALGORITMOS. Os lemas do WordNet 3.0 (dados/). Em algarismos: a palavra como número em base 26
   bijetiva (dígitos 1..26), que é injetiva. Em algoritmos: cada letra é uma operação x ↦ (a·x + b) mod p, e a palavra é o PROGRAMA que
   aplica as letras em ordem, a partir de x = 1. Com operações que não comutam (afins), a ordem das letras importa; com operações que comutam
   (só translações), todo anagrama dá o mesmo resultado.
3. A ESCALA DOS VETORES (paradigma) contra as MEDIDAS META-PARADIGMA. Vetores reais do dicionário (contagem de bigramas de letras das
   glosas, 676 dimensões) projetados em k dimensões por uma matriz gaussiana N(0, 1/k) nova por par (Johnson-Lindenstrauss). A medida é a
   distorção r = ‖Px‖²/‖x‖², que tem distribuição χ²_k/k para QUALQUER x (média 1, desvio √(2/k)). A meta-medida é a estimativa desse
   desvio sobre m pares, e o desvio DELA cai como 1/√m."""

import gzip
import math
import os
import random


# --- 1. as dez camadas ---

def tanh_(x):
    """tanh por (e^{2x} − 1)/(e^{2x} + 1); o exp é passado de fora (math.exp aqui, o exp_ próprio no diálogo)."""
    e = math.exp(2.0 * x)
    return (e - 1.0) / (e + 1.0)


def cadeia(pesos, h0, ativacao="tanh"):
    """Frente e trás numa cadeia escalar. Devolve (h_final, ∂h_final/∂h0, [∂h_final/∂w_k para k = 1..10])."""
    hs, pre = [h0], []
    for w in pesos:
        z = w * hs[-1]
        pre.append(z)
        hs.append(math.tanh(z) if ativacao == "tanh" else z)
    deriv = [(1.0 - hs[k + 1] * hs[k + 1]) if ativacao == "tanh" else 1.0 for k in range(len(pesos))]
    g = 1.0                                   # ∂h_final/∂h_k, de trás para frente
    gw = [0.0] * len(pesos)
    for k in range(len(pesos) - 1, -1, -1):
        gw[k] = g * deriv[k] * hs[k]          # ∂h_final/∂w_k = (∂h_final/∂h_{k+1})·φ′·h_k
        g = g * deriv[k] * pesos[k]
    return hs[-1], g, gw


def pesos_contrapostos(a, n=10):
    return [a if k % 2 == 0 else 1.0 / a for k in range(n)]


def superposicao(pesos, h0, eps, sinais=None):
    """Δh real (os 10 pesos mudam juntos, δw_k = eps·sinal_k) contra a soma dos 10 gradientes Σ g_k·δw_k. Devolve |Δh − Σ g δw|."""
    sinais = sinais or [1.0 if k % 3 else -1.0 for k in range(len(pesos))]
    h, _, gw = cadeia(pesos, h0)
    h2, _, _ = cadeia([w + eps * s for w, s in zip(pesos, sinais)], h0)
    linear = sum(g * eps * s for g, s in zip(gw, sinais))
    return abs((h2 - h) - linear)


# --- 2. o dicionário contado, em algarismos e em algoritmos ---

def _raiz():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def contar_wordnet():
    """Lê dados/wordnet30_sinsets.tsv.gz. Devolve {pos: conjunto de lemas, como estão}, o nº de pares (lema, sinset), e o mesmo com os
    marcadores sintáticos dos adjetivos tirados ('(a)', '(p)', '(ip)' colados ao lema)."""
    import re
    por_pos, por_pos_limpo, pares = {}, {}, 0
    with gzip.open(os.path.join(_raiz(), "dados", "wordnet30_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        for linha in f:
            c = linha.split("\t")
            pos = "a" if c[0] in ("a", "s") else c[0]
            for lema in c[2].split(","):
                pares += 1
                por_pos.setdefault(pos, set()).add(lema)
                por_pos_limpo.setdefault(pos, set()).add(re.sub(r"\((a|p|ip)\)$", "", lema))
    return por_pos, por_pos_limpo, pares


def contar_ownpt():
    """O português (OpenWordNet-PT, dados/ownpt_sinsets.tsv.gz): nº de lemas distintos e de pares (lema, sinset)."""
    lemas, pares = set(), 0
    with gzip.open(os.path.join(_raiz(), "dados", "ownpt_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        for linha in f:
            c = linha.rstrip("\n").split("\t")
            if len(c) < 2:
                continue
            for lema in c[1].split(","):   # formato: id-pos, lemas (separados por vírgula), glosa
                if lema:
                    pares += 1
                    lemas.add(lema)
    return len(lemas), pares


def em_algarismos(palavra):
    """A palavra (a-z) como número em base 26 BIJETIVA: dígitos 1..26, N = Σ dᵢ·26^(L−1−i). Injetiva: palavras diferentes, números diferentes."""
    n = 0
    for ch in palavra:
        n = n * 26 + (ord(ch) - 96)
    return n


def de_algarismos(n):
    """O inverso da base 26 bijetiva."""
    letras = []
    while n > 0:
        n, r = divmod(n - 1, 26)
        letras.append(chr(97 + r))
    return "".join(reversed(letras))


P_PRIMO = 1000003


def alfabeto_de_algoritmos(semente=115, comutam=False):
    """Cada letra vira uma operação x ↦ (a·x + b) mod p (a ∈ [1, p−1], b ∈ [0, p−1]); com comutam=True, só translações (a = 1)."""
    rng = random.Random(semente)
    ops = {}
    for i in range(26):
        a = 1 if comutam else rng.randrange(1, P_PRIMO)
        b = rng.randrange(P_PRIMO)
        ops[chr(97 + i)] = (a, b)
    return ops


def executar(palavra, ops, x=1):
    """A palavra como PROGRAMA: aplica as operações das letras, da esquerda para a direita."""
    for ch in palavra:
        a, b = ops[ch]
        x = (a * x + b) % P_PRIMO
    return x


def colisoes(palavras, ops):
    """Quantos resultados distintos e quantos PARES de palavras colidem (mesmo resultado)."""
    from collections import Counter
    c = Counter(executar(w, ops) for w in palavras)
    return len(c), sum(v * (v - 1) // 2 for v in c.values())


# --- 3. a escala dos vetores contra a meta-medida ---

def vetores_de_glosas(quantos, inicio=0):
    """Vetores reais: contagem dos 676 bigramas de letras a-z de cada glosa do WordNet, nas `quantos` glosas a partir de `inicio`."""
    out = []
    with gzip.open(os.path.join(_raiz(), "dados", "wordnet30_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        for i, linha in enumerate(f):
            if i < inicio:
                continue
            if len(out) == quantos:
                break
            g = "".join(ch for ch in linha.split("\t")[4].lower() if "a" <= ch <= "z" or ch == " ")
            v = [0.0] * 676
            for a, b in zip(g, g[1:]):
                if a != " " and b != " ":
                    v[(ord(a) - 97) * 26 + ord(b) - 97] += 1.0
            out.append(v)
    return out


def distorcoes(k, m, semente=1150, inicio=0):
    """m pares (x = v_{2i} − v_{2i+1}), cada um projetado por uma P gaussiana NOVA (k×676, entradas N(0, 1/k)). Devolve as razões ‖Px‖²/‖x‖²."""
    rng = random.Random(semente)
    vs = vetores_de_glosas(2 * m, inicio)
    rs = []
    for i in range(m):
        x = [a - b for a, b in zip(vs[2 * i], vs[2 * i + 1])]
        nx = sum(t * t for t in x)
        s = 1.0 / math.sqrt(k)
        tot = 0.0
        for _ in range(k):
            y = 0.0
            for t in x:
                if t != 0.0:
                    y += rng.gauss(0, s) * t
            tot += y * y
        rs.append(tot / nx)
    return rs


def media_desvio(xs):
    n = len(xs)
    mu = sum(xs) / n
    return mu, math.sqrt(sum((x - mu) ** 2 for x in xs) / (n - 1))
