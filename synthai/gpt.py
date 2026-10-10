"""A forma de GPT (Parte 69): um Generative Pre-trained Transformer mínimo, em Python puro.

Um bloco de transformador com atenção causal de uma cabeça, como no GPT: para a sequência de fichas x₀ … x_{n−1},
  e_t = E[x_t] + P[t]                                  (embedding da ficha + da posição)
  q_t, k_t, v_t = e_t Q, e_t K, e_t V                   (consulta, chave, valor)
  a_t = softmax_j≤t (q_t · k_j / √d)                   (atenção causal: só o passado)
  r_t = e_t + (Σ_j a_tj v_j) O                         (resíduo)
  z_t = r_t + relu(r_t W1 + b1) W2                     (MLP, resíduo)
  p_t = softmax(z_t U + c)                             (a distribuição do próximo caractere)
e a perda é a entropia cruzada média −(1/n) Σ ln p_t[x_{t+1}]. O gradiente é escrito à mão (sem bibliotecas) e conferido
por diferenças finitas nos testes; o treino é Adam. É a forma do GPT em miniatura: o tamanho cresce parte a parte, sempre
medido contra um modelo mais simples (o n-grama)."""

import math
import random

PARAMS = ("E", "P", "Q", "K", "V", "O", "W1", "b1", "W2", "U", "c")


def _zeros(n, m):
    return [[0.0] * m for _ in range(n)]


class GPT:
    def __init__(self, vocab, T=16, d=16, h=32, semente=69):
        r = random.Random(semente)
        self.vocab = vocab
        self.indice = {ch: i for i, ch in enumerate(vocab)}
        self.T, self.d, self.h, V = T, d, h, len(vocab)

        def g(n, m, s):
            return [[r.gauss(0.0, s) for _ in range(m)] for _ in range(n)]
        sd = 1.0 / math.sqrt(d)
        self.p = {"E": g(V, d, 0.3), "P": g(T, d, 0.3), "Q": g(d, d, sd), "K": g(d, d, sd), "V": g(d, d, sd),
                  "O": g(d, d, sd), "W1": g(d, h, sd), "b1": _zeros(1, h), "W2": g(h, d, 1.0 / math.sqrt(h)),
                  "U": g(d, V, sd), "c": _zeros(1, V)}
        self.m = {k: _zeros(len(v), len(v[0])) for k, v in self.p.items()}
        self.v = {k: _zeros(len(v), len(v[0])) for k, v in self.p.items()}
        self.passo = 0

    # ---------------------------------------------------------------- ida
    def adiante(self, x, exp=math.exp):
        """As ativações de cada posição de x (lista de índices, n ≤ T). Devolve o dicionário com tudo o que o gradiente usa;
        'probs' são as distribuições do próximo caractere."""
        p, d, h = self.p, self.d, self.h
        esc = 1.0 / math.sqrt(d)
        E, P, Q, K, Vm, O, W1, b1, W2, U, c = (p[k] for k in PARAMS)
        n = len(x)
        e = [[E[x[t]][i] + P[t][i] for i in range(d)] for t in range(n)]

        def mat(vet, M, colunas):
            saida = []
            for j in range(colunas):
                s = 0.0
                for i in range(len(vet)):
                    s += vet[i] * M[i][j]
                saida.append(s)
            return saida
        q = [mat(e[t], Q, d) for t in range(n)]
        k = [mat(e[t], K, d) for t in range(n)]
        v = [mat(e[t], Vm, d) for t in range(n)]
        a, o, u, r_, pre, mm, z, probs = [], [], [], [], [], [], [], []
        for t in range(n):
            s = []
            for j in range(t + 1):
                acc = 0.0
                for i in range(d):
                    acc += q[t][i] * k[j][i]
                s.append(acc * esc)
            mx = max(s)
            w = [exp(x_ - mx) for x_ in s]
            tot = 0.0
            for x_ in w:
                tot += x_
            at = [x_ / tot for x_ in w]
            a.append(at)
            ot = [0.0] * d
            for j in range(t + 1):
                for i in range(d):
                    ot[i] += at[j] * v[j][i]
            o.append(ot)
            ut = mat(ot, O, d)
            u.append(ut)
            rt = [e[t][i] + ut[i] for i in range(d)]
            r_.append(rt)
            pr = mat(rt, W1, h)
            pr = [pr[i] + b1[0][i] for i in range(h)]
            pre.append(pr)
            mt = [x_ if x_ > 0.0 else 0.0 for x_ in pr]
            mm.append(mt)
            w2 = mat(mt, W2, d)
            zt = [rt[i] + w2[i] for i in range(d)]
            z.append(zt)
            lg = mat(zt, U, len(c[0]))
            lg = [lg[i] + c[0][i] for i in range(len(lg))]
            mx = max(lg)
            w = [exp(x_ - mx) for x_ in lg]
            tot = 0.0
            for x_ in w:
                tot += x_
            probs.append([x_ / tot for x_ in w])
        return {"x": x, "e": e, "q": q, "k": k, "v": v, "a": a, "o": o, "r": r_, "pre": pre, "m": mm, "z": z, "probs": probs}

    def perda(self, x, y):
        """Entropia cruzada média (nats) de prever y[t] a partir de x[:t+1]."""
        pr = self.adiante(x)["probs"]
        return -sum(math.log(pr[t][y[t]]) for t in range(len(x))) / len(x)

    # ---------------------------------------------------------------- volta
    def gradiente(self, x, y):
        """(perda, gradientes) de uma sequência, à mão."""
        f = self.adiante(x)
        p, d, h = self.p, self.d, self.h
        esc = 1.0 / math.sqrt(d)
        n = len(x)
        G = {k: _zeros(len(v), len(v[0])) for k, v in p.items()}
        de = _zeros(n, d)
        dq, dk, dv = _zeros(n, d), _zeros(n, d), _zeros(n, d)
        perda = 0.0
        V = len(p["c"][0])
        for t in range(n):
            pt = f["probs"][t]
            perda -= math.log(pt[y[t]])
            dl = [pt[j] / n for j in range(V)]
            dl[y[t]] -= 1.0 / n
            zt = f["z"][t]
            for i in range(d):
                Gi, zi = G["U"][i], zt[i]
                for j in range(V):
                    Gi[j] += zi * dl[j]
            for j in range(V):
                G["c"][0][j] += dl[j]
            dz = [0.0] * d
            for i in range(d):
                Ui, s = p["U"][i], 0.0
                for j in range(V):
                    s += Ui[j] * dl[j]
                dz[i] = s
            dr = dz[:]
            mt, pr = f["m"][t], f["pre"][t]
            for a_ in range(h):
                for i in range(d):
                    G["W2"][a_][i] += mt[a_] * dz[i]
            dpre = [0.0] * h
            for a_ in range(h):
                if pr[a_] > 0.0:
                    s = 0.0
                    W2a = p["W2"][a_]
                    for i in range(d):
                        s += W2a[i] * dz[i]
                    dpre[a_] = s
            rt = f["r"][t]
            for i in range(d):
                for a_ in range(h):
                    G["W1"][i][a_] += rt[i] * dpre[a_]
                s = 0.0
                W1i = p["W1"][i]
                for a_ in range(h):
                    s += W1i[a_] * dpre[a_]
                dr[i] += s
            for a_ in range(h):
                G["b1"][0][a_] += dpre[a_]
            # r = e + o O
            for i in range(d):
                de[t][i] += dr[i]
            ot = f["o"][t]
            for i in range(d):
                for j in range(d):
                    G["O"][i][j] += ot[i] * dr[j]
            do = [0.0] * d
            for i in range(d):
                s = 0.0
                Oi = p["O"][i]
                for j in range(d):
                    s += Oi[j] * dr[j]
                do[i] = s
            at = f["a"][t]
            da = []
            for j in range(t + 1):
                s = 0.0
                vj = f["v"][j]
                for i in range(d):
                    s += do[i] * vj[i]
                da.append(s)
                for i in range(d):
                    dv[j][i] += at[j] * do[i]
            soma = 0.0
            for j in range(t + 1):
                soma += at[j] * da[j]
            for j in range(t + 1):
                ds = at[j] * (da[j] - soma) * esc
                kj, qt = f["k"][j], f["q"][t]
                for i in range(d):
                    dq[t][i] += ds * kj[i]
                    dk[j][i] += ds * qt[i]
        for t in range(n):
            et = f["e"][t]
            for nome, dd in (("Q", dq), ("K", dk), ("V", dv)):
                M = p[nome]
                GM = G[nome]
                for i in range(d):
                    ei = et[i]
                    for j in range(d):
                        GM[i][j] += ei * dd[t][j]
                for i in range(d):
                    s = 0.0
                    Mi = M[i]
                    for j in range(d):
                        s += Mi[j] * dd[t][j]
                    de[t][i] += s
            for i in range(d):
                G["E"][x[t]][i] += de[t][i]
                G["P"][t][i] += de[t][i]
        return perda / n, G

    def adam(self, G, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
        self.passo += 1
        c1, c2 = 1 - b1 ** self.passo, 1 - b2 ** self.passo
        for k, M in self.p.items():
            Gk, mk, vk = G[k], self.m[k], self.v[k]
            for i in range(len(M)):
                Mi, Gi, mi, vi = M[i], Gk[i], mk[i], vk[i]
                for j in range(len(Mi)):
                    g = Gi[j]
                    mi[j] = b1 * mi[j] + (1 - b1) * g
                    vi[j] = b2 * vi[j] + (1 - b2) * g * g
                    Mi[j] -= lr * (mi[j] / c1) / (math.sqrt(vi[j] / c2) + eps)

    def codificar(self, texto):
        return [self.indice.get(ch, self.indice.get("?", 0)) for ch in texto]

    def treinar(self, texto, passos=2000, lr=0.01, semente=69):
        """Pré-treino: em cada passo, uma janela de T + 1 caracteres sorteada do texto (semente fixa). Devolve as perdas."""
        r = random.Random(semente)
        ids = self.codificar(texto)
        perdas = []
        for _ in range(passos):
            i = r.randrange(0, len(ids) - self.T - 1)
            x, y = ids[i:i + self.T], ids[i + 1:i + self.T + 1]
            l, G = self.gradiente(x, y)
            self.adam(G, lr)
            perdas.append(l)
        return perdas

    def bits_por_caractere(self, texto, janelas=None):
        """Bits por caractere num texto, em janelas consecutivas de T caracteres (cada janela com o contexto dela)."""
        ids = self.codificar(texto)
        tot, n = 0.0, 0
        inicio = list(range(0, len(ids) - self.T - 1, self.T))
        if janelas is not None:
            inicio = inicio[:janelas]
        for i in inicio:
            x, y = ids[i:i + self.T], ids[i + 1:i + self.T + 1]
            tot += self.perda(x, y) * len(x)
            n += len(x)
        return tot / n / math.log(2)

    def gerar(self, inicio, n=60):
        """Gera n caracteres pelo argmax (determinístico), com a janela dos últimos T."""
        ids = self.codificar(inicio)
        for _ in range(n):
            pr = self.adiante(ids[-self.T:])["probs"][-1]
            ids.append(max(range(len(pr)), key=lambda j: (pr[j], -j)))
        return "".join(self.vocab[i] for i in ids)
