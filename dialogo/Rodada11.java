// Rodada 11 do diálogo Python <-> Java: o fecho das definições em português (θ = 0,6, as 300 palavras mais usadas nas
// glosas da OpenWordNet-PT como âncoras), a partir do grafo que rodada11.py --preparar PASTA exportou. O teto de θ·|s| é o
// inteiro da rodada 2. A ordenação das palavras com acento: String.compareTo compara unidades UTF-16, o sorted() do Python
// compara pontos de código; dentro do plano básico (todas as letras do português) as duas ordens coincidem. Uso: java Rodada11 PASTA
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;

public class Rodada11 {
    public static void main(String[] args) throws Exception {
        List<String> linhas = Files.readAllLines(Path.of(args[0], "grafo11.txt"), StandardCharsets.UTF_8);
        int n = linhas.size();
        String[] nome = new String[n];
        Map<String, Integer> indice = new HashMap<>(2 * n);
        for (int i = 0; i < n; i++) { nome[i] = linhas.get(i).split("\t", -1)[0]; indice.put(nome[i], i); }
        int[][] defs = new int[n][];
        boolean[] definida = new boolean[n];
        List<List<Integer>> usadoPor = new ArrayList<>();
        for (int i = 0; i < n; i++) usadoPor.add(new ArrayList<>());
        int nDef = 0;
        for (int i = 0; i < n; i++) {
            String[] c = linhas.get(i).split("\t", -1);
            String[] ps = c[1].isEmpty() ? new String[0] : c[1].split(" ");
            defs[i] = new int[ps.length];
            for (int k = 0; k < ps.length; k++) { defs[i][k] = indice.get(ps[k]); usadoPor.get(defs[i][k]).add(i); }
            definida[i] = c[2].equals("1");
            if (definida[i]) nDef++;
        }
        boolean[] conhecida = new boolean[n];
        int[] tem = new int[n], precisa = new int[n];
        for (int i = 0; i < n; i++) precisa[i] = (int) Math.floorDiv(600L * defs[i].length + 999, 1000);
        ArrayDeque<Integer> pilha = new ArrayDeque<>();
        for (String w : Files.readAllLines(Path.of(args[0], "ordem11.txt"), StandardCharsets.UTF_8)) {
            int i = indice.get(w);
            if (!conhecida[i]) { conhecida[i] = true; pilha.push(i); }
        }
        // como no Python: uma palavra COM definição e sem nenhuma palavra que a defina é entendida de saída;
        // as palavras sem definição não têm entrada no grafo do Python e só entram como âncoras
        for (int i = 0; i < n; i++) if (definida[i] && !conhecida[i] && precisa[i] == 0) { conhecida[i] = true; pilha.push(i); }
        while (!pilha.isEmpty()) {
            int y = pilha.pop();
            for (int x : usadoPor.get(y)) {
                if (conhecida[x] || !definida[x]) continue;
                if (++tem[x] >= precisa[x]) { conhecida[x] = true; pilha.push(x); }
            }
        }
        List<String> ent = new ArrayList<>();
        for (int i = 0; i < n; i++) if (conhecida[i] && definida[i]) ent.add(nome[i]);
        Collections.sort(ent);
        byte[] h = MessageDigest.getInstance("SHA-256").digest(String.join("\n", ent).getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : h) sb.append(String.format("%02x", b));
        System.out.println("lemas definidos em portugues = " + nDef + "; palavras no grafo = " + n);
        System.out.println("entendidos (theta 0,6, 300 ancoras) = " + ent.size() + "; sha = " + sb);
    }
}
