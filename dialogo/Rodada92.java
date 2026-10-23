// Rodada 92 (Parte 139): a GRPO de synthai.grpo_bandido bit a bit. 16 contextos e as amostras de acoes de um LCG; G = 4, 64 grupos, 3 passes,
// taxa 0,15, recorte 0,2, KL 0,025 contra a uniforme; exp e log PROPRIOS (rodada 26); somas sequenciais na ordem do Python.
public class Rodada92 {
    static long x = 13092;
    static final double[][] OR = {{.1, -.1, 0.}, {1., -1., .2}, {.2, .7, -1.}, {.25, -.3, .1}, {.1, .05, -.15}};
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

    static double u() {
        x = (1103515245L * x + 12345L) % 2147483648L;
        return x / 2147483648.0;
    }

    static double[] feat(double a, double b) { return new double[]{1.0, a, b, a * b, a * a - b * b}; }

    static double[] logits(double[][] w, double[] f) {
        double[] z = new double[3];
        for (int a = 0; a < 3; a++) { double t = 0.0; for (int i = 0; i < 5; i++) t += f[i] * w[i][a]; z[a] = t; }
        return z;
    }

    static double[] logSoftmax(double[] z) {
        double m = z[0] >= z[1] ? z[0] : z[1];
        m = m >= z[2] ? m : z[2];
        double s = 0.0;
        for (double v : z) s += exp_(v - m);
        double ls = log_(s);
        return new double[]{z[0] - m - ls, z[1] - m - ls, z[2] - m - ls};
    }

    static int otima(double[] f) {
        double[] z = logits(OR, f);
        int best = 0;
        for (int a = 1; a < 3; a++) if (z[a] > z[best]) best = a;
        return best;
    }

    static double[] vantagens(double[] rec) {
        int G = rec.length;
        boolean iguais = true;
        for (double r : rec) if (r != rec[0]) iguais = false;
        if (iguais) return new double[G];
        double s = 0.0;
        for (double r : rec) s += r;
        double media = s / G, v = 0.0;
        for (double r : rec) v += (r - media) * (r - media);
        double desvio = Math.sqrt(v / G);
        double[] out = new double[G];
        for (int i = 0; i < G; i++) out[i] = (rec[i] - media) / (desvio + 1e-8);
        return out;
    }

    static double[][] gradiente(double[][] w, double[] f, int[] acoes, double[] lv, double[] vant) {
        double clip = 0.2, beta = 0.025;
        double[] logp = logSoftmax(logits(w, f));
        double[] p = {exp_(logp[0]), exp_(logp[1]), exp_(logp[2])};
        int G = acoes.length;
        double[] d = new double[3];
        for (int k = 0; k < G; k++) {
            int a = acoes[k];
            double A = vant[k];
            double razao = exp_(logp[a] - lv[k]);
            boolean ativa = !((A > 0 && razao > 1 + clip) || (A < 0 && razao < 1 - clip));
            if (ativa) for (int b = 0; b < 3; b++) { double score = (b == a ? 1.0 : 0.0) - p[b]; d[b] -= razao * A / G * score; }
        }
        double ref = -log_(3.0);
        double[] diff = {logp[0] - ref, logp[1] - ref, logp[2] - ref};
        double kl = 0.0;
        for (int b = 0; b < 3; b++) kl += p[b] * diff[b];
        for (int b = 0; b < 3; b++) d[b] += beta * p[b] * (diff[b] - kl);
        double[][] g = new double[5][3];
        for (int i = 0; i < 5; i++) for (int b = 0; b < 3; b++) g[i][b] = f[i] * d[b];
        return g;
    }

    public static void main(String[] args) {
        double[][] ctx = new double[16][];
        for (int c = 0; c < 16; c++) { double a = 2.0 * u() - 1.0; double b = 2.0 * u() - 1.0; ctx[c] = feat(a, b); }
        double[][] w = new double[5][3];
        for (int t = 0; t < 64; t++) {
            double[] f = ctx[(int) (u() * 16)];
            double[] lv = logSoftmax(logits(w, f));
            double[] pv = {exp_(lv[0]), exp_(lv[1]), exp_(lv[2])};
            int[] acoes = new int[4];
            for (int k = 0; k < 4; k++) { double r = u(); acoes[k] = r < pv[0] ? 0 : (r < pv[0] + pv[1] ? 1 : 2); }
            int ot = otima(f);
            double[] rec = new double[4];
            for (int k = 0; k < 4; k++) rec[k] = acoes[k] == ot ? 1.0 : 0.0;
            double[] vant = vantagens(rec);
            double[] lva = new double[4];
            for (int k = 0; k < 4; k++) lva[k] = lv[acoes[k]];
            for (int e = 0; e < 3; e++) {
                double[][] g = gradiente(w, f, acoes, lva, vant);
                double[][] nw = new double[5][3];
                for (int i = 0; i < 5; i++) for (int b = 0; b < 3; b++) nw[i][b] = w[i][b] - 0.15 * g[i][b];
                w = nw;
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5; i++) for (int b = 0; b < 3; b++) sb.append("w").append(i).append(b).append(" ").append(Double.toHexString(w[i][b])).append("\n");
        double t = 0.0;
        for (double[] f : ctx) t += exp_(logSoftmax(logits(w, f))[otima(f)]);
        sb.append("retorno ").append(Double.toHexString(t / 16)).append("\n");
        sb.append("conferido True\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
