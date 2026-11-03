import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


class PersistenciaTests(unittest.TestCase):
    def test_activas_y_canceladas_sobreviven_a_proceso_nuevo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = str(Path(carpeta) / "reservas.db")
            crear = '''
import json, sys
from persistencia import Repositorio
from reservas import ServicioReservas
with Repositorio(sys.argv[1]) as repo:
    s = ServicioReservas(repo)
    r = s.crear("MIC-01", "Ana Demo", "2026-11-03 10:00", "2026-11-03 11:00")
    s.crear("MIC-02", "Beto Demo", "2026-11-03 10:00", "2026-11-03 11:00")
    s.cancelar(r["id"])
    print(json.dumps(s.historial()))
'''
            leer = '''
import json, sys
from persistencia import Repositorio
from reservas import ServicioReservas
with Repositorio(sys.argv[1]) as repo:
    s = ServicioReservas(repo)
    print(json.dumps(s.historial()))
    print(s.disponible("MIC-01", "2026-11-03 10:00", "2026-11-03 11:00"))
    print(s.disponible("MIC-02", "2026-11-03 10:00", "2026-11-03 11:00"))
'''
            anterior = subprocess.run([sys.executable, "-c", crear, ruta], cwd=RAIZ,
                                      capture_output=True, text=True, check=True, timeout=10)
            posterior = subprocess.run([sys.executable, "-c", leer, ruta], cwd=RAIZ,
                                       capture_output=True, text=True, check=True, timeout=10)
            lineas = posterior.stdout.splitlines()
            datos = json.loads(lineas[0])
            self.assertEqual(datos, json.loads(anterior.stdout))
            self.assertEqual([r["estado"] for r in datos], ["CANCELADA", "ACTIVA"])
            self.assertEqual(lineas[1:], ["True", "False"])


if __name__ == "__main__":
    unittest.main()
