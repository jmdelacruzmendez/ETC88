# Mi recomendación de diseño para el ETC 88

> Como diseñador editorial revisando el booklet actual: la base está sólida (pez ICTUS heredado, paleta amarillo/marrón/crema, los 5 colores de las letras griegas). Pero hay margen para que se sienta más **editorial y menos genérico**. Recomendaciones por bloque.

---

## 1. PALETA — refinar lo que ya tienes

### 1.1 Mi crítica a la paleta actual
- **El verde de Guías no pertenece** — rompe el sistema ΙΧΘΥΣ y se siente más "scout" que "ETC".
- **Los colores ΙΧΘΥΣ son puros y saturados** (rojo `#DA1F22`, azul `#1E2BB6`, magenta `#D21C82`) — funcionan bien en el pez chiquito, pero en bloques grandes saturarían y compiten con el dorado del pez. Hay que **tenerlos en dos versiones**: pura (acentos puntuales) y desaturada (filetes, fondos).
- **El crema actual (`#F7F1E3`) es muy claro** — en impresión puede verse amarillento o casi blanco. Probaría bajarlo un toque a `#F4EFE1` (más cuerpo de papel).

### 1.2 Paleta refinada — mi propuesta

**Base (sobria, de papel):**
| Rol | HEX | Uso |
|---|---|---|
| Papel | `#F4EFE1` | Fondo principal |
| Papel cálido | `#EAE2CC` | Filas alternas de tabla (zebra), fondos de callout |
| Marrón principal | `#3A2A1A` | Texto cuerpo, filetes |
| Marrón suave | `#6B4F38` | Texto secundario, fondos discretos |
| Dorado pez | `#E9C44E` | Acento cálido principal (pez, realces) |
| Dorado oscuro | `#B58A2C` | Acentos dorados que necesitan más contraste |

**Acentos ΙΧΘΥΣ (las 5 letras del pez) — versión PURA (acentos puntuales):**
| Letra | Rol | HEX |
|---|---|---|
| Ι (iota) | Guías | `#3FA5B0` ← te recomiendo bajar el celeste actual `#B7E9EC` que es muy claro |
| Χ (ji) | Asesores del retiro | `#B5392C` ← una versión más cálida y editorial del rojo `#DA1F22` |
| Θ (theta) | Cocina | `#253C8F` ← un azul más profundo/eteciano que el `#1E2BB6` original |
| Υ (ípsilon) | Música | `#D77B2A` ← naranja más oscuro y editorial que el `#F0871F` |
| Ϲ (sigma) | Asesores espirituales / Cierre | `#A02C68` ← magenta menos chillón que `#D21C82` |

**Acentos ΙΧΘΥΣ — versión TINTA (10–15% saturación, para fondos):**
Usa estos como sombra de fondo cuando necesites territorialidad (header de tabla del directorio por área, callouts del área, marca de página del anexo). Son las mismas familias pero al 12% — mantienen el color sin gritar.

**Modo 1-tinta (para imprenta económica):**
Todo el booklet debe sobrevivir a 1 tinta marrón sobre crema. Tradúcelo así:
- Marrón principal → tinta plena (100%)
- Acentos de área → tono medio (60%)
- Filetes secundarios → tono claro (35%)
- Marca de agua del pez → tono muy claro (15%)
- El pez pasa de full-color a contorno marrón solo.

### 1.3 Cómo asignar el color al booklet
- **Áreas operativas** (sección §3 + 4 anexos) = color de su letra ΙΧΘΥΣ.
- **Números de sección §1–§12** = todos en marrón. El color tiene que **decir algo**; si lo riegas en cada número se vuelve ornamento.
- **Callouts importantes** (los azules tipo "El retiro dura tres días, pero comienza el cuarto día") = mantenerlos en azul (Θ) — son momentos de énfasis transversales.
- **Citas bíblicas** (los pies de página tipo "ya no los llamo siervos…") = filete dorado, no de color área.

---

## 2. TIPOGRAFÍA — la decisión más importante

### 2.1 Mi crítica a la tipografía actual
- El **display serif** que usas es bonita pero **se siente genérica** (parece una de las defaults del sistema). Una serif con más carácter elevaría todo el booklet de "imprimible" a "editorial".
- La **fuente marker de los anexos** está bien (cálida, manual) pero hoy el grosor es muy ligero — se ve débil cuando debería gritar "es un anexo, hay un cambio aquí".
- El **sans del cuerpo** es funcional pero no aporta personalidad eteciana — podría ser una humanista cálida en vez de una geométrica neutra.

### 2.2 Mi recomendación de pareja tipográfica

**TODAS son de licencia abierta (Google Fonts / SIL OFL), pasan por imprenta sin problema.**

**Opción A — Mi favorita: "Editorial cálida":**
- **Display:** `Fraunces` (Google Fonts) — serif moderna con opciones de variabilidad (peso, óptico, "soft"). Carácter editorial sin ser pesada. Tiene **glifos griegos** (importante para ΙΧΘΥΣ).
- **Cuerpo:** `Inter` (Google Fonts) — sans humanista, hiperlegible, neutral pero cálido.
- **Marker (anexos):** `Caveat Brush` o `Permanent Marker` (la actual está cercana) — pero **en peso 700** para que se vea fuerte.

**Opción B — "Más clásica/católica":**
- **Display:** `Cormorant Garamond` (Google Fonts) — serif clásica estilo Garamond. Más tradicional, evoca devocional/litúrgico. Glifos griegos disponibles.
- **Cuerpo:** `Source Serif 4` para texto largo + `Source Sans 3` para etiquetas y datos.
- **Marker:** `Indie Flower` para anexos (más amable que marker).

**Opción C — "Más calidez manual":**
- **Display:** `DM Serif Display` (alto contraste, elegante) o `Lora` (legible y cálida).
- **Cuerpo:** `Atkinson Hyperlegible` (creada por la fundación Braille; altísima legibilidad).
- **Marker:** `Caveat` (más relajada y manuscrita que marker).

### 2.3 Jerarquía sugerida

| Elemento | Familia | Peso | Tamaño | Interlineado |
|---|---|---|---|---|
| Portada — "ETC 88" | Display | 800 | 96pt | 1.0 |
| Portada — lema | Display | 400 italic | 22pt | 1.3 |
| Portadilla interior — título | Display | 500 | 36pt | 1.1 |
| Título de sección (1–12) | Display | 600 | 32pt | 1.05 |
| Subtítulo de sección | Display | 400 italic | 13pt | 1.4 |
| Título de anexo | Marker | 700 | 48pt | 1.0 |
| H3 dentro de sección | Display | 600 | 14pt | 1.2 |
| Cuerpo | Sans | 400 | 10.5pt | 1.5 |
| Cuerpo énfasis | Sans | 600 | 10.5pt | 1.5 |
| Callout título | Sans uppercase | 700 | 8.5pt | 1.2 |
| Callout cuerpo | Sans | 400 | 10pt | 1.5 |
| Folio | Sans | 400 | 8pt | 1 |
| Tabla cabecera | Sans uppercase | 600 | 8pt letter-spacing 0.04em |
| Tabla cuerpo | Sans | 400 | 9.5pt | 1.3 |

### 2.4 Detalles que elevan
- **Versalitas (small caps)** para "Encuentro Total con Cristo", "Asociación Eteciana", "Mateo 6,21" — la display debe tenerlas.
- **Cifras antiguas (old-style figures)** para los números 1–12 de los íconos de sección — dan estética de libro impreso clásico.
- **Ligaduras tipográficas** activas (st, ct, fi, fl) — pequeño detalle de elegancia editorial.
- **Italic verdadero** (no falso) para citas bíblicas — la Display debe tener italic real.
- **ΙΧΘΥΣ en griego correcto** (no "transliterado") — verificar que la display tenga glifos griegos cubiertos.

---

## 3. ELEMENTOS GRÁFICOS — sistema, no improvisación

### 3.1 El pez ICTUS — sí, pero con sistema
El pez es el héroe. Mi recomendación de **tres tamaños de uso**:
- **Pez héroe (portada y contracubierta):** 50 mm. Full color, con detalle, sombra suave.
- **Pez medio (portadillas de anexo, cierre):** 22 mm. Color o contorno marrón según contexto.
- **Pez mínimo (folio, separador):** 4 mm. **Solo contorno marrón**, sin colores. Como bullet.

### 3.2 Iconografía secundaria — falta sistema
Hoy aparecen ad-hoc:
- Brújula (mensaje de directores)
- Banderín (Anexo Guías)
- Ícono "fogón/llama" (Anexo Cocina)
- Notas musicales (Anexo Música)
- Estrella (Anexo Oraciones)

**Mi recomendación:** sistematizar esos íconos en **un set coherente** — todos en **trazo de línea marrón**, mismo grosor (1.5 pt), mismo estilo (geométrico amable, redondeado en vértices). Como una **familia de glifos del ETC 88**:

| Ícono | Significado | Anexo / Sección |
|---|---|---|
| 🐟 Pez | Símbolo central | Portada, separador |
| 🧭 Brújula | Hilo espiritual (corazón apunta a Cristo) | Mensaje de cierre |
| 🚩 Banderín | Identidad del retiro | Anexo I Guías |
| 🔥 Llama | Servicio, encendido | Anexo II Cocina |
| 🎵 Nota | Música, animación | Anexo III Música |
| ✨ Estrella | Oración / vigilia | Anexo IV Oraciones |
| ❤️ Corazón (dos) | "Siempre amigos" / lema eteciano | Portada, cierre |
| 📖 Libro abierto | Escrituras | §6 |
| ⏱️ Reloj | Horario | §7 |
| 🎒 Maleta | Qué llevar | §8 |

**Diseñarlos como un set custom** (no usar emoji directos), en marrón sobre crema, todos del mismo tamaño base (12 mm) y proporción. Esto eleva el booklet de "documento con íconos" a "sistema visual".

### 3.3 Motivos gráficos — sutiles, no decorativos
- **Filete superior de sección** (3–5 mm desde el título): línea fina marrón al 60%, con un **pequeño detalle** al inicio (un punto del color del área, o un pez minúsculo). Hoy es solo línea.
- **Punto al final del título de subsección** (●): toma el color del área. Marca de territorialidad sutil.
- **Línea punteada del mensaje de directores**: bonita. Generalizarla como **motivo de unión** entre páginas que comparten un eje (ej. puede aparecer entre las páginas del Anexo IV de Oraciones uniendo cada oración).
- **Marca de agua del pez**: al 6–8% en las portadillas de anexo. Solo en portadillas, no en todas las páginas.

### 3.4 Firmas y marca de autoría
Las **firmas manuscritas** de Juan Manuel y Jean Carlo en pág 23 son **lo mejor del booklet** — dan calidez humana. Mantenerlas. **Sugerencia:** una firma colectiva tipo "Equipo ETC 88" al pie de la contracubierta (más relajada, casi de bitácora).

### 3.5 Bordes y enmarcado
El **borde dorado** alrededor del mensaje de directores (pág 23) está bien — es la única página con borde, marca el momento. **No lo extiendas a otras páginas**; perdería su valor.

### 3.6 La brújula — específica
La brújula del cierre debe ser:
- **No náutica chillona** — sin flecha N/E/S/O con colores rojo/azul.
- **Marrón sobre crema**, con la aguja apuntando al **lado del corazón** (no al norte).
- **Tamaño 18–22 mm** — no compite con la firma.
- Al 70% de opacidad, para que se sienta como evocación, no como instrumento.

---

## 4. PRINCIPIOS DE COMPOSICIÓN — el booklet completo

### 4.1 Aire (white space)
El booklet actual tiene espacios desiguales. Mi regla:
- **Margen interior** (lomo): 18 mm — siempre.
- **Margen exterior**: 14 mm — donde va el folio.
- **Margen superior**: 16 mm.
- **Margen inferior**: 18 mm.
- **Entre título de sección y cuerpo**: 8 mm.
- **Entre párrafos**: 3 mm.
- **Antes de un H3**: 6 mm. Después: 2 mm.

### 4.2 Color cromático
**Regla del 60-30-10:**
- **60% crema** (papel respira).
- **30% marrón** (texto, filetes, estructura).
- **10% acento** (un solo color de área por sección, no varios mezclados).

Hoy el booklet riega los 5 colores ΙΧΘΥΣ en cada página. **Disciplina:** en una página solo se permite el color del área correspondiente + marrón + crema + dorado del pez.

### 4.3 Densidad de información
El booklet impreso en media carta o A5 admite **300–450 palabras por página** sin saturarse. Hoy algunas páginas (§9 reglas, §11 glosario) están más densas y se sienten amontonadas; otras (portadillas de anexo) están casi vacías. **Recalibrar densidad** para que el ritmo sea constante.

---

## 5. RESUMEN — qué cambiaría hoy mismo

| # | Cambio | Impacto |
|---|---|---|
| 1 | Display: cambiar a **Fraunces** o **Cormorant Garamond** | Eleva carácter editorial |
| 2 | Cuerpo: **Inter** o **Atkinson Hyperlegible** | Más legibilidad y calidez |
| 3 | Marker en peso 700 (más fuerte) | Anexos marcan transición clara |
| 4 | Guías: verde → **celeste Ι desaturado** (`#3FA5B0`) | Alinea con sistema ΙΧΘΥΣ |
| 5 | Crema más cálido (`#F4EFE1`) | Sensación de papel impreso |
| 6 | Iconografía custom de 10 glifos en trazo marrón | Sistema, no improvisación |
| 7 | Pez en tres tamaños (50/22/4 mm) | Símbolo presente sin saturar |
| 8 | Números de sección §1–12 todos en marrón | El color dice algo, no es ornamento |
| 9 | Regla 60-30-10 en cada página | Disciplina cromática |
| 10 | Zebra `#F4EFE1` × `#EAE2CC` en tablas | Lectura más cómoda |

---

## 6. UN TEST RÁPIDO

Si Claude Design quiere ver si la propuesta funciona, pídele:
1. **Una sola página de muestra** con la paleta refinada, las 3 familias tipográficas en jerarquía, y 2 íconos custom de prueba (pez + brújula).
2. **Antes/después** de la portada y de una portadilla de anexo.
3. **Test 1 tinta** de esa página.

Si esa página se siente "premium editorial" en vez de "documento bien hecho", la dirección es correcta.

---

*Recomendación profesional · 7-jun-2026. Generada como diseñador editorial revisando el booklet de 33 pp del ETC 88. Todas las fuentes mencionadas son de licencia abierta (Google Fonts / SIL OFL) y pasan por imprenta sin restricciones.*
