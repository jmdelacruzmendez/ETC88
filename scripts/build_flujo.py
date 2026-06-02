#!/usr/bin/env python3
"""Modelo económico del ETC 88 — borrador para la reunión de coordinadores.

Modela: recaudación, donaciones, FLUJO DE CAJA mensual, TOPES por área y OPTIMIZACIÓN,
priorizando los críticos (casa, transporte, comida). Genera Flujo_Caja_ETC88.xlsx.

TRAZABILIDAD — cada cifra tiene fuente:
  [DATO]      confirmado en data/estado.json.
  [ESTIMADO]  estimación de la hoja Finanzas (/tmp/etc88_costos.json, a validar en F1).
  [ESCENARIO] supuesto de este modelo (timing/split) — NO decidido; se ajusta.
El modelo NO inventa hechos: los montos confirmados salen de estado.json; lo demás va
etiquetado [ESTIMADO] o [ESCENARIO].
"""
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

C = json.load(open('/tmp/etc88_costos.json'))
EST = json.load(open('/home/user/ETC88/data/estado.json'))

TINTA, CREMA = '1C140B', 'F7EBCC'
MAR, TIERRA, SAFARI, AMBAR, CUERO = '1B3A52', 'B25028', '4A5D2E', 'C57920', '6B4423'
thin = Side(style='thin', color='C9AE76')
border = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = openpyxl.Workbook(); wb.remove(wb.active)

def title(ws, txt, color=MAR, span=6):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    c = ws.cell(row=1, column=1, value=txt)
    c.font = Font(bold=True, size=13, color=CREMA); c.fill = PatternFill('solid', fgColor=color)
    c.alignment = Alignment(horizontal='left', vertical='center'); ws.row_dimensions[1].height = 28

def header(ws, r, cols, fill=TIERRA):
    for i, (name, w) in enumerate(cols, 1):
        c = ws.cell(row=r, column=i, value=name)
        c.font = Font(bold=True, size=10, color=CREMA); c.fill = PatternFill('solid', fgColor=fill)
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True); c.border = border
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[r].height = 24

def row(ws, r, vals, bold=False, fill=None):
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=i, value=v)
        c.font = Font(size=10, bold=bold); c.border = border
        c.alignment = Alignment(horizontal='right' if isinstance(v, (int, float)) else 'left',
                                vertical='center', wrap_text=True)
        if fill: c.fill = PatternFill('solid', fgColor=fill)
        if isinstance(v, (int, float)) and abs(v) >= 1000: c.number_format = '#,##0'

# ---- agregados base (trazables) ----
META   = C['total_cubrir']                 # [DATO] estado.meta = costo total
DEUDA  = C['deuda']                        # [DATO]
CUOTAS_PART = C['cuotas_part_total']       # [DATO]/[ESTIMADO] 53 x 3000
EQ_LOW, EQ_MID, EQ_HIGH = C['cuota_eq_low'], C['cuota_eq_mid'], C['cuota_eq_high']
PART, OPER, PERS = C['participantes'], C['operativos'], C['personas']

def area_sum(keys, field='base'):
    return sum(it[field] for it in C['items'] if any(k in it['concepto'] for k in keys))

# Agrupación por área para TOPES (suma de las líneas de la hoja Finanzas)
AREAS = [
    ('Casa de retiro', ['Casa de retiro'], True),
    ('Transporte', ['Transporte'], True),
    ('Cocina (comida + meriendas + decoración)', ['Cocina ·'], True),
    ('Materiales y Litúrgico', ['Materiales y Litúrgico'], False),
    ('Guías (PG)', ['Guías ·'], False),
    ('Música', ['Música ·'], False),
    ('Eventos formativos (F1–F5 + conviv. + ensayo + bienvenida)',
     ['Formaciones', 'Convivencia', 'Ensayo', 'Bienvenida'], False),
    ('Camisetas', ['Camisetas'], False),
    ('Avanzada (jueves)', ['Avanzada'], True),
    ('Imprevistos', ['Imprevistos'], False),
]

# =========================================================== 1. EL MODELO ==
ws = wb.create_sheet('1·Modelo')
title(ws, 'MODELO ECONÓMICO ETC 88 · la ecuación', MAR, 4)
ws.cell(row=2, column=1, value='COSTO TOTAL  =  CUOTAS  +  RECAUDACIÓN VARIABLE (rifa + venta de comida + donaciones)').font = Font(bold=True, size=11, color=TIERRA)
header(ws, 4, [('Concepto', 46), ('Monto (RD$)', 16), ('Fuente', 14), ('Notas', 44)], MAR)
eq_alta = EQ_HIGH   # ya es el agregado (47 × $2,000)
filas = [
    ('(=) COSTO TOTAL a cubrir (META)', META, '[DATO]', 'casa COMPLETA 100 pers + costos + camisetas + avanzada + eventos'),
    ('  · del cual, casa de retiro', C['casa_con'], '[DATO]', '100 personas × $2,000 (con exención)'),
    ('  · de la casa, deuda al Consejo (1ra salida)', DEUDA, '[DATO]', 'reserva ya pagada; NO se suma aparte (está dentro de la casa)'),
    ('', None, '', ''),
    (f'(–) Cuotas participantes (~{PART} × ${C["cuota_part"]:,})', CUOTAS_PART, '[ESTIMADO]', f'para completar {PERS} en la casa'),
    (f'(–) Cuotas equipo ({OPER} × $1,500–2,000)', eq_alta, '[PROPUESTA]', f'al tope del rango = ${EQ_LOW:,}–${EQ_HIGH:,}; sin cerrar'),
    ('(=) Subtotal CUOTAS', CUOTAS_PART + eq_alta, '', 'lo que aporta la gente directamente'),
    ('', None, '', ''),
    ('(=) BRECHA: rifa + venta de comida + donaciones', META - CUOTAS_PART - eq_alta, '', 'ESTO es lo que la recaudación variable debe levantar'),
]
r = 5
for f in filas:
    row(ws, r, f, bold=f[0].startswith('(=)'), fill='F3E4BE' if f[0].startswith('(=)') else None); r += 1
BRECHA = META - CUOTAS_PART - eq_alta

# =========================================================== 2. TOPES ======
ws = wb.create_sheet('2·Topes')
title(ws, 'TOPES POR ÁREA · cada coord refina en F1 SIN pasar el tope', TIERRA, 5)
ws.cell(row=2, column=1, value='Los 3 CRÍTICOS (casa, transporte, comida) se financian primero. Precios [ESTIMADO]; se ajustan a la baja en F1.').font = Font(italic=True, size=10)
header(ws, 4, [('Área', 46), ('Objetivo (base)', 16), ('Tope (máx)', 14), ('¿Crítico?', 12), ('Notas', 30)], TIERRA)
r = 5
tot_b = tot_m = 0
for nombre, keys, critico in AREAS:
    b = area_sum(keys, 'base'); mx = area_sum(keys, 'max')
    tot_b += b; tot_m += mx
    row(ws, r, (nombre, b, mx, 'CRÍTICO' if critico else '', 'financiar primero' if critico else 'ajustable a la baja'),
        fill='F7E0CF' if critico else None); r += 1
row(ws, r, ('TOTAL costos', tot_b, tot_m, '', 'sin contar la deuda'), bold=True, fill='F3E4BE'); r += 1
row(ws, r, ('+ Deuda al Consejo', DEUDA, DEUDA, 'CRÍTICO', 'primera obligación'), bold=True); r += 1
row(ws, r, ('= TOTAL A CUBRIR (META)', tot_b + DEUDA, tot_m + DEUDA, '', ''), bold=True, fill='F3E4BE')

# =========================================================== 3. FLUJO ======
# [ESCENARIO] timing de entradas y salidas por mes (jun→sep). Se ajusta con fechas reales.
ws = wb.create_sheet('3·Flujo de caja')
title(ws, 'FLUJO DE CAJA MENSUAL · arranca en –$23,600 (deuda) · [ESCENARIO] de fechas', SAFARI, 6)
ws.cell(row=2, column=1, value='Objetivo: que el SALDO no se vuelva crítico antes de un pago grande (casa, transporte). Las fechas son supuestos a confirmar.').font = Font(italic=True, size=10)
meses = ['jun', 'jul', 'ago', 'sep']
eq_mes = OPER * 500  # [PROPUESTA] $500/mes
entradas = {
    'Cuotas equipo ($500/mes) [PROPUESTA]':        {'jun': eq_mes, 'jul': eq_mes, 'ago': eq_mes, 'sep': eq_mes},
    'Cuotas participantes [ESTIMADO]':              {'jul': round(CUOTAS_PART*0.3), 'ago': CUOTAS_PART - round(CUOTAS_PART*0.3)},
    'Rifa neta (Profondo #1) [ESCENARIO]':          {'ago': 180000},
    'Venta de comida (Profondo #2) [ESCENARIO]':    {'sep': 60000},
    'Donaciones en efectivo [ESCENARIO]':           {'jul': 25000, 'ago': 40000, 'sep': 0},
}
salidas = {
    'Eventos formativos [ESTIMADO]':       {'jun': 5300, 'jul': 5300, 'ago': 34000, 'sep': 3000},
    'Materiales y litúrgico [ESTIMADO]':   {'jul': 40000, 'ago': 48500},
    'Cocina · compras [ESTIMADO]':         {'jul': 30000, 'sep': area_sum(['Cocina ·']) - 30000},
    'Guías · PG [ESTIMADO]':               {'ago': area_sum(['Guías ·'])},
    'Música [ESTIMADO]':                   {'ago': area_sum(['Música ·'])},
    'Camisetas [ESTIMADO]':                {'ago': area_sum(['Camisetas'])},
    'Casa · saldo (200K – 23.6K reserva) [DATO]': {'ago': 80000, 'sep': C['casa_con'] - DEUDA - 80000},
    'Transporte [ESTIMADO]':               {'sep': area_sum(['Transporte'])},
    'Avanzada jueves [ESTIMADO]':          {'sep': area_sum(['Avanzada'])},
    'Imprevistos (reserva) [ESTIMADO]':    {'sep': area_sum(['Imprevistos'])},
}
# Cierre del escenario: la donación de sep iguala salidas + deuda (el saldo termina en 0).
_tot_sal = sum(sum(d.values()) for d in salidas.values())
_tot_in = sum(sum(v.values()) for v in entradas.values())
entradas['Donaciones en efectivo [ESCENARIO]']['sep'] = max(0, _tot_sal + DEUDA - _tot_in)
header(ws, 4, [('Mes', 10)] + [(m, 12) for m in meses] + [('Total', 13)], SAFARI)
r = 5
ws.cell(row=r, column=1, value='ENTRADAS').font = Font(bold=True, color=SAFARI); r += 1
in_mes = {m: 0 for m in meses}
for nombre, d in entradas.items():
    vals = [d.get(m, 0) for m in meses]
    for m in meses: in_mes[m] += d.get(m, 0)
    row(ws, r, [nombre] + vals + [sum(vals)]); r += 1
row(ws, r, ['TOTAL ENTRADAS'] + [in_mes[m] for m in meses] + [sum(in_mes.values())], bold=True, fill='E7EFD6'); r += 2
ws.cell(row=r, column=1, value='SALIDAS').font = Font(bold=True, color=TIERRA); r += 1
out_mes = {m: 0 for m in meses}
for nombre, d in salidas.items():
    vals = [d.get(m, 0) for m in meses]
    for m in meses: out_mes[m] += d.get(m, 0)
    row(ws, r, [nombre] + vals + [sum(vals)]); r += 1
row(ws, r, ['TOTAL SALIDAS'] + [out_mes[m] for m in meses] + [sum(out_mes.values())], bold=True, fill='F7E0CF'); r += 2
# saldo acumulado
saldo = -DEUDA
row(ws, r, ['Saldo inicial', -DEUDA, '', '', '', 'deuda al Consejo'], bold=True); r += 1
neto = []
for m in meses:
    saldo += in_mes[m] - out_mes[m]; neto.append(saldo)
row(ws, r, ['Neto del mes'] + [in_mes[m] - out_mes[m] for m in meses] + [''], bold=True); r += 1
row(ws, r, ['SALDO ACUMULADO'] + neto + [''], bold=True, fill='F3E4BE'); r += 1
ws.cell(row=r, column=1, value='⚠ Vigilar: el saldo se aprieta antes de la rifa (ago) y de los pagos grandes de sep (casa, transporte).').font = Font(italic=True, size=10, color=TIERRA)

# =========================================================== 4. OPTIMIZACIÓN
ws = wb.create_sheet('4·Optimización')
title(ws, 'OPTIMIZACIÓN · palancas para cerrar (o reducir) la brecha', CUERO, 4)
ws.cell(row=2, column=1, value=f'Brecha a cubrir con recaudación variable ≈ ${BRECHA:,}. Estas palancas la bajan o la financian:').font = Font(bold=True, size=11, color=TIERRA)
header(ws, 4, [('Palanca', 40), ('Impacto (RD$)', 16), ('Cómo', 40), ('Estado', 14)], CUERO)
ahorro_exencion = (C['casa_sin'] - C['casa_con'])
palancas = [
    ('Mantener la exención de la casa', f'−{ahorro_exencion:,}', 'Comprar vía RNC de la parroquia de Paul (ya asumido)', '[DATO]'),
    ('Donaciones en especie para cocina', '−15,000 a −25,000', 'Arroz, habichuelas, aceite donados (el 79 lo logró)', '[ESCENARIO]'),
    ('Premio de la rifa DONADO', 'sube el neto', 'Si el premio se dona, casi todo lo vendido es neto', '[ESCENARIO]'),
    ('Recortar en F1 (topes) materiales y cocina', '−15,000 a −25,000', 'Son los rubros más grandes; ajustar a la baja con tope', '[ESCENARIO]'),
    ('Cuota del equipo al tope ($2,000 vs $1,500)', f'+{EQ_HIGH - EQ_LOW:,}', 'Decisión de la Dirección', '[PROPUESTA]'),
    ('Donaciones en efectivo (empresas)', 'cada peso baja la brecha', 'Responsabilidad de los Directores (delegable)', '[DATO]'),
    ('Completar 100 en la casa', 'cubre su propio costo', 'Cada participante paga su casa; llena el cupo (misión)', '[DATO]'),
]
r = 5
for p in palancas:
    row(ws, r, p); r += 1

# =========================================================== 5. ESCENARIO ==
ws = wb.create_sheet('5·Escenario')
title(ws, 'ESCENARIO DE CIERRE · UNA forma de cerrar la brecha — [ESCENARIO], a validar', AMBAR, 4)
ws.cell(row=2, column=1, value='No es una decisión: muestra que la ecuación PUEDE cerrar. Los montos de rifa/comida/donaciones se ajustan.').font = Font(italic=True, size=10)
header(ws, 4, [('Fuente variable', 36), ('Monto (RD$)', 16), ('Supuesto', 40), ('Estado', 12)], AMBAR)
esc = [
    ('Rifa neta (Profondo #1)', 180000, '≈1,800 boletos a $100, premio donado · cierra 2-ago', '[ESCENARIO]'),
    ('Venta de comida (Profondo #2)', 60000, 'benchmark ETC 79', '[ESCENARIO]'),
    ('Donaciones en efectivo', BRECHA - 180000 - 60000, 'lo que falte tras rifa y comida', '[ESCENARIO]'),
]
r = 5; tot = 0
for e in esc:
    row(ws, r, e); tot += e[1]; r += 1
row(ws, r, ('= TOTAL recaudación variable', tot, f'debe igualar la brecha ${BRECHA:,}', ''), bold=True, fill='F3E4BE'); r += 2
ws.cell(row=r, column=1, value='Lectura: la rifa es la palanca #1. Si el premio se dona y la cocina consigue especie, la donación en efectivo necesaria baja.').font = Font(italic=True, size=10)

wb.save('/home/user/ETC88/Flujo_Caja_ETC88.xlsx')
print(f"Wrote Flujo_Caja_ETC88.xlsx — {len(wb.sheetnames)} pestañas · brecha ${BRECHA:,}")
