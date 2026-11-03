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


## Episodio 2 — Servicio y persistencia

- Agregados SQLite y servicio. Creación usa directamente la consulta de disponibilidad.
- Cancelación comprobada con comparación de todos los campos antes/después.
- Se iniciaron y terminaron dos procesos independientes contra una base temporal:
  el segundo recuperó exactamente el historial, con estados ACTIVA y CANCELADA.
- Comando: `python3 -m unittest discover -s tests -v` (Python 3.9.6).
- Resultado: 18 pruebas ejecutadas, OK. Salida: `evidencia/episodio-2.txt`.
- No hubo fallos en esta ejecución. Revisión humana del episodio: pendiente.

## Episodio 3 — Menú e integración

- Implementado menú numerado, ruta alternativa de base y reinicio explícito con confirmación.
- Comando: `python3 -m unittest discover -s tests -v` (Python 3.9.6).
- Resultado: 25 pruebas ejecutadas, OK. Salida: `evidencia/episodio-3.txt`.
- Recorrido adicional del programa mediante entrada estándar: tres reservas válidas,
  una superposición rechazada, cancelación, disponibilidad e historial tras reiniciar.
  Ambos procesos terminaron con código 0 y sin stderr; salida: `evidencia/recorrido.txt`.
- Documentados comandos, matriz de aceptación, preparación del agente y guía manual.
- No hubo fallos en esta ejecución. Revisión humana de los tres episodios: pendiente.

### Ajuste de evidencia antes del commit

`git diff --cached --check` detectó espacios finales en la versión de Python y en dos
prompts capturados. Se recortaron esos espacios de los archivos de evidencia y se
declaró esa normalización en el recorrido; no se cambió el código del programa.
La primera comprobación de clon local ocurrió antes de completar el commit del episodio 3,
por lo que verificó el episodio 2 (18 pruebas, OK); se conserva con su commit real
en `evidencia/clon-episodio-2.txt`. La entrega completa se verificará después del commit.
