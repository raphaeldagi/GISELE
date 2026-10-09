// Rodada 21 do diálogo Python <-> Java: a série é um ciclo? Cosseno idf entre as seções (conjuntos de palavras, em
// secoes21.txt, escrito por rodada21.py --preparar). Uso: java Rodada21 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada21 {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<Integer> partes = new ArrayList<>();
        List<String[]> ws = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "secoes21.txt"), StandardCharsets.US_ASCII)) {
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
        int u = K - 1;
        for (int j = 0; j < K; j++)
            out.println("sim(parte " + partes.get(u) + ", parte " + partes.get(j) + ") = " + Double.toHexString(sim[u][j]));
        out.println("media a distancia 1 = " + Double.toHexString(media(sim, 1)) + "; a distancia 20 = " + Double.toHexString(media(sim, 20)));
        HashMap<Integer, Integer> pos = new HashMap<>();
        for (int i = 0; i < K; i++) pos.put(partes.get(i), i);
        double tc = 0.0, tm = 0.0;
        int nc = 0, nm = 0;
        for (int k = 1; k <= 10; k++) if (pos.containsKey(k)) { tc += sim[u][pos.get(k)]; nc++; }
        for (int k = 11; k <= 30; k++) if (pos.containsKey(k)) { tm += sim[u][pos.get(k)]; nm++; }
        out.println("indice do ciclo = " + Double.toHexString((tc / nc) / (tm / nm)));
    }

    static double media(double[][] sim, int L) {
        double t = 0.0;
        int n = 0;
        for (int i = 0; i + L < sim.length; i++) { t += sim[i][i + L]; n++; }
        return t / n;
    }
}
