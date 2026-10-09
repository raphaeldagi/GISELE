// Rodada 10 do diálogo Python <-> Java: as três lógicas difusas (Łukasiewicz, Gödel, produto) em Java, nos mesmos 1000
// pares do gerador da rodada 5. As somas usam a soma compensada do sum() do Python (rodada 5). Uso: java Rodada10
import java.util.function.DoubleBinaryOperator;

public class Rodada10 {
    static long x = 1010L;
    static final long A = 6364136223846793005L, C = 1442695040888963407L;

    static double uniforme() {
        x = A * x + C;
        return (x >>> 11) * 0x1.0p-53;
    }

    static double soma(double[] v) {
        double s = 0.0, c = 0.0;
        for (double y : v) {
            double t = s + y;
            if (Math.abs(s) >= Math.abs(y)) c += (s - t) + y; else c += (y - t) + s;
            s = t;
        }
        return s + c;
    }

    static DoubleBinaryOperator[] logica(String nome) {
        switch (nome) {
            case "lukasiewicz":
                return new DoubleBinaryOperator[]{(a, b) -> Math.max(0.0, a + b - 1.0), (a, b) -> Math.min(1.0, a + b),
                        (a, b) -> Math.min(1.0, 1.0 - a + b)};
            case "godel":
                return new DoubleBinaryOperator[]{Math::min, Math::max, (a, b) -> a <= b ? 1.0 : b};
            default:
                return new DoubleBinaryOperator[]{(a, b) -> a * b, (a, b) -> a + b - a * b, (a, b) -> 1.0 - a + a * b};
        }
    }

    static double[] grad(String nome, double a, double b) {
        if (nome.equals("lukasiewicz")) return a > b ? new double[]{-1.0, 1.0} : new double[]{0.0, 0.0};
        if (nome.equals("godel")) return a > b ? new double[]{0.0, 1.0} : new double[]{0.0, 0.0};
        return new double[]{b - 1.0, a};
    }

    static String h(double v) { return Double.toHexString(v); }

    public static void main(String[] args) {
        double[][] pares = new double[1000][];
        for (int i = 0; i < 1000; i++) { double a = uniforme(); pares[i] = new double[]{a, uniforme()}; }
        for (String nome : new String[]{"lukasiewicz", "godel", "produto"}) {
            DoubleBinaryOperator[] L = logica(nome);
            double a = pares[0][0], b = pares[0][1];
            double[] g = grad(nome, a, b);
            System.out.println(nome + " par 0: T = " + h(L[0].applyAsDouble(a, b)) + " S = " + h(L[1].applyAsDouble(a, b))
                    + " I = " + h(L[2].applyAsDouble(a, b)) + " dI = " + h(g[0]) + " " + h(g[1]));
            double[] t = new double[1000], s = new double[1000], i_ = new double[1000], ga = new double[1000], gb = new double[1000];
            for (int k = 0; k < 1000; k++) {
                double p = pares[k][0], q = pares[k][1];
                t[k] = L[0].applyAsDouble(p, q);
                s[k] = L[1].applyAsDouble(p, q);
                i_[k] = L[2].applyAsDouble(p, q);
                double[] gg = grad(nome, p, q);
                ga[k] = gg[0];
                gb[k] = gg[1];
            }
            System.out.println(nome + " somas: T = " + h(soma(t)) + " S = " + h(soma(s)) + " dIa = " + h(soma(ga)) + " dIb = " + h(soma(gb)));
            System.out.println(nome + " satisfacao = " + h(soma(i_) / 1000));
        }
    }
}
