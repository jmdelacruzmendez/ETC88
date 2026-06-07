# PROMPT FINAL para Claude Design — Carpeta ETC 88

> Este es el **único archivo que pegas al chat de Claude Design**. Reemplaza todos los anteriores (`v1` a `v5`, `RECOMENDACION_PALETA_TIPO_ELEMENTOS`, `RECOMENDACION_PORTADA`, `PROMPT_CONSOLIDADO`). Acompáñalo de **`DIRECTORIO_EQUIPO_88.md`** (lista de 53 servidores con tabla de teléfonos) y **`DESIGN_SYSTEM_ETC.md`** (identidad visual — ya está en project knowledge).

---

## A. AUDITORÍA FINAL antes del prompt

Revisé las 4 rondas de feedback + las 2 recomendaciones de diseño + las últimas 3 decisiones del director (7-jun). Esto es lo que cierro:

### A.1 Decisiones cerradas del director (confirmadas en `estado.json`)
| Decisión | Estado |
|---|---|
| Portada: solo fecha, sin lugar | ✅ confirmado |
| Lugar: **NO se menciona en ningún lado del booklet** (ni interior, ni footer) | ✅ confirmado 7-jun |
| 7 parejas de guías: NO se mencionan en el booklet | ✅ confirmado 6-jun |
| Brújula: SE QUEDA en el mensaje de cierre, con códigos del ETC | ✅ confirmado 6-jun |
| Tema 6 = "Alegría del Perdón" (no "Regalo del Perdón") | ✅ confirmado 7-jun |
| Asesores de comunidad sin nombres en el booklet | ✅ confirmado 5-jun |
| "Veterano/veteranos" prohibido — usar "los que ya han sido guías antes" | ✅ regla del proyecto |
| Identidad: pez ICTUS original como héroe, paleta ΙΧΘΥΣ | ✅ confirmado 5-jun |

### A.2 Pendientes (no del director — recomendaciones mías)
| Pendiente | Quién decide |
|---|---|
| Cambiar tipografía a Fraunces+Inter o variante | Director (mi recomendación) |
| Refinar HEX de los 5 colores ΙΧΘΥΣ (versión editorial) | Director |
| Portada nueva — Opción A/B/C | Director (mi recomendación: **B con elementos de A**) |
| Mover "Mensaje de los directores" al FINAL del booklet | Director (mi recomendación) |
| Ajustar a 32 o 36 páginas (múltiplo de 4) | Director / imprenta |
| Color de íconos de sección §1–§12 (todos marrón vs temático) | Director |
| Sistema de 10 íconos custom en trazo marrón | Director |
| Contracubierta | Director (no había antes) |

### A.3 Contradicciones detectadas y resueltas
- ❌ "Casa de Retiro La Ceiba del Salado" en `estado.json` como lugar confirmado **vs** decisión "NO mencionar lugar". **Resolución:** el lugar real sigue en `estado.json` (es info logística para coords), pero el booklet **no lo expone**. Son cosas distintas.
- ❌ Booklet actual dice "Regalo del Perdón" en 3 lugares y "Alegría del Perdón" en 1. **Resolución:** "Alegría del Perdón" en todos lados. Ya corregido en `COPY_GUIA_ETC88.md` y `GUIA_DE_GUIAS_88.md`.
- ❌ Recomendación de portada Opción B propone "ETC marrón + 88 dorado". El booklet actual usa "ETC azul + 88 rojo". **Resolución:** lo marco como **propuesta a aprobar por el director**, no decisión cerrada.

---

## B. HECHOS FIJOS — la fuente de verdad

| Hecho | Valor |
|---|---|
| Retiro | **ETC 88** (LXXXVIII) |
| Fechas | **4–6 de septiembre de 2026** |
| **Lugar** | **NO se menciona ningún lugar en el booklet.** Ni en portada, ni en interior, ni en footer. Solo la fecha. |
| Co-dirección | Juan Manuel de la Cruz Méndez · Jean Carlo de la Cruz Mendez |
| Lema del retiro | **"Donde está tu tesoro, allí estará también tu corazón"** — Mt 6,21 |
| Cita complementaria | Mt 13,44 |
| Lema eteciano | "Siempre amigos" — Jn 15,15 |
| Tema 6 | **"Alegría del Perdón"** (no "Regalo del Perdón") |
| Asesores espirituales | Padre Paul Ramírez · Sor Angelina Lebrón (transversales) |
| Asesores del retiro | Frank Morales (+ Banderín) · Laura Fernández · Tomás Lorenzo |
| Asesoras de cocina | Mary "Petra" Morales · Johanny García |
| Asesores de comunidad | Santo Domingo (2) · La Vega (1) — **SIN nombres en el booklet** |
| Coords Guías | Camila Fernández Hazim · Priscilla Hidalgo Pou |
| Coords Cocina | Paloma Méndez · Johnnito Richiez Brugal |
| Coord Música | José Ángel Tusen Russo |
| Equipo total | 53 servidores titulares · 48 operativos en el retiro |
| **Parejas de guías** | **NO se mencionan en el booklet** |
| **Brújula** | SE QUEDA en el mensaje de cierre — apunta al **corazón** |
| Palabra prohibida | "veterano/veteranos" — usar "los que ya han sido guías antes" |
| Solo mayores de edad | El ETC 88 NO admite menores |
| Camiseta | Solo del equipo (los participantes NO llevan) |

---

## C. CORRECCIONES DE CONTENIDO — urgente

Aplica las 6 correcciones siguientes al booklet actual:

1. **Quitar TODAS las referencias a lugar** del booklet.
   - Portada: solo fecha (ya está bien en la última versión).
   - Portadilla interior: si dice "Comunidad: Caminos de Vida, San Pedro de Macorís", es la **comunidad eteciana de pertenencia**, no el lugar — puedes mantenerlo si encaja, o quitarlo si dudas.
   - §9 "Reglas de la casa": header sin ciudad ni casa.
   - Footer: `ETC 88 · pág. N` (sin lugar, sin año).
   - **En ningún lugar del booklet va "La Ceiba del Salado", "Casa de Retiro", "Higüey" ni "SPM" como ubicación del retiro.**

2. **Quitar las 4 menciones de "7 parejas"** (págs 21, 24, 25 ×2).
   - Pág 21 "14 · 7 parejas" → **"14 guías"**.
   - Pág 24 callout PG "Son siempre 7 parejas (14 guías)" → reescribir sin parejas.
   - Pág 25 §1 "Trabajan en pareja (2 por PG). Son 7 parejas" → quitar.
   - Pág 25 §3 "Las parejas (color-coded)" → borrar la sección o reescribir como **"Cómo trabajan los guías"** sin mencionar parejas.

3. **Reemplazar "veteranos" → "los que ya han sido guías antes"** (pág 25).

4. **Unificar tema 6 a "Alegría del Perdón"** (corregir págs 11, 13, 15 — pág 26 ya estaba bien).

5. **Lema completo** en pág 2: **"Donde está tu tesoro, allí estará también tu corazón"** (hoy dice "Donde está tu tesoro está tu corazón").

6. **"Proyecto Esperanza"** (pág 18): confirmar el nombre con el director o marcar como **`[POR DEFINIR — proyecto que presenta Sor Angelina]`**.

---

## D. PALETA — refinada y alineada con ΙΧΘΥΣ

### D.1 Base
| Rol | HEX | Uso |
|---|---|---|
| Papel | `#F4EFE1` | Fondo principal |
| Papel cálido | `#EAE2CC` | Filas alternas de tabla (zebra), fondos de callout |
| Marrón principal | `#3A2A1A` | Texto cuerpo, filetes, titulares |
| Marrón suave | `#6B4F38` | Texto secundario |
| Dorado pez | `#E9C44E` | Pez, realces cálidos |
| Dorado oscuro | `#B58A2C` | Filete editorial, "88" en portada (propuesta), pie |

### D.2 Acentos ΙΧΘΥΣ — versión editorial refinada
Los HEX originales son muy saturados para bloques grandes. Versión recomendada:

| Letra | Área | HEX editorial | HEX original |
|---|---|---|---|
| Ι (iota) | **Guías** | `#3FA5B0` | `#B7E9EC` (demasiado claro) |
| Χ (ji) | Asesores del retiro | `#B5392C` | `#DA1F22` |
| Θ (theta) | Cocina | `#253C8F` | `#1E2BB6` |
| Υ (ípsilon) | Música | `#D77B2A` | `#F0871F` |
| Ϲ (sigma) | Asesores espirituales / Cierre | `#A02C68` | `#D21C82` |

**Cambio principal:** Guías hoy es verde — debe ser **celeste Ι** alineado con ΙΧΘΥΣ.

### D.3 Reglas de uso
- **60-30-10:** 60% crema (papel), 30% marrón (estructura), 10% acento (un solo color de área por sección).
- **Íconos de número de sección §1–§12:** todos en **marrón uniforme** — el color de área se reserva para §3 (Roles) y los 4 anexos.
- **Pez ICTUS:** único elemento full-color obligatorio. Las 5 letras dentro del pez conservan colores ΙΧΘΥΣ puros (acento puntual).
- **Modo 1-tinta:** todo el booklet debe sobrevivir a 1 tinta marrón sobre crema. Acentos = tono medio 60%, filetes = 35%, marca de agua del pez = 15%.

---

## E. TIPOGRAFÍA — recomendación

Pareja base (todas Google Fonts / SIL OFL, sin restricciones de impresión):

**Recomendada — "Editorial cálida":**
- **Display:** `Fraunces` — serif moderna con glifos griegos para ΙΧΘΥΣ.
- **Cuerpo:** `Inter` — sans humanista, hiperlegible.
- **Marker (anexos + mensaje de directores):** `Permanent Marker` o `Caveat Brush` en peso 700.

Alternativas: `Cormorant Garamond + Source Sans 3 + Indie Flower` (clásica/católica) · `Lora + Atkinson Hyperlegible + Caveat` (cálida/manual).

### Jerarquía
| Elemento | Familia | Peso | Tamaño | Interlineado |
|---|---|---|---|---|
| Título de sección (1–12) | Display | 600 | 32pt | 1.05 |
| Subtítulo de sección | Display | 400 italic | 13pt | 1.4 |
| Título de anexo | Marker | 700 | 48pt | 1.0 |
| H3 dentro de sección | Display | 600 | 14pt | 1.2 |
| Cuerpo | Sans | 400 | 10.5pt | 1.5 |
| Callout título | Sans uppercase | 700 | 8.5pt tracking 0.04em | 1.2 |
| Callout cuerpo | Sans | 400 | 10pt | 1.5 |
| Folio | Sans | 400 | 8pt | 1 |
| Tabla cabecera | Sans uppercase | 600 | 8pt tracking 0.04em | 1 |
| Tabla cuerpo | Sans | 400 | 9.5pt | 1.3 |

### Detalles editoriales
- Versalitas (small caps) para "Mateo 6,21", "Asociación Eteciana".
- Cifras antiguas (old-style figures) en los números §1–12.
- Ligaduras (st, ct, fi, fl) activas.
- Italic verdadero (no falso) para citas bíblicas.
- ΙΧΘΥΣ en griego correcto (display debe tener glifos griegos).

---

## F. PORTADA — propuesta nueva

### F.1 Diagnóstico de la portada actual
- 9 elementos apilados (demasiado).
- ETC azul + 88 rojo desconectados de la paleta.
- 2 corazones marrón + negro (el negro no está en la paleta).
- Pez mediano, no héroe.
- "Siempre amigos" en portada es ruido (es lema eteciano, no del retiro).
- Sin estructura editorial (marco, filetes).

### F.2 Portada propuesta — Opción B

**Composición horizontal:** `ETC` — 🐟 pez héroe (55mm) — `88`

| Elemento | Spec |
|---|---|
| Formato | Media carta (5.5×8.5") o A5 (148×210mm) |
| Fondo | Crema `#F4EFE1` con grano sutil 4% |
| Eyebrow | "ENCUENTRO TOTAL CON CRISTO" — sans uppercase 8.5pt tracking 0.18em, marrón, centrado, a 25mm del borde superior, con filete fino abajo de 30mm de ancho |
| Bloque "ETC + 🐟 + 88" | "ETC" serif 64pt peso 700 marrón `#3A2A1A` + Pez 55mm centrado + "88" serif 64pt peso 700 dorado oscuro `#B58A2C`. Separación letras-pez: 12mm. Composición horizontal en mitad superior. |
| Pez | Versión heredada (la original), 55mm de alto, contorno marrón 1.5pt, las 5 letras en ΙΧΘΥΣ refinados, sombra suave 18% |
| Subtítulo | "Carpeta del equipo · 2026" — serif italic 14pt marrón al 70%, centrado, 12mm debajo |
| Bloque del lema | Cuadro 95mm ancho con filete dorado `#B58A2C` izquierdo 1.5mm. Interior: lema serif italic 22pt marrón alineado izquierda + "Mateo 6,21" small caps 9pt marrón 60% separado 4mm. Tercio inferior, centrado |
| Fecha | "4-6 de septiembre" serif italic 12pt marrón 80%, centrada, 18mm del borde inferior |
| Marco | Filete dorado al 5% en los 4 lados, a 8mm del borde físico |

### F.3 Cambios respecto a hoy
1. ❌ Quitas "Siempre amigos" + 2 corazones (van a portadilla interior y/o contracubierta).
2. ❌ Quitas "Carpeta del equipo" como subtítulo grande arriba (reemplazado por uno más limpio abajo).
3. ✅ Cambias colores: ETC azul + 88 rojo → **ETC marrón + 88 dorado oscuro**.
4. ✅ Cambias composición: vertical → **horizontal con pez al centro entre letras**.
5. ✅ Agregas filete dorado izquierdo en el bloque del lema (callout editorial).
6. ✅ Agregas marco dorado al 5% en bordes (estructura editorial).

### F.4 Contracubierta — nueva
- Pez héroe **45mm** centrado en tercio superior.
- "Siempre amigos · Jn 15,15" + **2 corazones dorados** (no marrón + negro).
- Pie institucional: "Asociación Eteciana · Obra de la Iglesia Católica · 2026".
- Mismo marco dorado.

---

## G. MAQUETACIÓN — ajustes estructurales

1. **Mover el "Mensaje de los directores" al FINAL** del booklet (después del Anexo IV de Oraciones). Hoy está en pág 23, en medio — rompe el flujo. La brújula va con él al final (no se quita, solo se reubica).
2. **Ajustar a 36 páginas** (múltiplo de 4 para imprenta cosida) — hoy 33. Con la contracubierta nueva entra 1 página, las 2 restantes son aire intencionado en portadillas.
3. **Portadillas de sección y anexos en página impar (derecha)**. Hoy 8 de 14 arrancan en par; los 4 anexos arrancan TODOS en par. Ajustar con páginas en blanco intencionadas (con marca de agua de pez al 6%).
4. **Retícula consistente:**
   - **1 columna larga:** narrativa (§1, §2, §5, §10, mensaje directores).
   - **2 columnas:** bullets cortos (§4, §8, §9, §11).
   - **Tabla a 1 columna ancha:** §6, §7, §12, tabla PG del Anexo I.
5. **Anexo IV · Oraciones:** marcar `[POR DEFINIR — texto pendiente]` bajo cada una de las 6 oraciones listadas (los textos los cierran Paul + Sor).
6. **Folio:** `ETC 88 · pág. N` — sans 8pt marrón al 50%, alineado al exterior. Sin folio en portada, portadillas y contracubierta.

---

## H. ELEMENTOS — sistema de iconografía

### H.1 Pez ICTUS en tres tamaños
| Uso | Tamaño | Tratamiento |
|---|---|---|
| Héroe (portada, contracubierta) | 55 mm / 45 mm | Full color con sombra suave |
| Medio (portadillas de anexo) | 22 mm | Color o contorno marrón |
| Mínimo (folio, separadores) | 4 mm | Solo contorno marrón |
| Marca de agua | — | 6–8% opacidad en portadillas de anexo |

### H.2 Sistema de 10 íconos custom
Diseñar como set coherente — todos trazo de línea marrón `#3A2A1A`, grosor 1.5pt, vértices redondeados, base 12mm:

| Ícono | Significado | Dónde |
|---|---|---|
| Pez | Símbolo central | Portada, separadores, cierre |
| Brújula | Hilo espiritual (apunta al corazón) | Mensaje de cierre |
| Banderín | Identidad del retiro | Anexo I (Guías) |
| Llama | Servicio, encendido | Anexo II (Cocina) |
| Notas musicales | Música, animación | Anexo III (Música) |
| Estrella | Oración / vigilia | Anexo IV (Oraciones) |
| 2 corazones | "Siempre amigos" | Portada (no), contracubierta (sí) |
| Libro abierto | Escrituras | §6 |
| Reloj | Horario | §7 |
| Maleta | Qué llevar | §8 |

### H.3 La brújula — específica
- **No náutica chillona** (sin colores rojo/azul).
- Marrón sobre crema, con la aguja apuntando al **lado del corazón** (no al norte literal).
- Tamaño 18–22 mm, opacidad 70%.
- Solo en el mensaje de directores (al final del booklet).

### H.4 Tablas
- **Zebra sutil:** `#F4EFE1` × `#EAE2CC` en filas alternas (horario, directorio, citas).
- **Horario VIE/SÁB/DOM:** colorear bloque de texto por tipo:
  - **Testimonio** → filete del color del área temática.
  - **Plenario** → fondo crema oscuro.
  - **PG (pequeño grupo)** → fondo crema claro.
  - **Comida** → marca dorada al margen.

### H.5 Portadillas de anexo — aprovechar el espacio
Cada portadilla incluye:
- **Sumario "Qué encontrarás aquí"** — 3 ítems.
- **Cita-eje del área** (regla de oro): Guías = *"Enfocados en el participante"* · Cocina = *"Entrega y sacrificio · Jn 13"* · Música = *"Animación espiritual antes que técnica"* · Oraciones = *"Oren sin cesar · 1 Tes 5,17"*.
- **Número romano gigante** (I, II, III, IV) al 20% opacidad como motivo de fondo.

---

## I. ADJUNTOS QUE LLEVA ESTE PROMPT

1. **`DIRECTORIO_EQUIPO_88.md`** — directorio completo de 53 servidores en tabla de 4 columnas (Nombre · Rol · Cumpleaños · Teléfono). **Úsalo tal cual para reemplazar §12 completo.** Asesores de comunidad enmascarados (Santo Domingo + La Vega sin nombres).
2. **`DESIGN_SYSTEM_ETC.md`** (project knowledge) — identidad visual.
3. **Textos fuente** (project knowledge) — `CARPETA_ETC88.txt` + `ANEXO_1_GUIA_DE_GUIAS.txt` + `ANEXO_2_COCINA.txt` + `ANEXO_3_MUSICA.txt` + `ANEXO_4_ORACIONES.txt`.

---

## J. ORDEN DE EJECUCIÓN

### Fase 1 — validar la dirección (antes de rehacer 33 páginas)
Pídele a Claude Design **una sola muestra**:
1. **Portada Opción B** + **contracubierta pareja** con las specs exactas de §F.
2. **Una página interior representativa** (sugiero la de "Roles" §3 o una portadilla de anexo) con la paleta refinada, tipografía recomendada y 2 íconos custom (pez + brújula).
3. **Test 1 tinta** de esa portada y esa página interior.

Si esa muestra se siente **editorial premium** (no documento bien hecho), el pez **domina sin saturar**, el lema **lee como eje espiritual** y sobrevive a **1 tinta** → la dirección es correcta. Apruebas y pasas a Fase 2.

### Fase 2 — rehacer el booklet completo
1. Aplica las 6 correcciones de contenido (§C).
2. Aplica la paleta refinada (§D).
3. Aplica la tipografía nueva (§E).
4. Construye la portada Opción B + contracubierta (§F).
5. Mueve el mensaje de directores al final + ajusta a 36 pp con portadillas en impar (§G).
6. Diseña el sistema de 10 íconos custom (§H.2).
7. Aplica el pez en tres tamaños (§H.1).
8. Mejora las tablas con zebra y bloques de color (§H.4).
9. Enriquece las portadillas de anexo (§H.5).
10. Marca placeholders en Anexo IV.
11. Reemplaza el directorio §12 completo con el archivo adjunto.
12. **Test 1 tinta** de todo el booklet + exporta PDF imprimible final.

---

*Prompt FINAL · 7-jun-2026. Auditado contra `data/estado.json` y `data/equipo.json` (fuente única). Pipeline verificado (9/9 PASS). Este archivo reemplaza todos los feedbacks/recomendaciones previos.*
