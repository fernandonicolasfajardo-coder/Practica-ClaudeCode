import sys
from datetime import datetime

PILARES: list[str] = [
    "1. Planificación: definir alcance, objetivos y riesgos de la auditoría.",
    "2. Ejecución: recopilar evidencias y evaluar controles.",
    "3. Informe y seguimiento: comunicar hallazgos y verificar acciones correctivas.",
]

RUTA_LOG: str = "log.txt"


def mostrar_pilares(pilares: list[str]) -> None:
    """Imprime por consola los pilares del proceso de auditoría."""
    print("Los 3 pilares clave de un proceso de auditoría:")
    print("\n".join(pilares))


def registrar_ejecucion(ruta: str) -> None:
    """Añade al log la marca de tiempo de la ejecución actual.

    Lanza OSError si no se puede escribir en el archivo.
    """
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"Ejecución: {datetime.now():%Y-%m-%d %H:%M:%S}\n")


def main() -> int:
    """Punto de entrada. Devuelve el código de salida del proceso."""
    mostrar_pilares(PILARES)
    try:
        registrar_ejecucion(RUTA_LOG)
    except OSError as e:
        print(f"No se pudo escribir en {RUTA_LOG}: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
