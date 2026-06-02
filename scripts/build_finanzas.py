#!/usr/bin/env python3
"""Sheet vivo de Finanzas ETC 88 — multi-pestaña editable.
Construye un xlsx con: Resumen · Casa · Menú · Cocina-Compras · Materiales/Litúrgico ·
Guías · Música · Formaciones · Transporte · Recaudación · Pagos equipo · Cómo usar.
Itemiza por área. Precios ESTIMADOS a validar con cada coord en F1. Refleja la deuda
inicial de RD$23,600 del 10% de la casa (Juan Manuel pagó, ya devuelto)."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

# Paleta
TINTA, CREMA, VELA = '1C140B', 'F7EBCC', 'F7EFD9'
MAR, TIERRA, SAFARI, AMBAR, CUERO = '1B3A52', 'B25028', '4A5D2E', 'C57920', '6B4423'

thin = Side(style='thin', color='C9AE76')
border = Border(left=thin, right=thin, top=thin, bottom=thin)

# ===== Cifras-decisión: SIEMPRE desde data/estado.json (no hardcodear inventos) =====
import json, re as _re
_estado = json.load(open('/home/user/ETC88/data/estado.json'))
def _ev(n): return n['valor'] if isinstance(n, dict) and 'valor' in n else n
_ef = _estado['finanzas']; _er = _estado['recaudacion']
CASA_SIN  = _ev(_ef['casa_por_persona_sin_exencion'])   # 2300 confirmado
CASA_CON  = _ev(_ef['casa_por_persona_con_exencion'])    # 2000 confirmado
DEUDA     = _ev(_ef['deuda_inicial'])                    # 23600 confirmado
CUOTA_PART= _ev(_ef['cuota_participante'])               # 3000 confirmado
PERSONAS  = _ev(_ef['personas_casa_piso'])               # 100 confirmado (piso en la casa)
OPERATIVOS= _estado['conteos_esperados']['operativos']   # 47
PARTICIPANTES = _ev(_ef['participantes_objetivo'])       # 53 (= 100 - 47), derivado
_cuota    = _ev(_ef['cuota_equipo'])                     # propuesta (rango + mensual)
CUOTA_MES = _cuota['mensual']
_nums     = [int(x.replace(',','')) for x in _re.findall(r'[\d,]+', _cuota['total_rango'])]
CUOTA_LOW, CUOTA_HIGH = (_nums[0], _nums[-1]) if len(_nums) >= 2 else (1500, 2000)
# Etiquetas de estado para render
P = '[PROPUESTA] '   # prefijo obligatorio para cifras no confirmadas

wb = openpyxl.Workbook()
wb.remove(wb.active)

def title(ws, txt, color=MAR, span=6):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    c = ws.cell(row=1, column=1, value=txt)
    c.font = Font(bold=True, size=13, color=CREMA)
    c.fill = PatternFill('solid', fgColor=color)
    c.alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[1].height = 28

def header(ws, row, cols, fill_color=TIERRA):
    for i, (name, width) in enumerate(cols, start=1):
        c = ws.cell(row=row, column=i, value=name)
        c.font = Font(bold=True, size=10, color=CREMA)
        c.fill = PatternFill('solid', fgColor=fill_color)
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        c.border = border
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[row].height = 26

def row(ws, r, vals, bold_last=False, total_row=False):
    for i, v in enumerate(vals, start=1):
        c = ws.cell(row=r, column=i, value=v)
        c.font = Font(size=10, bold=total_row)
        c.border = border
        c.alignment = Alignment(horizontal='right' if isinstance(v, (int, float)) else 'left', vertical='center', wrap_text=True)
        if total_row:
            c.fill = PatternFill('solid', fgColor='F3E4BE')
        if isinstance(v, (int, float)) and v > 0:
            c.number_format = '#,##0'

# ============ Hoja 1: RESUMEN ============
ws = wb.create_sheet('Resumen')
title(ws, 'ETC 88 · FINANZAS VIVO · Resumen Ejecutivo (v8 · 2-jun-2026)')
header(ws, 3, [('Concepto', 36), ('Mín. (RD$)', 14), ('Base', 14), ('Máx.', 14), ('Notas', 50)], MAR)
casa_con = PERSONAS * CASA_CON
casa_sin = PERSONAS * CASA_SIN
costo_items = [
 (f'Casa de retiro (con exención ${CASA_CON:,}/p × {PERSONAS} pers.)', casa_con, casa_con, casa_con, f'CON exención · {OPERATIVOS} equipo + ~{PARTICIPANTES} part. = {PERSONAS} en la casa'),
 ('Transporte (SPM→Higüey, equipo + participantes + clausura)', 69000, 77500, 86000, '3 cotizaciones a pedir (Metro, Transportando RD, DominicanBus)'),
 ('Cocina · Mercado (canasta)', 59000, 62410, 65800, 'La casa INCLUYE gas; no se compra gasoil'),
 ('Cocina · Meriendas / Correcaminos', 9000, 9756, 10000, ''),
 ('Cocina · Decoración / motivos comedor', 8000, 10000, 12000, 'Foami, velas, flores, cajitas, hilo (ref. ETC 78)'),
 ('Materiales y Litúrgico (itemizado)', 80000, 88500, 95000, 'Peces + Biblias + Banderín + Rosarios + Cofre palancas + Vino + Ofrenda confesores'),
 ('Guías · Materiales del PG (libretas, sobres, alambre…)', 14000, 17000, 20000, 'Libretas para participantes EN ESTE rubro'),
 ('Música · Impresión cancionero + cables/respaldo', 3000, 4500, 6000, 'La casa tiene sonido; solo respaldo'),
 ('Formaciones F1–F5 (5 sesiones · refrigerio + local)', 13000, 16315, 20000, ''),
 ('Convivencia del equipo (22-ago · día completo)', 8000, 12000, 18000, 'Miniretiro; confirmar si incluye almuerzo del equipo y local'),
 ('Ensayo General (23-ago · INCLUYE el almuerzo del equipo)', 12000, 16000, 20000, 'Almuerzo ~52 personas + refrigerio + local'),
 ('Bienvenida post-ETC (9-sep · bizcocho)', 2000, 3000, 4500, 'Bizcocho de bienvenida de los nuevos (1ra reunión post-retiro)'),
 ('Camisetas del equipo (~56 × est.)', 19600, 22400, 28000, 'Tallas PARCIALES (ver pestaña Camisetas); faltan invitados pendientes + Paul, Frank y la Sor. Mockup tras el Design System.'),
 ('Avanzada jueves 3-sep (porción casa + 3 comidas del equipo que adelanta)', 15000, 20000, 24000, 'CONFIRMAR con la casa la tarifa de noche/día extra; depende de cuántos adelantan (cocina). Desayuno + almuerzo + cena de ese día.'),
 ('Imprevistos 5%', 22000, 23900, 25000, ''),
]
tot_min = sum(x[1] for x in costo_items); tot_base = sum(x[2] for x in costo_items); tot_max = sum(x[3] for x in costo_items)
data = costo_items + [
 (f'Casa SIN exención (${CASA_SIN:,}/p × {PERSONAS}) — alternativa', casa_sin, casa_sin, casa_sin, 'Si NO se consigue exención: reemplaza la línea de casa (no se suma aquí)'),
 ('', None, None, None, ''),
 ('TOTAL ESTIMADO (con exención)', tot_min, tot_base, tot_max, f'Casa a {PERSONAS} personas; precios ESTIMADOS a validar en F1'),
]
r = 4
for d in data:
    row(ws, r, d, total_row=(d[0].startswith('TOTAL')))
    r += 1
r += 2
# Brecha
ws.cell(row=r, column=1, value='BRECHA Y RECAUDACIÓN').font = Font(bold=True, size=12, color=TIERRA)
r += 1
header(ws, r, [('Concepto', 36), ('Monto', 14), ('Notas', 50)], TIERRA)
r += 1
COSTO_BASE = tot_base                       # computado (con exención)
TOTAL_CUBRIR = COSTO_BASE + DEUDA           # = META de recaudación
cuota_eq_low, cuota_eq_high = OPERATIVOS * CUOTA_LOW, OPERATIVOS * CUOTA_HIGH
cuota_eq_mid = (cuota_eq_low + cuota_eq_high) // 2
cuotas_part = PARTICIPANTES * CUOTA_PART
brecha_fundraise = TOTAL_CUBRIR - cuotas_part - cuota_eq_mid  # lo que deben cubrir rifa+comida+donaciones
brecha = [
 ('(+) Costo estimado base (con exención)', COSTO_BASE, 'Estimado · suma de arriba; precios a validar en F1'),
 ('(+) Deuda inicial al Consejo (10% casa)', DEUDA, 'Juan Manuel pagó 5-mar; ya devuelto. Arrancamos en NEGATIVO.'),
 ('(=) Total a cubrir = META de recaudación', TOTAL_CUBRIR, 'La meta NO es un número fijo: es este costo total.'),
 (f'(-) Cuotas participantes (~{PARTICIPANTES} × ${CUOTA_PART:,})', cuotas_part, f'Para completar {PERSONAS} en la casa · confirmado $3,000/participante'),
 (f'(-) Cuotas equipo ({OPERATIVOS} × ${CUOTA_LOW:,}–{CUOTA_HIGH:,})', cuota_eq_mid, P + f'${CUOTA_MES}/mes · SIN CERRAR · rango ${cuota_eq_low:,}–${cuota_eq_high:,}'),
 ('(=) BRECHA: rifa + venta de comida + donaciones', brecha_fundraise, 'Montos VARIABLES (lo que se recaude). Rifa = primera actividad. Donaciones = responsabilidad de Directores.'),
]
for b in brecha:
    row(ws, r, b)
    r += 1

# ============ Hoja 2: CASA ============
ws = wb.create_sheet('Casa')
title(ws, 'CASA DE RETIRO · La Ceiba del Salado, Higüey · Samuel Montilla', MAR)
header(ws, 3, [('Concepto', 36), ('Personas', 12), ('$/persona', 14), ('Total', 14), ('Notas', 40)], MAR)
data = [
 ('SIN exención', PERSONAS, CASA_SIN, PERSONAS * CASA_SIN, 'Tarifa estándar · piso de 100 personas'),
 ('CON exención (RNC parroquia de Paul)', PERSONAS, CASA_CON, PERSONAS * CASA_CON, f'AHORRO ${(CASA_SIN-CASA_CON)*PERSONAS:,} · diferencia ${CASA_SIN-CASA_CON}/persona'),
 ('Reserva 10% pagada 5-mar (Juan Manuel · devuelto)', None, None, DEUDA, 'DEUDA INICIAL al Consejo · primera obligación'),
 ('Saldo con exención tras la deuda', None, None, PERSONAS * CASA_CON - DEUDA, f'{PERSONAS*CASA_CON:,} - {DEUDA:,}'),
]
r = 4
for d in data:
    row(ws, r, d)
    r += 1

# ============ Hoja 3: MENÚ ============
ws = wb.create_sheet('Menú')
title(ws, 'MENÚ POR TIEMPO DE COMIDA · estructura sin precios (a llenar)', SAFARI)
header(ws, 3, [('Día', 12), ('Tiempo', 18), ('Plato principal', 28), ('Acompañante', 22), ('Bebida', 16), ('Postre/Notas', 24)], SAFARI)
menu = [
 ('Viernes', 'Cena (8:00pm)', 'Pasta con bechamel/Prego (sin marisco)', 'Pan + ensalada', 'Jugo + agua', 'Bizcocho · motivo de bienvenida'),
 ('Sábado', 'Desayuno (8am)', 'Mangú/avena + queso + huevo (opción sin huevo · José Á.)', 'Salami opcional', 'Café · jugo · té', 'Frutas (NO piña)'),
 ('Sábado', 'Refrigerio AM (10:25)', 'Picaderas / galletas', '', 'Té frío · jugo', ''),
 ('Sábado', 'Almuerzo (12pm)', 'Pollo o res guisada (NO mariscos)', 'Arroz + habichuelas + ensalada', 'Refresco · agua', 'Frutas'),
 ('Sábado', 'Refrigerio PM (4:45)', 'Bizcocho / galletas dulces', '', 'Té · jugo', ''),
 ('Sábado', 'CENA con LAVATORIO (6:30)', 'Cena solemne (Lavatorio de pies — ¡lo lleva cocina!)', 'Pan ácimo opcional', 'Vino litúrgico + jugo', 'Motivo fuerte · silencio'),
 ('Sábado', 'Refrigerio noche', 'Chocolate caliente + galletas', '', 'Chocolate', 'Después de confesiones'),
 ('Domingo', 'Desayuno (8am)', 'Tostadas + huevo (opción sin)', 'Jamón + queso', 'Café · jugo', 'Frutas'),
 ('Domingo', 'Almuerzo (1pm · clausura)', 'Almuerzo de fiesta (carne + pollo)', 'Arroz + habichuelas + ensalada', 'Refresco · agua', 'Bizcocho de celebración'),
]
r = 4
for m in menu:
    row(ws, r, m)
    r += 1
ws.row_dimensions[r-1].height = 32

# ============ Hoja 4: COCINA · COMPRAS ============
ws = wb.create_sheet('Cocina-Compras')
title(ws, 'COCINA · LISTA DE COMPRAS (canasta · precios 2026)', SAFARI)
header(ws, 3, [('Cantidad', 10), ('Unidad', 12), ('Artículo', 28), ('P. Unit.', 12), ('Total', 12), ('Responsable / Donación', 30)], SAFARI)
canasta = [
 (180,'Unidad','Plátano verde',21,3780,''),
 (50,'Libras','Pechuga de pollo (con hueso)',140,7000,'Ahorro 25% vs deshuesada'),
 (45,'Libras','Fajitas de res',170,7650,''),
 (64,'Libras','Papa',48,3072,''),
 (8,'Libras','Cebolla roja',52,416,'OJO: en ETC86 pagaron sobreprecio'),
 (7,'Libras','Ají morrón',85,595,''),
 (10,'Libras','Tomate barceló',46,460,''),
 (6,'Libras','Chuleta ahumada',147,882,''),
 (3,'Barras','Salami',430,1290,''),
 (6,'Cartón 30','Huevos',250,1500,''),
 (6,'Libras','Jamón cocido lonjeado',250,1500,''),
 (5,'Libras','Queso amarillo lonjeado',260,1300,''),
 (15,'Libras','Pasta espagueti',38,570,''),
 (8,'Libras','Espirales',39,312,''),
 (5,'Cajas 12L','Leche entera',888,4440,''),
 (15,'Latas','Leche evaporada',72,1080,''),
 (8,'Paquetes','Café Santo Domingo 1lb',410,3280,'Subió 20% · buscar donación'),
 (4,'Paquetes 5lb','Azúcar (crema)',156,624,''),
 (1,'Galón','Mayonesa Baldom',550,550,'Vs $950 ETC86 — ahorro $400'),
 (1,'Galón','Aceite freír (MERCADOM)',615,615,'Mayorista'),
 (20,'Libras','Harina de trigo',42,840,''),
 (15,'Paq 12','Galletas Guarina salada',55,825,''),
 (15,'Paq 12','Galletas Guarina dulce',115,1725,''),
 (14,'Unidades','Refrescos 2L',85,1190,''),
 (2,'Faldos 24','Papel de baño',475,950,''),
 (30,'Libras','Arroz',38,1140,'¿Donación? Padre Paul en 79'),
 (15,'Libras','Habichuelas pintas',52,780,'¿Donación?'),
 (3,'Potes','Salsa Prego roja',250,750,''),
 (40,'Unidades','Pan baguette',50,2000,'Negociar con panadería local'),
 (4,'Fundas','Pan rebanado Lumijor',120,480,'Vs $195 marca premium — ahorro $280'),
 (None,'','OTROS (sazón, sal, vinagre, especias, frutas, picaderas)',None,18500,'Detallar con coords'),
]
r = 4
total = 0
for c in canasta:
    row(ws, r, c)
    if isinstance(c[4], (int, float)): total += c[4]
    r += 1
row(ws, r+1, ('','','TOTAL CANASTA ESTIMADA', None, total, 'Validar con Paloma + Jhonnito en F1'), total_row=True)

# ============ Hoja 5: MATERIALES Y LITÚRGICO ============
ws = wb.create_sheet('Materiales-Liturgico')
title(ws, 'MATERIALES Y LITÚRGICO (itemizado)', AMBAR)
header(ws, 3, [('Cantidad', 10), ('Unidad', 12), ('Artículo', 36), ('P. Unit.', 12), ('Total', 12), ('Notas / Momento', 38)], AMBAR)
mat = [
 (48,'Uds','Peces (entrega Eucaristía clausura)',715,34320,'Costo más alto del bloque'),
 (48,'Uds','Biblias',500,24000,'Cotizar local Higüey · SDQLee · Cuesta'),
 (4,'Uds','Ofrenda a sacerdotes confesores',2000,8000,'Sábado 9pm'),
 (1,'',' BANDERÍN (tela, asta, deco)',5000,5000,'NUEVO · sábado noche · diseño con la temática'),
 (2,'Gl','Vino litúrgico',1200,2400,'Misa clausura · ¿donación parroquia?'),
 (1,'Fda','Formas grandes (hostias)',400,400,''),
 (1,'Fda','Formas pequeñas',500,500,''),
 (2,'Packs','Cofre de palancas (48 pcs)',935,1870,''),
 (48,'Uds','Monedas de chocolate (palancas)',15,720,''),
 (1,'Pack 48','Porta-ID / Carnets',1100,1100,'Viernes'),
 (48,'Hojas','Impresión ID satinado',40,1920,''),
 (48,'Uds','ROSARIOS (oración a María sábado)',50,2400,'¿Donación parroquia?'),
 (1,'','Palangana + toallas (Lavatorio sábado)',1500,1500,'Cocina lo lleva'),
 (1,'','Lodo / arcilla (dinámica del pecado)',500,500,'Sábado noche'),
 (6,'Uds','Impresión horario 24×36',200,1200,''),
 (2,'Resmas','Papel 8.5×11',425,850,''),
 (15,'Yd','Papelógrafo',20,300,''),
 (1,'Rollo','Alambre cobre/dulce (70ft)',120,120,'Dinámica del alambre sábado AM'),
 (50,'Uds','Sobres blancos (palancas)',5,250,''),
 (7,'Uds','Cartulinas grandes',15,105,''),
 (4,'Cajas','Lapiceros (12 uds)',100,400,''),
 (2,'Uds','Marcadores negro',40,80,''),
 (2,'Uds','Marcadores verdes',40,80,''),
 (2,'Uds','Marcadores rojo',40,80,''),
 (7,'Cajas','Crayones (24 uds)',195,1365,''),
 (2,'Uds','Tape',120,240,''),
]
r = 4
total = 0
for c in mat:
    row(ws, r, c)
    if isinstance(c[4], (int, float)): total += c[4]
    r += 1
row(ws, r+1, ('','','TOTAL MATERIALES Y LITÚRGICO', None, total, 'Validar con Resp. Materiales en F1'), total_row=True)

# ============ Hoja 6: GUÍAS ============
ws = wb.create_sheet('Guías')
title(ws, 'GUÍAS · Materiales del PG (libretas, color-coded)', MAR)
header(ws, 3, [('Cantidad', 10), ('Unidad', 12), ('Artículo', 32), ('P. Unit.', 12), ('Total', 12), ('Notas', 36)], MAR)
guias = [
 (48,'Uds','Libretas / cuadernos para participantes',60,2880,'EN PRESUPUESTO DE GUÍAS · cada PG'),
 (7,'Sets','Tarjetas de color por pareja (color-coded)',150,1050,'Identifica cada PG'),
 (48,'Hojas','Hoja de datos personales (template)',5,240,''),
 (1,'','Materiales de sociodrama (vestuario simple)',2000,2000,'Sábado'),
 (1,'','Decoración de los 7 espacios de PG',3500,3500,'Cada pareja decora su rincón'),
 (1,'','Sobres manila grandes para palancas (×48)',800,800,''),
 (None,'','Imprevistos / extras del PG',None,2000,''),
]
r = 4
total = 0
for c in guias:
    row(ws, r, c)
    if isinstance(c[4], (int, float)): total += c[4]
    r += 1
row(ws, r+1, ('','','TOTAL GUÍAS', None, total, 'Validar con Priscilla + Camila'), total_row=True)

# ============ Hoja 7: MÚSICA ============
ws = wb.create_sheet('Música')
title(ws, 'MÚSICA · Cancionero + respaldo (la casa tiene sonido)', AMBAR)
header(ws, 3, [('Cantidad', 10), ('Unidad', 12), ('Artículo', 32), ('P. Unit.', 12), ('Total', 12), ('Notas', 30)], AMBAR)
musica = [
 (95,'Uds','Impresión cancionero (3 días)',25,2375,'Equipo + participantes'),
 (1,'','Cables/baterías de respaldo · cuerdas',1500,1500,'La casa tiene sonido'),
 (1,'','Atriles / partituras imprimibles',600,600,''),
]
r = 4
total = 0
for c in musica:
    row(ws, r, c)
    if isinstance(c[4], (int, float)): total += c[4]
    r += 1
row(ws, r+1, ('','','TOTAL MÚSICA', None, total, 'Validar con José Tusen'), total_row=True)

# ============ Hoja 8: FORMACIONES ============
ws = wb.create_sheet('Formaciones')
title(ws, 'FORMACIONES (5 sesiones · jun-ago)', TIERRA)
header(ws, 3, [('Sesión', 18), ('Fecha', 12), ('Refrigerio', 12), ('Local', 12), ('Materiales', 12), ('Total', 12)], TIERRA)
form = [
 ('F1 · El llamado', '14-jun', 1500, 0, 1500, 3000),
 ('F2 · Una sola tripulación', '28-jun', 1500, 0, 800, 2300),
 ('F3 · El tesoro', '5-jul', 1500, 0, 800, 2300),
 ('F4 · Conociendo el terreno', '19-jul', 1500, 0, 1500, 3000),
 ('F5 · Listos para zarpar', '16-ago', 2000, 0, 2000, 4000),
 ('Reunión coords (jue 4-jun virtual)', '4-jun', 0, 0, 0, 0),
 ('Convivencia (miniretiro · día completo)', '22-ago', 6000, 2000, 4000, 12000),
 ('Ensayo General (incluye almuerzo del equipo)', '23-ago', 15000, 0, 1000, 16000),
 ('Reunión final', '30-ago', 1500, 0, 500, 2000),
 ('Bienvenida post-ETC (bizcocho)', '9-sep', 3000, 0, 0, 3000),
]
r = 4
total = 0
for c in form:
    row(ws, r, c)
    if isinstance(c[5], (int, float)): total += c[5]
    r += 1
row(ws, r+1, ('TOTAL FORMACIONES','','','','', total), total_row=True)

# ============ Hoja 9: TRANSPORTE ============
ws = wb.create_sheet('Transporte')
title(ws, 'TRANSPORTE · SPM → Higüey (3 cotizaciones a pedir)', CUERO)
header(ws, 3, [('Concepto', 36), ('Mín.', 12), ('Base', 12), ('Máx.', 12), ('Empresa', 30)], CUERO)
trans = [
 ('Minibús equipo (15-20 pers.) IDA Y VUELTA', 12000, 14000, 16000, 'Metro Servicios 809-530-2850'),
 ('Autobús participantes (40-50) IDA Y VUELTA', 30000, 32500, 35000, 'Transportando RD 849-803-1626'),
 ('Autobús clausura (padres/etecianos) IDA Y VUELTA', 25000, 27500, 30000, 'DominicanBus'),
 ('Combustible + peajes (3 viajes)', 2000, 3500, 5000, '4 casetas × $60-100'),
]
r = 4
totM, totB, totMx = 0,0,0
for c in trans:
    row(ws, r, c)
    totM += c[1]; totB += c[2]; totMx += c[3]
    r += 1
row(ws, r+1, ('TOTAL', totM, totB, totMx, ''), total_row=True)

# ============ Hoja 10: RECAUDACIÓN ============
ws = wb.create_sheet('Recaudación')
title(ws, f'RECAUDACIÓN · la META = costo total ${TOTAL_CUBRIR:,} (cuotas + rifa/comida + donaciones)', SAFARI)
header(ws, 3, [('Fuente', 36), ('Monto (RD$)', 14), ('Estado', 16), ('Responsable', 22), ('Notas', 36)], SAFARI)
rec = [
 (f'Cuotas participantes (~{PARTICIPANTES} × ${CUOTA_PART:,})', cuotas_part, 'Confirmado', 'Cada misionero', f'Para completar {PERSONAS} en la casa'),
 (f'Aportes equipo ({OPERATIVOS} × ${CUOTA_LOW:,}–{CUOTA_HIGH:,})', cuota_eq_mid, 'PROPUESTA', 'Cada miembro', P + f'${CUOTA_MES}/mes · SIN CERRAR'),
 ('Exención casa (vía RNC parroquia Paul)', (CASA_SIN - CASA_CON) * PERSONAS, 'Por gestionar', 'Co-Dir + Padre Paul', f'Ahorro ${CASA_SIN - CASA_CON}/persona × {PERSONAS}'),
 ('Rifa (Profondo #1)', None, 'VARIABLE', 'Co-Dir + Recaudación', 'Primera actividad · lo que se recaude'),
 ('Venta de comida (Profondo #2)', None, 'VARIABLE', 'Equipo completo', 'Lo que se recaude'),
 ('Donaciones empresas/particulares', None, 'VARIABLE', 'DIRECTORES (resp.)', 'Lo que se recaude · delegable'),
 ('= BRECHA a cubrir con rifa + comida + donaciones', brecha_fundraise, '', '', 'Costo total − cuotas: esto es lo que la recaudación variable debe levantar'),
]
r = 4
for c in rec:
    row(ws, r, c)
    r += 1

# ============ Hoja 11: PAGOS EQUIPO ============
ws = wb.create_sheet('Pagos Equipo')
title(ws, f'[PROPUESTA] APORTES DEL EQUIPO · ${CUOTA_MES}/mes · total ${CUOTA_LOW:,}–${CUOTA_HIGH:,}/persona (SIN CERRAR)', MAR)
header(ws, 3, [('Nombre', 30), ('Área', 16), ('Jun', 10), ('Jul', 10), ('Ago', 10), ('Sep', 10), ('Total', 12), ('Notas', 24)], MAR)
d = json.load(open('/tmp/etc88_data.json'))
op = [p for p in d['equipo'] if p.get('operativo') and not p.get('vacante')]
op.sort(key=lambda p: (p['area'], p['nombre']))
TOT_PP = CUOTA_MES * 4  # jun-sep
r = 4
for p in op:
    nm = p['nombre'].replace(' (sin formulario)','')
    row(ws, r, (nm, p['area'], CUOTA_MES, CUOTA_MES, CUOTA_MES, CUOTA_MES, TOT_PP, '[PROPUESTA] sin cerrar'))
    r += 1
row(ws, r+1, ('TOTAL OBJETIVO (propuesta)','', len(op)*CUOTA_MES, len(op)*CUOTA_MES, len(op)*CUOTA_MES, len(op)*CUOTA_MES, len(op)*TOT_PP, P), total_row=True)

# ============ Hoja: CAMISETAS / TALLAS ============
from collections import Counter
ws = wb.create_sheet('Camisetas')
title(ws, 'CAMISETAS DEL EQUIPO · tallas (parcial) — mockup tras el Design System', AMBAR)
team = [p for p in d['equipo'] if not p.get('vacante') and not p.get('backup')]
con_talla = [p for p in team if p.get('talla')]
sin_talla = [p for p in team if not p.get('talla')]
dist = Counter(p['talla'] for p in con_talla)
header(ws, 3, [('Talla', 14), ('Cantidad', 12), ('Notas', 40)], AMBAR)
r = 4
orden = ['S', 'M', 'L', 'XL', 'XXL']
for size in orden + [s for s in dist if s not in orden]:
    if dist.get(size):
        row(ws, r, (size, dist[size], '')); r += 1
row(ws, r, ('CON talla', len(con_talla), f'de {len(team)} del equipo'), total_row=True); r += 1
row(ws, r, ('FALTAN talla', len(sin_talla), 'pedir antes de imprimir'), total_row=True); r += 2
ws.cell(row=r, column=1, value='A QUIÉNES FALTA LA TALLA:').font = Font(bold=True, size=11, color=TIERRA); r += 1
header(ws, r, [('Nombre', 30), ('Área', 18), ('Motivo', 26)], TIERRA); r += 1
for p in sorted(sin_talla, key=lambda x: (x['area'], x['nombre'])):
    motivo = 'sin formulario' if p.get('sin_formulario') else 'ampliado/transversal'
    row(ws, r, (p['nombre'].replace(' (sin formulario)', ''), p['area'], motivo)); r += 1

# ============ Hoja 12: Cómo usar ============
ws = wb.create_sheet('Cómo usar')
ws.column_dimensions['A'].width = 110
notas = [
 ('FINANZAS ETC 88 — HOJA VIVA · v8 · 2-jun-2026', True),
 ('', False),
 ('Cómo se usa:', True),
 ('1. La pestaña Resumen es la foto ejecutiva. Lee primero.', False),
 ('2. Las pestañas por área (Casa, Cocina-Compras, Materiales, Guías, Música, Formaciones, Transporte)', False),
 ('   son lo que cada coordinador entrega y refina en F1 (14-jun). Precios son ESTIMADOS a validar.', False),
 ('3. Menú es estructura sin precios; cocina lo refina y de ahí salen las cantidades de Cocina-Compras.', False),
 ('4. Recaudación: la META = el costo total. Se cubre con cuotas (participantes + equipo) +', False),
 ('   rifa + venta de comida + donaciones (montos VARIABLES, lo que se recaude).', False),
 ('5. Pagos Equipo: cuota PROPUESTA de $500/mes (total $1,500–2,000/persona). SIN CERRAR — la decide la Dirección.', False),
 ('', False),
 ('CONTEXTO CRÍTICO:', True),
 ('• Arrancamos en NEGATIVO: $23,600 (10% reserva casa pagada por Juan Manuel ya devuelto al Consejo).', False),
 ('  Es la PRIMERA deuda a cubrir con la recaudación.', False),
 ('• La casa INCLUYE gas y limpieza (no se compra). Con exención: $2,000/p; sin exención: $2,300/p.', False),
 ('• Casa tiene sonido (música solo lleva respaldo).', False),
 ('• Piso de personas: completar 100 en la casa (≈47 operativos + ~53 participantes).', False),
 ('', False),
 ('PENDIENTES PARA CERRAR EL PRESUPUESTO:', True),
 ('• Cerrar el monto final de la cuota del equipo (propuesta $500/mes, total $1,500–2,000).', False),
 ('• Gestionar exención con el Padre Paul (impacto ~$30,000 a 100 personas).', False),
 ('• Cotizar transporte (3 empresas) · fijar fecha límite (también biblias y peces).', False),
 ('• Banderín: diseño + cotización.', False),
 ('• Confirmar el conteo final para completar 100 en la casa (afecta peces, biblias, comida).', False),
 ('• Donaciones en especie: arroz, habichuelas, aceite (el ETC 79 los consiguió donados).', False),
]
for i, (txt, isheader) in enumerate(notas, start=1):
    c = ws.cell(row=i, column=1, value=txt)
    if isheader:
        c.font = Font(bold=True, size=13, color=TIERRA)
    else:
        c.font = Font(size=11)

# Save
wb.save('/home/user/ETC88/Finanzas_ETC88.xlsx')
print(f"Wrote Finanzas_ETC88.xlsx — {len(wb.sheetnames)} pestañas: {', '.join(wb.sheetnames)}")
