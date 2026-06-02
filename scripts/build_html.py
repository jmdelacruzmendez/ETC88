#!/usr/bin/env python3
"""Assemble the Tripulación HTML dashboard."""
import json

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
}
html, body { background: var(--crema); color: var(--tinta); }
body { font-family: 'Lora', Georgia, serif; font-size: 15px; line-height: 1.5; }
.f-display { font-family: 'Cinzel', serif; text-transform: uppercase; letter-spacing: 0.08em; }
.f-cond { font-family: 'Barlow Condensed', sans-serif; }
.f-mono { font-family: 'Special Elite', 'Courier Prime', monospace; }
.f-script { font-family: 'Caveat', cursive; }
.f-serif { font-family: 'Lora', serif; }
.bg-pergamino { background: var(--pergamino); }
.bg-pergamino-claro { background: var(--pergamino-claro); }
.bg-crema { background: var(--crema); }
.bg-vela { background: var(--vela); }
.bg-mar { background: var(--mar); color: var(--vela); }
.bg-mar-honda { background: var(--mar-honda); color: var(--vela); }
.bg-tierra { background: var(--tierra); color: var(--vela); }
.bg-safari { background: var(--safari); color: var(--vela); }
.bg-ambar { background: var(--ambar); color: var(--tinta); }
.bg-cuero { background: var(--cuero); color: var(--vela); }
.text-tierra { color: var(--tierra); }
.text-tierra-honda { color: var(--tierra-honda); }
.text-mar { color: var(--mar); }
.text-mar-honda { color: var(--mar-honda); }
.text-safari { color: var(--safari); }
.text-ambar { color: var(--ambar); }
.text-ambar-honda { color: var(--ambar-honda); }
.text-cuero { color: var(--cuero); }
.text-tinta { color: var(--tinta); }
.text-tinta-suave { color: var(--tinta-suave); }
.text-muted { color: var(--muted); }
.border-rule { border-color: var(--rule); }
.border-tierra { border-color: var(--tierra); }
.border-mar { border-color: var(--mar); }

/* sello / cartucho */
.cartucho {
  display: inline-block; padding: 4px 12px;
  background: var(--ambar); color: var(--tinta);
  border: 2px solid var(--tinta);
  font-family: 'Special Elite', monospace; font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.18em;
  position: relative;
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
  padding: 16px;
  position: relative;
  transition: all 0.15s;
}
.card-tripulante:hover { box-shadow: 0 4px 12px rgba(28,20,11,0.12); border-color: var(--ambar); }

.avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--pergamino-tibio); color: var(--cuero);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Cinzel', serif; font-weight: 600; font-size: 14px;
  flex-shrink: 0; letter-spacing: 0.02em;
}
.avatar.M { background: #B0C4D8; color: var(--mar-honda); }
.avatar.F { background: var(--pergamino-tibio); color: var(--tierra-honda); }

.coord-strip {
  height: 3px; width: 100%;
  background: var(--ambar);
  position: absolute; top: 0; left: 0;
}
.director-strip { background: var(--tierra); }
.asesor-strip { background: var(--mar); }

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

.kpi {
  background: var(--vela); border: 1px solid var(--rule);
  padding: 16px; text-align: center;
}
.kpi-num {
  font-family: 'Cinzel', serif; font-size: 36px;
  color: var(--tierra-honda); line-height: 1;
}
.kpi-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--muted); margin-top: 4px;
}

.evento-misa { border-left: 4px solid var(--muted); padding-left: 12px; opacity: 0.6; }
.evento-formacion { border-left: 4px solid var(--tierra); padding-left: 12px; }
.evento-profondo { border-left: 4px solid var(--mar); padding-left: 12px; }
.evento-retiro { border-left: 4px solid var(--ambar); padding-left: 12px; font-weight: 600; }
.evento-externo { border-left: 4px solid var(--cuero); padding-left: 12px; opacity: 0.7; font-style: italic; }
.evento-otro { border-left: 4px solid var(--safari); padding-left: 12px; }
.cumple-chip {
  display: inline-block; padding: 2px 6px;
  background: var(--pergamino-tibio); color: var(--cuero);
  font-family: 'Caveat', cursive; font-size: 16px; line-height: 1;
  border-radius: 12px; margin-left: 6px;
}

/* modal */
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
.modal-close {
  position: absolute; top: 12px; right: 16px;
  font-family: 'Special Elite', monospace; font-size: 18px;
  cursor: pointer; color: var(--cuero);
}

table { width: 100%; border-collapse: collapse; }
th, td { padding: 8px 12px; text-align: left; vertical-align: top; }
th {
  font-family: 'Barlow Condensed', sans-serif;
  text-transform: uppercase; letter-spacing: 0.08em;
  font-size: 11px; color: var(--muted);
  border-bottom: 2px solid var(--rule);
}
tr { border-bottom: 1px solid var(--pergamino-tibio); }
tr:hover { background: var(--pergamino-claro); }

.pez-icon {
  display: inline-block; width: 36px; height: 18px;
}

/* Constellation pattern */
.constelacion-bg {
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

@media (max-width: 640px) {
  .roster-grid { grid-template-columns: 1fr !important; }
  .kpi-grid { grid-template-columns: repeat(2, 1fr) !important; }
}
</style>
</head>
<body x-data="app()" x-cloak>

<!-- Header -->
<header class="bg-mar-honda relative overflow-hidden">
  <div class="constelacion-bg absolute inset-0 opacity-50"></div>
  <div class="relative max-w-6xl mx-auto px-6 py-8">
    <div class="flex items-center gap-4 mb-3">
      <!-- Pez IXΘYC SVG -->
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
      Constelación 49 · <span x-text="data.meta.total_equipo_v1"></span> registrados
    </div>
    <p class="f-serif italic mt-3 max-w-2xl text-sm md:text-base" style="color: rgba(247,239,217,0.92);">
      "Ya no os llamo siervos, os he llamado amigos." <span class="f-mono text-xs ml-1" style="color: var(--ambar);">— Jn 15:15</span>
    </p>
    <p class="f-serif italic text-sm mt-1" style="color: rgba(247,239,217,0.7);">
      No fuimos a buscarlo: él nos estaba esperando.
    </p>
  </div>
</header>

<!-- Tabs -->
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

<main class="max-w-6xl mx-auto px-4 md:px-6 py-8">

<!-- TAB: Tripulación -->
<section x-show="activeTab === 'tripulacion'" x-transition>
  <h2 class="section-title">Tripulación</h2>
  <p class="section-sub">Roster del equipo del retiro · busca, filtra y contacta.</p>

  <div class="flex flex-wrap gap-3 mb-6">
    <input type="search" x-model="search" placeholder="Buscar nombre…" class="flex-1 min-w-[200px]">
    <select x-model="filterArea">
      <option value="">Todas las áreas</option>
      <option value="directores">Directores</option>
      <option value="asesores">Asesores</option>
      <option value="guias">Guías</option>
      <option value="cocina">Cocina</option>
      <option value="musica">Música</option>
      <option value="por_asignar">Por asignar</option>
    </select>
    <select x-model="filterSexo">
      <option value="">F y M</option>
      <option value="F">Solo F</option>
      <option value="M">Solo M</option>
    </select>
    <select x-model="filterResidencia">
      <option value="">Todas residencias</option>
      <option value="SPM">SPM</option>
      <option value="Punta Cana">Punta Cana</option>
      <option value="Santo Domingo">Santo Domingo</option>
      <option value="El Seibo / SPM">El Seibo / SPM</option>
      <option value="Higüey / SPM">Higüey / SPM</option>
    </select>
    <select x-model="filterVeterania">
      <option value="">Toda veteranía</option>
      <option value="0">0 ETCs (rookies)</option>
      <option value="1">1 ETC</option>
      <option value="2-4">2-4 ETCs</option>
      <option value="5+">5+ ETCs (veteranos)</option>
    </select>
  </div>

  <p class="text-xs text-muted mb-4 f-cond uppercase tracking-widest">
    Mostrando <span x-text="filteredEquipo.length"></span> de <span x-text="data.equipo.length"></span>
  </p>

  <div class="roster-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <template x-for="p in filteredEquipo" :key="p.id">
      <div class="card-tripulante" @click="openModal(p)" style="cursor: pointer;">
        <div :class="stripClass(p)" class="coord-strip"></div>
        <div class="flex items-start gap-3">
          <div class="avatar" :class="p.sexo" x-text="initials(p.nombre)"></div>
          <div class="flex-1 min-w-0">
            <div class="f-display text-sm leading-tight" x-text="p.nombre"></div>
            <div class="flex flex-wrap gap-1 mt-1 items-center">
              <span class="parche" x-text="p.rol"></span>
              <span class="f-mono text-xs text-muted">·</span>
              <span class="f-mono text-xs text-muted" x-text="p.sexo + ' · ' + p.edad + 'a'"></span>
            </div>
          </div>
          <div class="cartucho" :class="cartuchoEtcsClass(p.etcs_servidos)">
            <div class="text-center leading-none">
              <div class="text-base" x-text="p.etcs_servidos"></div>
              <div style="font-size:8px; opacity:0.8; margin-top:2px;">ETCs sv.</div>
            </div>
          </div>
        </div>
        <div class="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-xs text-tinta-suave">
          <span><span class="f-cond uppercase tracking-widest text-muted text-[10px]">Cumple</span> <span x-text="formatCumple(p)"></span></span>
          <span><span class="f-cond uppercase tracking-widest text-muted text-[10px]">ETC</span> <span x-text="p.etc_propio + (p.etc_anio_propio ? ' (' + p.etc_anio_propio + ')' : '')"></span></span>
          <span><span class="f-cond uppercase tracking-widest text-muted text-[10px]">📍</span> <span x-text="p.residencia"></span></span>
        </div>
        <div class="mt-3 flex gap-2" @click.stop>
          <a class="btn-action btn-wa" :href="waLink(p.telefono)" target="_blank">WhatsApp</a>
          <a class="btn-action" :href="'tel:+' + p.telefono">Llamar</a>
        </div>
      </div>
    </template>
  </div>
</section>

<!-- TAB: Bitácora (dashboard) -->
<section x-show="activeTab === 'bitacora'" x-transition>
  <h2 class="section-title">Bitácora</h2>
  <p class="section-sub">Agregados del equipo · proporciones, veteranía, residencia, edad.</p>

  <div class="kpi-grid grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
    <div class="kpi"><div class="kpi-num" x-text="data.meta.total_equipo_v1"></div><div class="kpi-label">Tripulantes v1</div></div>
    <div class="kpi"><div class="kpi-num"><span x-text="countSexo('F')"></span><span class="text-tinta text-base mx-1">/</span><span x-text="countSexo('M')"></span></div><div class="kpi-label">Femenino / Masculino</div></div>
    <div class="kpi"><div class="kpi-num" x-text="countRookies()"></div><div class="kpi-label">Rookies (0-1 ETC)</div></div>
    <div class="kpi"><div class="kpi-num" x-text="countVeteranos()"></div><div class="kpi-label">Veteranos (5+ ETCs)</div></div>
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
      <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">Área (asignación actual)</h3>
      <canvas id="chart-area" height="180"></canvas>
    </div>
    <div class="bg-vela border border-rule p-4 md:col-span-2">
      <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">ETC de origen (cohorte)</h3>
      <canvas id="chart-etc-origen" height="120"></canvas>
    </div>
  </div>

  <div class="bg-pergamino-claro border border-rule p-4">
    <h3 class="f-cond uppercase tracking-widest text-xs text-muted mb-3">Tallas de t-shirt (para merch)</h3>
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

<!-- TAB: Travesía (cumpleaños × calendario) -->
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

<!-- TAB: Botiquín y rancho (salud) -->
<section x-show="activeTab === 'salud'" x-transition>
  <h2 class="section-title">Botiquín y rancho</h2>
  <p class="section-sub">Alergias, condiciones, menú y ambiente del retiro.</p>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div class="bg-vela border border-rule p-5">
      <h3 class="f-display text-base text-tierra-honda mb-3">Alergias alimentarias</h3>
      <ul class="space-y-2 text-sm">
        <template x-for="[k, v] in Object.entries(data.salud.alergias_alimentarias)" :key="k">
          <li>
            <span class="parche" x-text="k.toUpperCase() + ' · ' + v.length"></span>
            <span class="text-tinta-suave block mt-1" x-text="v.join(' · ')"></span>
          </li>
        </template>
      </ul>
    </div>

    <div class="bg-vela border border-rule p-5">
      <h3 class="f-display text-base text-tierra-honda mb-3">Alergias a medicamentos</h3>
      <ul class="space-y-2 text-sm">
        <template x-for="[k, v] in Object.entries(data.salud.alergias_medicamentos)" :key="k">
          <li>
            <span class="parche" x-text="k"></span>
            <span class="text-tinta-suave block mt-1" x-text="v.join(' · ')"></span>
          </li>
        </template>
      </ul>
    </div>

    <div class="bg-vela border border-rule p-5">
      <h3 class="f-display text-base text-tierra-honda mb-3">Condiciones</h3>
      <ul class="space-y-2 text-sm">
        <template x-for="[k, v] in Object.entries(data.salud.condiciones)" :key="k">
          <li>
            <span class="parche" x-text="k"></span>
            <span class="text-tinta-suave block mt-1" x-text="v.join(' · ')"></span>
          </li>
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
            <li>Paracetamol (analgésico universal)</li>
            <li>Inhalador / broncodilatador</li>
            <li>Antialérgico oral (Loratadina o Difenhidramina)</li>
            <li>Antimigrañosos / Triptanes (Dorian e Ismarie traen los suyos)</li>
            <li>Antiácido / Omeprazol</li>
            <li>Sales de rehidratación</li>
            <li>Curitas, gasas, termómetro, tensiómetro</li>
          </ul>
        </div>
        <div>
          <span class="f-cond uppercase tracking-widest text-xs" style="color: var(--ambar);">NO incluir / usar con cuidado extremo</span>
          <ul class="list-disc list-inside mt-1 space-y-1">
            <li>Penicilina / Amoxicilina (Luisa)</li>
            <li>Ibuprofeno (Tomás)</li>
            <li>AINEs en general (Dayrelins)</li>
            <li>Neo-Melubrina / Metamizol (Ismarie)</li>
            <li>Metoclopramida (Jhonnalia)</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="bg-safari p-5" style="color: var(--vela);">
      <h3 class="f-display text-base mb-3" style="color: var(--vela);">Menú · alérgenos a evitar</h3>
      <ul class="text-sm space-y-2 list-disc list-inside">
        <li><strong>Mariscos (4 alérgicas):</strong> evitar como plato principal; alternativa pollo/carne.</li>
        <li><strong>Piña (3 alérgicos):</strong> nada de piña en jugos, postres, marinadas tropicales.</li>
        <li><strong>Huevo (1):</strong> opción sin huevo en desayuno (avena, fruta, pan).</li>
        <li><strong>Canela (1):</strong> ojo con postres y atoles.</li>
        <li><strong>Diabetes (Luisa):</strong> horarios regulares, opciones bajas en azúcar.</li>
        <li><strong>Gastritis severa (Candy):</strong> nada irritante (no picante, no grasoso pesado).</li>
        <li><strong>Presión (María del Carmen):</strong> bajo en sodio.</li>
      </ul>
    </div>

    <div class="bg-cuero p-5" style="color: var(--vela);">
      <h3 class="f-display text-base mb-3" style="color: var(--vela);">Ambiente · Higüey (Casa de Retiro)</h3>
      <ul class="text-sm space-y-2 list-disc list-inside">
        <template x-for="item in data.salud.ambiente_higuey" :key="item">
          <li x-text="item"></li>
        </template>
      </ul>
    </div>
  </div>
</section>

<!-- TAB: Lazos -->
<section x-show="activeTab === 'lazos'" x-transition>
  <h2 class="section-title">Lazos</h2>
  <p class="section-sub">Matrimonios, noviazgos y núcleos familiares dentro del equipo.</p>

  <div class="bg-pergamino-claro border border-rule p-5 mb-6">
    <p class="text-sm text-tinta-suave"><strong>Implicación operativa:</strong> 18 de 39 personas (46%) están conectadas por familia o pareja con otra del equipo. Considerar al asignar áreas: separar parejas, distribuir familias.</p>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div class="bg-vela border border-rule p-5">
      <h3 class="f-display text-base text-tierra-honda mb-3">💍 Matrimonio dentro del equipo</h3>
      <template x-for="par in data.relaciones.matrimonios" :key="par[0]">
        <p class="text-sm" x-text="par[0] + ' ↔ ' + par[1]"></p>
      </template>
    </div>

    <div class="bg-vela border border-rule p-5">
      <h3 class="f-display text-base text-tierra-honda mb-3">💑 Noviazgos</h3>
      <ul class="text-sm space-y-1">
        <template x-for="par in data.relaciones.noviazgos" :key="par[0]">
          <li x-text="par[0] + ' ↔ ' + par[1]"></li>
        </template>
      </ul>
    </div>

    <div class="bg-vela border border-rule p-5 md:col-span-2">
      <h3 class="f-display text-base text-tierra-honda mb-3">👪 Núcleos familiares</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <template x-for="fam in data.relaciones.familias" :key="fam.nombre">
          <div class="border-l-2 border-cuero pl-3">
            <div class="f-cond uppercase tracking-widest text-xs text-cuero" x-text="fam.nombre"></div>
            <div class="text-sm mt-1">
              <template x-for="m in fam.miembros" :key="m">
                <div x-text="'· ' + m"></div>
              </template>
            </div>
            <div class="text-xs italic text-muted mt-2" x-text="fam.tipo"></div>
          </div>
        </template>
      </div>
    </div>
  </div>
</section>

<!-- TAB: Cartas náuticas (banderas) -->
<section x-show="activeTab === 'cartas'" x-transition>
  <h2 class="section-title">Cartas náuticas</h2>
  <p class="section-sub">Banderas operativas · advertencias y acciones recomendadas.</p>

  <div class="bg-vela border border-rule overflow-x-auto">
    <table class="text-sm">
      <thead>
        <tr>
          <th class="w-12">#</th>
          <th>Bandera</th>
          <th>Persona</th>
          <th>Acción</th>
          <th>Responsable</th>
        </tr>
      </thead>
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

<!-- TAB: Invitados y vituallas -->
<section x-show="activeTab === 'invitados'" x-transition>
  <h2 class="section-title">Invitados y vituallas</h2>
  <p class="section-sub">Quién invitó a quién, y el plan de recaudación según el equipo.</p>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div>
      <h3 class="f-display text-base text-tierra-honda mb-3">Invitados ya propuestos</h3>
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
      <h3 class="f-display text-base text-tierra-honda mb-3">Propuestas de recaudación</h3>
      <div class="bg-vela border border-rule p-4 text-sm">
        <table class="text-sm">
          <thead>
            <tr><th>Propuesta</th><th class="text-right">Menciones</th></tr>
          </thead>
          <tbody>
            <template x-for="r in data.recaudacion.top" :key="r.propuesta">
              <tr>
                <td x-text="r.propuesta"></td>
                <td class="text-right f-display text-tierra-honda" x-text="r.menciones"></td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <div class="bg-pergamino-claro border border-rule p-4 mt-4 text-sm space-y-3">
        <p class="italic">"<span x-text="data.recaudacion.cita_franklin"></span>" <span class="f-cond text-xs uppercase tracking-widest text-cuero">— Franklin</span></p>
        <p class="italic">"<span x-text="data.recaudacion.cita_jordelis"></span>" <span class="f-cond text-xs uppercase tracking-widest text-cuero">— Jordelis</span></p>
      </div>
    </div>
  </div>
</section>

</main>

<!-- Modal ficha persona -->
<div x-show="selected" @click.self="selected = null" class="modal-overlay" x-transition x-cloak>
  <div class="modal-content" x-show="selected">
    <div class="modal-close" @click="selected = null">✕</div>
    <template x-if="selected">
      <div>
        <div class="flex items-start gap-4 mb-4">
          <div class="avatar" :class="selected.sexo" x-text="initials(selected.nombre)" style="width:64px; height:64px; font-size:18px;"></div>
          <div class="flex-1">
            <div class="f-display text-xl text-tinta" x-text="selected.nombre"></div>
            <div class="flex flex-wrap gap-2 mt-2">
              <span class="parche" x-text="selected.rol"></span>
              <span class="f-mono text-xs text-muted" x-text="selected.sexo + ' · ' + selected.edad + ' años · cumple ' + formatCumple(selected)"></span>
            </div>
            <div class="f-mono text-xs text-muted mt-1" x-text="'ETC ' + selected.etc_propio + (selected.etc_anio_propio ? ' (' + selected.etc_anio_propio + ')' : '') + ' · ' + selected.etcs_servidos + ' ETCs servidos · ' + selected.residencia"></div>
          </div>
          <div class="cartucho" :class="cartuchoEtcsClass(selected.etcs_servidos)">
            <div class="text-center leading-none">
              <div class="text-lg" x-text="selected.etcs_servidos"></div>
              <div style="font-size:8px; opacity:0.8; margin-top:2px;">ETCs</div>
            </div>
          </div>
        </div>

        <div class="flex gap-2 mb-5">
          <a class="btn-action btn-wa" :href="waLink(selected.telefono)" target="_blank">WhatsApp</a>
          <a class="btn-action" :href="'tel:+' + selected.telefono">Llamar</a>
          <span class="ml-auto f-mono text-xs text-muted" x-text="'Tel: +' + selected.telefono"></span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Talla</div>
            <div x-text="selected.talla || '—'"></div>
          </div>
          <div>
            <div class="f-cond uppercase tracking-widest text-xs text-muted">¿Invita?</div>
            <div x-text="selected.invita || '—'"></div>
          </div>
          <div class="md:col-span-2">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Palabra con la que llega</div>
            <div class="f-script text-xl text-tierra-honda" x-text="(selected.palabra || '—').trim()"></div>
          </div>
          <div class="md:col-span-2">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Qué espera vivir</div>
            <div x-text="selected.que_espera || '—'"></div>
          </div>
          <div class="md:col-span-2">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Miedos / resistencias</div>
            <div x-text="selected.miedos || '—'"></div>
          </div>
          <div class="md:col-span-2">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Tema que Dios trabaja</div>
            <div x-text="selected.tema_dios || '—'"></div>
          </div>
          <div>
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Alergias</div>
            <div x-text="selected.alergias || 'Ninguna'"></div>
          </div>
          <div>
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Condiciones</div>
            <div x-text="selected.condiciones || 'Ninguna'"></div>
          </div>
          <div>
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Medicamentos</div>
            <div x-text="selected.medicamentos || 'Ninguno'"></div>
          </div>
          <div>
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Contacto emergencia</div>
            <div class="whitespace-pre-line" x-text="selected.contacto_emergencia || '—'"></div>
          </div>
          <div class="md:col-span-2" x-show="selected.dudas">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Dudas / inquietudes</div>
            <div x-text="selected.dudas"></div>
          </div>
          <div class="md:col-span-2" x-show="selected.algo_directores">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Para los directores</div>
            <div x-text="selected.algo_directores"></div>
          </div>
          <div class="md:col-span-2" x-show="selected.invitados && selected.invitados.length">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Invitados que propone</div>
            <ul class="list-disc list-inside">
              <template x-for="inv in selected.invitados" :key="inv.nombre">
                <li x-text="inv.nombre + ' · ' + inv.edad + ' · ' + inv.relacion"></li>
              </template>
            </ul>
          </div>
          <div class="md:col-span-2" x-show="vinculosDe(selected.nombre).length">
            <div class="f-cond uppercase tracking-widest text-xs text-muted">Vínculos en el equipo</div>
            <ul class="list-disc list-inside">
              <template x-for="v in vinculosDe(selected.nombre)" :key="v">
                <li x-text="v"></li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    </template>
  </div>
</div>

<!-- Footer -->
<footer class="bg-mar-honda mt-12 py-8 text-center" style="color: rgba(247,239,217,0.85);">
  <div class="f-script text-3xl text-ambar mb-2">siempre amigos</div>
  <div class="f-mono text-xs tracking-widest mb-1" style="color: rgba(247,239,217,0.6);">
    ETC LXXXVIII · TRIPULACIÓN PARA UNA EXPEDICIÓN
  </div>
  <div class="f-mono text-[10px] tracking-widest" style="color: rgba(247,239,217,0.4);">
    Datos · <span x-text="data.meta.version"></span> · <span x-text="data.equipo.length"></span> tripulantes registrados
  </div>
</footer>

<script>
const DATA = __DATA_JSON__;

function app() {
  return {
    data: DATA,
    activeTab: 'tripulacion',
    tabs: [
      {id:'tripulacion', label:'Tripulación'},
      {id:'bitacora', label:'Bitácora'},
      {id:'travesia', label:'Travesía'},
      {id:'salud', label:'Botiquín & rancho'},
      {id:'lazos', label:'Lazos'},
      {id:'cartas', label:'Cartas náuticas'},
      {id:'invitados', label:'Invitados & vituallas'},
    ],
    search: '',
    filterArea: '',
    filterSexo: '',
    filterResidencia: '',
    filterVeterania: '',
    selected: null,
    chartsInit: false,

    get filteredEquipo() {
      const s = (this.search || '').toLowerCase().trim();
      return this.data.equipo.filter(p => {
        if (s && !p.nombre.toLowerCase().includes(s)) return false;
        if (this.filterArea && p.area !== this.filterArea) return false;
        if (this.filterSexo && p.sexo !== this.filterSexo) return false;
        if (this.filterResidencia && p.residencia !== this.filterResidencia) return false;
        if (this.filterVeterania) {
          const e = p.etcs_servidos;
          if (this.filterVeterania === '0' && e !== 0) return false;
          if (this.filterVeterania === '1' && e !== 1) return false;
          if (this.filterVeterania === '2-4' && !(e >= 2 && e <= 4)) return false;
          if (this.filterVeterania === '5+' && e < 5) return false;
        }
        return true;
      });
    },

    initials(name) {
      return name.split(/\\s+/).slice(0,2).map(w => w[0] ? w[0].toUpperCase() : '').join('');
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

    stripClass(p) {
      if (p.area === 'directores') return 'director-strip';
      if (p.area === 'asesores') return 'asesor-strip';
      if (p.rol && p.rol.toLowerCase().includes('coord')) return '';
      return 'opacity-0';
    },

    cartuchoEtcsClass(n) {
      if (n === 0) return 'cartucho-cuero';
      if (n <= 2) return 'cartucho-safari';
      if (n <= 4) return '';
      if (n <= 7) return 'cartucho-tierra';
      return 'cartucho-mar';
    },

    countSexo(s) { return this.data.equipo.filter(p => p.sexo === s).length; },
    countRookies() { return this.data.equipo.filter(p => p.etcs_servidos <= 1).length; },
    countVeteranos() { return this.data.equipo.filter(p => p.etcs_servidos >= 5).length; },
    countTallas() {
      const c = {};
      this.data.equipo.forEach(p => { if (p.talla) c[p.talla.toUpperCase().trim()] = (c[p.talla.toUpperCase().trim()] || 0) + 1; });
      const order = ['XS','S','M','L','XL','XXL'];
      const out = {};
      order.forEach(t => { if (c[t]) out[t] = c[t]; });
      return out;
    },

    vinculosDe(nombre) {
      const out = [];
      this.data.relaciones.matrimonios.forEach(par => {
        if (par[0] === nombre) out.push('💍 Esposa/o: ' + par[1]);
        else if (par[1] === nombre) out.push('💍 Esposa/o: ' + par[0]);
      });
      this.data.relaciones.noviazgos.forEach(par => {
        if (par[0] === nombre) out.push('💑 Pareja: ' + par[1]);
        else if (par[1] === nombre) out.push('💑 Pareja: ' + par[0]);
      });
      this.data.relaciones.familias.forEach(fam => {
        if (fam.miembros.includes(nombre)) {
          const otros = fam.miembros.filter(m => m !== nombre);
          out.push('👪 ' + fam.nombre + ': ' + otros.join(', ') + ' (' + fam.tipo + ')');
        }
      });
      return out;
    },

    get mesesProceso() {
      const meses = [
        {m:6, nombre:'Junio'}, {m:7, nombre:'Julio'},
        {m:8, nombre:'Agosto'}, {m:9, nombre:'Septiembre'},
      ];
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
            items.push({
              key: 'c-' + p.id,
              fecha: p.cumple_dia,
              fechaTxt: String(p.cumple_dia).padStart(2,'0') + '-' + mesesNombres[mz.m-1],
              eventoClass: '',
              contenido: '<span class="cumple-chip">🎂</span> <span class="f-script text-lg text-tierra-honda">' + p.nombre + '</span> · <span class="text-muted text-xs">cumple ' + ((new Date().getFullYear()) - p.cumple_anio) + ' (' + p.rol + ')</span>'
            });
          }
        });
        items.sort((a,b) => a.fecha - b.fecha);
        return { ...mz, items };
      });
    },

    openModal(p) { this.selected = p; },

    initCharts() {
      if (this.chartsInit) return;
      this.chartsInit = true;
      const colors = {
        pergamino: '#E8D2A1', tierra: '#B25028', mar: '#1B3A52',
        safari: '#4A5D2E', ambar: '#C57920', cuero: '#6B4423', muted: '#7A6440'
      };
      const palette = [colors.tierra, colors.mar, colors.safari, colors.ambar, colors.cuero, colors.muted];
      const fontFamily = "'Lora', serif";

      // Residencia
      const resCount = {};
      this.data.equipo.forEach(p => resCount[p.residencia] = (resCount[p.residencia] || 0) + 1);
      new Chart(document.getElementById('chart-residencia'), {
        type: 'doughnut',
        data: { labels: Object.keys(resCount), datasets: [{ data: Object.values(resCount), backgroundColor: palette, borderColor: '#F7EFD9', borderWidth: 2 }] },
        options: { plugins: { legend: { position: 'right', labels: { font: { family: fontFamily, size: 11 } } } } }
      });

      // Veteranía
      let rook=0, m1=0, m24=0, v5=0;
      this.data.equipo.forEach(p => {
        if (p.etcs_servidos === 0) rook++;
        else if (p.etcs_servidos === 1) m1++;
        else if (p.etcs_servidos >= 2 && p.etcs_servidos <= 4) m24++;
        else v5++;
      });
      new Chart(document.getElementById('chart-veterania'), {
        type: 'bar',
        data: { labels: ['0 (rookies)','1','2-4','5+'], datasets: [{ data: [rook,m1,m24,v5], backgroundColor: [colors.cuero, colors.safari, colors.mar, colors.tierra] }] },
        options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { font: { family: fontFamily } } }, x: { ticks: { font: { family: fontFamily } } } } }
      });

      // Edad histogram
      const ages = this.data.equipo.filter(p => p.edad).map(p => p.edad);
      const bins = [[18,21,'18-21'],[22,25,'22-25'],[26,29,'26-29'],[30,34,'30-34'],[35,99,'35+']];
      const ageCount = bins.map(([lo,hi,l]) => ages.filter(a => a>=lo && a<=hi).length);
      new Chart(document.getElementById('chart-edad'), {
        type: 'bar',
        data: { labels: bins.map(b => b[2]), datasets: [{ data: ageCount, backgroundColor: colors.ambar }] },
        options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { font: { family: fontFamily } } }, x: { ticks: { font: { family: fontFamily } } } } }
      });

      // Área
      const areaCount = {};
      this.data.equipo.forEach(p => areaCount[p.area] = (areaCount[p.area] || 0) + 1);
      const areaLabels = { directores:'Directores', asesores:'Asesores', guias:'Guías', cocina:'Cocina', musica:'Música', por_asignar:'Por asignar' };
      new Chart(document.getElementById('chart-area'), {
        type: 'bar',
        data: {
          labels: Object.keys(areaCount).map(k => areaLabels[k] || k),
          datasets: [{ data: Object.values(areaCount), backgroundColor: palette }]
        },
        options: { indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { font: { family: fontFamily } } }, y: { ticks: { font: { family: fontFamily } } } } }
      });

      // ETC de origen
      const etcCount = {};
      this.data.equipo.forEach(p => { if (p.etc_propio) etcCount[p.etc_propio] = (etcCount[p.etc_propio] || 0) + 1; });
      const sortedEtcs = Object.keys(etcCount).map(Number).sort((a,b) => a-b);
      new Chart(document.getElementById('chart-etc-origen'), {
        type: 'bar',
        data: { labels: sortedEtcs.map(n => 'ETC ' + n), datasets: [{ data: sortedEtcs.map(n => etcCount[n]), backgroundColor: colors.mar }] },
        options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { font: { family: fontFamily }, stepSize: 1 } }, x: { ticks: { font: { family: fontFamily }, maxRotation: 45 } } } }
      });
    },

    init() {
      this.$watch('activeTab', val => {
        if (val === 'bitacora') this.$nextTick(() => this.initCharts());
      });
    }
  };
}
</script>
</body>
</html>
'''

# Inject JSON
output = HTML.replace('__DATA_JSON__', data_str)

with open('/home/user/ETC88/index.html', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Wrote /home/user/ETC88/index.html ({len(output)} bytes)")
