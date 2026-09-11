#!/usr/bin/env python3
"""
Conciliación Final ETC 88 — versión OFICIAL (11-sep-2026, post-retiro).
Genera data/presupuesto/Conciliacion_Final_ETC88.xlsx (7 hojas).

FUENTE ÚNICA de movimientos: pestañas Gastos / Donaciones / Profondo del panel de
administración de financetc88.streamlit.app (extraídas 11-sep-2026, cuadran al peso
con las tarjetas KPI del panel). Cuotas, tardanzas y pagos de participantes vienen de
las tarjetas KPI (detalle por persona no extraído).
Aclaraciones del director (10–11 sep) incorporadas como notas.
Regla #1: nada inventado. Regla #3: sumas verificadas con assert antes de escribir.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'data/presupuesto/Conciliacion_Final_ETC88.xlsx'

# ══════════ TARJETAS KPI DEL PANEL ══════════
CUOTAS      = 98000       # 49 miembros × 2,000 (100%)
TARDANZAS   = 6800
PARTICIP    = 156800      # 97% de 161,000 (46 × 3,500)
PART_ESPER  = 161000
REAL_CUENTAS= 34337       # estado de cuenta al 11-sep (tuya + Day)

# ══════════ GASTOS — ledger (22) ══════════
gastos = [
    ("05/07","Merienda formación 3",2500,""),
    ("21/07","Pago descontado a Priscila por donación de materiales guías",2000,"Efectivo a Priscila: reduce su donación en especie (ver hoja Especie)"),
    ("05/08","Pago courier materiales guías",2120,""),
    ("07/08","Pago llaveros Música (50%)",4500,""),
    ("16/08","Compra merienda convivencia",3420,""),
    ("16/08","Pago 50% t-shirt equipo",14400,""),
    ("16/08","Pago impresiones guías (mochilas)",3600,"Distinto de 'impresiones diversas' donadas por Darianny (director)"),
    ("19/08","Pago salón para Ensayo (dom 23-ago)",3000,""),
    ("19/08","Pago a JM x pago Biblias ETC 88",35360,"Reembolso. Proforma Paulinas 34,000 + 1,360"),
    ("21/08","Pago 50% faltante de camisetas",14400,""),
    ("28/08","Cajitas para palancas",2965,""),
    ("28/08","Saldo llaveros de música",4500,""),
    ("01/09","Transporte — abono (1ª mitad)",17500,""),
    ("07/09","Helados premios",1740,""),
    ("07/09","Para tener en efectivo para imprevistos",15000,"⚠ SIN LIQUIDAR: entrega de fondos, no gasto ejecutado. Falta desglose."),
    ("10/09","Compra de comida (transferencia a Iberia)",74509,"Cotización Paloma 01-sep 77,044.05 → pagado 74,509"),
    ("10/09","Pago a JM (transporte + imprevistos)",37500,"Reembolso. Desglose del director: transporte 2ª mitad 17,500 (10,000 + 7,500) + desvío 10,000 + ofrenda P. Héctor confesiones 10,000. ⚠ Desglose NO está en el ledger."),
    ("10/09","Devolución del 10% del pago de la casa al Consejo",23600,"Reserva/avance de la casa"),
    ("10/09","Cocina (detalles) + gasolina",15980,""),
    ("10/09","Comida de ensayo (a JC)",14730,""),
    ("10/09","Bizcocho de bienvenida",6000,""),
    ("10/09","Pago de la Casa (final)",216620,"97 pers × 2,360 − avance 23,600 + jueves 19×500 + habitaciones"),
]
GASTOS_TOT = sum(m for _,_,m,_ in gastos)
assert GASTOS_TOT == 515944, f"gastos={GASTOS_TOT}"
SALIDAS = GASTOS_TOT   # profondo: 0 salidas registradas

# ══════════ DONACIONES — ledger (49) ══════════
# (fecha, donante, monto, nota, flag_consejo)
donaciones = [
    ("—","Mamá de Juan Manuel",5000,"Merienda formación 3",""),
    ("21/07","Sobrante de cuenta de Risaira",100,"Le sobran 100 pesos",""),
    ("21/07","Maria Astacio",2000,"",""),
    ("25/07","Daysiber Madeline Pérez",4000,"",""),
    ("30/07","Gilberto Vásquez",6000,"Vía Johnnito R",""),
    ("31/07","Víctor Fernández",3000,"Papá de Laura",""),
    ("01/08","Scarlett Nivar",1000,"",""),
    ("02/08","Wilfrid",1000,"Transferencia 'fantasma' (atribución inferida)","NOTA"),
    ("04/08","Sahoni Angomas",2000,"",""),
    ("06/08","Roosbert Mejía",800,"#Dóname1biblia",""),
    ("06/08","Pamela Nivar",800,"#Dóname1biblia",""),
    ("06/08","Víctor Tomás Frías",20000,"",""),
    ("07/08","Alberlys",1000,"Gestión Day",""),
    ("07/08","Yelaxni",1200,"Para detergentes",""),
    ("08/08","Wendy",700,"Gestión Dayrelins",""),
    ("10/08","Julio Muñoz",5831,"Gestión JM",""),
    ("11/08","Carol Fernández",8400,"Donación biblias",""),
    ("12/08","Emmanuel Ureña",5000,"Gestión Nelson",""),
    ("13/08","Yendry Rincón",1000,"Aún no se reporta comprobante","NOTA"),
    ("13/08","Kharla C.",4500,"Donación biblias",""),
    ("14/08","Therapia Café",4500,"",""),
    ("16/08","Wirna (biblias)",2000,"Vía Wirna",""),
    ("18/08","Breezy Tavarez",3000,"Vía Wirna",""),
    ("18/08","Mirna Stapleton",2500,"Vía Wirna",""),
    ("18/08","Miriel Mercedes",1000,"",""),
    ("20/08","Brissa Angélica",800,"Vía Wirna",""),
    ("21/08","Gisselle Núñez",6633,"Vía Paloma",""),
    ("21/08","Sheiner",4000,"Vía Nelson",""),
    ("22/08","Emely Soriano",3000,"",""),
    ("22/08","Abrahan",10000,"",""),
    ("23/08","Mamá de Yelaxni",500,"",""),
    ("24/08","Jamirka",2000,"Vía Wirna",""),
    ("25/08","Zaglul",3000,"Cheque cambiado y depositado",""),
    ("27/08","Jessica De León",2000,"",""),
    ("28/08","Eliana Almeida Rogers",1500,"",""),
    ("28/08","Rosanna Matos",3000,"Para papel de baño",""),
    ("29/08","Carlos Rosario",1500,"",""),
    ("30/08","Carolina Almánzar",800,"",""),
    ("30/08","Bendición",3157,"Cayó a cuenta Risaira",""),
    ("31/08","Papá de J&J",5000,"",""),
    ("31/08","Jonathan Medina",1500,"Diferencia de devolución de pago de participante caído",""),
    ("01/09","Justin Méndez",5000,"",""),
    ("01/09","Melida Marian Feliz",800,"",""),
    ("03/09","Glennys Sosa",2000,"",""),
    ("03/09","Yaneris Almeida",5000,"",""),
    ("07/09","Sol Brito",1000,"",""),
    ("07/09","Maria Vizcaíno",2000,"",""),
    ("10/09","Depósito no identificado",1000,"Nunca se encontró el dueño (director: donación real)","NOTA"),
    ("10/09","Johan",3500,"Transferencia 'fantasma' (confirmada por director)","NOTA"),
]
DONAC_EFEC = sum(m for _,_,m,_,_ in donaciones)
assert DONAC_EFEC == 155021 and len(donaciones) == 49, f"donaciones={DONAC_EFEC} n={len(donaciones)}"

# ══════════ PROFONDO — ledger (8 entradas, 0 salidas) ══════════
profondo = [
    ("17/08","Efectivo depositado de profondo a finanzas",18700,"Efectivo que manejaba profondo"),
    ("21/08","Transferencia bancaria de profondo",26500,"Cuenta Banreservas"),
    ("22/08","Efectivo en cuenta Dorian",71700,"Venta de boletos"),
    ("23/08","Devuelta excedente compra abanico",1400,"→ indica que el premio (abanico) se pagó con fondos de profondo"),
    ("25/08","Efectivo profondo",16966.40,""),
    ("25/08","Boleto de Luis transferido a Banreservas",400,""),
    ("28/08","Helados",100,""),
    ("01/09","Más helados",100,""),
]
PROFONDO = sum(m for _,_,m,_ in profondo)
assert abs(PROFONDO - 135866.40) < 0.01, f"profondo={PROFONDO}"

# ══════════ TOTALES ══════════
ENTRADAS = CUOTAS + TARDANZAS + DONAC_EFEC + PARTICIP + PROFONDO   # 552,487.40
BALANCE  = ENTRADAS - SALIDAS                                       # 36,543.40
IMPUESTOS= BALANCE - REAL_CUENTAS                                   # 2,206.40
assert abs(ENTRADAS - 552487.40) < 0.01 and abs(BALANCE - 36543.40) < 0.01

# ══════════ DONACIONES EN ESPECIE (director + presupuesto) ══════════
especie = {
  'Guías': [
    ('Mochilas de colores', 3037, 'Priscila'),
    ('Rosarios', 2429, 'Priscila'),
    ('Courier (Aeropaq)', 800, 'Priscila'),
    ('Alambre de la fe', 1074, 'Priscila'),
    ('Reembolso en efectivo a Priscila (Gastos 21/07)', -2000, 'ajuste: reduce su donación neta'),
    ('Libretas participantes', 1619, 'Luisa'),
    ('Stickers habitaciones + PG', 1199, 'Luisa'),
    ('Separadores de libros', 750, 'Camila'),
    ('Impresiones diversas', 3600, 'Darianny (distinto de mochilas, pagadas)'),
    ('Forros de pequeños grupos', 7500, 'los guías'),
    ('Peces para los forros', 2000, 'los guías'),
    ('Pañuelos', 1032, 'los guías (propios)'),
  ],
  'Directores': [
    ('Peces (símbolo, 60 ud)', 36000, 'La Vega'),
    ('Resmas de papel', 800, 'directores · materiales oficina'),
    ('Sobres carta compromiso + lapiceros', 1500, 'directores · materiales oficina'),
    ('Banderín (tela, pintura)', 0, 'Frank (sin valor presupuestado)'),
  ],
  'Cocina': [
    ('Plátanos verdes (200 ud)', 4000, 'Yelaxni Mota'),
    ('Arroz (50 de 70 lb)', 2250, 'Padre Paul'),
    ('Pasta larga (10 de 14 lb)', 650, 'César Iglesia'),
    ('Papel toalla (7 de 10 ud)', 763, 'César Iglesia'),
    ('Papel de baño (2 fardos)', 1600, 'César Iglesia'),
    ('Cloro / desinfectante / jabón / servilletas / detergente', 742, 'César Iglesia'),
    ('Aceite verde, vinagre, papel plástico/aluminio, aceite gde', 4588, 'Bono Olé'),
    ('Decoración (cerrar comedor)', 10300, 'donada'),
  ],
  'Música': [
    ('Pilas Duracell', 718, 'donadas'),
    ('Chocolate M&M', 469, 'donados'),
    ('Rollo de alambre', 75, 'donado'),
  ],
}
especie_tot = {a: sum(v for _,v,_ in items) for a, items in especie.items()}
ESPECIE_TOTAL = sum(especie_tot.values())
assert abs(ESPECIE_TOTAL - 87494) <= 2, f"especie={ESPECIE_TOTAL} (esperado ~87,494)"
OFICINA_REAL = 3140.07 + 726.04 + 1440.00   # 5,306.11 — recibos Cactus + Medamax (03/09), asumido por directores; NO entra a costos por instrucción del director

# ══════════ PRESUPUESTO — dos baselines ══════════
ppto_11ago = [('Directores',428940),('Cocina',132639.84),('Guías',24157.86),('Música',10511.86)]
ppto_sistem= [('Directores',362205),('Cocina',112384.84),('Guías',27757.86),('Música',10511.86)]
PPTO_11AGO = sum(v for _,v in ppto_11ago)   # 596,249.56
PPTO_SISTEM= sum(v for _,v in ppto_sistem)  # 512,859.56
CASA_TOTAL = 216620 + 23600                 # 240,220

# ══════════ ESTILO ══════════
MAR='5B3A29'; VERDE='10B981'; AZUL='0B1F3A'; ROJO='EF4444'; CREMA='F7EFD9'; AMBAR='F59E0B'
def fill(h): return PatternFill('solid', fgColor=h)
def font(sz=11, b=False, color='1E293B'): return Font(size=sz, bold=b, color=color)
border = Border(bottom=Side(style='thin', color='D0D0D0'))
FMT = '#,##0.00'
wb = openpyxl.Workbook()
def money(ws, r, c, v):
    cell = ws.cell(r, c, v); cell.number_format = FMT; return cell
def title(ws, text, color, span):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    c = ws['A1']; c.value = text; c.font = Font(size=13, bold=True, color=CREMA); c.fill = fill(color); c.alignment = Alignment(horizontal='center')
def widths(ws, *ws_):
    for i, w in enumerate(ws_): ws.column_dimensions[chr(65+i)].width = w

# ────── 1. CONCILIACIÓN ──────
ws = wb.active; ws.title = 'Conciliación Final'; widths(ws, 46, 18, 44)
title(ws, 'CONCILIACIÓN FINAL · ETC 88', MAR, 3)
ws.merge_cells('A2:C2'); c = ws['A2']; c.value = '11-sep-2026 · post-retiro · fuente: ledger admin del panel (Gastos/Donaciones/Profondo) + KPI · estado de cuenta al 11-sep'; c.font = Font(size=9, italic=True, color='666666'); c.alignment = Alignment(horizontal='center')
r = 4
ws.cell(r,1,'ENTRADAS').font = font(12, True, MAR); r += 1
for label, val, nota in [
    ('Cuotas del equipo', CUOTAS, '49 miembros × 2,000 · 100% (KPI)'),
    ('Tardanzas', TARDANZAS, 'multas de formaciones (KPI)'),
    ('Donaciones en efectivo', DONAC_EFEC, '49 aportantes · ledger'),
    ('Pagos de participantes', PARTICIP, f'97% de {PART_ESPER:,} · faltan {PART_ESPER-PARTICIP:,} (KPI)'),
    ('Profondo (rifa) — entradas netas', PROFONDO, '8 entregas de la comisión · 0 salidas registradas'),
]:
    ws.cell(r,1,label).font = font(); money(ws,r,2,val); ws.cell(r,3,nota).font = font(9, color='888888')
    for cc in range(1,4): ws.cell(r,cc).border = border
    r += 1
ws.cell(r,1,'ENTRADAS TOTALES').font = font(11, True); money(ws,r,2,ENTRADAS).font = font(11, True)
for cc in range(1,3): ws.cell(r,cc).fill = fill('E8F5E9')
r += 2
ws.cell(r,1,'SALIDAS').font = font(12, True, ROJO); r += 1
ws.cell(r,1,'Gastos (22 movimientos · ledger)').font = font(); money(ws,r,2,GASTOS_TOT); r += 1
ws.cell(r,1,'Salidas profondo').font = font(); money(ws,r,2,0); ws.cell(r,3,'ninguna registrada (ver nota Consejo #3)').font = font(9, color='888888'); r += 1
ws.cell(r,1,'SALIDAS TOTALES').font = font(11, True); money(ws,r,2,SALIDAS).font = font(11, True)
for cc in range(1,3): ws.cell(r,cc).fill = fill('FDE8E8')
r += 2
ws.cell(r,1,'BALANCE').font = font(12, True, AZUL); r += 1
ws.cell(r,1,'Balance (entradas − salidas)').font = font(11, True); money(ws,r,2,BALANCE).font = font(11, True)
for cc in range(1,3): ws.cell(r,cc).fill = fill('E3F2FD')
r += 1
ws.cell(r,1,'Dinero real en cuentas (tuya + Day) al 11-sep').font = font(); money(ws,r,2,REAL_CUENTAS); r += 1
ws.cell(r,1,'Diferencia = impuestos/comisiones no reflejados (director)').font = font(9, color='888888'); money(ws,r,2,IMPUESTOS).font = font(9, color='888888'); r += 2
ws.cell(r,1,'APOYO TOTAL DONADO').font = font(12, True, VERDE); r += 1
ws.cell(r,1,'Donaciones en efectivo (entraron a caja)').font = font(); money(ws,r,2,DONAC_EFEC); r += 1
ws.cell(r,1,'Donaciones en especie (bajaron el costo · estimado)').font = font(); money(ws,r,2,ESPECIE_TOTAL); r += 1
ws.cell(r,1,'TOTAL DONADO').font = font(11, True); money(ws,r,2,DONAC_EFEC+ESPECIE_TOTAL).font = font(11, True)
for cc in range(1,3): ws.cell(r,cc).fill = fill('E8F5E9')

# ────── 2. GASTOS ──────
ws2 = wb.create_sheet('Gastos'); widths(ws2, 8, 52, 14, 70)
title(ws2, 'GASTOS — ledger admin (22 movimientos)', ROJO, 4)
for i, h in enumerate(['Fecha','Concepto','RD$','Nota'], 1): ws2.cell(3,i,h).font = font(10, True)
r = 4
for f, cpt, m, n in gastos:
    ws2.cell(r,1,f).font = font(10); ws2.cell(r,2,cpt).font = font(10); money(ws2,r,3,m); ws2.cell(r,4,n).font = font(9, color=(ROJO if '⚠' in n else '888888'))
    for cc in range(1,5): ws2.cell(r,cc).border = border
    r += 1
ws2.cell(r,2,'TOTAL GASTOS (= salidas del panel)').font = font(11, True); money(ws2,r,3,GASTOS_TOT).font = font(11, True)
for cc in range(1,4): ws2.cell(r,cc).fill = fill('FDE8E8')
r += 2
ws2.cell(r,2,'Lectura: transporte total 45,000 = abono 17,500 + (dentro del reembolso a JM) 17,500 + desvío 10,000.').font = font(9, color='888888'); r += 1
ws2.cell(r,2,f'Casa total = final 216,620 + avance 23,600 = {CASA_TOTAL:,}.').font = font(9, color='888888')

# ────── 3. DONACIONES EFECTIVO ──────
ws3 = wb.create_sheet('Donaciones efectivo'); widths(ws3, 8, 30, 14, 52, 8)
title(ws3, 'DONACIONES EN EFECTIVO — ledger admin (49)', MAR, 5)
for i, h in enumerate(['Fecha','Donante','RD$','Nota','Consejo'], 1): ws3.cell(3,i,h).font = font(10, True)
r = 4
for f, d, m, n, flag in donaciones:
    ws3.cell(r,1,f).font = font(10); ws3.cell(r,2,d).font = font(10); money(ws3,r,3,m); ws3.cell(r,4,n).font = font(9, color='888888')
    if flag: ws3.cell(r,5,'⚠').font = font(10, True, AMBAR); ws3.cell(r,2).fill = fill('FFF4E0')
    for cc in range(1,6): ws3.cell(r,cc).border = border
    r += 1
ws3.cell(r,2,'TOTAL (= KPI del panel)').font = font(11, True); money(ws3,r,3,DONAC_EFEC).font = font(11, True)
for cc in range(1,4): ws3.cell(r,cc).fill = fill('E8F5E9')
r += 2
ws3.cell(r,2,'⚠ = requiere nota explícita para el Consejo (origen no verificado o sin comprobante). Suman 6,500.').font = font(9, color=AMBAR)

# ────── 4. PROFONDO ──────
ws4 = wb.create_sheet('Profondo'); widths(ws4, 8, 46, 14, 56)
title(ws4, 'PROFONDO (rifa) — ledger admin (8 entradas · 0 salidas)', AZUL, 4)
for i, h in enumerate(['Fecha','Concepto','RD$','Nota'], 1): ws4.cell(3,i,h).font = font(10, True)
r = 4
for f, cpt, m, n in profondo:
    ws4.cell(r,1,f).font = font(10); ws4.cell(r,2,cpt).font = font(10); money(ws4,r,3,m); ws4.cell(r,4,n).font = font(9, color='888888')
    for cc in range(1,5): ws4.cell(r,cc).border = border
    r += 1
ws4.cell(r,2,'TOTAL ENTRADAS PROFONDO').font = font(11, True); money(ws4,r,3,PROFONDO).font = font(11, True)
for cc in range(1,4): ws4.cell(r,cc).fill = fill('E3F2FD')
r += 2
ws4.cell(r,2,'⚠ Registrado en NETO: son las entregas de la comisión a finanzas. Los costos de la rifa (premio/abanico, boletos, helados) no aparecen como salida.').font = font(9, color=AMBAR); r += 1
ws4.cell(r,2,'   El Consejo no puede ver el bruto ni cuánto costó generar estos 135,866. Pedir el detalle a la comisión de Profondo.').font = font(9, color=AMBAR)

# ────── 5. DONACIONES ESPECIE ──────
ws5 = wb.create_sheet('Donaciones especie'); widths(ws5, 54, 14, 40)
title(ws5, 'DONACIONES EN ESPECIE (bajaron el costo · valoración a precio de presupuesto)', MAR, 3)
r = 3
for area, items in especie.items():
    ws5.cell(r,1,f'{area}  —  subtotal {especie_tot[area]:,.0f}').font = font(11, True, MAR)
    for cc in range(1,4): ws5.cell(r,cc).fill = fill('F0EAD6')
    r += 1
    for desc, val, quien in items:
        ws5.cell(r,1,desc).font = font(10, color=(ROJO if val < 0 else '1E293B')); money(ws5,r,2,val); ws5.cell(r,3,quien).font = font(9, color='888888')
        for cc in range(1,4): ws5.cell(r,cc).border = border
        r += 1
    r += 1
ws5.cell(r,1,'TOTAL DONADO EN ESPECIE').font = font(11, True); money(ws5,r,2,ESPECIE_TOTAL).font = font(11, True)
for cc in range(1,3): ws5.cell(r,cc).fill = fill('E8F5E9')
r += 2
ws5.cell(r,1,f'Nota: materiales de oficina costaron realmente {OFICINA_REAL:,.2f} (Cactus 3,140.07 + 726.04 · Medamax 1,440.00 · 03/09), asumidos por los directores.').font = font(9, color='888888'); r += 1
ws5.cell(r,1,'   Aquí se valoran a presupuesto (2,300) por instrucción del director; a valor real la especie subiría +3,006.11.').font = font(9, color='888888')

# ────── 6. PRESUPUESTO vs REAL (dos baselines) ──────
ws6 = wb.create_sheet('Presupuesto vs Real'); widths(ws6, 40, 16, 16, 16)
title(ws6, 'PRESUPUESTO vs REAL — dos baselines (ninguno cerrado: "Tentativo")', AZUL, 4)
for i, h in enumerate(['Área','11-Ago (usado)','Sistem (panel)','Donado especie'], 1): ws6.cell(3,i,h).font = font(10, True)
r = 4
for (a, v1), (_, v2) in zip(ppto_11ago, ppto_sistem):
    ws6.cell(r,1,a).font = font(10); money(ws6,r,2,v1); money(ws6,r,3,v2); money(ws6,r,4,especie_tot.get(a,0)); r += 1
ws6.cell(r,1,'TOTAL').font = font(11, True); money(ws6,r,2,PPTO_11AGO).font = font(11, True); money(ws6,r,3,PPTO_SISTEM).font = font(11, True); money(ws6,r,4,ESPECIE_TOTAL).font = font(11, True)
for cc in range(1,5): ws6.cell(r,cc).fill = fill('E3F2FD')
r += 2
ws6.cell(r,1,'Salidas reales ejecutadas').font = font(10, True); money(ws6,r,2,SALIDAS); money(ws6,r,3,SALIDAS); r += 1
ws6.cell(r,1,'Ejecución vs baseline').font = font(10); money(ws6,r,2,SALIDAS-PPTO_11AGO); money(ws6,r,3,SALIDAS-PPTO_SISTEM); r += 1
ws6.cell(r,1,'   (negativo = subejecución; positivo = sobrecosto)').font = font(9, color='888888'); r += 2
ws6.cell(r,1,'Casa: presupuesto').font = font(10); money(ws6,r,2,236000); money(ws6,r,3,200000); r += 1
ws6.cell(r,1,'Casa: real (216,620 + 23,600)').font = font(10); money(ws6,r,2,CASA_TOTAL); money(ws6,r,3,CASA_TOTAL); r += 1
ws6.cell(r,1,'Casa: desvío').font = font(10); money(ws6,r,2,CASA_TOTAL-236000); money(ws6,r,3,CASA_TOTAL-200000); r += 2
ws6.cell(r,1,'Diferencia entre baselines 83,390 = casa 36,000 + peces 31,000 + cocina 20,255 + transporte 5,000 + biblias 1,600 − guías 3,600 − ensayo 3,000 − avanzada 3,900 + palancas 35.').font = font(9, color='888888'); r += 1
ws6.cell(r,1,'Recomendación: declarar el 11-Ago como baseline ante el Consejo (refleja la tarifa real de la casa, 2,360); el Sistem es "lo que ve el panel".').font = font(9, color='888888')

# ────── 7. NOTAS PARA EL CONSEJO ──────
ws7 = wb.create_sheet('Notas Consejo'); widths(ws7, 10, 110)
title(ws7, 'PUNTOS QUE EL CONSEJO VA A PREGUNTAR — estado al 11-sep', AMBAR, 2)
notas = [
 ('ABIERTO', '15,000 "para tener en efectivo para imprevistos" (07/09): entrega de fondos sin desglose de uso. Es la única salida sin soporte.'),
 ('ABIERTO', '37,500 "Pago a JM (transporte + imprevistos)" (10/09): el director lo desglosa (transporte 17,500 + desvío 10,000 + ofrenda P. Héctor 10,000) pero el ledger no. Registrar el desglose y los recibos.'),
 ('ABIERTO', 'Profondo registrado en neto (135,866.40). Sin bruto ni costos (premio/abanico, boletos, helados). Pedir liquidación de la comisión.'),
 ('NOTA',    'Donaciones con origen no verificado o sin comprobante (6,500): Wilfrid 1,000 · Depósito no identificado 1,000 · Johan 3,500 · Yendry Rincón 1,000 (sin comprobante). Dejar nota explícita.'),
 ('CERRADO', 'Impresiones de guías: mochilas (3,600, pagadas) e "impresiones diversas" (3,600, donadas por Darianny) son trabajos distintos — no hay doble conteo.'),
 ('CERRADO', 'Priscila: donó materiales (7,340) y recibió 2,000 en efectivo (21/07). Su donación neta es 5,340; la especie de Guías ya lo descuenta.'),
 ('CERRADO', 'Balance 117,611 de la hoja General del presupuesto: celda manual de ~11-ago, pre-retiro. No es un segundo balance. El oficial es 36,543.40 → real 34,337 (dif 2,206.40 impuestos/comisiones).'),
 ('CERRADO', 'Casa: 216,620 final + 23,600 avance = 240,220. vs 11-Ago (236,000): +4,220. vs Sistem (200,000): +40,220 — el Sistem nunca actualizó la tarifa de 2,360.'),
 ('INFO',    f'Especie total {ESPECIE_TOTAL:,.0f}: el Sheet de presupuesto solo reflejaba 30,301 (flags sin actualizar). Peces (36,000, La Vega), decoración (10,300), Bono Olé (4,588), oficina y cocina no estaban marcados.'),
 ('INFO',    'Ambos presupuestos siguen marcados "Tentativo — sujeto a ajustes" (2/7/2026). Lección: cerrar formalmente el presupuesto antes del retiro.'),
 ('OPORT.',  f'Participantes: faltan {PART_ESPER-PARTICIP:,} por cobrar (97.4% de {PART_ESPER:,}).'),
]
r = 3
for tag, txt in notas:
    col = {'ABIERTO':ROJO,'NOTA':AMBAR,'CERRADO':VERDE,'INFO':'888888','OPORT.':AZUL}[tag]
    ws7.cell(r,1,tag).font = font(9, True, col); ws7.cell(r,2,txt).font = font(10); ws7.cell(r,2).alignment = Alignment(wrap_text=True)
    ws7.cell(r,1).border = border; ws7.cell(r,2).border = border; r += 1

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(f'✓ Wrote {OUT}')
print(f'  Entradas {ENTRADAS:,.2f} = cuotas {CUOTAS:,} + tard {TARDANZAS:,} + don {DONAC_EFEC:,} + part {PARTICIP:,} + profondo {PROFONDO:,.2f}')
print(f'  Salidas {SALIDAS:,} (22 gastos, 0 profondo) · Balance {BALANCE:,.2f} · real {REAL_CUENTAS:,} · dif {IMPUESTOS:,.2f}')
print(f'  Especie {ESPECIE_TOTAL:,} · Apoyo total donado {DONAC_EFEC+ESPECIE_TOTAL:,}')
print(f'  Baselines: 11-Ago {PPTO_11AGO:,.2f} · Sistem {PPTO_SISTEM:,.2f} · casa real {CASA_TOTAL:,}')
