#!/usr/bin/env python3
"""B2 · Tracker de captación de participantes.
Lee data/participantes.json (semilla) → escribe /tmp/drive_captacion.csv para subir
como Google Sheet EDITABLE por el equipo (cada misionero actualiza el estado).
DATOS SENSIBLES: no va a la carpeta pública; es para el seguimiento interno.
"""
import json, csv, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(f'{REPO}/data/participantes.json', encoding='utf-8'))
pros = data['prospectos']
meta = data.get('meta_participantes', 52)
out = '/tmp/drive_captacion.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['#', 'Participante', 'Edad', 'Invita (misionero)', 'Relación',
                'Fuente', 'Estado', 'Perfil recibido', 'Notas'])
    for i, p in enumerate(pros, 1):
        w.writerow([i, p['nombre'], p.get('edad') or '', p.get('invita') or '',
                    p.get('relacion') or '', p.get('fuente') or '',
                    p.get('estado') or 'propuesto',
                    'Sí' if p.get('perfil') else 'No', p.get('notas') or ''])
    con = sum(1 for p in pros if p.get('invita'))
    sin = len(pros) - con
    w.writerow([])
    w.writerow(['', f'TOTAL prospectos: {len(pros)}', '',
                f'con misionero: {con}', f'sin misionero: {sin}', '',
                f'meta: {meta}', f'faltan captar: {meta - len(pros)}', ''])
print(f"Wrote {out} · {len(pros)} prospectos · {con} con misionero · meta {meta} · faltan {meta-len(pros)}")
