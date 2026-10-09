// Rodada 29 do diálogo Python <-> Java: o ulp que chega à saída. Para cada par de saídas (normal e com um ulp em cada exp e
// log) em dialogo/saidas29/: quantos números hexadecimais, a maior mudança relativa |u - v|/|u| e se o texto fora dos números
// mudou. Uso: java Rodada29 PASTA (lê a partir da raiz do repositório)
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class Rodada29 {
    static final Pattern HEX = Pattern.compile("-?0x[0-9a-fA-F]+(?:\\.[0-9a-fA-F]*)?p[+-]?[0-9]+");

    static List<String> numeros(String s) {
        List<String> r = new ArrayList<>();
        Matcher m = HEX.matcher(s);
        while (m.find()) r.add(m.group());
        return r;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        String[] rodadas = {"06", "09", "14", "18", "19", "20", "21", "22", "23", "24", "25", "26"};
        for (String r : rodadas) {
            String[] la = Files.readString(Path.of("dialogo", "saidas29", "normal" + r + ".txt"), StandardCharsets.UTF_8).split("\n", -1);
            String[] lb = Files.readString(Path.of("dialogo", "saidas29", "perturbada" + r + ".txt"), StandardCharsets.UTF_8).split("\n", -1);
            boolean texto = la.length != lb.length;
            int n = 0;
            double m = 0.0;
            for (int i = 0; i < Math.min(la.length, lb.length); i++) {
                if (!HEX.matcher(la[i]).replaceAll("#").equals(HEX.matcher(lb[i]).replaceAll("#"))) texto = true;
                List<String> nu = numeros(la[i]), nv = numeros(lb[i]);
                for (int k = 0; k < Math.min(nu.size(), nv.size()); k++) {
                    double u = Double.parseDouble(nu.get(k)), v = Double.parseDouble(nv.get(k));
                    n++;
                    if (u != v) { double rr = Math.abs(u - v) / Math.abs(u); if (rr > m) m = rr; }
                }
            }
            out.println("rodada" + r + ": " + n + " numeros; maior mudanca relativa = " + Double.toHexString(m) + "; texto " + (texto ? "mudou" : "igual"));
        }
    }
}
