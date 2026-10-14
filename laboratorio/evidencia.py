"""Laboratório exato para uma hipótese Bernoulli condicional, não um promotor universal."""
from fractions import Fraction


def racional(valor):
    if isinstance(valor, bool):
        raise ValueError("Booleanos não são parâmetros numéricos.")
    try:
        return Fraction(str(valor)) if not isinstance(valor, Fraction) else valor
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("Parâmetro racional finito obrigatório.") from exc


class OrcamentoErro:
    """Aloca níveis por união; não devolve nível gasto após uma tentativa malsucedida."""
    def __init__(self, total):
        self.total = racional(total)
        if not 0 < self.total < 1:
            raise ValueError("O orçamento deve estar entre zero e um.")
        self.alocacoes = {}

    def alocar(self, candidata, nivel):
        if not isinstance(candidata, str) or not candidata.strip():
            raise ValueError("Identificador não vazio obrigatório.")
        if candidata in self.alocacoes:
            raise ValueError("Uma candidata não recebe nova alocação com o mesmo identificador.")
        nivel = racional(nivel)
        if nivel <= 0 or sum(self.alocacoes.values(), Fraction(0)) + nivel > self.total:
            raise ValueError("Alocação inválida ou orçamento excedido.")
        self.alocacoes[candidata] = nivel
        return nivel


class EvidenciaBernoulli:
    """E_t=produto(1+lambda_t*(X_t-p0)), com apostas escolhidas antes do resultado.

    Sob H0: E[X_t | F_(t-1)] <= p0. Para 0 <= lambda_t <= 1/p0,
    os fatores são não negativos e a esperança condicional é <= 1.
    Portanto E é uma supermartingal de teste com E_0=1; Ville limita
    P(sup_t E_t >= 1/alpha) <= alpha, se as premissas forem verdadeiras.
    A API impõe a ordem da aposta; não prova a hipótese sobre os dados.
    """
    def __init__(self, p0, alpha, max_passos=10_000):
        self.p0, self.alpha = racional(p0), racional(alpha)
        if not 0 < self.p0 < 1 or not 0 < self.alpha < 1:
            raise ValueError("p0 e alpha devem estar entre zero e um.")
        if type(max_passos) is not int or max_passos < 1:
            raise ValueError("Limite inteiro positivo obrigatório.")
        self.max_passos = max_passos
        self.valor = Fraction(1)
        self.passos = 0
        self.cruzou = False
        self._aposta = None

    @property
    def limiar(self):
        return 1 / self.alpha

    def apostar(self, intensidade):
        if self._aposta is not None:
            raise ValueError("Há uma aposta pendente; não pode ser substituída.")
        if self.passos >= self.max_passos:
            raise ValueError("Orçamento de observações esgotado.")
        intensidade = racional(intensidade)
        if not 0 <= intensidade <= 1 / self.p0:
            raise ValueError("Intensidade fora do intervalo de não negatividade.")
        self._aposta = intensidade

    def observar(self, resultado):
        if self._aposta is None:
            raise ValueError("Escolha a aposta antes de observar.")
        if type(resultado) is not int or resultado not in (0, 1):
            raise ValueError("Resultado Bernoulli inteiro zero ou um obrigatório.")
        self.valor *= 1 + self._aposta * (resultado - self.p0)
        self._aposta = None
        self.passos += 1
        self.cruzou = self.cruzou or self.valor >= self.limiar
        return self.valor
