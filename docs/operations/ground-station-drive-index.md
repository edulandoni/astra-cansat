# Ground Station — ASTRA CanSat
Autor: Cristian Ponsone. Actualizado: 12 de octubre de 2026.

Me encargo de recibir, registrar y mostrar los datos del CanSat, y de la interfaz para enviar telecomandos. Mantengo el código y los contratos compartidos en [GitHub](https://github.com/edulandoni/astra-cansat). Esta carpeta reúne el material original, las decisiones, las evidencias y las entregas de Ground Station.

## Cómo retomar

1. Leer la revisión actual en **03_Documentacion_y_decisiones**.
2. Para revisar la estación, usar **01_Archivo_original_2026-10-12 / CanSat_UTN_FRD_2026-2027 / Iteracion_04 / Estacion_simulada**. Mantener también su carpeta hermana **Referencias**.
3. Para revisar cálculos y presupuesto, usar **Iteracion_05** del mismo paquete. El laboratorio es una aplicación separada.
4. Consultar el protocolo acordado en **protocol/** del repositorio. Al corte de esta revisión sigue pendiente de definición.

## Organización

| Carpeta | Contenido y uso |
| --- | --- |
| [01_Archivo_original_2026-10-12](https://drive.google.com/drive/folders/1fP87iRnI99sJf3BuwS-V5zAXWfBRCnYM) | Paquete de traspaso, versiones históricas, fuentes y aplicaciones. Conservar sus contenidos sin sobrescribirlos. |
| [02_Estacion_simulada_v04_original](https://drive.google.com/drive/folders/1czmyjIeHlK3XrtRwmsIABAQj-74LC8Eb) | Copia independiente recibida. No incluye todas las referencias enlazadas por la ayuda. Preferir el paquete completo para ejecutarla. |
| [03_Documentacion_y_decisiones](https://drive.google.com/drive/folders/1i523f6PGiS5qzzRei1rGly_dQpq7r40M) | Estado actual, arquitectura, interfaces, consultas y decisiones con fecha. |
| [04_Ensayos_y_resultados](https://drive.google.com/drive/folders/13_8vXCp0y_ZmDmbBt74g-o_noXORcOKM) | Registros originales de ensayos, configuración, resultados y evidencia. |
| [05_Entregables](https://drive.google.com/drive/folders/1t_MY6pQ0dQlwyEijGzghcCDUrdUNqTSH) | Versiones preparadas para compartir o entregar, identificadas por fecha y versión. |

## Criterios de trabajo

- El reglamento y sus aclaraciones oficiales definen los requisitos. Los textos del traspaso son antecedentes y propuestas.
- Cada decisión registra motivo, fuente, fecha, estado y prueba que la respalda.
- Separar datos simulados, ensayos de banco y vuelo. No sobrescribir originales.
- Conservar el registro recibido y guardar los cálculos derivados por separado.
- Código y contratos: Git. Archivos y evidencia: Drive. Seguimiento de tareas: Jira cuando esté disponible y verificado.
- La documentación se redacta desde mi responsabilidad dentro del proyecto. No contiene narración del chat.
- La estación actual es un prototipo de simulación: no recibe radio real ni realiza respaldo automático a disco.
