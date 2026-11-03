# Decisiones y delegación

## Decisiones técnicas

| Decisión | Motivo, alternativa y consecuencia |
|---|---|
| Python y biblioteca estándar | Reducir instalación. Frente a C# con ORM o una web, basta Python instalado; SQLite y unittest vienen incluidos. |
| Menú numerado | Facilita el uso sin memorizar comandos. Frente a una API, permite probar directamente en terminal. |
| SQLite | Persistencia transaccional en un archivo; frente a reescribir JSON evita manejar manualmente escrituras completas. |
| Tres módulos | Separar interfaz, reglas y persistencia sin framework ni múltiples capas de abstracción. |
| Horario UTC-3 fijo y pasado permitido | Ejemplos reproducibles, sin dependencia del reloj ni de la zona del equipo. No contempla cambios de huso horario. |
| Pruebas de comportamiento | Cubrir reglas requeridas, reinicios y menú; no perseguir un número de pruebas como objetivo. |

## Autorización y revisión

El autor aceptó la propuesta con «ok implementalo» y proporcionó el destino GitHub.
Esa autorización permite implementar y publicar; no prueba que haya revisado cada resultado.
Los siguientes episodios son fases del trabajo del mismo agente bajo esa instrucción,
no tres mensajes separados del autor ni tres agentes. Los extractos de instrucciones
provienen del archivo `AGENTS.md` realmente leído. Las decisiones humanas de cada episodio
deben completarse con su revisión real; no se atribuyen automáticamente al autor.

## Episodio 1 — Reglas e inventario

- Objetivo/requisitos: CA01, CA03–CA07; modelar validaciones y conflictos.
- Contexto: consigna revisada, propuesta aceptada, especificación v1 e instrucciones.
- Extracto aplicado: «Los intervalos son [inicio, fin): 10:00-11:00 y 11:00-12:00 deben poder coexistir».
- Acción del agente: implementó funciones puras, inventario original y nueve pruebas con subcasos.
- Verificación del agente: `python3 -m unittest discover -s tests -v`, Python 3.9.6,
  9 pruebas ejecutadas, OK; [salida](evidencia/episodio-1.txt).
- Evidencia: [reglas](../reservas.py), [pruebas](../tests/test_reglas.py).
- Decisión humana: **pendiente**. Falta indicar aceptar/corregir/rechazar y motivo tras revisar.

## Episodio 2 — Persistencia y cancelación

- Objetivo/requisitos: CA02–CA11; integrar reglas con guardado durable.
- Contexto: especificación v1, reglas y evidencia del episodio 1, instrucciones y progreso.
- Extracto aplicado: «Cancelar mediante UPDATE, conservando ID y datos. Nunca borrar para cancelar»;
  «Crear tablas si no existen; abrir la aplicación nunca debe reiniciar los datos».
- Acción del agente: agregó repositorio SQLite y servicio que reutiliza disponibilidad al crear;
  pruebas de integración y de persistencia con dos procesos independientes.
- Verificación del agente: `python3 -m unittest discover -s tests -v`, Python 3.9.6,
  18 pruebas ejecutadas, OK; [salida](evidencia/episodio-2.txt).
- Evidencia: [persistencia](../persistencia.py), [servicio](../tests/test_servicio.py),
  [prueba de reinicio](../tests/test_persistencia.py).
- Decisión humana: **pendiente**. Falta indicar aceptar/corregir/rechazar y motivo tras revisar.

## Episodio 3 — Menú e integración

- Objetivo/requisitos: CA01–CA12 desde la interfaz y ejecución reproducible de la entrega.
- Contexto: especificación, reglas, servicio, persistencia y resultados de los episodios anteriores.
- Extracto aplicado: «Mantener menú, reglas y persistencia separados; no agregar web ni servicios externos»;
  «Ejecutar pruebas con bases temporales. Nunca usar la base del usuario para pruebas».
- Acción del agente: implementó menú numerado, mensajes de error, selección de base y
  reinicio confirmado; documentó instalación, uso, supuestos y revisión pendiente.
- Verificación del agente: `python3 -m unittest discover -s tests -v`, Python 3.9.6,
  25 pruebas ejecutadas, OK; [salida](evidencia/episodio-3.txt).
  Recorrido adicional de dos procesos del menú con entradas y [salida real](evidencia/recorrido.txt).
- Evidencia: [interfaz](../main.py), [pruebas de menú](../tests/test_menu.py),
  [matriz de aceptación](verificacion.md), [README](../README.md).
- Decisión humana: **pendiente**. Falta indicar aceptar/corregir/rechazar y motivo tras revisar.

## Versiones y evidencia

- Especificación anterior al código: `6537eae`.
- Episodio 1: `4516aff`.
- Episodio 2: `9cd5676`.
- Episodio 3: `8fb34d5`, `feat: episodio 3 menu y documentacion de entrega`.
- Reproducción del episodio 3 desde un clon limpio local: [25 pruebas, OK](evidencia/clon-limpio.txt).
- Las pruebas de cada fase siguen incluidas en la versión final. La última ejecución
  agrupa las tres fases. Los logs anteriores describen únicamente su versión histórica.
