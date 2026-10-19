// Rodada 85 (Parte 118): o MCCFR com amostragem do ACASO no poquer de Kuhn, bit a bit. Cada iteracao sorteia uma distribuicao por um LCG
// inteiro (o acaso dado de fora), T = 3000; imprime a estrategia MEDIA (P(b)) nos 12 conjuntos. So +,-,*,/, comparacoes e inteiros.
public class Rodada85 {
    static final int T = 3000;
    static final int[][] DIST = {{1, 2}, {1, 3}, {2, 1}, {2, 3}, {3, 1}, {3, 2}};
    static final String[] HIST = {"", "pb", "p", "b"};
    static double[][] reg = new double[12][2], soma = new double[12][2];

    static int indice(int carta, String h) {
        int i = 0;
        for (int k = 0; k < 4; k++) if (HIST[k].equals(h)) i = k;
        return (carta - 1) * 4 + i;
    }

    static Double terminal(String h, int c1, int c2) {
        double ganha = c1 > c2 ? 1.0 : -1.0;
        if (h.equals("pp")) return ganha;
        if (h.equals("bb") || h.equals("pbb")) return 2.0 * ganha;
        if (h.equals("bp")) return 1.0;
        if (h.equals("pbp")) return -1.0;
        return null;
    }

    static double[] estrategia(int k) {
        double a = reg[k][0] > 0.0 ? reg[k][0] : 0.0;
        double b = reg[k][1] > 0.0 ? reg[k][1] : 0.0;
        double s = a + b;
        if (s > 0.0) return new double[]{a / s, b / s};
        return new double[]{0.5, 0.5};
    }

    static double cfr(int c1, int c2, String h, double p1, double p2) {
        Double u = terminal(h, c1, c2);
        if (u != null) return u;
        int j = h.length() % 2;
        int k = indice(j == 0 ? c1 : c2, h);
        double[] s = estrategia(k);
        double[] util = {0.0, 0.0};
        double no = 0.0;
        for (int a = 0; a < 2; a++) {
            String letra = a == 0 ? "p" : "b";
            if (j == 0) util[a] = cfr(c1, c2, h + letra, p1 * s[a], p2);
            else util[a] = cfr(c1, c2, h + letra, p1, p2 * s[a]);
            no = no + s[a] * util[a];
        }
        double sinal = j == 0 ? 1.0 : -1.0;
        double adv = j == 0 ? p2 : p1;
        double prop = j == 0 ? p1 : p2;
        for (int a = 0; a < 2; a++) {
            reg[k][a] = reg[k][a] + adv * sinal * (util[a] - no);
            soma[k][a] = soma[k][a] + prop * s[a];
        }
        return no;
    }

    public static void main(String[] args) {
        long x = 1185;
        for (int it = 0; it < T; it++) {
            x = (1103515245L * x + 12345L) % 2147483648L;
            int[] d = DIST[(int) ((x >> 16) % 6)];
            cfr(d[0], d[1], "", 1.0, 1.0);
        }
        StringBuilder sb = new StringBuilder();
        for (int carta = 1; carta <= 3; carta++) {
            sb.append("carta ").append(carta);
            for (String h : HIST) {
                int k = indice(carta, h);
                double s = soma[k][0] + soma[k][1];
                sb.append(" ").append(Double.toHexString(s > 0.0 ? soma[k][1] / s : 0.5));
            }
            sb.append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
