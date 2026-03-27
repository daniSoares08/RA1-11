# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import sys

from src.arquivos import lerArquivo
from src.exibicao import exibirResultados


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python main.py teste1.txt")
        return 1

    try:
        nome_arquivo = sys.argv[1]
        linhas: list[str] = []
        lerArquivo(nome_arquivo, linhas)
        exibirResultados(
            [
                "Arquivo carregado com {0} linhas para a proxima etapa de integracao.".format(
                    len([linha for linha in linhas if linha.strip()])
                )
            ]
        )
        return 0
    except (FileNotFoundError, ValueError) as erro:
        print("Erro: {0}".format(erro))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
