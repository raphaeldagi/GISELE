// Rodada 70 (Parte 103): a atencao de MULTIPLAS CABECAS concatenadas, bit a bit. A concatenacao e so layout; a projecao de saida soma sobre
// a dim concatenada na MESMA ordem de indice nos dois lados. O unico transcendental e o exp do softmax de cada cabeca (Parte 52).
public class Rodada70 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final int DH = 2;
    static final double[][] X = {
        {0.5, -0.2, 0.1, 0.4},
        {-0.3, 0.8, 0.2, -0.1},
        {0.2, 0.2, -0.5, 0.6},
    };
    static final double[][] WQ = {{0.1,-0.2,0.3,0.0},{0.2,0.1,-0.1,0.4},{0.0,0.3,0.2,-0.2},{-0.1,0.1,0.4,0.3}};
    static final double[][] WK = {{0.2,0.0,-0.1,0.3},{0.1,0.2,0.3,-0.2},{-0.3,0.1,0.0,0.2},{0.4,-0.1,0.2,0.1}};
    static final double[][] WV = {{0.3,0.1,0.0,-0.2},{0.0,-0.1,0.2,0.3},{0.1,0.4,-0.2,0.1},{0.2,0.0,0.3,-0.1}};
    static final double[][] WO = {{0.1,0.2,-0.1,0.3},{0.3,-0.2,0.1,0.0},{-0.1,0.1,0.2,0.2},{0.2,0.3,0.0,-0.1}};

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double[] matvec(double[][] W, double[] x) {
        double[] o = new double[W.length];
        for (int i = 0; i < W.length; i++) {
            double s = 0.0;
            for (int j = 0; j < x.length; j++) s += W[i][j] * x[j];
            o[i] = s;
        }
        return o;
    }

    static double[] softmax(double[] scores, int n) {
        double m = scores[0];
        for (int i = 0; i < n; i++) if (scores[i] > m) m = scores[i];
        double[] e = new double[n];
        double tot = 0.0;
        for (int i = 0; i < n; i++) { e[i] = exp_(scores[i] - m); tot = tot + e[i]; }
        for (int i = 0; i < n; i++) e[i] = e[i] / tot;
        return e;
    }

    public static void main(String[] args) {
        int T = X.length;
        double[][] Q = new double[T][], K = new double[T][], V = new double[T][];
        for (int t = 0; t < T; t++) { Q[t] = matvec(WQ, X[t]); K[t] = matvec(WK, X[t]); V[t] = matvec(WV, X[t]); }
        double esc = 1.0 / Math.sqrt(DH);
        StringBuilder sb = new StringBuilder();
        for (int t = 0; t < T; t++) {
            double[] concat = new double[4];
            for (int h = 0; h < 2; h++) {
                int c0 = h * DH;
                double[] scores = new double[t + 1];
                for (int u = 0; u <= t; u++) {
                    double dot = 0.0;
                    for (int d = 0; d < DH; d++) dot = dot + Q[t][c0 + d] * K[u][c0 + d];
                    scores[u] = dot * esc;
                }
                double[] a = softmax(scores, t + 1);
                for (int d = 0; d < DH; d++) {
                    double acc = 0.0;
                    for (int u = 0; u <= t; u++) acc = acc + a[u] * V[u][c0 + d];
                    concat[c0 + d] = acc;
                }
            }
            double[] out = matvec(WO, concat);
            sb.append("saida ").append(t);
            for (double v : out) sb.append(" ").append(Double.toHexString(v));
            sb.append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
