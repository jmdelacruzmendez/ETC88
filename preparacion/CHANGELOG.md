# Changelog ETC 88
### Decisiones, cambios y cierres por fecha (lo nuevo arriba)

> Historial vivo. Cada entrada lleva fecha real (git log), tipo y dueño. Las decisiones del director se reflejan también en `estado.json` (`estado=confirmado`). El detalle técnico de cada cambio está en los commits.

---

## 2026-06-03 — Sesión de cierre y materialización

### Drive · materialización oficial
- ✅ **6 entregables concretos en Drive:** 4 oficiales (Asesores · Carpeta F1 · Equipo · Finanzas) + 2 hojas vivas en subcarpeta interna `OPERACIÓN` (Control de Pagos · Captación).
- ✅ Carpeta consolidada (opción A · lean): solo Formulario + Borrador abril + 3 insumos originales + jpeg reserva + ENTREGABLES + OPERACIÓN.

### Datos · roster
- ✅ **Randol Joseph Payano** (nombre del formulario, decisión del director) confirmado en Cocina · vacante cerrada.
- ✅ **Daylin M Rambalde Moreta** confirmada en Música · no puede asumir coordinaciones (cambio de empleo + distancia, PC) · resistencia a la insulina (Metformina).
- ✅ **Marian Olanlly Ortiz Carrasco** (Cocina, 19 años, talla S) — nombre completo del form.
- ⏳ Sin formulario: **Pamela, Frank**.

### Estructura del equipo
- ✅ **Intersección** redefinido = **diáspora** (etecianos fuera del país); ya no es "espiritual".
- ✅ **Finanzas / Tesorería** agregado como **5.º equipo auxiliar** (medida #3 Informe 85). Responsable [POR DEFINIR].

### Participantes
- ✅ Cruce Doc-abril × formulario: **28 prospectos** (16 con misionero · 12 sin).
- ✅ **Diana Constanzo** = hermana de Ismarie (Música) → lazo a marcar al asignar PGs.
- ✅ **Marianne Beltre = Castro** (dedup confirmada).
- ✅ **+2 invitados** de Olanlly (Lusiany Castillo · Hemerson Asencio).

### Reglas confirmadas (corrección de inventos)
- ✅ **Solo mayores de edad** — el ETC no admite menores. *(Purgada toda la sección "menores/permisos" que Claude había metido sin fuente.)*
- ✅ **Camiseta solo del equipo** — los participantes NO llevan. *(Purgada la "talla" del perfil del participante.)*

### Sistema · optimizaciones adoptadas
- ✅ **D1** `list_recent_files` como descubridor primario (búsqueda por título tiene lag).
- ✅ **D2** Sync de Drive **por hitos**, no por micro-cambio.
- ✅ **D3** `.gitignore` de binarios `.docx/.xlsx` (regenerables, viven en Drive).
- ✅ **D4** Overrides del form en **datos** (`data/form_live_overrides.json`), no en código.
- ✅ **B2** Tracker de captación: `data/participantes.json` + `build_captacion.py`.
- ✅ **B4** Bus factor: `scripts/run_all.sh` (un solo comando) + sección en CLAUDE.md.

### Documentos nuevos / corregidos
- ✅ `MODELO_FLUJO_CAJA.md` revisado: 5 reglas de tesorería + tabla mes-a-mes.
- ✅ `RESPONSABILIDADES_ASESORES.md` (gap #5 Informe 85).
- ✅ `CARTAS_DONACION.md` (3 plantillas + matriz + flujo).
- ✅ `EVALUACION_SISTEMA.md` (rúbrica 5.2/6.1/7.2 → global 6.2).
- ✅ `ROADMAP_SISTEMA.md` (qué falta + camino HTML dinámico + cómo sobrellevar).
- ✅ `web/tablero.html` (tablero dinámico interactivo, JS validado).
- ✅ **Este consolidado:** `SEGUIMIENTO_ETC88.md` reemplaza a `RESUMEN_MAESTRO` + `REVISION_3JUN` + `QUE_NECESITO_DE_TI`.

### Cosas que se quedaron abiertas (decisión del director)
- 🔴 Esta semana: Tesorería · Samuel Montilla · exención Paul · cuenta bancaria.
- 🟠 Antes de F1: responsables 5 auxiliares · lema/hilo · cuota equipo · misionero a los 12 huérfanos.
- 🟡 Antes de F3: Tesorería operando · Intersección/diáspora asignado · cotizaciones.

---

## 2026-06-02 — Reseteo del sistema (fuente única + verify)

- ✅ Adoptada la regla: **fuente única `estado.json` + `equipo.json`**, todo lo compartible se **genera**, `verify.py` es la **compuerta** (9 chequeos).
- ✅ Drive: barrido inicial (21 sueltos a papelera la primera vez) + opción **A lean**.
- ✅ Decisiones del director consolidadas: Constelación quitada · Leober "Soriano" · Roselyn fuera · backups Rodolfo/Scarlett/Kamila · Recaudación+Donaciones = 1 equipo · Guagua = equipo de transporte · Paul + Sor = transversales · Frank asesor + Banderín · convivencia 22-ago con miniretiro · ensayo 23-ago obligatorio · reunión coords jue 4-jun · branding desde 0 · temática expedición/tesoro · casa con sonido + gas + limpieza · cuota participante $3,000 · casa $2,300/$2,000 (con exención RNC Paul) · piso 100 personas en la casa.
- ✅ Barrido de asignaciones sin consulta (caso Roberto Figueroa) + check #9 en `verify.py`: nunca inferir rol desde formulario.
- ✅ Contraste con ETC 78/79/85 + mapa de donaciones por rubro + 10 gaps del Informe 85.

> Detalle de cada commit en `git log --since=2026-06-02`. Hay 38 commits ese día.
