// Rodada 75 (Parte 108): o minimax de um jogo de soma zero, bit a bit. Forma fechada + jogo ficticio (argmax + media corrente). So +,-,*,/,
// argmax e comparacoes - nenhuma transcendental, portavel por construcao (Parte 52).
public class Rodada75 {
    static final double[][] A = {{1.0, -1.0}, {-2.0, 3.0}};
    static final int ITER = 500;

    static double[] valorFechado() {
        double a = A[0][0], b = A[0][1], c = A[1][0], d = A[1][1];
        double den = a + d - b - c;
        return new double[]{(a * d - b * c) / den, (d - c) / den, (d - b) / den};
    }

    static double ficticio(int iteracoes) {
        int m = 2, n = 2;
        int[] cl = {0, 0}, cc = {0, 0};
        double[] gcol = {0.0, 0.0}, glin = {0.0, 0.0};
        cl[0] += 1;
        for (int j = 0; j < n; j++) gcol[j] += A[0][j];
        double vs = 0.0, vi = 0.0;
        for (int it = 0; it < iteracoes; it++) {
            int jc = 0;
            for (int j = 1; j < n; j++) if (gcol[j] < gcol[jc]) jc = j;
            cc[jc] += 1;
            for (int i = 0; i < m; i++) glin[i] += A[i][jc];
            int il = 0;
            for (int i = 1; i < m; i++) if (glin[i] > glin[il]) il = i;
            cl[il] += 1;
            for (int j = 0; j < n; j++) gcol[j] += A[il][j];
            int tl = cl[0] + cl[1], tc = cc[0] + cc[1];
            vs = Math.max(glin[0], glin[1]) / tc;
            vi = Math.min(gcol[0], gcol[1]) / tl;
        }
        return (vs + vi) / 2.0;
    }

    public static void main(String[] args) {
        double[] vpq = valorFechado();
        StringBuilder sb = new StringBuilder();
        sb.append("valor ").append(Double.toHexString(vpq[0])).append("\n");
        sb.append("p ").append(Double.toHexString(vpq[1])).append("\n");
        sb.append("q ").append(Double.toHexString(vpq[2])).append("\n");
        sb.append("ficticio ").append(Double.toHexString(ficticio(ITER))).append("\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
