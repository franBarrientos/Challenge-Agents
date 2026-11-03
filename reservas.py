"""Reglas de ReservaLab. Los horarios representan UTC-3 fijo."""

import json
import re
from datetime import datetime
from pathlib import Path

FORMATO = "%Y-%m-%d %H:%M"
INVENTARIO = Path(__file__).resolve().parent / "data" / "inventario.json"


class ErrorReserva(ValueError):
    """Error de negocio que la interfaz puede mostrar al usuario."""


def cargar_inventario():
    with INVENTARIO.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def validar_unidad(unidad, inventario):
    if not isinstance(unidad, str) or unidad not in inventario:
        raise ErrorReserva("La unidad no existe en el inventario.")


def validar_solicitante(solicitante):
    if not isinstance(solicitante, str) or not solicitante.strip():
        raise ErrorReserva("El solicitante no puede estar vacío ni contener solo espacios.")
    return solicitante.strip()


def validar_intervalo(inicio, fin):
    fechas = []
    for valor in (inicio, fin):
        if not isinstance(valor, str) or not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", valor
        ):
            raise ErrorReserva("Usá el formato AAAA-MM-DD HH:MM.")
        try:
            fechas.append(datetime.strptime(valor, FORMATO))
        except ValueError:
            raise ErrorReserva("La fecha o la hora no es válida.") from None
    if fechas[0] >= fechas[1]:
        raise ErrorReserva("El inicio debe ser anterior al fin.")
    return tuple(fechas)


def se_superponen(inicio, fin, otro_inicio, otro_fin):
    """Intervalos [inicio, fin): los extremos consecutivos no se superponen."""
    return inicio < otro_fin and otro_inicio < fin


def buscar_conflictos(reservas, unidad, inicio, fin):
    return [
        reserva for reserva in reservas
        if reserva["unidad"] == unidad
        and reserva["estado"] == "ACTIVA"
        and se_superponen(inicio, fin, reserva["inicio"], reserva["fin"])
    ]


class ServicioReservas:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.inventario = cargar_inventario()

    def disponible(self, unidad, inicio, fin):
        validar_unidad(unidad, self.inventario)
        validar_intervalo(inicio, fin)
        # El formato fijo ordena las fechas cronológicamente también como texto.
        return not buscar_conflictos(self.repositorio.listar(), unidad, inicio, fin)

    def crear(self, unidad, solicitante, inicio, fin):
        solicitante = validar_solicitante(solicitante)
        if not self.disponible(unidad, inicio, fin):
            raise ErrorReserva("La unidad ya está reservada en ese horario.")
        return self.repositorio.insertar(unidad, solicitante, inicio, fin)

    def cancelar(self, identificador):
        if type(identificador) is not int or not 0 < identificador <= 9223372036854775807:
            raise ErrorReserva("El ID debe ser un entero positivo válido.")
        reserva = self.repositorio.obtener(identificador)
        if reserva is None:
            raise ErrorReserva("No existe una reserva con ese ID.")
        if reserva["estado"] == "CANCELADA":
            raise ErrorReserva("La reserva ya está cancelada.")
        return self.repositorio.cancelar(identificador)

    def historial(self):
        return self.repositorio.listar()
