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


# --- Parte 31: o currículo, o MinSet mínimo (local), e duas medidas de significado ---

def fecho_parcial(ancoradas, defs, theta=1.0):
    """Fecho com entendimento parcial (P381): uma palavra passa a ser entendida quando pelo menos uma fração `theta` das
    palavras da sua definição já é conhecida (theta = 1 é o fecho exato da P371). Propagação em O(arestas): cada
    palavra guarda quantas das que a definem já se conhecem."""
    conhecidas = set(ancoradas)
    precisa = {x: max(0, -(-int(round(theta * 1000)) * len(s) // 1000)) for x, s in defs.items()}  # teto(theta·|s|)
    tem = {x: 0 for x in defs}
    usado_por = {}
    for x, s in defs.items():
        for y in s:
            usado_por.setdefault(y, []).append(x)
    fila = list(conhecidas)
    for x in defs:
        if x not in conhecidas and precisa[x] == 0:
            conhecidas.add(x)
            fila.append(x)
    while fila:
        y = fila.pop()
        for x in usado_por.get(y, ()):
            if x in conhecidas:
                continue
            tem[x] += 1
            if tem[x] >= precisa[x]:
                conhecidas.add(x)
                fila.append(x)
    return conhecidas


def minset_reduzido(nos, defs, minset):
    """Tira as palavras redundantes de um conjunto de retroalimentação (o pós-processamento padrão, P382): uma palavra
    v do conjunto é redundante se, devolvida ao grafo que já é acíclico, não fecha nenhum ciclo, isto é, se nenhuma
    palavra que v define alcança, pelo que está fora do conjunto, uma palavra que define v. Testa as palavras na ordem
    inversa da escolha gulosa (as últimas escolhidas primeiro) e devolve o conjunto mínimo (não necessariamente o
    mínimo de todos) resultante."""
    conjunto = set(minset)
    sai = {x: [] for x in nos}
    for x in nos:
        for y in defs[x]:
            if y in nos:
                sai[y].append(x)   # y define x: aresta y -> x
    for v in reversed(list(minset)):
        conjunto.discard(v)
        alvo = set(y for y in defs[v] if y in nos and y not in conjunto)
        fecha = v in alvo
        vistos = {v}
        pilha = [x for x in sai[v] if x not in conjunto]
        while pilha and not fecha:
            x = pilha.pop()
            if x in vistos:
                continue
            vistos.add(x)
            if x in alvo or x == v:
                fecha = True
                break
            pilha.extend(z for z in sai[x] if z not in conjunto and z not in vistos)
        if fecha:
            conjunto.add(v)
    return conjunto


def profundidades(d):
    """Profundidade de cada sinset na taxonomia: o menor número de hiperônimos até uma raiz (um sinset sem hiperônimo).
    Busca em largura a partir das raízes, descendo pelos hipônimos. O WordNet 3.0 tem um ciclo nos hiperônimos (P384): a
    primeira versão (recursão pela pilha) não terminava nele e estourou 13,9 GB de memória; a busca em largura visita
    cada sinset uma vez, com ou sem ciclo. Um sinset que não alcança raiz nenhuma fica de fora."""
    filhos = {}
    raizes = []
    for i, x in enumerate(d.sinsets):
        pais = [d.indice[h] for h in x[2] if h in d.indice]
        if not pais:
            raizes.append(i)
        for k in pais:
            filhos.setdefault(k, []).append(i)
    prof = {i: 0 for i in raizes}
    fila = list(raizes)
    for j in fila:
        for k in filhos.get(j, ()):
            if k not in prof:
                prof[k] = prof[j] + 1
                fila.append(k)
    return prof


def ancestrais(d, i):
    """Todos os ancestrais de um sinset na taxonomia (ele incluído)."""
    vistos, pilha = set(), [i]
    while pilha:
        j = pilha.pop()
        if j in vistos:
            continue
        vistos.add(j)
        pilha.extend(d.indice[h] for h in d.sinsets[j][2] if h in d.indice)
    return vistos


def wu_palmer(d, prof, a, b):
    """Similaridade de Wu e Palmer (1994): 2·prof(LCS) / (prof(a) + prof(b)), com profundidade contada em nós (raiz = 1)
    e LCS o ancestral comum mais profundo. 0 se não houver ancestral comum."""
    comuns = ancestrais(d, a) & ancestrais(d, b)
    if not comuns:
        return 0.0
    lcs = max(prof[c] for c in comuns) + 1
    return 2 * lcs / ((prof[a] + 1) + (prof[b] + 1))


def lesk(d, a, b):
    """Sobreposição de Lesk (1986): o índice de Jaccard entre as palavras de conteúdo das duas definições."""
    pa = set(d.palavras_da_definicao(d.sinsets[a][3]))
    pb = set(d.palavras_da_definicao(d.sinsets[b][3]))
    return len(pa & pb) / len(pa | pb) if pa | pb else 0.0


def spearman(x, y):
    """Correlação de postos de Spearman (com empates pela média dos postos)."""
    def postos(v):
        ordem = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[ordem[j + 1]] == v[ordem[i]]:
                j += 1
            for k in range(i, j + 1):
                r[ordem[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = postos(x), postos(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    return cov / (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5


def fecho_incremental(ordem, defs, theta=1.0, ate=None):
    """O fecho parcial (P381) para TODOS os prefixos de um currículo de uma vez (P421): ancora as palavras de `ordem` uma
    a uma e propaga só o que a nova âncora destrava. Como o fecho é monótono nas âncoras, os contadores nunca voltam: o
    custo total é O(arestas), contra O(arestas) POR PONTO na bisseção da P385. Devolve a lista cob, com cob[k] = número
    de palavras entendidas com as k primeiras âncoras (k = 0..ate)."""
    ate = len(ordem) if ate is None else ate
    precisa = {x: max(0, -(-int(round(theta * 1000)) * len(s) // 1000)) for x, s in defs.items()}
    tem = {x: 0 for x in defs}
    usado_por = {}
    for x, s in defs.items():
        for y in s:
            usado_por.setdefault(y, []).append(x)
    conhecidas = set()

    def propagar(fila):
        while fila:
            y = fila.pop()
            for x in usado_por.get(y, ()):
                if x in conhecidas:
                    continue
                tem[x] += 1
                if tem[x] >= precisa[x]:
                    conhecidas.add(x)
                    fila.append(x)

    inicio = [x for x in defs if precisa[x] == 0]
    conhecidas.update(inicio)
    propagar(list(inicio))
    cob = [len(conhecidas)]
    for x in ordem[:ate]:
        if x not in conhecidas:
            conhecidas.add(x)
            propagar([x])
        cob.append(len(conhecidas))
    return cob



class NaiveBayesContagens:
    """Classificador bayesiano ingênuo multinomial (Parte 34): o estado inteiro é uma tabela de contagens (classe,
    palavra) e o total por classe: uma estatística suficiente. Aprender um exemplo é somar; nada é sobrescrito, então
    a ordem dos exemplos não muda o resultado (o aprendizado contínuo sem esquecimento, ↩ P403). Suavização de Laplace."""

    def __init__(self, alfa=1.0):
        self.alfa = alfa
        self.cont = {}
        self.total = {}
        self.ncls = {}
        self.vocab = set()

    def aprender(self, palavras, classe):
        c = self.cont.setdefault(classe, {})
        for w in palavras:
            c[w] = c.get(w, 0) + 1
            self.vocab.add(w)
        self.total[classe] = self.total.get(classe, 0) + len(palavras)
        self.ncls[classe] = self.ncls.get(classe, 0) + 1

    def prever(self, palavras):
        from math import log
        n = sum(self.ncls.values())
        v = len(self.vocab) or 1
        melhor, arg = None, None
        for cl in sorted(self.ncls):
            sc = log(self.ncls[cl] / n)
            c, t = self.cont[cl], self.total[cl]
            for w in palavras:
                sc += log((c.get(w, 0) + self.alfa) / (t + self.alfa * v))
            if melhor is None or sc > melhor:
                melhor, arg = sc, cl
        return arg


class LogisticaSGD:
    """Regressão logística multinomial (softmax) por gradiente estocástico, uma passada, passo constante: o rival padrão
    do aprendizado contínuo. Atributos: presença das palavras da definição."""

    def __init__(self, classes, passo=0.1):
        self.classes = sorted(classes)
        self.w = {c: {} for c in self.classes}
        self.b = {c: 0.0 for c in self.classes}
        self.passo = passo

    def _escores(self, palavras):
        return {c: self.b[c] + sum(self.w[c].get(x, 0.0) for x in set(palavras)) for c in self.classes}

    def prever(self, palavras):
        s = self._escores(palavras)
        return max(self.classes, key=lambda c: (s[c], c))

    def aprender(self, palavras, classe):
        from math import exp
        s = self._escores(palavras)
        m = max(s.values())
        z = {c: exp(v - m) for c, v in s.items()}
        tot = sum(z.values())
        for c in self.classes:
            g = (1.0 if c == classe else 0.0) - z[c] / tot
            self.b[c] += self.passo * g
            wc = self.w[c]
            for x in set(palavras):
                wc[x] = wc.get(x, 0.0) + self.passo * g



def sentidos_por_lema(d):
    """Quantos sinsets contêm cada lema de uma palavra só (a polissemia, contada em todas as classes gramaticais)."""
    m = {}
    for _, lemas, _, _ in d.sinsets:
        for x in lemas:
            if "_" not in x and x.isalpha():
                m[x] = m.get(x, 0) + 1
    return m

PALAVRAS_VAZIAS_PT = frozenset("""a à ao aos as às o os de da das do dos em na nas no nos um uma uns umas e ou que se
por para pelo pela pelos pelas com sem como mais menos muito muita não é são ser ter seu sua seus suas lhe lhes qual
quais quando onde este esta estes estas esse essa esses essas isso isto aquele aquela algo alguém etc ex""".split())


class DicionarioPT:
    """O português do data lake (Parte 40): a OpenWordNet-PT (dados/ownpt_sinsets.tsv.gz, CC BY 4.0), alinhada ao WordNet
    3.0 pelo identificador do sinset. `lemas[sid]` são os lemas em português; `glosas[sid]`, a glosa (só ~15% dos sinsets
    com lema têm uma)."""

    def __init__(self, pasta=PASTA):
        import gzip
        self.lemas, self.glosas = {}, {}
        with gzip.open(os.path.join(pasta, "ownpt_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
            for linha in f:
                sid, lemas, glosa = linha.rstrip("\n").split("\t")
                if lemas:
                    self.lemas[sid] = lemas.split("|")
                if glosa:
                    self.glosas[sid] = glosa
        self.vocabulario = {x.lower() for ls in self.lemas.values() for x in ls if x.isalpha()}

    @staticmethod
    def fichas(texto):
        """As palavras de um texto em português: minúsculas, só letras (com acentos)."""
        import re
        return [w for w in re.findall(r"[a-záàâãéêíóôõúüç]+", texto.lower()) if w not in PALAVRAS_VAZIAS_PT]

    def lema(self, w, plurais=True):
        """A palavra, se for um lema; senão, com `plurais`, a forma singular pelas regras regulares do português
        (-ões/-ães → -ão, -ais → -al, -eis → -el, -óis → -ol, -is → -il, -ns → -m, -res/-zes/-ses → -r/-z/-s, -s → ∅)."""
        if w in self.vocabulario:
            return w
        if not plurais:
            return None
        for suf, troca in (("ões", "ão"), ("ães", "ão"), ("ais", "al"), ("eis", "el"), ("óis", "ol"), ("is", "il"),
                           ("ns", "m"), ("res", "r"), ("zes", "z"), ("ses", "s"), ("s", "")):
            if w.endswith(suf) and w[: -len(suf)] + troca in self.vocabulario:
                return w[: -len(suf)] + troca
        return None

    def grafo_de_definicoes(self, plurais=True):
        """Para cada lema (de uma palavra só) que pertence a um sinset com glosa: o conjunto dos lemas que aparecem nas glosas
        dos seus sinsets. Como no inglês (P371), uma palavra não se define por si mesma."""
        defs = {}
        for sid, glosa in self.glosas.items():
            usadas = {self.lema(w, plurais) for w in self.fichas(glosa)} - {None}
            for x in self.lemas.get(sid, []):
                x = x.lower()
                if x.isalpha():
                    defs.setdefault(x, set()).update(usadas)
        for x, s in defs.items():
            s.discard(x)
        return defs
