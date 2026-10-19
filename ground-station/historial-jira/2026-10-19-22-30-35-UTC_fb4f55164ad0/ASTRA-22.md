# ASTRA-22 — GND — Implementar GUI PDR mínima de telemetría en tiempo real

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-22)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

## Descripción original consultada

## Objetivo

Construir una primera GUI funcional de Ground Station que demuestre el flujo completo de telemetría y cubra los requisitos CONAE aplicables a visualización.

## Trabajo a realizar

* Mostrar simultáneamente los campos de telemetría requeridos, sin pestañas.
* Usar tema claro, tipografía ≥14 pt y gráficos/ejes legibles bajo luz intensa.
* Graficar en tiempo real altitud, voltaje, corriente, aceleración XYZ y giro XYZ.
* Mostrar tiempo de misión, temperatura, GPS, paquetes recibidos/perdidos, estado FSW y CMD_ECHO.
* Incorporar indicadores de estado de enlace y logging.
* No acoplar la GUI directamente al puerto serie: consumir datos desde el módulo de telemetría/parser.

## Entregable

`ASTRA Ground Station GUI v0.1` ejecutable en la notebook de Cristian + capturas para PDR.

## Criterio de finalización

* Todos los datos requeridos aparecen simultáneamente.
* Los gráficos actualizan a 1 Hz sin congelar la interfaz.
* La GUI permanece operativa durante una misión simulada completa.
* Diseño compatible con G5–G8 y G12–G14.
* Capturas y arquitectura listas para la PDR.



## Comentarios conservados

### 2026-10-17T12:14:56.866-0300 — comentario 10010

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10010). Última edición informada: 2026-10-17T12:14:56.866-0300.

## Revisión de GUI frente a v2 — 17/10/2026

G5–G8 y G12–G14 conservan contenido. El banco Python muestra 22 campos y seis gráficos simultáneos sin pestañas. Se comprobó geometría de ventana; falta inspección bajo sol y en portátil de operación.

G6: presentar giro en rad/s o junto a conversión SI; hoy el banco etiqueta grados/s. Conservar datos brutos con unidad de origen, sin cambiar sólo una etiqueta. Ejes/validez GPS y formato temporal deben cerrarse en el ICD. Falta señal solar y operación de comandos del esquema final; CMD_ECHO=NONE no demuestra ejecución. No transferir a operación el comportamiento de v04 que pausa la simulación al abrir una ayuda.

Informe: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit?usp=drivesdk  
Banco y evidencias sintéticas: https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf

### 2026-10-17T12:31:23.792-0300 — comentario 10024

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10024). Última edición informada: 2026-10-17T12:31:23.792-0300.

## Bitácora 17/10/2026 — pantalla del banco y límites de validación

### Por qué y qué se buscó

G5–G8/G12–G14 requieren lectura y gráficos simultáneos, legibilidad bajo luz intensa y conteos/estado visibles. La pantalla consume la adquisición separada para mantener el registro aunque el dibujo demore. Se eligió Tkinter para que la simulación PC funcione con el Python disponible sin instalar un framework gráfico adicional.

### Qué hicimos y verificamos

GUI con 22 campos del perfil heredado y seis gráficos simultáneos: altitud, voltaje, corriente, aceleración XYZ, giro XYZ y presión. Fondo claro, texto de 14 pt, ejes destacados, sin pestañas. Se muestra conexión, logging, respaldo configurado/ausente, conteos y advertencia de datos antiguos tras tres segundos. El gráfico deja abiertos los huecos entre contadores. Historial de presentación acotado a 300 muestras, independiente del archivo.

Comprobación geométrica: ventana de 1450×949, 45 etiquetas y seis gráficos; ninguna etiqueta fuera de la ventana en la comprobación realizada. No fue un ensayo bajo sol ni valida todo tamaño/escala de portátil. Las nueve pruebas corresponden al software de datos; no certifican legibilidad ni operación de campo.

### Límites y siguiente trabajo

Faltan telecomandos y señal solar del esquema definitivo. El giro se muestra en grados/s: para G6 acordar y presentar conversión a rad/s con unidad correcta, conservando los datos originales. MODE/STATE/CMD_ECHO/horas/GPS siguen el perfil de banco v1 y requieren ICD. En el HTML v04 abrir una ayuda pausa la simulación; ese comportamiento no se adopta como recepción operativa.

El PDR puede mostrar la interfaz y el flujo de datos sintéticos con etiqueta de simulación. Para cerrar: notebook real, sol, distancia de lectura, resolución/escala, dos horas y casos de enlace/registro fallidos.  
Código y evidencia: https://drive.google.com/file/d/1dOL2imloQJ7vsTKhMbexEt3YG8NyAUSK/view  
Informe: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit

### 2026-10-17T12:43:32.356-0300 — comentario 10032

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10032). Última edición informada: 2026-10-17T12:43:32.356-0300.

## Bitácora 17/10/2026 — estado de trabajo y alcance

Paso esta tarea de Backlog a **En curso**.

Ya implementé la pantalla del banco con telemetría y gráficos simultáneos. Me faltan unidades/payload definitivos, solar/comandos y prueba de legibilidad con la notebook real.

Uso Backlog para ideas que todavía no asumimos; Por hacer para trabajo previsto sin iniciar; y En curso cuando ya estoy trabajando. La tarea sigue abierta hasta cumplir sus criterios y conservar la evidencia. En adelante gestiono únicamente tareas que creé o que están asignadas a mí; las dependencias con Edu y Rebe las documento desde mis propias tareas.

### 2026-10-19T19:28:22.883-0300 — comentario 10041

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10041). Última edición informada: 2026-10-19T19:28:22.883-0300.

## 19/10/2026 — COMENTARIO 4 — GUI y antecedente visual conservados

Publiqué la GUI del banco USB del 17/10 junto con una guía comprensible de su alcance. Conservo el antecedente v04 como DEPRECATED, sin editar su código ni sus explicaciones originales. Sus referencias reglamentarias son históricas v1 y algunas ayudas externas no están recuperadas en esta copia.

El banco permite mostrar el recorrido de datos sintéticos y mantiene separada la pantalla de adquisición, parser y registro. Las nueve pruebas del banco y las trece pruebas de lógica v04 aprobaron. No hice una verificación visual nueva ni un ensayo bajo sol, de pantalla de operación o de misión física; no cierro G12/G13 por esos tests.

Guía: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/README.md  
Banco: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/banco-usb-v0.1/README.md  
Histórico: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/archive/DEPRECATED/estacion-v04/README.md  
Verificación y límites: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/pruebas-2026-10-19.md  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/a1a7d383ed4498b540c0f7a12500a66f84bc3551

Quedan pendientes unidades SI, telecomandos y solar, pruebas de pantalla y operación real. La tarea continúa En curso.

## Historial de cambios de campos

### 2026-10-13T01:43:11.324-0300 — cambio 10079

Autoría original: Eduardo Landoni.

Campo: Rank.

Antes: (sin valor informado)

Después: Ranked higher

### 2026-10-13T01:56:02.014-0300 — cambio 10086

Autoría original: Cristian Ponsone.

Campo: assignee.

Antes: cristianponsone9

Después: Cristian Ponsone

### 2026-10-17T12:42:37.690-0300 — cambio 10122

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-17T12:43:24.059-0300 — cambio 10129

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

