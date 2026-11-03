import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from persistencia import Repositorio

RAIZ = Path(__file__).resolve().parents[1]


class MenuTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.db = Path(self.temporal.name) / "reservas.db"

    def ejecutar(self, entradas, *opciones):
        proceso = subprocess.run(
            [sys.executable, str(RAIZ / "main.py"), "--db", str(self.db), *opciones],
            input=entradas, capture_output=True, text=True, encoding="utf-8",
            cwd=self.temporal.name, timeout=10,
        )
        self.assertEqual(proceso.returncode, 0, proceso.stderr + proceso.stdout)
        self.assertEqual(proceso.stderr, "")
        return proceso.stdout

    def reservar(self):
        return "3\n1\nAna Demo\n2026-11-03 10:00\n2026-11-03 11:00\n"

    def test_recorrido_completo_y_reinicio(self):
        salida = self.ejecutar(
            "1\n" + self.reservar()
            + "2\n1\n2026-11-03 10:00\n2026-11-03 11:00\n"
            + self.reservar()
            + "4\n1\n2\n1\n2026-11-03 10:00\n2026-11-03 11:00\n"
            + self.reservar() + "5\n0\n"
        )
        self.assertIn("FUE-01", salida)
        self.assertEqual(salida.count("Reserva creada."), 2)
        self.assertIn("OCUPADA", salida)
        self.assertIn("ya está reservada", salida)
        self.assertIn("DISPONIBLE", salida)
        self.assertIn("horario liberado", salida)
        reinicio = self.ejecutar("5\n0\n")
        self.assertIn("#1 | MIC-01 | Ana Demo | 2026-11-03 10:00 → 2026-11-03 11:00 | CANCELADA", reinicio)
        self.assertIn("#2 | MIC-01 | Ana Demo | 2026-11-03 10:00 → 2026-11-03 11:00 | ACTIVA", reinicio)

    def test_opciones_invalidas_no_cierran_el_programa(self):
        salida = self.ejecutar("99\n2\n0\n2\n6\n2\nabc\n4\nabc\n4\n999\n5\n0\n")
        self.assertIn("Opción inválida", salida)
        self.assertEqual(salida.count("fuera de rango"), 2)
        self.assertIn("número de equipo válido", salida)
        self.assertIn("entero positivo", salida)
        self.assertIn("No existe una reserva", salida)
        self.assertIn("No hay reservas", salida)

    def test_fecha_invalida_y_solicitante_vacio_no_crean_reservas(self):
        salida = self.ejecutar(
            "3\n1\nAna Demo\nfecha\n2026-11-03 11:00\n"
            "3\n1\n   \n2026-11-03 10:00\n2026-11-03 11:00\n5\n0\n"
        )
        self.assertIn("Usá el formato", salida)
        self.assertIn("solicitante no puede estar vacío", salida)
        self.assertIn("No hay reservas", salida)

    def test_fin_de_entrada_conserva_reservas(self):
        salida = self.ejecutar(self.reservar())
        self.assertIn("Los cambios confirmados quedan guardados", salida)
        self.assertIn("ACTIVA", self.ejecutar("5\n0\n"))

    def test_reinicio_cancelado_conserva_reservas(self):
        self.ejecutar(self.reservar() + "0\n")
        self.assertIn("Reinicio cancelado", self.ejecutar("NO\n", "--reiniciar-datos"))
        self.assertIn("ACTIVA", self.ejecutar("5\n0\n"))

    def test_reinicio_confirmado_borra_ambos_estados(self):
        self.ejecutar(self.reservar() + "4\n1\n" + self.reservar() + "0\n")
        salida = self.ejecutar("BORRAR\n", "--reiniciar-datos")
        self.assertIn("Inventario conservado", salida)
        with Repositorio(self.db) as repo:
            self.assertEqual(repo.listar(), [])
        self.assertIn("MIC-01", self.ejecutar("1\n0\n"))

    def test_base_no_escribible_informa_error_sin_traceback(self):
        proceso = subprocess.run(
            [sys.executable, str(RAIZ / "main.py"), "--db", self.temporal.name],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(proceso.returncode, 1)
        self.assertIn("No se pudo completar", proceso.stderr)
        self.assertNotIn("Traceback", proceso.stderr)


if __name__ == "__main__":
    unittest.main()
