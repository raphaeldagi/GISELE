"""Semiótica medida (Parte 42): a premissa é o significante, a resposta é o significado.

- Quanto uma resposta acrescenta à sua premissa: a informação condicional por compressão, I(r | p) = C(p + r) − C(p),
  com C o tamanho comprimido por zlib (nível 9). A redundância da resposta com a premissa é 1 − I(r | p)/C(r): 0 se a
  premissa não ajuda em nada a comprimir a resposta, perto de 1 se a resposta já estava na premissa.
- A arbitrariedade do signo (Saussure) num dicionário: a forma da palavra (os trigramas de letras do lema, o significante)
  prevê o significado (a classe do sinset)? Comparada com a definição (o significado escrito por extenso).

Só biblioteca padrão.
"""

import re
import zlib

from .engenharia_reversa import palavras


def comprimido(texto):
    return len(zlib.compress(texto.encode("utf-8"), 9))


def informacao_condicional(premissa, resposta):
    """(C(r), I(r | p), redundância 1 − I/C), em bytes comprimidos."""
    c_r = comprimido(resposta)
    i = comprimido(premissa + "\n" + resposta) - comprimido(premissa)
    return c_r, i, 1 - i / c_r


def premissas_e_respostas(documento):
    """As perguntas de um documento da série ("### Pnnn (0x…). título") e o corpo de cada resposta, até o próximo
    título de nível 1 a 3. Devolve [(número, premissa, resposta)]."""
    blocos = re.split(r"\n(?=#{1,3} )", documento)
    res = []
    for b in blocos:
        m = re.match(r"### P(\d+) \([^)]*\)\. (.*)\n", b)
        if m:
            res.append((int(m.group(1)), m.group(2).strip(), b[m.end():].strip()))
    return res


def retorno_da_premissa(premissa, resposta):
    """A fração das palavras de conteúdo da premissa (mais de 3 letras) que voltam na resposta."""
    p = {w for w in palavras(premissa) if len(w) > 3}
    if not p:
        return None
    r = set(palavras(resposta))
    return len(p & r) / len(p)


def trigramas_de_forma(lema):
    """Os trigramas de letras de um lema, com as bordas marcadas: 'cão' -> {'^cã', 'cão', 'ão$'}."""
    x = "^" + lema.lower() + "$"
    return frozenset(x[i:i + 3] for i in range(len(x) - 2))
