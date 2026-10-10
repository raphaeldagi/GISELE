// Rodada 46 do diálogo Python <-> Java: o motor de Horn em tempo linear (Dowling e Gallier, 1984). Lê PASTA/horn46.txt (os fatos e as regras "p ⇒ c" da
// hiperonímia dos substantivos que o Python gravou) e roda o mesmo algoritmo (contadores de premissas, fila FIFO: ArrayDeque, como o texto recebido sugeria).
// Uso: java Rodada46 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada46 {
    static final long MOD = (1L << 61) - 1;

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<String> linhas = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "horn46.txt"), StandardCharsets.UTF_8)) if (!l.isEmpty()) linhas.add(l);
        String[] fs = linhas.get(0).trim().split(" ");
        int R = linhas.size() - 1;
        int[][] prem = new int[R][];
        int[] concl = new int[R];
        for (int r = 0; r < R; r++) {
            String[] xs = linhas.get(r + 1).trim().split(" ");
            prem[r] = new int[xs.length - 1];
            for (int k = 0; k < xs.length - 1; k++) prem[r][k] = Integer.parseInt(xs[k]);
            concl[r] = Integer.parseInt(xs[xs.length - 1]);
        }
        for (String f : fs) {
            int fato = Integer.parseInt(f);
            int[] falta = new int[R];
            Map<Integer, List<Integer>> vigia = new HashMap<>();
            for (int r = 0; r < R; r++) {
                List<Integer> distintas = new ArrayList<>();
                for (int a : prem[r]) if (!distintas.contains(a)) distintas.add(a);
                falta[r] = distintas.size();
                for (int a : distintas) vigia.computeIfAbsent(a, k -> new ArrayList<>()).add(r);
            }
            Map<Integer, Integer> prova = new HashMap<>();
            List<Integer> ordem = new ArrayList<>();
            ArrayDeque<Integer> fila = new ArrayDeque<>();
            prova.put(fato, -1);
            ordem.add(fato);
            fila.add(fato);
            long dec = 0;
            while (!fila.isEmpty()) {
                int a = fila.poll();
                for (int r : vigia.getOrDefault(a, Collections.emptyList())) {
                    falta[r]--;
                    dec++;
                    int c = concl[r];
                    if (falta[r] == 0 && !prova.containsKey(c)) {
                        prova.put(c, r);
                        ordem.add(c);
                        fila.add(c);
                    }
                }
            }
            long controle = 0;
            for (int k = 0; k < ordem.size(); k++) controle = (controle + (long) (k + 1) * ordem.get(k)) % MOD;
            StringBuilder cadeia = new StringBuilder();
            int a = ordem.get(ordem.size() - 1);
            boolean primeiro = true;
            while (prova.get(a) != -1) {
                int r = prova.get(a);
                if (!primeiro) cadeia.append(' ');
                cadeia.append(r);
                primeiro = false;
                a = prem[r][0];
            }
            out.println("fato " + fato + ": derivados " + ordem.size() + " controle " + controle + " decrementos " + dec + " prova " + cadeia);
        }
    }
}
