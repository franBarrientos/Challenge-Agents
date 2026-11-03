"""Menú de ReservaLab. Ejecutar con python3 main.py."""

import argparse
import sqlite3
import sys

from persistencia import BASE_PREDETERMINADA, Repositorio
from reservas import ErrorReserva, ServicioReservas

MENU = """
1. Ver equipos
2. Consultar disponibilidad
3. Crear reserva
4. Cancelar reserva
5. Ver historial
0. Salir
"""


def mostrar_equipos(inventario):
    for numero, (unidad, equipo) in enumerate(inventario.items(), 1):
        print("{}. {} — {}".format(numero, unidad, equipo))


def elegir_unidad(inventario):
    mostrar_equipos(inventario)
    try:
        numero = int(input("Número de equipo: "))
    except ValueError:
        raise ErrorReserva("Ingresá un número de equipo válido.") from None
    unidades = list(inventario)
    if not 1 <= numero <= len(unidades):
        raise ErrorReserva("El número de equipo está fuera de rango.")
    return unidades[numero - 1]


def pedir_intervalo():
    print("Formato: AAAA-MM-DD HH:MM. Horario UTC-3 fijo.")
    inicio = input("Inicio: ").strip()
    fin = input("Fin: ").strip()
    return inicio, fin


def mostrar_reserva(reserva):
    print("#{id} | {unidad} | {solicitante} | {inicio} → {fin} | {estado}".format(**reserva))


def ejecutar_menu(servicio):
    while True:
        print(MENU)
        opcion = input("Elegí una opción: ").strip()
        try:
            if opcion == "0":
                return
            if opcion == "1":
                mostrar_equipos(servicio.inventario)
            elif opcion in ("2", "3"):
                unidad = elegir_unidad(servicio.inventario)
                solicitante = input("Solicitante ficticio: ") if opcion == "3" else None
                inicio, fin = pedir_intervalo()
                if opcion == "2":
                    libre = servicio.disponible(unidad, inicio, fin)
                    print("DISPONIBLE" if libre else "OCUPADA")
                else:
                    reserva = servicio.crear(unidad, solicitante, inicio, fin)
                    print("Reserva creada.")
                    mostrar_reserva(reserva)
            elif opcion == "4":
                try:
                    identificador = int(input("ID de reserva a cancelar: "))
                except ValueError:
                    raise ErrorReserva("El ID debe ser un número entero positivo.") from None
                mostrar_reserva(servicio.cancelar(identificador))
                print("Reserva cancelada; horario liberado.")
            elif opcion == "5":
                historial = servicio.historial()
                if not historial:
                    print("No hay reservas registradas.")
                for reserva in historial:
                    mostrar_reserva(reserva)
            else:
                print("Opción inválida. Elegí un número entre 0 y 5.")
        except ErrorReserva as error:
            print("Error: {}".format(error))


def main():
    parser = argparse.ArgumentParser(description="ReservaLab — reservas locales de laboratorio")
    parser.add_argument("--db", default=str(BASE_PREDETERMINADA), help="Ruta del archivo SQLite")
    parser.add_argument("--reiniciar-datos", action="store_true", help="Borrar todas las reservas con confirmación")
    args = parser.parse_args()
    try:
        with Repositorio(args.db) as repositorio:
            print("ReservaLab | Horarios UTC-3 | Base: {}".format(args.db))
            if args.reiniciar_datos:
                print("ATENCIÓN: se borrarán TODAS las reservas, activas y canceladas.")
                if input("Escribí BORRAR para confirmar: ") != "BORRAR":
                    print("Reinicio cancelado. Los datos se conservan.")
                    return 0
                repositorio.reiniciar()
                print("Reservas eliminadas. Inventario conservado.")
                return 0
            ejecutar_menu(ServicioReservas(repositorio))
    except (EOFError, KeyboardInterrupt):
        print("\nSalida. Los cambios confirmados quedan guardados.")
    except (OSError, sqlite3.Error, ValueError) as error:
        print("No se pudo completar la operación: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
