"""Auditoria da arquitetura autopoietica recebida (Parte 88): a LFI1 (logica de inconsistencia formal) e a "probabilidade dentro da probabilidade", reimplementadas
na biblioteca padrao para medir o que o codigo recebido afirma. Nada e executado do texto do usuario; estas sao versoes escritas do zero (regra da Parte 72)."""


def lfi1_negacao(v):
    if v == 1.0:
        return 0.0
    if v == 0.0:
        return 1.0
    return 0.5  # a negacao de uma dialeteia permanece dialeteia


def lfi1_conjuncao(a, b):
    if a == 0.5 or b == 0.5:
        if a == 0.0 or b == 0.0:
            return 0.0
        return 0.5
    return min(a, b)


def lfi1_disjuncao(a, b):
    if a == 0.5 or b == 0.5:
        if a == 1.0 or b == 1.0:
            return 1.0
        return 0.5
    return max(a, b)


def lfi1_consistencia(v):
    """Operador de consistencia o(A): 1.0 se estritamente consistente (0 ou 1), 0.0 se dialeteia."""
    return 1.0 if v in (0.0, 1.0) else 0.0


def nested_probability(x):
    """A 'probabilidade dentro da probabilidade' do codigo recebido: media de Beta(10x+1, 10(1-x)+1) = (10x+1)/12. Uma contracao afim para 0,5."""
    x = min(0.999, max(0.001, x))
    a = x * 10 + 1
    b = (1 - x) * 10 + 1
    return a / (a + b)


def iterar_nested_probability(x, n):
    for _ in range(n):
        x = nested_probability(x)
    return x
