// Rodada 74 (Parte 107): a inducao reversa (iteracao de valor, horizonte 2), bit a bit. V[h][s]=max_a(r+V[h-1][T]). So +, max e
// comparacoes - nenhuma transcendental; a recursao entre ruas NAO cria fronteira (como o MPC da Parte 93).
public class Rodada74 {
    static final String[] ESTADOS = {"A", "B"};
    static double r(String s, int a) {
        if (s.equals("A")) return a == 0 ? 1.0 : 0.0;
        return a == 0 ? 0.0 : 3.0;
    }
    static String t(String s, int a) {
        if (s.equals("A")) return a == 0 ? "A" : "B";
        return a == 0 ? "A" : "B";
    }
    static java.util.Map<String,Double> passo(java.util.Map<String,Double> Va) {
        java.util.Map<String,Double> novo = new java.util.HashMap<>();
        for (String s : ESTADOS) {
            double melhor = r(s, 0) + Va.get(t(s, 0));
            for (int a = 1; a < 2; a++) {
                double cand = r(s, a) + Va.get(t(s, a));
                if (cand > melhor) melhor = cand;
            }
            novo.put(s, melhor);
        }
        return novo;
    }
    public static void main(String[] args) {
        java.util.Map<String,Double> V0 = new java.util.HashMap<>();
        for (String s : ESTADOS) V0.put(s, 0.0);
        java.util.Map<String,Double> V1 = passo(V0);
        java.util.Map<String,Double> V2 = passo(V1);
        StringBuilder sb = new StringBuilder();
        sb.append("V1 ").append(Double.toHexString(V1.get("A"))).append(" ").append(Double.toHexString(V1.get("B"))).append("\n");
        sb.append("V2 ").append(Double.toHexString(V2.get("A"))).append(" ").append(Double.toHexString(V2.get("B"))).append("\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
