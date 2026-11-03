# ReservaLab · Challenge Agents

Sistema local de reservas de equipos de laboratorio. Python, SQLite y menú de consola,
sin paquetes externos. Trabajo individual de Fran Barrientos.

**Estado:** implementación y 25 pruebas automáticas ejecutadas por el agente.
La revisión humana de los tres episodios está pendiente; el registro no la da por realizada.

## 1. Especificación breve

El laboratorio necesita evitar reservas superpuestas y liberar horarios al cancelar,
sin perder el historial. Permite ver cinco equipos precargados, consultar disponibilidad,
crear y cancelar reservas, y consultar el historial persistente.

- Una unidad física por reserva, solicitante ficticio obligatorio, inicio anterior al fin.
- Reservas activas de una misma unidad no se superponen. Horarios consecutivos sí se permiten.
- Equipos diferentes pueden reservarse al mismo tiempo. Canceladas no bloquean.
- Cancelar conserva ID, unidad, solicitante y fechas. La consulta y la creación comparten reglas.
- Fechas: `AAAA-MM-DD HH:MM`, UTC-3 fijo, precisión de minutos; pasado permitido.
- Sin límite de duración ni anticipación. Un operador y proceso a la vez.

La [especificación](docs/especificacion.md) define los criterios CA01–CA12.
Se guardó antes del código en el commit `6537eae`; evolución:
`git log -p -- docs/especificacion.md`.

## 2. Solución

### Requisitos e instalación

Python 3.9 o superior y Git para clonar. Verificado en macOS con Python 3.9.6;
versiones exactas en [entorno](docs/evidencia/entorno.txt). No se necesita cuenta de IA,
conexión a internet para ejecutar, servidor de base de datos ni instalación con pip.
No hay dependencias externas ni archivos de bloqueo necesarios.

```bash
git clone https://github.com/franBarrientos/Challenge-Agents.git
cd Challenge-Agents
python3 main.py
```

En Windows, si el comando disponible es `py`, usar `py main.py` y
`py -m unittest discover -s tests -v`. Windows no se verificó en esta sesión.

### Uso

```text
1. Ver equipos
2. Consultar disponibilidad
3. Crear reserva
4. Cancelar reserva
5. Ver historial
0. Salir
```

El equipo se elige por número. El programa muestra el ID de cada reserva para cancelarla.
Ejemplo reproducido por el agente con una base temporal:

```text
Equipo: 1 (MIC-01)
Solicitante ficticio: Ana Demo
Inicio: 2026-11-03 10:00
Fin: 2026-11-03 11:00
Reserva creada.
#1 | MIC-01 | Ana Demo | 2026-11-03 10:00 → 2026-11-03 11:00 | ACTIVA
```

Una segunda reserva de MIC-01 en ese intervalo informa:
`Error: La unidad ya está reservada en ese horario.`
Tras cancelar la primera, la consulta muestra `DISPONIBLE` y el historial conserva `CANCELADA`.
Ver [recorrido ejecutado](docs/evidencia/recorrido.txt).

### Almacenamiento y reinicio

El inventario se lee de [data/inventario.json](data/inventario.json).
La base `data/reservas.db` se crea automáticamente al primer uso; los siguientes arranques
conservan sus registros. La ruta predeterminada se resuelve respecto al proyecto.
Las bases no se versionan. Para elegir otra base:

```bash
python3 main.py --db data/demo.db
```

**Reiniciar datos borra todas las reservas, activas y canceladas.** No modifica el inventario.
El programa exige escribir exactamente `BORRAR`; cualquier otra respuesta conserva los datos.
Los IDs anteriores no se reutilizan. Usar solo cuando se quiera vaciar esa base:

```bash
python3 main.py --db data/demo.db --reiniciar-datos
```

### Estructura y decisiones técnicas

```text
main.py                  Menú, argumentos y mensajes
reservas.py              Validaciones, conflictos y casos de uso
persistencia.py          SQLite y operaciones de almacenamiento
data/inventario.json      Cinco unidades de la consigna
tests/                   Reglas, servicio, reinicio y menú
AGENTS.md                Instrucciones realmente usadas por el agente
docs/                    Especificación, decisiones, progreso y evidencia
```

Python reduce los requisitos de instalación; SQLite guarda en un único archivo.
Tres módulos separan responsabilidades sin frameworks. Se usan consultas SQL parametrizadas.
Las decisiones y sus alternativas están en [decisiones](docs/decisiones.md).

### Pruebas y limitaciones

Desde la carpeta del proyecto:

```bash
python3 -m unittest discover -s tests -v
```

Resultado registrado: **25 tests, OK**; [salida completa](docs/evidencia/episodio-3.txt).
También se verificaron las 25 pruebas desde un [clon limpio local](docs/evidencia/clon-limpio.txt).
Las pruebas usan bases temporales. La persistencia se comprueba cerrando un proceso y
abriendo otro, y también reiniciando la aplicación del menú.
La [matriz](docs/verificacion.md) conecta requisitos con pruebas.

Pendientes y límites: revisión humana, ejecución en otros sistemas operativos, uso concurrente,
cambios de huso horario. No se implementan edición de reservas, autenticación, notificaciones,
web ni escalabilidad. Se recorre el historial en memoria para buscar conflictos, adecuado
para este ejercicio pequeño. No se garantiza exclusión entre dos procesos simultáneos.

## 3. Preparación del agente

Se utilizó el agente de programación del entorno Codex de escritorio, con acceso real a
archivos y terminal. El agente editó, ejecutó pruebas y creó commits; no se copió código
de una respuesta de chat. Se eligió el entorno ya disponible para trabajar sobre el repositorio.

Las instrucciones están en [AGENTS.md](AGENTS.md). Documentación del entorno, datos no visibles,
contexto, permisos y adaptación comprobada en [preparación](docs/preparacion-agente.md).
El progreso se conserva en [docs/progreso.md](docs/progreso.md).

Adaptaciones concretas: permitir límites consecutivos, cancelar con UPDATE y probar
reinicios con bases temporales. Sus resultados están registrados en los tres episodios.

## 4. Registro de decisiones y delegación

El autor aceptó el alcance y autorizó implementar y subir el proyecto. El trabajo del agente
se dividió en tres episodios reales bajo esa autorización:

| Episodio | Resultado del agente | Evidencia | Decisión humana |
|---|---|---|---|
| 1. Reglas e inventario | 9 pruebas, OK | [Registro](docs/decisiones.md#episodio-1--reglas-e-inventario) | Pendiente |
| 2. Persistencia y cancelación | 18 pruebas, OK | [Registro](docs/decisiones.md#episodio-2--persistencia-y-cancelación) | Pendiente |
| 3. Menú e integración | 25 pruebas, OK | [Registro](docs/decisiones.md#episodio-3--menú-e-integración) | Pendiente |

Cada [registro](docs/decisiones.md) contiene objetivo, contexto, instrucción aplicada,
acciones y evidencia. No se inventaron errores ni aprobaciones humanas.
La [guía de revisión manual](docs/verificacion-manual.md) permite completar esa parte antes
de entregar: anotar lo observado y aceptar, corregir o rechazar cada episodio con un motivo.
