# Claude Design — montar un PROYECTO NUEVO para maquetar la Carpeta del ETC 88

> Guía paso a paso para arrancar **desde cero** un proyecto en Claude dedicado al diseño de la Carpeta. La idea: cargar una sola vez el **sistema de diseño + los textos + el logo** como *conocimiento del proyecto*, y a partir de ahí pedir las piezas en chats. Así el sistema (Dirección A · Expedición) queda "fijo" y no hay que repegarlo cada vez.

---

## 0. Antes de empezar — ten a mano estos archivos del repo
Súbelos desde tu copia del repo (carpeta `ETC88/`). Son los que el proyecto necesita "saber":

**El sistema de diseño (Dirección A):**
- `design/DESIGN_SYSTEM_A.md` — la especificación (paleta, tipografía, concepto, piezas).
- `design/A/01_logo.svg` … `design/A/07_iconografia.svg` — las 7 láminas de referencia (logo, tipografía/color, portada, interior, separadores, banderín, iconografía).
- `design/logo_eteciano.png` — el **pez ICTUS de colores** (el ícono/acento). *(Si ya generaste el oficial con `PROMPT_LOGO_PEZ.md`, sube ese.)*

**Los textos reales (lo que se va a maquetar):**
- `entrega_diseno/CARPETA_ETC88.txt` — el cuerpo de la Carpeta (12 secciones).
- `entrega_diseno/ANEXO_1_GUIA_DE_GUIAS.txt`
- `entrega_diseno/ANEXO_2_COCINA.txt`
- `entrega_diseno/ANEXO_3_MUSICA.txt`
- `entrega_diseno/ANEXO_4_ORACIONES.txt`

**El prompt principal (lo que vas a pegar en el primer chat):**
- `entrega_diseno/INSTRUCCION_CLAUDE_DESIGN.txt` — la instrucción "afinar-y-aplicar".

**Opcional (referencia de contenido / paridad de librito):**
- `entrega_diseno/CARPETA_ETC88.docx` — el booklet ya armado (sirve para que vea el orden, índice y tablas).

---

## 1. Crea el proyecto
1. Entra a **claude.ai** → barra lateral → **Projects** → **New project** (o "Crear proyecto").
2. Nómbralo: **`ETC 88 · Carpeta (Dirección A)`**.
3. Descripción corta: *"Maquetar la Carpeta del retiro ETC 88 aplicando el Design System Dirección A · Expedición."*

## 2. Carga el conocimiento del proyecto (una sola vez)
En el panel del proyecto, en **Project knowledge** (o "Conocimiento") → **Add content / subir archivos**:
1. Sube **todos los archivos del paso 0** (el `.md` del sistema, los 7 `.svg`, el `.png` del logo, los 5 `.txt`, y el `.docx` opcional).
2. Esto queda disponible para **todos los chats** del proyecto — no hay que volver a subirlo.

## 3. Pon las instrucciones del proyecto (las reglas que no cambian)
En **Project instructions / "Set custom instructions"**, pega esto:

> Eres el diseñador de la **Carpeta del retiro ETC 88**. Trabajas con el **Design System Dirección A · Expedición** que está en el conocimiento del proyecto (`DESIGN_SYSTEM_A.md` + los SVG de `design/A/`). **No reconstruyas el sistema: aplícalo.**
> **Reglas fijas:**
> - Paleta: azul profundo `#1B3A5C`, arena `#E8D4A8`, coral `#E36C4F`, crema `#F7F1E3`, tinta `#1A1A1A`. Tipografía: **Cormorant Garamond** (display) + **Inter** (cuerpo).
> - **Lema del retiro:** *"Donde está tu tesoro, allí estará tu corazón"* · **Mt 6,21**. Cita complementaria: Mt 13,44. Lema eteciano: "Siempre amigos" · Jn 15,15.
> - Símbolo central: la **brújula del corazón** que apunta al tesoro (la estrella polar = Cristo). El **pez ICTUS** es el acento. **Nada de cofre pirata, calavera ni mapa con X.** Sobrio, contemplativo, gozoso — es un retiro católico.
> - Retiro: **4–6 sep 2026 · Casa La Ceiba del Salado, Higüey · San Pedro de Macorís.**
> - **No inventes** nombres ni cifras: usa solo el texto del conocimiento. **Sin conteos ni nombres** en piezas atemporales (portada, banderín). Si falta un dato, pídemelo o déjalo como placeholder.
> - Entrega imprimible y barato: que todo **sobreviva a 1 tinta**; el pez a color como único acento full-color.

## 4. Primer chat — establecer y aplicar el sistema
1. Abre un **chat nuevo dentro del proyecto**.
2. Pega el contenido de **`entrega_diseno/INSTRUCCION_CLAUDE_DESIGN.txt`** (el prompt "afinar-y-aplicar").
3. Añade al final: *"El sistema, el logo y los textos están en el conocimiento del proyecto. Empieza confirmándome en 3 líneas que el sistema está cargado (paleta + tipografía + concepto) y muéstrame la **portada** como primera pieza."*
4. Claude responde con un **artifact** (SVG/HTML) que puedes previsualizar a la derecha.

## 5. Pide las piezas en orden (una por mensaje)
Avanza pieza por pieza para poder corregir cada una:
1. **Portada** — lema Mt 6,21 + datos del retiro + pez-brújula.
2. **Índice / tabla de contenido** (12 secciones + 4 anexos).
3. **Páginas interiores** fluyendo el texto de la Carpeta (`CARPETA_ETC88.txt`).
4. **Separadores por sección** y **por área** (Guías / Cocina / Música / Asesores) con los mensajes pastorales de Padre Paul.
5. **Los 9 temas** como una secuencia visual sobria (ruta del retiro).
6. **Portadillas de los 4 anexos** (Guías, Cocina, Música, Oraciones) — cada uno abre como capítulo.
7. **Tablas** formateadas: horario (VIE/SÁB/DOM) y directorio del equipo (déjalo como **plantilla**, se llena al final).
8. **Pie de página** con folio + "ETC 88 · Higüey 2026".

Para cada pieza, si hay más de una salida posible, pídele: *"dame 2 opciones y una recomendación."*

## 6. Itera
- Corrige con frases concretas: *"sube el contraste del subtítulo", "el pez más pequeño en la portada", "esta tabla a 1 tinta"*.
- Si se desvía del sistema, recuérdale: *"aplica `DESIGN_SYSTEM_A.md`, no inventes paleta."*

## 7. Exporta
1. En cada artifact, usa **Copy / Download** (SVG o PNG; HTML si es maqueta de varias páginas).
2. Para el librito completo, pídele: *"compón todo en un solo documento imprimible (media carta / A5), con folios e índice"* y expórtalo a **PDF**.
3. Guarda los exportables en `entrega_diseno/` del repo (o donde lleves los finales) y, cuando esté aprobado, súbelo a la carpeta de Drive **"ETC 88 · ENTREGABLES (oficial)"**.

---

## Notas
- **Proyecto nuevo vs. sesión vieja:** si ya tenías una sesión con el sistema cargado, no hace falta el proyecto; pero el proyecto es mejor porque el conocimiento queda fijo y compartible. Esta guía cubre el caso **desde cero**.
- **El logo** tiene sus propios colores (celeste/rojo/azul/naranja/magenta); el sistema de la Carpeta (azul/arena/coral) lo **enmarca**. No los mezcles dentro de una misma pieza salvo el pez como acento.
- **Antes de imprimir:** confirma con la imprenta el **# de tintas** y el formato (media carta o A5).

---
*Pasos para montar el proyecto de Claude Design de la Carpeta ETC 88 · Dirección A · Expedición.*
