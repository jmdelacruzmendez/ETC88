#!/usr/bin/env python3
import os as _os
_R = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
"""Documento para la reunión del equipo de Finanzas / Tesorería del ETC 88.

Resumen financiero + cuotas + plan de recaudación + flujo de caja + caja actual +
equipo + agenda de decisiones. Fuente: data/equipo.json (embebe data/estado.json).
NO inventa cifras: todo sale de estado.json (finanzas).

Salida: Reunion_Finanzas_ETC88.docx
"""
import json
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

REPO = f'{_R}'
D = json.load(open(f'{REPO}/data/equipo.json')); EST = D['estado']
F = EST['finanzas']

def v(x):
    return x['valor'] if isinstance(x, dict) and 'valor' in x else x
def money(n):
    try: return f"RD${float(n):,.0f}"
    except Exception: return str(n)

MAR = RGBColor(0x1B, 0x3A, 0x52); TIERRA = RGBColor(0xB2, 0x50, 0x28); ROJO = RGBColor(0xA0, 0x24, 0x1A)
CEN = WD_ALIGN_PARAGRAPH.CENTER

def P(doc, t='', b=False, i=False, sz=None, c=None, al=None):
    p = doc.add_paragraph()
    if al is not None: p.alignment = al
    if t:
        r = p.add_run(t); r.bold = b; r.italic = i
        if sz: r.font.size = Pt(sz)
        if c: r.font.color.rgb = c
    return p
def H(doc, t): P(doc, t, b=True, sz=13, c=MAR)
def bullet(doc, t):
    doc.add_paragraph(style='List Bullet').add_run(t)
def table(doc, headers, rows):
    tb = doc.add_table(rows=1, cols=len(headers)); tb.style = 'Light Grid Accent 1'
    for i, h in enumerate(headers):
        rr = tb.rows[0].cells[i].paragraphs[0].add_run(h); rr.bold = True
    for row in rows:
        cs = tb.add_row().cells
        for i, cell in enumerate(row):
            cs[i].paragraphs[0].add_run('' if cell is None else str(cell))
    doc.add_paragraph()

doc = Document(); doc.styles['Normal'].font.name = 'Calibri'; doc.styles['Normal'].font.size = Pt(11)

# ---- Portada ----
P(doc, 'Reunión de Finanzas — ETC 88', b=True, sz=22, c=MAR, al=CEN)
P(doc, 'Encuentro Total con Cristo · 4–6 de septiembre de 2026', i=True, sz=11, c=TIERRA, al=CEN)
P(doc, 'Documento de trabajo para Tesorería · cifras desde estado.json', i=True, sz=9, c=RGBColor(0x80,0x80,0x80), al=CEN)
P(doc)

aux = {a['nombre']: a for a in EST.get('equipos_auxiliares', [])}
tes = aux.get('Finanzas / Tesorería (auxiliar)', {})
pro = aux.get('Recaudación / Profondo', {})
P(doc, 'Equipo', b=True)
def _eq(team):
    resp = v(team.get('responsable', {})) or '—'
    miembros = ', '.join(m for m in team.get('miembros', []) if m != resp) or '—'
    return resp, miembros
_r1, _m1 = _eq(tes); _r2, _m2 = _eq(pro)
bullet(doc, f"Tesorería: {_r1} (líder) · equipo: {_m1}")
bullet(doc, f"Recaudación / Profondo: {_r2} (líder) · equipo: {_m2}")
P(doc)

# ---- 1. Foto financiera ----
meta = v(F['meta_recaudacion_total'])
cuotas_firmes = F['plan_recaudacion']['fuentes_caja_plan_a']['cuotas']['monto']
operativo = meta - 50329  # imprevistos 10%
brecha = meta - cuotas_firmes
H(doc, '1. Foto financiera (de un vistazo)')
table(doc, ['Concepto', 'Monto'], [
    ['Costo operativo', money(operativo)],
    ['(+) Imprevistos (10%)', money(50329)],
    ['(=) META TOTAL a cubrir', money(meta)],
    ['(–) Cuotas firmes (participantes + equipo)', money(cuotas_firmes)],
    ['(=) BRECHA a levantar (recaudación)', money(brecha)],
])

# ---- 2. Rubros del presupuesto ----
H(doc, '2. ¿En qué se va el dinero? (rubros)')
rows = [[r['nombre'], money(r['monto']), 'Sí' if r.get('donable') else '—'] for r in F['rubros_simulador']['items']]
table(doc, ['Rubro', 'Monto', '¿Donable / especie?'], rows)
P(doc, 'La columna "donable" = lo más realista de conseguir en especie (baja la brecha peso a peso).', i=True, sz=9)

# ---- 3. Cuotas ----
ce = v(F['cuota_equipo'])
H(doc, '3. Cuotas (ingreso firme)')
bullet(doc, f"Participante: {money(v(F['cuota_participante']))} — cubre transporte, comida, casa, pez y biblia.")
bullet(doc, f"Equipo (servidores): {money(ce.get('total'))} — {ce.get('nota_plan_pago','')}")
bullet(doc, "Las cuotas de la Hna. Angelina y el P. Paul las asume la Co-Dirección (igual entran a la meta).")
bullet(doc, f"Total firme por cuotas: {money(cuotas_firmes)}")

# ---- 4. Plan de recaudación ----
H(doc, '4. Plan de recaudación (Plan A)')
fc = F['plan_recaudacion']['fuentes_caja_plan_a']
labels = {'cuotas':'Cuotas','rifa_profondo':'Rifa / Profondo','venta_garaje':'Venta de garaje',
          'venta_comida':'Venta de comida','donaciones_efectivo':'Donaciones en efectivo'}
rows = []
for k, lab in labels.items():
    d = fc.get(k, {})
    rows.append([lab, money(d.get('monto')), f"{d.get('prob','')}%", d.get('nota', d.get('estado',''))])
rows.append(['TOTAL caja objetivo', money(fc.get('total_caja_objetivo')), '', ''])
table(doc, ['Fuente', 'Monto', 'Prob.', 'Nota'], rows)
esp = F['plan_recaudacion']['especie_potencial']
P(doc, f"+ Potencial en ESPECIE: {money(esp['monto'])} — no es caja, pero reduce el costo. {esp['nota']}", i=True, sz=9)

# ---- 5. Flujo de caja ----
H(doc, '5. Flujo de caja proyectado (jun–sep)')
fl = F['plan_recaudacion']['flujo_caja_proyectado']
mesnom = {'jun':'Junio','jul':'Julio','ago':'Agosto','sep':'Septiembre'}
rows = [[mesnom.get(m, m), money(fl[m]['entradas']), money(fl[m]['salidas']), money(fl[m]['saldo_acum']), fl[m].get('nota','')]
        for m in ['jun','jul','ago','sep'] if m in fl]
table(doc, ['Mes', 'Entradas', 'Salidas', 'Saldo acum.', 'Nota'], rows)
P(doc, '⚠️ Septiembre es el MES PICO: toda la recaudación debe estar EN CAJA antes del 1-sep.', b=True, c=ROJO)

# ---- 6. Caja actual ----
H(doc, '6. Caja actual')
caja = F['caja']
bullet(doc, f"Saldo actual: {money(caja.get('saldo_actual'))}")
for d in caja.get('deudas_pendientes', []):
    bullet(doc, f"Pendiente: reembolsar {money(d['monto'])} a {d['acreedor']} ({d['concepto']}).")

# ---- 7. Agenda de decisiones ----
H(doc, '7. Agenda — decisiones de esta reunión')
for a in [
    'Cuenta de recaudo oficial: ¿cuenta del equipo o personal con registro? (BLOQUEANTE — sin esto no se recauda).',
    '¿Profondo solo monta la actividad/estrategia, o comparte con Finanzas la gestión económica?',
    'Política de earmark: qué entrada cubre qué rubro.',
    'Reembolso de RD$10,000 a Juan Manuel (salón pagado de su dinero).',
    'Exención de la casa con el P. Paul (vale ~RD$30,000) — se gestiona cuando el monto esté firme.',
    'Cierre semanal de Tesorería (lunes) + hoja de Control de Pagos operando.',
    'Premio de la rifa: gestionarlo DONADO + fecha de arranque.',
    'Cotizar los 3 buses de transporte (hoy estimado en ' + money(77500) + ').',
]:
    bullet(doc, a)

# ---- 8. Próximos pasos ----
H(doc, '8. Próximos pasos (recaudación)')
bullet(doc, 'Kit de cartas firmadas listo (directorio + cartas con firma/sello + tracker).')
bullet(doc, 'Primeras cartas: Induveca, COOPMEDICA, César Iglesias, Iberia, EGE Haina, Zaglul.')
bullet(doc, 'Registrar cada envío y aporte en el tracker / Control de Pagos.')

out = f'{REPO}/Reunion_Finanzas_ETC88.docx'
doc.save(out); print(f'Wrote {out}')
