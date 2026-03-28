# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.arquivos import (
    garantirDiretorioSaidas,
    lerArquivo,
    salvarAssemblyUltimaExecucao,
    salvarTokensUltimaExecucao,
)


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

    def test_salvar_artefatos(self) -> None:
        with tempfile.TemporaryDirectory() as diretorio:
            caminho_tokens = Path(diretorio) / "saidas" / "tokens.txt"
            caminho_assembly = Path(diretorio) / "saidas" / "programa.s"

            salvarTokensUltimaExecucao(["(", "1", "RES", ")"], str(caminho_tokens))
            salvarAssemblyUltimaExecucao(".text\n", str(caminho_assembly))

            self.assertEqual(
                caminho_tokens.read_text(encoding="utf-8").splitlines(),
                ["(", "1", "RES", ")"],
            )
            self.assertEqual(caminho_assembly.read_text(encoding="utf-8"), ".text\n")

    def test_garantir_diretorio_saidas(self) -> None:
        with tempfile.TemporaryDirectory() as diretorio:
            atual = Path.cwd()
            try:
                Path(diretorio).mkdir(parents=True, exist_ok=True)
                import os

                os.chdir(diretorio)
                garantirDiretorioSaidas()
                self.assertTrue(Path("saidas").exists())
                self.assertTrue(Path("saidas").is_dir())
            finally:
                os.chdir(atual)


if __name__ == "__main__":
    unittest.main()
