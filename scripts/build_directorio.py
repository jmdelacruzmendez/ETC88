#!/usr/bin/env python3
"""Genera el DIRECTORIO del equipo (lista de nombres por área) desde data/equipo.json.
Fuente única: equipo.json. Salida compartible para la Carpeta / Claude Design.
NO se edita a mano la lista; se corrige el roster y se regenera (regla #2)."""
import json, os
from collections import defaultdict

REPO = '/home/user/ETC88'
e = json.load(open(f'{REPO}/data/equipo.json', encoding='utf-8'))
team = e['equipo'] if isinstance(e, dict) and 'equipo' in e else e

ORDER = ['directores', 'asesores', 'asesores_espirituales', 'guias', 'cocina',
         'musica', 'asesores_cocina', 'asesores_diocesanos']
LABELS = {
    'directores': 'Dirección', 'asesores': 'Asesores',
    'asesores_espirituales': 'Asesores espirituales', 'guias': 'Guías',
    'cocina': 'Cocina', 'musica': 'Música',
    'asesores_cocina': 'Asesoras de cocina',
    'asesores_diocesanos': 'Asesores diocesanos · comunidad',
}
by = defaultdict(list)
for p in team:
    by[p['area']].append(p)

lines = []
lines.append('# Directorio del equipo — ETC 88')
lines.append('### Lista de servidores por área · generada desde data/equipo.json (fuente única)')
lines.append('')
lines.append('> No editar a mano. Si un nombre cambia, se corrige el roster y se regenera con `python scripts/build_directorio.py`.')
lines.append('')

total_tit = 0
for a in ORDER:
    ppl = [p for p in by.get(a, []) if not p.get('backup') and not p.get('vacante')]
    if not ppl:
        continue
    ppl.sort(key=lambda p: (0 if (p['rol'] == 'Director' or 'Coord' in p['rol']) else 1, p['nombre']))
    total_tit += len(ppl)
    lines.append(f'## {LABELS.get(a, a)} ({len(ppl)})')
    for p in ppl:
        if p['rol'] == 'Director':
            tag = ' — Director'
        elif 'Coord' in p['rol']:
            tag = ' — Coordinador/a'
        elif p.get('transversal'):
            tag = ' — (acompaña todo el proceso)'
        else:
            tag = ''
        lines.append(f'- {p["nombre"]}{tag}')
    lines.append('')

backs = [p for p in team if p.get('backup')]
if backs:
    bg = [p['nombre'] for p in backs if 'Guía' in p['rol']]
    bc = [p['nombre'] for p in backs if 'Cocina' in p['rol']]
    lines.append(f'## Cantera · backups ({len(backs)})')
    lines.append('> Cantera del equipo; se activan según necesidad. No son titulares operativos.')
    if bg:
        lines.append(f'- **Guías ({len(bg)}):** ' + ' · '.join(sorted(bg)))
    if bc:
        lines.append(f'- **Cocina ({len(bc)}):** ' + ' · '.join(sorted(bc)))
    lines.append('')

lines.append('---')
lines.append(f'*Titulares: {total_tit} · Cantera: {len(backs)} · Total: {total_tit + len(backs)}. '
             'Directorio generado del roster — los datos de contacto viven en `Equipo_ETC88.xlsx`.*')

out_md = f'{REPO}/entrega_diseno/DIRECTORIO_EQUIPO_88.md'
os.makedirs(os.path.dirname(out_md), exist_ok=True)
with open(out_md, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print(f'Wrote {out_md} · titulares {total_tit} · cantera {len(backs)} · total {total_tit + len(backs)}')
