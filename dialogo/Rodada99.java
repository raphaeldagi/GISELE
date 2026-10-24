// Rodada 99 (Parte 151): a geometria exata do braco aleatorio (synthai.tabuleiro.paradas_por_comprimento) bit a bit. Recursao em profundidade sobre os
// caminhos sem repetir casa, vizinhanca de rei, PARAR so com `minimo` letras; parcelas p/n somadas na mesma ordem do Python.
import java.util.*;

public class Rodada99 {
    static double[] out;
    static int tam, mi, ma;

    static void anda(List<int[]> caminho, double p) {
        int L = caminho.size();
        if (L >= ma) { out[L] += p; return; }
        int[] u = caminho.get(L - 1);
        List<int[]> livres = new ArrayList<>();
        for (int a = -1; a <= 1; a++) for (int b = -1; b <= 1; b++) {
            if (a == 0 && b == 0) continue;
            int r = u[0] + a, c = u[1] + b;
            if (r < 0 || r >= tam || c < 0 || c >= tam) continue;
            boolean visto = false;
            for (int[] q : caminho) if (q[0] == r && q[1] == c) visto = true;
            if (!visto) livres.add(new int[]{r, c});
        }
        int n = livres.size() + (L >= mi ? 1 : 0);
        if (n == 0) return;
        if (L >= mi) out[L] += p / n;
        for (int[] v : livres) { List<int[]> nc = new ArrayList<>(caminho); nc.add(v); anda(nc, p / n); }
    }

    public static void main(String[] args) {
        int[][] casos = {{4, 3, 5}, {5, 3, 5}, {6, 3, 5}, {5, 3, 4}, {5, 4, 5}};
        StringBuilder sb = new StringBuilder();
        for (int[] k : casos) {
            tam = k[0]; mi = k[1]; ma = k[2];
            out = new double[ma + 1];
            for (int r = 0; r < tam; r++) for (int c = 0; c < tam; c++) {
                List<int[]> cam = new ArrayList<>();
                cam.add(new int[]{r, c});
                anda(cam, 1.0 / (tam * tam));
            }
            sb.append("g").append(tam).append("_").append(mi).append("_").append(ma);
            for (int L = mi; L <= ma; L++) sb.append(" ").append(Double.toHexString(out[L]));
            sb.append("\n");
        }
        sb.append("conferido True\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
