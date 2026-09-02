# Historia gerencial — Conversation Intelligence v0.1

Objetivo: condensar el análisis de conversaciones Mantra → leads Cygnus en un máximo de 2 slides. No reportar métricas como resultados hasta que el pipeline las calcule sobre el universo de PDFs.

## Slide 1 — ¿Mantra logra mantener al lead conversando y llevarlo al siguiente paso?

### Headline dinámico
`De {N_CONVERSATIONS} conversaciones digitales, {REPLY_RATE}% generan respuesta del lead y {VISIT_PROGRESS_RATE}% alcanzan una señal de avance hacia visita/asesor.`

### KPI strip
- Conversaciones analizadas: `N_CONVERSATIONS`
- Leads que responden: `REPLY_RATE%`
- Conversaciones con interacción sostenida (>= 2 turnos del lead): `SUSTAINED_RATE%`
- Invitación a sala emitida: `VISIT_OFFER_RATE%`
- Interés/aceptación de visita: `VISIT_INTEREST_RATE%`

### Visual principal: funnel de progresión
1. Conversaciones iniciadas = 100%
2. Lead responde
3. Lead mantiene conversación
4. Mantra ofrece visita / asesor
5. Lead muestra interés / acepta
6. Handoff o visita confirmada (solo si existe evidencia)

Mostrar tanto N como % sobre la base inicial. No mezclar “oferta de visita” con “aceptación”.

### Mensaje gerencial
Separar el problema en dos preguntas: (1) capacidad de Mantra para activar y sostener la conversación; (2) capacidad para convertir esa conversación en un siguiente paso comercial observable.

## Slide 2 — ¿Qué está funcionando y dónde se pierden oportunidades?

### Headline dinámico
`La principal oportunidad está en {BIGGEST_LEAK_STAGE}; {BIGGEST_LEAK_RATE}% de las conversaciones que llegan a esa etapa no progresan al siguiente estado.`

### Visual A: top motivos/intenciones del lead
Top 5–7 categorías, por ejemplo precio, ubicación, dormitorios, financiamiento, disponibilidad, entrega, promoción. Usar categorías observadas, no imponerlas si el texto no las soporta.

### Visual B: efectividad de respuesta por intención
Para cada intención con base suficiente:
- N conversaciones
- continuation_rate: lead vuelve a escribir después de respuesta Mantra
- visit_progress_rate: posteriormente aparece señal de visita/handoff

La comparación debe indicar tamaño de muestra para evitar interpretar ruido como desempeño.

### Tres hallazgos máximos
Formato obligatorio:
1. **Evidencia:** métrica observada.
   **Implicancia:** qué significa comercialmente.
   **Acción:** cambio concreto de guion/regla/handoff a probar.

### Cierre
`Siguiente decisión: experimentar sobre el mayor punto de fuga y medir uplift en progresión, no solamente calidad textual.`

## Métricas canónicas

- `reply_rate = conversaciones con >=1 mensaje posterior del lead / conversaciones iniciadas`
- `sustained_rate = conversaciones con >=2 turnos del lead / conversaciones iniciadas`
- `visit_offer_rate = conversaciones con invitación explícita a visita / conversaciones iniciadas`
- `visit_interest_rate = conversaciones con respuesta positiva o solicitud de coordinación de visita / conversaciones iniciadas`
- `continuation_after_assistant = respuestas Mantra seguidas por un nuevo mensaje del lead / respuestas Mantra elegibles`
- `handoff_rate = conversaciones con evidencia explícita de transferencia/contacto con asesor / conversaciones iniciadas`

## Guardrails

- “Visita confirmada” requiere evidencia explícita; una invitación no cuenta como conversión.
- Reportar `unknown` cuando el PDF termina antes de conocer el outcome.
- Separar métricas observadas de inferencias semánticas.
- No exponer nombres, teléfonos ni texto identificable en slides gerenciales.
- Mantener vínculo interno de cada agregado con el PDF fuente para auditoría.
- No comparar proyectos/intenciones con bases demasiado pequeñas sin advertencia.

## Evolución posterior

Cuando exista match con Sperant, reemplazar el final del funnel por outcomes CRM observados: visita registrada → separación → minuta. Esto permite medir efectividad comercial real y no solo engagement conversacional.
