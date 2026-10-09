// Rodada 2 do diálogo Python <-> Java: a IA-Java reescreve o fecho parcial do dicionário (synthai/dicionario.py, P381).
// Lê o grafo que rodada02.py --preparar PASTA escreveu (PASTA/grafo02.txt) e imprime no mesmo formato que rodada02.py.
// Uso: javac Rodada02.java && java Rodada02 PASTA
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;

public class Rodada02 {
    static final double[] THETAS = {1.0, 0.9, 0.8, 0.7, 0.6};
    static final int ANCORAS = 2000;

    // O grafo em Java: as palavras viram inteiros (0..n-1, na ordem alfabética do arquivo) e as arestas viram arrays de int.
    static String[] nome;
    static int[][] defs;      // defs[x] = as palavras que definem x
    static int[][] usadoPor;  // usadoPor[y] = as palavras em cuja definição y aparece

    static void ler(Path arquivo) throws Exception {
        List<String> linhas = Files.readAllLines(arquivo, StandardCharsets.UTF_8);
        int n = linhas.size();
        nome = new String[n];
        Map<String, Integer> indice = new HashMap<>(2 * n);
        for (int i = 0; i < n; i++) {
            nome[i] = linhas.get(i).substring(0, linhas.get(i).indexOf('\t'));
            indice.put(nome[i], i);
        }
        defs = new int[n][];
        int[] grau = new int[n];
        for (int i = 0; i < n; i++) {
            String resto = linhas.get(i).substring(linhas.get(i).indexOf('\t') + 1);
            String[] ps = resto.isEmpty() ? new String[0] : resto.split(" ");
            defs[i] = new int[ps.length];
            for (int k = 0; k < ps.length; k++) {
                defs[i][k] = indice.get(ps[k]);
                grau[defs[i][k]]++;
            }
        }
        usadoPor = new int[n][];
        for (int y = 0; y < n; y++) usadoPor[y] = new int[grau[y]];
        int[] pos = new int[n];
        for (int x = 0; x < n; x++) for (int y : defs[x]) usadoPor[y][pos[y]++] = x;
    }

    static int tetoInteiro(double theta, int n) {  // -(-round(1000·theta)·n // 1000), como no Python
        long m = Math.round(theta * 1000) * (long) n;
        return (int) Math.floorDiv(m + 999, 1000);
    }

    static BitSet fecho(int[] ancoras, double theta, boolean ingenuo) {
        int n = nome.length;
        BitSet conhecidas = new BitSet(n);
        int[] precisa = new int[n], tem = new int[n];
        ArrayDeque<Integer> pilha = new ArrayDeque<>();
        for (int x = 0; x < n; x++)
            precisa[x] = ingenuo ? (int) Math.ceil(theta * defs[x].length) : tetoInteiro(theta, defs[x].length);
        for (int a : ancoras) if (!conhecidas.get(a)) { conhecidas.set(a); pilha.push(a); }
        for (int x = 0; x < n; x++) if (!conhecidas.get(x) && precisa[x] == 0) { conhecidas.set(x); pilha.push(x); }
        while (!pilha.isEmpty()) {
            int y = pilha.pop();
            for (int x : usadoPor[y]) {
                if (conhecidas.get(x)) continue;
                if (++tem[x] >= precisa[x]) { conhecidas.set(x); pilha.push(x); }
            }
        }
        return conhecidas;
    }

    static String sha(List<String> palavras) throws Exception {
        List<String> ordem = new ArrayList<>(palavras);
        Collections.sort(ordem);
        byte[] h = MessageDigest.getInstance("SHA-256").digest(String.join("\n", ordem).getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : h) sb.append(String.format("%02x", b));
        return sb.toString();
    }

    static List<String> nomes(BitSet b) {
        List<String> r = new ArrayList<>();
        for (int i = b.nextSetBit(0); i >= 0; i = b.nextSetBit(i + 1)) r.add(nome[i]);
        return r;
    }

    public static void main(String[] args) throws Exception {
        ler(Path.of(args[0], "grafo02.txt"));
        int n = nome.length;
        long arestas = 0;
        for (int[] d : defs) arestas += d.length;
        Integer[] ordem = new Integer[n];
        for (int i = 0; i < n; i++) ordem[i] = i;
        // as que mais definem; empate pela ordem alfabética (os índices já estão em ordem alfabética)
        Arrays.sort(ordem, (a, b) -> usadoPor[a].length != usadoPor[b].length
                ? Integer.compare(usadoPor[b].length, usadoPor[a].length) : Integer.compare(a, b));
        int[] ancoras = new int[ANCORAS];
        List<String> nomesAncoras = new ArrayList<>();
        for (int i = 0; i < ANCORAS; i++) { ancoras[i] = ordem[i]; nomesAncoras.add(nome[ordem[i]]); }
        System.out.println("palavras = " + n + ", arestas = " + arestas);
        System.out.println("ancoras = " + ANCORAS + ", sha = " + sha(nomesAncoras));
        for (double t : THETAS) {
            List<String> a = nomes(fecho(ancoras, t, false)), b = nomes(fecho(ancoras, t, true));
            System.out.println("theta = " + Double.toHexString(t) + ": inteiro n = " + a.size() + " sha = " + sha(a)
                    + "; ingenuo n = " + b.size() + " sha = " + sha(b));
        }
    }
}
