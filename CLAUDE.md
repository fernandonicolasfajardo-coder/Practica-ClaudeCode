# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos Frecuentes

- Ejecutar script principal: `python resumen_expediente.py`
- Opciones: `-v/--verbose` (muestra por consola la línea registrada) y `-m/--mensaje TEXTO` (la añade a la línea del log). Ejemplo: `python resumen_expediente.py -v -m "revisión trimestral"`.
- Ver logs: `log.txt` en la raíz del proyecto (el script lo crea/amplía en modo `append`).

- Tests (requiere `python -m pip install pytest`): `python -m pytest`
- Cobertura (requiere `python -m pip install pytest-cov`): `python -m pytest --cov=resumen_expediente --cov-report=term-missing --cov-fail-under=90`. El CI aplica el mismo umbral del 90 %; la única línea sin cubrir es la guarda `if __name__ == "__main__"`.
- Un solo test: `python -m pytest tests/test_resumen_expediente.py::test_main_verbose_con_mensaje`
- Lint (requiere `python -m pip install ruff`): `python -m ruff check .`
- Tipado estricto (requiere `python -m pip install mypy`): `python -m mypy --strict resumen_expediente.py tests/`

El script usa solo la biblioteca estándar; `pytest`, `ruff` y `mypy` son únicamente dependencias de desarrollo. No hay configuración de build. Los tests redirigen el log a `tmp_path` (fixture `ruta_log`), así que nunca tocan el `log.txt` real; `tests/conftest.py` añade la raíz al `sys.path` para importar el módulo.

## Arquitectura

- `resumen_expediente.py` es el único módulo. Imprime por consola los 3 pilares de un proceso de auditoría (constante `PILARES`) y registra cada ejecución con marca de tiempo en `log.txt`.
- La ruta de `log.txt` es relativa al directorio de trabajo, así que el log se genera donde se lance el comando; conviene ejecutarlo desde la raíz del proyecto.
- Flujo de errores: `main()` devuelve el código de salida del proceso (`sys.exit(main())`). `registrar_ejecucion` deja propagar `OSError`; `main()` lo captura, escribe el mensaje en stderr y devuelve `1`. Los cambios deben mantener este patrón: las funciones auxiliares lanzan, solo `main()` decide el código de salida.

## Estilo y Normas de Código

- Python 3.10+ estrictamente tipado.
- Manejo explícito de excepciones (nada de bloques `except:` vacíos).
- Comentarios y documentación técnica en castellano.

## graphify

El grafo de conocimiento del proyecto se genera en `graphify-out/` (ignorado por git, regenerable). Requiere `python -m pip install graphifyy`. Se invoca con `python -m graphify`, porque el ejecutable `graphify` no está en el `PATH`.

- Generar o actualizar el grafo (solo AST, sin coste de API): `python -m graphify update .`. Ejecutarlo tras modificar código.
- Si existe `graphify-out/graph.json`, consultar antes de hacer grep o leer código fuente: `python -m graphify query "<pregunta>"`, `python -m graphify path "<A>" "<B>"` para relaciones y `python -m graphify explain "<concepto>"` para un concepto concreto. Después, leer solo las líneas que el grafo haya localizado.
- Leer `graphify-out/GRAPH_REPORT.md` únicamente para una revisión amplia de la arquitectura.
- Los hooks `PreToolUse` de graphify viven en `.claude/settings.json`, que no se versiona porque contiene rutas absolutas de la máquina local. Se instalan con `python -m graphify claude install` y se retiran con `python -m graphify claude uninstall`.
