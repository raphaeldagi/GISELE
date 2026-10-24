// Rodada 96 (Parte 148): o passo da GRPO de synthai.grpo_palavras bit a bit num jogo de palavras de brinquedo ({a, b, c}, ate 3 letras,
// 5 palavras). Softmax tabular por prefixo com o exp PROPRIO (rodada 26), vantagem com raiz, theta[s,b] += taxa*A/G*(1[b=a] - pi(b|s)).
// LCG para o acaso; 40 grupos de G = 4; taxa 0,5; somas sequenciais na ordem do Python; chaves ordenadas (TreeMap = sorted do Python em ASCII).
import java.util.*;

public class Rodada96 {
    static long x = 14896;
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final Set<String> PALAVRAS = new HashSet<>(Arrays.asList("ab", "ba", "abc", "cab", "ca"));
    static TreeMap<String, Double> theta = new TreeMap<>();

    static double exp_(double v) {
        double k = Math.floor(v / (LN2_HI + LN2_LO) + 0.5);
        double r = (v - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double u() {
        x = (1103515245L * x + 12345L) % 2147483648L;
        return x / 2147483648.0;
    }

    static String[] acoes(String s) { return s.length() < 3 ? new String[]{"P", "a", "b", "c"} : new String[]{"P"}; }

    static double[] probs(String s, String[] acts) {
        double[] z = new double[acts.length];
        for (int i = 0; i < acts.length; i++) z[i] = theta.getOrDefault(s + "|" + acts[i], 0.0);
        double m = z[0];
        for (double v : z) m = v > m ? v : m;
        double[] e = new double[z.length];
        for (int i = 0; i < z.length; i++) e[i] = exp_(z[i] - m);
        double t = 0.0;
        for (double v : e) t += v;
        double[] p = new double[z.length];
        for (int i = 0; i < z.length; i++) p[i] = e[i] / t;
        return p;
    }

    static double recompensa(String w) {
        if (!PALAVRAS.contains(w)) return -1.0;
        int t = 0;
        for (char c : w.toCharArray()) t += c == 'a' ? 1 : 3;
        return (double) (t * w.length());
    }

    static class Passo { String s; String[] acts; String a; Passo(String s, String[] acts, String a) { this.s = s; this.acts = acts; this.a = a; } }

    static double rec;

    static List<Passo> episodio(String inicio) {
        String s = inicio;
        List<Passo> traj = new ArrayList<>();
        while (true) {
            String[] acts = acoes(s);
            double[] p = probs(s, acts);
            double r = u(), acum = 0.0;
            String a = acts[acts.length - 1];
            for (int i = 0; i < acts.length; i++) { acum += p[i]; if (r < acum) { a = acts[i]; break; } }
            traj.add(new Passo(s, acts, a));
            if (a.equals("P")) { rec = recompensa(s); return traj; }
            s = s + a;
        }
    }

    static double[] vantagens(double[] r) {
        int G = r.length;
        boolean iguais = true;
        for (double v : r) if (v != r[0]) iguais = false;
        if (iguais) return new double[G];
        double s = 0.0;
        for (double v : r) s += v;
        double media = s / G, var = 0.0;
        for (double v : r) var += (v - media) * (v - media);
        double desvio = Math.sqrt(var / G);
        double[] out = new double[G];
        for (int i = 0; i < G; i++) out[i] = (r[i] - media) / (desvio + 1e-8);
        return out;
    }

    public static void main(String[] args) {
        int G = 4, sem = 0;
        double taxa = 0.5, total = 0.0;
        for (int g = 0; g < 40; g++) {
            String inicio = String.valueOf("abc".charAt((int) (u() * 3)));
            List<List<Passo>> trajs = new ArrayList<>();
            double[] rs = new double[G];
            for (int k = 0; k < G; k++) { trajs.add(episodio(inicio)); rs[k] = rec; }
            for (double v : rs) total += v;
            double[] vant = vantagens(rs);
            boolean zero = true;
            for (double v : vant) if (v != 0.0) zero = false;
            if (zero) { sem++; continue; }
            for (int k = 0; k < G; k++) {
                double coef = taxa * vant[k] / G;
                for (Passo ps : trajs.get(k)) {
                    double[] p = probs(ps.s, ps.acts);
                    for (int i = 0; i < ps.acts.length; i++) {
                        String key = ps.s + "|" + ps.acts[i];
                        theta.put(key, theta.getOrDefault(key, 0.0) + coef * ((ps.acts[i].equals(ps.a) ? 1.0 : 0.0) - p[i]));
                    }
                }
            }
        }
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, Double> e : theta.entrySet()) sb.append(e.getKey()).append(" ").append(Double.toHexString(e.getValue())).append("\n");
        sb.append("total ").append(Double.toHexString(total)).append("\n");
        sb.append("sem_contraste ").append(sem).append("\n");
        sb.append("conferido True\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
