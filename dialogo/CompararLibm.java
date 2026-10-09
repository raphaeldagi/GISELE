// Ferramenta da Rodada 28 (não é uma rodada): lê "argumento_hex valor_glibc_hex" e conta em quantos o Math.exp/Math.log do
// Java dá outro valor. Uso: java CompararLibm ARQUIVO exp|log
import java.nio.file.*;
import java.util.*;

public class CompararLibm {
    public static void main(String[] a) throws Exception {
        int n = 0, dif = 0;
        for (String l : Files.readAllLines(Path.of(a[0]))) {
            String[] c = l.split(" ");
            double x = Double.parseDouble(c[0].replace("0x", "0x")), g = Double.parseDouble(c[1]);
            double j = a[1].equals("exp") ? Math.exp(x) : Math.log(x);
            n++;
            if (Double.doubleToRawLongBits(j) != Double.doubleToRawLongBits(g)) dif++;
        }
        System.out.println(n + " " + dif);
    }
}
