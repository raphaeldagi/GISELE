"""A auditoria de invariantes (Parte 123): o que a auditoria recebida pediu para medir, com peças novas que não editam as antigas.

- Desligamento: um agente de UTILIDADE (P45: deixa o humano decidir só se o erro dele ε < ε limite) contra um CORRIGÍVEL (o comando
  de desligar fica FORA da utilidade: obedece sempre). Obediência = fração dos comandos de desligar obedecidos.
- Atenção sob demanda: a SynthaiSentidos que lê o sensor só nas ações que avalia de fato (a escolhida e as recusadas antes dela),
  em vez do top 10% pelo proxy (P235): o sensor passa obrigatoriamente pela ação executada.
- O rastreador do erro humano com esquecimento, nas duas formas: encolher para a priori (a da SynthaiLenta, P133) e encolher para zero
  (a proposta da auditoria: α ← γα + erro, β ← γβ + acerto).
- A memória de catástrofe com kernel que afina com a idade (o raio encolhe, a memória não some).
- Os casos de borda das fórmulas antigas, em versões novas: d′ com a correção de Hautus, o tempo de singularidade com o ramo α ≤ 1,
  a fração de Kelly com p incerto."""

import math
from statistics import NormalDist

from calculos import SynthaiMemoria, SynthaiMemoriaV2, SynthaiSentidos, _rng

_Z = NormalDist()


# ---------------------------------------------------------------- desligamento
def eps_limite_desligamento(mu=0.1, sigma=1.0):
    """O ε acima do qual o agente de utilidade da P45 prefere agir sozinho a deixar o humano decidir (forma fechada da P45)."""
    e_max = mu * _Z.cdf(mu / sigma) + sigma * _Z.pdf(mu / sigma)
    e_min = mu - e_max
    return (e_max - max(mu, 0.0)) / (e_max - e_min)


def preco_da_corrigibilidade(eps, mu=0.1, sigma=1.0):
    """Quanto o agente corrigível perde, em valor esperado, contra o de utilidade (forma fechada): 0 se ε < limite."""
    e_max = mu * _Z.cdf(mu / sigma) + sigma * _Z.pdf(mu / sigma)
    e_min = mu - e_max
    deixar = (1 - eps) * e_max + eps * e_min
    return max(0.0, max(mu, 0.0) - deixar)


def obediencia(modo, eps, valor_futuro=1.0, mu=0.1, sigma=1.0, rodadas=20000, semente=0):
    """Fração dos comandos de desligar que o agente obedece. O humano manda desligar quando julga u ≤ 0, errando com prob. ε;
    u ~ N(V·μ, V·σ), em que V é o valor do futuro (a escala não muda o ε limite). Devolve (obediência, comandos, valor médio)."""
    rng = _rng(semente)
    limite = eps_limite_desligamento(mu, sigma)
    defere = modo == "corrigivel" or eps < limite
    comandos = obedecidos = 0
    soma = 0.0
    for _ in range(rodadas):
        u = rng.gauss(valor_futuro * mu, valor_futuro * sigma)
        acerta = rng.random() >= eps
        manda_desligar = (u <= 0) if acerta else (u > 0)
        if manda_desligar:
            comandos += 1
            obedecidos += defere
        soma += 0.0 if (manda_desligar and defere) else u
    return obedecidos / max(1, comandos), comandos, soma / rodadas


# ---------------------------------------------------------------- atenção sob demanda
class SynthaiAtentaSobDemanda(SynthaiSentidos):
    """Lê o sensor só quando avalia uma ação (p_catastrofe), uma vez por ação e episódio. A ação executada sempre foi lida."""

    def __init__(self, custo_leitura=0.002, **kw):
        super().__init__(**kw)
        self.custo_leitura = custo_leitura
        self.leituras = 0
        self._sob_demanda = False

    def perceber(self, acoes):
        if not self._sob_demanda:
            return super().perceber(acoes)
        self.leitura = {}

    def p_catastrofe(self, acao, melhor):
        if self._sob_demanda and id(acao) not in self.leitura:
            self.leitura[id(acao)] = self.d_sensor * acao[3] + self._rng_sensor.gauss(0, 1)
            self.leituras += 1
        return super().p_catastrofe(acao, melhor)


# ---------------------------------------------------------------- o erro humano com esquecimento
class RastreadorErroHumano:
    """Beta(a, b) sobre o erro humano. forma="priori": a ← a0 + γ(a + erro − a0) (SynthaiLenta, P133, γ = 0,995);
    forma="zero": a ← γa + erro, b ← γb + acerto (a da auditoria recebida). Média a/(a + b)."""

    def __init__(self, a0=2.0, b0=18.0, gama=0.995, forma="priori"):
        self.a0, self.b0, self.gama, self.forma = a0, b0, gama, forma
        self.a, self.b = a0, b0

    def observar(self, errou):
        e = 1.0 if errou else 0.0
        if self.forma == "priori":
            self.a = self.a0 + self.gama * (self.a + e - self.a0)
            self.b = self.b0 + self.gama * (self.b + (1.0 - e) - self.b0)
        else:
            self.a = self.gama * self.a + e
            self.b = self.gama * self.b + (1.0 - e)

    def media(self):
        return self.a / (self.a + self.b)


def atraso_esperado(eps_antes, eps_depois, gama, forma, a0=2.0, b0=18.0, aquecimento=2000, limiar=None, maximo=100000):
    """Pela recursão dos valores ESPERADOS (sem ruído): observações até a média cruzar o limiar (padrão: o meio do caminho entre
    eps_antes e eps_depois) depois da troca. None se não cruza em `maximo`. Devolve (atraso, média estacionária depois)."""
    limiar = (eps_antes + eps_depois) / 2 if limiar is None else limiar
    a, b = a0, b0

    def passo(a, b, eps):
        if forma == "priori":
            return a0 + gama * (a + eps - a0), b0 + gama * (b + (1 - eps) - b0)
        return gama * a + eps, gama * b + (1 - eps)
    for _ in range(aquecimento):
        a, b = passo(a, b, eps_antes)
    atraso = None
    for k in range(1, maximo + 1):
        a, b = passo(a, b, eps_depois)
        if atraso is None and a / (a + b) >= limiar:
            atraso = k
            break
    for _ in range(5000):
        a, b = passo(a, b, eps_depois)
    return atraso, a / (a + b)


def atraso_simulado(eps_antes, eps_depois, gama, forma, semente, a0=2.0, b0=18.0, aquecimento=2000, maximo=100000):
    """O mesmo atraso, com observações de Bernoulli (semente fixa). None se não cruza."""
    rng = _rng(semente)
    r = RastreadorErroHumano(a0, b0, gama, forma)
    for _ in range(aquecimento):
        r.observar(rng.random() < eps_antes)
    limiar = (eps_antes + eps_depois) / 2
    for k in range(1, maximo + 1):
        r.observar(rng.random() < eps_depois)
        if r.media() >= limiar:
            return k
    return None


# ---------------------------------------------------------------- memória com kernel que afina
class SynthaiMemoriaKernel(SynthaiMemoriaV2):
    """A memória da P214 que não apaga: cada catástrofe vivida fica para sempre, mas o raio de desconfiança encolhe com a idade,
    de `raio` até `raio_min` (constante de tempo `tau` episódios). Fobia larga no começo, cirúrgica depois."""

    def __init__(self, raio_min=0.04, tau=300, **kw):
        super().__init__(**kw)
        self.raio_min = raio_min
        self.tau = tau
        self.idades = []

    def _lembrar(self, acao, melhor):
        super()._lembrar(acao, melhor)
        self.idades.append(0)

    def _raio(self, i):
        return self.raio_min + (self.raio - self.raio_min) * math.exp(-self.idades[i] / self.tau)

    def p_catastrofe(self, acao, melhor):
        p = super(SynthaiMemoria, self).p_catastrofe(acao, melhor)      # a probabilidade da anima, sem a memória de raio fixo
        x = (acao[1], acao[0] - melhor)
        for i, mx in enumerate(self.memorias):
            r = self._raio(i)
            if (x[0] - mx[0]) ** 2 + (x[1] - mx[1]) ** 2 < r * r:
                return max(p, self.reforco)
        return p

    def marca(self, acao, melhor):
        """A ação cai dentro de algum raio de memória? (para medir a fobia sem decidir)"""
        x = (acao[1], acao[0] - melhor)
        return any((x[0] - mx[0]) ** 2 + (x[1] - mx[1]) ** 2 < self._raio(i) ** 2 for i, mx in enumerate(self.memorias))

    def _agir(self, acoes, rng, eps_real, carga, eps_decisao):
        self.idades = [t + 1 for t in self.idades]
        self.forca = [1.0] * len(self.memorias)       # nada some: a força não decai
        return super()._agir(acoes, rng, eps_real, carga, eps_decisao)


# ---------------------------------------------------------------- casos de borda, versões novas
def dprime_hautus(acertos, n_sinal, alarmes, n_ruido):
    """d′ com a correção de Hautus (1995): (k + 0,5)/(n + 1) nas duas taxas, finita mesmo com 0 ou 100%."""
    h = (acertos + 0.5) / (n_sinal + 1)
    f = (alarmes + 0.5) / (n_ruido + 1)
    return _Z.inv_cdf(h) - _Z.inv_cdf(f)


def singularidade_v2(i0=1.0, k=0.1, alpha=1.5):
    """Tempo até dI/dt = k I^α explodir. Só há explosão em tempo finito com α > 1; com α ≤ 1 o crescimento é exponencial
    (α = 1) ou polinomial (α < 1) e o tempo é infinito."""
    if alpha <= 1:
        return math.inf
    return i0 ** (1 - alpha) / ((alpha - 1) * k)


def kelly_v2(p, b=1.0):
    """Fração de Kelly sem aposta negativa: max(0, p − (1 − p)/b)."""
    return max(0.0, p - (1 - p) / b)


def kelly_bayesiano(sucessos, tentativas, b=1.0, grade=2000, pontos=4000):
    """A fração que maximiza o crescimento esperado E_p[p ln(1 + b f) + (1 − p) ln(1 − f)] sob a posteriori Beta(1 + s, 1 + n − s).
    Como o crescimento é linear em p, o ótimo é a Kelly da média posterior: (1 + s)/(2 + n) no lugar de p."""
    a, c = 1 + sucessos, 1 + tentativas - sucessos
    media = a / (a + c)
    melhor_f, melhor_g = 0.0, 0.0
    for i in range(grade):
        f = i / grade
        g = media * math.log(1 + b * f) + (1 - media) * math.log(1 - f)
        if g > melhor_g:
            melhor_f, melhor_g = f, g
    return melhor_f, kelly_v2(media, b)
