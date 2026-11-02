# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Directrices del Proyecto

## Comandos Frecuentes

- Ejecutar script principal: `python resumen_expediente.py`
- Ver logs: `log.txt` en la raíz del proyecto (el script lo crea/amplía en modo `append`).

No hay dependencias externas, tests ni configuración de lint/build: el proyecto es un único script que usa solo la biblioteca estándar.

## Arquitectura

- `resumen_expediente.py` es el único módulo. Imprime por consola los 3 pilares de un proceso de auditoría (constante `PILARES`) y registra cada ejecución con marca de tiempo en `log.txt`.
- La ruta de `log.txt` es relativa al directorio de trabajo, así que el log se genera donde se lance el comando; conviene ejecutarlo desde la raíz del proyecto.

## Estilo y Normas de Código

- Python 3.10+ estrictamente tipado.
- Manejo explícito de excepciones (nada de bloques `except:` vacíos).
- Comentarios y documentación técnica en castellano.
