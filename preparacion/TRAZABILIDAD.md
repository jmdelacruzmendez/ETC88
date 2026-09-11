# TRAZABILIDAD ETC 88 — registro de hechos, fuentes y estados

> Generado desde `data/estado.json` + `data/equipo.json`. Todos los entregables se generan
> de estas dos fuentes; `verify.py` bloquea cualquier desvío. Trazabilidad por construcción.

**Resumen:** 55 confirmados · 11 propuestas · 7 pendientes (en estado.json).

## Roster (data/equipo.json · generado del formulario)
- Total 56 · operativos titulares 48 · vacantes 0 · backups 3.
- Por área (operativos): asesores 3 · asesores_espirituales 2 · cocina 21 · directores 2 · guias 14 · musica 6

## ✅ Confirmados (se pueden mostrar como hecho)
| Campo | Valor | Fuente | Nota |
|---|---|---|---|
| `retiro.numero` | 88 | director |  |
| `retiro.romano` | LXXXVIII | director |  |
| `retiro.fechas` | 4–6 de septiembre de 2026 | director |  |
| `retiro.lugar` | Casa de Retiro La Ceiba del Salado, Higüey | director |  |
| `retiro.co_direccion` | ["Juan Manuel de la Cruz", "Jean Carlo de la Cruz"] | director |  |
| `reglas.parejas_guias` | 7 | director | REGLA: 7 parejas de guías (14 guías). No hay más ni menos parejas. Lo … |
| `reglas.participantes_solo_mayores` | True | director (3-jun) | El ETC 88 NO admite menores de edad como participantes. Por tanto NO e… |
| `reglas.camiseta_solo_equipo` | True | director (3-jun) | La camiseta es SOLO del equipo de servidores. Los participantes NO lle… |
| `finanzas.casa_por_persona_sin_exencion` | 2300 | director |  |
| `finanzas.casa_por_persona_con_exencion` | 2000 | director | Vía RNC de la parroquia del Padre Paul. Diferencia: $300/persona. |
| `finanzas.casa_incluye` | gas y limpieza | director |  |
| `finanzas.casa_tiene_sonido` | True | director | Música solo lleva equipo de respaldo. |
| `finanzas.deuda_inicial` | 23600 | director | 10% de reserva de la casa (pagado 5-mar por Juan Manuel; ya le fue dev… |
| `finanzas.cuota_participante` | 3000 | director · Presupuesto Maestro 14-jun-2026 | 1er + 2do pago. Cubre transporte/comida/casa/pez/biblia. NO cubre su c… |
| `finanzas.cuota_equipo` | {"total": 2000, "mensual": 500, "nota_plan_pago": "2,000 tot… | director · Presupuesto Maestro 14-jun-2026 | Confirmada en 2,000 (era propuesta 1,500–2,000). Cubre ensayo general … |
| `finanzas.personas_casa_piso` | 100 | director | Piso fijado: completar 100 personas en la casa de retiro. |
| `finanzas.meta_recaudacion_total` | 553622 | director · Presupuesto Maestro 14-jun-2026 | LADO A consolidado: subtotal operativo 503,293 + imprevistos 10% (50,3… |
| `recaudacion.modelo` | cuotas + actividad de recaudación + venta de comida + donaci… | director | La meta = el costo total del retiro. Se cubre con: cuotas de participa… |
| `recaudacion.donaciones_responsable` | Directores (delegable) | director | Conseguir donaciones a empresas/particulares es responsabilidad de los… |
| `marca.lema_eteciano` | Siempre amigos | asociación |  |
| `marca.lema_retiro` | Donde está tu tesoro, allí estará tu corazón | director | Lema del retiro ETC 88 confirmado por el director (Mt 6,21). El retiro… |
| `marca.hilo_espiritual` | El corazón y el tesoro (Mt 6,21): donde pongo mi tesoro, all… | director |  |
| `marca.tematica` | expedición · el tesoro y el corazón | director | Temática confirmada: la expedición es hacia adentro — la brújula del c… |
| `comunidades_y_parroquias.parroquia_spm` | San José Obrero (SPM) | director | Parroquia de referencia en SPM (misas etecianas y posibles actividades… |
| `comunidades_y_parroquias.parroquia_pc` | Nuestra Señora del Pilar (Punta Cana) | director | Parroquia en PC con representación del 88 en el equipo; aún no se han … |
| `comunidades_y_parroquias.etecianos_pc_en_88` | ["Candy Elizabeth Gatwood Ramos", "Dorian Elina Rodriguez Be… | data/equipo.json (residencia=Punta Cana) | Etecianos del 88 residentes en Punta Cana — base natural para activar … |
| `comunidades_y_parroquias.liga_softball_etecianos` | Equipo/liga de softball de etecianos que ya se reúne y juega | director | Actividad existente de la comunidad eteciana — potenciable para profon… |
| `asesores_externos.cocina` | ["Mary \"Petra\" Morales", "Johanny García"] | director |  |
| `asesores_externos.comunidad_sd` | ["Marleny", "Sandrita"] | director | 2 representantes (asesores) de la comunidad de Santo Domingo. |
| `asesores_externos.comunidad_la_vega` | ["Leticia González"] | director | 1 representante (asesor): Leticia González. |
| `calendario_hitos.reunion_coordinadores` | jueves 4-jun (Corpus Christi, virtual) | coordinadores |  |
| `calendario_hitos.misa_eteciana_7jun` | domingo 7-jun | ics | Misa Eteciana. |
| `calendario_hitos.formacion_1` | domingo 14-jun | ics | Primera Formación. |
| `calendario_hitos.clausura_etc87_la_vega` | domingo 21-jun | ics | Clausura del ETC 87 en La Vega. NO hay Formación este domingo. |
| `calendario_hitos.formacion_2` | domingo 28-jun | ics | Segunda Formación. |
| `calendario_hitos.formacion_3` | domingo 5-jul | ics + director | Tercera Formación. Inicio de recaudación de cuotas (el miembro paga to… |
| `calendario_hitos.misa_eteciana_12jul` | domingo 12-jul | ics | Misa Eteciana. NO hay Formación este domingo. |
| `calendario_hitos.formacion_4` | domingo 19-jul | ics | Cuarta Formación. Contemplar la lectura de perfiles. |
| `calendario_hitos.dia_del_padre` | domingo 26-jul | ics | Día del Padre. NO hay Formación este domingo. |
| `calendario_hitos.profondo_1` | viernes 31-jul → domingo 2-ago | ics | Actividad Profondo No. 01 (formato por definir por el director); el ne… |
| `calendario_hitos.misa_eteciana_9ago` | domingo 9-ago | ics | Misa Eteciana. NO hay Formación este domingo. |
| `calendario_hitos.convivencia` | domingo 16-ago | ics | Convivencia / Retiro. Programar temprano y concluir al mediodía para r… |
| `calendario_hitos.ensayo_general` | domingo 23-ago | ics + director | Ensayo General del ETC 88. Asistencia obligatoria. |
| `calendario_hitos.conciliacion_pre_etc` | domingo 30-ago | ics | Conciliar todos los pagos, corregir testimonios, atender observaciones… |
| `calendario_hitos.avanzada_cocina` | jueves 3-sep | ics | Avanzada del Equipo de Cocina (jueves). |
| `calendario_hitos.retiro_etc88` | viernes 4-sep → domingo 6-sep | ics + director | Encuentro ETC 88. Horario detallado en la Carpeta (Sección 7). |
| `historial.etcs_disponibles_en_drive` | ["ETC 78", "ETC 79", "ETC 83", "ETC 85", "ETC 88"] | exploración Drive 2026-06-04 | Carpeta padre Drive contiene 78, 79, 83, 85, 88. El ETC 83 fue agregad… |
| `historial.etc_83_disponible` | True | Drive: carpeta ETC 83 compartida por el director 2026-06-04 | Contiene 4 archivos: Presupuesto cocina ETC 83 (xlsx grande), Roster +… |
| `historial.informe_final_85` | Informe Final ETC 85.pdf — leído en Drive | Drive: ETC 85 / Informe Final ETC 85.pdf | Roster 85 + puntos positivos + aspectos a mejorar + medidas financiera… |
| `historial.drive_88_carpetas_vacias` | ["Operaciones", "Finanzas"] | exploración Drive 2026-06-02 | Las subcarpetas Operaciones y Finanzas del ETC 88 están vacías (los pa… |
| `historial.revision_cruzada_completa` | 78/79/83/85 revisados a fondo 2026-06-04 | Drive: lectura de los 5 folders | Síntesis en preparacion/RESUMEN_MIGRACION_ETCS.md. 79 tiene el set doc… |
| `historial.asesoras_cocina_continuidad` | Petra Morales + Johanny García sirvieron en ETC 83 y ETC 85 | Informe Final ETC 85 (roster: 'Asesores de cocina: Johani y Petra') + Presupuesto cocina ETC 83 | Continuidad de asesoras de cocina confirmada en 83 y 85. Son cantera c… |
| `mapa_donaciones_por_rubro.zonas.spm` | San Pedro de Macorís — parroquia San José Obrero + comercios… | director |  |
| `mapa_donaciones_por_rubro.zonas.higuey` | Higüey — cerca de la casa, proveedores locales (insumos pesa… | ubicación de la casa |  |
| `mapa_donaciones_por_rubro.zonas.pc` | Punta Cana — parroquia Nuestra Señora del Pilar + hoteles pa… | director |  |

## 🟡 Propuestas (sin cerrar — se muestran [PROPUESTA]; OJO con la fuente)
| Campo | Valor | Fuente | Nota |
|---|---|---|---|
| `marca.branding_reglas_esteticas` | Identidad ORIGINAL del ETC: el pez ICTUS de colores (logo or… | director + logo original | 7-jun (final): el director descartó la Dirección A y pidió la identida… |
| `equipos_auxiliares[1].responsable` | Producción | — |  |
| `gaps_post_informe_85.informe_post_retiro` | Comparar presupuesto planificado vs gastos reales tras el re… | Informe 85, medida #5 | Compromiso para post-retiro (14-sep en adelante). |
| `gaps_post_informe_85.oracion_grupal_obligatoria` | Participación obligatoria de TODOS los equipos (guías y ases… | Informe 85, aspecto a mejorar | Agregar a las reglas como equipo en F1. |
| `gaps_post_informe_85.confirmar_n_etc_con_consejo` | Confirmar el # del ETC con concilio/consejo TEMPRANO; cambio… | Informe 85 | Relevante a 'completar 100 en la casa'. |
| `gaps_post_informe_85.responsabilidades_asesores_estandarizadas` | Estandarizar y documentar las responsabilidades de los aseso… | Informe 85 | Producir doc breve por tipo de asesor antes de F2. |
| `gaps_post_informe_85.escenario_cocina_con_donaciones` | Modelar la canasta de cocina con un escenario 'con donacione… | ETC 78 Costo ETC Participantes + Presupuesto General Agosto 7 | Reforzar gestión de donaciones en especie (arroz, habichuelas, aceite … |
| `gaps_post_informe_85.visiteo_casa_obligatorio` | Hacer obligatorio el visiteo a la casa de retiro previo (ref… | Informe 85 | Coordina con Samuel Montilla antes de fijar fecha. |
| `gaps_post_informe_85.oficina_separada_pg` | La oficina debe estar separada de los pequeños grupos y orga… | Informe 85 | A tener en cuenta en el visiteo a la casa. |
| `gaps_post_informe_85.cocina_no_abrumar_palancas` | La cocina no abruma a los participantes durante el proceso d… | Informe 85 | Recordatorio para el Ensayo General. |
| `gaps_post_informe_85.luces_apagadas_cena_sabado` | Evaluar mantener las luces apagadas en la cena del sábado pa… | Informe 85 | Decisión de Co-Dir + asesores espirituales. |

## 🔴 Pendientes (faltan — se muestran [POR DEFINIR])
| Campo | Valor | Fuente | Nota |
|---|---|---|---|
| `equipos_auxiliares[0].responsable` | Por nombrar (Co-Dir decide) | — | Roberto Figueroa y Guido propusieron en el formulario (col 18) ideas d… |
| `equipos_auxiliares[2].responsable` | Por nombrar (Co-Dir decide) | — | El director clarificó (3-jun) que Intersección es tradicionalmente la … |
| `equipos_auxiliares[3].responsable` | Por nombrar dentro del equipo (Co-Dir decide) | — | El director (3-jun) pidió identificar responsable o equipo financiero … |
| `pendientes_direccion.fecha_limite_cotizar_transporte` | None | director | Fecha límite para cotizar transporte, biblias y peces. Definir. |
| `pendientes_direccion.asignacion_entradas` | None | director | Política de earmark (qué entrada se destina a qué compromiso). Se revi… |
| `pendientes_direccion.visiteo_coordinadores_casa` | None | director | Visiteo OBLIGATORIO de coordinadores a la casa de retiro ANTES del ret… |
| `gaps_post_informe_85.responsable_financiero` | None | Informe 85 + director (3-jun) | Nombrar 1-2 personas dentro del equipo como Finanzas / Tesorería auxil… |

## Decisiones confirmadas (lista del director)
- Retiro ETC 88: 4–6 de septiembre de 2026, Casa de Retiro La Ceiba del Salado, Higüey.
- Co-dirección: Juan Manuel de la Cruz y Jean Carlo de la Cruz.
- Casa: $2,300/persona sin exención · $2,000/persona con exención (RNC parroquia del Padre Paul). Incluye gas y limpieza. Tiene sonido.
- Deuda inicial: $23,600 al Consejo Eteciano (10% reserva que Juan Manuel adelantó y ya le fue devuelto).
- Cuota de participante: $3,000.
- Frank Morales es asesor (como Laura y Tomás) y además lleva el Banderín.
- Padre Paul y Sor Angelina son Asesores Espirituales transversales (todo el proceso, no solo el retiro).
- Apellido de Leober: Soriano.
- Roselyn DENTRO de cocina (4-jun): el director confirmó que Roselyn y Randol están AMBOS en cocina; Pamela queda fuera. Cocina sigue en 21.
- Backups (4-jun; actualizado 7-jun): Backup de GUÍAS = Rodolfo Telémaco, Scarlett Nivar, Kamila Todd (3). Backup de COCINA = Emily de la Rosa, Zahir, Vileimi, Yileivi, Eduardo, Emmanuel, Ricaira, Nestor, Leandro, Samuel, Emily, Emilio, Carlos, Rosanna, Inomar (15). Total 18 backups. NO son operativos. (Merkin subió de backup a titular cocina el 7-jun, reemplazando a Fabelly Maciel que salió del equipo.)
- Cambio de equipo 7-jun: Fabelly Maciel Fabian Bello SALE del equipo. Merkin Jean sube de backup a titular en cocina. Cocina sigue en 21 titulares.
- Equipos auxiliares (5): Recaudación y Donaciones · Guagua (Transporte) · Actividad Profondo · Intersección (diáspora) · Finanzas / Tesorería (auxiliar).
- Intersección (auxiliar) = vínculo con la diáspora (etecianos fuera del país que apoyan); NO es el equipo espiritual transversal — esa función la cubren Paul + Sor como Asesores Espirituales transversales (ya en asesores_espirituales).
- Randol Joseph Payano (nombre tomado del formulario, confirmado 3-jun) ACTIVO en Cocina (no backup). El 4-jun el director confirmó: Roselyn y Randol ambos dentro, Pamela fuera.
- Daylin M Rambalde Moreta confirmada en Música (3-jun); indicó que no puede asumir coordinaciones (posible cambio de empleo + distancia/asistencia, reside en Punta Cana).
- Profondo #1 = primera actividad de recaudación (formato por definir por el director).
- Asesoras de cocina: Mary "Petra" Morales y Johanny García.
- Convivencia 16-ago (programar temprano y concluir al mediodía para reducir costos de almuerzo). Ensayo General 23-ago es obligatorio.
- Reunión de coordinadores: jueves 4-jun (Corpus Christi, virtual).
- Piso de personas: completar 100 en la casa de retiro.
- La meta de recaudación = el costo total del retiro (se cubre con cuotas + Profondo #1 y #2 + donaciones).
- Santo Domingo: 2 asesores de comunidad, Marleny y Sandrita.
- La Vega: 1 asesor de comunidad, Leticia González.
- Nombres corregidos: Guido Maldonado · Fabelly Maciel Fabian Bello.
- 10-jun-2026: Pamela Colón entra a Cocina (titular); Jordelis Mateo sale del equipo. Pamela respondió formulario 10-jun (cumple 15-may, tel 829-342-2888). Condición de salud relevante: Migralepsia — riesgo con mucho calor o sin desayunar (bandera #35).
- 10-jun-2026: Cumpleaños confirmados vía Carpeta v9 PDF: Paul 9-nov · Sor Angelina 22-oct · Frank 11-jul · Mary "Petra" 19-oct · Johanny 13-feb.
- 10-jun-2026: Rodolfo Telémaco Arrendel llenó formulario pero sigue como backup de Guías sin cambio (decisión Co-Dir).
- 10-jun-2026: Risaira y Risairi Santana Rosario son hermanas (no es typo). Confirmado por director.
- 10-jun-2026: Target de participantes confirmado en 45–48 (para completar ~100 personas en la casa con los 48 operativos).
- 10-jun-2026: Mensaje de WhatsApp para F1 (dom 14-jun, 9:30 AM, Sta. Clara de Asís) enviado al equipo.
- 10-jun-2026: Hilo espiritual y reglas estéticas/branding confirmados (trabajados con Claude Design — detalles vivos en el material de diseño).
- 10-jun-2026: Equipo de Profondo = Equipo de Recaudación (es UN solo equipo, no dos). Equipos auxiliares pasan de 5 a 4.
- 10-jun-2026: Asesores Comunidad (Leticia · Marleny · Sandrita) son representación que envía la comunidad (no decisión interna del equipo). Sus datos personales (tel/cumple) no son bloqueante interno.
- 10-jun-2026: Biblias cotizadas. Librería Paulinas (Av. Bolívar 203 Gazcue, SD · 809-685-7542 · paulinasventasrd@gmail.com). Proforma 32397 (08-jun-2026, prep. Norberto, término 30 días). 50 × Biblia Latinoamericana bolsillo color a $800 c/u con 15% desc = $680 efectivo. Total $34,000.
- 10-jun-2026: Pez ICTUS para participantes — referencia: Bronze Fish Pendant de Terra Sancta Guild en Amazon (B00VB37PIK). Costo y proveedor final pendiente.
- 14-jun-2026: Presupuesto Maestro construido (Juan Manuel, Co-Dir.). Cifra TOTAL LADO A = RD$ 553,622 (reemplaza estimado previo 583,281). Subtotal operativo 503,293 + imprevistos 10% (50,329).
- 14-jun-2026: Cuotas CONFIRMADAS: participante RD$ 3,000 (1er + 2do pago) · equipo RD$ 2,000.
- 14-jun-2026: Target presupuestario 50 participantes (rango operativo 45–50). Cierra casa con 100 personas (50 part. + 50 equipo cubierto).
- 14-jun-2026: Plan A de recaudación confirmado (caja objetivo 471,000 + especie 114,701). Margen proyectado +32,079 (cierre POSITIVO, no empatado · lección ETC 83).
- 14-jun-2026: Caja registrada — Reserva casa 23,600 (depositada y devuelta el 7-jun) · Salón 10,000 (Juan Manuel pagó con dinero personal, deuda al grupo).
- 14-jun-2026: Plan de Recaudación documentado en `data/presupuesto/ETC88_Analisis_y_Plan_de_Recaudacion.docx` + Maestro vivo en `data/presupuesto/ETC88_Presupuesto_Maestro.xlsx`.
- 20-jun-2026: Backups de Cocina (15 personas — cantera) ELIMINADOS del repo por decisión del director. El equipo de cocina queda con sus 21 titulares + 2 asesoras cocina. Backups de Guías (3) se mantienen.
- 11-sep-2026: Presupuesto OFICIAL del ETC 88 = Finanzas 11-Ago (596,249.56, costo completo con la tarifa real de la casa). El Sistem (512,859.56) queda como referencia operativa del panel. Conciliación final post-retiro generada por scripts/build_conciliacion.py (caja 515,944 · costo económico 615,809 · balance 36,543.40 → 34,337 en cuentas).
- 11-sep-2026: Salón de formaciones (Santa Clara, 5 × 2,000 = 10,000, pagado el 07-jun en efectivo a Franklin Pozo con aporte personal de Juan Manuel): aporte YA REEMBOLSADO a Juan Manuel, deuda saldada. Participantes confirmados: 46 (156,800); los 4,200 pendientes = Karen Berroa 1,000 + Melany Ceverino 200 + Karen 2,500 + 500 de una de las 7 sin cifra. Pendiente: identificar de qué salida del ledger salió el reembolso del salón.
- 11-sep-2026: Profondo liquidado por la comisión (Desglose_Ganancias_Actividad_Pro_Fondo.xlsx): bruto 154,420 (680.5 boletas pagadas × 200 = 136,100 + venta de comida y helados 18,320) − premios 19,900 (aire acondicionado 16,900 + abanico de torre 3,000) = 134,520; entregado a finanzas 135,866.40 (1,346.40 de helados posteriores al informe). Boletas colocadas no pagadas: 73.5 × 200 = 14,700 por cobrar. Efectivo de imprevistos 15,000: 5,000 a cocina en la casa de retiro; los 10,000 restantes = reembolso del salón [POR CONFIRMAR]. Cuotas: participante 3,500 · equipo 2,000.
- 11-sep-2026: Confirmado: los 10,000 restantes del efectivo de imprevistos fueron el reembolso del salón de formaciones a Juan Manuel (efectivo 15,000 liquidado: 5,000 cocina + 10,000 salón). Los 4,200 de participantes son los pagos que faltaron para completar 3,500 (no se registran como cuenta por cobrar). Las 73.5 boletas del profondo sin pagar (14,700) NO se cobrarán. Costo del retiro 615,809 (caja 515,944 + cubierto sin pagar 99,865); base recurrente 599,809. Tesorería del 88: 3 roles (recibir, registrar, conciliar) + 1 rol de plataforma.
- 11-sep-2026: Impresión de libretas (1,260) sumada a la especie → especie 92,405; costo del retiro 617,069. La diferencia con el banco (2,206.40) se desglosa en impuesto bancario por transacción (0.20% sobre los 1,068,431.40 movidos = 2,136.86) más copias pagadas (69.54); ninguna comisión de los directores. Participantes: no hay pagos pendientes; los 161,000 son referencia teórica (46 × 3,500) y cuatro pagaron menos. Cuotas del equipo: 98,000 = 49 × 2,000; no pagaron cuota el padre Paul, la sor, Petra y Johanny; los 3 guías de reserva no entran en el conteo.
- 11-sep-2026: Cierre verificado nombre por nombre. No hay ningún pago a nombre de Amanda Rivera en ninguna fuente (solo figura como invitada en el formulario de junio); los únicos abonos de 500 de la lista de participantes son de Melany Ceverino y Erilis Polanco. Boris queda fuera de los 156,800 (neto 1,500 como donación de Jonathan Medina). Cristofer (Cristopher Jiménez) figuraba en 0 en junio pero los 21 de cocina cierran al 100%; de Dahiony no hay rastro en ninguna lista. Impuesto bancario confirmado en 0.20%. El sobrante de 34,337 se expondrá en la actividad de cierre (evaluación) para decidirlo con el equipo. Único pendiente: la nota en el acta de las 4 donaciones sin identificar (6,500).
- 11-sep-2026: Son dos personas distintas: Cristopher Jiménez (cocina, sí pagó su cuota) y Cristofer (participante, no pagó). Al retiro fueron 48 participantes: 46 pagaron y 2 entraron sin cuota (Cristofer y Dahiony), 7,000 de cuota no recaudada. Los 99 de la casa = 48 participantes + 51 del equipo.

## Pendientes y decisiones por cerrar (lista del director)
- [ ] 🚩 Verificar avanzada con Cocina (cuántas personas jue/vie 3-sep · hospedaje + 3 comidas). Hoy el LADO A tiene 0 ahí — subestima el total.
- [ ] 🚩 Confirmar exención de la casa con Padre Paul (vale 30,000 — convierte 200,000 estimado en firme).
- [ ] 🚩 BLOQUEANTE: Nombrar responsable único de Tesorería ANTES de recaudar el primer peso (Informe ETC 85 + Plan Recaudación §8). Sin esto, NO se opera el modelo.
- [ ] Definir los responsables de cada uno de los 4 equipos auxiliares (Recaudación-Profondo (un solo equipo) · Guagua · Intersección/diáspora · Finanzas/Tesorería).
- [ ] Identificar responsable o equipo de Finanzas / Tesorería dentro del equipo (auxilia a la Co-Dirección; control de pagos y reportes — medida #3 Informe 85).
- [ ] Asignar el equipo de Intersección — diáspora del 88 (etecianos fuera del país que sirven como padrinos / red de oración / donaciones desde el exterior).
- [ ] Confirmar la exención de la casa con el Padre Paul.
- [ ] Confirmar con la casa la tarifa de la avanzada (noche/día extra del equipo que adelanta el jueves) + sus 3 comidas.
- [ ] Completar las tallas de camiseta del EQUIPO que faltan (Paul, Frank, Sor y demás del equipo sin talla). La camiseta es SOLO del equipo; los participantes no llevan. El mockup va tras el Design System.
- [ ] Pedir 3 cotizaciones reales de transporte (Metro Servicios 809-530-2850 · Transportando RD 849-803-1626 · DominicanBus 809-530-9742). Hoy 77,500 es estimado.
- [ ] Lanzar rifa/profondo: 600 boletos × 200 (premio 30,000) — meta caja 90,000 para sorteo en agosto.
- [ ] Gestionar donaciones en especie: biblias 34K, peces 30K, camisetas 20K, materiales guías 17K = 88% del potencial 114,701.
- [ ] Verificar si 2 buses cubren en vez de 3 (lección ETC 86 SD usó 2×26pax) — posible ahorro estructural.
- [ ] Confirmar lista REAL de participantes (hoy 50 es estimado; rango operativo 45–50).
- [ ] Cerrar ítems cocina no verificados: té frío, sazón, orégano, puerro, bizcocho, salsa roja kg.
