#!/usr/bin/env python3
import os as _os
_R = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
"""Genera la GUÍA DEL ETC 88 (la 'carpeta' que se entrega en F1).
Jala equipo + calendario del data; embebe el contenido canónico (base LXXXV) adaptado al 88."""
import json

d = json.load(open('/tmp/etc88_data.json'))
eq = d['equipo']
MESES = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']

AREAS = [('directores','Directores'),('asesores','Asesores del Retiro'),
         ('guias','Guías'),('cocina','Cocina'),('musica','Música')]

L = []
A = L.append

# ---------- Portada ----------
A("# GUÍA DEL ETC LXXXVIII")
A("## San Pedro de Macorís")
A("")
_m = d.get('marca', {})
_lema_tag = '[PROPUESTA] ' if _m.get('lema_retiro_estado') == 'propuesta' else ''
_tema_tag = '[PROPUESTA] ' if _m.get('tematica_estado') == 'propuesta' else ''
A(f"> **Lema eteciano:** *“{_m.get('lema','Siempre amigos')}”* · **{_m.get('cita','Jn 15:15')}**")
A(f"> **Lema del retiro:** {_lema_tag}*“{_m.get('lema_retiro','')}”*")
A(f"> **Temática:** {_tema_tag}{_m.get('tematica','')}")
if _m.get('hilo'):
    A(f"> **Hilo espiritual:** {_m.get('hilo')} · **{_m.get('hilo_cita','Mt 13:44')}**")
A("> **Retiro:** 4–6 de septiembre de 2026 · Casa de Retiro «La Ceiba del Salado», Higüey")
A("> **Co-Dirección:** Juan Manuel de la Cruz · Jean Carlo de la Cruz")
A("")
A("*Esta es tu carpeta. Tráela a cada formación. Aquí está quiénes somos, el equipo, el calendario, las reglas y cómo nos preparamos.*")
A("")
A("---")

# ---------- 1. Qué es un ETC ----------
A("## 1. ¿Qué es un ETC?")
A("")
A("El **Encuentro Total con Cristo (ETC)** es *una experiencia que lleva a las personas a Jesús a través del encuentro consigo mismo y con sus semejantes* (Estatutos, Art. 6).")
A("Somos la **Asociación Eteciana**, una obra de la Iglesia Católica. Lo nuestro: acercar a las personas a Cristo, formar comunidad de vida cristiana, vivir coherentes con la fe y servir a los más necesitados.")
A("**Siempre amigos** (Jn 15,15) — esa es nuestra firma.")
A("")
A("---")

# ---------- 2. El equipo ----------
A("## 2. El Equipo del ETC 88")
A("")
op = [p for p in eq if p.get('operativo')]
A(f"Somos **{len(op)} servidores operativos** + asesores ampliados y transversales. Una sola tripulación, diferentes funciones.")
A("")
for area, label in AREAS:
    ms = [p for p in eq if p['area']==area and p.get('operativo') and not p.get('vacante') and not p.get('backup')]
    if not ms: continue
    coords = [p for p in ms if 'coord' in p['rol'].lower()]
    A(f"**{label} ({len(ms)})**" + (f" — Coord.: {', '.join(c['nombre'].replace(' (sin formulario)','') for c in coords)}" if coords else ""))
    nombres = [p['nombre'].replace(' (sin formulario)','') for p in sorted(ms, key=lambda x:(0 if 'coord' in x['rol'].lower() else 1, x['nombre']))]
    A("> " + " · ".join(nombres))
    A("")
# Transversales + ampliados
trans = [p['nombre'] for p in eq if p.get('transversal')]
if trans:
    A(f"**Asesores Espirituales (transversales):** {' · '.join(trans)}")
amp_coc = [p['nombre'].replace(' (sin formulario)','') for p in eq if p['area']=='asesores_cocina']
amp_com = [p['nombre'].replace(' (sin formulario)','') for p in eq if p['area']=='asesores_diocesanos']
if amp_coc: A(f"**Asesoras de Cocina:** {' · '.join(amp_coc)}")
if amp_com: A(f"**Asesores de Comunidad:** {' · '.join(amp_com)}")
A("")
A("**Equipos auxiliares:** " + " · ".join(a['nombre'] for a in d.get('equipos_auxiliares', [])))
A("")
A("---")

# ---------- 3. Calendario ----------
A("## 3. Calendario 2026")
A("")
A("| Fecha | Actividad |")
A("|---|---|")
for e in d['calendario']:
    f = e['fecha']
    try:
        y,m,dd = f.split('-')
        fecha = f"{int(dd)}-{MESES[int(m)-1]}"
    except Exception:
        fecha = f
    flag = " *(sin formación)*" if e.get('sin_formacion') else ""
    A(f"| {fecha} | {e['titulo']}{flag} |")
A("")
A("> **Retiro: 4–6 septiembre.** Asistencia obligatoria al **Ensayo General (23-ago)**. Máximo **3 ausencias justificadas** en las reuniones programadas.")
A("")
A("---")

# ---------- 4. Reglas como equipo ----------
A("## 4. Nuestras reglas como equipo (16)")
A("")
reglas = [
 "Conducta y comportamiento **cristiano** antes, durante y después del ETC.",
 "Cada quien es responsable de lo asignado (testimonios, dinámicas, materiales).",
 "**Obedecer a los directores.** Los complejos de superioridad se quedan en casa.",
 "Traer reloj. Evitar celulares y cámaras (según se acuerde).",
 "Tareas terminadas antes de que lleguen los participantes.",
 "Promover amistad desde la llegada: conversar, animar, dar la bienvenida.",
 "Ser guías cuando los participantes se mueven — respetar el horario.",
 "Estar preparados con conversaciones para los pequeños grupos.",
 "Escribir palancas a **todos** los miembros de su pequeño grupo.",
 "Poner las necesidades propias de último — **el ETC es del participante, no del guía.**",
 "Mantener limpia el área del PG y los baños. Seguir en contacto con el PG después.",
 "**La cocina está en función del ETC, no el ETC en función de la cocina.**",
 "Amor en la comunicación y buenas maneras, antes/durante/después.",
 "Máximo **3 ausencias** justificadas en reuniones.",
 "Presencia **obligatoria** en el Ensayo General.",
 "Somos instrumentos de la gracia — ponerse en manos del Señor.",
]
for i,r in enumerate(reglas,1): A(f"{i}. {r}")
A("")
A("---")

# ---------- 5. Responsabilidades por rol ----------
A("## 5. Responsabilidades por rol (resumen)")
A("")
A("**Directores:** escogen y forman al equipo · planifican reuniones equilibradas · velan el horario · cuidan que no haya hermanos/pareja de un miembro en un mismo plenario · oran antes de decidir · *un solo equipo con diferentes funciones*.")
A("")
A("**Asesores:** apoyan con experiencia · aclaran dinámicas · ayudan a preparar testimonios · enlace entre Dirección y Cocina · organizan oraciones y palancas · conciliadores. **Frank** lleva además el **Banderín**.")
A("")
A("**Asesores Espirituales (Paul + Sor Angelina):** acompañan **todo el proceso** (transversales) · presiden/animan la liturgia · cadena de oración · Proyecto Esperanza.")
A("")
A("**Guías:** trabajo cara a cara con el participante · preparan y dan testimonio · libretas y decoración del PG · se aprenden el horario · palanca a cada participante · confidencialidad · ejemplo de vida sacramental.")
A("")
A("**Cocina:** unidad y armonía · sencillez en comidas y motivos · presupuesto y donaciones · menú · bendiciones breves ligadas al tema · **Lavatorio** en la cena del sábado · ejemplo en el servicio.")
A("")
A("**Música:** amenizan los 3 días · cancionero · **oración Sal y Luz «Bayuyo»** (antifaces) · música al despertar · cantos de la misa de clausura · oración a María del sábado · **canción de despedida** · apoyo a todas las áreas desde el jueves previo.")
A("")
A("---")

# ---------- 6. Cómo preparar un testimonio ----------
A("## 6. Cómo preparar un testimonio")
A("")
A("*Sé descriptivo: esto es para que cualquiera entienda cómo hacerlo. Los que ya han servido dan el ejemplo primero.*")
A("")
A("1. Empieza con un **bosquejo** de ideas generales.")
A("2. **Simple:** una idea central, lenguaje claro y llano.")
A("3. No repitas, no aburras.")
A("4. Comparte una **experiencia personal ya superada** (no algo en lucha actual).")
A("5. **No prediques** ni des clase — comparte momentos.")
A("6. Actitud **positiva**: evita criticar y el negativismo. Inculca la alegría de saberse amado por Dios.")
A("7. Demuestra entusiasmo. Exprésate como eres (dentro de lo decente).")
A("8. Proyecta la voz, habla despacio, **contacto visual** — **no leas** el papel.")
A("9. Opcionales: una canción, diapositiva, póster, silencio.")
A("10. **Prepáralo con tiempo y en oración.** Si los nervios te bloquean: silencio, oración, y ponte en manos de Dios.")
A("")
A("---")

# ---------- 7. Los 9 testimonios ----------
A("## 7. Los 9 testimonios del retiro")
A("")
A("Confianza · Singularidad · Libertad para Aceptar · Libertad para Entregarse · Regalo de la Vida · Perdón · Nacer de Nuevo · Compromiso · Cuarto Día.")
A("")
A("*(En la temática de expedición: confiar en el capitán, cada tripulante único, aceptar la travesía, soltar lastre, la vida como tesoro, sanar heridas, llegar a tierra nueva, sostener el rumbo, la expedición continúa.)*")
A("")
A("---")

# ---------- 8. Horario del retiro ----------
A("## 8. Horario del retiro (resumen)")
A("")
A("**Viernes:** llegada cocina (10am) · llegada equipo (3pm) · llegada participantes (6pm) · plenario, bienvenida y reglas (6:30) · dinámicas rompehielo · formación de pequeños grupos · cena · dinámica del tiempo/tarjeta · **testimonio Confianza y Singularidad** · dinámica del abrigo · oración Bayuyo · descanso.")
A("")
A("**Sábado:** oración mañana · desayuno · **Libertad para Aceptar** + dinámica del alambre de la fe · sociodrama · **Libertad para Entregarse** · almuerzo · **entrega de palancas** + Biblia · **Regalo de la Vida** · sociodramas · **cena con Lavatorio** · **Perdón** + dinámica del lodo · **confesiones + carta de compromiso** · preparar misa y banderín.")
A("")
A("**Domingo:** oración · recoger la casa · desayuno · **Nacer de Nuevo y Compromiso** · dinámica del cariño (último PG) · **Cuarto Día** · evaluación · almuerzo · **Eucaristía + entrega de los peces** · salida.")
A("")
A("---")

# ---------- 9. Glosario ----------
A("## 9. Glosario eteciano")
A("")
A("- **Palanca:** carta/oración de apoyo que se escribe a participantes y compañeros.")
A("- **PG (Pequeño Grupo):** grupo de 6–7 participantes con sus guías.")
A("- **Plenario:** reunión de todos en el salón principal.")
A("- **Banderín:** estandarte/insignia del retiro (lo coordina Frank + 2 guías).")
A("- **Bayuyo:** oración «Sal y Luz del Mundo» del viernes en la noche (con antifaces).")
A("- **Padrino/Madrina:** quien apoya espiritual o económicamente a un participante.")
A("- **Correcaminos:** rol vehicular de apoyo a cocina (compras/diligencias).")
A("- **4º Día:** la vida después del retiro — el ETC en realidad ahí comienza.")
A("- **Profondo:** actividad de recaudación de fondos del equipo.")
A("")
A("---")
A(f"*Guía ETC LXXXVIII · {d['meta']['version']} · generada del Tablero de la Tripulación. El lema y el branding se confirman esta semana.*")

txt = "\n".join(L)
open(f'{_R}/GUIA_ETC88.md','w').write(txt)
print(f"Wrote GUIA_ETC88.md ({len(txt)} chars, {len(L)} líneas)")
