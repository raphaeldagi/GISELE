// Rodada 37 do diálogo Python <-> Java: o fator de congruência efetivo dos narcisistas (bases 3 a 16, k de 2 a 7), contra o g
// da Parte 60; a conta com F no lugar de g; por base, nas células sem interruptor. Uso (da raiz do repositório): java Rodada37
import java.io.PrintStream;
import java.util.*;

public class Rodada37 {
    static long fat(int n) { long r = 1; for (int i = 2; i <= n; i++) r *= i; return r; }
    static long pw(long a, int e) { long r = 1; for (int i = 0; i < e; i++) r *= a; return r; }

    static long cand, iguais, medido, num;

    static void percorre(int b, int k, int[] ds, int pos, int min, long[] pot) {
        if (pos == k) {
            long s = 0, sd = 0;
            for (int d : ds) { s += pot[d]; sd += d; }
            if (s < pw(b, k - 1) || s >= pw(b, k)) return;
            cand++;
            if ((s - sd) % (b - 1) == 0) iguais++;
            int[] cont = new int[b];
            for (int d : ds) cont[d]++;
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

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        long longe = 0, comCand = 0, tm = 0;
        double tg = 0.0, tf = 0.0;
        for (int b = 3; b <= 16; b++) {
            long m = 0;
            double cg = 0.0, cf = 0.0;
            for (int k = 2; k <= 7; k++) {
                long[] pot = new long[b];
                for (int d = 0; d < b; d++) pot[d] = pw(d, k);
                cand = iguais = medido = num = 0;
                percorre(b, k, new int[k], 0, 0, pot);
                if (cand == 0) continue;
                long den = (long) (b - 1) * pw(b, k - 1);
                int g = 1;
                for (int c = 1; c < b; c++) {
                    if ((b - 1) % c != 0) continue;
                    boolean ok = true;
                    for (int d = 0; d < b; d++) if ((pw(d, k) - d) % c != 0) { ok = false; break; }
                    if (ok) g = c;
                }
                boolean inter = false;
                for (int d = 2; d < b; d++) for (int p = 0; p < k; p++) if (pw(d, k - 1) == pw(b, p)) inter = true;
                double f = (double) ((b - 1) * iguais) / (double) cand;
                comCand++;
                if (Math.abs(f - g) > 0.1 * g) longe++;
                out.println("b=" + b + " k=" + k + " candidatos=" + cand + " iguais=" + iguais + " F=" + Double.toHexString(f) + " g=" + g
                            + " interruptor=" + (inter ? 1 : 0));
                if (inter) continue;
                double e = (double) num / (double) den;
                m += medido;
                cg += e * g;
                cf += e * f;
            }
            tm += m; tg += cg; tf += cf;
            out.println("base " + b + ": medido=" + m + " conta_g=" + Double.toHexString(cg) + " conta_F=" + Double.toHexString(cf)
                        + " razao_g=" + Double.toHexString(m / cg) + " razao_F=" + Double.toHexString(m / cf));
        }
        out.println("celulas com candidatos=" + comCand + "; F longe de g (>10%)=" + longe + "; fracao=" + Double.toHexString((double) longe / comCand));
        out.println("total: medido=" + tm + " conta_g=" + Double.toHexString(tg) + " conta_F=" + Double.toHexString(tf) + " razao_g="
                    + Double.toHexString(tm / tg) + " razao_F=" + Double.toHexString(tm / tf));
    }
}
