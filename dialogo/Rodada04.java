// Rodada 4 do diálogo Python <-> Java: a IA-Java audita a arquitetura "pós-ASI" só como TEXTO (sem árvore sintática) e
// calcula, de fora do Python, o selo do avaliador: o SHA-256 do código de regret_do_genoma em synthai/rsi.py, recortado
// do arquivo do mesmo jeito que o inspect.getsource do Python recorta. Uso, da raiz: java Rodada04.java (ou javac + java)
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

public class Rodada04 {
    // as linhas de um bloco que começa numa linha "def nome" (ou "class nome") até a próxima linha com indentação menor
    // ou igual, sem as linhas vazias do fim (é o que o inspect.getsource devolve)
    static List<String> bloco(List<String> linhas, String inicio) {
        int i = 0;
        while (!linhas.get(i).trim().startsWith(inicio)) i++;
        int recuo = linhas.get(i).length() - linhas.get(i).stripLeading().length();
        List<String> b = new ArrayList<>(List.of(linhas.get(i)));
        for (int j = i + 1; j < linhas.size(); j++) {
            String l = linhas.get(j);
            if (!l.isBlank() && l.length() - l.stripLeading().length() <= recuo) break;
            b.add(l);
        }
        while (b.get(b.size() - 1).isBlank()) b.remove(b.size() - 1);
        return b;
    }

    public static void main(String[] args) throws Exception {
        Path raiz = Path.of(args.length > 0 && Files.exists(Path.of(args[0], "externos")) ? args[0] : ".");
        if (!Files.exists(raiz.resolve("externos"))) raiz = Path.of("..");
        List<String> arq = Files.readAllLines(raiz.resolve("externos/arquitetura_pos_asi.py"), StandardCharsets.UTF_8);

        List<String> visita = bloco(arq, "def visit_BinOp");
        boolean devolve = visita.get(visita.size() - 1).trim().equals("return node");
        System.out.println("transformador devolve o no: " + (devolve ? "True" : "False"));
        // um transformador cuja única visita devolve o próprio nó, depois de visitar os filhos, é a identidade
        System.out.println("nos mudados: " + (devolve ? 0 : -1));

        List<String> laco = bloco(arq, "def main_evolution_loop");
        Matcher m = Pattern.compile("inspect\\.getsource\\(([^)]*)\\)").matcher(String.join("\n", laco));
        List<String> mutados = new ArrayList<>();
        while (m.find()) mutados.add(m.group());
        System.out.println("texto mutado: " + String.join(", ", mutados));

        List<String> rb = bloco(arq, "def run_benchmarks");
        String ret = rb.stream().filter(l -> l.trim().startsWith("return ")).findFirst().orElseThrow().trim().substring(7);
        System.out.println("run_benchmarks constante: " + Double.toHexString(Double.parseDouble(ret)));

        List<String> ev = bloco(arq, "class EnvironmentEvaluator");
        boolean pergunta = ev.stream().anyMatch(l -> l.contains("agent_instance.run_benchmarks()"));
        System.out.println("avaliador pergunta ao agente: " + (pergunta ? "True" : "False"));

        List<String> rsi = Files.readAllLines(raiz.resolve("synthai/rsi.py"), StandardCharsets.UTF_8);
        String fonte = String.join("\n", bloco(rsi, "def regret_do_genoma")) + "\n";
        byte[] h = MessageDigest.getInstance("SHA-256").digest(fonte.getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : h) sb.append(String.format("%02x", b));
        System.out.println("selo do avaliador: " + sb);
    }
}
