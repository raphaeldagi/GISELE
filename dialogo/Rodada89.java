// Rodada 89 (Parte 122): a decomposicao de Murphy COMPLETA do Brier (BS = REL - RES + UNC + WBV - WBC), bit a bit. Previsoes p = x/2^31 de
// um LCG, eventos y = [u < p*p], N = 3000, 10 faixas; somas sequenciais na mesma ordem do Python.
import java.util.*;

public class Rodada89 {
    public static void main(String[] args) {
        int N = 3000, F = 10;
        long x = 1221;
        double[] p = new double[N];
        int[] y = new int[N];
        for (int i = 0; i < N; i++) {
            x = (1103515245L * x + 12345L) % 2147483648L;
            double q = x / 2147483648.0;
            x = (1103515245L * x + 12345L) % 2147483648L;
            double u = x / 2147483648.0;
            p[i] = q;
            y[i] = u < q * q ? 1 : 0;
        }
        int somaY = 0;
        for (int v : y) somaY += v;
        double obar = (double) somaY / N;
        List<List<Integer>> grupos = new ArrayList<>();
        for (int k = 0; k < F; k++) grupos.add(new ArrayList<>());
        for (int i = 0; i < N; i++) {
            int k = (int) (p[i] * F);
            grupos.get(k < F ? k : F - 1).add(i);
        }
        double rel = 0.0, res = 0.0, wbv = 0.0, wbc = 0.0;
        for (List<Integer> g : grupos) {
            if (g.isEmpty()) continue;
            int nk = g.size();
            double sp = 0.0;
            int so = 0;
            for (int i : g) { sp += p[i]; so += y[i]; }
            double pk = sp / nk, ok = (double) so / nk;
            rel += nk * ((pk - ok) * (pk - ok));
            res += nk * ((ok - obar) * (ok - obar));
            for (int i : g) {
                wbv += (p[i] - pk) * (p[i] - pk);
                wbc += 2.0 * ((p[i] - pk) * (y[i] - ok));
            }
        }
        rel = rel / N; res = res / N; wbv = wbv / N; wbc = wbc / N;
        double unc = obar * (1.0 - obar);
        double bs = 0.0;
        for (int i = 0; i < N; i++) bs += (p[i] - y[i]) * (p[i] - y[i]);
        bs = bs / N;
        double[] v = {bs, rel, res, unc, wbv, wbc, rel - res + unc + wbv - wbc};
        String[] nomes = {"brier", "rel", "res", "unc", "wbv", "wbc", "soma"};
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 7; i++) sb.append(nomes[i]).append(" ").append(Double.toHexString(v[i])).append("\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
