// Rodada 91 (Parte 136): a descida do gradiente de synthai.passos (fixo, secante de Barzilai-Borwein protegida, media exponencial do
// gradiente e limite da norma), bit a bit. A = I + M^T M/(2d) com M de um LCG, d = 6, 24 passos; somas sequenciais na ordem do Python.
public class Rodada91 {
    static final int D = 6;
    static long x = 9136;

    static double u() {
        x = (1103515245L * x + 12345L) % 2147483648L;
        return 2.0 * (x / 2147483648.0) - 1.0;
    }

    static double custo(double[][] A, double[] v) {
        double t = 0.0;
        for (int i = 0; i < D; i++) {
            double s = 0.0;
            for (int j = 0; j < D; j++) s += A[i][j] * v[j];
            t += v[i] * s;
        }
        return t;
    }

    static double[] gradiente(double[][] A, double[] v) {
        double[] g = new double[D];
        for (int i = 0; i < D; i++) {
            double s = 0.0;
            for (int j = 0; j < D; j++) s += A[i][j] * v[j];
            g[i] = 2.0 * s;
        }
        return g;
    }

    static double[] descer(double[][] A, double[] x0, int T, String metodo, double passo, double beta, double limite) {
        double[] v = x0.clone();
        double[] out = new double[T + 1];
        out[0] = custo(A, v);
        double[] xAnt = null, gAnt = null, media = null;
        for (int t = 0; t < T; t++) {
            double[] g = gradiente(A, v);
            double eta = passo;
            double[] dir = g;
            if (metodo.equals("secante")) {
                if (xAnt != null) {
                    double ss = 0.0, sy = 0.0;
                    for (int i = 0; i < D; i++) { double s = v[i] - xAnt[i]; ss += s * s; }
                    for (int i = 0; i < D; i++) { double s = v[i] - xAnt[i], y = g[i] - gAnt[i]; sy += s * y; }
                    if (Double.isFinite(ss) && Double.isFinite(sy) && ss > 1e-12 && sy > 1e-10)
                        eta = Math.min(0.4, Math.max(0.002, 0.8 * ss / sy));
                }
            } else if (metodo.equals("media")) {
                if (media == null) media = g.clone();
                else { double[] m = new double[D]; for (int i = 0; i < D; i++) m[i] = beta * g[i] + (1 - beta) * media[i]; media = m; }
                dir = media;
            }
            double[] delta = new double[D];
            for (int i = 0; i < D; i++) delta[i] = -eta * dir[i];
            if (limite > 0) {
                double n2 = 0.0;
                for (int i = 0; i < D; i++) n2 += delta[i] * delta[i];
                double n = Math.sqrt(n2);
                if (n > limite) for (int i = 0; i < D; i++) delta[i] = delta[i] * limite / n;
            }
            xAnt = v; gAnt = g;
            double[] nv = new double[D];
            for (int i = 0; i < D; i++) nv[i] = v[i] + delta[i];
            v = nv;
            out[t + 1] = custo(A, v);
        }
        return out;
    }

    public static void main(String[] args) {
        double[][] M = new double[D][D];
        for (int i = 0; i < D; i++) for (int j = 0; j < D; j++) M[i][j] = u();
        double[][] A = new double[D][D];
        for (int i = 0; i < D; i++) for (int j = 0; j < D; j++) {
            double t = 0.0;
            for (int k = 0; k < D; k++) t += M[k][i] * M[k][j];
            A[i][j] = (i == j ? 1.0 : 0.0) + t / (2.0 * D);
        }
        double[] x0 = new double[D];
        for (int i = 0; i < D; i++) x0[i] = u();
        StringBuilder sb = new StringBuilder();
        String[] nomes = {"fixo", "secante", "media", "limite"};
        String[] metodos = {"fixo", "secante", "media", "fixo"};
        double[] passos = {0.05, 0.05, 0.05, 0.3};
        double[] limites = {-1, -1, -1, 0.05};
        for (int c = 0; c < 4; c++) {
            double[] cs = descer(A, x0, 24, metodos[c], passos[c], 0.6, limites[c]);
            for (int t = 0; t <= 24; t++) sb.append(nomes[c]).append(" ").append(t).append(" ").append(Double.toHexString(cs[t])).append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
