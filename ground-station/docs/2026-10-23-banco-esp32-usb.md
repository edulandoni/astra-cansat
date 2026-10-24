# 23/10/2026 — Primer desarrollo con mi ESP32 físico

Diarios: [ASTRA-20, simulador](https://astrateam2026.atlassian.net/browse/ASTRA-20) y [ASTRA-21, recepción y registro](https://astrateam2026.atlassian.net/browse/ASTRA-21). Continúo el [banco experimental](../banco-usb-v0.1/README.md), conservando sus fuentes y los resultados anteriores. Este desarrollo usa USB; no incorpora SX1276 ni un perfil de radio.

## Qué conecté y qué comprobé

Recibí una placa con módulo rotulado ZY-ESP32 y una base de borneras. La foto permite registrar el montaje, pero no confirmar el silicio ni el mapa eléctrico de la base. No utilicé las borneras ni periféricos externos en esta etapa; su pinout queda pendiente de comprobación.

Windows detectó CP2102 USB to UART Bridge Controller, VID 10C4 / PID EA60, con código de problema 28 y sin puerto COM. Instalé el controlador Silicon Labs 11.5.0.417 del catálogo oficial de Microsoft, verificando firma válida Microsoft Windows Hardware Compatibility Publisher y coincidencia del ID del dispositivo. La descarga directa de Silicon Labs había respondido HTTP 403. La instalación requirió aceptar la elevación de Windows. Después apareció COM5, estado OK.

Con esptool consulté el dispositivo: ESP32-D0WD-V3, revisión 3.1, cristal de 40 MHz y flash detectada de 4 MB. El arranque del firmware original declaraba 2 MB; conservo esa diferencia entre configuración del programa y capacidad detectada del chip. No publico su contenido ni identificadores únicos de la placa.

## Procedimiento manual que necesité

El primer intento de conexión automática respondió `Wrong boot mode detected (0x13)`: había comunicación, pero el micro arrancaba la aplicación en lugar del cargador. Seguí esta secuencia:

1. Mantuve apretado BOOT.
2. Toqué y solté EN/RST, manteniendo BOOT.
3. Solté BOOT y dejé la placa conectada.
4. Consulté con `esptool --port COM5 --before no-reset --after no-reset flash-id`.

La identificación fue correcta. `no-reset` evita deshacer esa entrada manual antes de conectar; no garantiza que todos los comandos posteriores funcionen. Si el puerto cambia, debo volver a identificarlo; COM5 es la observación de esta PC, no una propiedad fija de la placa.

La primera lectura de respaldo de 4 MB, a 460800 baudios, se interrumpió porque el chip dejó de responder. Un intento posterior sin repetir BOOT no sincronizó. En ese momento todavía no había escrito flash y no había una copia completa acreditada. Conservo ambos diagnósticos y documento las pruebas posteriores en entradas nuevas. No presento un archivo parcial como respaldo válido.

## Código y herramientas

Compilé el [sketch original](../banco-usb-v0.1/firmware/GCS_FlightSimulator/GCS_FlightSimulator.ino) sin cambiarlo. Configuración: Arduino CLI 1.5.1, Arduino-ESP32 3.3.12, FQBN `esp32:esp32:esp32:FlashMode=dio,FlashFreq=40,FlashSize=4M,UploadSpeed=115200`. La compilación correcta informó 281044 bytes de programa y 22124 bytes de variables globales. El SHA-256 del sketch y la preparación quedan en [evidencia](../evidence/2026-10-23-esp32-usb/preparacion-01.json).

El primer intento de compilación falló al buscar `bits/c++config.h`. Resolví la compilación usando una ruta corta de acceso al compilador con `runtime.tools.esp-x32.path`, manteniendo la ubicación real de `directories.data`. Usar el enlace corto como directorio de datos de Arduino no funcionó en esta instalación. No cambié bibliotecas ni el sketch para ocultar el error. Los diagnósticos quedan conservados localmente.

Agregué [compilar_banco_usb.ps1](../tools/compilar_banco_usb.ps1): recibe las rutas de Arduino CLI, configuración y salida; crea un destino nuevo y conserva diagnóstico y huellas. El parámetro opcional CompilerRoot permite señalar una ruta corta del compilador. Este comando sólo compila, no escribe firmware.

También agregué [probar_banco_usb.py](../tools/probar_banco_usb.py): captura bytes originales USB, usa el parser y registrador existentes, y guarda un resultado con contadores, rechazos, estados, tiempos de llegada y huellas de los archivos. Cada sesión tiene carpeta propia. La opción `--scenario` sólo etiqueta el firmware ya cargado: no selecciona escenarios ni transmite comandos. `--reset` solicita reinicio por RTS, no un corte de alimentación. Conserva los primeros 0,5 segundos de arranque en crudo, fuera del parser, porque este sketch empieza a emitir al segundo; esa ventana debe revisarse si cambia el firmware.

Desde una terminal con pyserial 3.5 instalado:

```powershell
python ground-station/tools/probar_banco_usb.py --port COM5 --team 1000 --reset --seconds 137 --scenario NOMINAL --output ./capturas-locales
```

Debo cerrar otros monitores del puerto antes de capturar. El resultado distingue captura terminada de misión nominal completa. La evidencia nominal exige los contadores 1–131, llegada a LANDED, sin rechazos, desbordes ni errores de archivo; las estadísticas de llegada miden esta PC y USB, no el reloj del vuelo ni latencia RF.

Para abrir la pantalla existente, desde `ground-station/banco-usb-v0.1/`:

```powershell
python app.py --port COM5 --team 1000
```

La pantalla y el capturador no deben abrir COM5 al mismo tiempo. El sketch termina después de 131 muestras; reiniciar EN/RST vuelve a empezar. No es todavía una sesión de vuelo real ni un protocolo compartido aprobado.

## Evidencia, límites y siguiente paso

Pasaron las nueve pruebas de `python -m unittest -v test_ground` en PC. Eso valida sus casos de software, no una misión por USB. Esta entrada registra identificación y compilación; las pruebas de carga y recepción que se realicen después deben tener su propia evidencia y actualización, sin convertir lo pendiente en aprobado.

El TEAM_ID `1000` sigue siendo ficticio. Los 22 campos ASCII y CR son un adaptador experimental heredado; no los declaro formato obligatorio CONAE v2. Todos los valores de misión del sketch son sintéticos. RESET es una interrupción lógica conservando RAM, no un reinicio físico. No medí radio, alcance, sensores, autonomía, recuperación eléctrica ni respaldo en disco independiente. Los originales de descarga y eventual flash quedan fuera del repositorio público.

## Fuentes de instalación y diagnóstico

- [Silicon Labs: controladores CP210x](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers).
- [Catálogo Microsoft: CP210x](https://www.catalog.update.microsoft.com/Search.aspx?q=CP210x%20USB%20to%20UART%20Bridge), paquete `dea925e6-68b5-4568-9490-351d8621e7af`.
- [Espressif: comandos de esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/basic-commands.html).
- [Espressif: diagnóstico de modo de arranque](https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html).
- [Espressif: instalación de Arduino-ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
- [Arduino: instalación de CLI](https://docs.arduino.cc/arduino-cli/installation/).
