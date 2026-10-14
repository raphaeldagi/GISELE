"""Rodada 50 do diálogo Python <-> Java, com os PAPÉIS INVERTIDOS (Parte 83: "depois inverta"): a IA-Java pergunta, a IA-Python responde. O GAN de Dirac
(Mescheder, Geiger e Nowozin, 2018): dados verdadeiros em 0, gerador θ, discriminador D(x) = ψ·x, perda L = f(ψθ) + f(0), f(t) = −log(1 + e^(−t)), f'(t) =
1/(1 + e^t). Três treinos de 1000 passos com η = 0,1 a partir de (0,1; 0): síncrono (os dois gradientes no mesmo ponto), alternado (o discriminador vê o θ
novo) e assíncrono (a cada passo, uma moeda escolhe quem se move; a moeda é o bit de cima de um LCG de 64 bits, o mesmo nas duas linguagens). O exp é o
PRÓPRIO (dialogo/exatas.py, regra da Parte 52). Imprime cada passo em hexadecimal e, por treino, a norma final, a norma máxima e as trocas de sinal de θ.
Rodar da raiz: python3 dialogo/rodada50.py"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

M64 = (1 << 64) - 1


def df(t):
    return 1.0 / (1.0 + exp_(t))


def treinar(esquema, eta=0.1, n=1000, th=0.1, ps=0.0, lcg=83):
    traj = [(th, ps)]
    for _ in range(n):
        if esquema == "sincrono":
            g = df(ps * th)
            th, ps = th - eta * g * ps, ps + eta * g * th
        elif esquema == "alternado":
            th = th - eta * df(ps * th) * ps
            ps = ps + eta * df(ps * th) * th
        else:
            lcg = (lcg * 6364136223846793005 + 1442695040888963407) & M64
            if lcg >> 63:
                th = th - eta * df(ps * th) * ps
            else:
                ps = ps + eta * df(ps * th) * th
        traj.append((th, ps))
    return traj


def resumo(traj):
    normas = [math.sqrt(t * t + p * p) for t, p in traj]
    trocas = sum(1 for k in range(len(traj) - 1) if traj[k][0] * traj[k + 1][0] < 0.0)
    return normas[-1], max(normas), trocas


def main():
    for esquema in ("sincrono", "alternado", "assincrono"):
        traj = treinar(esquema)
        for k, (t, p) in enumerate(traj):
            print(f"{esquema} {k} {t.hex()} {p.hex()}")
        final, maximo, trocas = resumo(traj)
        print(f"{esquema}: final {final.hex()} maximo {maximo.hex()} trocas {trocas}")


if __name__ == "__main__":
    main()
