// Rodada 35 do diálogo Python <-> Java: o dobro que falta nos narcisistas (bases 3 a 16, k de 2 a 7), medido contra a conta da
// Parte 60 com o fator de congruência; células com e sem interruptor. Uso (da raiz do repositório): java Rodada35
import java.io.PrintStream;
import java.util.*;

public class Rodada35 {
    static final int[] NOVAS = {3, 4, 5, 7, 9, 11, 13, 14, 15};

    static long fat(int n) { long r = 1; for (int i = 2; i <= n; i++) r *= i; return r; }
    static long pw(long a, int e) { long r = 1; for (int i = 0; i < e; i++) r *= a; return r; }

    static long medido, num;

    static void percorre(int b, int k, int[] ds, int pos, int min, long[] pot) {
        if (pos == k) {
            long s = 0;
            for (int d : ds) s += pot[d];
            if (s < pw(b, k - 1) || s >= pw(b, k)) return;
            long m = fat(k);
            int[] cont = new int[b];
            for (int d : ds) cont[d]++;
            for (int d = 0; d < b; d++) m /= fat(cont[d]);
            int z = cont[0];
            num += m * (k - z) / k;
            int[] dig = new int[b];
            long x = s;
            while (x > 0) { dig[(int) (x % b)]++; x /= b; }
            if (Arrays.equals(dig, cont)) medido++;
            return;
        }
        for (int d = min; d < b; d++) { ds[pos] = d; percorre(b, k, ds, pos + 1, d, pot); }
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<long[]> cel = new ArrayList<>();      // b, k, medido, inter
        List<Double> contas = new ArrayList<>();
        for (int b = 3; b <= 16; b++) for (int k = 2; k <= 7; k++) {
            long[] pot = new long[b];
            for (int d = 0; d < b; d++) pot[d] = pw(d, k);
            medido = 0; num = 0;
            percorre(b, k, new int[k], 0, 0, pot);
            long den = (long) (b - 1) * pw(b, k - 1);
            int g = 1;
            for (int c = 1; c < b; c++) {
                if ((b - 1) % c != 0) continue;
                boolean ok = true;
                for (int d = 0; d < b; d++) if ((pw(d, k) - d) % c != 0) { ok = false; break; }
                if (ok) g = c;
            }
            boolean inter = false;
            for (int d = 2; d < b; d++) for (int p = 0; p < k; p++) if (pw(d, k - 1) == pw(b, p)) inter = true;
            double e = ((double) num / (double) den) * g;
            cel.add(new long[]{b, k, medido, inter ? 1 : 0});
            contas.add(e);
            out.println("b=" + b + " k=" + k + " medido=" + medido + " num=" + num + " den=" + den + " g=" + g + " interruptor=" + (inter ? 1 : 0)
                        + " conta=" + Double.toHexString(e));
        }
        String[] nomes = {"sem interruptor, impares", "sem interruptor, pares", "sem interruptor, bases novas", "sem interruptor", "com interruptor"};
        long[] ms = new long[5];
        double[] es = new double[5];
        for (int i = 0; i < cel.size(); i++) {
            long[] c = cel.get(i);
            int b = (int) c[0];
            boolean inter = c[3] == 1, nova = false;
            for (int n : NOVAS) if (n == b) nova = true;
            boolean[] f = {!inter && b % 2 == 1, !inter && b % 2 == 0, !inter && nova, !inter, inter};
            for (int j = 0; j < 5; j++) if (f[j]) { ms[j] += c[2]; es[j] += contas.get(i); }
        }
        for (int j = 0; j < 5; j++)
            out.println(nomes[j] + ": medido=" + ms[j] + " conta=" + Double.toHexString(es[j]) + " razao=" + Double.toHexString(ms[j] / es[j]));
        out.println("razao com/sem interruptor = " + Double.toHexString((ms[4] / es[4]) / (ms[3] / es[3])));
    }
}
