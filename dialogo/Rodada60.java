// Rodada 60 (Parte 93): a decisao do MPC — rollout no modelo de mundo e argmin do custo sobre sequencias FIXAS de acao — bit a bit.
// A dinamica, o custo e o argmin usam so + - * e comparacoes (exatos no IEEE 754): planejar/controlar NAO cria fronteira (Parte 52).
public class Rodada60 {
    static final double[][] A = {{1.0, 0.15}, {0.0, 0.9}};
    static final double[][] B = {{0.0}, {0.15}};
    static final double ALVO = 1.0, PESO_ACAO = 0.05;
    static final double[] S0 = {-1.5, 0.3};
    static final double[][] CANDIDATOS = {
        {0.0, 0.0, 0.0, 0.0},
        {1.0, 1.0, 1.0, 1.0},
        {0.5, 0.5, 0.5, 0.5},
        {1.0, 0.5, 0.25, 0.0},
        {0.25, 0.5, 0.75, 1.0},
        {-1.0, -1.0, -1.0, -1.0},
        {0.75, 0.25, -0.25, -0.75},
        {1.0, 0.0, -1.0, 0.0},
        {0.3, 0.6, 0.3, 0.6},
    };

    static double[] transicao(double s0, double s1, double a) {
        double n0 = A[0][0] * s0 + A[0][1] * s1 + B[0][0] * a;
        double n1 = A[1][0] * s0 + A[1][1] * s1 + B[1][0] * a;
        return new double[]{n0, n1};
    }

    static double custo(double[] acoes) {
        double s0 = S0[0], s1 = S0[1], c = 0.0;
        for (double a : acoes) {
            double[] n = transicao(s0, s1, a);
            s0 = n[0]; s1 = n[1];
            c = c + (s0 - ALVO) * (s0 - ALVO) + s1 * s1;
        }
        for (double a : acoes) c = c + PESO_ACAO * a * a;
        return c;
    }

    public static void main(String[] args) {
        int melhor = 0;
        double melhorC = custo(CANDIDATOS[0]);
        double[] custos = new double[CANDIDATOS.length];
        custos[0] = melhorC;
        for (int k = 1; k < CANDIDATOS.length; k++) {
            double ck = custo(CANDIDATOS[k]);
            custos[k] = ck;
            if (ck < melhorC) { melhorC = ck; melhor = k; }
        }
        for (int k = 0; k < custos.length; k++) System.out.println("candidato " + k + " custo " + Double.toHexString(custos[k]));
        System.out.println("melhor " + melhor + " primeira_acao " + Double.toHexString(CANDIDATOS[melhor][0]));
        System.out.println("custo_otimo " + Double.toHexString(melhorC));
        System.out.println("fim");
    }
}
