# 26/10/2026 — Peralta: recepción, historial y análisis posterior

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Agrego una ficha acotada al [catálogo existente](2026-10-19-catalogo-cansat.csv), sin presentar sus registros como auditorías completas.

## Fuentes y cobertura

Leí completos tres archivos del repositorio publicado por su autor: [README](https://github.com/aron-8/CanSat_peralta/blob/4b57c9679da1f1aecef90cb16ace9b5d8ac1044f/README.md), [GUI](https://github.com/aron-8/CanSat_peralta/blob/4b57c9679da1f1aecef90cb16ace9b5d8ac1044f/ground_station/f%C3%B6ldi_lora_gui.py) y [procesamiento de SD](https://github.com/aron-8/CanSat_peralta/blob/4b57c9679da1f1aecef90cb16ace9b5d8ac1044f/ground_station/sd_feldolgoz.py). Fijé la revisión en `4b57c9679da1f1aecef90cb16ace9b5d8ac1044f`, commit fechado el 26/02/2026. El árbol consultado no estaba truncado. No ejecuté código ajeno ni conecté dispositivos.

El README identifica el proyecto como Peralta/ESA 2025 y describe RP2040, radio de 868 MHz, respaldo SD y análisis aerodinámico. Son afirmaciones del autor: no verifican clasificación oficial, alcance ni éxito de vuelo. En el árbol no encontré registros crudos de misión; sus PDF de diseño y pre-lanzamiento quedaron localizados, no leídos en esta pasada.

## Lo observado en el código

La GUI abre un puerto fijo y programa la lectura serial con el reloj de Kivy. Aunque el README describe lectura y pantalla en hilos separados, el archivo leído usa ese callback para leer, analizar y guardar; los hilos visibles se destinan a secuencias de órdenes. No atribuyo un fallo de vuelo a esta diferencia documental.

La lectura toma los bytes disponibles como un bloque y lo analiza como un mensaje, sin un acumulador de tramas entre llamadas en ese método. Además solicita indicadores de radio con lecturas adicionales y espera dentro del procesamiento. Conserva listas crecientes y vuelve a escribir su representación completa por recepción. Son riesgos de encuadre, bloqueo y crecimiento que requieren ensayos; no medí aquí su impacto.

El procesador de SD separa lectura y análisis posterior: acepta líneas con un prefijo, descarta filas no interpretables y presiones fuera de una ventana fija, calcula una referencia de las primeras diez muestras y aplica filtrado. No encontré en ese archivo un informe de las filas descartadas ni una salida de procedencia por registro. Sin el dataset no puedo decidir si el filtro es adecuado ni validar su altura obtenida.

## Antecedente → riesgo propio → prueba

| Evidencia | Riesgo propio | Prueba útil / situación de ASTRA |
| --- | --- | --- |
| Un bloque disponible se analiza como un mensaje | Perder límites ante fragmentación o ráfagas | Mantener campañas de fragmentación y mensajes concatenados del banco; esta lectura no constituye una prueba nueva |
| Lecturas/esperas auxiliares dentro del callback | Un diagnóstico interrumpe adquisición o dibujo | Ensayar coexistencia de telemetría, controles y destinos lentos; no adoptar llamadas bloqueantes en la GUI |
| Historial creciente reescrito completo | Coste de almacenamiento y memoria aumenta con la misión | Ventanas/colas acotadas y registro incremental propios; repetir campaña prolongada sólo cuando cambie lo relevante |
| Filas omitidas durante análisis posterior | Un gráfico limpio oculta información rechazada | Conservar original, criterio, descartes y procedencia; separar medición, dato inválido y dato filtrado |
| Referencia inicial calculada sobre muestras seleccionadas | Confundir alturas absolutas y relativas | Explicar referencia y unidad; una curva suavizada no acredita precisión de sensor |

Estas propuestas son mi análisis. No importo parámetros RF, filtros ni requisitos de otra competencia; no cambié software ni el ICD por esta revisión. Los resultados propios se consultan en el [banco integrado](../historial/2026-10-26-laboratorio-completo-04.md), con su alcance de software y sus pendientes físicos.

## Referencias visuales y faltantes

Localicé archivos de imagen y documentos en el árbol, registrados en el [catálogo visual nuevo](2026-10-26-catalogo-visual-peralta.csv). No abrí sus píxeles: sus nombres no prueban qué componente muestran, un vuelo real ni su rendimiento. Conservo sólo enlaces, sin descargar ni republicar imágenes. El README declara licencia MIT del proyecto; no verifiqué una autorización individual de esas imágenes.

La búsqueda adicional no aportó en esta pasada un PFR/dataset de Daedalus ni puntuaciones técnicas aplicadas a DJS Arya. Esos faltantes continúan abiertos; no confundo un repositorio de nombre parecido con el ganador. Rotor sigue separado: estos tres archivos no demuestran energía eléctrica generada.
