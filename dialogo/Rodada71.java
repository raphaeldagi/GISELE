// Rodada 71 (Parte 104): a codificacao posicional senoidal, bit a bit — versao PORTAVEL (seno/cosseno proprios, serie de Taylor; frequencias sem
// Math.pow, so sqrt e multiplicacao repetida). Nao depende de nenhuma transcendental da libm (regra da Parte 52/77). A sonda SondaSeno104 mede o naive.
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
        double r = 1.0 / Math.sqrt(Math.sqrt(10000.0));
        double[] w = new double[D / 2];
        double cur = 1.0;
        for (int i = 0; i < D / 2; i++) { w[i] = cur; cur = cur * r; }
        return w;
    }

    static double[] pe(int pos) {
        double[] w = freqs();
        double[] v = new double[D];
        for (int i = 0; i < D / 2; i++) {
            double arg = pos * w[i];
            v[2 * i] = sin_(arg);
            v[2 * i + 1] = cos_(arg);
        }
        return v;
    }

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int pos : POS) {
            sb.append("proprio ").append(pos);
            for (double v : pe(pos)) sb.append(" ").append(Double.toHexString(v));
            sb.append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
