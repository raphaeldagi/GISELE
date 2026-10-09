// Rodada 5 do diálogo Python <-> Java: a regra de aceitação com t pareado (synthai/rsi.py, _t_pareado), alimentada pelo
// mesmo gerador congruencial de 64 bits. O long de Java transborda módulo 2^64 sozinho; o >>> é o deslocamento sem
// sinal (o >> do Python num inteiro positivo). E a soma: o sum() do Python (3.12+) é compensado (Neumaier); para dar os
// mesmos bits, eu escrevo a mesma soma compensada. Uso: javac Rodada05.java && java Rodada05
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class Rodada05 {
    static long x = 2026L;
    static final long A = 6364136223846793005L, C = 1442695040888963407L;

    static double uniforme() {
        x = A * x + C;
        return (x >>> 11) * 0x1.0p-53;
    }

    static double normal() {
        double s = 0.0;
        for (int i = 0; i < 12; i++) s += uniforme();
        return s - 6.0;
    }

    // a soma de floats do Python 3.12+ (Objects/bltinmodule.c): Neumaier, começando do inteiro 0
    static double somaPython(double[] v) {
        double s = 0.0, c = 0.0;
        for (double y : v) {
            double t = s + y;
            if (Math.abs(s) >= Math.abs(y)) c += (s - t) + y;
            else c += (y - t) + s;
            s = t;
        }
        return s + c;
    }

    static double tPareado(double[] a, double[] b, boolean compensada) {
        int n = a.length;
        double[] d = new double[n];
        for (int i = 0; i < n; i++) d[i] = a[i] - b[i];
        double m;
        if (compensada) m = somaPython(d) / n;
        else { double s = 0.0; for (double y : d) s += y; m = s / n; }
        double[] q = new double[n];
        for (int i = 0; i < n; i++) q[i] = (d[i] - m) * (d[i] - m);
        double v;
        if (compensada) v = somaPython(q) / (n - 1);
        else { double s = 0.0; for (double y : q) s += y; v = s / (n - 1); }
        return v > 0 ? m / Math.sqrt(v / n) : (m > 0 ? Double.POSITIVE_INFINITY : 0.0);
    }

    public static void main(String[] args) throws Exception {
        StringBuilder aceites = new StringBuilder();
        double[] ts = new double[200];
        int mudam = 0, n1 = 0;
        for (int e = 0; e < 200; e++) {
            double efeito = (e % 5 - 2) * 10.0;
            double[] filho = new double[10], pai = new double[10];
            for (int i = 0; i < 10; i++) filho[i] = efeito + 50.0 * normal();
            for (int i = 0; i < 10; i++) pai[i] = 50.0 * normal();
            ts[e] = tPareado(filho, pai, true);
            if (ts[e] != tPareado(filho, pai, false)) mudam++;
            aceites.append(ts[e] > 3 ? '1' : '0');
            if (ts[e] > 3) n1++;
        }
        byte[] h = MessageDigest.getInstance("SHA-256").digest(aceites.toString().getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : h) sb.append(String.format("%02x", b));
        System.out.println("aceites = " + n1 + " de 200; sha = " + sb);
        StringBuilder l = new StringBuilder("t[0..4] =");
        for (int i = 0; i < 5; i++) l.append(' ').append(Double.toHexString(ts[i]));
        System.out.println(l);
        double mx = ts[0], mn = ts[0];
        for (double t : ts) { mx = Math.max(mx, t); mn = Math.min(mn, t); }
        System.out.println("maior t = " + Double.toHexString(mx) + "; menor t = " + Double.toHexString(mn));
        System.out.println("t que mudariam com a soma ingenua = " + mudam);
    }
}
