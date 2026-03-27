# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import unittest

from src.lexer import parseExpressao


class TestLexer(unittest.TestCase):
    def test_expressao_valida(self) -> None:
        tokens: list[str] = []
        parseExpressao("(3.14 2.0 +)", tokens, 1)
        self.assertEqual(tokens, ["(", "3.14", "2.0", "+", ")"])

    def test_expressao_aninhada_com_memoria_e_res(self) -> None:
        tokens: list[str] = []
        linha = "(((1 RES) (X) +) ((9 4 %) 2.0 *) /)"
        parseExpressao(linha, tokens, 10)
        self.assertEqual(
            tokens,
            [
                "(",
                "(",
                "(",
                "1",
                "RES",
                ")",
                "(",
                "X",
                ")",
                "+",
                ")",
                "(",
                "(",
                "9",
                "4",
                "%",
                ")",
                "2.0",
                "*",
                ")",
                "/",
                ")",
            ],
        )

    def test_divisao_inteira(self) -> None:
        tokens: list[str] = []
        parseExpressao("(9 4 //)", tokens, 1)
        self.assertEqual(tokens, ["(", "9", "4", "//", ")"])

    def test_memoria(self) -> None:
        tokens: list[str] = []
        parseExpressao("(10.5 MEM)", tokens, 1)
        self.assertEqual(tokens, ["(", "10.5", "MEM", ")"])

    def test_res(self) -> None:
        tokens: list[str] = []
        parseExpressao("(5 RES)", tokens, 1)
        self.assertEqual(tokens, ["(", "5", "RES", ")"])

    def test_numero_malformado(self) -> None:
        tokens: list[str] = []
        with self.assertRaises(ValueError):
            parseExpressao("(3.14.5 2.0 +)", tokens, 1)

    def test_virgula_decimal_invalida(self) -> None:
        tokens: list[str] = []
        with self.assertRaises(ValueError):
            parseExpressao("(3,14 2.0 +)", tokens, 1)

    def test_memoria_com_minusculas_invalida(self) -> None:
        tokens: list[str] = []
        with self.assertRaises(ValueError):
            parseExpressao("(10.5 CONTADOr)", tokens, 1)

    def test_token_invalido(self) -> None:
        tokens: list[str] = []
        with self.assertRaises(ValueError):
            parseExpressao("(3.14 2.0 &)", tokens, 1)

    def test_parenteses_desbalanceados(self) -> None:
        tokens: list[str] = []
        with self.assertRaises(ValueError):
            parseExpressao("((3.14 2.0 +)", tokens, 1)


if __name__ == "__main__":
    unittest.main()
