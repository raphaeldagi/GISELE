// Rodada 22 do diálogo Python <-> Java: a deriva tem meia-vida (exponencial) ou memória longa (potência)? A semelhança idf
// da Rodada 21 (secoes22.txt, escrito por rodada22.py --preparar), médias por distância 1..20, dois ajustes em log.
// Uso: java Rodada22 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada22Libm {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<Integer> partes = new ArrayList<>();
        List<String[]> ws = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "secoes22.txt"), StandardCharsets.US_ASCII)) {
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
        int A = 20;
        double[] xe = new double[A], xp = new double[A], ys = new double[A];
        for (int L = 1; L <= A; L++) {
            ys[L - 1] = Math.log(media(sim, L));
            xe[L - 1] = (double) L;
            xp[L - 1] = Math.log(L);
            out.println("distancia " + L + ": ln(media) = " + Double.toHexString(ys[L - 1]));
        }
        double[] e = reta(xe, ys), p = reta(xp, ys);
        out.println("exponencial: a = " + Double.toHexString(e[0]) + "; tau = " + Double.toHexString(-1.0 / e[1]) + "; residuo = " + Double.toHexString(e[2]));
        out.println("potencia: b = " + Double.toHexString(p[0]) + "; alfa = " + Double.toHexString(-p[1]) + "; residuo = " + Double.toHexString(p[2]));
        out.println("melhor: " + (e[2] < p[2] ? "exponencial" : "potencia"));
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
