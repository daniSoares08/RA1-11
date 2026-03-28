# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from src.lexer import parseExpressao


class TestPipeline(unittest.TestCase):
    def test_arquivos_de_teste_seguem_requisitos(self) -> None:
        operadores = ["+", "-", "*", "/", "//", "%", "^"]

        for nome_arquivo in ("teste1.txt", "teste2.txt", "teste3.txt"):
            conteudo = Path(nome_arquivo).read_text(encoding="utf-8").splitlines()
            linhas = [linha for linha in conteudo if linha.strip()]

            self.assertGreaterEqual(len(linhas), 10)
            for operador in operadores:
                self.assertTrue(any(operador in linha for linha in linhas), nome_arquivo)
            self.assertTrue(any("RES" in linha for linha in linhas), nome_arquivo)
            self.assertTrue(any("(X)" in linha or "(TOTAL)" in linha or "(ACUM)" in linha for linha in linhas), nome_arquivo)
            self.assertTrue(any(linha.count("(") > 2 for linha in linhas), nome_arquivo)

    def test_fluxo_completo_gera_artefatos(self) -> None:
        comando = [sys.executable, "main.py", "teste1.txt"]
        resultado = subprocess.run(
            comando,
            cwd=str(Path(__file__).resolve().parent.parent),
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Linha 1", resultado.stdout)

        caminho_tokens = Path("saidas/ultimo_tokens.txt")
        caminho_assembly = Path("saidas/ultimo_programa_armv7.s")

        self.assertTrue(caminho_tokens.exists())
        self.assertTrue(caminho_assembly.exists())
        self.assertIn(".text", caminho_assembly.read_text(encoding="utf-8"))

        tokens_esperados: list[str] = []
        for indice, linha in enumerate(Path("teste1.txt").read_text(encoding="utf-8").splitlines(), start=1):
            if not linha.strip():
                continue
            parseExpressao(linha, tokens_esperados, indice)

        self.assertEqual(
            caminho_tokens.read_text(encoding="utf-8").splitlines(),
            tokens_esperados,
        )

    def test_sem_argumento_retorna_erro(self) -> None:
        comando = [sys.executable, "main.py"]
        resultado = subprocess.run(
            comando,
            cwd=str(Path(__file__).resolve().parent.parent),
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("Uso: python main.py teste1.txt", resultado.stdout)


if __name__ == "__main__":
    unittest.main()
