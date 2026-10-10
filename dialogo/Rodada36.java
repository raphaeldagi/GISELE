// Rodada 36 do diálogo Python <-> Java: o último dígito dos narcisistas (bases 3 a 16, k de 2 a 7). Por base, nas células sem
// interruptor: o excesso do teste do último dígito, a razão medido/conta e a conta corrigida; e a correlação de postos.
// Uso (da raiz do repositório): java Rodada36
import java.io.PrintStream;
import java.util.*;

public class Rodada36 {
    static long fat(int n) { long r = 1; for (int i = 2; i <= n; i++) r *= i; return r; }
    static long pw(long a, int e) { long r = 1; for (int i = 0; i < e; i++) r *= a; return r; }

    static long cand, passa, dist, medido, num;

    static void percorre(int b, int k, int[] ds, int pos, int min, long[] pot) {
        if (pos == k) {
            long s = 0;
            for (int d : ds) s += pot[d];
            if (s < pw(b, k - 1) || s >= pw(b, k)) return;
            cand++;
            int[] cont = new int[b];
            for (int d : ds) cont[d]++;
            int nd = 0;
            for (int d = 0; d < b; d++) if (cont[d] > 0) nd++;
            dist += nd;
            if (cont[(int) (s % b)] > 0) passa++;
            long m = fat(k);
            for (int d = 0; d < b; d++) m /= fat(cont[d]);
            num += m * (k - cont[0]) / k;
            int[] dig = new int[b];
            long x = s;
            while (x > 0) { dig[(int) (x % b)]++; x /= b; }
            if (Arrays.equals(dig, cont)) medido++;
            return;
        }
        for (int d = min; d < b; d++) { ds[pos] = d; percorre(b, k, ds, pos + 1, d, pot); }
    }

    static double[] postos(double[] xs) {
        Integer[] ordem = new Integer[xs.length];
        for (int i = 0; i < xs.length; i++) ordem[i] = i;
        Arrays.sort(ordem, (a, c) -> xs[a] != xs[c] ? Double.compare(xs[a], xs[c]) : Integer.compare(a, c));
        double[] r = new double[xs.length];
        int i = 0;
        while (i < ordem.length) {
            int j = i;
            while (j + 1 < ordem.length && xs[ordem[j + 1]] == xs[ordem[i]]) j++;
            for (int t = i; t <= j; t++) r[ordem[t]] = (i + j + 2) / 2.0;
            i = j + 1;
        }
        return r;
    }

    static double pearson(double[] xs, double[] ys) {
        int n = xs.length;
        double mx = 0.0, my = 0.0;
        for (double x : xs) mx += x;
        for (double y : ys) my += y;
        mx = mx / n; my = my / n;
        double sxy = 0.0, sxx = 0.0, syy = 0.0;
        for (int i = 0; i < n; i++) {
            sxy += (xs[i] - mx) * (ys[i] - my);
            sxx += (xs[i] - mx) * (xs[i] - mx);
            syy += (ys[i] - my) * (ys[i] - my);
        }
        return sxy / Math.sqrt(sxx * syy);
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        int nb = 14;
        double[] exc = new double[nb], raz = new double[nb], conta = new double[nb], corr = new double[nb];
        long[] med = new long[nb];
        for (int b = 3; b <= 16; b++) {
            long pa = 0, di = 0, me = 0;
            double ct = 0.0, co = 0.0;
            for (int k = 2; k <= 7; k++) {
                long[] pot = new long[b];
                for (int d = 0; d < b; d++) pot[d] = pw(d, k);
                cand = passa = dist = medido = num = 0;
                percorre(b, k, new int[k], 0, 0, pot);
                boolean inter = false;
                for (int d = 2; d < b; d++) for (int p = 0; p < k; p++) if (pw(d, k - 1) == pw(b, p)) inter = true;
                if (inter || cand == 0) continue;
                long den = (long) (b - 1) * pw(b, k - 1);
                int g = 1;
                for (int c = 1; c < b; c++) {
                    if ((b - 1) % c != 0) continue;
                    boolean ok = true;
                    for (int d = 0; d < b; d++) if ((pw(d, k) - d) % c != 0) { ok = false; break; }
                    if (ok) g = c;
                }
                pa += passa; di += dist; me += medido;
                double e = ((double) num / (double) den) * g;
                ct += e;
                co += e * ((double) (passa * b) / (double) dist);
            }
            int i = b - 3;
            exc[i] = (double) (pa * b) / (double) di;
            raz[i] = me / ct;
            med[i] = me; conta[i] = ct; corr[i] = co;
            out.println("b=" + b + " excesso=" + Double.toHexString(exc[i]) + " razao=" + Double.toHexString(raz[i]) + " medido=" + me
                        + " conta=" + Double.toHexString(ct) + " corrigida=" + Double.toHexString(co));
        }
        out.println("spearman = " + Double.toHexString(pearson(postos(exc), postos(raz))));
        long m = 0;
        double e = 0.0, ec = 0.0;
        for (int i = 0; i < nb; i++) { m += med[i]; e += conta[i]; ec += corr[i]; }
        out.println("total: medido=" + m + " conta=" + Double.toHexString(e) + " corrigida=" + Double.toHexString(ec) + " razao="
                    + Double.toHexString(m / e) + " razao corrigida=" + Double.toHexString(m / ec));
    }
}
