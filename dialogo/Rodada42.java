// Rodada 42 do diálogo Python <-> Java: a densidade que a conta usa. R_b = π(b⁵)/(Li(b⁵) − Li(2)) (série de Li, log próprio); a conta C
// multiplicada por R_b; a inclinação de z contra b antes e depois. Uso (da raiz do repositório): java Rodada42
import java.io.PrintStream;
import java.util.*;

public class Rodada42 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = Math.sqrt(2.0);
    static final double GAMA = 0.5772156649015329;
    static final int[] QS = {3, 5, 7, 11, 13};
    static boolean[] comp;

    static double log_(double x) {
        int e = Math.getExponent(x);
        double m = Math.scalb(x, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    static List<Integer> primosDe(int m) {
        List<Integer> ps = new ArrayList<>();
        for (int p = 2; (long) p * p <= m; p++) if (m % p == 0) { ps.add(p); while (m % p == 0) m /= p; }
        if (m > 1) ps.add(m);
        return ps;
    }

    static long pw(long a, int e) { long r = 1; for (int i = 0; i < e; i++) r *= a; return r; }

    static long[] palindromos(int b, int L) {
        int h = (L + 1) / 2;
        long lim = pw(b, h - 1);
        long[] out = new long[(int) ((b - 1) * lim)];
        int k = 0;
        int[] ds = new int[L];
        for (int primeiro = 1; primeiro < b; primeiro++) {
            for (long resto = 0; resto < lim; resto++) {
                ds[0] = primeiro;
                int j = 1;
                for (int i = h - 2; i >= 0; i--) ds[j++] = (int) ((resto / pw(b, i)) % b);
                for (int i = 0; i < L / 2; i++) ds[h + i] = ds[L / 2 - 1 - i];
                long n = 0;
                for (int d : ds) n = n * b + d;
                out[k++] = n;
            }
        }
        return out;
    }


    // a base da rodada 39: {N, exatos, medido3, medido5} em long, {correção, C3, C5, var} em double
    static long[] bl = new long[4];
    static double[] bd = new double[4];

    static void base(int b) {
        List<Integer> ps = primosDe(2 * b);
        double f = 1.0;
        for (int p : ps) f = f * p / (p - 1);
        List<Integer> qs = new ArrayList<>();
        for (int q : QS) if (!ps.contains(q)) qs.add(q);
        long exatos = 0;
        for (int L : new int[]{1, 2, 4}) for (long n : palindromos(b, L)) if (!comp[(int) n]) exatos++;
        long N = 0;
        long[] div = new long[qs.size()];
        for (int L : new int[]{3, 5}) for (long n : palindromos(b, L)) {
            boolean cop = true;
            for (int p : ps) if (n % p == 0) cop = false;
            if (!cop) continue;
            N++;
            for (int i = 0; i < qs.size(); i++) if (n % qs.get(i) == 0) div[i]++;
        }
        double corr = 1.0;
        for (int i = 0; i < qs.size(); i++) { int q = qs.get(i); corr = corr * ((double) ((N - div[i]) * q) / (double) (N * (q - 1))); }
        long[] med = new long[6];
        double[] conta = new double[6];
        double var = 0.0;
        for (int L : new int[]{3, 5}) {
            long m = 0;
            double s = 0.0;
            for (long n : palindromos(b, L)) {
                boolean cop = true;
                for (int p : ps) if (n % p == 0) cop = false;
                if (!cop) continue;
                if (!comp[(int) n]) m++;
                double pr = f * corr / log_((double) n);
                s += pr;
                var += pr * (1.0 - pr);
            }
            med[L] = m; conta[L] = s;
        }
        bl[0] = N; bl[1] = exatos; bl[2] = med[3]; bl[3] = med[5];
        bd[0] = corr; bd[1] = conta[3]; bd[2] = conta[5]; bd[3] = var;
    }



    static double li(double x) {
        double L = log_(x), s = 0.0, termo = 1.0;
        for (int k = 1; k < 200; k++) {
            termo = termo * L / k;
            s += termo / k;
            if (termo / k < 1e-17 * s) break;
        }
        return GAMA + log_(L) + s;
    }

    static double reta(List<double[]> pts) {
        int n = pts.size();
        double sb = 0.0, sz = 0.0;
        for (double[] p : pts) { sb += p[0]; sz += p[1]; }
        double mb = sb / n, mz = sz / n, sbb = 0.0, sbz = 0.0;
        for (double[] p : pts) { sbb += (p[0] - mb) * (p[0] - mb); sbz += (p[0] - mb) * (p[1] - mz); }
        return sbz / sbb;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        int LIM = 40 * 40 * 40 * 40 * 40;
        comp = new boolean[LIM];
        comp[0] = comp[1] = true;
        for (int i = 2; (long) i * i < LIM; i++) if (!comp[i]) for (int j = i * i; j < LIM; j += i) comp[j] = true;
        double li2 = li(2.0), maior = 0.0;
        List<double[]> antes = new ArrayList<>(), depois = new ArrayList<>();
        long pi = 0;
        int ate = 0;
        for (int b = 5; b <= 40; b++) {
            int x = b * b * b * b * b;
            for (int n = ate; n < x; n++) if (!comp[n]) pi++;
            ate = x;
            double R = pi / (li((double) x) - li2);
            if (b >= 10) maior = Math.max(maior, Math.abs(R - 1.0));
            base(b);
            long m = bl[1] + bl[2] + bl[3];
            double C = bl[1] + bd[1] + bd[2], s = Math.sqrt(bd[3]);
            double C2 = bl[1] + (bd[1] + bd[2]) * R, s2 = s * Math.sqrt(R);
            antes.add(new double[]{b, (m - C) / s});
            depois.add(new double[]{b, (m - C2) / s2});
            out.println("b=" + b + " pi=" + pi + " R=" + Double.toHexString(R) + " z=" + Double.toHexString((m - C) / s) + " z2=" + Double.toHexString((m - C2) / s2));
        }
        double b1 = reta(antes), b2 = reta(depois);
        out.println("maior |R-1| (10-40)=" + Double.toHexString(maior) + "; inclinacao antes=" + Double.toHexString(b1) + " depois=" + Double.toHexString(b2)
                    + " mudanca=" + Double.toHexString(Math.abs(b2 - b1)));
    }
}
