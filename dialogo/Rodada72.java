// Rodada 72 (Parte 105): a decisao de equilibrio do blefe, bit a bit. alpha=B/(P+2B), c=P/(P+B), b=alpha/(1-alpha) e os EVs usam so
// +, -, *, / e comparacoes - nenhuma transcendental, portavel por construcao (Parte 52). A decisao e sortear contra a frequencia (comparacao).
public class Rodada72 {
    static final double P = 2.0, B = 2.0;
    static final double[] ACASO = {0.10, 0.33, 0.50, 0.67, 0.90};

    public static void main(String[] args) {
        double alpha = B / (P + 2.0 * B);
        double c = P / (P + B);
        double b = alpha / (1.0 - alpha);
        double evp = alpha * (P + B) - (1.0 - alpha) * B;
        double evb = (1.0 - c) * P - c * B;
        StringBuilder sb = new StringBuilder();
        sb.append("alpha ").append(Double.toHexString(alpha)).append("\n");
        sb.append("c ").append(Double.toHexString(c)).append("\n");
        sb.append("b ").append(Double.toHexString(b)).append("\n");
        sb.append("evpagar ").append(Double.toHexString(evp)).append("\n");
        sb.append("evblefar ").append(Double.toHexString(evb)).append("\n");
        sb.append("decisoes");
        for (double u : ACASO) sb.append(" ").append(Double.toHexString(u < c ? 1.0 : 0.0));
        sb.append("\n").append("fim");
        System.out.println(sb.toString());
    }
}
