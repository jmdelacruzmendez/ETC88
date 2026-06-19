#!/usr/bin/env python3
"""Genera el Tablero de la Tripulación ETC 88 (Misión 88) — UN archivo HTML
autocontenido (HTML + CSS + JS nativo, sin dependencias ni CDNs).

IMPORTANTE (legibilidad en móvil): el contenido se RENDERIZA en el HTML (server-
side, aquí en Python). El JavaScript solo MEJORA (cuenta regresiva en vivo,
animaciones, simulador interactivo). Así el tablero se ve completo aunque se abra
en una vista previa del teléfono que no ejecute JavaScript (WhatsApp, Drive,
visor de archivos). Para interactuar (simulador) hace falta abrirlo en un
navegador real.

Ejercicio de concientización, tono sencillo, tema espacial. Orden narrativo:
  hook → KPIs → estructura (pastel) → costo por persona → cuotas → simulador
  (cohete) → áreas → cuenta regresiva → presupuesto completo (desplegable).

Cifras desde data/estado.json; detalle del presupuesto desde el Maestro xlsx.
Uso: python scripts/build_campana.py
"""
import json
import os
import base64
import urllib.parse
import datetime as dt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EST = json.load(open(os.path.join(REPO, 'data', 'estado.json'), encoding='utf-8'))

fin = EST['finanzas']
meta_blk = fin['meta_recaudacion_total']
desg = meta_blk['desglose']
cpp = fin['costos_por_persona']
corr = fin['corresponsabilidad_areas']
av = fin['avanzada_estimada']
sim = fin['rubros_simulador']
exentos = fin['cuota_equipo_exentos']['asumidos_por_codireccion']
cita = EST['marca']['cita_mision_88']

meta    = meta_blk['valor']
cuotas  = desg['cuotas_firmes']
brecha  = desg['brecha_tras_cuotas']

cuota_part = fin['cuota_participante']['valor']
n_part     = fin['participantes_objetivo']['valor']
part_cuota_total = cuota_part * n_part
equipo_cuotas = cuotas - part_cuota_total
eq_pago  = fin['cuota_equipo']['valor']['mensual']
eq_total = fin['cuota_equipo']['valor']['total']
eq_pagos = eq_total // eq_pago
n_equipo = equipo_cuotas // eq_total

pdesg = cpp['participante']['desglose_persona']
edesg = cpp['equipo']['desglose_persona']
part_costo = cpp['participante']['con_imprevistos_persona']
eq_costo   = cpp['equipo']['con_imprevistos_persona']
part_oper  = cpp['participante']['operativo_persona']
eq_oper    = cpp['equipo']['operativo_persona']

PART_LBL = [('casa', 'Casa (hospedaje)'), ('cocina', 'Comida del retiro'), ('biblias_y_peces', 'Biblia + pez'),
            ('transporte', 'Su transporte'), ('guias', 'Materiales de su PG'), ('liturgico', 'Litúrgico'), ('musica', 'Música')]
EQ_LBL = [('casa', 'Casa (hospedaje)'), ('transporte', 'Transporte (equipo + clausura)'), ('camisetas', 'Camiseta'),
          ('eventos_formativos', 'Formación'), ('almuerzo_ensayo', 'Almuerzo del ensayo'), ('liturgico', 'Litúrgico'), ('musica', 'Música')]
desg_part = [{"label": lbl, "monto": pdesg[k]} for k, lbl in PART_LBL]
desg_eq   = [{"label": lbl, "monto": edesg[k]} for k, lbl in EQ_LBL]
estructura = [{"label": r['nombre'], "monto": r['monto']} for r in sim['items']]
cubre_part = ["Transporte al retiro", "Comida del retiro", "Casa (hospedaje)", "Pez", "Biblia"]
cubre_eq = ["Ensayo general", "Prorrateo del salón", "Transporte al retiro", "Comida del ensayo", "Camiseta del equipo"]

FECHA_CPAGO = "2026-08-30"; FECHA_CPAGO_T = "30 de agosto de 2026"
FECHA_RET = "2026-09-04"; FECHA_RET_T = "4 – 6 de septiembre de 2026"
ACTUALIZADO = "17 de junio de 2026"

# detalle del presupuesto (Maestro)
presupuesto = []
sub_operativo = 0
try:
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(REPO, 'data', 'presupuesto', 'ETC88_Presupuesto_Maestro.xlsx'), data_only=True)['01 · LADO A Costos']
    groups, order = {}, []
    for row in ws.iter_rows(values_only=True):
        a = row[0]
        if not isinstance(a, str) or not a[:1].isdigit() or '·' not in a or row[2] is None:
            continue
        try:
            q = float(row[3]) if row[3] not in (None, '') else 0
            p = float(row[5]) if row[5] not in (None, '') else 0
            monto = q * p
        except (TypeError, ValueError):
            q = p = monto = 0
        detalle = ' '.join(str(x) for x in (row[3], row[4]) if x not in (None, '')).strip()
        groups.setdefault(a, []) or (a not in order and order.append(a))
        groups[a].append({"item": str(row[2]), "cantidad": q, "unidad": str(row[4] or '').strip(),
                          "precio": p, "detalle": detalle, "monto": round(monto, 2)})
    for rb in order:
        st = round(sum(i['monto'] for i in groups[rb]), 2)
        presupuesto.append({"rubro": rb, "items": groups[rb], "subtotal": st}); sub_operativo += st
    sub_operativo = round(sub_operativo, 2)
except Exception as e:   # noqa
    print("  aviso: no se pudo leer el Maestro (", e, ")")
    for r in sim['items']:
        presupuesto.append({"rubro": r['nombre'], "items": [], "subtotal": r['monto']})
    sub_operativo = sum(r['monto'] for r in sim['items'])

# chequeos
errs = []
if round(sum(d['monto'] for d in desg_part), 2) != part_oper: errs.append("desglose participante")
if round(sum(d['monto'] for d in desg_eq), 2) != eq_oper: errs.append("desglose equipo")
if sum(r['monto'] for r in sim['items']) != meta: errs.append("rubros ≠ meta")
if part_cuota_total + equipo_cuotas != cuotas: errs.append("cuotas")
if errs:
    raise SystemExit("NO CUADRA: " + ", ".join(errs))

# ------------------------------------------------------------- helpers render
PALETTE = ['#38BDF8', '#34D399', '#F2C572', '#FC5130', '#A78BFA', '#22D3EE', '#FB7185', '#FACC15', '#4ADE80', '#60A5FA', '#F97316']
def money(n):  return "RD$ " + format(int(round(n)), ",")
def money2(n): return "RD$ " + format(round(n + 1e-9, 2), ",.2f")
def pctf(x):   return format(x, ".1f").replace(".", ",")
def pie_bg(items):
    total = sum(i['monto'] for i in items); acc = 0; parts = []
    for idx, it in enumerate(items):
        col = PALETTE[idx % len(PALETTE)]; s = acc / total * 100; acc += it['monto']; e = acc / total * 100
        parts.append(f"{col} {s:.2f}% {e:.2f}%")
    return "conic-gradient(" + ", ".join(parts) + ")"
def legend(items, fmt):
    total = sum(i['monto'] for i in items); out = []
    for idx, it in enumerate(items):
        col = PALETTE[idx % len(PALETTE)]
        out.append(f'<div class="leg-row"><span class="leg-dot" style="background:{col}"></span>'
                   f'<span class="leg-l">{it["label"]}</span>'
                   f'<span class="leg-v">{fmt(it["monto"])} · {pctf(it["monto"]/total*100)}%</span></div>')
    return "".join(out)
def days_to(iso):
    y, m, d = map(int, iso.split('-'))
    return max(0, (dt.date(y, m, d) - dt.date.today()).days)
dias_cpago = days_to(FECHA_CPAGO); dias_ret = days_to(FECHA_RET)

# secciones (renderizadas en el HTML — legibles sin JS)
chips_p = "".join(f'<span class="chip">{c}</span>' for c in cubre_part)
chips_e = "".join(f'<span class="chip">{c}</span>' for c in cubre_eq)
sim_btns = ""
for i, r in enumerate(sim['items']):
    tag = ' <span class="rub-tag">donable</span>' if r['donable'] else ''
    sim_btns += (f'<button type="button" class="rub" data-monto="{r["monto"]}" data-donable="{1 if r["donable"] else 0}">'
                 f'<span class="rub-check"></span><span class="rub-n">{r["nombre"]}{tag}</span>'
                 f'<span class="rub-m">{money(r["monto"])}</span></button>')
AREA_COLOR = {'Guías': '#34D399', 'Música': '#F2C572', 'Cocina': '#38BDF8', 'Directores': '#FC5130'}
areas_cards = ""
for a in corr['areas']:
    col = AREA_COLOR.get(a['area'], '#34D399')
    lis = "".join(f'<li>{x}</li>' for x in a['items'])
    areas_cards += (f'<div class="area-card" style="border-top-color:{col}"><div class="area-h">'
                    f'<span class="area-name" style="color:{col}">{a["area"]}</span>'
                    f'<span class="area-amt">≈ {money(a["monto_indicativo"])}</span></div>'
                    f'<ul class="area-items">{lis}</ul></div>')
def _esc(s): return str(s).replace('"', "'")
def _raw(n): n = float(n); return str(int(n)) if n.is_integer() else ('%g' % n)
def _disp(n): n = float(n); return format(int(n), ',') if n.is_integer() else format(n, ',g')
def _short_rubro(r): return r.split('·', 1)[1].strip() if '·' in r else r

# Explorador del presupuesto: lista plana (cantidad · precio · total) para ver/ordenar/clasificar/simular
bud_items = []
for gi, g in enumerate(presupuesto):
    for it in g['items']:
        bud_items.append({**it, "rubro_idx": gi, "rubro_corto": _short_rubro(g['rubro'])})
bud_items.sort(key=lambda x: x['monto'], reverse=True)
bud_rows = ""
for it in bud_items:
    bud_rows += (
        f'<div class="bi" data-rubro="{it["rubro_idx"]}" data-qty="{_raw(it["cantidad"])}" '
        f'data-precio="{_raw(it["precio"])}" data-monto="{int(round(it["monto"]))}" data-item="{_esc(it["item"])}">'
        f'<div class="bi-main"><span class="bi-n">{it["item"]}</span><span class="bi-rub">{it["rubro_corto"]}</span></div>'
        f'<span class="bi-q" data-u="{_esc(it["unidad"])}"><b>{_disp(it["cantidad"])}</b> {it["unidad"]}</span>'
        f'<span class="bi-p">× {money(it["precio"])}</span>'
        f'<b class="bi-t">{money(it["monto"])}</b>'
        f'<button type="button" class="apad-mini" data-apad data-tipo="item" '
        f'data-label="{_esc(it["item"])}" data-monto="{int(round(it["monto"]))}">apadrinar</button></div>')
bud_chips = '<button type="button" class="bchip on" data-rub="all">Todos</button>'
for gi, g in enumerate(presupuesto):
    bud_chips += f'<button type="button" class="bchip" data-rub="{gi}">{_short_rubro(g["rubro"])}</button>'

# Aplicativo "Apadrina la Misión 88": selector (carta + lo que falta + rubros) + WhatsApp
WA_CONTACTS = EST['marca']['contacto_whatsapp']['contactos']
_sel = ['<option value="__sel" hidden>— elegido desde el presupuesto —</option>',
        '<option value="carta" data-tipo="carta" data-label="Carta de donación" selected>Pedir una carta de donación</option>',
        f'<option data-tipo="meta" data-label="Lo que falta de la misión" data-monto="{brecha}">Lo que falta de la misión — {money(brecha)}</option>']
for g in presupuesto:
    if g['subtotal'] > 0:
        _sel.append(f'<option data-tipo="rubro" data-label="{_esc(g["rubro"])}" data-monto="{g["subtotal"]}">{g["rubro"]} — {money(g["subtotal"])}</option>')
APAD_OPTS = "".join(_sel)

# Botones de WhatsApp renderizados en el HTML (funcionan aun SIN JS: llevan href y
# nombre del director; el JS solo refina el mensaje según lo elegido).
WA_ICON = ('<svg class="wa-ic" viewBox="0 0 24 24" width="19" height="19" aria-hidden="true" fill="currentColor">'
           '<path d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21h.004c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01zM12.04 20.15h-.003a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.11.82.83-3.04-.2-.31a8.16 8.16 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.69 8.23-8.23 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43-.14-.01-.31-.01-.48-.01s-.43.06-.66.31c-.23.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28z"/></svg>')
_wa_default = urllib.parse.quote("Hola. Quiero apoyar el ETC · Misión 88 (Encuentro Total con Cristo).")
wa_btns = "".join(
    f'<a class="wa-btn" id="wa-{i}" target="_blank" rel="noopener" '
    f'href="https://wa.me/{c["wa"]}?text={_wa_default}">{WA_ICON}'
    f'<span class="wa-name" id="wa-{i}-n">WhatsApp a {c["nombre"]}</span></a>'
    for i, c in enumerate(WA_CONTACTS))

# Bloque "Cómo pagar tu cuota": transferencia + reenviar comprobante + PayPal opcional (data-driven)
APORTE = EST['marca'].get('aporte', {})
_cta = APORTE.get('cuenta', {}); _cf = APORTE.get('contacto_financiero', {}); _pp = APORTE.get('paypal', {})
POR_DEF = '<span class="pordef">[POR DEFINIR]</span>'
def _copy_btn(val): return f'<button type="button" class="cp-btn" data-copy="{_esc(val)}" title="Copiar">📋</button>'
def _pay_row(lbl, val, copy=False):
    v = (f'<span class="pay-val">{val}</span>' + (_copy_btn(val) if copy else '')) if val else POR_DEF
    return f'<div class="pay-row"><span class="pay-k">{lbl}</span><span class="pay-v">{v}</span></div>'
cuenta_rows = "".join([
    _pay_row('Banco', _cta.get('banco', '')),
    _pay_row('Tipo de cuenta', _cta.get('tipo', '')),
    _pay_row('Número', _cta.get('numero', ''), copy=True),
    _pay_row('Titular', _cta.get('titular', '')),
    _pay_row(_cta.get('documento_tipo', 'Cédula'), _cta.get('documento', ''), copy=True),
])
if _cta.get('numero'):
    _all = f"{_cta.get('banco','')} · {_cta.get('tipo','')} · Cuenta {_cta.get('numero','')} · {_cta.get('titular','')} · {_cta.get('documento_tipo','Cédula')} {_cta.get('documento','')}"
    cuenta_extra = f'<button type="button" class="cp-all" data-copy="{_esc(_all)}">📋 Copiar todos los datos</button>'
else:
    cuenta_extra = '<p class="pay-note">Esperando los datos de la cuenta de Tesorería — no se inventan (regla #1).</p>'
_fin, _prov = (_cf['contactos'], False) if _cf.get('contactos') else (WA_CONTACTS, True)
_comp_msg = urllib.parse.quote("Hola. Hice mi aporte para el ETC · Misión 88 (Encuentro Total con Cristo) por transferencia. Te adjunto el comprobante. 🙏")
comp_btns = "".join(
    f'<a class="wa-btn" target="_blank" rel="noopener" href="https://wa.me/{c["wa"]}?text={_comp_msg}">{WA_ICON}'
    f'<span class="wa-name">Enviar comprobante a {c["nombre"]}</span></a>' for c in _fin)
prov_note = '<p class="pay-note">Contacto provisional (Co-Dirección) hasta nombrar Tesorería.</p>' if _prov else ''
if _pp.get('habilitado') and _pp.get('url'):
    paypal_html = (f'<a class="pp-btn" target="_blank" rel="noopener" href="{_pp["url"]}">Donar con PayPal</a>'
                   '<p class="pay-note">PayPal cobra comisión; úsalo solo si no tienes cuenta local.</p>')
else:
    paypal_html = f'<div class="pay-pend">{POR_DEF} — opcional; se activa cuando exista el link de PayPal</div>'
PAY_SECTION = f'''  <section class="panel pay reveal" id="pay-panel">
    <h2>Cómo pagar tu cuota</h2>
    <p class="h2note">Por transferencia: copia los datos, transfiere y reenvía tu comprobante con un toque. El control de pagos es interno de Tesorería — aquí no se listan nombres.</p>
    <div class="pay-grid">
      <div class="pay-card">
        <div class="pay-card-h">1 · Datos para transferir</div>
        {cuenta_rows}
        {cuenta_extra}
      </div>
      <div class="pay-card">
        <div class="pay-card-h">2 · Ya transferí → enviar comprobante</div>
        <p class="pay-sub">Se abre WhatsApp con el mensaje listo; solo adjunta tu captura y envía.</p>
        {comp_btns}
        {prov_note}
      </div>
    </div>
    <div class="pay-card pay-pp">
      <div class="pay-card-h">¿Sin cuenta local? PayPal (opcional)</div>
      <p class="pay-sub">Para diáspora o quien no tenga cuenta dominicana.</p>
      {paypal_html}
    </div>
  </section>
'''

datos_js = json.dumps({"costoTotal": meta, "cuotas": cuotas, "brecha": brecha, "subOperativo": sub_operativo,
                       "fechaCierrePagos": FECHA_CPAGO, "fechaRetiro": FECHA_RET, "locale": "es-DO", "moneda": "RD$",
                       "wa": [{"n": c["nombre"], "num": c["wa"]} for c in WA_CONTACTS]}, ensure_ascii=False)

CSS = r'''
  :root{--bg:#0B1F3A;--bg2:#0e2a4d;--bg3:#071427;--ink:#EAF2FF;--muted:#9DB2D4;--muted2:#8EA3C6;
    --line:rgba(255,255,255,.10);--card:rgba(255,255,255,.045);--card-h:rgba(255,255,255,.075);--hole:#10233f;
    --green:#34D399;--green3:#059669;--sky:#38BDF8;--gold:#F2C572;--red:#FC5130;--shadow:0 20px 50px -20px rgba(0,0,0,.6);--r:20px}
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);line-height:1.5;min-height:100vh;
    background:radial-gradient(1100px 700px at 12% -8%,rgba(56,189,248,.12),transparent 60%),radial-gradient(900px 600px at 95% 0%,rgba(252,81,48,.10),transparent 55%),radial-gradient(1200px 900px at 50% 120%,rgba(52,211,153,.08),transparent 60%),linear-gradient(160deg,var(--bg2),var(--bg) 45%,var(--bg3));
    background-attachment:fixed;-webkit-font-smoothing:antialiased;padding:clamp(14px,3vw,40px);overflow-x:hidden}
  .stars{position:fixed;inset:0;z-index:-1;overflow:hidden}
  .stars i{position:absolute;width:2px;height:2px;background:#fff;border-radius:50%;opacity:.5;animation:tw 4s infinite ease-in-out}
  @keyframes tw{0%,100%{opacity:.2}50%{opacity:.8}}
  .wrap{max-width:1180px;margin:0 auto}
  header{text-align:center;padding:clamp(12px,3vw,30px) 0 clamp(10px,2vw,22px)}
  .patch{width:clamp(120px,30vw,168px);height:auto;display:block;margin:0 auto 14px;filter:drop-shadow(0 10px 24px rgba(0,0,0,.45))}
  h1{font-size:clamp(1.9rem,7vw,4.2rem);font-weight:800;line-height:1.04;letter-spacing:-.02em;margin:6px 0;background:linear-gradient(180deg,#fff,#cfe0ff 70%,#9db2d4);-webkit-background-clip:text;background-clip:text;color:transparent}
  .sub{color:var(--muted);font-size:clamp(.98rem,2.6vw,1.25rem);font-weight:500;max-width:760px;margin:6px auto 0}
  .cita{margin:16px auto 0;max-width:640px;color:var(--gold);font-style:italic;font-size:clamp(.98rem,3vw,1.3rem);line-height:1.35}
  .cita b{font-style:normal;color:var(--muted2);font-size:.8em;display:block;margin-top:5px;letter-spacing:.04em}
  .kpis{display:grid;gap:clamp(10px,1.6vw,18px);margin:clamp(18px,3vw,30px) 0;grid-template-columns:repeat(auto-fit,minmax(160px,1fr))}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:clamp(14px,2vw,22px);position:relative;overflow:hidden;transition:transform .35s,background .35s,border-color .35s}
  .kpi:hover{transform:translateY(-4px);background:var(--card-h);border-color:rgba(255,255,255,.2)}
  .kpi::before{content:"";position:absolute;inset:0 auto auto 0;width:100%;height:3px;background:linear-gradient(90deg,var(--sky),var(--green))}
  .kpi .lbl{font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
  .kpi .val{font-size:clamp(1.4rem,4.5vw,2.3rem);font-weight:800;letter-spacing:-.02em;margin-top:8px;font-variant-numeric:tabular-nums;line-height:1.05}
  .kpi .note{font-size:.78rem;color:var(--muted2);margin-top:6px}
  .kpi.green .val{color:var(--green)}.kpi.red .val{color:var(--red)}
  .panel{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:clamp(16px,2.6vw,32px);box-shadow:var(--shadow);margin-bottom:clamp(14px,2vw,22px)}
  .panel h2{font-size:clamp(1.15rem,3vw,1.6rem);font-weight:700;letter-spacing:-.01em}
  .panel .h2note{color:var(--muted);font-size:clamp(.85rem,2.2vw,.92rem);margin-top:5px;margin-bottom:20px}
  .grid2{display:grid;gap:clamp(16px,2.4vw,26px);grid-template-columns:1fr 1fr}
  @media(max-width:820px){.grid2{grid-template-columns:1fr}}
  .pie-row{display:flex;gap:clamp(14px,2.5vw,22px);align-items:center;flex-wrap:wrap}
  .pie{width:clamp(128px,40vw,180px);aspect-ratio:1;border-radius:50%;flex:none;box-shadow:0 0 0 6px rgba(255,255,255,.03);position:relative}
  .pie.donut::after{content:"";position:absolute;inset:30%;border-radius:50%;background:var(--hole);box-shadow:inset 0 2px 8px rgba(0,0,0,.4)}
  .legend{flex:1;min-width:min(100%,200px);display:grid;gap:7px}
  .leg-row{display:grid;grid-template-columns:auto 1fr auto;gap:9px;align-items:center;font-size:clamp(.82rem,2.2vw,.9rem);font-variant-numeric:tabular-nums}
  .leg-dot{width:11px;height:11px;border-radius:3px}
  .leg-l{color:var(--ink)}.leg-v{color:var(--muted);font-weight:600;white-space:nowrap}
  .costo-card .ct{color:var(--muted);text-transform:uppercase;letter-spacing:.07em;font-size:.78rem;font-weight:700;margin-bottom:4px}
  .costo-card .cbig{font-size:clamp(1.7rem,5vw,2.4rem);font-weight:800;color:var(--green);font-variant-numeric:tabular-nums;line-height:1}
  .costo-card .csub{color:var(--muted);font-size:.85rem;margin:4px 0 16px}.costo-card .csub b{color:var(--ink)}
  .costo-card .csub b.cuota-amt{font-size:1.5rem;color:var(--gold);line-height:1.1}
  .costo-card .ct .role-p{color:var(--green)}
  .costo-card .ct .role-e{color:var(--sky)}
  .qcard{background:rgba(0,0,0,.18);border:1px solid var(--line);border-radius:16px;padding:clamp(16px,2.2vw,24px)}
  .qcard .qt{color:var(--muted);text-transform:uppercase;letter-spacing:.07em;font-size:.78rem;font-weight:700}
  .qcard .qbig{font-size:clamp(1.7rem,5vw,2.3rem);font-weight:800;color:var(--sky);font-variant-numeric:tabular-nums;line-height:1;margin:6px 0}
  .qcard .qline{color:var(--muted);font-size:.92rem;margin-bottom:14px}.qcard .qline b{color:var(--ink)}
  .chips{display:flex;flex-wrap:wrap;gap:7px}
  .chip{background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.25);color:#cfeafe;font-size:.82rem;padding:5px 11px;border-radius:100px}
  .qtot{margin-top:18px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:.95rem;font-variant-numeric:tabular-nums}.qtot b{color:var(--ink)}
  .sim{background:linear-gradient(135deg,rgba(56,189,248,.12),rgba(52,211,153,.06) 70%,transparent),var(--card);border:1px solid rgba(56,189,248,.28)}
  .sim-flex{display:flex;gap:clamp(18px,3vw,34px);align-items:flex-start;flex-wrap:wrap}
  .rocket-wrap{flex:none;width:clamp(120px,32vw,180px);margin:0 auto;text-align:center}
  .rocket-wrap svg{width:100%;height:auto;display:block;overflow:visible}
  .sim-read{flex:1;min-width:min(100%,240px)}
  .sim-falta{font-size:clamp(2.2rem,9vw,4rem);font-weight:800;color:var(--red);letter-spacing:-.03em;font-variant-numeric:tabular-nums;line-height:1}
  .sim-falta.done{color:var(--green)}
  .sim-falta-lbl{color:var(--muted);margin:4px 0 14px;font-size:1.02rem}
  .sim-mini{display:flex;gap:22px;flex-wrap:wrap;color:var(--muted);font-size:.92rem;font-variant-numeric:tabular-nums;margin-bottom:16px}
  .sim-mini b{color:var(--ink);display:block;font-size:1.15rem;font-weight:800}
  .sim-actions{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px}
  .sim-btn{font-family:inherit;cursor:pointer;border-radius:100px;padding:9px 16px;font-size:.86rem;font-weight:700;border:1px solid var(--line);background:rgba(255,255,255,.05);color:var(--ink);transition:all .2s}
  .sim-btn:hover{border-color:rgba(255,255,255,.3)}
  .sim-btn.go{background:linear-gradient(180deg,var(--sky),#0c8fce);border-color:var(--sky);color:#04243a}
  .sim-list{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:18px}
  @media(max-width:680px){.sim-list{grid-template-columns:1fr}}
  .rub{display:flex;align-items:center;gap:10px;width:100%;text-align:left;font-family:inherit;cursor:pointer;background:rgba(0,0,0,.2);border:1px solid var(--line);border-radius:12px;padding:11px 13px;color:var(--ink);transition:all .18s}
  .rub:hover{border-color:rgba(255,255,255,.28)}
  .rub.on{background:rgba(52,211,153,.14);border-color:var(--green)}
  .rub-check{width:20px;height:20px;border-radius:6px;border:2px solid var(--muted2);flex:none;position:relative;transition:all .18s}
  .rub.on .rub-check{background:var(--green);border-color:var(--green)}
  .rub.on .rub-check::after{content:"✓";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#04241a;font-size:13px;font-weight:900}
  .rub-n{flex:1;font-size:.92rem}.rub-m{font-variant-numeric:tabular-nums;font-weight:700;color:var(--muted)}
  .rub.on .rub-m{color:var(--green)}
  .rub-tag{font-size:.66rem;color:var(--green);border:1px solid rgba(52,211,153,.4);border-radius:100px;padding:1px 7px;margin-left:4px;vertical-align:middle}
  .sim-note{color:var(--muted);font-size:.88rem;margin-top:16px;line-height:1.5}.sim-note b{color:var(--ink)}
  .areas-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
  .area-card{background:rgba(0,0,0,.18);border:1px solid var(--line);border-radius:16px;padding:18px 20px;border-top:3px solid var(--green)}
  .area-h{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:12px;padding-bottom:11px;border-bottom:1px solid var(--line)}
  .area-name{font-weight:800;font-size:1.16rem}.area-amt{color:var(--muted);font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap;font-size:.92rem}
  .area-items{list-style:none;display:grid;gap:8px}
  .area-items li{color:var(--muted);padding-left:18px;position:relative;font-size:.94rem}
  .area-items li::before{content:"";position:absolute;left:3px;top:.55em;width:6px;height:6px;border-radius:50%;background:var(--green)}
  .areas-foot{color:var(--muted);margin-top:16px;font-size:.9rem}.areas-foot b{color:var(--ink)}
  .cd-two{display:grid;gap:14px;grid-template-columns:1fr 1fr}
  @media(max-width:680px){.cd-two{grid-template-columns:1fr}}
  .cd-block{background:rgba(0,0,0,.2);border:1px solid var(--line);border-radius:14px;padding:14px 14px 16px}
  .cd-block.urgent{border-color:rgba(252,81,48,.4);background:rgba(252,81,48,.06)}
  .cd-head{color:var(--muted);font-size:.85rem;margin-bottom:10px}.cd-head b{color:var(--ink)}.cd-block.urgent .cd-head b{color:var(--red)}
  .cd-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
  .cd-cell{background:rgba(0,0,0,.25);border:1px solid var(--line);border-radius:12px;padding:12px 2px;text-align:center}
  .cd-num{font-size:clamp(1.3rem,5vw,2.2rem);font-weight:800;font-variant-numeric:tabular-nums;line-height:1;background:linear-gradient(180deg,#fff,#bcd2f5);-webkit-background-clip:text;background-clip:text;color:transparent}
  .cd-lbl{font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:7px}
  .pres-grp{border:1px solid var(--line);border-radius:12px;margin-bottom:8px;overflow:hidden;background:rgba(0,0,0,.14)}
  .pres-grp summary{display:flex;align-items:center;gap:10px;padding:13px 16px;cursor:pointer;list-style:none;font-weight:700}
  .pres-grp summary::-webkit-details-marker{display:none}
  .pres-grp summary::before{content:"▸";color:var(--sky);transition:transform .2s;font-size:.9em}
  .pres-grp[open] summary::before{transform:rotate(90deg)}
  .pres-grp summary:hover{background:rgba(255,255,255,.03)}
  .pg-n{flex:1}.pg-c{color:var(--muted2);font-size:.8rem;font-weight:600}.pg-s{font-variant-numeric:tabular-nums;color:var(--sky)}
  .pres-items{padding:4px 16px 14px}
  .pres-it{display:grid;grid-template-columns:1fr auto;gap:4px 10px;align-items:baseline;padding:6px 0;border-top:1px solid rgba(255,255,255,.05);font-size:.86rem}
  .pi-n{color:var(--ink)}.pi-d{color:var(--muted2);font-size:.78rem;grid-column:1;grid-row:2}.pi-m{font-variant-numeric:tabular-nums;color:var(--muted);font-weight:600;white-space:nowrap;grid-column:2;grid-row:1}
  .pres-foot{color:var(--muted);margin-top:14px;font-size:.9rem;font-variant-numeric:tabular-nums}.pres-foot b{color:var(--ink)}
  footer{text-align:center;color:var(--muted2);font-size:.82rem;padding:24px 0 8px;line-height:1.7}footer b{color:var(--muted)}
  .reveal{opacity:0;transform:translateY(20px);transition:opacity .7s,transform .7s cubic-bezier(.16,1,.3,1)}
  .reveal.visible{opacity:1;transform:none}
  @media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}.stars i{animation:none}html{scroll-behavior:auto}}
  .no-js .reveal{opacity:1;transform:none}
  .apad{background:linear-gradient(135deg,rgba(37,211,102,.10),rgba(56,189,248,.05) 70%,transparent),var(--card);border:1px solid rgba(37,211,102,.28)}
  .apad-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  @media(max-width:680px){.apad-grid{grid-template-columns:1fr}}
  .apad-f{display:flex;flex-direction:column;gap:6px;font-size:.85rem;color:var(--muted)}
  .apad-f input,.apad-f select{font-family:inherit;font-size:1rem;color:var(--ink);background:rgba(0,0,0,.25);border:1px solid var(--line);border-radius:12px;padding:12px 14px;width:100%}
  .apad-read{margin:16px 0;font-size:1.05rem;color:var(--muted)}.apad-read b{color:var(--ink)}
  .apad-btns{display:flex;gap:12px;flex-wrap:wrap}
  .wa-btn{display:inline-flex;align-items:center;gap:8px;background:#25D366;color:#053a1e;font-weight:800;padding:13px 20px;border-radius:100px;text-decoration:none;font-size:1rem}
  .wa-btn:hover{filter:brightness(1.07)}
  .apad-note{color:var(--muted2);font-size:.85rem;margin-top:12px}
  .apad-mini{font-family:inherit;cursor:pointer;display:inline-flex;align-items:center;min-height:30px;background:rgba(37,211,102,.14);border:1px solid rgba(37,211,102,.4);color:#8df3b3;border-radius:100px;padding:5px 13px;font-size:.76rem;font-weight:700;white-space:nowrap}
  .apad-mini:hover{background:rgba(37,211,102,.26)}
  .apad-mini:active{transform:scale(.97)}
  .rub-mini{margin-bottom:10px}
  .wa-btn .wa-ic{flex:none}
  .pres-it .pi-n{grid-column:1;grid-row:1}
  .pres-it .apad-mini{grid-column:2;grid-row:2;justify-self:end;margin-top:2px}
  .qbig.hl{color:var(--gold)}
  .hl-amt{color:var(--gold)}
  /* explorador + simulador del presupuesto */
  .bud-ctrls{display:flex;flex-direction:column;gap:12px;margin:6px 0 16px}
  .bchips{display:flex;flex-wrap:wrap;gap:7px}
  .bchip{font-family:inherit;cursor:pointer;background:rgba(255,255,255,.05);border:1px solid var(--line);color:var(--muted);border-radius:100px;padding:6px 13px;font-size:.82rem;font-weight:600;min-height:32px}
  .bchip.on{background:rgba(56,189,248,.16);border-color:var(--sky);color:#cfeafe}
  .bud-tools{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
  .bud-sort{display:flex;align-items:center;gap:8px;color:var(--muted);font-size:.85rem}
  .bud-sort select{font-family:inherit;font-size:.9rem;color:var(--ink);background:rgba(0,0,0,.25);border:1px solid var(--line);border-radius:10px;padding:8px 10px}
  .bud-simbtn{font-family:inherit;cursor:pointer;border-radius:100px;padding:9px 16px;font-size:.85rem;font-weight:700;border:1px solid rgba(52,211,153,.4);background:rgba(52,211,153,.12);color:#8df3b3}
  .bud-simbtn.on{background:var(--green);color:#04241a;border-color:var(--green)}
  .bi{display:grid;grid-template-columns:1fr auto auto auto auto;gap:6px 14px;align-items:center;padding:9px 4px;border-top:1px solid rgba(255,255,255,.06)}
  .bi-head{color:var(--muted2);font-size:.72rem;text-transform:uppercase;letter-spacing:.04em;border-top:none;padding-bottom:4px}
  .bi-main{display:flex;flex-direction:column;min-width:0}
  .bi-n{color:var(--ink);font-size:.9rem}
  .bi-rub{color:var(--muted2);font-size:.72rem}
  .bi-q,.bi-p{color:var(--muted);font-size:.84rem;font-variant-numeric:tabular-nums;white-space:nowrap}.bi-q b{color:var(--ink)}
  .bi-t{color:var(--sky);font-variant-numeric:tabular-nums;font-weight:700;white-space:nowrap}
  .bi.chg .bi-t{color:var(--gold)}
  .bi-qi,.bi-pi{font-family:inherit;width:5ch;font-size:.84rem;color:var(--ink);background:rgba(0,0,0,.3);border:1px solid var(--line);border-radius:8px;padding:4px 6px;font-variant-numeric:tabular-nums}
  .bi-pi{width:7ch}
  .bud-foot{margin-top:12px;color:var(--muted);font-size:.9rem;font-variant-numeric:tabular-nums}.bud-foot b{color:var(--ink)}
  .sim2{margin-top:18px;background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.3);border-radius:16px;padding:16px}
  .sim2-h{color:var(--green);font-weight:700;font-size:.82rem;margin-bottom:12px;letter-spacing:.02em}
  .sim2-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
  @media(max-width:680px){.sim2-grid{grid-template-columns:1fr}}
  .sim2-l{color:var(--muted);font-size:.78rem;margin-bottom:3px}
  .sim2-v{font-size:1.5rem;font-weight:800;font-variant-numeric:tabular-nums;line-height:1}.sim2-v.red{color:var(--red)}
  .sim2-dif{font-size:1.15rem;font-weight:700}.sim2-dif.save{color:var(--green)}.sim2-dif.up{color:var(--red)}
  @media(max-width:640px){
    .bi{grid-template-columns:1fr auto;gap:3px 10px}
    .bi-head{display:none}
    .bi-main{grid-column:1;grid-row:1}
    .bi-t{grid-column:2;grid-row:1;justify-self:end}
    .bi-q{grid-column:1;grid-row:2}
    .bi-p{grid-column:2;grid-row:2;justify-self:end}
    .bi .apad-mini{grid-column:1 / -1;grid-row:3;justify-self:start;margin-top:5px}
  }
  /* bloque pagar cuota: cuenta + comprobante + paypal + copiar */
  .pay-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  @media(max-width:680px){.pay-grid{grid-template-columns:1fr}}
  .pay-card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px}
  .pay-pp{margin-top:14px}
  .pay-card-h{color:var(--sky);font-weight:700;font-size:.9rem;margin-bottom:12px}
  .pay-sub{color:var(--muted);font-size:.83rem;margin-bottom:12px}
  .pay-row{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:7px 0;border-top:1px solid rgba(255,255,255,.06)}
  .pay-row:first-of-type{border-top:none}
  .pay-k{color:var(--muted);font-size:.84rem}
  .pay-v{color:var(--ink);font-size:.9rem;text-align:right;display:flex;align-items:center;gap:8px;justify-content:flex-end;flex-wrap:wrap}
  .pay-val{font-variant-numeric:tabular-nums;font-weight:600}
  .pordef{color:var(--gold);font-size:.8rem;font-weight:700;letter-spacing:.02em}
  .cp-btn{font-family:inherit;cursor:pointer;background:rgba(56,189,248,.14);border:1px solid rgba(56,189,248,.4);border-radius:8px;padding:3px 8px;font-size:.85rem;line-height:1}
  .cp-all{font-family:inherit;cursor:pointer;margin-top:12px;width:100%;background:rgba(56,189,248,.12);border:1px solid rgba(56,189,248,.4);color:#cfeafe;border-radius:10px;padding:10px;font-size:.86rem;font-weight:700}
  .pay-note{color:var(--muted2);font-size:.78rem;margin-top:10px}
  .pay-pend{color:var(--muted);font-size:.85rem;padding:8px 0}
  .pay .wa-btn{margin-top:8px}
  .pp-btn{display:inline-block;background:#0070BA;color:#fff;border-radius:10px;padding:10px 18px;font-weight:700;text-decoration:none;font-size:.9rem}
  .cp-toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(12px);background:#04241a;color:#8df3b3;border:1px solid var(--green);border-radius:100px;padding:9px 18px;font-size:.85rem;font-weight:700;opacity:0;transition:opacity .25s,transform .25s;z-index:50;pointer-events:none}
  .cp-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
'''

JS = r'''
const datos = __DATOS_JS__;
const REDUCE = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const nf = new Intl.NumberFormat(datos.locale), nf2 = new Intl.NumberFormat(datos.locale,{minimumFractionDigits:2,maximumFractionDigits:2});
const money = n => datos.moneda+' '+nf.format(Math.round(n));
const $ = id => document.getElementById(id);
const setText = (id,v)=>{const e=$(id); if(e)e.textContent=v;};
const ease = t => 1-Math.pow(1-t,3);
function animate(d,on,done){ if(REDUCE){on(1);if(done)done();return;} const t0=performance.now();
  (function f(now){const t=Math.min(1,(now-t0)/d); on(ease(t)); if(t<1)requestAnimationFrame(f); else if(done)done();})(performance.now()); }
/* estrellas */
(function(){let h='';for(let i=0;i<48;i++){h+='<i style="left:'+(Math.random()*100).toFixed(2)+'%;top:'+(Math.random()*100).toFixed(2)+'%;animation-delay:'+(Math.random()*4).toFixed(2)+'s"></i>';}var s=$('stars'); if(s)s.innerHTML=h;})();
/* count-up sobre los valores ya impresos */
document.querySelectorAll('[data-count]').forEach(el=>{ const to=+el.dataset.count, k=el.dataset.kind;
  const f = k==='money2' ? (n=>datos.moneda+' '+nf2.format(n)) : money;
  animate(1400, p=>{ el.textContent=f(to*p); }); });
/* cuenta regresiva en vivo */
function dl(iso){const p=iso.split('-').map(Number);return new Date(p[0],p[1]-1,p[2],0,0,0,0);}
function diff(iso){let ms=Math.max(0,dl(iso)-Date.now());const d=Math.floor(ms/86400000);ms-=d*86400000;const h=Math.floor(ms/3600000);ms-=h*3600000;const m=Math.floor(ms/60000);ms-=m*60000;return{d:d,h:h,m:m,s:Math.floor(ms/1000)};}
function cd(pfx,iso,alsoKpi){function t(){const x=diff(iso);setText(pfx+'-d',x.d);setText(pfx+'-h',String(x.h).padStart(2,'0'));setText(pfx+'-m',String(x.m).padStart(2,'0'));setText(pfx+'-s',String(x.s).padStart(2,'0'));if(alsoKpi)setText('kpi-dias',x.d);}t();setInterval(t,1000);}
cd('cpago',datos.fechaCierrePagos,true); cd('ret',datos.fechaRetiro,false);
/* simulador (cohete) */
const RBOT=328,RRANGE=250; let fuelCur=0;
function setFuel(fr){var f=$('fuel');if(!f)return;f.setAttribute('y',RBOT-fr*RRANGE);f.setAttribute('height',fr*RRANGE);
  var fl=$('flame');if(fl){fl.setAttribute('transform','translate(80 330) scale('+(0.7+fr*0.6)+','+(0.4+fr*1.4)+') translate(-80 -330)');fl.setAttribute('opacity',(0.4+fr*0.5).toFixed(2));}}
function aFuel(t){if(REDUCE){setFuel(t);fuelCur=t;return;}const from=fuelCur;animate(600,p=>setFuel(from+(t-from)*p),()=>{fuelCur=t;});}
function recompute(){let S=0;document.querySelectorAll('.rub.on').forEach(b=>S+=+b.dataset.monto);
  const cub=datos.cuotas+S, falta=datos.costoTotal-cub; setText('sim-cubierto',money(cub));
  var fE=$('sim-falta');
  if(falta>0){fE.textContent=money(falta);fE.classList.remove('done');setText('sim-falta-lbl','hay que reunir entre todos');}
  else{fE.textContent=falta===0?money(0):('+'+money(Math.abs(falta)));fE.classList.add('done');setText('sim-falta-lbl',falta===0?'¡misión cubierta!':'¡misión cubierta! incluso sobra');}
  setText('sim-porcabeza',money(Math.max(0,falta)/100)); aFuel(Math.max(0,Math.min(1,cub/datos.costoTotal)));}
var sl=$('sim-list');
if(sl){ sl.addEventListener('click',e=>{var b=e.target.closest('.rub');if(!b)return;b.classList.toggle('on');recompute();});
  $('sim-realista').addEventListener('click',()=>{document.querySelectorAll('.rub').forEach(b=>b.classList.toggle('on',b.dataset.donable==='1'));recompute();});
  $('sim-reset').addEventListener('click',()=>{document.querySelectorAll('.rub').forEach(b=>b.classList.remove('on'));recompute();}); }
recompute();
/* reveal */
(function(){var ns=document.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window)){ns.forEach(n=>n.classList.add('visible'));return;}
  var io=new IntersectionObserver((es,ob)=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');ob.unobserve(e.target);}});},{threshold:.12});
  ns.forEach(n=>io.observe(n));})();
/* apadrinar por WhatsApp */
(function(){
  var WA = datos.wa || [];
  var s = $('apad-sel');
  var sel = {label:'Carta de donación', monto:null, tipo:'carta'};
  function msg(){ var n=(($('apad-name')||{}).value||'').trim(); var hi = n ? ('Hola, soy '+n+'. ') : 'Hola. ';
    if(sel.tipo==='carta') return hi+'Quiero pedir una carta de donación para el ETC · Misión 88 (Encuentro Total con Cristo).';
    if(sel.tipo==='meta')  return hi+'Me gustaría aportar a lo que falta de la misión'+(sel.monto?(' ('+money(sel.monto)+')'):'')+' del ETC · Misión 88.';
    return hi+'Me gustaría apadrinar: '+sel.label+(sel.monto?(' ('+money(sel.monto)+')'):'')+' para el ETC · Misión 88.'; }
  function upd(){ var t=encodeURIComponent(msg());
    WA.forEach(function(c,i){ var a=$('wa-'+i); if(a) a.href='https://wa.me/'+c.num+'?text='+t; var e=$('wa-'+i+'-n'); if(e) e.textContent='WhatsApp a '+c.n; });
    var r=$('apad-read'); if(r){ r.innerHTML = sel.tipo==='carta' ? 'Vas a: <b>pedir una carta de donación</b>'
      : (sel.tipo==='meta' ? 'Vas a: <b>aportar a lo que falta</b>'+(sel.monto?(' — '+money(sel.monto)):'')
        : 'Vas a apadrinar: <b>'+sel.label+'</b>'+(sel.monto?(' — '+money(sel.monto)):'')); } }
  function setSel(label,monto,tipo){ sel={label:label||'Carta de donación', monto:(monto?+monto:null), tipo:tipo||'item'}; upd(); }
  if(s){ s.addEventListener('change',function(e){ var o=e.target.selectedOptions[0]; setSel(o.dataset.label||o.textContent, o.dataset.monto, o.dataset.tipo); }); }
  var nm=$('apad-name'); if(nm){ nm.addEventListener('input', upd); }
  document.addEventListener('click', function(e){ var b=e.target.closest('[data-apad]'); if(!b) return; e.preventDefault();
    setSel(b.dataset.label, b.dataset.monto, b.dataset.tipo);
    if(s){ var fi=-1; for(var k=0;k<s.options.length;k++){ if(s.options[k].getAttribute('data-label')===b.dataset.label){fi=k;break;} } s.selectedIndex = fi>=0?fi:0; }
    var p=$('apad-panel'); if(p) p.scrollIntoView({behavior:'smooth',block:'start'}); });
  upd();
})();
/* explorador + simulador del presupuesto */
(function(){
  var list=$('bud-list'); if(!list) return;
  var rows=[].slice.call(list.getElementsByClassName('bi'));
  var base=0; rows.forEach(function(r){ base+=(+r.dataset.monto); });
  var simOn=false, factor = base ? (datos.costoTotal/base) : 1.1;
  function val(r,w){ if(simOn){ var i=r.querySelector(w==='q'?'.bi-qi':'.bi-pi'); if(i) return parseFloat(i.value)||0; } return parseFloat(w==='q'?r.dataset.qty:r.dataset.precio)||0; }
  function monto(r){ return simOn ? val(r,'q')*val(r,'p') : (+r.dataset.monto); }
  function paint(r){ var t=r.querySelector('.bi-t'); if(t) t.textContent=money(monto(r)); r.classList.toggle('chg', simOn && Math.abs(monto(r)-(+r.dataset.monto))>0.5); }
  function recompute(){ var sub=0,n=0,all=0;
    rows.forEach(function(r){ var m=monto(r); all+=m; if(r.style.display!=='none'){n++;sub+=m;} });
    setText('bud-count',n); setText('bud-sub',money(sub));
    var metaSim=all*factor, falta=metaSim-datos.cuotas, dif=datos.costoTotal-metaSim;
    setText('sim2-meta',money(metaSim)); setText('sim2-falta',money(Math.max(0,falta)));
    var d=$('sim2-dif'); if(d){ if(Math.abs(dif)<1){d.textContent='igual al original';d.className='sim2-dif';}
      else if(dif>0){d.textContent='↓ ahorro de '+money(dif);d.className='sim2-dif save';}
      else{d.textContent='↑ aumento de '+money(-dif);d.className='sim2-dif up';} } }
  function filter(rub){ rows.forEach(function(r){ r.style.display=(rub==='all'||r.dataset.rubro===rub)?'':'none'; });
    var cs=document.getElementsByClassName('bchip'); for(var i=0;i<cs.length;i++) cs[i].classList.toggle('on',cs[i].dataset.rub===rub); recompute(); }
  function sortBy(mode){ rows.slice().sort(function(a,b){
      if(mode==='monto-asc') return monto(a)-monto(b);
      if(mode==='qty-desc')  return val(b,'q')-val(a,'q');
      if(mode==='name')      return a.dataset.item.localeCompare(b.dataset.item,'es');
      return monto(b)-monto(a); }).forEach(function(r){ list.appendChild(r); }); }
  function setSim(on){ simOn=on; var b=$('bud-simbtn'); if(b){ b.classList.toggle('on',on); b.textContent=on?'✓ Simulando — toca para salir':'🧮 Simular cantidades y precios'; }
    rows.forEach(function(r){ var q=r.querySelector('.bi-q'), p=r.querySelector('.bi-p'); var u=q.getAttribute('data-u')||'';
      if(on){ q.innerHTML='<input class="bi-qi" type="number" min="0" inputmode="decimal" value="'+r.dataset.qty+'"> '+u; p.innerHTML='RD$ <input class="bi-pi" type="number" min="0" inputmode="decimal" value="'+r.dataset.precio+'">'; }
      else  { q.innerHTML='<b>'+(+r.dataset.qty).toLocaleString(datos.locale)+'</b> '+u; p.textContent='× '+money(+r.dataset.precio); }
      paint(r); });
    var s=$('sim2'); if(s) s.style.display=on?'':'none'; recompute(); }
  function reset(){ rows.forEach(function(r){ var q=r.querySelector('.bi-qi'), p=r.querySelector('.bi-pi'); if(q)q.value=r.dataset.qty; if(p)p.value=r.dataset.precio; paint(r); }); recompute(); }
  var cb=document.querySelector('.bchips'); if(cb) cb.addEventListener('click',function(e){ var b=e.target.closest('.bchip'); if(b) filter(b.dataset.rub); });
  var ss=$('bud-sort'); if(ss) ss.addEventListener('change',function(e){ sortBy(e.target.value); });
  var sb=$('bud-simbtn'); if(sb) sb.addEventListener('click',function(){ setSim(!simOn); });
  var rb=$('sim2-reset'); if(rb) rb.addEventListener('click',reset);
  list.addEventListener('input',function(e){ if(e.target.classList.contains('bi-qi')||e.target.classList.contains('bi-pi')){ paint(e.target.closest('.bi')); recompute(); } });
  sortBy('monto-desc');
})();
/* copiar al portapapeles (datos de la cuenta) */
(function(){
  function toast(m){ var t=document.createElement('div'); t.className='cp-toast'; t.textContent=m; document.body.appendChild(t);
    requestAnimationFrame(function(){ t.classList.add('show'); }); setTimeout(function(){ t.classList.remove('show'); setTimeout(function(){ t.remove(); },300); },1500); }
  document.addEventListener('click',function(e){ var b=e.target.closest('[data-copy]'); if(!b) return; e.preventDefault();
    var v=b.getAttribute('data-copy')||'';
    if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(v).then(function(){ toast('Copiado ✓'); }, function(){ toast('No se pudo copiar'); }); }
    else { try{ var ta=document.createElement('textarea'); ta.value=v; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.focus(); ta.select(); document.execCommand('copy'); ta.remove(); toast('Copiado ✓'); }catch(_){ toast('No se pudo copiar'); } }
  });
})();
'''.replace('__DATOS_JS__', datos_js)

PATCH = r'''<svg class="patch" viewBox="0 0 200 200" role="img" aria-label="ETC Misión 88">
  <defs><path id="patchArc" d="M30,108 A74,74 0 0 1 170,108"/></defs>
  <circle cx="100" cy="100" r="95" fill="#0B2A52" stroke="#fff" stroke-width="5"/>
  <circle cx="100" cy="100" r="86" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="1.5"/>
  <ellipse cx="100" cy="98" rx="44" ry="72" fill="none" stroke="#fff" stroke-width="2.4" transform="rotate(24 100 100)"/>
  <g fill="#fff"><circle cx="62" cy="58" r="1.6"/><circle cx="142" cy="54" r="2"/><circle cx="151" cy="120" r="1.5"/><circle cx="55" cy="132" r="1.7"/><circle cx="122" cy="150" r="1.5"/><circle cx="80" cy="151" r="1.3"/><circle cx="44" cy="94" r="1.3"/><circle cx="158" cy="86" r="1.3"/></g>
  <path d="M20,150 Q120,56 188,64 Q120,90 34,158 Z" fill="#FC5130"/>
  <text x="100" y="122" text-anchor="middle" font-size="56" font-weight="800" fill="#fff" letter-spacing="2" font-family="-apple-system,Segoe UI,Roboto,sans-serif">ETC</text>
  <text fill="#fff" font-size="13" font-weight="700" letter-spacing="2.4" font-family="-apple-system,Segoe UI,Roboto,sans-serif"><textPath href="#patchArc" startOffset="50%" text-anchor="middle">ENCUENTRO TOTAL CON CRISTO</textPath></text>
  <text x="100" y="178" text-anchor="middle" font-size="12.5" font-weight="700" letter-spacing="4" fill="#fff" font-family="-apple-system,Segoe UI,Roboto,sans-serif">MISIÓN 88</text>
</svg>'''

# Logo original Misión 88 (extraído del chat, fondo transparente). Si existe el
# archivo, se incrusta tal cual (base64, self-contained); si no, cae al SVG.
_logo_path = os.path.join(REPO, 'design', 'logo_mision88.png')
if os.path.exists(_logo_path):
    _raw = open(_logo_path, 'rb').read()
    try:  # optimización NO destructiva (no modifica el archivo fuente): redimensiona a 360px + 256 colores
        from PIL import Image
        import io as _io
        _im = Image.open(_io.BytesIO(_raw)).convert('RGBA')
        _W = 360
        if _im.width > _W:
            _im = _im.resize((_W, round(_im.height * _W / _im.width)), Image.LANCZOS)
        _im = _im.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.NONE)
        _buf = _io.BytesIO(); _im.save(_buf, format='PNG', optimize=True)
        if len(_buf.getvalue()) < len(_raw):
            _raw = _buf.getvalue()
    except Exception:   # sin Pillow se incrusta el original (run_all sigue funcionando)
        pass
    _b64 = base64.b64encode(_raw).decode()
    LOGO_HTML = '<img class="patch" src="data:image/png;base64,' + _b64 + '" alt="ETC · Misión 88">'
else:
    LOGO_HTML = PATCH

ROCKET = r'''<svg viewBox="0 0 160 430">
  <defs><linearGradient id="fuelG" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#0c8fce"/><stop offset="55%" stop-color="#34D399"/><stop offset="100%" stop-color="#A7F3D0"/></linearGradient>
  <clipPath id="bodyClip"><rect x="55" y="78" width="50" height="250" rx="12"/></clipPath></defs>
  <path id="flame" d="M70,330 Q80,395 90,330 Z" fill="#FC5130" opacity=".9"/>
  <rect x="55" y="78" width="50" height="250" rx="12" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.16)"/>
  <rect id="fuel" x="55" y="328" width="50" height="0" fill="url(#fuelG)" clip-path="url(#bodyClip)"/>
  <path d="M55,80 L80,20 L105,80 Z" fill="#E7EEFA"/>
  <path d="M55,300 L38,346 L55,332 Z" fill="#FC5130"/><path d="M105,300 L122,346 L105,332 Z" fill="#FC5130"/>
  <rect x="55" y="78" width="50" height="250" rx="12" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="2"/>
  <circle cx="80" cy="112" r="11" fill="#0B2A52" stroke="#E7EEFA" stroke-width="3"/>
  <line x1="44" x2="116" y1="78" y2="78" stroke="#fff" stroke-dasharray="4 4" stroke-width="1.5" opacity=".7"/>
  <text x="120" y="82" fill="#fff" font-size="10" font-weight="700">META</text></svg>'''

cd_cell = lambda v, lbl, idp: f'<div class="cd-cell"><div class="cd-num" id="{idp}">{v}</div><div class="cd-lbl">{lbl}</div></div>'

BODY = f'''
<div class="stars" id="stars" aria-hidden="true"></div>
<main class="wrap">
  <header class="reveal">
    {LOGO_HTML}
    <h1>ETC · Misión 88</h1>
    <p class="sub">Lo que cuesta la misión, y cómo —trabajando como tripulación— la hacemos posible</p>
    <p class="cita">«{cita['valor']}»<b>{cita['cita']}</b></p>
  </header>

  <section class="kpis reveal">
    <div class="kpi"><div class="lbl">Costo de la misión</div><div class="val" data-count="{meta}" data-kind="money">{money(meta)}</div><div class="note">lo que cuesta el retiro completo</div></div>
    <div class="kpi green"><div class="lbl">Lo que ya ponemos</div><div class="val" data-count="{cuotas}" data-kind="money">{money(cuotas)}</div><div class="note">cuotas de participantes + equipo</div></div>
    <div class="kpi red"><div class="lbl">Falta por reunir</div><div class="val" data-count="{brecha}" data-kind="money">{money(brecha)}</div><div class="note">y depende de nosotros</div></div>
    <div class="kpi"><div class="lbl">Días: cierre de pagos</div><div class="val" id="kpi-dias">{dias_cpago}</div><div class="note">lanzamiento: 4–6 sep</div></div>
  </section>

  <section class="panel reveal">
    <h2>En qué se va el costo de la misión</h2>
    <p class="h2note">La estructura completa, por rubro (incluye el 10% de imprevistos)</p>
    <div class="pie-row"><div class="pie" style="background:{pie_bg(estructura)}"></div><div class="legend">{legend(estructura, money)}</div></div>
  </section>

  <section class="panel reveal">
    <h2>Lo que cuesta la misión, por persona</h2>
    <p class="h2note">Para dimensionar el esfuerzo — sencillo y claro. (Incluye el 10% de imprevistos.)</p>
    <div class="grid2">
      <div class="costo-card"><div class="ct">Por <span class="role-p">participante</span></div>
        <div class="cbig" data-count="{part_costo}" data-kind="money2">{money2(part_costo)}</div>
        <div class="csub">su cuota es <b class="cuota-amt">{money(cuota_part)}</b> · el resto no recae en él</div>
        <div class="pie-row"><div class="pie donut" style="background:{pie_bg(desg_part)}"></div><div class="legend">{legend(desg_part, money2)}</div></div></div>
      <div class="costo-card"><div class="ct">Por <span class="role-e">miembro de equipo</span></div>
        <div class="cbig" style="color:var(--sky)" data-count="{eq_costo}" data-kind="money2">{money2(eq_costo)}</div>
        <div class="csub">su cuota es <b class="cuota-amt">{money(eq_total)}</b></div>
        <div class="pie-row"><div class="pie donut" style="background:{pie_bg(desg_eq)}"></div><div class="legend">{legend(desg_eq, money2)}</div></div></div>
    </div>
  </section>

  <section class="panel reveal">
    <h2>Lo que ponemos nosotros</h2>
    <p class="h2note">La cuota no cubre el costo real — pero es nuestro primer aporte como tripulación</p>
    <div class="grid2">
      <div class="qcard"><div class="qt">Cuota del participante</div><div class="qbig" data-count="{part_cuota_total}" data-kind="money">{money(part_cuota_total)}</div>
        <div class="qline"><b>{money(cuota_part)}</b> × {n_part} participantes</div><div class="chips">{chips_p}</div>
        <div class="qtot">Aporta en total <b>{money(part_cuota_total)}</b></div></div>
      <div class="qcard"><div class="qt">Cuota del equipo · lo que aporta el equipo</div><div class="qbig hl" data-count="{equipo_cuotas}" data-kind="money">{money(equipo_cuotas)}</div>
        <div class="qline"><b class="hl-amt">{money(eq_total)}</b> = <b class="hl-amt">{eq_pagos} pagos de {money(eq_pago)}</b> (jun–sep) · {n_equipo} del equipo</div><div class="chips">{chips_e}</div>
        <div class="qtot">Aporta en total <b>{money(equipo_cuotas)}</b></div></div>
    </div>
  </section>

  <section class="panel sim reveal">
    <h2>El ejercicio de la tripulación</h2>
    <p class="h2note">Marca lo que crees que podemos conseguir donado o gestionado, y mira bajar lo que hay que reunir. No es una meta fría: es ver que, juntos, se puede. (Para tocar y probar, ábrelo en un navegador.)</p>
    <div class="sim-flex">
      <div class="rocket-wrap" aria-hidden="true">{ROCKET}<div style="color:var(--muted);font-size:.82rem;margin-top:6px">cubierto: <b id="sim-cubierto" style="color:var(--ink)">{money(cuotas)}</b></div></div>
      <div class="sim-read">
        <div class="sim-falta" id="sim-falta">{money(brecha)}</div>
        <div class="sim-falta-lbl" id="sim-falta-lbl">hay que reunir entre todos</div>
        <div class="sim-mini"><div>por cada uno (100)<b id="sim-porcabeza">{money(brecha/100)}</b></div><div>costo de la misión<b>{money(meta)}</b></div></div>
        <div class="sim-actions"><button type="button" class="sim-btn go" id="sim-realista">Probar: lo realista</button><button type="button" class="sim-btn" id="sim-reset">Reiniciar</button></div>
        <div class="sim-list" id="sim-list">{sim_btns}</div>
        <p class="sim-note">Es un ejercicio para imaginar y validar juntos — no un compromiso. Lo marcado como <b style="color:var(--green)">donable</b> es lo más realista de gestionar (en el ETC 78 se donó más de la mitad).</p>
      </div>
    </div>
  </section>

  <section class="panel reveal">
    <h2>Cada área aporta su parte</h2>
    <p class="h2note">El esfuerzo no es solo de los directores — cada área de la tripulación carga lo suyo</p>
    <div class="areas-grid">{areas_cards}</div>
    <p class="areas-foot">Montos <b>indicativos</b>. Casa, transporte y la coordinación general completan el costo total.</p>
  </section>

  <section class="panel reveal">
    <h2>Cuenta regresiva</h2>
    <p class="h2note">El dinero debe estar conciliado para el cierre de pagos, antes del lanzamiento</p>
    <div class="cd-two">
      <div class="cd-block urgent"><div class="cd-head">Cierre de pagos · <b>{FECHA_CPAGO_T}</b></div>
        <div class="cd-grid">{cd_cell(dias_cpago,"Días","cpago-d")}{cd_cell("00","Hrs","cpago-h")}{cd_cell("00","Min","cpago-m")}{cd_cell("00","Seg","cpago-s")}</div></div>
      <div class="cd-block"><div class="cd-head">Lanzamiento (retiro) · <b>{FECHA_RET_T}</b></div>
        <div class="cd-grid">{cd_cell(dias_ret,"Días","ret-d")}{cd_cell("00","Hrs","ret-h")}{cd_cell("00","Min","ret-m")}{cd_cell("00","Seg","ret-s")}</div></div>
    </div>
  </section>

  <section class="panel apad reveal" id="apad-panel">
    <h2>Apadrina la Misión 88</h2>
    <p class="h2note">Elige algo del presupuesto (o pide una carta de donación) y escríbele directo a un director por WhatsApp. También puedes tocar “apadrinar” en cualquier ítem del presupuesto de abajo.</p>
    <div class="apad-grid">
      <label class="apad-f"><span>Tu nombre (opcional)</span><input id="apad-name" type="text" placeholder="Tu nombre" autocomplete="name"></label>
      <label class="apad-f"><span>¿Qué quieres apoyar?</span><select id="apad-sel">{APAD_OPTS}</select></label>
    </div>
    <div class="apad-read" id="apad-read">Vas a: <b>pedir una carta de donación</b></div>
    <div class="apad-btns">{wa_btns}</div>
    <p class="apad-note">Se abre WhatsApp con el mensaje ya escrito; tú solo lo revisas y envías. El donante elige a qué director escribir.</p>
  </section>

{PAY_SECTION}
  <section class="panel bud reveal" id="bud-panel">
    <h2>Explora y simula el presupuesto</h2>
    <p class="h2note">Los {len(bud_items)} ítems del Maestro. Filtra por rubro, ordena por precio o cantidad, y activa el simulador para "rejugar" cantidades y precios y ver cómo cambia lo que falta. (Para tocar y simular, ábrelo en un navegador.)</p>
    <div class="bud-ctrls">
      <div class="bchips">{bud_chips}</div>
      <div class="bud-tools">
        <label class="bud-sort">Ordenar <select id="bud-sort"><option value="monto-desc" selected>Mayor precio total</option><option value="monto-asc">Menor precio total</option><option value="qty-desc">Mayor cantidad</option><option value="name">Nombre (A–Z)</option></select></label>
        <button type="button" class="bud-simbtn" id="bud-simbtn">🧮 Simular cantidades y precios</button>
      </div>
    </div>
    <div class="bi bi-head" aria-hidden="true"><span class="bi-main">Ítem</span><span class="bi-q">Cantidad</span><span class="bi-p">Precio unit.</span><b class="bi-t">Total</b><span></span></div>
    <div class="bud-list" id="bud-list">{bud_rows}</div>
    <div class="bud-foot"><b id="bud-count">{len(bud_items)}</b> ítems mostrados · subtotal mostrado <b id="bud-sub">{money(sub_operativo)}</b></div>
    <div class="sim2" id="sim2" style="display:none">
      <div class="sim2-h">SIMULADOR · esto NO cambia el presupuesto real — es un "¿y si…?"</div>
      <div class="sim2-grid">
        <div class="sim2-c"><div class="sim2-l">Meta simulada (con ~10%)</div><div class="sim2-v" id="sim2-meta">{money(meta)}</div></div>
        <div class="sim2-c"><div class="sim2-l">vs. original</div><div class="sim2-dif" id="sim2-dif">igual al original</div></div>
        <div class="sim2-c"><div class="sim2-l">Falta por reunir (simulado)</div><div class="sim2-v red" id="sim2-falta">{money(brecha)}</div></div>
      </div>
      <button type="button" class="sim-btn" id="sim2-reset">Reiniciar valores</button>
    </div>
    <p class="pres-foot">Subtotal operativo <b>{money(sub_operativo)}</b> + 10% de imprevistos = <b>{money(meta)}</b> (la meta de la misión).</p>
  </section>

  <footer>
    Hecho por la tripulación · desde data/estado.json y el Presupuesto Maestro · actualizado {ACTUALIZADO}.<br>
    La avanzada del equipo (jueves, ~{av['personas']} personas: {av['comidas']['cantidad']} comidas + {av['hospedaje']['noches']} noche) está como PROPUESTA y NO se suma al costo. El control de pagos por nombre es interno (Excel de Tesorería).
  </footer>
</main>'''

PAGE = ('<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<meta name="description" content="ETC · Misión 88: lo que cuesta la misión y cómo, como tripulación, la hacemos posible. Apadrina un rubro o pide una carta de donación.">'
        '<title>ETC · Misión 88 · Tablero de la Tripulación</title>'
        '<style>' + CSS + '</style></head>'
        '<body class="no-js">' + BODY +
        '<script>document.body.classList.remove("no-js");' + JS + '</script>'
        '</body></html>')

with open(os.path.join(REPO, 'tablero_campana_etc88.html'), 'w', encoding='utf-8') as f:
    f.write(PAGE)
# copia lista para hosting privado (Cloudflare Pages / repo-connect): public/index.html
_pub = os.path.join(REPO, 'public'); os.makedirs(_pub, exist_ok=True)
with open(os.path.join(_pub, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(PAGE)

print("OK  tablero_campana_etc88.html  (contenido renderizado en HTML — legible sin JS / en móvil)")
print(f"    cita: «{cita['valor']}» {cita['cita']}")
print(f"    estructura {len(estructura)} rubros · presupuesto {len(presupuesto)} rubros · subtotal {sub_operativo:,.0f}")
print(f"    música ahora: {corr['areas'][1]['items']}")
print(f"    días: cierre {dias_cpago} · lanzamiento {dias_ret}")
print("    aritmética cuadra ✓")
