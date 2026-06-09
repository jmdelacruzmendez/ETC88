#!/usr/bin/env python3
"""
Genera archivo .vcf (vCard) con los contactos del equipo ETC 88 para importar al
teléfono y crear listas de difusión de WhatsApp.

Lee data/equipo.json. Exporta los titulares con teléfono confirmado. Excluye
backups y contactos "Por confirmar".

Uso:
  python3 scripts/build_difusion.py

Salida:
  entrega_diseno/EQUIPO_ETC88.vcf   (importable a iOS/Android)
  entrega_diseno/EQUIPO_ETC88.csv   (referencia plana)

Cómo usar el .vcf (iOS):
  1. AirDrop / Email / iCloud → abrir el .vcf en el iPhone.
  2. Tocar "Añadir 50 contactos" (los etiqueta con prefijo "ETC88·").
  3. Abrir WhatsApp → Listas de difusión → Nueva → seleccionar contactos con
     prefijo "ETC88·" → Crear.

Cómo usar el .vcf (Android):
  1. Copiar el archivo al teléfono. Abrirlo desde Files / Contactos.
  2. Importar todos los contactos.
  3. WhatsApp → ⋮ → Nueva difusión → seleccionar contactos.
"""
import json
import csv
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EQUIPO = json.load(open(REPO / 'data/equipo.json', encoding='utf-8'))

def format_tel(t):
    if not t:
        return ''
    digits = re.sub(r'\D', '', str(t))
    if len(digits) == 10:           # 8298083399 → +1 829 808 3399
        digits = '1' + digits
    return '+' + digits if digits else ''

def vcf_entry(nombre, tel, area):
    prefijo = f'ETC88·{area_label(area)}'
    full = f'{prefijo} {nombre.strip()}'.replace('"', '')
    return (
        'BEGIN:VCARD\r\n'
        'VERSION:3.0\r\n'
        f'N:{nombre.strip()};;;;\r\n'
        f'FN:{full}\r\n'
        f'TEL;TYPE=CELL:{tel}\r\n'
        f'NOTE:Equipo ETC 88 · {area_label(area)}\r\n'
        'END:VCARD\r\n'
    )

def area_label(a):
    return {
        'directores': 'Dir',
        'asesores': 'Asesor',
        'asesores_espirituales': 'AsesorEsp',
        'guias': 'Guía',
        'cocina': 'Cocina',
        'musica': 'Música',
        'asesores_cocina': 'AsesorCoc',
        'asesores_diocesanos': 'AsesorCom',
    }.get(a, 'Equipo')

titulares = [p for p in EQUIPO['equipo'] if not p.get('backup')]
con_tel = []
for p in titulares:
    tel = format_tel(p.get('telefono'))
    if not tel:
        continue
    con_tel.append((p['nombre'].strip(), tel, p.get('area', '')))

out_vcf = REPO / 'entrega_diseno/EQUIPO_ETC88.vcf'
out_csv = REPO / 'entrega_diseno/EQUIPO_ETC88.csv'

with open(out_vcf, 'w', encoding='utf-8') as f:
    for nom, tel, ar in con_tel:
        f.write(vcf_entry(nom, tel, ar))

with open(out_csv, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Nombre', 'Área', 'Teléfono'])
    for nom, tel, ar in con_tel:
        w.writerow([nom, area_label(ar), tel])

print(f'Wrote {out_vcf} ({len(con_tel)} contactos)')
print(f'Wrote {out_csv}')
