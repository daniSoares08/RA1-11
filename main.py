# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import sys

from src.arquivos import lerArquivo
from src.assembly import gerarProgramaAssembly
from src.exibicao import exibirResultados
from src.executor import executarExpressao
from src.lexer import parseExpressao
from src.tipos import EstadoPrograma


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python main.py teste1.txt")
        return 1

    try:
        nome_arquivo = sys.argv[1]
        linhas: list[str] = []
        lerArquivo(nome_arquivo, linhas)

        estado_programa = EstadoPrograma()
        planos = []

        for indice_linha, linha in enumerate(linhas, start=1):
            if not linha.strip():
                continue

            tokens_linha: list[str] = []
            parseExpressao(linha, tokens_linha, indice_linha)
            planos.append(executarExpressao(tokens_linha, estado_programa, indice_linha))

        codigo_assembly = gerarProgramaAssembly(planos, estado_programa)
        if not codigo_assembly.strip():
            raise ValueError("Falha ao gerar o codigo Assembly")

        exibirResultados([plano.rotulo_resultado for plano in planos])
        return 0
    except (FileNotFoundError, ValueError) as erro:
        print("Erro: {0}".format(erro))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
