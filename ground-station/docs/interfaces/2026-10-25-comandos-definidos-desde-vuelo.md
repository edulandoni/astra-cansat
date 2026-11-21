# 25/10/2026 — ACTUALIZACIÓN: definición de comandos desde vuelo

Diario: [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Actualizo el reparto de implementación de la [propuesta anterior](2026-10-23-propuesta-banco-y-vuelo.md) y conservo su contenido como antecedente.

Acordamos que Edu define los comandos de vuelo y yo adapto groundstation a esa definición. Así evitamos que tenga que acomodar el STM32 a la sintaxis que usé para practicar por USB. Esto fija el sentido de la adaptación; no da por aprobado un formato todavía no recibido.

Seguimos necesitando las funciones de referencia de altura, espera/activación y consulta de alimentación. El detalle de cada función, argumentos, estados permitidos, confirmaciones y fallas debe quedar explícito en la definición que recibamos. No equiparo automáticamente «detener simulación» con «standby del CanSat» ni una consulta de corriente con otra de tensión o señal solar.

Los nombres RUN/STOP/CAL_ZERO/SET_TIME/POWER_STATUS y el prefijo @BENCH permanecen exclusivamente en el banco experimental. No los envío como protocolo de vuelo ni cambio firmware sólo por esta decisión. Prepararé el adaptador cuando tenga especificación versionada y ejemplos de bytes válidos, inválidos y respuestas de Edu.

El acuerdo necesita identificar: versión, destinatario, orden y argumentos, unidades/referencias, estado permitido, recibido/aceptado/ejecutado/rechazado, respuesta desconocida, repetición y efectos tras reset. Las propuestas anteriores sobre identidad y confirmaciones son casos para revisar; no obligaciones impuestas unilateralmente al extremo de vuelo. Si falta una capacidad, registraré la limitación antes de mostrarla como comprobada en la app.

Agrego las funciones de cámaras en [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39): comprobar ambas, preparar/iniciar y finalizar grabación. Son conceptos de operación propuestos, pendientes del acuerdo y de ensayos; no selecciono nombres ni bytes de telecomando. La [investigación de cámaras](../camaras/2026-10-25-energia-chequeo-dual.md) explica por qué el inicio de grabación debe separarse de poner altura en cero.

No modifiqué tareas de Edu, protocol/, código de vuelo ni perfil RF. Falta recibir la especificación, implementar y probar mi adaptación, y ejecutar interoperabilidad real. Esta entrada registra una decisión de coordinación, no una prueba cruzada aprobada.
