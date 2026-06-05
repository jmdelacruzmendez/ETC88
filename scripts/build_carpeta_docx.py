#!/usr/bin/env python3
"""Renderiza preparacion/COPY_GUIA_ETC88.md a un .docx con formato (logo,
encabezados, tablas, viñetas, negritas/cursivas) para VER cómo se vería la
Carpeta del ETC 88. Mismo estilo (Dirección A) que el doc de trabajo.
Salida: entrega_diseno/CARPETA_ETC88.docx
"""
import os, re
import cairosvg
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'preparacion', 'COPY_GUIA_ETC88.md')
OUT = os.path.join(REPO, 'entrega_diseno', 'CARPETA_ETC88.docx')
LOGO_SVG = os.path.join(REPO, 'design', 'logo_eteciano.svg')
LOGO_PNG = os.path.join(REPO, 'design', 'logo_eteciano.png')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
if not os.path.exists(LOGO_PNG):
    cairosvg.svg2png(url=LOGO_SVG, write_to=LOGO_PNG, output_width=900)

AZUL, ARENA, CORAL, TINTA, GRIS = (RGBColor(0x1B,0x3A,0x5C), RGBColor(0xC0,0xA0,0x6C),
    RGBColor(0xE3,0x6C,0x4F), RGBColor(0x1A,0x1A,0x1A), RGBColor(0x66,0x66,0x66))
FUENTE = 'Calibri'

def set_cell_bg(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),hexc)
    tcPr.append(shd)

def add_runs(p, text, size=11, color=TINTA):
    parts = re.split(r'(\*\*[^*]+?\*\*|\*[^*\n]+?\*|`[^`]+?`)', text)
    for part in parts:
        if not part: continue
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith('*') and part.endswith('*'):
            r = p.add_run(part[1:-1]); r.italic = True
        elif part.startswith('`') and part.endswith('`'):
            r = p.add_run(part[1:-1])
        else:
            r = p.add_run(part)
        r.font.name = FUENTE; r.font.size = Pt(size); r.font.color.rgb = color

def h1(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(16); p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text); r.bold = True; r.font.name = FUENTE; r.font.size = Pt(19); r.font.color.rgb = AZUL
    pPr = p._p.get_or_add_pPr(); pBdr = OxmlElement('w:pBdr'); b = OxmlElement('w:bottom')
    b.set(qn('w:val'),'single'); b.set(qn('w:sz'),'8'); b.set(qn('w:space'),'4'); b.set(qn('w:color'),'C0A06C')
    pBdr.append(b); pPr.append(pBdr)

def h2(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text); r.bold = True; r.font.name = FUENTE; r.font.size = Pt(13); r.font.color.rgb = AZUL

def h3(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(7); p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text); r.bold = True; r.font.name = FUENTE; r.font.size = Pt(11); r.font.color.rgb = CORAL

def para(doc, text, italic=False):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; p.paragraph_format.space_after = Pt(4)
    add_runs(p, text)
    if italic:
        for r in p.runs: r.italic = True; r.font.color.rgb = GRIS
    return p

def bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(1)
    add_runs(p, text)

def numbered(doc, num, text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.8); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(f'{num}. '); r.bold = True; r.font.name = FUENTE; r.font.size = Pt(11); r.font.color.rgb = AZUL
    add_runs(p, text)

def callout(doc, lines):
    t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.cell(0,0); set_cell_bg(cell, 'F7F1E3'); cell.width = Cm(16)
    tcPr = cell._tc.get_or_add_tcPr(); tcB = OxmlElement('w:tcBorders')
    for side,color,sz in [('left','E36C4F','24'),('top','E8D4A8','4'),('right','E8D4A8','4'),('bottom','E8D4A8','4')]:
        b = OxmlElement(f'w:{side}'); b.set(qn('w:val'),'single'); b.set(qn('w:sz'),sz); b.set(qn('w:color'),color); tcB.append(b)
    tcPr.append(tcB)
    cell.text = ''
    for j, ln in enumerate(lines):
        p = cell.paragraphs[0] if j == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        add_runs(p, ln, size=10.5, color=AZUL)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

def make_table(doc, headers, rows):
    t = doc.add_table(rows=len(rows)+1, cols=len(headers)); t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j,h in enumerate(headers):
        c = t.cell(0,j); set_cell_bg(c,'1B3A5C'); c.text=''
        p = c.paragraphs[0]; r = p.add_run(h); r.bold=True; r.font.name=FUENTE; r.font.size=Pt(10); r.font.color.rgb=RGBColor(0xFF,0xFF,0xFF)
    for i,rowv in enumerate(rows, start=1):
        for j,val in enumerate(rowv):
            c = t.cell(i,j); c.text=''; add_runs(c.paragraphs[0], val, size=10)

# ===== Parse markdown =====
doc = Document()
for s in doc.sections:
    s.top_margin = s.bottom_margin = Cm(2.0); s.left_margin = s.right_margin = Cm(2.2)

lines = open(SRC, encoding='utf-8').read().split('\n')
i, in_cover, first_section = 0, True, True
while i < len(lines):
    line = lines[i].rstrip()
    stripped = line.lstrip()

    # --- tabla ---
    if stripped.startswith('|'):
        block = []
        while i < len(lines) and lines[i].lstrip().startswith('|'):
            block.append(lines[i].strip()); i += 1
        def cells(r): return [c.strip() for c in r.strip().strip('|').split('|')]
        headers = cells(block[0])
        rows = [cells(b) for b in block[2:]] if len(block) > 2 else []
        make_table(doc, headers, rows)
        continue

    # --- blockquote (callout) ---
    if stripped.startswith('>'):
        block = []
        while i < len(lines) and lines[i].lstrip().startswith('>'):
            block.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
        block = [b for b in block if b.strip()]
        if block: callout(doc, block)
        continue

    # --- títulos ---
    if line.startswith('# '):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(); run.add_picture(LOGO_PNG, width=Inches(1.7)); p.paragraph_format.space_after = Pt(6)
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line[2:]); r.bold=True; r.font.name=FUENTE; r.font.size=Pt(30); r.font.color.rgb=AZUL
        i += 1; continue
    if line.startswith('### '):
        if in_cover:
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_runs(p, line[4:], size=14, color=ARENA)
            for r in p.runs: r.italic = True
        else:
            h3(doc, re.sub(r'\*','',line[4:]))
        i += 1; continue
    if line.startswith('#### '):
        h3(doc, line[5:]); i += 1; continue
    if line.startswith('## '):
        if not first_section: doc.add_page_break()
        first_section = False; in_cover = False
        h1(doc, line[3:]); i += 1; continue

    # --- separador / vacío ---
    if line.startswith('---') or line.strip() == '':
        i += 1; continue

    # --- listas ---
    m = re.match(r'^(\d+)\.\s+(.*)', line)
    if m:
        numbered(doc, m.group(1), m.group(2)); i += 1; continue
    if stripped.startswith('- ') or stripped.startswith('* '):
        bullet(doc, stripped[2:]); i += 1; continue

    # --- párrafo (cursiva si toda la línea es *...* ) ---
    if line.strip().startswith('*') and line.strip().endswith('*') and line.count('*') == 2:
        para(doc, line.strip()[1:-1], italic=True)
    else:
        para(doc, line)
    i += 1

doc.save(OUT)
print(f"Wrote {OUT}")
