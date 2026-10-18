// Rodada 81 (Parte 114): a rede LINEAR profunda treinada por GD, bit a bit. d = 3, h = 4, n = 50 e a inicializacao por um LCG inteiro;
// 500 passos, lr 0.02; imprime beta = W2 W1. So +,-,*,/ em lacos sequenciais.
public class Rodada81 {
    static final int D = 3, H = 4, N = 50, PASSOS = 500;
    static final double LR = 0.02;

    static long lcg(long x) {
        return (x * 1103515245L + 12345L) % 2147483648L;
    }

    public static void main(String[] args) {
        double[][] X = new double[N][D];
        double[] y = new double[N];
        long x = 81;
        for (int i = 0; i < N; i++) {
            x = lcg(x); double a = (double) (x % 2001 - 1000) / 1000.0;
            x = lcg(x); double b = (double) (x % 2001 - 1000) / 1000.0;
            x = lcg(x); double ruido = (double) (x % 201 - 100) / 1000.0;
            X[i][0] = a; X[i][1] = b; X[i][2] = 1.0;
            y[i] = 0.7 * a - 0.3 * b + 0.1 + ruido;
        }
        double[][] W1 = new double[H][D];
        double[] W2 = new double[H];
        for (int k = 0; k < H; k++) for (int j = 0; j < D; j++) { x = lcg(x); W1[k][j] = (double) (x % 201 - 100) / 1000.0; }
        for (int k = 0; k < H; k++) { x = lcg(x); W2[k] = (double) (x % 201 - 100) / 1000.0; }
        for (int p = 0; p < PASSOS; p++) {
            double[][] g1 = new double[H][D];
            double[] g2 = new double[H];
            for (int i = 0; i < N; i++) {
                double[] a = new double[H];
                for (int k = 0; k < H; k++) {
                    double s = 0.0;
                    for (int j = 0; j < D; j++) s = s + W1[k][j] * X[i][j];
                    a[k] = s;
                }
                double r = 0.0;
                for (int k = 0; k < H; k++) r = r + W2[k] * a[k];
                r = r - y[i];
                for (int k = 0; k < H; k++) {
                    g2[k] = g2[k] + 2.0 * r * a[k] / N;
                    for (int j = 0; j < D; j++) g1[k][j] = g1[k][j] + 2.0 * r * W2[k] * X[i][j] / N;
                }
            }
            for (int k = 0; k < H; k++) {
                W2[k] = W2[k] - LR * g2[k];
                for (int j = 0; j < D; j++) W1[k][j] = W1[k][j] - LR * g1[k][j];
            }
        }
        StringBuilder sb = new StringBuilder("beta");
        for (int j = 0; j < D; j++) {
            double s = 0.0;
            for (int k = 0; k < H; k++) s = s + W2[k] * W1[k][j];
            sb.append(" ").append(Double.toHexString(s));
        }
        sb.append("\nfim");
        System.out.println(sb.toString());
    }
}
