// Rodada 48 do diálogo Python <-> Java: escolher experimentos com orçamento. Lê PASTA/mochila48.txt (as 300 instâncias da P1662 que o Python gravou) e calcula,
// como o Python, o ótimo da mochila 0-1 por programação dinâmica e os dois gulosos (por VOI/custo e por H/custo, empates pelo índice). Uso: java Rodada48 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada48 {
    static double guloso(int B, double[] vs, double[] chave, int[] cs) {
        int n = vs.length;
        Integer[] idx = new Integer[n];
        for (int i = 0; i < n; i++) idx[i] = i;
        double[] razao = new double[n];
        for (int i = 0; i < n; i++) razao[i] = -(chave[i] / cs[i]);
        Arrays.sort(idx, (a, b) -> razao[a] != razao[b] ? Double.compare(razao[a], razao[b]) : Integer.compare(a, b));
        int resto = B;
        double total = 0.0;
        for (int i : idx) if (cs[i] <= resto) { resto -= cs[i]; total += vs[i]; }
        return total;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<String> linhas = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "mochila48.txt"), StandardCharsets.UTF_8)) if (!l.isEmpty()) linhas.add(l);
        double so = 0.0, s1 = 0.0, s2 = 0.0;
        int otimos = 0;
        for (int k = 0; k < linhas.size() / 2; k++) {
            int B = Integer.parseInt(linhas.get(2 * k).trim());
            String[] xs = linhas.get(2 * k + 1).split(" ");
            int n = xs.length / 3;
            double[] vs = new double[n], hs = new double[n];
            int[] cs = new int[n];
            for (int i = 0; i < n; i++) { vs[i] = Double.parseDouble(xs[3 * i]); hs[i] = Double.parseDouble(xs[3 * i + 1]); cs[i] = Integer.parseInt(xs[3 * i + 2]); }
            double[] melhor = new double[B + 1];
            for (int i = 0; i < n; i++)
                for (int b = B; b >= cs[i]; b--)
                    if (melhor[b - cs[i]] + vs[i] > melhor[b]) melhor[b] = melhor[b - cs[i]] + vs[i];
            double ot = melhor[B], g1 = guloso(B, vs, vs, cs), g2 = guloso(B, vs, hs, cs);
            so += ot; s1 += g1; s2 += g2;
            if (g1 >= ot - 1e-12) otimos++;
            out.println("instancia " + k + ": otimo " + Double.toHexString(ot) + " guloso_voi " + Double.toHexString(g1) + " guloso_h " + Double.toHexString(g2));
        }
        out.println("totais: otimo " + Double.toHexString(so) + " guloso_voi " + Double.toHexString(s1) + " guloso_h " + Double.toHexString(s2) + " guloso_otimo_em " + otimos);
    }
}
