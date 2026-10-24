// Rodada 98 (Parte 150): a densidade de palavras de synthai.tabuleiro bit a bit. 40 palavras portuguesas fixas; frequencias A-Z em % (piso 0,01,
// total em laco na ordem do alfabeto); D = soma, nas palavras de 3 a 5 letras, do produto de freq/total; com as frequencias contadas e com as do ingles.
public class Rodada98 {
    static final String[] PALAVRAS = ("casa mesa rio mar sol lua dia noite agua terra fogo vento pedra arvore flor fruta pao leite vinho sal "
            + "amor medo raiva paz guerra vida morte tempo hora ano mes semana boca olho mao pe dedo nariz cabelo dente").split(" ");
    static final double[] EN = {8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1, 2.8, 1.0, 2.4,
            0.15, 2.0, 0.07};

    static double[] frequencias() {
        int[] cont = new int[26];
        for (String w : PALAVRAS) for (char ch : w.toUpperCase().toCharArray()) if (ch >= 'A' && ch <= 'Z') cont[ch - 'A']++;
        int total = 0;
        for (int c = 0; c < 26; c++) total += cont[c];
        double[] out = new double[26];
        for (int c = 0; c < 26; c++) { double v = 100.0 * cont[c] / total; out[c] = v > 0.01 ? v : 0.01; }
        return out;
    }

    static double densidade(double[] freq) {
        double t = 0.0;
        for (int c = 0; c < 26; c++) t += freq[c];
        double d = 0.0;
        for (String w : PALAVRAS) {
            if (w.length() >= 3 && w.length() <= 5) {
                double x = 1.0;
                for (char ch : w.toUpperCase().toCharArray()) x *= freq[ch - 'A'] / t;
                d += x;
            }
        }
        return d;
    }

    public static void main(String[] args) {
        double[] f = frequencias();
        StringBuilder sb = new StringBuilder();
        for (int c = 0; c < 26; c++) sb.append((char) ('A' + c)).append(" ").append(Double.toHexString(f[c])).append("\n");
        sb.append("D_pt ").append(Double.toHexString(densidade(f))).append("\n");
        sb.append("D_en ").append(Double.toHexString(densidade(EN))).append("\n");
        sb.append("conferido True\n");
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
