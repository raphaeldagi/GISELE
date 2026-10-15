"""O dicionário convertido em NÚMEROS, tratado como equações (Parte 103, P2533/P2534).

O pedido ("o dicionário pode ser convertido em números para que se possa tratá-lo como equações e cálculos binários
ou não binários") vira duas conversões honestas e offline (só biblioteca padrão), cada uma com a sua conta fechada:

- BINÁRIA (GF(2)⁴, o hexadecimal das Partes 30/70): cada palavra vira um vetor de 4 bits (os 4 bits baixos de um hash
  estável). A matriz palavras × 4 bits tem posto de coluna cheio = 4 com probabilidade esmagadora (as 4 colunas de
  bits são quase independentes). Álgebra linear SOBRE GF(2) (eliminação de Gauss com XOR), não sobre os reais.
- NÃO-BINÁRIA (hash num inteiro): jogar n palavras em m baldes por um hash; o nº de colisões (pares no mesmo balde)
  é ~ C(n,2)/m pela conta do aniversário (Poisson de média C(n,2)/m). É o PREÇO de tratar palavra como número: dois
  significados distintos no mesmo número."""


def _hash_estavel(palavra):
    """Um hash determinístico (não depende do PYTHONHASHSEED): FNV-1a de 32 bits sobre os bytes da palavra."""
    h = 0x811C9DC5
    for b in palavra.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def vetor_gf2(palavra):
    """A palavra como vetor de GF(2)⁴: os 4 bits baixos do hash estável (o dígito hexadecimal baixo)."""
    h = _hash_estavel(palavra)
    return [(h >> i) & 1 for i in range(4)]


def posto_gf2(vetores):
    """O posto, sobre GF(2), da matriz cujas linhas são os vetores de bits (eliminação de Gauss com XOR). Devolve o
    nº de pivôs — o posto de coluna cheio de uma matriz de 4 colunas é 4."""
    linhas = [list(v) for v in vetores]
    ncol = len(linhas[0]) if linhas else 0
    posto = 0
    usadas = [False] * len(linhas)
    for c in range(ncol):
        piv = next((i for i in range(len(linhas)) if not usadas[i] and linhas[i][c]), None)
        if piv is None:
            continue
        usadas[piv] = True
        posto += 1
        for i in range(len(linhas)):
            if i != piv and linhas[i][c]:
                linhas[i] = [x ^ y for x, y in zip(linhas[i], linhas[piv])]
    return posto


def posto_do_dicionario_gf2(palavras):
    """O posto sobre GF(2) da matriz dos dígitos-hex das palavras (o "cálculo binário" do dicionário)."""
    return posto_gf2([vetor_gf2(p) for p in palavras])


def colisoes(palavras, m=10007):
    """O nº de colisões (pares de palavras no mesmo balde) ao jogar as palavras em m baldes por hash estável — o custo,
    não-binário, de tratar palavra como número. Conta fechada esperada: C(n,2)/m (aniversário/Poisson)."""
    from collections import Counter
    c = Counter(_hash_estavel(p) % m for p in palavras)
    return sum(k * (k - 1) // 2 for k in c.values())


def colisoes_esperadas(n, m=10007):
    """A conta fechada do nº esperado de colisões: C(n,2)/m."""
    return n * (n - 1) / 2 / m
