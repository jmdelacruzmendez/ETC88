#!/usr/bin/env python3
import os as _os
_R = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
"""Presentación (PPTX) del Tablero de la Misión 88 — para enviar como deck.

MISMAS cifras confirmadas que el tablero (data/estado.json). No inventa nada:
todo sale de finanzas/marca/retiro. Tema espacial, 16:9.

Salida: Presentacion_ETC88.pptx
Uso: python scripts/build_pptx.py
"""
import json, datetime as dt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

REPO = f'{_R}'
E = json.load(open(f'{REPO}/data/estado.json', encoding='utf-8'))
F = E['finanzas']; M = E['marca']; RET = E['retiro']
def v(x): return x['valor'] if isinstance(x, dict) and 'valor' in x else x
def money(n): return "RD$ " + format(int(round(n)), ",d")

meta = v(F['meta_recaudacion_total']); dg = F['meta_recaudacion_total']['desglose']
cuotas = dg['cuotas_firmes']; brecha = dg['brecha_tras_cuotas']; cob = dg['cobertura_cuotas_pct']
costo_pp = dg['costo_por_persona_100']; especie = dg['especie_potencial']
caja_obj = dg['plan_a_caja_objetivo']
cuota_part = v(F['cuota_participante']); CEQ = v(F['cuota_equipo']); cuota_eq = CEQ['total']
rubros = sorted(F['rubros_simulador']['items'], key=lambda r: -r['monto'])
donables = [r['nombre'] for r in F['rubros_simulador']['items'] if r.get('donable')]
fc = F['plan_recaudacion']['fuentes_caja_plan_a']
cita = M['cita_mision_88']; contactos = M['contacto_whatsapp']['contactos']

MES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
hoy = dt.date.today(); HOY_TXT = f"{hoy.day} de {MES[hoy.month-1]} de {hoy.year}"
def days_to(y, m, d): return max(0, (dt.date(y, m, d) - hoy).days)
dias_ret = days_to(2026, 9, 4)

# ----- paleta (tema espacial, igual que el tablero) -----
BG='0E1A2E'; CARD='16243B'; LINE='2A3950'; INK='E8EDF2'; MUT='93A4B8'
GOLD='F2C572'; GREEN='34D399'; RED='FC5130'; SKY='38BDF8'
BARC=['38BDF8','34D399','F2C572','FC5130','A78BFA','22D3EE','F472B6','60A5FA','FBBF24','2DD4BF','FB7185']

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
def rgb(h): return RGBColor.from_string(h)

def slide():
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = rgb(BG); r.line.fill.background(); r.shadow.inherit = False
    return s

def rect(s, x, y, w, h, fill=None, line=None, lw=1.0, rounded=False, rad=0.10):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded:
        try: shp.adjustments[0] = rad
        except Exception: pass
    if fill: shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill)
    else: shp.fill.background()
    if line: shp.line.color.rgb = rgb(line); shp.line.width = Pt(lw)
    else: shp.line.fill.background()
    shp.shadow.inherit = False
    return shp

def lines(s, x, y, w, h, items, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in (0.02,):
        tf.margin_left = Inches(0.06); tf.margin_right = Inches(0.06); tf.margin_top = Inches(0.02); tf.margin_bottom = Inches(0.02)
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = it.get('align', align)
        if 'sa' in it: p.space_after = Pt(it['sa'])
        if 'sb' in it: p.space_before = Pt(it['sb'])
        if 'ls' in it: p.line_spacing = it['ls']
        r = p.add_run(); r.text = it['t']
        r.font.size = Pt(it.get('sz', 16)); r.font.bold = it.get('b', False); r.font.italic = it.get('i', False)
        r.font.name = it.get('f', 'Calibri'); r.font.color.rgb = rgb(it.get('c', INK))
    return tb

def title(s, t, sub=None):
    rect(s, 0.7, 0.55, 0.12, 0.62, fill=GOLD)
    lines(s, 0.95, 0.5, 11.6, 0.8, [{'t': t, 'sz': 30, 'b': True, 'c': INK}])
    if sub: lines(s, 0.97, 1.18, 11.6, 0.5, [{'t': sub, 'sz': 14, 'c': MUT}])

LOGO = f'{REPO}/data/logo_etc.png'

# ============ 1. PORTADA ============
s = slide()
try: s.shapes.add_picture(LOGO, Inches((13.333-2.0)/2), Inches(0.85), width=Inches(2.0))
except Exception: pass
lines(s, 1, 3.05, 11.333, 1.0, [{'t': 'ETC · Misión 88', 'sz': 46, 'b': True, 'c': INK, 'align': PP_ALIGN.CENTER}], align=PP_ALIGN.CENTER)
lines(s, 1, 4.0, 11.333, 0.9, [
    {'t': 'Encuentro Total con Cristo', 'sz': 20, 'c': GOLD, 'align': PP_ALIGN.CENTER, 'sa': 4},
    {'t': f"{v(RET['fechas'])} · {v(RET['lugar'])}", 'sz': 15, 'c': MUT, 'align': PP_ALIGN.CENTER},
], align=PP_ALIGN.CENTER)
lines(s, 1, 5.25, 11.333, 1.0, [
    {'t': f"«{cita['valor']}»", 'sz': 18, 'i': True, 'c': INK, 'align': PP_ALIGN.CENTER, 'sa': 2},
    {'t': cita['cita'], 'sz': 13, 'c': MUT, 'align': PP_ALIGN.CENTER},
], align=PP_ALIGN.CENTER)
lines(s, 1, 6.85, 11.333, 0.4, [{'t': f"Tablero de la Tripulación · actualizado: {HOY_TXT}", 'sz': 11, 'c': MUT, 'align': PP_ALIGN.CENTER}], align=PP_ALIGN.CENTER)

# ============ 2. LA MISIÓN EN NÚMEROS ============
s = slide(); title(s, 'La misión en números', 'De un vistazo: cuánto cuesta, cuánto ya ponemos y cuánto falta')
kpis = [('COSTO DE LA MISIÓN', money(meta), INK, 'el retiro completo'),
        ('LO QUE YA PONEMOS', money(cuotas), GREEN, 'cuotas de participantes + equipo'),
        ('FALTA POR REUNIR', money(brecha), RED, 'y depende de nosotros'),
        ('DÍAS AL RETIRO', str(dias_ret), SKY, f"{v(RET['fechas'])}")]
x = 0.7; cw = 2.92; gap = 0.13
for lbl, val, col, note in kpis:
    rect(s, x, 1.95, cw, 1.95, fill=CARD, line=LINE, rounded=True, rad=0.06)
    rect(s, x, 1.95, cw, 0.07, fill=col)
    lines(s, x+0.18, 2.2, cw-0.36, 1.6, [
        {'t': lbl, 'sz': 11, 'b': True, 'c': MUT, 'sa': 8},
        {'t': val, 'sz': 26, 'b': True, 'c': col, 'sa': 6},
        {'t': note, 'sz': 11, 'c': MUT},
    ])
    x += cw + gap
# barra de progreso
lines(s, 0.7, 4.35, 11.9, 0.4, [{'t': f"Cubierto con cuotas: {cob}%  ·  falta {money(brecha)} por levantar entre todos", 'sz': 14, 'b': True, 'c': INK}])
rect(s, 0.7, 4.95, 11.9, 0.5, fill='0B1424', line=LINE, rounded=True, rad=0.5)
rect(s, 0.72, 4.97, 11.86*(cob/100.0), 0.46, fill=GREEN, rounded=True, rad=0.5)
lines(s, 0.7, 5.7, 11.9, 1.3, [
    {'t': f"Imprevistos incluidos (10% = {money(dg['imprevistos_10pct'])}).  Además hay un potencial de {money(especie)} en ESPECIE (no es caja: reduce el costo peso a peso).", 'sz': 12.5, 'c': MUT, 'ls': 1.2},
], anchor=MSO_ANCHOR.TOP)

# ============ 3. ¿EN QUÉ SE VA EL DINERO? ============
s = slide(); title(s, '¿En qué se va el dinero?', f"Estructura del costo (incluye 10% de imprevistos) — total {money(meta)}")
mx = rubros[0]['monto']; y = 1.85; bar_x = 4.15; bar_max = 6.2; row_h = 0.46
for i, r in enumerate(rubros):
    lines(s, 0.7, y-0.04, 3.35, row_h, [{'t': r['nombre'] + ('  ·  donable' if r.get('donable') else ''), 'sz': 12.5, 'c': INK if not r.get('donable') else GREEN}], anchor=MSO_ANCHOR.MIDDLE)
    w = max(0.08, bar_max*(r['monto']/mx))
    rect(s, bar_x, y+0.04, w, row_h-0.16, fill=BARC[i % len(BARC)], rounded=True, rad=0.5)
    lines(s, bar_x+bar_max+0.15, y-0.04, 1.9, row_h, [{'t': money(r['monto']), 'sz': 12.5, 'b': True, 'c': INK, 'align': PP_ALIGN.RIGHT}], anchor=MSO_ANCHOR.MIDDLE)
    y += row_h
lines(s, 0.7, y+0.05, 11.9, 0.4, [{'t': 'En verde, los rubros más realistas de conseguir en ESPECIE (donación en producto).', 'sz': 11.5, 'i': True, 'c': MUT}])

# ============ 4. COSTO POR PERSONA Y CUOTAS ============
s = slide(); title(s, 'Costo por persona y cuotas', f"La misión cuesta {money(costo_pp)} por persona (base 100). La cuota es solo una parte.")
cards = [('PARTICIPANTE', money(cuota_part), 'de cuota', SKY,
          ['Cubre su parte de casa, comida, transporte,', 'biblia y pez. El resto se levanta entre todos.']),
         ('EQUIPO (SERVIDOR)', money(cuota_eq), 'de cuota', GREEN,
          [CEQ.get('nota_plan_pago', '500/mes × 4 meses (jun–sep).'), 'Cada servidor también aporta su cuota.'])]
x = 0.9
for lbl, val, suf, col, notes in cards:
    rect(s, x, 2.1, 5.55, 3.2, fill=CARD, line=LINE, rounded=True, rad=0.05)
    rect(s, x, 2.1, 5.55, 0.09, fill=col)
    body = [{'t': lbl, 'sz': 14, 'b': True, 'c': MUT, 'sa': 10},
            {'t': val + '  ', 'sz': 40, 'b': True, 'c': col, 'sa': 0},
            {'t': suf, 'sz': 13, 'c': MUT, 'sa': 12}]
    for n in notes: body.append({'t': n, 'sz': 13, 'c': INK, 'sa': 4, 'ls': 1.15})
    lines(s, x+0.35, 2.45, 4.9, 2.7, body)
    x += 5.95
lines(s, 0.9, 5.6, 11.5, 1.0, [
    {'t': f"Las cuotas suman {money(cuotas)} ({cob}% del costo). Faltan {money(brecha)} que reunimos como tripulación: rifa, ventas y donaciones.", 'sz': 13.5, 'c': INK, 'ls': 1.2}])

# ============ 5. PLAN A DE RECAUDACIÓN ============
s = slide(); title(s, 'Cómo lo hacemos posible', f"Plan A de recaudación — caja objetivo {money(caja_obj)}")
rows = [('Cuotas (equipo + participantes)', fc['cuotas']['monto'], 'firme', 'ya comprometido'),
        ('Rifa / Profondo', fc['rifa_profondo']['monto'], f"{fc['rifa_profondo']['prob']}%", fc['rifa_profondo'].get('nota','')),
        ('Venta de garaje', fc['venta_garaje']['monto'], f"{fc['venta_garaje']['prob']}%", fc['venta_garaje'].get('nota','')),
        ('Venta de comida', fc['venta_comida']['monto'], f"{fc['venta_comida']['prob']}%", fc['venta_comida'].get('nota','')),
        ('Donaciones en efectivo', fc['donaciones_efectivo']['monto'], f"{fc['donaciones_efectivo']['prob']}%", fc['donaciones_efectivo'].get('nota',''))]
hdr = ['Fuente', 'Monto', 'Prob.', 'Cómo']
colx = [0.7, 4.7, 6.4, 7.5]; colw = [4.0, 1.7, 1.1, 5.1]
ty = 1.95; rh = 0.62
# header
for j, h in enumerate(hdr):
    lines(s, colx[j], ty, colw[j], rh, [{'t': h, 'sz': 12, 'b': True, 'c': GOLD, 'align': PP_ALIGN.RIGHT if j==1 else PP_ALIGN.LEFT}], anchor=MSO_ANCHOR.MIDDLE)
ty += 0.5
for name, mon, prob, nota in rows:
    rect(s, 0.7, ty, 11.9, rh, fill=CARD, line=LINE, rounded=True, rad=0.08)
    lines(s, colx[0]+0.12, ty, colw[0]-0.2, rh, [{'t': name, 'sz': 12.5, 'b': True, 'c': INK}], anchor=MSO_ANCHOR.MIDDLE)
    lines(s, colx[1], ty, colw[1]-0.15, rh, [{'t': money(mon), 'sz': 12.5, 'b': True, 'c': INK, 'align': PP_ALIGN.RIGHT}], anchor=MSO_ANCHOR.MIDDLE)
    lines(s, colx[2]+0.15, ty, colw[2], rh, [{'t': prob, 'sz': 11.5, 'c': GREEN if prob=='firme' else MUT}], anchor=MSO_ANCHOR.MIDDLE)
    lines(s, colx[3]+0.1, ty, colw[3]-0.2, rh, [{'t': nota, 'sz': 11, 'c': MUT}], anchor=MSO_ANCHOR.MIDDLE)
    ty += rh + 0.1
rect(s, 0.7, ty, 11.9, rh, fill='13402F', line=GREEN, rounded=True, rad=0.08)
lines(s, colx[0]+0.12, ty, colw[0], rh, [{'t': 'TOTAL caja objetivo', 'sz': 12.5, 'b': True, 'c': GREEN}], anchor=MSO_ANCHOR.MIDDLE)
lines(s, colx[1], ty, colw[1]-0.15, rh, [{'t': money(caja_obj), 'sz': 13, 'b': True, 'c': GREEN, 'align': PP_ALIGN.RIGHT}], anchor=MSO_ANCHOR.MIDDLE)
lines(s, colx[3]+0.1, ty, colw[3], rh, [{'t': f"+ {money(especie)} en especie (no es caja)", 'sz': 11, 'i': True, 'c': MUT}], anchor=MSO_ANCHOR.MIDDLE)

# ============ 6. CÓMO AYUDAR ============
s = slide(); title(s, 'Cómo ser parte de la misión', f"Faltan {dias_ret} días para el retiro ({v(RET['fechas'])})")
blocks = [('🎁  Apadrina un rubro (en especie)', GOLD, [', '.join(donables[:3]) + ',', ', '.join(donables[3:]) + '.', 'Donar el producto reduce el costo directo.']),
          ('💛  Aporta a lo que falta', GREEN, [f"Cualquier aporte al fondo de {money(brecha)}.", 'O pide una carta de donación formal', 'para tu empresa, fundación o padrino.']),
          ('📲  Escríbele a la Co-Dirección', SKY, [f"{c['nombre']}: {c['wa'][1:][:3]}-{c['wa'][1:][3:6]}-{c['wa'][1:][6:]}" for c in contactos] + ['(WhatsApp)'])]
x = 0.7; cw = 3.9
for head, col, body in blocks:
    rect(s, x, 2.0, cw, 3.7, fill=CARD, line=LINE, rounded=True, rad=0.05)
    rect(s, x, 2.0, cw, 0.09, fill=col)
    items = [{'t': head, 'sz': 14.5, 'b': True, 'c': col, 'sa': 12}]
    for b in body: items.append({'t': b, 'sz': 13, 'c': INK, 'sa': 7, 'ls': 1.12})
    lines(s, x+0.3, 2.35, cw-0.6, 3.1, items)
    x += cw + 0.1
lines(s, 0.7, 6.05, 11.9, 1.0, [{'t': 'Cada peso, cada producto y cada oración hacen la misión posible. Gracias por ser tripulación.', 'sz': 13, 'i': True, 'c': MUT, 'align': PP_ALIGN.CENTER}], align=PP_ALIGN.CENTER)

# ============ 7. CIERRE ============
s = slide()
try: s.shapes.add_picture(LOGO, Inches((13.333-1.5)/2), Inches(1.4), width=Inches(1.5))
except Exception: pass
lines(s, 1, 3.4, 11.333, 1.6, [
    {'t': f"«{cita['valor']}»", 'sz': 30, 'i': True, 'b': True, 'c': GOLD, 'align': PP_ALIGN.CENTER, 'sa': 6},
    {'t': cita['cita'], 'sz': 16, 'c': MUT, 'align': PP_ALIGN.CENTER},
], align=PP_ALIGN.CENTER)
lines(s, 1, 5.6, 11.333, 0.8, [
    {'t': 'Gracias por ser tripulación.', 'sz': 18, 'b': True, 'c': INK, 'align': PP_ALIGN.CENTER, 'sa': 3},
    {'t': 'Encuentro Total con Cristo · Misión 88', 'sz': 13, 'c': MUT, 'align': PP_ALIGN.CENTER},
], align=PP_ALIGN.CENTER)

OUT = f'{REPO}/Presentacion_ETC88.pptx'
prs.save(OUT)
print(f"Wrote {OUT}  ({len(prs.slides)} slides)")
print(f"  meta {money(meta)} · cuotas {money(cuotas)} · brecha {money(brecha)} · días {dias_ret}")
print(f"  actualizado: {HOY_TXT}")
