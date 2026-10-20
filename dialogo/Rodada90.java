// Rodada 90 (Parte 123): o rastreador do erro humano com esquecimento, nas duas formas (encolher para a priori Beta(2, 18) e encolher
// para zero), gama = 0.995 e 0.93; observacoes de um LCG; epsilon 0.15 por 2000 observacoes e depois 0.6. So +, -, *, / e comparacoes.
public class Rodada90 {
    public static void main(String[] args) {
        double[] gamas = {0.995, 0.93};
        StringBuilder sb = new StringBuilder();
        for (double gama : gamas) {
            for (int forma = 0; forma < 2; forma++) {
                long x = 1231;
                double a = 2.0, b = 18.0;
                int atraso = -1;
                StringBuilder ms = new StringBuilder();
                for (int t = 0; t < 4000; t++) {
                    double eps = t < 2000 ? 0.15 : 0.6;
                    x = (1103515245L * x + 12345L) % 2147483648L;
                    double e = x / 2147483648.0 < eps ? 1.0 : 0.0;
                    if (forma == 0) {
                        a = 2.0 + gama * (a + e - 2.0);
                        b = 18.0 + gama * (b + (1.0 - e) - 18.0);
                    } else {
                        a = gama * a + e;
                        b = gama * b + (1.0 - e);
                    }
                    double m = a / (a + b);
                    if (t >= 2000 && atraso < 0 && m >= 0.375) atraso = t - 1999;
                    if (t % 500 == 499) ms.append(" ").append(Double.toHexString(m));
                }
                sb.append("gama ").append(gama).append(" forma ").append(forma).append(" atraso ").append(atraso).append(ms).append("\n");
            }
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
