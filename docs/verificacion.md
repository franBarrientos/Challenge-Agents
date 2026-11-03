# Matriz de verificación

Comando ejecutado: `python3 -m unittest discover -s tests -v`.
Entorno: [versiones](evidencia/entorno.txt). Resultado final: 25 pruebas ejecutadas, OK,
con varios subcasos; [salida](evidencia/episodio-3.txt). Estas son comprobaciones del agente.

| Criterios | Pruebas verificables (archivo: método) |
|---|---|
| CA01 | test_reglas.py: test_inventario_de_la_consigna |
| CA02 | test_servicio.py: test_creacion_valida_con_identificadores_distintos |
| CA03 | test_reglas.py: test_superposiciones_parciales_contenidas_e_identicas; test_servicio.py: test_rechazo_de_superposiciones_no_guarda_registros |
| CA04 | test_reglas.py: test_consecutivas_y_separadas_en_ambos_sentidos; test_servicio.py: test_consecutivas_antes_y_despues |
| CA05 | test_servicio.py: test_unidades_distintas_simultaneas |
| CA06 | test_reglas.py: test_solicitante_vacio_y_espacios, test_unidad_desconocida, test_fecha_invalida_o_formato_incorrecto, test_inicio_igual_o_posterior_al_fin; test_menu.py: test_fecha_invalida_y_solicitante_vacio_no_crean_reservas |
| CA07 | test_servicio.py: test_consulta_y_creacion_rechazan_mismas_entradas_invalidas, test_rechazo_de_superposiciones_no_guarda_registros |
| CA08, CA11 | test_servicio.py: test_cancelar_conserva_datos_y_libera |
| CA09 | test_servicio.py: test_cancelaciones_invalidas_no_modifican_historial |
| CA10 | test_persistencia.py: test_activas_y_canceladas_sobreviven_a_proceso_nuevo; test_menu.py: test_recorrido_completo_y_reinicio |
| CA12 | test_menu.py: test_opciones_invalidas_no_cierran_el_programa, test_fin_de_entrada_conserva_reservas |
| Reinicio explícito | test_menu.py: test_reinicio_cancelado_conserva_reservas, test_reinicio_confirmado_borra_ambos_estados |
| Supuestos de fechas | test_reglas.py: test_fechas_pasadas_bisiestas_y_cambio_de_dia |

No se ejecutaron comprobaciones humanas ni pruebas en Windows/Linux en esta sesión.
No se probaron accesos concurrentes, fuera de alcance. No hubo fallos en las tres
ejecuciones de unittest registradas; no se provocaron errores de implementación para documentarlos.
