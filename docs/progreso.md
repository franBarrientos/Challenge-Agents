# Progreso

## 2026-11-03 — Preparación

- Revisada la consigna y los ejemplos proporcionados; se implementa una solución propia.
- Alcance aceptado por el autor: consola Python, SQLite, pruebas y documentación.
- Repositorio remoto consultado con `git ls-remote`: sin referencias (vacío).
- Entorno local: macOS; `python3 --version`: Python 3.9.6;
  `git --version`: git version 2.39.5 (Apple Git-154).
- Se fijaron especificación e instrucciones antes de implementar.
- Próximos episodios: 1) reglas y pruebas, 2) persistencia y servicio,
  3) menú, integración y documentación.
- La aprobación del alcance no equivale a verificar los resultados posteriores.

## Episodio 1 — Reglas

- Implementados inventario y reglas en `reservas.py`; 9 pruebas, con subcasos.
- Comando: `python3 -m unittest discover -s tests -v` (Python 3.9.6).
- Resultado: 9 pruebas ejecutadas, OK. Salida: `evidencia/episodio-1.txt`.
- Verificados extremos consecutivos, contención, igualdad, estados, unidades y fechas.
- No hubo fallos en esta ejecución. Revisión humana del episodio: pendiente.
