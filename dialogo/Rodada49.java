// Rodada 49 do diálogo Python <-> Java: o valor de um conjunto de experimentos dependentes (P1841, P1842). Lê PASTA/sensores49.txt (as 300 instâncias da
// semente 80) e calcula, como o Python, o VOI de cada conjunto (enumerando as respostas, o conjunto em ordem crescente), o ótimo dentro do orçamento 6 e os
// dois gulosos (olhar 1 e 2, com os mesmos desempates). Só + − × ÷ e comparações. Uso: java Rodada49 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada49 {
    static final int K = 6, ORC = 6;
    static double p;
    static double[][] u;
    static double[] qs;
    static int[] cs;
    static Map<String, Double> memo;

    static double voi(List<Integer> conj) {
        double sem = Math.max(p * u[0][1] + (1 - p) * u[0][0], p * u[1][1] + (1 - p) * u[1][0]);
        double total = 0.0;
        int n = conj.size();
        for (int m = 0; m < (1 << n); m++) {
            double l1 = p, l0 = 1 - p;
            for (int b = 0; b < n; b++) {
                int i = conj.get(b);
                if (((m >> b) & 1) == 1) { l1 *= qs[i]; l0 *= 1 - qs[i]; } else { l1 *= 1 - qs[i]; l0 *= qs[i]; }
            }
            double a0 = l1 * u[0][1] + l0 * u[0][0], a1 = l1 * u[1][1] + l0 * u[1][0];
            total += (a1 > a0) ? a1 : a0;
        }
        double r = total - sem;
        return r > 0.0 ? r : 0.0;
    }

    static double v(List<Integer> c) {
        List<Integer> s = new ArrayList<>(c);
        Collections.sort(s);
        String chave = s.toString();
        Double x = memo.get(chave);
        if (x == null) { x = voi(s); memo.put(chave, x); }
        return x;
    }

    static List<Integer> mais(List<Integer> esc, int... novos) {
        List<Integer> r = new ArrayList<>(esc);
        for (int x : novos) r.add(x);
        return r;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        double so = 0.0, s1 = 0.0, s2 = 0.0;
        int k = 0;
        for (String l : Files.readAllLines(Path.of(args[0], "sensores49.txt"), StandardCharsets.UTF_8)) {
            if (l.isEmpty()) continue;
            String[] xs = l.split(" ");
            double[] w = new double[5 + K];
            for (int i = 0; i < 5 + K; i++) w[i] = Double.parseDouble(xs[i]);
            p = w[0];
            u = new double[][]{{w[1], w[2]}, {w[3], w[4]}};
            qs = Arrays.copyOfRange(w, 5, 5 + K);
            cs = new int[K];
            for (int i = 0; i < K; i++) cs[i] = Integer.parseInt(xs[5 + K + i]);
            memo = new HashMap<>();
            double ot = 0.0;
            for (int m = 0; m < (1 << K); m++) {
                int custo = 0;
                List<Integer> c = new ArrayList<>();
                for (int i = 0; i < K; i++) if ((m >> i & 1) == 1) { custo += cs[i]; c.add(i); }
                if (custo <= ORC) { double x = v(c); if (x > ot) ot = x; }
            }
            double[] g = new double[2];
            List<List<Integer>> e = new ArrayList<>();
            for (int olhar = 1; olhar <= 2; olhar++) {
                List<Integer> esc = new ArrayList<>();
                int resto = ORC;
                while (true) {
                    List<Integer> idx = new ArrayList<>();
                    for (int i = 0; i < K; i++) if (!esc.contains(i) && cs[i] <= resto) idx.add(i);
                    if (idx.isEmpty()) break;
                    double melhor = -1.0;
                    int j = -1;
                    for (int i : idx) { double gi = (v(mais(esc, i)) - v(esc)) / cs[i]; if (gi > melhor) { melhor = gi; j = i; } }
                    if (melhor <= 1e-15) {
                        if (olhar < 2) break;
                        double mp = -1.0;
                        int pi = -1, pj = -1;
                        for (int i : idx) for (int jj : idx)
                            if (i < jj && cs[i] + cs[jj] <= resto) {
                                double gi = (v(mais(esc, i, jj)) - v(esc)) / (cs[i] + cs[jj]);
                                if (gi > mp) { mp = gi; pi = i; pj = jj; }
                            }
                        if (pi < 0 || mp <= 1e-15) break;
                        esc.add(pi); esc.add(pj);
                        resto -= cs[pi] + cs[pj];
                        continue;
                    }
                    esc.add(j);
                    resto -= cs[j];
                }
                g[olhar - 1] = v(esc);
                List<Integer> ord = new ArrayList<>(esc);
                Collections.sort(ord);
                e.add(ord);
            }
            so += ot; s1 += g[0]; s2 += g[1];
            out.println("instancia " + k + ": otimo " + Double.toHexString(ot) + " guloso1 " + Double.toHexString(g[0]) + " " + e.get(0).toString().replace(", ", ",")
                        + " guloso2 " + Double.toHexString(g[1]) + " " + e.get(1).toString().replace(", ", ","));
            k++;
        }
        out.println("totais: otimo " + Double.toHexString(so) + " guloso1 " + Double.toHexString(s1) + " guloso2 " + Double.toHexString(s2));
    }
}
