// Rodada 47 do diálogo Python <-> Java: quanto vale perguntar. Lê PASTA/voi47.txt (os 2.000 problemas de decisão da P1632) e calcula, como o Python, o valor
// da informação perfeita e a prioridade S(q) do texto recebido na Parte 73 (H com o log_ próprio: só + − × ÷ e escalas por 2^k). Uso: java Rodada47 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada47 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;

    static double log_(double x) {
        int e = Math.getExponent(x);
        double m = Math.scalb(x, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    static Integer[] topo(double[] chave, int k) {
        Integer[] idx = new Integer[chave.length];
        for (int i = 0; i < idx.length; i++) idx[i] = i;
        Arrays.sort(idx, (a, b) -> chave[a] != chave[b] ? Double.compare(chave[b], chave[a]) : Integer.compare(a, b));
        return Arrays.copyOf(idx, k);
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<double[]> linhas = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "voi47.txt"), StandardCharsets.UTF_8)) {
            if (l.isEmpty()) continue;
            String[] xs = l.split(" ");
            double[] v = new double[5];
            for (int k = 0; k < 5; k++) v[k] = Double.parseDouble(xs[k]);
            linhas.add(v);
        }
        int n = linhas.size();
        double ln2 = log_(2.0);
        double[] voi = new double[n], s = new double[n];
        for (int i = 0; i < n; i++) {
            double[] x = linhas.get(i);
            double p = x[0], u00 = x[1], u01 = x[2], u10 = x[3], u11 = x[4];
            double com = p * Math.max(u01, u11) + (1.0 - p) * Math.max(u00, u10);
            double sem = Math.max(p * u01 + (1.0 - p) * u00, p * u11 + (1.0 - p) * u10);
            double v = com - sem;
            if (v < 0.0) v = 0.0;
            double h = 0.0;
            for (double q : new double[]{p, 1.0 - p}) if (q > 0.0) h -= q * log_(q) / ln2;
            voi[i] = v;
            s[i] = h + Math.max(Math.abs(u00 - u10), Math.abs(u01 - u11)) + 1.0;
        }
        double sv = 0.0, ss = 0.0;
        int zero = 0;
        for (int i = 0; i < n; i++) { sv += voi[i]; ss += s[i]; if (voi[i] == 0.0) zero++; }
        Integer[] ts = topo(s, 200), tv = topo(voi, 200);
        double mts = 0.0, mtv = 0.0;
        int zt = 0;
        for (int i : ts) { mts += voi[i]; if (voi[i] == 0.0) zt++; }
        for (int i : tv) mtv += voi[i];
        out.println("n=" + n + " voi_zero=" + zero + " soma_voi=" + Double.toHexString(sv) + " soma_s=" + Double.toHexString(ss));
        out.println("topo_s_voi_zero=" + zt + " voi_medio_topo_voi=" + Double.toHexString(mtv / 200) + " voi_medio_topo_s=" + Double.toHexString(mts / 200));
    }
}
