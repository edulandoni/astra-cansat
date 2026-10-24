# 23/10/2026 — ACTUALIZACIÓN02: módulo informado y preparación de telecomandos

Diarios: [ASTRA-18 evaluación](https://astrateam2026.atlassian.net/browse/ASTRA-18), [ASTRA-23 integración pendiente](https://astrateam2026.atlassian.net/browse/ASTRA-23), [ASTRA-24 interfaz](https://astrateam2026.atlassian.net/browse/ASTRA-24) y [ASTRA-25 tiempos/enlace](https://astrateam2026.atlassian.net/browse/ASTRA-25). Amplío la [propuesta anterior](2026-10-23-propuesta-banco-y-vuelo.md) y el [presupuesto preliminar](2026-10-23-antenas-y-link-budget-preliminar.md), sin reemplazarlos.

## Qué sé y qué falta confirmar

Edu me informó que tiene el módulo identificado como **NiceRF LoRa1276-915, SX1276, SPI,915MHz,100mW/20dBm** y compartió una foto de dos placas con antenas helicoidales. Todavía no lo tengo conectado a mi ESP32. Registro915MHz como dato informado por Edu, no como identificación independiente de la foto ni frecuencia de operación acordada.

SX1276 es el chip; LoRa1276-915 es una referencia de módulo. Compartir chip no garantiza mismo pinout, alimentación, red RF, antena o control de conmutador. No trato todas las marcas como intercambiables sin comprobar sus placas.

La [guía oficial NiceRF](https://www.nicerf.com/lora-modules/) vincula el modelo con SX1276/SPI/915MHz/100mW. Descargué el [manual LoRa127Xrev3.1](https://www.nicerf.com/pdf/lora127x-100mw-lora-wireless-transceiver-module-v3.1.pdf): enumera14conexiones en una distribución12+2 y revisiones con distinto control de antena. **La foto aportada muestra una distribución diferente, de dos hileras de ocho contactos**, y rótulos DIO que no coinciden con esa tabla. No confirmo por eso marca, variante o compatibilidad de cableado; quedaTBR revisar referencia/revisión real con Edu. No adjunto ni republico su foto privada.

El manual indica3,3V típicos, rango1,8–3,7V y120mA a20dBm; no habilita conectar5V al módulo. Es información de esa referencia, aún por verificar contra la placa real. No copio la tensión de su demo board al módulo suelto. Antena y adaptación también siguen pendientes: ver una hélice no acredita banda, VSWR o eficiencia.

## Hallazgo: máximo alcance de catálogo no equivale a1Hz

El catálogo condiciona −139dBm a LoRaBW125kHz/SF12/CR4/5. Leí la fórmula de tiempo de aire en SemtechSX1276rev4, sección4.1.1.7, p31, distribuida por [NiceRF](https://www.nicerf.com/pdf/sx1276-77-78-79.pdf). Preparé un [calculador offline](../../tools/airtime_lora.py), sin acceso a la radio y con todas las entradas explícitas.

Medí121–134bytes por trama en los629registros USB conservados, incluyendo CR. Para134bytes, preámbulo8, encabezado explícito, CRC yCR4/5, este barrido **ilustrativo** da:

| SF / BW hipotéticos | Tiempo de una trama | Consecuencia para una trama/segundo |
|---|---:|---|
| 7 /125kHz | 0,220416s | Queda tiempo teórico; faltan órdenes, confirmaciones, guardas y margen |
| 9 /125kHz | 0,697344s | Ventana restante reducida; no demuestra viabilidad del ciclo completo |
| 12 /125kHz | 5,087232s | No entra a1Hz en un enlace de este tipo |

El payload final puede agregar identificación, versión y otras sobrecargas: estos tamaños no lo cierran. No mando los metadatos@BENCH porRF por defecto ni seleccionoSF7 por esta cuenta. FSK/GFSK requieren su propia evaluación de bitrate, desviación, BW, sensibilidad y tiempos; no heredan la fórmula LoRa.

La copia Semtechrev4 también limita operación+20dBm a1% de ciclo de transmisión y VSWR3:1 en las condiciones indicadas(p84). Es una restricción del componente en esa revisión, distinta de la normativa local; necesito contrastarla con documentación vigente y el módulo real antes de usar máxima potencia. No adopto20dBm continuo como configuración. El enlace actual de Semtech a su hoja de2020 no entregó PDF legible por esta vía; conservo esta limitación de versión. No uso −148dBm genéricos del chip como sensibilidad garantizada del módulo.

## Qué voy a preparar de mi lado para los comandos

Puedo encargarme del catálogo, la interfaz de PC, las reglas de confirmación y las pruebas de referencia. Edu mantiene el extremo de vuelo: ambos debemos revisar/adoptar el mismo contrato antes de integrarlo. No modifico su código ni tomo su aceptación por implícita. SPI controla registros del radio; los telecomandos de misión los definimos entre los microcontroladores, no vienen resueltos por el módulo.

| Tema | Propuesta de trabajo | Pendiente concreto |
|---|---|---|
| Identidad/destino | Equipo y destinatario comprobables antes de ejecutar | Acordar encuadre y filtrado sin broadcast; TEAM_ID realTBD |
| Orden e ID | Catálogo versionado, argumentos y unidades inequívocas | Nombres/códigos y tamaño máximoTBR |
| Calibración | Pedido de cero con condiciones previas y resultado | Ventana válida y dato físico de referenciaTBR |
| Tiempo | AjusteUTC con fecha/precisión declaradas | Formato, persistencia y confirmaciónTBD |
| Alimentación | Consulta de batería y solar con validez/edad | Canales y unidades físicasTBD |
| Inicio y simulación | Separar inicio real, habilitación y ejecución simulada | Semántica oficial y estados compartidosTBR; RUN de banco no pasa directo a vuelo |
| Confirmación | Separar recibido/aceptado/ejecutado/rechazado/desconocido | Qué confirma ejecución real y plazoTBD |
| Duplicados y reset | ID+contexto, no repetir efecto al reenvío | Persistencia, expiración y recuperaciónTBR |
| Fallos | Casos válidos/ajenos/corruptos/tardíos/sinrespuesta | Vectores comunes y medición sobre ambos extremos |

El bancoUSB ya permite practicar estos estados y efectos sintéticos. No traslado su timeout3s, memoria64órdenes oJSON a vuelo sin evaluar airtime y memoria persistente. Una confirmación de software no prueba un mecanismo físico.

## Secuencia de integración pendiente

1. Confirmar placa/revisión y pinout; cotejar ambas unidades y antenas, alimentación y desacoplo. Sin mapaGPIO aprobado ni cableado de este módulo todavía.
2. Preparar diagnóstico SPI inicialmente sin transmisión: reset y lectura de registros, incluyendo RegVersion0x42. Su valor0x12 no identifica por sí solo915MHz, fabricante o variante de toda la placa.
3. Acordar RadioProfile y contrato; evaluar airtime máximo de telemetría+órdenes+ACK/guardas y restricciones de potencia. Mantengo frecuencia exacta, modulación, BW/bitrate, potencia, SyncWord, CRC y direccionamientoTBD/TBR.
4. Ensayar RX/TX de banco y cruce con STM32; luego reconexiones, dos horasRF y campo con perfiles/versiones fijos. Los ensayos USB previos no cierran estas pruebas.

MantengoASTRA-23 Por hacer: identifiqué una referencia informada y abrí verificaciones, pero no inicié cableado ni integración física. El diseño de interfaz ya iniciado continúa enASTRA-24; evaluación en18y25. No creo una tarea duplicada ni cambio responsables ajenos.

## Evidencia y reproducción

Ejemplo de cálculo, sin configurarRF:

```powershell
python tools/airtime_lora.py --payload 134 --sf 12 --bw 125000 --cr 1 --preamble 8 --crc 1 --implicit 0
python -m unittest discover -s tools -p test_airtime_lora.py -v
```

Dos pruebas numéricas/de restricciones pasaron. Un valor esperado del test se había transcripto mal(5,095424 frente a155,25×0,032768=5,087232); corregí esa cifra del test antes de publicar, conservando aquí la incidencia. No ajusté el cálculo para hacer coincidir un resultado físico.

[Resultado reproducible, tamaños de las629tramas y huellas](../../evidence/2026-10-23-banco02/airtime-y-modulo-04.json).

ManualNiceRF:10p, SHA256 `8e55a960b0797513a462eeb214c7d401f801a0b9e3f26abe45cf66b3dc55c156`, texto leído y páginas6–7 inspeccionadas visualmente; no afirmo inspección de todos sus esquemas. Semtechrev4:132p, SHA256 `6c24c19ee54309633d4a9057bb8663d1aacdb7f456bebcc6973728a07bd7854e`, lectura enfocada29–33/83–84/105; no auditoría completa ni errata revisada. Originales conservados en la carpeta temática de Descargas del23/10, con registro de origen/destino y sin movimientos. El buscador falló con502 para esosPDF; la descarga directa oficial funcionó y se verificó firmaPDF. [Sitio del chip Semtech](https://www.semtech.com/products/wireless-rf/lora-connect/sx1276).
