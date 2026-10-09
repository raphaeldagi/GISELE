// Rodada 27 do diálogo Python <-> Java: o preditor de mim mesma (p1032): para cada medida do histórico congelado em
// dialogo/historico27.tsv, o centro (média das últimas 8 partes com valor) e a meia-largura (1,645 × desvio padrão
// amostral), com laços simples e Math.sqrt. Uso: java Rodada27 PASTA (lê o arquivo a partir da raiz do repositório)
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada27 {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<String> linhas = Files.readAllLines(Path.of("dialogo", "historico27.tsv"), StandardCharsets.US_ASCII);
        String[] nomes = linhas.get(0).split("\t");
        String[] ordem = {"caracteres", "compressao", "testes_unidade", "testes", "erros", "redundancia"};
        for (String medida : ordem) {
            int col = Arrays.asList(nomes).indexOf(medida);
            List<Double> vals = new ArrayList<>();
            for (int i = 1; i < linhas.size(); i++) {
                String[] c = linhas.get(i).split("\t");
                if (!c[col].equals("-")) vals.add(Double.parseDouble(c[col]));
            }
            List<Double> ult = vals.subList(Math.max(0, vals.size() - 8), vals.size());
            double t = 0.0;
            for (double v : ult) t += v;
            double m = t / ult.size(), q = 0.0;
            for (double v : ult) q += (v - m) * (v - m);
            double w = 1.645 * Math.sqrt(q / (ult.size() - 1));
            out.println(medida + ": centro = " + Double.toHexString(m) + "; meia-largura = " + Double.toHexString(w)
                    + "; ingenuo = " + Double.toHexString(ult.get(ult.size() - 1)));
        }
    }
}
