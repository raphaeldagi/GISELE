// Rodada 50 (Parte 83), PAPÉIS INVERTIDOS: a IA-Java pergunta ("o treino adversário síncrono, o alternado e o assíncrono dão a mesma trajetória nas duas
// linguagens, bit a bit?") e a IA-Python responde com dialogo/rodada50.py. O GAN de Dirac: f'(t) = 1/(1 + e^t), com o exp PRÓPRIO (o mesmo de exatas.py,
// na mesma ordem de operações); a moeda do assíncrono é o bit de cima de um LCG de 64 bits (o long do Java dá a volta como o & M64 do Python).
public class Rodada50 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double df(double t) { return 1.0 / (1.0 + exp_(t)); }

    public static void main(String[] a) {
        String[] esquemas = {"sincrono", "alternado", "assincrono"};
        double eta = 0.1;
        for (String esq : esquemas) {
            double th = 0.1, ps = 0.0;
            long lcg = 83L;
            int n = 1000;
            double[] ts = new double[n + 1], pss = new double[n + 1];
            ts[0] = th; pss[0] = ps;
            for (int k = 1; k <= n; k++) {
                if (esq.equals("sincrono")) {
                    double g = df(ps * th);
                    double nt = th - eta * g * ps, np = ps + eta * g * th;
                    th = nt; ps = np;
                } else if (esq.equals("alternado")) {
                    th = th - eta * df(ps * th) * ps;
                    ps = ps + eta * df(ps * th) * th;
                } else {
                    lcg = lcg * 6364136223846793005L + 1442695040888963407L;
                    if ((lcg >>> 63) == 1L) th = th - eta * df(ps * th) * ps;
                    else ps = ps + eta * df(ps * th) * th;
                }
                ts[k] = th; pss[k] = ps;
            }
            double maximo = -1.0, ultima = 0.0;
            int trocas = 0;
            for (int k = 0; k <= n; k++) {
                System.out.println(esq + " " + k + " " + Double.toHexString(ts[k]) + " " + Double.toHexString(pss[k]));
                double nr = Math.sqrt(ts[k] * ts[k] + pss[k] * pss[k]);
                if (nr > maximo) maximo = nr;
                ultima = nr;
                if (k < n && ts[k] * ts[k + 1] < 0.0) trocas++;
            }
            System.out.println(esq + ": final " + Double.toHexString(ultima) + " maximo " + Double.toHexString(maximo) + " trocas " + trocas);
        }
    }
}
