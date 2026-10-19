// Rodada 86 (Parte 119): o MCCFR com amostragem EXTERNA no poquer de Kuhn, bit a bit. Para cada jogador, sorteia o acaso e as acoes do
// adversario (LCG inteiro; uniforme = x/2^31, exato); percorre so as acoes do viajante. T = 3000. So +,-,*,/, comparacoes e inteiros.
public class Rodada86 {
    static final int T = 3000;
    static final String[] HIST = {"", "pb", "p", "b"};
    static final int[][] DIST = {{1, 2}, {1, 3}, {2, 1}, {2, 3}, {3, 1}, {3, 2}};
    static double[][] reg = new double[12][2], soma = new double[12][2];
    static long x = 1195;

    static long proximo() {
        x = (1103515245L * x + 12345L) % 2147483648L;
        return x;
    }

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

    static double es(int c1, int c2, String h, int i) {
        Double u = terminal(h, c1, c2);
        if (u != null) return i == 0 ? u : -u;
        int j = h.length() % 2;
        int k = indice(j == 0 ? c1 : c2, h);
        double[] s = estrategia(k);
        if (j == i) {
            double u0 = es(c1, c2, h + "p", i);
            double u1 = es(c1, c2, h + "b", i);
            double no = s[0] * u0 + s[1] * u1;
            reg[k][0] = reg[k][0] + (u0 - no);
            reg[k][1] = reg[k][1] + (u1 - no);
            return no;
        }
        soma[k][0] = soma[k][0] + s[0];
        soma[k][1] = soma[k][1] + s[1];
        return es(c1, c2, h + (proximo() / 2147483648.0 < s[0] ? "p" : "b"), i);
    }

    public static void main(String[] args) {
        for (int it = 0; it < T; it++)
            for (int i = 0; i < 2; i++) {
                int[] d = DIST[(int) ((proximo() >> 16) % 6)];
                es(d[0], d[1], "", i);
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
