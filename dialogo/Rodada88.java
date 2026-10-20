// Rodada 88 (Parte 120): o CFR VANILLA no poquer Leduc, bit a bit. Regras: 6 cartas, carta publica, apostas 2 e 4, no maximo 2
// aumentos por rodada; as 120 distribuicoes na ordem de itertools.permutations; T = 3; imprime a estrategia MEDIA dos 288 conjuntos em
// ordem de chave. So +,-,*,/, max e comparacoes, na mesma ordem do Python.
import java.util.*;

public class Rodada88 {
    static final int T = 3;
    static final int[] APOSTA = {2, 4};
    static TreeMap<String, double[]> REG = new TreeMap<>(), SOMA = new TreeMap<>();

    static String ultimaRodada(String h) {
        int i = h.lastIndexOf('/');
        return i < 0 ? h : h.substring(i + 1);
    }

    static int nRodada(String h) {
        int n = 0;
        for (char ch : h.toCharArray()) if (ch == '/') n++;
        return n;
    }

    static int contar(String s, char c) {
        int n = 0;
        for (char ch : s.toCharArray()) if (ch == c) n++;
        return n;
    }

    static String[] acoes(String h) {
        String s = ultimaRodada(h);
        if (s.endsWith("r")) return contar(s, 'r') < 2 ? new String[]{"f", "c", "r"} : new String[]{"f", "c"};
        return new String[]{"c", "r"};
    }

    static int jogador(String h) {
        return ultimaRodada(h).length() % 2;
    }

    static boolean acabou(String s) {
        return s.equals("cc") || (s.length() >= 2 && s.endsWith("rc"));
    }

    static String proximo(String h, String a) {
        String h2 = h + a;
        return (nRodada(h2) == 0 && acabou(ultimaRodada(h2))) ? h2 + "/" : h2;
    }

    static int[] contribuicoes(String h) {
        int[] pos = {1, 1};
        String[] rodadas = h.split("/", -1);
        for (int r = 0; r < rodadas.length; r++) {
            String s = rodadas[r];
            int[] devido = {0, 0};
            for (int i = 0; i < s.length(); i++) {
                char a = s.charAt(i);
                if (a == 'c') devido[i % 2] = Math.max(devido[0], devido[1]);
                else if (a == 'r') devido[i % 2] = Math.max(devido[0], devido[1]) + APOSTA[r];
            }
            pos[0] += devido[0];
            pos[1] += devido[1];
        }
        return pos;
    }

    static Double terminal(String h, int c1, int c2, int b) {
        String s = ultimaRodada(h);
        int r = nRodada(h);
        if (s.endsWith("f")) {
            int[] pos = contribuicoes(h.substring(0, h.length() - 1));
            return (s.length() - 1) % 2 == 0 ? -(double) pos[0] : (double) pos[1];
        }
        if (r == 1 && acabou(s)) {
            int[] pos = contribuicoes(h);
            int f1 = c1 == b ? 10 + c1 : c1, f2 = c2 == b ? 10 + c2 : c2;
            return f1 > f2 ? (double) pos[1] : (f2 > f1 ? -(double) pos[0] : 0.0);
        }
        return null;
    }

    static String chave(String h, int c1, int c2, int b) {
        int j = jogador(h);
        return (j == 0 ? c1 : c2) + "|" + (h.contains("/") ? b : -1) + "|" + h;
    }

    static double[] estrategia(String k, int n) {
        double[] u = new double[n];
        Arrays.fill(u, 1.0 / n);
        double[] r = REG.get(k);
        if (r == null) return u;
        double[] pos = new double[n];
        double s = 0.0;
        for (int i = 0; i < n; i++) pos[i] = r[i] > 0.0 ? r[i] : 0.0;
        for (int i = 0; i < n; i++) s += pos[i];
        if (!(s > 0.0)) return u;
        for (int i = 0; i < n; i++) pos[i] = pos[i] / s;
        return pos;
    }

    static double cfr(int c1, int c2, int b, String h, double p1, double p2) {
        Double u = terminal(h, c1, c2, b);
        if (u != null) return u;
        int j = jogador(h);
        String[] acs = acoes(h);
        int n = acs.length;
        String k = chave(h, c1, c2, b);
        double[] s = estrategia(k, n);
        double[] util = new double[n];
        double no = 0.0;
        for (int i = 0; i < n; i++) {
            util[i] = j == 0 ? cfr(c1, c2, b, proximo(h, acs[i]), p1 * s[i], p2) : cfr(c1, c2, b, proximo(h, acs[i]), p1, p2 * s[i]);
            no += s[i] * util[i];
        }
        double sinal = j == 0 ? 1.0 : -1.0;
        double adv = j == 0 ? p2 : p1, prop = j == 0 ? p1 : p2;
        double[] r = REG.computeIfAbsent(k, z -> new double[n]);
        double[] m = SOMA.computeIfAbsent(k, z -> new double[n]);
        for (int i = 0; i < n; i++) {
            r[i] += adv * sinal * (util[i] - no);
            m[i] += prop * s[i];
        }
        return no;
    }

    public static void main(String[] args) {
        List<int[]> dist = new ArrayList<>();
        for (int a = 0; a < 6; a++)
            for (int b = 0; b < 6; b++)
                for (int c = 0; c < 6; c++)
                    if (a != b && a != c && b != c) dist.add(new int[]{a / 2, b / 2, c / 2});
        for (int t = 0; t < T; t++)
            for (int[] d : dist) cfr(d[0], d[1], d[2], "", 1.0, 1.0);
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, double[]> e : SOMA.entrySet()) {
            double[] m = e.getValue();
            double s = 0.0;
            for (double x : m) s += x;
            sb.append(e.getKey());
            for (double x : m) sb.append(" ").append(Double.toHexString(s > 0.0 ? x / s : 1.0 / m.length));
            sb.append("\n");
        }
        sb.append("fim ").append(SOMA.size());
        System.out.println(sb.toString());
    }
}
