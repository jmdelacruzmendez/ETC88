# RIFA ETC 88 — Concepto, factibilidad y parámetros (DOCUMENTO DE TRABAJO)

> **Estatus:** ideación. Esto NO es entregable de Drive ni hecho cerrado. Recoge ideas,
> lo ya decidido y los parámetros abiertos para que el director los cierre. Cuando un
> dato se confirme, va a `data/estado.json` y se regenera por el pipeline — no se edita a mano.

## 0. Punto de partida (ya confirmado en `data/estado.json` → `rifa_profondo`)
- **600 boletos × RD$200** = RD$120,000 bruto.
- **Premio: RD$30,000** → **meta neta RD$90,000** para la caja.
- **Sorteo: agosto 2026** · probabilidad estimada 50%.

⚠️ **Ventana de tiempo:** sorteo en agosto → quedan ~6–8 semanas de venta. Favorece una
solución ligera frente a una app web completa.

## 1. Qué queremos del aplicativo (idea del director)
1. Emitir **boletos electrónicos** con **identificador + número por vendedor**.
2. **Modelo mixto**: boletas físicas y digitales conviviendo en un mismo sorteo.
3. La **venta digital** se paga por **transferencia bancaria (fuera del app)**; al confirmarla
   se **envía el boleto** (imagen / código / QR).
4. **Control y monitoreo** de ventas.
5. **Sorteo final** combinando físicas y digitales (las físicas pueden llevar identificador
   también, aunque encarece la impresión).

## 2. Modelo conceptual (entidades a rastrear)
| Entidad | Campos clave |
|---|---|
| **Boleto** | número único · tipo (físico/digital) · identificador/serie de vendedor · estado (`disponible → asignado → pagado → anulado`) |
| **Vendedor** | código + nombre + rango de números asignados (= "número por vendedor") |
| **Comprador** | nombre + WhatsApp (opcional) |
| **Pago** | medio (transferencia/efectivo) · referencia · comprobante · quién confirmó · fecha |
| **Sorteo** | pozo = boletos `pagados` (físicos + digitales) · número ganador verificable |

**Regla de oro de numeración:** un solo espacio global **001–600** particionado en **series
por vendedor** (ej. Vendedor A = 001–050, B = 051–100…), para que físicos y digitales caigan
en el mismo sorteo **sin colisión de números**.

## 3. Flujo de venta digital
```
acuerdo de compra
   → comprador hace TRANSFERENCIA BANCARIA (fuera del app)
   → un humano CONFIRMA el pago (revisa banco / comprobante)
   → se GENERA el boleto (imagen + QR) y se ENVÍA por WhatsApp
   → queda registrado como "pagado" en el control
```
> Realidad: nadie integra una pasarela bancaria para una rifa. El aplicativo automatiza
> **generación + registro + monitoreo**, NO el cobro. La confirmación de pago es **manual**.

## 4. Control y monitoreo
Tablero con: vendidos vs meta (600) · recaudado vs RD$120k · ranking por vendedor · físicos
vs digitales · pendientes de cobro. Encaja con la infraestructura existente
(`data/*.json` → `scripts/build_*.py` → CSV + tablero Alpine.js/Chart.js).

## 5. El sorteo
- **Pozo = solo boletos VENDIDOS (pagados).** *(decidido — imposible que gane uno no vendido)*
- Número ganador **verificable**: a definir (atado a Lotería Nacional / sorteo en vivo /
  función reproducible con semilla pública).
- El identificador en los físicos sirve para **validar al ganador**.

## 6. Factibilidad — dos caminos
| | **Camino A — Tracker generado (ligero)** | **Camino B — App web completa** |
|---|---|---|
| Qué es | `data/rifa.json` + `scripts/build_rifa.py` → boletos con QR + CSV de control + tab en el tablero | Sistema aparte: backend, login de vendedores, subida de comprobante, envío automático |
| Pago / envío | Manual (humano confirma; reenvía por WhatsApp) | Semi-automatizado |
| Costo / tiempo | Días · sin servidor · sin costo · lo opera cualquier asesor con Python | Semanas · hosting + BD + auth + mantenimiento |
| Encaja con el repo | ✅ Patrón exacto (ver `scripts/build_captacion.py` + `data/participantes.json`) | ❌ |
| Realista para agosto | ✅ | ⚠️ riesgo alto |

**Recomendación (sin cerrar):** Camino A. Librerías a sumar: `qrcode` + `Pillow`.

## 7. Decisiones tomadas
- ✅ **Entrega del boleto digital → WhatsApp** (genera imagen/QR; un humano la reenvía).
- ✅ **Sorteo → solo entran los boletos vendidos.**

## 8. Parámetros aún por definir (cerrar con el director)
- [ ] **Camino técnico**: A (ligero) vs B (app web) vs híbrido.
- [ ] **Split físico vs digital** de los 600.
- [ ] **Quiénes venden** (¿los 56 del equipo? ¿cantera/padrinos?) y **cuántos números c/u**.
- [ ] **QR en boletas físicas**: sí (rastreable/anti-fraude, +costo impresión) vs no.
- [ ] **Quién confirma pagos** (tesorero central vs cada vendedor) y **cuenta bancaria** destino.
- [ ] **Método del sorteo** (Lotería Nacional / en vivo / semilla reproducible).
- [ ] **Diseño del boleto** (branding aún `[POR DEFINIR]`; iría a Claude Design / Adobe Express).

---
*Fuente: ideación con el director, 29-jun-2026. Cifras base citadas de `data/estado.json` → `rifa_profondo`.*
