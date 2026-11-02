"""Pruebas de resumen_expediente. Nunca tocan el log.txt real: usan tmp_path."""

import re
from pathlib import Path

import pytest

import resumen_expediente as re_exp

PATRON_LINEA = r"Ejecución: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"


@pytest.fixture
def ruta_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirige RUTA_LOG a un archivo temporal."""
    ruta = tmp_path / "log.txt"
    monkeypatch.setattr(re_exp, "RUTA_LOG", str(ruta))
    return ruta


def test_construir_linea_sin_mensaje() -> None:
    assert re.fullmatch(PATRON_LINEA, re_exp.construir_linea_log())


def test_construir_linea_con_mensaje() -> None:
    linea = re_exp.construir_linea_log("revisión trimestral")
    assert re.fullmatch(PATRON_LINEA + r" - revisión trimestral", linea)


def test_construir_linea_colapsa_saltos_de_linea() -> None:
    linea = re_exp.construir_linea_log("uno\ndos\r\n  tres")
    assert "\n" not in linea and "\r" not in linea
    assert linea.endswith(" - uno dos tres")


def test_construir_linea_ignora_mensaje_vacio() -> None:
    assert re.fullmatch(PATRON_LINEA, re_exp.construir_linea_log(""))


def test_registrar_ejecucion_anade_y_devuelve_la_linea(tmp_path: Path) -> None:
    ruta = tmp_path / "log.txt"
    primera = re_exp.registrar_ejecucion(str(ruta), "a")
    segunda = re_exp.registrar_ejecucion(str(ruta))
    assert ruta.read_text(encoding="utf-8").splitlines() == [primera, segunda]


def test_registrar_ejecucion_propaga_oserror(tmp_path: Path) -> None:
    ruta_invalida = tmp_path / "no_existe" / "log.txt"
    with pytest.raises(OSError):
        re_exp.registrar_ejecucion(str(ruta_invalida))


def test_mostrar_pilares(capsys: pytest.CaptureFixture[str]) -> None:
    re_exp.mostrar_pilares(["uno", "dos"])
    assert capsys.readouterr().out.splitlines()[-2:] == ["uno", "dos"]


def test_parsear_argumentos_por_defecto() -> None:
    args = re_exp.parsear_argumentos([])
    assert args.verbose is False
    assert args.mensaje is None


def test_parsear_argumentos_opciones() -> None:
    args = re_exp.parsear_argumentos(["-v", "-m", "hola"])
    assert args.verbose is True
    assert args.mensaje == "hola"


def test_parsear_argumentos_invalido_sale_con_codigo_2() -> None:
    with pytest.raises(SystemExit) as info:
        re_exp.parsear_argumentos(["--foo"])
    assert info.value.code == 2


def test_main_sin_argumentos(
    ruta_log: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert re_exp.main([]) == 0
    salida = capsys.readouterr().out
    assert all(p in salida for p in re_exp.PILARES)
    assert "Registrado en" not in salida
    assert re.fullmatch(PATRON_LINEA, ruta_log.read_text(encoding="utf-8").strip())


def test_main_verbose_con_mensaje(
    ruta_log: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert re_exp.main(["-v", "-m", "prueba"]) == 0
    linea = ruta_log.read_text(encoding="utf-8").strip()
    assert linea.endswith(" - prueba")
    assert f"Registrado en {ruta_log}: {linea}" in capsys.readouterr().out


def test_main_devuelve_1_si_falla_la_escritura(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    ruta_invalida = tmp_path / "no_existe" / "log.txt"
    monkeypatch.setattr(re_exp, "RUTA_LOG", str(ruta_invalida))
    assert re_exp.main(["-v"]) == 1
    captura = capsys.readouterr()
    assert "No se pudo escribir en" in captura.err
    assert "Registrado en" not in captura.out
