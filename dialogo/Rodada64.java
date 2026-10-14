// Rodada 64 (Parte 97): um BLOCO TRANSFORMER completo de 2 camadas, bit a bit. Cada camada: LayerNorm(x+atencao) e LayerNorm(h+MLP(ReLU)).
// O UNICO transcendental e o exp do softmax (exp proprio, fronteira da Parte 52); o resto e +-*/ e sqrt. Pesos/entrada por LCG inteiro identico.
public class Rodada64 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final int T = 3, D = 4, H = 4;
    static final double EPS = 1e-5;
    static final long M = 2147483648L;
    static long estado = 12345L;

    static double lcg() {
        estado = (1103515245L * estado + 12345L) % M;
        return (double) estado / (double) M - 0.5;
    }

    static double[][] mat(int linhas, int colunas) {
        double[][] w = new double[linhas][colunas];
        for (int i = 0; i < linhas; i++) for (int j = 0; j < colunas; j++) w[i][j] = lcg();
        return w;
    }

    static double[] vec(int n) {
        double[] v = new double[n];
        for (int i = 0; i < n; i++) v[i] = lcg();
        return v;
    }

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double[] matvec(double[][] W, double[] x, double[] b) {
        double[] out = new double[W.length];
        for (int o = 0; o < W.length; o++) {
            double s = 0.0;
            for (int k = 0; k < x.length; k++) s = s + W[o][k] * x[k];
            out[o] = s + b[o];
        }
        return out;
    }

    static double[] layernorm(double[] v, double[] gamma, double[] beta) {
        double soma = 0.0;
        for (double z : v) soma = soma + z;
        double mu = soma / v.length;
        double sq = 0.0;
        for (double z : v) sq = sq + (z - mu) * (z - mu);
        double var = sq / v.length;
        double inv = 1.0 / Math.sqrt(var + EPS);
        double[] out = new double[v.length];
        for (int i = 0; i < v.length; i++) out[i] = gamma[i] * ((v[i] - mu) * inv) + beta[i];
        return out;
    }

    static double[][] atencao(double[][] seq, double[][] Wq, double[][] Wk, double[][] Wv) {
        double[] zero = new double[D];
        double[][] Q = new double[T][], K = new double[T][], V = new double[T][];
        for (int i = 0; i < T; i++) { Q[i] = matvec(Wq, seq[i], zero); K[i] = matvec(Wk, seq[i], zero); V[i] = matvec(Wv, seq[i], zero); }
        double escala = Math.sqrt((double) D);
        double[][] saidas = new double[T][D];
        for (int i = 0; i < T; i++) {
            double[] e = new double[i + 1];
            for (int j = 0; j <= i; j++) {
                double dot = 0.0;
                for (int k = 0; k < D; k++) dot = dot + Q[i][k] * K[j][k];
                e[j] = dot / escala;
            }
            double m = e[0];
            for (double x : e) if (x > m) m = x;
            double[] ex = new double[i + 1];
            double s = 0.0;
            for (int j = 0; j <= i; j++) { ex[j] = exp_(e[j] - m); s = s + ex[j]; }
            double[] o = new double[D];
            for (int j = 0; j <= i; j++) { double pj = ex[j] / s; for (int k = 0; k < D; k++) o[k] = o[k] + pj * V[j][k]; }
            saidas[i] = o;
        }
        return saidas;
    }

    static double relu(double x) { return x > 0.0 ? x : 0.0; }

    static double[][] camada(double[][] seq, double[][][] W, double[][] b, double[][] g) {
        // W = {Wq,Wk,Wv,W1,W2}; b = {b1,b2}; g = {g1,be1,g2,be2}
        double[][] attn = atencao(seq, W[0], W[1], W[2]);
        double[][] h = new double[T][];
        for (int i = 0; i < T; i++) {
            double[] soma = new double[D];
            for (int k = 0; k < D; k++) soma[k] = seq[i][k] + attn[i][k];
            h[i] = layernorm(soma, g[0], g[1]);
        }
        double[][] saida = new double[T][];
        for (int i = 0; i < T; i++) {
            double[] oculto = matvec(W[3], h[i], b[0]);
            for (int k = 0; k < oculto.length; k++) oculto[k] = relu(oculto[k]);
            double[] mlp = matvec(W[4], oculto, b[1]);
            double[] soma = new double[D];
            for (int k = 0; k < D; k++) soma[k] = h[i][k] + mlp[k];
            saida[i] = layernorm(soma, g[2], g[3]);
        }
        return saida;
    }

    static Object[] params() {
        double[][] Wq = mat(D, D), Wk = mat(D, D), Wv = mat(D, D), W1 = mat(H, D);
        double[] b1 = vec(H);
        double[][] W2 = mat(D, H);
        double[] b2 = vec(D), g1 = vec(D), be1 = vec(D), g2 = vec(D), be2 = vec(D);
        return new Object[]{new double[][][]{Wq, Wk, Wv, W1, W2}, new double[][]{b1, b2}, new double[][]{g1, be1, g2, be2}};
    }

    public static void main(String[] args) {
        estado = 12345L;
        double[][] seq = new double[T][];
        for (int i = 0; i < T; i++) seq[i] = vec(D);
        Object[] P1 = params();
        Object[] P2 = params();
        double[][] Wo = mat(2, D);
        double[] bo = vec(2);
        seq = camada(seq, (double[][][]) P1[0], (double[][]) P1[1], (double[][]) P1[2]);
        seq = camada(seq, (double[][][]) P2[0], (double[][]) P2[1], (double[][]) P2[2]);
        double[] logits = matvec(Wo, seq[T - 1], bo);
        int arg = logits[0] >= logits[1] ? 0 : 1;
        for (int i = 0; i < T; i++) for (int k = 0; k < D; k++)
            System.out.println("pos " + i + " dim " + k + " " + Double.toHexString(seq[i][k]));
        for (int k = 0; k < 2; k++) System.out.println("logit " + k + " " + Double.toHexString(logits[k]));
        System.out.println("decisao " + arg);
        System.out.println("fim");
    }
}
