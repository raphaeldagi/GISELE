// Rodada 69 (Parte 102): o beam search (busca em feixe), bit a bit. A cada passo estende cada hipotese por cada token; escore = SOMA
// de log-probabilidades (log proprio); mantem os K melhores por comparacao (ordenacao estavel). exp/log sao a unica fronteira; somar/ordenar e exato.
import java.util.ArrayList;
import java.util.List;
import java.util.Comparator;

public class Rodada69 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = 1.4142135623730951;
    static final int K = 3;
    static final double[][] PASSOS = {
        {2.0, 1.0, 0.5, 0.0},
        {0.2, 1.5, 0.3, 0.9},
        {1.1, 0.4, 2.2, 0.1},
        {0.7, 0.6, 0.5, 1.9},
    };

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double log_(double x) {
        int e = Math.getExponent(x);
        double m = Math.scalb(x, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    static double[] logprobs(double[] logits) {
        double m = logits[0];
        for (double x : logits) if (x > m) m = x;
        double s = 0.0;
        for (double x : logits) s = s + exp_(x - m);
        double ls = log_(s);
        double[] out = new double[logits.length];
        for (int i = 0; i < logits.length; i++) out[i] = (logits[i] - m) - ls;
        return out;
    }

    static class Hyp {
        List<Integer> seq;
        double sc;
        Hyp(List<Integer> s, double c) { seq = s; sc = c; }
    }

    public static void main(String[] args) {
        List<Hyp> feixe = new ArrayList<>();
        feixe.add(new Hyp(new ArrayList<>(), 0.0));
        for (double[] passo : PASSOS) {
            double[] lp = logprobs(passo);
            List<Hyp> cand = new ArrayList<>();
            for (Hyp h : feixe) {
                for (int tok = 0; tok < passo.length; tok++) {
                    List<Integer> ns = new ArrayList<>(h.seq);
                    ns.add(tok);
                    cand.add(new Hyp(ns, h.sc + lp[tok]));
                }
            }
            cand.sort(new Comparator<Hyp>() {        // estavel, escore decrescente
                public int compare(Hyp a, Hyp b) { return Double.compare(b.sc, a.sc); }
            });
            feixe = new ArrayList<>(cand.subList(0, Math.min(K, cand.size())));
        }
        Hyp best = feixe.get(0);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < best.seq.size(); i++) { if (i > 0) sb.append(' '); sb.append(best.seq.get(i)); }
        System.out.println("melhor " + sb.toString());
        System.out.println("escore " + Double.toHexString(best.sc));
        System.out.println("fim");
    }
}
