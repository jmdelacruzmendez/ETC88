# Feedback v4 para Claude Design — Carpeta ETC 88

> **Cómo usar:** copia y pega este archivo al chat de Claude Design para la **v5 del booklet**. Esta auditoría revisa el PDF de 30 páginas (`Carpeta · ETC 88 · 2026`).

**Veredicto general:** la maqueta ya está madura. Las decisiones grandes (portada sin lugar, directorio en tabla con tels, anexo IV de Oraciones, brújula en el cierre) están aplicadas. Quedan **6 inconsistencias del contenido** que se contradicen con decisiones del director, **3 ajustes de paleta** para alinear con el sistema ΙΧΘΥΣ, y **5 mejoras finas de maquetación**. Lo pongo todo en orden de prioridad.

---

## 🔴 INCONSISTENCIAS — corregir antes de imprimir

### 1. Mencionas "7 parejas" en 3 lugares (decisión director: NO ponerlo)
- **Pág. 21** (Directorio · Guías): subtítulo "14 · **7 parejas**"
- **Pág. 24** (Anexo I · callout Pequeño Grupo): "Son siempre **7 parejas (14 guías)**: regla fija."
- **Pág. 25** (Anexo I · §1 El rol del guía): "Trabajan en pareja (2 por PG). **Son 7 parejas — ni más ni menos.**"
- **Pág. 25** (Anexo I · §3): **toda la sección "Las parejas (color-coded)"** habla de las 7 parejas.

**Acción:** El director dijo expresamente que **NO se mencionen las parejas** en el booklet (las parejas se comunican aparte). Quita las 4 menciones; donde diga "7 parejas" déjalo como "**14 guías**" sin agrupación. La §3 del Anexo I puede desaparecer o reescribirse como **"Cómo trabajan los guías"** sin mencionar el sistema de parejas.

### 2. Palabra "veteranos" (palabra prohibida en el sistema del proyecto)
- **Pág. 25** (Anexo I · §2): "Los **veteranos** inician para que el formato se entienda; no todos dan testimonio."

**Acción:** reemplaza "veteranos" por **"los que ya han sido guías antes"**. (Es una regla escrita del proyecto — el verificador automático del repo bloquea esa palabra.)

### 3. Inconsistencia interna en el nombre del tema 6
- **Pág. 11** (§5 Los temas del retiro): tema 6 = "**Regalo del Perdón**"
- **Pág. 13** (§6 Citas para testimonios): tema 6 = "**Regalo del Perdón**"
- **Pág. 15** (§7 Horario sábado): "**Regalo del Perdón**"
- **Pág. 26** (Anexo I · Secuencia de PG, 8.°): "**Alegría del Perdón**" ❌

**Acción:** unifica a **"Regalo del Perdón"** (es el oficial del 88; "Alegría del Perdón" era el del ETC 86). Corrige la tabla del Anexo I.

### 4. Lema del retiro abreviado en la portadilla interior
- **Pág. 2**: "Donde está tu tesoro está tu corazón"
- **Oficial (Mt 6,21):** "**Donde está tu tesoro, allí estará también tu corazón.**"

**Acción:** restituye el lema completo. Las versiones de portada (pág 1) y otras citas dentro del booklet ya lo tienen completo.

### 5. Falta el lugar de retiro en la página de logística
- **Pág. 17** (§9 Reglas de la casa) y **§8 Qué debe llevar el equipo** — no mencionan **cuál casa**.

**Acción:** agrega al header de §9 (o como callout breve) **"La Ceiba del Salado"** — sin "Casa de Retiro" delante, sin "Higüey" detrás. Es la única referencia al lugar interior que pide el director.

### 6. "Proyecto Esperanza" no es un dato confirmado
- **Pág. 18** (§10 Cierre — Los 3 pilares del Cuarto Día): "**Proyecto Esperanza** — lo presenta Sor Angelina."

**Acción:** este nombre no está en `estado.json` como confirmado. Si Sor Angelina presenta algo específico llamado así, déjalo; si no, márcalo como **"[POR DEFINIR — proyecto que presenta Sor Angelina]"**. Pregúntale al director.

---

## 🟡 PALETA — alinear con el DESIGN_SYSTEM (decisión a tomar)

El sistema visual del ETC dice: los 5 colores son las **letras ΙΧΘΥΣ del pez**:
- Ι (iota) = **celeste**
- Χ (ji) = **rojo**
- Θ (theta) = **azul**
- Υ (ípsilon) = **naranja**
- Ϲ (sigma) = **magenta**

Hoy el booklet usa **verde para Guías**, que NO está en el sistema. La asignación actual:
- Guías = verde ❌ → debería ser **celeste (Ι)**
- Cocina = azul ✅ (es Θ)
- Música = naranja ✅ (es Υ)
- Asesores espirituales / 88 = azul intenso + rojo (en portada) ✅

**Opción A — pureza del sistema (recomendada):**
- Guías = **celeste Ι** `#B7E9EC` (filete sobre crema, texto en marrón para legibilidad)
- Cocina = **azul Θ** `#1E2BB6` (ya está cerca)
- Música = **naranja Υ** `#F0871F` (ya está)
- Asesores del retiro = **rojo Χ** `#DA1F22`
- Asesores espirituales / Cierre = **magenta Ϲ** `#D21C82` o **dorado**

**Opción B — mantener el verde:** funciona visualmente pero rompe el sistema. Si el director lo aprueba, **documentar la decisión en el DESIGN_SYSTEM** para evitar disonancia futura.

**Mi recomendación:** Opción A — Guías = celeste. El verde se siente más "scout/excursionista" y se aleja del logo. El celeste viene literalmente del pez.

---

## 🟢 LO QUE QUEDÓ BIEN (mantener)

- **Portada (pág 1):** ETC en azul + 88 en rojo, pez ICTUS amarillo con las 5 letras, lema Mt 6,21, "Siempre amigos" con dos corazones, fecha sin lugar. ✅
- **Anexo IV · Oraciones agregado** (págs 32–33). ✅
- **Directorio en tabla con teléfonos + cumpleaños + asesores de comunidad enmascarados** (págs 20–22). ✅
- **Brújula en el mensaje de cierre** (pág 23), discreta y en marrón/rojo (no náutica chillona). ✅
- **Mensaje de los directores firmado por ambos** (pág 23). ✅
- **Glosario completo** (pág 19) — incluye Correcaminos, Bayuyo, Profondo, Intersección, Carpeta. ✅
- **Tabla VIE/SÁB/DOM del horario** (págs 14–16) — densa, legible, destaca testimonios y plenarios en negrita. ✅
- **Tabla de Pasajes del Hilo** (pág 12) + **tabla de citas sugeridas por testimonio** (pág 13). ✅
- **Los 5 principios del ETC 88** (pág 9, §4.4). ✅
- **Los 9 temas con día y momento** (págs 10–11). ✅
- **Callouts con estilo consistente** (filete de color + título en mayúsculas + texto). ✅

---

## 🟢 MEJORAS FINAS DE MAQUETACIÓN

### 1. Pez chiquito como motivo de cierre
Hoy el pez ICTUS aparece **solo en portada y pág. 4**. Sugerencia: agregar un **pez en línea (contorno marrón sin relleno, 8mm)** como **motivo de cierre** al pie de cada anexo o al final de cada sección larga. Refuerza el símbolo sin saturar.

### 2. Portadillas de anexo (págs 24, 28, 30, 32) — agregar un sumario breve
Hoy las portadillas tienen mucho aire blanco. Sugerencia: agregar bajo el título una **lista de 3 ítems "Qué encontrarás aquí"** (ej. para Cocina: *Rol · Estructura · Avanzada · Lavatorio*). Da orientación al lector y aprovecha el espacio.

### 3. Folio inferior
No se ve en estas capturas, pero asegúrate de que el footer sea: **`ETC 88 · La Ceiba del Salado · pág. N`** o solo **`ETC 88 · pág. N`** — discreto, 8pt, marrón al 50%.

### 4. Inicial decorativa de sección
Los números de sección (1–12) usan una serif decorativa hermosa. Para mantener consistencia: **el ícono de inicio de cada sección** (ej. el "0" verde de la §2, el "5" naranja de §5, el "10" azul de §10) debería usar el **color del área** o **el acento del eje** (no aleatorio). Hoy parece que algunos sí cuadran, otros no.

### 5. Anexo IV · Oraciones — marcar textos pendientes
Hoy enumera 6 tipos de oración pero **no incluye el texto de las oraciones**. La nota dice "Los textos completos los cierran Padre Paul y Sor Angelina". Sugerencia: bajo cada oración listada, dejar un **placeholder visible: `[POR DEFINIR — texto pendiente]`** para que cuando llegue se vea dónde pegarlo. Mejor un hueco marcado que ausencia silenciosa.

---

## 📋 HECHOS CONFIRMADOS (úsalos como verdad)

| Hecho | Valor |
|---|---|
| Número del retiro | ETC 88 (LXXXVIII) |
| Fechas | 4–6 de septiembre de 2026 |
| **Lugar (interior)** | **La Ceiba del Salado** (sin "Casa de Retiro", sin "Higüey") |
| **Lugar (portada)** | NO va lugar — solo fecha |
| Co-dirección | Juan Manuel de la Cruz Méndez · Jean Carlo de la Cruz Mendez |
| Lema retiro | "Donde está tu tesoro, **allí estará también** tu corazón" — Mt 6,21 |
| Cita complementaria | Mt 13,44 |
| Lema eteciano | "Siempre amigos" — Jn 15,15 |
| Tema 6 | **Regalo del Perdón** (no "Alegría del Perdón") |
| Brújula | Sí, con códigos del ETC, apunta al corazón ✅ ya está |
| Parejas de guías | **NO van en el booklet** — solo "14 guías" sin agrupación |
| Palabras prohibidas | **"veterano/veteranos"** — usar "los que ya han sido guías antes" |
| Asesores de comunidad | Santo Domingo (2) · La Vega (1) — sin nombres ✅ ya está |
| Asesores espirituales | Padre Paul Ramírez · Sor Angelina Lebrón (transversales) |

---

## 🎯 ORDEN DE EJECUCIÓN PARA LA v5

1. **Quitar las 4 menciones de "7 parejas"** (págs 21, 24, 25 ×2). Resultado: solo se ve "14 guías" sin agrupación.
2. **Reemplazar "veteranos"** por "los que ya han sido guías antes" (pág 25).
3. **Unificar tema 6 a "Regalo del Perdón"** (corregir tabla del Anexo I pág 26).
4. **Lema completo en pág 2:** "Donde está tu tesoro, allí estará también tu corazón".
5. **Agregar "La Ceiba del Salado"** en §9 Reglas de la casa (pág 17) — sin "Casa de Retiro" delante, sin "Higüey" detrás.
6. **Confirmar / marcar "Proyecto Esperanza"** como `[POR DEFINIR]` hasta que el director cierre el nombre.
7. **Decidir paleta de Guías:** ¿celeste (Ι) o mantener verde? Si celeste, ajusta acentos de la sección y de los íconos de número.
8. **Marcar textos pendientes en Anexo IV** Oraciones (placeholders visibles).
9. **Mejoras finas opcionales:** pez chiquito como cierre, sumario en portadillas de anexo, folio consistente, ícono de sección con color del área.
10. Exporta PDF imprimible (media carta o A5) cuando esté listo.

---

*Feedback v4 — 7-jun-2026. Generado del audit del PDF de 30 páginas. Datos cruzados con `data/estado.json` + `data/equipo.json`. Los hechos de la tabla son `confirmados` del director.*
