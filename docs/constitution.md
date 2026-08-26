# Constitution — Jorbit

> Documento de nivel 1. Define **por qué** existe el proyecto y **qué es innegociable**.
> No define features (ver `docs/spec.md`) ni implementación (ver `ARCHITECTURE.md`).
> Cambiar este documento requiere aprobación explícita del owner.

- **Producto:** Jorbit (Job + Orbit)
- **Repositorio:** `jorbit-webmcp`
- **Owner:** Daniel Gambin (desarrollador humano único)
- **Estado:** **v0.3 — APPROVED / FROZEN**
- **Fecha:** 2026-08-26
- **Contexto de entrega:** OpenAI WebMCP Challenge

---

## 1. Problema

Las plataformas de empleo actuales obligan al candidato a **saber de antemano qué buscar**.
El usuario escribe el job title que cree que le corresponde, y el sistema devuelve
coincidencias para esa consulta. Las oportunidades que el candidato no sabe nombrar
nunca entran en el conjunto de resultados.

El resultado es un techo invisible: alguien que se identifica como "Project Coordinator"
busca "Project Coordinator", y nunca descubre que su experiencia ya satisface la mayor
parte de "Implementation Specialist", "Customer Success Operations" o "Revenue Operations".

Formulado como la frustración real:

> "Tengo un CV y sé lo que he hecho, pero para buscar trabajo tengo que adivinar job
> titles, keywords y filtros. Las oportunidades que no sé que existen nunca aparecen."

## 2. La pregunta que responde el producto

Los productos existentes (LinkedIn, Simplify, Jobright) optimizan **matching**:

> "How well do you match this job?" → un feed ordenado 92% / 87% / 81%.

Jorbit optimiza **descubrimiento contrafactual**:

> **"What becomes possible if one variable changes?"**

### 2.1 Regla de identidad

> **Jorbit should never tell you only what jobs you match. It should explain what is just
> outside your current orbit — and why.**

Esta frase es el test de identidad del producto. Una feature que no la honra no es Jorbit.

### 2.2 La cadena conceptual

Toda decisión del proyecto debe poder situarse en esta cadena. Lo que la contradice, se
señala y se resuelve antes de implementarse.

```text
PROBLEM
"I don't know what jobs I should search for."
        ↓
JORBIT
"What exists just outside my orbit?"
        ↓
COUNTERFACTUAL
"What changes if I change X?"
        ↓
EVIDENCE
"These exact opportunities become reachable."
        ↓
HUMAN
"Is that trade-off worth it to me?"
```

### 2.3 Forma de las salidas

Ejemplos **ilustrativos** de la clase de salida que caracteriza al producto. Las cifras y la
variable concreta de cada ejemplo son placeholders: cuál de ellas es demostrable con datos
reales lo decide el Data Coverage Audit (§11.2), no este documento.

- "Remote-only is hiding N opportunities where your profile has high fit."
- "Lowering your minimum salary from $90k to $80k reveals N additional jobs."
- "SQL unlocks N opportunities."
- "You searched for Customer Success, but your profile is also surprisingly close to
  Implementation Consultant, Product Operations and Revenue Operations."

## 3. Para quién

| Consumidor | Quién es | Qué hace |
|---|---|---|
| **Primario** | Job seeker **no técnico** | Decide qué trade-offs acepta |
| **Secundario** | Su agente de IA (ChatGPT vía WebMCP) | Interpreta el CV, explora, itera restricciones |

La tesis del producto es que los tres actúan sobre **el mismo sistema a la vez**. Ninguno es
suficiente solo:

```text
Agent  = intelligent interpreter        (lenguaje, CV, intención)
Jorbit = specialized opportunity engine (datos, taxonomía, cálculo, evidencia)
Human  = trade-off arbiter              (qué precio está dispuesto a pagar)
```

**El agente es externo a Jorbit.** Jorbit no lo contiene, no lo embebe y no lo sustituye:

```text
External AI agent / ChatGPT
            ↕
          WebMCP
            ↕
          Jorbit
            ↕
   opportunity engine + UI
```

> **Jorbit is not an AI chatbot. Jorbit is a visual, specialized opportunity engine that an
> external AI agent can operate through WebMCP — and that remains manually usable without it.**

## 4. Definición de éxito

### 4.1 La prueba de los 60 segundos (criterio primario)

> Después de 60 segundos, el usuario descubre **al menos una posibilidad profesional que
> no habría pensado buscar**, y entiende **exactamente qué la hace alcanzable**.

Esta prueba es el árbitro de todas las decisiones de alcance. Si una feature no sirve a
este momento, no entra en v1.

### 4.2 Éxito de entrega (hackathon)

Submission completa y competitiva antes del **3 sep 2026, 1:00pm PT (3:00pm COT)**.

### 4.3 Éxito posterior (no compromete v1)

Decenas de testers reales; validar si el concepto sostiene un producto más allá del demo.

## 5. Principios innegociables

Cada principio es **falsable**: se puede señalar una violación concreta.

**P1 — Agent-native, no agent-added.**
Toda **acción de dominio** útil para un agente se expone vía WebMCP. La UI y las tools operan
sobre el **mismo estado de aplicación y la misma lógica de dominio** — no son dos caminos con
capacidades distintas.

Acciones de dominio (ejemplos): `set_candidate_profile`, `search_opportunities`,
`debug_constraints`, `inspect_unlock`, `compare_career_worlds`.

Las interacciones puramente visuales — zoom, colapsar un panel, cambiar layout, animaciones,
leyenda — **no** necesitan tool. Exponerlas sería ruido para el agente.

WebMCP no puede ser decorativo ni una capa superficial añadida al final.
*Violación:* una capacidad de dominio que solo se puede usar haciendo clic; o tools que
duplican lógica en vez de compartirla con la UI.

**P2 — Contrafactual sobre matching.**
El producto responde "qué cambia si...", no "qué tan compatible eres". Un score de
compatibilidad aislado no es una salida válida del producto.
*Violación:* una pantalla cuyo valor principal es una lista ordenada por % de match.

**P3 — Evidence over hallucination.**
Cada score, constraint y unlock que Jorbit muestra debe ser trazable a datos concretos:
el perfil, un job posting real, o la taxonomía. El LLM del agente externo puede
**interpretar**; no puede **inventar evidencia**.

Regla operativa, la más importante del producto:

> Jorbit nunca muestra un número de unlock que no pueda reconstruir a partir del conjunto
> actual de jobs + la taxonomía.

Corolarios:

- Cada resultado declara por qué aparece; cada bloqueo declara qué restricción lo causa y
  qué la levantaría. Sin números opacos.
- **Un Skill Unlock solo puede contar una oferta cuando existe evidencia suficientemente
  fuerte para reconstruir por qué esa skill la bloquea.** Encontrar la palabra "SQL" en una
  descripción no establece por sí solo si SQL es *required*, *preferred*, o simplemente
  *mentioned*. Una mención ambigua **no** incrementa un número.
- De ahí que la representación interna de skills sea de **evidencia**, no una clasificación
  binaria: qué skill, qué texto lo respalda, qué nivel de requisito y con qué confianza. El
  esquema concreto se define en `docs/spec.md`.

*Violación:* mostrar "27 roles unlocked" sin poder enumerar esos 27 y citar la evidencia de
cada uno.

**P4 — No external side effects in v1.**
Jorbit y el agente **aconsejan**; el humano controla toda acción hacia terceros. Jorbit nunca
envía, publica ni presenta una candidatura ante un tercero sin una acción explícita posterior
del usuario. La generación privada está permitida; el efecto externo no.

| Permitido | Prohibido |
|---|---|
| Abrir la oferta original | Auto-apply |
| Explicar fit | Enviar formularios |
| Explicar gaps | Escribir a reclutadores |
| Generar estrategia de aplicación | Mensajes de LinkedIn |
| Generar un draft privado | Publicar |
| Sugerir ajustes de CV | Enviar emails |
| | Actuar externamente en nombre del usuario |

*Violación:* una tool que produce un efecto fuera de la sesión del usuario.

**P5 — Datos personales mínimos por diseño.**
Un CV es dato personal. En v1: sin cuentas, sin multi-tenant, perfil en cliente/sesión,
sin persistencia permanente del CV salvo que el usuario lo pida explícitamente. Los datos
agregados de oportunidades sí viven en servidor.
*Violación:* un CV que sobrevive a la sesión sin acción deliberada del usuario.

**P6 — Agent-enhanced, not agent-dependent.**
La mejor experiencia ocurre con WebMCP + agente, pero las funciones fundamentales tienen un
fallback manual mínimo, de modo que Jorbit sigue siendo una web usable por sí sola. Y sin
WebMCP disponible, la app **dice claramente** que el modo agente no está disponible en ese
navegador. Nunca simular un agente conectado, nunca fingir tool-calls.
*Violación:* un demo que aparenta interacción con agente cuando no la hay; o una app que es
una pantalla muerta sin agente.

**P7 — Datos reales y de procedencia declarada.**
Las ofertas son reales, vía APIs públicas y documentadas, con fuente y enlace original citados,
respetando las condiciones y la atribución de cada fuente. Nada de scraping. Cuando se sirve
desde caché o snapshot, la UI lo indica con su antigüedad. La taxonomía lleva su atribución de
licencia.
*Violación:* una oferta inventada, o una caché presentada como dato en vivo.

**P8 — Presupuesto cercano a $0, sin LLM de pago obligatorio.**
El razonamiento en lenguaje natural lo aporta el agente **externo** del usuario (ChatGPT);
Jorbit aporta tools, datos y lógica especializada. Jorbit no incorpora un LLM propio, de pago
ni gratuito (§8). Otras APIs de pago pueden añadirse como mejora, nunca como requisito para
que el demo funcione.
*Violación:* el demo deja de funcionar si se agota una API key.

**P9 — Open source real.**
Repositorio público, licencia MIT detectable en la sección About desde el primer commit público.

**P10 — Vertical slice temprano y siempre desplegable.**
Existe una URL pública funcional lo antes posible, verificada en el navegador objetivo real,
y se mantiene funcional cada día. La integración no se deja para el final. La primera
milestone técnica del proyecto está definida en §11.1.
*Violación:* llegar al día 6 sin haber visto la app corriendo en el navegador de los jueces.

**P11 — Discovery over application automation.**
El propósito central de Jorbit es ampliar el espacio de oportunidades que una persona
entiende que tiene. Si una feature no mejora **discovery**, **understanding** o
**decision-making**, está fuera del alcance de v1.
*Violación:* tiempo invertido en automatizar el acto de aplicar en vez de en entender el espacio.

**P12 — Depth over breadth.**
Preferimos pocos roles con relaciones, evidencia y unlocks creíbles antes que muchos roles
parcialmente soportados. La credibilidad de un unlock es el producto; la cobertura no lo es.
*Violación:* ampliar el universo de análisis a costa de la calidad de la evidencia.

## 6. Restricciones duras

Solo restricciones innegociables de producto y entrega. Los detalles técnicos volátiles
—versiones de navegador, firmas de API concretas, mecanismo de acceso a datos— se documentan
en `ARCHITECTURE.md`, donde pueden actualizarse sin tocar la constitución.

| # | Restricción | Origen |
|---|---|---|
| R1 | Deadline **3 sep 2026, 1:00pm PT / 3:00pm COT**. | Devpost |
| R2 | Debe funcionar en el navegador in-app de ChatGPT **o** Chrome con WebMCP habilitado. | Devpost |
| R3 | Jorbit **debe usar la API WebMCP vigente soportada por el navegador/runtime objetivo del challenge**. La firma exacta vigente se documenta y mantiene en `ARCHITECTURE.md`. | Spec W3C |
| R4 | **HTTPS obligatorio** — la API WebMCP solo existe en contexto seguro. | Runtime |
| R5 | Entregables: live URL, descripción de texto, video YouTube público **<3 min con audio**, repo público con licencia OSS visible en About. | Devpost |
| R6 | Un solo desarrollador humano + agentes de IA. ~8 días de calendario. | Recurso |
| R7 | Presupuesto ≈ $0. | Owner |
| R8 | Stack cerrado: **TypeScript + React/Next.js**. Persistencia solo si es imprescindible. | Owner |
| R9 | Ofertas exclusivamente vía **APIs públicas y documentadas**, respetando sus condiciones y atribución. Scraping prohibido. | Owner |
| R10 | Taxonomía base: **O\*NET**, con su atribución de licencia. ESCO queda para expansión futura. | Owner |
| R11 | Sin i18n en v1. Código, UI, demo, README y nombres de tools en **inglés**. | Owner |

## 7. Decisiones cerradas

Tomadas y no reabiertas sin aprobación explícita.

### 7.1 Estrategia de datos de empleo

Arquitectura conceptual **multi-source con modelo normalizado único**:

```text
Browser / Jorbit UI / WebMCP
            ↓
      Jorbit backend
            ↓
     normalized adapters
            ↓
        Job APIs
            ↓
      cache / snapshot
```

**Fuentes candidatas aprobadas** — APIs públicas y documentadas que permiten obtener ofertas
sin scraping y sin coste obligatorio para v1. **No se ha realizado una revisión legal formal**
de sus términos, licencias o condiciones de redistribución; una API pública no equivale a
validación legal para cualquier uso. Se respetan las condiciones y la atribución aplicables de
cada fuente, y esa revisión queda pendiente antes de cualquier uso comercial (ver RK10).
**No hay jerarquía primary/secondary/fallback congelada.**

| Fuente | Qué aporta | Nota |
|---|---|---|
| **JobsCollider** | Empleos remotos con descripción completa, categoría, seniority, salario min/max, ubicaciones, fecha, URL original | Orientada a remoto |
| **Arbeitnow** | Agrega desde ATS reales (Greenhouse, SmartRecruiters, Teamtailor, Recruitee, Comeet). Sin API key. Señal de `remote` y de **visa sponsorship**. Cobertura EU/UK | Única candidata con cobertura no-remota significativa y señal de visa |
| **Jobicy** | Remoto internacional, sin API key, jobLevel, tipo de empleo, geografía, descripción completa, salarios estructurados cuando existen | Orientada a remoto |

**Por qué no se congela la jerarquía:** JobsCollider y Jobicy son ambas fuentes de *remote
jobs*. Un universo donde casi toda oferta ya es remota no puede sostener un contrafactual
sobre la variable `remote`. Cuál es la fuente principal, y cuál es la variable estrella del
demo, se decide **después** del Data Coverage Audit (§11.2), con porcentajes reales de
cobertura por campo — no con lo que el schema declara posible.

**Resiliencia:** se mantiene un snapshot cacheado de las mismas APIs. Las ofertas son reales,
pero el demo no se rompe si una API cae. Sujeto a P7 — la caché se etiqueta con su antigüedad.

**Acceso server-side (confirmado):** las APIs de empleo se consumen desde el backend de Jorbit,
nunca directamente desde el navegador. Motivos: CORS, caching, normalización, rate limiting,
fallback, atribución de fuente y resistencia a cambios de schema. El mecanismo concreto
(Route Handlers, Server Actions u otro) se documenta en `ARCHITECTURE.md`.

**Modelo normalizado:** todas las fuentes se normalizan a un modelo `Job` único con campos de
fuente, puesto, clasificación, ubicación/remoto/visa, salario estructurado y fecha, más campos
**derivados por Jorbit** — mapeo a ocupación y **evidencia de skills** (P3), no una lista plana
de skills requeridas. El esquema canónico se define en `docs/spec.md`.

### 7.2 Los dos tipos de Unlock

Distinción fundamental: tienen coste de implementación y nivel de confianza distintos.

| Tipo | Ejemplo | Cómo se computa | Confianza |
|---|---|---|---|
| **Constraint Unlock** | "Relaxing constraint X reveals N jobs" | Re-filtrado contrafactual directo sobre campos estructurados del conjunto de jobs | Alta — determinista |
| **Skill Unlock** | "SQL unlocks N opportunities" | Requiere segunda capa: extraer evidencia de requisitos desde la descripción y matchearla contra la taxonomía | Menor — depende de la calidad de la evidencia |

**Prioridad congelada:**

> Constraint Unlocks = núcleo demostrable **garantizado**.
> Skill Unlocks = objetivo ambicioso pero **degradable**.

**No está congelado cuál constraint es la estrella del demo.** Candidatas: remote, salary,
seniority, location, visa, u otra restricción estructurada. La regla de decisión es:

> Elegimos para el demo el Constraint Unlock que tenga datos reales suficientes y produzca
> el contrafactual más convincente.

Se resuelve con el Data Coverage Audit (§11.2). Ambos tipos están sujetos a P3: si el número
no se puede reconstruir, no se muestra.

### 7.3 Universo de análisis v1

Jorbit **no** es conceptualmente "solo para Operations". Pero el motor de análisis de v1 se
restringe deliberadamente, por P12.

- **Se ingieren** ofertas de muchas categorías.
- **Se da análisis de alta confianza** sobre **~10–20 role archetypes** de tech knowledge-work.

Familia de referencia (lista ilustrativa, no congelada): Project Coordinator, Project Manager,
Program Manager, Customer Success Specialist, Customer Success Manager, Customer Success
Operations, Implementation Specialist, Implementation Consultant, Business Operations,
Product Operations, Revenue Operations, Business Analyst, Data Analyst, Operations Analyst.

Elegidas porque sus habilidades se cruzan mucho entre sí: es donde el concepto de órbita y de
unlock tiene densidad real. Post-hackathon el universo puede crecer a otros verticales.

### 7.4 Taxonomía

Tres capas, de la más estable a la más específica:

```text
O*NET             = conocimiento base (ocupaciones, skills, knowledge, abilities,
                    technology skills, títulos alternativos, ocupaciones relacionadas)
Jorbit mappings   = aliases y adaptación al mercado tech moderno
                    "CS Ops" / "Customer Success Operations" / "Customer Operations" → occupation
Job description   = evidencia de esa oferta concreta
```

### 7.5 Onboarding del perfil

El agente interpreta el CV; **Jorbit no construye un CV parser propio**.

```text
Usuario da el CV al agente → el agente lo entiende
→ llama set_candidate_profile({ skills, experienceYears, roles, industries, preferences })
→ Jorbit computa el universo de oportunidades
```

Fallback obligatorio por P6: formulario manual mínimo — current role, skills, experience,
location, remote preference, salary. **No se construye un segundo CV parser.**

### 7.6 Hosting

**Vercel.** Next.js nativo, HTTPS, rutas server-side, free tier suficiente, mínima fricción
operativa. No se evalúan alternativas salvo blocker concreto.

## 8. No-objetivos de v1

Explícitamente fuera de alcance. Añadir cualquiera requiere aprobación y cambio de este documento.

- **Auto-apply**, envío de formularios, contacto con reclutadores, cualquier side effect externo.
- **Scraping** de cualquier fuente.
- **Cobertura exhaustiva** de bolsas de empleo.
- **CV parser propio** — lo hace el agente (§7.5).
- **Chatbot embebido, copilot, prompt box, sidebar conversacional, floating chat bubble o
  "Jorbit AI Assistant"** en cualquier forma.
- **LLM o agente propiedad de Jorbit.** El agente es externo a la aplicación e interactúa con
  Jorbit a través de WebMCP (§3). Jorbit no razona en lenguaje natural: calcula, busca,
  compara y evidencia.
- Cuentas de usuario, autenticación, multi-tenant, perfiles persistentes.
- i18n / multi-idioma. ESCO.
- Servidor MCP tradicional, o un navegador/agente que controle webs de terceros.
- Extensión de navegador propia. CLI. Desktop.
- Infraestructura para escala superior a ~1.000 usuarios.

## 9. Criterios de desempate

Cuando dos opciones compiten y el tiempo es escaso:

1. **¿Sirve a la prueba de los 60 segundos?** (§4.1)
2. **¿Aumenta WebMCP Leverage?** — primer criterio del jurado; una implementación trivial de
   WebMCP hunde la submission por buena que sea la app.
3. **¿Es demostrable en <3 minutos de video?** Lo que no cabe en el video no compite.
4. **¿Reduce riesgo de entrega?** Ante empate, gana lo que se puede terminar antes.
5. **Menos código gana.** Ante empate real, la opción más pequeña.

Alineación con los criterios publicados del jurado:

| Criterio del jurado | Cómo lo atacamos |
|---|---|
| WebMCP Leverage | P1 + §7.5: el producto **es** su superficie de tools; el agente es intérprete, no adorno |
| Execution | P10 + §11.1: vertical slice verificado temprano, producto coherente y no PoC |
| Potential Impact | §1–§2: problema nombrado, audiencia nombrada, mecanismo específico |
| Creativity & Ambition | P2 + §2.1: descubrimiento contrafactual, categoría distinta al matching |

## 10. Riesgos aceptados

| # | Riesgo | Severidad | Postura |
|---|---|---|---|
| RK1 | **La API WebMCP es un draft en movimiento.** Su superficie ha cambiado recientemente y puede volver a hacerlo dentro del plazo. | Alta | Aislar el registro de tools tras una capa fina y propia. Mantener la firma vigente documentada en `ARCHITECTURE.md`, no en la constitución. Verificar contra el runtime real, no contra la documentación. |
| RK2 | **Host/runtime variance.** El navegador in-app de ChatGPT es target oficial con soporte WebMCP, pero tool discovery, invocation, lifecycle y comportamiento pueden diferir respecto a Chrome con WebMCP habilitado. | **Alta** | Validar un vertical slice real directamente en ChatGPT desde el día 1 (§11.1). No asumir que lo observado en Chrome será idéntico. |
| RK3 | **Extracción de evidencia de skills desde descripciones.** Cuello de botella de los Skill Unlocks y, sin LLM de pago (P8), debe ser determinista y trazable. Una extracción pobre degrada el mensaje central. | **Alta** | P3 es el freno: si la evidencia no sostiene un número, se muestran Constraint Unlocks, que sí son deterministas. Los Constraint Unlocks solos ya pasan la prueba de los 60 segundos. |
| RK4 | **Dependencia de APIs de terceros** sin SLA: caída, rate limit, cambio de esquema. Y sesgo de cobertura: dos de las tres candidatas son remote-only. | Media | Multi-source por diseño + snapshot de respaldo (§7.1). El Data Coverage Audit (§11.2) mide el sesgo antes de comprometer la variable del demo. |
| RK5 | **El concepto puede no necesitar WebMCP.** Si un chatbot + buscador reproduce la experiencia, WebMCP no aporta nada esencial. | Media | Condición de pivote declarada por el owner. Se evalúa contra §4.1 antes del día 4. |
| RK6 | **Alcance excesivo para 8 días**: multi-source + taxonomía + evidencia + 5 tools + UI orbital. | **Alta** | §9 como árbitro. P12 reduce el universo. Las tools y las fuentes se priorizan; ninguna se entrega por defecto. |
| RK7 | **Densidad del universo estrecho.** Reducir a ~10–20 archetypes (P12) reduce el pool de ofertas analizables; un pool pequeño produce números de unlock poco impresionantes ("unlocks 2 opportunities"). Depth y magnitud tiran en direcciones opuestas. | **Alta** | El Data Coverage Audit debe medir **cuántas ofertas reales mapean a los archetypes elegidos**, no solo la cobertura de campos. Si el pool es demasiado pequeño, se amplía el conjunto de archetypes o se amplían las fuentes — pero nunca se infla el número violando P3. |
| RK8 | **Sesgo y daño en recomendaciones de carrera.** Sugerir roles inalcanzables o reforzar sesgos del dataset perjudica a un usuario real. | Media | P3: evidencia obligatoria; el usuario ve el razonamiento y puede rechazarlo. |
| RK9 | **CV como dato personal** en una app pública sin cuentas. | Media | P5: minimización por diseño. |
| RK10 | **Marca "Jorbit" ya usada** por otros proyectos públicos (paquete científico, Jorbit Technologies). | Baja | No bloqueante para el hackathon. Verificar marca y dominio antes de cualquier uso comercial. |

## 11. Verificaciones bloqueantes

Deben completarse **antes** de cerrar `docs/spec.md`. Ninguna se marca como superada sin
confirmación explícita del owner.

### 11.1 WebMCP vertical slice — primera milestone técnica

Antes de implementar O\*NET, integrar las APIs de empleo, construir o integrar la **UI de
producción**, el motor de Skill Unlocks, o cualquier lógica de producción que dependa de
WebMCP, debe verificarse end-to-end:

```text
minimal Jorbit page
        ↓
register one trivial WebMCP tool
        ↓
deploy to Vercel
        ↓
open in target ChatGPT browser
        ↓
agent discovers tool
        ↓
agent invokes tool
        ↓
visible UI/state change
```

**Estado: NO VERIFICADO.** Hasta ver esto funcionar end-to-end en el navegador objetivo,
RK1 y RK2 siguen plenamente activos y ninguna estimación posterior es fiable.

**Design exploration and prototyping may proceed in parallel** — no alteran la arquitectura de
producción ni bloquean la validación de WebMCP.

| Track A — Engineering (bloqueado por 11.1) | Track B — Design (libre desde ahora) |
|---|---|
| Integración de job APIs | Product design exploration, Claude Design |
| O\*NET runtime work | Identidad visual, design system |
| UI de producción e integración con estado real | UX exploration, mockups, prototipos visuales interactivos |
| Arquitectura compleja de frontend | Conceptos de Career Orbit |
| Skill Unlock engine | Conceptos de Constraint Debugger |
| Lógica de producción dependiente de WebMCP | Conceptos visuales de Opportunity Unlock, motion/animación |

```text
TRACK A — ENGINEERING          TRACK B — DESIGN

WebMCP vertical slice          Visual exploration
Data Coverage Audit            Design system
                               Career Orbit UX
                               Constraint Debugger
                               Opportunity Unlocks

          ↓                         ↓
               INTEGRATION
```

Ni el track técnico espera al diseño, ni el diseño espera a ingeniería.

### 11.2 Data Coverage Audit

Medir cobertura **real** —no lo que el schema permite— sobre JobsCollider, Arbeitnow y Jobicy:

```text
                        JobsCollider   Arbeitnow   Jobicy
jobs (total)                  ?             ?          ?
description                   ?%            ?%         ?%
salary (structured)           ?%            ?%         ?%
seniority                     ?%            ?%         ?%
remote                        ?%            ?%         ?%
location                      ?%            ?%         ?%
visa sponsorship              ?%            ?%         ?%
employment type               ?%            ?%         ?%
category / occupation map     ?%            ?%         ?%
jobs mapping to archetypes    ?             ?          ?     ← RK7
```

**Estado: NO EJECUTADO.** Su salida determina tres decisiones aún abiertas: fuente principal,
variable estrella del Constraint Unlock, y si el universo de ~10–20 archetypes produce pool
suficiente.

## 12. Supuestos declarados

Se asumen ciertos hasta que el owner los confirme o corrija.

- **S1** — Los Constraint Unlocks son el núcleo demostrable garantizado; los Skill Unlocks son
  el objetivo ambicioso degradable (consecuencia de RK3).
- **S2** — El subset de O\*NET se descarga y versiona en el repo con su atribución de licencia,
  sin llamadas en runtime. El mecanismo se confirma en `ARCHITECTURE.md`.
- **S3** — El alcance real de v1 son ~3 tools bien hechas antes que 5 a medias; las cinco
  candidatas siguen siendo `set_candidate_profile`, `search_opportunities`,
  `debug_constraints`, `compare_career_worlds`, `inspect_unlock`.

## 13. Gobernanza

**Regla de documentación:**

> No se implementa ningún **core behavior**, **contrato**, **cambio de alcance** ni **decisión
> arquitectónica** sin estar documentado al nivel que le corresponde. Los detalles de
> implementación que no alteran esos contratos **no requieren aprobación del owner**.

Loading states, empty states, retries, microcopy y detalles visuales menores son detalles de
implementación: se hacen sin pedir permiso.

**Jerarquía documental:**

```text
Constitution > Spec > Architecture > Plan > Tasks
```

En conflicto, gana el documento de nivel más alto. Esta constitución gana sobre todos.

**Reglas de trabajo:**

- Cambios de alcance o de arquitectura core requieren aprobación explícita del owner.
- No se trabaja directamente sobre `main`. No se hace merge a `main` sin aprobación.
- No se modifica el worktree de otro agente.
