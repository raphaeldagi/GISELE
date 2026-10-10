// Rodada 33 do diálogo Python <-> Java: o nome próprio e a palavra comum. Dos lemas de PASTA/lemas33.txt (em ordem de pontos de
// código) que começam com maiúscula, quantos têm uma irmã com a mesma grafia em minúsculas. Uso: java Rodada33 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada33 {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<String> ws = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "lemas33.txt"), StandardCharsets.UTF_8)) if (!l.isEmpty()) ws.add(l);
        Set<String> conj = new HashSet<>(ws);
        int n = 0;
        List<String> com = new ArrayList<>();
        for (String w : ws) {
            if (!Character.isUpperCase(w.codePointAt(0))) continue;
            n++;
            String m = w.toLowerCase(Locale.ROOT);
            if (conj.contains(m) && !m.equals(w)) com.add(w);
        }
        out.println("com maiuscula: " + n + "; com irma minuscula: " + com.size() + "; fracao = " + Double.toHexString((double) com.size() / n));
        out.println("exemplos: " + String.join(" ", com.subList(0, Math.min(12, com.size()))));
    }
}
