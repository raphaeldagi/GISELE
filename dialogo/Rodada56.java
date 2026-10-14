// Rodada 56 (Parte 89): uma populacao de 6 neuronios de Izhikevich acoplados, bit a bit. Matriz de pesos fixa; corrente = externa + soma(W[i][j]*disparou[j]).
// Ordem das somas identica ao rodada56.py; so +,-,* (sem libm).
public class Rodada56 {
    static final int N = 6, PASSOS = 300;
    static final double DT = 0.5, I_EXT = 5.0;
    static final double[][] W = {
        {0.0, 0.3, 0.0, 0.0, 0.2, 0.0},
        {0.0, 0.0, 0.4, 0.0, 0.0, 0.0},
        {0.2, 0.0, 0.0, 0.3, 0.0, 0.0},
        {0.0, 0.0, 0.0, 0.0, 0.5, 0.0},
        {0.0, 0.0, 0.0, 0.0, 0.0, 0.3},
        {0.4, 0.0, 0.0, 0.0, 0.0, 0.0}};

    public static void main(String[] args) {
        double[] v = new double[N], u = new double[N];
        int[] disparou = new int[N];
        for (int i = 0; i < N; i++) { v[i] = -65.0; u[i] = 0.2 * -65.0; disparou[i] = 0; }
        int total = 0;
        for (int k = 0; k < PASSOS; k++) {
            int[] novoDisp = new int[N];
            double[] correntes = new double[N];
            for (int i = 0; i < N; i++) {
                double acopl = 0.0;
                for (int j = 0; j < N; j++) acopl = acopl + W[i][j] * disparou[j];
                correntes[i] = I_EXT + acopl;
            }
            for (int i = 0; i < N; i++) {
                double ii = correntes[i];
                v[i] = v[i] + (DT / 2.0) * (0.04 * v[i] * v[i] + 5.0 * v[i] + 140.0 - u[i] + ii);
                v[i] = v[i] + (DT / 2.0) * (0.04 * v[i] * v[i] + 5.0 * v[i] + 140.0 - u[i] + ii);
                u[i] = u[i] + DT * 0.02 * (0.2 * v[i] - u[i]);
                if (v[i] >= 30.0) { v[i] = -65.0; u[i] = u[i] + 8.0; novoDisp[i] = 1; total = total + 1; }
            }
            disparou = novoDisp;
            for (int i = 0; i < N; i++) System.out.println("passo " + k + " n " + i + " v " + Double.toHexString(v[i]));
        }
        System.out.println("disparos: " + total);
    }
}
