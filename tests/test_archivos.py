# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.arquivos import lerArquivo


class TestArquivos(unittest.TestCase):
    def test_ler_arquivo(self) -> None:
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "teste.txt"
            caminho.write_text("(3.14 2.0 +)\n(9 4 //)\n", encoding="utf-8")

            linhas: list[str] = []
            lerArquivo(str(caminho), linhas)

            self.assertEqual(linhas, ["(3.14 2.0 +)", "(9 4 //)"])

    def test_arquivo_inexistente(self) -> None:
        linhas: list[str] = []
        with self.assertRaises(FileNotFoundError):
            lerArquivo("nao_existe.txt", linhas)


if __name__ == "__main__":
    unittest.main()
