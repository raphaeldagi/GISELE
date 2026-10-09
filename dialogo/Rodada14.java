// Rodada 14 do diálogo Python <-> Java: os trigramas de letras que carregam significado (animal ou não), a partir de
// PASTA/formas14.txt. Cada lema conta cada trigrama UMA vez (o frozenset do Python); a lista "menos animais" é a ordem
// crescente invertida da lista ordenada, como o ok[::-1] do Python (o que inverte também a ordem dos empates).
// Uso: java Rodada14 PASTA
import java.io.PrintStream;
import java.io.FileOutputStream;
import java.io.FileDescriptor;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada14 {
    static Set<String> trigramas(String lema) {
        String x = "^" + lema.toLowerCase(Locale.ROOT) + "$";
        Set<String> r = new HashSet<>();
        for (int i = 0; i + 3 <= x.length(); i++) r.add(x.substring(i, i + 3));
        return r;
    }

    public static void main(String[] args) throws Exception {
        System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out), true, StandardCharsets.UTF_8));
        Map<String, Integer> ca = new HashMap<>(), co = new HashMap<>();
        for (String l : Files.readAllLines(Path.of(args[0], "formas14.txt"), StandardCharsets.UTF_8)) {
            int tab = l.indexOf('\t');
            Map<String, Integer> alvo = l.substring(0, tab).equals("1") ? ca : co;
            for (String t : trigramas(l.substring(tab + 1))) alvo.merge(t, 1, Integer::sum);
        }
        Set<String> voc = new HashSet<>(ca.keySet());
        voc.addAll(co.keySet());
        long na = 0, no = 0;
        for (int c : ca.values()) na += c;
        for (int c : co.values()) no += c;
        int v = voc.size();
        Map<String, Double> peso = new HashMap<>();
        for (String t : voc)
            peso.put(t, Math.log((ca.getOrDefault(t, 0) + 1) / (double) (na + v)) - Math.log((co.getOrDefault(t, 0) + 1) / (double) (no + v)));
        List<String> ok = new ArrayList<>();
        for (String t : voc) if (ca.getOrDefault(t, 0) + co.getOrDefault(t, 0) >= 10) ok.add(t);
        ok.sort((p, q) -> { int c = Double.compare(-peso.get(p), -peso.get(q)); return c != 0 ? c : p.compareTo(q); });
        List<String> inv = new ArrayList<>(ok);
        Collections.reverse(inv);
        System.out.println("trigramas distintos = " + v + "; dae = " + Double.toHexString(peso.get("dae")) + "; ae$ = " + Double.toHexString(peso.get("ae$")));
        System.out.println("mais animais: " + String.join(" ", ok.subList(0, 12)));
        System.out.println("menos animais: " + String.join(" ", inv.subList(0, 12)));
    }
}
