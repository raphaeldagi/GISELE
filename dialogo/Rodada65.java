// Rodada 65 (Parte 98): a geracao autorregressiva — amostrar o proximo token do softmax por inversao de CDF, bit a bit.
// p = softmax(logits) com o EXP PROPRIO (unica fronteira, Parte 52); acumula a CDF e devolve o 1o token cujo acumulado passa de u (dado de fora).
public class Rodada65 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final double[][] LOGITS = {{2.0, 1.0, 0.5, 0.0, -1.0}, {0.1, 0.2, 0.3, 0.25, 0.0}, {-1.0, 3.0, 2.0, 2.9, 0.5}, {1.0, 1.0, 1.0, 1.0, 1.0}, {5.0, -2.0, 0.0, 1.0, 3.0}};
    static final double[] U = {0.37, 0.95, 0.05, 0.5, 0.999};

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double[] softmax(double[] logits) {
        double m = logits[0];
        for (double x : logits) if (x > m) m = x;
        double[] e = new double[logits.length];
        double s = 0.0;
        for (int i = 0; i < logits.length; i++) { e[i] = exp_(logits[i] - m); s = s + e[i]; }
        for (int i = 0; i < e.length; i++) e[i] = e[i] / s;
        return e;
    }

    public static void main(String[] args) {
        for (int c = 0; c < LOGITS.length; c++) {
            double[] p = softmax(LOGITS[c]);
            double u = U[c];
            double acum = 0.0;
            int tok = p.length - 1;
            double pt = p[p.length - 1];
            for (int i = 0; i < p.length; i++) {
                acum = acum + p[i];
                if (u < acum) { tok = i; pt = p[i]; break; }
            }
            System.out.println("caso " + c + " token " + tok + " p " + Double.toHexString(pt));
        }
        System.out.println("fim");
    }
}
