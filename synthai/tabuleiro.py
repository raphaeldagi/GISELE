"""O tabuleiro do jogo de palavras com as letras de outra língua (Parte 150). O `WordGridEnv` da Parte 111 sorteia as letras com
`palavras_rl.LETTER_FREQ` (as frequências do inglês), lido a cada `reset`. Aqui: as frequências contadas num conjunto de lemas, e um
gerenciador de contexto que troca o `LETTER_FREQ` do módulo enquanto um experimento roda e o devolve no fim (o módulo não é editado:
o treino, o avaliador e a GRPO continuam os mesmos). E a densidade D = Σ_w Π_c p(c) das palavras de 3 a 5 letras sob as frequências do
tabuleiro: a chance de que uma sequência sorteada letra a letra seja uma palavra, a conta de peso que a Parte 149 pediu.
"""
import contextlib

from synthai import palavras_rl


def frequencias_de(palavras):
    """Frequência relativa (em %, como LETTER_FREQ) de cada letra A-Z nas palavras dadas; letra ausente fica com 0,01 (o sorteio precisa de peso
    positivo)."""
    cont = {chr(65 + i): 0 for i in range(26)}
    for w in palavras:
        for c in w.upper():
            if c in cont:
                cont[c] += 1
    total = sum(cont.values())
    return {c: max(100.0 * n / total, 0.01) for c, n in cont.items()}


@contextlib.contextmanager
def com_frequencias(freq):
    antigo = palavras_rl.LETTER_FREQ
    palavras_rl.LETTER_FREQ = dict(freq)
    try:
        yield
    finally:
        palavras_rl.LETTER_FREQ = antigo


def densidade(palavras, freq, minimo=3, maximo=5):
    """D = Σ_w Π_c p(c), p normalizada, sobre as palavras de minimo a maximo letras."""
    t = sum(freq.values())
    p = {c: v / t for c, v in freq.items()}
    d = 0.0
    for w in palavras:
        if minimo <= len(w) <= maximo:
            x = 1.0
            for c in w.upper():
                x *= p.get(c, 0.0)
            d += x
    return d


def paradas_por_comprimento(tamanho=5, minimo=3, maximo=5):
    """A geometria do braço aleatório (Parte 151), por enumeração exata dos caminhos sem repetir casa na grade com vizinhança de rei: começa numa casa
    uniforme; em cada casa, as ações são as vizinhas ainda não visitadas mais PARAR (se o caminho já tem `minimo` letras), e com `maximo` letras só PARAR;
    escolhe uma ação uniforme; sem ação, falha. Devolve {L: chance de parar com L letras}. Supõe que toda vizinha é uma ação distinta (ignora o colapso
    de duas vizinhas com a mesma letra, que o `valid_actions` junta numa ação só)."""
    def viz(r, c):
        return [(r + a, c + b) for a in (-1, 0, 1) for b in (-1, 0, 1)
                if (a or b) and 0 <= r + a < tamanho and 0 <= c + b < tamanho]
    out = {L: 0.0 for L in range(minimo, maximo + 1)}

    def anda(caminho, p):
        L = len(caminho)
        if L >= maximo:
            out[L] += p
            return
        livres = [v for v in viz(*caminho[-1]) if v not in caminho]
        n = len(livres) + (1 if L >= minimo else 0)
        if n == 0:
            return
        if L >= minimo:
            out[L] += p / n
        for v in livres:
            anda(caminho + [v], p / n)
    for r in range(tamanho):
        for c in range(tamanho):
            anda([(r, c)], 1.0 / (tamanho * tamanho))
    return out


def densidade_por_comprimento(palavras, freq, minimo=3, maximo=5):
    return {L: densidade(palavras, freq, L, L) for L in range(minimo, maximo + 1)}


def aleatorio_geometrico(palavras, freq, tamanho=5, minimo=3, maximo=5):
    """A previsão sem constante ajustada: Σ_L s_L · D_L (s da geometria, D das letras)."""
    s = paradas_por_comprimento(tamanho, minimo, maximo)
    d = densidade_por_comprimento(palavras, freq, minimo, maximo)
    return sum(s[L] * d[L] for L in s)


# --- o colapso das vizinhas de mesma letra (Parte 152) ---

def _distintas(p, n):
    """dist[k] = P(n sorteios iid com as probabilidades p (lista) têm k letras distintas), e, para cada letra c, comc[c][k] = P(c aparece e há k
    distintas). Programação dinâmica sobre as letras, com o peso multinomial n!·Π p_i^{m_i}/m_i!."""
    import math
    L = len(p)
    fat = [math.factorial(m) for m in range(n + 1)]

    def dp(forcar):
        # estado: (sorteios usados, distintas) -> peso
        est = {(0, 0): 1.0}
        for i, pi in enumerate(p):
            novo = {}
            for (t, k), w in est.items():
                inicio = 1 if i == forcar else 0
                for m in range(inicio, n - t + 1):
                    chave = (t + m, k + (1 if m else 0))
                    novo[chave] = novo.get(chave, 0.0) + w * pi ** m / fat[m]
            est = novo
        return [fat[n] * est.get((n, k), 0.0) for k in range(n + 1)]
    return dp(-1), [dp(c) for c in range(L)]


def tabela_colapso(freq, nmax=8):
    """Para n = 1..nmax vizinhas livres: (P(parar | n, com PARAR), [P(letra c | n, com PARAR)], [P(letra c | n, sem PARAR)]), com K = nº de letras
    distintas entre as n vizinhas: P(parar) = E[1/(K+1)]; P(c) = E[1{c presente}/(K+1)] (ou /K sem PARAR)."""
    letras = sorted(freq)
    t = sum(freq.values())
    p = [freq[c] / t for c in letras]
    tab = {}
    for n in range(1, nmax + 1):
        dist, comc = _distintas(p, n)
        parar = sum(dist[k] / (k + 1) for k in range(1, n + 1))
        com = {c: sum(comc[i][k] / (k + 1) for k in range(1, n + 1)) for i, c in enumerate(letras)}
        sem = {c: sum(comc[i][k] / k for k in range(1, n + 1)) for i, c in enumerate(letras)}
        tab[n] = (parar, com, sem)
    return tab


def assinaturas(tamanho=5, minimo=3, maximo=5):
    """Os caminhos geométricos agrupados pela sequência de nº de vizinhas livres em cada decisão: {(n_1, ..., n_L): peso}, peso = (1/casas) · Π (1/n_i)
    sobre as escolhas de casa (cada casa livre tem chance 1/n de ser a escolhida, dado o lado da letra). n_L é o nº de livres na última casa (a do PARAR);
    com L = maximo, n_L = -1 (só PARAR)."""
    def viz(r, c):
        return [(r + a, c + b) for a in (-1, 0, 1) for b in (-1, 0, 1)
                if (a or b) and 0 <= r + a < tamanho and 0 <= c + b < tamanho]
    out = {}

    def anda(caminho, ns, w):
        L = len(caminho)
        livres = [v for v in viz(*caminho[-1]) if v not in caminho]
        if L >= minimo:
            chave = tuple(ns + [len(livres) if L < maximo else -1])
            out[chave] = out.get(chave, 0.0) + w
        if L >= maximo:
            return
        for v in livres:
            anda(caminho + [v], ns + [len(livres)], w / len(livres))
    for r in range(tamanho):
        for c in range(tamanho):
            anda([(r, c)], [], 1.0 / (tamanho * tamanho))
    return out


def aleatorio_colapso(palavras, freq, tamanho=5, minimo=3, maximo=5):
    """A previsão com o colapso, em campo médio (as letras das vizinhas de cada decisão são sorteios novos e independentes; ignora que vizinhas já
    vistas reaparecem, e que o `setdefault` fica com a PRIMEIRA casa de cada letra). Para a palavra w (comprimento L) e uma assinatura (n_1..n_L):
    p(w_1) · Π_{i<L} q(w_{i+1} | n_i) · P(parar | n_L) (os 1/n_i da casa estão no peso), com q com ou sem PARAR conforme i ≥ minimo. A soma em w e nas assinaturas
    (pesos de assinaturas() já incluem os 1/n_i)."""
    t = sum(freq.values())
    p = {c: v / t for c, v in freq.items()}
    tab = tabela_colapso(freq)
    por_L = {}
    for w in palavras:
        if minimo <= len(w) <= maximo:
            por_L.setdefault(len(w), []).append(w.upper())
    total = 0.0
    for sig, peso in assinaturas(tamanho, minimo, maximo).items():
        L = len(sig)
        nL = sig[-1]
        parar = 1.0 if nL == -1 else (1.0 if nL == 0 else tab[nL][0])
        s = 0.0
        for w in por_L.get(L, []):
            x = p.get(w[0], 0.0)
            for i in range(1, L):
                n = sig[i - 1]
                q = tab[n][1] if i >= minimo else tab[n][2]
                x *= q.get(w[i], 0.0)
            s += x
        total += peso * parar * s
    return total


# --- o braço aleatório EXATO numa grade pequena (Parte 153) ---

def aleatorio_exato(palavras, freq, tamanho=3, minimo=3, maximo=5, casa="primeira"):
    """A chance exata de o braço aleatório achar uma palavra, somando sobre TODAS as atribuições de letras às casas (peso Π p) e, em cada uma, sobre
    todos os caminhos com a regra real do `valid_actions` (Parte 111): as vizinhas livres na ordem (−1, −1), …, (1, 1), uma ação por LETRA com a primeira
    casa daquela letra (setdefault), PARAR com `minimo` letras ou mais, só PARAR com `maximo`; escolha uniforme entre as ações; sem ação, falha. Só para
    grades pequenas e alfabetos pequenos (len(freq) ** (tamanho²) atribuições). casa = "uniforme" (Parte 154): em vez da primeira casa de cada letra,
    uma casa sorteada uniforme entre as livres daquela letra (separa o efeito do setdefault do da memória das letras)."""
    import itertools
    letras = [c for c in sorted(freq) if freq[c] > 0]
    t = sum(freq[c] for c in letras)
    p = {c: freq[c] / t for c in letras}
    dic = {w.upper() for w in palavras}
    casas = [(r, c) for r in range(tamanho) for c in range(tamanho)]

    def viz(r, c):
        return [(r + a, c + b) for a in (-1, 0, 1) for b in (-1, 0, 1)
                if (a or b) and 0 <= r + a < tamanho and 0 <= c + b < tamanho]
    vz = {u: viz(*u) for u in casas}
    total = 0.0
    for atrib in itertools.product(letras, repeat=len(casas)):
        grade = dict(zip(casas, atrib))
        peso = 1.0
        for x in atrib:
            peso *= p[x]

        def anda(caminho, prefixo):
            acoes = {}
            if len(caminho) < maximo:
                vis = set(caminho)
                for v in vz[caminho[-1]]:
                    if v not in vis:
                        acoes.setdefault(grade[v], []).append(v)
            parar = len(caminho) >= minimo
            n = len(acoes) + (1 if parar else 0)
            if n == 0:
                return 0.0
            s = (1.0 if prefixo in dic else 0.0) if parar else 0.0
            for letra, vs in acoes.items():
                if casa == "primeira":
                    s += anda(caminho + [vs[0]], prefixo + letra)
                else:
                    m = 0.0
                    for v in vs:
                        m += anda(caminho + [v], prefixo + letra)
                    s += m / len(vs)
            return s / n
        acerto = 0.0
        for u in casas:
            acerto += anda([u], grade[u])
        total += peso * acerto / len(casas)
    return total


def estatisticas_exatas(palavras, freq, tamanho=3, minimo=3, maximo=5, casa="primeira", ordem="direta"):
    """Parte 155: o enumerador exato de aleatorio_exato com a ordem das vizinhas escolhível ('direta' = (−1, −1), …, (1, 1); 'reversa' = (1, 1), …,
    (−1, −1)) e, além do acerto, as esperanças sobre o fim do episódio (o PARAR): deslocamento da casa final em relação à inicial (dr, dc), distância da
    casa final à borda mais próxima e comprimento do caminho. Devolve {acerto, dr, dc, borda, comprimento, falha} (falha = chance de ficar sem ação)."""
    import itertools
    letras = [c for c in sorted(freq) if freq[c] > 0]
    t = sum(freq[c] for c in letras)
    p = {c: freq[c] / t for c in letras}
    dic = {w.upper() for w in palavras}
    casas = [(r, c) for r in range(tamanho) for c in range(tamanho)]
    deltas = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]
    if ordem == "reversa":
        deltas = deltas[::-1]
    vz = {(r, c): [(r + a, c + b) for a, b in deltas if 0 <= r + a < tamanho and 0 <= c + b < tamanho] for r, c in casas}
    tot = {"acerto": 0.0, "dr": 0.0, "dc": 0.0, "borda": 0.0, "comprimento": 0.0, "falha": 0.0}
    for atrib in itertools.product(letras, repeat=len(casas)):
        grade = dict(zip(casas, atrib))
        peso = 1.0
        for x in atrib:
            peso *= p[x]

        def anda(caminho, prefixo):
            # devolve o vetor (acerto, dr, dc, borda, comprimento, falha) esperado a partir daqui
            acoes = {}
            if len(caminho) < maximo:
                vis = set(caminho)
                for v in vz[caminho[-1]]:
                    if v not in vis:
                        acoes.setdefault(grade[v], []).append(v)
            parar = len(caminho) >= minimo
            n = len(acoes) + (1 if parar else 0)
            if n == 0:
                return (0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
            s = [0.0] * 6
            if parar:
                (r0, c0), (r1, c1) = caminho[0], caminho[-1]
                fim = (1.0 if prefixo in dic else 0.0, r1 - r0, c1 - c0, min(r1, c1, tamanho - 1 - r1, tamanho - 1 - c1), len(caminho), 0.0)
                s = list(fim)
            for letra, vs in acoes.items():
                escolhidas = vs[:1] if casa == "primeira" else vs
                m = [0.0] * 6
                for v in escolhidas:
                    f = anda(caminho + [v], prefixo + letra)
                    m = [a + b for a, b in zip(m, f)]
                s = [a + b / len(escolhidas) for a, b in zip(s, m)]
            return tuple(x / n for x in s)
        for u in casas:
            f = anda([u], grade[u])
            for k, x in zip(("acerto", "dr", "dc", "borda", "comprimento", "falha"), f):
                tot[k] += peso * x / len(casas)
    return tot


def ramificacao_exata(palavras, freq, tamanho=3, minimo=3, maximo=5, casa="primeira"):
    """Parte 156: o enumerador exato de aleatorio_exato com as esperanças sobre as DECISÕES do episódio: o número esperado de decisões (nós visitados
    com ao menos uma opção), o número esperado de opções somadas sobre elas (ações por letra + PARAR) e o número esperado de casas livres vizinhas
    (antes do colapso por letra). Devolve {acerto, falha, decisoes, opcoes, livres}; a ramificação média é opcoes/decisoes, o colapso médio é
    1 − (opções sem o PARAR)/livres."""
    import itertools
    letras = [c for c in sorted(freq) if freq[c] > 0]
    t = sum(freq[c] for c in letras)
    p = {c: freq[c] / t for c in letras}
    dic = {w.upper() for w in palavras}
    casas = [(r, c) for r in range(tamanho) for c in range(tamanho)]
    deltas = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]
    vz = {(r, c): [(r + a, c + b) for a, b in deltas if 0 <= r + a < tamanho and 0 <= c + b < tamanho] for r, c in casas}
    nomes = ("acerto", "falha", "decisoes", "opcoes", "livres", "acoes")
    tot = dict.fromkeys(nomes, 0.0)
    for atrib in itertools.product(letras, repeat=len(casas)):
        grade = dict(zip(casas, atrib))
        peso = 1.0
        for x in atrib:
            peso *= p[x]

        def anda(caminho, prefixo):
            acoes = {}
            livres = 0
            if len(caminho) < maximo:
                vis = set(caminho)
                for v in vz[caminho[-1]]:
                    if v not in vis:
                        livres += 1
                        acoes.setdefault(grade[v], []).append(v)
            parar = len(caminho) >= minimo
            n = len(acoes) + (1 if parar else 0)
            if n == 0:
                return (0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
            s = [0.0] * 6
            if parar:
                s[0] = 1.0 if prefixo in dic else 0.0
            for letra, vs in acoes.items():
                escolhidas = vs[:1] if casa == "primeira" else vs
                m = [0.0] * 6
                for v in escolhidas:
                    f = anda(caminho + [v], prefixo + letra)
                    m = [a + b for a, b in zip(m, f)]
                s = [a + b / len(escolhidas) for a, b in zip(s, m)]
            s = [x / n for x in s]
            # esta decisão conta uma vez, com as suas opções e as suas casas livres
            s[2] += 1.0
            s[3] += n
            s[4] += livres
            s[5] += len(acoes)
            return tuple(s)
        for u in casas:
            f = anda([u], grade[u])
            for k, x in zip(nomes, f):
                tot[k] += peso * x / len(casas)
    return tot
