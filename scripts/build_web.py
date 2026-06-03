#!/usr/bin/env python3
"""Genera los CSV que alimentan el tablero vivo (web/tablero.html).
Fuentes: data/equipo.json · control_pagos.json · participantes.json · pendientes.json.
Los CSV en web/ hacen que el tablero funcione de inmediato (local / GitHub Pages).
Si el equipo publica las hojas de Google como CSV, el tablero puede leer EN VIVO
(ver el bloque CONFIG en web/tablero.html).
"""
import json, csv, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = f'{REPO}/web'
os.makedirs(WEB, exist_ok=True)

def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        c = csv.writer(f); c.writerow(header)
        for r in rows:
            c.writerow(r)

# 1 · Equipo (roster)
eq = json.load(open(f'{REPO}/data/equipo.json'))['equipo']
write_csv(f'{WEB}/equipo.csv',
          ['Nombre', 'Área', 'Rol', 'Edad', 'Comunidad', 'Operativo', 'SinFormulario'],
          [[p['nombre'], p['area'], p['rol'], p.get('edad') or '', p.get('comunidad') or '',
            'Sí' if p.get('operativo') else 'No', 'Sí' if p.get('sin_formulario') else 'No'] for p in eq])

# 2 · Control de pagos
cp = json.load(open(f'{REPO}/data/control_pagos.json'))
rows = []
for sec, label in (('ingresos', 'INGRESO'), ('egresos', 'EGRESO')):
    for it in cp.get(sec, []):
        rows.append([it['concepto'], label, it.get('estimado', ''), '', '', '', it.get('nota', '')])
write_csv(f'{WEB}/control_pagos.csv',
          ['Concepto', 'Tipo', 'Estimado', 'Comprometido', 'Movido', 'Saldo', 'Notas'], rows)

# 3 · Captación
pr = json.load(open(f'{REPO}/data/participantes.json'))['prospectos']
write_csv(f'{WEB}/captacion.csv',
          ['Participante', 'Edad', 'Invita', 'Relación', 'Estado', 'Perfil'],
          [[p['nombre'], p.get('edad') or '', p.get('invita') or '', p.get('relacion') or '',
            p.get('estado') or '', 'Sí' if p.get('perfil') else 'No'] for p in pr])

# 4 · Pendientes
pe = json.load(open(f'{REPO}/data/pendientes.json'))['pendientes']
write_csv(f'{WEB}/pendientes.csv',
          ['Horizonte', 'Tarea', 'Dueño', 'Estado'],
          [[x['horizonte'], x['tarea'], x.get('dueño', ''), x.get('estado', 'abierto')] for x in pe])

print(f"Wrote web/ CSVs · equipo {len(eq)} · pagos {len(rows)} · captación {len(pr)} · pendientes {len(pe)}")
