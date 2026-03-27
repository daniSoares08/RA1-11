# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python main.py teste1.txt")
        return 1

    print("Estrutura inicial criada. Integracao das etapas em andamento.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
