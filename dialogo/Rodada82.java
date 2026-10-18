// Rodada 82 (Parte 115): as dez camadas contrapostas (a, 1/a, ..., a = 2), tanh pelo exp proprio, frente e tras: o gradiente de ponta a ponta e
// os dez gradientes sobrepostos dh10/dw_k. Bit a bit. O exp_ e copia exata do de dialogo/exatas.py (regra da Parte 76).
public class Rodada82 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final int N = 10;
    static final double A = 2.0, H0 = 0.5;

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double tanh_(double x) {
        double e = exp_(2.0 * x);
        return (e - 1.0) / (e + 1.0);
    }

    public static void main(String[] args) {
        double[] w = new double[N];
        for (int k = 0; k < N; k++) w[k] = (k % 2 == 0) ? A : 1.0 / A;
        double[] hs = new double[N + 1];
        hs[0] = H0;
        for (int k = 0; k < N; k++) hs[k + 1] = tanh_(w[k] * hs[k]);
        double g = 1.0;
        double[] gw = new double[N];
        for (int k = N - 1; k >= 0; k--) {
            double d = 1.0 - hs[k + 1] * hs[k + 1];
            gw[k] = g * d * hs[k];
            g = g * d * w[k];
        }
        StringBuilder sb = new StringBuilder();
        sb.append("h10 ").append(Double.toHexString(hs[N])).append("\n");
        sb.append("dh10/dh0 ").append(Double.toHexString(g)).append("\n");
        sb.append("dh10/dw");
        for (int k = 0; k < N; k++) sb.append(" ").append(Double.toHexString(gw[k]));
        sb.append("\nfim");
        System.out.println(sb.toString());
    }
}
