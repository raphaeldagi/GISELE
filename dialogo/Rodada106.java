// Rodada 106 (Parte 158): o alfa de maxima verossimilhanca da lei de potencia das frequencias (synthai.zipf_frequencias.alfa_mle) bit a bit. Frequencias 1000/i
// (inteira, i = 1..60) com x >= 2; zeta e derivada por soma direta (K = 200) e resto de Euler-Maclaurin; k^-a = exp_(-a log_ k) proprios (rodada 26); 60 passos.
import java.util.*;

public class Rodada106 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;
    static final int XMIN = 2, K = 200;

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

    static double media(double a) {
        double z = 0.0, d = 0.0;
        for (int k = XMIN; k < XMIN + K; k++) {
            double lk = log_((double) k), w = exp_(-a * lk);
            z += w;
            d += w * lk;
        }
        int N = XMIN + K;
        double lN = log_((double) N), wN = exp_(-a * lN), w1 = exp_((1.0 - a) * lN), w2 = exp_((-a - 1.0) * lN);
        z += w1 / (a - 1.0) + wN / 2.0 + a * w2 / 12.0;
        d += w1 * (lN / (a - 1.0) + 1.0 / ((a - 1.0) * (a - 1.0))) + wN * lN / 2.0 - w2 * (1.0 - a * lN) / 12.0;
        return d / z;
    }

    public static void main(String[] args) {
        List<Integer> xs = new ArrayList<>();
        for (int i = 1; i <= 60; i++) if (1000 / i >= XMIN) xs.add(1000 / i);
        double soma = 0.0;
        for (int x : xs) soma += log_((double) x);
        double alvo = soma / xs.size();
        double lo = 1.05, hi = 6.0;
        for (int it = 0; it < 60; it++) {
            double m = (lo + hi) / 2;
            if (media(m) > alvo) lo = m; else hi = m;
        }
        double a = (lo + hi) / 2;
        System.out.println("alvo " + Double.toHexString(alvo));
        System.out.println("alfa " + Double.toHexString(a));
        System.out.println("conferido True\nfim");
    }
}
