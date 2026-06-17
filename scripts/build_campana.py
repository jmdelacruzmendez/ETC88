#!/usr/bin/env python3
"""Genera el Tablero de la Tripulación ETC 88 (Misión 88) — UN archivo HTML
autocontenido (HTML + CSS + JS nativo, sin dependencias ni CDNs).

NO es una presentación económica: es un EJERCICIO de concientización para que el
equipo vea, juegue y valide cómo, trabajando como tripulación, sube o baja lo que
hay que reunir. Tono sencillo, sin jerga.

Contiene:
  - Lo que cuesta la misión por persona (participante y equipo), DESGLOSADO (pastel).
  - Lo que ponemos nosotros en cuotas (participante y equipo) y qué cubre cada una.
  - SIMULADOR: marca los rubros que creamos poder conseguir (donación/gestión) y
    mira bajar lo que hay que reunir — termómetro tipo cohete.
  - Corresponsabilidad: qué cubre cada área.
  - Cuenta regresiva (cierre de pagos y lanzamiento).

El control de pagos por NOMBRE no va aquí (es interno): vive en el Excel de
Tesorería (scripts/build_tripulacion_xlsx.py). La avanzada queda como PROPUESTA y
NO se suma al costo.

Cifras desde data/estado.json. Salida: tablero_campana_etc88.html
Uso: python scripts/build_campana.py
"""
import json
import os

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

meta     = meta_blk['valor']
cuotas   = desg['cuotas_firmes']            # 256_000
brecha   = desg['brecha_tras_cuotas']       # 297_622
especie  = desg['especie_potencial']        # 114_701

cuota_part = fin['cuota_participante']['valor']      # 3000
n_part     = fin['participantes_objetivo']['valor']  # 50
part_cuota_total = cuota_part * n_part               # 150_000
equipo_cuotas = cuotas - part_cuota_total            # 106_000
eq_pago    = fin['cuota_equipo']['valor']['mensual'] # 500
eq_total   = fin['cuota_equipo']['valor']['total']   # 2000
eq_pagos   = eq_total // eq_pago                      # 4
n_equipo   = equipo_cuotas // eq_total                # 53

pdesg = cpp['participante']['desglose_persona']
edesg = cpp['equipo']['desglose_persona']
part_costo = cpp['participante']['con_imprevistos_persona']   # 6548.92
eq_costo   = cpp['equipo']['con_imprevistos_persona']         # 4523.53
part_oper  = cpp['participante']['operativo_persona']         # 5953.56
eq_oper    = cpp['equipo']['operativo_persona']               # 4112.30

PART_LBL = [('casa', 'Casa (hospedaje)'), ('cocina', 'Comida del retiro'),
            ('biblias_y_peces', 'Biblia + pez'), ('transporte', 'Su transporte'),
            ('guias', 'Materiales de su PG'), ('liturgico', 'Litúrgico'), ('musica', 'Música')]
EQ_LBL = [('casa', 'Casa (hospedaje)'), ('transporte', 'Transporte (equipo + clausura)'),
          ('camisetas', 'Camiseta'), ('eventos_formativos', 'Formación'),
          ('almuerzo_ensayo', 'Almuerzo del ensayo'), ('liturgico', 'Litúrgico'), ('musica', 'Música')]
desg_part = [{"label": lbl, "monto": pdesg[k]} for k, lbl in PART_LBL]
desg_eq   = [{"label": lbl, "monto": edesg[k]} for k, lbl in EQ_LBL]

lema = EST['marca']['lema_retiro']['valor']

# --------------------------------------------------------- chequeo aritmética
errs = []
if round(sum(d['monto'] for d in desg_part), 2) != part_oper:
    errs.append(f"desglose participante {sum(d['monto'] for d in desg_part)} ≠ {part_oper}")
if round(sum(d['monto'] for d in desg_eq), 2) != eq_oper:
    errs.append(f"desglose equipo {sum(d['monto'] for d in desg_eq)} ≠ {eq_oper}")
if sum(r['monto'] for r in sim['items']) != meta:
    errs.append(f"rubros simulador {sum(r['monto'] for r in sim['items'])} ≠ meta {meta}")
if abs(round(part_costo * n_part + eq_costo * 50) - meta) > 5:
    errs.append("costo/persona ×50 no amarra con la meta")
if part_cuota_total + equipo_cuotas != cuotas:
    errs.append("cuotas no cuadran")
if errs:
    raise SystemExit("NO CUADRA con estado.json:\n  - " + "\n  - ".join(errs))

datos = {
    "evento": "ETC · Misión 88",
    "subtitulo": "Lo que cuesta la misión, y cómo —trabajando como tripulación— la hacemos posible",
    "lema": lema, "citaBiblica": "Mt 6, 21",
    "moneda": "RD$", "locale": "es-DO", "actualizado": "17 de junio de 2026",
    "fechaCierrePagos": "2026-08-30", "fechaCierrePagosTexto": "30 de agosto de 2026",
    "fechaRetiro": "2026-09-04", "fechaRetiroTexto": "4 – 6 de septiembre de 2026",

    "costoTotal": meta, "cuotas": cuotas, "especie": especie, "brecha": brecha,

    "costoPersona": {
        "participante": {"costo": part_costo, "cuota": cuota_part, "oper": part_oper, "desglose": desg_part},
        "equipo":       {"costo": eq_costo,   "cuota": eq_total,   "oper": eq_oper,   "desglose": desg_eq},
    },
    "cuotaParticipante": {"monto": cuota_part, "n": n_part, "total": part_cuota_total,
                          "cubre": ["Transporte al retiro", "Comida del retiro", "Casa (hospedaje)", "Pez", "Biblia"]},
    "cuotaEquipo": {"pago": eq_pago, "pagos": eq_pagos, "total": eq_total, "n": n_equipo,
                    "totalRecaudo": equipo_cuotas, "asumidos": len(exentos),
                    "cubre": ["Ensayo general", "Prorrateo del salón", "Transporte al retiro", "Comida del ensayo", "Camiseta del equipo"]},

    "rubrosSimulador": [{"nombre": r['nombre'], "monto": r['monto'], "donable": r['donable']} for r in sim['items']],
    "corresponsabilidad": corr['areas'],
    "avanzada": {"personas": av['personas'], "comidas": av['comidas']['cantidad'],
                 "noches": av['hospedaje']['noches'], "total": av['total_estimado']},
}
datos_json = json.dumps(datos, ensure_ascii=False, indent=2)

TEMPLATE = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ETC · Misión 88 · Tablero de la Tripulación</title>
<style>
  :root{
    --bg:#0B1F3A; --bg2:#0e2a4d; --bg3:#071427;
    --ink:#EAF2FF; --muted:#9DB2D4; --muted2:#6F87AD;
    --line:rgba(255,255,255,.10); --card:rgba(255,255,255,.045); --card-h:rgba(255,255,255,.075);
    --hole:#10233f;
    --green:#34D399; --green3:#059669; --sky:#38BDF8; --gold:#F2C572; --red:#FC5130;
    --shadow:0 20px 50px -20px rgba(0,0,0,.6); --r:20px;
  }
  *{box-sizing:border-box; margin:0; padding:0}
  html{scroll-behavior:smooth}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    color:var(--ink); line-height:1.5; min-height:100vh;
    background:
      radial-gradient(1100px 700px at 12% -8%, rgba(56,189,248,.12), transparent 60%),
      radial-gradient(900px 600px at 95% 0%, rgba(252,81,48,.10), transparent 55%),
      radial-gradient(1200px 900px at 50% 120%, rgba(52,211,153,.08), transparent 60%),
      linear-gradient(160deg, var(--bg2), var(--bg) 45%, var(--bg3));
    background-attachment:fixed; -webkit-font-smoothing:antialiased; padding:clamp(16px,3vw,40px)}
  .stars{position:fixed; inset:0; z-index:-1; overflow:hidden}
  .stars i{position:absolute; width:2px; height:2px; background:#fff; border-radius:50%; opacity:.5; animation:tw 4s infinite ease-in-out}
  @keyframes tw{0%,100%{opacity:.2} 50%{opacity:.8}}
  .wrap{max-width:1180px; margin:0 auto}

  header{text-align:center; padding:clamp(14px,3vw,30px) 0 clamp(10px,2vw,22px)}
  .patch{width:clamp(120px,22vw,168px); height:auto; display:block; margin:0 auto 14px; filter:drop-shadow(0 10px 24px rgba(0,0,0,.45))}
  h1{font-size:clamp(2.1rem,6vw,4.2rem); font-weight:800; line-height:1.02; letter-spacing:-.02em; margin:6px 0;
    background:linear-gradient(180deg,#fff,#cfe0ff 70%,#9db2d4); -webkit-background-clip:text; background-clip:text; color:transparent}
  .sub{color:var(--muted); font-size:clamp(1rem,2.1vw,1.25rem); font-weight:500; max-width:760px; margin:6px auto 0}
  .lema{margin:16px auto 0; max-width:640px; color:var(--gold); font-style:italic; font-size:clamp(.98rem,2.2vw,1.3rem); line-height:1.35}
  .lema b{font-style:normal; color:var(--muted2); font-size:.8em; display:block; margin-top:5px; letter-spacing:.04em}

  .kpis{display:grid; gap:clamp(10px,1.6vw,18px); margin:clamp(18px,3vw,30px) 0; grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
  .kpi{background:var(--card); border:1px solid var(--line); border-radius:var(--r); padding:clamp(15px,2vw,22px); position:relative; overflow:hidden;
    transition:transform .35s ease, background .35s ease, border-color .35s ease}
  .kpi:hover{transform:translateY(-4px); background:var(--card-h); border-color:rgba(255,255,255,.2)}
  .kpi::before{content:""; position:absolute; inset:0 auto auto 0; width:100%; height:3px; background:linear-gradient(90deg,var(--sky),var(--green))}
  .kpi .lbl{font-size:.8rem; letter-spacing:.06em; text-transform:uppercase; color:var(--muted)}
  .kpi .val{font-size:clamp(1.5rem,3.2vw,2.3rem); font-weight:800; letter-spacing:-.02em; margin-top:8px; font-variant-numeric:tabular-nums; line-height:1.05}
  .kpi .note{font-size:.8rem; color:var(--muted2); margin-top:6px}
  .kpi.green .val{color:var(--green)} .kpi.red .val{color:var(--red)} .kpi.sky .val{color:var(--sky)}

  .panel{background:var(--card); border:1px solid var(--line); border-radius:var(--r); padding:clamp(18px,2.6vw,32px); box-shadow:var(--shadow); margin-bottom:clamp(14px,2vw,22px)}
  .panel h2{font-size:clamp(1.2rem,2.4vw,1.6rem); font-weight:700; letter-spacing:-.01em}
  .panel .h2note{color:var(--muted); font-size:.92rem; margin-top:5px; margin-bottom:20px}
  .grid2{display:grid; gap:clamp(16px,2.4vw,26px); grid-template-columns:1fr 1fr}
  @media(max-width:820px){ .grid2{grid-template-columns:1fr} }

  /* pastel + leyenda */
  .costo-card .ct{color:var(--muted); text-transform:uppercase; letter-spacing:.07em; font-size:.78rem; font-weight:700; margin-bottom:4px}
  .costo-card .cbig{font-size:clamp(1.7rem,4.5vw,2.4rem); font-weight:800; color:var(--green); font-variant-numeric:tabular-nums; line-height:1}
  .costo-card .csub{color:var(--muted); font-size:.85rem; margin:4px 0 16px}
  .pie-row{display:flex; gap:clamp(14px,2.5vw,22px); align-items:center; flex-wrap:wrap}
  .pie{width:clamp(120px,26vw,160px); aspect-ratio:1; border-radius:50%; flex:none; box-shadow:0 0 0 6px rgba(255,255,255,.03); position:relative}
  .pie::after{content:""; position:absolute; inset:30%; border-radius:50%; background:var(--hole); box-shadow:inset 0 2px 8px rgba(0,0,0,.4)}
  .legend{flex:1; min-width:170px; display:grid; gap:7px}
  .leg-row{display:grid; grid-template-columns:auto 1fr auto; gap:9px; align-items:center; font-size:.9rem; font-variant-numeric:tabular-nums}
  .leg-dot{width:11px; height:11px; border-radius:3px}
  .leg-l{color:var(--ink)} .leg-v{color:var(--muted); font-weight:600}

  /* cuotas */
  .qcard{background:rgba(0,0,0,.18); border:1px solid var(--line); border-radius:16px; padding:clamp(16px,2.2vw,24px)}
  .qcard .qt{color:var(--muted); text-transform:uppercase; letter-spacing:.07em; font-size:.78rem; font-weight:700}
  .qcard .qbig{font-size:clamp(1.7rem,4.5vw,2.3rem); font-weight:800; color:var(--sky); font-variant-numeric:tabular-nums; line-height:1; margin:6px 0}
  .qcard .qline{color:var(--muted); font-size:.92rem; margin-bottom:14px}
  .qcard .qline b{color:var(--ink)}
  .chips{display:flex; flex-wrap:wrap; gap:7px}
  .chip{background:rgba(56,189,248,.1); border:1px solid rgba(56,189,248,.25); color:#cfeafe; font-size:.82rem; padding:5px 11px; border-radius:100px}
  .qtot{margin-top:18px; padding-top:14px; border-top:1px solid var(--line); color:var(--muted); font-size:.95rem; font-variant-numeric:tabular-nums}
  .qtot b{color:var(--ink)}

  /* simulador */
  .sim{background:linear-gradient(135deg, rgba(56,189,248,.12), rgba(52,211,153,.06) 70%, transparent), var(--card); border:1px solid rgba(56,189,248,.28)}
  .sim-flex{display:flex; gap:clamp(18px,3vw,34px); align-items:flex-start; flex-wrap:wrap}
  .rocket-wrap{flex:none; width:clamp(130px,30vw,180px); text-align:center}
  .rocket-wrap svg{width:100%; height:auto; display:block; overflow:visible}
  .sim-read{flex:1; min-width:240px}
  .sim-falta{font-size:clamp(2.4rem,8vw,4rem); font-weight:800; color:var(--red); letter-spacing:-.03em; font-variant-numeric:tabular-nums; line-height:1}
  .sim-falta.done{color:var(--green)}
  .sim-falta-lbl{color:var(--muted); margin:4px 0 14px; font-size:1.02rem}
  .sim-mini{display:flex; gap:22px; flex-wrap:wrap; color:var(--muted); font-size:.92rem; font-variant-numeric:tabular-nums; margin-bottom:16px}
  .sim-mini b{color:var(--ink); display:block; font-size:1.15rem; font-weight:800}
  .sim-actions{display:flex; gap:10px; flex-wrap:wrap; margin-bottom:8px}
  .sim-btn{font-family:inherit; cursor:pointer; border-radius:100px; padding:9px 16px; font-size:.86rem; font-weight:700;
    border:1px solid var(--line); background:rgba(255,255,255,.05); color:var(--ink); transition:all .2s}
  .sim-btn:hover{border-color:rgba(255,255,255,.3)}
  .sim-btn.go{background:linear-gradient(180deg,var(--sky),#0c8fce); border-color:var(--sky); color:#04243a}
  .sim-list{display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:18px}
  @media(max-width:680px){ .sim-list{grid-template-columns:1fr} }
  .rub{display:flex; align-items:center; gap:10px; width:100%; text-align:left; font-family:inherit; cursor:pointer;
    background:rgba(0,0,0,.2); border:1px solid var(--line); border-radius:12px; padding:11px 13px; color:var(--ink); transition:all .18s}
  .rub:hover{border-color:rgba(255,255,255,.28)}
  .rub.on{background:rgba(52,211,153,.14); border-color:var(--green)}
  .rub-check{width:20px; height:20px; border-radius:6px; border:2px solid var(--muted2); flex:none; position:relative; transition:all .18s}
  .rub.on .rub-check{background:var(--green); border-color:var(--green)}
  .rub.on .rub-check::after{content:"✓"; position:absolute; inset:0; display:flex; align-items:center; justify-content:center; color:#04241a; font-size:13px; font-weight:900}
  .rub-n{flex:1; font-size:.92rem} .rub-m{font-variant-numeric:tabular-nums; font-weight:700; color:var(--muted)}
  .rub.on .rub-m{color:var(--green)}
  .rub-tag{font-size:.66rem; color:var(--green); border:1px solid rgba(52,211,153,.4); border-radius:100px; padding:1px 7px; margin-left:4px; vertical-align:middle}
  .sim-note{color:var(--muted); font-size:.88rem; margin-top:16px; line-height:1.5}

  /* corresponsabilidad */
  .areas-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(238px,1fr)); gap:14px}
  .area-card{background:rgba(0,0,0,.18); border:1px solid var(--line); border-radius:16px; padding:18px 20px; border-top:3px solid var(--green)}
  .area-h{display:flex; justify-content:space-between; align-items:baseline; gap:10px; margin-bottom:12px; padding-bottom:11px; border-bottom:1px solid var(--line)}
  .area-name{font-weight:800; font-size:1.16rem} .area-amt{color:var(--muted); font-weight:700; font-variant-numeric:tabular-nums; white-space:nowrap; font-size:.92rem}
  .area-items{list-style:none; display:grid; gap:8px}
  .area-items li{color:var(--muted); padding-left:18px; position:relative; font-size:.94rem}
  .area-items li::before{content:""; position:absolute; left:3px; top:.55em; width:6px; height:6px; border-radius:50%; background:var(--green)}
  .areas-foot{color:var(--muted); margin-top:16px; font-size:.9rem} .areas-foot b{color:var(--ink)}

  /* countdown */
  .cd-two{display:grid; gap:14px; grid-template-columns:1fr 1fr}
  @media(max-width:680px){ .cd-two{grid-template-columns:1fr} }
  .cd-block{background:rgba(0,0,0,.2); border:1px solid var(--line); border-radius:14px; padding:14px 14px 16px}
  .cd-block.urgent{border-color:rgba(252,81,48,.4); background:rgba(252,81,48,.06)}
  .cd-head{color:var(--muted); font-size:.85rem; margin-bottom:10px} .cd-head b{color:var(--ink)}
  .cd-block.urgent .cd-head b{color:var(--red)}
  .cd-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:8px}
  .cd-cell{background:rgba(0,0,0,.25); border:1px solid var(--line); border-radius:12px; padding:12px 4px; text-align:center}
  .cd-num{font-size:clamp(1.4rem,4.5vw,2.2rem); font-weight:800; font-variant-numeric:tabular-nums; line-height:1;
    background:linear-gradient(180deg,#fff,#bcd2f5); -webkit-background-clip:text; background-clip:text; color:transparent}
  .cd-lbl{font-size:.64rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-top:7px}

  footer{text-align:center; color:var(--muted2); font-size:.82rem; padding:24px 0 8px; line-height:1.7}
  footer b{color:var(--muted)}

  .reveal{opacity:0; transform:translateY(20px); transition:opacity .7s ease, transform .7s cubic-bezier(.16,1,.3,1)}
  .reveal.visible{opacity:1; transform:none}
  @media(prefers-reduced-motion:reduce){ .reveal{opacity:1; transform:none; transition:none} .stars i{animation:none} html{scroll-behavior:auto} }
</style>
</head>
<body>
<div class="stars" id="stars" aria-hidden="true"></div>
<div class="wrap">

  <header class="reveal">
    <svg class="patch" viewBox="0 0 200 200" role="img" aria-label="ETC Misión 88">
      <defs><path id="patchArc" d="M30,108 A74,74 0 0 1 170,108"/></defs>
      <circle cx="100" cy="100" r="95" fill="#0B2A52" stroke="#fff" stroke-width="5"/>
      <circle cx="100" cy="100" r="86" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="1.5"/>
      <ellipse cx="100" cy="98" rx="44" ry="72" fill="none" stroke="#fff" stroke-width="2.4" transform="rotate(24 100 100)"/>
      <g fill="#fff">
        <circle cx="62" cy="58" r="1.6"/><circle cx="142" cy="54" r="2"/><circle cx="151" cy="120" r="1.5"/>
        <circle cx="55" cy="132" r="1.7"/><circle cx="122" cy="150" r="1.5"/><circle cx="80" cy="151" r="1.3"/>
        <circle cx="44" cy="94" r="1.3"/><circle cx="158" cy="86" r="1.3"/>
      </g>
      <path d="M20,150 Q120,56 188,64 Q120,90 34,158 Z" fill="#FC5130"/>
      <text x="100" y="122" text-anchor="middle" font-size="56" font-weight="800" fill="#fff" letter-spacing="2" font-family="-apple-system,Segoe UI,Roboto,sans-serif">ETC</text>
      <text fill="#fff" font-size="13" font-weight="700" letter-spacing="2.4" font-family="-apple-system,Segoe UI,Roboto,sans-serif"><textPath href="#patchArc" startOffset="50%" text-anchor="middle">ENCUENTRO TOTAL CON CRISTO</textPath></text>
      <text x="100" y="178" text-anchor="middle" font-size="12.5" font-weight="700" letter-spacing="4" fill="#fff" font-family="-apple-system,Segoe UI,Roboto,sans-serif">MISIÓN 88</text>
    </svg>
    <h1 id="evento">ETC · Misión 88</h1>
    <p class="sub" id="subtitulo"></p>
    <p class="lema" id="lema"></p>
  </header>

  <section class="kpis reveal" id="kpis">
    <div class="kpi"><div class="lbl">Costo de la misión</div><div class="val" id="kpi-costo">RD$ 0</div><div class="note">lo que cuesta el retiro completo</div></div>
    <div class="kpi green"><div class="lbl">Lo que ya ponemos</div><div class="val" id="kpi-cuotas">RD$ 0</div><div class="note">cuotas de participantes + equipo</div></div>
    <div class="kpi red"><div class="lbl">Falta por reunir</div><div class="val" id="kpi-falta">RD$ 0</div><div class="note">y depende de nosotros</div></div>
    <div class="kpi"><div class="lbl">Días: cierre de pagos</div><div class="val" id="kpi-dias">0</div><div class="note" id="kpi-dias-note">lanzamiento: 4–6 sep</div></div>
  </section>

  <!-- costo por persona -->
  <section class="panel reveal" id="costo-panel">
    <h2>Lo que cuesta la misión, por persona</h2>
    <p class="h2note">Para dimensionar el esfuerzo — sencillo y claro. (Incluye el 10% de imprevistos.)</p>
    <div class="grid2">
      <div class="costo-card">
        <div class="ct">Por participante</div>
        <div class="cbig" id="cp-part">RD$ 0</div>
        <div class="csub">su cuota es <b id="cp-part-cuota"></b> · el resto no recae en él</div>
        <div class="pie-row"><div class="pie" id="pie-part"></div><div class="legend" id="leg-part"></div></div>
      </div>
      <div class="costo-card">
        <div class="ct">Por miembro de equipo</div>
        <div class="cbig" id="cp-eq" style="color:var(--sky)">RD$ 0</div>
        <div class="csub">su cuota es <b id="cp-eq-cuota"></b></div>
        <div class="pie-row"><div class="pie" id="pie-eq"></div><div class="legend" id="leg-eq"></div></div>
      </div>
    </div>
  </section>

  <!-- cuotas -->
  <section class="panel reveal" id="cuota-panel">
    <h2>Lo que ponemos nosotros</h2>
    <p class="h2note">La cuota no cubre el costo real — pero es nuestro primer aporte como tripulación</p>
    <div class="grid2">
      <div class="qcard">
        <div class="qt">Cuota del participante</div>
        <div class="qbig" id="q-part">RD$ 0</div>
        <div class="qline" id="q-part-line"></div>
        <div class="chips" id="q-part-chips"></div>
        <div class="qtot" id="q-part-tot"></div>
      </div>
      <div class="qcard">
        <div class="qt">Cuota del equipo</div>
        <div class="qbig" id="q-eq" style="color:var(--green)">RD$ 0</div>
        <div class="qline" id="q-eq-line"></div>
        <div class="chips" id="q-eq-chips"></div>
        <div class="qtot" id="q-eq-tot"></div>
      </div>
    </div>
  </section>

  <!-- SIMULADOR -->
  <section class="panel sim reveal" id="sim-panel">
    <h2>El ejercicio de la tripulación</h2>
    <p class="h2note">Marca lo que crees que podemos conseguir donado o gestionado, y mira bajar lo que hay que reunir. No es una meta fría: es ver que, juntos, se puede.</p>
    <div class="sim-flex">
      <div class="rocket-wrap" aria-hidden="true">
        <svg viewBox="0 0 160 430">
          <defs>
            <linearGradient id="fuelG" x1="0" y1="1" x2="0" y2="0">
              <stop offset="0%" stop-color="#0c8fce"/><stop offset="55%" stop-color="#34D399"/><stop offset="100%" stop-color="#A7F3D0"/>
            </linearGradient>
            <clipPath id="bodyClip"><rect x="55" y="78" width="50" height="250" rx="12"/></clipPath>
          </defs>
          <!-- flame -->
          <path id="flame" d="M70,330 Q80,395 90,330 Z" fill="#FC5130" opacity=".9"/>
          <!-- body track -->
          <rect x="55" y="78" width="50" height="250" rx="12" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.16)"/>
          <!-- fuel -->
          <rect id="fuel" x="55" y="328" width="50" height="0" fill="url(#fuelG)" clip-path="url(#bodyClip)"/>
          <!-- nose -->
          <path d="M55,80 L80,20 L105,80 Z" fill="#E7EEFA"/>
          <!-- fins -->
          <path d="M55,300 L38,346 L55,332 Z" fill="#FC5130"/>
          <path d="M105,300 L122,346 L105,332 Z" fill="#FC5130"/>
          <!-- body outline + window -->
          <rect x="55" y="78" width="50" height="250" rx="12" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="2"/>
          <circle cx="80" cy="112" r="11" fill="#0B2A52" stroke="#E7EEFA" stroke-width="3"/>
          <!-- meta line -->
          <line x1="44" x2="116" y1="78" y2="78" stroke="#fff" stroke-dasharray="4 4" stroke-width="1.5" opacity=".7"/>
          <text x="120" y="82" fill="#fff" font-size="10" font-weight="700">META</text>
        </svg>
        <div style="color:var(--muted); font-size:.82rem; margin-top:6px">cubierto: <b id="sim-cubierto" style="color:var(--ink)">RD$ 0</b></div>
      </div>
      <div class="sim-read">
        <div class="sim-falta" id="sim-falta">RD$ 0</div>
        <div class="sim-falta-lbl" id="sim-falta-lbl">hay que reunir entre todos</div>
        <div class="sim-mini">
          <div>por cada uno (100)<b id="sim-porcabeza">RD$ 0</b></div>
          <div>costo de la misión<b id="sim-costo">RD$ 0</b></div>
        </div>
        <div class="sim-actions">
          <button type="button" class="sim-btn go" id="sim-realista">Probar: lo realista</button>
          <button type="button" class="sim-btn" id="sim-reset">Reiniciar</button>
        </div>
        <div class="sim-list" id="sim-list"></div>
        <p class="sim-note">Es un ejercicio para imaginar y validar juntos — no un compromiso. Lo marcado como <b style="color:var(--green)">donable</b> es lo más realista de gestionar (en el ETC 78 se donó más de la mitad).</p>
      </div>
    </div>
  </section>

  <!-- corresponsabilidad -->
  <section class="panel reveal" id="areas-panel">
    <h2>Cada área aporta su parte</h2>
    <p class="h2note">El esfuerzo no es solo de los directores — cada área de la tripulación carga lo suyo</p>
    <div class="areas-grid" id="areas-grid"></div>
    <p class="areas-foot">Montos <b>indicativos</b>. Casa, transporte y la coordinación general completan el costo total.</p>
  </section>

  <!-- countdown -->
  <section class="panel reveal" id="cd-panel">
    <h2>Cuenta regresiva</h2>
    <p class="h2note">El dinero debe estar conciliado para el cierre de pagos, antes del lanzamiento</p>
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
        <div class="cd-head">Lanzamiento (retiro) · <b id="cd-ret-when"></b></div>
        <div class="cd-grid">
          <div class="cd-cell"><div class="cd-num" id="ret-d">0</div><div class="cd-lbl">Días</div></div>
          <div class="cd-cell"><div class="cd-num" id="ret-h">00</div><div class="cd-lbl">Hrs</div></div>
          <div class="cd-cell"><div class="cd-num" id="ret-m">00</div><div class="cd-lbl">Min</div></div>
          <div class="cd-cell"><div class="cd-num" id="ret-s">00</div><div class="cd-lbl">Seg</div></div>
        </div>
      </div>
    </div>
  </section>

  <footer>
    Hecho por la tripulación · desde <b>data/estado.json</b> · actualizado <span id="ft-fecha"></span>.<br>
    <span id="ft-avanzada"></span> El control de pagos por nombre es interno (Excel de Tesorería), no se muestra aquí.
  </footer>

</div>

<script>
const datos = __DATOS_JSON__;

/* ---- utilidades ---- */
const REDUCE = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const nf  = new Intl.NumberFormat(datos.locale || 'es-DO');
const nf2 = new Intl.NumberFormat(datos.locale || 'es-DO', {minimumFractionDigits:2, maximumFractionDigits:2});
const money  = n => datos.moneda + ' ' + nf.format(Math.round(n));
const money2 = n => datos.moneda + ' ' + nf2.format(n);
const $ = id => document.getElementById(id);
const setText = (id, v) => { const e = $(id); if (e) e.textContent = v; };
const easeOutCubic = t => 1 - Math.pow(1 - t, 3);
const PALETTE = ['#38BDF8','#34D399','#F2C572','#FC5130','#A78BFA','#22D3EE','#FB7185'];
function animate(duration, onUpdate, onDone){
  if (REDUCE){ onUpdate(1); if (onDone) onDone(); return; }
  const t0 = performance.now();
  (function f(now){ const t = Math.min(1,(now-t0)/duration); onUpdate(easeOutCubic(t)); if (t<1) requestAnimationFrame(f); else if (onDone) onDone(); })(performance.now());
}
function countUp(id, to, fmt, dur){ const e=$(id); if(!e) return; animate(dur||1500, p=>{ e.textContent = fmt(to*p); }); }

/* ---- estrellas ---- */
(function(){ const s=$('stars'); let h=''; for(let i=0;i<48;i++){ h+='<i style="left:'+(Math.random()*100).toFixed(2)+'%;top:'+(Math.random()*100).toFixed(2)+'%;animation-delay:'+(Math.random()*4).toFixed(2)+'s"></i>'; } s.innerHTML=h; })();

/* ---- textos ---- */
setText('evento', datos.evento);
setText('subtitulo', datos.subtitulo);
$('lema').innerHTML = '«' + datos.lema + '»<b>' + datos.citaBiblica + '</b>';
setText('cd-cpago-when', datos.fechaCierrePagosTexto);
setText('cd-ret-when', datos.fechaRetiroTexto);
setText('ft-fecha', datos.actualizado);
setText('sim-costo', money(datos.costoTotal));
setText('cp-part-cuota', money(datos.cuotaParticipante.monto));
setText('cp-eq-cuota', money(datos.cuotaEquipo.total));
$('ft-avanzada').textContent = 'La avanzada del equipo (jueves, ~' + datos.avanzada.personas + ' personas: ' + datos.avanzada.comidas + ' comidas + ' + datos.avanzada.noches + ' noche) está como PROPUESTA y NO se suma al costo hasta cotizarla.';

/* ---- fechas / countdown ---- */
function dateLocal(iso){ const p=iso.split('-').map(Number); return new Date(p[0],p[1]-1,p[2],0,0,0,0); }
function diffParts(iso){ let ms=Math.max(0,dateLocal(iso).getTime()-Date.now());
  const d=Math.floor(ms/86400000); ms-=d*86400000; const h=Math.floor(ms/3600000); ms-=h*3600000; const m=Math.floor(ms/60000); ms-=m*60000; return {d,h,m,s:Math.floor(ms/1000)}; }
function mkCountdown(pfx, iso){ function tick(){ const t=diffParts(iso); setText(pfx+'-d',t.d); setText(pfx+'-h',String(t.h).padStart(2,'0')); setText(pfx+'-m',String(t.m).padStart(2,'0')); setText(pfx+'-s',String(t.s).padStart(2,'0')); } tick(); setInterval(tick,1000); }

/* ---- KPIs ---- */
function runKpis(){
  countUp('kpi-costo', datos.costoTotal, money);
  countUp('kpi-cuotas', datos.cuotas, money);
  countUp('kpi-falta', datos.brecha, money);
  animate(1500, p=>{ $('kpi-dias').textContent = nf.format(Math.round(diffParts(datos.fechaCierrePagos).d*p)); });
}

/* ---- pastel + costo por persona ---- */
function renderPie(pieId, legId, items){
  const total=items.reduce((a,i)=>a+i.monto,0); let acc=0, parts=[], leg='';
  items.forEach((it,idx)=>{ const col=PALETTE[idx%PALETTE.length]; const s=acc/total*100; acc+=it.monto; const e=acc/total*100;
    parts.push(col+' '+s.toFixed(2)+'% '+e.toFixed(2)+'%');
    leg+='<div class="leg-row"><span class="leg-dot" style="background:'+col+'"></span><span class="leg-l">'+it.label+'</span><span class="leg-v">'+money2(it.monto)+'</span></div>'; });
  $(pieId).style.background='conic-gradient('+parts.join(',')+')';
  $(legId).innerHTML=leg;
}
function runCosto(){
  const C=datos.costoPersona;
  countUp('cp-part', C.participante.costo, money2);
  countUp('cp-eq', C.equipo.costo, money2);
  renderPie('pie-part','leg-part', C.participante.desglose);
  renderPie('pie-eq','leg-eq', C.equipo.desglose);
}

/* ---- cuotas ---- */
function runCuotas(){
  const P=datos.cuotaParticipante, E=datos.cuotaEquipo;
  countUp('q-part', P.total, money);
  $('q-part-line').innerHTML = '<b>'+money(P.monto)+'</b> × '+P.n+' participantes';
  $('q-part-chips').innerHTML = P.cubre.map(c=>'<span class="chip">'+c+'</span>').join('');
  $('q-part-tot').innerHTML = 'Aporta en total <b>'+money(P.total)+'</b>';
  countUp('q-eq', E.totalRecaudo, money);
  $('q-eq-line').innerHTML = '<b>'+money(E.total)+'</b> = '+E.pagos+' pagos de '+money(E.pago)+' (jun–sep) · '+E.n+' del equipo';
  $('q-eq-chips').innerHTML = E.cubre.map(c=>'<span class="chip">'+c+'</span>').join('');
  $('q-eq-tot').innerHTML = 'Aporta en total <b>'+money(E.totalRecaudo)+'</b> · la Sor y el Padre Paul no pagan: lo asume la Co-Dirección';
}

/* ---- SIMULADOR (cohete) ---- */
const RBOT=328, RTOP=78, RRANGE=RBOT-RTOP;
let fuelCur=0;
function setFuel(frac){ const f=$('fuel'); const y=RBOT-frac*RRANGE; f.setAttribute('y',y); f.setAttribute('height',frac*RRANGE);
  const fl=$('flame'); const sc=0.4+frac*1.4; fl.setAttribute('transform','translate(80 330) scale('+(0.7+frac*0.6)+','+sc+') translate(-80 -330)'); fl.setAttribute('opacity', (0.4+frac*0.5).toFixed(2)); }
function animateFuel(target){ if(REDUCE){ setFuel(target); fuelCur=target; return; } const from=fuelCur; animate(600, p=>{ setFuel(from+(target-from)*p); }, ()=>{ fuelCur=target; }); }
const simSel = new Set();
function renderSim(){
  let html='';
  datos.rubrosSimulador.forEach((r,i)=>{ html+='<button type="button" class="rub" data-i="'+i+'"><span class="rub-check"></span><span class="rub-n">'+r.nombre+(r.donable?' <span class="rub-tag">donable</span>':'')+'</span><span class="rub-m">'+money(r.monto)+'</span></button>'; });
  $('sim-list').innerHTML=html;
  $('sim-list').addEventListener('click', e=>{ const b=e.target.closest('.rub'); if(!b) return; const i=+b.dataset.i;
    if(simSel.has(i)){ simSel.delete(i); b.classList.remove('on'); } else { simSel.add(i); b.classList.add('on'); } recomputeSim(); });
  $('sim-realista').addEventListener('click', ()=>preset(true));
  $('sim-reset').addEventListener('click', ()=>preset(false));
}
function preset(donable){ simSel.clear(); if(donable) datos.rubrosSimulador.forEach((r,i)=>{ if(r.donable) simSel.add(i); });
  document.querySelectorAll('.rub').forEach(b=>b.classList.toggle('on', simSel.has(+b.dataset.i))); recomputeSim(); }
function recomputeSim(){
  let S=0; datos.rubrosSimulador.forEach((r,i)=>{ if(simSel.has(i)) S+=r.monto; });
  const cubierto=datos.cuotas+S, falta=datos.costoTotal-cubierto;
  setText('sim-cubierto', money(cubierto));
  const fEl=$('sim-falta');
  if(falta>0){ fEl.textContent=money(falta); fEl.classList.remove('done'); setText('sim-falta-lbl','hay que reunir entre todos'); }
  else { fEl.textContent = falta===0?money(0):('+'+money(Math.abs(falta))); fEl.classList.add('done'); setText('sim-falta-lbl', falta===0?'¡misión cubierta!':'¡misión cubierta! incluso sobra'); }
  setText('sim-porcabeza', money(Math.max(0,falta)/100));
  animateFuel(Math.max(0,Math.min(1,cubierto/datos.costoTotal)));
}

/* ---- corresponsabilidad ---- */
const AREA_COLOR = {'Guías':'#34D399','Música':'#F2C572','Cocina':'#38BDF8','Directores':'#FC5130'};
function renderAreas(){
  const g=$('areas-grid');
  datos.corresponsabilidad.forEach(a=>{ const col=AREA_COLOR[a.area]||'#34D399';
    const c=document.createElement('div'); c.className='area-card'; c.style.borderTopColor=col;
    c.innerHTML='<div class="area-h"><span class="area-name" style="color:'+col+'">'+a.area+'</span><span class="area-amt">≈ '+money(a.monto_indicativo)+'</span></div><ul class="area-items">'+a.items.map(x=>'<li>'+x+'</li>').join('')+'</ul>';
    g.appendChild(c); });
}

/* ---- reveal + init ---- */
function onVisible(node, cb){ if(!node) return; if(!('IntersectionObserver' in window)){ cb(); return; }
  const io=new IntersectionObserver((es,ob)=>{ es.forEach(e=>{ if(e.isIntersecting){ cb(); ob.disconnect(); } }); }, {threshold:.15}); io.observe(node); }
window.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.reveal').forEach(n=>onVisible(n, ()=>n.classList.add('visible')));
  mkCountdown('cpago', datos.fechaCierrePagos);
  mkCountdown('ret', datos.fechaRetiro);
  renderAreas();
  renderSim();
  onVisible($('kpis'), runKpis);
  onVisible($('costo-panel'), runCosto);
  onVisible($('cuota-panel'), runCuotas);
  onVisible($('sim-panel'), recomputeSim);
});
</script>
</body>
</html>
'''

html = TEMPLATE.replace('__DATOS_JSON__', datos_json)
with open(os.path.join(REPO, 'tablero_campana_etc88.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print("OK  tablero_campana_etc88.html  (tema Misión 88 · simulador)")
print(f"    costo misión       RD$ {meta:,}  ·  cuotas {cuotas:,}  ·  falta {brecha:,}")
print(f"    part RD$ {part_costo:,.2f} (desglose suma {sum(d['monto'] for d in desg_part):,.2f} oper)")
print(f"    equipo RD$ {eq_costo:,.2f} (desglose suma {sum(d['monto'] for d in desg_eq):,.2f} oper)")
print(f"    simulador {len(sim['items'])} rubros suman {sum(r['monto'] for r in sim['items']):,} = meta ✓")
print(f"    cuota equipo {eq_pagos}×{eq_pago} ·  {n_equipo} del equipo · {len(exentos)} asumidos (Sor + Paul)")
print(f"    avanzada PROPUESTA {av['total_estimado']:,} (NO sumada)")
print("    aritmética cuadra ✓")
