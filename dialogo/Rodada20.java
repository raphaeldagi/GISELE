// Rodada 20 do diálogo Python <-> Java: o Naive Bayes multinomial da Parte 34 (contagens, Laplace com alfa = 1) reconhece a
// época de cada seção (Partes 1-20 = 1; 21-41 = 2), deixando uma de fora. As seções vêm de secoes20.txt (rodada20.py
// --preparar). Uso: java Rodada20 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada20 {
    static class NaiveBayes {
        final double alfa = 1.0;
        final TreeMap<Integer, HashMap<String, Integer>> cont = new TreeMap<>();
        final HashMap<Integer, Integer> total = new HashMap<>(), ncls = new HashMap<>();
        final HashSet<String> vocab = new HashSet<>();

        void aprender(String[] ps, int cl) {
            HashMap<String, Integer> c = cont.computeIfAbsent(cl, k -> new HashMap<>());
            for (String w : ps) { c.merge(w, 1, Integer::sum); vocab.add(w); }
            total.merge(cl, ps.length, Integer::sum);
            ncls.merge(cl, 1, Integer::sum);
        }

        double escore(int cl, String[] ps) {
            int n = 0;
            for (int x : ncls.values()) n += x;
            int v = vocab.isEmpty() ? 1 : vocab.size();
            double sc = Math.log((double) ncls.get(cl) / n);
            HashMap<String, Integer> c = cont.get(cl);
            int t = total.get(cl);
            for (String w : ps) sc += Math.log((c.getOrDefault(w, 0) + alfa) / (t + alfa * v));
            return sc;
        }

        int prever(String[] ps) {
            Double melhor = null;
            int arg = -1;
            for (int cl : cont.keySet()) {
                double sc = escore(cl, ps);
                if (melhor == null || sc > melhor) { melhor = sc; arg = cl; }
            }
            return arg;
        }
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<int[]> rot = new ArrayList<>();
        List<String[]> pal = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "secoes20.txt"), StandardCharsets.US_ASCII)) {
            String[] p = l.split("\t", -1);
            rot.add(new int[]{Integer.parseInt(p[0]), Integer.parseInt(p[1])});
            pal.add(p[2].isEmpty() ? new String[0] : p[2].split(" "));
        }
        int acertos = 0;
        for (int i = 0; i < rot.size(); i++) {
            NaiveBayes nb = new NaiveBayes();
            for (int j = 0; j < rot.size(); j++) if (j != i) nb.aprender(pal.get(j), rot.get(j)[1]);
            int prev = nb.prever(pal.get(i));
            if (prev == rot.get(i)[1]) acertos++;
            double dif = nb.escore(1, pal.get(i)) - nb.escore(2, pal.get(i));
            out.println("parte " + rot.get(i)[0] + ": epoca " + rot.get(i)[1] + "; prevista " + prev
                    + "; escore(1) - escore(2) = " + Double.toHexString(dif));
        }
        out.println("acertos: " + acertos);
    }
}
