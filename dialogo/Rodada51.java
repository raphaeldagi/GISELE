// Rodada 51 (Parte 84): a decisao de Metropolis do recozimento, bit a bit, com o exp PROPRIO (o mesmo de exatas.py). O LCG de 64 bits e o long do Java
// (o & M64 do Python e o overflow natural do long); u = (lcg >>> 11) / 2^53. Imprime exp(-dE/T) e a decisao por caso, e os totais.
public class Rodada51 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    public static void main(String[] a) {
        long lcg = 51L;
        int aceitos = 0;
        double somaP = 0.0;
        for (int k = 0; k < 400; k++) {
            lcg = lcg * 6364136223846793005L + 1442695040888963407L;
            double u = (lcg >>> 11) / (double) (1L << 53);
            double dE = (k - 200) / 50.0;
            double T = 0.5 + (k % 20) / 10.0;
            double p;
            int ac;
            if (dE <= 0.0) { p = 1.0; ac = 1; }
            else { p = exp_(-dE / T); ac = (u < p) ? 1 : 0; }
            somaP += p;
            aceitos += ac;
            System.out.println("caso " + k + " dE " + Double.toHexString(dE) + " T " + Double.toHexString(T)
                + " u " + Double.toHexString(u) + " p " + Double.toHexString(p) + " aceita " + ac);
        }
        System.out.println("totais: aceitos " + aceitos + " soma_p " + Double.toHexString(somaP));
    }
}
