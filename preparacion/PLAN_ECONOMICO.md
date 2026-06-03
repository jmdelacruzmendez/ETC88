> **DOCUMENTO CONSOLIDADO (3-jun-2026).** Único documento económico del ETC 88: ecuación, presupuesto itemizado, brecha de materiales, recaudación, flujo de caja y optimización. Fusiona `MODELO_FLUJO_CAJA`, `BRECHA_PRESUPUESTO_MATERIALES` y el presupuesto itemizado (ahora stubs). Acompaña a `Finanzas_ETC88.xlsx` (12 pestañas) + `Flujo_Caja_ETC88.xlsx` (5 pestañas).
>
> Cifras: **[DATO]** = confirmado en `estado.json` · **[ESTIMADO]** = hoja Finanzas, a validar en F1 · **[ESCENARIO]** = supuesto del modelo, se ajusta · **[PROPUESTA]** = sin decidir.

# Plan Económico ETC 88
### Presupuesto · Recaudación · Flujo de caja · Optimización

## 1. La ecuación (lo primero que hay que entender)
**COSTO TOTAL = CUOTAS + RECAUDACIÓN VARIABLE.**

| Concepto | Monto (RD$) | Fuente |
|---|---:|---|
| **Costo total a cubrir (META)** | **≈ 583,281** | [DATO] · se recalcula con el presupuesto |
| — de la casa (200,000), $23,600 es la deuda al Consejo | (200,000) | [DATO] · la deuda **NO** se suma aparte: ya está dentro de la casa |
| (–) Cuotas participantes (~52 × $3,000) | 156,000 | [ESTIMADO] |
| (–) Cuotas equipo (48 × $1,500–2,000) | 72,000 – 96,000 | [PROPUESTA] |
| **(=) BRECHA: rifa + venta de comida + donaciones** | **≈ 331,281 – 355,281** | lo que la recaudación variable debe levantar |

> La meta **no es un número inventado**: es el costo. Las cuotas cubren sobre todo la casa; **la rifa, la venta de comida y las donaciones cubren la brecha**.

## 2. Presupuesto por partida (itemizado)
Los 3 críticos se financian primero; el resto es ajustable a la baja. Cada coord refina su línea en F1 sin pasar su tope.

| Partida | Estimado (RD$) | Nota |
|---|---:|---|
| **Casa de retiro** (100 personas, con exención) | 200,000 | [DATO] · 1.er crítico |
| **Transporte** | 77,500 | [ESTIMADO] · 2.º crítico · 3 cotizaciones pendientes |
| **Cocina** (canasta + meriendas) | 82,166 | [ESTIMADO] · 3.º crítico · baja con donaciones en especie |
| **Materiales y litúrgico** (ver §2b) | 88,500 | itemizado abajo |
| **Guías / PG** (libretas, materiales) | 17,000 | libretas van aquí, no en cocina |
| **Música** | 4,500 | casa tiene sonido → solo respaldo |
| **Eventos formativos** (5 formaciones) | 16,315 | |
| **Camisetas del equipo** | 22,000 | solo equipo |
| **Imprevistos + avanzada** | ~30K–47K | 5–8% del total |

### 2b. Materiales y litúrgico — itemización (lo que la guía exige)
| Ítem | Cálculo | RD$ |
|---|---|---:|
| Peces (entrega en la clausura) | 48 × $715 | 34,320 |
| Biblias (entrega sábado) | 48 × $500 | 24,000 |
| Ofrenda a 4 confesores | 4 × $2,000 | 8,000 |
| Vino + formas/hostias | — | 3,300 |
| Cofre de palancas + monedas de chocolate | — | 3,000 |
| Carnets / porta-ID + impresión | — | 2,000 |
| Alambre · cartulinas · marcadores · sobres · tape | — | 5,000 |
| Impresión del horario grande | — | 1,500 |
| Rosarios | 48 × $50 | 2,400 |
| **Banderín** (tela, asta, deco) | a cotizar | 5,000 |

> El presupuesto completo (12 pestañas) está en **`Finanzas_ETC88.xlsx`**. **Antifaces NO se incluyen** (la temática no está cerrada; el banderín sí).

## 3. La brecha de materiales — RESUELTA (registro del hallazgo)
- **Hallazgo original:** el presupuesto v2 estaba a nivel de **categoría** ("Guías Materiales" y "Misceláneos" eran cajas negras), y por eso no se veía si cubría lo que la guía exige (rosarios, banderín, ofrenda confesores, palangana del Lavatorio…).
- **Resuelto:** la hoja Finanzas está **itemizada** e incluye todas las líneas que faltaban (§2b).
- **Banderín:** era obligatorio (sábado noche) y **no tenía línea** → agregado (~$3–6K, a cotizar).
- **Casa incluye gas y limpieza** [DATO] → se eliminaron limpieza (~$9,600) y gasoil de planta (~$3,600) = ahorro ~$13,000.
- **Por confirmar con cocina:** ¿se paga señora/o de cocina local? · arroz/habichuelas/aceite (el 79 los consiguió donados del Padre Paul).

## 4. Recaudación y donaciones (5 fuentes / 5 auxiliares)
- **Cuotas (lo más estable):** participantes $3,000 [DATO] · equipo $1,500–2,000 [PROPUESTA].
- **Rifa (Profondo #1 · equipo Actividad Profondo)** — primera actividad [DATO]; **palanca #1**. Premio donado = casi todo neto.
- **Venta de comida (Profondo #2).**
- **Donaciones (equipo Recaudación):** en **efectivo** (empresas/particulares — responsabilidad de Directores, delegable) · en **especie** (arroz, habichuelas, aceite → bajan el costo de cocina, no entran como efectivo).
- **Intersección (diáspora):** etecianos del 88 fuera del país + comunidad amplia → padrinazgo, donaciones desde el exterior, red de oración.
- **Finanzas / Tesorería [POR DEFINIR responsable]:** no recauda; **vigila el flujo**, concilia y lleva la pizarra.

## 5. Flujo de caja (mes a mes) — arranca en –$23,600 (la deuda)
**Entradas:**
| Mes | Entrada principal | Quién | Riesgo |
|---|---|---|---|
| jun | Cuotas equipo (3 × $500 desde F1) | Tesorería | bajo |
| jul | F3 = arranca cobro participantes + 2da cuota equipo | Tesorería + coords | **medio** (depende de invitaciones) |
| **ago** | **Rifa (cierre 31-jul→2-ago) + 3ra cuota** + 1er bloque donaciones | Profondo + Recaudación + diáspora | **alto** (palanca grande) |
| sep | Saldo cuotas + donaciones + venta comida | Recaudación + cocina | medio |

**Salidas:**
| Mes | Salida grande | Mitigación |
|---|---|---|
| jun | Deuda Consejo ($23,600) + materiales F1 | apropiar a la 1ra ronda de cuotas |
| jul | Compras anticipadas cocina + cotizaciones transporte | pagar solo si el saldo del mes lo aguanta |
| ago | Camisetas + litúrgicos (peces, biblias, banderín) | **espera a la rifa**; usa el neto de agosto |
| sep | **Saldo casa + transporte + avanzada** — la peor concentración | pre-pago si llegan donaciones; si no, esperar al 30-ago |

**Lectura:** el saldo se aprieta al inicio (la deuda) y **depende de que la rifa (ago) y las cuotas entren ANTES** de los pagos grandes de septiembre.

**5 reglas de tesorería (las aplica Finanzas/Tesorería):**
1. **No comprometer un pago grande si el saldo del mes no lo aguanta.**
2. **Earmark:** cada entrada se etiqueta para un compromiso ([POR DEFINIR la política].
3. **Imprevistos = 5–8%** reservados (~$30K–47K) — no se tocan salvo emergencia.
4. **Cierre semanal del saldo** desde F3 (5-jul), publicado en el seguimiento.
5. **2 cierres parciales de rifa** (mediados + final de jul) para detectar a tiempo si no llega a meta.

## 6. Optimización (palancas para reducir/cerrar la brecha, por impacto)
1. **Mantener la exención** de la casa → ahorra ~$30,000 [DATO].
2. **Premio de la rifa donado** → sube el neto de la palanca #1.
3. **Donaciones en especie para cocina** → –$15K a –$25K [ESCENARIO].
4. **Topes en F1** sobre materiales y cocina → –$15K a –$25K.
5. **Cuota del equipo al tope** ($2,000 vs $1,500) → +$24,000 [PROPUESTA, 48 personas].
6. **Donaciones en efectivo** → cada peso baja la brecha (Directores).

## 7. Cómo se presenta a los coordinadores (3 min)
1. "El retiro cuesta **~$583K**. Las cuotas cubren **~$240K** (sobre todo la casa)."
2. "Falta **~$331K–355K**: lo levantan **rifa + comida + donaciones + diáspora**. Por eso la rifa es lo primero."
3. "Cada área tiene un **tope**; en F1 lo refinan **a la baja**. Casa, transporte y comida se pagan primero."
4. "El **flujo de caja** manda: la rifa (ago) entra antes de los pagos de septiembre."

## 8. Pendientes para cerrar el modelo (insumos reales)
- **Fechas de pago** de la casa (abono/saldo), transporte y compras grandes de cocina.
- **Fechas de ingreso** de cuotas, cierre de rifa, donaciones.
- **Cuota final** del equipo + **conteo de participantes** (fija las cuotas exactas).
- **Tarifa de la avanzada** + costo real de camisetas + **cotización del banderín**.
- **Política de earmark** (qué entrada cubre qué) — la decide el director.
- **Nombrar Tesorería** — sin responsable, el modelo no opera.
