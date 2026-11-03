# Revisión humana antes de entregar

**Estado: pendiente.** La siguiente guía no afirma que el autor haya realizado los pasos.
Las pruebas automáticas y el recorrido de `evidencia/recorrido.txt` fueron ejecutados por el agente.

Desde la carpeta del proyecto, usar una base separada:

```bash
python3 main.py --db data/revision.db
```

Usar una base vacía. Si ya tiene datos, elegir otro nombre de archivo; no hace falta borrar nada.
Todas las fechas del recorrido son `2026-11-03`; las fechas pasadas están permitidas.

| Paso | Acción | Resultado esperado | Observado por el autor |
|---|---|---|---|
| 1 | Opción 1 | Cinco unidades, incluidos MIC-01 y MIC-02 | Pendiente |
| 2 | Opción 3; equipo 1; Ana Demo; 10:00–11:00 | Reserva #1 ACTIVA | Pendiente |
| 3 | Opción 3; equipo 1; Beto Demo; 10:30–11:30 | Rechazo por horario ocupado | Pendiente |
| 4 | Opción 3; equipo 1; Beto Demo; 11:00–12:00 | Reserva #2 ACTIVA | Pendiente |
| 5 | Opción 3; equipo 2; Carla Demo; 10:00–11:00 | Reserva #3 ACTIVA | Pendiente |
| 6 | Opción 3 con solicitante solo espacios, o fin igual al inicio | Error y ninguna reserva adicional | Pendiente |
| 7 | Opción 4; ID 1 | Reserva #1 CANCELADA | Pendiente |
| 8 | Opción 2; equipo 1; 10:00–11:00 | DISPONIBLE | Pendiente |
| 9 | Opción 5 | #1 CANCELADA, #2 y #3 ACTIVAS | Pendiente |
| 10 | Opción 0; volver a ejecutar el mismo comando; opción 5 | Mismos IDs, datos y estados | Pendiente |

Ingresar fechas completas, por ejemplo `2026-11-03 10:00`.
Ejecutar también `python3 -m unittest discover -s tests -v` y verificar que muestre
`Ran 25 tests` y `OK`, sin confundir una compilación o importación exitosa con pruebas ejecutadas.

## Cierre de los episodios

Luego de revisar, completar en `decisiones.md` para cada episodio:

- Decisión: aceptar / corregir / rechazar.
- Motivo y qué se comprobó realmente (lectura de evidencia, ejecución de pruebas, uso manual).
- Fecha y referencia al resultado o archivo revisado.

Episodio 1: revisar reglas y pasos 1–6. Episodio 2: cancelación y persistencia, pasos 7–10.
Episodio 3: facilidad de uso, manejo de errores y ejecución del programa/pruebas.
Si solo se leyó la evidencia del agente, indicarlo sin afirmar que se ejecutó el programa.
