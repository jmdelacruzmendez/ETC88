# Tablero ETC 88 — web/

Tablero de signos vitales del retiro (días al retiro · finanzas vs meta · captación · pendientes · equipo). Se genera con `python scripts/build_web.py` (lee `data/*.json`).

## Archivos
| Archivo | Qué es | Cuándo usarlo |
|---|---|---|
| `tablero.html` | Tablero que lee los CSV de al lado (`equipo.csv`, `control_pagos.csv`, `captacion.csv`, `pendientes.csv`). Soporta **modo vivo** si llenas el bloque `CONFIG`. | desarrollo local · GitHub Pages · modo vivo |
| `tablero_offline.html` | **Autocontenido**: los datos van embebidos dentro del archivo. **No necesita red, no expone nada público.** Es un *snapshot* de la última corrida. | **compartir privado con un equipo puntual** |
| `*.csv` | Las 4 alimentaciones (foto de `data/` al correr el build). | las consume `tablero.html` |

## Modos de `tablero.html`
- **Snapshot (por defecto):** lee los `*.csv` locales. Se refresca corriendo `build_web.py`.
- **Vivo:** en el bloque `CONFIG` pega la URL de cada Google Sheet *publicada como CSV* (Archivo → Compartir → Publicar en la web → CSV). El tablero se actualiza solo cuando el equipo edita la hoja. **Ojo:** publicar = público para cualquiera con el link.

## Cómo darlo a un equipo puntual SIN hacerlo público
`tablero_offline.html` resuelve la mitad (no expone datos en una URL). Para que **solo el equipo lo vea**, ponle un candado de acceso. Dos rutas (decisión del director):

1. **App de Google Apps Script (vivo + privado, Google-nativo).** Un script que sirve el tablero y lee las hojas *privadas* directamente, restringido a una lista de correos. Nada se publica. Más plomería, pero todo dentro de Google.
2. **Snapshot + portón de acceso (lo más simple).** Sube `tablero_offline.html` detrás de un portón por correo (p. ej. Cloudflare Access, gratis ≤50 personas). El equipo entra con su correo; nadie más abre. Para actualizar, regeneras el archivo y lo reemplazas.

> El archivo `tablero_offline.html` por sí solo **no tiene contraseña**: quien tenga el archivo ve los datos. El candado lo pone el hosting (ruta 1 o 2). No lo subas a un sitio público tal cual si los datos son sensibles (Control de Pagos / Captación lo son).
