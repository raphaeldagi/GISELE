// Rodada 54 (Parte 87): a vantagem normalizada do GRPO, bit a bit. A_i = (r_i - media)/(desvio + 1e-8). So +,-,*,/,sqrt; a ordem das somas e identica a do
// rodada54.py (media por acumulacao da esquerda; variancia idem).
public class Rodada54 {
    static final double[][] GRUPOS = {{5.0, 2.0}, {1.0, 2.0, 3.0, 4.0}, {0.5, 0.5, 0.5}, {10.0, -3.0, 7.0, 0.0, 2.5}, {1.0, 1.0, 1.0, 9.0}};

    static double[] vantagens(double[] rs) {
        int g = rs.length;
        double soma = 0.0;
        for (double r : rs) soma = soma + r;
        double media = soma / g;
        double sq = 0.0;
        for (double r : rs) sq = sq + (r - media) * (r - media);
        double desvio = Math.sqrt(sq / g);
        double[] out = new double[g];
        for (int i = 0; i < g; i++) out[i] = (rs[i] - media) / (desvio + 1e-8);
        return out;
    }

    public static void main(String[] args) {
        for (int gi = 0; gi < GRUPOS.length; gi++) {
            double[] a = vantagens(GRUPOS[gi]);
            for (int vi = 0; vi < a.length; vi++)
                System.out.println("grupo " + gi + " i " + vi + " A " + Double.toHexString(a[vi]));
        }
        System.out.println("fim");
    }
}
