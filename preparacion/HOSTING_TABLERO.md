# Hosting del Tablero ETC 88 — privacidad primero

> **Decisión (26-jun-2026):** el repositorio principal pasa a **PRIVADO** y el tablero
> público se hospeda **APARTE**. Motivo: el repo estaba **público** y versionaba datos
> sensibles (salud/alergias/medicamentos y teléfonos del equipo, nombres de
> participantes **menores**, donantes personales y el formulario crudo). Un repo
> privado es el "portón" que pide la regla de privacidad de CLAUDE.md.

## Qué es PÚBLICO y qué es PRIVADO
- **Público (se puede hospedar y compartir):** el **Tablero de la Tripulación**
  (`tablero_campana_etc88.html`, idéntico a `public/index.html`). Autocontenido
  (HTML+CSS+JS, sin archivos externos). Verificado **sin nombres**: solo cifras
  agregadas (costo, cuotas, meta, brecha, simulador, cuenta regresiva) y los
  contactos de **Co-Dirección** (que ya van firmados en las cartas).
- **Privado (NUNCA en hosting público):** `data/equipo.json` (salud), `data/participantes.json`
  y `web/captacion.csv` (menores), `web/equipo.csv` (roster), `data/fuente_formulario.xlsx`
  (formulario crudo), directorios de donantes, y el **tablero interno**
  `web/tablero.html` (muestra equipo y captación **con nombres**).

## Paso 1 — Poner el repo en PRIVADO (lo haces tú, ~30 s) — URGENTE
GitHub → repo **ETC88** → **Settings** → (pestaña *General*, hasta abajo)
*Danger Zone* → **Change repository visibility** → **Make private** → confirmar.
Esto corta la exposición pública al instante.

## Paso 2 — Hospedar el tablero público APARTE
GitHub Pages **gratis no sirve en repo privado**, por eso el tablero va aparte.
Es **un solo archivo autocontenido**, así que hay dos rutas fáciles:

**A) Repo público nuevo + GitHub Pages (recomendado, todo en GitHub)**
1. Crea un repo **nuevo y público**, p. ej. `etc88-tablero` (vacío).
2. Sube el archivo `tablero_campana_etc88.html` y renómbralo **`index.html`**
   (arrastrar y soltar en la web de GitHub → *commit*).
3. *Settings → Pages → Build and deployment → Source: Deploy from a branch →*
   rama por defecto, carpeta `/ (root)` → *Save*.
4. Link: **`https://jmdelacruzmendez.github.io/etc88-tablero/`** (sale tras el 1.er deploy).

**B) Cloudflare Pages (sin segundo repo)**
Cuenta gratis → *Create a project → Direct Upload* → arrastra el archivo (como
`index.html`) → publica. Link: `https://<proyecto>.pages.dev`.

> Como el archivo es autocontenido, también se puede simplemente **enviar por
> WhatsApp/Drive** y se abre en cualquier navegador, sin hosting.

## "Dinámico con Drive" (datos vivos) — estado
- El tablero **público** muestra cifras **confirmadas** (de `estado.json`) + cuenta
  regresiva. Es estático (se regenera con el pipeline).
- El tablero **interno** `web/tablero.html` ya lee **en vivo** la hoja *Control de Pagos*
  de Drive (CSV, sin nombres en esa hoja) — pero como también pinta equipo/captación
  **con nombres**, se queda **privado**.
- **Opción pendiente de tu visto bueno:** añadir al tablero **público** un dato vivo
  **"Recaudado a la fecha"** (termómetro, **sin nombres**) leído de la hoja de Drive.
  Es coherente con lo que ya muestra (meta/brecha) y da el "vivo con Drive" sin exponer a nadie.

## Regla que NO cambia
`data/estado.json` es la **fuente de los hechos confirmados**. La hoja de Drive solo
alimenta **lo que se mueve** (pagos). `verify.py` sigue siendo la compuerta.
