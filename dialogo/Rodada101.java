// Rodada 101 (Parte 153): o braco aleatorio EXATO (synthai.tabuleiro.aleatorio_exato) bit a bit, grade 3 x 3. Todas as atribuicoes de letras (a ultima
// casa varia mais depressa), peso = produto na ordem das casas; recursao sobre os caminhos com as acoes por letra na ordem de insercao (LinkedHashMap).
import java.util.*;

public class Rodada101 {
    static int T = 3, MIN = 3, MAX = 5;
    static char[] grade = new char[9];
    static Set<String> dic;

    static List<Integer> viz(int u) {
        int r = u / T, c = u % T;
        List<Integer> l = new ArrayList<>();
        for (int a = -1; a <= 1; a++) for (int b = -1; b <= 1; b++) {
            if (a == 0 && b == 0) continue;
            int rr = r + a, cc = c + b;
            if (rr >= 0 && rr < T && cc >= 0 && cc < T) l.add(rr * T + cc);
        }
        return l;
    }

    static double anda(List<Integer> caminho, String prefixo) {
        LinkedHashMap<Character, Integer> acoes = new LinkedHashMap<>();
        if (caminho.size() < MAX) {
            for (int v : viz(caminho.get(caminho.size() - 1))) if (!caminho.contains(v) && !acoes.containsKey(grade[v])) acoes.put(grade[v], v);
        }
        boolean parar = caminho.size() >= MIN;
        int n = acoes.size() + (parar ? 1 : 0);
        if (n == 0) return 0.0;
        double s = parar ? (dic.contains(prefixo) ? 1.0 : 0.0) : 0.0;
        for (Map.Entry<Character, Integer> e : acoes.entrySet()) {
            List<Integer> nc = new ArrayList<>(caminho);
            nc.add(e.getValue());
            s += anda(nc, prefixo + e.getKey());
        }
        return s / n;
    }

    static List<String> palavras(String alfa) {
        List<String> out = new ArrayList<>();
        for (int L = 3; L <= 5; L++) {
            int k = alfa.length(), tot = 1;
            for (int i = 0; i < L; i++) tot *= k;
            for (int x = 0; x < tot; x++) {
                char[] w = new char[L];
                int y = x;
                for (int i = L - 1; i >= 0; i--) { w[i] = alfa.charAt(y % k); y /= k; }
                out.add(new String(w));
            }
        }
        return out;
    }

    static double exato(Set<String> d, String letras, double[] pesos) {
        dic = d;
        double t = 0.0;
        for (double w : pesos) t += w;
        double[] p = new double[pesos.length];
        for (int i = 0; i < p.length; i++) p[i] = pesos[i] / t;
        int k = letras.length(), tot = 1;
        for (int i = 0; i < 9; i++) tot *= k;
        double total = 0.0;
        for (int x = 0; x < tot; x++) {
            int[] idx = new int[9];
            int y = x;
            for (int i = 8; i >= 0; i--) { idx[i] = y % k; y /= k; }
            double peso = 1.0;
            for (int i = 0; i < 9; i++) { grade[i] = letras.charAt(idx[i]); }
            for (int i = 0; i < 9; i++) peso = peso * p[idx[i]];
            double acerto = 0.0;
            for (int u = 0; u < 9; u++) {
                List<Integer> cam = new ArrayList<>();
                cam.add(u);
                acerto += anda(cam, String.valueOf(grade[u]));
            }
            total += peso * acerto / 9;
        }
        return total;
    }

    public static void main(String[] args) {
        Set<String> A = new HashSet<>();
        for (String w : palavras("ab")) if (w.charAt(0) == 'a' && w.charAt(w.length() - 1) == 'b') A.add(w);
        Set<String> B = new HashSet<>();
        for (String w : palavras("abc")) {
            boolean ok = true;
            for (int i = 1; i < w.length(); i++) if (w.charAt(i) == w.charAt(i - 1)) ok = false;
            if (ok) B.add(w);
        }
        double ea = exato(A, "ab", new double[]{0.7, 0.3});
        double eb = exato(B, "abc", new double[]{0.5, 0.3, 0.2});
        System.out.println("A' " + Double.toHexString(ea) + "\nB " + Double.toHexString(eb) + "\nconferido True\nfim");
    }
}
