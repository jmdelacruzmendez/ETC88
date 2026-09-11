#!/usr/bin/env bash
# B4 · Bus factor: regenera TODO el sistema ETC 88 y corre la compuerta.
# Para CUALQUIER asesor — un solo comando. Si algo falla, se detiene (set -e).
# Uso:  bash scripts/run_all.sh
set -e
cd "$(dirname "$0")/.."
echo "== ETC 88 · regenerando sistema =="
python scripts/build_data.py
python scripts/build_directorio.py
python scripts/build_docx.py
python scripts/build_finanzas.py
python scripts/build_flujo.py
python scripts/build_excel.py
python scripts/build_guia.py
python scripts/build_html.py
python scripts/build_trazabilidad.py
python scripts/build_cantera.py
python scripts/build_captacion.py
python scripts/build_web.py
python scripts/build_drive.py
python scripts/build_trabajo.py
python scripts/build_entrega_diseno.py
python scripts/build_doc_trabajo_88.py
python scripts/build_carpeta_docx.py
# Cierre económico post-retiro (conciliación final)
python scripts/build_conciliacion.py
python scripts/build_conciliacion_docx.py
python scripts/build_conciliacion_pptx.py
python scripts/build_prompt_conciliacion.py
echo "== Compuerta de verificación =="
python scripts/verify.py
echo "== Listo. Si dice TODO PASS, el sistema está coherente. =="
