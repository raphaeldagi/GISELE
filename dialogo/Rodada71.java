// Rodada 71 (Parte 104): a codificacao posicional senoidal, bit a bit. Dois blocos: 'proprio' (seno/cosseno proprios, serie de Taylor) e
// 'naive' (Math.sin/Math.cos da libm). O proprio deve ser IGUAL; o naive mostra se a libm difere entre as linguas (6a face da fronteira da Parte 52).
public class Rodada71 {
    static final double PI2_HI = 6.283185307179586, PI2_LO = 2.4492935982947064e-16;
    static final int D = 8;
    static final int[] POS = {0, 1, 2, 5, 13, 40};

    static double sin_(double x) {
        double k = Math.floor(x / (PI2_HI + PI2_LO) + 0.5);
        double r = (x - k * PI2_HI) - k * PI2_LO;
        double s2 = r * r, p = 1.0;
        for (int n = 16; n >= 1; n--) p = 1.0 - s2 * p / ((2 * n) * (2 * n + 1));
        return r * p;
    }

    static double cos_(double x) {
        double k = Math.floor(x / (PI2_HI + PI2_LO) + 0.5);
        double r = (x - k * PI2_HI) - k * PI2_LO;
        double s2 = r * r, p = 1.0;
        for (int n = 16; n >= 1; n--) p = 1.0 - s2 * p / ((2 * n - 1) * (2 * n));
        return p;
    }

    static double[] freqs() {
        double[] w = new double[D / 2];
        for (int i = 0; i < D / 2; i++) w[i] = Math.pow(10000.0, -2.0 * i / D);
        return w;
    }

    static double[] pe(int pos, boolean proprio) {
        double[] w = freqs();
        double[] v = new double[D];
        for (int i = 0; i < D / 2; i++) {
            double arg = pos * w[i];
            v[2 * i] = proprio ? sin_(arg) : Math.sin(arg);
            v[2 * i + 1] = proprio ? cos_(arg) : Math.cos(arg);
        }
        return v;
    }

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        String[] rot = {"proprio", "naive"};
        boolean[] pr = {true, false};
        for (int j = 0; j < 2; j++) {
            for (int pos : POS) {
                sb.append(rot[j]).append(" ").append(pos);
                for (double v : pe(pos, pr[j])) sb.append(" ").append(Double.toHexString(v));
                sb.append("\n");
            }
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
