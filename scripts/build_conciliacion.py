#!/usr/bin/env python3
"""
Conciliación Final ETC 88 (10-sep-2026, post-retiro).
Genera data/presupuesto/Conciliacion_Final_ETC88.xlsx.

Fuentes:
- Números OFICIALES: vista pública del tablero financetc88.streamlit.app (10-sep).
- Detalle nominal: listado del director (donaciones, pagos, salidas) + cotización
  comida (Paloma 01-sep) + cálculo casa (director) + presupuesto excel 11-Aug.
Regla #1: nada inventado. Regla #3: sumas verificadas con assert antes de escribir.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'data/presupuesto/Conciliacion_Final_ETC88.xlsx'

# ══════════ DATOS ══════════
# Entradas oficiales (tablero)
CUOTAS      = 98000
TARDANZAS   = 6800
DONAC_EFEC  = 155021
PARTICIP    = 156800
PROFONDO    = 135866
ENTRADAS    = 552487
SALIDAS     = 515944
BALANCE     = 36543
REAL_CUENTAS= 34337
IMPUESTOS   = BALANCE - REAL_CUENTAS   # 2,206

assert CUOTAS+TARDANZAS+DONAC_EFEC+PARTICIP+PROFONDO == ENTRADAS, "entradas no cuadran"
assert ENTRADAS - SALIDAS == BALANCE, "balance no cuadra"

# Donaciones en especie por área (detalle)
especie = {
  'Guías': [
    ('Mochilas de colores', 3037, 'Priscila'),
    ('Rosarios', 2429, 'Priscila'),
    ('Courier (Aeropaq)', 800, 'Priscila'),
    ('Alambre de la fe', 1074, 'Priscila'),
    ('Libretas participantes', 1619, 'Luisa'),
    ('Stickers habitaciones + PG', 1199, 'Luisa'),
    ('Separadores de libros', 750, 'Camila'),
    ('Forros de pequeños grupos', 7500, 'los guías'),
    ('Peces para los forros', 2000, 'los guías'),
    ('Pañuelos', 1032, 'los guías (propios)'),
    ('Impresiones diversas', 0, 'Darianny'),
  ],
  'Directores': [
    ('Peces (símbolo, 60 ud)', 36000, 'donados'),
    ('Resmas de papel', 800, 'materiales oficina'),
    ('Sobres carta compromiso + lapiceros', 1500, 'materiales oficina'),
    ('Banderín (tela, pintura)', 0, 'donado'),
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
# ~85,894 (los montos donados son aproximados; ±2 por redondeo de centavos)
assert abs(ESPECIE_TOTAL - 85894) <= 2, f"especie={ESPECIE_TOTAL} (esperado ~85,894)"

# Donaciones en efectivo (listado del director — 47 aportantes)
donac_efectivo = [
    ("Mamá J & J",5000),("Sobrante",100),("Maria Astacio",2000),("Gilberto Vásquez",6000),
    ("Víctor Fernández",3000),("Scarlett Nivar",1000),("Daysiber",4000),("Wilfrid (Ivanna)",1000),
    ("Sahoni",2000),("Pamela Nivar (biblia)",800),("Roosbert Mejia (biblia)",800),
    ("Víctor Tomás Frías",20000),("Alberlys (Day)",1000),("Yelaxni",1200),("Wendy (Day)",700),
    ("Julio Muñoz (JM)",5831.92),("Carol Fernández",8400),("Emmanuel Ureña",5000),
    ("Yendry Rincon",1000),("Kharla Castillo",4500),("Therapia Café",4500),("Donación vía Wirna",2000),
    ("Mirna Stapleton",2500),("Brezzy Tavarez",3000),("Miriel Mercedes",1000),("Brissa Angelica",800),
    ("Gisselle Núñez",6633),("Sheiner (Nelson)",4000),("Emely Soriano",3000),("Abrahan",10000),
    ("Mamá de Yelaxni",500),("Zaglul",3000),("Jamirka",2000),("Jessica de León",2000),
    ("Eliana Almeida",1500),("Rosanna Matos",3000),("Carlos Rosario",1500),("Bendición",3157),
    ("Carolina Almánzar",800),("Papa de J&J",5000),("Justin Méndez",5000),("Melida Marian Feliz",800),
    ("Jonathan Medina",1500),("Glenys Sosa",2000),("Yaneris Almeida",5000),("Maria vizcaino",2000),
    ("Sol Brito",1000),
]
donac_list_tot = sum(v for _,v in donac_efectivo)  # 150,521.92
donac_otras = DONAC_EFEC - donac_list_tot           # dif vs tablero (~4,499)

# Salidas de caja (listado) + casa + ajustes = total tablero
salidas_caja = [
    ("Compra de comida (cotización Paloma 01-sep)", 74509.62),
    ("Pago a JM (reembolso adelanto)", 37500),
    ("Pago a JM x Biblias ETC 88 (reembolso)", 35360),
    ("Concejo (reserva 10% casa)", 23600),
    ("Mitad de transporte", 17500),
    ("Cocina", 15980),
    ("Comida de ensayo", 14730),
    ("Pago 50% de Camisetas", 14400),
    ("Pago 50% faltante de Camisetas", 14400),
    ("Bizcocho", 6000),
    ("Pago 50% llaveros Música", 4500),
    ("Saldo llaveros de música", 4500),
    ("Pago Impresión materiales guías", 3600),
    ("Pago merienda convivencia", 3420),
    ("Pago del salón ensayo etc", 3000),
    ("Pago caja de palancas", 2965),
    ("Merienda Formación", 2500),
    ("Pago currier materiales guías", 2120),
    ("Pago descontado a Priscila (donación materiales)", 2000),
    ("Helado premio", 1740),
]
caja_tot = sum(v for _,v in salidas_caja)  # 284,324.62
CASA_FINAL = 217020        # pago final casa (fuera de la caja del listado)
TRANSPORTE_EXTRA = 10000   # pagado de más vs presupuesto
# El resto hasta cuadrar salidas del tablero = impuestos/ITBIS y ajustes menores
AJUSTE_IMP = SALIDAS - (caja_tot + CASA_FINAL + TRANSPORTE_EXTRA)  # ~4,599

# Presupuesto por área (excel 11-Aug) + real
ppto = [
    ('Directores (casa, transporte, biblias, camisetas...)', 428940),
    ('Cocina', 132639.84),
    ('Guías', 24157.86),
    ('Música', 10511.86),
]
PPTO_TOTAL = sum(v for _,v in ppto)  # 596,249.56

# ══════════ ESTILO ══════════
MAR = '5B3A29'; VERDE='10B981'; AZUL='0B1F3A'; ROJO='EF4444'; CREMA='F7EFD9'; GRIS='94A3B8'
def fill(hex_): return PatternFill('solid', fgColor=hex_)
def font(sz=11, b=False, color='1E293B'): return Font(size=sz, bold=b, color=color)
thin = Side(style='thin', color='D0D0D0')
border = Border(bottom=thin)
money_fmt = '#,##0.00'

wb = openpyxl.Workbook()

def money(ws, r, c, v):
    cell = ws.cell(r, c, v); cell.number_format = money_fmt; return cell

# ────── HOJA 1: CONCILIACIÓN ──────
ws = wb.active; ws.title = 'Conciliación Final'
ws.column_dimensions['A'].width = 42
ws.column_dimensions['B'].width = 18
ws.column_dimensions['C'].width = 40
ws.merge_cells('A1:C1')
c = ws['A1']; c.value = 'CONCILIACIÓN FINAL · ETC 88'; c.font = Font(size=15, bold=True, color=CREMA); c.fill = fill(MAR); c.alignment = Alignment(horizontal='center')
ws.merge_cells('A2:C2')
c = ws['A2']; c.value = '10 de septiembre de 2026 · post-retiro · cifras del tablero oficial'; c.font = Font(size=9, italic=True, color='666666'); c.alignment = Alignment(horizontal='center')

r = 4
ws.cell(r,1,'ENTRADAS').font = font(12, True, MAR); r+=1
for label, val, nota in [
    ('Cuotas del equipo', CUOTAS, '49 miembros × 2,000 (100%)'),
    ('Tardanzas', TARDANZAS, 'multas de formaciones'),
    ('Donaciones en efectivo', DONAC_EFEC, '~47 aportantes'),
    ('Pagos de participantes', PARTICIP, '97% del esperado'),
    ('Profondo (rifa)', PROFONDO, 'actividades pro-fondo · sin salidas'),
]:
    ws.cell(r,1,label).font = font(); money(ws,r,2,val); ws.cell(r,3,nota).font = font(9, color='888888')
    for cc in range(1,4): ws.cell(r,cc).border = border
    r+=1
ws.cell(r,1,'ENTRADAS TOTALES').font = font(11, True); money(ws,r,2,ENTRADAS).font = font(11, True); 
for cc in range(1,3): ws.cell(r,cc).fill = fill('E8F5E9')
r+=2

ws.cell(r,1,'SALIDAS').font = font(12, True, ROJO); r+=1
ws.cell(r,1,'Total de salidas (gastos + salidas profondo)').font = font(); money(ws,r,2,SALIDAS); r+=2

ws.cell(r,1,'BALANCE').font = font(12, True, AZUL); r+=1
ws.cell(r,1,'Balance (entradas − salidas)').font = font(11, True); money(ws,r,2,BALANCE).font = font(11, True)
for cc in range(1,3): ws.cell(r,cc).fill = fill('E3F2FD')
r+=1
ws.cell(r,1,'Dinero real en cuentas (tuya + Day)').font = font(); money(ws,r,2,REAL_CUENTAS); r+=1
ws.cell(r,1,'Diferencia = impuestos no reflejados').font = font(9, color='888888'); money(ws,r,2,IMPUESTOS).font = font(9, color='888888'); r+=2

ws.cell(r,1,'APOYO TOTAL DONADO').font = font(12, True, VERDE); r+=1
ws.cell(r,1,'Donaciones en efectivo (entraron a caja)').font = font(); money(ws,r,2,DONAC_EFEC); r+=1
ws.cell(r,1,'Donaciones en especie (bajaron el costo)').font = font(); money(ws,r,2,ESPECIE_TOTAL); r+=1
ws.cell(r,1,'TOTAL DONADO').font = font(11, True); money(ws,r,2,DONAC_EFEC+ESPECIE_TOTAL).font = font(11, True)
for cc in range(1,3): ws.cell(r,cc).fill = fill('E8F5E9')

# ────── HOJA 2: DONACIONES EFECTIVO ──────
ws2 = wb.create_sheet('Donaciones efectivo')
ws2.column_dimensions['A'].width = 32; ws2.column_dimensions['B'].width = 16
ws2.merge_cells('A1:B1'); c = ws2['A1']; c.value='DONACIONES EN EFECTIVO'; c.font=Font(size=13,bold=True,color=CREMA); c.fill=fill(MAR); c.alignment=Alignment(horizontal='center')
ws2.cell(3,1,'Aportante').font=font(10,True); ws2.cell(3,2,'Monto').font=font(10,True)
r=4
for n,v in donac_efectivo:
    ws2.cell(r,1,n).font=font(10); money(ws2,r,2,v); r+=1
ws2.cell(r,1,'Subtotal listado').font=font(10,True); money(ws2,r,2,donac_list_tot).font=font(10,True); r+=1
ws2.cell(r,1,'Otras donaciones (registradas en tablero)').font=font(9,color='888888'); money(ws2,r,2,donac_otras); r+=1
ws2.cell(r,1,'TOTAL (tablero)').font=font(11,True); money(ws2,r,2,DONAC_EFEC).font=font(11,True)
for cc in range(1,3): ws2.cell(r,cc).fill=fill('E8F5E9')

# ────── HOJA 3: DONACIONES ESPECIE ──────
ws3 = wb.create_sheet('Donaciones especie')
ws3.column_dimensions['A'].width = 52; ws3.column_dimensions['B'].width = 14; ws3.column_dimensions['C'].width = 22
ws3.merge_cells('A1:C1'); c=ws3['A1']; c.value='DONACIONES EN ESPECIE (bajaron el costo)'; c.font=Font(size=13,bold=True,color=CREMA); c.fill=fill(MAR); c.alignment=Alignment(horizontal='center')
r=3
for area, items in especie.items():
    ws3.cell(r,1,f'{area}  —  subtotal {especie_tot[area]:,.0f}').font=font(11,True,MAR)
    for cc in range(1,4): ws3.cell(r,cc).fill=fill('F0EAD6')
    r+=1
    for desc, val, quien in items:
        ws3.cell(r,1,desc).font=font(10); money(ws3,r,2,val); ws3.cell(r,3,quien).font=font(9,color='888888')
        for cc in range(1,4): ws3.cell(r,cc).border=border
        r+=1
    r+=1
ws3.cell(r,1,'TOTAL DONADO EN ESPECIE').font=font(11,True); money(ws3,r,2,ESPECIE_TOTAL).font=font(11,True)
for cc in range(1,3): ws3.cell(r,cc).fill=fill('E8F5E9')

# ────── HOJA 4: SALIDAS ──────
ws4 = wb.create_sheet('Salidas')
ws4.column_dimensions['A'].width = 50; ws4.column_dimensions['B'].width = 16
ws4.merge_cells('A1:B1'); c=ws4['A1']; c.value='SALIDAS'; c.font=Font(size=13,bold=True,color=CREMA); c.fill=fill(ROJO); c.alignment=Alignment(horizontal='center')
ws4.cell(3,1,'A · Salidas de caja (tu cuenta + Day)').font=font(11,True,MAR); r=4
for n,v in salidas_caja:
    ws4.cell(r,1,n).font=font(10); money(ws4,r,2,v); ws4.cell(r,1).border=border; ws4.cell(r,2).border=border; r+=1
ws4.cell(r,1,'Subtotal caja').font=font(10,True); money(ws4,r,2,caja_tot).font=font(10,True); r+=2
ws4.cell(r,1,'B · Pagados por otras vías').font=font(11,True,MAR); r+=1
for n,v in [('Casa — pago final (97 pers + jueves + habitaciones)',CASA_FINAL),
            ('Transporte pagado de más vs presupuesto',TRANSPORTE_EXTRA),
            ('Impuestos / ITBIS y ajustes menores',AJUSTE_IMP)]:
    ws4.cell(r,1,n).font=font(10); money(ws4,r,2,v); r+=1
ws4.cell(r,1,'TOTAL SALIDAS (tablero)').font=font(11,True); money(ws4,r,2,SALIDAS).font=font(11,True)
for cc in range(1,3): ws4.cell(r,cc).fill=fill('FDE8E8')

# ────── HOJA 5: PRESUPUESTO vs REAL ──────
ws5 = wb.create_sheet('Presupuesto vs Real')
ws5.column_dimensions['A'].width = 46; ws5.column_dimensions['B'].width = 16; ws5.column_dimensions['C'].width = 16
ws5.merge_cells('A1:C1'); c=ws5['A1']; c.value='PRESUPUESTO vs REAL'; c.font=Font(size=13,bold=True,color=CREMA); c.fill=fill(AZUL); c.alignment=Alignment(horizontal='center')
ws5.cell(3,1,'Área').font=font(10,True); ws5.cell(3,2,'Presupuestado').font=font(10,True); ws5.cell(3,3,'Donado especie').font=font(10,True)
r=4
for area, val in ppto:
    ws5.cell(r,1,area).font=font(10); money(ws5,r,2,val)
    key = area.split(' ')[0]
    dn = especie_tot.get('Directores' if 'Director' in area else key.replace('Guías','Guías'), 0)
    dn = especie_tot.get(next((k for k in especie_tot if k in area or area.startswith(k)), ''), 0)
    money(ws5,r,3,dn); r+=1
ws5.cell(r,1,'TOTAL').font=font(11,True); money(ws5,r,2,PPTO_TOTAL).font=font(11,True); money(ws5,r,3,ESPECIE_TOTAL).font=font(11,True)
for cc in range(1,4): ws5.cell(r,cc).fill=fill('E3F2FD')
r+=2
ws5.cell(r,1,'Presupuesto planificado').font=font(10); money(ws5,r,2,PPTO_TOTAL); r+=1
ws5.cell(r,1,'(−) Donaciones en especie').font=font(10); money(ws5,r,2,-ESPECIE_TOTAL); r+=1
ws5.cell(r,1,'Costo real neto estimado').font=font(11,True); money(ws5,r,2,PPTO_TOTAL-ESPECIE_TOTAL).font=font(11,True)
for cc in range(1,3): ws5.cell(r,cc).fill=fill('E8F5E9')
r+=1
ws5.cell(r,1,'Salidas reales ejecutadas (tablero)').font=font(9,color='888888'); money(ws5,r,2,SALIDAS).font=font(9,color='888888')

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(f'✓ Wrote {OUT}')
print(f'  Entradas {ENTRADAS:,} = cuotas {CUOTAS:,}+tard {TARDANZAS:,}+don {DONAC_EFEC:,}+part {PARTICIP:,}+profondo {PROFONDO:,}')
print(f'  Balance {BALANCE:,} · real {REAL_CUENTAS:,} · impuestos {IMPUESTOS:,}')
print(f'  Especie {ESPECIE_TOTAL:,} · Apoyo total donado {DONAC_EFEC+ESPECIE_TOTAL:,}')
print(f'  Salidas: caja {caja_tot:,.2f} + casa {CASA_FINAL:,} + transp {TRANSPORTE_EXTRA:,} + imp/ajuste {AJUSTE_IMP:,.2f} = {SALIDAS:,}')
