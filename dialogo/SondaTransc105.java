// Sonda da Parte 105: sin/cos/tan/atan2 da libm, 10000 argumentos x=k/1000, para medir se divergem entre Python e Java (6a face da fronteira).
// Nao e rodada do dialogo. Comparacao por prefixo conta divergencias por funcao.
public class SondaTransc105 {
    static final int N = 10000;

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int k = 1; k <= N; k++) {
            double x = k / 1000.0;
            sb.append("sin ").append(Double.toHexString(Math.sin(x))).append("\n");
            sb.append("cos ").append(Double.toHexString(Math.cos(x))).append("\n");
            sb.append("tan ").append(Double.toHexString(Math.tan(x))).append("\n");
            sb.append("atan2 ").append(Double.toHexString(Math.atan2(x, 1.0))).append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
