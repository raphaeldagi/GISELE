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


def _ref_generica(fn, x, prec=40):
    """Referência de prec dígitos (decimal) para sin/cos/tan, após reduzir x mod 2pi; arredondada ao float mais próximo."""
    from decimal import Decimal, getcontext
    getcontext().prec = prec
    dois_pi = Decimal("6.283185307179586476925286766559005768394338798750211641949889")
    r = Decimal(x) - (Decimal(x) / dois_pi).to_integral_value(rounding="ROUND_HALF_EVEN") * dois_pi
    sen = Decimal(0); termo = r; n = 0
    while abs(termo) > Decimal(10) ** (-prec - 5) and n < 300:
        sen += termo; n += 1; termo = -termo * r * r / ((2 * n) * (2 * n + 1))
    cos = Decimal(0); termo = Decimal(1); n = 0
    while abs(termo) > Decimal(10) ** (-prec - 5) and n < 300:
        cos += termo; n += 1; termo = -termo * r * r / ((2 * n - 1) * (2 * n))
    if fn == "sin":
        return float(sen)
    if fn == "cos":
        return float(cos)
    return float(sen / cos)   # tan


def contar_fora_wide(fn="sin", n=2000):
    """Quantos de n argumentos x = k/1000 (faixa larga [0,001; n/1000], onde a redução mod 2pi importa) a libm (`math.<fn>`)
    difere da referência de 40 dígitos: a prova local de que sin/cos/tan NÃO são corretamente arredondadas na faixa larga
    (a 6ª face da fronteira da Parte 52 EXISTE; a Parte 104 só não a viu porque usou argumentos pequenos e benignos)."""
    f = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[fn]
    return sum(1 for k in range(1, n + 1) if f(k / 1000.0) != _ref_generica(fn, k / 1000.0))


def sin_uma_parte(x):
    """sin x com reducao de argumento de UMA parte so (k*PI2_HI), para comparar com a de duas partes (sin_ de exatas.py): mostra
    que a segunda parte (PI2_LO) so importa para x grande (o erro de uma parte ~ (x/2pi)*2,45e-16)."""
    PI2 = 6.283185307179586
    k = math.floor(x / PI2 + 0.5)
    r = x - k * PI2
    s2 = r * r
    p = 1.0
    for nn in range(16, 0, -1):
        p = 1.0 - s2 * p / ((2 * nn) * (2 * nn + 1))
    return r * p
