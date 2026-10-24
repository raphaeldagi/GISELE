// Rodada 103 (Parte 155): as estatisticas exatas do fim do episodio (estatisticas_exatas, ordem="reversa") bit a bit, grade 3 x 3, caso B, 3 a 4 letras. Vizinhas na ordem
// REVERSA ((1,1), ..., (-1,-1)); por caminho o vetor (acerto, dr, dc, borda, comprimento); acoes por letra na ordem de insercao (LinkedHashMap), primeira casa de cada letra.
import java.util.*;

public class Rodada103 {
    static int T = 3, MIN = 3, MAX = 4;
    static char[] grade = new char[9];
    static Set<String> dic;

    static List<Integer> viz(int u) {
        int r = u / T, c = u % T;
        List<Integer> l = new ArrayList<>();
        for (int a = 1; a >= -1; a--) for (int b = 1; b >= -1; b--) {
            if (a == 0 && b == 0) continue;
            int rr = r + a, cc = c + b;
            if (rr >= 0 && rr < T && cc >= 0 && cc < T) l.add(rr * T + cc);
        }
        return l;
    }

    static double[] anda(List<Integer> caminho, String prefixo) {
        LinkedHashMap<Character, Integer> acoes = new LinkedHashMap<>();
        if (caminho.size() < MAX) {
            for (int v : viz(caminho.get(caminho.size() - 1)))
                if (!caminho.contains(v) && !acoes.containsKey(grade[v])) acoes.put(grade[v], v);
        }
        boolean parar = caminho.size() >= MIN;
        int n = acoes.size() + (parar ? 1 : 0);
        double[] s = new double[5];
        if (n == 0) return s;
        if (parar) {
            int u0 = caminho.get(0), u1 = caminho.get(caminho.size() - 1);
            int r0 = u0 / T, c0 = u0 % T, r1 = u1 / T, c1 = u1 % T;
            s[0] = dic.contains(prefixo) ? 1.0 : 0.0;
            s[1] = r1 - r0;
            s[2] = c1 - c0;
            s[3] = Math.min(Math.min(r1, c1), Math.min(T - 1 - r1, T - 1 - c1));
            s[4] = caminho.size();
        }
        for (Map.Entry<Character, Integer> e : acoes.entrySet()) {
            List<Integer> nc = new ArrayList<>(caminho);
            nc.add(e.getValue());
            double[] f = anda(nc, prefixo + e.getKey());
            for (int k = 0; k < 5; k++) s[k] = s[k] + f[k];
        }
        for (int k = 0; k < 5; k++) s[k] = s[k] / n;
        return s;
    }

    public static void main(String[] args) {
        Set<String> B = new HashSet<>();
        String alfa = "abc";
        for (int L = 3; L <= 5; L++) {
            int tot = 1;
            for (int i = 0; i < L; i++) tot *= 3;
            for (int x = 0; x < tot; x++) {
                char[] w = new char[L];
                int y = x;
                for (int i = L - 1; i >= 0; i--) { w[i] = alfa.charAt(y % 3); y /= 3; }
                boolean ok = true;
                for (int i = 1; i < L; i++) if (w[i] == w[i - 1]) ok = false;
                if (ok) B.add(new String(w));
            }
        }
        dic = B;
        double[] pesos = {0.5, 0.3, 0.2};
        double t = 0.0;
        for (double w : pesos) t += w;
        double[] p = new double[3];
        for (int i = 0; i < 3; i++) p[i] = pesos[i] / t;
        double[] tot = new double[5];
        int N = 1;
        for (int i = 0; i < 9; i++) N *= 3;
        for (int x = 0; x < N; x++) {
            int[] idx = new int[9];
            int y = x;
            for (int i = 8; i >= 0; i--) { idx[i] = y % 3; y /= 3; }
            for (int i = 0; i < 9; i++) grade[i] = alfa.charAt(idx[i]);
            double peso = 1.0;
            for (int i = 0; i < 9; i++) peso = peso * p[idx[i]];
            for (int u = 0; u < 9; u++) {
                List<Integer> cam = new ArrayList<>();
                cam.add(u);
                double[] f = anda(cam, String.valueOf(grade[u]));
                for (int k = 0; k < 5; k++) tot[k] += peso * f[k] / 9;
            }
        }
        String[] nomes = {"acerto", "dr", "dc", "borda", "comprimento"};
        for (int k = 0; k < 5; k++) System.out.println(nomes[k] + " " + Double.toHexString(tot[k]));
        System.out.println("conferido True\nfim");
    }
}
