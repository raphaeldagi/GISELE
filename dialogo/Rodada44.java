// Rodada 44 do diálogo Python <-> Java: a lei de escala da forma de GPT, por álgebra (equações normais em log-log, log e exp próprios da rodada 26).
// Lê dialogo/escala44.tsv. Uso (da raiz do repositório): java Rodada44
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada44 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = Math.sqrt(2.0);
    static final double TRIGRAMA = 2.768;

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
        TreeMap<Integer, List<double[]>> pontos = new TreeMap<>();
        for (String linha : Files.readAllLines(Path.of("dialogo", "escala44.tsv"), StandardCharsets.UTF_8)) {
            if (linha.isBlank()) continue;
            String[] c = linha.trim().split("\\s+");
            pontos.computeIfAbsent(Integer.parseInt(c[0]), k -> new ArrayList<>()).add(new double[]{Integer.parseInt(c[1]), Double.parseDouble(c[2])});
        }
        for (Map.Entry<Integer, List<double[]>> en : pontos.entrySet()) {
            List<double[]> pts = en.getValue();
            int k = pts.size();
            double sx = 0.0, sy = 0.0;
            for (double[] p : pts) { sx += log_(p[0]); sy += log_(p[1]); }
            double mx = sx / k, my = sy / k, sxx = 0.0, sxy = 0.0;
            for (double[] p : pts) { double x = log_(p[0]) - mx, y = log_(p[1]) - my; sxx += x * x; sxy += x * y; }
            double alfa = -(sxy / sxx);
            double A = exp_(my + alfa * mx);
            double ne = exp_((log_(A) - log_(TRIGRAMA)) / alfa);
            out.println("d=" + en.getKey() + " pontos=" + k + " A=" + Double.toHexString(A) + " alfa=" + Double.toHexString(alfa) + " n_estrela=" + Double.toHexString(ne));
        }
        double b24 = 0, b48 = 0;
        for (double[] p : pontos.get(24)) if (p[0] == 8000) b24 = p[1];
        for (double[] p : pontos.get(48)) if (p[0] == 8000) b48 = p[1];
        out.println("bits(d=48) - bits(d=24) em 8000 passos = " + Double.toHexString(b48 - b24));
    }
}
