// Rodada 45 do diálogo Python <-> Java: os autovalores da atenção. Lê PASTA/qk45.txt (W_Q e W_K que o Python pré-treinou), calcula M = W_Q W_Kᵀ, MᵀM,
// os autovalores por Jacobi clássico (só + − × ÷ e √, na mesma ordem do Python) e a razão de participação. Uso: java Rodada45 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada45 {
    static double[] jacobi(double[][] S, int varreduras) {
        int n = S.length;
        double[][] A = new double[n][];
        for (int i = 0; i < n; i++) A[i] = S[i].clone();
        for (int v = 0; v < varreduras; v++) {
            double fora = 0.0;
            for (int p = 0; p < n; p++) for (int q = p + 1; q < n; q++) fora += A[p][q] * A[p][q];
            if (fora == 0.0) break;
            for (int p = 0; p < n; p++) for (int q = p + 1; q < n; q++) {
                if (A[p][q] == 0.0) continue;
                double tau = (A[q][q] - A[p][p]) / (2.0 * A[p][q]);
                double t = (tau >= 0.0 ? 1.0 : -1.0) / (Math.abs(tau) + Math.sqrt(tau * tau + 1.0));
                double c = 1.0 / Math.sqrt(t * t + 1.0), s = t * c;
                for (int k = 0; k < n; k++) { double akp = A[k][p], akq = A[k][q]; A[k][p] = c * akp - s * akq; A[k][q] = s * akp + c * akq; }
                for (int k = 0; k < n; k++) { double apk = A[p][k], aqk = A[q][k]; A[p][k] = c * apk - s * aqk; A[q][k] = s * apk + c * aqk; }
            }
        }
        double[] diag = new double[n];
        for (int i = 0; i < n; i++) diag[i] = A[i][i];
        Arrays.sort(diag);
        double[] dec = new double[n];
        for (int i = 0; i < n; i++) dec[i] = diag[n - 1 - i];
        return dec;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<String> linhas = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "qk45.txt"), StandardCharsets.UTF_8)) if (!l.isEmpty()) linhas.add(l);
        int d = linhas.size() / 2;
        double[][] Q = new double[d][d], K = new double[d][d];
        for (int i = 0; i < d; i++) {
            String[] a = linhas.get(i).split(" "), b = linhas.get(d + i).split(" ");
            for (int j = 0; j < d; j++) { Q[i][j] = Double.parseDouble(a[j]); K[i][j] = Double.parseDouble(b[j]); }
        }
        double[][] M = new double[d][d], MtM = new double[d][d];
        for (int i = 0; i < d; i++) for (int j = 0; j < d; j++) { double s = 0.0; for (int k = 0; k < d; k++) s += Q[i][k] * K[j][k]; M[i][j] = s; }
        for (int i = 0; i < d; i++) for (int j = 0; j < d; j++) { double s = 0.0; for (int k = 0; k < d; k++) s += M[k][i] * M[k][j]; MtM[i][j] = s; }
        double[] lam = jacobi(MtM, 60);
        for (int i = 0; i < d; i++) if (!(lam[i] > 0.0)) lam[i] = 0.0;
        double s2 = 0.0, s4 = 0.0;
        for (double x : lam) { s2 += x; s4 += x * x; }
        StringBuilder sb = new StringBuilder("autovalores de MtM:");
        for (double x : lam) sb.append(" ").append(Double.toHexString(x));
        out.println(sb);
        out.println("PR=" + Double.toHexString(s2 * s2 / s4) + " fracao_maior=" + Double.toHexString(lam[0] / s2));
    }
}
