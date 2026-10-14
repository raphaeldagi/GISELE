// Rodada 62 (Parte 95): o passo de atualizacao do EWC, bit a bit. sigmoide = 1/(1+exp(-z)) com o EXP PROPRIO (fronteira da Parte 52);
// w_i <- w_i - lr*(erro*x_i + lam*F_i*(w_i-w0_i)). O resto e so +-*. Pesos e entrada fixos.
public class Rodada62 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final double LR = 0.025, LAM = 0.2;
    static final double[] W = {0.4, -0.3, 0.2, 0.1};
    static final double[] W0 = {0.5, -0.2, 0.1, 0.0};
    static final double[] FISHER = {10.0, 0.1, 2.0, 0.5};
    static final double[] X = {1.3, 0.7, 1.0, 1.0};
    static final double ROTULO = 1.0;

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double sigmoide(double z) {
        double zc = Math.max(-15.0, Math.min(15.0, z));
        return 1.0 / (1.0 + exp_(-zc));
    }

    static double pCatInicial() {
        double z = 0.0;
        for (int i = 0; i < W.length; i++) z = z + W[i] * X[i];
        return sigmoide(z);
    }

    public static void main(String[] args) {
        double pred = pCatInicial();
        System.out.println("p_cat " + Double.toHexString(pred));
        double erro = pred - ROTULO;
        double[] novo = new double[W.length];
        for (int i = 0; i < W.length; i++) {
            double g = erro * X[i] + LAM * FISHER[i] * (W[i] - W0[i]);
            novo[i] = W[i] - LR * g;
        }
        for (int i = 0; i < novo.length; i++) System.out.println("w " + i + " " + Double.toHexString(novo[i]));
        System.out.println("fim");
    }
}
