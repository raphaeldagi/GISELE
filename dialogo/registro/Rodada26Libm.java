// Rodada 26 do diálogo Python <-> Java: o método ou a série? As duas exponenciais ajustadas EM LOG por Gauss-Newton a partir
// do melhor ponto da grade da Rodada 25 (eliminação de Gauss com pivô parcial; passo dividido por 2 até 30 vezes). Lê
// secoes26.txt. Uso: java Rodada26 PASTA
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Rodada26Libm {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        List<Integer> partes = new ArrayList<>();
        List<String[]> ws = new ArrayList<>();
        for (String l : Files.readAllLines(Path.of(args[0], "secoes26.txt"), StandardCharsets.US_ASCII)) {
            String[] p = l.split("\t", -1);
            partes.add(Integer.parseInt(p[0]));
            ws.add(p[1].isEmpty() ? new String[0] : p[1].split(" "));
        }
        int K = partes.size();
        HashMap<String, Integer> df = new HashMap<>();
        for (String[] a : ws) for (String w : a) df.merge(w, 1, Integer::sum);
        HashMap<String, Double> idf2 = new HashMap<>();
        for (Map.Entry<String, Integer> e : df.entrySet()) {
            double x = Math.log((double) K / e.getValue());
            idf2.put(e.getKey(), x * x);
        }
        double[] norma = new double[K];
        for (int i = 0; i < K; i++) { double t = 0.0; for (String w : ws.get(i)) t += idf2.get(w); norma[i] = t; }
        double[][] sim = new double[K][K];
        for (int i = 0; i < K; i++) {
            HashSet<String> a = new HashSet<>(Arrays.asList(ws.get(i)));
            for (int j = 0; j < K; j++) {
                double t = 0.0;
                for (String w : ws.get(j)) if (a.contains(w)) t += idf2.get(w);
                sim[i][j] = (norma[i] > 0 && norma[j] > 0) ? t / Math.sqrt(norma[i] * norma[j]) : 0.0;
            }
        }
        int n = 20;
        double[] ys = new double[n], ly = new double[n], xe = new double[n], xp = new double[n];
        for (int L = 1; L <= n; L++) { ys[L - 1] = media(sim, L); ly[L - 1] = Math.log(ys[L - 1]); xe[L - 1] = (double) L; xp[L - 1] = Math.log(L); }
        double se = reta(xe, ly)[2], sp = reta(xp, ly)[2];
        double ms = 0, mA = 0, mB = 0, m1 = 0, m2 = 0;
        boolean tem = false;
        for (int i = 1; i <= 20; i++) {
            double t1 = 0.25 * i;
            double[] u = new double[n];
            for (int L = 1; L <= n; L++) u[L - 1] = Math.exp(-L / t1);
            for (int jj = 1; jj <= 100; jj++) {
                double t2 = 2.0 * jj;
                if (t1 >= t2) continue;
                double[] v = new double[n];
                for (int L = 1; L <= n; L++) v[L - 1] = Math.exp(-L / t2);
                double suu = 0, svv = 0, suv = 0, suy = 0, svy = 0;
                for (int q = 0; q < n; q++) {
                    suu += u[q] * u[q]; svv += v[q] * v[q]; suv += u[q] * v[q]; suy += u[q] * ys[q]; svy += v[q] * ys[q];
                }
                double det = suu * svv - suv * suv;
                if (det == 0.0) continue;
                double A = (suy * svv - svy * suv) / det, B = (svy * suu - suy * suv) / det;
                if (A <= 0.0 || B <= 0.0) continue;
                double sse = 0.0;
                for (int q = 0; q < n; q++) { double e = Math.log(ys[q]) - Math.log(A * u[q] + B * v[q]); sse += e * e; }
                if (!tem || sse < ms) { tem = true; ms = sse; mA = A; mB = B; m1 = t1; m2 = t2; }
            }
        }
        double[] th = {Math.log(mA), Math.log(mB), m1, m2};
        double ini = erro(th, ly);
        double sse = ini;
        for (int it = 0; it < 100; it++) {
            double[][] JtJ = new double[4][4];
            double[] Jtr = new double[4];
            for (int L = 1; L <= n; L++) {
                double[] abm = modelo(th, L);
                double S = abm[0] + abm[1];
                double[] jj = {abm[0] / S, abm[1] / S, abm[0] * (L / (th[2] * th[2])) / S, abm[1] * (L / (th[3] * th[3])) / S};
                double r = ly[L - 1] - abm[2];
                for (int i = 0; i < 4; i++) { Jtr[i] += jj[i] * r; for (int k = 0; k < 4; k++) JtJ[i][k] += jj[i] * jj[k]; }
            }
            double[] d = resolver(JtJ, Jtr);
            double passo = 1.0;
            boolean melhorou = false;
            for (int t = 0; t < 30; t++) {
                double[] novo = new double[4];
                for (int i = 0; i < 4; i++) novo[i] = th[i] + passo * d[i];
                if (novo[2] > 0.0 && novo[3] > 0.0) {
                    double s2 = erro(novo, ly);
                    if (s2 < sse) { th = novo; sse = s2; melhorou = true; break; }
                }
                passo /= 2.0;
            }
            if (!melhorou) break;
        }
        out.println("inicio: sse = " + Double.toHexString(ini));
        out.println("em log: A = " + Double.toHexString(Math.exp(th[0])) + "; B = " + Double.toHexString(Math.exp(th[1])) + "; t1 = "
                + Double.toHexString(th[2]) + "; t2 = " + Double.toHexString(th[3]) + "; sse = " + Double.toHexString(sse));
        out.println("aic = " + Double.toHexString(aic(sse, n, 4)) + "; limiar para vencer a potencia = " + Double.toHexString(0.3095 * Math.exp(-0.2)));
    }

    static double[] modelo(double[] th, int L) {
        double a = Math.exp(th[0]) * Math.exp(-L / th[2]);
        double b = Math.exp(th[1]) * Math.exp(-L / th[3]);
        return new double[]{a, b, Math.log(a + b)};
    }

    static double erro(double[] th, double[] ly) {
        double s = 0.0;
        for (int L = 1; L <= ly.length; L++) { double e = ly[L - 1] - modelo(th, L)[2]; s += e * e; }
        return s;
    }

    static double[] resolver(double[][] M, double[] v) {
        int n = v.length;
        double[][] A = new double[n][n + 1];
        for (int i = 0; i < n; i++) { for (int k = 0; k < n; k++) A[i][k] = M[i][k]; A[i][n] = v[i]; }
        for (int c = 0; c < n; c++) {
            int piv = c;
            for (int r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[piv][c])) piv = r;
            double[] tmp = A[c]; A[c] = A[piv]; A[piv] = tmp;
            for (int r = c + 1; r < n; r++) {
                double f = A[r][c] / A[c][c];
                for (int k = c; k <= n; k++) A[r][k] -= f * A[c][k];
            }
        }
        double[] x = new double[n];
        for (int i = n - 1; i >= 0; i--) {
            double s = A[i][n];
            for (int k = i + 1; k < n; k++) s -= A[i][k] * x[k];
            x[i] = s / A[i][i];
        }
        return x;
    }

    static double aic(double sse, int n, int k) { return n * Math.log(sse / n) + 2 * k; }

    static double[] reta(double[] xs, double[] ys) {
        int n = xs.length;
        double sx = 0.0, sy = 0.0;
        for (int i = 0; i < n; i++) { sx += xs[i]; sy += ys[i]; }
        double mx = sx / n, my = sy / n, sxy = 0.0, sxx = 0.0;
        for (int i = 0; i < n; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) * (xs[i] - mx); }
        double m = sxy / sxx, c = my - m * mx, sse = 0.0;
        for (int i = 0; i < n; i++) { double r = ys[i] - (c + m * xs[i]); sse += r * r; }
        return new double[]{c, m, sse};
    }

    static double media(double[][] sim, int L) {
        double t = 0.0;
        int n = 0;
        for (int i = 0; i + L < sim.length; i++) { t += sim[i][i + L]; n++; }
        return t / n;
    }
}
