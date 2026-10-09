"""Verifica todas as rodadas do diálogo: para cada RodadaNN.java com o seu rodadaNN.py, compila o Java, roda os dois e
compara as saídas bit a bit (comparar.py). Uso, da raiz do repositório: python3 dialogo/verificar.py"""

import glob
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from comparar import comparar  # noqa: E402


def main():
    tudo_ok = True
    with tempfile.TemporaryDirectory() as tmp:
        for java in sorted(glob.glob(os.path.join(AQUI, "Rodada*.java"))):
            nome = os.path.basename(java)[:-5]
            py = os.path.join(AQUI, "r" + nome[1:] + ".py")
            subprocess.run(["javac", "-d", tmp, java], check=True, capture_output=True)
            if "--preparar" in open(py, encoding="utf-8").read():  # a rodada escreve primeiro os dados que o Java lê
                subprocess.run([sys.executable, py, "--preparar", tmp], check=True)
            sj = subprocess.run(["java", "-cp", tmp, nome, tmp], check=True, capture_output=True, text=True,
                                cwd=os.path.dirname(AQUI)).stdout
            sp = subprocess.run([sys.executable, py], check=True, capture_output=True, text=True).stdout
            fj, fp = os.path.join(tmp, nome + ".java.txt"), os.path.join(tmp, nome + ".py.txt")
            open(fj, "w").write(sj)
            open(fp, "w").write(sp)
            ok, msg = comparar(fp, fj)
            tudo_ok &= ok
            print(f"{nome}: {'IGUAIS' if ok else 'DIFERENTES'} ({msg})")
    sys.exit(0 if tudo_ok else 1)


if __name__ == "__main__":
    main()
