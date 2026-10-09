// Rodada 19 do diálogo Python <-> Java: reconstruir a parte a partir só das palavras (sem rótulos, sem acentos pela NFD,
// minúsculas, a-z com 4 letras ou mais). A lista de documentos vem de docs19.txt. Uso: java Rodada19 PASTA
import java.io.PrintStream;
import java.text.Normalizer;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class Rodada19 {
    static final Pattern ROTULO = Pattern.compile("P[0-9]+|0x[0-9A-Fa-f]+");
    static final Pattern PALAVRA = Pattern.compile("[a-z]{4,}");

    static TreeSet<String> numeros(String texto) {
        String t = Normalizer.normalize(ROTULO.matcher(texto).replaceAll(" "), Normalizer.Form.NFD);
        t = t.replaceAll("\\p{M}", "").toLowerCase(java.util.Locale.ROOT);
        TreeSet<String> res = new TreeSet<>();
        Matcher m = PALAVRA.matcher(t);
        while (m.find()) res.add(m.group());
        return res;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        TreeMap<Integer, String> docs = new TreeMap<>();
        for (String l : Files.readAllLines(Path.of(args[0], "docs19.txt"), StandardCharsets.UTF_8)) {
            String[] p = l.split("\t");
            docs.put(Integer.parseInt(p[0]), p[1]);
        }
        TreeMap<Integer, StringBuilder> sec = new TreeMap<>();
        int atual = 1;
        sec.put(1, new StringBuilder());
        boolean primeira = true;
        Pattern cab = Pattern.compile("--- Parte ([0-9]+).*");
        for (String linha : Files.readString(Path.of("resultados.txt"), StandardCharsets.UTF_8).split("\n", -1)) {
            Matcher m = cab.matcher(linha);
            if (m.lookingAt()) {
                atual = Integer.parseInt(m.group(1));
                sec.put(atual, new StringBuilder());
                primeira = true;
            } else if (linha.startsWith("=== Unificacao")) {
                break;
            } else {
                StringBuilder b = sec.get(atual);
                if (!primeira) b.append("\n");
                b.append(linha);
                primeira = false;
            }
        }
        List<Integer> partes = new ArrayList<>();
        for (int k : docs.keySet()) if (sec.containsKey(k)) partes.add(k);
        HashMap<Integer, TreeSet<String>> dn = new HashMap<>();
        HashMap<String, Integer> df = new HashMap<>();
        for (int k : partes) {
            dn.put(k, numeros(Files.readString(Path.of(docs.get(k)), StandardCharsets.UTF_8)));
            for (String t : dn.get(k)) df.merge(t, 1, Integer::sum);
        }
        int K = partes.size(), acertos = 0;
        for (int n : partes) {
            TreeSet<String> r = numeros(sec.get(n).toString());
            int melhor = -1;
            double me = -1.0;
            for (int k : partes) {
                double s = 0.0;
                for (String t : r) if (dn.get(k).contains(t)) s += Math.log((double) K / df.get(t));
                if (s > me) { melhor = k; me = s; }
            }
            if (n == melhor) acertos++;
            out.println("parte " + n + ": " + r.size() + " palavras; escolhe a parte " + melhor + "; escore = " + Double.toHexString(me));
        }
        out.println("acertos: " + acertos);
    }
}
