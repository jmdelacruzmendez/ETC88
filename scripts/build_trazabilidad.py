#!/usr/bin/env python3
"""Registro de TRAZABILIDAD del ETC 88 — se genera desde data/estado.json + data/equipo.json.

Lista todo hecho con su ESTADO (confirmado/propuesta/pendiente) y su FUENTE, para tener
trazabilidad de contenido y de fuentes. Como TODOS los entregables se generan desde estas
dos fuentes y verify.py bloquea cualquier desvío, el contenido es trazable por construcción.

Salida: preparacion/TRAZABILIDAD.md
"""
import json
from collections import Counter

REPO = '/home/user/ETC88'
EST = json.load(open(f'{REPO}/data/estado.json'))
EQ = json.load(open(f'{REPO}/data/equipo.json'))

# --- recorrer estado.json y juntar todo nodo con 'estado' ---
facts = []  # (ruta, valor, estado, fuente, nota)
def walk(node, path):
    if isinstance(node, dict):
        if 'estado' in node and ('valor' in node or 'estado_equipo' in node):
            val = node.get('valor', node.get('nombre', ''))
            if isinstance(val, (dict, list)):
                val = json.dumps(val, ensure_ascii=False)
            facts.append((path, val, node.get('estado', node.get('estado_equipo', '')),
                          node.get('fuente', '—'), node.get('nota', '')))
            return
        for k, v in node.items():
            if k.startswith('_'):
                continue
            walk(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]")

walk(EST, '')

by_estado = {'confirmado': [], 'propuesta': [], 'pendiente': []}
for f in facts:
    by_estado.setdefault(f[2], []).append(f)

L = []
A = L.append
A('# TRAZABILIDAD ETC 88 — registro de hechos, fuentes y estados')
A('')
A('> Generado desde `data/estado.json` + `data/equipo.json`. Todos los entregables se generan')
A('> de estas dos fuentes; `verify.py` bloquea cualquier desvío. Trazabilidad por construcción.')
A('')
cnt = Counter(f[2] for f in facts)
A(f'**Resumen:** {cnt.get("confirmado",0)} confirmados · {cnt.get("propuesta",0)} propuestas · '
  f'{cnt.get("pendiente",0)} pendientes (en estado.json).')
A('')

# --- Roster (trazabilidad de conteos) ---
eq = EQ['equipo']
op = [p for p in eq if p.get('operativo') and not p.get('vacante') and not p.get('backup')]
A('## Roster (data/equipo.json · generado del formulario)')
A(f'- Total {len(eq)} · operativos titulares {len(op)} · '
  f'vacantes {sum(1 for p in eq if p.get("vacante"))} · backups {sum(1 for p in eq if p.get("backup"))}.')
areas = Counter(p['area'] for p in op)
A('- Por área (operativos): ' + ' · '.join(f'{a} {n}' for a, n in sorted(areas.items())))
A('')

def tabla(rows):
    A('| Campo | Valor | Fuente | Nota |')
    A('|---|---|---|---|')
    for ruta, val, est, fue, nota in rows:
        v = str(val); v = v[:60] + '…' if len(v) > 60 else v
        n = (nota or '')[:70] + ('…' if len(nota or '') > 70 else '')
        A(f'| `{ruta}` | {v} | {fue} | {n} |')
    A('')

A('## ✅ Confirmados (se pueden mostrar como hecho)')
tabla(by_estado['confirmado'])
A('## 🟡 Propuestas (sin cerrar — se muestran [PROPUESTA]; OJO con la fuente)')
tabla(by_estado['propuesta'])
A('## 🔴 Pendientes (faltan — se muestran [POR DEFINIR])')
tabla(by_estado['pendiente'])

A('## Decisiones confirmadas (lista del director)')
for d in EST.get('decisiones_confirmadas', []):
    A(f'- {d}')
A('')
A('## Pendientes y decisiones por cerrar (lista del director)')
for d in EST.get('pendientes', []):
    A(f'- [ ] {d}')
A('')

open(f'{REPO}/preparacion/TRAZABILIDAD.md', 'w', encoding='utf-8').write('\n'.join(L))
print(f"Wrote preparacion/TRAZABILIDAD.md · {len(facts)} hechos "
      f"({cnt.get('confirmado',0)} conf · {cnt.get('propuesta',0)} prop · {cnt.get('pendiente',0)} pend)")
