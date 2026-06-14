#!/usr/bin/env python3
"""Genera versiones LIMPIAS para Google Drive (text/plain -> Google Doc, text/csv ->
Google Sheet) SIN sintaxis markdown, porque Google escapa el markdown de text/plain
(\\#, \\-, \\[ ]). Reglas: encabezados en MAYÚSCULA, viñetas con '•', etiquetas con
'(PROPUESTA)'/'(POR DEFINIR)' (los corchetes [] se escapan), nada de # - * | = ` _ [ ].

Lee SOLO de data/equipo.json + data/estado.json.
Salidas en /tmp para subir con el MCP de Drive:
  /tmp/drive_asesores.txt · /tmp/drive_carpeta.txt · /tmp/drive_equipo.csv · /tmp/drive_finanzas.csv
"""
import json, re, csv, io

REPO = '/home/user/ETC88'
D = json.load(open(f'{REPO}/data/equipo.json'))
EST = D['estado']

def _v(n): return n['valor'] if isinstance(n, dict) and 'valor' in n else n
def tag(n):
    st = n.get('estado') if isinstance(n, dict) else None
    return {'propuesta': '(PROPUESTA) ', 'pendiente': '(POR DEFINIR) '}.get(st, '')
def denum(s):
    """'1. Título' -> '1 · Título' (el 'N.' al inicio lo escapa Google como lista)."""
    return re.sub(r'^(\s*)(\d+)\.\s+', r'\1\2 · ', s)

def clean(t):
    """Quita lo que Google escaparía y normaliza (#, **, *, [], `)."""
    t = t.replace('**', '').replace('`', '')
    t = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\1', t)   # *cursiva* -> cursiva
    t = t.replace('[', '(').replace(']', ')')
    t = t.replace('#', '')                             # '#' Google lo escapa siempre
    t = re.sub(r'[ ]{2,}', ' ', t)
    return t.strip()

L = []
def line(s=''): L.append(s)
def head(s): line(); line(denum(s).upper()); line()
def bullet(s): line('   •  ' + clean(s))

# ============================= DOC 1 · ASESORES =============================
ret = EST['retiro']
line('DOCUMENTO DE ASESORES · ETC 88')
line(f"{_v(ret['fechas'])} · {_v(ret['lugar'])}")
line('Co-dirección: ' + ' y '.join(_v(ret['co_direccion'])))
line()
line('Cómo leer: lo que no lleva marca está CONFIRMADO. (PROPUESTA) = sugerencia sin')
line('decidir. (POR DEFINIR) = falta el dato. Generado desde data/estado.json + equipo.json.')

head('1. El equipo del ETC 88')
op = [x for x in D['equipo'] if x.get('operativo')]
line(f"{len(op)} servidores operativos + asesores ampliados y transversales.")
AREAS = [('directores', 'Directores'), ('asesores', 'Asesores'),
         ('asesores_espirituales', 'Asesores Espirituales (transversales)'),
         ('guias', 'Guías'), ('cocina', 'Cocina'), ('musica', 'Música')]
for area, label in AREAS:
    ms = [x for x in D['equipo'] if x['area'] == area and x.get('operativo')
          and not x.get('vacante') and not x.get('backup')]
    if not ms: continue
    ms.sort(key=lambda x: (0 if 'coord' in x['rol'].lower() else 1, x['nombre']))
    line(); line(f"{label} ({len(ms)})")
    for x in ms:
        bullet(f"{x['nombre'].replace(' (sin formulario)','')} · {x['rol']}")
vac = [x for x in D['equipo'] if x.get('vacante')]
bks = [x for x in D['equipo'] if x.get('backup')]
ac  = [x for x in D['equipo'] if x['area'] == 'asesores_cocina']
ad  = [x for x in D['equipo'] if x['area'] == 'asesores_diocesanos']
line(); line('Vacantes, backups y asesores externos')
for x in vac: bullet('(POR DEFINIR) ' + x['nombre'])
if bks: bullet('Backups (no son parte del equipo per se): ' + ' · '.join(x['nombre'] for x in bks))
if ac: bullet('Asesoras de cocina: ' + ' · '.join(x['nombre'] for x in ac))
if ad: bullet('Asesores de comunidad: ' + ' · '.join(x['nombre'] for x in ad))

head('2. Cronograma 2026')
MESES = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
for e in D['calendario']:
    try:
        y, m, dd = e['fecha'].split('-'); fecha = f"{int(dd)}-{MESES[int(m)-1]}"
    except Exception:
        fecha = e['fecha']
    bullet(f"{fecha} — {e['titulo']}" + (' (sin formación)' if e.get('sin_formacion') else ''))

head('3. Finanzas (resumen)')
ef = EST['finanzas']
def fin(label, node, fmt=lambda v: f"RD${v:,}"):
    nota = f" — {node['nota']}" if isinstance(node, dict) and node.get('nota') else ''
    bullet(f"{label}: {tag(node)}{fmt(_v(node))}{nota}")
fin('Casa por persona (sin exención)', ef['casa_por_persona_sin_exencion'])
fin('Casa por persona (con exención)', ef['casa_por_persona_con_exencion'])
fin('Deuda inicial al Consejo', ef['deuda_inicial'])
fin('Cuota de participante', ef['cuota_participante'])
cq = ef['cuota_equipo']
_cv = _v(cq)
_tot = _cv.get('total') if isinstance(_cv, dict) else _cv
_tot = _cv.get('total_rango', _tot) if isinstance(_cv, dict) else _tot
_mens = _cv.get('mensual') if isinstance(_cv, dict) else None
_cubre = _cv.get('cubre', '') if isinstance(_cv, dict) else ''
bullet(f"Cuota del equipo: {tag(cq)}${_tot} total" +
       (f" · ${_mens}/mes" if _mens else '') +
       (f" · cubre {_cubre}" if _cubre else '') +
       f" — {cq['nota']}")
fin('Meta de recaudación', ef['meta_recaudacion_total'])
fin('Personas en la casa (piso)', ef['personas_casa_piso'], fmt=lambda v: str(v))
fin('Participantes (objetivo)', ef['participantes_objetivo'], fmt=lambda v: str(v))

head('4. Recaudación')
er = EST['recaudacion']
mod = er['modelo']
bullet(f"Modelo: {_v(mod)} — {mod['nota']}")
bullet('Profondo #1, Profondo #2 y donaciones: montos variables (lo que se recaude); cubren la brecha = costo − cuotas.')
bullet('Profondo #1 = primera actividad de recaudación (formato por definir por el director). Donaciones a empresas/particulares = responsabilidad de los Directores (delegable).')

head('5. Equipos auxiliares')
for a in D['equipos_auxiliares']:
    rt = {'pendiente': '(POR DEFINIR) ', 'propuesta': '(PROPUESTA) '}.get(a.get('responsable_estado'), '')
    bullet(f"{a['nombre']}: {a['descripcion']} Responsable: {rt}{a['responsable_sugerido']}.")

head('6. Decisiones confirmadas')
for d in EST['decisiones_confirmadas']: bullet(d)
head('7. Pendientes (decisiones tuyas — no las invento)')
for d in EST['pendientes']: bullet('(POR DEFINIR) ' + d)

head('8. Alertas clave de salud y convivencia')
sal = D.get('salud', {})
al = sal.get('alergias_alimentarias', {})
if al: bullet('Alergias alimentarias: ' + ' · '.join(f"{k} ({len(v)})" for k, v in al.items()))
for amb in sal.get('ambiente_higuey', []): bullet(amb)
line(); line('Generado automáticamente desde los datos. No editar a mano: cambiar los datos y regenerar.')

open('/tmp/drive_asesores.txt', 'w', encoding='utf-8').write('\n'.join(L))

# ============================= DOC 2 · CARPETA =============================
def md_to_plain(md):
    out = []
    for raw in md.split('\n'):
        s = raw.rstrip()
        st = s.strip()
        if st.startswith('|') and set(st) <= set('|-: '):
            continue  # separador de tabla
        if st.startswith('|'):
            cells = [clean(c) for c in st.strip('|').split('|')]
            out.append('   •  ' + ' — '.join(c for c in cells if c))
            continue
        if st.startswith('#'):
            out.append(''); out.append(denum(clean(st.lstrip('#').strip())).upper()); out.append('')
        elif st == '---':
            out.append('')
        elif st.startswith('>'):
            body = clean(st.lstrip('>').strip())
            if body: out.append('   ' + body)
        elif re.match(r'^[-*]\s', st):
            out.append('   •  ' + clean(re.sub(r'^[-*]\s', '', st)))
        elif re.match(r'^\d+\.\s', st):
            out.append('   •  ' + clean(re.sub(r'^\d+\.\s', '', st)))
        else:
            out.append(clean(st))
    return '\n'.join(out)

C = []
C.append('CARPETA (F1) · ETC 88')
C.append(f"{_v(ret['fechas'])} · {_v(ret['lugar'])}")
C.append('')
for fn in ['GUIA_ETC88.md', 'GUIA_DE_GUIAS_88.md', 'ANEXO_COCINA_88.md']:
    import os
    if os.path.exists(f'{REPO}/{fn}'):
        C.append(md_to_plain(open(f'{REPO}/{fn}', encoding='utf-8').read()))
        C.append('')
        C.append('· · ·')
        C.append('')
open('/tmp/drive_carpeta.txt', 'w', encoding='utf-8').write('\n'.join(C))

# ============================= HOJA · EQUIPO (csv) =========================
AREA_LABEL = {'directores': 'Directores', 'asesores': 'Asesores',
              'asesores_espirituales': 'Asesores Espirituales', 'asesores_cocina': 'Asesoras Cocina',
              'asesores_diocesanos': 'Asesores Comunidad', 'guias': 'Guías', 'cocina': 'Cocina',
              'musica': 'Música'}
buf = io.StringIO(); w = csv.writer(buf)
w.writerow(['Nombre', 'Área', 'Rol', 'Sexo', 'Edad', 'Comunidad', 'Operativo'])
ORD = {'directores': 0, 'asesores': 1, 'asesores_espirituales': 2, 'guias': 3,
       'cocina': 4, 'musica': 5, 'asesores_cocina': 6, 'asesores_diocesanos': 7}
for x in sorted(D['equipo'], key=lambda p: (ORD.get(p['area'], 9), 0 if 'coord' in p['rol'].lower() else 1, p['nombre'])):
    w.writerow([x['nombre'].replace(' (sin formulario)', ''), AREA_LABEL.get(x['area'], x['area']),
                x['rol'], x.get('sexo', ''), x.get('edad', '') or '', x.get('comunidad', ''),
                'Sí' if x.get('operativo') else 'No'])
w.writerow([])
w.writerow(['NOTA: contacto completo (teléfono, talla, salud) en Equipo_ETC88.xlsx (repo).'])
open('/tmp/drive_equipo.csv', 'w', encoding='utf-8').write(buf.getvalue())

# ============================= HOJA · FINANZAS (csv) ======================
buf = io.StringIO(); w = csv.writer(buf)
w.writerow(['Concepto', 'Monto (RD$)', 'Estado', 'Nota'])
def frow(label, node, fmt=lambda v: v):
    st = {'confirmado': 'Confirmado', 'propuesta': 'PROPUESTA', 'pendiente': 'POR DEFINIR'}.get(
        node.get('estado') if isinstance(node, dict) else '', '')
    w.writerow([label, fmt(_v(node)), st, (node.get('nota', '') if isinstance(node, dict) else '')])
frow('Casa por persona (sin exención)', ef['casa_por_persona_sin_exencion'])
frow('Casa por persona (con exención)', ef['casa_por_persona_con_exencion'])
frow('Deuda inicial al Consejo', ef['deuda_inicial'])
frow('Cuota de participante', ef['cuota_participante'])
_cv2 = _v(cq)
_tot2 = _cv2.get('total') or _cv2.get('total_rango', '—')
_mens2 = _cv2.get('mensual')
_cuota_str = f"{_tot2}" + (f" ({_mens2}/mes)" if _mens2 else "")
_estado2 = cq.get('estado', '').upper() or 'PROPUESTA'
w.writerow(['Cuota del equipo', _cuota_str, _estado2, cq['nota']])
frow('Meta de recaudación (= costo total)', ef['meta_recaudacion_total'])
frow('Personas en la casa (piso)', ef['personas_casa_piso'])
frow('Participantes (objetivo)', ef['participantes_objetivo'])
w.writerow(['Profondo #1 / Profondo #2 / donaciones', 'variable', 'VARIABLE', 'Cubren la brecha (costo − cuotas); lo que se recaude. Profondo #1 = primera actividad, formato por definir.'])
w.writerow([])
w.writerow(['NOTA: el presupuesto itemizado completo (12 pestañas) está en Finanzas_ETC88.xlsx (repo).', '', '', ''])
open('/tmp/drive_finanzas.csv', 'w', encoding='utf-8').write(buf.getvalue())

import os
for f in ['drive_asesores.txt', 'drive_carpeta.txt', 'drive_equipo.csv', 'drive_finanzas.csv']:
    print(f"  /tmp/{f}: {os.path.getsize('/tmp/'+f)} bytes")
