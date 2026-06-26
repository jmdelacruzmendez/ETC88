#!/usr/bin/env python3
import os as _os
_R = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
"""Genera el DIRECTORIO del equipo (lista de nombres por área, con cumpleaños) desde
data/equipo.json. Fuente única: equipo.json. Salida compartible para la Carpeta /
Claude Design. NO se edita a mano la lista; se corrige el roster y se regenera (regla #2).
No incluye cantera/backups (solo titulares del equipo)."""
import json, os
from collections import defaultdict

REPO = f'{_R}'
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


def cumple_str(p):
    d, m = p.get('cumple_dia'), p.get('cumple_mes')
    if d and m and m in MES:
        return f'{d} {MES[m]}'
    return '—'


def telefono_str(p):
    """Formatea teléfono dominicano. Acepta:
    - 10 dígitos con código de área DR (809/829/849).
    - 11 dígitos comenzando con '1' (código país) + área DR.
    Cualquier otro caso se devuelve sin formatear (mantiene el dato crudo)
    para no inventar números — el responsable corrige en el formulario."""
    t = p.get('telefono')
    if not t:
        return '—'
    s = ''.join(c for c in str(t) if c.isdigit())
    if len(s) == 11 and s.startswith('1'):
        s = s[1:]
    if len(s) == 10 and s[0:3] in ('809', '829', '849'):
        return f'({s[0:3]}) {s[3:6]}-{s[6:10]}'
    return s or '—'


def rol_tag(p, area):
    if p['rol'] == 'Director':
        return 'Director'
    if 'Coord' in p['rol']:
        return 'Coordinador/a'
    if p.get('transversal'):
        return 'Acompaña todo el proceso'
    if area == 'guias':
        return 'Guía'
    if area == 'cocina':
        return 'Cocina'
    if area == 'musica':
        return 'Música'
    if area == 'asesores':
        return p['rol'] if p['rol'] else 'Asesor/a'
    if area == 'asesores_espirituales':
        return 'Asesor/a Espiritual'
    if area == 'asesores_cocina':
        return 'Asesora de Cocina'
    return p['rol'] or ''


by = defaultdict(list)
for p in team:
    by[p['area']].append(p)

lines = []
lines.append('# Directorio del equipo — ETC 88')
lines.append('### Lista de servidores por área · 53 servidores · generada desde data/equipo.json (fuente única)')
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

    # ENMASCARAR asesores de comunidad: solo "Santo Domingo (2)" / "La Vega (1)" — sin nombres.
    if a == 'asesores_diocesanos':
        sd = sum(1 for p in ppl if comunidad_from_rol(p['rol']) == 'Santo Domingo')
        lv = sum(1 for p in ppl if comunidad_from_rol(p['rol']) == 'La Vega')
        lines.append(f'## {LABELS.get(a, a)} ({len(ppl)})')
        lines.append('')
        if sd:
            lines.append(f'- **Santo Domingo** — {sd} asesor{"es" if sd != 1 else ""} de comunidad')
        if lv:
            lines.append(f'- **La Vega** — {lv} asesor{"es" if lv != 1 else ""} de comunidad')
        lines.append('')
        continue

    lines.append(f'## {LABELS.get(a, a)} ({len(ppl)})')
    lines.append('')
    lines.append('| Nombre | Rol | Cumpleaños | Teléfono |')
    lines.append('|---|---|---|---|')
    for p in ppl:
        nombre = p['nombre']
        rol = rol_tag(p, a)
        c = cumple_str(p)
        t = telefono_str(p)
        lines.append(f'| {nombre} | {rol} | {c} | {t} |')
    lines.append('')

lines.append('---')
lines.append(f'*{total_tit} servidores del equipo (sin cantera ni backups). Asesores de comunidad se muestran sin nombres — solo la comunidad que representan (decisión 5-jun: la comunidad reconoce a sus propios asesores).*')

out_md = f'{REPO}/entrega_diseno/DIRECTORIO_EQUIPO_88.md'
os.makedirs(os.path.dirname(out_md), exist_ok=True)
with open(out_md, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print(f'Wrote {out_md} · {total_tit} titulares (sin cantera)')
