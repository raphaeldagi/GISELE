// Rodada 12 do diálogo Python <-> Java: a IA-Java faz a engenharia reversa dos textos da IA-Python. Os mesmos 4-gramas
// mais repetidos nas Partes 31-40 e as mesmas estatísticas das duas vozes do diálogo. Duas armadilhas de tradução: o \s
// do Python (em str) casa qualquer espaço Unicode, o do Java só os ASCII, a menos que se ligue UNICODE_CHARACTER_CLASS;
// o lower() do Python é o toLowerCase(Locale.ROOT) do Java (sem regras de idioma); e a saída tem de ser UTF-8. Uso, da raiz: java Rodada12
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Rodada12 {
    static final Pattern PALAVRA = Pattern.compile("[a-záàâãéêíóôõúüç]+");

    static List<String> palavras(String t) {
        List<String> r = new ArrayList<>();
        Matcher m = PALAVRA.matcher(t.toLowerCase(Locale.ROOT));
        while (m.find()) r.add(m.group());
        return r;
    }

    public static void main(String[] args) throws Exception {
        // a saída padrão do Java codifica com a localidade do sistema (aqui, ASCII: 'é' sai como '?'); o Python escreve UTF-8
        System.setOut(new java.io.PrintStream(new java.io.FileOutputStream(java.io.FileDescriptor.out), true, StandardCharsets.UTF_8));
        Path raiz = Path.of(".");
        List<String> nomes;
        try (Stream<Path> s = Files.list(raiz)) {
            nomes = s.map(p -> p.getFileName().toString()).sorted().collect(Collectors.toList());
        }
        Map<List<String>, Integer> emDocs = new HashMap<>(), total = new HashMap<>();
        for (int n = 31; n <= 40; n++) {
            String pref = "ASI_AGI_parte" + n + "_";
            String nome = nomes.stream().filter(x -> x.startsWith(pref)).findFirst().orElseThrow();
            List<String> ps = palavras(Files.readString(raiz.resolve(nome), StandardCharsets.UTF_8));
            Set<List<String>> vistos = new HashSet<>();
            for (int i = 0; i + 4 <= ps.size(); i++) {
                List<String> g = List.copyOf(ps.subList(i, i + 4));
                total.merge(g, 1, Integer::sum);
                vistos.add(g);
            }
            for (List<String> g : vistos) emDocs.merge(g, 1, Integer::sum);
        }
        Comparator<List<String>> lex = (a, b) -> {
            for (int i = 0; i < 4; i++) { int c = a.get(i).compareTo(b.get(i)); if (c != 0) return c; }
            return 0;
        };
        List<List<String>> ordem = new ArrayList<>(emDocs.keySet());
        ordem.sort(Comparator.<List<String>>comparingInt(g -> -emDocs.get(g)).thenComparingInt(g -> -total.get(g)).thenComparing(lex));
        for (List<String> g : ordem.subList(0, 12))
            System.out.println(String.join(" ", g) + " | " + emDocs.get(g) + " | " + total.get(g));

        String dialogo = Files.readString(raiz.resolve("dialogo/DIALOGO.md"), StandardCharsets.UTF_8);
        Pattern fala = Pattern.compile("\\*\\*(IA-Python|IA-Java)[^*]*\\*\\*:?\\s*(.*)", Pattern.DOTALL | Pattern.UNICODE_CHARACTER_CLASS);
        Map<String, int[]> voz = new LinkedHashMap<>();
        voz.put("IA-Python", new int[2]);
        voz.put("IA-Java", new int[2]);
        for (String par : Pattern.compile("\\n\\s*\\n", Pattern.UNICODE_CHARACTER_CLASS).split(dialogo)) {
            Matcher m = fala.matcher(par.strip());
            if (m.lookingAt()) {
                int[] v = voz.get(m.group(1));
                v[0]++;
                v[1] += palavras(m.group(2)).size();
            }
        }
        for (Map.Entry<String, int[]> e : voz.entrySet())
            System.out.println(e.getKey() + ": " + e.getValue()[0] + " falas, " + e.getValue()[1] + " palavras, "
                    + Double.toHexString((double) e.getValue()[1] / e.getValue()[0]) + " por fala");
    }
}
