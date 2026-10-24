// Rodada 104 (Parte 156): as esperancas exatas das decisoes do episodio (ramificacao_exata, primeira casa) bit a bit, grade 3 x 3, caso B, 3 a 4 letras. Por caminho o vetor
// (acerto, falha, decisoes, opcoes, livres, acoes): filhos somados na ordem das acoes (LinkedHashMap), divididos por n, e depois a decisao do proprio no.
import java.util.*;

public class Rodada104 {
    static int T = 3, MIN = 3, MAX = 4;
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

    static double[] anda(List<Integer> caminho, String prefixo) {
        LinkedHashMap<Character, Integer> acoes = new LinkedHashMap<>();
        int livres = 0;
        if (caminho.size() < MAX) {
            for (int v : viz(caminho.get(caminho.size() - 1))) if (!caminho.contains(v)) {
                livres++;
                if (!acoes.containsKey(grade[v])) acoes.put(grade[v], v);
            }
        }
        boolean parar = caminho.size() >= MIN;
        int n = acoes.size() + (parar ? 1 : 0);
        double[] s = new double[6];
        if (n == 0) { s[1] = 1.0; return s; }
        if (parar) s[0] = dic.contains(prefixo) ? 1.0 : 0.0;
        for (Map.Entry<Character, Integer> e : acoes.entrySet()) {
            List<Integer> nc = new ArrayList<>(caminho);
            nc.add(e.getValue());
            double[] f = anda(nc, prefixo + e.getKey());
            for (int k = 0; k < 6; k++) s[k] = s[k] + f[k];
        }
        for (int k = 0; k < 6; k++) s[k] = s[k] / n;
        s[2] += 1.0;
        s[3] += n;
        s[4] += livres;
        s[5] += acoes.size();
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
        double[] tot = new double[6];
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
                for (int k = 0; k < 6; k++) tot[k] += peso * f[k] / 9;
            }
        }
        String[] nomes = {"acerto", "falha", "decisoes", "opcoes", "livres", "acoes"};
        for (int k = 0; k < 6; k++) System.out.println(nomes[k] + " " + Double.toHexString(tot[k]));
        System.out.println("conferido True\nfim");
    }
}
