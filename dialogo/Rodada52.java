// Rodada 52 (Parte 85): a trajetoria inteira de um recozimento, bit a bit. Um LCG de 64 bits (o long do Java) gera a direcao (bit de cima) e o u da
// aceitacao (53 bits de cima do proximo avanco). exp PROPRIO (o mesmo de exatas.py). Mesma paisagem, mesmo cronograma do rodada52.py.
public class Rodada52 {
    static final double LN2_HI = 6.93147180369123816490e-01, LN2_LO = 1.90821492927058770002e-10;
    static final int N = 20, PASSOS = 300;

    static double exp_(double x) {
        double k = Math.floor(x / (LN2_HI + LN2_LO) + 0.5);
        double r = (x - k * LN2_HI) - k * LN2_LO;
        double p = 1.0;
        for (int i = 22; i >= 1; i--) p = 1.0 + r * p / i;
        return Math.scalb(p, (int) k);
    }

    static double energia(int i) {
        double e = 0.01 * ((i - 15) * (i - 15));
        if (i == 3) e = -5.0;
        else if (i == 2 || i == 4) e = -3.0;
        return e;
    }

    public static void main(String[] a) {
        long lcg = 52L;
        int i = 10, melhorI = 10;
        double melhorE = energia(10);
        for (int k = 0; k < PASSOS; k++) {
            double T = 2.0 * Math.pow(0.01 / 2.0, (double) k / (PASSOS - 1));
            lcg = lcg * 6364136223846793005L + 1442695040888963407L;
            int direcao = (lcg >>> 63) == 1L ? 1 : -1;
            lcg = lcg * 6364136223846793005L + 1442695040888963407L;
            double u = (lcg >>> 11) / (double) (1L << 53);
            int j = i + direcao;
            if (j >= 0 && j < N) {
                double dE = energia(j) - energia(i);
                if (dE <= 0.0 || u < exp_(-dE / T)) i = j;
            }
            double ei = energia(i);
            if (ei < melhorE) { melhorE = ei; melhorI = i; }
            System.out.println("passo " + k + " i " + i + " T " + Double.toHexString(T) + " E " + Double.toHexString(ei));
        }
        System.out.println("melhor: i " + melhorI + " E " + Double.toHexString(melhorE));
    }
}
