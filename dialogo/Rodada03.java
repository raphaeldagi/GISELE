// Rodada 3 do diálogo Python <-> Java: a avalanche do dicionário com o fecho INCREMENTAL. Lê o grafo e o currículo que
// rodada03.py --preparar PASTA escreveu e imprime no mesmo formato. O tempo vai para a saída de erro.
// Uso: javac Rodada03.java && java Rodada03 PASTA
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

public class Rodada03 {
    static final double[] THETAS = {1.0, 0.9, 0.8, 0.7, 0.6};
    static String[] nome;
    static int[] grau;        // |s|: quantas palavras definem x
    static int[][] usadoPor;  // usadoPor[y] = as palavras em cuja definição y aparece

    public static void main(String[] args) throws Exception {
        List<String> linhas = Files.readAllLines(Path.of(args[0], "grafo03.txt"), StandardCharsets.UTF_8);
        int n = linhas.size();
        nome = new String[n];
        Map<String, Integer> indice = new HashMap<>(2 * n);
        for (int i = 0; i < n; i++) {
            nome[i] = linhas.get(i).substring(0, linhas.get(i).indexOf('\t'));
            indice.put(nome[i], i);
        }
        int[][] defs = new int[n][];
        grau = new int[n];
        int[] usos = new int[n];
        for (int i = 0; i < n; i++) {
            String resto = linhas.get(i).substring(linhas.get(i).indexOf('\t') + 1);
            String[] ps = resto.isEmpty() ? new String[0] : resto.split(" ");
            defs[i] = new int[ps.length];
            grau[i] = ps.length;
            for (int k = 0; k < ps.length; k++) { defs[i][k] = indice.get(ps[k]); usos[defs[i][k]]++; }
        }
        usadoPor = new int[n][];
        for (int y = 0; y < n; y++) usadoPor[y] = new int[usos[y]];
        int[] pos = new int[n];
        for (int x = 0; x < n; x++) for (int y : defs[x]) usadoPor[y][pos[y]++] = x;
        List<String> ordemTxt = Files.readAllLines(Path.of(args[0], "ordem03.txt"), StandardCharsets.UTF_8);
        int[] ordem = new int[ordemTxt.size()];
        for (int i = 0; i < ordem.length; i++) ordem[i] = indice.get(ordemTxt.get(i));

        for (double t : THETAS) {
            long t0 = System.nanoTime();
            long m = Math.round(t * 1000);
            int[] precisa = new int[n], tem = new int[n];
            for (int x = 0; x < n; x++) precisa[x] = (int) Math.floorDiv(m * grau[x] + 999, 1000);
            boolean[] conhecida = new boolean[n];
            int[] pilha = new int[n];  // cada palavra entra na pilha no máximo uma vez: n posições bastam
            int topo = 0, total = 0;
            for (int x = 0; x < n; x++) if (precisa[x] == 0) { conhecida[x] = true; pilha[topo++] = x; total++; }
            total += propagar(pilha, topo, conhecida, tem, precisa);
            int k50 = 2 * total >= n ? 0 : -1, maiorSalto = -1, kSalto = -1;
            for (int k = 0; k < ordem.length; k++) {
                int antes = total, x = ordem[k];
                if (!conhecida[x]) {
                    conhecida[x] = true;
                    pilha[0] = x;
                    total += 1 + propagar(pilha, 1, conhecida, tem, precisa);
                }
                if (total - antes > maiorSalto) { maiorSalto = total - antes; kSalto = k + 1; }
                if (k50 < 0 && 2 * total >= n) k50 = k + 1;
            }
            double dt = (System.nanoTime() - t0) / 1e9;
            System.out.println("theta = " + Double.toHexString(t) + ": k50 = " + k50 + "; maior salto = " + maiorSalto
                    + " palavras, em k = " + kSalto + " (" + nome[ordem[kSalto - 1]] + ")");
            System.err.printf("tempo java theta %s: %.3f s%n", t, dt);
        }
    }

    // propaga a partir da pilha; devolve quantas palavras novas ficaram conhecidas
    static int propagar(int[] pilha, int topo, boolean[] conhecida, int[] tem, int[] precisa) {
        int novas = 0;
        while (topo > 0) {
            int y = pilha[--topo];
            for (int x : usadoPor[y]) {
                if (conhecida[x]) continue;
                if (++tem[x] >= precisa[x]) { conhecida[x] = true; pilha[topo++] = x; novas++; }
            }
        }
        return novas;
    }
}
