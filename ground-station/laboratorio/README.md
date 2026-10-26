# ASTRA — Laboratorio

[ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41). Aplicación nativa para presentar avances, experimentar y consultar evidencia sin recorrer el diario completo. Las explicaciones comienzan por utilidad y límites, seguidas del fundamento técnico. No abre puertos al iniciar.

Desde esta carpeta, con Python 3.12, Tk y las dependencias del banco (`pyserial`, `Pillow`):

```powershell
python app.py
python -m unittest test_laboratory -v
```

## Recorrido

1. Leer Recorrido y abrir Telemetría. Iniciar NOMINAL a 5×; observar ascenso/descenso. Detener y conservar antes de otro escenario.
2. Probar PACKET_LOSS, CORRUPTED_PACKET o GPS_LOSS. Los huecos de contador, los inválidos y las escrituras pendientes son magnitudes diferentes. RESET en este emisor es omisión lógica, no reinicio físico.
3. Mover el instante en Paquete: muestra texto ASCII, bytes y los 22 campos originales. Seleccionar un campo abre su explicación.
4. Cámaras muestra evidencia local conservada; no es video ni captura nueva. Abrir el chequeo físico sólo con unidades preparadas.
5. Radio LoRa compara tamaño/SF/BW/CR mediante cálculo, sin configurar hardware ni medir confiabilidad. Evidencias contiene informes locales y pendientes.

La estación completa se abre por demanda en modo PC. «Preparar recepción USB…» exige elegir explícitamente el puerto de telemetría antes de abrirlo; no pide reset ni carga firmware. El panel de cámaras se abre por demanda con registro privado. Evitar abrir dos bancos sobre el mismo puerto. Las ventanas de bancos son independientes y se cierran desde su propia interfaz; cerrar Laboratorio conserva su propia simulación y no termina capturas ajenas.

## Configuración local opcional

`python app.py --config ruta/privada.json`. No subir ese archivo ni las fotografías al repositorio. Claves:

```json
{
  "output": "ruta de ensayos nuevos",
  "camera_registry": "ruta del registro privado del banco",
  "photos": {
    "1": {"path": "ruta foto cámara 1", "caption": "Fecha, origen y condición conservada"},
    "2": {"path": "ruta foto cámara 2", "caption": "Fecha, origen y condición conservada"}
  }
}
```

Sin configuración las simulaciones y cálculos funcionan; la sección cámaras explica la ausencia de imagen y permite consultar los informes. Los ensayos se guardan por defecto en `~/ASTRA-Laboratorio/ensayos`, con nueva sesión para cada inicio. No se borran originales. El gráfico mantiene como máximo 180 muestras; los escritores reutilizados conservan sus límites de cola.

## Alcance

Integro el motor existente de banco y la fórmula SX1276 existente, conservando sus pruebas. El Laboratorio no aprueba comandos de vuelo, RF, consumo, autonomía o video. No acredita cumplimiento total del PDR. El objetivo de cámaras continúa secundario; los acuerdos con Edu permanecen explícitos.
