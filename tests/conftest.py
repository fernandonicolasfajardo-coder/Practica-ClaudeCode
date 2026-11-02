"""Configuración de pytest: hace importable el módulo de la raíz del proyecto."""

import sys
from pathlib import Path

RAIZ_PROYECTO: Path = Path(__file__).resolve().parent.parent

if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))
