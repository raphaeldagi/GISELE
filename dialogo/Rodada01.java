// Rodada 1 do diálogo Python <-> Java: a IA-Java traduz o módulo hexadecimal da SYNTHAI (synthai/hexadecimal.py).
// Compilar e rodar: javac Rodada01.java && java Rodada01
// A saída tem de ser IDÊNTICA à de rodada01.py (o teste é a comparação das duas, caractere por caractere).

import java.util.Arrays;
import java.util.Locale;

public class Rodada01 {

    // Python: v[j], v[j + h] = a + b, a - b  (borboletas da transformada de Walsh-Hadamard)
    static double[] walshHadamard(double[] valores) {
        double[] v = Arrays.copyOf(valores, valores.length);
        int n = v.length;
        if (Integer.bitCount(n) != 1) throw new IllegalArgumentException("o tamanho tem de ser uma potência de 2");
        for (int h = 1; h < n; h *= 2)
            for (int i = 0; i < n; i += 2 * h)
                for (int j = i; j < i + h; j++) {
                    double a = v[j], b = v[j + h];
                    v[j] = a + b;
                    v[j + h] = a - b;
                }
        return v;
    }

    // Python: [t[0] / n] + [(-1) ** bin(j).count("1") * t[j] / (n / 2) for j in range(1, n)]
    static double[] efeitosFatoriais(double[] valores) {
        double[] t = walshHadamard(valores);
        int n = valores.length;
        double[] e = new double[n];
        e[0] = t[0] / n;
        for (int j = 1; j < n; j++) e[j] = (Integer.bitCount(j) % 2 == 0 ? 1 : -1) * t[j] / (n / 2.0);
        return e;
    }

    static int gray(int n) { return n ^ (n >> 1); }                     // igual em Python e em Java
    static int hamming(int a, int b) { return Integer.bitCount(a ^ b); } // Python: bin(a ^ b).count("1")

    static String lista(double[] v) {
        StringBuilder s = new StringBuilder("[");
        for (int i = 0; i < v.length; i++) s.append(i == 0 ? "" : ", ").append(Double.toHexString(v[i]));
        return s.append("]").toString();
    }

    public static void main(String[] args) {
        Locale.setDefault(Locale.ROOT);
        System.out.println("P* = " + Double.toHexString(0.1 / (0.9 * 50)));
        System.out.println("WH [1,2,3,4] = " + lista(walshHadamard(new double[]{1, 2, 3, 4})));
        System.out.println("efeitos [10,12,20,30] = " + lista(efeitosFatoriais(new double[]{10, 12, 20, 30})));
        double[] y = new double[8];
        for (int i = 0; i < 8; i++) y[i] = Math.sqrt(i + 1) / 3.0;
        System.out.println("efeitos sqrt = " + lista(efeitosFatoriais(y)));
        StringBuilder g = new StringBuilder();
        for (int i = 0; i < 16; i++) g.append(Integer.toHexString(gray(i)).toUpperCase());
        System.out.println("gray = " + g);
        System.out.println("hamming(0x3, 0xC) = " + hamming(0x3, 0xC) + "; hamming(0xB, 0x4) = " + hamming(0xB, 0x4));
    }
}
