#!/usr/bin/env python3
"""Genera el PAQUETE para Claude Design en .txt LIMPIO (sin markdown crudo).
Reusa el conversor de build_trabajo.py. Salida: entrega_diseno/*.txt
  - INSTRUCCION_CLAUDE_DESIGN.txt  (el prompt para pegar)
  - CARPETA_ETC88.txt              (cuerpo de la Carpeta del retiro)
  - ANEXO_1_GUIA_DE_GUIAS.txt      (anexo 1)
  - ANEXO_2_COCINA.txt             (anexo 2)
Para adjuntar/pegar en la sesión de Claude Design (Dirección A ya cargada).
"""
import os
from build_trabajo import md_to_text

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'entrega_diseno')
os.makedirs(OUT, exist_ok=True)

PAQUETE = {
    'INSTRUCCION_CLAUDE_DESIGN.txt': 'preparacion/PROMPT_DISENO_CARPETA_88.md',
    'CARPETA_ETC88.txt':             'preparacion/COPY_GUIA_ETC88.md',
    'ANEXO_1_GUIA_DE_GUIAS.txt':     'GUIA_DE_GUIAS_88.md',
    'ANEXO_2_COCINA.txt':            'ANEXO_COCINA_88.md',
    'ANEXO_3_MUSICA.txt':            'ANEXO_MUSICA_88.md',
}

for out_name, src in PAQUETE.items():
    md = open(f'{REPO}/{src}', encoding='utf-8').read()
    open(f'{OUT}/{out_name}', 'w', encoding='utf-8').write(md_to_text(md))
    print(f"Wrote entrega_diseno/{out_name}  <-  {src}")
