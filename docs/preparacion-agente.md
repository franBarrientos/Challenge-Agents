# Preparación del agente

## Entorno y función

- Harness existente: aplicación Codex de escritorio, agente con herramientas reales de
  lectura/escritura, ejecución de comandos y Git. No se construyó un harness.
- Función: implementar el alcance aprobado, verificar y documentar resultados reproducibles.
- Motivo: entorno ya disponible para el autor, capaz de actuar sobre los archivos locales.
- Versión de la aplicación e identificador exacto del modelo: no visibles de forma verificable
  en el registro de esta ejecución; no se atribuye un identificador supuesto.
- Versiones efectivamente medidas: [entorno.txt](evidencia/entorno.txt).
- Un único agente; sin multiagente, MCP externo, API de IA dentro de la app ni servicios pagos requeridos para ejecutarla.

## Contexto e instrucciones realmente aplicadas

Se suministraron el PDF de la consigna, dos ejemplos locales de compañeros, la propuesta
de alcance y el mensaje del autor «ok implementalo» con el repositorio destino.
Los ejemplos se consultaron para entender el alcance; no se incluyeron en este repositorio.
La solución y sus registros corresponden al trabajo de esta sesión.

Antes del código se creó y leyó [AGENTS.md](../AGENTS.md), junto a la especificación y progreso.
Las instrucciones permanecen versionadas. No se dependió de un archivo de configuración
privado para que el programa funcione.

Contexto excluido de la entrega: proyectos ajenos, PDF original, conversaciones completas,
credenciales, bases de uso y datos personales de estudiantes. Solo solicitantes ficticios.

## Permisos y controles

Configuración del entorno externo, resumida y saneada: escritura restringida al espacio de
trabajo y temporales; red restringida; acciones fuera de esos permisos requieren aprobación
del entorno. Este resumen describe los controles de la sesión, no una política impuesta por Python.

Acciones usadas: leer requisitos y archivos, aplicar cambios, ejecutar Python/unittest,
inicializar Git, crear commits y consultar/publicar en el remoto autorizado.
El autor autorizó expresamente implementar y proporcionó instrucciones de publicación.
No se requirieron instalaciones. No se enviaron correos ni se crearon servicios externos.

La primera consulta de GitHub falló por resolución de host dentro del entorno restringido;
se solicitó y obtuvo permiso para repetirla con acceso de red, y el remoto estaba vacío.
Se crea un repositorio separado para no versionar los ejemplos suministrados.

Control previsto para cada episodio: revisar diff, resultado de pruebas y comportamiento
correspondiente antes de aceptar. Control aplicado por el agente: ejecución de pruebas y
lectura de resultados en cada episodio. Control humano aplicado: aprobación del alcance.
La revisión humana posterior de los resultados está pendiente y se registra como tal.

## Adaptación específica con evidencia

1. Instrucción: «Los intervalos son [inicio, fin)». Aplicación: `se_superponen` usa comparaciones
   estrictas; pruebas de consecutivas en reglas y servicio, [episodio 1](evidencia/episodio-1.txt)
   y [episodio 2](evidencia/episodio-2.txt).
2. Instrucción: «Cancelar mediante UPDATE, conservando ID y datos». Aplicación:
   `Repositorio.cancelar` actualiza únicamente el estado; prueba
   `test_cancelar_conserva_datos_y_libera` compara el registro completo y vuelve a reservar.
3. Instrucción: «Abrir la aplicación nunca debe reiniciar los datos». Aplicación:
   `CREATE TABLE IF NOT EXISTS`, más pruebas en procesos independientes y reinicio del menú.

## Retención de progreso

[progreso.md](progreso.md) resume lo realizado y lo pendiente. [decisiones.md](decisiones.md)
conserva alternativas, instrucciones aplicadas y episodios. Los logs tienen comandos y
versiones asociados; Git conserva la especificación anterior al código y los cambios por fase.
