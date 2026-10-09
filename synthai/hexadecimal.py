"""A SYNTHAI em hexadecimal (Parte 30, P361).

Um dígito hexadecimal são 4 bits. Aqui cada bit liga um módulo das Partes 22–29, e o código do tipo diz qual SYNTHAI é:

    bit 0x1  pensamento de Newton (P302)          (desligado: o gradiente da Parte 22)
    bit 0x2  limiar autorregulado com âncora (P343) (desligado: o limiar fixo 2P*)
    bit 0x4  exploração de Thompson (P295)        (desligado: o bônus UCB entregue pelo mundo)
    bit 0x8  leitura neutra do sensor (P292)      (desligado: a leitura que falta vale 0)

São 16 tipos, de 0x0 (a SYNTHAI da Parte 22) a 0xF. A versão principal antiga (SynthaiExploradora) é o tipo 0x4; a composta
(P356) é 0x4 no bandido e 0x3 fora dele. Cada tipo é montado por composição de módulos já testados (P351).

Também: a transformada de Walsh–Hadamard (o algoritmo de Yates, 1937) que dá todos os efeitos de um experimento fatorial
2^k de uma vez, e a quantização dos pesos do pensamento em 1 ou 2 dígitos hexadecimais (4 ou 8 bits) por peso."""

from .ancora import SynthaiComAncora
from .limiar import SynthaiAjustada
from .reconhecimento import SynthaiReconhecida

BITS = ((0x1, "Newton"), (0x2, "âncora"), (0x4, "Thompson"), (0x8, "neutro"))


def nome_do_tipo(codigo):
    ligados = [nome for bit, nome in BITS if codigo & bit]
    return f"0x{codigo:X} ({' + '.join(ligados) if ligados else 'Parte 22'})"


def synthai_do_tipo(codigo, semente=0):
    """A SYNTHAI do tipo `codigo` (0x0 a 0xF)."""
    if not 0 <= codigo <= 0xF:
        raise ValueError("o tipo é um dígito hexadecimal: 0x0 a 0xF")
    flags = dict(neutro=bool(codigo & 0x8), atencao_inteira=False, memoria=False, thompson=bool(codigo & 0x4))
    if codigo & 0x2:
        return SynthaiComAncora(semente, newton=bool(codigo & 0x1), z=0.8416, auditoria=True, **flags)
    if codigo & 0x1:
        return SynthaiAjustada(semente, mult=2.0, **flags)
    return SynthaiReconhecida(semente, **flags)


def walsh_hadamard(valores):
    """Transformada rápida de Walsh–Hadamard (borboletas, k passes de somas e diferenças). Para y em ordem de Yates
    (índice = código binário dos fatores), a saída j é Σ_i (−1)^popcount(i & j) y_i: j = 0 é o total; um j com um só
    bit é o contraste de um fator; com vários bits, o da interação deles."""
    v = list(valores)
    n = len(v)
    if n & (n - 1):
        raise ValueError("o tamanho tem de ser uma potência de 2")
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]
                v[j], v[j + h] = a + b, a - b
        h *= 2
    return v


def efeitos_fatoriais(valores):
    """Efeitos de um fatorial 2^k (média no nível alto − média no nível baixo) a partir das respostas em ordem de Yates.
    O sinal da transformada é (+) no nível baixo, então o efeito é −contraste / 2^(k−1); o índice 0 devolve a média."""
    t = walsh_hadamard(valores)
    n = len(valores)
    return [t[0] / n] + [-c / (n / 2) for c in t[1:]]


def quantizar(pesos, bits):
    """Quantização uniforme de um vetor de pesos em `bits` por peso (4 = um dígito hex; 8 = dois), com uma escala por
    vetor: a grade vai de −R a R, R = max |w|, com 2^bits níveis (passo Δ = 2R / (2^bits − 1)). Devolve os pesos
    reconstruídos, os códigos em hexadecimal e o passo Δ."""
    r = max(abs(w) for w in pesos) or 1.0
    niveis = 2 ** bits - 1
    passo = 2 * r / niveis
    codigos = [min(niveis, max(0, round((w + r) / passo))) for w in pesos]
    digitos = bits // 4
    return [c * passo - r for c in codigos], "".join(f"{c:0{digitos}X}" for c in codigos), passo
