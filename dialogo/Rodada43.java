// Rodada 43 do diálogo Python <-> Java: a forma de GPT decide o próximo caractere. Lê PASTA/gpt43.txt (os pesos que o Python pré-treinou) e faz
// a mesma ida do synthai/gpt.py (atenção causal, resíduo, MLP, softmax), com exp e log próprios (rodada 26), na mesma frase.
// Uso: java Rodada43 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada43 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = Math.sqrt(2.0);
    static final String FRASE = "a domestic animal kept for comp";
    static final int T = 8, D = 8, H = 16;
    static Map<String, double[][]> P = new HashMap<>();
    static String vocab;

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

    static double[] mat(double[] vet, double[][] M, int colunas) {
        double[] out = new double[colunas];
        for (int j = 0; j < colunas; j++) {
            double s = 0.0;
            for (int i = 0; i < vet.length; i++) s += vet[i] * M[i][j];
            out[j] = s;
        }
        return out;
    }

    static double[] softmax(double[] s) {
        double mx = s[0];
        for (double x : s) if (x > mx) mx = x;
        double[] w = new double[s.length];
        for (int i = 0; i < s.length; i++) w[i] = exp_(s[i] - mx);
        double tot = 0.0;
        for (double x : w) tot += x;
        for (int i = 0; i < s.length; i++) w[i] = w[i] / tot;
        return w;
    }

    /** a distribuição do próximo caractere na última posição da janela */
    static double[] adiante(int[] x) {
        int n = x.length, V = vocab.length();
        double esc = 1.0 / Math.sqrt(D);
        double[][] E = P.get("E"), Pp = P.get("P"), Q = P.get("Q"), K = P.get("K"), Vm = P.get("V"), O = P.get("O"), W1 = P.get("W1"), b1 = P.get("b1"),
                W2 = P.get("W2"), U = P.get("U"), c = P.get("c");
        double[][] e = new double[n][D], q = new double[n][], k = new double[n][], v = new double[n][];
        for (int t = 0; t < n; t++) for (int i = 0; i < D; i++) e[t][i] = E[x[t]][i] + Pp[t][i];
        for (int t = 0; t < n; t++) { q[t] = mat(e[t], Q, D); k[t] = mat(e[t], K, D); v[t] = mat(e[t], Vm, D); }
        double[] probs = null;
        for (int t = 0; t < n; t++) {
            double[] s = new double[t + 1];
            for (int j = 0; j <= t; j++) {
                double acc = 0.0;
                for (int i = 0; i < D; i++) acc += q[t][i] * k[j][i];
                s[j] = acc * esc;
            }
            double[] at = softmax(s);
            double[] ot = new double[D];
            for (int j = 0; j <= t; j++) for (int i = 0; i < D; i++) ot[i] += at[j] * v[j][i];
            double[] ut = mat(ot, O, D), rt = new double[D];
            for (int i = 0; i < D; i++) rt[i] = e[t][i] + ut[i];
            double[] pr = mat(rt, W1, H);
            for (int i = 0; i < H; i++) pr[i] = pr[i] + b1[0][i];
            double[] mt = new double[H];
            for (int i = 0; i < H; i++) mt[i] = pr[i] > 0.0 ? pr[i] : 0.0;
            double[] w2 = mat(mt, W2, D), zt = new double[D];
            for (int i = 0; i < D; i++) zt[i] = rt[i] + w2[i];
            double[] lg = mat(zt, U, V);
            for (int i = 0; i < V; i++) lg[i] = lg[i] + c[0][i];
            probs = softmax(lg);
        }
        return probs;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<String> linhas = Files.readAllLines(Path.of(args[0], "gpt43.txt"), StandardCharsets.UTF_8);
        vocab = linhas.get(0);
        int i = 1;
        while (i < linhas.size() && !linhas.get(i).isEmpty()) {
            String[] cab = linhas.get(i).split(" ");
            int n = Integer.parseInt(cab[1]), m = Integer.parseInt(cab[2]);
            double[][] M = new double[n][m];
            for (int r = 0; r < n; r++) {
                String[] xs = linhas.get(i + 1 + r).split(" ");
                for (int j = 0; j < m; j++) M[r][j] = Double.parseDouble(xs[j]);
            }
            P.put(cab[0], M);
            i += 1 + n;
        }
        int[] ids = new int[FRASE.length()];
        for (int t = 0; t < ids.length; t++) { int j = vocab.indexOf(FRASE.charAt(t)); ids[t] = j >= 0 ? j : vocab.indexOf('?'); }
        double bits = 0.0;
        for (int t = 0; t < ids.length - 1; t++) {
            int ini = Math.max(0, t + 1 - T);
            int[] janela = Arrays.copyOfRange(ids, ini, t + 1);
            double[] pr = adiante(janela);
            int melhor = 0;
            for (int j = 1; j < pr.length; j++) if (pr[j] > pr[melhor]) melhor = j;
            bits -= log_(pr[ids[t + 1]]) / log_(2.0);
            out.println("t=" + t + " contexto='" + FRASE.substring(ini, t + 1) + "' argmax='" + vocab.charAt(melhor) + "' p=" + Double.toHexString(pr[melhor])
                        + " p_real=" + Double.toHexString(pr[ids[t + 1]]));
        }
        out.println("bits totais=" + Double.toHexString(bits));
    }
}
