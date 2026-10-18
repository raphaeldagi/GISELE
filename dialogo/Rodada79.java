// Rodada 79 (Parte 112): o simplex proprio (regra de Bland) num jogo de soma zero 4x5, bit a bit. A fixture: entradas (x mod 11) - 5, LCG a
// partir de 112. Coluna: max soma w s.a. A w <= 1; linha pelos precos duais. So +,-,*,/ e comparacoes.
public class Rodada79 {
    static final int N = 4, M = 5;

    public static void main(String[] args) {
        double[][] A = new double[N][M];
        long x = 112;
        for (int i = 0; i < N; i++)
            for (int j = 0; j < M; j++) {
                x = (1103515245L * x + 12345L) % 2147483648L;
                A[i][j] = (double) (x % 11 - 5);
            }
        double menor = A[0][0];
        for (double[] l : A) for (double v : l) if (v < menor) menor = v;
        double desloc = menor <= 0.0 ? 1.0 - menor : 0.0;
        int C = M + N + 1;
        double[][] T = new double[N][C];
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) T[i][j] = A[i][j] + desloc;
            for (int k = 0; k < N; k++) T[i][M + k] = (k == i) ? 1.0 : 0.0;
            T[i][M + N] = 1.0;
        }
        double[] obj = new double[C];
        for (int j = 0; j < M; j++) obj[j] = -1.0;
        int[] base = new int[N];
        for (int i = 0; i < N; i++) base[i] = M + i;
        int pivos = 0;
        while (true) {
            int entra = -1;
            for (int j = 0; j < M + N; j++) if (obj[j] < 0.0) { entra = j; break; }
            if (entra < 0) break;
            int sai = -1;
            double melhor = 0.0;
            for (int i = 0; i < N; i++) {
                if (T[i][entra] > 0.0) {
                    double razao = T[i][M + N] / T[i][entra];
                    if (sai < 0 || razao < melhor || (razao == melhor && base[i] < base[sai])) { sai = i; melhor = razao; }
                }
            }
            double p = T[sai][entra];
            for (int j = 0; j < C; j++) T[sai][j] = T[sai][j] / p;
            for (int i = 0; i < N; i++) {
                if (i != sai && T[i][entra] != 0.0) {
                    double f = T[i][entra];
                    for (int j = 0; j < C; j++) T[i][j] = T[i][j] - f * T[sai][j];
                }
            }
            double f = obj[entra];
            for (int j = 0; j < C; j++) obj[j] = obj[j] - f * T[sai][j];
            base[sai] = entra;
            pivos++;
        }
        double[] w = new double[M];
        for (int i = 0; i < N; i++) if (base[i] < M) w[base[i]] = T[i][M + N];
        double vd = 1.0 / obj[M + N];
        StringBuilder sb = new StringBuilder();
        sb.append("valor ").append(Double.toHexString(vd - desloc)).append("\n");
        sb.append("p");
        for (int i = 0; i < N; i++) sb.append(" ").append(Double.toHexString(obj[M + i] * vd));
        sb.append("\nq");
        for (int j = 0; j < M; j++) sb.append(" ").append(Double.toHexString(w[j] * vd));
        sb.append("\npivos ").append(pivos).append("\nfim");
        System.out.println(sb.toString());
    }
}
