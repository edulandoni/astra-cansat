# 19/10/2026 — Resiliencia y recuperación sin hardware

Continúo [la investigación anterior](../../docs/investigacion/2026-10-19-innovacion-y-prevencion.md) y registro el trabajo en [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21).

## Qué ejecuto

Desde la raíz del repositorio:

```text
python ground-station/experiments/2026-10-19-resiliencia/explorar.py --salida ground-station/evidence/MI_NUEVA_PRUEBA
```

Uso Python y su biblioteca estándar, sin instalar controladores ni abrir puertos reales. Ejecuto adquisición y almacenamiento originales con sustitutos controlados para la conexión y una escritura CSV. La espera entre reconexiones se registra, pero se salta para que la prueba sea breve. No modifico los módulos del banco.

1. Entrego 7200 paquetes sintéticos sin consumir la cola de pantalla y compruebo su conservación en CSV y raw.
2. Hago fallar diez escrituras del CSV principal y comparo lo que queda en cada copia.
3. Simulo una apertura fallida, un corte con una trama incompleta y la reconexión con dos paquetes completos.

Los CSV y raw pequeños de fallos y conexión se conservan en la salida. Del ensayo de 7200 paquetes conservo el resumen, comprobaciones y huella del CSV; sus archivos completos se generan temporalmente y pueden reproducirse. No presento 7200 mensajes acelerados como dos horas reales de autonomía ni como una misión físicamente coherente.

## Demostración de recuperación offline

Con las dos copias de la misma sesión de laboratorio:

```text
python ground-station/experiments/2026-10-19-resiliencia/reconciliar.py --principal ground-station/evidence/2026-10-19-resiliencia/fallo_csv/principal.csv --respaldo ground-station/evidence/2026-10-19-resiliencia/fallo_csv/respaldo.csv --salida ground-station/evidence/MI_NUEVA_RECUPERACION --misma-sesion-de-laboratorio
```

Creo recuperado.csv y procedencia.csv nuevos cuando no encuentro contradicciones. El reporte identifica qué registros llegaron solo desde respaldo y conserva las huellas de los originales. Si dos registros del mismo equipo/contador difieren, el programa informa el conflicto y no escribe un CSV recuperado. No elige silenciosamente una de las versiones.

El argumento de misma sesión declara una condición del experimento: no identifica sesiones automáticamente ni permite mezclar vuelos o reinicios. Este demostrador no debe usarse como recuperador general de archivos de vuelo. La identidad de sesión real sigue pendiente del ICD.

Cada ejecución exige una salida nueva. No reemplazo los CSV originales ni los resultados anteriores. La demostración recupera lo que está en otra copia; no inventa mensajes que falten en todas.

## Evidencia

- [Experimentos de adquisición](../../evidence/2026-10-19-resiliencia/resultados.json).
- [Demostración de recuperación](../../evidence/2026-10-19-resiliencia-reconciliacion/resultado.json).
- [Interpretación y siguiente prioridad](../../docs/investigacion/2026-10-19-resiliencia-y-recuperacion.md).
