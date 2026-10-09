// Rodada 7 do diálogo Python <-> Java: o detector de surpresa da ThompsonSurpresa (synthai/decisao.py), em Java: posterior
// Beta por braço, janela das últimas 20 recompensas, renovação quando |média da janela − média do posterior| passa de
// 3·√(m(1 − m)/20). Ações em rodízio, recompensas do gerador da rodada 5 (semente 707). Uso: java Rodada07
import java.util.*;

public class Rodada07 {
    static long x = 707L;
    static final long A = 6364136223846793005L, C = 1442695040888963407L;

    static double uniforme() {
        x = A * x + C;
        return (x >>> 11) * 0x1.0p-53;
    }

    public static void main(String[] args) {
        int k = 3, janela = 20;
        double z = 3.0;
        double[] a = {1, 1, 1}, b = {1, 1, 1};
        List<ArrayDeque<Integer>> rec = new ArrayList<>();
        for (int i = 0; i < k; i++) rec.add(new ArrayDeque<>());
        int renov = 0;
        StringBuilder ev = new StringBuilder("eventos =");
        for (int passo = 0; passo < 1200; passo++) {
            double[] ps = passo < 600 ? new double[]{0.2, 0.5, 0.8} : new double[]{0.8, 0.5, 0.2};
            int br = passo % 3;
            int r = uniforme() < ps[br] ? 1 : 0;
            if (r == 1) a[br] += 1; else b[br] += 1;
            ArrayDeque<Integer> q = rec.get(br);
            q.addLast(r);
            if (q.size() > janela) q.removeFirst();
            if (q.size() == janela) {
                double m = a[br] / (a[br] + b[br]);
                int soma = 0;
                for (int y : q) soma += y;
                double mj = (double) soma / janela;  // o sum(rec) / janela do Python: soma inteira, depois divisão
                if (Math.abs(mj - m) > z * Math.sqrt(Math.max(m * (1 - m), 1e-9) / janela)) {
                    a[br] = 1.0 + soma;
                    b[br] = 1.0 + janela - soma;
                    renov++;
                    ev.append(' ').append(passo).append(':').append(br);
                }
            }
        }
        System.out.println("renovacoes = " + renov);
        System.out.println(ev);
        System.out.println("a = " + Double.toHexString(a[0]) + " " + Double.toHexString(a[1]) + " " + Double.toHexString(a[2]));
        System.out.println("b = " + Double.toHexString(b[0]) + " " + Double.toHexString(b[1]) + " " + Double.toHexString(b[2]));
    }
}
