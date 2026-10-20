

# =============================================================================
# EXTENSÃO 3.0 — LÓGICA (FNC, TSEITIN, DPLL), CODIFICAÇÕES E EXPERIMENTOS CORRIGIDOS
# =============================================================================
# A 2.2.0 decide satisfatibilidade por força bruta (2ⁿ, até 16 variáveis). Aqui: conversão de
# Tseitin (fórmula → cláusulas, tamanho linear) e DPLL com propagação de unidade e literal puro,
# conferidos contra a tabela-verdade da 2.2.0 em fórmulas aleatórias.

class LogicaSAT:
    @staticmethod
    def tseitin(ast: tuple) -> tuple[list[list[int]], dict[str, int]]:
        """Cláusulas equi-satisfatíveis: cada subfórmula ganha uma variável nova; literal = ±índice."""
        nomes: dict[str, int] = {}
        clausulas: list[list[int]] = []
        contador = [0]

        def nova() -> int:
            contador[0] += 1
            return contador[0]

        def visita(no: tuple) -> int:
            op = no[0]
            if op == "var":
                if no[1] not in nomes:
                    nomes[no[1]] = nova()
                return nomes[no[1]]
            if op == "not":
                return -visita(no[1])
            a, b = visita(no[1]), visita(no[2])
            x = nova()
            if op == "and":
                clausulas.extend([[-x, a], [-x, b], [x, -a, -b]])
            elif op == "or":
                clausulas.extend([[-x, a, b], [x, -a], [x, -b]])
            elif op == "imp":
                clausulas.extend([[-x, -a, b], [x, a], [x, -b]])
            elif op == "iff":
                clausulas.extend([[-x, -a, b], [-x, a, -b], [x, a, b], [x, -a, -b]])
            else:
                raise ValueError("Operação lógica desconhecida")
            return x
        raiz = visita(ast)
        clausulas.append([raiz])
        return clausulas, nomes

    @staticmethod
    def dpll(clausulas: list[list[int]], limite_decisoes: int = 1_000_000) -> dict[str, Any]:
        """DPLL iterativo-recursivo com propagação de unidade e eliminação de literal puro."""
        estat = dict(decisoes=0, propagacoes=0)

        def simplificar(cls, lit):
            out = []
            for c in cls:
                if lit in c:
                    continue
                if -lit in c:
                    c = [x for x in c if x != -lit]
                    if not c:
                        return None
                out.append(c)
            return out

        def resolve(cls, atrib):
            while True:
                unit = next((c[0] for c in cls if len(c) == 1), None)
                if unit is None:
                    break
                estat["propagacoes"] += 1
                atrib[abs(unit)] = unit > 0
                cls = simplificar(cls, unit)
                if cls is None:
                    return None
            literais = {x for c in cls for x in c}
            for lit in [x for x in literais if -x not in literais]:
                atrib[abs(lit)] = lit > 0
                cls = simplificar(cls, lit)
            if not cls:
                return atrib
            estat["decisoes"] += 1
            if estat["decisoes"] > limite_decisoes:
                raise TimeoutError("Limite de decisões do DPLL")
            contagem = collections.Counter(abs(x) for c in cls for x in c)
            v = max(contagem, key=lambda k: (contagem[k], -k))
            for lit in (v, -v):
                c2 = simplificar(cls, lit)
                if c2 is not None:
                    a2 = dict(atrib)
                    a2[v] = lit > 0
                    r = resolve(c2, a2)
                    if r is not None:
                        return r
            return None
        r = resolve([list(c) for c in clausulas], {})
        return dict(satisfativel=r is not None, atribuicao=r or {}, **estat)

    @staticmethod
    def satisfativel(formulas: list[str]) -> dict[str, Any]:
        """Mesmo contrato da Logica.satisfativel da 2.2.0, sem o teto de 16 variáveis."""
        ast = Logica.analisar(formulas[0])
        for f in formulas[1:]:
            ast = ("and", ast, Logica.analisar(f))
        clausulas, nomes = LogicaSAT.tseitin(ast)
        r = LogicaSAT.dpll(clausulas)
        if not r["satisfativel"]:
            return dict(estado="CONTRADITORIO", variaveis=len(nomes), clausulas=len(clausulas))
        test = {n: r["atribuicao"].get(i, False) for n, i in nomes.items()}
        if not Logica.calcular(ast, test):
            raise AssertionError("Testemunha do DPLL não satisfaz a fórmula")
        return dict(estado="CONSISTENTE", testemunha=test, variaveis=len(nomes), clausulas=len(clausulas))

    @staticmethod
    def formula_aleatoria(rng: random.Random, nvar: int, profundidade: int) -> str:
        if profundidade == 0 or rng.random() < .25:
            v = f"x{rng.randrange(nvar)}"
            return ("!" + v) if rng.random() < .5 else v
        op = rng.choice(["&", "|", "->", "<->"])
        return f"({LogicaSAT.formula_aleatoria(rng, nvar, profundidade-1)} {op} " \
               f"{LogicaSAT.formula_aleatoria(rng, nvar, profundidade-1)})"

    @staticmethod
    def pombos(n: int) -> list[list[int]]:
        """Princípio da casa dos pombos: n+1 pombos em n casas (insatisfatível; difícil para resolução)."""
        var = lambda p, c: p * n + c + 1
        cls = [[var(p, c) for c in range(n)] for p in range(n + 1)]
        for c in range(n):
            for p in range(n + 1):
                for q in range(p + 1, n + 1):
                    cls.append([-var(p, c), -var(q, c)])
        return cls

    @staticmethod
    def k_sat_aleatorio(rng: random.Random, nvar: int, ncl: int, k: int = 3) -> list[list[int]]:
        return [[v * rng.choice((1, -1)) for v in rng.sample(range(1, nvar + 1), k)] for _ in range(ncl)]

    @staticmethod
    def transicao_3sat(nvar: int, razoes: list[float], instancias: int, seed: int) -> dict[float, float]:
        """Fração satisfatível do 3-SAT aleatório por razão cláusulas/variáveis (transição perto de 4,27)."""
        rng = random.Random(seed)
        out = {}
        for r in razoes:
            ok = sum(LogicaSAT.dpll(LogicaSAT.k_sat_aleatorio(rng, nvar, round(r * nvar)))["satisfativel"]
                     for _ in range(instancias))
            out[r] = ok / instancias
        return out


class CodificacaoNumerica:
    """Representações numéricas exatas de palavras (todas com ida e volta testadas)."""
    ALFABETO = "abcdefghijklmnopqrstuvwxyz"

    @staticmethod
    def base26_bijetiva(palavra: str) -> int:
        n = 0
        for c in palavra.lower():
            i = CodificacaoNumerica.ALFABETO.find(c)
            if i < 0:
                raise ValueError("Só letras a-z")
            n = n * 26 + i + 1
        return n

    @staticmethod
    def de_base26(n: int) -> str:
        if n < 0:
            raise ValueError("Inteiro não negativo")
        out = []
        while n:
            n, r = divmod(n - 1, 26)
            out.append(CodificacaoNumerica.ALFABETO[r])
        return "".join(reversed(out))

    @staticmethod
    def hamming74_codificar(nibble: int) -> int:
        """Código de Hamming (7,4): corrige 1 bit. Bits de paridade nas posições 1, 2 e 4."""
        d = [(nibble >> i) & 1 for i in range(4)]
        p1 = d[0] ^ d[1] ^ d[3]
        p2 = d[0] ^ d[2] ^ d[3]
        p3 = d[1] ^ d[2] ^ d[3]
        bits = [p1, p2, d[0], p3, d[1], d[2], d[3]]
        return sum(b << i for i, b in enumerate(bits))

    @staticmethod
    def hamming74_decodificar(palavra: int) -> tuple[int, int]:
        b = [(palavra >> i) & 1 for i in range(7)]
        s = (b[0] ^ b[2] ^ b[4] ^ b[6]) | ((b[1] ^ b[2] ^ b[5] ^ b[6]) << 1) | ((b[3] ^ b[4] ^ b[5] ^ b[6]) << 2)
        if s:
            b[s - 1] ^= 1
        return b[2] | (b[4] << 1) | (b[5] << 2) | (b[6] << 3), s

    @staticmethod
    def crc32(dados: bytes) -> int:
        """CRC-32 (polinômio refletido 0xEDB88320), conferido contra zlib.crc32 nos testes."""
        c = 0xFFFFFFFF
        for byte in dados:
            c ^= byte
            for _ in range(8):
                c = (c >> 1) ^ (0xEDB88320 if c & 1 else 0)
        return c ^ 0xFFFFFFFF

    @staticmethod
    def huffman(texto: str) -> dict[str, Any]:
        """Código de Huffman: comprimento médio entre H e H+1 bits por símbolo (Shannon)."""
        import heapq
        freq = collections.Counter(texto)
        if len(freq) == 1:
            codigos = {next(iter(freq)): "0"}
        else:
            heap = [(f, i, {s: ""}) for i, (s, f) in enumerate(sorted(freq.items()))]
            heapq.heapify(heap)
            k = len(heap)
            while len(heap) > 1:
                f1, _, a = heapq.heappop(heap)
                f2, _, b = heapq.heappop(heap)
                junto = {s: "0" + c for s, c in a.items()}
                junto.update({s: "1" + c for s, c in b.items()})
                heapq.heappush(heap, (f1 + f2, k, junto))
                k += 1
            codigos = heap[0][2]
        n = len(texto)
        media = sum(freq[s] * len(c) for s, c in codigos.items()) / n
        h = -sum(f / n * math.log2(f / n) for f in freq.values())
        bits = "".join(codigos[c] for c in texto)
        return dict(codigos=codigos, bits=bits, media=media, entropia=h)

    @staticmethod
    def huffman_decodificar(bits: str, codigos: dict[str, str]) -> str:
        inverso = {c: s for s, c in codigos.items()}
        out, atual = [], ""
        for b in bits:
            atual += b
            if atual in inverso:
                out.append(inverso[atual])
                atual = ""
        if atual:
            raise ValueError("Bits sobrando")
        return "".join(out)

    @staticmethod
    def lz78(texto: str) -> list[tuple[int, str]]:
        dic, out, w = {"": 0}, [], ""
        for c in texto:
            if w + c in dic:
                w += c
            else:
                out.append((dic[w], c))
                dic[w + c] = len(dic)
                w = ""
        if w:
            out.append((dic[w[:-1]], w[-1]))
        return out

    @staticmethod
    def lz78_decodificar(pares: list[tuple[int, str]]) -> str:
        dic, out = [""], []
        for i, c in pares:
            s = dic[i] + c
            out.append(s)
            dic.append(s)
        return "".join(out)


class ExperimentosCorrigidos:
    """Os experimentos da 2.2.0 refeitos com as correções medidas (Parte 121 da série SYNTHAI):
    o IC do bootstrap pelos quantis da contagem real de réplicas (o código antigo fixava os índices
    24 e 974 e quebrava com 500 réplicas); o qui-quadrado da Mega-Sena com o fator de correção do
    sorteio sem reposição e com p-valor; o veredito do H-M3 por seed E combinado; o H-M7 com o
    arrependimento medido pelas médias verdadeiras, em muitas sementes."""

    @staticmethod
    def megasena(n: int, seed: int, replicas: int = 1000) -> dict[str, Any]:
        rng = random.Random(seed)
        sorteios = [set(rng.sample(range(1, 61), 6)) for _ in range(n)]
        deltas = []
        for pos in range(100, n):
            passado = collections.Counter(x for s in sorteios[pos - 100:pos] for x in s)
            quentes = set(sorted(range(1, 61), key=lambda x: (-passado[x], x))[:6])
            aleatoria = set(rng.sample(range(1, 61), 6))
            deltas.append(len(quentes & sorteios[pos]) - len(aleatoria & sorteios[pos]))
        media, inf, sup = Estatistica.bootstrap_media(deltas, seed + 999, replicas)
        contagem = collections.Counter(x for s in sorteios for x in s)
        # Cada dezena: Binomial(n, 1/10), variância n·0,1·0,9; sem reposição dentro do sorteio as contagens se
        # correlacionam negativamente: Σ(c−e)²/e tem média 60·0,9 = 54 e se distribui como (54/59)·χ²₅₉.
        q = Estatistica.qui2_uniformidade([contagem[x] for x in range(1, 61)], 54 / 59)
        t = Estatistica.media_ic_t(deltas)
        return dict(sorteios=n, media_delta=media, ic95_bootstrap=[inf, sup], ic95_t=[t[1], t[2]],
                    qui2=q["estatistica"], qui2_esperado=54.0, fator=q["fator"], p_valor=q["p_valor"],
                    veredito="ACEITA" if inf > 0 else ("REJEITADA" if sup < 0 else "INCONCLUSIVA (inclui 0)"))

    @staticmethod
    def h_m3(n: int, seeds: list[int], replicas: int = 1000) -> dict[str, Any]:
        por_seed, ganhos = [], []
        for seed in seeds:
            rng = random.Random(seed)
            amostras = [rng.randrange(2) for _ in range(n)]
            amostras = [(x, int(rng.random() < (.15 if x == 0 else .85))) for x in amostras]
            treino, teste = amostras[:int(.6 * n)], amostras[int(.8 * n):]
            glob = BetaBernoulli()
            grupos = {0: BetaBernoulli(), 1: BetaBernoulli()}
            for x, y in treino:
                glob.observar(y)
                grupos[x].observar(y)
            d = [(glob.prever() - y) ** 2 - (grupos[x].prever() - y) ** 2 for x, y in teste]
            m, inf, sup = Estatistica.bootstrap_media(d, seed + 100, replicas)
            ganhos.extend(d)
            por_seed.append(dict(seed=seed, ganho=m, ic=[inf, sup], aceita=inf > 0))
        m, inf, sup = Estatistica.bootstrap_media(ganhos, 12345, replicas)
        return dict(por_seed=por_seed, aceitas=sum(r["aceita"] for r in por_seed), seeds=len(seeds),
                    ganho_combinado=m, ic95_combinado=[inf, sup],
                    veredito_combinado="ACEITA" if inf > 0 else "INCONCLUSIVA")

    @staticmethod
    def h_m7(seeds: int, passos: int = 1000) -> dict[str, Any]:
        """Os dois reforços da 2.2.0 em `seeds` sementes, com o arrependimento pelas médias verdadeiras
        (0,75 e 0,55): sem ruído de avaliação de 200 passos. Teste t pareado e de sinal."""
        arrep = {"ordinario": [], "extraordinario": []}
        travado = {"ordinario": 0, "extraordinario": 0}
        for s in range(seeds):
            for tipo in arrep:
                r = BandidoContextual.simular(s, tipo, passos)
                arrep[tipo].append(0.20 if r["acao_escolhida"] == 1.0 else 0.0)
                travado[tipo] += r["acao_escolhida"] == 1.0
        dif = [a - b for a, b in zip(arrep["ordinario"], arrep["extraordinario"])]
        return dict(seeds=seeds, trava_no_pior={k: v / seeds for k, v in travado.items()},
                    diferenca_media=statistics.fmean(dif),
                    t_pareado=Estatistica.t_pareado(arrep["ordinario"], arrep["extraordinario"]),
                    sinal=Estatistica.sinal(dif))
