// Rodada 53 (Parte 86): o passo de Izhikevich, bit a bit. So +,-,*,/ (sem libm), mas a ORDEM das operacoes e identica a do rodada53.py (dois meios-passos
// em v, mesma ordem de somas): 0.04*v*v + 5.0*v + 140.0 - u + I, da esquerda para a direita.
public class Rodada53 {
    static final double A = 0.02, B = 0.2, C = -65.0, D = 8.0, DT = 0.5, I = 10.0;
    static final int PASSOS = 400;

    public static void main(String[] args) {
        double v = C, u = B * C;
        int disparos = 0;
        for (int k = 0; k < PASSOS; k++) {
            v = v + (DT / 2.0) * (0.04 * v * v + 5.0 * v + 140.0 - u + I);
            v = v + (DT / 2.0) * (0.04 * v * v + 5.0 * v + 140.0 - u + I);
            u = u + DT * A * (B * v - u);
            if (v >= 30.0) { v = C; u = u + D; disparos += 1; }
            System.out.println("passo " + k + " v " + Double.toHexString(v) + " u " + Double.toHexString(u));
        }
        System.out.println("disparos: " + disparos);
    }
}
