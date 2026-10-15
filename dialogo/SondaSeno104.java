// Sonda da Parte 104: a sin/cos NAIVE da libm na codificacao posicional (mesmas frequencias portaveis via sqrt da rodada 71, so trocando a
// transcendental). Nao e rodada do dialogo. Resultado nesta maquina: IGUAL ao Python (sin nao e fronteira aqui).
public class SondaSeno104 {
    static final int D = 8;
    static final int[] POS = {0, 1, 2, 5, 13, 40};

    static double[] freqs() {
        double r = 1.0 / Math.sqrt(Math.sqrt(10000.0));
        double[] w = new double[D / 2];
        double cur = 1.0;
        for (int i = 0; i < D / 2; i++) { w[i] = cur; cur = cur * r; }
        return w;
    }

    static double[] pe(int pos) {
        double[] w = freqs();
        double[] v = new double[D];
        for (int i = 0; i < D / 2; i++) {
            double arg = pos * w[i];
            v[2 * i] = Math.sin(arg);     // NAIVE: a sin da libm
            v[2 * i + 1] = Math.cos(arg);
        }
        return v;
    }

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int pos : POS) {
            sb.append("naive ").append(pos);
            for (double v : pe(pos)) sb.append(" ").append(Double.toHexString(v));
            sb.append("\n");
        }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
