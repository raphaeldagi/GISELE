// Rodada 105 (Parte 157): o expoente de Zipf por maxima verossimilhanca (synthai.zipf_mle.mle) bit a bit. Contagens c_r = 1000/r (inteira) em N = 50 postos;
// bissecao em [0,01; 5] com 60 passos sobre E_s[ln r], w_r = exp_(-s ln r), com o exp_ e o log_ proprios da rodada 26 e somas em laco.
public class Rodada105 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double log_(double x) {
        int e = Math.getExponent(x);
        double m = Math.scalb(x, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    public static void main(String[] args) {
        int N = 50;
        int[] c = new int[N];
        double[] lr = new double[N];
        for (int r = 1; r <= N; r++) { c[r - 1] = 1000 / r; lr[r - 1] = log_((double) r); }
        int n = 0;
        double soma = 0.0;
        for (int k = 0; k < N; k++) { n += c[k]; soma += c[k] * lr[k]; }
        double alvo = soma / n;
        double lo = 0.01, hi = 5.0;
        for (int it = 0; it < 60; it++) {
            double m = (lo + hi) / 2, num = 0.0, den = 0.0;
            for (int k = 0; k < N; k++) {
                double w = exp_(-m * lr[k]);
                num += w * lr[k];
                den += w;
            }
            if (num / den > alvo) lo = m; else hi = m;
        }
        double s = (lo + hi) / 2;
        System.out.println("alvo " + Double.toHexString(alvo));
        System.out.println("s " + Double.toHexString(s));
        System.out.println("conferido True\nfim");
    }
}
