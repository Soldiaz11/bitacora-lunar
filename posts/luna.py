"""Cálculo aproximado de la fase lunar y su dibujo en SVG."""
import math
from datetime import datetime, timezone

LUNA_NUEVA_REFERENCIA = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
MES_SINODICO = 29.530588853


def fase_actual(momento=None):
    """Devuelve la fase como número entre 0 (luna nueva) y 1."""
    momento = momento or datetime.now(timezone.utc)
    dias = (momento - LUNA_NUEVA_REFERENCIA).total_seconds() / 86400
    return (dias / MES_SINODICO) % 1


def nombre_fase(fase):
    tramos = [
        (0.03, "Luna nueva"),
        (0.22, "Luna creciente"),
        (0.28, "Cuarto creciente"),
        (0.47, "Gibosa creciente"),
        (0.53, "Luna llena"),
        (0.72, "Gibosa menguante"),
        (0.78, "Cuarto menguante"),
        (0.97, "Luna menguante"),
    ]
    for limite, nombre in tramos:
        if fase < limite:
            return nombre
    return "Luna nueva"


def fase_simple(fase):
    """Traduce la fase exacta a una de las cuatro opciones del modelo Post."""
    if fase < 0.06 or fase > 0.94:
        return "nueva"
    if fase < 0.44:
        return "creciente"
    if fase < 0.56:
        return "llena"
    return "menguante"


def camino_svg(fase, cx=100, cy=100, r=90):
    """Path SVG de la parte iluminada de la luna."""
    k = math.cos(2 * math.pi * fase)
    rx = abs(k) * r
    exterior = 1 if fase < 0.5 else 0
    terminador = exterior if k < 0 else 1 - exterior
    return (
        f"M{cx} {cy - r} A{r} {r} 0 0 {exterior} {cx} {cy + r} "
        f"A{rx:.2f} {r} 0 0 {terminador} {cx} {cy - r} Z"
    )


def luna_de_hoy():
    fase = fase_actual()
    return {
        "nombre": nombre_fase(fase),
        "iluminacion": round((1 - math.cos(2 * math.pi * fase)) / 2 * 100),
        "camino": camino_svg(fase),
        "simple": fase_simple(fase),
    }
