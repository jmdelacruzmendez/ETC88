# Hosting del Tablero ETC 88 — al día, en GitHub, y dinámico con Drive

Estado: **Fase 1 lista en código** (este commit). Faltan 3 pasos que dependen de tu
cuenta (no los puede hacer Claude). Abajo, qué quedó hecho y qué falta.

## Lo que YA quedó hecho (código)
- `requirements.txt` — dependencias del pipeline (para que el CI sea reproducible).
- `.github/workflows/deploy.yml` — GitHub Actions:
  - **build**: instala deps, corre `run_all.sh` + `verify.py` (compuerta) y sube `public/`.
  - **deploy**: publica `public/` en GitHub Pages.
  - Dispara en: cada push (build+verify), **cron diario** (cuenta regresiva al día) y manual.
- `public/index.html` ya lo genera `build_campana.py` (el tablero de campaña, sin nombres de pagos).

## Lo que falta — 3 pasos tuyos (una sola vez)
1. **Activar Pages:** repo → *Settings* → *Pages* → *Build and deployment* → **Source: GitHub Actions**.
2. **Fusionar esta rama a la rama por defecto** del repo (los cron y el deploy automático solo
   corren desde ahí). Tras el merge, el tablero se redepliega en cada push y **se actualiza solo cada día**.
3. (Opcional) **Dominio propio** en *Settings → Pages → Custom domain*.

> Resultado de la Fase 1: **tablero de campaña público, en una URL de GitHub, al día.**

## Fase 2 — "dinámico con Drive" (datos vivos)
El tablero `web/tablero.html` ya trae un bloque `CONFIG` para **modo vivo**:
- **Datos agregados (público):** en Google Sheets → *Archivo → Compartir → Publicar en la web → CSV*,
  copia cada URL en `CONFIG` de `web/tablero.html`. El tablero se actualiza cuando el equipo edita la hoja.
  *Ojo: "publicar" = público para cualquiera con el link.* Úsalo solo para cifras SIN nombres.
- **Datos por nombre (Control de Pagos / Captación — privados):** NO publicar. Dos rutas:
  1. **Google Apps Script** (web app que lee las hojas privadas, restringida a una lista de correos).
  2. **GitHub Action + cuenta de servicio de Google** (lee las hojas por API, regenera y despliega)
     detrás de un **portón por correo** (Cloudflare Access, gratis ≤50). Requiere crear la cuenta de
     servicio y guardar su credencial como **secreto del repo** (eso lo haces tú).

## Regla que NO cambia
`data/estado.json` sigue siendo la **fuente de los hechos confirmados** (presupuesto, cuotas,
decisiones). El Sheet de Drive solo alimenta **lo que se mueve** (pagos recibidos, donaciones,
captación). Así no hay dos "verdades" y `verify.py` sigue cuidando lo confirmado.

## Privacidad (resumen)
- **Público:** tablero de campaña (costo, presupuesto, cuotas, simulador — *sin nombres*).
- **Privado:** Control de Pagos y Captación (con nombres) → siempre detrás de portón o en el Excel interno.
