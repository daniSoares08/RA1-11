# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class TestPipelineInicial(unittest.TestCase):
    def test_sem_argumento_retorna_erro(self) -> None:
        comando = [sys.executable, "main.py"]
        resultado = subprocess.run(
            comando,
            cwd=str(Path(__file__).resolve().parent.parent),
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("Uso: python main.py teste1.txt", resultado.stdout)


if __name__ == "__main__":
    unittest.main()
