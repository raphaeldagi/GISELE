// Rodada 78 (Parte 111): o passo de Q-learning tabular, bit a bit. Tabela 5x3; 2000 transicoes geradas por um LCG inteiro;
// Q <- Q + alfa(r + gama*max Q(s',.) - Q), max por comparacao. So +,-,* e comparacao.
public class Rodada78 {
    static final int S = 5, A = 3, N = 2000;
    static final double ALFA = 0.2, GAMA = 0.95;

    static long lcg(long x) {
        return (x * 1103515245L + 12345L) % 2147483648L;
    }

    public static void main(String[] args) {
        double[][] q = new double[S][A];
        long x = 78;
        for (int i = 0; i < N; i++) {
            x = lcg(x); int s = (int) (x % S);
            x = lcg(x); int a = (int) (x % A);
            x = lcg(x); double r = (double) (x % 7) - 3.0;
            x = lcg(x); int s2 = (int) (x % S);
            x = lcg(x); boolean fim = (x % 10) == 0;
            double futuro = 0.0;
            if (!fim) {
                futuro = q[s2][0];
                for (int b = 1; b < A; b++) if (q[s2][b] > futuro) futuro = q[s2][b];
            }
            q[s][a] = q[s][a] + ALFA * (r + GAMA * futuro - q[s][a]);
        }
        StringBuilder sb = new StringBuilder();
        for (int s = 0; s < S; s++) {
            sb.append("q ").append(s);
            for (int a = 0; a < A; a++) sb.append(" ").append(Double.toHexString(q[s][a]));
            sb.append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
