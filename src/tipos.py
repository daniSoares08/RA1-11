# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class TipoToken(Enum):
    ABRE_PAREN = auto()
    FECHA_PAREN = auto()
    NUMERO = auto()
    OPERADOR = auto()
    IDENTIFICADOR = auto()
    KEYWORD_RES = auto()


class TipoNo(Enum):
    NUMERO = auto()
    OPERACAO = auto()
    MEMORIA_LEITURA = auto()
    MEMORIA_ESCRITA = auto()
    RESULTADO_ANTERIOR = auto()


@dataclass
class Token:
    tipo: TipoToken
    lexema: str
    linha: int
    coluna: int


@dataclass
class ContextoLexico:
    linha: str
    linha_numero: int
    indice: int = 0
    inicio_lexema: int = 0
    lexema_atual: list[str] = field(default_factory=list)
    tokens: list[str] = field(default_factory=list)
    tokens_detalhados: list[Token] = field(default_factory=list)


@dataclass
class NoExpressao:
    tipo: TipoNo
    valor: str | None = None
    operador: str | None = None
    esquerda: NoExpressao | None = None
    direita: NoExpressao | None = None


@dataclass
class PlanoLinha:
    indice_linha: int
    tokens: list[str]
    arvore: NoExpressao
    rotulo_resultado: str


@dataclass
class EstadoPrograma:
    memorias: set[str] = field(default_factory=set)
    historico_rotulos: list[str] = field(default_factory=list)
