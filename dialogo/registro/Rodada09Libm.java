// Rodada 9 do diálogo Python <-> Java: a média bayesiana de modelos (ThompsonMistura) em Java. Reusa a atualização da
// rodada 8 para cada modelo e soma os logs das preditivas. Tudo o que o Python soma com sum() é somado aqui com a soma
// compensada (rodada 5); exp e log são os da classe Math. Uso: java Rodada09
import java.util.*;

public class Rodada09Libm {
    static long x = 909L;
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

    static double somaPesos(List<double[]> hs) {
        double[] v = new double[hs.size()];
        for (int i = 0; i < v.length; i++) v[i] = hs.get(i)[0];
        return soma(v);
    }

    static void cortar(List<double[]> hs, int n) {
        hs.sort((p, q) -> Double.compare(-p[0], -q[0]));
        while (hs.size() > n) hs.remove(hs.size() - 1);
    }

    // um ThompsonBOCPD: k braços, cada um uma lista de hipóteses {peso, a, b}
    static void atualizarBOCPD(List<List<double[]>> mist, double H, int br, int r, int n) {
        for (List<double[]> hs : mist) {
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
        cortar(hs, n);
        double tot = somaPesos(hs);
        for (double[] h : hs) h[0] /= tot;
        for (int i = 0; i < mist.size(); i++) {
            List<double[]> o = mist.get(i);
            if (i != br && o.size() > n) {
                cortar(o, n);
                double t2 = somaPesos(o);
                for (double[] h : o) h[0] /= t2;
            }
        }
    }

    static double[] pesos(double[] logw) {
        double m = logw[0];
        for (double v : logw) m = Math.max(m, v);
        double[] e = new double[logw.length];
        for (int i = 0; i < e.length; i++) e[i] = Math.exp(logw[i] - m);
        double t = soma(e);
        for (int i = 0; i < e.length; i++) e[i] /= t;
        return e;
    }

    public static void main(String[] args) {
        int k = 3, n = 16;
        double[] riscos = {0.0, 1.0 / 2000, 1.0 / 500, 1.0 / 100};
        List<List<List<double[]>>> modelos = new ArrayList<>();
        for (double H : riscos) {
            List<List<double[]>> mist = new ArrayList<>();
            for (int i = 0; i < k; i++) mist.add(new ArrayList<>(List.of(new double[]{1.0, 1.0, 1.0})));
            modelos.add(mist);
        }
        double[] logw = new double[4], perda = new double[4];
        double perdaMistura = 0.0;
        for (int passo = 0; passo < 1200; passo++) {
            double[] ps = passo < 600 ? new double[]{0.2, 0.5, 0.8} : new double[]{0.8, 0.5, 0.2};
            int br = passo % 3;
            int r = uniforme() < ps[br] ? 1 : 0;
            double[] ws = pesos(logw), preds = new double[4];
            for (int m = 0; m < 4; m++) {
                List<double[]> hs = modelos.get(m).get(br);
                double[] termos = new double[hs.size()];
                for (int i = 0; i < termos.length; i++) {
                    double[] h = hs.get(i);
                    termos[i] = h[0] * ((r == 1 ? h[1] : h[2]) / (h[1] + h[2]));
                }
                preds[m] = (1 - riscos[m]) * soma(termos) + riscos[m] * 0.5;
            }
            double[] wp = new double[4];
            for (int m = 0; m < 4; m++) wp[m] = ws[m] * preds[m];
            perdaMistura -= Math.log(soma(wp));
            for (int m = 0; m < 4; m++) { logw[m] += Math.log(preds[m]); perda[m] -= Math.log(preds[m]); }
            for (int m = 0; m < 4; m++) atualizarBOCPD(modelos.get(m), riscos[m], br, r, n);
        }
        StringBuilder a = new StringBuilder("logw ="), b = new StringBuilder("perda ="), c = new StringBuilder("pesos =");
        double[] ws = pesos(logw);
        for (int m = 0; m < 4; m++) {
            a.append(' ').append(Double.toHexString(logw[m]));
            b.append(' ').append(Double.toHexString(perda[m]));
            c.append(' ').append(Double.toHexString(ws[m]));
        }
        System.out.println(a);
        System.out.println(b);
        System.out.println("perda da mistura = " + Double.toHexString(perdaMistura));
        System.out.println(c);
    }
}
