"""SQLite local. Abrir conserva datos; cancelar actualiza, nunca elimina."""

import sqlite3
from pathlib import Path

BASE_PREDETERMINADA = Path(__file__).resolve().parent / "data" / "reservas.db"


class Repositorio:
    def __init__(self, ruta=BASE_PREDETERMINADA):
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.conexion = sqlite3.connect(str(ruta))
        self.conexion.row_factory = sqlite3.Row
        self.conexion.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unidad TEXT NOT NULL,
                solicitante TEXT NOT NULL,
                inicio TEXT NOT NULL,
                fin TEXT NOT NULL,
                estado TEXT NOT NULL CHECK (estado IN ('ACTIVA', 'CANCELADA')),
                CHECK (inicio < fin)
            )
        """)
        self.conexion.commit()

    def listar(self):
        return [dict(fila) for fila in self.conexion.execute("SELECT * FROM reservas ORDER BY id")]

    def obtener(self, identificador):
        fila = self.conexion.execute("SELECT * FROM reservas WHERE id = ?", (identificador,)).fetchone()
        return dict(fila) if fila else None

    def insertar(self, unidad, solicitante, inicio, fin):
        with self.conexion:
            cursor = self.conexion.execute(
                "INSERT INTO reservas (unidad, solicitante, inicio, fin, estado) VALUES (?, ?, ?, ?, 'ACTIVA')",
                (unidad, solicitante, inicio, fin),
            )
        return self.obtener(cursor.lastrowid)

    def cancelar(self, identificador):
        with self.conexion:
            self.conexion.execute("UPDATE reservas SET estado = 'CANCELADA' WHERE id = ?", (identificador,))
        return self.obtener(identificador)

    def reiniciar(self):
        """Solo para la opción explícita y confirmada de reinicio de datos."""
        with self.conexion:
            self.conexion.execute("DELETE FROM reservas")

    def cerrar(self):
        self.conexion.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cerrar()
