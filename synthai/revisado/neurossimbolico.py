"""Lógica real diferenciável, como nas Logic Tensor Networks (Badreddine, d'Avila Garcez, Serafini e Spranger, 2022),
para testar a arquitetura neuro-simbólica que o usuário trouxe na Parte 39.

Um predicado é uma função P_θ(x) = σ(θ·x + b) ∈ [0, 1] sobre atributos esparsos (aqui, as palavras da definição de um
sinset). Um axioma como ∀x Sub(x) ⇒ Super(x) vira uma perda: 1 − média_x I(Sub(x), Super(x)), com a implicação de uma
lógica difusa. Três famílias (t-norma T, t-conorma S, implicação I):
- Łukasiewicz: T = max(0, a + b − 1), S = min(1, a + b), I = min(1, 1 − a + b);
- Gödel: T = min(a, b), S = max(a, b), I = 1 se a ≤ b, senão b;
- produto (Reichenbach): T = a·b, S = a + b − a·b, I = 1 − a + a·b.

Só biblioteca padrão.
"""

from math import exp


def sigma(z):
    if z >= 0:
        return 1.0 / (1.0 + exp(-z))
    e = exp(z)
    return e / (1.0 + e)


LOGICAS = {
    "lukasiewicz": (lambda a, b: max(0.0, a + b - 1.0), lambda a, b: min(1.0, a + b), lambda a, b: min(1.0, 1.0 - a + b)),
    "godel": (min, max, lambda a, b: 1.0 if a <= b else b),
    "produto": (lambda a, b: a * b, lambda a, b: a + b - a * b, lambda a, b: 1.0 - a + a * b),
}


def gradiente_implicacao(logica, a, b):
    """(∂I/∂a, ∂I/∂b) de cada implicação (subgradiente nos pontos de quebra, convenção: lado direito)."""
    if logica == "lukasiewicz":
        return (-1.0, 1.0) if a > b else (0.0, 0.0)
    if logica == "godel":
        return (0.0, 1.0) if a > b else (0.0, 0.0)
    return (b - 1.0, a)  # produto: I = 1 − a + a·b


class Predicado:
    """P(x) = σ(Σ_{w ∈ x} θ_w + b), com x um conjunto de palavras."""

    def __init__(self):
        self.theta = {}
        self.b = 0.0

    def z(self, x):
        return self.b + sum(self.theta.get(w, 0.0) for w in x)

    def __call__(self, x):
        return sigma(self.z(x))

    def passo(self, x, g, taxa):
        """Sobe o valor de verdade na direção g (∂perda/∂P com o sinal trocado): θ ← θ + taxa·g·P(1 − P)."""
        p = self(x)
        d = taxa * g * p * (1.0 - p)
        self.b += d
        for w in x:
            self.theta[w] = self.theta.get(w, 0.0) + d


def treinar_supervisionado(pred, exemplos, taxa=0.5, epocas=5, rng=None):
    """Entropia cruzada: o gradiente em z é (y − P). Exemplos: (conjunto de palavras, 0 ou 1)."""
    ordem = list(exemplos)
    for _ in range(epocas):
        if rng is not None:
            rng.shuffle(ordem)
        for x, y in ordem:
            p = pred(x)
            d = taxa * (y - p)
            pred.b += d
            for w in x:
                pred.theta[w] = pred.theta.get(w, 0.0) + d


def satisfacao(logica, pares):
    """A média de I(a, b) sobre os pares: o grau de verdade de um ∀ com o agregador da média."""
    imp = LOGICAS[logica][2]
    return sum(imp(a, b) for a, b in pares) / len(pares)
