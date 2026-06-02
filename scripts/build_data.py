#!/usr/bin/env python3
"""Build ETC88 data JSON from form responses + user corrections."""
import openpyxl
import json
import re
from datetime import datetime

XLSX = '/root/.claude/uploads/2da4a2cd-be63-4d49-b615-cf5c7554c95e/93ed3347-Respuestas__Formulario_preformacio_n_ETC_88.xlsx'

MONTHS = {'enero':1,'ene':1,'febrero':2,'feb':2,'marzo':3,'mar':3,'abril':4,'abr':4,
          'mayo':5,'may':5,'junio':6,'jun':6,'julio':7,'jul':7,'agosto':8,'ago':8,
          'septiembre':9,'sept':9,'sep':9,'octubre':10,'oct':10,'noviembre':11,'nov':11,
          'diciembre':12,'dic':12}

# Manual data — corrections + assignments per user input
EXCLUDE = {'Mary Carmen Ramírez Vásquez', 'Roberto Figueroa'}

GENDER = {  # F unless listed
    'Jean Carlo De la Cruz Mendez':'M', 'Kelvin Alexis Ventura Santana':'M',
    'Juan Pablo Argüello Alzate':'M', 'Fernando Cordero':'M',
    'Oliver Rafael De León Ramírez':'M', 'Adrián Francisco Santana Puente':'M',
    'Franklin De Jesús Silverio Delgadillo':'M', 'José Ángel Tusen Russo':'M',
    'Leober Carrion Soriank':'M', 'Tommy Nova Nolasco':'M',
    'Juan Manuel de la Cruz Méndez':'M', 'Roberto Figueroa':'M',
    'Jonathan Andres Medina Mota':'M', 'Johnnito Richiez Brugal':'M',
    'Guido Mardonado':'M', 'Tomás Lorenzo':'M',
}

# Residence overrides (defaults to SPM)
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

# Area assignments (per Borrador 11-abr + user updates)
AREA = {
    # Directores
    'Jean Carlo De la Cruz Mendez':       ('directores', 'Director'),
    'Juan Manuel de la Cruz Méndez':      ('directores', 'Director'),
    # Asesores
    'Laura Fernández':                     ('asesores', 'Asesora'),
    'Tomás Lorenzo':                       ('asesores', 'Asesor'),
    # Guías coords
    'Priscilla Hidalgo Pou':              ('guias', 'Coord. Guías'),
    'Camila Fernández Hazim':             ('guias', 'Coord. Guías'),
    # Guías
    'Jonathan Andres Medina Mota':        ('guias', 'Guía'),
    'Luisa Maria Fiorentino Brugal':      ('guias', 'Guía'),
    'Juan Pablo Argüello Alzate':         ('guias', 'Guía'),
    'Yelaxni Mota':                        ('guias', 'Guía'),
    'Oliver Rafael De León Ramírez':      ('guias', 'Guía'),
    'Victoria Lorenzo Rivera':            ('guias', 'Guía'),
    'Wirna Miguelina Stapleton Pilier':   ('guias', 'Guía'),
    'Leober Carrion Soriank':             ('guias', 'Guía'),
    'Franklin De Jesús Silverio Delgadillo':('guias','Guía'),
    'Darianny Rodriguez Belliard':        ('guias', 'Guía'),
    'Jhonnalia Franchesca Silvestre Guzmán':('guias','Guía'),
    # Cocina coords
    'Paloma Mendez':                       ('cocina', 'Coord. Cocina'),
    'Johnnito Richiez Brugal':             ('cocina', 'Coord. Cocina'),
    'Dayrelins Jazmin Santana Salas':      ('cocina', 'Coord. Cocina (posible)'),
    # Cocina
    'Adrián Francisco Santana Puente':     ('cocina', 'Cocina'),
    'Ambar Liz Jáquez Lebrón':             ('cocina', 'Cocina'),
    'Brianelis Abreu Calderón':            ('cocina', 'Cocina'),
    'Candy Elizabeth Gatwood Ramos':       ('cocina', 'Cocina'),
    'Chantal Melissa Carpio Jiménez':      ('cocina', 'Cocina'),
    'Kelvin Alexis Ventura Santana':       ('cocina', 'Cocina'),
    'Risaira Santana Rosario':             ('cocina', 'Cocina'),
    'Risairi Santana Rosario':             ('cocina', 'Cocina'),
    'Tommy Nova Nolasco':                  ('cocina', 'Cocina'),
    'Wilka María Reyes Mota':              ('cocina', 'Cocina'),
    'Guido Mardonado':                     ('cocina', 'Cocina'),
    'Maria del Carmen Mejías Mateo':       ('cocina', 'Cocina'),
    'Jordelis Mateo':                      ('cocina', 'Cocina'),
    'Ivanna Marien Mercedes Sosa':         ('cocina', 'Cocina'),
    # Música
    'José Ángel Tusen Russo':              ('musica', 'Coord. Música'),
    'Dorian Elina Rodriguez Belliard':     ('musica', 'Música'),
    'Fernando Cordero':                    ('musica', 'Música'),
    'Ismarie Sthepanie Constanzo Ramos':   ('musica', 'Música'),
    # Por asignar
    'Fabelle maciel fabian bello':         ('por_asignar', 'Por asignar'),
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
        return ((b, a), y) if a <= 12 and b <= 12 else ((b, a), y) if a > 12 else ((a, b), y)
    m = re.search(r'(\d{1,2})de\s*([a-zé]+)\s*(\d{4})?', s)
    if m:
        d, mo, y = int(m.group(1)), MONTHS.get(m.group(2)), m.group(3)
        if mo: return ((mo, d), int(y) if y else None)
    m = re.search(r'(\d{1,2})\s*(\d{1,2})\s*([a-zé]+)\s*(\d{4})', s)
    if m:
        d, mo_w, y = int(m.group(2)), m.group(3), m.group(4)
        mo = MONTHS.get(mo_w)
        if mo: return ((mo, d), int(y))
    return (None, None)

def parse_etcs_servidos(s):
    """Returns int or None."""
    if s is None: return None
    s = str(s).strip().lower()
    if s in ['en ninguno','ninguno','ningunos','primera vez','en 0','en ningunos']: return 0
    m = re.match(r'^(\d+)', s)
    if m: return int(m.group(1))
    if 'desde el 2012' in s or 'desde 2012' in s: return 12  # Priscilla
    if '10 a 12' in s or '10-12' in s: return 11
    if '5 o 6' in s or '5-6' in s: return 6
    if '8' in s and '2018' in s: return 8  # José Ángel
    if 'una cocina dos guías' in s: return 3  # Jhonnalia
    if 'en 1' in s or '1 solo' in s: return 1
    return None

def parse_etc_propio(s):
    if not s: return (None, None)
    s = str(s).strip()
    m = re.search(r'(?:etc\s*)?#?(\d{2,3})', s, re.I)
    num = int(m.group(1)) if m else None
    if num and num > 100:  # like 522012 = ETC 52 año 2012
        sn = str(num)
        if len(sn) == 6:
            num = int(sn[:2])
            year = int(sn[2:])
            return (num, year)
    m_y = re.search(r'(20\d{2})', s)
    year = int(m_y.group(1)) if m_y else None
    return (num, year)

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb['Form Responses 1']

equipo = []
for row in range(2, ws.max_row + 1):
    name = ws.cell(row=row, column=2).value
    if not name: continue
    name = name.strip()
    if name in EXCLUDE: continue

    bday, byear = parse_bday(ws.cell(row=row, column=3).value)
    etc_num, etc_year = parse_etc_propio(ws.cell(row=row, column=7).value)
    etcs_servidos = parse_etcs_servidos(ws.cell(row=row, column=6).value)
    area, rol = AREA.get(name, ('por_asignar', 'Por asignar'))

    # edad: extract from raw
    edad_raw = str(ws.cell(row=row, column=3).value or '')
    m_edad = re.search(r'(\d{2,3})\s*(?:años|-|—)', edad_raw)
    edad = int(m_edad.group(1)) if m_edad else None
    if not edad:
        m_edad = re.match(r'^\s*(\d{2})\s', edad_raw)
        if m_edad: edad = int(m_edad.group(1))

    person = {
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
        'area': area,
        'rol': rol,
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
    }
    # Invitados
    inv1 = {'nombre': ws.cell(row=row, column=12).value, 'edad': ws.cell(row=row, column=13).value, 'relacion': ws.cell(row=row, column=14).value}
    inv2 = {'nombre': ws.cell(row=row, column=15).value, 'edad': ws.cell(row=row, column=16).value, 'relacion': ws.cell(row=row, column=17).value}
    for inv in [inv1, inv2]:
        if inv['nombre'] and str(inv['nombre']).strip().lower() not in ['n/a','na','-']:
            person['invitados'].append({k: str(v).strip() if v else None for k, v in inv.items()})

    equipo.append(person)

print(f"Parsed {len(equipo)} personas (esperado 39)")

# Sort by nombre
equipo.sort(key=lambda p: p['nombre'])

# Calendar events from NEW ICS
calendario = [
    {'fecha': '2026-06-07', 'titulo': 'Misa Eteciana', 'tipo': 'misa', 'sin_formacion': True},
    {'fecha': '2026-06-14', 'titulo': 'F1 — Primera Formación', 'tipo': 'formacion'},
    {'fecha': '2026-06-21', 'titulo': 'Clausura ETC 87 — La Vega', 'tipo': 'externo', 'sin_formacion': True},
    {'fecha': '2026-06-28', 'titulo': 'F2 — Segunda Formación', 'tipo': 'formacion'},
    {'fecha': '2026-07-05', 'titulo': 'F3 — Tercera Formación', 'tipo': 'formacion'},
    {'fecha': '2026-07-12', 'titulo': 'Misa Eteciana', 'tipo': 'misa', 'sin_formacion': True},
    {'fecha': '2026-07-19', 'titulo': 'F4 — Cuarta Formación (lectura de perfiles)', 'tipo': 'formacion'},
    {'fecha': '2026-07-26', 'titulo': 'Día del Padre', 'tipo': 'externo', 'sin_formacion': True},
    {'fecha': '2026-07-31', 'titulo': 'Profondo #1 (31-jul → 2-ago)', 'tipo': 'profondo', 'fin': '2026-08-02'},
    {'fecha': '2026-08-09', 'titulo': 'Misa Eteciana', 'tipo': 'misa', 'sin_formacion': True},
    {'fecha': '2026-08-16', 'titulo': 'Convivencia / Retiro (media jornada)', 'tipo': 'convivencia'},
    {'fecha': '2026-08-23', 'titulo': 'Ensayo General del ETC 88', 'tipo': 'ensayo'},
    {'fecha': '2026-08-30', 'titulo': 'Conciliación y Planificación pre-ETC 88', 'tipo': 'pre_retiro'},
    {'fecha': '2026-09-03', 'titulo': 'Avanzada del Equipo de Cocina', 'tipo': 'avanzada'},
    {'fecha': '2026-09-04', 'titulo': 'ETC 88 (4 → 6 sep)', 'tipo': 'retiro', 'fin': '2026-09-06'},
]

relaciones = {
    'matrimonios': [['Dorian Elina Rodriguez Belliard', 'José Ángel Tusen Russo']],
    'noviazgos': [
        ['Kelvin Alexis Ventura Santana', 'Brianelis Abreu Calderón'],
        ['Juan Manuel de la Cruz Méndez', 'Yelaxni Mota'],
        ['Oliver Rafael De León Ramírez', 'Dayrelins Jazmin Santana Salas'],
    ],
    'familias': [
        {'nombre':'De la Cruz Méndez (extendida)', 'miembros':['Jean Carlo De la Cruz Mendez','Juan Manuel de la Cruz Méndez','Paloma Mendez','Fabelle maciel fabian bello'], 'tipo':'Hermanos + prima (Paloma) + cuñada (Fabelle vía Fabelly, esposa de JC)'},
        {'nombre':'Lorenzo','miembros':['Tomás Lorenzo','Victoria Lorenzo Rivera'],'tipo':'Hermanos'},
        {'nombre':'Fernández','miembros':['Camila Fernández Hazim','Laura Fernández'],'tipo':'Hermanas'},
        {'nombre':'Santana Rosario','miembros':['Risaira Santana Rosario','Risairi Santana Rosario'],'tipo':'Hermanas'},
        {'nombre':'Rodríguez Belliard','miembros':['Dorian Elina Rodriguez Belliard','Darianny Rodriguez Belliard'],'tipo':'Hermanas'},
    ],
}

banderas = [
    {'n':1, 'bandera':'Cumple en F1', 'persona':'Ismarie Sthepanie Constanzo Ramos', 'accion':'Preparar momento corto en F1', 'resp':'Directores'},
    {'n':2, 'bandera':'Cumple en Reunión final pre-retiro', 'persona':'Dayrelins Jazmin Santana Salas', 'accion':'Preparar momento corto', 'resp':'Directores'},
    {'n':3, 'bandera':'Cumple en Día del Padre (sin formación)', 'persona':'Jordelis Mateo', 'accion':'Mensaje virtual + saludo en F4', 'resp':'Directores'},
    {'n':4, 'bandera':'Cumples post-retiro Tommy (7-sep) y Wilka (8-sep)', 'persona':'Tommy, Wilka', 'accion':'Mencionar/celebrar en bienvenida', 'resp':'Directores'},
    {'n':5, 'bandera':'Viaje julio vs Profondo (31-jul a 2-ago)', 'persona':'Fabelle maciel fabian bello', 'accion':'Confirmar agenda ASAP', 'resp':'Directores'},
    {'n':6, 'bandera':'Necesita rides', 'persona':'Wilka María Reyes Mota', 'accion':'Asignar buddy con auto desde F1', 'resp':'Coord. Cocina'},
    {'n':7, 'bandera':'Postoperatoria', 'persona':'Jordelis Mateo', 'accion':'No asignar carga física pesada', 'resp':'Coord. Cocina'},
    {'n':8, 'bandera':'Cirugía reciente columna (escoliosis)', 'persona':'Jhonnalia Franchesca Silvestre Guzmán', 'accion':'No esfuerzo físico + ayuda para movilizar cosas', 'resp':'Coord. Guías'},
    {'n':9, 'bandera':'Sin claridad de rol', 'persona':'Wirna Miguelina Stapleton Pilier', 'accion':'Conversación 1:1 con Directores antes de F1', 'resp':'Directores'},
    {'n':10, 'bandera':'Timidez declarada — roles tras bastidores', 'persona':'Adrián, Risairi, Mary Carmen (excluida)', 'accion':'No exposición pública obligada', 'resp':'Coordinadores'},
    {'n':11, 'bandera':'Memoria de fricciones pasadas', 'persona':'Luisa, Franklin, Fabelle, Juan Manuel', 'accion':'Trabajar alianza interna en Profondo #1', 'resp':'Directores'},
    {'n':12, 'bandera':'Pareja Dorian↔José Ángel — asignar áreas distintas', 'persona':'Dorian, José Ángel', 'accion':'Áreas o equipos diferentes', 'resp':'Directores'},
    {'n':13, 'bandera':'Noviazgo Kelvin↔Brianelis — áreas distintas', 'persona':'Kelvin, Brianelis', 'accion':'Áreas diferentes', 'resp':'Directores'},
    {'n':14, 'bandera':'Noviazgo Juan Manuel↔Yelaxni — áreas distintas', 'persona':'Juan Manuel, Yelaxni', 'accion':'Áreas diferentes', 'resp':'Directores'},
    {'n':15, 'bandera':'Noviazgo Oliver↔Dayrelins — áreas distintas', 'persona':'Oliver, Dayrelins', 'accion':'Áreas diferentes', 'resp':'Directores'},
    {'n':16, 'bandera':'Familia De la Cruz Méndez (4 personas) — distribuir', 'persona':'JC, JM, Paloma, Fabelle', 'accion':'Distribuir en áreas distintas', 'resp':'Directores'},
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
]

invitados_list = []
for p in equipo:
    if p['invita'] == 'Sí' and p['invitados']:
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

data = {
    'meta': {'numero':88, 'romano':'LXXXVIII', 'constelacion':49, 'version':'v1-2026-06-02', 'total_equipo_v1':len(equipo)},
    'marca': {
        'lema':'Siempre amigos',
        'cita':'Jn 15:15',
        'cita_texto':'Ya no os llamo siervos, os he llamado amigos',
        'frase':'No fuimos a buscarlo: él nos estaba esperando',
        'sub':'Tripulación para una expedición',
    },
    'equipo': equipo,
    'areas': {
        'directores':['Jean Carlo De la Cruz Mendez','Juan Manuel de la Cruz Méndez'],
        'asesores':['Laura Fernández','Tomás Lorenzo'],
        'cocina_coords':['Paloma Mendez','Johnnito Richiez Brugal'],
        'cocina_coord_posible':['Dayrelins Jazmin Santana Salas'],
        'musica_coord':['José Ángel Tusen Russo'],
        'guias_coords':['Priscilla Hidalgo Pou','Camila Fernández Hazim'],
    },
    'calendario': calendario,
    'relaciones': relaciones,
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
            'Postquirúrgica escoliosis':['Mary Carmen Ramírez Vásquez (excluida)'],
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
print(f"Wrote /tmp/etc88_data.json ({len(equipo)} personas)")
