# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import unittest

from src.executor import executarExpressao
from src.tipos import EstadoPrograma, TipoNo


class TestExecutor(unittest.TestCase):
    def test_operacao_simples(self) -> None:
        estado = EstadoPrograma()
        plano = executarExpressao(["(", "3.14", "2.0", "+", ")"], estado, 1)
        self.assertEqual(plano.arvore.tipo, TipoNo.OPERACAO)
        self.assertEqual(plano.arvore.operador, "+")
        self.assertEqual(estado.historico_rotulos, ["resultado_linha_1"])

    def test_leitura_memoria(self) -> None:
        estado = EstadoPrograma()
        plano = executarExpressao(["(", "MEM", ")"], estado, 1)
        self.assertEqual(plano.arvore.tipo, TipoNo.MEMORIA_LEITURA)
        self.assertEqual(plano.arvore.valor, "MEM")
        self.assertIn("MEM", estado.memorias)

    def test_escrita_memoria(self) -> None:
        estado = EstadoPrograma()
        plano = executarExpressao(["(", "7.5", "X", ")"], estado, 1)
        self.assertEqual(plano.arvore.tipo, TipoNo.MEMORIA_ESCRITA)
        self.assertEqual(plano.arvore.valor, "X")
        self.assertIn("X", estado.memorias)

    def test_res_valido(self) -> None:
        estado = EstadoPrograma(historico_rotulos=["resultado_linha_1"])
        plano = executarExpressao(["(", "1", "RES", ")"], estado, 2)
        self.assertEqual(plano.arvore.tipo, TipoNo.RESULTADO_ANTERIOR)
        self.assertEqual(plano.arvore.valor, "1")
        self.assertEqual(estado.historico_rotulos[-1], "resultado_linha_2")

    def test_res_invalido(self) -> None:
        estado = EstadoPrograma()
        with self.assertRaises(ValueError):
            executarExpressao(["(", "1", "RES", ")"], estado, 1)

    def test_expressao_aninhada(self) -> None:
        estado = EstadoPrograma(historico_rotulos=["resultado_linha_1"])
        tokens = [
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
        ]
        plano = executarExpressao(tokens, estado, 2)

        self.assertEqual(plano.arvore.tipo, TipoNo.OPERACAO)
        self.assertEqual(plano.arvore.esquerda.tipo, TipoNo.RESULTADO_ANTERIOR)
        self.assertEqual(plano.arvore.direita.tipo, TipoNo.MEMORIA_LEITURA)
        self.assertIn("X", estado.memorias)


if __name__ == "__main__":
    unittest.main()
