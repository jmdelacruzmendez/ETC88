> **DOCUMENTO DE TRABAJO — no es entregable oficial.** Encuadre de una sesión aparte. Aún NO está construido el modelo; aquí queda el alcance y los insumos.

# Modelo de flujo de caja + asignación de entradas — ETC 88 (sesión aparte)

El presupuesto actual (hoja Finanzas) dice **cuánto cuesta** y **de dónde sale** (cuotas + rifa/comida + donaciones). Lo que falta —y el director pidió como **sesión aparte**— es el **flujo de caja**: *cuándo* entra cada peso, *cuándo* hay que pagar cada compromiso, y **a qué se destina cada entrada**, para no caer en negativo antes de una fecha de pago.

## Qué va a producir esa sesión
Una **hoja de tesorería** con, por fecha:
- **Entradas** (con su fuente): cuotas mensuales del equipo, cuotas de participantes, neto de la rifa (al cerrar), Profondo #2, donaciones (cuando lleguen).
- **Salidas** (con su compromiso): abonos a la casa, transporte, compras de cocina, materiales/litúrgico, formaciones, **camisetas**, **avanzada del jueves**.
- **Saldo acumulado** (arranca en **−$23,600**, la deuda al Consejo).
- **Asignación / earmark:** a qué compromiso queda destinada cada entrada (ej.: rifa → saldo de la casa; cuotas del equipo → comida + avanzada; donaciones en especie → canasta de cocina).
- **Alertas de liquidez:** fechas donde el saldo se acercaría a 0 o negativo antes de un pago.

## Insumos que necesito para construirlo (lo que hay que cerrar antes)
- **Calendario de pagos reales:** ¿cuándo vence el/los abono(s) a la casa? ¿cuándo se paga transporte, compras grandes de cocina, materiales? ¿la casa pide depósito y saldo, en qué fechas?
- **Calendario de ingresos:** fechas de cobro de cuotas (¿mensual jun–sep?), cierre de la rifa (≈2-ago), cuándo se esperan donaciones.
- **Montos que estemos cerrando:** cuota final del equipo, # de participantes (para completar 100), tarifa de la avanzada, costo real de camisetas.
- **Política de asignación:** qué entrada se destina a qué compromiso (lo define el director).

## Cómo lo construiríamos (sin inventar)
- Sale de `data/estado.json` (hechos confirmados) + la hoja Finanzas (estimados a validar).
- Un generador nuevo `scripts/build_flujo.py` → pestaña/hoja de tesorería; pasa por `verify.py`.
- Nada se presenta como decidido salvo lo que esté `confirmado`; lo demás, `[PROPUESTA]`/`[POR DEFINIR]`.

## Relacionado (ya agregado al presupuesto en esta ronda)
- **Camisetas del equipo:** línea estimada (~56 × est.); tallas parciales en la pestaña *Camisetas* de la hoja Finanzas; faltan invitados pendientes + Paul, Frank y la Sor; mockup tras el Design System.
- **Avanzada del jueves (3-sep):** línea estimada = porción de casa (noche/día extra) + desayuno/almuerzo/cena del equipo que adelanta; **confirmar tarifa con la casa**.
