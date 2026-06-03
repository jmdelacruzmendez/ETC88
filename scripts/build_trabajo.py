#!/usr/bin/env python3
"""Convierte los documentos MAESTROS de trabajo (.md) a texto LIMPIO para Drive,
sin markdown crudo (sin #, |, ** ni tablas pipe) — igual que build_drive.py hace
con los 4 entregables, pero para los masters de trabajo.
Salida: /tmp/trabajo_*.txt  (se suben como Google Doc limpio a 'ETC 88 · TRABAJO').
"""
import re, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTERS = {
    'plan_formacion':   'preparacion/PLAN_FORMACION.md',
    'plan_economico':   'preparacion/PLAN_ECONOMICO.md',
    'plan_recaudacion': 'preparacion/PLAN_RECAUDACION.md',
    'seguimiento':      'preparacion/SEGUIMIENTO_ETC88.md',
    'roadmap':          'preparacion/ROADMAP_SISTEMA.md',
    'reunion_coords':   'preparacion/REUNION_COORDS_4JUN.md',
}

def md_to_text(md):
    out = []
    for line in md.split('\n'):
        s = line.rstrip()
        if re.match(r'^\s*\|[\s:|+-]+\|\s*$', s):          # separador de tabla |---|
            continue
        if s.lstrip().startswith('|'):                      # fila de tabla -> " · "
            cells = [c.strip() for c in s.strip().strip('|').split('|')]
            s = '   ' + '  ·  '.join(c for c in cells if c)
        m = re.match(r'^(#{1,6})\s+(.*)', s)                # encabezados
        if m:
            s = '\n' + (m.group(2).upper() if len(m.group(1)) <= 2 else m.group(2))
        s = re.sub(r'^\s*>\s?', '', s)                      # blockquote
        s = re.sub(r'^(\s*)[-*]\s+', r'\1•  ', s)            # viñetas
        s = s.replace('**', '').replace('`', '')             # bold / code
        s = re.sub(r'\*([^*\n]+)\*', r'\1', s)               # italic *...* -> ...
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', s)  # links [t](u) -> t (u)
        out.append(s)
    txt = re.sub(r'\n{3,}', '\n\n', '\n'.join(out))
    return txt.strip() + '\n'

if __name__ == '__main__':
    for name, path in MASTERS.items():
        md = open(f'{REPO}/{path}', encoding='utf-8').read()
        open(f'/tmp/trabajo_{name}.txt', 'w', encoding='utf-8').write(md_to_text(md))
        print(f"Wrote /tmp/trabajo_{name}.txt ({path})")
