// Rodada 38 do diálogo Python <-> Java: o fator do dígito final nos primos palíndromos (bases 5 a 16, até b^5): crivo, conta A
// (2/ln n nos ímpares) e conta B (Π p/(p − 1) dos primos de 2b nos coprimos), com o log próprio da rodada 26.
// Uso (da raiz do repositório): java Rodada38
import java.io.PrintStream;
import java.util.*;

public class Rodada38 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10, SQRT2 = Math.sqrt(2.0);

    static double log_(double x) {
        int e = Math.getExponent(x);
        double m = Math.scalb(x, -e);
        if (m > SQRT2) { m = m / 2.0; e = e + 1; }
        double s = (m - 1.0) / (m + 1.0), s2 = s * s, p = 1.0 / 41.0;
        for (int jj = 19; jj >= 0; jj--) p = 1.0 / (2 * jj + 1) + s2 * p;
        return e * LN2_HI + (e * LN2_LO + 2.0 * s * p);
    }

    static List<Integer> primosDe(int m) {
        List<Integer> ps = new ArrayList<>();
        for (int p = 2; (long) p * p <= m; p++) if (m % p == 0) { ps.add(p); while (m % p == 0) m /= p; }
        if (m > 1) ps.add(m);
        return ps;
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        int N = 1 << 20;
        boolean[] composto = new boolean[N];
        composto[0] = composto[1] = true;
        for (int i = 2; (long) i * i < N; i++) if (!composto[i]) for (int j = i * i; j < N; j += i) composto[j] = true;
        long tm = 0, perto = 0;
        double tb = 0.0, absrel = 0.0;
        for (int b = 5; b <= 16; b++) {
            int ate = b * b * b * b * b;
            List<Integer> ps = primosDe(2 * b);
            double f = 1.0;
            for (int p : ps) f = f * p / (p - 1);
            long medido = 0, exatos = 0;
            double A = 0.0, B = 0.0, var = 0.0;
            int[] ds = new int[8];
            for (int n = 1; n < ate; n++) {
                int L = 0, x = n;
                while (x > 0) { ds[L++] = x % b; x /= b; }
                boolean pal = true;
                for (int i = 0; i < L / 2; i++) if (ds[i] != ds[L - 1 - i]) { pal = false; break; }
                if (!pal) continue;
                int primo = composto[n] ? 0 : 1;
                medido += primo;
                if (L == 1 || L % 2 == 0) { exatos += primo; continue; }
                double ln = log_((double) n);
                if (n % 2 == 1) A += 2.0 / ln;
                boolean cop = true;
                for (int p : ps) if (n % p == 0) cop = false;
                if (cop) { double q = f / ln; B += q; var += q * (1.0 - q); }
            }
            double a = A + exatos, bb = B + exatos, s = Math.sqrt(var);
            if (Math.abs(medido - bb) < 2.0 * s) perto++;
            absrel += Math.abs(medido - bb) / bb;
            tm += medido; tb += bb;
            out.println("b=" + b + " medido=" + medido + " contaA=" + Double.toHexString(a) + " contaB=" + Double.toHexString(bb) + " sigma=" + Double.toHexString(s));
        }
        out.println("bases a menos de 2 sigma=" + perto + "; media |medido-B|/B=" + Double.toHexString(absrel / 12) + "; soma medido-B=" + Double.toHexString(tm - tb));
    }
}
