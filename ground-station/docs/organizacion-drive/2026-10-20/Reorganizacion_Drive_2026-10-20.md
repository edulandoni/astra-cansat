# 20/10/2026 — Actualización: Drive organizado por temas estables

Diario: [ASTRA-33](https://astrateam2026.atlassian.net/browse/ASTRA-33). [Mi espacio de groundstation](https://drive.google.com/drive/folders/1A0cwBwNxL71eGML2LtCtk9gcUtgK1u50).

## Problema y resultado

La entrada de Drive seguía orientada al prototipo del 12/10. Las investigaciones, las revisiones del aula y el banco USB habían crecido dentro de documentación general y comparación de reglamentos. Organicé nuestro trabajo por funciones que pueden mantenerse aunque cambien las herramientas: desarrollo, requisitos/aula, decisiones/interfaces, ensayos, investigación, material PDR/video e histórico.

La nueva [entrada de consulta](https://drive.google.com/file/d/12H-VdifFyThzj4Tz-kXOLtM6EO0BBj49/view?usp=drivesdk) identifica el estado al corte y enlaza cada tema. La [pauta de mejora continua](https://drive.google.com/file/d/1CI3WMSbKoRgJsBWNnndZ4AgolJRQ-34V/view?usp=drivesdk) establece cómo incorporar novedades sin reorganizar carpetas en cada avance. El [mapa Drive–Jira–GitHub](https://drive.google.com/file/d/1LIF_YtBnltenTIXojtHhaE4o8xGO4hWM/view?usp=drivesdk) permite ubicar el diario y las evidencias de cada línea de trabajo.

## Qué cambié y por qué

Creé 11 carpetas dentro de mi área, moví 18 elementos y renombré 2 carpetas. Conservo los identificadores y enlaces de los originales. Los dos paquetes históricos se movieron completos sin alterar su interior; la estación v04 queda identificada como antecedente DEPRECATED para la línea actual. El banco USB sigue disponible como herramienta experimental de software; su sintaxis heredada no se convierte en protocolo final por el cambio de ubicación.

Los análisis del aula están en requisitos, los estudios de otros CanSat y rotor en investigación, y la metodología en decisiones. Las fuentes v1/v2 conservan nombre y versiones. La comparación del 17/10 permanece en su carpeta fechada con los manifiestos originales; el nuevo registro explica las ubicaciones que cambiaron desde aquella captura. Los estados del 12 y 13/10 y el antiguo instructivo se conservan como históricos.

Publiqué 17 archivos: 9 guías nuevas, 6 copias de consulta de documentos versionados, un paquete de evidencias/experimentos y un registro de movimientos. Las copias conservan fecha y texto originales; convierto los enlaces locales en enlaces al commit revisado y agrego una nota de procedencia. Las claves antiguas dentro de esos textos siguen siendo históricas: el mapa nuevo indica la tarea temática actual.

El paquete de PC reúne 39 archivos originales de evidence/ y experiments/, con manifiesto SHA-256 y estructura de carpetas. No contiene datos de vuelo real ni nuevas pruebas ejecutadas hoy. Para reproducirlo uso el banco del commit 51c475eb2df8cf2ab5317c5e03455f8ad7c4b729. No representa una descarga completa del repositorio ni acredita hardware.

## Mantenimiento diario

Amplié las instrucciones de la automatización existente para usar estos identificadores de Drive y publicar sólo análisis nuevos fechados en su tema. Mantengo su frecuencia diaria de las 21:00 de Argentina, estado ACTIVE y configuración de notificaciones anterior. Verifiqué el cambio guardado; esto no prueba una ejecución futura. La documentación oficial de [tareas programadas](https://developers.openai.com/training/walkthroughs/scheduled-tasks) explica la edición de una tarea existente y la necesidad de mantener la computadora y aplicación activas cuando se usan archivos locales.

El respaldo completo de Jira continúa en GitHub; Drive enlaza ese historial y su explicación, sin generar una segunda copia diaria redundante. No publico cambios por contadores de lectura ni por contenidos sin novedades. La estructura se revisa ante una confusión real o al preparar un hito, conservando entradas y versiones anteriores.

## Verificación y límites

Comprobé nombres y padres de los 17 archivos nuevos. Releí completos los 15 Markdown y comparé su contenido; comprobé igualdad semántica del JSON y SHA-256 del ZIP remoto. Verifiqué los 39 archivos del ZIP contra su manifiesto y los 20 cambios de metadatos. Sólo utilicé operaciones de movimiento/nombre para los originales, sin reemplazar sus bytes. El [registro de movimientos](https://drive.google.com/file/d/1HzmyHC56TMmEU8mlIeICc2xucVqjt9JP/view?usp=drivesdk) conserva padres anteriores y nuevos para reconstruir o revertir las ubicaciones.

No cambié permisos, responsables, estados, descripciones o comentarios anteriores de Jira, main, protocol/ ni las carpetas generales HARDWARE y DOCUMENTOS. Las mejoras pendientes del software, la identificación de la placa, el TEAM_ID, el acuerdo de interfaz y las pruebas físicas continúan pendientes. Ordenar evidencia no resuelve esas tareas ni agrega una validación nueva.

## Archivos de consulta publicados

| Archivo | Tipo |
| --- | --- |
| [00_EMPEZAR_ACA_2026-10-20.md](https://drive.google.com/file/d/12H-VdifFyThzj4Tz-kXOLtM6EO0BBj49/view?usp=drivesdk) | guia |
| [Mantenimiento_y_mejora_continua_2026-10-20.md](https://drive.google.com/file/d/1CI3WMSbKoRgJsBWNnndZ4AgolJRQ-34V/view?usp=drivesdk) | guia |
| [Mapa_Drive_Jira_GitHub_2026-10-20.md](https://drive.google.com/file/d/1LIF_YtBnltenTIXojtHhaE4o8xGO4hWM/view?usp=drivesdk) | guia |
| [Desarrollo_y_banco_USB_2026-10-20.md](https://drive.google.com/file/d/1V22bAxp2p7CfRRPXy0tF3X1WKu5_lmme/view?usp=drivesdk) | guia |
| [Requisitos_fuentes_y_pendientes_2026-10-20.md](https://drive.google.com/file/d/18f7j--mGYvyaIkXE4ntVa9wrJUvQkufe/view?usp=drivesdk) | guia |
| [Historico_y_DEPRECATED_2026-10-20.md](https://drive.google.com/file/d/1LrhGfuercaFtbWMkDHTgNRuSJQK0bZkU/view?usp=drivesdk) | guia |
| [Investigacion_y_estado_de_las_ideas_2026-10-20.md](https://drive.google.com/file/d/1qfDXLtABcSzrIQQSNry1O0dk1WwH50Q7/view?usp=drivesdk) | guia |
| [Ensayos_evidencia_y_reproduccion_2026-10-20.md](https://drive.google.com/file/d/1FMIqxAZqkdamJMJ1ObIlpMjkH3cictql/view?usp=drivesdk) | guia |
| [Material_PDR_y_video_2026-10-20.md](https://drive.google.com/file/d/1EwFMrUSZiGu_atCcs1zzDbjkYfCeBI2t/view?usp=drivesdk) | guia |
| [pendientes-groundstation-2026-10-19.md](https://drive.google.com/file/d/16HjPLx0ZMEbL0WdGY1lDWt8jv_e0I3rc/view?usp=drivesdk) | copia_consulta |
| [metodologia-2026-10-19.md](https://drive.google.com/file/d/1yoskwMYdTVN5KPfzVKdPSEZRRXY1cYwe/view?usp=drivesdk) | copia_consulta |
| [2026-10-19-innovacion-y-prevencion.md](https://drive.google.com/file/d/1b01Qc7DAqaV8GyF8z_vSYI0Awmmb96Af/view?usp=drivesdk) | copia_consulta |
| [2026-10-19-resiliencia-y-recuperacion.md](https://drive.google.com/file/d/1-uOQrEel2tuwk48ZgtxhgpxgkEa5nWSp/view?usp=drivesdk) | copia_consulta |
| [pruebas-2026-10-19.md](https://drive.google.com/file/d/1v8u_g9v9e9b2qoAf5Nu1Df1pvaNWE4pb/view?usp=drivesdk) | copia_consulta |
| [v1-v2-groundstation-2026-10-19.md](https://drive.google.com/file/d/1ORgTrnnD88SJ4IgM_b0T2sgaNnEQbmz-/view?usp=drivesdk) | copia_consulta |
| [Evidencias_y_experimentos_PC_2026-10-19.zip](https://drive.google.com/file/d/1iivBri2-v-b6dQeOi7q9KId0zxaM8ACf/view?usp=drivesdk) | evidencia |
| [Registro_movimientos_Drive_2026-10-20.json](https://drive.google.com/file/d/1HzmyHC56TMmEU8mlIeICc2xucVqjt9JP/view?usp=drivesdk) | registro |

Los [identificadores y huellas de publicación](Publicaciones_Drive_verificadas_2026-10-20.json) y el [registro completo de movimientos](Registro_movimientos_Drive_2026-10-20.json) respaldan esta actualización. La copia local de estos documentos queda versionada en groundstation; las publicaciones nuevas enlazan esta tarea y sus fuentes.
