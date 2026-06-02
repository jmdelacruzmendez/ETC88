import json
d = json.load(open('/tmp/etc88_data.json'))
eq = d['equipo']
M = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']

def cumple(p):
    return f"{p['cumple_dia']}-{M[p['cumple_mes']-1]}" if p.get('cumple_mes') else '—'

AREAS = [('directores','Directores'),('asesores','Asesores de Directores'),
         ('guias','Guías'),('cocina','Cocina'),('musica','Música')]
AMPL = [('asesores_espirituales','Asesores Espirituales'),
        ('asesores_cocina','Asesores de Cocina'),
        ('asesores_diocesanos','Asesores de Comunidad')]

L = []
L.append("ROSTER ETC 88 — ACTUALIZADO 2-jun-2026")
L.append("LXXXVIII edición nacional · Comunidad de San Pedro de Macorís «Caminos de Vida»")
L.append("Retiro: 4–6 septiembre 2026 · Casa de Retiro, Higüey · Co-Dir: Juan Manuel + Jean Carlo de la Cruz")
L.append("")
L.append("Documento generado automáticamente desde el Tablero de la Tripulación (v5).")
L.append("Reconcilia el Borrador de abril + Doc de Asesores 17-may + actualizaciones de junio.")
L.append("NO sustituye los documentos originales; es la foto del equipo a la fecha.")
L.append("")
op = [p for p in eq if p.get('operativo')]
noop = [p for p in eq if not p.get('operativo')]
L.append(f"RESUMEN: {len(eq)} en el manifiesto = {len(op)} operativos + {len(noop)} ampliados (solo retiro).")
fem = sum(1 for p in op if p['sexo']=='F'); mas = sum(1 for p in op if p['sexo']=='M')
bel = sum(1 for p in op if p['comunidad']=='Belén'); bet = sum(1 for p in op if p['comunidad']=='Betania')
L.append(f"Operativos: {fem} F / {mas} M · Belén {bel} / Betania {bet}.")
L.append("")
L.append("="*60)
L.append("EQUIPO OPERATIVO")
L.append("="*60)
for area, label in AREAS:
    ms = [p for p in eq if p['area']==area]
    if not ms: continue
    L.append("")
    L.append(f"{label} ({len(ms)})")
    for p in sorted(ms, key=lambda x: (0 if 'coord' in x['rol'].lower() else 1, x['nombre'])):
        star = '★ ' if 'coord' in p['rol'].lower() else '• '
        bits = [p['rol']]
        if p.get('etc_propio'): bits.append(f"ETC {p['etc_propio']}")
        if p.get('etcs_servidos') is not None: bits.append(f"{p['etcs_servidos']} sv.")
        if p.get('comunidad') and p['comunidad'] not in ('—','Por confirmar'): bits.append(p['comunidad'])
        if p.get('sin_formulario'): bits.append('SIN FORMULARIO')
        nm = p['nombre'].replace(' (sin formulario)','')
        L.append(f"  {star}{nm} — {' · '.join(bits)}")
L.append("")
L.append("="*60)
L.append("ASESORES AMPLIADOS (presentes en el retiro, no operativos)")
L.append("="*60)
for area, label in AMPL:
    ms = [p for p in eq if p['area']==area]
    if not ms: continue
    names = ', '.join(p['nombre'].replace(' (sin formulario)','') for p in ms)
    L.append(f"  {label}: {names}")
L.append("")
L.append("="*60)
L.append("CALENDARIO 2026 (actualizado)")
L.append("="*60)
for e in d['calendario']:
    flag = ' [SIN FORMACIÓN]' if e.get('sin_formacion') else ''
    L.append(f"  {e['fecha']} · {e['titulo']}{flag}")
L.append("")
L.append("="*60)
L.append("EQUIPOS AUXILIARES (por formular)")
L.append("="*60)
for a in d.get('equipos_auxiliares', []):
    L.append(f"  {a['nombre']} — {a['estado']} · resp. sugerido: {a['responsable_sugerido']}")
L.append("")
L.append("="*60)
L.append("PENDIENTE DE CONFIRMAR (al 2-jun)")
L.append("="*60)
L.append("  ROSTER:")
L.append("    • Guías del doc de mayo aún sin decidir (¿entran o se caen?): Scarlett Nivar, Rodolfo Telémaco, Dionis Sosa.")
L.append("    • Cocina del doc de mayo aún sin decidir: Emmanuel Mieses, Coraima Martínez, Neyrelis Santana, Randolph Joseph.")
L.append("    • Cupo varón en cocina (posible cambio de Roselyn): recomendados Néstor Vidal o Leandro Fernández (cocina ETC 85).")
L.append("    • Confirmar formularios pendientes: Daylin, Olanlly, Roselyn, Pamela.")
L.append("  ASESORES:")
L.append("    • Punta Cana: confirmar si envía asesor de comunidad.")
L.append("    • SPM: definir el asesor de comunidad faltante.")
L.append("  FINANZAS / ROADMAP (del Doc de Asesores):")
L.append("    • Profondo #2: definir actividad + meta (deadline 30-jun).")
L.append("    • Cierre nominal de padrinos (deadline 30-jul).")
L.append("    • Tema espiritual del retiro: lema + cita (deadline 31-may).")
L.append("")
L.append(f"— Fin · {d['meta']['version']} · generado del Tablero de la Tripulación.")

txt = "\n".join(L)
open('/tmp/roster_drive.txt','w').write(txt)
print(f"Wrote /tmp/roster_drive.txt ({len(txt)} chars, {len(L)} lines)")
print("="*60)
print(txt[:1200])
