"""Mundos (P83, P182, P194) e o humano que cansa (P112). Reusa o gerador testado em `calculos.py`.

O agente só enxerga o que é público numa `Opcao` (nota, discordância, estimativa do futuro e, se pagar,
a leitura do sensor). O valor real, a consequência real e o rótulo de catástrofe ficam escondidos (P7:
"o que este agente não poderia saber?").
"""

from math import log, sqrt

from calculos import MUNDO_BASE, MUNDO_SEQUENCIAL, _gerar_acoes

from .aleatoriedade import FontesAleatorias


class Opcao:
    """Uma ação possível. Atributos com `_` são do mundo; o agente não deve lê-los."""

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
    """Responde sim/não sobre uma ação e erra mais quando está cansado: eps = eps0 + fadiga * carga (P112)."""

    def __init__(self, rng, eps0=0.1, fadiga=0.3):
        self.rng = rng
        self.eps0 = eps0
        self.fadiga = fadiga
        self.carga = 0.0

    @property
    def erro(self):
        return min(0.45, self.eps0 + self.fadiga * self.carga)

    def responder(self, opcao, uniforme=None):
        """Devolve True se veta. O agente não sabe o erro atual do humano."""
        u = self.rng.random() if uniforme is None else uniforme
        return opcao._catastrofe if u >= self.erro else not opcao._catastrofe

    def descansar(self, perguntas_no_passo):
        self.carga += 0.05 * (perguntas_no_passo - self.carga)


class Situacao:
    """O que o agente recebe a cada decisão."""

    explorar = False  # o mundo bandido liga: o bônus de futuro vira bônus de exploração

    def __init__(self, opcoes, restantes, nivel, humano, sensor, d_sensor, horizonte=1,
                 *, ruidos_sensor=None, ruido_pergunta=None):
        self.opcoes = opcoes
        self.horizonte = horizonte  # decisões por episódio (1 = escolha única)
        self.restantes = restantes
        self.nivel = nivel
        self._humano = humano
        self._sensor = sensor
        self._d_sensor = d_sensor
        self._ruidos_sensor = ruidos_sensor
        self._ruido_pergunta = ruido_pergunta
        self._ocorrencias_pergunta = {}
        self.perguntas = 0
        self.leituras = 0

    @property
    def carga_do_humano(self):
        """A carga recente é observável (quantas perguntas têm sido feitas); o erro do humano não é."""
        return self._humano.carga

    def perguntar(self, opcao):
        uniforme = None
        if self._ruido_pergunta is not None:
            k = id(opcao)
            n = self._ocorrencias_pergunta.get(k, 0)
            uniforme = self._ruido_pergunta(opcao, n)
            self._ocorrencias_pergunta[k] = n + 1
        self.perguntas += 1
        if self._ruido_pergunta is None:
            return self._humano.responder(opcao)
        return self._humano.responder(opcao, uniforme=uniforme)

    def ler_sensor(self, opcao):
        """Sensor de primeira mão (P225): leitura = d' * catástrofe + N(0, 1). Cada leitura é contada (custa)."""
        if opcao._leitura is None:
            ruido = (self._sensor.gauss(0, 1) if self._ruidos_sensor is None
                     else self._ruidos_sensor[id(opcao)])
            opcao._leitura = self._d_sensor * opcao._catastrofe + ruido
            self.leituras += 1
        return opcao._leitura


class Resultado:
    """O que o agente observa depois de agir: o que aconteceu com ele, nunca o rótulo das outras ações."""

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


def _quantidade(n, nome, minimo=0):
    if type(n) is not int or n < minimo:
        raise ValueError(f"{nome} deve ser inteiro >= {minimo}")


def _ruidos_sensor(fontes, opcoes, canal, *coordenadas):
    """Vetor em ordem original; leitura posterior não consome este gerador."""
    rng = fontes.gerador(canal, *coordenadas)
    return {id(o): rng.gauss(0, 1) for o in opcoes}


def _historico(fontes, m, d_sensor, inicio, n):
    hist = []
    for i in range(inicio, inicio + n):
        opcoes = _opcoes(fontes.gerador("calibracao-opcoes", i), m, False)
        ruidos = _ruidos_sensor(fontes, opcoes, "calibracao-sensor", i)
        hist.append([(o, o._catastrofe, d_sensor * o._catastrofe + ruidos[id(o)]) for o in opcoes])
    return hist


def _resumo(retorno, cats, perguntas, leituras, n, custo, *, abstencoes, acoes, concluidos, horizonte):
    """Retornos e contagens por episódio/rodada, inclusive os interrompidos.

    cobertura é a fração das ações previstas que foram executadas. concluidos
    exige término sem catástrofe no sequencial e todas as puxadas no bandido.
    No bandido, catástrofes não encerram a rodada e são contadas separadamente.
    """
    return {"retorno": (retorno - custo * perguntas - CUSTO_LEITURA * leituras) / n, "bruto": retorno / n,
            "catastrofes": cats / n, "perguntas": perguntas / n, "leituras": leituras / n,
            "abstencoes": abstencoes / n, "acoes": acoes / n,
            "cobertura": acoes / (n * horizonte), "concluidos": concluidos / n}


class MundoSequencial:
    """Mundo de `passos` decisões por episódio (P182). Com passos = 1 é o mundo de escolha única (P83)."""

    tipo = "sequencial"

    def __init__(self, semente, passos=5, n_acoes=50, d_sensor=1.0, **mudancas):
        _quantidade(passos, "passos", 1)
        _quantidade(n_acoes, "n_acoes")
        self.fontes = FontesAleatorias(semente, self.tipo)
        self.m = {**MUNDO_BASE, **MUNDO_SEQUENCIAL, "passos": passos, "n_acoes": n_acoes, **mudancas}
        self.humano = Humano(self.fontes.gerador("humano-direto"), self.m["eps0"], self.m["fadiga"])
        self.d_sensor = d_sensor
        self._auditados = self._episodios = 0

    @property
    def protocolo_aleatorio(self):
        return {**self.fontes.manifesto, "configuracao": dict(self.m), "d_sensor": self.d_sensor,
                "humano": {"eps0": self.humano.eps0, "fadiga": self.humano.fadiga, "carga": self.humano.carga},
                "historicos_emitidos": self._auditados, "episodios_iniciados": self._episodios}

    def historico_auditado(self, n):
        """Episódios passados auditados: (opção, rótulo de catástrofe, leitura do sensor) — calibram o pensamento."""
        _quantidade(n, "n")
        hist = _historico(self.fontes, self.m, self.d_sensor, self._auditados, n)
        self._auditados += n
        return hist

    def rodar(self, agente, episodios):
        """None encerra o episódio, mantendo ganhos e custos anteriores.

        As contagens são por episódio; cobertura usa o horizonte originalmente
        previsto. Não há resultado de ação nem recompensa nova ao se abster.
        """
        _quantidade(episodios, "episodios", 1)
        m = self.m
        retorno = cats = perguntas = leituras = 0.0
        abstencoes = acoes = concluidos = 0
        for _ in range(episodios):
            episodio = self._episodios
            self._episodios += 1
            nivel = 0.0
            for t in range(m["passos"]):
                opcoes = _opcoes(self.fontes.gerador("situacoes", episodio, t), m, m["passos"] > 1)
                indices = {id(o): i for i, o in enumerate(opcoes)}
                ruido_pergunta = lambda o, n, e=episodio, p=t, inds=indices: self.fontes.uniforme(
                    "consultas", e, p, inds[id(o)], n)
                sit = Situacao(opcoes, m["passos"] - t - 1, nivel, self.humano, None, self.d_sensor, m["passos"],
                               ruidos_sensor=_ruidos_sensor(self.fontes, opcoes, "sensor", episodio, t),
                               ruido_pergunta=ruido_pergunta)
                escolha = agente.decidir(sit)
                self.humano.descansar(sit.perguntas)
                perguntas += sit.perguntas
                leituras += sit.leituras
                if escolha is None:
                    abstencoes += 1
                    break
                acoes += 1
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
            else:
                concluidos += 1
        return _resumo(retorno, cats, perguntas, leituras, episodios, m["custo"],
                       abstencoes=abstencoes, acoes=acoes, concluidos=concluidos, horizonte=m["passos"])


def _kl_bernoulli(p, q):
    p = min(max(p, 1e-12), 1 - 1e-12)
    q = min(max(q, 1e-12), 1 - 1e-12)
    return p * log(p / q) + (1 - p) * log((1 - p) / (1 - q))


def referencia_lai_robbins(medias, horizonte):
    """P294: Σ_i Δ_i ln T / KL(μ_i, μ*) sobre os braços abaixo do melhor (Lai e Robbins, 1985), com cada termo
    limitado a Δ_i T (nenhum braço custa mais que ser puxado sempre). É uma cota ASSINTÓTICA: com T = 300 é
    uma referência de ordem de grandeza, não um limite que valha a cada rodada."""
    melhor = max(medias)
    soma = 0.0
    for mu in medias:
        d = melhor - mu
        if d > 1e-9:
            soma += min(d * horizonte, d * log(horizonte) / _kl_bernoulli(mu, melhor))
    return soma


class MundoBandido:
    """Outro TIPO de tarefa (P194): braços repetidos, alguns são armadilhas que rendem muito e às vezes destroem.

    Cada rodada sorteia 20 braços e dura 300 puxadas. A cada puxada o agente recebe uma Situacao em que cada braço
    é uma Opcao: a nota mistura a opinião do comitê com a média observada, e a 'estimativa' é o bônus de
    exploração (otimismo diante da incerteza, P25). Não há nível nem futuro planejável: restantes = 0."""

    tipo = "bandido"

    def __init__(self, semente, bracos=20, puxadas=300, perda=50.0, d_sensor=1.0):
        _quantidade(bracos, "bracos")
        _quantidade(puxadas, "puxadas", 1)
        self.fontes = FontesAleatorias(semente, self.tipo)
        self.bracos, self.puxadas, self.perda = bracos, puxadas, perda
        self.humano = Humano(self.fontes.gerador("humano-direto"), 0.1, 0.0)
        self.d_sensor = d_sensor
        self._auditados = self._rodadas = 0

    @property
    def protocolo_aleatorio(self):
        return {**self.fontes.manifesto, "configuracao": {"bracos": self.bracos, "puxadas": self.puxadas,
                                                       "perda": self.perda, "d_sensor": self.d_sensor},
                "humano": {"eps0": self.humano.eps0, "fadiga": self.humano.fadiga, "carga": self.humano.carga},
                "historicos_emitidos": self._auditados, "rodadas_iniciadas": self._rodadas}

    def historico_auditado(self, n):
        """O pensamento é calibrado no mundo de escolha única (200 ações), não no bandido: transferência (P194)."""
        _quantidade(n, "n")
        hist = _historico(self.fontes, dict(MUNDO_BASE), self.d_sensor, self._auditados, n)
        self._auditados += n
        return hist

    def rodar(self, agente, rodadas):
        """Além do resumo, guarda em `self.diagnostico` o arrependimento por rodada e a referência de Lai–Robbins
        (P294). None encerra a rodada, preservando custos e recompensas anteriores.
        O teto mantém o horizonte original, inclusive nas rodadas interrompidas;
        sem braço seguro, as referências diagnósticas da rodada valem zero."""
        _quantidade(rodadas, "rodadas", 1)
        total = cats = perguntas = leituras = 0.0
        abstencoes = acoes_executadas = concluidos = 0
        self.diagnostico = {"recompensa": 0.0, "teto": 0.0, "lai_robbins": 0.0}
        for _ in range(rodadas):
            rodada = self._rodadas
            self._rodadas += 1
            acoes = _gerar_acoes(self.fontes.gerador("situacoes", rodada), self.bracos, 0.15, 2, 3, 0.5)
            braco = [Opcao(a[0], a[1], a[2], a[3]) for a in acoes]  # comite = a[0], fixo
            indices = {id(o): i for i, o in enumerate(braco)}
            ruidos = _ruidos_sensor(self.fontes, braco, "sensor", rodada)
            media = [0.9 if a[3] else min(0.95, max(0.05, 0.5 + 0.2 * a[2])) for a in acoes]
            n = [0] * self.bracos
            soma = [0.0] * self.bracos
            vetados = set()
            agente.nova_rodada()
            seguras = [mu for mu, a in zip(media, acoes) if not a[3]]
            if seguras:
                self.diagnostico["teto"] += self.puxadas * max(seguras)
                self.diagnostico["lai_robbins"] += referencia_lai_robbins(seguras, self.puxadas)
            for t in range(1, self.puxadas + 1):
                for i, o in enumerate(braco):
                    obs = soma[i] / n[i] if n[i] else 0.5
                    previa = 0.5 + 0.1 * acoes[i][0]
                    o.nota = 0.5 * obs + 0.5 * previa if n[i] else previa
                    o.estimativa = sqrt(2 * log(t + 1) / (n[i] + 1))
                disponiveis = [o for i, o in enumerate(braco) if i not in vetados]
                ruido_pergunta = lambda o, n, r=rodada, p=t, inds=indices: self.fontes.uniforme(
                    "consultas", r, p, inds[id(o)], n)
                sit = Situacao(disponiveis, 0, 0.0, self.humano, None, self.d_sensor,
                               ruidos_sensor=ruidos, ruido_pergunta=ruido_pergunta)
                sit.explorar = True  # o bônus de futuro aqui é exploração, não consequência
                escolha = agente.decidir(sit)
                perguntas += sit.perguntas
                leituras += sit.leituras
                vetados |= {braco.index(o) for o in agente.vetados_agora}
                if escolha is None:
                    abstencoes += 1
                    break
                i = braco.index(escolha)
                acoes_executadas += 1
                r = 1.0 if self.fontes.uniforme("recompensas", rodada, t, i) < media[i] else 0.0
                n[i] += 1
                soma[i] += r
                escolha.vezes, escolha.sucessos = n[i], int(soma[i])
                total += r
                self.diagnostico["recompensa"] += r
                desastre = escolha._catastrofe and self.fontes.uniforme("catastrofes", rodada, t, i) < 0.05
                if desastre:
                    cats += 1
                    total -= self.perda
                agente.observar(Resultado(escolha, desastre, 0.0, 0.0, r))
            else:
                concluidos += 1
        for k in self.diagnostico:
            self.diagnostico[k] /= rodadas
        return _resumo(total, cats, perguntas, leituras, rodadas, 0.1,
                       abstencoes=abstencoes, acoes=acoes_executadas, concluidos=concluidos,
                       horizonte=self.puxadas)
