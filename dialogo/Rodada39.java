// Rodada 39 do diálogo Python <-> Java: o que não é divisor (bases 5 a 22, até b^5): a fração dos palíndromos de comprimento 3 e 5
// coprimos a 2b divisíveis por cada q de {3, 5, 7, 11, 13} que não divide 2b; a correção; a conta C por comprimento (log próprio).
// Uso (da raiz do repositório): java Rodada39
import java.io.PrintStream;
import java.util.*;

public class Rodada39 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = Math.sqrt(2.0);
    static final int[] QS = {3, 5, 7, 11, 13};

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

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        int LIM = 22 * 22 * 22 * 22 * 22;
        boolean[] comp = new boolean[LIM];
        comp[0] = comp[1] = true;
        for (int i = 2; (long) i * i < LIM; i++) if (!comp[i]) for (int j = i * i; j < LIM; j += i) comp[j] = true;
        double somaCorr = 0.0, tot = 0.0, zs = 0.0, def5 = 0.0, deft = 0.0;
        for (int b = 5; b <= 22; b++) {
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
            long m = exatos + med[3] + med[5];
            double C = exatos + conta[3] + conta[5];
            double sg = Math.sqrt(var);
            somaCorr += Math.abs(corr - 1.0);
            tot += m - C;
            if (b >= 17) { zs += (m - C) / sg; def5 += med[5] - conta[5]; deft += m - C; }
            StringBuilder dv = new StringBuilder("[");
            for (int i = 0; i < div.length; i++) { if (i > 0) dv.append(", "); dv.append(div[i]); }
            dv.append("]");
            out.println("b=" + b + " N=" + N + " div=" + dv + " correcao=" + Double.toHexString(corr) + " exatos=" + exatos + " medido3=" + med[3]
                        + " medido5=" + med[5] + " C3=" + Double.toHexString(conta[3]) + " C5=" + Double.toHexString(conta[5]) + " sigma=" + Double.toHexString(sg));
        }
        out.println("media |correcao-1|=" + Double.toHexString(somaCorr / 18) + "; soma medido-C=" + Double.toHexString(tot) + "; media z 17-22="
                    + Double.toHexString(zs / 6) + "; fracao do deficit em L=5=" + Double.toHexString(def5 / deft));
    }
}
