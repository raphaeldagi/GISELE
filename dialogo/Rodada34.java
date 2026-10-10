// Rodada 34 do diálogo Python <-> Java: o placar por voz, contado por uma função que lê dialogo/DIALOGO.md (rodadas 13 a 33).
// Regra estrita (vereditos com dono, mais os declarados das duas vozes) e generosa (mais os sem dono, dados às duas).
// Uso (da raiz do repositório): java Rodada34
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class Rodada34 {
    static final Pattern VEREDITO = Pattern.compile("\\(([a-z])\\)[ \\t\\n*:]*(✅|❌)");
    static final Pattern DONO = Pattern.compile("[ \\t\\n*(]*(?:a previsão da |a da )?(IA-Python|IA-Java)");
    static final Pattern CONJUNTA = Pattern.compile("\\(([a-z])\\),? (?:das duas vozes|para as duas)");
    static final Pattern CABECA = Pattern.compile("## Rodada ([0-9]+) ");
    static final String[] VOZES = {"IA-Python", "IA-Java"};

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        String texto = new String(Files.readAllBytes(Path.of("dialogo", "DIALOGO.md")), StandardCharsets.UTF_8);
        List<Integer> ns = new ArrayList<>();
        List<String> secs = new ArrayList<>();
        Integer atual = null;
        StringBuilder sb = new StringBuilder();
        boolean primeira = true;
        for (String l : texto.split("\n", -1)) {
            if (l.startsWith("## ")) {
                if (atual != null) { ns.add(atual); secs.add(sb.toString()); }
                Matcher m = CABECA.matcher(l);
                atual = null;
                if (m.lookingAt()) { int n = Integer.parseInt(m.group(1)); if (n >= 13 && n <= 33) atual = n; }
                sb = new StringBuilder();
                primeira = true;
            } else if (atual != null) {
                if (!primeira) sb.append('\n');
                sb.append(l);
                primeira = false;
            }
        }
        if (atual != null) { ns.add(atual); secs.add(sb.toString()); }
        long[][] tot = new long[2][4];
        for (int i = 0; i < ns.size(); i++) {
            String sec = secs.get(i);
            Set<String> conj = new HashSet<>();
            Matcher mc = CONJUNTA.matcher(sec);
            while (mc.find()) conj.add(mc.group(1));
            TreeMap<String, Boolean> dono = new TreeMap<>();  // chave "letra\0voz": a ordem de (letra, voz) do Python
            TreeMap<String, Boolean> juntas = new TreeMap<>(), sem = new TreeMap<>();
            Set<String> vistas = new HashSet<>();
            Matcher mv = VEREDITO.matcher(sec);
            Matcher md = DONO.matcher(sec);
            while (mv.find()) {
                String letra = mv.group(1);
                boolean ok = mv.group(2).equals("✅");
                md.region(mv.end(), sec.length());
                if (md.lookingAt()) dono.putIfAbsent(letra + "\0" + md.group(1), ok);
                else if (conj.contains(letra)) juntas.putIfAbsent(letra, ok);
                else if (!vistas.contains(letra)) sem.putIfAbsent(letra, ok);
                vistas.add(letra);
            }
            for (String k : new ArrayList<>(sem.keySet())) {
                boolean tem = juntas.containsKey(k);
                for (String c : dono.keySet()) if (c.startsWith(k + "\0")) tem = true;
                if (tem) sem.remove(k);
            }
            List<String> partes = new ArrayList<>();
            for (int v = 0; v < 2; v++) {
                int n = 0, a = 0;
                for (Map.Entry<String, Boolean> e : dono.entrySet())
                    if (e.getKey().endsWith("\0" + VOZES[v])) { n++; if (e.getValue()) a++; }
                for (boolean ok : juntas.values()) { n++; if (ok) a++; }
                int ne = sem.size(), ae = 0;
                for (boolean ok : sem.values()) if (ok) ae++;
                tot[v][0] += n; tot[v][1] += a; tot[v][2] += n + ne; tot[v][3] += a + ae;
                partes.add(VOZES[v] + " " + a + "/" + n);
            }
            out.println("rodada " + ns.get(i) + ": " + String.join("; ", partes) + "; conjuntas " + String.join("", juntas.keySet())
                        + "; sem dono " + String.join("", sem.keySet()));
        }
        for (int v = 0; v < 2; v++)
            out.println(VOZES[v] + ": estrita " + tot[v][1] + " em " + tot[v][0] + "; generosa " + tot[v][3] + " em " + tot[v][2]);
    }
}
