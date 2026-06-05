# Claude Design — montar un PROYECTO NUEVO para maquetar la Carpeta del ETC 88

> Guía paso a paso para arrancar **desde cero** un proyecto en Claude dedicado al diseño de la Carpeta, con la **identidad ORIGINAL del ETC** (el pez ICTUS de colores). La idea: cargar una sola vez la **identidad + los textos + el logo** como *conocimiento del proyecto*, y a partir de ahí pedir las piezas en chats. Así no hay que repegar todo cada vez.

---

## 0. Antes de empezar — ten a mano estos archivos del repo
Súbelos desde tu copia del repo (carpeta `ETC88/`). Son los que el proyecto necesita "saber":

**La identidad (original del ETC):**
- `design/DESIGN_SYSTEM_ETC.md` — la especificación (logo, paleta derivada del logo, estética, aplicación a la Carpeta).
- **El LOGO ORIGINAL del ETC** — el archivo del **pez ICTUS de colores** que tienes. ⚠️ **Súbelo tú** (no usamos una recreación). Guárdalo como `design/logo_eteciano_oficial.png` y súbelo.

**Los textos reales (lo que se va a maquetar):**
- `entrega_diseno/CARPETA_ETC88.txt` — el cuerpo de la Carpeta (13 secciones, incluye el mensaje de los directores al final).
- `entrega_diseno/ANEXO_1_GUIA_DE_GUIAS.txt`
- `entrega_diseno/ANEXO_2_COCINA.txt`
- `entrega_diseno/ANEXO_3_MUSICA.txt`
- `entrega_diseno/ANEXO_4_ORACIONES.txt`
- `entrega_diseno/DIRECTORIO_EQUIPO_88.md` — la lista del equipo por área, con cumpleaños (para la página de directorio).

**El prompt principal (lo que vas a pegar en el primer chat):**
- `entrega_diseno/INSTRUCCION_CLAUDE_DESIGN.txt` — la instrucción de diseño.

**Opcional (referencia de contenido / paridad de librito):**
- `entrega_diseno/CARPETA_ETC88.docx` — el booklet ya armado (sirve para que vea el orden, índice y tablas).

---

## 1. Crea el proyecto
1. Entra a **claude.ai** → barra lateral → **Projects** → **New project** (o "Crear proyecto").
2. Nómbralo: **`ETC 88 · Carpeta`**.
3. Descripción corta: *"Maquetar la Carpeta del retiro ETC 88 con la identidad original del ETC (pez ICTUS de colores)."*

## 2. Carga el conocimiento del proyecto (una sola vez)
En el panel del proyecto, en **Project knowledge** (o "Conocimiento") → **Add content / subir archivos**:
1. Sube **todos los archivos del paso 0** (el `DESIGN_SYSTEM_ETC.md`, el **logo original**, los 5 `.txt`, el `DIRECTORIO_EQUIPO_88.md`, y el `.docx` opcional).
2. Esto queda disponible para **todos los chats** del proyecto — no hay que volver a subirlo.

## 3. Pon las instrucciones del proyecto (las reglas que no cambian)
En **Project instructions / "Set custom instructions"**, pega esto:

> Eres el diseñador de la **Carpeta del retiro ETC 88**. Usas la **identidad ORIGINAL del ETC**: su símbolo es el **pez ICTUS de colores** (ΙΧΘΥΣ). El sistema está en `DESIGN_SYSTEM_ETC.md` (en el conocimiento del proyecto). **Aplícalo; no inventes una identidad nueva.**
> **Reglas fijas:**
> - **Logo:** el **pez ICTUS de colores original** (archivo adjunto) — úsalo como está, **no lo rediseñes**; en la Carpeta se le agrega **"ETC 88"**.
> - Paleta (derivada del logo): amarillo dorado `#E9C44E`, marrón `#4E3119`, crema `#F7F1E3`, tinta `#2A2118`; **acentos = las 5 letras ΙΧΘΥΣ** (celeste `#B7E9EC`, rojo `#DA1F22`, azul `#1E2BB6`, naranja `#F0871F`, magenta `#D21C82`) como acentos puntuales (uno por área/sección), no en bloques grandes.
> - **Lema del retiro:** *"Donde está tu tesoro, allí estará tu corazón"* · **Mt 6,21** (en la portada). Complementaria: Mt 13,44. Lema eteciano: "Siempre amigos" · Jn 15,15.
> - Tono **cálido, amistoso y gozoso**, con el respeto de un retiro católico. **Nada de náutico/expedición/brújula ni cofre pirata.**
> - Retiro: **4–6 sep 2026 · Casa La Ceiba del Salado, Higüey · San Pedro de Macorís.**
> - **No inventes** nombres ni cifras: usa solo el texto del conocimiento. **Sin conteos** en piezas atemporales (portada). Si falta un dato, pídemelo o déjalo como placeholder.
> - Imprimible y barato: que todo **sobreviva a 1 tinta**; el pez a color como único acento full-color.

## 4. Primer chat — establecer y aplicar el sistema
1. Abre un **chat nuevo dentro del proyecto**.
2. Pega el contenido de **`entrega_diseno/INSTRUCCION_CLAUDE_DESIGN.txt`** y **adjunta el logo original** en ese mensaje.
3. Añade al final: *"El sistema, el logo y los textos están en el conocimiento del proyecto. Confírmame en 3 líneas que el sistema está cargado (logo + paleta + tono) y muéstrame la **portada** como primera pieza."*
4. Claude responde con un **artifact** (SVG/HTML) que puedes previsualizar a la derecha.

## 5. Pide las piezas en orden (una por mensaje)
Avanza pieza por pieza para poder corregir cada una:
1. **Portada** — el **pez ICTUS original a color** + **"ETC 88"** + el lema *"Donde está tu tesoro…"* (Mt 6,21) + fechas y lugar. **Sin conteos.**
2. **Índice / tabla de contenido** (13 secciones + 4 anexos).
3. **Páginas interiores** fluyendo el texto de la Carpeta (`CARPETA_ETC88.txt`).
4. **Separadores por sección** y **por área** (Guías / Cocina / Música / Asesores) — un color de los 5 por área, con los mensajes pastorales de Padre Paul.
5. **Los 9 temas** como una secuencia visual sobria (ruta del retiro).
6. **Portadillas de los 4 anexos** (Guías, Cocina, Música, Oraciones) — cada uno abre como capítulo.
7. **Directorio del equipo** — usa la lista real `DIRECTORIO_EQUIPO_88.md` (por área, **con cumpleaños**); marca coordinadores.
8. **Mensaje de los directores** — ya viene al final del texto de la Carpeta; trátalo como página de cierre.
9. **Tablas** del horario (VIE/SÁB/DOM). **Pie** con folio + "ETC 88 · Higüey 2026".

Para cada pieza, si hay más de una salida posible, pídele: *"dame 2 opciones y una recomendación."*

## 6. Itera
- Corrige con frases concretas: *"el pez más pequeño en la portada", "esta tabla a 1 tinta", "usa el magenta solo en los títulos de Cocina"*.
- Si se desvía, recuérdale: *"aplica `DESIGN_SYSTEM_ETC.md` y el logo original, no inventes paleta."*

## 7. Exporta
1. En cada artifact, usa **Copy / Download** (SVG o PNG; HTML si es maqueta de varias páginas).
2. Para el librito completo, pídele: *"compón todo en un solo documento imprimible (media carta / A5), con folios e índice"* y expórtalo a **PDF**.
3. Guarda los exportables en `entrega_diseno/` del repo y, cuando esté aprobado, súbelo a la carpeta de Drive **"ETC 88 · ENTREGABLES (oficial)"**.

---

## Notas
- **Proyecto nuevo vs. sesión vieja:** el proyecto es mejor porque el conocimiento queda fijo y compartible. Esta guía cubre el caso **desde cero**.
- **El color:** la base es **marrón + dorado + crema** (sobria); las **5 letras-color** son acentos puntuales y el **pez a color** es el único elemento full-color. Así se conserva la alegría del logo sin volverse ruidoso.
- **Antes de imprimir:** confirma con la imprenta el **# de tintas** y el formato (media carta o A5).

---
*Pasos para montar el proyecto de Claude Design de la Carpeta ETC 88 · identidad original del ETC (pez ICTUS de colores).*
