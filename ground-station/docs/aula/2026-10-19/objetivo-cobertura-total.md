# 19/10/2026 — Objetivo de cobertura completa y seguimiento diario

Diario: [ASTRA-37](https://astrateam2026.atlassian.net/browse/ASTRA-37). Amplío el alcance de la [primera revisión](revision-aula.md), sin reemplazarla. El objetivo es investigar el **100% de toda la documentación oficial disponible para nuestra cuenta**, incluidos archivos, anexos, aclaraciones, plantillas, criterios de evaluación y audiovisuales. El objetivo sigue activo; la revisión inicial no acredita cobertura total.

## Cómo demuestro la cobertura

El [inventario inicial](cobertura-inicial.json) separa 17 recursos ya identificados: cuatro archivos, seis debates, cinco páginas de información y dos audiovisuales. Esa cifra es un inventario inicial; no demuestra que no existan más recursos ni que se haya analizado todo su contenido. Se amplía al detectar páginas, adjuntos o materiales nuevos.

Conservo la primera lectura de los cuatro archivos como revisión parcial hasta completar un control exhaustivo por página/diapositiva/criterio, incluidas imágenes y referencias. Los debates y páginas tienen constancia de su lectura textual al corte anterior. Las dos piezas audiovisuales siguen pendientes de análisis íntegro de audio; la reunión de 51:45 no ofrece transcripción accesible en la vía comprobada.

Cada recurso debe tener URL estable, fecha/versión o huella cuando sea archivo, evidencia, estado y pendiente. Para audiovisuales registro segmentos realmente revisados. No declaro 100% por haber descargado archivos, extraído texto, leído títulos o localizado videos; tampoco calculo un porcentaje de contenido dividiendo recursos de tamaños distintos.

Los documentos anunciados y aún no publicados se registran como seguimiento separado. Cuando aparezcan entran al inventario. Una contradicción identificada puede seguir abierta aunque su fuente esté completamente leída: la cobertura no significa que CONAE ya haya aclarado la duda.

## Ampliación de la automatización existente

Actualicé `respaldo-diario-jira-github-groundstation`, ahora llamada **Aula CONAE y respaldo diario · Groundstation**. Conservé ejecución diaria a las **21:00 de Argentina**, estado ACTIVE, chat de destino y política de notificaciones `failed_runs_only`. No creé una segunda automatización.

En cada ejecución revisará el curso oficial, todas sus secciones y páginas de foros, sin depender sólo de mensajes no leídos. Comparará recursos, versiones/huellas, ediciones de respuestas, fechas y condiciones de entrega. Un archivo con el mismo nombre o URL puede haber cambiado. Contadores de leído y tokens de sesión no constituyen novedades.

Si hay novedades o avance real de cobertura, conservará versiones y agregará una entrada en ASTRA-37 con fuente, antes/después, consecuencias y pendientes. Los efectos técnicos se documentarán en su tarea correspondiente. Después respaldará todas mis tareas Jira y registrará el aviso documental en ASTRA-33. Sin cambios ni avances no generará comentarios o commits repetidos.

La sesión autorizada del aula se usa sólo en el sitio oficial. El prompt no contiene la contraseña; tampoco se guardan cookies o enlaces de sesión en documentación. Si no puede acceder o necesita intervención humana, debe informar el impedimento y no afirmar una revisión completada. No enviará consultas, presentaciones, entregas ni marcará actividades manualmente.

Los análisis y sus índices se publican en ground-station/docs/aula/; los originales conservan versiones localmente o en mi carpeta privada autorizada. Los avisos de respaldo siguen en ASTRA-33. No se modifica main ni tareas o carpetas ajenas. La disponibilidad de aplicación, equipo y conexiones sigue siendo una dependencia; esta configuración no acredita una ejecución futura.
