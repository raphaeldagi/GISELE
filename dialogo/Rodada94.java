// Rodada 94 (Parte 143): o retrocesso e a memoria congelada de synthai.memoria_congelada bit a bit. Tarefas quadraticas d = 6 de um LCG,
// sem ruido e sem conflito; 8 de treino alimentam a memoria, que e congelada; 8 de teste rodam com o fator; passo 0,2, orcamento 24.
public class Rodada94 {
    static final int D = 6;
    static long x = 15194;
    static int[][] cont = new int[3][2]; // baixo, medio, alto: (n, r)

    static double u() {
        x = (1103515245L * x + 12345L) % 2147483648L;
        return 2.0 * (x / 2147483648.0) - 1.0;
    }

    static double[][] A; static double[] alvo, x0;

    static void tarefa() {
        double[][] M = new double[D][D];
        for (int a = 0; a < D; a++) for (int b = 0; b < D; b++) M[a][b] = u();
        A = new double[D][D];
        for (int a = 0; a < D; a++) for (int b = 0; b < D; b++) {
            double t = 0.0;
            for (int k = 0; k < D; k++) t += M[k][a] * M[k][b];
            A[a][b] = (a == b ? 0.5 : 0.0) + t / (2.0 * D);
        }
        alvo = new double[D]; x0 = new double[D];
        for (int i = 0; i < D; i++) alvo[i] = u();
        for (int i = 0; i < D; i++) x0[i] = u();
    }

    static double custo(double[][] A, double[] v, double[] al) {
        double[] d = new double[D];
        for (int i = 0; i < D; i++) d[i] = v[i] - al[i];
        double t = 0.0;
        for (int i = 0; i < D; i++) { double s = 0.0; for (int j = 0; j < D; j++) s += A[i][j] * d[j]; t += d[i] * s; }
        return t;
    }

    static double[] grad(double[][] A, double[] v, double[] al) {
        double[] d = new double[D];
        for (int i = 0; i < D; i++) d[i] = v[i] - al[i];
        double[] g = new double[D];
        for (int i = 0; i < D; i++) { double s = 0.0; for (int j = 0; j < D; j++) s += A[i][j] * d[j]; g[i] = 2.0 * s; }
        return g;
    }

    static int contexto(double[] g, double f) {
        double s = 0.0;
        for (double v : g) s += v * v;
        double razao = Math.sqrt(s) / Math.sqrt(Math.max(f, 1e-12));
        return razao < 3 ? 0 : (razao < 6 ? 1 : 2);
    }

    static double fator(int c) {
        int n = cont[c][0], r = cont[c][1];
        return n >= 8 ? 1 - 0.6 * (r + 1) / (n + 2) : 1.0;
    }

    static double executar(double passo, boolean comFator, boolean coletar) {
        double[] v = x0.clone();
        double f = custo(A, v, alvo), f0 = f;
        for (int t = 1; t <= 24; t++) {
            double[] g = grad(A, v, alvo);
            int ctx = contexto(g, f);
            if (t == 1 && comFator) passo *= fator(ctx);
            double[] cand = new double[D];
            for (int i = 0; i < D; i++) cand[i] = v[i] - passo * g[i];
            double fc = custo(A, cand, alvo);
            double s = 0.0;
            for (int i = 0; i < D; i++) s += (cand[i] - v[i]) * (cand[i] - v[i]);
            double desloc = Math.sqrt(s);
            int motivo = desloc > 1.0 ? 2 : (fc > f + 1e-12 ? 1 : 0); // 0 aceita, 1 custo, 2 deslocamento
            double ganho = 0.0;
            if (motivo == 0) { ganho = f - fc; v = cand; f = fc; }
            if (coletar) { cont[ctx][0] += 1; cont[ctx][1] += motivo != 0 ? 1 : 0; }
            if (motivo != 0) passo = Math.max(0.002, passo * 0.5);
            else if (ganho > 1e-3 * Math.max(f + ganho, 1e-12)) passo = Math.min(0.4, passo * 1.06);
        }
        return f / Math.max(f0, 1e-12);
    }

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 8; i++) { tarefa(); executar(0.2, false, true); }
        String[] nomes = {"baixo", "medio", "alto"};
        for (int c = 0; c < 3; c++) sb.append(nomes[c]).append(" ").append(cont[c][0]).append(" ").append(cont[c][1]).append(" ").append(Double.toHexString(fator(c))).append("\n");
        for (int i = 0; i < 8; i++) { tarefa(); sb.append("razao ").append(Double.toHexString(executar(0.2, true, false))).append("\n"); }
        sb.append("fim");
        System.out.println(sb.toString());
    }
}
