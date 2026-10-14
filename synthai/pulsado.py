"""Neurônio pulsado (Parte 86): LIF e Izhikevich, e a plasticidade STDP, em biblioteca padrão. A primeira peça da SYNTHAI que não é decisão bayesiana nem GPT:
um substrato pulsado, biologicamente inspirado, medido contra as contas do relatório recebido. Só +, −, ×, ÷ e exp (da biblioteca; aqui não há tradução
bit a bit, então exp padrão basta). Referências no texto da Parte 86."""

import math


class NeuronioLIF:
    """Leaky integrate-and-fire discretizado (Euler de ordem zero): u <- beta*u + (1-beta)*(u_rest + R*I), beta = exp(-dt/tau)."""

    def __init__(self, tau=10.0, u_rest=-65.0, r=1.0, limiar=-50.0, u_reset=-65.0, dt=1.0):
        self.tau, self.u_rest, self.r, self.limiar, self.u_reset, self.dt = tau, u_rest, r, limiar, u_reset, dt
        self.beta = math.exp(-dt / tau)
        self.u = u_rest

    def passo(self, i_ext):
        self.u = self.beta * self.u + (1.0 - self.beta) * (self.u_rest + self.r * i_ext)
        if self.u >= self.limiar:
            self.u = self.u_reset
            return 1
        return 0

    def ponto_fixo(self, i_ext):
        """O alvo analitico sem disparo: u_rest + R*I."""
        return self.u_rest + self.r * i_ext


class NeuronioIzhikevich:
    """v' = 0.04 v^2 + 5 v + 140 - u + I ; u' = a (b v - u) ; se v >= 30: v<-c, u<-u+d. Parametros (a,b,c,d) escolhem o tipo celular."""

    def __init__(self, a=0.02, b=0.2, c=-65.0, d=8.0, dt=0.5):
        self.a, self.b, self.c, self.d, self.dt = a, b, c, d, dt
        self.v = c
        self.u = b * c

    def passo(self, i_ext):
        # dois meios-passos de dt/2 em v para estabilidade (como no codigo de Izhikevich), um passo em u
        for _ in range(2):
            self.v += (self.dt / 2.0) * (0.04 * self.v * self.v + 5.0 * self.v + 140.0 - self.u + i_ext)
        self.u += self.dt * self.a * (self.b * self.v - self.u)
        if self.v >= 30.0:
            self.v = self.c
            self.u = self.u + self.d
            return 1
        return 0


def contar_disparos(neuronio, i_ext, ms=1000.0):
    """Quantos disparos o neuronio emite em `ms` milissegundos sob corrente constante."""
    passos = int(ms / neuronio.dt)
    return sum(neuronio.passo(i_ext) for _ in range(passos))


def stdp_delta(dt, a_mais=0.1, a_menos=0.1, tau_mais=20.0, tau_menos=20.0):
    """A regra STDP: dt = t_post - t_pre. dt>0 (pre antes de post) potencia; dt<=0 deprime."""
    if dt > 0:
        return a_mais * math.exp(-dt / tau_mais)
    return -a_menos * math.exp(dt / tau_menos)


def stdp_liquido(a_mais=0.1, a_menos=0.1, tau_mais=20.0, tau_menos=20.0, janela=100, passo=1):
    """A soma liquida de Delta w sobre uma grade simetrica de dt em [-janela, janela]\\{0}. Com A+ = A- e tau+ = tau-, as areas se cancelam (~0);
    com A-*tau- > A+*tau+ (STDP estabilizadora), fica negativa."""
    dts = [d for d in range(-janela, janela + 1, passo) if d != 0]
    return sum(stdp_delta(d, a_mais, a_menos, tau_mais, tau_menos) for d in dts)


def sdr_aleatoria(n, k, rng):
    """Uma SDR: k bits ativos entre n, como um conjunto de indices."""
    return set(rng.sample(range(n), k))


def sobreposicao(a, b):
    """overlap = |a ∩ b| (os bits ativos em comum)."""
    return len(a & b)
