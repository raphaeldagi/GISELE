// Rodada 59 (Parte 92): um passo de Adam, bit a bit. b1^t e b2^t por MULTIPLICACAO REPETIDA (pow inteiro proprio); sqrt IEEE; exp/log proprios no forward.
public class Rodada59 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;
    static final double LR = 0.1, B1 = 0.9, B2 = 0.999, EPS = 1e-8;
    static final double[][] LOGITS = {{2.0, 1.0, 0.5, 0.0}, {0.1, 0.2, 0.3, 0.25}, {-1.0, 3.0, 2.0, 2.9}, {1.0, 1.0, 1.0, 1.0}, {5.0, -2.0, 0.0, 1.0}};
    static final int[] ALVO = {2, 0, 3, 1, 1};

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double log_(double x) {
        int e = Math.getExponent(x);
        double m = Math.scalb(x, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    static double powInt(double base, int n) {
        double r = 1.0;
        for (int i = 0; i < n; i++) r = r * base;
        return r;
    }

    static double[] softmax(double[] logits) {
        double mx = logits[0];
        for (double x : logits) if (x > mx) mx = x;
        double[] e = new double[logits.length];
        double s = 0.0;
        for (int i = 0; i < logits.length; i++) { e[i] = exp_(logits[i] - mx); s = s + e[i]; }
        for (int i = 0; i < e.length; i++) e[i] = e[i] / s;
        return e;
    }

    public static void main(String[] args) {
        for (int c = 0; c < LOGITS.length; c++) {
            int n = LOGITS[c].length, alvo = ALVO[c];
            double[] w = new double[n], m = new double[n], v = new double[n];
            for (int i = 0; i < n; i++) { w[i] = LOGITS[c][i]; m[i] = 0.0; v[i] = 0.0; }
            for (int t = 1; t <= 3; t++) {
                double[] p = softmax(w);
                double[] g = new double[n];
                for (int i = 0; i < n; i++) g[i] = p[i] - (i == alvo ? 1.0 : 0.0);
                double c1 = 1.0 - powInt(B1, t), c2 = 1.0 - powInt(B2, t);
                for (int i = 0; i < n; i++) {
                    m[i] = B1 * m[i] + (1.0 - B1) * g[i];
                    v[i] = B2 * v[i] + (1.0 - B2) * g[i] * g[i];
                    double mhat = m[i] / c1, vhat = v[i] / c2;
                    w[i] = w[i] - LR * mhat / (Math.sqrt(vhat) + EPS);
                }
            }
            double[] p = softmax(w);
            double perda = -log_(p[alvo]);
            for (int i = 0; i < n; i++) System.out.println("caso " + c + " w " + i + " " + Double.toHexString(w[i]));
            System.out.println("caso " + c + " perda " + Double.toHexString(perda));
        }
        System.out.println("fim");
    }
}
