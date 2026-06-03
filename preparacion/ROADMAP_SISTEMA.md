> **DOCUMENTO DE TRABAJO.** Roadmap del sistema + diagnóstico experto (3-jun, 93 días al retiro). Qué falta por **vincular · trazar · documentar · recopilar · mostrar**, el camino a un **tablero HTML dinámico**, y cómo el director **sobrelleva** la gestión del retiro. Acompaña a `EVALUACION_SISTEMA.md`.

# Roadmap del sistema ETC 88 + diagnóstico experto

## 1. Lo que falta por VINCULAR · TRAZAR · DOCUMENTAR · RECOPILAR · MOSTRAR
Organizado por los flujos reales del retiro. (✅ existe · 🟡 parcial · 🔴 falta)

### Participantes
| Elemento | Vincular con | Recopilar cómo | Mostrar dónde | Estado |
|---|---|---|---|---|
| **Tracker de captación** (28 → 52) | roster (quién invita) | Sheet editable (B2, hoy) | panel "Captación" | 🟡 semilla lista |
| **Perfil del participante** (salud, sacramentos, lazos) | cocina (alergias), guías (PG) | Google Form vivo → hoja | panel "Participantes" | 🔴 spec lista, form no creado |
| **Asignación de 7 PGs color-coded** | lazos del equipo (regla: no hermano/pareja en su plenario) | herramienta de armado | panel "Pequeños Grupos" | 🔴 falta (depende de perfiles) |

### Finanzas
| Elemento | Vincular con | Recopilar | Mostrar | Estado |
|---|---|---|---|---|
| **Control de pagos** (comprometido/cobrado/gastado) | meta $583,281 · flujo de caja | Sheet de Tesorería (B1) | panel "Finanzas" | 🔴 falta |
| **Registro de donaciones** | cartas a donantes · rubros | Sheet vinculado | panel "Donaciones" | 🔴 falta |
| **Constancias + cuenta bancaria** | donaciones | plantilla PDF firmada | — | 🔴 falta |
| **Informe post-retiro** (planificado vs real) | presupuesto | Sheet | panel cierre | 🔴 falta (gap Informe 85) |

### Logística y materiales
| Elemento | Vincular con | Estado |
|---|---|---|
| **Materiales con cantidades** (peces/biblias/rosarios/banderín/camisetas) | **conteo final de participantes** → cantidades → presupuesto | 🟡 estimado, no atado al conteo vivo |
| **Transporte** (3 cotizaciones → elegido → manifiesto) | zonas (SPM/Higüey/PC) | 🔴 falta cotizar |
| **Menú vs alergias** (vista derivada) | perfiles + roster (mariscos/piña/diabetes/insulina) | 🟡 alergias del equipo ✓, faltan las de participantes |
| **Tallas de camiseta (SOLO equipo)** | roster del equipo (los participantes NO llevan camiseta) | 🟡 faltan varias del equipo |

### Formación y seguimiento
| Elemento | Vincular | Estado |
|---|---|---|
| **Asistencia por formación** (regla máx 3 ausencias) | roster | 🔴 falta hoja |
| **Entrega de presupuestos por área en F1** | finanzas | 🟡 pendiente F1 |
| **Palancas** (quién escribe a quién) | PGs | 🔴 falta (cerca del retiro) |

### Espiritual / liturgia / post
| Elemento | Estado |
|---|---|
| Confesores (≥2–3) · banderín · misa clausura · vino/formas | 🔴 checklist por armar |
| Cadena de oración (Intersección/diáspora) | 🟡 equipo por nombrar |
| Evaluación participantes + 4º día | 🔴 post-retiro |
| Assets de branding (Claude Design) | 🔴 cuando existan → carpeta Branding |

> **El hilo que une todo:** el **conteo final de participantes** es el número del que cuelgan materiales, comida, transporte, casa y presupuesto. Hoy es estimado (52). Cuando se cierre, **todo el modelo se recalibra solo** si está bien vinculado.

---

## 2. Camino a un TABLERO HTML dinámico e interactivo
**Hoy:** `index.html` es estático, generado de `equipo.json` (foto, no vivo).
**Meta:** un tablero que **lee en vivo** de los Google Sheets que el equipo edita → el director ve el estado real sin que yo intervenga.

### Arquitectura recomendada (sin servidor — apta para una parroquia)
```
Google Sheets (lo que el equipo edita)        Tablero (1 archivo HTML)
 ├─ Equipo (roster oficial)        ──┐
 ├─ Control de Pagos (Tesorería)    ─┼─►  publicar cada hoja como CSV
 ├─ Captación (participantes)       ─┤    (Archivo→Compartir→Publicar en la web→CSV)
 └─ Pendientes / hitos              ──┘            │
                                                   ▼
                              tablero.html hace fetch() de cada CSV
                              y dibuja paneles (sin backend):
                               • Días al retiro + % completitud
                               • Finanzas: comprometido / cobrado / gastado + barra de meta
                               • Captación: funnel 0 → 52 + sin-misionero
                               • Roster por área + alertas de salud/alergias
                               • Pendientes por horizonte (semana / F1 / F3)
```
**Interactivo:** filtros por área, búsqueda, orden, marcar; auto-refresh cada N minutos.
**Ventajas:** el equipo edita Sheets (familiar) y el tablero refleja en vivo; **cero servidor**; se puede alojar en GitHub Pages o abrir el archivo.
**Decisiones previas (tuyas):** (a) qué hojas se publican; (b) privacidad del panel de participantes (datos sensibles → o se agrega solo agregado, o el tablero se comparte solo con Co-Dir). 
**Pasos:** 1) crear las 4 hojas vivas · 2) publicarlas como CSV · 3) yo construyo `tablero.html` (fetch + render) · 4) alojar. Estimado: lo construyo en 1 sesión una vez existan las hojas.

---

## 3. Diagnóstico experto — cómo se maneja un ETC y cómo sobrellevarlo
Sabiendo cómo corre un ETC (retiro de 3 días, 100 personas, cocina/guías/música, palancas, PGs, liturgia, 4º día):

### La verdad incómoda
**El cuello de botella no son los documentos — son las DECISIONES y la DELEGACIÓN.** El sistema ya produce datos limpios; lo que falta es que **cada flujo tenga un dueño con nombre** para que tú (Co-Dir) dejes de ser el único nodo.

### La carga del director es triple
1. **Pastoral** (las personas) · 2. **Operativa** (logística + plata) · 3. **Espiritual** (el mensaje).
**El sistema debe quitarte la #2 para que te quedes con la #1 y la #3.** Hoy cargas las tres.

### Cómo sobrellevarlo (concreto)
1. **Nombra responsables** de los 5 auxiliares + Tesorería. Cada uno **dueño de su tracker**. Dejas de ser el único que sabe.
2. **Ritual semanal de 30 min** (Co-Dir + asesores): mirar **2 números** — *recaudado vs meta* y *captados vs 52* — y los pendientes de la semana. Nada más.
3. **Bitácora de decisiones** (ya está en `estado.json` + SEGUIMIENTO): una decisión tomada **no se vuelve a discutir**. Esto solo ahorra horas.
4. **Bus factor 2:** capacita a **Tomás** (ya lleva el tablero) para correr `bash scripts/run_all.sh`. Si me ausento, el sistema sigue.
5. **Un solo panel** (el tablero dinámico) en vez de 29 docs: tú miras una pantalla, no un repo.
6. **Protege el núcleo espiritual:** la **raíz/hilo espiritual de esta semana** es la decisión de mayor palanca — todo (formación, branding, banderín, misa) hereda de ahí. Ciérrala con Paul/Sor y lo demás fluye.

### Los 2 números que deciden el retiro (vigílalos cada semana)
- **💰 Plata:** sin Tesorería operando antes de F3 (5-jul), recaudas a ciegas. *Riesgo #1.*
- **👥 Gente:** captación atorada en 28/52. Si no sube, llegas con la casa a medias. *Riesgo #2.*
> Si esos dos van bien, el retiro va bien. El resto es ejecución.

### Lo que aún no existe y más mueve la aguja (orden de impacto)
1. **Tesorería con nombre** (esta semana) → desbloquea todo el flujo financiero.
2. **Hojas vivas** (Control de Pagos + Captación) → el equipo actualiza, tú ves.
3. **Tablero dinámico** que lee esas hojas → tu "panel del director".
4. **Form de Perfil del Participante vivo** → alimenta cocina (alergias) y guías (PGs).
5. **Bus factor 2** → resiliencia.

---

## 4. Qué puedo construir yo sin esperar decisiones (orden sugerido)
1. ✅ **B2 — Tracker de captación** (hoy: `data/participantes.json` + `build_captacion.py` → CSV).
2. ✅ **B4 — `run_all.sh` + doc en CLAUDE.md** (bus factor).
3. ⏭ **B1 — Plantilla "Control de Pagos"** (CSV/Sheet con columnas de tesorería).
4. ⏭ **B3 — Plantilla de Constancia de Donación**.
5. ⏭ **`tablero.html` dinámico** (cuando definas qué hojas se publican).
6. ⏭ **Consolidar los docs duplicados** (SEGUIMIENTO+TRAZABILIDAD+RESUMEN+REVISION → índice + changelog).
