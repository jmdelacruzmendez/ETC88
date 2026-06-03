> **DOCUMENTO DE TRABAJO.** Evaluación experta del sistema documental, financiero y de tracking del ETC 88 al 3-jun-2026 (93 días al retiro). Rúbrica explícita · sesgo declarado: yo construí buena parte del sistema, así que la nota refleja también lo que **yo** podría hacer mejor, no solo lo que el director puede mejorar.

# Evaluación experta — Sistema ETC 88
### 3-jun-2026 · 93 días al retiro · 52 commits · 29 docs · `verify.py` 9/9

## 0. Encuadre y método
**Rúbrica (1–10) por dimensión = promedio simple de 5–6 criterios objetivos.** Cada criterio se justifica con evidencia del repo o de Drive.
- **10** = sólido, automatizado, sin un solo punto de falla, autoevidente.
- **7** = funciona, manual pero confiable.
- **5** = existe el concepto, ejecución a medias.
- **3** = idea pero sin operación.
- **1** = no existe.

**Sesgo declarado:** soy autor de ~80% del sistema. Mitigo con criterios cuantificables y honestidad sobre el bus factor (cuántas personas pueden operarlo además de mí).

---

## 1. Gestión documental — **7.2 / 10**

| Criterio | Nota | Evidencia |
|---|:--:|---|
| Trazabilidad (cada cifra/decisión tiene fuente) | **9** | `TRAZABILIDAD.md` con 60 hechos sourced · `verify.py` check #4 |
| Fuente única de verdad | **9** | `estado.json` + `equipo.json` · CLAUDE.md regla #1 |
| Verificabilidad automática | **10** | `verify.py` 9 checks, compuerta antes de entregar |
| Organización (sin duplicados/overlap) | **5** | 29 docs en `preparacion/` · 5 con función solapada: SEGUIMIENTO + TRAZABILIDAD + RESUMEN_MAESTRO + REVISION_3JUN + QUE_NECESITO_DE_TI |
| Accesibilidad al equipo (10 personas con acceso a Drive) | **6** | 4 oficiales en Drive ✓ · pero el equipo **no edita ahí**, solo lee |
| Bus factor (cuántos pueden operar sin mí) | **3** | Pipeline + verify + Drive sync = lo hago yo · nadie más fue instruido aún |

**Lo notable:** los entregables que el equipo ve **no contradicen** los datos — el barrido de Roberto y la corrección de Intersección llegaron de punta a punta (repo → 4 oficiales). Eso lo veo poco en proyectos pastorales.
**Lo frágil:** si yo no estoy mañana, el director hereda 29 docs en `preparacion/` sin un mapa, y nadie sabe correr `verify.py`.

---

## 2. Gestión financiera — **5.2 / 10**

| Criterio | Nota | Evidencia |
|---|:--:|---|
| Modelo conceptual (costo, brecha, recaudación) | **9** | `MODELO_FLUJO_CAJA.md` con 5 reglas de tesorería · `Finanzas_ETC88.xlsx` 12 pestañas |
| Cifras sourced y trazadas | **8** | meta $583,281 ✓ · falta validación en F1 por coords (estimadas) |
| **Responsable financiero operando** | **2** | **[POR DEFINIR]** — sin Tesorería, el modelo es teórico |
| Sistema de control de pagos | **2** | No existe hoja de cobros/conciliación · sin cierre semanal |
| Cuenta bancaria del retiro + constancias | **2** | Sin cuenta dedicada · sin formato de constancia con firma Co-Dir |
| Tracking comprometido vs cobrado vs gastado | **3** | Cifras existen como estimado; no hay reporting en vivo |
| Política de earmark | **3** | `asignacion_entradas` = pendiente en `estado.json` |

**Lo notable:** **el modelo es maduro** (entradas por mes, salidas por mes, reglas de no comprometer si saldo no aguanta, imprevistos 5–8%, dos cierres parciales de rifa). Es mejor que lo que tuvieron el 78 y el 85.
**El cuello:** el modelo **no opera** porque no hay quien lo lleve. **Sin Tesorería identificada antes de F3 (5-jul · 32 días), arrancamos a recaudar a ciegas.** Riesgo financiero #1 del proyecto.

---

## 3. Seguimiento de progreso y tracking — **6.1 / 10**

| Criterio | Nota | Evidencia |
|---|:--:|---|
| Datos cuantificables (roster, prospectos, pendientes) | **8** | 56 personas trazados · 28 prospectos · 8 pendientes oficiales |
| Calendario operativo (hitos con dueño) | **9** | `estado.json.calendario_hitos` · `SEGUIMIENTO_ETC88.md` |
| Pendientes priorizados por horizonte | **9** | esta semana / F1 / F3 / retiro · `REVISION_3JUN.md` |
| Métrica en vivo (% completitud, días al retiro) | **3** | No hay panel del director · cada vez te lo armo yo |
| Update continuo por el equipo (no por mí) | **3** | Cero edición en vivo por los coords · todo pasa por sesión |
| Visibilidad del director sin intermediario | **5** | Drive lee los 4 oficiales · pero el detalle de pendientes vive en docs en repo (que no tiene) |

**Lo notable:** los pendientes están **bien priorizados** (horizonte temporal + dueño + criterio de cierre). El calendario es realista.
**Lo frágil:** **el sistema no se sostiene solo.** Si pasan 4 días sin que tú me pidas algo, el equipo no actualiza nada. No hay tablero que el director consulte en cualquier momento sin abrir 5 docs.

---

## 4. **Nota global: 6.2 / 10**
- *Diseño:* 9/10 — el modelo es bueno.
- *Operación:* 4/10 — depende de mí y de tus decisiones.
- *Resiliencia (¿qué pasa si yo no estoy?):* 3/10.

> *Lo que el rating dice:* tenemos un excelente esqueleto y un esqueleto no es un cuerpo. La diferencia entre 6 y 9 es **dejar de tener un solo operador** y **que el equipo pueda actualizar en vivo**.

---

## 5. Riesgos priorizados (top 5, con probabilidad × impacto)

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|---|:--:|:--:|---|
| 1 | **Sin Tesorería antes de F3 (5-jul)** | alta | $$$$ | Co-Dir nombra responsable ESTA SEMANA (ver §6 A1) |
| 2 | **Bus factor = 1** (yo) | alta | $$$ | Documentar pipeline · capacitar a un asesor (Tomás/Laura) |
| 3 | **Constancias y cuenta de transferencia inexistentes** | alta | $$$ | Abrir cuenta del retiro + plantilla de constancia con firma Co-Dir |
| 4 | **Captación atorada en 28/52** | media | $$$ | Tracker en vivo + asignar misionero a los 12 huérfanos antes de F1 |
| 5 | **Branding viejo (v4.pdf) en Drive contradice "desde 0"** | media | $$ | Marcar OBSOLETO o papelera + dejar solo el brief vivo |

---

## 6. Correcciones con accionables (priorizados y fechados)

### 🔴 A · Esta semana (3-jun → 9-jun)
| # | Acción | Dueño | Cómo se mide cerrado |
|---|---|---|---|
| A1 | **Nombrar Tesorería** (1–2 personas dentro del equipo) | Co-Dir | nombre en `estado.json` con `estado=confirmado` |
| A2 | **Abrir cuenta bancaria del retiro** (o decidir transferencia personal con trazabilidad) | Co-Dir + Tesorería | datos en `estado.json` + en Plantilla C de cartas |
| A3 | **Mensaje al equipo con link de los 4 oficiales** (Drive) — para que tengan algo vivo que mirar | Co-Dir | WhatsApp enviado + acuse |
| A4 | **Renombrar 5 supervivientes + refrescar 4 oficiales** (script pendiente) | JM + Claude | Drive con los 4 al día (Olanlly + Randol + Daylin con nombres completos) |
| A5 | **Marcar `Brand_Guidelines_v4.pdf` como OBSOLETO** o papelera | JM | archivo renombrado o eliminado |

### 🟠 B · Antes de F1 (14-jun)
| # | Acción | Dueño | Cómo se mide |
|---|---|---|---|
| B1 | **Hoja "Control de Pagos"** (Google Sheet abierto + editable por Tesorería): cuotas equipo, cuotas participante, donaciones, gastos — comprometido vs cobrado vs gastado por mes | Tesorería + Claude (yo genero la plantilla) | sheet creado y vinculado a `Finanzas (oficial)` |
| B2 | **Tracker de captación de participantes** (28 prospectos × misionero × estado: invitado / aceptó / canceló) | Recaudación + cantera | sheet creado con los 28 hoy |
| B3 | **Plantilla de Constancia de Donación** (PDF que Tesorería firma + Co-Dir contrafirma) | Claude (genero plantilla) → Co-Dir aprueba | plantilla en `preparacion/` + ejemplo firmado |
| B4 | **Documentar el pipeline** en `CLAUDE.md` para que cualquier asesor lo corra (10 líneas + el comando único) | Claude | un párrafo nuevo en CLAUDE.md |
| B5 | **Capacitar 1 asesor** (sugerencia: Tomás, que ya lleva el tablero) para que ejecute `verify.py` y avise si rompe | Co-Dir + Tomás | Tomás corrió el pipeline 1 vez con éxito |
| B6 | **Lugar de las 5 formaciones** (sede fija/rotativa) | Co-Dir | en `estado.json` confirmado |

### 🟡 C · Antes de F3 (5-jul · arranca recaudación)
| # | Acción | Dueño | Cómo se mide |
|---|---|---|---|
| C1 | **Cierre semanal de Tesorería** (todos los lunes) publicado en el grupo | Tesorería | cierre #1 publicado lunes 7-jul |
| C2 | **Consolidar docs duplicados** en `preparacion/`: SEGUIMIENTO + TRAZABILIDAD + RESUMEN_MAESTRO + REVISION → 1 índice maestro + 1 changelog | Claude | 4 docs → 2 docs (sin pérdida de info) |
| C3 | **Política de earmark** (qué entrada cubre qué compromiso) | Co-Dir + Tesorería | `asignacion_entradas` confirmado en `estado.json` |
| C4 | **Cotizar transporte/biblias/peces** (deadline pendiente fijado) | Recaudación | 3 cotizaciones por línea |
| C5 | **Visiteo a la casa** con Samuel Montilla | Co-Dir + coords | fecha confirmada |

### 🟢 D · Operativo continuo (de aquí al retiro)
| # | Acción | Cómo se mide |
|---|---|---|
| D1 | Métrica única de "días al retiro" + "% completitud" en cada cierre semanal | número visible en cada update |
| D2 | Convención de versionado de entregables: `vN-AAAAMMDD` (no "v8" suelto) | aplicado desde el próximo sync |
| D3 | **Llenar o eliminar** las subcarpetas `Finanzas/` y `Operaciones/` (vacías hoy) | decisión Co-Dir |
| D4 | Roadmap claro de **publicación a Drive: solo en hitos** (F1, F3, F5, Convivencia, Ensayo, Retiro) — no cada cambio | reduce churn |

---

## 7. Lo que NO es problema (para no sobre-corregir)
- **Compuerta de calidad** (`verify.py`) — es lo más sólido del sistema; no la toquen.
- **Fuente única de verdad** (`estado.json` + `equipo.json`) — funciona.
- **Cuatro entregables canónicos** — ya consolidados, opción A cumplida.
- **El barrido de errores históricos** (Roberto, Dionis-guía, Constelación, $260K) — purgado de punta a punta.

---

## 8. Resumen ejecutivo (1 párrafo para el director)
> El sistema documental del ETC 88 tiene un **diseño 9/10** y una **operación 4/10**. Si el retiro fuera dentro de un mes, sería tarde. Tenemos **93 días**, lo que es suficiente para corregir las tres cosas que mueven el rating de 6 a 9: **(1) nombrar Tesorería esta semana**, **(2) bajar el bus factor de 1 a 2** (un asesor capacitado), **(3) habilitar al equipo a actualizar en vivo** (hoja de Control de Pagos + tracker de captación, ambas editables). Sin esos tres, llegaremos al retiro con los datos correctos pero **sin sistema de operación**, lo que en finanzas significa **conciliación caótica** y en captación significa **48 personas en la casa en vez de 100**.
