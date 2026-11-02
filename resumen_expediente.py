import argparse
import sys
from collections.abc import Sequence
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


def parsear_argumentos(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Interpreta los argumentos de línea de comandos.

    Con argumentos inválidos, argparse termina el proceso con código 2.
    """
    parser = argparse.ArgumentParser(
        description="Muestra los 3 pilares de una auditoría y registra la ejecución."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="muestra por consola la línea que se escribe en el log",
    )
    parser.add_argument(
        "-m", "--mensaje", default=None, metavar="TEXTO",
        help="mensaje personalizado que se añade a la línea del log",
    )
    return parser.parse_args(argv)


def construir_linea_log(mensaje: str | None = None) -> str:
    """Construye la línea de log con marca de tiempo y mensaje opcional.

    Los saltos de línea del mensaje se sustituyen por espacios para que cada
    ejecución ocupe siempre una única línea.
    """
    linea = f"Ejecución: {datetime.now():%Y-%m-%d %H:%M:%S}"
    if mensaje:
        linea += f" - {' '.join(mensaje.split())}"
    return linea


def registrar_ejecucion(ruta: str, mensaje: str | None = None) -> str:
    """Añade al log la ejecución actual y devuelve la línea escrita.

    Lanza OSError si no se puede escribir en el archivo.
    """
    linea = construir_linea_log(mensaje)
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    return linea


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada. Devuelve el código de salida del proceso."""
    args = parsear_argumentos(argv)
    mostrar_pilares(PILARES)
    try:
        linea = registrar_ejecucion(RUTA_LOG, args.mensaje)
    except OSError as e:
        print(f"No se pudo escribir en {RUTA_LOG}: {e}", file=sys.stderr)
        return 1
    if args.verbose:
        print(f"Registrado en {RUTA_LOG}: {linea}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
