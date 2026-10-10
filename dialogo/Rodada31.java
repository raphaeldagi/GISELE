// Rodada 31 do diálogo Python <-> Java: o alfabeto do português. Os 4-gramas de PASTA/gramas31.txt reordenados com a chave de um
// dicionário português (sem acentos e minúscula, pela NFD sem as marcas; depois a original), contra a ordem dos códigos.
// Uso: java Rodada31 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.text.Normalizer;
import java.util.*;

public class Rodada31 {
    record G(String g, int nd, int nt) {}

    static String chavePt(String g) {
        return Normalizer.normalize(g, Normalizer.Form.NFD).replaceAll("\\p{M}", "").toLowerCase(Locale.ROOT);
    }

    // comparação por pontos de código, como o Python (não por unidades UTF-16)
    static int cmpCodigo(String a, String b) {
        int i = 0, j = 0;
        while (i < a.length() && j < b.length()) {
            int ca = a.codePointAt(i), cb = b.codePointAt(j);
            if (ca != cb) return Integer.compare(ca, cb);
            i += Character.charCount(ca);
            j += Character.charCount(cb);
        }
        return Integer.compare(a.length() - i, b.length() - j);
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<G> gs = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "gramas31.txt"), StandardCharsets.UTF_8)) {
            if (l.isEmpty()) continue;
            String[] c = l.split("\t");
            gs.add(new G(c[0], Integer.parseInt(c[1]), Integer.parseInt(c[2])));
        }
        Comparator<G> base = Comparator.comparingInt((G x) -> -x.nd()).thenComparingInt(x -> -x.nt());
        List<G> uni = new ArrayList<>(gs);
        uni.sort(base.thenComparing((x, y) -> cmpCodigo(x.g(), y.g())));
        List<G> pt = new ArrayList<>(gs);
        pt.sort(base.thenComparing((x, y) -> cmpCodigo(chavePt(x.g()), chavePt(y.g()))).thenComparing((x, y) -> cmpCodigo(x.g(), y.g())));
        Map<String, Integer> pos = new HashMap<>();
        for (int i = 0; i < pt.size(); i++) pos.put(pt.get(i).g(), i);
        for (G x : pt) out.println(x.g() + " | " + x.nd() + " | " + x.nt());
        List<String> trocas = new ArrayList<>();
        for (int i = 0; i < uni.size(); i++)
            for (int j = i + 1; j < uni.size(); j++)
                if (pos.get(uni.get(i).g()) > pos.get(uni.get(j).g())) trocas.add("  " + uni.get(i).g() + " <-> " + uni.get(j).g());
        out.println("pares que mudam de ordem: " + trocas.size());
        for (String t : trocas) out.println(t);
    }
}
