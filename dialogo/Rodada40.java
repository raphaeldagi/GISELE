// Rodada 40 do diálogo Python <-> Java: o endereço da falta. Base 21, palíndromos de 5 dígitos coprimos a 42, por primeiro dígito e
// por dígito do meio, contra a conta C da rodada 39 reescalada; o qui-quadrado; e as bases 23 a 28 com a conta C.
// Uso (da raiz do repositório): java Rodada40
import java.io.PrintStream;
import java.util.*;

public class Rodada40 {
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

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        int LIM = 28 * 28 * 28 * 28 * 28;
        comp = new boolean[LIM];
        comp[0] = comp[1] = true;
        for (int i = 2; (long) i * i < LIM; i++) if (!comp[i]) for (int j = i * i; j < LIM; j += i) comp[j] = true;
        int b = 21;
        List<Integer> ps = primosDe(2 * b);
        double f = 1.0;
        for (int p : ps) f = f * p / (p - 1);
        base(b);
        double corr = bd[0];
        TreeMap<Long, double[]> c0 = new TreeMap<>(), c2 = new TreeMap<>();   // {medido, conta, var}
        for (long n : palindromos(b, 5)) {
            boolean cop = true;
            for (int p : ps) if (n % p == 0) cop = false;
            if (!cop) continue;
            double pr = f * corr / log_((double) n);
            long[] ds = {n / (b * b * b * b), (n / (b * b)) % b};
            for (int t = 0; t < 2; t++) {
                TreeMap<Long, double[]> cl = t == 0 ? c0 : c2;
                double[] x = cl.computeIfAbsent(ds[t], kk -> new double[3]);
                if (!comp[(int) n]) x[0] += 1.0;
                x[1] += pr;
                x[2] += pr * (1.0 - pr);
            }
        }
        String[] nomes = {"d0", "d2"};
        for (int t = 0; t < 2; t++) {
            TreeMap<Long, double[]> cl = t == 0 ? c0 : c2;
            long m = 0;
            double e = 0.0;
            for (Map.Entry<Long, double[]> en : cl.entrySet()) {
                out.println(nomes[t] + "=" + en.getKey() + " medido=" + (long) en.getValue()[0] + " conta=" + Double.toHexString(en.getValue()[1]));
                m += (long) en.getValue()[0];
                e += en.getValue()[1];
            }
            double k = m / e, q = 0.0;
            for (double[] x : cl.values()) q += (x[0] - k * x[1]) * (x[0] - k * x[1]) / (k * x[2]);
            int gl = cl.size() - 1;
            out.println(nomes[t] + ": qui2=" + Double.toHexString(q) + " gl=" + gl + " k=" + Double.toHexString(k) + " qui2/gl=" + Double.toHexString(q / gl));
        }
        double zs = 0.0;
        int neg = 0;
        for (int bb = 23; bb <= 28; bb++) {
            base(bb);
            long m = bl[1] + bl[2] + bl[3];
            double C = bl[1] + bd[1] + bd[2], s = Math.sqrt(bd[3]), z = (m - C) / s;
            zs += z;
            if (z < 0) neg++;
            out.println("b=" + bb + " medido=" + m + " C=" + Double.toHexString(C) + " sigma=" + Double.toHexString(s) + " z=" + Double.toHexString(z));
        }
        out.println("media z 23-28=" + Double.toHexString(zs / 6) + "; negativos=" + neg);
    }
}
