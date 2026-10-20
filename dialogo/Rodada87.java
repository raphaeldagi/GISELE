// Rodada 87 (Parte 121): a regressao logistica do experimento do angulo duplo do NEXUS-RAPHAEL 2.2.0, bit a bit. Dados de um LCG inteiro
// (u em [-1,1) no papel de cos t; 2u^2 - 1 no de cos 2t; y = 1 se u^2 > 0,49), descida do gradiente (0,8; 300 passos), exp_ proprio.
public class Rodada87 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final int N = 200, PASSOS = 300;
    static final double TAXA = 0.8;
    static double[][] D = new double[N][3];

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double sigmoide(double z) {
        if (z >= 0.0) return 1.0 / (1.0 + exp_(-z));
        double e = exp_(z);
        return e / (1.0 + e);
    }

    static String treinar(boolean duplo) {
        double[] w = {0.0, 0.0, 0.0};
        for (int it = 0; it < PASSOS; it++) {
            double[] g = {0.0, 0.0, 0.0};
            for (int i = 0; i < N; i++) {
                double u = D[i][0], c2 = D[i][1], y = D[i][2];
                double z = w[0] + w[1] * u + (duplo ? w[2] * c2 : 0.0);
                double r = sigmoide(z) - y;
                g[0] += r;
                g[1] += r * u;
                if (duplo) g[2] += r * c2;
            }
            for (int i = 0; i < 3; i++) w[i] = w[i] - TAXA * (g[i] / N);
        }
        double brier = 0.0;
        for (int i = 0; i < N; i++) {
            double p = sigmoide(w[0] + w[1] * D[i][0] + (duplo ? w[2] * D[i][1] : 0.0));
            brier += (p - D[i][2]) * (p - D[i][2]);
        }
        StringBuilder sb = new StringBuilder(duplo ? "duplo" : "simples");
        for (double v : w) sb.append(" ").append(Double.toHexString(v));
        sb.append(" brier ").append(Double.toHexString(brier / N));
        return sb.toString();
    }

    public static void main(String[] args) {
        long x = 1210;
        for (int i = 0; i < N; i++) {
            x = (1103515245L * x + 12345L) % 2147483648L;
            double u = (x / 2147483648.0) * 2.0 - 1.0;
            D[i][0] = u;
            D[i][1] = 2.0 * u * u - 1.0;
            D[i][2] = u * u > 0.49 ? 1.0 : 0.0;
        }
        System.out.println(treinar(false) + "\n" + treinar(true) + "\nfim");
    }
}
