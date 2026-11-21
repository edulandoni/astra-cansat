# ASTRA-22 · Diseño final de la estación terrena

20 de noviembre de 2026. Entrega de diseño para ASTRA y el PDR. Las pantallas utilizan datos de ejemplo. El [registro de verificación Qt](../Verificacion_GCS_G12_G13_Qt.md) identifica la implementación y las pruebas disponibles.

| Pantalla | Qué incluye | Imagen |
| --- | --- | --- |
| Operación | 22 campos del perfil de banco, cinco gráficos simultáneos, fuente y antigüedad, RX válido, huecos, estado de guardado, consola y accesos a sesión y diagnóstico. | [01 Operación](01_operacion.svg) |
| Comandos | Destino y perfil, selección, argumentos, previsualización, confirmación, recepción de respuesta y comprobación del efecto. | [02 Comandos](02_comandos.svg) |
| Sesión y archivos | Fuente y puerto, destinos, estado por escritor y totales de cierre, con ejemplo de pérdida del segundo destino. | [03 Sesión y archivos](03_sesion_guardado.svg) |
| Diagnóstico | Caducidad, GPS, secuencia, tramas, cambios de fuente y exportación de evidencia. | [04 Diagnóstico](04_diagnostico.svg) |

[Descargar la galería HTML sin dependencias](Dise%C3%B1o_final_estacion_terrena.html) · [Captura de la aplicación Qt en ejecución](../ASTRA_estacion_terrena_Qt_replay.png).

## Decisiones y verificación

| Decisión | Fundamento | Cómo se verifica |
| --- | --- | --- |
| Telemetría y gráficas en la misma vista, consola lateral | El panel de laboratorio distribuye la información entre pestañas. La operación simultánea permite consultar valores y tendencias mientras se prepara una orden. | El ensayo Qt ya comprobó simultaneidad y ajuste en la revisión 78b735d. Repetir la comprobación con el diseño final implementado, la pantalla objetivo y los campos del ICD de vuelo. |
| Jerarquía clara de avisos, texto oscuro, fondo claro y ejes marcados | Fuente, faltantes, GPS y errores de guardado requieren una lectura rápida. Color y texto identifican juntos cada alerta. | Aplicar el procedimiento exterior G12 en el equipo de campo y comprobar el mínimo de 14 pt, la lectura de unidades, ejes y leyendas bajo luz solar. |
| Transmisión supervisada | La reproducción conserva la evidencia sin habilitar envío. Una confirmación no demuestra recepción ni ejecución. | Comprobar controles bloqueados en reproducción y con enlace o destino sin verificar. En banco, correlacionar el ID con la respuesta y, cuando sea observable, con el cambio en telemetría. Validar el enlace y el protocolo de vuelo por separado. |
| Diario y CSV con estado separado por destino | Un segundo escritor degradado requiere una indicación propia mientras se conoce qué se sigue guardando. | El ensayo previo verificó el aviso con un estado inyectado. Ensayar la desconexión y el cierre con dos medios físicamente independientes. |

## Reglas de la consola

- El selector sólo ofrece operaciones del perfil verificado. El perfil de banco actual dispone de inicio y parada de emisión, referencia de altura, hora UTC y consulta de energía. La sintaxis, el direccionamiento y el conjunto de comandos de vuelo se incorporan al acordar el ICD.
- Antes de confirmar, mostrar destino, operación, argumentos validados, efecto esperado e identificador de correlación. Con reproducción, sesión cerrada, enlace caído o destino sin verificar, el control de envío queda deshabilitado. Si cambia la sesión o el perfil, invalidar la orden preparada.
- El historial distingue envío local, respuesta correlacionada y efecto observado. Con tiempo agotado se presenta resultado desconocido. El operador decide cómo continuar según el procedimiento y el perfil. Evitar reintentos automáticos.
- Al iniciar, mostrar el origen sin muestras hasta recibir la primera trama válida. Una desconexión conserva la última muestra, con antigüedad visible. GPS sin solución se marca explícitamente. RX válido, TX, huecos e inválidos se presentan como conteos distintos.
- Cerrar la sesión detiene la adquisición y registra los resultados de cada escritor. Los archivos de sesiones anteriores se conservan.
