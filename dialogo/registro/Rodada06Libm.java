// Rodada 6 do diálogo Python <-> Java: o Naive Bayes com pares de palavras, em Java, a partir dos atributos que
// rodada06.py --preparar PASTA exportou. Tudo na mesma ordem que o Python (classes em ordem alfabética, atributos na
// ordem do exemplo), para que as somas de logaritmos deem os mesmos bits. Uso: java Rodada06 PASTA
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;

public class Rodada06Libm {
    public static void main(String[] args) throws Exception {
        TreeMap<String, HashMap<String, Integer>> cont = new TreeMap<>();
        HashMap<String, Integer> total = new HashMap<>(), ncls = new HashMap<>();
        HashSet<String> vocab = new HashSet<>();
        for (String l : Files.readAllLines(Path.of(args[0], "treino06.txt"), StandardCharsets.UTF_8)) {
            int tab = l.indexOf('\t');
            String y = l.substring(0, tab), resto = l.substring(tab + 1);
            String[] x = resto.isEmpty() ? new String[0] : resto.split(" ");
            HashMap<String, Integer> c = cont.computeIfAbsent(y, k -> new HashMap<>());
            for (String w : x) { c.merge(w, 1, Integer::sum); vocab.add(w); }
            total.merge(y, x.length, Integer::sum);
            ncls.merge(y, 1, Integer::sum);
        }
        int n = 0;
        for (int q : ncls.values()) n += q;
        int v = vocab.size();
        StringBuilder prev = new StringBuilder();
        List<String> linhas = new ArrayList<>();
        int acertos = 0, i = 0;
        List<String> teste = Files.readAllLines(Path.of(args[0], "teste06.txt"), StandardCharsets.UTF_8);
        for (String l : teste) {
            int tab = l.indexOf('\t');
            String y = l.substring(0, tab), resto = l.substring(tab + 1);
            String[] x = resto.isEmpty() ? new String[0] : resto.split(" ");
            StringBuilder esc = new StringBuilder(i + ":");
            String melhorCl = null;
            double melhor = 0;
            for (String cl : cont.keySet()) {  // TreeMap: ordem alfabética, como o sorted() do Python
                double s = Math.log((double) ncls.get(cl) / n);
                HashMap<String, Integer> c = cont.get(cl);
                int t = total.get(cl);
                for (String w : x) s += Math.log((c.getOrDefault(w, 0) + 1.0) / (t + 1.0 * v));
                esc.append(' ').append(Double.toHexString(s));
                if (melhorCl == null || s > melhor) { melhor = s; melhorCl = cl; }
            }
            prev.append(melhorCl);
            if (melhorCl.equals(y)) acertos++;
            if (i < 50) linhas.add(esc.toString());
            i++;
        }
        byte[] h = MessageDigest.getInstance("SHA-256").digest(prev.toString().getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : h) sb.append(String.format("%02x", b));
        System.out.println("acertos = " + acertos + " de " + teste.size() + "; sha = " + sb);
        for (String l : linhas) System.out.println(l);
    }
}
