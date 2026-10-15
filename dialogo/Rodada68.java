// Rodada 68 (Parte 101): a penalidade de repeticao (CTRL) na amostragem, bit a bit. Antes do softmax, o logit de cada token usado e
// dividido por pen se positivo, multiplicado se negativo. softmax com EXP PROPRIO (unica fronteira); amostra por CDF com u dado de fora.
public class Rodada68 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final double[][] LOGITS = {{2.0, 1.0, 0.5, 0.0, -1.0}, {2.0, 1.0, 0.5, 0.0, -1.0}, {0.1, 3.0, 2.0, 2.9, 0.5}, {1.0, -1.0, 2.0, -0.5, 0.0}, {5.0, -2.0, 0.0, 1.0, 3.0}};
    static final int[][] USADOS = {{0}, {0, 1}, {1}, {1, 3}, {0, 4}};
    static final double[] PEN = {1.3, 1.3, 1.5, 1.2, 2.0};
    static final double[] U = {0.37, 0.60, 0.50, 0.80, 0.95};

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double[] penalizar(double[] logits, int[] usados, double pen) {
        boolean[] s = new boolean[logits.length];
        for (int i : usados) s[i] = true;
        double[] out = new double[logits.length];
        for (int i = 0; i < logits.length; i++) {
            double x = logits[i];
            if (s[i]) x = x > 0.0 ? x / pen : x * pen;
            out[i] = x;
        }
        return out;
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
            double[] p = softmax(penalizar(LOGITS[c], USADOS[c], PEN[c]));
            double u = U[c];
            double acum = 0.0;
            int tok = p.length - 1;
            for (int i = 0; i < p.length; i++) { acum = acum + p[i]; if (u < acum) { tok = i; break; } }
            double top1 = p[0];
            for (double x : p) if (x > top1) top1 = x;
            System.out.println("caso " + c + " token " + tok + " top1 " + Double.toHexString(top1) + " p0 " + Double.toHexString(p[0]));
        }
        System.out.println("fim");
    }
}
