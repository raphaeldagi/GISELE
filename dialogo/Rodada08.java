// Rodada 8 do diálogo Python <-> Java: a atualização da ThompsonBOCPD em Java. Duas armadilhas da tradução, ambas das
// rodadas anteriores: o sum() do Python é a soma compensada de Neumaier (rodada 5), e o sort do Python é estável, como o
// Collections.sort (TimSort) do Java: hipóteses com o mesmo peso ficam na ordem em que estavam. Uso: java Rodada08
import java.util.*;

public class Rodada08 {
    static long x = 808L;
    static final long A = 6364136223846793005L, C = 1442695040888963407L;

    static double uniforme() {
        x = A * x + C;
        return (x >>> 11) * 0x1.0p-53;
    }

    static double somaPython(List<double[]> hs) {
        double s = 0.0, c = 0.0;
        for (double[] h : hs) {
            double y = h[0], t = s + y;
            if (Math.abs(s) >= Math.abs(y)) c += (s - t) + y; else c += (y - t) + s;
            s = t;
        }
        return s + c;
    }

    static void ordenarECortar(List<double[]> hs, int n) {
        hs.sort((p, q) -> Double.compare(-p[0], -q[0]));  // a chave -h[0] do Python, estável
        while (hs.size() > n) hs.remove(hs.size() - 1);
    }

    public static void main(String[] args) {
        int k = 3, n = 16;
        double H = 1.0 / 50;
        List<List<double[]>> mist = new ArrayList<>();
        for (int i = 0; i < k; i++) mist.add(new ArrayList<>(List.of(new double[]{1.0, 1.0, 1.0})));
        for (int passo = 0; passo < 1200; passo++) {
            double[] ps = passo < 600 ? new double[]{0.2, 0.5, 0.8} : new double[]{0.8, 0.5, 0.2};
            int br = passo % 3;
            int r = uniforme() < ps[br] ? 1 : 0;
            for (List<double[]> hs : mist) {  // o risco, em todos os braços
                for (double[] h : hs) h[0] *= 1 - H;
                boolean achou = false;
                for (double[] h : hs) if (h[1] == 1.0 && h[2] == 1.0) { h[0] += H; achou = true; break; }
                if (!achou) hs.add(new double[]{H, 1.0, 1.0});
            }
            List<double[]> hs = mist.get(br);
            for (double[] h : hs) {
                h[0] *= (r == 1 ? h[1] : h[2]) / (h[1] + h[2]);
                if (r == 1) h[1] += 1; else h[2] += 1;
            }
            ordenarECortar(hs, n);
            double tot = somaPython(hs);
            for (double[] h : hs) h[0] /= tot;
            for (int i = 0; i < k; i++) {
                List<double[]> o = mist.get(i);
                if (i != br && o.size() > n) {
                    ordenarECortar(o, n);
                    double t2 = somaPython(o);
                    for (double[] h : o) h[0] /= t2;
                }
            }
        }
        for (int i = 0; i < k; i++) {
            List<double[]> hs = mist.get(i);
            System.out.println("braco " + i + ": " + hs.size() + " hipoteses");
            for (double[] h : hs)
                System.out.println("  " + Double.toHexString(h[0]) + " " + Double.toHexString(h[1]) + " " + Double.toHexString(h[2]));
        }
    }
}
