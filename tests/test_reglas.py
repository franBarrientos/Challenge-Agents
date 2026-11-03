import unittest

from reservas import (
    ErrorReserva, buscar_conflictos, cargar_inventario, se_superponen,
    validar_intervalo, validar_solicitante, validar_unidad,
)


class ReglasTests(unittest.TestCase):
    def test_inventario_de_la_consigna(self):
        inventario = cargar_inventario()
        self.assertEqual(set(inventario), {"MIC-01", "MIC-02", "OSC-01", "MUL-01", "FUE-01"})
        self.assertEqual(inventario["MIC-01"], "Microscopio digital")

    def test_superposiciones_parciales_contenidas_e_identicas(self):
        for inicio, fin in [(9, 11), (11, 13), (10, 12), (11, 12), (9, 13)]:
            with self.subTest(inicio=inicio, fin=fin):
                self.assertTrue(se_superponen(inicio, fin, 10, 12))

    def test_consecutivas_y_separadas_en_ambos_sentidos(self):
        for inicio, fin in [(8, 9), (9, 10), (12, 13), (13, 14)]:
            with self.subTest(inicio=inicio, fin=fin):
                self.assertFalse(se_superponen(inicio, fin, 10, 12))

    def test_conflictos_solo_activa_misma_unidad(self):
        reservas = [
            dict(unidad="MIC-01", inicio=10, fin=12, estado="CANCELADA"),
            dict(unidad="MIC-02", inicio=10, fin=12, estado="ACTIVA"),
            dict(unidad="MIC-01", inicio=12, fin=13, estado="ACTIVA"),
        ]
        self.assertEqual(buscar_conflictos(reservas, "MIC-01", 10, 12), [])
        self.assertEqual(buscar_conflictos(reservas, "MIC-02", 10, 12), [reservas[1]])

    def test_solicitante_vacio_y_espacios(self):
        for nombre in ("", "   ", "\t\n", None, 123):
            with self.subTest(nombre=nombre), self.assertRaises(ErrorReserva):
                validar_solicitante(nombre)
        self.assertEqual(validar_solicitante(" Ana Demo "), "Ana Demo")

    def test_unidad_desconocida(self):
        for unidad in ("NO-EXISTE", "mic-01", None, []):
            with self.subTest(unidad=unidad), self.assertRaises(ErrorReserva):
                validar_unidad(unidad, cargar_inventario())

    def test_fecha_invalida_o_formato_incorrecto(self):
        for valor in ("2026-02-30 10:00", "2026-11-03 24:00", "2026-11-03 10:60",
                      "2026-1-03 10:00", "03/11/2026 10:00", "2026-11-03T10:00", "", None):
            for inicio, fin in [(valor, "2026-11-03 11:00"), ("2026-11-03 10:00", valor)]:
                with self.subTest(inicio=inicio, fin=fin), self.assertRaises(ErrorReserva):
                    validar_intervalo(inicio, fin)

    def test_inicio_igual_o_posterior_al_fin(self):
        for fin in ("2026-11-03 10:00", "2026-11-03 09:00"):
            with self.subTest(fin=fin), self.assertRaises(ErrorReserva):
                validar_intervalo("2026-11-03 10:00", fin)

    def test_fechas_pasadas_bisiestas_y_cambio_de_dia(self):
        for inicio, fin in [("2024-02-29 23:00", "2024-03-01 01:00"),
                            ("2000-01-01 10:00", "2000-01-01 11:00")]:
            with self.subTest(inicio=inicio):
                a, b = validar_intervalo(inicio, fin)
                self.assertLess(a, b)


if __name__ == "__main__":
    unittest.main()
