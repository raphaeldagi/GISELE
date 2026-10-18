// Rodada 83 (Parte 116): a avaliacao pareada que substitui a avaliacao metacognitiva do NEXUS-RAPHAEL v2 recebido. d = valor - base,
// t = media(d)/(s_d/sqrt(n)), confirmed se t > 2.131847, rejected se t < -2.131847. So + - * / e sqrt, somas em laco na mesma ordem. Bit a bit.
public class Rodada83 {
    static final double T_CRITICO = 2.131847;
    static final double[][][] H = {
        {{10.4, 11.2, 9.8, 12.1, 10.9}, {10.0, 10.1, 9.9, 10.3, 10.2}},
        {{9.1, 10.7, 8.8, 11.9, 10.2}, {10.0, 10.1, 9.9, 10.3, 10.2}},
        {{8.2, 9.0, 8.7, 9.4, 8.1}, {10.0, 10.1, 9.9, 10.3, 10.2}},
    };

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < H.length; i++) {
            double[] v = H[i][0], b = H[i][1];
            int n = v.length;
            double[] d = new double[n];
            for (int j = 0; j < n; j++) d[j] = v[j] - b[j];
            double soma = 0.0;
            for (int j = 0; j < n; j++) soma += d[j];
            double media = soma / n;
            double q = 0.0;
            for (int j = 0; j < n; j++) q += (d[j] - media) * (d[j] - media);
            double s = Math.sqrt(q / (n - 1));
            double t = media / (s / Math.sqrt(n));
            String st = t > T_CRITICO ? "confirmed" : (t < -T_CRITICO ? "rejected" : "inconclusive");
            sb.append("H").append(i).append(" t ").append(Double.toHexString(t)).append(" ").append(st).append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
