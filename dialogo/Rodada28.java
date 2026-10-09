// Rodada 28 do diálogo Python <-> Java: exatidão ou sorte? A chance de cada rodada antiga passar por sorte com outra libm,
// P = exp(n_exp ln(1 - 0,0029) + n_log ln(1 - 0,0007)), a partir de dialogo/contagens28.tsv, com o exp e o log próprios
// da Rodada 26. Uso: java Rodada28 PASTA (lê o arquivo a partir da raiz do repositório)
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada28 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double log_(double x) {
        int e = Math.getExponent(x);
        double m = Math.scalb(x, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<String> linhas = Files.readAllLines(Path.of("dialogo", "contagens28.tsv"), StandardCharsets.US_ASCII);
        int sorte = 0;
        for (int i = 1; i < linhas.size(); i++) {
            String[] c = linhas.get(i).split("\t");
            int e = Integer.parseInt(c[1]), g = Integer.parseInt(c[2]), p = Integer.parseInt(c[3]);
            double ch = exp_(e * log_(1.0 - 0.0029) + g * log_(1.0 - 0.0007));
            if (ch < 0.5) sorte++;
            out.println(c[0] + ": exp " + e + ", log " + g + ", pow " + p + "; chance de passar por sorte = " + Double.toHexString(ch));
        }
        out.println("rodadas com chance < 0,5: " + sorte);
    }
}
