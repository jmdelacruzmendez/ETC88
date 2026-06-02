#!/usr/bin/env python3
"""Apply v2 changes: new area structure, re-include Mary Carmen + Roberto,
add Daylin + vacantes, add comunidad field, remove Lazos."""
import openpyxl, json, re, os

REPO = '/home/user/ETC88'
# El xlsx fuente puede estar en el dir efímero de uploads o en la copia durable del repo.
# Se prefiere la copia del repo si la de uploads no existe (contenedor nuevo).
_XLSX_CANDIDATES = [
    '/root/.claude/uploads/2da4a2cd-be63-4d49-b615-cf5c7554c95e/93ed3347-Respuestas__Formulario_preformacio_n_ETC_88.xlsx',
    f'{REPO}/data/fuente_formulario.xlsx',
]
XLSX = next((p for p in _XLSX_CANDIDATES if os.path.exists(p)), _XLSX_CANDIDATES[-1])

MONTHS = {'enero':1,'ene':1,'febrero':2,'feb':2,'marzo':3,'mar':3,'abril':4,'abr':4,
          'mayo':5,'may':5,'junio':6,'jun':6,'julio':7,'jul':7,'agosto':8,'ago':8,
          'septiembre':9,'sept':9,'sep':9,'octubre':10,'oct':10,'noviembre':11,'nov':11,
          'diciembre':12,'dic':12}

GENDER = {
    'Jean Carlo De la Cruz Mendez':'M', 'Kelvin Alexis Ventura Santana':'M',
    'Juan Pablo Argüello Alzate':'M', 'Fernando Cordero':'M',
    'Oliver Rafael De León Ramírez':'M', 'Adrián Francisco Santana Puente':'M',
    'Franklin De Jesús Silverio Delgadillo':'M', 'José Ángel Tusen Russo':'M',
    'Leober Carrion Soriank':'M', 'Tommy Nova Nolasco':'M',
    'Juan Manuel de la Cruz Méndez':'M', 'Roberto Figueroa':'M',
    'Jonathan Andres Medina Mota':'M', 'Johnnito Richiez Brugal':'M',
    'Guido Mardonado':'M', 'Tomás Lorenzo':'M',
}

RESIDENCIA = {
    'Candy Elizabeth Gatwood Ramos':'Punta Cana',
    'Dorian Elina Rodriguez Belliard':'Punta Cana',
    'Jordelis Mateo':'Punta Cana',
    'José Ángel Tusen Russo':'Punta Cana',
    'Ivanna Marien Mercedes Sosa':'Punta Cana',
    'Tommy Nova Nolasco':'Punta Cana',
    'Yelaxni Mota':'Punta Cana',
    'Priscilla Hidalgo Pou':'Santo Domingo',
    'Juan Pablo Argüello Alzate':'Santo Domingo',
    'Camila Fernández Hazim':'Santo Domingo',
    'Ismarie Sthepanie Constanzo Ramos':'El Seibo / SPM',
    'Chantal Melissa Carpio Jiménez':'Higüey / SPM',
}

# v3 area assignments per xlsx ETC_88_1 manifest (2026-06-02)
# Fabelle = Fabelly → cocina; Chantal → cocina; Olanlly/Roselyn/Pamela = new cocina; total 45
AREA = {
    # Directores
    'Jean Carlo De la Cruz Mendez':       ('directores', 'Director'),
    'Juan Manuel de la Cruz Méndez':      ('directores', 'Director'),
    # Asesores
    'Laura Fernández':                     ('asesores', 'Asesora'),
    'Tomás Lorenzo':                       ('asesores', 'Asesor'),
    # Guías (14, Priscilla + Camila coords)
    'Priscilla Hidalgo Pou':              ('guias', 'Coord. Guía'),
    'Camila Fernández Hazim':             ('guias', 'Coord. Guía'),
    'Yelaxni Mota':                        ('guias', 'Guía'),
    'Ivanna Marien Mercedes Sosa':         ('guias', 'Guía'),
    'Juan Pablo Argüello Alzate':         ('guias', 'Guía'),
    'Victoria Lorenzo Rivera':            ('guias', 'Guía'),
    'Fernando Cordero':                   ('guias', 'Guía'),
    'Jonathan Andres Medina Mota':        ('guias', 'Guía'),
    'Oliver Rafael De León Ramírez':      ('guias', 'Guía'),
    'Wilka María Reyes Mota':              ('guias', 'Guía'),
    'Luisa Maria Fiorentino Brugal':      ('guias', 'Guía'),
    'Darianny Rodriguez Belliard':        ('guias', 'Guía'),
    'Jhonnalia Franchesca Silvestre Guzmán':('guias','Guía'),
    'Franklin De Jesús Silverio Delgadillo':('guias','Guía'),
    # Música (6, José coord)
    'José Ángel Tusen Russo':              ('musica', 'Coord. Música'),
    'Dorian Elina Rodriguez Belliard':     ('musica', 'Música'),
    'Ismarie Sthepanie Constanzo Ramos':   ('musica', 'Música'),
    'Leober Carrion Soriank':              ('musica', 'Música'),
    'Mary Carmen Ramírez Vásquez':         ('musica', 'Música'),
    'Daylin (sin formulario)':             ('musica', 'Música'),
    # Cocina (21 = 2 coords + 19, todas filas del xlsx)
    'Paloma Mendez':                       ('cocina', 'Coord. Cocina'),
    'Johnnito Richiez Brugal':             ('cocina', 'Coord. Cocina'),
    'Dayrelins Jazmin Santana Salas':      ('cocina', 'Cocina'),
    'Fabelle maciel fabian bello':         ('cocina', 'Cocina'),  # = Fabelly per user
    'Wirna Miguelina Stapleton Pilier':    ('cocina', 'Cocina'),
    'Jordelis Mateo':                      ('cocina', 'Cocina'),
    'Candy Elizabeth Gatwood Ramos':       ('cocina', 'Cocina'),
    'Kelvin Alexis Ventura Santana':       ('cocina', 'Cocina'),
    'Olanlly (sin formulario)':            ('cocina', 'Cocina'),  # NEW
    'Ambar Liz Jáquez Lebrón':             ('cocina', 'Cocina'),
    'Brianelis Abreu Calderón':            ('cocina', 'Cocina'),
    'Tommy Nova Nolasco':                  ('cocina', 'Cocina'),
    'Maria del Carmen Mejías Mateo':       ('cocina', 'Cocina'),
    'Risaira Santana Rosario':             ('cocina', 'Cocina'),
    'Adrián Francisco Santana Puente':     ('cocina', 'Cocina'),
    'Risairi Santana Rosario':             ('cocina', 'Cocina'),
    'Chantal Melissa Carpio Jiménez':      ('cocina', 'Cocina'),
    'Roberto Figueroa':                    ('cocina', 'Cocina'),
    'Guido Mardonado':                     ('cocina', 'Cocina'),
    'Pamela (sin formulario)':             ('cocina', 'Cocina'),  # NEW
    # Roselyn fuera (2-jun): su cupo pasa a un varón, candidato Randolph → 1 vacante abierta
}

def parse_bday(s):
    if not s: return (None, None)
    s = str(s).lower().strip()
    m = re.search(r'(\d{1,2})\s*de\s*([a-zé]+)(?:\s*(?:de(?:l)?\s*)?(\d{4}))?', s)
    if m:
        d, mo_w, y = int(m.group(1)), m.group(2), m.group(3)
        mo = MONTHS.get(mo_w)
        if mo: return ((mo, d), int(y) if y else None)
    m = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', s)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return ((b, a), y)
    return (None, None)

def parse_etcs_servidos(s):
    if s is None: return None
    s = str(s).strip().lower()
    if s in ['en ninguno','ninguno','ningunos','primera vez','en 0','en ningunos']: return 0
    m = re.match(r'^(\d+)', s)
    if m: return int(m.group(1))
    if 'desde el 2012' in s or 'desde 2012' in s: return 12
    if '10 a 12' in s or '10-12' in s: return 11
    if '5 o 6' in s or '5-6' in s: return 6
    if '8' in s and '2018' in s: return 8
    if 'una cocina dos guías' in s: return 3
    if 'en 1' in s or '1 solo' in s: return 1
    return None

def parse_etc_propio(s):
    if not s: return (None, None)
    s = str(s).strip()
    m = re.search(r'#?(\d{2,3})', s)
    num = int(m.group(1)) if m else None
    if num and num > 100:
        sn = str(num)
        if len(sn) == 6:
            num = int(sn[:2])
            return (num, int(sn[2:]))
    m_y = re.search(r'(20\d{2})', s)
    return (num, int(m_y.group(1)) if m_y else None)

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb['Form Responses 1']

equipo = []
for row in range(2, ws.max_row + 1):
    name = ws.cell(row=row, column=2).value
    if not name: continue
    name = name.strip()

    bday, byear = parse_bday(ws.cell(row=row, column=3).value)
    etc_num, etc_year = parse_etc_propio(ws.cell(row=row, column=7).value)
    etcs_servidos = parse_etcs_servidos(ws.cell(row=row, column=6).value)
    area, rol = AREA.get(name, ('por_asignar', 'Por asignar'))

    edad_raw = str(ws.cell(row=row, column=3).value or '')
    m_edad = re.search(r'(\d{2,3})\s*(?:años|-|—)', edad_raw)
    edad = int(m_edad.group(1)) if m_edad else None
    if not edad:
        m_edad = re.match(r'^\s*(\d{2})\s', edad_raw)
        if m_edad: edad = int(m_edad.group(1))

    comunidad = 'Belén' if etc_num == 85 else 'Betania'

    p = {
        'id': re.sub(r'[^a-z0-9]+','-', name.lower()).strip('-'),
        'nombre': name,
        'sexo': GENDER.get(name, 'F'),
        'edad': edad,
        'cumple_mes': bday[0] if bday else None,
        'cumple_dia': bday[1] if bday else None,
        'cumple_anio': byear,
        'etc_propio': etc_num,
        'etc_anio_propio': etc_year,
        'etcs_servidos': etcs_servidos,
        'residencia': RESIDENCIA.get(name, 'SPM'),
        'comunidad': comunidad,
        'area': area, 'rol': rol,
        'talla': ws.cell(row=row, column=5).value,
        'telefono': re.sub(r'\D', '', str(ws.cell(row=row, column=4).value or '')) or None,
        'que_espera': ws.cell(row=row, column=8).value,
        'miedos': ws.cell(row=row, column=9).value,
        'tema_dios': ws.cell(row=row, column=10).value,
        'invita': ws.cell(row=row, column=11).value,
        'alergias': ws.cell(row=row, column=19).value,
        'condiciones': ws.cell(row=row, column=20).value,
        'medicamentos': ws.cell(row=row, column=21).value,
        'contacto_emergencia': ws.cell(row=row, column=22).value,
        'palabra': ws.cell(row=row, column=23).value,
        'dudas': ws.cell(row=row, column=24).value,
        'algo_directores': ws.cell(row=row, column=25).value,
        'invitados': [],
        'sin_formulario': False,
    }
    inv1 = {'nombre': ws.cell(row=row, column=12).value, 'edad': ws.cell(row=row, column=13).value, 'relacion': ws.cell(row=row, column=14).value}
    inv2 = {'nombre': ws.cell(row=row, column=15).value, 'edad': ws.cell(row=row, column=16).value, 'relacion': ws.cell(row=row, column=17).value}
    for inv in [inv1, inv2]:
        if inv['nombre'] and str(inv['nombre']).strip().lower() not in ['n/a','na','-']:
            p['invitados'].append({k: str(v).strip() if v else None for k, v in inv.items()})
    equipo.append(p)

# Manual fixes
FIXES = {
    'Victoria Lorenzo Rivera': {'edad': 27, 'cumple_mes': 9, 'cumple_dia': 21, 'cumple_anio': 1998},
    'Jhonnalia Franchesca Silvestre Guzmán': {'cumple_mes': 10, 'cumple_dia': 20, 'cumple_anio': 1999, 'edad': 26},
    'Paloma Mendez': {'cumple_mes': 6, 'cumple_dia': 27, 'cumple_anio': 1990, 'edad': 35},
    'Jordelis Mateo': {'edad': 26},
    'José Ángel Tusen Russo': {'edad': 26},
    'Wirna Miguelina Stapleton Pilier': {'edad': 32},
    'Darianny Rodriguez Belliard': {'edad': 24},
    'Jean Carlo De la Cruz Mendez': {'etc_propio': 52, 'etc_anio_propio': 2012},
    'Priscilla Hidalgo Pou': {'etc_propio': 51, 'etc_anio_propio': 2011},
    'Ivanna Marien Mercedes Sosa': {'etc_propio': 74, 'etc_anio_propio': 2018},
    'Mary Carmen Ramírez Vásquez': {'etc_propio': 73, 'etc_anio_propio': 2018, 'etcs_servidos': 2},
    'Roberto Figueroa': {'etc_propio': 55, 'etc_anio_propio': None, 'etcs_servidos': 3},
}
for p in equipo:
    nm = p['nombre']
    if nm in FIXES:
        for k, v in FIXES[nm].items(): p[k] = v
    # Re-compute comunidad after ETC fix
    p['comunidad'] = 'Belén' if p['etc_propio'] == 85 else 'Betania'

# Mark existing equipo as operativo=True
for p in equipo:
    p['operativo'] = True
    p['backup'] = False
    p['vacante'] = False
    p['transversal'] = False

# Placeholders for people in xlsx without form response (operativos)
PLACEHOLDERS_OP = [
    ('Daylin (sin formulario)', 'musica', 'Música', 'F'),
    ('Olanlly (sin formulario)', 'cocina', 'Cocina', 'F'),
    ('Pamela (sin formulario)', 'cocina', 'Cocina', 'F'),
    ('Frank Morales', 'asesores', 'Asesor + Banderín', 'M'),  # asesor normal; además lleva el Banderín
    ('Vacante Cocina (varón — candidato Randolph)', 'cocina', 'Vacante', '?'),  # Roselyn salió 2-jun
    ('Rodolfo Telémaco', 'guias', 'Backup Guía', 'M'),   # backup
    ('Scarlett Nivar', 'guias', 'Backup Guía', 'F'),     # backup
    ('Kamila Todd', 'guias', 'Backup Guía', 'F'),        # backup
]
# Asesores transversales: Paul y Sor Angelina están en TODO el proceso (no solo retiro)
PLACEHOLDERS_TRANSVERSAL = [
    ('Padre Paul Ramírez', 'asesores_espirituales', 'Asesor Espiritual transversal', 'M'),
    ('Sor Angelina Lebrón', 'asesores_espirituales', 'Asesora Espiritual transversal', 'F'),
]
# Asesores ampliados (en el retiro pero NO operativos en formación) — confirmados 2-jun
PLACEHOLDERS_NO_OP = [
    ('Mary "Petra" Morales', 'asesores_cocina', 'Asesora Cocina', 'F'),
    ('Johanny García', 'asesores_cocina', 'Asesora Cocina', 'F'),
    ('Sandrita', 'asesores_diocesanos', 'Asesora Comunidad SD', 'F'),
    ('Marleny', 'asesores_diocesanos', 'Asesora Comunidad SD', 'F'),
    ('Leticia González', 'asesores_diocesanos', 'Asesora Comunidad La Vega', 'F'),
]

def make_placeholder(name, area, rol, sexo, operativo):
    return {
        'id': re.sub(r'[^a-z0-9]+','-', name.lower()).strip('-'),
        'nombre': name,
        'sexo': sexo, 'edad': None,
        'cumple_mes': None, 'cumple_dia': None, 'cumple_anio': None,
        'etc_propio': None, 'etc_anio_propio': None, 'etcs_servidos': None,
        'residencia': '—', 'comunidad': 'Por confirmar',
        'area': area, 'rol': rol,
        'talla': None, 'telefono': None,
        'que_espera': None, 'miedos': None, 'tema_dios': None, 'invita': None,
        'alergias': None, 'condiciones': None, 'medicamentos': None,
        'contacto_emergencia': None, 'palabra': None, 'dudas': None, 'algo_directores': None,
        'invitados': [],
        'sin_formulario': True,
        'operativo': operativo,
        'backup': rol == 'Backup Guía',
        'vacante': rol == 'Vacante',
        'transversal': False,
    }

for name, area, rol, sexo in PLACEHOLDERS_OP:
    # backups y vacante NO son titulares operativos
    is_op = rol not in ('Backup Guía', 'Vacante')
    equipo.append(make_placeholder(name, area, rol, sexo, is_op))
for name, area, rol, sexo in PLACEHOLDERS_NO_OP:
    equipo.append(make_placeholder(name, area, rol, sexo, False))
for name, area, rol, sexo in PLACEHOLDERS_TRANSVERSAL:
    p = make_placeholder(name, area, rol, sexo, True)
    p['transversal'] = True  # están en todo el proceso, no solo retiro
    equipo.append(p)

# Correcciones de nombre confirmadas por el director (la clave es el nombre del formulario).
RENAMES = {
    'Leober Carrion Soriank': 'Leober Carrion Soriano',
    'Guido Mardonado': 'Guido Maldonado',
    'Fabelle maciel fabian bello': 'Fabelly Maciel Fabian Bello',
}
# Apellidos mal escritos que también aparecen en campos de texto (p. ej. contacto de emergencia del mismo familiar).
SURNAME_FIX = {'Mardonado': 'Maldonado'}
for p in equipo:
    if p['nombre'] in RENAMES:
        p['nombre'] = RENAMES[p['nombre']]
        p['id'] = re.sub(r'[^a-z0-9]+', '-', p['nombre'].lower()).strip('-')
    ce = p.get('contacto_emergencia')
    if ce:
        for bad, good in SURNAME_FIX.items():
            if bad in ce:
                p['contacto_emergencia'] = ce.replace(bad, good)

ROL_ORDER = {
    'Director':1, 'Asesora':2, 'Asesor':2, 'Asesor (laico)':2,
    'Coord. Guía':3, 'Guía':4,
    'Coord. Cocina':5, 'Cocina':6,
    'Coord. Música':7, 'Música':8,
    'Asesora Cocina':10, 'Asesor Espiritual':11, 'Asesora Espiritual':11,
    'Asesor SD':12, 'Asesor La Vega':12, 'Asesor La Vega (opcional)':13,
}
equipo.sort(key=lambda p: (0 if p.get('operativo') else 1, ROL_ORDER.get(p['rol'], 99), p['nombre']))

print(f"Total tripulantes: {len(equipo)}")
from collections import Counter
print('Por área:', dict(Counter(p['area'] for p in equipo)))
print('Por rol:', dict(Counter(p['rol'] for p in equipo)))
print('Comunidades:', dict(Counter(p['comunidad'] for p in equipo)))

# Calendar / banderas (unchanged from v1)
calendario = [
    {'fecha': '2026-06-07', 'titulo': 'Misa Eteciana', 'tipo': 'misa', 'sin_formacion': True},
    {'fecha': '2026-06-04', 'titulo': 'Reunión de Coordinadores (jueves 4-jun · Corpus Christi · virtual)', 'tipo': 'coordinacion'},
    {'fecha': '2026-06-14', 'titulo': 'F1 — Primera Formación (presupuesto, sentido, temática)', 'tipo': 'formacion'},
    {'fecha': '2026-06-21', 'titulo': 'Clausura ETC 87 — La Vega', 'tipo': 'externo', 'sin_formacion': True},
    {'fecha': '2026-06-28', 'titulo': 'F2 — Segunda Formación', 'tipo': 'formacion'},
    {'fecha': '2026-07-05', 'titulo': 'F3 — Tercera Formación', 'tipo': 'formacion'},
    {'fecha': '2026-07-12', 'titulo': 'Misa Eteciana', 'tipo': 'misa', 'sin_formacion': True},
    {'fecha': '2026-07-19', 'titulo': 'F4 — Cuarta Formación (lectura de perfiles)', 'tipo': 'formacion'},
    {'fecha': '2026-07-26', 'titulo': 'Día del Padre', 'tipo': 'externo', 'sin_formacion': True},
    {'fecha': '2026-07-31', 'titulo': 'Profondo #1 (31-jul → 2-ago)', 'tipo': 'profondo', 'fin': '2026-08-02'},
    {'fecha': '2026-08-09', 'titulo': 'Misa Eteciana', 'tipo': 'misa', 'sin_formacion': True},
    {'fecha': '2026-08-16', 'titulo': 'F5 — Quinta Formación (lectura de perfiles 2 + cobro al cierre)', 'tipo': 'formacion'},
    {'fecha': '2026-08-22', 'titulo': 'Convivencia del Equipo (inicia con miniretiro/reflexión · día completo)', 'tipo': 'convivencia'},
    {'fecha': '2026-08-23', 'titulo': 'Ensayo General del ETC 88 (obligatorio)', 'tipo': 'ensayo'},
    {'fecha': '2026-08-30', 'titulo': 'Reunión final · deadline pagos equipo + padrinos', 'tipo': 'pre_retiro'},
    {'fecha': '2026-09-03', 'titulo': 'Avanzada del Equipo de Cocina', 'tipo': 'avanzada'},
    {'fecha': '2026-09-04', 'titulo': 'ETC 88 (4 → 6 sep)', 'tipo': 'retiro', 'fin': '2026-09-06'},
    {'fecha': '2026-09-09', 'titulo': 'Bienvenida post-ETC a los nuevos (baile + bizcocho)', 'tipo': 'post_retiro', 'sin_formacion': True},
]

banderas = [
    {'n':1, 'bandera':'Cumple en F1', 'persona':'Ismarie Sthepanie Constanzo Ramos', 'accion':'Preparar momento corto en F1', 'resp':'Directores'},
    {'n':2, 'bandera':'Cumple en Reunión final pre-retiro', 'persona':'Dayrelins Jazmin Santana Salas', 'accion':'Preparar momento corto', 'resp':'Directores'},
    {'n':3, 'bandera':'Cumple en Día del Padre (sin formación)', 'persona':'Jordelis Mateo', 'accion':'Mensaje virtual + saludo en F4', 'resp':'Directores'},
    {'n':4, 'bandera':'Cumples post-retiro Tommy (7-sep) y Wilka (8-sep)', 'persona':'Tommy, Wilka', 'accion':'Mencionar/celebrar en bienvenida', 'resp':'Directores'},
    {'n':5, 'bandera':'Viaje julio vs Profondo (31-jul a 2-ago)', 'persona':'Fabelly (revisar lista v2)', 'accion':'Confirmar agenda ASAP', 'resp':'Directores'},
    {'n':6, 'bandera':'Necesita rides', 'persona':'Wilka María Reyes Mota', 'accion':'Asignar buddy con auto desde F1', 'resp':'Coord. Guía'},
    {'n':7, 'bandera':'Postoperatoria', 'persona':'Jordelis Mateo', 'accion':'No asignar carga física pesada', 'resp':'Coord. Cocina'},
    {'n':8, 'bandera':'Cirugía reciente columna (escoliosis)', 'persona':'Jhonnalia + Mary Carmen', 'accion':'No esfuerzo físico + ayuda para movilizar cosas', 'resp':'Coord. Guía / Coord. Música'},
    {'n':9, 'bandera':'Sin claridad de rol', 'persona':'Wirna Miguelina Stapleton Pilier', 'accion':'Conversación 1:1 con Directores antes de F1', 'resp':'Directores'},
    {'n':10, 'bandera':'Timidez declarada — roles tras bastidores', 'persona':'Adrián, Risairi, Mary Carmen', 'accion':'No exposición pública obligada', 'resp':'Coordinadores'},
    {'n':11, 'bandera':'Memoria de fricciones pasadas', 'persona':'Luisa, Franklin, Fabelly, Juan Manuel', 'accion':'Trabajar alianza interna en Profondo #1', 'resp':'Directores'},
    {'n':12, 'bandera':'Pareja Dorian↔José Ángel — ambos en Música', 'persona':'Dorian, José Ángel', 'accion':'Reconsiderar: están en la misma área', 'resp':'Directores'},
    {'n':13, 'bandera':'Noviazgo Kelvin↔Brianelis — ambos en Cocina', 'persona':'Kelvin, Brianelis', 'accion':'Reconsiderar: están en la misma área', 'resp':'Directores'},
    {'n':14, 'bandera':'Noviazgo Juan Manuel↔Yelaxni — áreas distintas ✓', 'persona':'Juan Manuel (Dir), Yelaxni (Guía)', 'accion':'OK', 'resp':'—'},
    {'n':15, 'bandera':'Noviazgo Oliver↔Dayrelins — áreas distintas ✓', 'persona':'Oliver (Guía), Dayrelins (Cocina)', 'accion':'OK', 'resp':'—'},
    {'n':16, 'bandera':'Familia De la Cruz Méndez — Paloma en Cocina, JC/JM en Dirección, Fabelly en Cocina', 'persona':'JC, JM, Paloma, Fabelly', 'accion':'Confirmar distribución', 'resp':'Directores'},
    {'n':17, 'bandera':'Mariscos prohibidos como plato principal', 'persona':'Priscilla, Ivanna, Jonathan, Laura (4 alérgicas)', 'accion':'Avisar a Cocina', 'resp':'Coord. Cocina'},
    {'n':18, 'bandera':'Evitar piña en menú', 'persona':'Wilka, Candy, José Ángel (3 alérgicos)', 'accion':'No piña en jugos, postres, marinadas', 'resp':'Coord. Cocina'},
    {'n':19, 'bandera':'Alternativa sin huevo en desayunos', 'persona':'José Ángel', 'accion':'Avisar Cocina', 'resp':'Coord. Cocina'},
    {'n':20, 'bandera':'Cuidado con canela', 'persona':'Wilka María Reyes Mota', 'accion':'No canela en postres', 'resp':'Coord. Cocina'},
    {'n':21, 'bandera':'Diabetes — horarios y comida adaptada', 'persona':'Luisa María Fiorentino Brugal', 'accion':'Horarios regulares, opciones bajas en azúcar', 'resp':'Coord. Cocina'},
    {'n':22, 'bandera':'Gastritis severa — comidas no irritantes', 'persona':'Candy Elizabeth Gatwood Ramos', 'accion':'Sin picante/grasoso pesado', 'resp':'Coord. Cocina'},
    {'n':23, 'bandera':'Botiquín SIN Penicilina, Ibuprofeno, AINEs, Neo-Melubrina, Metoclopramida', 'persona':'Luisa, Tomás, Dayrelins, Ismarie, Jhonnalia', 'accion':'Avisar Enfermería', 'resp':'Producción'},
    {'n':24, 'bandera':'Botiquín CON Paracetamol + inhalador + antialérgico', 'persona':'Yelaxni, Fernando, Ivanna (asmáticas)', 'accion':'Asegurar disponibilidad', 'resp':'Producción'},
    {'n':25, 'bandera':'Confirmar gatos en Casa de Retiro', 'persona':'Dorian (alérgica)', 'accion':'Coordinar con Higüey', 'resp':'Producción'},
    {'n':26, 'bandera':'NO fumigar (Baygon) durante el retiro', 'persona':'José Ángel', 'accion':'Coordinar con Higüey', 'resp':'Producción'},
    {'n':27, 'bandera':'Limpieza profunda de polvo previa al retiro', 'persona':'Luisa, Fernando, Victoria, Dorian (4 sensibles)', 'accion':'Avanzada cocina 3-sep', 'resp':'Coord. Cocina'},
    {'n':28, 'bandera':'Pedir contacto de emergencia a Jonathan', 'persona':'Jonathan Andres Medina Mota', 'accion':'Solicitar dato', 'resp':'Directores'},
    {'n':29, 'bandera':'Pregunta "Oremos por JC"', 'persona':'Victoria Lorenzo Rivera', 'accion':'Acompañamiento espiritual a Jean Carlo', 'resp':'Asesores'},
    {'n':30, 'bandera':'Wirna: "No se dejen humillar"', 'persona':'Wirna Stapleton', 'accion':'Conversación 1:1', 'resp':'Directores'},
    {'n':31, 'bandera':'4 tripulantes sin formulario', 'persona':'Daylin (Música), Olanlly + Roselyn + Pamela (Cocina)', 'accion':'Enviar formulario antes de F1 (14-jun)', 'resp':'Coord. Música / Coord. Cocina'},
    {'n':32, 'bandera':'Nombre confirmado: Fabelly Maciel Fabian Bello (Cocina)', 'persona':'Fabelly Maciel Fabian Bello', 'accion':'OK · nombre validado', 'resp':'Directores'},
    {'n':33, 'bandera':'Familia De la Cruz Méndez (4 personas) — distribuida', 'persona':'JC (Dir), JM (Dir), Paloma (Cocina coord), Fabelly (Cocina)', 'accion':'OK distribución; 3 en cocina/dirección, 1 en cocina', 'resp':'Directores'},
]

invitados_list = []
for p in equipo:
    if p.get('invita') == 'Sí' and p['invitados']:
        invitados_list.append({'inviter': p['nombre'], 'invitados': p['invitados']})

recaudacion = {
    'top': [
        {'propuesta':'Rifa', 'menciones':23},
        {'propuesta':'Venta de comida', 'menciones':10},
        {'propuesta':'Bazar / venta de garaje', 'menciones':4},
        {'propuesta':'Noche de talento / karaoke / película', 'menciones':4},
        {'propuesta':'Lavado de autos', 'menciones':2},
        {'propuesta':'Rally / actividad deportiva', 'menciones':2},
        {'propuesta':'Carrera 5K + coffee party (Chantal)', 'menciones':1},
        {'propuesta':'Excursión / día-pass / tómbola', 'menciones':3},
        {'propuesta':'Donaciones empresas (Guido)', 'menciones':1},
        {'propuesta':'Donaciones etecianos viejos (Roberto)', 'menciones':1},
        {'propuesta':'Merch eteciana (Paloma)', 'menciones':1},
        {'propuesta':'Rifa de viaje internacional (Franklin)', 'menciones':1},
    ],
    'cita_franklin':'Tomar en cuenta el tiempo de preparación para recaudar fondos.',
    'cita_jordelis':'Tómbolas con PRECIOS ASEQUIBLES para darle más oportunidad a quienes siempre nos apoyan.'
}

# ===== Fuente única de hechos NO-roster: data/estado.json =====
# build_data.py NO inventa cifras ni decisiones: las toma de estado.json (con sus
# banderas confirmado/propuesta/pendiente). Los docs renderizan esas banderas.
estado = json.load(open(f'{REPO}/data/estado.json'))

def _v(node):
    """Extrae .valor de un nodo {valor, estado, ...}; si no, devuelve el nodo tal cual."""
    return node['valor'] if isinstance(node, dict) and 'valor' in node else node

ef = estado['finanzas']
finanzas = {
    'casa_por_persona_sin_exencion': _v(ef['casa_por_persona_sin_exencion']),
    'casa_por_persona_con_exencion': _v(ef['casa_por_persona_con_exencion']),
    'exencion_nota': ef['casa_por_persona_con_exencion'].get('nota', ''),
    'deuda_inicial': {
        'monto': _v(ef['deuda_inicial']),
        'descripcion': ef['deuda_inicial'].get('nota', ''),
        'acreedor': ef['deuda_inicial'].get('acreedor', ''),
    },
    'cuota_participante': _v(ef['cuota_participante']),
    'meta_recaudacion_total': _v(ef['meta_recaudacion_total']),
    'meta_recaudacion_estado': ef['meta_recaudacion_total']['estado'],
    'cuota_equipo_propuesta': {
        **_v(ef['cuota_equipo']),
        'estado': ef['cuota_equipo']['estado'],
        'nota': ef['cuota_equipo'].get('nota', ''),
    },
}

equipos_auxiliares = [
    {
        'nombre': a['nombre'],
        'descripcion': a['descripcion'],
        'estado': 'Por formular',
        'miembros': a.get('miembros', []),
        'responsable_sugerido': a['responsable']['valor'],
        'responsable_estado': a['responsable']['estado'],
    }
    for a in estado['equipos_auxiliares']
]

data = {
    'meta': {'numero':88, 'romano':'LXXXVIII', 'version':'v8-2026-06-02', 'total_equipo':len(equipo), 'operativos':sum(1 for p in equipo if p.get('operativo')), 'no_operativos':sum(1 for p in equipo if not p.get('operativo'))},
    'finanzas': finanzas,
    'estado': estado,
    'equipos_auxiliares': equipos_auxiliares,
    'marca': {
        'lema': _v(estado['marca']['lema_eteciano']),
        'cita': estado['marca']['lema_eteciano'].get('cita'),
        'cita_texto': estado['marca']['lema_eteciano'].get('cita_texto'),
        'lema_retiro': _v(estado['marca']['lema_retiro']),
        'lema_retiro_estado': estado['marca']['lema_retiro']['estado'],
        'tematica': _v(estado['marca']['tematica']),
        'tematica_estado': estado['marca']['tematica']['estado'],
        'sub':'Tripulación para una expedición',
    },
    'equipo': equipo,
    'calendario': calendario,
    'banderas': banderas,
    'invitados': invitados_list,
    'recaudacion': recaudacion,
    'salud': {
        'alergias_alimentarias': {
            'mariscos': ['Priscilla Hidalgo Pou','Ivanna Marien Mercedes Sosa','Jonathan Andres Medina Mota','Laura Fernández'],
            'pina': ['Wilka María Reyes Mota','Candy Elizabeth Gatwood Ramos','José Ángel Tusen Russo'],
            'huevo': ['José Ángel Tusen Russo'],
            'canela': ['Wilka María Reyes Mota'],
        },
        'alergias_medicamentos': {
            'Penicilina': ['Luisa Maria Fiorentino Brugal'],
            'AINEs': ['Dayrelins Jazmin Santana Salas'],
            'Ibuprofeno': ['Tomás Lorenzo'],
            'Neo-Melubrina / Metamizol': ['Ismarie Sthepanie Constanzo Ramos'],
            'Metoclopramida': ['Jhonnalia Franchesca Silvestre Guzmán'],
        },
        'asmaticas': ['Yelaxni Mota','Fernando Cordero','Ivanna Marien Mercedes Sosa'],
        'condiciones': {
            'Diabetes + tiroides':['Luisa Maria Fiorentino Brugal'],
            'Gastritis severa':['Candy Elizabeth Gatwood Ramos'],
            'Migraña':['Dorian Elina Rodriguez Belliard','Ismarie Sthepanie Constanzo Ramos'],
            'Postoperatoria reciente':['Jordelis Mateo','Jhonnalia Franchesca Silvestre Guzmán'],
            'Postquirúrgica escoliosis':['Mary Carmen Ramírez Vásquez'],
            'Pastillas presión':['Maria del Carmen Mejías Mateo'],
        },
        'ambiente_higuey': [
            'Confirmar gatos en Casa de Retiro (Dorian alérgica)',
            'NO fumigar (Baygon) durante retiro (José Ángel alérgico)',
            'Limpieza profunda de polvo previa (4 sensibles)',
            'Usar productos de limpieza suaves (Victoria atópica)',
            'Jabón alternativo en duchas (Franklin alérgico al de cuaba)',
            'Tener espacio oscuro/silencioso disponible (Dorian, Ismarie migrañas)',
        ]
    }
}

with open('/tmp/etc88_data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open('/tmp/etc88_data_min.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',',':'))
# Refresca la copia durable/committeada (roster + hechos de estado.json ensamblados).
with open(f'{REPO}/data/equipo.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Wrote {len(equipo)} tripulantes · data/equipo.json refrescado desde xlsx + estado.json")
