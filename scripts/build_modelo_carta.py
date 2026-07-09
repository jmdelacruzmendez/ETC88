#!/usr/bin/env python3
"""
Genera un MODELO VACÍO de carta de donación (.docx) para el ETC 88.

Datos FIJOS del retiro (fechas, casa, contacto, cita) van correctos desde
estado.json. Los datos del DONANTE y del pedido van en blanco con marcadores
[____] para llenar a mano o en Word.

Regla #5: entregable Drive = .docx generado (no markdown escapado).
Regla #1: cifras del retiro cuadran con estado.json (no inventadas).

Salida: entrega_diseno/MODELO_Carta_Donacion_ETC88.docx
"""
import json
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

REPO = Path(__file__).resolve().parent.parent
estado = json.load(open(REPO / 'data/estado.json', encoding='utf-8'))

FECHAS = estado['retiro']['fechas']['valor']          # 4–6 de septiembre de 2026
COSTO = estado['finanzas']['meta_recaudacion_total']['valor']  # 553622

MAR = RGBColor(0x5B, 0x3A, 0x29)      # marrón cuero
GRIS = RGBColor(0x88, 0x88, 0x88)
AZUL = RGBColor(0x0B, 0x1F, 0x3A)

doc = Document()

# Márgenes
for s in doc.sections:
    s.top_margin = Inches(0.8); s.bottom_margin = Inches(0.8)
    s.left_margin = Inches(1.0); s.right_margin = Inches(1.0)

# Estilo base
base = doc.styles['Normal']
base.font.name = 'Georgia'
base.font.size = Pt(11)

def blank(label, width=28):
    """Devuelve una línea con guion bajo para llenar."""
    return f'{label}: ' + '_' * width

def p(text='', *, bold=False, italic=False, size=11, color=None, align=None, space_after=6):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    if align: par.alignment = align
    run = par.add_run(text)
    run.bold = bold; run.italic = italic
    run.font.size = Pt(size)
    if color: run.font.color.rgb = color
    return par

def field(label, hint=''):
    """Campo a llenar: etiqueta en negrita + línea + hint gris opcional."""
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(4)
    r1 = par.add_run(f'{label}: ')
    r1.bold = True
    r2 = par.add_run('_' * 40)
    if hint:
        r3 = par.add_run(f'   ({hint})')
        r3.italic = True; r3.font.size = Pt(9); r3.font.color.rgb = GRIS
    return par

# ─── ENCABEZADO ───
p('ENCUENTRO TOTAL CON CRISTO · ETC 88', bold=True, size=15, color=MAR,
  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
p('Solicitud de donación', italic=True, size=12, color=GRIS,
  align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
p(f'Retiro · {FECHAS} · Casa de Retiro La Ceiba del Salado, Higüey',
  size=9, color=GRIS, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)

# ─── FECHA Y DESTINATARIO ───
field('Fecha', 'día en que se envía')
field('Destinatario', 'nombre de la empresa / persona / parroquia')
field('A la atención de', 'nombre del contacto')
p(space_after=8)

# ─── SALUDO ───
p('Estimado(a) ______________________:', space_after=10)

# ─── CUERPO (fijo + huecos) ───
p('Reciba un cordial saludo de parte de la Co-Dirección del Encuentro Total '
  'con Cristo No. 88 (ETC 88), un retiro espiritual católico para jóvenes que '
  f'se celebrará del {FECHAS} en la Casa de Retiro La Ceiba del Salado, Higüey, '
  'reuniendo a unas 100 personas (participantes y equipo de servicio).',
  space_after=8)

p('Nos dirigimos a usted para solicitar su valioso apoyo a esta obra. '
  'Concretamente, quisiéramos pedirle:', space_after=6)

# Bloque de pedido (a llenar)
pd = doc.add_paragraph(); pd.paragraph_format.space_after = Pt(2)
pd.add_run('   ▢ Producto / bien específico: ').bold = True
pd.add_run('_' * 34)
pd2 = doc.add_paragraph(); pd2.paragraph_format.space_after = Pt(2)
pd2.add_run('   ▢ Donación en especie: ').bold = True
pd2.add_run('_' * 40)
pd3 = doc.add_paragraph(); pd3.paragraph_format.space_after = Pt(2)
pd3.add_run('   ▢ Aporte económico a un rubro: RD$ ').bold = True
pd3.add_run('_' * 20)
pd4 = doc.add_paragraph(); pd4.paragraph_format.space_after = Pt(10)
pd4.add_run('   ▢ Otro: ').bold = True
pd4.add_run('_' * 48)

p('Su generosidad hace posible que más jóvenes vivan esta experiencia de fe. '
  'En reconocimiento, ofrecemos:', space_after=6)
p('   •  Constancia de donación firmada por la Co-Dirección.', space_after=2)
p('   •  Mención en nuestros agradecimientos (si usted lo autoriza).', space_after=2)
p('   •  Una cadena de oración por sus intenciones durante el retiro.', space_after=10)

p('Quedamos a su disposición para cualquier información adicional. '
  'Agradecemos de antemano su tiempo y su apoyo a esta misión.', space_after=14)

# ─── CIERRE / CITA ───
p('«Ya no os llamo siervos, os he llamado amigos.» — Jn 15,15',
  italic=True, color=MAR, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)

# ─── FIRMA ───
p('Siempre amigos,', space_after=18)
p('_' * 34, space_after=2)
p('Co-Dirección · ETC 88', bold=True, space_after=1)
p('Juan Manuel de la Cruz  ·  Jean Carlo de la Cruz', size=10, space_after=1)
p('WhatsApp: ____________________', size=9, color=GRIS, space_after=14)

# ─── PIE: FICHA TÉCNICA ───
p('— — — — — — — — — — — — — — — — — — — — — — — — — — — — —',
  color=GRIS, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
p('FICHA TÉCNICA DEL RETIRO', bold=True, size=9, color=AZUL, space_after=3)
ficha = (
    f'Fechas: {FECHAS}.  ·  Lugar: Casa de Retiro La Ceiba del Salado, Higüey.  ·  '
    '100 personas en casa (participantes + equipo de servicio).  ·  '
    'Origen: San Pedro de Macorís (mayoría), Higüey, Punta Cana.  ·  '
    'Asesores Espirituales: P. Paul Ramírez y Hna. Angelina Lebrón.  ·  '
    'Co-Dirección: Juan Manuel y Jean Carlo de la Cruz.  ·  '
    f'Costo total estimado del retiro: RD$ {COSTO:,}.'
)
p(ficha, size=8, color=GRIS, space_after=2)
p('Toda donación se respalda con una constancia firmada por la Co-Dirección.',
  size=8, italic=True, color=GRIS)

out = REPO / 'entrega_diseno/MODELO_Carta_Donacion_ETC88.docx'
doc.save(out)
print(f'Wrote {out}')
