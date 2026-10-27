# ASTRA — Laboratorio

## Vista previa Wi-Fi de mantenimiento — 27/10/2026

[Panel Qt, candidato cargado en cámara 1 y modelo de supervisión](../docs/camaras/2026-10-27-vista-previa-wifi-banco.md). Wi-Fi se activa explícitamente por USB; abrir la app no conecta la cámara. Carga/INFO verificados, imagen física Wi-Fi y grabación autónoma todavía pendientes. Cada cámara cuenta con su propia SD; sonido queda fuera de esta etapa.

## Grabación verificada y exportación — 27/10/2026

Ver última grabación abre la secuencia privada configurada por unidad. El visor comprueba sus originales, reproduce por tiempos guardados y exporta un MP4 derivado, con verificación posterior de cuadros/marcas y sin alterar los JPEG. La exportación necesita PyAV 19.0.1, fijado en requirements-qt.txt. [Primer ensayo físico: doce cuadros y límites](../docs/camaras/2026-10-27-primera-secuencia-y-mp4-18.md). Clave privada opcional: `sequences: {"1": "carpeta de secuencia verificada"}`; no se publica con el repositorio.

## Foto física y secuencia — 27/10/2026

Cámaras ofrece Sacar foto, Foto + microSD y ampliación nativa, con captura en curso y foto anterior identificadas. Grabar prueba solicita doce cuadros sólo si la unidad anuncia CLIP; su cierre reportado requiere verificación independiente. [Foto física de cámara 1, pruebas y pendientes](../docs/camaras/2026-10-27-foto-qt-fisica-y-secuencia-17.md). Entrada directa: `python app.py --config CONFIGURACION_PRIVADA --page camaras`.

## Banco integrado — actualización del 26/10/2026

Telemetría contiene Variables (22), Gráficos (11), Comandos, Guardado, Diagnóstico, Tramas y Estado. Los gráficos incluyen los quince canales numéricos; el giro se presenta en rad/s sin alterar el paquete original. USB, simulación PC y reproducción son selecciones explícitas; PC y reproducción permiten velocidades ×1/×5/×10. Sin fuente no hay mediciones. El archivo completo conserva el flujo aunque la pantalla sólo mantenga las últimas 180 muestras y 300 eventos.

Cámaras ofrece **Foto USB** y **Foto + microSD** por unidad, con identidad y puerto explícitos, más el visor Qt de secuencias guardadas. Foto USB no requiere una tarjeta; Foto + microSD solicita el chequeo de escritura/lectura reportado por la cámara. Los botones están conectados al capturador existente y comprobados con sustituto de hardware; su campaña física Qt sigue pendiente.

Ensayos y análisis reúne presupuesto de enlace, rotor/energía, campaña ejecutable de calidad/direccionamiento y archivo filtrable de todos los resultados, configuraciones y documentos textuales del proyecto. Los cálculos guardan archivos nuevos e identifican sus hipótesis. Enlace RF permite comparar los seis SF7–SF12 y cuatro CR; no configura radio. El [informe de cobertura y pruebas](../docs/historial/2026-10-26-laboratorio-completo-04.md) documenta funciones, evidencia y pendientes.

## Entrada vigente: aplicación nativa Qt

Uso `app.py`, que abre la interfaz Qt Widgets (PySide6). La copia Tk queda en `archive/DEPRECATED/laboratorio-tk-20261026/` como referencia histórica. Los bancos y registros anteriores se conservan.

En esta notebook el acceso **ASTRA Laboratorio** del escritorio apunta al entorno dedicado de Qt. No se abre ni conecta hardware al actualizar el acceso. Si ya hay una ventana antigua abierta, cerrarla y volver a abrir el acceso permite entrar a la interfaz vigente.

Para otra instalación, preparar un entorno Python de ruta corta en Windows e instalar `requirements-qt.txt`; luego:

```powershell
python app.py --config ruta/privada.json
```

### Cómo usarlo

1. **Avances del proyecto**: siete subsistemas con implementación, estado de verificación y prueba disponible. El detalle técnico se despliega bajo demanda.
2. **Telemetría**: elijo una fuente explícita. USB abre sólo el puerto elegido; simulación PC genera una misión ficticia a 5×; reproducción lee un diario anterior y genera registros nuevos.
3. **Cámaras**: imágenes conservadas con procedencia y comprobación nueva bajo demanda, con puerto e identidad esperados. Ningún chequeo nuevo ocurre al abrir la pantalla.
4. **Enlace RF**: cálculo LoRa, sin emisión. **Recuperación de datos**: tres casos sintéticos. **Documentación**: informes nativos y decisiones con límites.

Sin fuente, las mediciones empiezan vacías. Desconectar el ESP32 no activa un simulador: los valores recibidos se marcan históricos, su edad sigue creciendo y el receptor intenta reconectar bajo sus reglas existentes. «Por guardar» cuenta filas recibidas pendientes de escritura, no paquetes ausentes durante el corte. El firmware de banco del ESP32 también genera valores ficticios; recibirlo físicamente por USB no transforma esos valores en sensores de vuelo.

Las comprobaciones de esta interfaz utilizan `QT_QPA_PLATFORM=offscreen`: renderizado real de widgets en memoria sin ventanas en el escritorio. Los tests de USB usan un transporte simulado; la nueva interfaz no acredita una campaña física de desconexión. La tecnología y los módulos están documentados en [Qt for Python](https://doc.qt.io/qtforpython-6/gettingstarted.html).

```powershell
python -m unittest discover -s . -p "test_*.py" -v
```

Las siguientes secciones conservan el procedimiento de la primera entrega y sus conceptos; su presentación vigente está organizada en las páginas Qt anteriores.

[ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41). Aplicación nativa para presentar avances, experimentar y consultar evidencia sin recorrer el diario completo. Las explicaciones comienzan por utilidad y límites, seguidas del fundamento técnico. No abre puertos al iniciar.

Desde esta carpeta, con Python 3.12, Tk y las dependencias del banco (`pyserial`, `Pillow`):

```powershell
python app.py
python -m unittest test_laboratory -v
python -m unittest test_gui_close -v
```

## Recorrido

1. Leer Recorrido y abrir Telemetría. Iniciar NOMINAL a 5×; observar ascenso/descenso. Detener y conservar antes de otro escenario.
2. Probar PACKET_LOSS, CORRUPTED_PACKET o GPS_LOSS. Los huecos de contador, los inválidos y las escrituras pendientes son magnitudes diferentes. RESET en este emisor es omisión lógica, no reinicio físico.
3. Mover el instante en Paquete: muestra texto ASCII, bytes y los 22 campos originales. Seleccionar un campo abre su explicación.
4. Cámaras muestra evidencia local conservada; no es video ni captura nueva. Abrir el chequeo físico sólo con unidades preparadas.
5. Radio LoRa compara tamaño/SF/BW/CR mediante cálculo, sin configurar hardware ni medir confiabilidad. Evidencias contiene informes locales y pendientes.
6. Recuperación crea dos fuentes sintéticas complementarias, incompletas o contradictorias. Ejecuta el recuperador real, conserva originales y genera resultados nuevos. No prueba soportes independientes: ambas fuentes están en este disco.

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
