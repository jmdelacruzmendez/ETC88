# ETC 88 — Reglas del proyecto (LÉEME ANTES DE TOCAR NADA)

Sistema de gestión y documentación del **Encuentro Total con Cristo #88**
(4–6 sep 2026, Higüey). Dirección: Juan Manuel de la Cruz · Jean Carlo de la Cruz.

Este archivo existe porque en el pasado se **inventaron datos y decisiones**, se
**generaron documentos que contradecían el roster** y se subió a Drive **markdown
escapado**. Las reglas de abajo evitan que vuelva a pasar.

## Fuente única de verdad (datos, no prosa)
- **`data/equipo.json`** — el ROSTER (personas, áreas, roles, salud). Se genera con
  `scripts/build_data.py` desde el formulario (`data/fuente_formulario.xlsx`) + `estado.json`.
- **`data/estado.json`** — TODO lo demás (finanzas, calendario, decisiones, metas,
  temática, equipos auxiliares). Cada hecho lleva `estado`:
  - `confirmado` → lo dijo el director. Se puede mostrar como hecho.
  - `propuesta` → sugerencia sin decidir. Se renderiza con **`[PROPUESTA]`**.
  - `pendiente` → falta el dato. Se renderiza con **`[POR DEFINIR]`**.

## Las 5 reglas (obligatorias)
1. **No inventar.** Nunca escribas un nombre, cifra, fecha o decisión en un documento
   compartible salvo que esté en `equipo.json`/`estado.json` como `confirmado`. Si no
   lo está, renderízalo como `[PROPUESTA]` o `[POR DEFINIR]` — **jamás como hecho**.
2. **Todo lo compartible se genera.** No se editan a mano los documentos de salida; se
   cambian los DATOS y se regenera. (La prosa pastoral autorizada vive en los `.md`
   fuente, pero cualquier nombre/cifra dentro de ella debe cuadrar con los datos.)
3. **Verifica antes de entregar.** Corre `python scripts/verify.py` y muéstrale el
   PASS al director **antes** de subir o entregar cualquier cosa.
4. **Sub-agentes con fuente obligatoria.** A cualquier sub-agente se le pasa
   `equipo.json` como única fuente del roster; prohibido inferir personas de prosa
   vieja. Su salida se valida con `verify.py` (los agentes también alucinan).
5. **Drive = `.docx` generado, nunca `text/plain`.** Subir markdown como `text/plain`
   hace que Google escape los símbolos (`\-`, `\[`, `\#`) y rompa los emoji. Los
   entregables de Drive se generan con `scripts/build_docx.py` (python-docx).

## Pipeline (regenerar SIEMPRE en este orden)
```
python scripts/build_data.py       # lee xlsx + estado.json → data/equipo.json + /tmp
python scripts/build_docx.py       # → Documento_Asesores_ETC88.docx + Carpeta_F1_ETC88.docx
python scripts/build_finanzas.py   # → Finanzas_ETC88.xlsx (+ /tmp/etc88_costos.json)
python scripts/build_flujo.py      # → Flujo_Caja_ETC88.xlsx (modelo: topes, flujo, optimización)
python scripts/build_excel.py      # → Equipo_ETC88.xlsx
python scripts/build_guia.py       # → GUIA_ETC88.md (fuente de la Carpeta)
python scripts/build_html.py       # → index.html (Tablero)
python scripts/build_trazabilidad.py # → preparacion/TRAZABILIDAD.md (registro de fuentes)
python scripts/build_cantera.py     # → Cantera_ETC88.xlsx (maqueta: padrinos + auxiliares)
python scripts/build_captacion.py   # → /tmp/drive_captacion.csv (tracker de participantes, desde data/participantes.json)
python scripts/build_drive.py      # → /tmp/drive_*.txt|.csv (versiones LIMPIAS para Drive)
python scripts/verify.py           # COMPUERTA — debe imprimir TODO PASS
```

**Atajo (bus factor #B4):** `bash scripts/run_all.sh` corre TODO el pipeline + `verify.py` de una sola vez. Cualquier asesor con **Python 3** (`pip install openpyxl python-docx`) + **Node** puede operarlo desde la raíz del repo. Debe terminar en **TODO PASS**; si imprime FALLOS, se corrige el **DATO** (en `data/estado.json` o `data/equipo.json`) — nunca el documento de salida — y se vuelve a correr.

Para Drive: subir `/tmp/drive_asesores.txt` y `/tmp/drive_carpeta.txt` como `text/plain`
(→ Google Doc limpio) y `/tmp/drive_equipo.csv` + `/tmp/drive_finanzas.csv` como `text/csv`
(→ Google Sheet). build_drive.py ya evita lo que Google escapa (#, [], *, `N.` al inicio).

## Entregables OFICIALES (lo único que va a Drive, consolidado)
- **2 documentos** (`.docx`): `Documento_Asesores_ETC88.docx`, `Carpeta_F1_ETC88.docx`.
- **2 hojas** (`.xlsx`/Google Sheet): `Equipo_ETC88.xlsx`, `Finanzas_ETC88.xlsx`.
- Carpeta de Drive: **"ETC 88 · ENTREGABLES (oficial)"**.

Todo lo demás (`preparacion/`) es **DOCUMENTO DE TRABAJO**, no entregable.

## Las 5 reglas (continuación) — Regla #6
6. **Nunca inferir rol desde formulario.** Una respuesta de formulario (p. ej. col 18 "¿qué
   actividad propondrías?") captura *ideas*, no voluntarios para liderar. Nunca escribir
   "X lidera / es responsable / encargado de Y" a partir de una propuesta de formulario o
   una sugerencia de idea. Solo el director confirma roles operativos; sin confirmación,
   siempre `[POR DEFINIR]` + nota "(Co-Dir decide)".

## Decisiones que son del director (NO inventar — quedan `propuesta`/`pendiente`)
Lema del retiro · hilo espiritual · reglas estéticas/branding (van a Claude Design) ·
monto final de la cuota del equipo · número final de participantes · varón de cocina ·
1 o 2 representantes de La Vega · responsables de los equipos auxiliares.
