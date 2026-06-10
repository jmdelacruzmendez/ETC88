#!/usr/bin/env python3
"""Assemble the Tripulación HTML dashboard v3 (45 tripulantes, no vacantes, batches temáticos)."""
with open('/tmp/etc88_data_min.json') as f:
    data_str = f.read()

HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tablero de la Tripulación · ETC LXXXVIII</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Lora:ital,wght@0,400;0,600;1,400;1,600&family=Barlow+Condensed:wght@400;500;600;700&family=Special+Elite&family=Caveat:wght@400;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script defer src="https://unpkg.com/alpinejs@3.13.5/dist/cdn.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {
  --pergamino:#E8D2A1; --pergamino-claro:#F3E4BE; --pergamino-tibio:#DCC080;
  --crema:#F7EBCC; --vela:#F7EFD9;
  --tierra:#B25028; --tierra-honda:#762E10;
  --mar:#1B3A52; --mar-honda:#0E2238;
  --safari:#4A5D2E; --safari-honda:#2E3C1C;
  --ambar:#C57920; --ambar-honda:#8F4E10;
  --cuero:#6B4423; --cuero-claro:#8B5C30;
  --tinta:#1C140B; --tinta-suave:#4A372A;
  --rule:#C9AE76; --muted:#7A6440;
  --team-guias: #1B3A52;
  --team-guias-soft: #DCE5EE;
  --team-cocina: #4A5D2E;
  --team-cocina-soft: #DBE3CC;
  --team-musica: #C57920;
  --team-musica-soft: #F3DDB7;
  --team-dir: #B25028;
  --team-dir-soft: #EBCFC1;
  --team-ases: #6B4423;
  --team-ases-soft: #DDCAB2;
  --team-ases-coc: #6E7F4C;
  --team-ases-coc-soft: #E4EAD2;
  --team-ases-esp: #4A372A;
  --team-ases-esp-soft: #D9CFC4;
  --team-ases-dio: #8F4E10;
  --team-ases-dio-soft: #F0D8B0;
}
html, body { background: var(--crema); color: var(--tinta); }
body { font-family: 'Lora', Georgia, serif; font-size: 15px; line-height: 1.5; }
.f-display { font-family: 'Cinzel', serif; text-transform: uppercase; letter-spacing: 0.08em; }
.f-cond { font-family: 'Barlow Condensed', sans-serif; }
.f-mono { font-family: 'Special Elite', 'Courier Prime', monospace; }
.f-script { font-family: 'Caveat', cursive; }
.bg-pergamino { background: var(--pergamino); }
.bg-pergamino-claro { background: var(--pergamino-claro); }
.bg-vela { background: var(--vela); }
.bg-mar { background: var(--mar); color: var(--vela); }
.bg-mar-honda { background: var(--mar-honda); color: var(--vela); }
.bg-tierra { background: var(--tierra); color: var(--vela); }
.bg-safari { background: var(--safari); color: var(--vela); }
.bg-cuero { background: var(--cuero); color: var(--vela); }
.text-tierra { color: var(--tierra); }
.text-tierra-honda { color: var(--tierra-honda); }
.text-mar { color: var(--mar); }
.text-safari { color: var(--safari); }
.text-ambar { color: var(--ambar); }
.text-cuero { color: var(--cuero); }
.text-tinta { color: var(--tinta); }
.text-tinta-suave { color: var(--tinta-suave); }
.text-muted { color: var(--muted); }
.border-rule { border-color: var(--rule); }

.team-strip { position: absolute; top: 0; left: 0; bottom: 0; width: 6px; }
.team-guias .team-strip { background: var(--team-guias); }
.team-cocina .team-strip { background: var(--team-cocina); }
.team-musica .team-strip { background: var(--team-musica); }
.team-directores .team-strip { background: var(--team-dir); }
.team-asesores .team-strip { background: var(--team-ases); }
.team-asesores_cocina .team-strip { background: var(--team-ases-coc); }
.team-asesores_espirituales .team-strip { background: var(--team-ases-esp); }
.team-asesores_diocesanos .team-strip { background: var(--team-ases-dio); }
.card-tripulante.no-operativo { background: var(--pergamino-claro); opacity: 0.92; }
.card-tripulante.no-operativo:hover { opacity: 1; }

.team-badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 3px 9px; border-radius: 999px;
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.14em;
}
.team-badge::before { content: ''; width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.team-badge-guias { background: var(--team-guias-soft); color: var(--team-guias); }
.team-badge-guias::before { background: var(--team-guias); }
.team-badge-cocina { background: var(--team-cocina-soft); color: var(--team-cocina); }
.team-badge-cocina::before { background: var(--team-cocina); }
.team-badge-musica { background: var(--team-musica-soft); color: var(--team-musica); }
.team-badge-musica::before { background: var(--team-musica); }
.team-badge-directores { background: var(--team-dir-soft); color: var(--team-dir); }
.team-badge-directores::before { background: var(--team-dir); }
.team-badge-asesores { background: var(--team-ases-soft); color: var(--team-ases); }
.team-badge-asesores::before { background: var(--team-ases); }
.team-badge-asesores_cocina { background: var(--team-ases-coc-soft); color: var(--team-ases-coc); }
.team-badge-asesores_cocina::before { background: var(--team-ases-coc); }
.team-badge-asesores_espirituales { background: var(--team-ases-esp-soft); color: var(--team-ases-esp); }
.team-badge-asesores_espirituales::before { background: var(--team-ases-esp); }
.team-badge-asesores_diocesanos { background: var(--team-ases-dio-soft); color: var(--team-ases-dio); }
.team-badge-asesores_diocesanos::before { background: var(--team-ases-dio); }

.coord-mark {
  display: inline-block; margin-left: 4px;
  font-family: 'Special Elite', monospace; font-weight: 700;
  font-size: 11px; color: var(--ambar-honda);
}

.cartucho {
  display: inline-block; padding: 4px 12px;
  background: var(--ambar); color: var(--tinta);
  border: 2px solid var(--tinta);
  font-family: 'Special Elite', monospace; font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.18em;
}
.cartucho-mar { background: var(--mar); color: var(--vela); border-color: var(--mar-honda); }
.cartucho-tierra { background: var(--tierra); color: var(--vela); border-color: var(--tierra-honda); }
.cartucho-safari { background: var(--safari); color: var(--vela); border-color: var(--safari-honda); }
.cartucho-cuero { background: var(--cuero); color: var(--vela); border-color: var(--cuero-claro); }

.parche {
  display: inline-block; padding: 2px 8px; border-radius: 2px;
  background: rgba(178,80,40,0.12); color: var(--tierra-honda);
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600; font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.12em;
}
.parche-belen { background: rgba(74,93,46,0.15); color: var(--safari-honda); }
.parche-betania { background: rgba(27,58,82,0.15); color: var(--mar-honda); }
.parche-warn { background: rgba(197,121,32,0.22); color: var(--ambar-honda); }

.tab-btn {
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.14em; font-size: 13px;
  padding: 12px 16px; border-bottom: 3px solid transparent;
  color: var(--muted); cursor: pointer; transition: all 0.15s;
  white-space: nowrap;
}
.tab-btn:hover { color: var(--tinta); }
.tab-btn.active { color: var(--tierra-honda); border-bottom-color: var(--tierra); }

.card-tripulante {
  background: var(--vela);
  border: 1px solid var(--rule);
  padding: 16px 16px 16px 22px;
  position: relative;
  transition: all 0.15s;
}
.card-tripulante:hover { box-shadow: 0 4px 12px rgba(28,20,11,0.12); border-color: var(--ambar); }
.card-tripulante.sin-form { border-style: dashed; }

.avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--pergamino-tibio); color: var(--cuero);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Cinzel', serif; font-weight: 600; font-size: 14px;
  flex-shrink: 0; letter-spacing: 0.02em;
}
.avatar.M { background: #B0C4D8; color: var(--mar-honda); }
.avatar.F { background: var(--pergamino-tibio); color: var(--tierra-honda); }

input[type="text"], input[type="search"], select {
  background: var(--vela);
  border: 1px solid var(--rule);
  padding: 8px 12px;
  font-family: 'Lora', serif;
  color: var(--tinta);
}
input:focus, select:focus { outline: 2px solid var(--ambar); outline-offset: -1px; border-color: var(--ambar); }

.btn-action {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 5px 10px;
  background: var(--mar); color: var(--vela);
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.08em;
  border-radius: 2px; text-decoration: none;
  transition: all 0.15s;
}
.btn-action:hover { background: var(--mar-honda); }
.btn-wa { background: #25D366; color: var(--tinta); }
.btn-wa:hover { background: #1ea855; }

.section-title {
  font-family: 'Cinzel', serif;
  font-size: 22px; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--tinta); margin-bottom: 8px;
}
.section-sub {
  font-family: 'Lora', serif; font-style: italic;
  color: var(--tinta-suave); margin-bottom: 24px;
}

.kpi { background: var(--vela); border: 1px solid var(--rule); padding: 16px; text-align: center; }
.kpi-num { font-family: 'Cinzel', serif; font-size: 36px; color: var(--tierra-honda); line-height: 1; }
.kpi-label { font-family: 'Barlow Condensed', sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--muted); margin-top: 4px; }

.evento-misa { border-left: 4px solid var(--muted); padding-left: 12px; opacity: 0.6; }
.evento-formacion { border-left: 4px solid var(--tierra); padding-left: 12px; }
.evento-profondo { border-left: 4px solid var(--mar); padding-left: 12px; }
.evento-retiro { border-left: 4px solid var(--ambar); padding-left: 12px; font-weight: 600; }
.evento-externo { border-left: 4px solid var(--cuero); padding-left: 12px; opacity: 0.7; font-style: italic; }
.evento-otro { border-left: 4px solid var(--safari); padding-left: 12px; }
.cumple-chip { display: inline-block; padding: 2px 6px; background: var(--pergamino-tibio); color: var(--cuero); font-family: 'Caveat', cursive; font-size: 16px; line-height: 1; border-radius: 12px; margin-left: 6px; }

.modal-overlay {
  position: fixed; inset: 0; background: rgba(28,20,11,0.55);
  z-index: 50; overflow-y: auto;
  display: flex; align-items: flex-start; justify-content: center;
  padding: 40px 16px;
}
.modal-content {
  background: var(--crema); max-width: 720px; width: 100%;
  border: 1px solid var(--cuero); padding: 28px;
  position: relative;
}
.modal-close { position: absolute; top: 12px; right: 16px; font-family: 'Special Elite', monospace; font-size: 18px; cursor: pointer; color: var(--cuero); }

table { width: 100%; border-collapse: collapse; }
th, td { padding: 8px 12px; text-align: left; vertical-align: top; }
th { font-family: 'Barlow Condensed', sans-serif; text-transform: uppercase; letter-spacing: 0.08em; font-size: 11px; color: var(--muted); border-bottom: 2px solid var(--rule); }
tr { border-bottom: 1px solid var(--pergamino-tibio); }
tr:hover { background: var(--pergamino-claro); }

.starfield-bg {
  background-image:
    radial-gradient(1.2px 1.2px at 12% 18%, rgba(197,121,32,0.7) 50%, transparent 50%),
    radial-gradient(1.6px 1.6px at 28% 42%, rgba(197,121,32,0.5) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 44% 28%, rgba(197,121,32,0.6) 50%, transparent 50%),
    radial-gradient(1.4px 1.4px at 58% 64%, rgba(197,121,32,0.4) 50%, transparent 50%),
    radial-gradient(1.0px 1.0px at 76% 22%, rgba(197,121,32,0.7) 50%, transparent 50%),
    radial-gradient(1.8px 1.8px at 88% 52%, rgba(197,121,32,0.5) 50%, transparent 50%),
    radial-gradient(0.6px 0.6px at 18% 78%, rgba(197,121,32,0.6) 50%, transparent 50%),
    radial-gradient(1.4px 1.4px at 38% 88%, rgba(197,121,32,0.4) 50%, transparent 50%),
    radial-gradient(1.0px 1.0px at 64% 84%, rgba(197,121,32,0.6) 50%, transparent 50%),
    radial-gradient(1.2px 1.2px at 92% 80%, rgba(197,121,32,0.5) 50%, transparent 50%);
}

.team-panel {
  background: var(--vela); border: 1px solid var(--rule); padding: 16px; position: relative;
}
.team-panel-header {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 12px; padding-bottom: 10px;
  border-bottom: 2px solid var(--rule);
}
.team-panel-title { font-family: 'Cinzel', serif; font-size: 18px; text-transform: uppercase; letter-spacing: 0.08em; }
.team-panel-count {
  font-family: 'Special Elite', monospace; font-size: 11px;
  padding: 2px 8px; background: var(--tinta); color: var(--vela);
  border-radius: 2px;
}

.bar-h {
  display: flex; height: 22px; border: 1px solid var(--rule); overflow: hidden;
  font-family: 'Barlow Condensed', sans-serif; font-size: 11px;
  font-weight: 600; color: var(--vela);
}
.bar-h > div {
  display: flex; align-items: center; justify-content: center;
  padding: 0 4px; white-space: nowrap;
}

@media (max-width: 640px) {
  .roster-grid { grid-template-columns: 1fr !important; }
  .kpi-grid { grid-template-columns: repeat(2, 1fr) !important; }
  .team-grid { grid-template-columns: 1fr !important; }
}
[x-cloak] { display: none !important; }
</style>
</head>
<body x-data="app()" x-cloak>

<header class="bg-mar-honda relative overflow-hidden">
  <div class="starfield-bg absolute inset-0 opacity-50"></div>
  <div class="relative max-w-6xl mx-auto px-6 py-8">
    <div class="flex items-center gap-4 mb-3">
      <svg viewBox="0 0 80 40" class="w-12 h-6" xmlns="http://www.w3.org/2000/svg">
        <path d="M 8 20 C 8 10, 25 6, 40 6 C 55 6, 65 10, 70 20 C 65 30, 55 34, 40 34 C 25 34, 8 30, 8 20 Z M 70 20 L 80 12 L 80 28 Z"
              fill="none" stroke="#C57920" stroke-width="1.8" stroke-linejoin="round"/>
        <circle cx="58" cy="18" r="1.6" fill="#C57920"/>
      </svg>
      <div class="f-mono text-xs tracking-widest" style="color: rgba(247,239,217,0.7);">
        ★ ETC · LXXXVIII · TRIPULACIÓN PARA UNA EXPEDICIÓN · ✦
      </div>
    </div>
    <h1 class="f-display text-3xl md:text-4xl" style="color: var(--vela);">Tablero de la Tripulación</h1>
    <div class="f-cond text-sm md:text-base mt-2" style="color: #E8CD88; letter-spacing: 0.18em; text-transform: uppercase;">
      <span x-text="data.meta.operativos"></span> operativos + <span x-text="data.meta.no_operativos"></span> ampliados = <span x-text="data.meta.total_equipo"></span> en el retiro
    </div>
    <p class="f-serif italic mt-3 max-w-2xl text-sm md:text-base" style="color: rgba(247,239,217,0.92);">
      "Ya no os llamo siervos, os he llamado amigos." <span class="f-mono text-xs ml-1" style="color: var(--ambar);">— Jn 15:15</span>
    </p>
    <p class="f-serif italic text-sm mt-1" style="color: rgba(247,239,217,0.7);">
      No fuimos a buscarlo: él nos estaba esperando.
    </p>
  </div>
</header>

<nav class="bg-pergamino border-b border-rule sticky top-0 z-40">
  <div class="max-w-6xl mx-auto px-2 overflow-x-auto">
    <div class="flex">
      <template x-for="tab in tabs" :key="tab.id">
        <button class="tab-btn" :class="{ 'active': activeTab === tab.id }"
                @click="activeTab = tab.id" x-text="tab.label"></button>
      </template>
    </div>
  </div>
</nav>

<!-- Barra de fuente de datos -->
<div class="bg-pergamino-claro border-b border-rule">
  <div class="max-w-6xl mx-auto px-4 md:px-6 py-2 flex items-center gap-2 text-xs flex-wrap">
    <span :class="dataSourceClass()" style="font-size: 14px; line-height: 1;">●</span>
    <span class="f-cond uppercase tracking-widest" :class="dataSourceClass()" x-text="dataSourceLabel()"></span>
    <span class="text-muted" x-show="lastSync" x-text="'· sync ' + lastSync"></span>
    <button class="btn-action" @click="sheetUrl ? loadFromSheet(sheetUrl) : (showSettings = true)" style="background: var(--mar); padding: 3px 8px;" x-show="dataSource !== 'local' || sheetUrl">↻ Recargar</button>
    <button class="ml-auto btn-action" @click="showSettings = !showSettings" style="background: var(--cuero); padding: 3px 8px;">⚙ Datos</button>
  </div>
  <div x-show="showSettings" x-transition class="max-w-6xl mx-auto px-4 md:px-6 pb-4">
    <div class="bg-vela border border-rule p-4 text-sm">
      <p class="mb-1"><strong>Conectar Google Sheet en vivo.</strong> Pegá la URL <em>CSV publicada</em> de la pestaña <em>Equipo</em>. Se guarda solo en este navegador.</p>
      <p class="text-xs text-muted mb-3">En Google Sheets: <em>Archivo → Compartir → Publicar en la web → </em> elegí la hoja "Equipo" y formato <em>CSV</em> → copiá el enlace y pegalo acá.</p>
      <div class="flex flex-wrap gap-2">
        <input type="text" x-model="sheetUrlInput" placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?gid=0&single=true&output=csv" class="flex-1 min-w-[260px]">
        <button class="btn-action btn-wa" @click="saveSheetUrl()">Guardar y cargar</button>
        <button class="btn-action" @click="sheetUrlInput=''; saveSheetUrl()" style="background: var(--muted);">Usar copia local</button>
      </div>
      <p class="text-xs mt-2 text-tierra" x-show="dataSource==='error'">⚠ No se pudo leer la hoja. Verificá que esté <strong>publicada como CSV</strong> y que el enlace termine en <code>output=csv</code>. Mientras tanto se muestra la copia local.</p>
      <p class="text-xs mt-2 text-safari" x-show="dataSource==='live'">✓ Leyendo de la hoja en vivo. Editás en Google Sheets y al recargar la página (o con ↻) se actualiza.</p>
    </div>
  </div>
</div>

<main class="max-w-6xl mx-auto px-4 md:px-6 py-8">

<!-- TAB: Tripulación -->
<section x-show="activeTab === 'tripulacion'" x-transition>
  <h2 class="section-title">Tripulación</h2>
  <p class="section-sub">Roster del equipo del retiro · busca, filtra y contacta.</p>

  <div class="flex flex-wrap gap-2 mb-4 items-center">
    <span class="team-badge team-badge-directores">Director</span>
    <span class="team-badge team-badge-asesores">Asesor</span>
    <span class="team-badge team-badge-guias">Guía</span>
    <span class="team-badge team-badge-cocina">Cocina</span>
    <span class="team-badge team-badge-musica">Música</span>
    <span class="team-badge team-badge-asesores_cocina">Asesor Cocina</span>
    <span class="team-badge team-badge-asesores_espirituales">Asesor Esp.</span>
    <span class="team-badge team-badge-asesores_diocesanos">Diocesano</span>
    <span class="f-mono text-xs text-muted ml-2">★ coord · borde discontinuo = sin form · fondo claro = no operativo</span>
  </div>

  <div class="flex flex-wrap gap-3 mb-6">
    <input type="search" x-model="search" placeholder="Buscar nombre…" class="flex-1 min-w-[200px]">
    <select x-model="filterOperativo">
      <option value="">Operativos + presentes</option>
      <option value="op">Solo operativos</option>
      <option value="no_op">Solo presentes no-op</option>
    </select>
    <select x-model="filterArea">
      <option value="">Todas las áreas</option>
      <option value="directores">Directores</option>
      <option value="asesores">Asesores</option>
      <option value="guias">Guías</option>
      <option value="cocina">Cocina</option>
      <option value="musica">Música</option>
      <option value="asesores_cocina">Asesores Cocina</option>
      <option value="asesores_espirituales">Asesores Espirituales</option>
      <option value="asesores_diocesanos">Asesores Diocesanos</option>
    </select>
    <select x-model="filterSexo">
      <option value="">F y M</option>
      <option value="F">Solo F</option>
      <option value="M">Solo M</option>
    </select>
    <select x-model="filterComunidad">
      <option value="">Todas comunidades</option>
      <option value="Belén">Belén</option>
      <option value="Betania">Betania</option>
      <option value="Por confirmar">Por confirmar</option>
    </select>
    <select x-model="filterVeterania">
      <option value="">Toda veteranía</option>
      <option value="0">0 ETCs (rookies)</option>
      <option value="1">1 ETC</option>
      <option value="2-4">2-4 ETCs</option>
      <option value="5+">5+ ETCs (experimentados)</option>
    </select>
  </div>

  <p class="text-xs text-muted mb-4 f-cond uppercase tracking-widest">
    Mostrando <span x-text="filteredEquipo.length"></span> de <span x-text="data.equipo.length"></span>
  </p>

  <div class="roster-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <template x-for="p in filteredEquipo" :key="p.id">
      <div class="card-tripulante" :class="cardClass(p)" @click="openModal(p)" style="cursor: pointer;">
        <div class="team-strip"></div>
        <div class="flex items-start gap-3">
          <div class="avatar" :class="p.sexo" x-text="initials(p.nombre)"></div>
          <div class="flex-1 min-w-0">
            <div class="f-display text-sm leading-tight" x-text="cleanName(p.nombre)"></div>
            <div class="flex flex-wrap gap-1 mt-1 items-center">
              <span class="team-badge" :class="'team-badge-' + p.area" x-text="teamLabel(p.area)"></span>
              <span class="coord-mark" x-show="isCoord(p)" title="Coordinador">★</span>
              <span x-show="p.sin_formulario && !p.vacante" class="parche parche-warn">Sin formulario</span>
              <span x-show="p.backup" class="parche" style="background: rgba(27,58,82,0.15); color: var(--mar);">Backup</span>
              <span x-show="p.vacante" class="parche parche-warn">Vacante</span>
              <span x-show="!p.operativo && !p.backup && !p.vacante" class="parche" style="background: rgba(122,100,64,0.18); color: var(--muted);">Solo retiro</span>
            </div>
            <div class="text-xs text-muted mt-1 f-mono" x-show="!p.sin_formulario || p.vacante" x-text="p.sexo + ' · ' + (p.edad ? p.edad + 'a' : '?') + ' · ' + p.rol"></div>
          </div>
          <div class="cartucho" :class="cartuchoEtcsClass(p)" x-show="p.etcs_servidos !== null && p.etcs_servidos !== undefined">
            <div class="text-center leading-none">
              <div class="text-base" x-text="p.etcs_servidos"></div>
              <div style="font-size:8px; opacity:0.8; margin-top:2px;">ETCs sv.</div>
            </div>
          </div>
        </div>
        <div class="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-xs text-tinta-suave" x-show="!p.sin_formulario">
          <span x-show="p.cumple_mes"><span class="f-cond uppercase tracking-widest text-muted text-[10px]">Cumple</span> <span x-text="formatCumple(p)"></span></span>
          <span x-show="p.etc_propio"><span class="f-cond uppercase tracking-widest text-muted text-[10px]">ETC</span> <span x-text="p.etc_propio + (p.etc_anio_propio ? ' (' + p.etc_anio_propio + ')' : '')"></span></span>
          <span x-show="p.residencia && p.residencia !== '—'"><span class="f-cond uppercase tracking-widest text-muted text-[10px]">📍</span> <span x-text="p.residencia"></span></span>
          <span x-show="p.comunidad && p.comunidad !== '—' && p.comunidad !== 'Por confirmar'" class="parche" :class="comunidadClass(p.comunidad)" x-text="p.comunidad"></span>
        </div>
        <div class="mt-3 flex gap-2" @click.stop x-show="p.telefono">
          <a class="btn-action btn-wa" :href="waLink(p.telefono)" target="_blank">WhatsApp</a>
          <a class="btn-action" :href="'tel:+' + p.telefono">Llamar</a>
        </div>
        <div class="mt-3 text-xs italic text-muted" x-show="p.sin_formulario">
          Pendiente formulario · click para más detalles
        </div>
      </div>
    </template>
  </div>
</section>

<!-- TAB: Dimensiones por equipo (NEW) -->
<section x-show="activeTab === 'dimensiones'" x-transition>
  <h2 class="section-title">Dimensiones por equipo</h2>
  <p class="section-sub">Composición de cada equipo para evaluar balance y decidir asignaciones.</p>

  <div class="team-grid grid grid-cols-1 md:grid-cols-2 gap-5">
    <template x-for="t in teamStats" :key="t.area">
      <div class="team-panel">
        <div class="team-panel-header">
          <span class="team-badge" :class="'team-badge-' + t.area" x-text="t.label"></span>
          <span class="team-panel-count"><span x-text="t.n"></span> tripulantes</span>
          <span x-show="t.sin_form > 0" class="parche parche-warn" x-text="t.sin_form + ' sin form'"></span>
        </div>

        <div class="space-y-3 text-sm">
          <div>
            <div class="flex justify-between text-xs text-muted f-cond uppercase tracking-widest mb-1">
              <span>Sexo (de <span x-text="t.confirmados"></span> con form)</span>
              <span x-text="'F ' + t.F + ' · M ' + t.M"></span>
            </div>
            <div class="bar-h" x-html="t.bar_sexo"></div>
          </div>
          <div>
            <div class="flex justify-between text-xs text-muted f-cond uppercase tracking-widest mb-1">
              <span>Comunidad</span>
              <span x-text="'Belén ' + t.belen + ' · Betania ' + t.beta"></span>
            </div>
            <div class="bar-h" x-html="t.bar_comu"></div>
          </div>
          <div>
            <div class="flex justify-between text-xs text-muted f-cond uppercase tracking-widest mb-1">
              <span>Veteranía</span>
              <span class="f-mono text-xs" x-text="'rk ' + t.rook + ' · biz ' + t.bz + ' · med ' + t.med + ' · vet ' + t.vet"></span>
            </div>
            <div class="bar-h" x-html="t.bar_vet"></div>
          </div>
          <div class="grid grid-cols-2 gap-3 pt-2 border-t border-rule">
            <div>
              <div class="f-cond uppercase tracking-widest text-xs text-muted">Edad</div>
              <div x-text="t.edad_rango + ' (avg ' + t.edad_avg + ')'"></div>
            </div>
            <div>
              <div class="f-cond uppercase tracking-widest text-xs text-muted">Residencia</div>
              <div class="text-xs" x-text="t.residencia"></div>
            </div>
          </div>

          <div x-show="t.alerta" class="mt-3 p-2 text-xs italic" style="background: rgba(197,121,32,0.12); color: var(--ambar-honda); border-left: 3px solid var(--ambar);">
            <span x-text="t.alerta"></span>
          </div>
        </div>
      </div>
    </template>
  </div>

  <div class="mt-6 bg-pergamino-claro border border-rule p-5">
    <h3 class="f-display text-base text-tierra-honda mb-2">Recomendaciones para nuevas en Cocina</h3>
    <p class="text-sm text-tinta-suave mb-3">El equipo de cocina ya completó sus formularios. Para balancear el perfil del equipo, la sugerencia es:</p>
    <ul class="text-sm space-y-1 list-disc list-inside" x-html="recomendacionVacantes()"></ul>
  </div>
</section>

<!-- TAB: Equipos auxiliares -->
<section x-show="activeTab === 'auxiliares'" x-transition>
  <h2 class="section-title">Equipos auxiliares</h2>
  <p class="section-sub">Equipos no operativos que se forman aparte del cuerpo de retiro · pueden incluir gente externa al equipo.</p>

  <div class="bg-pergamino-claro border border-rule p-4 mb-6 text-sm">
    <p><strong>Distinción:</strong> el manifiesto operativo (45 personas) son los que sostienen la formación semanal y el retiro mismo. Los <em>asesores ampliados</em> (9) están en el retiro pero no en la formación; los <em>equipos auxiliares</em> son verticales paralelos.</p>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
    <template x-for="aux in data.equipos_auxiliares" :key="aux.nombre">
      <div class="bg-vela border border-rule p-5 relative" style="border-style: dashed;">
        <div style="position:absolute; top:-10px; left:16px; background:var(--ambar); color:var(--tinta); padding:2px 10px; font-family:'Special Elite',monospace; font-size:10px; letter-spacing:0.16em;" x-text="aux.estado"></div>
        <h3 class="f-display text-base text-tierra-honda mb-2" x-text="aux.nombre"></h3>
        <p class="text-sm text-tinta-suave mb-3" x-text="aux.descripcion"></p>
        <div class="text-xs">
          <div class="f-cond uppercase tracking-widest text-muted">Responsable sugerido</div>
          <div x-text="aux.responsable_sugerido"></div>
        </div>
        <div class="text-xs mt-2">
          <div class="f-cond uppercase tracking-widest text-muted">Miembros</div>
          <div x-show="!aux.miembros.length" class="italic text-muted">— por designar —</div>
          <ul x-show="aux.miembros.length" class="list-disc list-inside">
            <template x-for="m in aux.miembros" :key="m"><li x-text="m"></li></template>
          </ul>
        </div>
      </div>
    </template>
  </div>

  <h3 class="f-display text-lg text-tierra-honda mb-3">Asesores ampliados (presentes en retiro)</h3>
  <p class="text-sm text-tinta-suave mb-4">Aparecen en el retiro pero no son parte del equipo operativo de formación.</p>
  <div class="roster-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <template x-for="p in noOperativos" :key="p.id">
      <div class="card-tripulante" :class="cardClass(p)" @click="openModal(p)" style="cursor: pointer;">
        <div class="team-strip"></div>
        <div class="flex items-start gap-3">
          <div class="avatar" :class="p.sexo" x-text="initials(p.nombre)"></div>
          <div class="flex-1 min-w-0">
            <div class="f-display text-sm leading-tight" x-text="cleanName(p.nombre)"></div>
            <div class="flex flex-wrap gap-1 mt-1 items-center">
              <span class="team-badge" :class="'team-badge-' + p.area" x-text="teamLabel(p.area)"></span>
              <span class="parche" style="background: rgba(122,100,64,0.18); color: var(--muted);">Solo retiro</span>
            </div>
            <div class="text-xs text-muted mt-1 italic" x-text="p.rol"></div>
          </div>
        </div>
      </div>
    </template>
  </div>
</section>

<!-- TAB: Bitácora -->
<section x-show="activeTab === 'bitacora'" x-transition>
  <h2 class="section-title">Bitácora</h2>
  <p class="section-sub">Agregados del equipo · proporciones generales.</p>

  <p class="text-xs text-muted mb-4 f-cond uppercase tracking-widest">KPIs sobre los <span x-text="data.meta.operativos"></span> operativos (excluye asesores ampliados)</p>
  <div class="kpi-grid grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
    <div class="kpi"><div class="kpi-num" x-text="data.meta.operativos"></div><div class="kpi-label">Operativos</div></div>
    <div class="kpi"><div class="kpi-num"><span x-text="countSexoOp('F')"></span><span class="text-tinta text-base mx-1">/</span><span x-text="countSexoOp('M')"></span></div><div class="kpi-label">F / M</div></div>
    <div class="kpi"><div class="kpi-num"><span x-text="countComunidadOp('Belén')"></span><span class="text-tinta text-base mx-1">/</span><span x-text="countComunidadOp('Betania')"></span></div><div class="kpi-label">Belén / Betania</div></div>
    <div class="kpi"><div class="kpi-num" x-text="countSinFormOp()"></div><div class="kpi-label">Sin formulario</div></div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
    <div class="bg-vela border border-rule p-4">
      <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">Residencia</h3>
      <canvas id="chart-residencia" height="180"></canvas>
    </div>
    <div class="bg-vela border border-rule p-4">
      <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">Veteranía (ETCs servidos)</h3>
      <canvas id="chart-veterania" height="180"></canvas>
    </div>
    <div class="bg-vela border border-rule p-4">
      <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">Edad</h3>
      <canvas id="chart-edad" height="180"></canvas>
    </div>
    <div class="bg-vela border border-rule p-4">
      <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">Área</h3>
      <canvas id="chart-area" height="180"></canvas>
    </div>
    <div class="bg-vela border border-rule p-4 md:col-span-2">
      <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">ETC de origen (cohorte) · color por comunidad</h3>
      <canvas id="chart-etc-origen" height="120"></canvas>
    </div>
  </div>

  <div class="bg-pergamino-claro border border-rule p-4">
    <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">Tallas de t-shirt</h3>
    <div class="flex flex-wrap gap-4">
      <template x-for="(n, talla) in countTallas()" :key="talla">
        <div class="flex items-center gap-2">
          <span class="cartucho cartucho-cuero" x-text="talla"></span>
          <span class="f-display text-lg" x-text="n"></span>
        </div>
      </template>
    </div>
  </div>
</section>

<!-- TAB: Travesía -->
<section x-show="activeTab === 'travesia'" x-transition>
  <h2 class="section-title">Travesía</h2>
  <p class="section-sub">Calendario del proceso cruzado con cumpleaños del equipo.</p>
  <template x-for="mes in mesesProceso" :key="mes.nombre">
    <div class="mb-6 bg-vela border border-rule p-4">
      <h3 class="f-display text-lg text-tierra-honda mb-3" x-text="mes.nombre + ' 2026'"></h3>
      <ul class="space-y-2 text-sm">
        <template x-for="item in mes.items" :key="item.key">
          <li :class="item.eventoClass">
            <div class="flex items-baseline gap-3">
              <span class="f-mono text-xs text-cuero whitespace-nowrap" x-text="item.fechaTxt"></span>
              <span x-html="item.contenido"></span>
            </div>
          </li>
        </template>
      </ul>
    </div>
  </template>
</section>

<!-- TAB: Salud -->
<section x-show="activeTab === 'salud'" x-transition>
  <h2 class="section-title">Botiquín y rancho</h2>
  <p class="section-sub">Alergias, condiciones, menú y ambiente del retiro.</p>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div class="bg-vela border border-rule p-5">
      <h3 class="f-display text-base text-tierra-honda mb-3">Alergias alimentarias</h3>
      <ul class="space-y-2 text-sm">
        <template x-for="[k, v] in Object.entries(data.salud.alergias_alimentarias)" :key="k">
          <li><span class="parche" x-text="k.toUpperCase() + ' · ' + v.length"></span><span class="text-tinta-suave block mt-1" x-text="v.join(' · ')"></span></li>
        </template>
      </ul>
    </div>
    <div class="bg-vela border border-rule p-5">
      <h3 class="f-display text-base text-tierra-honda mb-3">Alergias a medicamentos</h3>
      <ul class="space-y-2 text-sm">
        <template x-for="[k, v] in Object.entries(data.salud.alergias_medicamentos)" :key="k">
          <li><span class="parche" x-text="k"></span><span class="text-tinta-suave block mt-1" x-text="v.join(' · ')"></span></li>
        </template>
      </ul>
    </div>
    <div class="bg-vela border border-rule p-5">
      <h3 class="f-display text-base text-tierra-honda mb-3">Condiciones</h3>
      <ul class="space-y-2 text-sm">
        <template x-for="[k, v] in Object.entries(data.salud.condiciones)" :key="k">
          <li><span class="parche" x-text="k"></span><span class="text-tinta-suave block mt-1" x-text="v.join(' · ')"></span></li>
        </template>
        <li class="pt-2 border-t border-rule mt-3">
          <span class="parche" style="background: rgba(74,93,46,0.18); color: var(--safari);">ASMÁTICAS</span>
          <span class="text-tinta-suave block mt-1" x-text="data.salud.asmaticas.join(' · ')"></span>
        </li>
      </ul>
    </div>
    <div class="bg-mar p-5" style="color: var(--vela);">
      <h3 class="f-display text-base mb-3" style="color: var(--vela);">Botiquín del retiro</h3>
      <div class="text-sm space-y-3">
        <div>
          <span class="f-cond uppercase tracking-widest text-xs" style="color: #E8CD88;">SÍ incluir</span>
          <ul class="list-disc list-inside mt-1 space-y-1">
            <li>Paracetamol</li><li>Inhalador / broncodilatador</li>
            <li>Antialérgico oral (Loratadina o Difenhidramina)</li>
            <li>Antimigrañosos (Dorian e Ismarie traen los suyos)</li>
            <li>Antiácido / Omeprazol</li><li>Sales de rehidratación</li>
            <li>Curitas, gasas, termómetro, tensiómetro</li>
          </ul>
        </div>
        <div>
          <span class="f-cond uppercase tracking-widest text-xs" style="color: var(--ambar);">NO incluir</span>
          <ul class="list-disc list-inside mt-1 space-y-1">
            <li>Penicilina (Luisa)</li><li>Ibuprofeno (Tomás)</li>
            <li>AINEs en general (Dayrelins)</li>
            <li>Neo-Melubrina / Metamizol (Ismarie)</li>
            <li>Metoclopramida (Jhonnalia)</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="bg-safari p-5" style="color: var(--vela);">
      <h3 class="f-display text-base mb-3" style="color: var(--vela);">Menú · alérgenos</h3>
      <ul class="text-sm space-y-2 list-disc list-inside">
        <li><strong>Mariscos (4):</strong> evitar como plato principal.</li>
        <li><strong>Piña (3):</strong> nada en jugos, postres, marinadas.</li>
        <li><strong>Huevo (1):</strong> opción sin huevo en desayuno.</li>
        <li><strong>Canela (1):</strong> ojo postres.</li>
        <li><strong>Diabetes (Luisa):</strong> horarios regulares, bajo azúcar.</li>
        <li><strong>Gastritis (Candy):</strong> nada irritante.</li>
        <li><strong>Presión (María del Carmen):</strong> bajo sodio.</li>
      </ul>
    </div>
    <div class="bg-cuero p-5" style="color: var(--vela);">
      <h3 class="f-display text-base mb-3" style="color: var(--vela);">Ambiente · Higüey</h3>
      <ul class="text-sm space-y-2 list-disc list-inside">
        <template x-for="item in data.salud.ambiente_higuey" :key="item"><li x-text="item"></li></template>
      </ul>
    </div>
  </div>
</section>

<!-- TAB: Cartas -->
<section x-show="activeTab === 'cartas'" x-transition>
  <h2 class="section-title">Cartas náuticas</h2>
  <p class="section-sub">Banderas operativas · advertencias y acciones.</p>
  <div class="bg-vela border border-rule overflow-x-auto">
    <table class="text-sm">
      <thead><tr><th class="w-12">#</th><th>Bandera</th><th>Persona</th><th>Acción</th><th>Responsable</th></tr></thead>
      <tbody>
        <template x-for="b in data.banderas" :key="b.n">
          <tr>
            <td class="f-mono text-cuero" x-text="b.n"></td>
            <td x-text="b.bandera"></td>
            <td class="text-tinta-suave" x-text="b.persona"></td>
            <td class="text-tinta-suave" x-text="b.accion"></td>
            <td><span class="parche" x-text="b.resp"></span></td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</section>

<!-- TAB: Invitados -->
<section x-show="activeTab === 'invitados'" x-transition>
  <h2 class="section-title">Invitados y vituallas</h2>
  <p class="section-sub">Invitados propuestos + plan de recaudación.</p>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div>
      <h3 class="f-display text-base text-tierra-honda mb-3">Invitados propuestos</h3>
      <div class="bg-vela border border-rule p-4 text-sm space-y-3">
        <template x-for="x in data.invitados" :key="x.inviter">
          <div class="border-b border-pergamino-tibio pb-2 last:border-b-0">
            <div class="f-cond uppercase tracking-widest text-xs text-cuero" x-text="x.inviter + ' →'"></div>
            <template x-for="inv in x.invitados" :key="inv.nombre">
              <div class="ml-2" x-text="'· ' + inv.nombre + ' (' + (inv.edad || '?') + ', ' + inv.relacion + ')'"></div>
            </template>
          </div>
        </template>
      </div>
    </div>
    <div>
      <h3 class="f-display text-base text-tierra-honda mb-3">Recaudación</h3>
      <div class="bg-vela border border-rule p-4 text-sm">
        <table class="text-sm">
          <thead><tr><th>Propuesta</th><th class="text-right">Menciones</th></tr></thead>
          <tbody>
            <template x-for="r in data.recaudacion.top" :key="r.propuesta">
              <tr><td x-text="r.propuesta"></td><td class="text-right f-display text-tierra-honda" x-text="r.menciones"></td></tr>
            </template>
          </tbody>
        </table>
      </div>
      <div class="bg-pergamino-claro border border-rule p-4 mt-4 text-sm space-y-3">
        <p class="italic">"<span x-text="data.recaudacion.cita_franklin"></span>" <span class="f-cond text-xs uppercase tracking-widest text-cuero">— Franklin</span></p>
        <p class="italic">"<span x-text="data.recaudacion.cita_pamela"></span>" <span class="f-cond text-xs uppercase tracking-widest text-cuero">— Pamela</span></p>
      </div>
    </div>
  </div>
</section>

</main>

<!-- Modal -->
<div x-show="selected" @click.self="selected = null" class="modal-overlay" x-transition x-cloak>
  <div class="modal-content" x-show="selected">
    <div class="modal-close" @click="selected = null">✕</div>
    <template x-if="selected">
      <div>
        <div class="flex items-start gap-4 mb-4">
          <div class="avatar" :class="selected.sexo" x-text="initials(selected.nombre)" style="width:64px; height:64px; font-size:18px;"></div>
          <div class="flex-1">
            <div class="f-display text-xl text-tinta" x-text="cleanName(selected.nombre)"></div>
            <div class="flex flex-wrap gap-2 mt-2 items-center">
              <span class="team-badge" :class="'team-badge-' + selected.area" x-text="teamLabel(selected.area)"></span>
              <span class="coord-mark" x-show="isCoord(selected)">★ Coordinador</span>
              <span x-show="selected.sin_formulario" class="parche parche-warn">Sin formulario aún</span>
              <span x-show="selected.comunidad && !['—','Por confirmar'].includes(selected.comunidad)" class="parche" :class="comunidadClass(selected.comunidad)" x-text="'Comunidad ' + selected.comunidad"></span>
            </div>
            <div class="f-mono text-xs text-muted mt-2" x-show="!selected.sin_formulario" x-text="selected.sexo + ' · ' + (selected.edad ? selected.edad + ' años · ' : '') + 'cumple ' + formatCumple(selected)"></div>
            <div class="f-mono text-xs text-muted" x-show="selected.etc_propio" x-text="'ETC ' + selected.etc_propio + (selected.etc_anio_propio ? ' (' + selected.etc_anio_propio + ')' : '') + ' · ' + (selected.etcs_servidos !== null ? selected.etcs_servidos + ' ETCs servidos' : '') + ' · ' + selected.residencia"></div>
          </div>
          <div class="cartucho" :class="cartuchoEtcsClass(selected)" x-show="selected.etcs_servidos !== null && selected.etcs_servidos !== undefined">
            <div class="text-center leading-none">
              <div class="text-lg" x-text="selected.etcs_servidos"></div>
              <div style="font-size:8px; opacity:0.8; margin-top:2px;">ETCs</div>
            </div>
          </div>
        </div>

        <div class="flex gap-2 mb-5" x-show="selected.telefono">
          <a class="btn-action btn-wa" :href="waLink(selected.telefono)" target="_blank">WhatsApp</a>
          <a class="btn-action" :href="'tel:+' + selected.telefono">Llamar</a>
          <span class="ml-auto f-mono text-xs text-muted" x-text="'Tel: +' + selected.telefono"></span>
        </div>

        <div x-show="selected.sin_formulario" class="bg-pergamino-claro border border-rule p-4 text-sm">
          <p>Esta persona aún no ha respondido el formulario de preformación.</p>
          <p class="mt-2 f-cond uppercase tracking-widest text-xs text-cuero">Acción: enviar formulario antes de F1 (14-jun).</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm" x-show="!selected.sin_formulario">
          <div><div class="f-cond uppercase tracking-widest text-xs text-muted">Talla</div><div x-text="selected.talla || '—'"></div></div>
          <div><div class="f-cond uppercase tracking-widest text-xs text-muted">¿Invita?</div><div x-text="selected.invita || '—'"></div></div>
          <div class="md:col-span-2"><div class="f-cond uppercase tracking-widest text-xs text-muted">Palabra con la que llega</div><div class="f-script text-xl text-tierra-honda" x-text="(selected.palabra || '—').trim()"></div></div>
          <div class="md:col-span-2"><div class="f-cond uppercase tracking-widest text-xs text-muted">Qué espera vivir</div><div x-text="selected.que_espera || '—'"></div></div>
          <div class="md:col-span-2"><div class="f-cond uppercase tracking-widest text-xs text-muted">Miedos / resistencias</div><div x-text="selected.miedos || '—'"></div></div>
          <div class="md:col-span-2"><div class="f-cond uppercase tracking-widest text-xs text-muted">Tema que Dios trabaja</div><div x-text="selected.tema_dios || '—'"></div></div>
          <div><div class="f-cond uppercase tracking-widest text-xs text-muted">Alergias</div><div x-text="selected.alergias || 'Ninguna'"></div></div>
          <div><div class="f-cond uppercase tracking-widest text-xs text-muted">Condiciones</div><div x-text="selected.condiciones || 'Ninguna'"></div></div>
          <div><div class="f-cond uppercase tracking-widest text-xs text-muted">Medicamentos</div><div x-text="selected.medicamentos || 'Ninguno'"></div></div>
          <div><div class="f-cond uppercase tracking-widest text-xs text-muted">Contacto emergencia</div><div class="whitespace-pre-line" x-text="selected.contacto_emergencia || '—'"></div></div>
          <div class="md:col-span-2" x-show="selected.dudas"><div class="f-cond uppercase tracking-widest text-xs text-muted">Dudas / inquietudes</div><div x-text="selected.dudas"></div></div>
          <div class="md:col-span-2" x-show="selected.algo_directores"><div class="f-cond uppercase tracking-widest text-xs text-muted">Para los directores</div><div x-text="selected.algo_directores"></div></div>
          <div class="md:col-span-2" x-show="selected.invitados && selected.invitados.length">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Invitados que propone</div>
            <ul class="list-disc list-inside">
              <template x-for="inv in selected.invitados" :key="inv.nombre">
                <li x-text="inv.nombre + ' · ' + inv.edad + ' · ' + inv.relacion"></li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    </template>
  </div>
</div>

<footer class="bg-mar-honda mt-12 py-8 text-center" style="color: rgba(247,239,217,0.85);">
  <div class="f-script text-3xl text-ambar mb-2">siempre amigos</div>
  <div class="f-mono text-xs tracking-widest mb-1" style="color: rgba(247,239,217,0.6);">
    ETC LXXXVIII · TRIPULACIÓN PARA UNA EXPEDICIÓN
  </div>
  <div class="f-mono text-[10px] tracking-widest" style="color: rgba(247,239,217,0.4);">
    Datos · <span x-text="data.meta.version"></span> · <span x-text="data.equipo.length"></span> en el manifiesto
  </div>
</footer>

<script>
const DATA = __DATA_JSON__;

// ============================================================
// FUENTE DE DATOS EN VIVO (Google Sheet)
// Pegá la URL CSV publicada de la pestaña "Equipo" desde el botón
// "⚙ Datos" del tablero (se guarda en este navegador). O dejala fija acá:
// Google Sheets → Archivo → Compartir → Publicar en la web →
// hoja "Equipo", formato CSV → copiar enlace.
// ============================================================
const SHEET_CSV_URL_DEFAULT = '';
const AREA_ORDER = { directores:1, asesores:2, guias:3, cocina:4, musica:5, asesores_cocina:6, asesores_espirituales:7, asesores_diocesanos:8 };
const MESES_ABBR = { ene:1, feb:2, mar:3, abr:4, may:5, jun:6, jul:7, ago:8, sep:9, oct:10, nov:11, dic:12 };

function gName(n) { return (n || '').replace(' (sin formulario)', ''); }
function normName(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/\\s+/g, ' ').trim(); }
function parseCumpleStr(s) {
  const m = (s || '').match(/(\\d{1,2})\\s*[-\\/ ]\\s*([a-záéíóú]+)/i);
  if (!m) return {};
  const mo = MESES_ABBR[m[2].toLowerCase().slice(0, 3)];
  return mo ? { cumple_mes: mo, cumple_dia: parseInt(m[1]) } : {};
}
function parseCSV(text) {
  const rows = []; let row = [], field = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (q) {
      if (ch === '"') { if (text[i+1] === '"') { field += '"'; i++; } else q = false; }
      else field += ch;
    } else {
      if (ch === '"') q = true;
      else if (ch === ',') { row.push(field); field = ''; }
      else if (ch === '\\n') { row.push(field); rows.push(row); row = []; field = ''; }
      else if (ch === '\\r') { /* skip */ }
      else field += ch;
    }
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows;
}

function app() {
  return {
    data: DATA,
    baseEquipo: null,
    dataSource: 'local',
    sheetUrl: '',
    sheetUrlInput: '',
    showSettings: false,
    lastSync: '',
    activeTab: 'tripulacion',
    tabs: [
      {id:'tripulacion', label:'Tripulación'},
      {id:'dimensiones', label:'Dimensiones'},
      {id:'auxiliares', label:'Equipos auxiliares'},
      {id:'bitacora', label:'Bitácora'},
      {id:'travesia', label:'Travesía'},
      {id:'salud', label:'Botiquín & rancho'},
      {id:'cartas', label:'Cartas náuticas'},
      {id:'invitados', label:'Invitados & vituallas'},
    ],
    search: '',
    filterOperativo: '',
    filterArea: '',
    filterSexo: '',
    filterComunidad: '',
    filterVeterania: '',
    selected: null,
    chartsInit: false,

    get noOperativos() {
      return this.data.equipo.filter(p => !p.operativo && !p.backup && !p.vacante);
    },
    get backupsList() {
      return this.data.equipo.filter(p => p.backup);
    },

    get filteredEquipo() {
      const s = (this.search || '').toLowerCase().trim();
      return this.data.equipo.filter(p => {
        if (s && !p.nombre.toLowerCase().includes(s)) return false;
        if (this.filterOperativo === 'op' && !p.operativo) return false;
        if (this.filterOperativo === 'no_op' && p.operativo) return false;
        if (this.filterArea && p.area !== this.filterArea) return false;
        if (this.filterSexo && p.sexo !== this.filterSexo) return false;
        if (this.filterComunidad && p.comunidad !== this.filterComunidad) return false;
        if (this.filterVeterania) {
          const e = p.etcs_servidos;
          if (e === null || e === undefined) return false;
          if (this.filterVeterania === '0' && e !== 0) return false;
          if (this.filterVeterania === '1' && e !== 1) return false;
          if (this.filterVeterania === '2-4' && !(e >= 2 && e <= 4)) return false;
          if (this.filterVeterania === '5+' && e < 5) return false;
        }
        return true;
      });
    },

    cleanName(name) { return name.replace(' (sin formulario)', ''); },

    initials(name) {
      const parts = this.cleanName(name).split(/\\s+/).filter(w => w.length > 0);
      return parts.slice(0, 2).map(w => w[0] ? w[0].toUpperCase() : '').join('');
    },

    formatCumple(p) {
      if (!p.cumple_mes) return '—';
      const meses = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
      return p.cumple_dia + '-' + meses[p.cumple_mes - 1];
    },

    waLink(tel) {
      if (!tel) return '#';
      let t = tel.toString().replace(/[^0-9]/g, '');
      if (t.length === 10) t = '1' + t;
      return 'https://wa.me/' + t;
    },

    cardClass(p) {
      const c = ['team-' + p.area];
      if (p.sin_formulario) c.push('sin-form');
      if (!p.operativo) c.push('no-operativo');
      return c.join(' ');
    },

    teamLabel(area) {
      const m = {
        directores:'Director', asesores:'Asesor', guias:'Guía', cocina:'Cocina', musica:'Música',
        asesores_cocina:'Asesor Cocina', asesores_espirituales:'Asesor Espiritual', asesores_diocesanos:'Asesor Diocesano'
      };
      return m[area] || area;
    },

    isCoord(p) { return p.es_coord === true || (p.rol && p.rol.toLowerCase().includes('coord')); },

    comunidadClass(c) {
      if (c === 'Belén') return 'parche-belen';
      if (c === 'Betania') return 'parche-betania';
      return '';
    },

    cartuchoEtcsClass(p) {
      const n = p.etcs_servidos;
      if (n === null || n === undefined) return '';
      if (n === 0) return 'cartucho-cuero';
      if (n <= 2) return 'cartucho-safari';
      if (n <= 4) return '';
      if (n <= 7) return 'cartucho-tierra';
      return 'cartucho-mar';
    },

    countSexo(s) { return this.data.equipo.filter(p => p.sexo === s).length; },
    countComunidad(c) { return this.data.equipo.filter(p => p.comunidad === c).length; },
    countSinForm() { return this.data.equipo.filter(p => p.sin_formulario).length; },
    countSexoOp(s) { return this.data.equipo.filter(p => p.operativo && p.sexo === s).length; },
    countComunidadOp(c) { return this.data.equipo.filter(p => p.operativo && p.comunidad === c).length; },
    countSinFormOp() { return this.data.equipo.filter(p => p.operativo && p.sin_formulario).length; },
    countTallas() {
      const c = {};
      this.data.equipo.forEach(p => { if (p.talla) c[p.talla.toUpperCase().trim()] = (c[p.talla.toUpperCase().trim()] || 0) + 1; });
      const order = ['XS','S','M','L','XL','XXL'];
      const out = {};
      order.forEach(t => { if (c[t]) out[t] = c[t]; });
      return out;
    },

    pct(n, t) { return t ? Math.round(n*100/t) + '%' : '—'; },

    buildBar(parts) {
      const total = parts.reduce((s, p) => s + p[1], 0);
      if (total === 0) return '<div style="width:100%; background:var(--muted);">—</div>';
      return parts.map(([label, n, color]) => {
        if (n === 0) return '';
        const w = (n / total) * 100;
        return `<div style="width:${w}%; background:${color};" title="${label}: ${n}">${n > 0 && w > 8 ? label[0] + ':' + n : n}</div>`;
      }).join('');
    },

    get teamStats() {
      const areas = [
        { area: 'directores', label: 'Directores', color: 'var(--team-dir)' },
        { area: 'asesores', label: 'Asesores', color: 'var(--team-ases)' },
        { area: 'guias', label: 'Guías', color: 'var(--team-guias)' },
        { area: 'cocina', label: 'Cocina', color: 'var(--team-cocina)' },
        { area: 'musica', label: 'Música', color: 'var(--team-musica)' },
      ];
      return areas.map(a => {
        const all = this.data.equipo.filter(p => p.area === a.area && p.operativo);
        const conf = all.filter(p => !p.sin_formulario);
        const n = all.length;
        const nc = conf.length;
        const F = conf.filter(p => p.sexo === 'F').length;
        const M = conf.filter(p => p.sexo === 'M').length;
        const belen = conf.filter(p => p.comunidad === 'Belén').length;
        const beta = conf.filter(p => p.comunidad === 'Betania').length;
        const rook = conf.filter(p => p.etcs_servidos === 0).length;
        const bz = conf.filter(p => p.etcs_servidos === 1).length;
        const med = conf.filter(p => p.etcs_servidos !== null && p.etcs_servidos >= 2 && p.etcs_servidos <= 4).length;
        const vet = conf.filter(p => p.etcs_servidos !== null && p.etcs_servidos >= 5).length;
        const edades = conf.filter(p => p.edad).map(p => p.edad);
        const edad_min = edades.length ? Math.min(...edades) : '—';
        const edad_max = edades.length ? Math.max(...edades) : '—';
        const edad_avg = edades.length ? (edades.reduce((s,e) => s+e, 0) / edades.length).toFixed(1) : '—';
        const resCount = {};
        conf.forEach(p => { if (p.residencia && p.residencia !== '—') resCount[p.residencia] = (resCount[p.residencia] || 0) + 1; });
        const residencia = Object.entries(resCount).map(([r,n]) => `${r}=${n}`).join(' · ');

        // Alerta
        let alerta = '';
        if (a.area === 'cocina' && nc > 0) {
          if (M / nc < 0.35) alerta = `Solo ${M} hombres de ${nc} (${this.pct(M,nc)}). Priorizar M en nuevas.`;
          if (rook + bz > nc * 0.55) alerta = (alerta ? alerta + ' · ' : '') + `${rook+bz} de ${nc} con 0-1 ETC servido — equipo verde.`;
        }
        if (a.area === 'guias' && belen === 0) alerta = '0 personas de Belén — equipo 100% Betania.';
        if (a.area === 'musica' && belen === 0 && nc > 0) alerta = 'Equipo 100% Betania.';

        return {
          area: a.area,
          label: a.label,
          n, confirmados: nc, sin_form: n - nc,
          F, M, belen, beta, rook, bz, med, vet,
          edad_rango: edades.length ? `${edad_min}-${edad_max}` : '—',
          edad_avg,
          residencia: residencia || '—',
          bar_sexo: this.buildBar([['F', F, '#762E10'], ['M', M, '#1B3A52']]),
          bar_comu: this.buildBar([['Belén', belen, '#4A5D2E'], ['Betania', beta, '#1B3A52']]),
          bar_vet: this.buildBar([['Rookies', rook, '#6B4423'], ['Biz', bz, '#8B5C30'], ['Med', med, '#4A5D2E'], ['Vet', vet, '#C57920']]),
          alerta
        };
      });
    },

    recomendacionVacantes() {
      const t = this.teamStats.find(x => x.area === 'cocina');
      const out = [];
      if (t.M / t.confirmados < 0.35) {
        out.push(`<li>🧔 Priorizar <strong>hombres</strong> — Cocina actual ${t.M}/${t.confirmados} (${this.pct(t.M, t.confirmados)}). Subir a 6-7 M ayuda con la carga física.</li>`);
      } else {
        out.push(`<li>✓ Balance F/M aceptable; ambos sirven.</li>`);
      }
      const belenPct = t.belen / t.confirmados;
      if (belenPct > 0.40) {
        out.push(`<li>🌿 Priorizar <strong>Betania</strong> — Belén está sobrerrepresentado (${this.pct(t.belen, t.confirmados)}).</li>`);
      } else if (belenPct < 0.20) {
        out.push(`<li>🌿 Priorizar <strong>Belén</strong> — solo ${this.pct(t.belen, t.confirmados)} actualmente.</li>`);
      } else {
        out.push(`<li>✓ Balance Belén/Betania OK; cualquier comunidad sirve.</li>`);
      }
      if ((t.rook + t.bz) / t.confirmados > 0.55) {
        out.push(`<li>⚓ Priorizar <strong>veteranas con experiencia previa en cocina</strong> (2+ ETCs) — ${t.rook+t.bz}/${t.confirmados} actuales son rookies/biz.</li>`);
      } else {
        out.push(`<li>✓ Veteranía balanceada; rookies pueden entrar.</li>`);
      }
      out.push(`<li class="italic text-xs">Evitar duplicar alergias críticas (mariscos, piña, gastritis severa).</li>`);
      return out.join('');
    },

    get mesesProceso() {
      const meses = [{m:6, nombre:'Junio'}, {m:7, nombre:'Julio'}, {m:8, nombre:'Agosto'}, {m:9, nombre:'Septiembre'}];
      const mesesNombres = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
      return meses.map(mz => {
        const items = [];
        this.data.calendario.forEach(e => {
          const fmes = parseInt(e.fecha.split('-')[1]);
          if (fmes === mz.m) {
            const dia = parseInt(e.fecha.split('-')[2]);
            items.push({
              key: 'e-' + e.fecha,
              fecha: dia,
              fechaTxt: String(dia).padStart(2,'0') + '-' + mesesNombres[fmes-1],
              eventoClass: 'evento-' + (e.tipo === 'misa' ? 'misa' : e.tipo === 'formacion' ? 'formacion' : e.tipo === 'profondo' ? 'profondo' : e.tipo === 'retiro' ? 'retiro' : e.tipo === 'externo' ? 'externo' : 'otro'),
              contenido: '<strong>' + e.titulo + '</strong>' + (e.sin_formacion ? ' <span class="parche" style="background: rgba(122,100,64,0.18); color: var(--muted); margin-left: 6px;">SIN FORMACIÓN</span>' : '')
            });
          }
        });
        this.data.equipo.forEach(p => {
          if (p.cumple_mes === mz.m) {
            const teamColor = p.area === 'guias' ? 'var(--team-guias)' : p.area === 'cocina' ? 'var(--team-cocina)' : p.area === 'musica' ? 'var(--team-musica)' : p.area === 'directores' ? 'var(--team-dir)' : 'var(--team-ases)';
            items.push({
              key: 'c-' + p.id,
              fecha: p.cumple_dia,
              fechaTxt: String(p.cumple_dia).padStart(2,'0') + '-' + mesesNombres[mz.m-1],
              eventoClass: '',
              contenido: '<span class="cumple-chip">🎂</span> <span class="f-script text-lg" style="color:' + teamColor + ';">' + this.cleanName(p.nombre) + '</span> · <span class="text-muted text-xs">' + (p.cumple_anio ? 'cumple ' + ((new Date().getFullYear()) - p.cumple_anio) + ' · ' : '') + '<span class="team-badge team-badge-' + p.area + '" style="font-size:9px; padding: 1px 6px;">' + this.teamLabel(p.area) + '</span></span>'
            });
          }
        });
        items.sort((a,b) => a.fecha - b.fecha);
        return { ...mz, items };
      });
    },

    openModal(p) { this.selected = p; },

    mkChart(id, cfg) {
      const el = document.getElementById(id);
      if (!el) return null;
      const ex = Chart.getChart(el);
      if (ex) ex.destroy();
      return new Chart(el, cfg);
    },

    initCharts() {
      if (this.chartsInit) return;
      this.chartsInit = true;
      const colors = { pergamino:'#E8D2A1', tierra:'#B25028', mar:'#1B3A52', safari:'#4A5D2E', ambar:'#C57920', cuero:'#6B4423', muted:'#7A6440' };
      const palette = [colors.tierra, colors.mar, colors.safari, colors.ambar, colors.cuero, colors.muted];
      const fontFamily = "'Lora', serif";

      const resCount = {};
      this.data.equipo.forEach(p => { if (p.residencia && p.residencia !== '—') resCount[p.residencia] = (resCount[p.residencia] || 0) + 1; });
      this.mkChart('chart-residencia', {
        type: 'doughnut',
        data: { labels: Object.keys(resCount), datasets: [{ data: Object.values(resCount), backgroundColor: palette, borderColor: '#F7EFD9', borderWidth: 2 }] },
        options: { plugins: { legend: { position: 'right', labels: { font: { family: fontFamily, size: 11 } } } } }
      });

      let rook=0, m1=0, m24=0, v5=0;
      this.data.equipo.forEach(p => {
        if (p.etcs_servidos === null || p.etcs_servidos === undefined) return;
        if (p.etcs_servidos === 0) rook++;
        else if (p.etcs_servidos === 1) m1++;
        else if (p.etcs_servidos >= 2 && p.etcs_servidos <= 4) m24++;
        else v5++;
      });
      this.mkChart('chart-veterania', {
        type: 'bar',
        data: { labels: ['0 (rookies)','1','2-4','5+'], datasets: [{ data: [rook,m1,m24,v5], backgroundColor: [colors.cuero, colors.safari, colors.mar, colors.tierra] }] },
        options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { font: { family: fontFamily } } }, x: { ticks: { font: { family: fontFamily } } } } }
      });

      const ages = this.data.equipo.filter(p => p.edad).map(p => p.edad);
      const bins = [[18,21,'18-21'],[22,25,'22-25'],[26,29,'26-29'],[30,34,'30-34'],[35,99,'35+']];
      const ageCount = bins.map(([lo,hi,l]) => ages.filter(a => a>=lo && a<=hi).length);
      this.mkChart('chart-edad', {
        type: 'bar',
        data: { labels: bins.map(b => b[2]), datasets: [{ data: ageCount, backgroundColor: colors.ambar }] },
        options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { font: { family: fontFamily } } }, x: { ticks: { font: { family: fontFamily } } } } }
      });

      const areaCount = {};
      this.data.equipo.forEach(p => areaCount[p.area] = (areaCount[p.area] || 0) + 1);
      const areaColors = { directores: colors.tierra, asesores: colors.cuero, guias: colors.mar, cocina: colors.safari, musica: colors.ambar };
      const areaLabels = { directores:'Directores', asesores:'Asesores', guias:'Guías', cocina:'Cocina', musica:'Música' };
      const keys = Object.keys(areaCount);
      this.mkChart('chart-area', {
        type: 'bar',
        data: { labels: keys.map(k => areaLabels[k] || k), datasets: [{ data: keys.map(k => areaCount[k]), backgroundColor: keys.map(k => areaColors[k] || colors.muted) }] },
        options: { indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { font: { family: fontFamily }, stepSize: 1 } }, y: { ticks: { font: { family: fontFamily } } } } }
      });

      const etcMap = {};
      this.data.equipo.forEach(p => {
        if (!p.etc_propio) return;
        if (!etcMap[p.etc_propio]) etcMap[p.etc_propio] = { belen: 0, betania: 0 };
        if (p.comunidad === 'Belén') etcMap[p.etc_propio].belen++;
        else if (p.comunidad === 'Betania') etcMap[p.etc_propio].betania++;
      });
      const sortedEtcs = Object.keys(etcMap).map(Number).sort((a,b) => a-b);
      this.mkChart('chart-etc-origen', {
        type: 'bar',
        data: {
          labels: sortedEtcs.map(n => 'ETC ' + n),
          datasets: [
            { label: 'Belén', data: sortedEtcs.map(n => etcMap[n].belen), backgroundColor: colors.safari, stack: 's1' },
            { label: 'Betania', data: sortedEtcs.map(n => etcMap[n].betania), backgroundColor: colors.mar, stack: 's1' },
          ]
        },
        options: { plugins: { legend: { labels: { font: { family: fontFamily } } } }, scales: { y: { stacked: true, beginAtZero: true, ticks: { font: { family: fontFamily }, stepSize: 1 } }, x: { stacked: true, ticks: { font: { family: fontFamily }, maxRotation: 45 } } } }
      });
    },

    // ===== Fuente de datos en vivo =====
    dataSourceClass() { return this.dataSource === 'live' ? 'text-safari' : this.dataSource === 'error' ? 'text-tierra' : 'text-muted'; },
    dataSourceLabel() {
      if (this.dataSource === 'live') return 'Hoja en vivo';
      if (this.dataSource === 'error') return 'Error de hoja — usando copia local';
      return 'Copia local';
    },

    useLocalData() {
      this.data.equipo = JSON.parse(JSON.stringify(this.baseEquipo));
      this.recomputeMeta();
      this.dataSource = 'local';
      this.refreshCharts();
    },

    saveSheetUrl() {
      this.sheetUrl = (this.sheetUrlInput || '').trim();
      if (this.sheetUrl) localStorage.setItem('etc88_sheet_url', this.sheetUrl);
      else localStorage.removeItem('etc88_sheet_url');
      this.showSettings = false;
      this.loadFromSheet(this.sheetUrl);
    },

    async loadFromSheet(url) {
      if (!url) { this.useLocalData(); return; }
      try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 12000);
        const res = await fetch(url, { signal: ctrl.signal, redirect: 'follow' });
        clearTimeout(timer);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const text = await res.text();
        this.applySheetText(text);
        this.dataSource = 'live';
        this.lastSync = new Date().toLocaleTimeString('es-DO', { hour: '2-digit', minute: '2-digit' });
        this.refreshCharts();
      } catch (e) {
        console.warn('No se pudo leer la hoja en vivo:', e.message);
        this.dataSource = 'error';
      }
    },

    applySheetText(text) {
      const rows = parseCSV(text);
      const hi = rows.findIndex(r => r.map(x => (x || '').trim().toLowerCase()).includes('nombre'));
      if (hi < 0) throw new Error('No encontré la fila de encabezados (columna "Nombre")');
      const headers = rows[hi].map(h => (h || '').trim().toLowerCase());
      const col = {}; headers.forEach((h, i) => { if (!(h in col)) col[h] = i; });
      const val = (r, name) => { const i = col[name]; return i != null ? (r[i] || '').trim() : ''; };
      const dataRows = rows.slice(hi + 1).filter(r => r.some(c => (c || '').trim() !== ''));

      const baseByName = {};
      this.baseEquipo.forEach(p => { baseByName[normName(gName(p.nombre))] = p; });

      const out = [];
      dataRows.forEach((r, idx) => {
        const nm = val(r, 'nombre');
        if (!nm) return;
        const base = baseByName[normName(nm)] || {};
        const p = Object.assign({}, base);
        p.id = base.id || ('sheet-' + idx);
        p.nombre = base.nombre || nm;
        p.sexo = val(r, 'sexo') || base.sexo || '?';
        p.edad = parseInt(val(r, 'edad')) || base.edad || null;
        p.area = (val(r, 'área') || val(r, 'area') || base.area || 'por_asignar').trim();
        p.rol = val(r, 'rol') || base.rol || '';
        p.es_coord = /^s/i.test(val(r, 'coordinador'));
        p.operativo = /^s/i.test(val(r, 'operativo'));
        p.comunidad = val(r, 'comunidad') || base.comunidad || 'Por confirmar';
        p.residencia = val(r, 'residencia') || base.residencia || '—';
        p.etc_propio = parseInt(val(r, 'etc propio')) || base.etc_propio || null;
        p.etc_anio_propio = parseInt(val(r, 'año etc')) || base.etc_anio_propio || null;
        const sv = val(r, 'etcs servidos');
        p.etcs_servidos = sv === '' ? (base.etcs_servidos != null ? base.etcs_servidos : null) : parseInt(sv);
        if (isNaN(p.etcs_servidos)) p.etcs_servidos = null;
        const cp = parseCumpleStr(val(r, 'cumpleaños'));
        if (cp.cumple_mes) { p.cumple_mes = cp.cumple_mes; p.cumple_dia = cp.cumple_dia; }
        const tel = val(r, 'teléfono').replace(/[^0-9]/g, '');
        if (tel) p.telefono = tel;
        const talla = val(r, 'talla'); if (talla) p.talla = talla;
        p.sin_formulario = /^s/i.test(val(r, 'sin formulario'));
        out.push(p);
      });
      if (!out.length) throw new Error('La hoja no tiene filas de datos');
      this.sortEquipo(out);
      this.data.equipo = out;
      this.recomputeMeta();
    },

    sortEquipo(arr) {
      arr.sort((a, b) => {
        const op = (a.operativo ? 0 : 1) - (b.operativo ? 0 : 1); if (op) return op;
        const ar = (AREA_ORDER[a.area] || 9) - (AREA_ORDER[b.area] || 9); if (ar) return ar;
        const co = ((a.es_coord || /coord/i.test(a.rol || '')) ? 0 : 1) - ((b.es_coord || /coord/i.test(b.rol || '')) ? 0 : 1); if (co) return co;
        return gName(a.nombre).localeCompare(gName(b.nombre), 'es');
      });
    },

    recomputeMeta() {
      this.data.meta.operativos = this.data.equipo.filter(p => p.operativo).length;
      this.data.meta.no_operativos = this.data.equipo.filter(p => !p.operativo).length;
      this.data.meta.total_equipo = this.data.equipo.length;
    },

    refreshCharts() {
      this.chartsInit = false;
      if (this.activeTab === 'bitacora') this.$nextTick(() => this.initCharts());
    },

    init() {
      this.baseEquipo = JSON.parse(JSON.stringify(DATA.equipo));
      this.sheetUrl = localStorage.getItem('etc88_sheet_url') || SHEET_CSV_URL_DEFAULT;
      this.sheetUrlInput = this.sheetUrl;
      this.$watch('activeTab', val => {
        if (val === 'bitacora') this.$nextTick(() => this.initCharts());
      });
      if (this.sheetUrl) this.loadFromSheet(this.sheetUrl);
    }
  };
}
</script>
</body>
</html>
'''

output = HTML.replace('__DATA_JSON__', data_str)
with open('/home/user/ETC88/index.html', 'w', encoding='utf-8') as f:
    f.write(output)
print(f"Wrote /home/user/ETC88/index.html ({len(output)} bytes)")
