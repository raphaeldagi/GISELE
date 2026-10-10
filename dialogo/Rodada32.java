// Rodada 32 do diálogo Python <-> Java: a primeira diferença no dicionário português. Os lemas de PASTA/lemas32.txt (já em
// ordem de pontos de código, escritos por rodada32.py --preparar): a posição média da primeira letra diferente entre vizinhos
// (por pontos de código) e quantos vizinhos ficam invertidos pela chave portuguesa. Uso: java Rodada32 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.text.Normalizer;
import java.util.*;

public class Rodada32 {
    static String chavePt(String w) {
        return Normalizer.normalize(w, Normalizer.Form.NFD).replaceAll("\\p{M}", "").toLowerCase(Locale.ROOT);
    }

    static int cmpCodigo(String a, String b) {
        int i = 0, j = 0;
        while (i < a.length() && j < b.length()) {
            int ca = a.codePointAt(i), cb = b.codePointAt(j);
            if (ca != cb) return Integer.compare(ca, cb);
            i += Character.charCount(ca);
            j += Character.charCount(cb);
        }
        return Integer.compare(a.length() - i, b.length() - j);
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<String> ws = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "lemas32.txt"), StandardCharsets.UTF_8)) if (!l.isEmpty()) ws.add(l);
        long soma = 0;
        int inv = 0;
        for (int i = 0; i + 1 < ws.size(); i++) {
            int[] a = ws.get(i).codePoints().toArray(), b = ws.get(i + 1).codePoints().toArray();
            int k = 0;
            while (k < a.length && k < b.length && a[k] == b[k]) k++;
            soma += k + 1;
            int c = cmpCodigo(chavePt(ws.get(i)), chavePt(ws.get(i + 1)));
            if (c > 0 || (c == 0 && cmpCodigo(ws.get(i), ws.get(i + 1)) > 0)) inv++;
        }
        int pares = ws.size() - 1;
        out.println("lemas: " + ws.size() + "; pares de vizinhos: " + pares);
        out.println("posicao media da primeira diferenca = " + Double.toHexString((double) soma / pares) + " (soma " + soma + ")");
        out.println("pares invertidos pela ordem portuguesa: " + inv);
    }
}
