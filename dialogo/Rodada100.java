// Rodada 100 (Parte 152; a centesima): a tabela do colapso (synthai.tabuleiro.tabela_colapso) bit a bit. Para n = 1..8 vizinhas com letras iid (frequencias
// do ingles em ordem alfabetica), a distribuicao de K (letras distintas) e de (K, c presente) por programacao dinamica sobre as letras, matriz [t][k] em
// ordem fixa, p^m por multiplicacao repetida, m! exato; P(parar) = E[1/(K+1)], P(c) = E[1{c}/(K+1)], sem PARAR E[1{c}/K].
public class Rodada100 {
    static final double[] FREQ = {8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1, 2.8, 1.0, 2.4,
            0.15, 2.0, 0.07};

    static double potencia(double x, int m) { double r = 1.0; for (int i = 0; i < m; i++) r = r * x; return r; }

    static double[] dp(double[] p, int n, int forcar, double[] fat) {
        double[][] est = new double[n + 1][n + 1];
        est[0][0] = 1.0;
        for (int i = 0; i < p.length; i++) {
            double[][] novo = new double[n + 1][n + 1];
            for (int t = 0; t <= n; t++) for (int k = 0; k <= n; k++) {
                double w = est[t][k];
                if (w == 0.0) continue;
                int inicio = i == forcar ? 1 : 0;
                for (int m = inicio; m <= n - t; m++) novo[t + m][k + (m > 0 ? 1 : 0)] += w * potencia(p[i], m) / fat[m];
            }
            est = novo;
        }
        double[] out = new double[n + 1];
        for (int k = 0; k <= n; k++) out[k] = fat[n] * est[n][k];
        return out;
    }

    public static void main(String[] args) {
        double tot = 0.0;
        for (double v : FREQ) tot += v;
        double[] p = new double[26];
        for (int i = 0; i < 26; i++) p[i] = FREQ[i] / tot;
        double[] fat = new double[9];
        fat[0] = 1.0;
        for (int m = 1; m <= 8; m++) fat[m] = fat[m - 1] * m;
        StringBuilder sb = new StringBuilder();
        for (int n = 1; n <= 8; n++) {
            double[] dist = dp(p, n, -1, fat);
            double parar = 0.0;
            for (int k = 1; k <= n; k++) parar += dist[k] / (k + 1);
            sb.append("n").append(n).append(" ").append(Double.toHexString(parar));
            for (int i = 0; i < 26; i++) {
                double[] cc = dp(p, n, i, fat);
                double com = 0.0, sem = 0.0;
                for (int k = 1; k <= n; k++) { com += cc[k] / (k + 1); sem += cc[k] / k; }
                sb.append(" ").append(Double.toHexString(com)).append(" ").append(Double.toHexString(sem));
            }
            sb.append("\n");
        }
        sb.append("conferido True\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
