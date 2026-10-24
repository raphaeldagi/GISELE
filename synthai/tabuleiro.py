"""O tabuleiro do jogo de palavras com as letras de outra língua (Parte 150). O `WordGridEnv` da Parte 111 sorteia as letras com
`palavras_rl.LETTER_FREQ` (as frequências do inglês), lido a cada `reset`. Aqui: as frequências contadas num conjunto de lemas, e um
gerenciador de contexto que troca o `LETTER_FREQ` do módulo enquanto um experimento roda e o devolve no fim (o módulo não é editado:
o treino, o avaliador e a GRPO continuam os mesmos). E a densidade D = Σ_w Π_c p(c) das palavras de 3 a 5 letras sob as frequências do
tabuleiro: a chance de que uma sequência sorteada letra a letra seja uma palavra, a conta de peso que a Parte 149 pediu.
"""
import contextlib

from synthai import palavras_rl


def frequencias_de(palavras):
    """Frequência relativa (em %, como LETTER_FREQ) de cada letra A-Z nas palavras dadas; letra ausente fica com 0,01 (o sorteio precisa de peso
    positivo)."""
    cont = {chr(65 + i): 0 for i in range(26)}
    for w in palavras:
        for c in w.upper():
            if c in cont:
                cont[c] += 1
    total = sum(cont.values())
    return {c: max(100.0 * n / total, 0.01) for c, n in cont.items()}


@contextlib.contextmanager
def com_frequencias(freq):
    antigo = palavras_rl.LETTER_FREQ
    palavras_rl.LETTER_FREQ = dict(freq)
    try:
        yield
    finally:
        palavras_rl.LETTER_FREQ = antigo


def densidade(palavras, freq, minimo=3, maximo=5):
    """D = Σ_w Π_c p(c), p normalizada, sobre as palavras de minimo a maximo letras."""
    t = sum(freq.values())
    p = {c: v / t for c, v in freq.items()}
    d = 0.0
    for w in palavras:
        if minimo <= len(w) <= maximo:
            x = 1.0
            for c in w.upper():
                x *= p.get(c, 0.0)
            d += x
    return d
