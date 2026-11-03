# Especificación v1 — ReservaLab

Fecha: 2026-11-03. Aprobación del alcance: el autor respondió «ok implementalo»
a la propuesta de una aplicación Python por consola con SQLite y pruebas estándar.

## Problema y alcance

El laboratorio necesita evitar reservas superpuestas y liberar horarios al cancelar,
conservando su historial. Aplicación local de un solo proceso y operador a la vez.
Incluye inventario precargado de cinco unidades, consulta por unidad e intervalo,
creación, cancelación, historial y persistencia. No incluye administración de inventario,
edición de reservas, web, usuarios, pagos, notificaciones ni despliegue.

## Inventario

| ID | Equipo |
|---|---|
| MIC-01 | Microscopio digital |
| MIC-02 | Microscopio digital |
| OSC-01 | Osciloscopio |
| MUL-01 | Multímetro |
| FUE-01 | Fuente de alimentación |

## Reglas y aceptación

| ID | Requisito y resultado verificable |
|---|---|
| CA01 | Leer el inventario JSON y mostrar las cinco unidades físicas diferenciadas por ID. |
| CA02 | Crear una reserva válida con ID único, unidad, solicitante, inicio, fin y estado ACTIVA. |
| CA03 | Rechazar cualquier superposición entre reservas activas de la misma unidad, incluyendo contención e igualdad. |
| CA04 | Permitir 10:00-11:00 seguido por 11:00-12:00, también en orden inverso de creación. |
| CA05 | Permitir reservas simultáneas para unidades distintas. |
| CA06 | Rechazar unidad desconocida, solicitante vacío o solo espacios, fechas imposibles o mal formadas e inicio mayor o igual al fin. |
| CA07 | Consulta y creación comparten validación de unidad, intervalo y búsqueda de conflictos. |
| CA08 | Cancelar conserva ID y todos los datos originales, cambia estado y libera disponibilidad. |
| CA09 | Informar error al cancelar ID inexistente, inválido o ya cancelado, sin modificar registros. |
| CA10 | Conservar reservas activas y canceladas tras detener y reiniciar el proceso sin borrar datos. |
| CA11 | Mostrar historial de ambos estados, ordenado por ID de creación. |
| CA12 | El menú informa errores y permite continuar; salir o fin de entrada cierra la conexión. |

## Supuestos explícitos

- Fechas en formato exacto `AAAA-MM-DD HH:MM`, precisión de minutos.
- Todos los horarios representan UTC-3 fijo; no se convierten según el sistema operativo.
- Se permiten fechas pasadas para registrar y reproducir ejemplos; no se compara con el reloj.
- Sin límite de duración o anticipación, dentro del rango de fechas admitido por Python.
- Intervalos semiabiertos: hay conflicto si `nuevo_inicio < fin_existente` y
  `inicio_existente < nuevo_fin`, solo para la misma unidad y estado ACTIVA.
- Una unidad por reserva. Solicitante ficticio; se recortan espacios extremos.
- Cancelar no elimina datos. No se permite cancelar dos veces.
- SQLite local, inventario JSON versionado. Sin garantías de uso concurrente.
- Reinicio de datos únicamente mediante comando explícito con confirmación textual;
  borra reservas activas y canceladas, pero no modifica inventario.

## Plan de verificación y evolución

Pruebas automáticas de reglas, servicio, persistencia en procesos separados y menú.
Ejecución reproducible con `python3 -m unittest discover -s tests -v`.
Recorrido manual reproducible en `docs/verificacion-manual.md` al finalizar.
Registrar versión inicial en Git antes del código. Cambios posteriores a este documento
deben explicar motivo y quedar recuperables en `git log -p -- docs/especificacion.md`.
