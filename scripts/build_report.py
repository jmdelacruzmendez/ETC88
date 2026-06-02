#!/usr/bin/env python3
"""Generate dimensional report (MD) of the ETC 88 team."""
import json
from collections import Counter

with open('/tmp/etc88_data.json') as f:
    d = json.load(f)

eq_all = d['equipo']
eq = [p for p in eq_all if p.get('operativo')]  # solo operativos para el análisis principal
eq_no_op = [p for p in eq_all if not p.get('operativo')]

def pct(n, t): return f"{n/t*100:.0f}%" if t else "—"

def stats(people):
    n = len(people)
    confirmados = [p for p in people if not p.get('sin_formulario')]
    nc = len(confirmados)
    sf = n - nc
    out = {'n': n, 'confirmados': nc, 'sin_form': sf}
    # Sexo
    f = sum(1 for p in confirmados if p['sexo'] == 'F')
    m = sum(1 for p in confirmados if p['sexo'] == 'M')
    out['F'] = f
    out['M'] = m
    out['F_pct'] = pct(f, nc)
    out['M_pct'] = pct(m, nc)
    # Comunidad
    belen = sum(1 for p in confirmados if p['comunidad'] == 'Belén')
    beta = sum(1 for p in confirmados if p['comunidad'] == 'Betania')
    out['belen'] = belen
    out['beta'] = beta
    out['belen_pct'] = pct(belen, nc)
    out['beta_pct'] = pct(beta, nc)
    # Veteranía
    rook = sum(1 for p in confirmados if p['etcs_servidos'] == 0)
    bz = sum(1 for p in confirmados if p['etcs_servidos'] == 1)
    med = sum(1 for p in confirmados if p['etcs_servidos'] is not None and 2 <= p['etcs_servidos'] <= 4)
    vet = sum(1 for p in confirmados if p['etcs_servidos'] is not None and p['etcs_servidos'] >= 5)
    out['rook'] = rook
    out['bz'] = bz
    out['med'] = med
    out['vet'] = vet
    out['rook_pct'] = pct(rook, nc)
    out['bz_pct'] = pct(bz, nc)
    out['med_pct'] = pct(med, nc)
    out['vet_pct'] = pct(vet, nc)
    # Edad
    edades = [p['edad'] for p in confirmados if p['edad']]
    out['edad_min'] = min(edades) if edades else '—'
    out['edad_max'] = max(edades) if edades else '—'
    out['edad_avg'] = round(sum(edades)/len(edades), 1) if edades else '—'
    # Residencia
    res = Counter(p['residencia'] for p in confirmados if p['residencia'] != '—')
    out['residencia'] = dict(res)
    # ETC propios
    etcs = [p['etc_propio'] for p in confirmados if p['etc_propio']]
    out['etc_min'] = min(etcs) if etcs else '—'
    out['etc_max'] = max(etcs) if etcs else '—'
    return out

def bar(label, parts, width=30):
    total = sum(p[1] for p in parts)
    if total == 0: return ''
    out = []
    for name, n, sym in parts:
        chars = int(n / total * width)
        out.append(sym * chars)
    return ''.join(out) + f" {label}"

teams = {
    'Directores': [p for p in eq if p['area'] == 'directores'],
    'Asesores':   [p for p in eq if p['area'] == 'asesores'],
    'Guías':      [p for p in eq if p['area'] == 'guias'],
    'Cocina':     [p for p in eq if p['area'] == 'cocina'],
    'Música':     [p for p in eq if p['area'] == 'musica'],
}

# Build MD
lines = []
lines.append("# Manifiesto de la Tripulación — ETC LXXXVIII")
lines.append("")
lines.append(f"**Versión:** {d['meta']['version']} · **Equipo operativo:** {d['meta']['operativos']} · **Ampliados (solo retiro):** {d['meta']['no_operativos']} · **Total en retiro:** {d['meta']['total_equipo']} · **Fecha:** 2026-06-02")
lines.append("")
lines.append("> *Cambios v4:* Fabelle = Fabelly → Cocina · Chantal → Cocina · 3 nuevas Cocina (Olanlly, Roselyn, Pamela) · Daylin Música pendiente form · **Nuevo bloque \"ampliados\":** Johany + Petra (asesoras cocina), Frank Morales (asesor laico), Paul + Sor Angelina (espirituales), 2 SD + 2 La Vega (diocesanos) · **3 equipos auxiliares** por formular: Donaciones, Guagua, Actividad Profondo.")
lines.append("")

# Total team summary
t = stats(eq)
lines.append("## Manifiesto general")
lines.append("")
lines.append(f"- **Total:** {t['n']} ({t['confirmados']} con formulario, {t['sin_form']} pendientes)")
lines.append(f"- **Sexo:** F = {t['F']} ({t['F_pct']}) · M = {t['M']} ({t['M_pct']})")
lines.append(f"- **Comunidad:** Belén = {t['belen']} ({t['belen_pct']}) · Betania = {t['beta']} ({t['beta_pct']})")
lines.append(f"- **Veteranía:** rookies (0) = {t['rook']} · biz (1) = {t['bz']} · intermedios (2-4) = {t['med']} · veteranos (5+) = {t['vet']}")
lines.append(f"- **Edad:** {t['edad_min']}–{t['edad_max']} años (promedio {t['edad_avg']})")
lines.append(f"- **Residencia:** " + " · ".join(f"{r}={n}" for r,n in t['residencia'].items()))
lines.append("")

# Per-team breakdown
for tname, members in teams.items():
    if not members: continue
    s = stats(members)
    lines.append(f"## {tname} ({s['n']})")
    lines.append("")
    if s['sin_form']:
        sin_form_names = [p['nombre'].replace(' (sin formulario)','') for p in members if p.get('sin_formulario')]
        lines.append(f"_Pendientes formulario:_ **{', '.join(sin_form_names)}**")
        lines.append("")
    coords = [p for p in members if 'Coord' in p.get('rol','')]
    if coords:
        lines.append(f"_Coordinadores:_ **{' · '.join(p['nombre'] for p in coords)}**")
        lines.append("")
    lines.append("| Dimensión | Distribución |")
    lines.append("|---|---|")
    lines.append(f"| Sexo (de {s['confirmados']} con form) | F = {s['F']} ({s['F_pct']}) · M = {s['M']} ({s['M_pct']}) |")
    lines.append(f"| Comunidad | Belén = {s['belen']} ({s['belen_pct']}) · Betania = {s['beta']} ({s['beta_pct']}) |")
    lines.append(f"| Veteranía | Rookies (0) = {s['rook']} · 1 ETC = {s['bz']} · 2-4 = {s['med']} · 5+ = {s['vet']} |")
    lines.append(f"| Edad | {s['edad_min']}-{s['edad_max']} años (avg {s['edad_avg']}) |")
    res_str = " · ".join(f"{r}={n}" for r,n in s['residencia'].items())
    lines.append(f"| Residencia | {res_str} |")
    lines.append(f"| ETC propio (cohorte) | {s['etc_min']} - {s['etc_max']} |")
    lines.append("")

    # Roster of this team
    lines.append("**Tripulantes:**")
    lines.append("")
    for p in members:
        flags = []
        if 'Coord' in p.get('rol',''): flags.append('★ Coord')
        if p.get('sin_formulario'): flags.append('⚠ sin form')
        if p.get('etc_propio'):
            flags.append(f"ETC {p['etc_propio']}")
        if p.get('etcs_servidos') is not None:
            flags.append(f"{p['etcs_servidos']} sv.")
        if p.get('sexo') in ['F','M']:
            flags.append(p['sexo'])
        if p.get('comunidad') and p['comunidad'] not in ['—','Por confirmar']:
            flags.append(p['comunidad'])
        if p.get('edad'):
            flags.append(f"{p['edad']}a")
        name_clean = p['nombre'].replace(' (sin formulario)','')
        lines.append(f"- **{name_clean}** — {' · '.join(flags)}")
    lines.append("")

# Especific insight for cocina (largest team)
lines.append("## Análisis: Equipo de Cocina")
lines.append("")
cocina = teams['Cocina']
c = stats(cocina)
cocina_conf = [p for p in cocina if not p.get('sin_formulario')]
n = len(cocina_conf)
lines.append(f"Cocina es el equipo más grande del retiro: **{c['n']} tripulantes** ({c['confirmados']} con formulario + {c['sin_form']} pendientes).")
lines.append("")
lines.append("### Balance interno (de los {} con formulario)".format(c['confirmados']))
lines.append("")
lines.append(f"- **Sexo:** F = {c['F']} ({c['F_pct']}) · M = {c['M']} ({c['M_pct']})")
if c['F'] / c['confirmados'] > 0.65:
    lines.append(f"  - ⚠️ Predominio femenino fuerte. {c['M']} hombres de {c['confirmados']} confirmados.")
elif c['M'] / c['confirmados'] > 0.65:
    lines.append(f"  - ⚠️ Predominio masculino fuerte.")
else:
    lines.append(f"  - ✓ Balance razonable.")
lines.append(f"- **Comunidad:** Belén = {c['belen']} ({c['belen_pct']}) · Betania = {c['beta']} ({c['beta_pct']})")
belen_pct = c['belen'] / c['confirmados'] if c['confirmados'] else 0
if belen_pct > 0.45:
    lines.append(f"  - ⚠️ Belén sobrerrepresentado vs el equipo total ({pct(t['belen'], t['confirmados'])} global).")
elif belen_pct < 0.10:
    lines.append(f"  - ⚠️ Pocos de Belén — considerar reforzar.")
else:
    lines.append(f"  - ✓ Reparto OK.")
lines.append(f"- **Veteranía:** Rookies (0 ETCs servidos) = {c['rook']} · 1 servicio = {c['bz']} · 2-4 = {c['med']} · 5+ = {c['vet']}")
rook_pct = (c['rook'] + c['bz']) / c['confirmados'] if c['confirmados'] else 0
if rook_pct > 0.55:
    lines.append(f"  - ⚠️ Cocina muy verde: {c['rook']+c['bz']} de {c['confirmados']} con 0-1 ETC servido. Reforzar veteranía si entran nuevos.")
elif rook_pct < 0.30:
    lines.append(f"  - ✓ Cocina experimentada.")
lines.append(f"- **Edad:** {c['edad_min']}-{c['edad_max']} años (avg {c['edad_avg']})")
lines.append("")

# Recommendation for sin_form additions
lines.append("### Recomendación para las 3 nuevas (Olanlly · Roselyn · Pamela)")
lines.append("")
lines.append("Con base en las proporciones actuales del equipo de Cocina:")
lines.append("")
if c['M'] / c['confirmados'] < 0.35:
    lines.append(f"- **Sexo:** priorizar **hombres** — Cocina actual tiene solo {c['M']} hombres ({c['M_pct']}). Subir el M a 6-7 ayudaría a balancear el carga física típica de cocina.")
else:
    lines.append(f"- **Sexo:** balance OK actual.")
if belen_pct < 0.30:
    lines.append(f"- **Comunidad:** priorizar **Belén** — solo {c['belen']} de {c['confirmados']} confirmados ({c['belen_pct']}).")
elif belen_pct > 0.50:
    lines.append(f"- **Comunidad:** priorizar **Betania** — Belén ya tiene {c['belen']} ({c['belen_pct']}).")
else:
    lines.append(f"- **Comunidad:** balance OK actual.")
if rook_pct > 0.50:
    lines.append(f"- **Veteranía:** priorizar **veteranas con experiencia previa en cocina** (2+ servicios). {c['rook']+c['bz']} de {c['confirmados']} actuales son rookies/biz.")
else:
    lines.append(f"- **Veteranía:** balance OK; pueden entrar rookies sin problema.")
lines.append("")
lines.append("### Alergias críticas ya presentes en Cocina")
lines.append("")
lines.append("- **Mariscos:** Ivanna ⚠️ (también está en Guías ahora, ojo si come en cocina)")
lines.append("- **Piña:** Wilka (ahora Guía), Candy, José Ángel (Música) — 3 alérgicos cubren todos los equipos")
lines.append("- **Huevo:** José Ángel")
lines.append("- **Canela:** Wilka")
lines.append("- **Gastritis severa:** Candy — comidas no irritantes")
lines.append("- **Diabetes:** Luisa (Guías) — horarios regulares")
lines.append("- **Presión alta:** María del Carmen (Cocina) — bajo sodio")
lines.append("")
lines.append("**Acción:** evitar que las 3 nuevas tripulantes aporten más alergias críticas que dupliquen las ya cubiertas.")
lines.append("")

# Insight cross-team
lines.append("## Análisis cruzado")
lines.append("")
lines.append("### Familias y parejas distribuidas por área")
lines.append("")
lines.append("| Núcleo | Áreas |")
lines.append("|---|---|")
lines.append("| **De la Cruz Méndez** (Jean Carlo, Juan Manuel, Paloma, Fabelle) | Directores ×2 · Cocina ×2 |")
lines.append("| **Fernández** (Camila, Laura) | Guías (coord) · Asesores |")
lines.append("| **Lorenzo** (Tomás, Victoria) | Asesores · Guías |")
lines.append("| **Santana Rosario** (Risaira, Risairi) | Cocina ×2 ⚠️ misma área |")
lines.append("| **Rodríguez Belliard** (Dorian, Darianny) | Música · Guías ✓ |")
lines.append("| **Dorian ↔ José Ángel** (matrimonio) | Música ×2 ⚠️ misma área |")
lines.append("| **Kelvin ↔ Brianelis** (noviazgo) | Cocina ×2 ⚠️ misma área |")
lines.append("| **Juan Manuel ↔ Yelaxni** (noviazgo) | Director · Guía ✓ |")
lines.append("| **Oliver ↔ Dayrelins** (noviazgo) | Guía · Cocina ✓ |")
lines.append("")
lines.append("**Flags por discutir:** Santana Rosario (hermanas en cocina), Dorian-José (matrimonio en música), Kelvin-Brianelis (noviazgo en cocina). Revisar si separar o si está OK por dinámica.")
lines.append("")

lines.append("### Comparativa de equipos")
lines.append("")
lines.append("| Equipo | n | F/M | Belén/Betania | Rookies+biz / Vet+ | Edad avg |")
lines.append("|---|---|---|---|---|---|")
for tname, members in teams.items():
    if not members: continue
    s = stats(members)
    if s['confirmados'] == 0: continue
    rookbz = s['rook'] + s['bz']
    vetplus = s['med'] + s['vet']
    lines.append(f"| {tname} | {s['n']} ({s['confirmados']}+{s['sin_form']}) | {s['F']}/{s['M']} | {s['belen']}/{s['beta']} | {rookbz}/{vetplus} | {s['edad_avg']} |")
lines.append("")

# Ampliados
lines.append("## Asesores ampliados (presentes en retiro, no operativos)")
lines.append("")
lines.append("Suman al equipo solo en el retiro · no participan de la formación semanal.")
lines.append("")
lines.append("| Nombre | Rol | Estado |")
lines.append("|---|---|---|")
for p in eq_no_op:
    nm = p['nombre']
    flag = '⚠ sin form' if p.get('sin_formulario') else ''
    lines.append(f"| {nm} | {p['rol']} | {flag} |")
lines.append("")

# Equipos auxiliares
lines.append("## Equipos auxiliares (por formular)")
lines.append("")
lines.append("Verticales paralelos al equipo operativo. Pueden integrar gente externa al equipo.")
lines.append("")
lines.append("| Equipo | Descripción | Responsable sugerido | Estado |")
lines.append("|---|---|---|---|")
for aux in d.get('equipos_auxiliares', []):
    lines.append(f"| **{aux['nombre']}** | {aux['descripcion']} | {aux['responsable_sugerido']} | {aux['estado']} |")
lines.append("")

lines.append("---")
lines.append("")
lines.append("*Fuente:* Formulario de preformación + xlsx ETC_88_1 (manifest) + actualizaciones del usuario 2-jun.")
lines.append(f"*Generado:* 2026-06-02 · {d['meta']['version']}")

with open('/home/user/ETC88/MANIFIESTO.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"Wrote MANIFIESTO.md ({sum(len(l) for l in lines)} chars, {len(lines)} lines)")
