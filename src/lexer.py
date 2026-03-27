# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

from src.tipos import ContextoLexico, TipoToken, Token

OPERADORES = {"+", "-", "*", "/", "//", "%", "^"}


def caractereAtual(contexto: ContextoLexico) -> str | None:
    if contexto.indice >= len(contexto.linha):
        return None
    return contexto.linha[contexto.indice]


def avancar(contexto: ContextoLexico) -> str | None:
    caractere = caractereAtual(contexto)
    if caractere is not None:
        contexto.indice += 1
    return caractere


def iniciarLexema(contexto: ContextoLexico) -> None:
    contexto.inicio_lexema = contexto.indice
    contexto.lexema_atual.clear()


def anexarAtualEAvancar(contexto: ContextoLexico) -> None:
    caractere = avancar(contexto)
    if caractere is not None:
        contexto.lexema_atual.append(caractere)


def lexemaAtual(contexto: ContextoLexico) -> str:
    return "".join(contexto.lexema_atual)


def adicionarTokenSimples(contexto: ContextoLexico, lexema: str, tipo: TipoToken) -> None:
    coluna = contexto.indice + 1
    avancar(contexto)
    contexto.tokens.append(lexema)
    contexto.tokens_detalhados.append(
        Token(tipo=tipo, lexema=lexema, linha=contexto.linha_numero, coluna=coluna)
    )


def finalizarLexema(contexto: ContextoLexico, tipo: TipoToken) -> None:
    lexema = lexemaAtual(contexto)
    contexto.tokens.append(lexema)
    contexto.tokens_detalhados.append(
        Token(
            tipo=tipo,
            lexema=lexema,
            linha=contexto.linha_numero,
            coluna=contexto.inicio_lexema + 1,
        )
    )
    contexto.lexema_atual.clear()


def classificarPalavraMaiuscula(lexema: str) -> TipoToken:
    if lexema == "RES":
        return TipoToken.KEYWORD_RES
    return TipoToken.IDENTIFICADOR


def erroLexico(contexto: ContextoLexico, mensagem: str, coluna: int | None = None) -> ValueError:
    coluna_erro = coluna if coluna is not None else contexto.indice + 1
    return ValueError(
        "Erro lexico na linha {0}, coluna {1}: {2}".format(
            contexto.linha_numero,
            coluna_erro,
            mensagem,
        )
    )


def caractereFechaToken(caractere: str | None) -> bool:
    if caractere is None:
        return True
    return caractere.isspace() or caractere in {"(", ")"}


def garantirDelimitador(contexto: ContextoLexico, descricao: str) -> None:
    caractere = caractereAtual(contexto)
    if not caractereFechaToken(caractere):
        raise erroLexico(
            contexto,
            "{0} seguido por caractere invalido '{1}'".format(descricao, caractere),
        )


def parseExpressao(linha: str, tokens: list[str], numero_linha: int = 1) -> None:
    contexto = ContextoLexico(linha=linha, linha_numero=numero_linha, tokens=tokens)
    estado = estadoInicial

    while estado is not None:
        estado = estado(contexto)

    validarParentesesBalanceados(contexto.tokens, numero_linha)


def estadoInicial(contexto: ContextoLexico):
    caractere = caractereAtual(contexto)

    if caractere is None:
        return None

    if caractere.isspace():
        avancar(contexto)
        return estadoInicial

    if caractere == "(":
        adicionarTokenSimples(contexto, "(", TipoToken.ABRE_PAREN)
        return estadoInicial

    if caractere == ")":
        adicionarTokenSimples(contexto, ")", TipoToken.FECHA_PAREN)
        return estadoInicial

    if caractere.isdigit():
        iniciarLexema(contexto)
        return estadoNumeroInteiro

    if caractere == "/":
        iniciarLexema(contexto)
        return estadoBarra

    if caractere in {"+", "-", "*", "%", "^"}:
        adicionarTokenSimples(contexto, caractere, TipoToken.OPERADOR)
        return estadoInicial

    if "A" <= caractere <= "Z":
        iniciarLexema(contexto)
        return estadoPalavraMaiuscula

    raise erroLexico(
        contexto,
        "token invalido '{0}'".format(caractere),
    )


def estadoNumeroInteiro(contexto: ContextoLexico):
    caractere = caractereAtual(contexto)

    if caractere is not None and caractere.isdigit():
        anexarAtualEAvancar(contexto)
        return estadoNumeroInteiro

    if caractere == ".":
        anexarAtualEAvancar(contexto)
        return estadoNumeroFracionario

    garantirDelimitador(contexto, "numero")
    finalizarLexema(contexto, TipoToken.NUMERO)
    return estadoInicial


def estadoNumeroFracionario(contexto: ContextoLexico):
    caractere = caractereAtual(contexto)

    if caractere is not None and caractere.isdigit():
        anexarAtualEAvancar(contexto)
        return estadoNumeroFracionario

    if caractere == ".":
        raise erroLexico(
            contexto,
            "numero malformado",
            contexto.inicio_lexema + 1,
        )

    if lexemaAtual(contexto).endswith("."):
        raise erroLexico(
            contexto,
            "numero malformado",
            contexto.inicio_lexema + 1,
        )

    garantirDelimitador(contexto, "numero")
    finalizarLexema(contexto, TipoToken.NUMERO)
    return estadoInicial


def estadoPalavraMaiuscula(contexto: ContextoLexico):
    caractere = caractereAtual(contexto)

    if caractere is not None and "A" <= caractere <= "Z":
        anexarAtualEAvancar(contexto)
        return estadoPalavraMaiuscula

    if caractere is not None and (caractere.isdigit() or caractere.islower()):
        raise erroLexico(
            contexto,
            "identificador de memoria deve conter apenas letras maiusculas",
            contexto.inicio_lexema + 1,
        )

    garantirDelimitador(contexto, "identificador")
    finalizarLexema(contexto, classificarPalavraMaiuscula(lexemaAtual(contexto)))
    return estadoInicial


def estadoBarra(contexto: ContextoLexico):
    if not contexto.lexema_atual:
        anexarAtualEAvancar(contexto)

    caractere = caractereAtual(contexto)
    if caractere == "/":
        anexarAtualEAvancar(contexto)
    elif not caractereFechaToken(caractere):
        raise erroLexico(
            contexto,
            "operador invalido iniciando com '/'",
            contexto.inicio_lexema + 1,
        )

    finalizarLexema(contexto, TipoToken.OPERADOR)
    return estadoInicial


def validarParentesesBalanceados(tokens: list[str], numero_linha: int) -> None:
    saldo = 0

    for token in tokens:
        if token == "(":
            saldo += 1
        elif token == ")":
            saldo -= 1

        if saldo < 0:
            raise ValueError("Parenteses desbalanceados na linha {0}".format(numero_linha))

    if saldo != 0:
        raise ValueError("Parenteses desbalanceados na linha {0}".format(numero_linha))

    for token in tokens:
        if token in OPERADORES:
            continue
        if token in {"(", ")", "RES"}:
            continue
        if token.replace(".", "", 1).isdigit():
            continue
        if token.isupper():
            continue
        raise ValueError(
            "Token invalido na linha {0}: {1}".format(numero_linha, token)
        )
