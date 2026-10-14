// Rodada 61 (Parte 94): uma cabeca de ATENCAO causal inteira, bit a bit. Q=XWq,K=XWk,V=XWv; escores causais (Q[i].K[j])/sqrt(d);
// softmax com EXP PROPRIO (o exp e a fronteira da Parte 52); saida o[i]=sum p[i][j] V[j]; decisao por argmax da projecao. Pesos/entrada fixos.
public class Rodada61 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final int T = 4, D = 3;
    static final double[][] X = {{0.5, -1.0, 0.25}, {1.0, 0.0, -0.5}, {-0.75, 0.5, 1.0}, {0.1, -0.2, 0.3}};
    static final double[][] WQ = {{0.2, -0.1, 0.4}, {0.3, 0.5, -0.2}, {-0.4, 0.1, 0.6}};
    static final double[][] WK = {{0.1, 0.3, -0.5}, {-0.2, 0.4, 0.2}, {0.6, -0.3, 0.1}};
    static final double[][] WV = {{0.5, 0.2, -0.1}, {0.1, -0.4, 0.3}, {-0.2, 0.6, 0.4}};
    static final double[][] WO = {{0.3, -0.2}, {0.1, 0.5}, {-0.4, 0.2}};

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double[] matvec(double[][] M, double[] v) {
        int m = M[0].length;
        double[] out = new double[m];
        for (int j = 0; j < m; j++) {
            double s = 0.0;
            for (int k = 0; k < v.length; k++) s = s + v[k] * M[k][j];
            out[j] = s;
        }
        return out;
    }

    public static void main(String[] args) {
        double[][] Q = new double[T][], K = new double[T][], V = new double[T][];
        for (int i = 0; i < T; i++) { Q[i] = matvec(WQ, X[i]); K[i] = matvec(WK, X[i]); V[i] = matvec(WV, X[i]); }
        double escala = Math.sqrt((double) D);
        double[][] saidas = new double[T][D];
        for (int i = 0; i < T; i++) {
            double[] e = new double[i + 1];
            for (int j = 0; j <= i; j++) {
                double dot = 0.0;
                for (int k = 0; k < D; k++) dot = dot + Q[i][k] * K[j][k];
                e[j] = dot / escala;
            }
            double m = e[0];
            for (double x : e) if (x > m) m = x;
            double[] ex = new double[i + 1];
            double s = 0.0;
            for (int j = 0; j <= i; j++) { ex[j] = exp_(e[j] - m); s = s + ex[j]; }
            double[] p = new double[i + 1];
            for (int j = 0; j <= i; j++) p[j] = ex[j] / s;
            double[] o = new double[D];
            for (int j = 0; j <= i; j++) for (int k = 0; k < D; k++) o[k] = o[k] + p[j] * V[j][k];
            saidas[i] = o;
        }
        for (int i = 0; i < T; i++) for (int k = 0; k < D; k++)
            System.out.println("pos " + i + " saida " + k + " " + Double.toHexString(saidas[i][k]));
        double[] logits = matvec(WO, saidas[T - 1]);
        for (int k = 0; k < logits.length; k++) System.out.println("logit " + k + " " + Double.toHexString(logits[k]));
        int arg = logits[0] >= logits[1] ? 0 : 1;
        System.out.println("decisao " + arg);
        System.out.println("fim");
    }
}
