# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

from src.tipos import EstadoPrograma, NoExpressao, PlanoLinha, TipoNo

OPERADORES = {"+", "-", "*", "/", "//", "%", "^"}


def ehNumeroLiteral(lexema: str) -> bool:
    return lexema.replace(".", "", 1).isdigit()


def ehInteiroNaoNegativo(lexema: str) -> bool:
    return lexema.isdigit()


def ehNomeMemoria(lexema: str) -> bool:
    return lexema.isupper() and lexema != "RES"


def executarExpressao(tokens: list[str], estado_programa: EstadoPrograma, indice_linha: int) -> PlanoLinha:
    arvore, indice_final = construirArvoreExpressao(tokens, 0)

    if indice_final != len(tokens):
        raise ValueError(
            "Sobrou token depois do fim da expressao na linha {0}".format(indice_linha)
        )

    validarReferencias(arvore, estado_programa, indice_linha)
    registrarMemorias(arvore, estado_programa)

    rotulo_resultado = "resultado_linha_{0}".format(indice_linha)
    estado_programa.historico_rotulos.append(rotulo_resultado)

    return PlanoLinha(
        indice_linha=indice_linha,
        tokens=tokens[:],
        arvore=arvore,
        rotulo_resultado=rotulo_resultado,
    )


def construirArvoreExpressao(tokens: list[str], indice: int) -> tuple[NoExpressao, int]:
    if indice >= len(tokens) or tokens[indice] != "(":
        raise ValueError("Expressao deve comecar com '('")

    indice += 1
    if indice >= len(tokens):
        raise ValueError("Fim inesperado da expressao")

    if ehNomeMemoria(tokens[indice]) and indice + 1 < len(tokens) and tokens[indice + 1] == ")":
        return NoExpressao(tipo=TipoNo.MEMORIA_LEITURA, valor=tokens[indice]), indice + 2

    primeiro, indice = lerOperando(tokens, indice)

    if indice >= len(tokens):
        raise ValueError("Fim inesperado apos o primeiro operando")

    token_atual = tokens[indice]

    if token_atual == "RES":
        if primeiro.tipo != TipoNo.NUMERO or primeiro.valor is None or not ehInteiroNaoNegativo(primeiro.valor):
            raise ValueError("Comando RES exige inteiro nao negativo")
        if indice + 1 >= len(tokens) or tokens[indice + 1] != ")":
            raise ValueError("Comando RES malformado")
        return NoExpressao(tipo=TipoNo.RESULTADO_ANTERIOR, valor=primeiro.valor), indice + 2

    if ehNomeMemoria(token_atual):
        if indice + 1 >= len(tokens) or tokens[indice + 1] != ")":
            raise ValueError("Comando de memoria malformado")
        return NoExpressao(
            tipo=TipoNo.MEMORIA_ESCRITA,
            valor=token_atual,
            esquerda=primeiro,
        ), indice + 2

    segundo, indice = lerOperando(tokens, indice)
    if indice >= len(tokens) or tokens[indice] not in OPERADORES:
        raise ValueError("Operador invalido ou ausente")

    operador = tokens[indice]
    indice += 1

    if indice >= len(tokens) or tokens[indice] != ")":
        raise ValueError("Expressao operacional malformada")

    return (
        NoExpressao(
            tipo=TipoNo.OPERACAO,
            operador=operador,
            esquerda=primeiro,
            direita=segundo,
        ),
        indice + 1,
    )


def lerOperando(tokens: list[str], indice: int) -> tuple[NoExpressao, int]:
    if indice >= len(tokens):
        raise ValueError("Fim inesperado ao ler operando")

    token = tokens[indice]
    if token == "(":
        return construirArvoreExpressao(tokens, indice)

    if ehNumeroLiteral(token):
        return NoExpressao(tipo=TipoNo.NUMERO, valor=token), indice + 1

    raise ValueError("Operando invalido: {0}".format(token))


def validarReferencias(no: NoExpressao, estado_programa: EstadoPrograma, indice_linha: int) -> None:
    if no.tipo == TipoNo.RESULTADO_ANTERIOR:
        if no.valor is None:
            raise ValueError("Referencia RES sem valor")
        linhas_voltadas = int(no.valor)
        if linhas_voltadas > len(estado_programa.historico_rotulos):
            raise ValueError("RES invalido na linha {0}".format(indice_linha))
        return

    if no.esquerda is not None:
        validarReferencias(no.esquerda, estado_programa, indice_linha)

    if no.direita is not None:
        validarReferencias(no.direita, estado_programa, indice_linha)


def registrarMemorias(no: NoExpressao, estado_programa: EstadoPrograma) -> None:
    if no.tipo in {TipoNo.MEMORIA_LEITURA, TipoNo.MEMORIA_ESCRITA} and no.valor is not None:
        estado_programa.memorias.add(no.valor)

    if no.esquerda is not None:
        registrarMemorias(no.esquerda, estado_programa)

    if no.direita is not None:
        registrarMemorias(no.direita, estado_programa)
