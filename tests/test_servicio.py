import tempfile
import unittest
from pathlib import Path

from persistencia import Repositorio
from reservas import ErrorReserva, ServicioReservas


class ServicioTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.repo = Repositorio(Path(self.temporal.name) / "reservas.db")
        self.addCleanup(self.repo.cerrar)
        self.servicio = ServicioReservas(self.repo)

    def crear(self, unidad="MIC-01", nombre="Ana Demo", inicio="2026-11-03 10:00", fin="2026-11-03 11:00"):
        return self.servicio.crear(unidad, nombre, inicio, fin)

    def test_creacion_valida_con_identificadores_distintos(self):
        primera = self.crear(nombre=" Ana Demo ")
        segunda = self.crear(unidad="MIC-02")
        self.assertEqual(primera, dict(id=1, unidad="MIC-01", solicitante="Ana Demo",
                                      inicio="2026-11-03 10:00", fin="2026-11-03 11:00", estado="ACTIVA"))
        self.assertNotEqual(primera["id"], segunda["id"])

    def test_rechazo_de_superposiciones_no_guarda_registros(self):
        self.crear()
        for inicio, fin in [("09:30", "10:30"), ("10:30", "11:30"), ("09:00", "12:00"),
                            ("10:10", "10:50"), ("10:00", "11:00")]:
            with self.subTest(inicio=inicio, fin=fin):
                a, b = "2026-11-03 " + inicio, "2026-11-03 " + fin
                self.assertFalse(self.servicio.disponible("MIC-01", a, b))
                with self.assertRaisesRegex(ErrorReserva, "reservada"):
                    self.crear(inicio=a, fin=b)
        self.assertEqual(len(self.servicio.historial()), 1)

    def test_consecutivas_antes_y_despues(self):
        self.crear()
        for inicio, fin in [("09:00", "10:00"), ("11:00", "12:00")]:
            a, b = "2026-11-03 " + inicio, "2026-11-03 " + fin
            self.assertTrue(self.servicio.disponible("MIC-01", a, b))
            self.crear(inicio=a, fin=b)
        self.assertEqual(len(self.servicio.historial()), 3)

    def test_unidades_distintas_simultaneas(self):
        self.crear()
        self.assertTrue(self.servicio.disponible("MIC-02", "2026-11-03 10:00", "2026-11-03 11:00"))
        self.crear(unidad="MIC-02")
        self.assertEqual(len(self.servicio.historial()), 2)

    def test_cancelar_conserva_datos_y_libera(self):
        original = self.crear()
        cancelada = self.servicio.cancelar(original["id"])
        self.assertEqual(cancelada, dict(original, estado="CANCELADA"))
        self.assertTrue(self.servicio.disponible("MIC-01", original["inicio"], original["fin"]))
        nueva = self.crear()
        self.assertEqual(self.servicio.historial(), [cancelada, nueva])

    def test_cancelaciones_invalidas_no_modifican_historial(self):
        reserva = self.crear()
        for identificador in (0, -1, "1", True, 999, 10**100):
            with self.subTest(identificador=identificador), self.assertRaises(ErrorReserva):
                self.servicio.cancelar(identificador)
        self.assertEqual(self.servicio.historial(), [reserva])
        self.servicio.cancelar(reserva["id"])
        with self.assertRaisesRegex(ErrorReserva, "ya está cancelada"):
            self.servicio.cancelar(reserva["id"])

    def test_consulta_y_creacion_rechazan_mismas_entradas_invalidas(self):
        for unidad, inicio, fin in [
            ("NO", "2026-11-03 10:00", "2026-11-03 11:00"),
            ("MIC-01", "2026-02-30 10:00", "2026-11-03 11:00"),
            ("MIC-01", "2026-11-03 11:00", "2026-11-03 10:00"),
            ("MIC-01", "2026-11-03 10:00", "2026-11-03 10:00"),
        ]:
            with self.subTest(unidad=unidad, inicio=inicio):
                with self.assertRaises(ErrorReserva):
                    self.servicio.disponible(unidad, inicio, fin)
                with self.assertRaises(ErrorReserva):
                    self.crear(unidad=unidad, inicio=inicio, fin=fin)
        for nombre in ("", "   "):
            with self.assertRaises(ErrorReserva):
                self.crear(nombre=nombre)
        self.assertEqual(self.servicio.historial(), [])

    def test_solicitante_con_comillas_se_guarda_como_dato(self):
        nombre = "Demo O'Connor; DROP TABLE reservas;"
        self.crear(nombre=nombre)
        self.assertEqual(self.servicio.historial()[0]["solicitante"], nombre)


if __name__ == "__main__":
    unittest.main()
