// Rodada 77 (Parte 110): o aprendizado continuo em R2 (GD e OGD, duas tarefas de posto 1), bit a bit. u vem de sqrt (IEEE), nao de
// sin/cos (fronteira da Parte 105): theta = 0, 45, 60 graus. So +,-,*,/ e sqrt.
public class Rodada77 {
    static final double PASSO = 0.1;
    static final int PASSOS = 2000;

    static double[] continuo(double u0, double u1, boolean ogd) {
        double w0 = 0.0, w1 = 0.0;
        for (int i = 0; i < PASSOS; i++) w0 = w0 - PASSO * (2.0 * (w0 - 1.0));
        double a0 = w0, a1 = w1;
        double cb = u0 * a0 + u1 * a1 + 1.0;
        for (int i = 0; i < PASSOS; i++) {
            double r = u0 * w0 + u1 * w1 - cb;
            double g0 = 2.0 * r * u0;
            double g1 = 2.0 * r * u1;
            if (ogd) g0 = g0 - g0 * 1.0;
            w0 = w0 - PASSO * g0;
            w1 = w1 - PASSO * g1;
        }
        double esq = (w0 - 1.0) * (w0 - 1.0);
        double rb = u0 * w0 + u1 * w1 - cb;
        double norma = Math.sqrt((w0 - a0) * (w0 - a0) + (w1 - a1) * (w1 - a1));
        return new double[]{esq, rb * rb, norma};
    }

    public static void main(String[] args) {
        String[] nomes = {"0", "45", "60"};
        double[][] us = {{1.0, 0.0}, {Math.sqrt(0.5), Math.sqrt(0.5)}, {0.5, Math.sqrt(0.75)}};
        StringBuilder sb = new StringBuilder();
        for (int k = 0; k < 3; k++) {
            for (int o = 0; o < 2; o++) {
                double[] r = continuo(us[k][0], us[k][1], o == 1);
                sb.append(nomes[k]).append(o == 1 ? " ogd " : " gd ").append(Double.toHexString(r[0])).append(" ")
                  .append(Double.toHexString(r[1])).append(" ").append(Double.toHexString(r[2])).append("\n");
            }
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
