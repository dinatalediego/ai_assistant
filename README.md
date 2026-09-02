# AI Assistant — Conversation Intelligence Lab

Laboratorio reproducible para analizar conversaciones de Mantra con leads digitales de Cygnus y medir si las respuestas ayudan a mover al lead hacia una conversación con un asesor y una visita a sala de ventas.

## Objetivo

Transformar conversaciones crudas en evidencia operativa:

`mensaje -> conversación -> intención -> calidad de respuesta -> siguiente paso -> visita/handoff -> resultado`

## Uso recomendado

1. Abrir `notebooks/00_drive_inventory.ipynb` en Google Colab.
2. Montar Google Drive y apuntar `DRIVE_ROOT` a `MyDrive/mine_chatbot`.
3. Ejecutar el inventario para descubrir automáticamente formatos y estructura.
4. Ejecutar `01_conversation_overview.ipynb` para métricas descriptivas.
5. Ejecutar `02_response_effectiveness.ipynb` para evaluar progresión, invitaciones a visita, abandono y patrones de respuesta.

## Principios

- Los datos originales permanecen en Drive; el repositorio guarda código y reglas, no conversaciones con PII.
- Primero métricas/reglas reproducibles; NLP/LLM se incorpora después para clasificación semántica donde agregue valor.
- No se considera una respuesta “buena” solo porque suene bien: debe responder la necesidad y facilitar un siguiente paso comercial.

## Estructura

- `notebooks/`: notebooks ejecutables en Colab.
- `src/`: utilidades reutilizables de ingestión y normalización.
- `config/`: taxonomías y reglas de negocio.
- `outputs/`: resultados locales/Colab (no versionados).

## Métricas v0.1

- conversaciones y leads únicos
- mensajes por conversación
- duración de conversación
- tasa de respuesta del lead
- abandono temprano
- quién envía el último mensaje
- invitación a visita
- interés explícito en visita
- handoff a asesor
- progresión conversacional
- preguntas frecuentes e intenciones
- repetición y longitud de respuestas del asistente

> Nota: la primera ejecución de `00_drive_inventory.ipynb` sirve para adaptar el parser al formato real exportado por Mantra antes de declarar métricas definitivas.
