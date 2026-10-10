// Rodada 41 do diálogo Python <-> Java: tendência ou dispersão. O z dos primos palíndromos (conta C da rodada 39) nas bases 5 a 40; a
// reta de z contra b; a média e o desvio-padrão dos z das bases 35 a 40. Uso (da raiz do repositório): java Rodada41
import java.io.PrintStream;
import java.util.*;

public class Rodada41 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = Math.sqrt(2.0);
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


    static double[] mediaDp(List<Double> v) {
        int n = v.size();
        double s = 0.0;
        for (double x : v) s += x;
        double m = s / n, q = 0.0;
        for (double x : v) q += (x - m) * (x - m);
        return new double[]{m, Math.sqrt(q / (n - 1))};
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        int LIM = 40 * 40 * 40 * 40 * 40;
        comp = new boolean[LIM];
        comp[0] = comp[1] = true;
        for (int i = 2; (long) i * i < LIM; i++) if (!comp[i]) for (int j = i * i; j < LIM; j += i) comp[j] = true;
        List<double[]> pts = new ArrayList<>();
        List<Double> novos = new ArrayList<>(), todos = new ArrayList<>();
        for (int b = 5; b <= 40; b++) {
            base(b);
            long m = bl[1] + bl[2] + bl[3];
            double C = bl[1] + bd[1] + bd[2], z = (m - C) / Math.sqrt(bd[3]);
            out.println("b=" + b + " medido=" + m + " z=" + Double.toHexString(z));
            pts.add(new double[]{b, z});
            todos.add(z);
            if (b >= 35) novos.add(z);
        }
        int n = pts.size();
        double sb = 0.0, sz = 0.0;
        for (double[] p : pts) { sb += p[0]; sz += p[1]; }
        double mb = sb / n, mz = sz / n, sbb = 0.0, sbz = 0.0;
        for (double[] p : pts) { sbb += (p[0] - mb) * (p[0] - mb); sbz += (p[0] - mb) * (p[1] - mz); }
        double beta = sbz / sbb, alfa = mz - beta * mb, rr = 0.0;
        for (double[] p : pts) { double r = p[1] - (alfa + beta * p[0]); rr += r * r; }
        double ep = Math.sqrt(rr / (n - 2)) / Math.sqrt(sbb);
        double[] a = mediaDp(novos), t = mediaDp(todos);
        out.println("reta: inclinacao=" + Double.toHexString(beta) + " intercepto=" + Double.toHexString(alfa) + " ep=" + Double.toHexString(ep));
        out.println("bases 35-40: media=" + Double.toHexString(a[0]) + " dp=" + Double.toHexString(a[1]) + "; todas: media=" + Double.toHexString(t[0])
                    + " dp=" + Double.toHexString(t[1]));
    }
}
