# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

from src.tipos import EstadoPrograma, NoExpressao, PlanoLinha, TipoNo

OPERADORES = {"+", "-", "*", "/", "//", "%", "^"}


def ehNumeroLiteral(lexema: str) -> bool:
    return lexema.replace(".", "", 1).isdigit()


def executarExpressao(tokens: list[str], estado_programa: EstadoPrograma, indice_linha: int) -> PlanoLinha:
    if len(tokens) != 5:
        raise ValueError("A etapa atual aceita apenas expressoes simples com dois operandos")

    if tokens[0] != "(" or tokens[4] != ")":
        raise ValueError("Expressao malformada")

    if not ehNumeroLiteral(tokens[1]) or not ehNumeroLiteral(tokens[2]):
        raise ValueError("Operandos invalidos para a etapa atual")

    if tokens[3] not in OPERADORES:
        raise ValueError("Operador invalido")

    rotulo_resultado = "resultado_linha_{0}".format(indice_linha)
    estado_programa.historico_rotulos.append(rotulo_resultado)

    return PlanoLinha(
        indice_linha=indice_linha,
        tokens=tokens[:],
        arvore=NoExpressao(
            tipo=TipoNo.OPERACAO,
            operador=tokens[3],
            esquerda=NoExpressao(tipo=TipoNo.NUMERO, valor=tokens[1]),
            direita=NoExpressao(tipo=TipoNo.NUMERO, valor=tokens[2]),
        ),
        rotulo_resultado=rotulo_resultado,
    )
