# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos Frecuentes

- Ejecutar script principal: `python resumen_expediente.py`
- Opciones: `-v/--verbose` (muestra por consola la línea registrada) y `-m/--mensaje TEXTO` (la añade a la línea del log). Ejemplo: `python resumen_expediente.py -v -m "revisión trimestral"`.
- Ver logs: `log.txt` en la raíz del proyecto (el script lo crea/amplía en modo `append`).

- Tests (requiere `python -m pip install pytest`): `python -m pytest`
- Un solo test: `python -m pytest tests/test_resumen_expediente.py::test_main_verbose_con_mensaje`

El script usa solo la biblioteca estándar; `pytest` es únicamente dependencia de desarrollo. No hay configuración de lint/build. Los tests redirigen el log a `tmp_path` (fixture `ruta_log`), así que nunca tocan el `log.txt` real; `tests/conftest.py` añade la raíz al `sys.path` para importar el módulo.

## Arquitectura

- `resumen_expediente.py` es el único módulo. Imprime por consola los 3 pilares de un proceso de auditoría (constante `PILARES`) y registra cada ejecución con marca de tiempo en `log.txt`.
- La ruta de `log.txt` es relativa al directorio de trabajo, así que el log se genera donde se lance el comando; conviene ejecutarlo desde la raíz del proyecto.
- Flujo de errores: `main()` devuelve el código de salida del proceso (`sys.exit(main())`). `registrar_ejecucion` deja propagar `OSError`; `main()` lo captura, escribe el mensaje en stderr y devuelve `1`. Los cambios deben mantener este patrón: las funciones auxiliares lanzan, solo `main()` decide el código de salida.

## Estilo y Normas de Código

- Python 3.10+ estrictamente tipado.
- Manejo explícito de excepciones (nada de bloques `except:` vacíos).
- Comentarios y documentación técnica en castellano.
