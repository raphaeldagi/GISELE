"""Rodada 34 do diálogo Python <-> Java: o placar por voz, contado por uma função. Lê dialogo/DIALOGO.md, corta as seções
"## Rodada N" com 13 <= N <= 33 e conta, para cada voz, as previsões e os acertos, por duas regras escritas antes do código:
estrita (vereditos com dono, mais os que a seção declara das duas vozes) e generosa (mais os vereditos sem dono, dados às duas).
Rodar da raiz do repositório: python3 dialogo/rodada34.py"""

import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# só espaço, tabulação, quebra de linha, asterisco, dois-pontos e parêntese: nada de \s, que no Python inclui espaços Unicode
VEREDITO = re.compile(r"\(([a-z])\)[ \t\n*:]*(✅|❌)")
DONO = re.compile(r"[ \t\n*(]*(?:a previsão da |a da )?(IA-Python|IA-Java)")
CONJUNTA = re.compile(r"\(([a-z])\),? (?:das duas vozes|para as duas)")
VOZES = ("IA-Python", "IA-Java")


def secoes(texto, de=13, ate=33):
    """[(N, texto da seção)] das seções '## Rodada N', na ordem do arquivo."""
    saida, atual, linhas = [], None, []
    for l in texto.split("\n"):
        if l.startswith("## "):
            if atual is not None:
                saida.append((atual, "\n".join(linhas)))
            m = re.match(r"## Rodada ([0-9]+) ", l)
            atual = int(m.group(1)) if m and de <= int(m.group(1)) <= ate else None
            linhas = []
        elif atual is not None:
            linhas.append(l)
    if atual is not None:
        saida.append((atual, "\n".join(linhas)))
    return saida


def vereditos(sec):
    """(com dono {(letra, voz): acerto}, conjuntas {letra: acerto}, sem dono {letra: acerto}); o primeiro veredito de cada letra vale."""
    conj = set(CONJUNTA.findall(sec))
    dono, juntas, sem, vistas = {}, {}, {}, set()
    for m in VEREDITO.finditer(sec):
        letra, ok = m.group(1), m.group(2) == "✅"
        d = DONO.match(sec, m.end())
        if d:
            dono.setdefault((letra, d.group(1)), ok)
        elif letra in conj:
            juntas.setdefault(letra, ok)
        elif letra not in vistas:
            sem.setdefault(letra, ok)
        vistas.add(letra)
    for chave in list(sem):  # uma letra que tem dono em outro ponto da seção não é sem dono
        if any(k[0] == chave for k in dono) or chave in juntas:
            del sem[chave]
    return dono, juntas, sem


def placar(texto, de=13, ate=33):
    """{voz: [previsões estritas, acertos estritos, previsões generosas, acertos generosos]} e as linhas por rodada."""
    tot = {v: [0, 0, 0, 0] for v in VOZES}
    linhas = []
    for n, sec in secoes(texto, de, ate):
        dono, juntas, sem = vereditos(sec)
        partes = []
        for v in VOZES:
            meus = [ok for (l, voz), ok in sorted(dono.items()) if voz == v] + [ok for l, ok in sorted(juntas.items())]
            extra = [ok for l, ok in sorted(sem.items())]
            t = tot[v]
            t[0] += len(meus)
            t[1] += sum(meus)
            t[2] += len(meus) + len(extra)
            t[3] += sum(meus) + sum(extra)
            partes.append(f"{v} {sum(meus)}/{len(meus)}")
        linhas.append(f"rodada {n}: " + "; ".join(partes) + f"; conjuntas {''.join(sorted(juntas))}; sem dono {''.join(sorted(sem))}")
    return tot, linhas


def main():
    texto = open(os.path.join(RAIZ, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    tot, linhas = placar(texto)
    for l in linhas:
        print(l)
    for v in VOZES:
        a, b, c, d = tot[v]
        print(f"{v}: estrita {b} em {a}; generosa {d} em {c}")


if __name__ == "__main__":
    main()
