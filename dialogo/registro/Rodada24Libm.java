// Rodada 24 do diálogo Python <-> Java: a pergunta reconhece a sua resposta? O texto pós-ASI contra os documentos das
// Partes 1-49 (palavras em docs24.txt e texto24.txt, escritos por rodada24.py --preparar), soma de ln(K/df).
// Uso: java Rodada24 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada24Libm {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<Integer> partes = new ArrayList<>();
        List<String[]> ws = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "docs24.txt"), StandardCharsets.US_ASCII)) {
            String[] p = l.split("\t", -1);
            partes.add(Integer.parseInt(p[0]));
            ws.add(p[1].isEmpty() ? new String[0] : p[1].split(" "));
        }
        String lt = Files.readAllLines(Path.of(args[0], "texto24.txt"), StandardCharsets.US_ASCII).get(0);
        HashSet<String> t = new HashSet<>(Arrays.asList(lt.isEmpty() ? new String[0] : lt.split(" ")));
        int K = partes.size();
        HashMap<String, Integer> df = new HashMap<>();
        for (String[] a : ws) for (String w : a) df.merge(w, 1, Integer::sum);
        int melhor = -1;
        double me = -1.0;
        for (int i = 0; i < K; i++) {
            double s = 0.0;
            for (String w : ws.get(i)) if (t.contains(w)) s += Math.log((double) K / df.get(w));
            out.println("parte " + partes.get(i) + ": escore = " + Double.toHexString(s));
            if (s > me) { melhor = partes.get(i); me = s; }
        }
        out.println("o texto escolhe a parte " + melhor);
    }
}
