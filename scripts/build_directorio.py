#!/usr/bin/env python3
"""Genera el DIRECTORIO del equipo (lista de nombres por área, con cumpleaños) desde
data/equipo.json. Fuente única: equipo.json. Salida compartible para la Carpeta /
Claude Design. NO se edita a mano la lista; se corrige el roster y se regenera (regla #2).
No incluye cantera/backups (solo titulares del equipo)."""
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
    'asesores_diocesanos': 'Asesores de comunidad',
}
MES = {1: 'ene', 2: 'feb', 3: 'mar', 4: 'abr', 5: 'may', 6: 'jun',
       7: 'jul', 8: 'ago', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dic'}


def comunidad_from_rol(rol):
    if 'La Vega' in rol:
        return 'La Vega'
    if 'SD' in rol or 'Santo Domingo' in rol:
        return 'Santo Domingo'
    if 'SPM' in rol:
        return 'San Pedro de Macorís'
    return None


def cumple(p):
    d, m = p.get('cumple_dia'), p.get('cumple_mes')
    if d and m and m in MES:
        return f' · cumple {d} {MES[m]}'
    return ''


by = defaultdict(list)
for p in team:
    by[p['area']].append(p)

lines = []
lines.append('# Directorio del equipo — ETC 88')
lines.append('### Lista de servidores por área (con cumpleaños) · generada desde data/equipo.json (fuente única)')
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
        elif a == 'asesores_diocesanos':
            com = comunidad_from_rol(p['rol'])
            tag = f' — {com}' if com else ''
        else:
            tag = ''
        lines.append(f'- {p["nombre"]}{tag}{cumple(p)}')
    lines.append('')

lines.append('---')
lines.append(f'*{total_tit} servidores del equipo. Directorio generado del roster — '
             'los datos de contacto viven en `Equipo_ETC88.xlsx`.*')

out_md = f'{REPO}/entrega_diseno/DIRECTORIO_EQUIPO_88.md'
os.makedirs(os.path.dirname(out_md), exist_ok=True)
with open(out_md, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print(f'Wrote {out_md} · {total_tit} titulares (sin cantera)')
