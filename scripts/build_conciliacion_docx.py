#!/usr/bin/env python3
"""
Informe económico narrativo del ETC 88 (Word), con cuadros y tablas.
Se genera desde los MISMOS datos y cálculos de scripts/build_conciliacion.py (regla #2 y #5: los
entregables de Drive son .docx generados, nunca editados a mano).
Salida: data/presupuesto/Informe_Economico_ETC88.docx
Requiere: pip install python-docx
"""
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / 'scripts/build_conciliacion.py'
OUT = REPO / 'data/presupuesto/Informe_Economico_ETC88.docx'

src = SRC.read_text(encoding='utf-8')
MARK = '# ══════════ HELPERS DE HOJA ══════════'
assert MARK in src
ns = {'__file__': str(SRC)}
exec(compile(src.split(MARK)[0], str(SRC), 'exec'), ns)
D = ns

def n(v): return f'{v:,.0f}'
def d(v): return f'{v:,.2f}'
def pct(a, b): return f'{a / b * 100:.0f}%'

ENTRADAS, SALIDAS, BALANCE = D['ENTRADAS'], D['SALIDAS'], D['BALANCE']
REAL, IMPUESTOS = D['REAL_CUENTAS'], D['IMPUESTOS']
COSTO, GRATIS = D['COSTO_ECON'], D['RECIBIDO_GRATIS']
ESPECIE, C_JUE, C_HOSP = D['ESPECIE_TOTAL'], D['CORTESIA_JUEVES'], D['CORTESIA_HOSP']; CORT = C_JUE + C_HOSP
PPTO, PPTO_S, OFICIAL = D['PPTO_11AGO'], D['PPTO_SISTEM'], D['PPTO_OFICIAL']
PERSONAS, FUENTES, AREAS, cruce = D['PERSONAS'], D['FUENTES'], D['AREAS'], D['cruce']
esp, especie = D['especie_tot'], D['especie']
HAB_T, HAB_TAR, CASA = D['HAB_TOTAL'], D['HAB_TARIFA'], D['CASA_TOTAL']
BASE_REC = D['BASE_REC']; CUOTA_P, CUOTA_E = D['CUOTA_PARTICIPANTE'], D['CUOTA_EQUIPO']
CUOTAS, TARDANZAS, DONAC, PARTICIP, PART_ESPER, PROFONDO = D['CUOTAS'], D['TARDANZAS'], D['DONAC_EFEC'], D['PARTICIP'], D['PART_ESPER'], D['PROFONDO']
P_BRUTO, P_COSTOS, P_NETO, P_ADIC, P_COBRAR = D['PROF_BRUTO'], D['PROF_COSTOS'], D['PROF_NETO_INFORME'], D['PROF_ADICIONAL'], D['PROF_POR_COBRAR']
P_BOL_PAG, P_BOL_NO, P_ING_BOL, P_ING_COM = D['PROF_BOLETAS_PAG'], D['PROF_BOLETAS_NOPAG'], D['PROF_ING_BOLETAS'], D['PROF_ING_COMIDA']
EF_COCINA, EF_SALON = D['EFECTIVO_COCINA'], D['EFECTIVO_SALON']
IMP_BANCO, COPIAS, IMP_TASA, IMP_BASE = D['IMPUESTOS_BANCO'], D['COPIAS_PAGADAS'], D['IMPUESTO_TASA'], D['IMPUESTO_BASE']
pendientes, checks, AUDIT_N, AUDIT_PASS = D['pendientes'], D['checks'], D['AUDIT_N'], D['AUDIT_PASS']
RECS = D['RECOMENDACIONES_89']; gastos, donaciones, profondo = D['gastos'], D['donaciones'], D['profondo']
COMIDA_PP = (90489 + esp['Cocina'] - 10300) / PERSONAS

MAR = RGBColor(0x5B, 0x3A, 0x29); AZUL = RGBColor(0x0B, 0x1F, 0x3A); GRIS = RGBColor(0x66, 0x66, 0x66)

doc = Document()
for s_ in doc.sections:
    s_.left_margin = s_.right_margin = Cm(2.2); s_.top_margin = s_.bottom_margin = Cm(2)
st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
for lvl, size, color in [(1, 18, MAR), (2, 14, AZUL), (3, 12, AZUL)]:
    h = doc.styles[f'Heading {lvl}']; h.font.name = 'Calibri'; h.font.size = Pt(size); h.font.bold = True; h.font.color.rgb = color
    h.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor); tcPr.append(shd)

def para(text, bold=False, italic=False, size=None, color=None, align=None, space_after=6):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p

def bullets(items):
    for it in items:
        p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(3)
        if isinstance(it, tuple):
            r = p.add_run(it[0]); r.bold = True; p.add_run(it[1])
        else:
            p.add_run(it)

def table(rows, widths=None, header=True, bold_last=False, size=10, align_right_from=1):
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.text = ''
            p = c.paragraphs[0]; r = p.add_run(v if isinstance(v, str) else (d(v) if isinstance(v, float) and abs(v - round(v)) > 0.005 else n(v)))
            r.font.size = Pt(size)
            if isinstance(v, (int, float)) or (j >= align_right_from and i > 0 and isinstance(v, str) and v[:1] in '+-0123456789'): p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if header and i == 0: r.bold = True; r.font.color.rgb = RGBColor(0xF7, 0xEF, 0xD9); shade(c, '5B3A29')
            elif bold_last and i == len(rows) - 1: r.bold = True; shade(c, 'E3F2FD')
            elif i % 2 == 0: shade(c, 'F7F3EA')
            p.paragraph_format.space_after = Pt(0)
    if widths:
        t.autofit = False
        tblPr = t._tbl.tblPr; lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
        for j, w in enumerate(widths): t.columns[j].width = Cm(w)
        for row in t.rows:
            for j, w in enumerate(widths): row.cells[j].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def cuadro(text):
    """Cuadro resaltado de una sola celda para mensajes clave."""
    t = doc.add_table(rows=1, cols=1); t.style = 'Table Grid'; c = t.cell(0, 0); c.text = ''
    p = c.paragraphs[0]; r = p.add_run(text); r.font.size = Pt(11); r.bold = True; shade(c, 'FFF4E0')
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ── Portada ──
para('ETC 88 · Informe económico y conciliación final', bold=True, size=24, color=MAR, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
para('Encuentro Total con Cristo #88 · Casa La Ceiba del Salado, Higüey · 4–6 de septiembre de 2026', size=12, color=GRIS, space_after=2)
para('Co-Dirección: Juan Manuel de la Cruz · Jean Carlo de la Cruz', size=12, color=GRIS, space_after=2)
para(f'Cierre al 11 de septiembre de 2026 · {PERSONAS} personas en la casa · cifras en RD$', size=11, color=GRIS, space_after=14)

cuadro(f'El retiro costó {n(COSTO)}. De caja salieron {n(SALIDAS)}; los {n(GRATIS)} restantes ({pct(GRATIS, COSTO)}) los pusieron 30 donantes en especie y la casa en cortesías. '
       f'Las cuentas cuadran con el banco: quedan {n(REAL)}.')

# ── 1. Resumen ──
doc.add_heading('1. El retiro en seis números', 1)
table([['Concepto', 'RD$', 'Qué significa'],
       ['Entradas totales', ENTRADAS, 'participantes, donaciones, profondo, cuotas del equipo y tardanzas'],
       ['Salidas de caja', SALIDAS, '22 gastos del registro de tesorería'],
       ['Balance', BALANCE, f'entradas − salidas; en el banco {n(REAL)}, la diferencia ({d(IMPUESTOS)}) es el impuesto bancario por transacción más unas copias'],
       ['Lo que costó el retiro', COSTO, f'caja + donaciones en especie ({n(ESPECIE)}) + cortesías de la casa ({n(CORT)})'],
       ['Cubierto sin pagar', GRATIS, f'{pct(GRATIS, COSTO)} del costo'],
       ['Por persona', f'{n(SALIDAS / PERSONAS)} / {n(COSTO / PERSONAS)}', f'de caja / al costo; cada participante pagó {n(CUOTA_P)} y cada miembro del equipo {n(CUOTA_E)}']],
      widths=[5, 3, 9])

# ── 2. Cómo se organizó ──
doc.add_heading('2. Cómo se organizó la economía del retiro', 1)
para('El proceso económico del ETC 88 tuvo cinco momentos. Este informe sigue ese orden y, al final, deja la base y las recomendaciones para el ETC 89.')
doc.add_heading('2.1 Presupuesto', 2)
para(f'El presupuesto se elaboró en febrero por áreas (Directores, Cocina, Guías y Música) y se actualizó el 11 de agosto con la tarifa real de la casa. Esa versión del 11 de agosto, de {d(PPTO)}, es el presupuesto oficial contra el que se compara todo en este informe. '
     f'Existió además una versión operativa, la que alimentaba el tablero de finanzas, de {d(PPTO_S)}; la diferencia entre ambas (83,390) está en la casa, los peces, la cocina y el transporte.')
doc.add_heading('2.2 Cuotas y plan de recaudación', 2)
para(f'Cada participante pagó una cuota de {n(CUOTA_P)} y cada miembro del equipo una de {n(CUOTA_E)} (49 miembros, {n(CUOTAS)}). Como las cuotas no cubrían el presupuesto, el plan de recaudación se apoyó en tres fuentes más: donaciones en efectivo, la actividad Profondo (rifa y venta de comida y helados) y donaciones en especie que redujeron lo que había que comprar.')
doc.add_heading('2.3 Tesorería y registro', 2)
para('La tesorería la llevaron tres personas con roles de recibir, registrar y conciliar, más un cuarto rol de manejo de la plataforma. Todo movimiento se registró en el tablero de finanzas: 22 gastos, 49 donaciones en efectivo y 8 entregas de la comisión de Profondo.')
doc.add_heading('2.4 El retiro', 2)
para(f'Llegamos a la casa el jueves, no el viernes: 27 personas en la avanzada, de las que 19 pagaron 500 por la noche y 8 no se cobraron. En total dormimos {PERSONAS} personas; la casa facturó 97 y dio dos cortesías, para el padre y para la sor.')
doc.add_heading('2.5 Cierre y conciliación', 2)
para(f'Después del retiro se cruzó cada gasto del registro con su partida del presupuesto oficial, se valoró lo donado en especie al precio del presupuesto y se comprobó el resultado contra el banco. Sobre el resultado corren {AUDIT_N} verificaciones numéricas; todas cuadran.')

# ── 3. De dónde salió el dinero ──
doc.add_heading('3. De dónde salió el dinero', 1)
rows = [['Fuente', 'RD$', '%']] + [[l.split(' (')[0].split(',')[0], v, pct(v, ENTRADAS)] for l, v in FUENTES] + [['Entradas totales', ENTRADAS, '100%']]
table(rows, widths=[8, 4, 2], bold_last=True)
para('Participantes y donaciones en efectivo aportaron casi lo mismo; el profondo fue la tercera fuente y las cuotas del equipo cubrieron menos de una quinta parte.')
doc.add_heading('3.1 El profondo, abierto', 2)
table([['Concepto', 'RD$'],
       [f'Boletas colocadas y pagadas: {P_BOL_PAG:g} × 200', P_ING_BOL],
       ['Venta de comida y helados', P_ING_COM],
       ['Ingresos brutos', P_BRUTO],
       ['Premios: aire acondicionado 16,900 y abanico de torre 3,000', -P_COSTOS],
       ['Neto del informe de la comisión', P_NETO],
       ['Ventas de helados posteriores al informe', P_ADIC],
       ['Entregado a finanzas', PROFONDO]], widths=[11, 4], bold_last=True)
para(f'Quedaron {P_BOL_NO:g} boletas colocadas sin pagar ({n(P_COBRAR)}); la dirección decidió no cobrarlas. Los premios son costo de recaudar, no del retiro, y ya están descontados del neto.')

# ── 4. En qué se gastó ──
doc.add_heading('4. Presupuesto y costo, por área', 1)
para('Costó = pagado de caja + cubierto sin pagar. Cubierto sin pagar = donaciones en especie valoradas al precio del presupuesto y cortesías de la casa. Diferencia = costó − presupuestado.')
rows = [['Área', 'Presupuestado', 'Costó', 'Cubierto sin pagar', 'Pagado de caja', 'Diferencia']]
for a, (p11, ps, pag, don) in AREAS.items():
    rows.append([a, p11, pag + don, don, pag, f'{pag + don - p11:+,.0f}'])
rows.append(['Total', PPTO, COSTO, GRATIS, SALIDAS, f'{COSTO - PPTO:+,.0f}'])
table(rows, widths=[3.2, 2.8, 2.6, 3, 2.8, 2.6], bold_last=True, size=9)
doc.add_heading('4.1 Lo que explica cada área', 2)
bullets([
    ('Casa: ', f'{n(CASA)} pagados frente a 236,000 presupuestados. La diferencia es la noche del jueves (9,500) y las habitaciones de pequeños grupos (1,800). Las dos cortesías y los 8 del jueves suman {n(CORT)} de valor recibido.'),
    ('Transporte: ', '45,000, igual al presupuesto: dos autobuses (35,000) más un desvío de 10,000 que no estaba previsto.'),
    ('Materiales: ', 'las biblias costaron 35,360 (proforma 34,000 más 1,360). Los peces (36,000) los donó La Vega, la decoración (10,300) fue donada y los materiales de oficina (2,300) los pusieron los directores.'),
    ('Litúrgico: ', 'una ofrenda de 10,000 al padre por las confesiones (presupuesto 12,000) e insumos de misa donados (3,000).'),
    ('Formación: ', 'las cinco reuniones en Santa Clara (10,000) se pagaron en junio con un aporte personal de Juan Manuel, reembolsado del efectivo de imprevistos; la reunión extraordinaria del ensayo costó 3,000; el almuerzo del ensayo, 14,730; las meriendas, 5,920.'),
    ('Equipo: ', '60 camisetas, 28,800, igual al presupuesto.'),
    ('Guías: ', 'solo 7,720 salieron de caja (courier, impresión de mochilas y 2,000 a Priscila); 23,690 en materiales los pusieron Priscila, Luisa, Camila, Darianny y los propios guías.'),
    ('Música: ', 'llaveros 9,000; pilas, chocolates y alambre donados (1,262).'),
    ('Cocina: ', f'compra en Iberia 74,509 (cotización 77,044.05), detalles y combustible 15,980, efectivo en la casa 5,000; donados 14,593 en plátanos, arroz, pasta, papel y limpieza. Costó 110,082 frente a 120,840 presupuestados.'),
    ('Eventos: ', 'el bizcocho de la dinámica (presupuesto 1,500) se cambió por helados (1,740); el bizcocho de bienvenida (6,000) no estaba presupuestado.'),
])

# ── 5. Lo que otros pusieron ──
doc.add_heading('5. Lo que otros pusieron', 1)
para(f'{n(GRATIS)} del costo del retiro no pasaron por caja: {n(ESPECIE)} en donaciones en especie de unos 30 donantes y {n(CORT)} en cortesías de la casa. Se valoran al precio del presupuesto, no a factura.')
table([['Rubro', 'RD$'],
       ['Peces (símbolo del retiro), donados por La Vega', esp['Directores'] - 2300 - 3000],
       ['Cocina y decoración', esp['Cocina']],
       ['Materiales de guías', esp['Guías']],
       ['Insumos de misa', 3000],
       ['Materiales de oficina', 2300],
       ['Música', esp['Música']],
       ['Cortesías de la casa (8 del jueves y 2 del fin de semana)', CORT],
       ['Total cubierto sin pagar', GRATIS]], widths=[11, 4], bold_last=True)

# ── 6. La casa ──
doc.add_heading('6. La casa, al detalle', 1)
table([['Concepto', 'RD$'],
       ['Hospedaje: 97 personas × 2,360 (viernes a domingo)', 228920],
       ['Noche del jueves: 19 personas × 500', 9500],
       [f'Habitaciones para pequeños grupos: {n(HAB_TAR)} × 2 noches', HAB_T],
       ['Total pagado (avance 23,600 + pago final 216,620)', CASA],
       ['Cortesía: 8 personas del jueves', C_JUE],
       ['Cortesía: 2 personas el fin de semana', C_HOSP]], widths=[11, 4])
para(f'Frente al presupuesto oficial (236,000) la casa costó {n(CASA - 236000)} más. Frente al presupuesto operativo (200,000), 40,220 más, porque esa versión nunca actualizó la tarifa de 2,360 ni contempló el jueves.')

# ── 7. Presupuesto y realidad ──
doc.add_heading('7. Presupuesto y realidad', 1)
table([['Concepto', 'RD$', 'Frente al presupuesto'],
       [f'Presupuesto oficial ({OFICIAL})', PPTO, ''],
       ['Lo que costó el retiro', COSTO, f'{COSTO - PPTO:+,.0f} ({(COSTO / PPTO - 1) * 100:+.1f}%)'],
       ['Lo que salió de caja', SALIDAS, f'{SALIDAS - PPTO:+,.0f} ({(SALIDAS / PPTO - 1) * 100:+.1f}%)']], widths=[7, 4, 5])
cuadro('El retiro costó un poco más de lo presupuestado y salió bastante menos de caja, porque uno de cada seis pesos lo puso alguien más. El presupuesto oficial fue realista; lo que cambió fue quién pagó cada cosa.')

# ── 8. Las cuentas cuadran ──
doc.add_heading('8. Las cuentas cuadran', 1)
table([['Paso', 'RD$'],
       ['Entradas', ENTRADAS],
       ['− Salidas', -SALIDAS],
       ['= Balance', BALANCE],
       [f'− Impuesto bancario por transacción ({IMP_TASA*100:.2f}% sobre {n(IMP_BASE)})', -IMP_BANCO],
       ['− Copias pagadas', -COPIAS],
       ['En cuentas al 11 de septiembre', REAL]], widths=[11, 4], bold_last=True)
para(f'El efectivo de imprevistos (15,000) quedó liquidado: {n(EF_COCINA)} a cocina en la casa y {n(EF_SALON)} de reembolso del salón de formaciones. Los pagos de participantes suman {n(PARTICIP)}: no hay pagos pendientes; la referencia teórica de {n(PART_ESPER)} (46 × {n(CUOTA_P)}) es mayor porque cuatro participantes pagaron menos de {n(CUOTA_P)}.')

# ── 9. Por persona ──
doc.add_heading('9. Por persona', 1)
table([['Concepto', 'RD$'],
       [f'Costo de caja por persona ({PERSONAS})', SALIDAS / PERSONAS],
       ['Costo total por persona', COSTO / PERSONAS],
       ['Cuota de cada participante', CUOTA_P],
       ['Cuota de cada miembro del equipo', CUOTA_E]], widths=[11, 4])
para(f'La cuota del participante cubrió el {CUOTA_P / (SALIDAS / PERSONAS) * 100:.0f}% de su costo de caja; el resto lo cubrieron las donaciones, el profondo y las cuotas del equipo. No pagaron cuota los asesores espirituales y de cocina (el padre Paul, la sor, Petra y Johanny); los tres guías de reserva no entran en el conteo de 49.')

# ── 10. Lo que queda ──
doc.add_heading('10. Lo que queda por dejar constancia', 1)
notas = [x for x in pendientes if x[0] in ('ABIERTO', 'NOTA')]
bullets([(f'{t}: ', (f_ or det)) for _, t, det, f_ in notas])
para('Todo lo demás está cerrado: la casa, el transporte, el desglose de los pagos, el salón de formaciones, el profondo, los participantes que pagaron y no asistieron, y las donaciones en especie.', italic=True, color=GRIS)

# ── 11. Base y recomendaciones ──
doc.add_heading('11. Base y recomendaciones para el ETC 89', 1)
table([['Concepto', 'RD$', 'Por persona'],
       ['Costo real del ETC 88', COSTO, COSTO / PERSONAS],
       ['Base recurrente (sin desvío de transporte ni bizcocho de bienvenida)', BASE_REC, BASE_REC / PERSONAS]], widths=[10, 3, 3])
para(f'Partidas por persona para el próximo presupuesto: casa 2,360 · comida {n(COMIDA_PP)} · biblia 680 · pez 600 · camiseta 480 por miembro del equipo.')
for tema, items in RECS:
    doc.add_heading(tema, 3)
    bullets(items)

# ── Anexos ──
doc.add_page_break()
doc.add_heading('Anexo A · Gastos del registro de tesorería', 1)
rows = [['Fecha', 'Concepto', 'RD$']] + [[f, c, m] for f, c, m, _ in gastos] + [['', 'Total', D['GASTOS_TOT']]]
table(rows, widths=[2, 11, 3], bold_last=True, size=9)
doc.add_heading('Anexo B · Donaciones en efectivo', 1)
rows = [['Fecha', 'Donante', 'RD$']] + [[f, dn, m] for f, dn, m, _, _ in donaciones] + [['', 'Total', DONAC]]
table(rows, widths=[2, 11, 3], bold_last=True, size=9)
doc.add_heading('Anexo C · Donaciones en especie', 1)
rows = [['Área', 'Concepto', 'RD$', 'Quién']]
for area, items in especie.items():
    for desc, val, quien in items: rows.append([area, desc, val, quien])
rows.append(['', 'Total', ESPECIE, ''])
table(rows, widths=[2.5, 7, 2.5, 4], bold_last=True, size=9)
doc.add_heading('Anexo D · Entregas del profondo a finanzas', 1)
rows = [['Fecha', 'Concepto', 'RD$']] + [[f, c, m] for f, c, m, _ in profondo] + [['', 'Total', PROFONDO]]
table(rows, widths=[2, 11, 3], bold_last=True, size=9)
doc.add_heading('Anexo E · Verificaciones numéricas', 1)
rows = [['#', 'Verificación', 'Esperado', 'Obtenido']] + [[str(i), ch[0], ch[1], ch[2]] for i, ch in enumerate(checks, 1)]
table(rows, widths=[0.9, 11, 2.6, 2.6], size=8)
para(f'{AUDIT_PASS} de {AUDIT_N} verificaciones cuadran.', italic=True, color=GRIS)

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print(f'✓ Wrote {OUT}')
