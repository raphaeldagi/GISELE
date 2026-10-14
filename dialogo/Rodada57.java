// Rodada 57 (Parte 90): uma rede de Izhikevich acoplada que APRENDE por STDP, bit a bit. Pesos W mudam pela ordem dos disparos, com o exp PROPRIO (o mesmo de
// exatas.py). Mesma ordem de somas e de atualizacoes do rodada57.py. So +,-,* e exp_.
public class Rodada57 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final int N = 6, PASSOS = 300;
    static final double DT = 0.5, I_EXT = 5.0, A_MAIS = 0.002, A_MENOS = 0.0022, TAU = 20.0, WMAX = 1.0;
    static final double[][] W0 = {
        {0.0, 0.3, 0.0, 0.0, 0.2, 0.0},
        {0.0, 0.0, 0.4, 0.0, 0.0, 0.0},
        {0.2, 0.0, 0.0, 0.3, 0.0, 0.0},
        {0.0, 0.0, 0.0, 0.0, 0.5, 0.0},
        {0.0, 0.0, 0.0, 0.0, 0.0, 0.3},
        {0.4, 0.0, 0.0, 0.0, 0.0, 0.0}};

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    public static void main(String[] args) {
        double[] v = new double[N], u = new double[N], ult = new double[N];
        int[] disparou = new int[N];
        double[][] W = new double[N][N];
        for (int i = 0; i < N; i++) {
            v[i] = -65.0; u[i] = 0.2 * -65.0; disparou[i] = 0; ult[i] = -1.0e9;
            for (int j = 0; j < N; j++) W[i][j] = W0[i][j];
        }
        int total = 0;
        for (int k = 0; k < PASSOS; k++) {
            double t = k * DT;
            double[] correntes = new double[N];
            for (int i = 0; i < N; i++) {
                double acopl = 0.0;
                for (int j = 0; j < N; j++) acopl = acopl + W[i][j] * disparou[j];
                correntes[i] = I_EXT + acopl;
            }
            int[] novoDisp = new int[N];
            for (int i = 0; i < N; i++) {
                double ii = correntes[i];
                v[i] = v[i] + (DT / 2.0) * (0.04 * v[i] * v[i] + 5.0 * v[i] + 140.0 - u[i] + ii);
                v[i] = v[i] + (DT / 2.0) * (0.04 * v[i] * v[i] + 5.0 * v[i] + 140.0 - u[i] + ii);
                u[i] = u[i] + DT * 0.02 * (0.2 * v[i] - u[i]);
                if (v[i] >= 30.0) { v[i] = -65.0; u[i] = u[i] + 8.0; novoDisp[i] = 1; total = total + 1; }
            }
            for (int i = 0; i < N; i++) {
                if (novoDisp[i] == 1) {
                    for (int j = 0; j < N; j++) {
                        if (W0[i][j] > 0.0 && ult[j] > -1.0e8) {
                            double d = t - ult[j];
                            if (0.0 <= d) { double nw = W[i][j] + A_MAIS * exp_(-d / TAU); W[i][j] = nw < WMAX ? nw : WMAX; }
                        }
                    }
                    for (int kk = 0; kk < N; kk++) {
                        if (W0[kk][i] > 0.0 && ult[kk] > -1.0e8) {
                            double d = ult[kk] - t;
                            double nw = W[kk][i] - A_MENOS * exp_(d / TAU); W[kk][i] = nw > 0.0 ? nw : 0.0;
                        }
                    }
                    ult[i] = t;
                }
            }
            disparou = novoDisp;
            for (int i = 0; i < N; i++) System.out.println("passo " + k + " n " + i + " v " + Double.toHexString(v[i]));
        }
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++)
                if (W0[i][j] > 0.0) System.out.println("W " + i + " " + j + " " + Double.toHexString(W[i][j]));
        System.out.println("disparos: " + total);
    }
}
