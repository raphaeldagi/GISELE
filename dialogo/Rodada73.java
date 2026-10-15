// Rodada 73 (Parte 106): o seno/cosseno PROPRIOS (serie de Taylor + reducao em duas partes) nos 10000 args de [0,001; 10] onde a libm
// divergiu (Parte 105). So +, -, *, / e a mesma ordem -> IGUAL bit a bit entre as linguas: a serie propria e portavel onde a libm nao e.
public class Rodada73 {
    static final double PI2_HI = 6.283185307179586, PI2_LO = 2.4492935982947064e-16;
    static final int N = 10000;

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

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int k = 1; k <= N; k++) {
            double x = k / 1000.0;
            sb.append("s ").append(Double.toHexString(sin_(x))).append(" c ").append(Double.toHexString(cos_(x))).append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
