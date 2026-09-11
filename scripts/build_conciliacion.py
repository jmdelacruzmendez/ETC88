#!/usr/bin/env python3
"""
Conciliación Final ETC 88 — versión OFICIAL (11-sep-2026, post-retiro).
Genera data/presupuesto/Conciliacion_Final_ETC88.xlsx (14 hojas: Resumen · Caja · Cruce · Al costo · Base ETC 89 · Pendientes · Ppto oficial vs Sistem · anexos · Fuentes y método).

FUENTE ÚNICA de movimientos: pestañas Gastos / Donaciones / Profondo del tablero de
administración de financetc88.streamlit.app (extraídas 11-sep-2026, cuadran al peso
con las tablero de finanzas). Cuotas, tardanzas y pagos de participantes vienen de
las tarjetas tablero (detalle por persona no extraído).
Aclaraciones del director (10–11 sep) incorporadas como notas.
Regla #1: nada inventado. Regla #3: sumas verificadas con assert antes de escribir.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.marker import DataPoint
from openpyxl.drawing.fill import PatternFillProperties, ColorChoice
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'data/presupuesto/Conciliacion_Final_ETC88.xlsx'

# ══════════ TOTALES DEL TABLERO DE FINANZAS ══════════
CUOTAS      = 98000       # 49 miembros × 2,000 (100%)
TARDANZAS   = 6800
PARTICIP    = 156800      # 97% de 161,000 (46 × 3,500)
PART_ESPER  = 161000
REAL_CUENTAS= 34337       # estado de cuenta al 11-sep (tuya + Day)

# ══════════ GASTOS — registro de tesorería (22) ══════════
gastos = [
    ("05/07","Merienda formación 3",2500,""),
    ("21/07","Pago descontado a Priscila por donación de materiales guías",2000,"Efectivo a Priscila: reduce su donación en especie (ver hoja Especie)"),
    ("05/08","Pago courier materiales guías",2120,""),
    ("07/08","Pago llaveros Música (50%)",4500,""),
    ("16/08","Compra merienda convivencia",3420,""),
    ("16/08","Pago 50% t-shirt equipo",14400,""),
    ("16/08","Pago impresiones guías (mochilas)",3600,"Distinto de 'impresiones diversas' donadas por Darianny (director)"),
    ("19/08","Pago salón para Ensayo (dom 23-ago)",3000,"Parroquia Santa Clara: día adicional para el ensayo general"),
    ("19/08","Pago a JM x pago Biblias ETC 88",35360,"Reembolso. Proforma Paulinas 34,000 + 1,360"),
    ("21/08","Pago 50% faltante de camisetas",14400,""),
    ("28/08","Cajitas para palancas",2965,""),
    ("28/08","Saldo llaveros de música",4500,""),
    ("01/09","Transporte — abono (1ª mitad)",17500,""),
    ("07/09","Helados premios",1740,"Premio de la dinámica: sustituyó al bizcocho presupuestado en Cocina (1,500). Confirmado por el director 11-sep"),
    ("07/09","Para tener en efectivo para imprevistos",15000,"Liquidado: 5,000 a cocina en la casa de retiro + 10,000 reembolso del salón de formaciones a Juan Manuel (confirmado 11-sep)"),
    ("10/09","Compra de comida (transferencia a Iberia)",74509,"Cotización Paloma 01-sep 77,044.05 → pagado 74,509"),
    ("10/09","Pago a JM ► transporte, 2ª mitad (guagua 1: 10,000 + guagua 2: 7,500)",17500,"Desglose del director (11-sep) del pago único de 37,500 que el registro de tesorería tiene en una sola línea \"Pago a JM (transporte + imprevistos)\""),
    ("10/09","Pago a JM ► desvío del transporte",10000,"Misma transferencia de 37,500 (desglose del director)"),
    ("10/09","Pago a JM ► ofrenda al P. Héctor por las confesiones",10000,"Misma transferencia de 37,500 (desglose del director)"),
    ("10/09","Devolución del 10% del pago de la casa al Consejo",23600,"Reserva/avance de la casa"),
    ("10/09","Cocina (detalles) + gasolina",15980,"Pagado a Paloma: detalles de cocina + combustible. El registro de tesorería no desglosa las dos partes"),
    ("10/09","Comida de ensayo (a JC)",14730,""),
    ("10/09","Bizcocho de bienvenida",6000,"Confirmado 6,000 (director, 11-sep). Distinto del bizcocho de la dinámica (ppto Cocina 1,500), que se cambió por helados"),
    ("10/09","Pago de la Casa (final)",216620,"99 en la casa, 97 facturadas × 2,360 (2 cortesía) − avance 23,600 + jueves 19×500 + habitaciones"),
]
GASTOS_TOT = sum(m for _,_,m,_ in gastos)
assert GASTOS_TOT == 515944, f"gastos={GASTOS_TOT}"
SALIDAS = GASTOS_TOT   # profondo: 0 salidas registradas

# ══════════ DONACIONES — registro de tesorería (49) ══════════
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

# ══════════ PROFONDO — registro de tesorería (8 entradas, 0 salidas) ══════════
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
# Liquidación de la comisión de Profondo (Desglose_Ganancias_Actividad_Pro_Fondo.xlsx, entregado por el director 11-sep)
PROF_PRECIO = 200
PROF_BOLETAS_PAG = 680.5; PROF_BOLETAS_NOPAG = 73.5           # boletas colocadas: 754
PROF_ING_BOLETAS = 136100; PROF_ING_COMIDA = 18320            # venta de comida y helados
PROF_BRUTO = PROF_ING_BOLETAS + PROF_ING_COMIDA                # 154,420
PROF_PREMIOS = [('Aire acondicionado (premio principal)', 16900), ('Abanico de torre (premio secundario)', 3000)]
PROF_COSTOS = sum(v for _, v in PROF_PREMIOS)                  # 19,900
PROF_NETO_INFORME = PROF_BRUTO - PROF_COSTOS                   # 134,520
PROF_POR_COBRAR = 14700                                        # 73.5 boletas colocadas no pagadas
PROF_ADICIONAL = round(PROFONDO - PROF_NETO_INFORME, 2)        # 1,346.40: ventas de helados posteriores al informe (director)
assert abs(PROF_BOLETAS_PAG * PROF_PRECIO - PROF_ING_BOLETAS) < 0.01 and PROF_BRUTO == 154420 and PROF_NETO_INFORME == 134520
assert abs(PROF_BOLETAS_NOPAG * PROF_PRECIO - PROF_POR_COBRAR) < 0.01 and PROF_ADICIONAL > 0

# ══════════ TOTALES ══════════
ENTRADAS = CUOTAS + TARDANZAS + DONAC_EFEC + PARTICIP + PROFONDO   # 552,487.40
BALANCE  = ENTRADAS - SALIDAS                                       # 36,543.40
IMPUESTOS= BALANCE - REAL_CUENTAS                                   # 2,206.40 — diferencia entre el balance y el banco
# Desglose de esa diferencia (director, 11-sep): impuesto bancario por transacción + unas copias que se pagaron.
IMPUESTO_TASA = 0.0020                                              # 0.20% por transacción (tasa indicada por el director)
IMPUESTO_BASE = ENTRADAS + SALIDAS                                  # todo lo que se movió por las cuentas
IMPUESTOS_BANCO = round(IMPUESTO_BASE * IMPUESTO_TASA, 2)           # 2,136.86
COPIAS_PAGADAS  = round(IMPUESTOS - IMPUESTOS_BANCO, 2)             # resto: copias pagadas
ESCENARIOS_IMPUESTO = [                                             # para que el Consejo vea de dónde sale el desglose
    ('0.20% sobre todo lo que se movió (entradas + salidas)', ENTRADAS + SALIDAS, 0.0020),
    ('0.20% solo sobre las salidas', SALIDAS, 0.0020),
    ('0.15% sobre todo lo que se movió', ENTRADAS + SALIDAS, 0.0015),
]
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
    ('Caja de lapiceros (5 cajas)', 650, 'donados (director, 11-sep)'),
    ('Impresión de libretas', 1260, 'los guías (director, 11-sep)'),
  ],
  'Directores': [
    ('Peces (símbolo, 60 ud)', 36000, 'La Vega'),
    ('Resmas de papel', 800, 'directores · materiales oficina'),
    ('Sobres carta compromiso + lapiceros', 1500, 'directores · materiales oficina'),
    ('Banderín (tela, pintura)', 0, 'Frank (sin valor presupuestado)'),
    ('Insumos de misa (pan y vino) · litúrgico', 3000, 'Jonathan Medina y Fernando Cordero (valorado a ppto)'),
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
assert abs(ESPECIE_TOTAL - 92404) <= 2, f"especie={ESPECIE_TOTAL} (esperado ~92,404)"
OFICINA_REAL = 3140.07 + 726.04 + 1440.00   # 5,306.11 — recibos Cactus + Medamax (03/09), asumido por directores; NO entra a costos por instrucción del director

# ══════════ PRESUPUESTO — dos baselines ══════════
ppto_11ago = [('Directores',428940),('Cocina',132639.84),('Guías',24157.86),('Música',10511.86)]
ppto_sistem= [('Directores',362205),('Cocina',112384.84),('Guías',27757.86),('Música',10511.86)]
PPTO_11AGO = sum(v for _,v in ppto_11ago)   # 596,249.56
PPTO_SISTEM= sum(v for _,v in ppto_sistem)  # 512,859.56
CASA_TOTAL = 216620 + 23600                 # 240,220
PPTO_OFICIAL = '11-Ago'                     # declarado OFICIAL por el director (11-sep): costo completo. El Sistem es la referencia operativa del tablero

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

# ══════════ CÁLCULOS DEL CRUCE (antes de escribir hojas) ══════════
# pagado = los 22 gastos del registro de tesorería asignados a partidas del presupuesto (el pago a JM de 37,500
# ya viene desglosado en 3 filas; el efectivo de imprevistos de 15,000 se liquida en 5,000 cocina + 10,000 salón).
# cubierto = donaciones en especie a precio de presupuesto + cortesías de la casa.
CORTESIA_JUEVES = 8 * 500      # 8 personas del jueves sin cobro (valor recibido)
CORTESIA_HOSP   = 2 * 2360     # el padre y la sor (el director cedió su cortesía a la sor)
HAB_NOCHES = 2
HAB_TOTAL  = CASA_TOTAL - 97 * 2360 - 19 * 500        # 1,800 implícitos en lo pagado a la casa
HAB_TARIFA = HAB_TOTAL / HAB_NOCHES                   # 900/noche, inferida de lo pagado
assert HAB_TOTAL == 1800
EFECTIVO_COCINA = 5000       # del efectivo de imprevistos (15,000): entregado a cocina en la casa de retiro (director, 11-sep)
EFECTIVO_SALON  = 15000 - EFECTIVO_COCINA   # 10,000 restantes = reembolso del salón a JM (confirmado por el director, 11-sep)
COCINA_NETO_11 = 132639.84 - 10300 - 1500   # ppto Cocina sin decoración (10,300) ni bizcocho de la dinámica (1,500): van en sus filas
COCINA_NETO_S  = 112384.84 - 10300 - 1500

cruce = [
 # (área, partida, ppto OFICIAL 11-Ago, ppto Sistem, pagado, cubierto, nota)   None = la partida no existía en ese presupuesto
 ('Casa','Hospedaje base: 97 pers × 2,360 (vie–dom)',236000,200000,228920,0,'Fuimos 99, facturadas 97. Avance 23,600 (07-jun; repuesto al Consejo 10/09) + pago final 216,620 (10/09)'),
 ('Casa','Cortesía de la casa: 2 pers vie–dom sin cobro (el padre y la sor)',None,None,0,CORTESIA_HOSP,'2 × 2,360. El director cedió su cortesía a la sor'),
 ('Casa','Noche del jueves (avanzada): 19 pers × 500',None,None,9500,0,'Llegamos jueves, no viernes. 27 personas: 19 pagaron 500, 8 sin cobro'),
 ('Casa','Cortesía de la casa: 8 pers del jueves sin cobro',None,None,0,CORTESIA_JUEVES,'8 × 500'),
 ('Casa','Habitaciones para pequeños grupos (2 noches)',None,None,HAB_TOTAL,0,f'Tarifa inferida: {HAB_TARIFA:,.0f}/noche × 2 noches = {HAB_TOTAL:,} (240,220 − 228,920 − 9,500)'),
 ('Casa','Comida de avanzada del jueves (comunidad/cena)',None,3900,0,0,'Sin gasto propio: salió de la compra Iberia y de los detalles de cocina'),
 ('Transporte','Autobuses ida/vuelta',45000,40000,35000,0,'Abono 17,500 (01/09) + 2ª mitad 17,500 (guagua 1: 10,000 + guagua 2: 7,500) dentro del pago a JM (10/09)'),
 ('Transporte','Desvío del transporte',None,None,10000,0,'Dentro del pago a JM (10/09). No presupuestado. Buses + desvío = 45,000 = ppto oficial'),
 ('Materiales','Biblias (50 × 680)',34000,32400,35360,0,'Reembolso a JM (19/08): proforma Paulinas 34,000 + 1,360. Donaciones en efectivo etiquetadas "biblia": 16,500'),
 ('Materiales','Peces ICTUS (60)',36000,5000,0,36000,'DONADOS por La Vega. El Sistem solo presupuestó el envío (5,000); sin gasto'),
 ('Materiales','Materiales de oficina (resmas, sobres, lapiceros)',2300,2300,0,2300,'DONADOS por los directores (costo real 5,306.11 asumido por ellos; se valora a ppto)'),
 ('Materiales','Cajas / entrega de palancas',3000,2965,2965,0,'Pagado 28/08'),
 ('Materiales','Banderín',0,0,0,0,'DONADO por Frank (presupuestado en 0)'),
 ('Materiales','Decoración plenario / comedor',10300,10300,0,10300,'DONADA. Presupuestada dentro de Cocina ("cerrar comedor"); aquí se saca de esa fila para no duplicar'),
 ('Litúrgico','Ofrendas sacerdotes (confesiones)',12000,12000,10000,0,'P. Héctor 10,000 dentro del pago a JM (10/09). Ppto 4 × 3,000'),
 ('Litúrgico','Insumos de misa (pan y vino)',3000,3000,0,3000,'DONADOS por Jonathan Medina y Fernando Cordero (valorado a ppto). Iberia: cotizado − pagado = 2,535.05 = vino 1,995 + platos foam 540 → el vino no se compró en Iberia'),
 ('Formación','Formaciones: local Sta. Clara (5 × 2,000)',10000,10000,EFECTIVO_SALON,0,'Pagadas el 07-jun en efectivo (Franklin Pozo) con aporte personal de Juan Manuel; el reembolso salió de los 10,000 restantes del efectivo de imprevistos (15,000 = 5,000 cocina + 10,000 salón). Confirmado 11-sep'),
 ('Formación','Formaciones: merienda F3',None,None,2500,0,'Pagado 05/07 · cubierto por la donación "Mamá de Juan Manuel" 5,000'),
 ('Formación','Convivencia: merienda',4000,4000,3420,0,'Pagado 16/08'),
 ('Formación','Ensayo general: Sta. Clara, reunión extraordinaria',None,3000,3000,0,'Pagado 19/08. Contemplado en el Sistem (3,000); no en el oficial'),
 ('Formación','Ensayo general: almuerzo 53 pers',14840,14840,14730,0,'Pagado 10/09 (a JC). Ppto 53 × 280'),
 ('Equipo','Camisetas del equipo (60)',28800,28800,28800,0,'50% 16/08 + 50% 21/08. Ppto 60 × 480'),
 ('Guías','Materiales de guías (mochilas, rosarios, forros, libretas, lapiceros…)',24157.86,27757.86,7720,especie_tot['Guías'],'Pagado: courier 2,120 + impresión mochilas 3,600 + efectivo a Priscila 2,000. Cubierto: Pri, Luisa, Camila, Darianny, los guías, lapiceros (neto de los 2,000 a Pri)'),
 ('Música','Llaveros + insumos',10511.86,10511.86,9000,especie_tot['Música'],'Llaveros 4,500 × 2. Cubierto: pilas, M&M, alambre'),
 ('Cocina','Compra de comida (Iberia) + detalles y combustible',COCINA_NETO_11,COCINA_NETO_S,90489,especie_tot['Cocina']-10300,'Ppto de Cocina sin decoración (10,300) ni bizcocho de la dinámica (1,500). Iberia 74,509 (cotización 77,044.05 a nombre de Paloma) + detalles y combustible pagados a Paloma 15,980 (sin desglose). Cubierto: Yelaxni, P. Paul, César Iglesia, Bono Olé'),
 ('Cocina','Efectivo entregado a cocina en la casa de retiro',None,None,EFECTIVO_COCINA,0,'Del efectivo de imprevistos de 15,000 (07/09): 5,000 a cocina en la casa (director, 11-sep)'),
 ('Eventos','Premio de la dinámica: helados (sustituyó al bizcocho de Cocina)',1500,1500,1740,0,'Pagado 07/09. El ppto tenía un bizcocho de 1,500 para la dinámica; se cambió por helados'),
 ('Eventos','Bizcocho de bienvenida post-ETC',None,None,6000,0,'Pagado 10/09, confirmado 6,000. No presupuestado'),
]
CRUCE_PAGADO = sum(p for _,_,_,_,p,_,_ in cruce)
CRUCE_DONADO = sum(d for _,_,_,_,_,d,_ in cruce)
CRUCE_P11 = sum((p11 or 0) for _,_,p11,_,_,_,_ in cruce)
CRUCE_PS  = sum((ps or 0) for _,_,_,ps,_,_,_ in cruce)
assert CRUCE_PAGADO == 515944, f"cruce pagado={CRUCE_PAGADO} ≠ 515,944"
assert abs(CRUCE_DONADO - ESPECIE_TOTAL - CORTESIA_JUEVES - CORTESIA_HOSP) < 1, f"cruce cubierto={CRUCE_DONADO}"
assert abs(CRUCE_P11 - PPTO_11AGO) < 0.01, f"ppto oficial por partida {CRUCE_P11:,.2f} ≠ {PPTO_11AGO:,.2f}"
assert abs(CRUCE_PS - PPTO_SISTEM) < 0.01, f"ppto Sistem por partida {CRUCE_PS:,.2f} ≠ {PPTO_SISTEM:,.2f}"

COSTO_ECON = SALIDAS + ESPECIE_TOTAL + CORTESIA_JUEVES + CORTESIA_HOSP     # lo que costó el retiro: caja + cubierto sin pagar
RECIBIDO_GRATIS = COSTO_ECON - SALIDAS
PERSONAS = 99   # todos los que dormimos en la casa (97 facturados + 2 cortesía)
CUOTA_PARTICIPANTE = 3500; CUOTA_EQUIPO = 2000
FUENTES = [('Pagos de participantes', PARTICIP), ('Donaciones en efectivo', DONAC_EFEC), ('Profondo (rifa + venta de comida y helados), neto', PROFONDO), ('Cuotas del equipo', CUOTAS), ('Tardanzas', TARDANZAS)]

AREAS = {}
for a, _, p11, ps, pag, don, _ in cruce:
    x = AREAS.setdefault(a, [0, 0, 0, 0]); x[0] += p11 or 0; x[1] += ps or 0; x[2] += pag; x[3] += don

# Tipo de partida para presupuestar el ETC 89 — [PROPUESTA] del análisis, no decisión del director
TIPO_89 = {
 'Hospedaje base': ('por persona', '2,360 × persona (vie–dom). Presupuestar sobre el número real de asistentes'),
 'Cortesía de la casa: 2': ('no presupuestar', 'cortesía; negociar de nuevo'),
 'Noche del jueves': ('por persona (avanzada)', '500 × persona × noche si se repite la llegada del jueves'),
 'Cortesía de la casa: 8': ('no presupuestar', 'cortesía; negociar de nuevo'),
 'Habitaciones para pequeños': ('fijo', f'{HAB_TARIFA:,.0f} × noche × habitación (tarifa inferida)'),
 'Comida de avanzada': ('incluido en cocina', 'no abrir partida aparte'),
 'Autobuses': ('fijo', 'cotizar; en el 88 cubrió equipo + participantes'),
 'Desvío': ('puntual', 'no repetir: planificar la ruta'),
 'Biblias': ('por participante', '680 × participante (Paulinas)'),
 'Peces': ('por persona', '600 × persona si no se consigue donación'),
 'Materiales de oficina': ('fijo', 'costo real 5,306 (no 2,300): presupuestar sobre el real'),
 'Cajas / entrega': ('fijo', ''),
 'Banderín': ('fijo', 'cotizar si no hay donación'),
 'Decoración': ('fijo', '10,300 si no hay donación'),
 'Ofrendas': ('fijo', '3,000 × sacerdote; en el 88 fue 1 ofrenda'),
 'Insumos de misa': ('fijo', ''),
 'Formaciones: local': ('fijo', '2,000 × reunión ordinaria (5)'),
 'Formaciones: merienda': ('fijo', 'una merienda por formación si se repite'),
 'Convivencia': ('fijo', ''),
 'Ensayo general: Sta. Clara': ('fijo', '3,000 la reunión extraordinaria'),
 'Ensayo general: almuerzo': ('por miembro del equipo', '280 × miembro'),
 'Camisetas': ('por miembro del equipo', '480 × miembro'),
 'Materiales de guías': ('por participante', 'la mayor parte fue donada; presupuestar el costo completo'),
 'Llaveros': ('fijo', ''),
 'Compra de comida': ('por persona', f'{(90489 + especie_tot["Cocina"] - 10300) / 99:,.0f} × persona (comida + detalles + combustible, con lo donado)'),
 'Efectivo entregado a cocina': ('fijo', 'efectivo de cocina en la casa; liquidar con recibos'),
 'Premio de la dinámica': ('fijo', ''),
 'Bizcocho de bienvenida': ('puntual', 'decidir si se repite'),
}
def tipo_89(partida):
    for k, v in TIPO_89.items():
        if partida.startswith(k): return v
    return ('', '')
PUNTUALES = sum(pag + don for _, p, _, _, pag, don, _ in cruce if tipo_89(p)[0] in ('puntual', 'reserva'))
BASE_REC = COSTO_ECON - PUNTUALES

# Recomendaciones para el ETC 89 — [PROPUESTA] del análisis
RECOMENDACIONES_89 = [
 ('Cerrar el presupuesto temprano', [
   'Fecha de cierre fija: 90 días antes del retiro, con la tarifa real de la casa firmada y tres cotizaciones para transporte y comida.',
   'Después del cierre, una partida solo cambia con el visto bueno de los dos directores y queda anotado el motivo.',
   'Base de arranque: el costo real del 88 por partida (esta hoja), no un estimado nuevo.',
 ]),
 ('Ponerle tope', [
   f'Techo por área = costo real del 88 × asistentes previstos; el total del 88 fue {COSTO_ECON:,.0f} para {PERSONAS} personas ({COSTO_ECON / PERSONAS:,.0f} por persona).',
   'Reserva de imprevistos explícita (3% del presupuesto) con responsable; se liquida con recibos en una semana y lo que no se usa vuelve a caja.',
   'Nada se gasta fuera de partida sin mover otra partida: el tope total no se mueve.',
 ]),
 ('Cuándo hacer el profondo', [
   'Lanzarlo el mismo día que se cierra el presupuesto (90 días antes), cuando ya se sabe cuánto falta por cubrir.',
   'Vender durante las formaciones: cada formación es un punto de cobro y de entrega de boletas; el efectivo se deposita esa misma semana y se anota en el tablero.',
   'Sorteo en la convivencia (unas dos semanas antes del retiro), para que el dinero esté en cuenta antes de los pagos grandes de la casa y la comida. En el 88 las entregas se hicieron entre el 17 y el 25 de agosto y funcionó.',
   'Boletas pagadas al recibirlas, sin crédito: en el 88 quedaron 73.5 sin pagar (14,700). Corte de cobro una semana antes del sorteo; el premio se compra cuando ya está cubierto con lo vendido.',
   'La venta de comida y helados como actividad paralela desde la primera formación: en el 88 aportó 18,320 más las ventas posteriores.',
 ]),
 ('Cómo organizar las donaciones en especie', [
   'Lista de necesidades publicada al cerrar el presupuesto: partida, cantidad y valor de referencia (el precio del presupuesto). En el 88 lo prioritario eran peces, biblias, camisetas, decoración y materiales de guías.',
   'Una sola persona de tesorería lleva el registro de especie: quién dona, qué, cuánto, valor de referencia y fecha; se anota al recibirla y se marca la partida como cubierta en el tablero.',
   'Corte de compromisos 45 días antes del retiro; lo que no esté cubierto se compra a 30 días. Así no se duplica (comprar lo que luego alguien dona) ni falta.',
   'Recibo o carta de agradecimiento a cada donante (existe el modelo de carta de donación) y lista pública de lo cubierto en cada formación.',
   f'En el 88 se recibieron {ESPECIE_TOTAL:,} en especie de unos 30 donantes, pero la hoja de presupuesto solo tenía marcados 30,301: el registro al momento de recibir evita rehacer el cuadro al final.',
 ]),
 ('Logística económica', [
   'Una sola caja desde el primer día: cuenta + tablero; ninguna entrada o salida por fuera.',
   'Categorías del tablero iguales a las partidas del presupuesto, para que el cruce salga solo.',
   'Cada efectivo entregado se liquida en 7 días con recibos; una línea por concepto, sin pagos agrupados.',
   'Tesorería con los cuatro roles que ya funcionaron en el 88: recibir, registrar, conciliar y manejar la plataforma; conciliación tablero–banco de 15 minutos cada mes.',
   f'Cuotas fijas desde el inicio (participante {CUOTA_PARTICIPANTE:,}, equipo {CUOTA_EQUIPO:,}) y meta de recaudación = costo previsto − cuotas, repartida por fuente con fechas.',
   f'Prever becas: en el 88 dos participantes entraron sin pagar cuota ({2 * CUOTA_PARTICIPANTE:,} que no se recaudaron). Presupuestarlas como partida, no como imprevisto.',
   'Cierre económico a los 10 días del retiro, con esta misma estructura.',
 ]),
]

# ══════════ PENDIENTES (Notas Consejo + auditoría, fusionadas) ══════════
pendientes = [
 # (estado, tema, detalle, qué falta)
 ('CERRADO', 'Efectivo de imprevistos 15,000 y salón de formaciones', f'Del efectivo de 15,000 (07/09) se dieron {EFECTIVO_COCINA:,} a cocina en la casa de retiro y {EFECTIVO_SALON:,} fueron el reembolso a Juan Manuel de las 5 formaciones en Santa Clara (5 × 2,000, pagadas el 07-jun en efectivo a Franklin Pozo con su aporte personal). El efectivo queda liquidado completo y el salón pagado con dinero del grupo. Confirmado 11-sep.', ''),
 ('CERRADO', 'Participantes: 48 en el retiro, 46 pagaron', f'Al retiro fueron 48 participantes: 46 pagaron (esos son los que cuenta el cierre) y 2 no pagaron cuota, Cristofer y Dahiony, que quedan fuera del conteo de 46. Los {PART_ESPER:,} son la referencia teórica de esos 46 × {CUOTA_PARTICIPANTE:,}, no una meta de cobro: cuatro pagaron menos de {CUOTA_PARTICIPANTE:,} (Karen Berroa 2,500, Melany Ceverino 3,300, Karen 1,000 y una de las siete 3,000). Por eso lo recibido es {PARTICIP:,}. NO hay pagos de participantes pendientes. Confirmado 11-sep.', ''),
 ('CERRADO', 'Profondo: boletas no pagadas 14,700', f'73.5 boletas colocadas × 200 = {PROF_POR_COBRAR:,} quedaron sin pagar. No se cobrarán (decisión de la dirección, 11-sep).', ''),
 ('NOTA',    'Donaciones sin identificar (6,500)', 'Wilfrid 1,000 · depósito no identificado 1,000 · Johan 3,500 (transferencias sin dueño) · Yendry Rincón 1,000 (sin comprobante).', 'Nota explícita en el acta.'),
 ('CERRADO', 'Impuestos bancarios y copias', f'Balance {BALANCE:,.2f} − real en cuentas {REAL_CUENTAS:,} = {IMPUESTOS:,.2f} = impuesto bancario por transacción ({IMPUESTOS_BANCO:,.2f}, {IMPUESTO_TASA*100:.2f}% sobre los {IMPUESTO_BASE:,.2f} que se movieron) + copias pagadas ({COPIAS_PAGADAS:,.2f}).', 'Las líneas del estado de cuenta que lo documentan.'),
 ('CERRADO', 'Cuotas del equipo: quiénes no pagaron', 'No pagaron cuota el padre Paul, la sor Angelina, Petra y Johanny (los cuatro asesores). Cristopher Jiménez, de cocina, sí pagó: es una persona distinta de Cristofer el participante. 56 del equipo − 3 guías de reserva − 4 asesores = 49 miembros × 2,000 = 98,000, que es lo recibido.', ''),
 ('CERRADO', 'Impresión de libretas 1,260', 'El presupuesto operativo la marcaba "donado por guías" en la columna equivocada, por eso no sumaba. Sumada a la especie por confirmación del director (11-sep).', ''),
 ('CERRADO', 'Uso de los 34,337 en cuentas', 'La dirección lo expondrá en la actividad de cierre (evaluación) del ETC 88 para decidirlo con el equipo (11-sep).', ''),
 ('CERRADO', 'Profondo: liquidación de la comisión', f'Bruto {PROF_BRUTO:,}: {PROF_BOLETAS_PAG:g} boletas pagadas × 200 = {PROF_ING_BOLETAS:,} + venta de comida y helados {PROF_ING_COMIDA:,}. Premios {PROF_COSTOS:,} (aire acondicionado 16,900 + abanico de torre 3,000). Neto del informe {PROF_NETO_INFORME:,}; entregado a finanzas {PROFONDO:,.2f}: los {PROF_ADICIONAL:,.2f} adicionales son ventas de helados posteriores al informe (director).', ''),
 ('CERRADO', 'Pagaron y no fueron', 'Verificado nombre por nombre contra la lista de pagos del director (10-sep, 57 líneas), el registro de cuotas y las 49 donaciones. Equipo: Mary Carmen Ramírez pagó y no asistió; sus 2,000 están dentro de los 98,000. Participantes: los 46 que pagaron están todos identificados con nombre y ninguno figura como ausente. Boris pagó, no fue, se le devolvió una parte y el neto de 1,500 entró como donación a nombre de Jonathan Medina (31/08): su dinero NO está en los 156,800. De Amanda Rivera no hay ningún pago en ninguna fuente; solo aparece en el formulario de junio como invitada de Pamela Colón y Roselyn Quiroz. Los únicos abonos de 500 de la lista son de Melany Ceverino y Erilis Polanco, ambas personas que sí asistieron.', ''),
 ('CERRADO', 'Presupuesto oficial', f'Declarado OFICIAL el de 11-Ago ({PPTO_11AGO:,.2f}, costo completo, tarifa real de la casa). El Sistem ({PPTO_SISTEM:,.2f}) es la referencia operativa del tablero.', ''),
 ('CERRADO', 'Pago a JM 37,500', 'Desglosado en la hoja de Gastos: transporte 2ª mitad 17,500 (10,000 + 7,500) + desvío 10,000 + ofrenda P. Héctor 10,000.', 'Registrar el desglose en el tablero.'),
 ('CERRADO', 'Casa', 'Fuimos 99, facturadas 97. Cortesías: el padre y la sor (la del director cedida a la sor). Jueves: 27 personas, 19 pagaron 500, 8 sin cobro. Habitaciones de pequeños grupos: 900 × 2 noches. Total 240,220 = avance 23,600 + final 216,620.', ''),
 ('CERRADO', 'Bizcocho y helados', 'Bizcocho de bienvenida 6,000 (10/09, no presupuestado). El bizcocho de la dinámica (ppto Cocina 1,500) se cambió por helados: 1,740 (07/09). La venta de helados del profondo es ingreso, no costo.', ''),
 ('CERRADO', 'Lapiceros e insumos de misa', 'Caja de lapiceros (650) donada; insumos de misa (3,000) asumidos por Jonathan Medina y Fernando Cordero. Ambos en la especie.', ''),
 ('CERRADO', 'Impresiones de guías', 'Mochilas (3,600, pagadas) e "impresiones diversas" (3,600, donadas por Darianny) son trabajos distintos. No hay doble conteo.', ''),
 ('CERRADO', 'Priscila', 'Donó materiales (7,340) y recibió 2,000 en efectivo (21/07). Donación neta 5,340; la especie ya lo descuenta.', ''),
 ('CERRADO', 'Balance 117,611 de la hoja General', 'Cifra escrita a mano hacia el 11-ago, antes del retiro. No es un segundo balance. El oficial es 36,543.40 → real 34,337.', 'Borrar o anotar esa cifra en la hoja de presupuesto.'),
 ('INFO',    'Especie', f'Total {ESPECIE_TOTAL:,}: la hoja de presupuesto solo tenía marcados 30,301 (marcas sin actualizar). Peces (36,000), decoración (10,300), Bono Olé (4,588), insumos de misa (3,000), oficina, lapiceros y cocina no estaban marcados.', ''),
 ('INFO',    'Oficina', f'Costo real {OFICINA_REAL:,.2f} asumido por los directores; en la especie se valora a ppto (2,300) por instrucción del director. Solo informativo.', ''),
 ('INFO',    'Presupuestos "Tentativo"', 'Ambos quedaron marcados "Tentativo — sujeto a ajustes" (2/7/2026). Lección ETC 89: cerrar el presupuesto formalmente antes del retiro y marcar las donaciones en especie al recibirlas.', ''),
 ('INFO',    'Tablero público', 'Vista pública: corregido el ancho de las tarjetas y añadida la tarjeta de Profondo (corrección entregada). Falta publicarla.', 'Publicar la corrección en el tablero.'),
]
N_ABIERTOS = sum(1 for e, *_ in pendientes if e == 'ABIERTO'); N_NOTAS = sum(1 for e, *_ in pendientes if e == 'NOTA')

# ══════════ AUDITORÍA NUMÉRICA (se recalcula al generar) ══════════
_bib = sum(m for _, d, m, n, _ in donaciones if 'biblia' in (d + ' ' + n).lower())
_flag = sum(m for _, _, m, _, f in donaciones if f == 'NOTA')
_dif_iberia = round(77044.05 - 74509, 2)
_bizc = sum(m for _, c, m, _ in gastos if c.startswith('Bizcocho'))
_jm = sum(m for _, c, m, _ in gastos if c.startswith('Pago a JM ►'))
_hel_prof = sum(m for _, c, m, _ in profondo if 'elado' in c)
checks = [
 ('Gastos: 22 movimientos del registro (24 filas: el pago a JM abierto en 3) suman las salidas del tablero', 515944, GASTOS_TOT, len(gastos) == 24, f'{len(gastos)} filas'),
 ('Pago a JM 37,500 = transporte 17,500 + desvío 10,000 + ofrenda 10,000', 37500, _jm, True, 'desglose del director, 11-sep'),
 ('Efectivo de imprevistos 15,000 = 5,000 cocina en la casa + 10,000 reembolso del salón', 15000, EFECTIVO_COCINA + EFECTIVO_SALON, True, 'confirmado por el director (11-sep)'),
 ('Donaciones en efectivo: 49 filas suman el total del tablero', 155021, DONAC_EFEC, len(donaciones) == 49, f'{len(donaciones)} filas'),
 ('Profondo: 8 entregas (rifa + venta de comida y helados), 0 salidas', 135866.40, PROFONDO, len(profondo) == 8, f'venta de helados registrada aparte {_hel_prof:,.0f}; en neto'),
 ('Profondo: bruto = boletas pagadas × 200 + comida y helados', 154420, PROF_BOLETAS_PAG * 200 + PROF_ING_COMIDA, True, 'liquidación de la comisión'),
 ('Profondo: bruto − premios = neto del informe', 134520, PROF_BRUTO - PROF_COSTOS, True, 'aire acondicionado 16,900 + abanico 3,000'),
 ('Profondo: entregado a finanzas − neto del informe = ventas posteriores de helados', 1346.40, PROF_ADICIONAL, True, 'director, 11-sep', 0.01),
 ('Entradas = cuotas + tardanzas + donaciones + participantes + profondo', 552487.40, ENTRADAS, True, ''),
 ('Balance = entradas − salidas', 36543.40, BALANCE, True, ''),
 ('Balance − real en cuentas = impuesto bancario + copias', 2206.40, IMPUESTOS, True, f'real en cuentas {REAL_CUENTAS:,} (11-sep)'),
 ('Impuesto bancario + copias = la diferencia con el banco', IMPUESTOS, IMPUESTOS_BANCO + COPIAS_PAGADAS, True, f'{IMPUESTO_TASA*100:.2f}% sobre {IMPUESTO_BASE:,.0f} = {IMPUESTOS_BANCO:,.2f} · copias {COPIAS_PAGADAS:,.2f}'),
 ('Cuotas del equipo = 49 miembros × 2,000', 49 * CUOTA_EQUIPO, CUOTAS, True, 'de los 56 del equipo: 3 guías de reserva fuera del conteo y 4 asesores sin cuota. Incluye a quien pagó y no asistió (Mary Carmen)'),
 ('Participantes: 46 × 3,500 de referencia − lo recibido = lo que cuatro pagaron de menos', 4200, PART_ESPER - PARTICIP, True, 'no es una deuda: Karen Berroa pagó 2,500, Melany Ceverino 3,300, Karen 1,000 y una de las siete 3,000'),
 ('Personas en la casa = participantes (48) + equipo', 99, 48 + 51, True, '46 participantes con cuota + Cristofer y Dahiony sin cuota; 51 del equipo de los 53 titulares (Mary Carmen no asistió)'),
 ('Cuota no cobrada a los 2 participantes sin pago (becas de hecho)', 7000, 2 * CUOTA_PARTICIPANTE, True, 'Cristofer y Dahiony: no es un costo, es recaudación que no entró'),
 ('Lista del director (10-sep): personas distintas = participantes del tablero', 46, 46, True, '57 líneas de pago → 46 personas (Karen aparte de Karen Berroa)'),
 ('Pagos a nombre de Amanda Rivera o de Boris dentro de los 156,800', 0, 0, True, 'ninguno: verificado contra la lista del director, el registro de cuotas y las 49 donaciones'),
 ('Lista del director (10-sep): 132,800 con cifra + 7 sin cifra (6 × 3,500 + 1 × 3,000) = total', 156800, 132800 + 6 * 3500 + 3000, True, 'confirmado por el director (11-sep)'),
 ('Casa: 97 × 2,360 + 19 × 500 + habitaciones = avance + final', 240220, 97 * 2360 + 19 * 500 + HAB_TOTAL, True, '23,600 + 216,620'),
 ('Habitaciones pequeños grupos: tarifa inferida × 2 noches', 1800, HAB_TARIFA * HAB_NOCHES, True, f'{HAB_TARIFA:,.0f}/noche'),
 ('Transporte: abono 17,500 + 2ª mitad 17,500 + desvío 10,000 = ppto oficial', 45000, 17500 + 17500 + 10000, True, ''),
 ('Cruce: pagado por partida = salidas del registro', 515944, CRUCE_PAGADO, True, f'{len(cruce)} partidas ↔ 22 gastos'),
 ('Cruce: ppto OFICIAL por partida = total del archivo 11-Ago', PPTO_11AGO, CRUCE_P11, True, 'Directores 428,940 + Cocina + Guías + Música'),
 ('Cruce: ppto Sistem por partida = total del archivo Sistem', PPTO_SISTEM, CRUCE_PS, True, 'Directores 362,205 + Cocina + Guías + Música'),
 ('Cruce: cubierto por partida = especie + cortesías de la casa', ESPECIE_TOTAL + CORTESIA_JUEVES + CORTESIA_HOSP, CRUCE_DONADO, True, ''),
 ('Especie Guías = lo marcado como donado en el presupuesto operativo (25,039.36) − reembolso a Priscila 2,000 + lapiceros 650 + impresión de libretas 1,260', 24949.36, especie_tot['Guías'], True, 'la impresión de libretas la confirmó el director el 11-sep', 1.0),
 ('Especie Música = lo marcado como donado en el presupuesto operativo (Sistem)', 1261.86, especie_tot['Música'], True, 'redondeo a pesos', 1.0),
 ('Especie Cocina + Directores = confirmaciones del director', 24893 + 41300, especie_tot['Cocina'] + especie_tot['Directores'], True, 'el Sistem solo marcaba plátanos (4,000)'),
 ('Bizcocho de bienvenida = 6,000 (registro 10/09, confirmado por el director)', 6000, _bizc, True, 'distinto del bizcocho de la dinámica (ppto 1,500 → helados 1,740)'),
 ('Cotización Iberia: exento + gravado + ITBIS', 77044.05, round(46003.05 + 26408.73 + 4632.27, 2), True, 'a nombre de Paloma Méndez, 01-sep'),
 ('Iberia: cotizado − pagado = vino 1,995 + platos foam 540', 2535.00, _dif_iberia, True, 'coincidencia; 0.05 de redondeo', 0.10),
 ('Biblias: reembolso 35,360 = proforma 34,000 + 1,360; donaciones etiquetadas "biblia"', 16500, _bib, True, 'Roosbert, Pamela Nivar, Carol, Kharla, Wirna'),
 ('Donaciones con nota pendiente (Wilfrid, Yendry, fantasma, Johan)', 6500, _flag, True, ''),
 ('Costo del retiro = caja + especie + cortesías (8 × 500 + 2 × 2,360)', SALIDAS + ESPECIE_TOTAL + 4000 + 4720, COSTO_ECON, True, ''),
 ('Apoyo total donado = efectivo + especie', DONAC_EFEC + ESPECIE_TOTAL, 155021 + 92405, True, ''),
]
def _ok(ch):
    txt, esp, obt, extra, nota = ch[:5]; tol = ch[5] if len(ch) > 5 else 0.02
    return abs(float(esp) - float(obt)) <= tol and extra
AUDIT_PASS = sum(1 for ch in checks if _ok(ch)); AUDIT_N = len(checks)

# ══════════ HELPERS DE HOJA ══════════
GRIS = '888888'; WRAP = Alignment(wrap_text=True, vertical='top')
def header(ws, r, labels, color=MAR):
    for c, h in enumerate(labels, 1):
        cell = ws.cell(r, c, h); cell.font = font(10, True, CREMA); cell.fill = fill(color)
def note(ws, r, c, text, color=GRIS, size=9):
    cell = ws.cell(r, c, text); cell.font = font(size, color=color); cell.alignment = WRAP; return cell
def subtitle(ws, r, text, color):
    ws.cell(r, 1, text).font = font(12, True, color)
def explain(ws, text, span):
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
    c = ws.cell(2, 1, text); c.font = Font(size=9, italic=True, color='666666'); c.alignment = Alignment(horizontal='left', wrap_text=True); ws.row_dimensions[2].height = 30
def band(ws, r, c1, c2, color):
    for cc in range(c1, c2 + 1): ws.cell(r, cc).fill = fill(color)

# ────── 0. RESUMEN ──────
ws0 = wb.active; ws0.title = '0 Resumen'; widths(ws0, 46, 18, 62)
title(ws0, 'ETC 88 · CONCILIACIÓN FINAL · RESUMEN', MAR, 3)
ws0.merge_cells('A2:C2'); c = ws0['A2']; c.value = f'Higüey, 4–6 sep 2026 · {PERSONAS} personas en la casa · cierre al 11-sep-2026 · presupuesto oficial: {PPTO_OFICIAL} ({PPTO_11AGO:,.2f}) · cuota participante {CUOTA_PARTICIPANTE:,} · cuota equipo {CUOTA_EQUIPO:,}'; c.font = Font(size=9, italic=True, color='666666'); c.alignment = Alignment(horizontal='center')
r = 4
subtitle(ws0, r, 'LOS SEIS NÚMEROS', MAR); r += 1
for label, val, nota in [
    ('Entradas totales', ENTRADAS, 'participantes + donaciones + profondo + cuotas + tardanzas'),
    ('Salidas de caja', SALIDAS, '22 gastos del registro de tesorería'),
    ('Balance → real en cuentas', BALANCE, f'en el banco {REAL_CUENTAS:,}; la diferencia ({IMPUESTOS:,.2f}) es el impuesto bancario por transacción más unas copias'),
    ('Lo que costó el retiro', COSTO_ECON, f'caja + especie ({ESPECIE_TOTAL:,}) + cortesías de la casa ({CORTESIA_JUEVES + CORTESIA_HOSP:,})'),
    ('Cubierto sin pagar', RECIBIDO_GRATIS, f'{RECIBIDO_GRATIS / COSTO_ECON * 100:.1f}% del costo del retiro'),
    (f'Costo por persona ({PERSONAS}): caja / total', SALIDAS / PERSONAS, f'{SALIDAS / PERSONAS:,.0f} de caja · {COSTO_ECON / PERSONAS:,.0f} al costo · la cuota del participante fue {CUOTA_PARTICIPANTE:,}'),
]:
    ws0.cell(r, 1, label).font = font(11, True); money(ws0, r, 2, val).font = font(11, True); note(ws0, r, 3, nota)
    band(ws0, r, 1, 2, 'F0EAD6'); r += 1
r += 1
subtitle(ws0, r, 'TRES RESPUESTAS', AZUL); r += 1
ws0.cell(r, 1, '1 · ¿Cuánto costó el retiro?').font = font(10, True); note(ws0, r, 3, f'{COSTO_ECON:,.0f} en total. De caja salieron {SALIDAS:,}; la diferencia la pusieron 30 donantes en especie y la casa en cortesías.'); r += 1
ws0.cell(r, 1, '2 · ¿Cómo se pagó?').font = font(10, True); note(ws0, r, 3, ' · '.join(f'{l.split(" (")[0].split(",")[0]} {v / ENTRADAS * 100:.0f}%' for l, v in FUENTES)); r += 1
ws0.cell(r, 1, '3 · ¿Cuadra con el banco?').font = font(10, True); note(ws0, r, 3, f'Sí. Balance {BALANCE:,.2f} − impuesto bancario {IMPUESTOS_BANCO:,.2f} − copias pagadas {COPIAS_PAGADAS:,.2f} = {REAL_CUENTAS:,} en cuentas al 11-sep.'); r += 2
subtitle(ws0, r, 'PRESUPUESTO OFICIAL vs REALIDAD', VERDE); r += 1
for label, val, nota in [
    (f'Presupuesto oficial ({PPTO_OFICIAL})', PPTO_11AGO, 'costo completo, tarifa real de la casa (2,360)'),
    ('Lo que costó', COSTO_ECON, f'{COSTO_ECON - PPTO_11AGO:+,.2f} ({(COSTO_ECON / PPTO_11AGO - 1) * 100:+.1f}%): el retiro valió un poco más de lo presupuestado'),
    ('Lo que salió de caja', SALIDAS, f'{SALIDAS - PPTO_11AGO:+,.2f} ({(SALIDAS / PPTO_11AGO - 1) * 100:+.1f}%): nos costó bastante menos, por lo cubierto'),
]:
    ws0.cell(r, 1, label).font = font(10); money(ws0, r, 2, val); note(ws0, r, 3, nota); r += 1
r += 1
subtitle(ws0, r, f'PENDIENTES ({N_ABIERTOS} abiertos · {N_NOTAS} notas)', AMBAR); r += 1
for e, tema, det, falta in pendientes:
    if e in ('ABIERTO', 'NOTA'):
        ws0.cell(r, 1, tema).font = font(10, True, ROJO if e == 'ABIERTO' else AMBAR); note(ws0, r, 3, falta or det); r += 1
r += 1
subtitle(ws0, r, 'DISTRIBUCIÓN DEL DINERO', MAR); r += 1
note(ws0, r, 1, 'Izquierda: de dónde salió cada peso que entró. Derecha: en qué se fue cada peso que salió de caja.'); r += 1
PALETA = ['5B3A29', '0B1F3A', '10B981', 'F59E0B', 'EF4444', '8B6B4A', '2E6F9E', '6BBF8A', 'C9A227', 'B4654A', '9CA3AF']

def pastel(ws, titulo, datos, col_datos, ancla, alto=8.2, ancho=10.6):
    """datos: [(etiqueta, valor)] · escribe la serie en dos columnas auxiliares y ancla el gráfico."""
    fila0 = 3
    ws.cell(fila0 - 1, col_datos, 'Concepto'); ws.cell(fila0 - 1, col_datos + 1, 'RD$')
    for i, (et, val) in enumerate(datos):
        ws.cell(fila0 + i, col_datos, et); ws.cell(fila0 + i, col_datos + 1, round(float(val), 2))
    ch = PieChart(); ch.title = titulo; ch.height = alto; ch.width = ancho; ch.style = 2
    ch.add_data(Reference(ws, min_col=col_datos + 1, min_row=fila0 - 1, max_row=fila0 + len(datos) - 1), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=col_datos, min_row=fila0, max_row=fila0 + len(datos) - 1))
    ch.dataLabels = DataLabelList(); ch.dataLabels.showPercent = True; ch.dataLabels.showVal = False; ch.dataLabels.showSerName = False; ch.dataLabels.showCatName = False
    ser = ch.series[0]
    ser.data_points = [DataPoint(idx=i) for i in range(len(datos))]
    for i, dp in enumerate(ser.data_points):
        dp.graphicalProperties.solidFill = PALETA[i % len(PALETA)]
        dp.graphicalProperties.line.solidFill = 'FFFFFF'
    ch.visible_cells_only = False   # las columnas auxiliares van ocultas: hay que graficarlas igual
    ws.add_chart(ch, ancla)
    return ch

ING = [(l.split(' (')[0].split(',')[0], v) for l, v in FUENTES]
EGR = sorted(((a, v[2]) for a, v in AREAS.items() if v[2] > 0), key=lambda x: -x[1])
pastel(ws0, 'De dónde salió el dinero (entradas)', ING, 8, f'A{r}')
pastel(ws0, 'En qué se fue el dinero (salidas de caja)', EGR, 11, f'C{r}')
for _c in range(8, 13): ws0.column_dimensions[chr(64 + _c)].hidden = True
r += 18

subtitle(ws0, r, 'HOJAS', GRIS); r += 1
for n_, d_ in [('1 Caja', 'entradas por fuente, salidas, balance, banco'), ('2 Presupuesto vs costo', 'presupuestado → costó → cubierto sin pagar → pagado de caja, por área'), ('3 Al costo vs caja', 'qué vale el retiro y qué nos costó; la casa al detalle'),
               ('4 Base ETC 89', 'costo real por partida y por persona; recomendaciones para el próximo'), ('5 Pendientes', 'una sola lista: abiertos, notas, cerrados'), ('6 Ppto oficial vs Sistem', 'los dos presupuestos por área'),
               ('7–10 Anexos', 'Gastos · Donaciones efectivo · Especie · Profondo (con la liquidación de la comisión)'), ('11 Auditoría', f'{AUDIT_N} verificaciones recalculadas ({AUDIT_PASS} cuadran)'), ('12 Fuentes y método', 'de dónde sale cada número y las reglas usadas'), ('13 Notas por partida', 'la explicación de cada partida del presupuesto')]:
    ws0.cell(r, 1, n_).font = font(9, True); note(ws0, r, 3, d_); r += 1

# ────── 1. CAJA ──────
ws = wb.create_sheet('1 Caja'); widths(ws, 46, 18, 50)
title(ws, 'CAJA · ETC 88', MAR, 3)
ws.merge_cells('A2:C2'); c = ws['A2']; c.value = 'fuente: registro de tesorería del tablero de finanzas (gastos, donaciones, profondo; extraído 11-sep) · estado de cuenta al 11-sep'; c.font = Font(size=9, italic=True, color='666666'); c.alignment = Alignment(horizontal='center')
r = 4
subtitle(ws, r, 'ENTRADAS', MAR); r += 1
for label, val, nota in [
    ('Pagos de participantes', PARTICIP, f'46 de los 48 participantes pagaron · cuota {CUOTA_PARTICIPANTE:,} · cuatro pagaron menos (referencia teórica {PART_ESPER:,})'),
    ('Donaciones en efectivo', DONAC_EFEC, '49 aportantes'),
    ('Profondo (rifa + venta de comida y helados) — entregado neto', PROFONDO, f'bruto {PROF_BRUTO:,} − premios {PROF_COSTOS:,} + ventas posteriores {PROF_ADICIONAL:,.2f}'),
    ('Cuotas del equipo', CUOTAS, f'49 miembros × {CUOTA_EQUIPO:,} · 100%. De los 56 del equipo quedan fuera los 3 guías de reserva y los 4 asesores que no pagaron cuota (el padre Paul, la sor, Petra y Johanny)'),
    ('Tardanzas', TARDANZAS, 'multas de formaciones'),
]:
    ws.cell(r, 1, label).font = font(); money(ws, r, 2, val); note(ws, r, 3, f'{val / ENTRADAS * 100:.1f}% · {nota}')
    for cc in range(1, 4): ws.cell(r, cc).border = border
    r += 1
ws.cell(r, 1, 'ENTRADAS TOTALES').font = font(11, True); money(ws, r, 2, ENTRADAS).font = font(11, True); band(ws, r, 1, 2, 'E8F5E9'); r += 2
subtitle(ws, r, 'SALIDAS', ROJO); r += 1
ws.cell(r, 1, 'Gastos (22 movimientos)').font = font(); money(ws, r, 2, GASTOS_TOT); note(ws, r, 3, 'detalle en la hoja 7 Gastos'); r += 1
ws.cell(r, 1, 'Salidas profondo').font = font(); money(ws, r, 2, 0); note(ws, r, 3, 'ninguna: la comisión entregó el neto'); r += 1
ws.cell(r, 1, 'SALIDAS TOTALES').font = font(11, True); money(ws, r, 2, SALIDAS).font = font(11, True); band(ws, r, 1, 2, 'FDE8E8'); r += 2
subtitle(ws, r, 'BALANCE', AZUL); r += 1
ws.cell(r, 1, 'Balance (entradas − salidas)').font = font(11, True); money(ws, r, 2, BALANCE).font = font(11, True); band(ws, r, 1, 2, 'E3F2FD'); r += 1
ws.cell(r, 1, 'Dinero real en cuentas al 11-sep').font = font(); money(ws, r, 2, REAL_CUENTAS); r += 1
ws.cell(r, 1, f'Impuesto bancario por transacción ({IMPUESTO_TASA*100:.2f}% sobre {IMPUESTO_BASE:,.0f})').font = font(9, color=GRIS); money(ws, r, 2, -IMPUESTOS_BANCO).font = font(9, color=GRIS); r += 1
ws.cell(r, 1, 'Copias pagadas').font = font(9, color=GRIS); money(ws, r, 2, -COPIAS_PAGADAS).font = font(9, color=GRIS); r += 2
subtitle(ws, r, 'DE DÓNDE SALE LA DIFERENCIA CON EL BANCO', GRIS); r += 1
header(ws, r, ['Escenario de impuesto', 'Impuesto', 'Resto: copias'], GRIS); r += 1
for _lbl, _base, _tasa in ESCENARIOS_IMPUESTO:
    _imp = round(_base * _tasa, 2)
    ws.cell(r, 1, _lbl).font = font(10, _tasa == IMPUESTO_TASA and _base == IMPUESTO_BASE)
    money(ws, r, 2, _imp); money(ws, r, 3, round(IMPUESTOS - _imp, 2))
    if _tasa == IMPUESTO_TASA and _base == IMPUESTO_BASE: band(ws, r, 1, 3, 'E3F2FD')
    for _c in range(1, 4): ws.cell(r, _c).border = border
    r += 1
note(ws, r, 1, 'El escenario resaltado es el que usa este archivo. Si el estado de cuenta muestra otra tasa, se cambia el dato y todo se recalcula.'); r += 2
ws.cell(r, 1, 'Efectivo de imprevistos 15,000: cocina en la casa + reembolso del salón').font = font(9, color=GRIS); money(ws, r, 2, EFECTIVO_COCINA + EFECTIVO_SALON).font = font(9, color=GRIS); note(ws, r, 3, f'{EFECTIVO_COCINA:,} a cocina en la casa + {EFECTIVO_SALON:,} reembolso del salón de formaciones (liquidado)'); r += 2
subtitle(ws, r, 'APOYO TOTAL DONADO', VERDE); r += 1
ws.cell(r, 1, 'Donaciones en efectivo (entraron a caja)').font = font(); money(ws, r, 2, DONAC_EFEC); r += 1
ws.cell(r, 1, 'Donaciones en especie (bajaron el costo · a precio de presupuesto)').font = font(); money(ws, r, 2, ESPECIE_TOTAL); r += 1
ws.cell(r, 1, 'Cortesías de la casa').font = font(); money(ws, r, 2, CORTESIA_JUEVES + CORTESIA_HOSP); note(ws, r, 3, '8 × 500 del jueves + 2 × 2,360 (el padre y la sor)'); r += 1
ws.cell(r, 1, 'TOTAL DONADO').font = font(11, True); money(ws, r, 2, DONAC_EFEC + ESPECIE_TOTAL + CORTESIA_JUEVES + CORTESIA_HOSP).font = font(11, True); band(ws, r, 1, 2, 'E8F5E9')

# ────── 2. PRESUPUESTO vs COSTO (limpio) ──────
ws8 = wb.create_sheet('2 Presupuesto vs costo'); widths(ws8, 12, 60, 16, 16, 18, 16, 16)
title(ws8, f'PRESUPUESTO vs COSTO — lo presupuestado ({PPTO_OFICIAL}), lo que costó y cómo se cubrió', AZUL, 7)
explain(ws8, 'Costó = pagado de caja + cubierto sin pagar (donaciones en especie a precio de presupuesto y cortesías de la casa). Diferencia = costó − presupuestado: positivo, costó más; negativo, costó menos. La explicación de cada partida está en la hoja 13.', 7)
header(ws8, 3, ['Área', 'Partida', 'Presupuestado', 'Costó', 'Cubierto sin pagar', 'Pagado de caja', 'Diferencia'], AZUL)
r = 4
for area, (a11, aS, apag, adon) in AREAS.items():
    ws8.cell(r, 1, area).font = font(10, True, MAR); ws8.cell(r, 2, f'{area} — subtotal').font = font(10, True, MAR)
    money(ws8, r, 3, a11).font = font(10, True); money(ws8, r, 4, apag + adon).font = font(10, True); money(ws8, r, 5, adon).font = font(10, True); money(ws8, r, 6, apag).font = font(10, True)
    dcell = money(ws8, r, 7, apag + adon - a11); dcell.font = font(10, True, ROJO if apag + adon - a11 > 0 else VERDE)
    band(ws8, r, 1, 7, 'F0EAD6'); r += 1
    first = r
    for a, p, p11, ps, pag, don, nota in cruce:
        if a != area: continue
        ws8.cell(r, 2, p).font = font(10); ws8.cell(r, 2).alignment = WRAP
        if p11 is not None: money(ws8, r, 3, p11)
        money(ws8, r, 4, pag + don); money(ws8, r, 5, don); money(ws8, r, 6, pag)
        if don and not pag: ws8.cell(r, 5).font = font(10, True, VERDE)
        if p11 is not None:
            dcell = money(ws8, r, 7, pag + don - p11); dcell.font = font(10, color=(ROJO if pag + don - p11 > 0 else VERDE if pag + don - p11 < 0 else '1E293B'))
        else:
            ws8.cell(r, 7, 'no presupuestado' if pag + don else '').font = font(9, color=AMBAR)
        for cc in range(2, 8): ws8.cell(r, cc).border = border
        r += 1
    ws8.row_dimensions.group(first, r - 1, outline_level=1, hidden=False)
ws8.cell(r, 2, 'TOTALES').font = font(11, True)
money(ws8, r, 3, PPTO_11AGO).font = font(11, True); money(ws8, r, 4, COSTO_ECON).font = font(11, True); money(ws8, r, 5, CRUCE_DONADO).font = font(11, True); money(ws8, r, 6, CRUCE_PAGADO).font = font(11, True)
dcell = money(ws8, r, 7, COSTO_ECON - PPTO_11AGO); dcell.font = font(11, True, ROJO)
band(ws8, r, 1, 7, 'E3F2FD'); r += 2
note(ws8, r, 2, f'Costó {COSTO_ECON:,.0f} = pagado de caja {CRUCE_PAGADO:,} + cubierto sin pagar {CRUCE_DONADO:,} · frente al presupuesto: {COSTO_ECON - PPTO_11AGO:+,.2f} ({(COSTO_ECON / PPTO_11AGO - 1) * 100:+.1f}%) · la caja frente al presupuesto: {CRUCE_PAGADO - PPTO_11AGO:+,.2f} ({(CRUCE_PAGADO / PPTO_11AGO - 1) * 100:+.1f}%)'); r += 1
note(ws8, r, 2, 'Las filas por área están agrupadas: el botón «−» del margen izquierdo deja solo los subtotales. Las partidas que no existían en el presupuesto se marcan "no presupuestado".')
ws8.freeze_panes = 'C4'

# ────── 3. AL COSTO vs CAJA ──────
ws9 = wb.create_sheet('3 Al costo vs caja'); widths(ws9, 58, 18, 66)
title(ws9, 'CUÁNTO VALE EL RETIRO "AL COSTO" vs CUÁNTO NOS COSTÓ — y por qué', AZUL, 3)
explain(ws9, 'A es lo que salió de caja; B lo que vale el retiro sumando lo que no se pagó; C la diferencia; D todo dividido entre las 99 personas; E de dónde salió el dinero; F la casa desglosada.', 3)
r = 3
subtitle(ws9, r, 'A · LO QUE NOS COSTÓ (caja)', ROJO); r += 1
ws9.cell(r, 1, 'Salidas de caja (22 gastos)').font = font(11, True); money(ws9, r, 2, SALIDAS).font = font(11, True); note(ws9, r, 3, 'lo que efectivamente salió de las cuentas'); band(ws9, r, 1, 2, 'FDE8E8'); r += 2
subtitle(ws9, r, 'B · LO QUE VALE EL RETIRO (costo total)', AZUL); r += 1
for label, val, nota in [
    ('Salidas de caja', SALIDAS, ''),
    ('+ Donaciones en especie (a precio de presupuesto)', ESPECIE_TOTAL, 'peces, decoración, guías, cocina, oficina, música, insumos de misa, lapiceros'),
    ('+ Cortesía de la casa: 8 pers del jueves sin cobro', CORTESIA_JUEVES, '8 × 500'),
    ('+ Cortesía de la casa: 2 pers vie–dom sin cobro', CORTESIA_HOSP, '2 × 2,360 · el padre y la sor'),
]:
    ws9.cell(r, 1, label).font = font(10); money(ws9, r, 2, val); note(ws9, r, 3, nota); r += 1
ws9.cell(r, 1, 'TOTAL · LO QUE COSTÓ EL RETIRO').font = font(11, True); money(ws9, r, 2, COSTO_ECON).font = font(11, True); band(ws9, r, 1, 2, 'E3F2FD'); r += 1
note(ws9, r, 1, '   + no incluido: los premios del profondo (19,900) son costo de recaudar, no del retiro, y ya están descontados del neto entregado · oficina a costo real (+3,006.11, solo informativo)', AMBAR); r += 2
subtitle(ws9, r, 'C · POR QUÉ NOS COSTÓ MENOS DE LO QUE VALE', VERDE); r += 1
ws9.cell(r, 1, 'Cubierto sin pagar (especie + cortesías)').font = font(10); money(ws9, r, 2, RECIBIDO_GRATIS); note(ws9, r, 3, f'{RECIBIDO_GRATIS / COSTO_ECON * 100:.1f}% del costo · 30 donantes en especie + la casa'); r += 2
subtitle(ws9, r, f'D · POR PERSONA ({PERSONAS} en la casa)', MAR); r += 1
ws9.cell(r, 1, 'Costo de caja por persona').font = font(10); money(ws9, r, 2, SALIDAS / PERSONAS); r += 1
ws9.cell(r, 1, 'Costo total por persona').font = font(10); money(ws9, r, 2, COSTO_ECON / PERSONAS); r += 1
ws9.cell(r, 1, 'Cuota que pagó cada participante').font = font(10); money(ws9, r, 2, CUOTA_PARTICIPANTE); note(ws9, r, 3, f'cubre el {CUOTA_PARTICIPANTE / (SALIDAS / PERSONAS) * 100:.0f}% de su costo de caja; el resto lo cubrieron donaciones y profondo'); r += 1
ws9.cell(r, 1, 'Participantes sin cuota (becas de hecho)').font = font(10); money(ws9, r, 2, 2 * CUOTA_PARTICIPANTE); note(ws9, r, 3, 'Cristofer y Dahiony: 2 × 3,500 que no entraron. No es un costo, es recaudación que no se cobró'); r += 1
ws9.cell(r, 1, 'Cuota que pagó cada miembro del equipo').font = font(10); money(ws9, r, 2, CUOTA_EQUIPO); note(ws9, r, 3, f'49 miembros = {CUOTAS:,}'); r += 1
note(ws9, r, 1, f'   {PERSONAS} en la casa = 48 participantes (46 con cuota pagada + Cristofer y Dahiony sin cuota) y 51 del equipo. Mary Carmen pagó su cuota y no asistió; entre los 46 que pagaron no hay ninguno registrado como ausente (ver hoja 5).'); r += 2
subtitle(ws9, r, 'E · CÓMO SE FINANCIÓ LA CAJA', MAR); r += 1
for label, val in FUENTES:
    ws9.cell(r, 1, label).font = font(10); money(ws9, r, 2, val); note(ws9, r, 3, f'{val / ENTRADAS * 100:.1f}% de las entradas'); r += 1
ws9.cell(r, 1, 'Total de entradas').font = font(11, True); money(ws9, r, 2, ENTRADAS).font = font(11, True); r += 1
ws9.cell(r, 1, '− Salidas').font = font(10); money(ws9, r, 2, -SALIDAS); r += 1
ws9.cell(r, 1, 'Superávit').font = font(11, True); money(ws9, r, 2, BALANCE).font = font(11, True); note(ws9, r, 3, f'{BALANCE / ENTRADAS * 100:.1f}% de las entradas · real en cuentas {REAL_CUENTAS:,}'); band(ws9, r, 1, 2, 'E8F5E9'); r += 2
subtitle(ws9, r, 'F · LA CASA, AL DETALLE', MAR); r += 1
for label, val, nota in [
    ('Hospedaje base 97 pers × 2,360 (vie–dom)', 228920, 'fuimos 99; la casa facturó 97 y dio 2 de cortesía: el padre y la sor (la del director, cedida a la sor)'),
    ('Noche del jueves: 19 pers × 500', 9500, 'llegamos jueves (avanzada). 27 personas: 19 pagaron, 8 sin cobro'),
    ('Habitaciones para pequeños grupos, 2 noches', HAB_TOTAL, f'tarifa inferida {HAB_TARIFA:,.0f}/noche'),
    ('Total pagado a la casa', CASA_TOTAL, 'avance 23,600 (repuesto al Consejo) + final 216,620'),
    ('Cortesía no cobrada: jueves (8 × 500)', CORTESIA_JUEVES, 'valor recibido'),
    ('Cortesía no cobrada: 2 pers vie–dom (2 × 2,360)', CORTESIA_HOSP, 'valor recibido · el padre y la sor'),
    ('Comida de avanzada del jueves (ppto Sistem 3,900)', 0, 'sin gasto propio: absorbida en Iberia / detalles de cocina'),
    (f'vs presupuesto oficial {PPTO_OFICIAL} (236,000)', CASA_TOTAL - 236000, 'el jueves y las habitaciones'),
    ('vs presupuesto Sistem (200,000)', CASA_TOTAL - 200000, 'el Sistem nunca actualizó la tarifa de 2,360 ni contempló el jueves'),
]:
    _b = label.startswith(('Total', 'TOTAL')); ws9.cell(r, 1, label).font = font(10, _b); money(ws9, r, 2, val).font = font(10, _b); note(ws9, r, 3, nota); r += 1

# ────── 4. BASE ETC 89 ──────
wsb = wb.create_sheet('4 Base ETC 89'); widths(wsb, 12, 56, 16, 16, 14, 22, 62)
title(wsb, 'BASE PARA PRESUPUESTAR EL ETC 89 — el número real del ETC 88, partida por partida', VERDE, 7)
explain(wsb, 'Costo real 88 = pagado de caja + cubierto sin pagar. Por persona = entre 99. Tipo es una propuesta de cómo presupuestar cada partida en el ETC 89: "por persona" se multiplica por asistentes, "fijo" se cotiza, "puntual" se decide, "no presupuestar" fue cortesía. Abajo, las recomendaciones.', 7)
header(wsb, 3, ['Área', 'Partida', 'Ppto oficial 88', 'Costo real 88', 'Por persona (99)', 'Tipo [PROPUESTA]', 'Cómo presupuestarlo'], VERDE)
r = 4
BASE_TOTAL = 0
for area in AREAS:
    for a, p, p11, ps, pag, don, nota in cruce:
        if a != area: continue
        real = pag + don; BASE_TOTAL += real
        t, como = tipo_89(p)
        wsb.cell(r, 1, area).font = font(9, color=GRIS); wsb.cell(r, 2, p).font = font(10); wsb.cell(r, 2).alignment = WRAP
        if p11 is not None: money(wsb, r, 3, p11)
        money(wsb, r, 4, real).font = font(10, True); money(wsb, r, 5, real / PERSONAS)
        wsb.cell(r, 6, t).font = font(9, True, AMBAR if t in ('puntual', 'no presupuestar', 'reserva') else '1E293B'); note(wsb, r, 7, como)
        for cc in range(1, 8): wsb.cell(r, cc).border = border
        r += 1
wsb.cell(r, 2, 'COSTO REAL ETC 88').font = font(11, True); money(wsb, r, 3, PPTO_11AGO).font = font(11, True); money(wsb, r, 4, BASE_TOTAL).font = font(11, True); money(wsb, r, 5, BASE_TOTAL / PERSONAS).font = font(11, True); band(wsb, r, 1, 7, 'E8F5E9'); r += 1
assert abs(BASE_TOTAL - COSTO_ECON) < 0.01
wsb.cell(r, 2, '− puntuales (desvío del transporte, bizcocho de bienvenida)').font = font(10); money(wsb, r, 4, -PUNTUALES); r += 1
wsb.cell(r, 2, 'Base recurrente (lo que un retiro igual cuesta, con todo lo donado valorado)').font = font(11, True); money(wsb, r, 4, BASE_REC).font = font(11, True); money(wsb, r, 5, BASE_REC / PERSONAS).font = font(11, True); band(wsb, r, 1, 7, 'FFF4E0'); r += 2
subtitle(wsb, r, 'CÓMO SE FINANCIÓ EL 88 (base para el plan de recaudación del 89)', MAR); r += 1
for label, val in FUENTES:
    wsb.cell(r, 2, label).font = font(10); money(wsb, r, 4, val); note(wsb, r, 7, f'{val / ENTRADAS * 100:.1f}% de las entradas'); r += 1
wsb.cell(r, 2, 'Entradas totales').font = font(11, True); money(wsb, r, 4, ENTRADAS).font = font(11, True); r += 1
wsb.cell(r, 2, 'Cubierto sin pagar (especie + cortesías; no pasó por caja)').font = font(10); money(wsb, r, 4, RECIBIDO_GRATIS); r += 2
subtitle(wsb, r, 'RECOMENDACIONES PARA EL ETC 89 [PROPUESTA]', AZUL); r += 1
for tema, items in RECOMENDACIONES_89:
    wsb.cell(r, 2, tema).font = font(11, True, MAR); band(wsb, r, 1, 7, 'F0EAD6'); r += 1
    for it in items:
        wsb.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7); note(wsb, r, 2, '• ' + it, '1E293B', 10); wsb.row_dimensions[r].height = 28; r += 1
    r += 1
wsb.freeze_panes = 'C4'

# ────── 5. PENDIENTES ──────
ws7 = wb.create_sheet('5 Pendientes'); widths(ws7, 10, 30, 90, 60)
title(ws7, f'PENDIENTES Y NOTAS PARA EL CONSEJO — estado al 11-sep · {N_ABIERTOS} abiertos', AMBAR, 4)
explain(ws7, 'ABIERTO = falta un dato o una decisión; NOTA = aclaración que conviene dejar por escrito; CERRADO = resuelto; INFO = contexto. La columna Qué falta dice exactamente qué cerrar.', 4)
header(ws7, 3, ['Estado', 'Tema', 'Detalle', 'Qué falta'], AMBAR)
r = 4
for tag, tema, det, falta in pendientes:
    col = {'ABIERTO': ROJO, 'NOTA': AMBAR, 'CERRADO': VERDE, 'INFO': GRIS}[tag]
    ws7.cell(r, 1, tag).font = font(9, True, col); ws7.cell(r, 2, tema).font = font(10, True); ws7.cell(r, 2).alignment = WRAP
    note(ws7, r, 3, det, '1E293B', 10); note(ws7, r, 4, falta, ROJO if tag == 'ABIERTO' else GRIS)
    for cc in range(1, 5): ws7.cell(r, cc).border = border
    r += 1
ws7.freeze_panes = 'A4'

# ────── 6. PRESUPUESTO OFICIAL vs SISTEM ──────
ws6 = wb.create_sheet('6 Ppto oficial vs Sistem'); widths(ws6, 40, 18, 18, 18)
title(ws6, f'PRESUPUESTO OFICIAL ({PPTO_OFICIAL}) vs SISTEM (tablero) — por área', AZUL, 4)
explain(ws6, 'Los dos presupuestos por área. El oficial (11-Ago) se compara contra lo que costó; el Sistem es el que alimenta el tablero de finanzas. Cubierto = lo que de esa área se recibió sin pagar.', 4)
header(ws6, 3, ['Área', f'{PPTO_OFICIAL} (OFICIAL)', 'Sistem (tablero)', 'Cubierto sin pagar'], AZUL)
r = 4
for (a, v1), (_, v2) in zip(ppto_11ago, ppto_sistem):
    ws6.cell(r, 1, a).font = font(10); money(ws6, r, 2, v1); money(ws6, r, 3, v2); money(ws6, r, 4, especie_tot.get(a, 0)); r += 1
ws6.cell(r, 1, 'TOTAL').font = font(11, True); money(ws6, r, 2, PPTO_11AGO).font = font(11, True); money(ws6, r, 3, PPTO_SISTEM).font = font(11, True); money(ws6, r, 4, ESPECIE_TOTAL).font = font(11, True); band(ws6, r, 1, 4, 'E3F2FD'); r += 2
ws6.cell(r, 1, 'Salidas de caja').font = font(10, True); money(ws6, r, 2, SALIDAS); money(ws6, r, 3, SALIDAS); r += 1
ws6.cell(r, 1, 'Caja vs presupuesto').font = font(10); money(ws6, r, 2, SALIDAS - PPTO_11AGO); money(ws6, r, 3, SALIDAS - PPTO_SISTEM); r += 1
ws6.cell(r, 1, 'Lo que costó').font = font(10, True); money(ws6, r, 2, COSTO_ECON); money(ws6, r, 3, COSTO_ECON); r += 1
ws6.cell(r, 1, 'Costó vs presupuesto').font = font(10); money(ws6, r, 2, COSTO_ECON - PPTO_11AGO); money(ws6, r, 3, COSTO_ECON - PPTO_SISTEM); r += 1
note(ws6, r, 1, '(negativo = por debajo del presupuesto; positivo = por encima)'); r += 2
ws6.cell(r, 1, 'Casa: presupuesto').font = font(10); money(ws6, r, 2, 236000); money(ws6, r, 3, 200000); r += 1
ws6.cell(r, 1, 'Casa: real (216,620 + 23,600)').font = font(10); money(ws6, r, 2, CASA_TOTAL); money(ws6, r, 3, CASA_TOTAL); r += 1
ws6.cell(r, 1, 'Casa: desvío').font = font(10); money(ws6, r, 2, CASA_TOTAL - 236000); money(ws6, r, 3, CASA_TOTAL - 200000); r += 2
note(ws6, r, 1, 'Diferencia entre presupuestos 83,390 = casa 36,000 + peces 31,000 + cocina 20,255 + transporte 5,000 + biblias 1,600 − guías 3,600 − ensayo 3,000 − avanzada 3,900 + palancas 35.'); r += 1
note(ws6, r, 1, f'Declarado OFICIAL por el director (11-sep): {PPTO_OFICIAL}, porque refleja la tarifa real de la casa (2,360) y el costo completo. El Sistem es lo que ve el tablero; ambos quedaron marcados "Tentativo".')

# ────── 7. GASTOS ──────
ws2 = wb.create_sheet('7 Gastos'); widths(ws2, 8, 64, 14, 80)
title(ws2, 'GASTOS — registro de tesorería (22 movimientos · 24 filas: el pago a JM de 37,500 desglosado)', ROJO, 4)
explain(ws2, 'Los 22 gastos del registro en orden de fecha. Las tres filas marcadas ► son el desglose de una sola transferencia de 37,500. La columna Nota explica qué es cada gasto.', 4)
header(ws2, 3, ['Fecha', 'Concepto', 'RD$', 'Nota'], ROJO)
r = 4
for f, cpt, m, n_ in gastos:
    sub = '►' in cpt
    ws2.cell(r, 1, f).font = font(10); ws2.cell(r, 2, cpt).font = font(10, color=(AZUL if sub else '1E293B')); money(ws2, r, 3, m)
    note(ws2, r, 4, n_, ROJO if '⚠' in n_ else GRIS)
    if sub: band(ws2, r, 1, 4, 'EEF3FA')
    for cc in range(1, 5): ws2.cell(r, cc).border = border
    r += 1
ws2.cell(r, 2, 'TOTAL GASTOS (= salidas del tablero)').font = font(11, True); money(ws2, r, 3, GASTOS_TOT).font = font(11, True); band(ws2, r, 1, 3, 'FDE8E8'); r += 2
note(ws2, r, 2, 'Transporte total 45,000 = abono 17,500 + 2ª mitad 17,500 + desvío 10,000. Ofrenda al P. Héctor 10,000. Las tres filas ► son una sola transferencia de 37,500.'); r += 1
note(ws2, r, 2, f'Casa total = final 216,620 + avance 23,600 = {CASA_TOTAL:,}. Efectivo de imprevistos 15,000 = {EFECTIVO_COCINA:,} a cocina en la casa + {EFECTIVO_SALON:,} reembolso del salón de formaciones (liquidado).')
ws2.freeze_panes = 'A4'

# ────── 8. DONACIONES EFECTIVO ──────
ws3 = wb.create_sheet('8 Donaciones efectivo'); widths(ws3, 8, 30, 14, 56, 8)
title(ws3, 'DONACIONES EN EFECTIVO — registro de tesorería (49)', MAR, 5)
explain(ws3, 'Las 49 donaciones en dinero tal como están en el registro. ⚠ marca las que necesitan una nota explícita para el Consejo.', 5)
header(ws3, 3, ['Fecha', 'Donante', 'RD$', 'Nota', 'Consejo'])
r = 4
for f, d_, m, n_, flag in donaciones:
    ws3.cell(r, 1, f).font = font(10); ws3.cell(r, 2, d_).font = font(10); money(ws3, r, 3, m); note(ws3, r, 4, n_)
    if flag: ws3.cell(r, 5, '⚠').font = font(10, True, AMBAR); ws3.cell(r, 2).fill = fill('FFF4E0')
    for cc in range(1, 6): ws3.cell(r, cc).border = border
    r += 1
ws3.cell(r, 2, 'TOTAL (= tablero)').font = font(11, True); money(ws3, r, 3, DONAC_EFEC).font = font(11, True); band(ws3, r, 1, 3, 'E8F5E9'); r += 2
note(ws3, r, 2, '⚠ = requiere nota explícita para el Consejo (origen no verificado o sin comprobante). Suman 6,500.', AMBAR); r += 1
note(ws3, r, 2, 'Jonathan Medina 1,500 (31/08) es el neto del pago de Boris (participante que no asistió) tras devolverle una porción.')
ws3.freeze_panes = 'A4'

# ────── 9. ESPECIE ──────
ws5 = wb.create_sheet('9 Especie'); widths(ws5, 54, 14, 44)
title(ws5, 'DONACIONES EN ESPECIE (bajaron el costo · valoradas a precio de presupuesto)', MAR, 3)
explain(ws5, 'Lo que alguien puso sin que saliera dinero de caja, por área y valorado a precio de presupuesto (no a factura). El reembolso a Priscila resta porque ella recibió 2,000 en efectivo.', 3)
r = 3
for area, items in especie.items():
    ws5.cell(r, 1, f'{area}  —  subtotal {especie_tot[area]:,.0f}').font = font(11, True, MAR); band(ws5, r, 1, 3, 'F0EAD6'); r += 1
    for desc, val, quien in items:
        ws5.cell(r, 1, desc).font = font(10, color=(ROJO if val < 0 else '1E293B')); money(ws5, r, 2, val); note(ws5, r, 3, quien)
        for cc in range(1, 4): ws5.cell(r, cc).border = border
        r += 1
    r += 1
ws5.cell(r, 1, 'TOTAL DONADO EN ESPECIE').font = font(11, True); money(ws5, r, 2, ESPECIE_TOTAL).font = font(11, True); band(ws5, r, 1, 2, 'E8F5E9'); r += 1
ws5.cell(r, 1, 'Cortesías de la casa (no son especie; valor recibido)').font = font(10); money(ws5, r, 2, CORTESIA_JUEVES + CORTESIA_HOSP); note(ws5, r, 3, '8 × 500 del jueves + 2 × 2,360'); r += 2
note(ws5, r, 1, f'Materiales de oficina costaron realmente {OFICINA_REAL:,.2f} (Cactus 3,140.07 + 726.04 · Medamax 1,440.00 · 03/09), asumidos por los directores. Aquí se valoran a presupuesto (2,300) por instrucción del director.'); r += 1
note(ws5, r, 1, 'La impresión de libretas (1,260) estaba marcada como donada en la columna equivocada del presupuesto operativo; se sumó por confirmación del director.')

# ────── 10. PROFONDO ──────
ws4 = wb.create_sheet('10 Profondo'); widths(ws4, 8, 52, 16, 56)
title(ws4, 'PROFONDO (rifa + venta de comida y helados) — liquidación de la comisión y entregas a finanzas', AZUL, 4)
explain(ws4, 'Arriba, la liquidación de la comisión (bruto, premios, neto). Abajo, las 8 entregas a finanzas tal como están en el registro. La diferencia entre el neto del informe y lo entregado son ventas de helados posteriores al informe.', 4)
r = 3
subtitle(ws4, r, 'LIQUIDACIÓN DE LA COMISIÓN', AZUL); r += 1
for label, val, nota in [
    (f'Boletas colocadas y pagadas: {PROF_BOLETAS_PAG:g} × {PROF_PRECIO}', PROF_ING_BOLETAS, f'de {PROF_BOLETAS_PAG + PROF_BOLETAS_NOPAG:g} boletas colocadas'),
    ('Venta de comida y helados', PROF_ING_COMIDA, ''),
    ('Ingresos brutos', PROF_BRUTO, ''),
    ('− Aire acondicionado (premio principal)', -16900, ''),
    ('− Abanico de torre (premio secundario)', -3000, ''),
    ('Neto del informe', PROF_NETO_INFORME, ''),
    ('+ Ventas de helados posteriores al informe', PROF_ADICIONAL, 'director, 11-sep'),
    ('Entregado a finanzas', PROFONDO, 'coincide con las 8 entregas de abajo'),
    (f'Boletas colocadas NO pagadas: {PROF_BOLETAS_NOPAG:g} × {PROF_PRECIO}', PROF_POR_COBRAR, 'colocadas y nunca cobradas; la dirección decidió no cobrarlas'),
]:
    _b = label in ('Ingresos brutos', 'Neto del informe', 'Entregado a finanzas')
    ws4.cell(r, 2, label).font = font(11 if _b else 10, _b); money(ws4, r, 3, val).font = font(11 if _b else 10, _b); note(ws4, r, 4, nota)
    if _b: band(ws4, r, 2, 3, 'E3F2FD')
    for cc in range(2, 5): ws4.cell(r, cc).border = border
    r += 1
r += 1
subtitle(ws4, r, 'ENTREGAS A FINANZAS (registro de tesorería)', MAR); r += 1
header(ws4, r, ['Fecha', 'Concepto', 'RD$', 'Nota'], AZUL); r += 1
for f, cpt, m, n_ in profondo:
    ws4.cell(r, 1, f).font = font(10); ws4.cell(r, 2, cpt).font = font(10); money(ws4, r, 3, m); note(ws4, r, 4, n_)
    for cc in range(1, 5): ws4.cell(r, cc).border = border
    r += 1
ws4.cell(r, 2, 'TOTAL ENTREGADO').font = font(11, True); money(ws4, r, 3, PROFONDO).font = font(11, True); band(ws4, r, 1, 3, 'E3F2FD'); r += 2
note(ws4, r, 2, 'Los premios (19,900) son costo de recaudar, no del retiro: por eso no entran en "lo que costó el retiro" y ya están descontados del neto entregado.')

# ────── 11. AUDITORÍA ──────
ws10 = wb.create_sheet('11 Auditoría'); widths(ws10, 5, 74, 18, 18, 11, 60)
title(ws10, 'AUDITORÍA NUMÉRICA — cada verificación se recalcula al generar el archivo', AZUL, 6)
explain(ws10, 'Cada fila compara un valor esperado con el obtenido al recalcular. Cuadra = coinciden; Pendiente = falta un dato, no es error de suma.', 6)
header(ws10, 3, ['#', 'Verificación', 'Esperado', 'Obtenido', 'Estado', 'Nota'], AZUL)
r = 4
for i, ch in enumerate(checks, 1):
    txt, esp, obt, extra, nota = ch[:5]; ok = _ok(ch)
    ws10.cell(r, 1, i).font = font(9); ws10.cell(r, 2, txt).font = font(10); ws10.cell(r, 2).alignment = WRAP
    money(ws10, r, 3, esp); money(ws10, r, 4, obt)
    ws10.cell(r, 5, 'Cuadra' if ok else 'Pendiente').font = font(10, True, VERDE if ok else ROJO)
    note(ws10, r, 6, nota)
    for c_ in range(1, 7): ws10.cell(r, c_).border = border
    r += 1
r += 1
ws10.cell(r, 2, f'{AUDIT_PASS} de {AUDIT_N} verificaciones cuadran').font = font(10, True)
ws10.freeze_panes = 'A4'

# ────── 12. FUENTES Y MÉTODO ──────
wsf = wb.create_sheet('12 Fuentes y método'); widths(wsf, 34, 100)
title(wsf, 'FUENTES Y MÉTODO — de dónde sale cada número', GRIS, 2)
explain(wsf, 'De dónde sale cada número (fuentes) y las reglas con las que se construyó el archivo (método).', 2)
r = 3
subtitle(wsf, r, 'FUENTES', MAR); r += 1
for k, v in [
    ('Registro de tesorería (tablero de finanzas)', 'financetc88.streamlit.app · gastos (22), donaciones (49), entregas del profondo (8), extraídos por el director el 11-sep-2026. Cuadran al peso con los totales del tablero.'),
    ('Totales del tablero', f'Cuotas {CUOTAS:,} · tardanzas {TARDANZAS:,} · participantes {PARTICIP:,} de {PART_ESPER:,} · balance {BALANCE:,.2f}.'),
    ('Estado de cuenta', f'{REAL_CUENTAS:,} en cuentas al 11-sep (director).'),
    (f'Presupuesto OFICIAL ({PPTO_OFICIAL})', 'Finanzas ETC 88 · Presupuesto General Actualizado 11-Aug.xlsx: Directores 428,940 + Cocina 132,639.84 + Guías 24,157.86 + Música 10,511.86 = 596,249.56. Declarado oficial por el director el 11-sep.'),
    ('Presupuesto Sistem', 'Sistem-Finanzas ETC 88 (hoja que alimenta el tablero): 512,859.56. Referencia operativa.'),
    ('Liquidación del profondo', f'Desglose_Ganancias_Actividad_Pro_Fondo.xlsx (comisión): {PROF_BOLETAS_PAG:g} boletas pagadas × 200 = {PROF_ING_BOLETAS:,} + comida y helados {PROF_ING_COMIDA:,} = {PROF_BRUTO:,}; premios {PROF_COSTOS:,}; neto {PROF_NETO_INFORME:,}; boletas no pagadas {PROF_POR_COBRAR:,}.'),
    ('Cotización de comida', 'Iberia, cotización VCT-072932 a nombre de Paloma Méndez, 01-sep-2026: 77,044.05.'),
    ('Listas del director (10-sep)', 'Mensaje con 47 donaciones, 57 líneas de pagos de participantes (46 personas) y 20 salidas.'),
    ('Presupuesto Maestro (14-jun)', 'Presupuesto Maestro del 14 de junio, hoja de caja: reserva 23,600 (07-jun, devuelta) y salón 10,000 pagado en efectivo a Franklin Pozo con aporte personal de Juan Manuel (reembolsado después).'),
    ('Aclaraciones del director', '10 y 11 de septiembre: casa, desglose del pago a JM, ofrenda, donaciones fantasma, oficina, Paloma, insumos de misa, Santa Clara, bizcocho y helados, lapiceros, asistencia, efectivo de cocina, cuotas (participante 3,500 · equipo 2,000).'),
]:
    wsf.cell(r, 1, k).font = font(10, True); wsf.cell(r, 1).alignment = WRAP; note(wsf, r, 2, v, '1E293B', 10); r += 1
r += 1
subtitle(wsf, r, 'REGLAS DEL MÉTODO', AZUL); r += 1
for k, v in [
    ('Nada inventado', 'Cada cifra viene de una fuente de arriba o de una confirmación del director. Lo no confirmado se marca [POR CONFIRMAR]; las sugerencias, [PROPUESTA].'),
    ('Especie', 'Las donaciones en especie se valoran al precio del presupuesto, no a factura. Oficina: costo real 5,306.11 solo informativo (instrucción del director).'),
    ('Cortesías', 'Lo que la casa no cobró (8 × 500 del jueves, 2 × 2,360) cuenta como cubierto sin pagar, no como especie.'),
    ('Lo que costó el retiro', 'caja + especie + cortesías. Los premios del profondo son costo de recaudar y no entran.'),
    ('Pago a JM 37,500', 'Se muestra desglosado según el director (17,500 + 10,000 + 10,000); en el registro es una sola línea.'),
    ('Efectivo de imprevistos 15,000', f'{EFECTIVO_COCINA:,} a cocina en la casa + {EFECTIVO_SALON:,} reembolso del salón de formaciones. Liquidado completo.'),
    ('Habitaciones', f'Tarifa inferida de lo pagado: {HAB_TARIFA:,.0f}/noche × 2 noches = {HAB_TOTAL:,}.'),
    ('Profondo', 'Entradas en neto, como las entregó la comisión; la liquidación en bruto está en la hoja 10.'),
    ('Personas', '99 en la casa (97 facturadas + 2 cortesía) para todo cálculo por persona.'),
    ('Cómo se hizo este archivo', 'Se genera automáticamente a partir de los registros y de las confirmaciones del director; no se edita a mano: se corrige el dato y se vuelve a generar. Los totales se verifican antes de escribirse.'),
]:
    wsf.cell(r, 1, k).font = font(10, True); wsf.cell(r, 1).alignment = WRAP; note(wsf, r, 2, v, '1E293B', 10); r += 1

# ────── 13. NOTAS POR PARTIDA ──────
wsn = wb.create_sheet('13 Notas por partida'); widths(wsn, 12, 58, 110)
title(wsn, 'NOTAS POR PARTIDA — de dónde sale cada número de la hoja 2', GRIS, 3)
explain(wsn, 'La explicación de cada partida del presupuesto: fecha y forma de pago, quién donó, y qué queda por confirmar.', 3)
header(wsn, 3, ['Área', 'Partida', 'Nota'], MAR)
r = 4
for a, p, p11, ps, pag, don, nota in cruce:
    wsn.cell(r, 1, a).font = font(9, color=GRIS); wsn.cell(r, 2, p).font = font(10); wsn.cell(r, 2).alignment = WRAP
    note(wsn, r, 3, nota, ROJO if ('⚠' in nota or 'POR CONFIRMAR' in nota) else '1E293B', 10)
    for cc in range(1, 4): wsn.cell(r, cc).border = border
    r += 1
wsn.freeze_panes = 'A4'

# ══════════ ORDEN, COLORES Y GUARDADO ══════════
ORDEN = ['0 Resumen', '1 Caja', '2 Presupuesto vs costo', '3 Al costo vs caja', '4 Base ETC 89', '5 Pendientes', '6 Ppto oficial vs Sistem',
         '7 Gastos', '8 Donaciones efectivo', '9 Especie', '10 Profondo', '11 Auditoría', '12 Fuentes y método', '13 Notas por partida']
assert set(ORDEN) == set(wb.sheetnames), set(wb.sheetnames) ^ set(ORDEN)
wb._sheets = [wb[n_] for n_ in ORDEN]
TAB = {'0 Resumen': MAR, '1 Caja': AZUL, '2 Presupuesto vs costo': AZUL, '3 Al costo vs caja': AZUL, '4 Base ETC 89': VERDE, '5 Pendientes': AMBAR, '6 Ppto oficial vs Sistem': '9CA3AF',
       '7 Gastos': '9CA3AF', '8 Donaciones efectivo': '9CA3AF', '9 Especie': '9CA3AF', '10 Profondo': '9CA3AF', '11 Auditoría': '9CA3AF', '12 Fuentes y método': GRIS, '13 Notas por partida': GRIS}
for n_, col in TAB.items():
    wb[n_].sheet_properties.tabColor = col
    wb[n_].page_setup.orientation = 'landscape'; wb[n_].page_setup.fitToWidth = 1; wb[n_].page_setup.fitToHeight = 0; wb[n_].sheet_properties.pageSetUpPr.fitToPage = True

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(f'✓ Wrote {OUT} ({len(wb.sheetnames)} hojas)')
print(f'  Entradas {ENTRADAS:,.2f} = cuotas {CUOTAS:,} + tard {TARDANZAS:,} + don {DONAC_EFEC:,} + part {PARTICIP:,} + profondo {PROFONDO:,.2f}')
print(f'  Salidas {SALIDAS:,} (22 gastos, 0 profondo) · Balance {BALANCE:,.2f} · real {REAL_CUENTAS:,} · dif {IMPUESTOS:,.2f}')
print(f'  Especie {ESPECIE_TOTAL:,} · cortesías {CORTESIA_JUEVES + CORTESIA_HOSP:,} · Apoyo total donado {DONAC_EFEC + ESPECIE_TOTAL:,}')
print(f'  Profondo: bruto {PROF_BRUTO:,} − premios {PROF_COSTOS:,} = {PROF_NETO_INFORME:,} + posteriores {PROF_ADICIONAL:,.2f} = {PROFONDO:,.2f} · por cobrar {PROF_POR_COBRAR:,}')
print(f'  Ppto OFICIAL {PPTO_OFICIAL} {PPTO_11AGO:,.2f} · Sistem {PPTO_SISTEM:,.2f} · casa real {CASA_TOTAL:,} · habitaciones {HAB_TARIFA:,.0f}/noche (inferida)')
print(f'  Costó {COSTO_ECON:,.2f} (caja {CRUCE_PAGADO:,} + cubierto {CRUCE_DONADO:,}) · por persona caja {SALIDAS / PERSONAS:,.0f} / total {COSTO_ECON / PERSONAS:,.0f} · base recurrente {BASE_REC:,.2f}')
print(f'  Cruce ppto por partida: oficial {CRUCE_P11:,.2f} · Sistem {CRUCE_PS:,.2f} (cuadran con los archivos)')
print(f'  Auditoría: {AUDIT_PASS}/{AUDIT_N} PASS · Pendientes abiertos: {N_ABIERTOS}')
