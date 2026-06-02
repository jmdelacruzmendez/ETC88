# TRAZABILIDAD ETC 88 — registro de hechos, fuentes y estados

> Generado desde `data/estado.json` + `data/equipo.json`. Todos los entregables se generan
> de estas dos fuentes; `verify.py` bloquea cualquier desvío. Trazabilidad por construcción.

**Resumen:** 31 confirmados · 7 propuestas · 3 pendientes (en estado.json).

## Roster (data/equipo.json · generado del formulario)
- Total 56 · operativos titulares 47 · vacantes 1 · backups 3.
- Por área (operativos): asesores 3 · asesores_espirituales 2 · cocina 20 · directores 2 · guias 14 · musica 6

## ✅ Confirmados (se pueden mostrar como hecho)
| Campo | Valor | Fuente | Nota |
|---|---|---|---|
| `retiro.numero` | 88 | director |  |
| `retiro.romano` | LXXXVIII | director |  |
| `retiro.fechas` | 4–6 de septiembre de 2026 | director |  |
| `retiro.lugar` | Casa de Retiro La Ceiba del Salado, Higüey | director |  |
| `retiro.co_direccion` | ["Juan Manuel de la Cruz", "Jean Carlo de la Cruz"] | director |  |
| `reglas.parejas_guias` | 7 | director | REGLA: 7 parejas de guías (14 guías). No hay más ni menos parejas. Lo … |
| `finanzas.casa_por_persona_sin_exencion` | 2300 | director |  |
| `finanzas.casa_por_persona_con_exencion` | 2000 | director | Vía RNC de la parroquia del Padre Paul. Diferencia: $300/persona. |
| `finanzas.casa_incluye` | gas y limpieza | director |  |
| `finanzas.casa_tiene_sonido` | True | director | Música solo lleva equipo de respaldo. |
| `finanzas.deuda_inicial` | 23600 | director | 10% de reserva de la casa (pagado 5-mar por Juan Manuel; ya le fue dev… |
| `finanzas.cuota_participante` | 3000 | director |  |
| `finanzas.personas_casa_piso` | 100 | director | Piso fijado: completar 100 personas en la casa de retiro. |
| `finanzas.meta_recaudacion_total` | 583281 | director | No es un número fijo: = costo total estimado a cubrir (casa 100 person… |
| `recaudacion.primera_actividad_es_rifa` | True | director | Profondo #1 = rifa, primera actividad, por recomendación del equipo. |
| `recaudacion.modelo` | cuotas + rifa y/o venta de comida + donaciones | director | La meta = el costo total del retiro. Se cubre con: cuotas de participa… |
| `recaudacion.donaciones_responsable` | Directores (delegable) | director | Conseguir donaciones a empresas/particulares es responsabilidad de los… |
| `marca.lema_eteciano` | Siempre amigos | asociación |  |
| `equipos_auxiliares[3].responsable` | Asesores Espirituales (Padre Paul + Sor Angelina) | — |  |
| `comunidades_y_parroquias.parroquia_spm` | San José Obrero (SPM) | director | Parroquia de referencia en SPM (misas etecianas y posibles actividades… |
| `comunidades_y_parroquias.parroquia_pc` | Nuestra Señora del Pilar (Punta Cana) | director | Parroquia en PC con representación del 88 en el equipo; aún no se han … |
| `comunidades_y_parroquias.etecianos_pc_en_88` | ["Candy Elizabeth Gatwood Ramos", "Dorian Elina Rodriguez Be… | data/equipo.json (residencia=Punta Cana) | Etecianos del 88 residentes en Punta Cana — base natural para activar … |
| `comunidades_y_parroquias.liga_softball_etecianos` | Equipo/liga de softball de etecianos que ya se reúne y juega | director | Actividad existente de la comunidad eteciana — potenciable para profon… |
| `asesores_externos.cocina` | ["Mary \"Petra\" Morales", "Johanny García"] | director |  |
| `asesores_externos.comunidad_sd` | ["Marleny", "Sandrita"] | director | 2 representantes (asesores) de la comunidad de Santo Domingo. |
| `asesores_externos.comunidad_la_vega` | ["Leticia González"] | director | 1 representante (asesor): Leticia González. |
| `calendario_hitos.reunion_coordinadores` | jueves 4-jun (Corpus Christi, virtual) | coordinadores |  |
| `calendario_hitos.convivencia` | 22-ago · inicia con miniretiro / reflexión · día completo | director |  |
| `calendario_hitos.ensayo_general` | 23-ago · asistencia obligatoria | director |  |
| `calendario_hitos.inicio_recaudacion` | F3 · primera formación de julio (5-jul) | director | La recaudación de cuotas inicia en la 1ra formación de julio. El miemb… |
| `calendario_hitos.profondo1_fechas` | 31-jul → 2-ago | calendario | Rifa (Profondo #1); el neto entra a inicios de agosto. |

## 🟡 Propuestas (sin cerrar — se muestran [PROPUESTA]; OJO con la fuente)
| Campo | Valor | Fuente | Nota |
|---|---|---|---|
| `finanzas.cuota_equipo` | {"total_rango": "1,500 – 2,000", "mensual": 500, "cubre": "c… | director (planteado, sin cerrar) | NO está decidido. Mostrar primero los costos estimados del retiro para… |
| `finanzas.participantes_objetivo` | 53 | derivado (100 − 47 operativos) | Los que falten para completar 100 en la casa junto al equipo. Ajustar … |
| `marca.lema_retiro` | No fuimos a buscarlo: Él nos esperaba | propuesta Claude | Lema específico del ETC 88 SIN confirmar. |
| `marca.tematica` | expedición / búsqueda de tesoro | propuesta Claude | Dirección temática a confirmar. El branding se reconstruye desde 0 con… |
| `equipos_auxiliares[0].responsable` | Co-Dir + Coords de cocina + Roberto | — |  |
| `equipos_auxiliares[1].responsable` | Producción | — |  |
| `equipos_auxiliares[2].responsable` | Directores | — |  |

## 🔴 Pendientes (faltan — se muestran [POR DEFINIR])
| Campo | Valor | Fuente | Nota |
|---|---|---|---|
| `marca.branding_reglas_esteticas` | None | — | Las reglas estéticas NO están definidas. Se trabajan con Claude Design… |
| `calendario_hitos.fecha_limite_cotizar_transporte` | None | director | El director pidió fijar una fecha límite para cotizar transporte, bibl… |
| `calendario_hitos.asignacion_entradas` | None | director | Política de earmark (qué entrada se destina a qué compromiso). Se revi… |

## Decisiones confirmadas (lista del director)
- Retiro ETC 88: 4–6 de septiembre de 2026, Casa de Retiro La Ceiba del Salado, Higüey.
- Co-dirección: Juan Manuel de la Cruz y Jean Carlo de la Cruz.
- Casa: $2,300/persona sin exención · $2,000/persona con exención (RNC parroquia del Padre Paul). Incluye gas y limpieza. Tiene sonido.
- Deuda inicial: $23,600 al Consejo Eteciano (10% reserva que Juan Manuel adelantó y ya le fue devuelto).
- Cuota de participante: $3,000.
- Frank Morales es asesor (como Laura y Tomás) y además lleva el Banderín.
- Padre Paul y Sor Angelina son Asesores Espirituales transversales (todo el proceso, no solo el retiro).
- Apellido de Leober: Soriano.
- Roselyn sale del equipo (2-jun); su cupo pasa a un varón.
- Los backups (Rodolfo Telémaco, Scarlett Nivar, Kamila Todd) NO son parte del equipo per se.
- Equipos auxiliares: Recaudación y Donaciones · Guagua (Transporte) · Actividad Profondo · Intersección (espiritual).
- Profondo #1 = rifa (primera actividad, por recomendación del equipo).
- Asesoras de cocina: Mary "Petra" Morales y Johanny García.
- Convivencia (22-ago) inicia con miniretiro/reflexión. Ensayo General (23-ago) es obligatorio.
- Reunión de coordinadores: jueves 4-jun (Corpus Christi, virtual).
- Piso de personas: completar 100 en la casa de retiro.
- La meta de recaudación = el costo total del retiro (se cubre con cuotas + rifa/venta de comida + donaciones).
- Santo Domingo: 2 asesores de comunidad, Marleny y Sandrita.
- La Vega: 1 asesor de comunidad, Leticia González.
- Nombres corregidos: Guido Maldonado · Fabelly Maciel Fabian Bello.

## Pendientes y decisiones por cerrar (lista del director)
- [ ] Cerrar el monto final de la cuota del equipo (propuesta: $1,500–2,000, $500/mes).
- [ ] Confirmar el conteo final de participantes para completar 100 en la casa.
- [ ] Completar la vacante de cocina (varón — candidato Randolph).
- [ ] Definir los responsables de cada equipo auxiliar.
- [ ] Lema del retiro, hilo espiritual y reglas estéticas/branding (se trabajan con Claude Design).
- [ ] Confirmar la exención de la casa con el Padre Paul.
- [ ] Fijar fecha límite para cotizar transporte, biblias y peces.
- [ ] Cotizar transporte (3 empresas) y el banderín.
- [ ] Modelo de flujo de caja: asignar cada entrada a un compromiso e ir costeando con el calendario de pagos (sesión aparte).
- [ ] Confirmar con la casa la tarifa de la avanzada (noche/día extra del equipo que adelanta el jueves) + sus 3 comidas.
- [ ] Completar las tallas de camiseta que faltan (invitados pendientes + Paul, Frank y la Sor); el mockup va tras el Design System.
