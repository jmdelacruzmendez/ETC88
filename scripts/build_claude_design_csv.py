#!/usr/bin/env python3
"""
Genera entrega_diseno/EQUIPO_CLAUDE_DESIGN.csv — lista plana del equipo para
pasarle a Claude Design al rehacer la guía.

Incluye los 48 operativos del retiro + 5 apoyos no-presenciales (Asesoras Cocina,
Asesores Comunidad) = 53 personas. Backups NO se incluyen (no van al retiro).

Columnas:
  Orden, Área, Rol, Nombre, Cumple, Teléfono, Comunidad, Sexo, Edad, Salud relevante.
"""
import json, csv, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
d = json.load(open(REPO / 'data/equipo.json', encoding='utf-8'))

AREA_ORDER = {
    'directores': 1, 'asesores': 2, 'asesores_espirituales': 3,
    'guias': 4, 'cocina': 5, 'musica': 6,
    'asesores_cocina': 7, 'asesores_diocesanos': 8,
}
AREA_LABEL = {
    'directores': 'Dirección',
    'asesores': 'Asesores',
    'asesores_espirituales': 'Asesores Espirituales',
    'guias': 'Guías',
    'cocina': 'Cocina',
    'musica': 'Música',
    'asesores_cocina': 'Asesoras Cocina',
    'asesores_diocesanos': 'Asesores Comunidad',
}
MESES = ['', 'ene', 'feb', 'mar', 'abr', 'may', 'jun',
         'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

def fmt_cumple(p):
    dd, mm = p.get('cumple_dia'), p.get('cumple_mes')
    if not dd or not mm:
        return ''
    return f'{int(dd):02d}-{MESES[int(mm)]}'

def fmt_tel(t):
    if not t:
        return ''
    s = ''.join(c for c in str(t) if c.isdigit())
    if len(s) == 11 and s.startswith('1'):
        s = s[1:]
    if len(s) == 10:
        return f'{s[:3]}-{s[3:6]}-{s[6:]}'
    return str(t)

def salud_resumen(p):
    bits = []
    a = (p.get('alergias') or '').strip()
    c = (p.get('condiciones') or '').strip()
    m = (p.get('medicamentos') or '').strip()
    if a and a.lower() not in ('ninguna', 'ninguno', 'n/a', 'na', '-', 'nada'):
        bits.append(f'Alergias: {a}')
    if c and c.lower() not in ('ninguna', 'ninguno', 'n/a', 'na', '-', 'nada'):
        bits.append(f'Condiciones: {c}')
    if m and m.lower() not in ('ninguno', 'ninguna', 'n/a', 'na', '-', 'nada'):
        bits.append(f'Medicamentos: {m}')
    return ' | '.join(bits)[:300]

filas = []
for p in d['equipo']:
    if p.get('backup'):
        continue
    area = p.get('area', '')
    filas.append({
        'orden': AREA_ORDER.get(area, 99),
        'area': AREA_LABEL.get(area, area),
        'rol': p.get('rol', ''),
        'nombre': p['nombre'].strip(),
        'cumple': fmt_cumple(p),
        'telefono': fmt_tel(p.get('telefono')),
        'comunidad': p.get('comunidad', ''),
        'sexo': p.get('sexo', ''),
        'edad': p.get('edad', ''),
        'salud': salud_resumen(p),
    })

filas.sort(key=lambda r: (r['orden'], r['nombre']))

out = REPO / 'entrega_diseno/EQUIPO_CLAUDE_DESIGN.csv'
with open(out, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['#', 'Área', 'Rol', 'Nombre', 'Cumple', 'Teléfono',
                'Comunidad', 'Sexo', 'Edad', 'Salud relevante'])
    for i, r in enumerate(filas, 1):
        w.writerow([i, r['area'], r['rol'], r['nombre'], r['cumple'],
                    r['telefono'], r['comunidad'], r['sexo'], r['edad'], r['salud']])

print(f'Wrote {out} · {len(filas)} personas (operativos + apoyos)')
