#!/usr/bin/env python3
"""Genera los 2 .docx OFICIALES del ETC 88 con python-docx.

Por qué .docx y no markdown/text: Google Drive, al importar text/plain, trata el
contenido como markdown y ESCAPA los símbolos (\\-, \\[, \\#, \\=) y rompe los emoji.
python-docx produce encabezados, viñetas y tablas REALES → Google Docs los importa
limpios.

Fuente: SOLO data/equipo.json + data/estado.json. Nunca hardcodea nombres ni cifras.
Las propuestas se renderizan con [PROPUESTA]; lo que falta con [POR DEFINIR].

Salidas:
  1. Documento_Asesores_ETC88.docx  — consolidado para Dirección/Asesores.
  2. Carpeta_F1_ETC88.docx          — Guía del ETC + Guía de Guías + Anexo Cocina.
"""
import json, re, os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

REPO = '/home/user/ETC88'
D = json.load(open(f'{REPO}/data/equipo.json'))
EST = D['estado']

TINTA = RGBColor(0x1C, 0x14, 0x0B)
MAR   = RGBColor(0x1B, 0x3A, 0x52)
TIERRA= RGBColor(0xB2, 0x50, 0x28)

# ---------------------------------------------------------------- helpers ----
def _v(node):
    return node['valor'] if isinstance(node, dict) and 'valor' in node else node

def flag(node):
    """Prefijo visible según el estado del nodo."""
    st = node.get('estado') if isinstance(node, dict) else None
    return {'propuesta': '[PROPUESTA] ', 'pendiente': '[POR DEFINIR] '}.get(st, '')

def money(v):
    return f"RD${v:,}" if isinstance(v, (int, float)) else str(v)

def add_runs(p, text):
    """Añade runs interpretando **negrita** y *cursiva* (evita markdown crudo)."""
    pos = 0
    for m in re.finditer(r'\*\*(.+?)\*\*|\*(.+?)\*', text):
        if m.start() > pos:
            p.add_run(text[pos:m.start()])
        if m.group(1) is not None:
            p.add_run(m.group(1)).bold = True
        else:
            p.add_run(m.group(2)).italic = True
        pos = m.end()
    if pos < len(text):
        p.add_run(text[pos:])
    return p

def strip_md(t):
    return t.replace('**', '').replace('*', '').strip()

def base_style(doc):
    st = doc.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(11)

def cover(doc, titulo, subtitulo):
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = t.add_run(titulo); run.bold = True; run.font.size = Pt(24); run.font.color.rgb = MAR
    s = doc.add_paragraph(); s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = s.add_run(subtitulo); sr.italic = True; sr.font.size = Pt(12); sr.font.color.rgb = TIERRA

def legend(doc):
    p = doc.add_paragraph()
    p.add_run('Cómo leer este documento: ').bold = True
    p.add_run('lo que aparece sin marca está ')
    p.add_run('confirmado').bold = True
    p.add_run('. ')
    p.add_run('[PROPUESTA]').bold = True
    p.add_run(' = sugerencia aún no decidida. ')
    p.add_run('[POR DEFINIR]').bold = True
    p.add_run(' = falta el dato o la decisión. Generado desde data/estado.json + data/equipo.json.')

# ----------------------------------------------- markdown -> docx (Doc 2) ----
def render_md(doc, md):
    lines = md.split('\n')
    i, n = 0, len(lines)
    while i < n:
        line = lines[i].rstrip()
        s = line.strip()
        # Tabla: encabezado + línea separadora |---|---|
        if s.startswith('|') and i + 1 < n and re.match(r'^\s*\|[\s:|\-]+\|\s*$', lines[i + 1]):
            header = [c.strip() for c in s.strip('|').split('|')]
            i += 2
            body = []
            while i < n and lines[i].strip().startswith('|'):
                body.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            tbl = doc.add_table(rows=1, cols=len(header))
            tbl.style = 'Light Grid Accent 1'
            for j, h in enumerate(header):
                cp = tbl.rows[0].cells[j].paragraphs[0]
                add_runs(cp, h)
                for rr in cp.runs:
                    rr.bold = True
            for rowcells in body:
                cells = tbl.add_row().cells
                for j, c in enumerate(rowcells):
                    if j < len(cells):
                        add_runs(cells[j].paragraphs[0], c)
            doc.add_paragraph()
            continue
        if s.startswith('### '):
            doc.add_heading(strip_md(s[4:]), level=3)
        elif s.startswith('## '):
            doc.add_heading(strip_md(s[3:]), level=2)
        elif s.startswith('# '):
            doc.add_heading(strip_md(s[2:]), level=1)
        elif s == '---' or s == '>':
            pass
        elif s.startswith('> '):
            add_runs(doc.add_paragraph(style='Intense Quote'), s[2:])
        elif re.match(r'^[-*] ', s):
            add_runs(doc.add_paragraph(style='List Bullet'), s[2:])
        elif re.match(r'^\d+\. ', s):
            add_runs(doc.add_paragraph(style='List Number'), re.sub(r'^\d+\. ', '', s))
        elif s == '':
            pass
        else:
            add_runs(doc.add_paragraph(), s)
        i += 1

# ============================================================================
# DOC 1 · Documento de Asesores (data-driven)
# ============================================================================
def build_asesores():
    doc = Document(); base_style(doc)
    ret = EST['retiro']
    cover(doc, 'ETC 88 · Documento de Asesores',
          f"{_v(ret['fechas'])} · {_v(ret['lugar'])}")
    co = ' y '.join(_v(ret['co_direccion']))
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(f"Co-dirección: {co}").italic = True
    legend(doc)

    # 1. El equipo
    doc.add_heading('1. El equipo del ETC 88', level=1)
    op = [x for x in D['equipo'] if x.get('operativo')]
    doc.add_paragraph(f"{len(op)} servidores operativos + asesores ampliados y transversales. "
                      "Una sola tripulación, diferentes funciones.")
    AREAS = [('directores', 'Directores'), ('asesores', 'Asesores'),
             ('asesores_espirituales', 'Asesores Espirituales (transversales)'),
             ('guias', 'Guías'), ('cocina', 'Cocina'), ('musica', 'Música')]
    for area, label in AREAS:
        ms = [x for x in D['equipo'] if x['area'] == area
              and x.get('operativo') and not x.get('vacante') and not x.get('backup')]
        if not ms:
            continue
        doc.add_heading(f"{label} ({len(ms)})", level=2)
        ms.sort(key=lambda x: (0 if 'coord' in x['rol'].lower() else 1, x['nombre']))
        for x in ms:
            nm = x['nombre'].replace(' (sin formulario)', '')
            pr = doc.add_paragraph(style='List Bullet')
            pr.add_run(nm).bold = True
            pr.add_run(f" · {x['rol']}")

    # Vacante / backups / asesores externos
    vac = [x for x in D['equipo'] if x.get('vacante')]
    bks = [x for x in D['equipo'] if x.get('backup')]
    ac  = [x for x in D['equipo'] if x['area'] == 'asesores_cocina']
    ad  = [x for x in D['equipo'] if x['area'] == 'asesores_diocesanos']
    doc.add_heading('Vacantes, backups y asesores externos', level=2)
    if vac:
        for x in vac:
            doc.add_paragraph(f"[POR DEFINIR] {x['nombre']}", style='List Bullet')
    if bks:
        doc.add_paragraph('Backups (no son parte del equipo per se): '
                          + ' · '.join(x['nombre'] for x in bks), style='List Bullet')
    if ac:
        doc.add_paragraph('Asesoras de cocina: '
                          + ' · '.join(x['nombre'] for x in ac), style='List Bullet')
    if ad:
        doc.add_paragraph('Asesores de comunidad: '
                          + ' · '.join(x['nombre'] for x in ad), style='List Bullet')

    # 2. Cronograma
    doc.add_heading('2. Cronograma 2026', level=1)
    MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
    tbl = doc.add_table(rows=1, cols=2); tbl.style = 'Light Grid Accent 1'
    for j, h in enumerate(['Fecha', 'Actividad']):
        tbl.rows[0].cells[j].paragraphs[0].add_run(h).bold = True
    for e in D['calendario']:
        try:
            y, m, dd = e['fecha'].split('-'); fecha = f"{int(dd)}-{MESES[int(m) - 1]}"
        except Exception:
            fecha = e['fecha']
        cells = tbl.add_row().cells
        cells[0].paragraphs[0].add_run(fecha)
        cells[1].paragraphs[0].add_run(e['titulo'] + (' (sin formación)' if e.get('sin_formacion') else ''))

    # 3. Finanzas
    doc.add_heading('3. Finanzas (resumen)', level=1)
    ef = EST['finanzas']
    def fin_line(label, node, fmt=money):
        pr = doc.add_paragraph(style='List Bullet')
        pr.add_run(f"{label}: ").bold = True
        pr.add_run(flag(node) + fmt(_v(node)))
        if isinstance(node, dict) and node.get('nota'):
            pr.add_run(f" — {node['nota']}").italic = True
    fin_line('Casa por persona (sin exención)', ef['casa_por_persona_sin_exencion'])
    fin_line('Casa por persona (con exención)', ef['casa_por_persona_con_exencion'])
    fin_line('Deuda inicial al Consejo', ef['deuda_inicial'])
    fin_line('Cuota de participante', ef['cuota_participante'])
    cq = ef['cuota_equipo']
    pr = doc.add_paragraph(style='List Bullet')
    pr.add_run('Cuota del equipo: ').bold = True
    pr.add_run(flag(cq) + f"${_v(cq)['total_rango']} total · ${_v(cq)['mensual']}/mes · cubre {_v(cq)['cubre']}")
    pr.add_run(f" — {cq['nota']}").italic = True
    fin_line('Meta de recaudación', ef['meta_recaudacion_total'])
    fin_line('Participantes (estimado)', ef['participantes_estimado'], fmt=lambda v: str(v))

    # 4. Recaudación
    doc.add_heading('4. Recaudación', level=1)
    er = EST['recaudacion']
    for key, label in [('profondo1_rifa_neta', 'Rifa (Profondo #1, neta)'),
                       ('profondo2_comida_garaje', 'Profondo #2 (comida / garaje)'),
                       ('donaciones_empresas', 'Donaciones empresas/particulares')]:
        fin_line(label, er[key])
    doc.add_paragraph('La primera actividad es una rifa (confirmado, por recomendación del equipo).',
                      style='List Bullet')

    # 5. Equipos auxiliares
    doc.add_heading('5. Equipos auxiliares', level=1)
    for a in D['equipos_auxiliares']:
        pr = doc.add_paragraph(style='List Bullet')
        pr.add_run(a['nombre'] + ': ').bold = True
        pr.add_run(a['descripcion'])
        resp_tag = '[POR DEFINIR] ' if a.get('responsable_estado') == 'pendiente' \
            else ('[PROPUESTA] ' if a.get('responsable_estado') == 'propuesta' else '')
        pr.add_run(f" Responsable: {resp_tag}{a['responsable_sugerido']}.").italic = True

    # 6. Decisiones confirmadas / 7. Pendientes
    doc.add_heading('6. Decisiones confirmadas', level=1)
    for d in EST['decisiones_confirmadas']:
        doc.add_paragraph(d, style='List Bullet')
    doc.add_heading('7. Pendientes (decisiones tuyas — no las invento)', level=1)
    for d in EST['pendientes']:
        doc.add_paragraph('[POR DEFINIR] ' + d, style='List Bullet')

    # 8. Alertas de salud (para asesores/cocina)
    doc.add_heading('8. Alertas clave de salud y convivencia', level=1)
    sal = D.get('salud', {})
    al = sal.get('alergias_alimentarias', {})
    if al:
        doc.add_paragraph('Alergias alimentarias: '
                          + ' · '.join(f"{k} ({len(v)})" for k, v in al.items()), style='List Bullet')
    for amb in sal.get('ambiente_higuey', []):
        doc.add_paragraph(amb, style='List Bullet')

    foot = doc.add_paragraph()
    foot.add_run('Documento generado automáticamente desde data/estado.json + data/equipo.json. '
                 'No editar a mano: cambiar los datos y regenerar.').italic = True
    out = f'{REPO}/Documento_Asesores_ETC88.docx'
    doc.save(out)
    return out

# ============================================================================
# DOC 2 · Carpeta (F1) — consolida las 3 guías .md
# ============================================================================
def build_carpeta():
    doc = Document(); base_style(doc)
    ret = EST['retiro']
    cover(doc, 'ETC 88 · Carpeta (F1)', f"{_v(ret['fechas'])} · {_v(ret['lugar'])}")
    legend(doc)
    partes = ['GUIA_ETC88.md', 'GUIA_DE_GUIAS_88.md', 'ANEXO_COCINA_88.md']
    for k, fn in enumerate(partes):
        path = f'{REPO}/{fn}'
        if not os.path.exists(path):
            continue
        if k > 0:
            doc.add_page_break()
        render_md(doc, open(path, encoding='utf-8').read())
    out = f'{REPO}/Carpeta_F1_ETC88.docx'
    doc.save(out)
    return out

if __name__ == '__main__':
    o1 = build_asesores()
    o2 = build_carpeta()
    print(f"Wrote {os.path.basename(o1)} + {os.path.basename(o2)}")
