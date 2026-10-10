// Rodada 23 do diálogo Python <-> Java: as curvas individuais de esquecimento (Anderson e Tweney). Para cada parte i de
// 1 a 21, sim(i, i + L), L = 1..20, sem os zeros; os ajustes exponencial e potência em log. Lê secoes23.txt.
// Uso: java Rodada23 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada23Libm {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<Integer> partes = new ArrayList<>();
        List<String[]> ws = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "secoes23.txt"), StandardCharsets.US_ASCII)) {
            String[] p = l.split("\t", -1);
            partes.add(Integer.parseInt(p[0]));
            ws.add(p[1].isEmpty() ? new String[0] : p[1].split(" "));
        }
        int K = partes.size();
        HashMap<String, Integer> df = new HashMap<>();
        for (String[] a : ws) for (String w : a) df.merge(w, 1, Integer::sum);
        HashMap<String, Double> idf2 = new HashMap<>();
        for (Map.Entry<String, Integer> e : df.entrySet()) {
            double x = Math.log((double) K / e.getValue());
            idf2.put(e.getKey(), x * x);
        }
        double[] norma = new double[K];
        for (int i = 0; i < K; i++) { double t = 0.0; for (String w : ws.get(i)) t += idf2.get(w); norma[i] = t; }
        double[][] sim = new double[K][K];
        for (int i = 0; i < K; i++) {
            HashSet<String> a = new HashSet<>(Arrays.asList(ws.get(i)));
            for (int j = 0; j < K; j++) {
                double t = 0.0;
                for (String w : ws.get(j)) if (a.contains(w)) t += idf2.get(w);
                sim[i][j] = (norma[i] > 0 && norma[j] > 0) ? t / Math.sqrt(norma[i] * norma[j]) : 0.0;
            }
        }
        int A = 20, pot = 0;
        for (int i = 0; i + A < K; i++) {
            int k = 0;
            for (int L = 1; L <= A; L++) if (sim[i][i + L] > 0) k++;
            double[] xe = new double[k], xp = new double[k], ys = new double[k];
            int q = 0;
            for (int L = 1; L <= A; L++) {
                if (sim[i][i + L] > 0) {
                    xe[q] = (double) L; xp[q] = Math.log(L); ys[q] = Math.log(sim[i][i + L]); q++;
                }
            }
            double[] e = reta(xe, ys), p = reta(xp, ys);
            if (p[2] < e[2]) pot++;
            out.println("parte " + partes.get(i) + ": " + k + " pontos; tau = " + Double.toHexString(-1.0 / e[1]) + "; residuo exp = "
                    + Double.toHexString(e[2]) + "; alfa = " + Double.toHexString(-p[1]) + "; residuo pot = " + Double.toHexString(p[2]));
        }
        out.println("a potencia ganha em " + pot);
    }

    static double[] reta(double[] xs, double[] ys) {
        int n = xs.length;
        double sx = 0.0, sy = 0.0;
        for (int i = 0; i < n; i++) { sx += xs[i]; sy += ys[i]; }
        double mx = sx / n, my = sy / n, sxy = 0.0, sxx = 0.0;
        for (int i = 0; i < n; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) * (xs[i] - mx); }
        double m = sxy / sxx, c = my - m * mx, sse = 0.0;
        for (int i = 0; i < n; i++) { double r = ys[i] - (c + m * xs[i]); sse += r * r; }
        return new double[]{c, m, sse};
    }

    static double media(double[][] sim, int L) {
        double t = 0.0;
        int n = 0;
        for (int i = 0; i + L < sim.length; i++) { t += sim[i][i + L]; n++; }
        return t / n;
    }
}
