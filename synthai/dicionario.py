"""O dicionário como data lake (Parte 30, P371 em diante): o WordNet 3.0 de Princeton (dados/wordnet30_*.tsv.gz).

Um dicionário define palavras por palavras. Harnad (1990) chamou isso de carrossel do dicionário: quem só tem o
dicionário passa de símbolo em símbolo sem nunca chegar ao significado (o problema da ancoragem dos símbolos). Os
métodos aqui medem a estrutura que torna o problema finito (Vincent-Lamarre, Harnad et al., 2016):

- o GRAFO DE DEFINIÇÕES: uma aresta v -> w quando v aparece na definição de w (v ajuda a definir w);
- o NÚCLEO (kernel): tirar, repetidamente, as palavras que não definem nenhuma palavra que restou;
- o CORE: o maior componente fortemente conexo do núcleo (Tarjan);
- o MINSET: um conjunto de retroalimentação de vértices (feedback vertex set) do núcleo: com essas palavras
  ancoradas de fora (pela percepção), todas as outras se definem por cadeias de definições, sem círculos. Achar o mínimo é
  NP-completo; aqui, uma aproximação gulosa;
- e medidas do dicionário como texto: a lei de Zipf nas palavras das definições e a entropia das letras.

A morfologia é o Morphy do WordNet: listas de exceções e regras de sufixo."""

import gzip
import os
import re
from math import log, log2

PASTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados")

# Palavras gramaticais (de função), que não carregam definição: lista curta e explícita
FUNCAO = set("""a an the and or but nor not no of in on at to for from by with as into onto upon about above below over under
between among through during before after since until than then so such that this these those there here which who whom whose
what when where why how whether if else also very more most less least much many some any each every all both either neither
other another its it it's he she they them their his her him we us our you your i me my is are was were be been being am has
have had having do does did doing can could may might must shall should will would one ones something someone somebody
anything etc esp e.g. i.e. used use usually especially often typically""".split())

REGRAS = {"n": [("s", ""), ("ses", "s"), ("xes", "x"), ("zes", "z"), ("ches", "ch"), ("shes", "sh"), ("men", "man"), ("ies", "y")],
          "v": [("s", ""), ("ies", "y"), ("es", "e"), ("es", ""), ("ed", "e"), ("ed", ""), ("ing", "e"), ("ing", "")],
          "a": [("er", ""), ("est", ""), ("er", "e"), ("est", "e")],
          "r": []}


class Dicionario:
    def __init__(self, pasta=PASTA):
        self.sinsets = []           # (classe, lemas, hiperônimos, glosa)
        self.lemas = {}             # lema -> lista de índices de sinsets
        self.indice = {}            # "classe:deslocamento" -> índice
        with gzip.open(os.path.join(pasta, "wordnet30_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
            for linha in f:
                pos, desloc, lemas, hiper, glosa = linha.rstrip("\n").split("\t")
                lemas = [re.sub(r"\(.*\)$", "", x) for x in lemas.split(",") if x]
                i = len(self.sinsets)
                self.sinsets.append((pos, lemas, [h for h in hiper.split(",") if h], glosa))
                self.indice[f"{pos}:{desloc}"] = i
                for x in lemas:
                    self.lemas.setdefault(x, []).append(i)
        self.excecoes = {}
        with gzip.open(os.path.join(pasta, "wordnet30_excecoes.tsv.gz"), "rt", encoding="utf-8") as f:
            for linha in f:
                pos, forma, bases = linha.rstrip("\n").split("\t")
                self.excecoes.setdefault(forma, []).extend(bases.split(","))

    def morphy(self, palavra):
        """A forma-base de uma palavra flexionada que existe no dicionário (exceções primeiro, depois as regras)."""
        if palavra in self.lemas:
            return palavra
        for base in self.excecoes.get(palavra, []):
            if base in self.lemas:
                return base
        for pos in ("n", "v", "a"):
            for suf, fim in REGRAS[pos]:
                if palavra.endswith(suf) and len(palavra) > len(suf) + 1:
                    base = palavra[: -len(suf)] + fim
                    if base in self.lemas:
                        return base
        return None

    @staticmethod
    def definicao(glosa):
        """A parte de definição da glosa (sem os exemplos entre aspas)."""
        return re.sub(r'"[^"]*"', " ", glosa).split(";")[0] if glosa else ""

    def palavras_da_definicao(self, glosa):
        saida = []
        for t in re.findall(r"[a-z]+(?:-[a-z]+)*", self.definicao(glosa).lower()):
            if t in FUNCAO or len(t) < 2:
                continue
            base = self.morphy(t)
            if base is not None and "_" not in base:
                saida.append(base)
        return saida

    def grafo_de_definicoes(self):
        """Para cada lema de uma palavra só: o conjunto das palavras (lemas de uma palavra só) usadas nas definições de
        todos os seus sentidos. Devolve {palavra: conjunto de palavras que a definem}."""
        defs = {}
        for pos, lemas, _, glosa in self.sinsets:
            usadas = set(self.palavras_da_definicao(glosa))
            for x in lemas:
                if "_" not in x and x.isalpha():
                    defs.setdefault(x, set()).update(usadas)
        for x, s in defs.items():
            s.discard(x)
            s.intersection_update(defs.keys())
        return defs


def nucleo(defs):
    """O núcleo: tira, repetidamente, as palavras que não definem nenhuma palavra que restou."""
    usos = {x: 0 for x in defs}
    for x, s in defs.items():
        for y in s:
            usos[y] += 1
    restam = set(defs)
    fila = [x for x, u in usos.items() if u == 0]
    while fila:
        x = fila.pop()
        if x not in restam:
            continue
        restam.discard(x)
        for y in defs[x]:
            if y in restam:
                usos[y] -= 1
                if usos[y] == 0:
                    fila.append(y)
    return restam


def componentes_fortes(nos, defs):
    """Componentes fortemente conexos (Tarjan, versão iterativa) do grafo restrito a `nos` (arestas palavra -> as que a
    definem)."""
    indice, baixo, na_pilha, pilha, comps = {}, {}, set(), [], []
    contador = 0
    for raiz in nos:
        if raiz in indice:
            continue
        trabalho = [(raiz, iter([y for y in defs[raiz] if y in nos]))]
        indice[raiz] = baixo[raiz] = contador
        contador += 1
        pilha.append(raiz)
        na_pilha.add(raiz)
        while trabalho:
            v, it = trabalho[-1]
            avancou = False
            for w in it:
                if w not in indice:
                    indice[w] = baixo[w] = contador
                    contador += 1
                    pilha.append(w)
                    na_pilha.add(w)
                    trabalho.append((w, iter([y for y in defs[w] if y in nos])))
                    avancou = True
                    break
                if w in na_pilha:
                    baixo[v] = min(baixo[v], indice[w])
            if avancou:
                continue
            trabalho.pop()
            if trabalho:
                baixo[trabalho[-1][0]] = min(baixo[trabalho[-1][0]], baixo[v])
            if baixo[v] == indice[v]:
                comp = set()
                while True:
                    w = pilha.pop()
                    na_pilha.discard(w)
                    comp.add(w)
                    if w == v:
                        break
                comps.append(comp)
    return comps


def minset_guloso(nos, defs):
    """Aproximação gulosa de um conjunto de retroalimentação de vértices: reduz (tira as palavras sem entrada ou sem
    saída no que resta, que não estão em ciclo nenhum) e, enquanto sobrar algo, ancora a palavra com maior produto
    (definida por) × (define), e reduz de novo."""
    entra = {x: set(y for y in defs[x] if y in nos) for x in nos}   # x é definida por estas
    sai = {x: set() for x in nos}                                     # x define estas
    for x, s in entra.items():
        for y in s:
            sai[y].add(x)
    restam = set(nos)
    escolhidas = []

    def tirar(x):
        restam.discard(x)
        for y in entra[x]:
            sai[y].discard(x)
        for y in sai[x]:
            entra[y].discard(x)
        entra[x], sai[x] = set(), set()

    def reduzir():
        fila = [x for x in restam if not entra[x] or not sai[x]]
        while fila:
            x = fila.pop()
            if x not in restam:
                continue
            vizinhos = entra[x] | sai[x]
            tirar(x)
            fila.extend(y for y in vizinhos if y in restam and (not entra[y] or not sai[y]))
    reduzir()
    while restam:
        x = max(restam, key=lambda z: (len(entra[z]) * len(sai[z]), z))
        escolhidas.append(x)
        tirar(x)
        reduzir()
    return escolhidas


def fecho(ancoradas, defs):
    """Ancorando estas palavras, quantas se definem por cadeias de definições? Devolve o conjunto e o número de rodadas
    (a profundidade: em cada rodada entram as palavras cuja definição só usa palavras já conhecidas)."""
    conhecidas = set(ancoradas)
    faltam = {x: set(s) - conhecidas for x, s in defs.items() if x not in conhecidas}
    rodadas = 0
    while True:
        novas = [x for x, s in faltam.items() if not s]
        if not novas:
            break
        rodadas += 1
        for x in novas:
            del faltam[x]
            conhecidas.add(x)
        novas = set(novas)
        for s in faltam.values():
            s -= novas
    return conhecidas, rodadas


def zipf(frequencias, de=10, ate=10000):
    """Expoente s da lei de Zipf (f ~ r^−s) por mínimos quadrados em log-log, entre os postos `de` e `ate`."""
    fs = sorted(frequencias, reverse=True)[de - 1: ate]
    xs = [log(r) for r in range(de, de + len(fs))]
    ys = [log(f) for f in fs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return -sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def entropia(contagens):
    total = sum(contagens)
    return -sum(c / total * log2(c / total) for c in contagens if c)
