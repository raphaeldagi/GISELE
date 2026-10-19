// Rodada 84 (Parte 117): as camadas contrapostas com MATRIZES. W (4x4, LCG inteiro) e W^-1 (Gauss-Jordan com pivo parcial) alternadas em 10
// camadas; o produto J e o seu desvio da identidade. So + - * / na mesma ordem. Bit a bit.
public class Rodada84 {
    static final int D = 4, L = 10;

    static double[][] matriz() {
        long x = 117;
        double[][] W = new double[D][D];
        for (int i = 0; i < D; i++)
            for (int j = 0; j < D; j++) {
                x = (1103515245L * x + 12345L) % 2147483648L;
                W[i][j] = ((x % 2001) - 1000) / 500.0;
            }
        return W;
    }

    static double[][] inversa(double[][] A) {
        int d = A.length;
        double[][] M = new double[d][2 * d];
        for (int i = 0; i < d; i++) {
            for (int j = 0; j < d; j++) M[i][j] = A[i][j];
            for (int j = 0; j < d; j++) M[i][d + j] = (i == j) ? 1.0 : 0.0;
        }
        for (int c = 0; c < d; c++) {
            int p = c;
            for (int r = c + 1; r < d; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
            double[] t = M[c]; M[c] = M[p]; M[p] = t;
            double piv = M[c][c];
            for (int j = 0; j < 2 * d; j++) M[c][j] = M[c][j] / piv;
            for (int r = 0; r < d; r++) {
                if (r != c) {
                    double f = M[r][c];
                    if (f != 0.0) for (int j = 0; j < 2 * d; j++) M[r][j] = M[r][j] - f * M[c][j];
                }
            }
        }
        double[][] R = new double[d][d];
        for (int i = 0; i < d; i++) for (int j = 0; j < d; j++) R[i][j] = M[i][d + j];
        return R;
    }

    static double[][] matmul(double[][] A, double[][] B) {
        double[][] C = new double[D][D];
        for (int i = 0; i < D; i++)
            for (int k = 0; k < D; k++) {
                double a = A[i][k];
                if (a != 0.0) for (int j = 0; j < D; j++) C[i][j] += a * B[k][j];
            }
        return C;
    }

    public static void main(String[] args) {
        double[][] W = matriz(), Wi = inversa(W);
        double[][] J = new double[D][D];
        for (int i = 0; i < D; i++) J[i][i] = 1.0;
        for (int k = 0; k < L; k++) J = matmul(k % 2 == 0 ? W : Wi, J);
        double desvio = 0.0;
        for (int i = 0; i < D; i++)
            for (int j = 0; j < D; j++) {
                double e = Math.abs(J[i][j] - (i == j ? 1.0 : 0.0));
                if (e > desvio) desvio = e;
            }
        StringBuilder sb = new StringBuilder("Winv");
        for (double[] l : Wi) for (double v : l) sb.append(" ").append(Double.toHexString(v));
        sb.append("\nJ");
        for (double[] l : J) for (double v : l) sb.append(" ").append(Double.toHexString(v));
        sb.append("\ndesvio ").append(Double.toHexString(desvio)).append("\nfim");
        System.out.println(sb.toString());
    }
}
