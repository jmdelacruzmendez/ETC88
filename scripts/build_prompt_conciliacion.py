#!/usr/bin/env python3
"""
Prompt de contenido para Claude Design: presentación "ETC 88 · Conciliación final" (12 láminas).
Solo contenido y jerarquía (títulos, cifras, tablas, visual sugerido). El diseño lo pone el design system
del ETC 88 en Claude Design. Cifras tomadas de los mismos datos y cálculos de scripts/build_conciliacion.py.
Salida: entrega_diseno/PROMPT_CLAUDE_DESIGN_CONCILIACION_88.md
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / 'scripts/build_conciliacion.py'
OUT = REPO / 'entrega_diseno/PROMPT_CLAUDE_DESIGN_CONCILIACION_88.md'

src = SRC.read_text(encoding='utf-8')
MARK = '# ══════════ HELPERS DE HOJA ══════════'
assert MARK in src
ns = {'__file__': str(SRC)}
exec(compile(src.split(MARK)[0], str(SRC), 'exec'), ns)
D = ns

def n(v):  # entero con separador de miles
    return f'{v:,.0f}'
def d(v):  # con centavos
    return f'{v:,.2f}'

ENTRADAS, SALIDAS, BALANCE = D['ENTRADAS'], D['SALIDAS'], D['BALANCE']
REAL, IMPUESTOS = D['REAL_CUENTAS'], D['IMPUESTOS']
COSTO, GRATIS = D['COSTO_ECON'], D['RECIBIDO_GRATIS']
ESPECIE, C_JUE, C_HOSP = D['ESPECIE_TOTAL'], D['CORTESIA_JUEVES'], D['CORTESIA_HOSP']
CORT = C_JUE + C_HOSP
PPTO, PERSONAS, FUENTES, AREAS, cruce = D['PPTO_11AGO'], D['PERSONAS'], D['FUENTES'], D['AREAS'], D['cruce']
esp = D['especie_tot']; HAB_T, HAB_TAR = D['HAB_TOTAL'], D['HAB_TARIFA']; CASA = D['CASA_TOTAL']
BASE_REC, PUNTUALES = D['BASE_REC'], D['PUNTUALES']
CUOTA_P, CUOTA_E = D['CUOTA_PARTICIPANTE'], D['CUOTA_EQUIPO']
COMIDA_PP = (90489 + esp['Cocina'] - 10300) / PERSONAS
PART_PEND = D['PART_ESPER'] - D['PARTICIP']
DON_FLAG = sum(m for _, _, m, _, f in D['donaciones'] if f == 'NOTA')
PROFONDO = D['PROFONDO']; P_BRUTO, P_COSTOS, P_NETO, P_ADIC, P_COBRAR = D['PROF_BRUTO'], D['PROF_COSTOS'], D['PROF_NETO_INFORME'], D['PROF_ADICIONAL'], D['PROF_POR_COBRAR']
P_BOL_PAG, P_ING_BOL, P_ING_COM = D['PROF_BOLETAS_PAG'], D['PROF_ING_BOLETAS'], D['PROF_ING_COMIDA']
EF_COCINA, EF_SALON = D['EFECTIVO_COCINA'], D['EFECTIVO_SALON']

fuentes_rows = '\n'.join(f'| {l.split(" (")[0].split(",")[0]} | {n(v) if float(v).is_integer() else d(v)} | {v / ENTRADAS * 100:.0f}% |' for l, v in FUENTES)
area_rows = '\n'.join(f'| {a} | {n(p11)} | {n(pag + don)} | {n(don)} | {n(pag)} | {pag + don - p11:+,.0f} |' for a, (p11, ps, pag, don) in AREAS.items())

md = f"""# Prompt para Claude Design · Presentación "ETC 88 · Conciliación final"

## Instrucción

Diseña una presentación de 12 láminas (16:9) con el design system del ETC 88. Es el cierre financiero del Encuentro Total con Cristo #88 y se presenta al Consejo Eteciano y al equipo. Tono sobrio, claro y agradecido por lo que se logró. Todo en español; cifras en RD$ con separador de miles y sin decimales, salvo donde se escriben con centavos. No cambies ninguna cifra ni el orden de las láminas. Cada lámina debe hacer evidente su mensaje con el dato, la comparación o la tabla; sin párrafos. Debajo va el contenido lámina por lámina con una sugerencia de visual.

## Lámina 1 · Portada

- Título: ETC 88 · Conciliación final
- Subtítulo: Encuentro Total con Cristo #88 · Casa La Ceiba del Salado, Higüey · 4–6 de septiembre de 2026
- Co-Dirección: Juan Manuel de la Cruz · Jean Carlo de la Cruz
- Pie: {PERSONAS} personas en la casa · cierre al 11 de septiembre de 2026

## Lámina 2 · El retiro en tres números

Tres cifras grandes, en este orden:

- Lo que costó el retiro: RD$ {n(COSTO)} (todo, incluido lo que otros pusieron)
- Lo que salió de caja: RD$ {n(SALIDAS)}
- Lo que quedó en cuentas: RD$ {n(REAL)}

Debajo, una sola línea: RD$ {n(GRATIS)} ({GRATIS / COSTO * 100:.0f}%) llegaron sin pasar por caja: 30 donantes en especie y las cortesías de la casa.

Visual: tres tarjetas; la diferencia entre la primera y la segunda resaltada como "lo que pusieron otros".

## Lámina 3 · Cómo se construyó

Cinco pasos encadenados, cada uno con su cifra como protagonista:

1. Registro de tesorería: 22 gastos · 49 donaciones · 8 entregas del profondo
2. Caja: entradas {d(ENTRADAS)} · salidas {n(SALIDAS)}
3. Cruce con el presupuesto oficial del 11 de agosto: {d(PPTO)} en {len(cruce)} partidas
4. Lo que no pasó por caja: donaciones en especie {n(ESPECIE)} + cortesías de la casa {n(CORT)}
5. {D['AUDIT_N']} verificaciones numéricas sobre el resultado

Visual: flujo horizontal de cinco pasos.

## Lámina 4 · De dónde salió el dinero

| Fuente | RD$ | % |
|---|---|---|
{fuentes_rows}
| Entradas totales | {d(ENTRADAS)} | 100% |

Debajo, en pequeño, el profondo abierto: {P_BOL_PAG:g} boletas pagadas × 200 = {n(P_ING_BOL)} + venta de comida y helados {n(P_ING_COM)} = {n(P_BRUTO)} brutos − premios {n(P_COSTOS)} (aire acondicionado y abanico) = {n(P_NETO)}; con las ventas de helados posteriores, {d(PROFONDO)} entregados.

Mensaje: participantes y donaciones aportaron por igual; el profondo fue la tercera fuente.

Visual: barras horizontales ordenadas de mayor a menor, con el porcentaje al final de cada barra.

## Lámina 5 · Presupuesto y costo, por área

| Área | Presupuestado | Costó | Cubierto sin pagar | Pagado de caja | Diferencia |
|---|---|---|---|---|---|
{area_rows}
| Total | {d(PPTO)} | {n(COSTO)} | {n(GRATIS)} | {n(SALIDAS)} | {COSTO - PPTO:+,.0f} |

Costó = pagado de caja + cubierto sin pagar. Diferencia = costó − presupuestado.

Visual: la tabla completa; en cada área, una barra con dos tramos (pagado de caja y cubierto sin pagar) contra una marca del presupuesto.

## Lámina 6 · Lo que otros pusieron: RD$ {n(GRATIS)}

- Peces (símbolo del retiro), donados por La Vega: {n(esp['Directores'] - 2300 - 3000)}
- Cocina y decoración: {n(esp['Cocina'])}
- Materiales de guías (mochilas, rosarios, forros, libretas, impresiones, lapiceros): {n(esp['Guías'])}
- Insumos de misa: {n(3000)}
- Materiales de oficina: {n(2300)}
- Música (pilas, chocolates, alambre): {n(esp['Música'])}
- Cortesías de la casa: {n(CORT)} (8 personas la noche del jueves y 2 personas el fin de semana)

Visual: barras o tarjetas por rubro; el total {n(GRATIS)} = {GRATIS / COSTO * 100:.0f}% del costo del retiro como cifra grande.

## Lámina 7 · La casa

| Concepto | RD$ |
|---|---|
| Hospedaje: 97 personas × 2,360 (viernes a domingo) | {n(228920)} |
| Noche del jueves: 19 personas × 500 | {n(9500)} |
| Habitaciones para pequeños grupos: {n(HAB_TAR)} × 2 noches | {n(HAB_T)} |
| Total pagado (avance {n(23600)} + pago final {n(216620)}) | {n(CASA)} |
| Cortesía: 8 personas del jueves | {n(C_JUE)} |
| Cortesía: 2 personas el fin de semana | {n(C_HOSP)} |

Mensaje: fuimos {PERSONAS}, se pagaron 97. Frente al presupuesto (236,000), la casa costó {n(CASA - 236000)} más: la noche del jueves y las habitaciones de pequeños grupos.

Visual: tabla limpia; la línea del total destacada.

## Lámina 8 · Presupuesto y realidad

Tres cifras:

- Presupuesto oficial (11 de agosto): {n(PPTO)}
- Lo que costó el retiro: {n(COSTO)} ({(COSTO / PPTO - 1) * 100:+.1f}%)
- Lo que salió de caja: {n(SALIDAS)} ({(SALIDAS / PPTO - 1) * 100:+.1f}%)

Mensaje: el retiro costó un poco más de lo presupuestado y salió bastante menos de caja, porque uno de cada seis pesos lo puso alguien más.

Visual: tres barras (presupuesto, costo, caja) con la brecha entre costo y caja marcada como "lo que pusieron otros".

## Lámina 9 · Las cuentas cuadran

Cadena de cifras:

Entradas {d(ENTRADAS)} − Salidas {n(SALIDAS)} = Balance {d(BALANCE)} − Impuestos y comisiones bancarias {d(IMPUESTOS)} = En cuentas {n(REAL)}

Visual: cascada (waterfall) de izquierda a derecha, terminando en la cifra en cuentas.

## Lámina 10 · Por persona

- Costo de caja por persona ({PERSONAS}): {n(SALIDAS / PERSONAS)}
- Costo total por persona: {n(COSTO / PERSONAS)}
- Cuota de cada participante: {n(CUOTA_P)}, que cubre el {CUOTA_P / (SALIDAS / PERSONAS) * 100:.0f}% de su costo de caja
- Cuota de cada miembro del equipo: {n(CUOTA_E)} (49 miembros = {n(D['CUOTAS'])})

Visual: las cifras por persona y una barra que muestre la parte que cubre la cuota del participante y la parte que cubrieron donaciones, profondo y cuotas del equipo.

## Lámina 11 · Lo que queda por cerrar

- Efectivo de imprevistos ({n(15000)}): {n(EF_COCINA)} a cocina en la casa; confirmar que los {n(EF_SALON)} restantes fueron el reembolso del salón de formaciones.
- Participantes: {n(PART_PEND)} por cobrar entre cuatro personas; decidir si se cobra.
- Profondo: {n(P_COBRAR)} en boletas colocadas y no pagadas; decidir si se cobran.
- Donaciones sin identificar: {n(DON_FLAG)} en cuatro transferencias; dejar constancia.
- Uso de los {n(REAL)} en cuentas: decisión de la dirección y del Consejo.

Visual: lista de cinco puntos con una marca de estado por punto.

## Lámina 12 · Base y recomendaciones para el ETC 89

Cifras:

- Costo real del ETC 88: {n(COSTO)} ({n(COSTO / PERSONAS)} por persona)
- Base recurrente: {n(BASE_REC)} ({n(BASE_REC / PERSONAS)} por persona), sin el desvío de transporte ni el bizcocho de bienvenida
- Partidas por persona: casa 2,360 · comida {n(COMIDA_PP)} · biblia 680 · pez 600 · camiseta 480 por miembro del equipo

Recomendaciones, en tres bloques:

- Cerrar temprano: presupuesto cerrado 90 días antes, con la tarifa de la casa firmada y tres cotizaciones para transporte y comida; después solo cambia con el visto bueno de los dos directores.
- Tope: techo por área = costo real del 88 × asistentes; reserva de imprevistos del 3% con responsable, liquidada con recibos en una semana; nada fuera de partida sin mover otra.
- Logística: una sola caja desde el primer día; categorías iguales a las partidas; cada donación en especie anotada al recibirla; efectivos liquidados en 7 días; una línea por concepto; tesorería de tres personas (recibir, registrar, conciliar) con conciliación mensual; boletas del profondo cobradas antes del sorteo; cierre económico a los 10 días del retiro.

Visual: dos cifras grandes arriba, la fila de partidas por persona como iconos, los tres bloques de recomendaciones en columnas.
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(md, encoding='utf-8')
print(f'✓ Wrote {OUT} ({len(md.splitlines())} líneas)')
