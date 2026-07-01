# TRAZABILIDAD ETC 88 — registro de hechos, fuentes y estados

> Generado desde `data/estado.json` + `data/equipo.json`. Todos los entregables se generan
> de estas dos fuentes; `verify.py` bloquea cualquier desvío. Trazabilidad por construcción.

**Resumen:** 59 confirmados · 11 propuestas · 4 pendientes (en estado.json).

## Roster (data/equipo.json · generado del formulario)
- Total 69 · operativos titulares 48 · vacantes 0 · backups 16.
- Por área (operativos): asesores 3 · asesores_espirituales 2 · cocina 21 · directores 2 · guias 14 · musica 6

## ✅ Confirmados (se pueden mostrar como hecho)
| Campo | Valor | Fuente | Nota |
|---|---|---|---|
| `retiro.numero` | 88 | director |  |
| `retiro.romano` | LXXXVIII | director |  |
| `retiro.fechas` | 4–6 de septiembre de 2026 | director |  |
| `retiro.lugar` | Casa de Retiro La Ceiba del Salado, Higüey | director |  |
| `retiro.co_direccion` | ["Juan Manuel de la Cruz Méndez", "Jean Carlo de la Cruz Mén… | director |  |
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
| `marca.cita_mision_88` | Los cielos cuentan la gloria de Dios | director (17-jun-2026) | Cita bíblica para el Tablero de la Misión 88 (tema espacial). El lema … |
| `marca.lema_retiro` | Donde está tu tesoro, allí estará tu corazón | director | Lema del retiro ETC 88 confirmado por el director (Mt 6,21). El retiro… |
| `marca.hilo_espiritual` | El corazón y el tesoro (Mt 6,21): donde pongo mi tesoro, all… | director |  |
| `marca.tematica` | expedición · el tesoro y el corazón | director | Temática confirmada: la expedición es hacia adentro — la brújula del c… |
| `equipos_auxiliares[0].responsable` | Dorian | director (18-jun-2026) | Dorian coordina Recaudación/Profondo (confirmado 18-jun). A definir en… |
| `equipos_auxiliares[3].responsable` | Luisa | director (18-jun-2026) | Luisa = responsable única de Tesorería (confirmada 18-jun). Desbloquea… |
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
| `gaps_post_informe_85.responsable_financiero` | Luisa (responsable de Tesorería) · equipo: Risaira, Dayrelin… | director (18-jun-2026) | Confirmado: Luisa lidera Tesorería (medida financiera #3 del Informe 8… |
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
| `equipos_auxiliares[2].responsable` | Por nombrar (Co-Dir decide) | — | El director clarificó (3-jun) que Intersección es tradicionalmente la … |
| `pendientes_direccion.fecha_limite_cotizar_transporte` | None | director | Fecha límite para cotizar transporte, biblias y peces. Definir. |
| `pendientes_direccion.asignacion_entradas` | None | director | Política de earmark (qué entrada se destina a qué compromiso). Se revi… |
| `pendientes_direccion.visiteo_coordinadores_casa` | None | director | Visiteo OBLIGATORIO de coordinadores a la casa de retiro ANTES del ret… |

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
- Backups (4-jun; act. 1-jul): Backup de GUÍAS = Scarlett Nivar, Kamila Todd (2). Backup de COCINA = Emily de la Rosa, Vileimi, Yileivi, Eduardo, Emmanuel, Ricaira, Nestor, Leandro, Samuel, Emily, Emilio, Carlos, Rosanna, Inomar (14). Total 16 backups. NO son operativos. (Merkin subió a titular cocina el 7-jun; 1-jul: Zahir Valoy sube de backup a titular cocina reemplazando a Tommy Nova Nolasco, y Rodolfo Telémaco sale del equipo.)
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
- 1-jul-2026: Tommy Nova Nolasco SALE del equipo (decisión Co-Dir). Reemplazado por Zahir Valoy como titular de cocina.
- 1-jul-2026: Zahir Valoy entra como titular de cocina (respondió formulario 29-jun: 19 años, cumple 7-jun-2007, WhatsApp 849-460-1030, ETC 85/2025, talla L). Sube desde backup de cocina. Sexo M inferido del nombre (confirmar).
- 1-jul-2026: Rodolfo Telémaco Arrendel FUERA del equipo por completo (decisión Co-Dir); ya no figura ni como backup de guías.
- 10-jun-2026: Risaira y Risairi Santana Rosario son hermanas (no es typo). Confirmado por director.
- 10-jun-2026: Target de participantes confirmado en 45–48 (para completar ~100 personas en la casa con los 48 operativos).
- 10-jun-2026: Mensaje de WhatsApp para F1 (dom 14-jun, 9:30 AM, Sta. Clara de Asís) enviado al equipo.
- 10-jun-2026: Hilo espiritual y reglas estéticas/branding confirmados (trabajados con Claude Design — detalles vivos en el material de diseño).
- 10-jun-2026: Equipo de Profondo = Equipo de Recaudación (es UN solo equipo, no dos). Equipos auxiliares pasan de 5 a 4.
- 18-jun-2026: Director confirma miembros de equipos auxiliares — Profondo/Recaudación: Dorian, Daylin, Kelvin, Ivanna, Wilka · Intersección (diáspora): Isauris, Carol, Kharla Vanessa · Finanzas/Tesorería: Luisa, Risaira, Dayrelins.
- 18-jun-2026: Líderes confirmados — Tesorería: Luisa · Recaudación/Profondo: Dorian. Transporte/Guagua se difiere (no prioritario; se define cerca del retiro). A reunión: definición de cuentas de recaudo y si Profondo solo monta actividad/estrategia o comparte con Finanzas la gestión económica. Exención de la casa con el P. Paul: se gestiona cuando el monto esté firme.
- 10-jun-2026: Asesores Comunidad (Leticia · Marleny · Sandrita) son representación que envía la comunidad (no decisión interna del equipo). Sus datos personales (tel/cumple) no son bloqueante interno.
- 10-jun-2026: Biblias cotizadas. Librería Paulinas (Av. Bolívar 203 Gazcue, SD · 809-685-7542 · paulinasventasrd@gmail.com). Proforma 32397 (08-jun-2026, prep. Norberto, término 30 días). 50 × Biblia Latinoamericana bolsillo color a $800 c/u con 15% desc = $680 efectivo. Total $34,000.
- 10-jun-2026: Pez ICTUS para participantes — referencia: Bronze Fish Pendant de Terra Sancta Guild en Amazon (B00VB37PIK). Costo y proveedor final pendiente.
- 14-jun-2026: Presupuesto Maestro construido (Juan Manuel, Co-Dir.). Cifra TOTAL LADO A = RD$ 553,622 (reemplaza estimado previo 583,281). Subtotal operativo 503,293 + imprevistos 10% (50,329).
- 14-jun-2026: Cuotas CONFIRMADAS: participante RD$ 3,000 (1er + 2do pago) · equipo RD$ 2,000.
- 14-jun-2026: Target presupuestario 50 participantes (rango operativo 45–50). Cierra casa con 100 personas (50 part. + 50 equipo cubierto).
- 14-jun-2026: Plan A de recaudación confirmado (caja objetivo 471,000 + especie 114,701). Margen proyectado +32,079 (cierre POSITIVO, no empatado · lección ETC 83).
- 14-jun-2026: Caja registrada — Reserva casa 23,600 (depositada y devuelta el 7-jun) · Salón 10,000 (Juan Manuel pagó con dinero personal, deuda al grupo).
- 14-jun-2026: Plan de Recaudación documentado en `data/presupuesto/ETC88_Analisis_y_Plan_de_Recaudacion.docx` + Maestro vivo en `data/presupuesto/ETC88_Presupuesto_Maestro.xlsx`.

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
- [ ] Reembolsar 10,000 a Juan Manuel (Co-Dir.) por pago del salón (deuda pendiente desde 2026-06-07).
- [ ] Lanzar rifa/profondo: 600 boletos × 200 (premio 30,000) — meta caja 90,000 para sorteo en agosto.
- [ ] Gestionar donaciones en especie: biblias 34K, peces 30K, camisetas 20K, materiales guías 17K = 88% del potencial 114,701.
- [ ] Verificar si 2 buses cubren en vez de 3 (lección ETC 86 SD usó 2×26pax) — posible ahorro estructural.
- [ ] Confirmar lista REAL de participantes (hoy 50 es estimado; rango operativo 45–50).
- [ ] Cerrar ítems cocina no verificados: té frío, sazón, orégano, puerro, bizcocho, salsa roja kg.
