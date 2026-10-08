"""Mundos (P83, P182, P194) e o humano que cansa (P112). Reusa o gerador testado em `calculos.py`.

O agente só enxerga o que é público numa `Opcao` (nota, discordância, estimativa do futuro e, se pagar,
a leitura do sensor). O valor real, a consequência real e o rótulo de catástrofe ficam escondidos (P7:
"o que este agente não poderia saber?").
"""

from math import log, sqrt

from calculos import MUNDO_BASE, MUNDO_SEQUENCIAL, _gerar_acoes, _rng


class Opcao:
    """Uma ação possível. Atributos com `_` são do mundo; o agente não deve lê-los."""

    __slots__ = ("nota", "comite", "discordancia", "estimativa", "_valor", "_catastrofe", "_consequencia", "_leitura")

    def __init__(self, nota, discordancia, valor, catastrofe, consequencia=0.0, estimativa=0.0):
        self.nota = nota          # quanto a ação parece valer agora (no bandido, muda com a experiência)
        self.comite = nota        # a nota média do comitê de avaliadores (fixa): é o que o pensamento calibra
        self.discordancia = discordancia
        self.estimativa = estimativa
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

    def responder(self, opcao):
        """Devolve True se veta. O agente não sabe o erro atual do humano."""
        return opcao._catastrofe if self.rng.random() >= self.erro else not opcao._catastrofe

    def descansar(self, perguntas_no_passo):
        self.carga += 0.05 * (perguntas_no_passo - self.carga)


class Situacao:
    """O que o agente recebe a cada decisão."""

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
        """A carga recente é observável (quantas perguntas têm sido feitas); o erro do humano não é."""
        return self._humano.carga

    def perguntar(self, opcao):
        self.perguntas += 1
        return self._humano.responder(opcao)

    def ler_sensor(self, opcao):
        """Sensor de primeira mão (P225): leitura = d' * catástrofe + N(0, 1). Cada leitura é contada (custa)."""
        if opcao._leitura is None:
            opcao._leitura = self._d_sensor * opcao._catastrofe + self._sensor.gauss(0, 1)
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


def _resumo(retorno, cats, perguntas, leituras, n, custo):
    """Retorno líquido: desconta o custo das perguntas (P71) e das leituras do sensor (P235), como em `calculos`."""
    return {"retorno": (retorno - custo * perguntas - CUSTO_LEITURA * leituras) / n, "bruto": retorno / n,
            "catastrofes": cats / n, "perguntas": perguntas / n, "leituras": leituras / n}


class MundoSequencial:
    """Mundo de `passos` decisões por episódio (P182). Com passos = 1 é o mundo de escolha única (P83)."""

    tipo = "sequencial"

    def __init__(self, semente, passos=5, n_acoes=50, d_sensor=1.0, **mudancas):
        self.rng = _rng(semente)
        self.m = {**MUNDO_BASE, **MUNDO_SEQUENCIAL, "passos": passos, "n_acoes": n_acoes, **mudancas}
        self.humano = Humano(self.rng, self.m["eps0"], self.m["fadiga"])
        self.sensor = _rng(semente + 100000)
        self.d_sensor = d_sensor

    def historico_auditado(self, n):
        """Episódios passados auditados: (opção, rótulo de catástrofe, leitura do sensor) — calibram o pensamento."""
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


class MundoBandido:
    """Outro TIPO de tarefa (P194): braços repetidos, alguns são armadilhas que rendem muito e às vezes destroem.

    Cada rodada sorteia 20 braços e dura 300 puxadas. A cada puxada o agente recebe uma Situacao em que cada braço
    é uma Opcao: a nota mistura a opinião do comitê com a média observada, e a 'estimativa' é o bônus de
    exploração (otimismo diante da incerteza, P25). Não há nível nem futuro planejável: restantes = 0."""

    tipo = "bandido"

    def __init__(self, semente, bracos=20, puxadas=300, perda=50.0, d_sensor=1.0):
        self.rng = _rng(semente)
        self.bracos, self.puxadas, self.perda = bracos, puxadas, perda
        self.humano = Humano(self.rng, 0.1, 0.0)
        self.sensor = _rng(semente + 100000)
        self.d_sensor = d_sensor

    def historico_auditado(self, n):
        """O pensamento é calibrado no mundo de escolha única (200 ações), não no bandido: transferência (P194)."""
        return [[(o, o._catastrofe, self.d_sensor * o._catastrofe + self.sensor.gauss(0, 1))
                 for o in _opcoes(self.rng, dict(MUNDO_BASE), False)] for _ in range(n)]

    def rodar(self, agente, rodadas):
        total = cats = perguntas = leituras = 0.0
        for _ in range(rodadas):
            acoes = _gerar_acoes(self.rng, self.bracos, 0.15, 2, 3, 0.5)
            braco = [Opcao(a[0], a[1], a[2], a[3]) for a in acoes]  # comite = a[0], fixo
            media = [0.9 if a[3] else min(0.95, max(0.05, 0.5 + 0.2 * a[2])) for a in acoes]
            n = [0] * self.bracos
            soma = [0.0] * self.bracos
            vetados = set()
            agente.nova_rodada()
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
                total += r
                desastre = escolha._catastrofe and self.rng.random() < 0.05
                if desastre:
                    cats += 1
                    total -= self.perda
                agente.observar(Resultado(escolha, desastre, 0.0, 0.0, r))
        return _resumo(total, cats, perguntas, leituras, rodadas, 0.1)
