// Rodada 76 (Parte 109): o valor EXATO do Kuhn simplificado do NEXUS-RAPHAEL, bit a bit. Enumeracao das 6 distribuicoes (p0, p1
// distintos) para a probabilidade de apostar com Q em 0, 0.1, ..., 1 e o melhor da grade. So +,-,*,/ e comparacoes, ordem fixa das somas.
public class Rodada76 {
    static double valorKuhn(double paQ) {
        double tot = 0.0;
        for (int p0 = 1; p0 <= 3; p0++) {
            for (int p1 = 1; p1 <= 3; p1++) {
                if (p0 == p1) continue;
                double pa = (p0 == 3) ? 1.0 : ((p0 == 2) ? paQ : 0.0);
                double apostou = (p1 >= 2) ? ((p0 > p1) ? 2.0 : -2.0) : 1.0;
                tot = tot + (pa * apostou + (1.0 - pa) * (-1.0)) / 6.0;
            }
        }
        return tot;
    }


    public static void main(String[] args) {
        int melhorK = 0;
        double melhorV = valorKuhn(0.0);
        StringBuilder sb = new StringBuilder();
        for (int k = 0; k <= 10; k++) {
            double v = valorKuhn(k / 10.0);
            sb.append("pa ").append(k).append(" ").append(Double.toHexString(v)).append("\n");
            if (v > melhorV) { melhorK = k; melhorV = v; }
        }
        sb.append("melhor ").append(melhorK).append(" ").append(Double.toHexString(melhorV)).append("\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
