#!/usr/bin/env python3
"""Genera Tripulacion_ETC88.xlsx — el EXCEL INTERNO de Tesorería del ETC 88.

Mismo sistema de costos que el HTML, pero en hoja editable + el CONTROL DE PAGOS
por nombre (que NO va en el HTML público). Hojas:
  1. Costo por persona  — desglose participante y equipo (operativo + 10%).
  2. Cuotas             — qué se recauda y qué cubre cada cuota.
  3. Simulador          — marca '¿conseguido? S' por rubro y ve bajar la falta (fórmula).
  4. Control de pagos   — INTERNO: 53 del equipo × 4 cuotas (jun-sep) + saldo.

Cifras desde data/estado.json; roster desde data/equipo.json.
Uso: python scripts/build_tripulacion_xlsx.py
"""
import json
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EST = json.load(open(os.path.join(REPO, 'data', 'estado.json'), encoding='utf-8'))
EQ = json.load(open(os.path.join(REPO, 'data', 'equipo.json'), encoding='utf-8'))['equipo']

fin = EST['finanzas']
cpp = fin['costos_por_persona']
desg_blk = fin['meta_recaudacion_total']['desglose']
sim = fin['rubros_simulador']['items']
exentos = set(fin['cuota_equipo_exentos']['asumidos_por_codireccion'])
meta = fin['meta_recaudacion_total']['valor']
cuotas = desg_blk['cuotas_firmes']
cuota_part = fin['cuota_participante']['valor']
n_part = fin['participantes_objetivo']['valor']
part_cuota_total = cuota_part * n_part
equipo_cuotas = cuotas - part_cuota_total
eq_total = fin['cuota_equipo']['valor']['total']
eq_pago = fin['cuota_equipo']['valor']['mensual']

# estilos
NAVY = '0B2A52'; HEAD = PatternFill('solid', fgColor=NAVY)
ALT = PatternFill('solid', fgColor='EEF3FA'); GOLD = PatternFill('solid', fgColor='FCEFCB')
WHITE = Font(color='FFFFFF', bold=True); BOLD = Font(bold=True)
THIN = Side(style='thin', color='C9D6E5'); BORD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CEN = Alignment(horizontal='center', vertical='center')
MON = '#,##0'; MON2 = '#,##0.00'

wb = openpyxl.Workbook()

def head(ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.fill = HEAD; cell.font = WHITE; cell.alignment = CEN; cell.border = BORD
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

# ---------------------------------------------------- 1. Costo por persona ---
ws = wb.active; ws.title = '1 Costo por persona'
ws['A1'] = 'ETC · Misión 88 — Lo que cuesta la misión por persona'; ws['A1'].font = Font(bold=True, size=14)
ws['A2'] = 'Reparto del costo operativo (503,293) entre 50 participantes y 50 de equipo. "Con 10% imprevistos" amarra con la meta 553,622.'
ws['A2'].font = Font(italic=True, color='5A6B82')

PART_LBL = [('casa', 'Casa (hospedaje)'), ('cocina', 'Comida del retiro'), ('biblias_y_peces', 'Biblia + pez'),
            ('transporte', 'Su transporte'), ('guias', 'Materiales de su PG'), ('liturgico', 'Litúrgico'), ('musica', 'Música')]
EQ_LBL = [('casa', 'Casa (hospedaje)'), ('transporte', 'Transporte (equipo + clausura)'), ('camisetas', 'Camiseta'),
          ('eventos_formativos', 'Formación'), ('almuerzo_ensayo', 'Almuerzo del ensayo'), ('liturgico', 'Litúrgico'), ('musica', 'Música')]

def costo_tabla(ws, startrow, titulo, desg_dict, lbls, oper, conimpr, cuota):
    ws.cell(row=startrow, column=1, value=titulo).font = Font(bold=True, size=12)
    head(ws, startrow + 1, ['Rubro', 'Por persona (operativo)'], [34, 22])
    r = startrow + 2
    for k, lbl in lbls:
        ws.cell(row=r, column=1, value=lbl).border = BORD
        c = ws.cell(row=r, column=2, value=desg_dict[k]); c.number_format = MON2; c.border = BORD
        if (r % 2) == 0:
            ws.cell(row=r, column=1).fill = ALT; ws.cell(row=r, column=2).fill = ALT
        r += 1
    ws.cell(row=r, column=1, value='Total operativo').font = BOLD
    cc = ws.cell(row=r, column=2, value=oper); cc.number_format = MON2; cc.font = BOLD
    ws.cell(row=r + 1, column=1, value='Con 10% de imprevistos').font = BOLD
    cc = ws.cell(row=r + 1, column=2, value=conimpr); cc.number_format = MON2; cc.font = Font(bold=True, color='059669')
    ws.cell(row=r + 2, column=1, value='Cuota que paga')
    cc = ws.cell(row=r + 2, column=2, value=cuota); cc.number_format = MON
    ws.cell(row=r + 3, column=1, value='No cubre la cuota (lo bajan donaciones/gestión)')
    cc = ws.cell(row=r + 3, column=2, value=conimpr - cuota); cc.number_format = MON2; cc.font = Font(color='B45309')
    return r + 4

nxt = costo_tabla(ws, 4, 'POR PARTICIPANTE', cpp['participante']['desglose_persona'], PART_LBL,
                  cpp['participante']['operativo_persona'], cpp['participante']['con_imprevistos_persona'], cuota_part)
costo_tabla(ws, nxt + 1, 'POR MIEMBRO DE EQUIPO', cpp['equipo']['desglose_persona'], EQ_LBL,
            cpp['equipo']['operativo_persona'], cpp['equipo']['con_imprevistos_persona'], eq_total)

# ---------------------------------------------------------------- 2. Cuotas --
ws = wb.create_sheet('2 Cuotas')
ws['A1'] = 'Lo que ponemos nosotros (cuotas)'; ws['A1'].font = Font(bold=True, size=14)
head(ws, 3, ['Cuota', 'Monto', 'Cantidad', 'Recauda', 'Qué cubre'], [16, 12, 12, 14, 60])
ws.append([])  # placeholder safety
for r, (lbl, monto, n, total, cubre) in enumerate([
    ('Participante', cuota_part, n_part, part_cuota_total, 'Transporte · comida · casa · pez · biblia'),
    ('Equipo', eq_total, '53 (4×500)', equipo_cuotas, 'Ensayo general · prorrateo del salón · transporte · comida del ensayo · camiseta'),
], start=4):
    ws.cell(row=r, column=1, value=lbl).border = BORD
    c = ws.cell(row=r, column=2, value=monto); c.number_format = MON; c.border = BORD
    ws.cell(row=r, column=3, value=n).border = BORD
    c = ws.cell(row=r, column=4, value=total); c.number_format = MON; c.border = BORD
    ws.cell(row=r, column=5, value=cubre).border = BORD
ws.cell(row=6, column=1, value='TOTAL en cuotas').font = BOLD
c = ws.cell(row=6, column=4, value=cuotas); c.number_format = MON; c.font = Font(bold=True, color='059669')
ws['A8'] = 'La Sor y el Padre Paul NO pagan: lo asume la Co-Dirección (la meta 106,000 se mantiene). Los backups no van y no pagan.'
ws['A8'].font = Font(italic=True, color='5A6B82')

# ------------------------------------------------------------- 3. Simulador --
ws = wb.create_sheet('3 Simulador')
ws['A1'] = 'Simulador — ¿cuánto baja si lo conseguimos?'; ws['A1'].font = Font(bold=True, size=14)
ws['A2'] = 'Escribe "S" en "¿Conseguido?" para los rubros que se cubran con donación/gestión/exención. La falta se recalcula sola.'
ws['A2'].font = Font(italic=True, color='5A6B82')
ws['A4'] = 'Costo de la misión'; ws['B4'] = meta; ws['B4'].number_format = MON; ws['B4'].font = BOLD
ws['A5'] = 'Lo que ya ponemos (cuotas)'; ws['B5'] = cuotas; ws['B5'].number_format = MON
head(ws, 7, ['Rubro', 'Monto', 'Donable', '¿Conseguido? (S/N)'], [34, 14, 12, 18])
first = 8
for i, r in enumerate(sim):
    row = first + i
    ws.cell(row=row, column=1, value=r['nombre']).border = BORD
    c = ws.cell(row=row, column=2, value=r['monto']); c.number_format = MON; c.border = BORD
    ws.cell(row=row, column=3, value='sí' if r['donable'] else '—').border = BORD
    cc = ws.cell(row=row, column=4, value=''); cc.border = BORD; cc.alignment = CEN
    if r['donable']:
        ws.cell(row=row, column=3).fill = PatternFill('solid', fgColor='D7F5E6')
last = first + len(sim) - 1
sumif = f'SUMIF(D{first}:D{last},"S",B{first}:B{last})'
rr = last + 2
ws.cell(row=rr, column=1, value='Conseguido (donación/gestión)').font = BOLD
c = ws.cell(row=rr, column=2, value=f'={sumif}'); c.number_format = MON; c.font = Font(bold=True, color='0c8fce')
ws.cell(row=rr + 1, column=1, value='HAY QUE REUNIR (falta)').font = Font(bold=True, size=12)
c = ws.cell(row=rr + 1, column=2, value=f'=B4-B5-{sumif}'); c.number_format = MON; c.font = Font(bold=True, size=12, color='C2410C')
ws.cell(row=rr + 2, column=1, value='Por cada uno (100 personas)')
c = ws.cell(row=rr + 2, column=2, value=f'=MAX(0,(B4-B5-{sumif}))/100'); c.number_format = MON2

# ------------------------------------------------ 4. Control de pagos -------
ws = wb.create_sheet('4 Control de pagos (interno)')
ws['A1'] = 'Control de pagos del equipo — INTERNO (Tesorería)'; ws['A1'].font = Font(bold=True, size=14)
ws['A2'] = f'Cuota {eq_total:,} = 4 × {eq_pago} (jun-sep). Escribe el monto pagado en cada mes. NO se muestra en el HTML.'
ws['A2'].font = Font(italic=True, color='5A6B82')
head(ws, 4, ['Nombre', 'Área', 'Jun', 'Jul', 'Ago', 'Sep', 'Pagado', 'Saldo', 'Estado'],
     [32, 22, 8, 8, 8, 8, 11, 11, 16])
AREA_ORDER = ['directores', 'asesores', 'asesores_espirituales', 'guias', 'musica', 'cocina', 'asesores_cocina', 'asesores_diocesanos']
AREA_LABEL = {'directores': 'Co-Dirección', 'asesores': 'Asesores', 'asesores_espirituales': 'Asesores Espirituales',
              'guias': 'Guías', 'musica': 'Música', 'cocina': 'Cocina', 'asesores_cocina': 'Asesoras de Cocina',
              'asesores_diocesanos': 'Asesores de Comunidad'}
roster = []
for area in AREA_ORDER:
    for p in EQ:
        if p['area'] == area and not p.get('backup') and not p.get('vacante'):
            roster.append((p['nombre'], AREA_LABEL[area]))
r = 5
for nombre, area in roster:
    asumida = nombre in exentos
    ws.cell(row=r, column=1, value=nombre).border = BORD
    ws.cell(row=r, column=2, value=area).border = BORD
    for col in range(3, 7):
        cc = ws.cell(row=r, column=col, value=(eq_pago if asumida else None)); cc.number_format = MON; cc.border = BORD; cc.alignment = CEN
    cp = ws.cell(row=r, column=7, value=f'=SUM(C{r}:F{r})'); cp.number_format = MON; cp.border = BORD
    cs = ws.cell(row=r, column=8, value=f'={eq_total}-G{r}'); cs.number_format = MON; cs.border = BORD
    est = ws.cell(row=r, column=9, value='ASUMIDA · Co-Dir' if asumida else ''); est.border = BORD
    if asumida:
        for col in range(1, 10):
            ws.cell(row=r, column=col).fill = GOLD
    elif (r % 2) == 0:
        for col in range(1, 10):
            ws.cell(row=r, column=col).fill = ALT
    r += 1
ws.cell(row=r + 1, column=1, value='TOTAL cobrado').font = BOLD
c = ws.cell(row=r + 1, column=7, value=f'=SUM(G5:G{r-1})'); c.number_format = MON; c.font = BOLD
ws.cell(row=r + 1, column=8, value='meta');
c = ws.cell(row=r + 1, column=9, value=equipo_cuotas); c.number_format = MON; c.font = Font(bold=True, color='059669')
ws.freeze_panes = 'A5'

out = os.path.join(REPO, 'Tripulacion_ETC88.xlsx')
wb.save(out)
print(f"OK  Tripulacion_ETC88.xlsx — 4 hojas (costo/persona · cuotas · simulador · control de pagos interno · {len(roster)} del equipo)")
