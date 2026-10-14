// Rodada 55 (Parte 88): o passo do GRPO com corte, bit a bit. surrogate = min(r*A, clip(r,1-eps,1+eps)*A). Só comparações e ×, mesma ordem do rodada55.py.
public class Rodada55 {
    static final double EPS = 0.2;
    static final double[][] CASOS = {{1.0, 1.0}, {1.5, 1.0}, {0.5, 1.0}, {1.3, -1.0}, {0.7, -1.0}, {2.0, 0.5}, {0.1, -0.5}, {1.25, 1.0}};

    static double clip(double x, double lo, double hi) {
        if (x < lo) return lo;
        if (x > hi) return hi;
        return x;
    }

    static double surrogate(double r, double a) {
        double naoCortado = r * a;
        double cortado = clip(r, 1.0 - EPS, 1.0 + EPS) * a;
        return naoCortado < cortado ? naoCortado : cortado;
    }

    public static void main(String[] args) {
        for (int i = 0; i < CASOS.length; i++)
            System.out.println("caso " + i + " s " + Double.toHexString(surrogate(CASOS[i][0], CASOS[i][1])));
        System.out.println("fim");
    }
}
