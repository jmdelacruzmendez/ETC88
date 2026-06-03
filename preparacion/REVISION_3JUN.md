> **DOCUMENTO DE TRABAJO.** Revisión consolidada del 3-jun: cruce de información, trazabilidad, sincronización, pendientes cerrados/abiertos + **autocrítica de mis propios procesos** (lo pidió el director). Verificado con `verify.py` 9/9 y git en sync.

# Revisión consolidada — 3-jun-2026

## A. Pendientes CERRADOS hoy
| # | Cerrado | Fuente / verificación |
|---|---|---|
| 1 | **Randolph Joseph** confirmado en Cocina (cupo de Roselyn) — vacante cerrada | director · `estado.json` |
| 2 | **Daylin** confirmada en Música | director |
| 3 | **Intersección** redefinido = **diáspora** (no espiritual) | director · `estado.json` |
| 4 | **Finanzas / Tesorería** agregado como **5.º auxiliar** | director (medida #3 Informe 85) |
| 5 | **Flujo de caja revisado** (5 reglas de tesorería + tabla mes-a-mes) | `MODELO_FLUJO_CAJA.md` |
| 6 | **Cruce de participantes** — 28 prospectos (Diana=hermana de Ismarie, Marianne dedup, +2 de Olanlly) | `PARTICIPANTES_POTENCIALES.md` |
| 7 | **Formulario en vivo conectado** (44 respuestas leídas) | hoja "Respuestas…" id `1Vx0…` |
| 8 | **Olanlly + Randolph enriquecidos** con datos del form (nombre completo, edad, talla) | `build_data.py` override · live form |
| 9 | **Responsabilidades de asesores** por tipo (gap #5 Informe 85) | `RESPONSABILIDADES_ASESORES.md` |
| 10 | **Cartas a donantes** (3 plantillas + matriz + flujo) | `CARTAS_DONACION.md` |
| 11 | **Auditoría profunda de sueltos** (15 docs + 2 hojas leídos) | `SUELTOS_DRIVE_ASSESSMENT.md` |
| 12 | **Drive consolidado** (papelera 21 + 4 oficiales al día · opción A lean) | re-verificado en vivo |
| 13 | **ETAPAS** corregido (4→5 auxiliares · Intersección=diáspora) | `ETAPAS_FORMACIONES_PRIORIDADES.md` |

## B. Pendientes que SIGUEN ABIERTOS (solo el director los cierra)
**🔴 Esta semana:** contactar a **Samuel Montilla** (visiteo casa) · **exención RNC** con Padre Paul · **reunión coords jue 4-jun**.
**🟠 Antes de F1 (14-jun):** responsables de los 5 auxiliares · lema/hilo espiritual · cuota equipo · fecha límite cotizar transporte/biblias/peces.
**🟡 Antes de F3 (5-jul):** Tesorería operando · Intersección/diáspora asignado.
**Datos por completar:**
- **Daylin, Pamela y Frank** aún no llenaron el formulario (Olanlly y Randolph ya).
- **Confirmar grafía:** roster dice "Randolph Joseph"; el form se auto-reporta "Randol Joseph Payano" → director confirma.
- **15 personas con comunidad "Por confirmar"** (los sin-formulario + ampliados/transversales).

## C. Trazabilidad y sincronización (estado verificado)
- `verify.py` **9/9 PASS** · git **en sync** con remoto (0/0).
- `TRAZABILIDAD.md` regenerada desde `estado.json`.
- **Drive:** los 4 oficiales se re-verificaron **leyendo su contenido** (no asumiendo); 5 supervivientes conservados; 21 en papelera.
- **Gap conocido (lo anoto para no perderlo):** la idea de recaudación de Olanlly ("alcancías solidarias · venta de postres") está en el **form en vivo** pero NO en la lista de recaudación del repo, porque el `fuente_formulario.xlsx` es un snapshot anterior a su respuesta. Se incorpora cuando se refresque el xlsx.

## D. Autocrítica de mis procesos (dónde me equivoqué / qué optimizar)
Honesto, como pediste:

1. **Subestimé el acceso al formulario.** La hoja de respuestas existía desde el 31-may; tras **una** búsqueda por título fallida concluí "no accesible" y se lo dije al director. La encontré después con `list_recent_files`. → **Error de sub-búsqueda + sobre-conclusión.** Optimización: **usar `list_recent_files` como descubridor primario** (la búsqueda por título/parentId del conector tiene lag de indexado y devuelve vacío de forma intermitente).

2. **Churn de Drive.** Re-subí los 4 oficiales **3 veces** hoy (cada vez = borrar + subir que tú corres), porque el conector **no actualiza en sitio**. → Optimización: **sincronizar Drive en hitos, no en cada micro-cambio**; agrupar los cambios de datos y re-subir una sola vez. (Hoy lo combino: el script de renombrar + el refresh de oficiales van juntos.)

3. **Binarios versionados en git.** Sin `.gitignore`, cada regeneración produce diffs binarios (`.docx/.xlsx/index.html`) — ruido y el aviso de "cambios sin commitear". → Optimización: `.gitignore` de generados, o aceptarlo y automatizar el commit.

4. **Hardcodeé datos del form en `build_data.py`** (override de Olanlly/Randolph) porque el xlsx está viejo. Es un workaround. → Optimización real: que `build_data` lea la **hoja de respuestas en vivo** (export CSV) en vez del xlsx estático — así no hay que parchear a mano.

5. **Lecturas largas truncadas.** El form se truncó 2 veces (cortaba en Olanlly); lo cacé al segundo intento, pero pude usar export CSV de la hoja desde el principio.

6. **Regla #5 (.docx) vs lo que hago (text/plain → Google Doc).** Subo texto convertido, no el `.docx`. Produce un Google Doc limpio (cumple la *intención* de la regla) pero se desvía de la letra. A decidir si subo también los binarios.

## E. Lo que NO está mal (para no sobre-corregir)
- La **fuente única + `verify.py` + trazabilidad funcionó**: 0 errores de datos en los entregables; el error de Roberto se corrigió de punta a punta (incluido Drive); las cadenas prohibidas y nombres inventados están bloqueados por la compuerta.
- Drive quedó **lean y correcto** (opción A).
- Cada hecho compartible sigue trazado a `estado.json`/`equipo.json`.

## F. Acciones que salen de esta revisión
1. **Renombrar** los 5 supervivientes de Drive (script abajo) para que la carpeta se explique sola.
2. **Refrescar los 4 oficiales** con el nombre completo de Olanlly + edades (combinado en el mismo script).
3. **[opcional]** Adoptar las optimizaciones D1–D4 (list_recent primario · sync por hitos · .gitignore · build_data desde hoja viva).
