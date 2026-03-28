# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations


def exibirResultados(resultados: list[str]) -> None:
    for indice, resultado in enumerate(resultados, start=1):
        print("Linha {0}: resultado salvo em {1}".format(indice, resultado))

    print("Tokens salvos em saidas/ultimo_tokens.txt")
    print("Assembly salvo em saidas/ultimo_programa_armv7.s")
