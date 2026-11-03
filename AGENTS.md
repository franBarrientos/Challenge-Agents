# Instrucciones de ReservaLab

- Leer `docs/especificacion.md` y `docs/progreso.md` antes de continuar.
- Usar Python 3.9 o superior y únicamente su biblioteca estándar.
- Mantener menú, reglas y persistencia separados; no agregar web ni servicios externos.
- Los intervalos son [inicio, fin): 10:00-11:00 y 11:00-12:00 deben poder coexistir.
- Consulta y creación deben compartir la misma regla de conflictos.
- Cancelar mediante UPDATE, conservando ID y datos. Nunca borrar para cancelar.
- Crear tablas si no existen; abrir la aplicación nunca debe reiniciar los datos.
- Ejecutar pruebas con bases temporales. Nunca usar la base del usuario para pruebas.
- Ejecutar `python3 -m unittest discover -s tests -v` después de cada episodio.
- Registrar comandos, resultados y decisiones en docs; no inventar fallos ni revisión humana.
- Solo usar solicitantes ficticios. No versionar bases, credenciales ni ejemplos ajenos.
- No publicar ni instalar dependencias sin autorización. El usuario ya autorizó implementar
  este proyecto y subirlo a `franBarrientos/Challenge-Agents` en esta sesión.
