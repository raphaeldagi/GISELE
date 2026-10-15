// Rodada 67 (Parte 100): a amostragem NUCLEUS (top-p), bit a bit. softmax com EXP PROPRIO (unica fronteira); ordena decrescente,
// soma a CDF ate passar de p (o nucleo), zera o resto, renormaliza, amostra por CDF com u dado de fora. Ordenacao/soma/comparacao exatas.
import java.util.Arrays;
import java.util.Comparator;

public class Rodada67 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final double[][] LOGITS = {{2.0, 1.0, 0.5, 0.0, -1.0}, {2.0, 1.0, 0.5, 0.0, -1.0}, {0.1, 3.0, 2.0, 2.9, 0.5}, {1.0, 1.0, 1.0, 1.0, 1.0}, {5.0, -2.0, 0.0, 1.0, 3.0}};
    static final double[] P = {0.9, 0.5, 0.8, 0.6, 0.95};
    static final double[] U = {0.37, 0.60, 0.95, 0.50, 0.80};

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double pp = 1.0;
        for (int i = 22; i >= 1; i--) pp = 1.0 + r * pp / i;
        return Math.scalb(pp, (int) k);
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

    static double[] nucleus(double[] logits, double pLimiar) {
        double[] p = softmax(logits);
        int n = p.length;
        Integer[] ordem = new Integer[n];
        for (int i = 0; i < n; i++) ordem[i] = i;
        Arrays.sort(ordem, new Comparator<Integer>() {
            public int compare(Integer a, Integer b) { return Double.compare(p[b], p[a]); }
        });
        boolean[] conj = new boolean[n];
        double acum = 0.0;
        for (int idx = 0; idx < n; idx++) {
            int i = ordem[idx];
            conj[i] = true;
            acum = acum + p[i];
            if (acum >= pLimiar) break;
        }
        double massa = 0.0;
        for (int i = 0; i < n; i++) if (conj[i]) massa = massa + p[i];
        double[] q = new double[n];
        for (int i = 0; i < n; i++) q[i] = conj[i] ? p[i] / massa : 0.0;
        return q;
    }

    public static void main(String[] args) {
        for (int c = 0; c < LOGITS.length; c++) {
            double[] q = nucleus(LOGITS[c], P[c]);
            double u = U[c];
            double acum = 0.0;
            int tok = q.length - 1;
            for (int i = 0; i < q.length; i++) { acum = acum + q[i]; if (u < acum) { tok = i; break; } }
            int mantidos = 0;
            double top1 = 0.0;
            for (double x : q) { if (x > 0.0) mantidos++; if (x > top1) top1 = x; }
            System.out.println("caso " + c + " token " + tok + " mantidos " + mantidos + " top1 " + Double.toHexString(top1));
        }
        System.out.println("fim");
    }
}
