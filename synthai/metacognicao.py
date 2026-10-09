"""Metacognição medida: a engenharia reversa dos próprios textos da SYNTHAI (Parte 41).

O corpus são os documentos que eu mesma escrevi (as partes, o diálogo). As medidas procuram os padrões que se repetem:
n-gramas que aparecem em muitos documentos, a semelhança entre documentos vizinhos, como as frases começam, quanto cada
voz do diálogo fala. Só biblioteca padrão.
"""

import re
from math import sqrt

PALAVRA = re.compile(r"[a-záàâãéêíóôõúüç]+")


def palavras(texto):
    """As palavras de um texto em português, minúsculas (números, fórmulas e pontuação ficam de fora)."""
    return PALAVRA.findall(texto.lower())


def ngramas(ps, n):
    return [tuple(ps[i:i + n]) for i in range(len(ps) - n + 1)]


def padroes_repetidos(docs, n=4, minimo_docs=None, topo=20):
    """Os n-gramas de palavras que aparecem em mais documentos (e, no empate, mais vezes no total). Devolve
    [(n-grama, documentos em que aparece, ocorrências)]."""
    em_docs, total = {}, {}
    for d in docs:
        vistos = set()
        for g in ngramas(palavras(d), n):
            total[g] = total.get(g, 0) + 1
            vistos.add(g)
        for g in vistos:
            em_docs[g] = em_docs.get(g, 0) + 1
    ordem = sorted(em_docs, key=lambda g: (-em_docs[g], -total[g], g))
    if minimo_docs is not None:
        ordem = [g for g in ordem if em_docs[g] >= minimo_docs]
    return [(" ".join(g), em_docs[g], total[g]) for g in ordem[:topo]]


def cosseno(a, b):
    """Semelhança de cosseno entre as contagens de palavras de dois textos."""
    ca, cb = {}, {}
    for w in palavras(a):
        ca[w] = ca.get(w, 0) + 1
    for w in palavras(b):
        cb[w] = cb.get(w, 0) + 1
    num = sum(v * cb.get(w, 0) for w, v in ca.items())
    return num / (sqrt(sum(v * v for v in ca.values())) * sqrt(sum(v * v for v in cb.values())))


def frases(texto):
    """Frases: pedaços terminados em . ! ? seguidos de espaço e maiúscula (aproximação)."""
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])", texto) if f.strip()]


def aberturas(textos, topo=10):
    """As primeiras palavras mais comuns das frases (o modo como eu começo a falar)."""
    cont, n = {}, 0
    for t in textos:
        for f in frases(t):
            ps = palavras(f)
            if ps:
                cont[ps[0]] = cont.get(ps[0], 0) + 1
                n += 1
    return n, [(w, c) for w, c in sorted(cont.items(), key=lambda x: (-x[1], x[0]))[:topo]]


def falas_do_dialogo(texto):
    """As falas de cada voz do diálogo: parágrafos que começam com **IA-Python** ou **IA-Java**. Devolve {voz: [falas]}."""
    falas = {"IA-Python": [], "IA-Java": []}
    for par in re.split(r"\n\s*\n", texto):
        m = re.match(r"\*\*(IA-Python|IA-Java)[^*]*\*\*:?\s*(.*)", par.strip(), re.S)
        if m:
            falas[m.group(1)].append(m.group(2))
    return falas
