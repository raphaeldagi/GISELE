// Rodada 13 do diálogo Python <-> Java: o arquivo binário de pesos. A IA-Java calcula a mesma crença (ThompsonDescontado,
// γ = 0,99, 500 recompensas do gerador da rodada 5, semente 1313), lê o arquivo que o Python gravou, confere, e grava o
// seu: 'SYN1' + int32 k + 2k float64, little-endian. A armadilha da fronteira: o ByteBuffer do Java é BIG-endian por
// padrão; o struct "<" do Python é little-endian. Uso: java Rodada13 PASTA
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.*;
import java.security.MessageDigest;

public class Rodada13 {
    static long x = 1313L;
    static final long A = 6364136223846793005L, C = 1442695040888963407L;

    static double uniforme() {
        x = A * x + C;
        return (x >>> 11) * 0x1.0p-53;
    }

    static String sha(byte[] d) throws Exception {
        StringBuilder sb = new StringBuilder();
        for (byte b : MessageDigest.getInstance("SHA-256").digest(d)) sb.append(String.format("%02x", b));
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        int k = 10;
        double g = 0.99;
        double[] a = new double[k], b = new double[k];
        java.util.Arrays.fill(a, 1.0);
        java.util.Arrays.fill(b, 1.0);
        for (int passo = 0; passo < 500; passo++) {
            int i = passo % k;
            int r = uniforme() < (i + 1) / 11.0 ? 1 : 0;
            for (int j = 0; j < k; j++) { a[j] = 1.0 + g * (a[j] - 1.0); b[j] = 1.0 + g * (b[j] - 1.0); }
            if (r == 1) a[i] += 1; else b[i] += 1;
        }
        ByteBuffer buf = ByteBuffer.allocate(8 + 16 * k).order(ByteOrder.LITTLE_ENDIAN);
        buf.put(new byte[]{'S', 'Y', 'N', '1'}).putInt(k);
        for (double v : a) buf.putDouble(v);
        for (double v : b) buf.putDouble(v);
        byte[] meu = buf.array();
        Files.write(Path.of(args[0], "pesos_java.bin"), meu);
        byte[] py = Files.readAllBytes(Path.of(args[0], "pesos_py.bin"));
        ByteBuffer lp = ByteBuffer.wrap(py).order(ByteOrder.LITTLE_ENDIAN);
        lp.position(8);
        StringBuilder la = new StringBuilder("a ="), lb = new StringBuilder("b =");
        for (int j = 0; j < k; j++) la.append(' ').append(Double.toHexString(lp.getDouble()));
        for (int j = 0; j < k; j++) lb.append(' ').append(Double.toHexString(lp.getDouble()));
        System.out.println("arquivo do Python: " + py.length + " bytes; sha = " + sha(py));
        System.out.println("arquivo do Java: " + meu.length + " bytes; sha = " + sha(meu));
        System.out.println(la);
        System.out.println(lb);
        System.out.println("os dois arquivos sao iguais byte a byte: " + (java.util.Arrays.equals(py, meu) ? "True" : "False"));
    }
}
