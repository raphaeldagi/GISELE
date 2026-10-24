// Rodada 97 (Parte 149): o quantil t de Student (calculos.p3200_t_student_quantil) bit a bit. Densidade c*exp_(-(nu+1)/2*log_(1+s*s/nu)) com o
// exp e o log PROPRIOS (rodada 26); c = R(nu)/sqrt(nu*pi), R pela recorrencia R(nu+2) = R(nu)*(nu+1)/nu; Simpson com 2000 intervalos em laco;
// 80 bisseccoes em [0, 50].
public class Rodada97 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;

    static double exp_(double v) {
        double k = Math.floor(v / (LN2_HI + LN2_LO) + 0.5);
        double r = (v - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double log_(double v) {
        int e = Math.getExponent(v);
        double m = Math.scalb(v, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    static double razaoGama(int nu) {
        double r = nu % 2 == 1 ? 1.0 / Math.sqrt(Math.PI) : Math.sqrt(Math.PI) / 2.0;
        int k = nu % 2 == 1 ? 1 : 2;
        while (k < nu) { r = r * (k + 1.0) / k; k += 2; }
        return r;
    }

    static double f(double s, int nu, double c, double e) { return c * exp_(e * log_(1.0 + s * s / nu)); }

    static double cdf(double x, int nu, double c) {
        int n = 2000;
        double e = -((nu + 1.0) / 2.0);
        double h = x / n;
        double acc = f(0.0, nu, c, e) + f(x, nu, c, e);
        for (int i = 1; i < n; i++) acc += (i % 2 == 1 ? 4.0 : 2.0) * f(i * h, nu, c, e);
        return 0.5 + acc * h / 3.0;
    }

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int nu : new int[]{2, 7, 19, 27}) {
            double c = razaoGama(nu) / Math.sqrt(nu * Math.PI);
            double lo = 0.0, hi = 50.0;
            for (int it = 0; it < 80; it++) { double m = (lo + hi) / 2.0; if (cdf(m, nu, c) < 0.95) lo = m; else hi = m; }
            double t = (lo + hi) / 2.0;
            sb.append("nu").append(nu).append(" c ").append(Double.toHexString(c)).append(" t ").append(Double.toHexString(t)).append("\n");
        }
        sb.append("conferido True\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
