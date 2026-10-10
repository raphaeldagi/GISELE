// Rodada 18 do diálogo Python <-> Java: reconstruir as perguntas a partir só dos números. A lista de documentos vem de
// docs18.txt (escrito por rodada18.py --preparar); os textos são lidos da raiz do repositório. Uso: java Rodada18 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class Rodada18 {
    // Parte 73: log PRÓPRIO (cópia do da Rodada26), exato nas duas línguas; a versão com Math.log está em dialogo/registro/
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;

    static double log_(double x) {
        int e = Math.getExponent(x);
        double m = Math.scalb(x, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    static final Pattern ROTULO = Pattern.compile("P[0-9]+|0x[0-9A-Fa-f]+");
    static final Pattern NUMERO = Pattern.compile("[0-9][0-9.,]*[0-9]|[0-9]");

    static TreeSet<String> numeros(String texto) {
        TreeSet<String> res = new TreeSet<>();
        Matcher m = NUMERO.matcher(ROTULO.matcher(texto).replaceAll(" "));
        while (m.find()) {
            String d = m.group().replace(".", "").replace(",", "").replaceFirst("^0+", "");
            if (d.length() >= 3) res.add(d);
        }
        return res;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        TreeMap<Integer, String> docs = new TreeMap<>();
        for (String l : Files.readAllLines(Path.of(args[0], "docs18.txt"), StandardCharsets.UTF_8)) {
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
                for (String t : r) if (dn.get(k).contains(t)) s += log_((double) K / df.get(t));
                if (s > me) { melhor = k; me = s; }
            }
            if (n == melhor) acertos++;
            out.println("parte " + n + ": " + r.size() + " numeros; escolhe a parte " + melhor + "; escore = " + Double.toHexString(me));
        }
        out.println("acertos: " + acertos);
    }
}
