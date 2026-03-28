# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

from pathlib import Path


def lerArquivo(nomeArquivo: str, linhas: list[str]) -> None:
    caminho = Path(nomeArquivo)

    if not caminho.exists():
        raise FileNotFoundError("Arquivo nao encontrado: {0}".format(nomeArquivo))

    if not caminho.is_file():
        raise ValueError("O caminho informado nao e um arquivo: {0}".format(nomeArquivo))

    with caminho.open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linhas.append(linha.rstrip("\n"))


def garantirDiretorioSaidas() -> None:
    Path("saidas").mkdir(parents=True, exist_ok=True)


def salvarTokensUltimaExecucao(tokens: list[str], caminho: str) -> None:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with destino.open("w", encoding="utf-8") as arquivo:
        for token in tokens:
            arquivo.write("{0}\n".format(token))


def salvarAssemblyUltimaExecucao(codigoAssembly: str, caminho: str) -> None:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with destino.open("w", encoding="utf-8") as arquivo:
        arquivo.write(codigoAssembly)
