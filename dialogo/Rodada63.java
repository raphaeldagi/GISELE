// Rodada 63 (Parte 96): conexao residual + normalizacao de camada (LayerNorm), bit a bit. y = x + s(x); mu=media(y); var=media((y-mu)^2);
// out = gamma*(y-mu)/sqrt(var+eps) + beta. TUDO e + - * / e sqrt (exatos no IEEE); NENHUM transcendental (o exp nao aparece).
public class Rodada63 {
    static final int D = 4;
    static final double[] X = {0.5, -1.2, 0.8, 0.3};
    static final double[][] W = {{0.2, -0.1, 0.4, 0.0}, {0.3, 0.5, -0.2, 0.1}, {-0.4, 0.1, 0.6, -0.3}, {0.1, -0.2, 0.0, 0.5}};
    static final double[] B = {0.1, -0.1, 0.2, 0.0};
    static final double[] GAMMA = {1.1, 0.9, 1.0, 1.2};
    static final double[] BETA = {0.0, 0.1, -0.1, 0.05};
    static final double EPS = 1e-5;

    static double[] subcamada(double[] x) {
        double[] out = new double[D];
        for (int i = 0; i < D; i++) {
            double s = 0.0;
            for (int k = 0; k < D; k++) s = s + W[i][k] * x[k];
            out[i] = s + B[i];
        }
        return out;
    }

    public static void main(String[] args) {
        double[] s = subcamada(X);
        double[] y = new double[D];
        for (int i = 0; i < D; i++) y[i] = X[i] + s[i];
        double soma = 0.0;
        for (double v : y) soma = soma + v;
        double mu = soma / D;
        double sq = 0.0;
        for (double v : y) sq = sq + (v - mu) * (v - mu);
        double var = sq / D;
        double inv = 1.0 / Math.sqrt(var + EPS);
        double[] out = new double[D];
        for (int i = 0; i < D; i++) out[i] = GAMMA[i] * ((y[i] - mu) * inv) + BETA[i];
        for (int i = 0; i < D; i++) System.out.println("out " + i + " " + Double.toHexString(out[i]));
        System.out.println("fim");
    }
}
