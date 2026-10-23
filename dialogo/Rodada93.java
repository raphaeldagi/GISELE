// Rodada 93 (Parte 141): o reservatorio (algoritmo R) e o posto efetivo (Jacobi ciclico, exp e log proprios) de synthai.reservatorio bit a bit.
// 64 vetores de 4 dimensoes de um LCG; randrange(n) = (int)(u*n) do mesmo LCG; somas sequenciais na ordem do Python.
import java.util.*;

public class Rodada93 {
    static long x = 14193;
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;

    static double exp_(double v) {
        double k = Math.floor(v / (LN2_HI + LN2_LO) + 0.5);
        double r = (v - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double log_(double v) {
        int e = Math.getExponent(v);
        double m = Math.scalb(v, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    static double u() {
        x = (1103515245L * x + 12345L) % 2147483648L;
        return x / 2147483648.0;
    }

    static double[] jacobi(double[][] S) {
        int d = S.length;
        double[][] A = new double[d][];
        for (int i = 0; i < d; i++) A[i] = S[i].clone();
        for (int it = 0; it < 60; it++) {
            double fora = 0.0;
            for (int i = 0; i < d; i++) for (int j = 0; j < d; j++) if (i != j) fora += A[i][j] * A[i][j];
            if (fora < 1e-300) break;
            for (int p = 0; p < d - 1; p++) for (int q = p + 1; q < d; q++) {
                if (Math.abs(A[p][q]) < 1e-300) continue;
                double th = (A[q][q] - A[p][p]) / (2.0 * A[p][q]);
                double t = (th >= 0 ? 1.0 : -1.0) / (Math.abs(th) + Math.sqrt(th * th + 1.0));
                double c = 1.0 / Math.sqrt(t * t + 1.0), s = t * c;
                for (int k = 0; k < d; k++) { double akp = A[k][p], akq = A[k][q]; A[k][p] = c * akp - s * akq; A[k][q] = s * akp + c * akq; }
                for (int k = 0; k < d; k++) { double apk = A[p][k], aqk = A[q][k]; A[p][k] = c * apk - s * aqk; A[q][k] = s * apk + c * aqk; }
            }
        }
        double[] ev = new double[d];
        for (int i = 0; i < d; i++) ev[i] = A[i][i];
        Arrays.sort(ev);
        return ev;
    }

    public static void main(String[] args) {
        int cap = 16, vistos = 0;
        List<Integer> idx = new ArrayList<>();
        List<double[]> vet = new ArrayList<>();
        for (int i = 0; i < 64; i++) {
            double[] v = new double[4];
            for (int j = 0; j < 4; j++) v[j] = 2.0 * u() - 1.0;
            vistos++;
            if (idx.size() < cap) { idx.add(i); vet.add(v); }
            else { int j = (int) (u() * vistos); if (j < cap) { idx.set(j, i); vet.set(j, v); } }
        }
        int n = vet.size(), d = 4;
        double[] med = new double[d];
        for (int j = 0; j < d; j++) { double t = 0.0; for (double[] l : vet) t += l[j]; med[j] = t / n; }
        double[][] Hc = new double[n][d];
        for (int k = 0; k < n; k++) for (int j = 0; j < d; j++) Hc[k][j] = vet.get(k)[j] - med[j];
        double[][] Z = new double[d][d];
        for (int i = 0; i < d; i++) for (int j = 0; j < d; j++) { double t = 0.0; for (int k = 0; k < n; k++) t += Hc[k][i] * Hc[k][j]; Z[i][j] = t; }
        double[] ev = jacobi(Z);
        double[] s = new double[d];
        for (int i = 0; i < d; i++) s[i] = Math.sqrt(Math.max(ev[d - 1 - i], 0.0));
        double soma = 0.0;
        for (double v : s) if (v > 0) soma += v;
        double h = 0.0;
        for (double v : s) if (v > 0) h += (v / soma) * log_(v / soma);
        StringBuilder sb = new StringBuilder("indices");
        for (int i : idx) sb.append(" ").append(i);
        sb.append("\nposto ").append(Double.toHexString(exp_(-h))).append("\nfim");
        System.out.println(sb.toString());
    }
}
