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

    def test_formato_invalido(self) -> None:
        estado = EstadoPrograma()
        with self.assertRaises(ValueError):
            executarExpressao(["(", "3.14", "+", ")"], estado, 1)


if __name__ == "__main__":
    unittest.main()
