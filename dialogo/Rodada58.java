// Rodada 58 (Parte 91): o coracao de um passo de treino de GPT (gradiente softmax+entropia cruzada, SGD, decisao), bit a bit. exp/log PROPRIOS (exatas).
public class Rodada58 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951, LR = 0.5;
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
            double[] logits = LOGITS[c];
            int alvo = ALVO[c];
            double[] p = softmax(logits);
            double perda = -log_(p[alvo]);
            double[] grad = new double[logits.length];
            for (int i = 0; i < logits.length; i++) grad[i] = p[i] - (i == alvo ? 1.0 : 0.0);
            double[] novo = new double[logits.length];
            for (int i = 0; i < logits.length; i++) novo[i] = logits[i] - LR * grad[i];
            double[] p2 = softmax(novo);
            double perda2 = -log_(p2[alvo]);
            int arg = 0;
            for (int i = 0; i < novo.length; i++) if (novo[i] > novo[arg]) arg = i;
            System.out.println("caso " + c + " perda " + Double.toHexString(perda) + " perda2 " + Double.toHexString(perda2) + " arg " + arg);
            for (int i = 0; i < novo.length; i++) System.out.println("caso " + c + " w " + i + " " + Double.toHexString(novo[i]));
        }
        System.out.println("fim");
    }
}
