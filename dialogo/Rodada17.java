// Rodada 17 do diálogo Python <-> Java: a pergunta é a resposta, comprimida. Os mesmos pares (pergunta, rodada seguinte)
// que rodada17.py exportou em base64; C(t) = tamanho do fluxo zlib (Deflater nível 9, com cabeçalho e Adler-32, como o
// zlib.compress do Python). Uso: java Rodada17 PASTA
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;
import java.util.zip.Deflater;

public class Rodada17 {
    static int c(String t) {
        byte[] in = t.getBytes(StandardCharsets.UTF_8);
        Deflater d = new Deflater(9);
        d.setInput(in);
        d.finish();
        byte[] buf = new byte[in.length + 1024];
        int n = 0;
        while (!d.finished()) n += d.deflate(buf, n, buf.length - n);
        d.end();
        return n;
    }

    public static void main(String[] args) throws Exception {
        int i = 0;
        for (String l : Files.readAllLines(Path.of(args[0], "pares17.txt"), StandardCharsets.US_ASCII)) {
            String[] p = l.split("\t");
            String q = new String(Base64.getDecoder().decode(p[0]), StandardCharsets.UTF_8);
            String r = new String(Base64.getDecoder().decode(p[1]), StandardCharsets.UTF_8);
            System.out.println("par " + i + ": C(q) = " + c(q) + "; C(r) = " + c(r) + "; C(r+q) = " + c(r + "\n" + q));
            i++;
        }
    }
}
