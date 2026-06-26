#!/usr/bin/env python3
import os as _os
_R = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
"""Generate an editable master Excel (single source of truth) from the team data.

Idea: this xlsx is what YOU edit. Columns with dropdowns (Área, Rol, Coordinador,
Operativo, Comunidad) are the assignment layer you control. The dashboard can be
regenerated from this file so you never touch code to move someone between teams.
"""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

with open('/tmp/etc88_data.json') as f:
    d = json.load(f)

eq = d['equipo']

MESES = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
def cumple_txt(p):
    if not p.get('cumple_mes'): return ''
    return f"{p['cumple_dia']}-{MESES[p['cumple_mes']-1]}"

# Palette (matching the dashboard)
TINTA = '1C140B'; CREMA = 'F7EBCC'; PERG = 'E8D2A1'; VELA = 'F7EFD9'
AREA_FILL = {
    'directores':'B25028', 'asesores':'6B4423', 'guias':'1B3A52',
    'cocina':'4A5D2E', 'musica':'C57920',
    'asesores_cocina':'6E7F4C', 'asesores_espirituales':'4A372A', 'asesores_diocesanos':'8F4E10',
}

thin = Side(style='thin', color='C9AE76')
border = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()

# ============== Sheet 1: Equipo (editable master) ==============
ws = wb.active
ws.title = 'Equipo'

cols = [
    ('Nombre', 30), ('Sexo', 7), ('Edad', 7), ('Área', 16), ('Rol', 20),
    ('Coordinador', 13), ('Operativo', 11), ('Comunidad', 14), ('Residencia', 16),
    ('ETC propio', 11), ('Año ETC', 9), ('ETCs servidos', 13),
    ('Cumpleaños', 12), ('Teléfono', 15), ('Talla', 7), ('Sin formulario', 14),
]

# Title row
ws.merge_cells('A1:P1')
c = ws['A1']
c.value = 'ETC 88 · TRIPULACIÓN — Hoja maestra del equipo (editá las celdas; el tablero se regenera de aquí)'
c.font = Font(name='Calibri', bold=True, size=13, color=CREMA)
c.fill = PatternFill('solid', fgColor='0E2238')
c.alignment = Alignment(horizontal='left', vertical='center')
ws.row_dimensions[1].height = 26

# Header row
hdr = 2
for i, (name, width) in enumerate(cols, start=1):
    cell = ws.cell(row=hdr, column=i, value=name)
    cell.font = Font(bold=True, size=10, color=CREMA)
    cell.fill = PatternFill('solid', fgColor='762E10')
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = border
    ws.column_dimensions[get_column_letter(i)].width = width
ws.row_dimensions[hdr].height = 30

# Data rows
r = hdr + 1
for p in eq:
    vals = [
        p['nombre'].replace(' (sin formulario)', ''),
        p['sexo'],
        p['edad'] if p['edad'] else '',
        p['area'],
        p['rol'],
        'Sí' if (p.get('rol','').lower().find('coord') >= 0) else 'No',
        'Sí' if p.get('operativo') else 'No',
        p['comunidad'] if p['comunidad'] not in ('—',) else '',
        p['residencia'] if p['residencia'] != '—' else '',
        p['etc_propio'] if p['etc_propio'] else '',
        p['etc_anio_propio'] if p['etc_anio_propio'] else '',
        p['etcs_servidos'] if p['etcs_servidos'] is not None else '',
        cumple_txt(p),
        ('+' + p['telefono']) if p.get('telefono') else '',
        (p['talla'] or '').strip().upper() if p.get('talla') else '',
        'Sí' if p.get('sin_formulario') else 'No',
    ]
    for i, v in enumerate(vals, start=1):
        cell = ws.cell(row=r, column=i, value=v)
        cell.border = border
        cell.font = Font(size=10)
        cell.alignment = Alignment(horizontal='left' if i in (1,5,9) else 'center', vertical='center')
    # Tint the Área cell
    area_cell = ws.cell(row=r, column=4)
    fill = AREA_FILL.get(p['area'])
    if fill:
        area_cell.fill = PatternFill('solid', fgColor=fill)
        area_cell.font = Font(size=10, bold=True, color='FFFFFF')
    # Grey out non-operative rows lightly
    if not p.get('operativo'):
        for i in range(1, len(cols)+1):
            cc = ws.cell(row=r, column=i)
            if i != 4:
                cc.fill = PatternFill('solid', fgColor='F3E4BE')
    r += 1

last_row = r - 1

# Data validations (dropdowns)
def add_dv(col_letter, options, allow_blank=True):
    formula = '"' + ','.join(options) + '"'
    dv = DataValidation(type='list', formula1=formula, allow_blank=allow_blank)
    ws.add_data_validation(dv)
    dv.add(f'{col_letter}{hdr+1}:{col_letter}{last_row}')

add_dv('B', ['F','M','?'])
add_dv('D', list(AREA_FILL.keys()), allow_blank=False)
add_dv('F', ['Sí','No'], allow_blank=False)
add_dv('G', ['Sí','No'], allow_blank=False)
add_dv('H', ['Belén','Betania','Por confirmar'])
add_dv('P', ['Sí','No'], allow_blank=False)

ws.freeze_panes = 'A3'
ws.auto_filter.ref = f'A{hdr}:P{last_row}'

# ============== Sheet 2: Equipos auxiliares ==============
ws2 = wb.create_sheet('Equipos auxiliares')
ws2.merge_cells('A1:D1')
c = ws2['A1']
c.value = 'Equipos auxiliares (verticales por formular · pueden incluir gente externa)'
c.font = Font(bold=True, size=12, color=CREMA)
c.fill = PatternFill('solid', fgColor='8F4E10')
c.alignment = Alignment(horizontal='left', vertical='center')
ws2.row_dimensions[1].height = 24
aux_cols = [('Equipo', 22), ('Descripción', 60), ('Responsable sugerido', 28), ('Miembros (escribí aquí)', 40)]
for i, (name, width) in enumerate(aux_cols, start=1):
    cell = ws2.cell(row=2, column=i, value=name)
    cell.font = Font(bold=True, size=10, color=CREMA)
    cell.fill = PatternFill('solid', fgColor='4A372A')
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = border
    ws2.column_dimensions[get_column_letter(i)].width = width
rr = 3
for aux in d.get('equipos_auxiliares', []):
    for i, v in enumerate([aux['nombre'], aux['descripcion'], aux['responsable_sugerido'], ''], start=1):
        cell = ws2.cell(row=rr, column=i, value=v)
        cell.border = border
        cell.font = Font(size=10)
        cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    ws2.row_dimensions[rr].height = 42
    rr += 1

# ============== Sheet 3: Fichas (form responses, reference) ==============
ws3 = wb.create_sheet('Fichas (formulario)')
ws3.merge_cells('A1:I1')
c = ws3['A1']
c.value = 'Respuestas del formulario (referencia · no editar aquí, viene del Google Form)'
c.font = Font(bold=True, size=12, color=CREMA)
c.fill = PatternFill('solid', fgColor='1B3A52')
c.alignment = Alignment(horizontal='left', vertical='center')
ws3.row_dimensions[1].height = 24
ficha_cols = [
    ('Nombre', 26), ('Palabra', 16), ('Qué espera', 44), ('Miedos', 40),
    ('Tema (Dios)', 36), ('Alergias', 24), ('Condiciones', 24),
    ('Medicamentos', 24), ('Contacto emergencia', 30),
]
for i, (name, width) in enumerate(ficha_cols, start=1):
    cell = ws3.cell(row=2, column=i, value=name)
    cell.font = Font(bold=True, size=10, color=CREMA)
    cell.fill = PatternFill('solid', fgColor='0E2238')
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = border
    ws3.column_dimensions[get_column_letter(i)].width = width
rr = 3
for p in eq:
    if p.get('sin_formulario'): continue
    vals = [
        p['nombre'], (p.get('palabra') or '').strip(), p.get('que_espera') or '',
        p.get('miedos') or '', p.get('tema_dios') or '', p.get('alergias') or '',
        p.get('condiciones') or '', p.get('medicamentos') or '', p.get('contacto_emergencia') or '',
    ]
    for i, v in enumerate(vals, start=1):
        cell = ws3.cell(row=rr, column=i, value=v)
        cell.border = border
        cell.font = Font(size=9)
        cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    rr += 1
ws3.freeze_panes = 'A3'

# ============== Sheet 4: Leyenda ==============
ws4 = wb.create_sheet('Cómo usar')
notes = [
    ('Cómo usar esta hoja', True),
    ('', False),
    ('1. La pestaña "Equipo" es la fuente de verdad. Editá ahí: mové gente entre áreas, cambiá coordinadores, etc.', False),
    ('2. Las columnas Área, Sexo, Coordinador, Operativo y Comunidad tienen menú desplegable (clic en la celda).', False),
    ('3. Valores de Área: directores, asesores, guias, cocina, musica, asesores_cocina, asesores_espirituales, asesores_diocesanos.', False),
    ('4. "Operativo = Sí" = parte del equipo de formación semanal. "No" = solo está en el retiro (asesores ampliados).', False),
    ('5. "Sin formulario = Sí" = aún no llenó el formulario de preformación (Daylin, Olanlly, Roselyn, Pamela, asesores ampliados).', False),
    ('6. La pestaña "Fichas" es solo lectura: viene del Google Form. No la edites a mano.', False),
    ('7. La pestaña "Equipos auxiliares" es para Donaciones, Guagua y Actividad Profondo: escribí los miembros cuando los definas.', False),
    ('', False),
    ('Para regenerar el tablero HTML desde este archivo, se corre el script de build con este xlsx como entrada.', False),
    (f"Versión de datos: {d['meta']['version']} · {d['meta']['operativos']} operativos + {d['meta']['no_operativos']} ampliados = {d['meta']['total_equipo']} en el retiro.", False),
]
for i, (txt, isheader) in enumerate(notes, start=1):
    cell = ws4.cell(row=i, column=1, value=txt)
    if isheader:
        cell.font = Font(bold=True, size=14, color='762E10')
    else:
        cell.font = Font(size=11)
ws4.column_dimensions['A'].width = 120

wb.save(f'{_R}/Equipo_ETC88.xlsx')
print(f"Wrote Equipo_ETC88.xlsx ({last_row - hdr} personas en hoja Equipo)")
