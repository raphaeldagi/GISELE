// Rodada 15 do diálogo Python <-> Java: a detecção de mudança no nível do mundo (ThompsonBOCPDGlobal) em Java. Uma lista
// de hipóteses {peso, a[k], b[k]}; o risco cria (ou engorda) a hipótese com tudo em Beta(1, 1); a observação de um braço
// pesa TODAS as hipóteses pela preditiva desse braço. Soma compensada (rodada 5) e ordenação estável (rodada 8).
// Uso: java Rodada15
import java.util.*;

public class Rodada15 {
    static long x = 1515L;
    static final long A = 6364136223846793005L, C = 1442695040888963407L;

    static double uniforme() {
        x = A * x + C;
        return (x >>> 11) * 0x1.0p-53;
    }

    static double somaPesos(List<double[][]> hs) {
        double s = 0.0, c = 0.0;
        for (double[][] h : hs) {
            double y = h[0][0], t = s + y;
            if (Math.abs(s) >= Math.abs(y)) c += (s - t) + y; else c += (y - t) + s;
            s = t;
        }
        return s + c;
    }

    static boolean fresca(double[][] h) {
        for (double v : h[1]) if (v != 1.0) return false;
        for (double v : h[2]) if (v != 1.0) return false;
        return true;
    }

    static String h(double v) { return Double.toHexString(v); }

    public static void main(String[] args) {
        int k = 3, n = 16;
        double H = 1.0 / 50;
        List<double[][]> hs = new ArrayList<>();
        hs.add(new double[][]{{1.0}, {1, 1, 1}, {1, 1, 1}});
        for (int passo = 0; passo < 1200; passo++) {
            double[] ps = passo < 600 ? new double[]{0.2, 0.5, 0.8} : new double[]{0.8, 0.5, 0.2};
            int br = passo % 3;
            int r = uniforme() < ps[br] ? 1 : 0;
            for (double[][] hp : hs) hp[0][0] *= 1 - H;
            double[][] nova = null;
            for (double[][] hp : hs) if (fresca(hp)) { nova = hp; break; }
            if (nova == null) hs.add(new double[][]{{H}, {1, 1, 1}, {1, 1, 1}}); else nova[0][0] += H;
            for (double[][] hp : hs) {
                double a = hp[1][br], b = hp[2][br];
                hp[0][0] *= (r == 1 ? a : b) / (a + b);
                if (r == 1) hp[1][br] += 1; else hp[2][br] += 1;
            }
            hs.sort((p, q) -> Double.compare(-p[0][0], -q[0][0]));
            while (hs.size() > n) hs.remove(hs.size() - 1);
            double tot = somaPesos(hs);
            for (double[][] hp : hs) hp[0][0] /= tot;
        }
        System.out.println(hs.size() + " hipoteses");
        for (double[][] hp : hs)
            System.out.println(h(hp[0][0]) + " | " + h(hp[1][0]) + " " + h(hp[1][1]) + " " + h(hp[1][2]) + " | "
                    + h(hp[2][0]) + " " + h(hp[2][1]) + " " + h(hp[2][2]));
        double[][] top = hs.get(0);
        int obs = (int) (top[1][0] + top[1][1] + top[1][2] + top[2][0] + top[2][1] + top[2][2] - 6);
        System.out.println("observacoes da mais pesada = " + obs);
    }
}
