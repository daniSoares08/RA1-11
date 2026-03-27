# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from src.assembly import gerarProgramaAssembly
from src.executor import executarExpressao
from src.lexer import parseExpressao
from src.tipos import EstadoPrograma


class TestAssembly(unittest.TestCase):
    def localizar_ferramenta(self, nome: str) -> str | None:
        caminho_local = (
            Path(__file__).resolve().parent.parent
            / ".tools"
            / "gcc-arm-none-eabi-10.3-2021.10"
            / "gcc-arm-none-eabi-10.3-2021.10"
            / "bin"
            / ("{0}.exe".format(nome))
        )
        if caminho_local.exists():
            return str(caminho_local)
        return shutil.which(nome)

    def test_gera_secao_basica(self) -> None:
        estado = EstadoPrograma()
        linhas = [
            "(3.14 2.0 +)",
            "((10.0 4.0 -) (2.0 3.0 +) *)",
            "(7.5 X)",
            "((X) 2.5 +)",
            "(1 RES)",
            "(9 4 //)",
            "(9 4 %)",
            "(2.0 3 ^)",
        ]
        planos = []

        for indice, linha in enumerate(linhas, start=1):
            tokens: list[str] = []
            parseExpressao(linha, tokens, indice)
            planos.append(executarExpressao(tokens, estado, indice))

        codigo = gerarProgramaAssembly(planos, estado)

        self.assertIn(".data", codigo)
        self.assertIn(".text", codigo)
        self.assertIn("_start:", codigo)
        self.assertIn("resultado_linha_8", codigo)
        self.assertIn("mem_X", codigo)
        self.assertIn("const_0: .double 3.14", codigo)
        self.assertIn("push_d0", codigo)
        self.assertIn("pop_d0", codigo)
        self.assertIn("vadd.f64", codigo)
        self.assertIn("vsub.f64", codigo)
        self.assertIn("vmul.f64", codigo)
        self.assertIn("vdiv.f64", codigo)
        self.assertIn("op_mod_int", codigo)
        self.assertIn("op_pow_double", codigo)
        self.assertIn("resultado_linha_4", codigo)
        self.assertIn("dividir_inteiros_assinados", codigo)
        self.assertNotIn("sdiv ", codigo)
        self.assertNotIn("vmov d0, d2", codigo)

    def test_monta_e_linka_com_toolchain_arm_quando_disponivel(self) -> None:
        as_exe = self.localizar_ferramenta("arm-none-eabi-as")
        gcc_exe = self.localizar_ferramenta("arm-none-eabi-gcc")

        if not as_exe or not gcc_exe:
            self.skipTest("Toolchain ARM local nao disponivel")

        estado = EstadoPrograma()
        linhas = [
            "(1.25 8.75 +)",
            "(22 5 //)",
            "(22 5 %)",
            "(3.0 4 ^)",
            "(6.5 ACUM)",
            "((ACUM) 2.0 *)",
            "(2 RES)",
        ]
        planos = []

        for indice, linha in enumerate(linhas, start=1):
            tokens: list[str] = []
            parseExpressao(linha, tokens, indice)
            planos.append(executarExpressao(tokens, estado, indice))

        codigo = gerarProgramaAssembly(planos, estado)

        with tempfile.TemporaryDirectory() as diretorio:
            caminho_s = Path(diretorio) / "programa.s"
            caminho_o = Path(diretorio) / "programa.o"
            caminho_elf = Path(diretorio) / "programa.elf"
            caminho_s.write_text(codigo, encoding="utf-8")

            subprocess.run(
                [
                    as_exe,
                    "-mfloat-abi=softfp",
                    "-march=armv7-a",
                    "-mcpu=cortex-a9",
                    "-mfpu=neon-fp16",
                    "--gdwarf2",
                    "-o",
                    str(caminho_o),
                    str(caminho_s),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            subprocess.run(
                [
                    gcc_exe,
                    "-mfloat-abi=softfp",
                    "-march=armv7-a",
                    "-mcpu=cortex-a9",
                    "-mfpu=neon-fp16",
                    "-nostdlib",
                    "-Wl,-Ttext=0x0",
                    "-Wl,-Tdata=0x4000",
                    "-o",
                    str(caminho_elf),
                    str(caminho_s),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertTrue(caminho_o.exists())
            self.assertTrue(caminho_elf.exists())


if __name__ == "__main__":
    unittest.main()
