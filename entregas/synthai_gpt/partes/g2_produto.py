

# =============================================================================
# SYNTHAI-GPT — TOKENIZADORES, CORPUS, TREINO, AMOSTRAGEM, AVALIAÇÃO, PESOS
# =============================================================================

class TokenizadorCaracteres:
    """Uma ficha por caractere; caracteres fora do vocabulário viram '?' (que sempre está no vocabulário)."""
    tipo = "caracteres"

    def __init__(self, vocab: list[str]):
        if "?" not in vocab:
            vocab = sorted(set(vocab) | {"?"})
        self.vocab = list(vocab)
        self.indice = {c: i for i, c in enumerate(self.vocab)}

    @classmethod
    def de_texto(cls, texto: str, minimo: int = 1) -> "TokenizadorCaracteres":
        cont = collections.Counter(texto)
        return cls(sorted(c for c, n in cont.items() if n >= minimo))

    def codificar(self, texto: str) -> list[int]:
        q = self.indice["?"]
        return [self.indice.get(c, q) for c in texto]

    def decodificar(self, ids: list[int]) -> str:
        return "".join(self.vocab[i] for i in ids)

    def estado(self) -> dict[str, Any]:
        return dict(tipo=self.tipo, vocab=self.vocab)


class TokenizadorBPE:
    """Byte-pair encoding sobre caracteres (Sennrich et al., 2016): começa nos caracteres e funde,
    um a um, o par vizinho mais frequente. Decodificar é concatenar: a ida e volta é exata."""
    tipo = "bpe"

    def __init__(self, base: list[str], fusoes: list[tuple[str, str]]):
        self.base = list(base) if "?" in base else sorted(set(base) | {"?"})
        self.fusoes = [tuple(f) for f in fusoes]
        self.vocab = self.base + [a + b for a, b in self.fusoes]
        self.indice = {c: i for i, c in enumerate(self.vocab)}
        self.posto = {f: i for i, f in enumerate(self.fusoes)}

    @classmethod
    def treinar(cls, texto: str, fusoes: int) -> "TokenizadorBPE":
        base = sorted(set(texto))
        palavras = collections.Counter(re.findall(r" ?[^ ]+| +", texto))
        seqs = {w: list(w) for w in palavras}
        feitas = []
        for _ in range(fusoes):
            pares = collections.Counter()
            for w, n in palavras.items():
                s = seqs[w]
                for a, b in zip(s, s[1:]):
                    pares[(a, b)] += n
            if not pares:
                break
            (a, b), cont = max(pares.items(), key=lambda kv: (kv[1], kv[0]))
            if cont < 2:
                break
            feitas.append((a, b))
            for w in palavras:
                s, out, i = seqs[w], [], 0
                while i < len(s):
                    if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                        out.append(a + b)
                        i += 2
                    else:
                        out.append(s[i])
                        i += 1
                seqs[w] = out
        return cls(base, feitas)

    def _palavra(self, w: str) -> list[str]:
        s = [c if c in self.indice else "?" for c in w]
        while len(s) > 1:
            melhor = min(((self.posto.get((a, b), 10 ** 9), i) for i, (a, b) in enumerate(zip(s, s[1:]))))
            if melhor[0] == 10 ** 9:
                break
            i = melhor[1]
            s = s[:i] + [s[i] + s[i + 1]] + s[i + 2:]
        return s

    def codificar(self, texto: str) -> list[int]:
        return [self.indice[p] for w in re.findall(r" ?[^ ]+| +", texto) for p in self._palavra(w)]

    def decodificar(self, ids: list[int]) -> str:
        return "".join(self.vocab[i] for i in ids)

    def estado(self) -> dict[str, Any]:
        return dict(tipo=self.tipo, base=self.base, fusoes=[list(f) for f in self.fusoes])


def tokenizador_de_estado(e: dict[str, Any]):
    if e["tipo"] == "caracteres":
        return TokenizadorCaracteres(e["vocab"])
    if e["tipo"] == "bpe":
        return TokenizadorBPE(e["base"], e["fusoes"])
    raise ValueError("Tokenizador desconhecido")


class Corpus:
    """Fontes de texto offline. O dicionário (WordNet 3.0, en; OpenWordNet-PT, pt) é lido dos arquivos
    da série SYNTHAI (`dados/`); sem eles, usa o mini-léxico embutido. Qualquer .txt (UTF-8) também serve."""
    LICENCAS = {
        "wordnet": "WordNet 3.0 Copyright 2006 by Princeton University. All rights reserved. "
                   "(licença de uso, cópia e distribuição sem taxa, com este aviso; ver dados/WORDNET_LICENSE.txt)",
        "ownpt": "OpenWordNet-PT, Creative Commons Attribution 4.0 (CC BY 4.0); ver dados/OWNPT_LICENSE.txt",
        "embutido": "mini-léxico manual do NEXUS-RAPHAEL (CC0, redação original de teste)",
    }

    @staticmethod
    def _procurar(nome: str, pasta: str | None = None) -> Path | None:
        if pasta:
            p = Path(pasta) / nome
            return p if p.exists() else None
        for base in (Path.cwd(), Path(__file__).resolve().parent, Path(__file__).resolve().parent.parent,
                     Path(__file__).resolve().parents[2] if len(Path(__file__).resolve().parents) > 2 else Path.cwd()):
            p = base / "dados" / nome
            if p.exists():
                return p
        return None

    @staticmethod
    def glosas(fonte: str = "wordnet", limite: int | None = None, pasta: str | None = None) -> tuple[str, str]:
        """(texto, licença). Uma glosa por linha, na ordem do arquivo."""
        if fonte == "embutido":
            return "\n".join(d for _, _, d in lexico_embutido()) + "\n", Corpus.LICENCAS["embutido"]
        arquivo, coluna = {"wordnet": ("wordnet30_sinsets.tsv.gz", 4), "ownpt": ("ownpt_sinsets.tsv.gz", 2)}[fonte]
        p = Corpus._procurar(arquivo, pasta)
        if p is None:
            return Corpus.glosas("embutido", limite)
        linhas = []
        with gzip.open(p, "rt", encoding="utf-8") as f:
            for linha in f:
                partes = linha.rstrip("\n").split("\t")
                if len(partes) > coluna and partes[coluna].strip():
                    linhas.append(partes[coluna].strip())
                    if limite and len(linhas) >= limite:
                        break
        return "\n".join(linhas) + "\n", Corpus.LICENCAS[fonte]

    @staticmethod
    def arquivo(caminho: str) -> tuple[str, str]:
        return Path(caminho).read_text(encoding="utf-8"), f"arquivo do usuário: {caminho}"

    @staticmethod
    def dividir(texto: str, frac_teste: float = 0.1) -> tuple[str, str]:
        """Separa por LINHAS (o teste nunca vê uma glosa do treino); semente fixa."""
        linhas = texto.splitlines()
        r = random.Random(7)
        idx = list(range(len(linhas)))
        r.shuffle(idx)
        corte = max(1, int(len(idx) * frac_teste))
        teste = set(idx[:corte])
        tr = "\n".join(linhas[i] for i in range(len(linhas)) if i not in teste) + "\n"
        te = "\n".join(linhas[i] for i in sorted(teste)) + "\n"
        return tr, te


class Amostragem:
    """Decodificação: gulosa, temperatura, top-k, top-p (núcleo) e penalidade de repetição."""

    @staticmethod
    def filtrar(probs: list[float], temperatura: float = 1.0, top_k: int = 0, top_p: float = 1.0,
                penalidade: float = 1.0, recentes: list[int] = ()) -> list[float]:
        logp = [math.log(max(p, 1e-300)) for p in probs]
        if penalidade != 1.0:
            for i in set(recentes):
                logp[i] -= math.log(penalidade)
        if temperatura <= 0:
            m = max(range(len(logp)), key=lambda i: (logp[i], -i))
            return [1.0 if i == m else 0.0 for i in range(len(logp))]
        q = _softmax([v / temperatura for v in logp])
        ordem = sorted(range(len(q)), key=lambda i: (-q[i], i))
        manter = set(ordem[:top_k]) if top_k > 0 else set(ordem)
        if top_p < 1.0:
            acum, nucleo = 0.0, set()
            for i in ordem:
                nucleo.add(i)
                acum += q[i]
                if acum >= top_p - 1e-12:   # o menor conjunto com massa ≥ p, tolerando o arredondamento
                    break
            manter &= nucleo
        s = sum(q[i] for i in manter)
        return [q[i] / s if i in manter else 0.0 for i in range(len(q))]

    @staticmethod
    def sortear(dist: list[float], rng: random.Random) -> int:
        x, acum = rng.random(), 0.0
        ultimo = 0
        for i, p in enumerate(dist):
            if p > 0:
                ultimo = i
                acum += p
                if x < acum:
                    return i
        return ultimo


_MODELO_TRABALHADOR: list = []


def _trabalhador_iniciar(cfg: ConfigGPT) -> None:
    _MODELO_TRABALHADOR[:] = [ModeloGPT(cfg)]


def _trabalhador_gradiente(args) -> tuple[dict, float]:
    pesos, janelas = args
    m = _MODELO_TRABALHADOR[0]
    m.p = pesos
    G = m.zeros()
    tot = sum(m.gradiente(x, y, G) for x, y in janelas)
    return G, tot


class SynthaiGPT:
    """A fachada do produto: tokenizador + modelo + otimizador + avaliação + pesos em arquivo."""

    def __init__(self, tokenizador, cfg: ConfigGPT | None = None, **kw):
        self.tok = tokenizador
        self.cfg = cfg or ConfigGPT(vocab=len(tokenizador.vocab), **kw)
        if self.cfg.vocab != len(tokenizador.vocab):
            raise ValueError("vocab da configuração difere do tokenizador")
        self.modelo = ModeloGPT(self.cfg)
        self.historico: list[dict[str, float]] = []

    # ---------------- treino ----------------
    def treinar(self, texto: str, passos: int, lote: int = 8, lr: float = 3e-3, aquecimento: int = 100,
                semente: int = 1, validacao: str | None = None, a_cada: int = 0, relatorio=None,
                processos: int = 1, checkpoint: str | None = None, ate: int | None = None) -> list[float]:
        """Pré-treino por janelas sorteadas (semente fixa). Com `processos` > 1, o lote é repartido entre
        processos de trabalho (multiprocessing local, sem rede); o resultado é o MESMO gradiente médio.
        Com `checkpoint`, grava pesos e estado do otimizador a cada `a_cada` passos e retoma de lá; `ate` interrompe
        no passo dado sem mudar o plano (a taxa continua a do plano de `passos`)."""
        ids = self.tok.codificar(texto)
        T = self.cfg.contexto
        if len(ids) < T + 2:
            raise ValueError("Texto curto demais para o contexto")
        opt = getattr(self, "_otimizador", None) or AdamW(self.modelo, lr=lr)
        self._otimizador = opt
        feito = getattr(self, "_passos_feitos", 0)
        rng = random.Random(semente)
        for _ in range(feito * lote):            # retoma a mesma sequência de janelas
            rng.randrange(0, len(ids) - T - 1)
        piscina = None
        if processos > 1:
            import multiprocessing as mp
            piscina = mp.get_context("fork").Pool(processos, initializer=_trabalhador_iniciar, initargs=(self.cfg,))
        perdas = []
        inicio = time.perf_counter()
        try:
            for passo in range(feito, min(passos, ate) if ate else passos):
                janelas = []
                for _ in range(lote):
                    i = rng.randrange(0, len(ids) - T - 1)
                    janelas.append((ids[i:i + T], ids[i + 1:i + T + 1]))
                if piscina is None:
                    G = self.modelo.zeros()
                    tot = sum(self.modelo.gradiente(x, y, G) for x, y in janelas)
                else:
                    pedacos = [janelas[k::processos] for k in range(processos)]
                    res = piscina.map(_trabalhador_gradiente, [(self.modelo.p, p_) for p_ in pedacos if p_])
                    G, tot = res[0][0], res[0][1]
                    for Gk, tk in res[1:]:
                        tot += tk
                        for nome in G:
                            _somar_em(G[nome], Gk[nome])
                for m in G.values():
                    for linha in m:
                        for j in range(len(linha)):
                            linha[j] /= lote
                taxa = AdamW.taxa(passo, passos, lr, aquecimento)
                norma = opt.passo(G, taxa)
                perdas.append(tot / lote)
                self._passos_feitos = passo + 1
                if a_cada and (passo + 1) % a_cada == 0:
                    linha = dict(passo=passo + 1, perda_treino=statistics.fmean(perdas[-a_cada:]), taxa=taxa,
                                 norma=norma, segundos=time.perf_counter() - inicio)
                    if validacao:
                        linha["bpc_validacao"] = self.bits_por_caractere(validacao, janelas=40)
                    self.historico.append(linha)
                    if checkpoint:
                        self.salvar(checkpoint, dict(passos_feitos=passo + 1, otimizador=dict(
                            t=opt.t, m=opt.m, v=opt.v), plano=dict(passos=passos, lote=lote, lr=lr,
                                                                    aquecimento=aquecimento, semente=semente)))
                    if relatorio:
                        relatorio(linha)
        finally:
            if piscina is not None:
                piscina.close()
                piscina.join()
        return perdas

    def retomar_otimizador(self) -> None:
        """Depois de carregar(), recria o AdamW com o estado gravado no checkpoint (se houver)."""
        meta = getattr(self, "metadados", {}) or {}
        o = meta.get("otimizador")
        if o:
            opt = AdamW(self.modelo, lr=meta.get("plano", {}).get("lr", 3e-3))
            opt.t, opt.m, opt.v = o["t"], o["m"], o["v"]
            self._otimizador = opt
            self._passos_feitos = meta.get("passos_feitos", 0)

    # ---------------- avaliação ----------------
    def bits_por_caractere(self, texto: str, janelas: int | None = None) -> float:
        """Bits por CARACTERE (não por ficha: comparável entre tokenizadores e com o n-grama). Janelas
        consecutivas de T fichas; cada ficha é prevista só pelo que vem antes dela na janela."""
        ids = self.tok.codificar(texto)
        T = self.cfg.contexto
        nats, chars = 0.0, 0
        inicios = list(range(0, len(ids) - T - 1, T))
        if janelas is not None and len(inicios) > janelas:
            passo = len(inicios) / janelas
            inicios = [inicios[int(i * passo)] for i in range(janelas)]
        for i in inicios:
            x, y = ids[i:i + T], ids[i + 1:i + T + 1]
            nats += self.modelo.perda(x, y) * len(x)
            chars += len(self.tok.decodificar(y))
        return nats / max(1, chars) / math.log(2)

    def comparar_com_ngrama(self, treino: str, teste: str, ordem: int = 3, janelas: int = 60) -> dict[str, float]:
        """A linha de base honesta: um n-grama de caracteres (Witten-Bell) treinado no MESMO texto."""
        ng = ModeloCaracteres(ordem).treinar(treino)
        # o mesmo recorte de janelas para os dois
        ids = self.tok.codificar(teste)
        T = self.cfg.contexto
        inicios = list(range(0, len(ids) - T - 1, T))
        if len(inicios) > janelas:
            p = len(inicios) / janelas
            inicios = [inicios[int(i * p)] for i in range(janelas)]
        trecho = "".join(self.tok.decodificar(ids[i:i + T + 1]) for i in inicios)
        return dict(gpt_bpc=self.bits_por_caractere(teste, janelas), ngrama_bpc=ng.bits_por_caractere(trecho),
                    uniforme_bpc=math.log2(len(set(treino)) + 1), ordem_ngrama=ordem)

    # ---------------- geração ----------------
    def gerar(self, inicio: str, n: int = 200, temperatura: float = 0.8, top_k: int = 0, top_p: float = 0.95,
              penalidade: float = 1.0, semente: int = 0, parar_em: str | None = "\n") -> str:
        rng = random.Random(semente)
        ids = self.tok.codificar(inicio) or [0]
        saida = []
        for _ in range(n):
            janela = ids[-self.cfg.contexto:]
            probs, _ = self.modelo.adiante(janela, guardar=False)
            dist = Amostragem.filtrar(probs[-1], temperatura, top_k, top_p, penalidade, janela[-16:])
            prox = Amostragem.sortear(dist, rng)
            ids.append(prox)
            pedaco = self.tok.decodificar([prox])
            saida.append(pedaco)
            if parar_em and parar_em in pedaco:
                break
        return inicio + "".join(saida)

    def proximo(self, contexto: str, k: int = 5) -> list[tuple[str, float]]:
        """As k fichas mais prováveis depois do contexto, com a probabilidade."""
        ids = self.tok.codificar(contexto)[-self.cfg.contexto:] or [0]
        probs, _ = self.modelo.adiante(ids, guardar=False)
        ordem = sorted(range(len(probs[-1])), key=lambda i: -probs[-1][i])[:k]
        return [(self.tok.vocab[i], probs[-1][i]) for i in ordem]

    # ---------------- pesos ----------------
    def salvar(self, caminho: str, metadados: dict | None = None) -> str:
        corpo = dict(formato="synthai-gpt", versao=VERSAO_GPT, config=asdict(self.cfg),
                     tokenizador=self.tok.estado(), pesos=self.modelo.p, historico=self.historico,
                     metadados=metadados or {})
        texto = json.dumps(corpo, ensure_ascii=False, separators=(",", ":"))
        resumo = hashlib.sha256(texto.encode("utf-8")).hexdigest()
        Path(caminho).write_text(json.dumps(dict(sha256=resumo, conteudo=corpo), ensure_ascii=False,
                                            separators=(",", ":")), encoding="utf-8")
        return resumo

    @classmethod
    def carregar(cls, caminho: str) -> "SynthaiGPT":
        """Lê só JSON (nunca pickle: carregar pesos não executa código) e confere o SHA-256."""
        bruto = json.loads(Path(caminho).read_text(encoding="utf-8"))
        corpo = bruto["conteudo"]
        texto = json.dumps(corpo, ensure_ascii=False, separators=(",", ":"))
        if hashlib.sha256(texto.encode("utf-8")).hexdigest() != bruto["sha256"]:
            raise ValueError("Arquivo de pesos corrompido (SHA-256 não confere)")
        if corpo.get("formato") != "synthai-gpt":
            raise ValueError("Formato desconhecido")
        tok = tokenizador_de_estado(corpo["tokenizador"])
        obj = cls(tok, ConfigGPT(**corpo["config"]))
        esperado = obj.modelo.p
        for k, m in corpo["pesos"].items():
            if k not in esperado or len(m) != len(esperado[k]) or len(m[0]) != len(esperado[k][0]):
                raise ValueError(f"Peso incompatível: {k}")
        obj.modelo.p = {k: [list(map(float, l)) for l in m] for k, m in corpo["pesos"].items()}
        obj.historico = corpo.get("historico", [])
        obj.metadados = corpo.get("metadados", {})
        return obj

    def ficha(self) -> dict[str, Any]:
        return dict(produto="SYNTHAI-GPT", versao=VERSAO_GPT, arquitetura="transformer decodificador (forma de GPT), pré-LayerNorm",
                    parametros=self.modelo.contar(), parametros_formula=self.cfg.parametros(), config=asdict(self.cfg),
                    tokenizador=self.tok.tipo, vocabulario=len(self.tok.vocab))
