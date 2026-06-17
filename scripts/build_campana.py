#!/usr/bin/env python3
"""Genera el Tablero de Campaña (recaudación) del ETC 88 como UN archivo HTML
autocontenido (HTML + CSS + JS nativo, sin dependencias externas, sin CDNs).

Comunica 3 mensajes al EQUIPO:
  1. El COSTO REAL del retiro (por participante y por equipo, y de qué se
     compone) — para dimensionar el esfuerzo, que no es solo cuota+donaciones
     ni responsabilidad exclusiva de los directores.
  2. Los DRIVERS que alivianan el costo (Profondo, donaciones al presupuesto,
     donaciones en especie) — juntos lo bajamos.
  3. La CORRESPONSABILIDAD: qué cubre/prepara cada área (Guías, Música, Cocina,
     Directores).

Cifras trazadas a data/estado.json (Presupuesto Maestro + papel de costos por
persona, conciliado al peso con LADO A del Maestro):
  meta 553,622 · cuotas firmes 256,000 · palancas 215,000 · especie 114,701 ·
  proyección 585,701 · superávit +32,079 · brecha 297,622 ·
  costo/participante 6,548.92 · costo/equipo 4,523.53 (con 10% de imprevistos).

REGLAS ETC 88: nada se inventa (montos desde estado.json); lo no firme va como
'estimado'; fechas del ICS; es GENERADO (regla #2).

Salida:  tablero_campana_etc88.html
Uso:     python scripts/build_campana.py
"""
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EST = json.load(open(os.path.join(REPO, 'data', 'estado.json'), encoding='utf-8'))

# ----------------------------------------------------------- leer estado.json
fin = EST['finanzas']
meta_blk = fin['meta_recaudacion_total']
desg = meta_blk['desglose']
plan = fin['plan_recaudacion']['fuentes_caja_plan_a']
cpp = fin['costos_por_persona']
corr = fin['corresponsabilidad_areas']

meta      = meta_blk['valor']                 # 553_622
cuotas    = desg['cuotas_firmes']             # 256_000
brecha    = desg['brecha_tras_cuotas']        # 297_622
especie   = desg['especie_potencial']         # 114_701
margen    = desg['margen_proyectado']         # 32_079
rifa      = plan['rifa_profondo']['monto']    # 90_000
garaje    = plan['venta_garaje']['monto']     # 60_000
comida    = plan['venta_comida']['monto']     # 25_000
efectivo  = plan['donaciones_efectivo']['monto']   # 40_000
caja_obj  = plan['total_caja_objetivo']       # 471_000

cuota_part   = fin['cuota_participante']['valor']        # 3_000
n_part       = fin['participantes_objetivo']['valor']    # 50
part_cuotas  = cuota_part * n_part                       # 150_000
equipo_cuotas = cuotas - part_cuotas                     # 106_000

desglose   = cpp['participante']['desglose_persona']
part_costo = cpp['participante']['con_imprevistos_persona']   # 6_548.92
eq_costo   = cpp['equipo']['con_imprevistos_persona']         # 4_523.53
part_oper  = cpp['participante']['operativo_persona']         # 5_953.56
eq_oper    = cpp['equipo']['operativo_persona']               # 4_112.13

lema = EST['marca']['lema_retiro']['valor']

# ----------------------------------------------------- chequeo de aritmética
palancas   = rifa + garaje + comida + efectivo            # 215_000
profondo   = rifa + garaje + comida                       # 175_000
proyeccion = cuotas + palancas + especie                  # 585_701
superavit  = proyeccion - meta                            # 32_079

errores = []
if palancas + cuotas != caja_obj:
    errores.append(f"caja objetivo {caja_obj} ≠ cuotas+palancas {cuotas+palancas}")
if meta - cuotas != brecha:
    errores.append(f"brecha {brecha} ≠ meta-cuotas {meta-cuotas}")
if superavit != margen:
    errores.append(f"superávit {superavit} ≠ margen estado.json {margen}")
if round(sum(desglose.values()), 2) != part_oper:
    errores.append(f"desglose participante {sum(desglose.values())} ≠ {part_oper}")
tie = round(part_costo * n_part + eq_costo * cpp['base_personas']['equipo'])
if abs(tie - meta) > 5:
    errores.append(f"costo/persona×50 {tie} no amarra con meta {meta}")
if errores:
    raise SystemExit("CIFRAS NO CUADRAN con estado.json:\n  - " + "\n  - ".join(errores))

# ------------------------------------------------------------- objeto datos
datos = {
    "evento": "Retiro ETC 88",
    "subtitulo": "El costo real del retiro · cómo lo bajamos entre todos · quién cubre qué",
    "lema": lema,
    "citaBiblica": "Mt 6, 21",
    "moneda": "RD$",
    "locale": "es-DO",
    "actualizado": "17 de junio de 2026",

    "fechaCierrePagos": "2026-08-30",
    "fechaCierrePagosTexto": "30 de agosto de 2026",
    "fechaRetiro": "2026-09-04",
    "fechaRetiroTexto": "4 – 6 de septiembre de 2026",

    "costoTotal": meta,
    "recaudado": cuotas,

    # Fuentes (gráfico). tipo: firme|estimado|especie · grupo: cuota|profondo|donacion|especie
    "fuentes": [
        {"nombre": "Cuotas (participantes + equipo)", "monto": cuotas,   "tipo": "firme",    "grupo": "cuota"},
        {"nombre": "Rifa / Profondo",                 "monto": rifa,     "tipo": "estimado", "grupo": "profondo"},
        {"nombre": "Venta de garaje",                 "monto": garaje,   "tipo": "estimado", "grupo": "profondo"},
        {"nombre": "Venta de comida",                 "monto": comida,   "tipo": "estimado", "grupo": "profondo"},
        {"nombre": "Donaciones en efectivo",          "monto": efectivo, "tipo": "estimado", "grupo": "donacion"},
        {"nombre": "Donaciones en especie",           "monto": especie,  "tipo": "especie",  "grupo": "especie"},
    ],

    "cuotasDetalle": {
        "participantes": part_cuotas, "equipo": equipo_cuotas,
        "notaParticipantes": f"{n_part} × {cuota_part:,}", "notaEquipo": "53 × 2,000",
    },

    "costoPersona": {
        "base": "incluye el 10% de imprevistos",
        "participante": {"costo": part_costo, "cuota": cpp['participante']['cuota'], "operativo": part_oper},
        "equipo":       {"costo": eq_costo,   "cuota": cpp['equipo']['cuota'],       "operativo": eq_oper},
        "numParticipantes": cpp['base_personas']['participantes'],
        "numEquipo": cpp['base_personas']['equipo'],
    },
    "desgloseParticipante": desglose,
    "corresponsabilidad": corr['areas'],
}

datos_json = json.dumps(datos, ensure_ascii=False, indent=2)

# =========================================================================
#  PLANTILLA  (HTML + CSS + JS)  — el único marcador es __DATOS_JSON__
# =========================================================================
TEMPLATE = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Retiro ETC 88 · Tablero de Campaña</title>
<style>
  :root{
    --bg:#0B1F3A; --bg2:#0e2a4d; --bg3:#091830;
    --ink:#EAF2FF; --muted:#9DB2D4; --muted2:#6F87AD;
    --line:rgba(255,255,255,.10); --card:rgba(255,255,255,.045); --card-h:rgba(255,255,255,.075);
    --green:#34D399; --green2:#10B981; --green3:#059669;
    --amber:#FBBF24; --sky:#38BDF8; --gold:#F2C572;
    --shadow:0 20px 50px -20px rgba(0,0,0,.6); --r:20px;
  }
  *{box-sizing:border-box; margin:0; padding:0}
  html{scroll-behavior:smooth}
  body{
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    color:var(--ink); line-height:1.5; min-height:100vh;
    background:
      radial-gradient(1100px 700px at 12% -8%, rgba(52,211,153,.13), transparent 60%),
      radial-gradient(900px 600px at 95% 0%, rgba(56,189,248,.12), transparent 55%),
      radial-gradient(1200px 900px at 50% 120%, rgba(16,185,129,.08), transparent 60%),
      linear-gradient(160deg, var(--bg2), var(--bg) 45%, var(--bg3));
    background-attachment:fixed; -webkit-font-smoothing:antialiased; padding:clamp(16px,3vw,40px);
  }
  .wrap{max-width:1180px; margin:0 auto}

  header{text-align:center; padding:clamp(20px,4vw,48px) 0 clamp(14px,2vw,26px)}
  .eyebrow{display:inline-block; font-size:clamp(.72rem,1.4vw,.86rem); letter-spacing:.28em;
    text-transform:uppercase; color:var(--green); font-weight:700; padding:7px 16px;
    border:1px solid rgba(52,211,153,.35); border-radius:100px; background:rgba(52,211,153,.08)}
  h1{font-size:clamp(2.4rem,7vw,5rem); font-weight:800; line-height:1.02; letter-spacing:-.02em; margin:18px 0 6px;
    background:linear-gradient(180deg,#fff,#cfe0ff 70%,#9db2d4); -webkit-background-clip:text; background-clip:text; color:transparent}
  .sub{color:var(--muted); font-size:clamp(1rem,2.2vw,1.32rem); font-weight:500}
  .lema{margin:18px auto 0; max-width:680px; color:var(--gold); font-style:italic; font-size:clamp(1rem,2.4vw,1.45rem); line-height:1.35}
  .lema b{font-style:normal; color:var(--muted2); font-size:.8em; display:block; margin-top:6px; letter-spacing:.04em}

  .kpis{display:grid; gap:clamp(10px,1.6vw,18px); margin:clamp(20px,3vw,34px) 0;
    grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
  .kpi{background:var(--card); border:1px solid var(--line); border-radius:var(--r); padding:clamp(16px,2vw,24px);
    position:relative; overflow:hidden; transition:transform .35s ease, background .35s ease, border-color .35s ease}
  .kpi:hover{transform:translateY(-4px); background:var(--card-h); border-color:rgba(255,255,255,.2)}
  .kpi::before{content:""; position:absolute; inset:0 auto auto 0; width:100%; height:3px; background:linear-gradient(90deg,var(--green),var(--sky))}
  .kpi .lbl{font-size:.82rem; letter-spacing:.06em; text-transform:uppercase; color:var(--muted)}
  .kpi .val{font-size:clamp(1.6rem,3.4vw,2.5rem); font-weight:800; letter-spacing:-.02em; margin-top:8px; font-variant-numeric:tabular-nums; line-height:1.05}
  .kpi .note{font-size:.82rem; color:var(--muted2); margin-top:6px}
  .kpi.accent .val{color:var(--green)} .kpi.warn .val{color:var(--amber)}

  .panel{background:var(--card); border:1px solid var(--line); border-radius:var(--r); padding:clamp(18px,2.6vw,32px);
    box-shadow:var(--shadow); margin-bottom:clamp(14px,2vw,22px)}
  .panel h2{font-size:clamp(1.15rem,2.4vw,1.6rem); font-weight:700; letter-spacing:-.01em}
  .panel .h2note{color:var(--muted); font-size:.9rem; margin-top:4px; margin-bottom:18px}
  .grid2{display:grid; gap:clamp(14px,2vw,22px); grid-template-columns:1fr 1fr}
  @media(max-width:820px){ .grid2{grid-template-columns:1fr} }

  /* costo por persona */
  .pcard{background:rgba(0,0,0,.18); border:1px solid var(--line); border-radius:16px; padding:clamp(18px,2.4vw,26px)}
  .pc-tag{color:var(--muted); text-transform:uppercase; letter-spacing:.08em; font-size:.8rem; font-weight:700}
  .pc-cost{font-size:clamp(2rem,6vw,3rem); font-weight:800; color:var(--green); margin:6px 0 16px; font-variant-numeric:tabular-nums; line-height:1}
  .pc-rows{display:grid; gap:9px; margin-bottom:16px; font-variant-numeric:tabular-nums}
  .pc-rows>div{display:flex; justify-content:space-between; gap:12px}
  .pc-rows span{color:var(--muted)} .pc-rows b.warn{color:var(--amber)}
  .cover{height:12px; border-radius:6px; background:rgba(255,255,255,.08); overflow:hidden}
  .cover i{display:block; height:100%; width:0; background:linear-gradient(90deg,var(--green),var(--green3)); transition:width 1.3s cubic-bezier(.16,1,.3,1)}
  .cover-lbl{color:var(--muted); font-size:.85rem; margin-top:8px} .cover-lbl b{color:var(--ink)}
  .pc-foot{color:var(--muted); margin-top:18px; font-size:.92rem} .pc-foot b{color:var(--ink)}

  /* composición del costo */
  .compo{margin-top:24px; padding-top:22px; border-top:1px solid var(--line)}
  .compo-h{font-weight:700; margin-bottom:16px}
  .compo-row{display:grid; grid-template-columns:1fr auto; gap:5px 12px; align-items:center; margin-bottom:13px}
  .compo-row .cl{color:var(--ink)} .compo-row .cv{color:var(--muted); font-variant-numeric:tabular-nums; font-weight:700}
  .compo-row .ct{grid-column:1 / -1; height:8px; border-radius:4px; background:rgba(255,255,255,.07); overflow:hidden}
  .compo-row .ct i{display:block; height:100%; width:0; background:linear-gradient(90deg,var(--green),var(--green3)); transition:width 1s cubic-bezier(.16,1,.3,1)}
  .compo-foot{color:var(--muted); margin-top:8px; font-size:.92rem} .compo-foot b{color:var(--ink)}

  /* thermometer */
  .thermo-flex{display:flex; gap:clamp(14px,3vw,30px); align-items:center}
  .thermo-svg{width:clamp(120px,28vw,168px); flex:none}
  .thermo-svg svg{display:block; width:100%; height:auto; overflow:visible}
  .thermo-info{flex:1; min-width:0}
  .big-pct{font-size:clamp(3rem,11vw,5.2rem); font-weight:800; line-height:.95; letter-spacing:-.03em; color:var(--green); font-variant-numeric:tabular-nums}
  .big-pct small{font-size:.42em; color:var(--muted); font-weight:600; letter-spacing:0}
  .th-rows{margin-top:18px; display:grid; gap:10px}
  .th-row{display:flex; justify-content:space-between; align-items:baseline; gap:12px; padding-bottom:10px; border-bottom:1px solid var(--line); font-variant-numeric:tabular-nums}
  .th-row:last-child{border-bottom:0; padding-bottom:0}
  .th-row .k{color:var(--muted); font-size:.95rem} .th-row .v{font-weight:700; font-size:1.1rem}
  .th-row.is-falta .v{color:var(--amber)}

  /* countdown */
  .cd-two{display:grid; gap:14px}
  .cd-block{background:rgba(0,0,0,.18); border:1px solid var(--line); border-radius:14px; padding:14px 14px 16px}
  .cd-block.urgent{border-color:rgba(251,191,36,.45); background:rgba(251,191,36,.06)}
  .cd-head{color:var(--muted); font-size:.85rem; margin-bottom:10px} .cd-head b{color:var(--ink)}
  .cd-block.urgent .cd-head b{color:var(--amber)}
  .cd-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:clamp(6px,1.2vw,12px)}
  .cd-cell{background:rgba(0,0,0,.22); border:1px solid var(--line); border-radius:12px; padding:clamp(10px,1.6vw,16px) 4px; text-align:center}
  .cd-num{font-size:clamp(1.5rem,5vw,2.6rem); font-weight:800; font-variant-numeric:tabular-nums; line-height:1; letter-spacing:-.02em;
    background:linear-gradient(180deg,#fff,#bcd2f5); -webkit-background-clip:text; background-clip:text; color:transparent}
  .cd-block.urgent .cd-num{background:linear-gradient(180deg,#fff,#ffe2a6); -webkit-background-clip:text; background-clip:text}
  .cd-lbl{font-size:.66rem; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); margin-top:7px}

  /* bar chart */
  #chart-svg{width:100%; height:auto; display:block}
  .legend{display:flex; flex-wrap:wrap; gap:14px 22px; margin-top:18px; color:var(--muted); font-size:.88rem}
  .legend span{display:inline-flex; align-items:center; gap:8px}
  .sw{width:14px; height:14px; border-radius:4px; flex:none}
  .sw.firme{background:var(--green)} .sw.estimado{background:var(--amber)} .sw.especie{background:var(--sky)}

  /* drivers + projection */
  .proj{background:linear-gradient(135deg, rgba(52,211,153,.16), rgba(56,189,248,.08) 70%, transparent), var(--card); border:1px solid rgba(52,211,153,.3)}
  .drivers{display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin:6px 0 20px}
  .driver{background:rgba(0,0,0,.22); border:1px solid var(--line); border-radius:14px; padding:16px}
  .driver.amber{border-color:rgba(251,191,36,.32)} .driver.sky{border-color:rgba(56,189,248,.32)}
  .driver .dv{font-size:clamp(1.3rem,3.6vw,1.85rem); font-weight:800; font-variant-numeric:tabular-nums}
  .driver.amber .dv{color:var(--amber)} .driver.sky .dv{color:var(--sky)}
  .driver .dn{color:var(--muted); font-size:.85rem; margin-top:4px}
  .proj .surplus{font-size:clamp(2.2rem,7vw,3.6rem); font-weight:800; color:var(--green); letter-spacing:-.02em; font-variant-numeric:tabular-nums; line-height:1}
  .proj .surplus small{display:block; font-size:.26em; letter-spacing:.16em; text-transform:uppercase; color:var(--muted); font-weight:700; margin-bottom:6px}
  .formula{margin-top:18px; color:var(--muted); font-size:clamp(.92rem,2vw,1.05rem); line-height:1.8; font-variant-numeric:tabular-nums}
  .formula b{color:var(--ink); font-weight:700}
  .formula .t-firme{color:var(--green)} .formula .t-est{color:var(--amber)} .formula .t-esp{color:var(--sky)}
  .stack{height:34px; border-radius:10px; overflow:hidden; display:flex; margin-top:22px; background:rgba(0,0,0,.25); position:relative}
  .stack i{height:100%; display:block; width:0; transition:width 1.4s cubic-bezier(.16,1,.3,1)}
  .stack i.firme{background:linear-gradient(180deg,var(--green),var(--green3))}
  .stack i.estimado{background:linear-gradient(180deg,var(--amber),#d99908)}
  .stack i.especie{background:linear-gradient(180deg,var(--sky),#0c8fce)}
  .meta-mark{position:absolute; top:-6px; bottom:-6px; width:2px; background:#fff; box-shadow:0 0 0 1px rgba(0,0,0,.3)}
  .meta-mark span{position:absolute; top:-22px; transform:translateX(-50%); white-space:nowrap; font-size:.72rem; color:#fff; font-weight:700; letter-spacing:.04em}
  .stack-cap{display:flex; justify-content:space-between; margin-top:30px; color:var(--muted); font-size:.85rem; flex-wrap:wrap; gap:6px}
  .reduce{margin-top:20px; padding:14px 16px; border-radius:12px; background:rgba(56,189,248,.08); border:1px solid rgba(56,189,248,.25); color:var(--muted); font-size:clamp(.92rem,2vw,1.05rem); font-variant-numeric:tabular-nums}
  .reduce b{color:var(--ink)} .reduce .t-esp{color:var(--sky); font-weight:700}
  .msg{margin-top:18px; padding:18px 20px; border-radius:14px; background:rgba(0,0,0,.22); border-left:4px solid var(--green); font-size:clamp(1.02rem,2.3vw,1.28rem); line-height:1.5}
  .msg b{color:var(--green)}

  /* corresponsabilidad por área */
  .areas-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(238px,1fr)); gap:14px}
  .area-card{background:rgba(0,0,0,.18); border:1px solid var(--line); border-radius:16px; padding:18px 20px; border-top:3px solid var(--green)}
  .area-h{display:flex; justify-content:space-between; align-items:baseline; gap:10px; margin-bottom:12px; padding-bottom:11px; border-bottom:1px solid var(--line)}
  .area-name{font-weight:800; font-size:1.18rem}
  .area-amt{color:var(--muted); font-weight:700; font-variant-numeric:tabular-nums; white-space:nowrap; font-size:.95rem}
  .area-items{list-style:none; display:grid; gap:8px}
  .area-items li{color:var(--muted); padding-left:18px; position:relative; font-size:.95rem}
  .area-items li::before{content:""; position:absolute; left:3px; top:.55em; width:6px; height:6px; border-radius:50%; background:var(--green)}
  .areas-foot{color:var(--muted); margin-top:16px; font-size:.9rem} .areas-foot b{color:var(--ink)}

  footer{text-align:center; color:var(--muted2); font-size:.82rem; padding:26px 0 8px; line-height:1.7}

  .reveal{opacity:0; transform:translateY(20px); transition:opacity .7s ease, transform .7s cubic-bezier(.16,1,.3,1)}
  .reveal.visible{opacity:1; transform:none}
  @media(prefers-reduced-motion:reduce){
    .reveal{opacity:1; transform:none; transition:none}
    .stack i, .cover i, .compo-row .ct i{transition:none}
    html{scroll-behavior:auto}
  }
</style>
</head>
<body>
<div class="wrap">

  <header class="reveal">
    <span class="eyebrow">Encuentro Total con Cristo</span>
    <h1 id="evento">Retiro ETC 88</h1>
    <p class="sub" id="subtitulo"></p>
    <p class="lema" id="lema"></p>
  </header>

  <!-- KPI row -->
  <section class="kpis reveal" id="kpis">
    <div class="kpi"><div class="lbl">Costo total (meta)</div><div class="val" id="kpi-costo">RD$ 0</div><div class="note">cubrir el costo del retiro</div></div>
    <div class="kpi accent"><div class="lbl">Recaudado a la fecha</div><div class="val" id="kpi-recaudado">RD$ 0</div><div class="note">cuotas firmes comprometidas</div></div>
    <div class="kpi accent"><div class="lbl">% cubierto</div><div class="val" id="kpi-pct">0%</div><div class="note">de la meta</div></div>
    <div class="kpi warn"><div class="lbl">Falta por recaudar</div><div class="val" id="kpi-falta">RD$ 0</div><div class="note">brecha tras cuotas</div></div>
    <div class="kpi"><div class="lbl">Días: cierre de pagos</div><div class="val" id="kpi-dias">0</div><div class="note" id="kpi-dias-note">retiro: 4–6 sep</div></div>
  </section>

  <!-- 1 · costo real por persona -->
  <section class="panel reveal" id="costo-panel">
    <h2>1 · Lo que cuesta el retiro de verdad</h2>
    <p class="h2note">Costo real por cabeza (incluye el 10% de imprevistos) vs. la cuota que paga cada quien</p>
    <div class="grid2">
      <div class="pcard">
        <div class="pc-tag">Por participante</div>
        <div class="pc-cost" id="pc-part-cost">RD$ 0</div>
        <div class="pc-rows">
          <div><span>Cuota que paga</span><b id="pc-part-cuota">RD$ 0</b></div>
          <div><span>No cubre la cuota</span><b class="warn" id="pc-part-falta">RD$ 0</b></div>
        </div>
        <div class="cover"><i id="pc-part-bar" data-w="0"></i></div>
        <div class="cover-lbl">la cuota cubre <b id="pc-part-pct">0%</b> de su costo</div>
      </div>
      <div class="pcard">
        <div class="pc-tag">Por miembro de equipo</div>
        <div class="pc-cost" id="pc-eq-cost">RD$ 0</div>
        <div class="pc-rows">
          <div><span>Cuota que paga</span><b id="pc-eq-cuota">RD$ 0</b></div>
          <div><span>No cubre la cuota</span><b class="warn" id="pc-eq-falta">RD$ 0</b></div>
        </div>
        <div class="cover"><i id="pc-eq-bar" data-w="0"></i></div>
        <div class="cover-lbl">la cuota cubre <b id="pc-eq-pct">0%</b> de su costo</div>
      </div>
    </div>
    <div class="compo">
      <div class="compo-h">¿De qué se compone el costo de cada participante?</div>
      <div id="compo-bars"></div>
      <div class="compo-foot">Suma <b id="compo-sum">RD$ 0</b> (operativo) + 10% de imprevistos = <b id="compo-total">RD$ 0</b> por participante. Lo que la cuota no cubre <b>no recae en el participante</b>: lo bajan los drivers de abajo.</div>
    </div>
  </section>

  <!-- thermometer + countdowns -->
  <div class="grid2">
    <section class="panel reveal" id="thermo-panel">
      <h2>Progreso hacia la meta</h2>
      <p class="h2note">Recaudado vs. costo total del retiro</p>
      <div class="thermo-flex">
        <div class="thermo-svg" aria-hidden="true">
          <svg viewBox="0 0 200 470" role="img">
            <defs>
              <linearGradient id="gradFill" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stop-color="#059669"/><stop offset="55%" stop-color="#10B981"/><stop offset="100%" stop-color="#34D399"/>
              </linearGradient>
              <clipPath id="tubeClip"><rect x="84" y="24" width="38" height="350" rx="19"/></clipPath>
            </defs>
            <circle cx="103" cy="406" r="40" fill="rgba(255,255,255,.05)" stroke="rgba(255,255,255,.14)"/>
            <rect x="84" y="24" width="38" height="350" rx="19" fill="rgba(255,255,255,.05)" stroke="rgba(255,255,255,.14)"/>
            <circle cx="103" cy="406" r="33" fill="url(#gradFill)"/>
            <circle cx="94" cy="396" r="9" fill="rgba(255,255,255,.28)"/>
            <rect id="thermo-fill" x="84" y="374" width="38" height="0" fill="url(#gradFill)" clip-path="url(#tubeClip)"/>
            <line x1="70" x2="150" y1="24" y2="24" stroke="#fff" stroke-width="2" stroke-dasharray="4 4" opacity=".75"/>
            <text x="128" y="18" fill="#fff" font-size="12" font-weight="700">META</text>
            <g stroke="rgba(255,255,255,.25)" font-size="11" fill="var(--muted)">
              <line x1="122" x2="132" y1="111.5" y2="111.5"/><text x="136" y="115">75%</text>
              <line x1="122" x2="132" y1="199" y2="199"/><text x="136" y="203">50%</text>
              <line x1="122" x2="132" y1="286.5" y2="286.5"/><text x="136" y="290">25%</text>
            </g>
            <g id="thermo-marker" transform="translate(0,374)">
              <line x1="54" x2="84" y1="0" y2="0" stroke="var(--green)" stroke-width="2"/>
              <text id="thermo-marker-pct" x="50" y="5" text-anchor="end" fill="var(--green)" font-size="15" font-weight="800">0%</text>
            </g>
          </svg>
        </div>
        <div class="thermo-info">
          <div class="big-pct"><span id="th-pct">0,0</span><small>%</small></div>
          <div style="color:var(--muted); margin-top:2px">de la meta cubierta</div>
          <div class="th-rows">
            <div class="th-row"><span class="k">Recaudado</span><span class="v" id="th-recaudado">RD$ 0</span></div>
            <div class="th-row"><span class="k">Meta (costo total)</span><span class="v" id="th-meta">RD$ 0</span></div>
            <div class="th-row is-falta"><span class="k">Falta</span><span class="v" id="th-falta">RD$ 0</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="panel reveal" id="cd-panel">
      <h2>Cuánto falta</h2>
      <p class="h2note">El dinero debe estar conciliado para el cierre de pagos, antes del retiro</p>
      <div class="cd-two">
        <div class="cd-block urgent">
          <div class="cd-head">Cierre de pagos · <b id="cd-cpago-when"></b></div>
          <div class="cd-grid">
            <div class="cd-cell"><div class="cd-num" id="cpago-d">0</div><div class="cd-lbl">Días</div></div>
            <div class="cd-cell"><div class="cd-num" id="cpago-h">00</div><div class="cd-lbl">Hrs</div></div>
            <div class="cd-cell"><div class="cd-num" id="cpago-m">00</div><div class="cd-lbl">Min</div></div>
            <div class="cd-cell"><div class="cd-num" id="cpago-s">00</div><div class="cd-lbl">Seg</div></div>
          </div>
        </div>
        <div class="cd-block">
          <div class="cd-head">Inicio del retiro · <b id="cd-ret-when"></b></div>
          <div class="cd-grid">
            <div class="cd-cell"><div class="cd-num" id="ret-d">0</div><div class="cd-lbl">Días</div></div>
            <div class="cd-cell"><div class="cd-num" id="ret-h">00</div><div class="cd-lbl">Hrs</div></div>
            <div class="cd-cell"><div class="cd-num" id="ret-m">00</div><div class="cd-lbl">Min</div></div>
            <div class="cd-cell"><div class="cd-num" id="ret-s">00</div><div class="cd-lbl">Seg</div></div>
          </div>
        </div>
      </div>
    </section>
  </div>

  <!-- bar chart -->
  <section class="panel reveal" id="chart-panel">
    <h2>Recaudación por fuente</h2>
    <p class="h2note">Cuotas firmes + palancas estimadas + donaciones en especie</p>
    <svg id="chart-svg" role="img" aria-label="Recaudación por fuente"></svg>
    <div class="legend">
      <span><i class="sw firme"></i> Firme (comprometido)</span>
      <span><i class="sw estimado"></i> Estimado (palanca, no firme)</span>
      <span><i class="sw especie"></i> En especie (no es caja, reduce el costo)</span>
    </div>
  </section>

  <!-- 2 · drivers + projection -->
  <section class="panel proj reveal" id="proj-panel">
    <h2>2 · Drivers que alivianan: juntos bajamos el costo</h2>
    <p class="h2note">El costo no recae solo en las cuotas ni en los directores — estos drivers lo cubren y lo bajan entre todos</p>
    <div class="drivers" id="drivers"></div>
    <div class="surplus"><small>Superávit proyectado sobre el costo</small><span id="pr-superavit">RD$ 0</span></div>
    <div class="formula">
      <span class="t-firme"><b id="pr-cuotas">RD$ 0</b> cuotas</span> +
      <span class="t-est"><b id="pr-palancas">RD$ 0</b> palancas/Profondo</span> +
      <span class="t-esp"><b id="pr-especie">RD$ 0</b> especie</span> =
      <b id="pr-proyeccion">RD$ 0</b> proyectado &nbsp;vs.&nbsp; meta <b id="pr-meta">RD$ 0</b>
    </div>
    <div class="stack" id="stack"></div>
    <div class="stack-cap"><span>Recaudación total proyectada</span><span id="stack-total">RD$ 0</span></div>
    <div class="reduce">Las <b>donaciones en especie</b> reducen el costo peso a peso:
      <span id="rd-meta">RD$ 0</span> − <span class="t-esp" id="rd-especie">RD$ 0</span> = <b id="rd-caja">RD$ 0</b> a cubrir en efectivo.</div>
    <p class="msg">Si conseguimos las <b>donaciones en especie</b> (<span id="s-especie">RD$ 0</span>)
      y las <b>palancas</b>, cerramos con <b>superávit de <span id="s-superavit">RD$ 0</span></b>.</p>
  </section>

  <!-- 3 · corresponsabilidad -->
  <section class="panel reveal" id="areas-panel">
    <h2>3 · Corresponsabilidad: quién cubre qué</h2>
    <p class="h2note">El esfuerzo no es solo de los directores ni de las cuotas — cada área carga su parte</p>
    <div class="areas-grid" id="areas-grid"></div>
    <p class="areas-foot">Montos <b>indicativos</b> del Presupuesto Maestro. Además, <b>casa, transporte y la coordinación general</b> completan el costo total (RD$ 553,622).</p>
  </section>

  <footer>
    Generado desde <b>data/estado.json</b> (Presupuesto Maestro · papel de costos por persona conciliado al peso) · actualizado <span id="ft-fecha"></span>.<br>
    Cifras: cuotas = firmes · palancas y especie = <b>estimadas (no firmes)</b>. Edita el objeto <code>datos</code> para actualizar.
  </footer>

</div>

<script>
/* =========================================================================
   ETC 88 · TABLERO DE CAMPAÑA  —  DATOS EDITABLES (objeto `datos`)
   Cifras trazadas a data/estado.json. Edita un valor y recarga: el %, la
   brecha, la proyección, el superávit y los costos por persona se recalculan.
   ========================================================================= */
const datos = __DATOS_JSON__;

/* ---- Derivados (se calculan solos) ------------------------------------ */
const sumTipo  = t => datos.fuentes.filter(f => f.tipo  === t).reduce((a, f) => a + f.monto, 0);
const sumGrupo = g => datos.fuentes.filter(f => f.grupo === g).reduce((a, f) => a + f.monto, 0);
const D = { cuotas:sumTipo('firme'), palancas:sumTipo('estimado'), especie:sumTipo('especie') };
D.proyeccion = datos.fuentes.reduce((a, f) => a + f.monto, 0);
D.pct        = Math.min(100, (datos.recaudado / datos.costoTotal) * 100);
D.falta      = Math.max(0, datos.costoTotal - datos.recaudado);
D.superavit  = D.proyeccion - datos.costoTotal;
D.cajaTrasEspecie = datos.costoTotal - D.especie;
const DR = { profondo:sumGrupo('profondo'), donacion:sumGrupo('donacion'), especie:sumGrupo('especie') };

const CP = datos.costoPersona;
['participante', 'equipo'].forEach(k => {
  CP[k].noCubre  = CP[k].costo - CP[k].cuota;
  CP[k].cubrePct = CP[k].cuota / CP[k].costo * 100;
});

/* ---- Utilidades ------------------------------------------------------- */
const REDUCE = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const nf  = new Intl.NumberFormat(datos.locale || 'es-DO');
const nf2 = new Intl.NumberFormat(datos.locale || 'es-DO', {minimumFractionDigits:2, maximumFractionDigits:2});
const money  = n => datos.moneda + ' ' + nf.format(Math.round(n));
const money2 = n => datos.moneda + ' ' + nf2.format(n);
const pctTxt = n => n.toFixed(1).replace('.', ',');
const $ = id => document.getElementById(id);
const setText = (id, v) => { const e = $(id); if (e) e.textContent = v; };
const easeOutCubic = t => 1 - Math.pow(1 - t, 3);

function animate(duration, onUpdate, onDone){
  if (REDUCE){ onUpdate(1); if (onDone) onDone(); return; }
  const t0 = performance.now();
  function frame(now){
    const t = Math.min(1, (now - t0) / duration);
    onUpdate(easeOutCubic(t));
    if (t < 1) requestAnimationFrame(frame); else if (onDone) onDone();
  }
  requestAnimationFrame(frame);
}
function countUp(id, to, fmt, dur){ const e = $(id); if (!e) return; animate(dur || 1600, p => { e.textContent = fmt(to * p); }); }

/* ---- Textos estáticos ------------------------------------------------- */
setText('evento', datos.evento);
setText('subtitulo', datos.subtitulo);
$('lema').innerHTML = '«' + datos.lema + '»<b>' + datos.citaBiblica + '</b>';
setText('cd-cpago-when', datos.fechaCierrePagosTexto);
setText('cd-ret-when', datos.fechaRetiroTexto);
setText('ft-fecha', datos.actualizado);
setText('th-meta', money(datos.costoTotal));
setText('pr-meta', money(datos.costoTotal));

/* ---- Fechas objetivo (medianoche local) ------------------------------- */
function dateLocal(iso){ const p = iso.split('-').map(Number); return new Date(p[0], p[1]-1, p[2], 0,0,0,0); }
function diffParts(iso){
  let ms = Math.max(0, dateLocal(iso).getTime() - Date.now());
  const d = Math.floor(ms/86400000); ms -= d*86400000;
  const h = Math.floor(ms/3600000);  ms -= h*3600000;
  const m = Math.floor(ms/60000);    ms -= m*60000;
  return {d, h, m, s:Math.floor(ms/1000)};
}
function mkCountdown(prefix, iso){
  function tick(){
    const t = diffParts(iso);
    setText(prefix+'-d', t.d);
    setText(prefix+'-h', String(t.h).padStart(2,'0'));
    setText(prefix+'-m', String(t.m).padStart(2,'0'));
    setText(prefix+'-s', String(t.s).padStart(2,'0'));
  }
  tick(); setInterval(tick, 1000);
}

/* ---- KPIs ------------------------------------------------------------- */
function runKpis(){
  countUp('kpi-costo', datos.costoTotal, money);
  countUp('kpi-recaudado', datos.recaudado, money);
  countUp('kpi-falta', D.falta, money);
  animate(1600, p => { $('kpi-pct').textContent = pctTxt(D.pct * p) + '%'; });
  animate(1600, p => { $('kpi-dias').textContent = nf.format(Math.round(diffParts(datos.fechaCierrePagos).d * p)); });
}

/* ---- Costo por persona + composición ---------------------------------- */
const DESG_LBL = {casa:'Casa (hospedaje)', cocina:'Comida (cocina)', biblias_y_peces:'Biblia + pez',
                  transporte:'Transporte', guias:'Materiales de guía / PG', liturgico:'Litúrgico', musica:'Música'};
const DESG_ORDER = ['casa','cocina','biblias_y_peces','transporte','guias','liturgico','musica'];
function runCosto(){
  countUp('pc-part-cost', CP.participante.costo, money2);
  setText('pc-part-cuota', money(CP.participante.cuota));
  countUp('pc-part-falta', CP.participante.noCubre, money2);
  setText('pc-part-pct', pctTxt(CP.participante.cubrePct) + '%');
  countUp('pc-eq-cost', CP.equipo.costo, money2);
  setText('pc-eq-cuota', money(CP.equipo.cuota));
  countUp('pc-eq-falta', CP.equipo.noCubre, money2);
  setText('pc-eq-pct', pctTxt(CP.equipo.cubrePct) + '%');
  const fillCover = () => { $('pc-part-bar').style.width = CP.participante.cubrePct+'%'; $('pc-eq-bar').style.width = CP.equipo.cubrePct+'%'; };
  if (REDUCE) fillCover(); else setTimeout(fillCover, 120);
  // composición
  const wrap = $('compo-bars'), d = datos.desgloseParticipante;
  const max = Math.max.apply(null, DESG_ORDER.map(k => d[k]));
  let sum = 0;
  DESG_ORDER.forEach(k => {
    sum += d[k];
    const row = document.createElement('div'); row.className = 'compo-row';
    row.innerHTML = '<span class="cl">' + DESG_LBL[k] + '</span><span class="cv">' + money2(d[k]) + '</span>'
                  + '<div class="ct"><i data-w="' + (d[k]/max*100).toFixed(2) + '"></i></div>';
    wrap.appendChild(row);
  });
  setText('compo-sum', money2(sum));
  setText('compo-total', money2(CP.participante.costo));
  const fillCompo = () => wrap.querySelectorAll('i').forEach(i => i.style.width = i.dataset.w + '%');
  if (REDUCE) fillCompo(); else setTimeout(fillCompo, 160);
}

/* ---- Termómetro -------------------------------------------------------- */
function runThermo(){
  const fill = $('thermo-fill'), marker = $('thermo-marker'), mpct = $('thermo-marker-pct');
  const TOP = 24, BOTTOM = 374, RANGE = BOTTOM - TOP;
  const fracTarget = D.pct / 100;
  setText('th-recaudado', money(datos.recaudado));
  setText('th-falta', money(D.falta));
  animate(1800, p => {
    const frac = fracTarget * p, y = BOTTOM - frac * RANGE;
    fill.setAttribute('y', y); fill.setAttribute('height', BOTTOM - y);
    marker.setAttribute('transform', 'translate(0,' + y + ')');
    mpct.textContent = pctTxt(frac*100) + '%';
    $('th-pct').textContent = pctTxt(frac*100);
  });
}

/* ---- Gráfico de barras (SVG) ------------------------------------------ */
const SVGNS = 'http://www.w3.org/2000/svg';
function el(name, attrs){ const e = document.createElementNS(SVGNS, name); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; }
const COLOR = {firme:'var(--green)', estimado:'var(--amber)', especie:'var(--sky)'};
const TIPO_LBL = {firme:'firme', estimado:'estimado', especie:'especie'};
let _mctx;
function measure(txt){ if (!_mctx){ _mctx = document.createElement('canvas').getContext('2d'); _mctx.font = '700 21px -apple-system,Segoe UI,Roboto,sans-serif'; } return _mctx.measureText(txt).width; }
function renderChart(){
  const svg = $('chart-svg'), W = 1000, X0 = 12, ROW = 78, PAD = 8, BARH = 26;
  const trackW = W - X0 * 2, max = Math.max.apply(null, datos.fuentes.map(f => f.monto));
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + (PAD + datos.fuentes.length * ROW));
  const fills = [];
  datos.fuentes.forEach((f, i) => {
    const yTop = PAD + i * ROW, yName = yTop + 22, yBar = yTop + 34;
    const name = el('text', {x:X0, y:yName, fill:'var(--ink)', 'font-size':'21', 'font-weight':'700'}); name.textContent = f.nombre; svg.appendChild(name);
    const chip = el('text', {x:X0 + measure(f.nombre) + 14, y:yName, fill:COLOR[f.tipo], 'font-size':'15', 'font-weight':'700'}); chip.textContent = '· ' + TIPO_LBL[f.tipo]; svg.appendChild(chip);
    const amt = el('text', {x:W - X0, y:yName, fill:COLOR[f.tipo], 'font-size':'21', 'font-weight':'800', 'text-anchor':'end'}); amt.textContent = money(0); svg.appendChild(amt);
    svg.appendChild(el('rect', {x:X0, y:yBar, width:trackW, height:BARH, rx:BARH/2, fill:'rgba(255,255,255,.06)'}));
    const bar = el('rect', {x:X0, y:yBar, width:0, height:BARH, rx:BARH/2, fill:COLOR[f.tipo]});
    if (f.tipo !== 'firme') bar.setAttribute('opacity', '.92');
    svg.appendChild(bar);
    fills.push({bar, amt, wTarget: trackW * (f.monto / max), monto:f.monto});
  });
  return fills;
}
function animateChart(fills){
  fills.forEach((it, i) => animate(1500 + i*90, p => {
    it.bar.setAttribute('width', it.wTarget * Math.min(1, p));
    it.amt.textContent = money(it.monto * Math.min(1, p));
  }));
}

/* ---- Drivers + proyección --------------------------------------------- */
function runProjection(){
  const wrap = $('drivers');
  const items = [
    {n:'Profondo (rifa + comida + garaje)', v:DR.profondo, c:'amber'},
    {n:'Donaciones al presupuesto (efectivo)', v:DR.donacion, c:'amber'},
    {n:'Donaciones en especie', v:DR.especie, c:'sky'},
  ];
  items.forEach(it => {
    const d = document.createElement('div'); d.className = 'driver ' + it.c;
    d.innerHTML = '<div class="dv">' + money(it.v) + '</div><div class="dn">' + it.n + '</div>';
    wrap.appendChild(d);
  });
  countUp('pr-superavit', D.superavit, n => (n >= 0 ? '+' : '') + money(n));
  countUp('pr-cuotas', D.cuotas, money);
  countUp('pr-palancas', D.palancas, money);
  countUp('pr-especie', D.especie, money);
  countUp('pr-proyeccion', D.proyeccion, money);
  countUp('stack-total', D.proyeccion, money);
  setText('rd-meta', money(datos.costoTotal));
  setText('rd-especie', money(D.especie));
  countUp('rd-caja', D.cajaTrasEspecie, money);
  countUp('s-especie', D.especie, money);
  countUp('s-superavit', D.superavit, n => (n >= 0 ? '+' : '') + money(n));
  const stack = $('stack');
  [{t:'firme', v:D.cuotas}, {t:'estimado', v:D.palancas}, {t:'especie', v:D.especie}].forEach(s => {
    const seg = document.createElement('i'); seg.className = s.t; seg.dataset.w = (s.v / D.proyeccion * 100).toFixed(3); stack.appendChild(seg);
  });
  const mark = document.createElement('div'); mark.className = 'meta-mark';
  mark.style.left = (datos.costoTotal / D.proyeccion * 100) + '%';
  mark.innerHTML = '<span>META ' + money(datos.costoTotal) + '</span>'; stack.appendChild(mark);
  const fill = () => stack.querySelectorAll('i').forEach(i => i.style.width = i.dataset.w + '%');
  if (REDUCE) fill(); else setTimeout(fill, 120);
}

/* ---- Corresponsabilidad por área -------------------------------------- */
const AREA_COLOR = {'Guías':'#34D399', 'Música':'#FBBF24', 'Cocina':'#38BDF8', 'Directores':'#F2C572'};
function renderAreas(){
  const grid = $('areas-grid');
  datos.corresponsabilidad.forEach(a => {
    const col = AREA_COLOR[a.area] || 'var(--green)';
    const c = document.createElement('div'); c.className = 'area-card'; c.style.borderTopColor = col;
    const li = a.items.map(x => '<li>' + x + '</li>').join('');
    c.innerHTML = '<div class="area-h"><span class="area-name" style="color:' + col + '">' + a.area + '</span>'
                + '<span class="area-amt">≈ ' + money(a.monto_indicativo) + '</span></div>'
                + '<ul class="area-items">' + li + '</ul>';
    grid.querySelectorAll && grid.appendChild(c);
  });
}

/* ---- Reveal + init ---------------------------------------------------- */
function onVisible(node, cb){
  if (!node) return;
  if (!('IntersectionObserver' in window)){ cb(); return; }
  const io = new IntersectionObserver((entries, obs) => { entries.forEach(e => { if (e.isIntersecting){ cb(); obs.disconnect(); } }); }, {threshold:.2});
  io.observe(node);
}
window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.reveal').forEach(n => onVisible(n, () => n.classList.add('visible')));
  mkCountdown('cpago', datos.fechaCierrePagos);
  mkCountdown('ret', datos.fechaRetiro);
  renderAreas();
  let chartFills = null;
  onVisible($('kpis'), runKpis);
  onVisible($('costo-panel'), runCosto);
  onVisible($('thermo-panel'), runThermo);
  onVisible($('chart-panel'), () => { if (!chartFills) chartFills = renderChart(); animateChart(chartFills); });
  onVisible($('proj-panel'), runProjection);
});
</script>
</body>
</html>
'''

html = TEMPLATE.replace('__DATOS_JSON__', datos_json)
out = os.path.join(REPO, 'tablero_campana_etc88.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print("OK  tablero_campana_etc88.html")
print(f"    meta              RD$ {meta:,}")
print(f"    costo/participante RD$ {part_costo:,.2f}  (operativo {part_oper:,.2f} + 10%)")
print(f"    costo/equipo       RD$ {eq_costo:,.2f}")
print(f"    composición part.  {' + '.join(f'{k} {v:,.2f}' for k,v in desglose.items())}")
print(f"    drivers           Profondo {profondo:,} · efectivo {efectivo:,} · especie {especie:,}")
print(f"    áreas             {', '.join(a['area']+' ≈'+format(a['monto_indicativo'],',') for a in corr['areas'])}")
print(f"    proyección        RD$ {proyeccion:,}  · superávit RD$ {superavit:,}")
print("    aritmética cuadra con data/estado.json ✓  (imagen ≡ LADO A del Maestro)")
