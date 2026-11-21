# 26/10/2026 — ACTUALIZACIÓN 03: Laboratorio Qt y fuentes de telemetría

[ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41) · [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22). Continúo la [entrega inicial](2026-10-26-laboratorio-entrega-01.md) y la [recuperación](2026-10-26-laboratorio-recuperacion-02.md), conservando sus registros.

## Implementación

Rehice la entrada del Laboratorio con Qt Widgets/PySide6, con navegación por subsistema y presentación sobria. No utiliza navegador ni una página HTML como interfaz. La entrada sigue siendo `laboratorio/app.py`; el acceso existente del escritorio apunta al entorno Qt dedicado. La copia Tk queda archivada como referencia. Los bancos y registros originales se conservan.

Avances del proyecto recorre siete temas: simulador, adquisición/almacenamiento, reconexión/calidad, recuperación, cámaras, enlace LoRa y requisitos/verificación. Cada tema separa implementación, estado de verificación, prueba disponible y detalle técnico. Los títulos son nombres descriptivos; no utilizo hooks ni guiones publicitarios.

Telemetría exige elegir una fuente: USB, simulación PC o reproducción. Al iniciar las mediciones están vacías. No existe reemplazo automático de USB por simulación. Tras un corte, los valores conservados quedan identificados como históricos y aumenta su antigüedad. Los pendientes de escritura son filas ya recibidas; los mensajes ausentes durante el corte pueden quedar por determinar.

Reutilizo Engine/Store y las reglas de reconexión del banco: no configuro RF ni cambio el contrato de vuelo. USB no envía un reset al conectar. El inicio del ensayo en placa requiere acción explícita y una identidad disponible. La simulación PC y la reproducción no abren puertos; el emisor PC sólo se crea al seleccionarlo. Los valores del firmware de banco también son sintéticos aunque provengan de un ESP32 físico.

La interfaz integra métricas, gráfico sin unir huecos, contadores, inspección de la trama de 22 campos, fotografías conservadas y chequeo nuevo por unidad/puerto, cálculo LoRa y recuperación. La reproducción de registros conserva originales y genera otra sesión. Los trabajos de escritura y cámaras se completan antes del cierre; no termino una captura por cerrar la ventana.

## Verificación

La batería contiene diez pruebas del Laboratorio y 34 del banco de cámaras. Incluye recorrido/navegación Qt, arranque sin muestras, desconexión de transporte USB simulado sin crear un emisor PC, elección explícita de simulación, reproducción sin alterar originales, cierre durante misión/recuperación y escenarios nominal/pérdidas/corrupción/GPS/omisión lógica. El [control final](../../evidence/2026-10-26-laboratorio-qt/control-02.json) conserva resultados y huellas; el control 01 corresponde a la prueba previa a los ajustes de presentación.

Qt se ejecuta con plataforma `offscreen`: renderiza los widgets en memoria sin ventanas en el escritorio ni control de pantalla. Revisé imágenes generadas por la aplicación, incluida la distribución de selección de fuente y simulación activa. Es revisión del renderizado fuera de pantalla, no ensayo físico ni inspección interactiva de la sesión de Windows. La desconexión nueva se verifica con un transporte simulado; no ejecuté una maniobra USB real en esta actualización.

Las dependencias quedan fijadas en requirements-qt.txt. Utilicé un entorno dedicado de ruta corta para evitar el límite de rutas de Windows al instalar Qt. No cambié opciones de seguridad o de escritorio.

## Pendientes

Revisión de uso en la PC con el equipo y ensayo físico de conexión/desconexión de esta interfaz cuando esté disponible la placa. Se mantienen los pendientes de cámaras, circuito/medición de energía, grabación y acuerdos con Edu. No atribuyo a este cambio una prueba RF, sensores reales, autonomía o cumplimiento total del PDR.
