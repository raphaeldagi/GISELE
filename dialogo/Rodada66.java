// Rodada 66 (Parte 99): a amostragem com TEMPERATURA e TOP-K, bit a bit. Divide logits por T (divisao), mantem os k maiores (comparacao),
// softmax com EXP PROPRIO (unica fronteira), amostra por CDF com u dado de fora; imprime a entropia (log proprio). Pesos/entrada fixos.
import java.util.Arrays;
import java.util.Comparator;

public class Rodada66 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;
    static final double[][] LOGITS = {{2.0, 1.0, 0.5, 0.0, -1.0}, {2.0, 1.0, 0.5, 0.0, -1.0}, {2.0, 1.0, 0.5, 0.0, -1.0}, {2.0, 1.0, 0.5, 0.0, -1.0}, {0.1, 3.0, 2.0, 2.9, 0.5}};
    static final double[] T = {1.0, 0.5, 2.0, 1.0, 0.8};
    static final int[] K = {5, 5, 5, 2, 3};
    static final double[] U = {0.37, 0.60, 0.60, 0.60, 0.95};

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

    static double[] softmaxTopK(double[] logits, double t, int k) {
        int n = logits.length;
        double[] z = new double[n];
        for (int i = 0; i < n; i++) z[i] = logits[i] / t;
        Integer[] ord = new Integer[n];
        for (int i = 0; i < n; i++) ord[i] = i;
        Arrays.sort(ord, new Comparator<Integer>() {
            public int compare(Integer a, Integer b) { return Double.compare(z[b], z[a]); }
        });
        boolean[] mant = new boolean[n];
        for (int i = 0; i < k; i++) mant[ord[i]] = true;
        Double m = null;
        for (int i = 0; i < n; i++) if (mant[i] && (m == null || z[i] > m)) m = z[i];
        double[] e = new double[n];
        double s = 0.0;
        for (int i = 0; i < n; i++) { e[i] = mant[i] ? exp_(z[i] - m) : 0.0; s = s + e[i]; }
        for (int i = 0; i < n; i++) e[i] = e[i] / s;
        return e;
    }

    static double entropia(double[] p) {
        double h = 0.0;
        for (double x : p) if (x > 0.0) h = h - x * log_(x);
        return h;
    }

    public static void main(String[] args) {
        for (int c = 0; c < LOGITS.length; c++) {
            double[] p = softmaxTopK(LOGITS[c], T[c], K[c]);
            double u = U[c];
            double acum = 0.0;
            int tok = p.length - 1;
            for (int i = 0; i < p.length; i++) { acum = acum + p[i]; if (u < acum) { tok = i; break; } }
            double top1 = p[0];
            for (double x : p) if (x > top1) top1 = x;
            System.out.println("caso " + c + " token " + tok + " top1 " + Double.toHexString(top1) + " entropia " + Double.toHexString(entropia(p)));
        }
        System.out.println("fim");
    }
}
