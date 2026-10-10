// Rodada 30 do diálogo Python <-> Java: os empates nas escolhas das rodadas antigas. Lê PASTA/valores30.txt (rodada, grupo,
// valores em hexadecimal, escrito por rodada30.py --preparar) e conta, por rodada, os pares de vizinhos com o MESMO valor
// bit a bit. Uso: java Rodada30 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada30 {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        TreeMap<String, Integer> por = new TreeMap<>();
        for (String l : Files.readAllLines(Path.of(args[0], "valores30.txt"), StandardCharsets.US_ASCII)) {
            if (l.isEmpty()) continue;
            String[] c = l.split("\t");
            String[] vs = c[2].split(" ");
            int e = 0;
            for (int i = 0; i + 1 < vs.length; i++) {
                double a = Double.parseDouble(vs[i]), b = Double.parseDouble(vs[i + 1]);
                if (a == b) e++;
            }
            por.merge(c[0], e, Integer::sum);
        }
        int com = 0;
        for (Map.Entry<String, Integer> x : por.entrySet()) {
            out.println("rodada" + x.getKey() + ": " + x.getValue() + " empates");
            if (x.getValue() > 0) com++;
        }
        out.println("rodadas com empate na escolha impressa: " + com + " de " + por.size());
    }
}
