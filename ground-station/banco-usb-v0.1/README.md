# Banco USB v0.1 — experimental

Relacionado con [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21) y [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22).

Uso este banco para recorrer adquisición, interpretación, CSV y pantalla antes de integrar radio. Las fuentes importadas son las del 17/10/2026, conservadas sin cambios. Leo primero [el aviso v2](AVISO_BASELINE_V2.txt): el LEEME original usa referencias v1 que ya no deben interpretarse como obligaciones de sintaxis v2.

## Prueba en computadora

Necesito Python con Tkinter para la pantalla. Desde esta carpeta ejecuto:

```text
python app.py --scenario NOMINAL
python -m unittest -v test_ground
```

También puedo abrir INICIAR_SIMULACION.cmd en Windows. Los escenarios son NOMINAL, PACKET_LOSS, CORRUPTED_PACKET, GPS_LOSS y RESET. La simulación PC no necesita instalar paquetes adicionales; para conectar un puerto serie instalo `python -m pip install -r requirements.txt`.

La misión ficticia entrega hasta 131 muestras, una por segundo. Cada ejecución guarda una sesión nueva en runs/. `1000` es un TEAM_ID de ejemplo, no el asignado a ASTRA. Las coordenadas y todos los valores son sintéticos.

## Qué puedo comprobar

Puedo comprobar reconstrucción de paquetes, validación, contador, rechazos y registro CSV de datos sintéticos. El código separa generador o puerto USB, adquisición, parser, almacenamiento y GUI.

Todavía no demostré comunicación física con la placa. Antes de compilar el sketch necesito identificarla. No hay radio configurada, telecomandos completos ni ensayo de autonomía. RESET simula una interrupción lógica: no prueba un corte eléctrico. El descenso ficticio necesita revisión antes de usarlo como evidencia de C3. GPS_LOSS retiene el último dato y lo señala; no representa una posición nueva.

La carpeta runs/ es de uso local. Los resultados que publico como evidencia se guardan en ../evidence/ con fecha y contexto. Dos archivos en un mismo disco no acreditan respaldo físico independiente.

## Actualización del 23/10/2026 — placa física y arranque de banco

La [prueba física posterior](../docs/2026-10-23-prueba-usb-fisica-actualizacion-02.md) agrega identificación, carga y dos misiones USB completas. El sketch y parser se conservan; agregué la opción explícita de GUI python app.py --port COM5 --team 1000 --bench-reset-once para reiniciar una vez y conservar el arranque fuera del parser. Sólo se usa con el simulador conocido que comienza al segundo. La adquisición normal no activa esta ventana. Las versiones anteriores del código quedan en Git, incluidas las que documenta el estado inicial de este banco.
