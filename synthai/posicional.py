"""A codificação posicional senoidal do transformer (Parte 104, P2564/P2565) e a 6ª face da fronteira da Parte 52.

PE(pos)[2i] = sin(pos·wᵢ), PE(pos)[2i+1] = cos(pos·wᵢ), wᵢ = 10000^(−2i/d) (Vaswani et al. 2017). Duas medidas:
- a `sin`/`cos` da libm NÃO é corretamente arredondada (a 6ª face da fronteira): conta-se em quantos argumentos ela difere
  de uma referência de 40 dígitos (Taylor em `decimal`); com uma série de seno PRÓPRIA a codificação fica portável bit a bit;
- o produto interno PE(pos)·PE(pos+k) depende SÓ de k (identidade trig Σᵢ cos(k·wᵢ)) — a geometria da Parte 70."""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dialogo"))
from exatas import cos_, sin_  # noqa: E402  (o seno/cosseno próprios, série de Taylor)


def frequencias(d):
    """wᵢ = 10000^(−2i/d), i = 0..d/2−1."""
    return [10000.0 ** (-2.0 * i / d) for i in range(d // 2)]


def pe(pos, d, proprio=True):
    """O vetor de codificação posicional de dimensão d na posição pos. proprio=True usa o seno/cosseno próprios (portável)."""
    s, c = (sin_, cos_) if proprio else (math.sin, math.cos)
    v = []
    for w in frequencias(d):
        v.append(s(pos * w))
        v.append(c(pos * w))
    return v


def produto(pos, k, d):
    """PE(pos)·PE(pos+k): acumulação sequencial (não o sum() compensado, regra da Parte 34)."""
    a, b = pe(pos, d), pe(pos + k, d)
    s = 0.0
    for x, y in zip(a, b):
        s = s + x * y
    return s


def variancia_translacao(d=16, posicoes=range(0, 20), k=3):
    """A variância de PE(pos)·PE(pos+k) entre as posições, para k fixo: deve ser ~0 (depende só de k)."""
    vals = [produto(p, k, d) for p in posicoes]
    media = sum(vals) / len(vals)
    return max(abs(v - media) for v in vals)


def _sin_referencia(x, prec=40):
    """sin(x) com prec dígitos (Taylor em decimal, após reduzir x mod 2pi em alta precisão), arredondado ao float mais próximo."""
    from decimal import Decimal, getcontext
    getcontext().prec = prec
    # 2*pi com 50 digitos
    dois_pi = Decimal("6.283185307179586476925286766559005768394338798750211641949889")
    xd = Decimal(x)
    kd = (xd / dois_pi).to_integral_value(rounding="ROUND_HALF_EVEN")
    r = xd - kd * dois_pi
    termo = r
    soma = Decimal(0)
    n = 0
    while abs(termo) > Decimal(10) ** (-prec - 5) and n < 200:
        soma += termo
        n += 1
        termo = -termo * r * r / ((2 * n) * (2 * n + 1))
    return float(soma)


def contar_sin_fora_de_arredondamento(n=1000):
    """Quantos de n argumentos a `math.sin` da libm difere da referência de 40 dígitos (prova de que não é corretamente
    arredondada: a 6ª face da fronteira da Parte 52). Argumentos determinísticos k/7, k = 1..n."""
    fora = 0
    for k in range(1, n + 1):
        x = k / 7.0
        if math.sin(x) != _sin_referencia(x):
            fora += 1
    return fora
