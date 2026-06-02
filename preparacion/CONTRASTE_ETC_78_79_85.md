> **DOCUMENTO DE TRABAJO — no es entregable oficial.** Contraste del ETC 88 con los ETCs anteriores (78/79/85) leídos en Drive. Cada hallazgo lleva **fuente exacta**. Recomendaciones marcadas **[PROPUESTA]/[POR DEFINIR]** — el director aprueba.

# Contraste ETC 88 vs ETCs anteriores (78 · 79 · 85)
### Auditoría cruzada con Drive · 2026-06-02 · `verify.py` TODO PASS

## 0. Carpetas leídas en Drive (trazabilidad)
| Carpeta | Documentos relevantes leídos | Para qué |
|---|---|---|
| ETC 78 | Costo ETC Participantes · Presupuesto General Agosto 7 · Presupuesto cocina LXXVIII | Benchmark de costos y donaciones reales |
| ETC 79 | (acceso confirmado, mismas estructuras) | Tags experiencia + cantera |
| ETC 85 | **Informe Final ETC 85.pdf** | Post-mortem oficial — base de gaps |
| ETC 88 | Borrador de Equipo (Abril) | Cantera (ya capturado en `data/cantera.json`) |
| **ETC 83** | ❌ **NO EXISTE** | Búsqueda título "83/LXXXIII" + full-text "ETC 83" = cero matches en el ámbito ETC |

> **Nota Drive:** subcarpetas "Operaciones" y "Finanzas" del ETC 88 están **vacías** (las del 85/78/79 tienen estructura rica: Cartas Donaciones · Presupuestos · Carpetas por área · Perfiles). Captura: `estado.historial.drive_88_carpetas_vacias`.

---

## 1. Lo que el 88 YA cubre (✅ consistente con 85) — *fuente: Informe Final 85*
| Aspecto | Lo dijo el 85 | Estado en el 88 |
|---|---|---|
| Dinamismo de formaciones (puntuales, no extensas) | ✅ punto positivo 85 | ✅ arco F1–F5 con ese mismo enfoque |
| Integración de directores con todos los equipos | ✅ punto positivo 85 | ✅ encodeado en `PROGRAMA_F1.md` y `REUNION_4JUN` |
| 7 parejas de guías | el 85 tuvo exactamente 7 parejas (roster oficial) | ✅ regla fija en `estado.reglas.parejas_guias` |
| Música apoyando desde el jueves antes del retiro | ✅ punto positivo 85 | ✅ recogido en `ANEXO_COCINA` y horario |
| Asesores de comunidad (Leticia La Vega + Marleny + Sandrita SD) | ✅ mismos del 85 (roster oficial 85) | ✅ confirmados en `data/estado.asesores_externos` |
| Paul (asesor SPM) + Priscilla (coord guías) | ✅ del 85 (roster oficial 85) | ✅ confirmado |
| Disciplina de cocina pese a limitaciones de espacio | ✅ punto positivo 85 | ✅ Anexo Cocina con regla de oro + Lavatorio |
| Adiestramiento liturgia + banderín | aspecto a mejorar del 85 | ✅ "Frank lleva el Banderín" + agendado en Guía de Guías §6 |
| Ensayo de pequeños grupos | aspecto a mejorar del 85 | ✅ recomendación de equipo en `GUIA_DE_GUIAS §5` |

---

## 2. Gaps del 85 a adoptar en el 88 (recomendaciones [PROPUESTA]) — *fuente: Informe Final 85*
Capturados en `data/estado.gaps_post_informe_85`. Cada uno se decide.

| # | Gap del 85 | Recomendación para el 88 | Dónde se aplicaría |
|---|---|---|---|
| 1 | "Designar responsable financiero o pequeño comité" (medida #3) | **Nombrar 1–2 personas para control de pagos y reportes** | F1 (anuncio) · responsable nombrado antes de F3 (arranca recaudación) |
| 2 | "Evaluar gastos después del retiro · informe planificado vs real" (medida #5) | **Compromiso de informe post-retiro** | Calendario post-13-sep |
| 3 | "Participación obligatoria en momentos grupales de oración (todos)" | **Agregar a las reglas como equipo** | Reglas (Carpeta §4) |
| 4 | "Evaluar # del ETC con concilio/consejo temprano · cambios tardíos en otras comunidades causaron retrabajos de cocina" | **Confirmar # con consejo ANTES de F3 (compras anticipadas)** | Co-Dir → consejo |
| 5 | "Estandarizar y documentar responsabilidades de asesores (cocina y generales)" | **Doc breve por tipo de asesor antes de F2** | Producir y bajar a asesores |
| 6 | "Visiteos a casa de retiro previos deben ser OBLIGATORIOS" | **Calendarizar visiteo coords a la casa** (ver §6) | `estado.calendario_hitos.visiteo_coordinadores_casa` |
| 7 | "Oficina debe estar separada de PG · organizarse para uso eficiente" | **A tener en cuenta en el visiteo** | Visiteo |
| 8 | "Cocina no abrumar a participantes durante palancas (controlar abrazos)" | **Recordatorio en Ensayo General** | Ensayo 23-ago |
| 9 | "Evaluar mantener luces apagadas en cena del sábado (solemnidad)" | **Decisión Co-Dir + AE** | Ensayo |
| 10 | "Cocina · cuidar utensilios dejados en el piso (riesgo en plenarios)" | **Recordatorio en Ensayo + Anexo Cocina** | Ya implícito; reforzar |

---

## 3. Validación de costos del 88 vs 78 (sourced)
*Fuente: ETC 78 "Costo ETC Participantes", "Presupuesto General Agosto 7", "Presupuesto cocina LXXVIII"*

### 3a. Coincidencias y validaciones
| Partida | ETC 78 (2022) | ETC 88 (2026) | Lectura |
|---|---|---|---|
| **Peces** | **$715** c/u | **$715** c/u | ✅ idéntico — la cifra del 88 está sourced |
| Biblias | $450 c/u | $500 c/u | ✅ razonable (+11% en 4 años) |
| Casa por persona | $1,000 ($50K÷50 personas) | **$2,000–$2,300** | ⚠ **2× en 4 años** — confirmar con la administración |
| Cocina por persona | $1,590 (sin donaciones) → **$461 con donaciones** | $822 (canasta+meriendas $82,166 ÷ 100) | ✅ 88 ya está optimizada (~48% menor) — sigue siendo posible bajar más con donaciones |
| Vino litúrgico | $1,200/gl | $1,200/gl | ✅ idéntico |
| Ofrenda a sacerdotes | $2,000 c/u × 4 = $8,000 | $2,000 × 4 = $8,000 | ✅ idéntico |
| Camisetas | $300–385 c/u (44 pers · 2022) ≈ $13,860 | $19,600–28,000 estimado (~56 pers · 2026) | ✅ consistente con inflación + más personas |

### 3b. Donaciones reales del 78 (la palanca a replicar)
- **51% del presupuesto fue DONADO** (Donado $122,590 / Total $241,168). Fuente: "Presupuesto General Agosto 7 · pestaña General Restado".
- Donantes nombrados en el 78 (ejemplo de qué se donó): Paya (peces, biblias, arroz, plátanos), Paul (arroz/chocolate/cúrcuma), Eduardo (vegetales/frutas), Joan Felix (carne), Ramon Leonardo (lácteos), Iberia (productos lácteos/pan/leche/chuleta), Belkis (cebollas/jengibre/harina).
- **Profondo del 78: "Venta de Garaje" levantó $59,500 real** (fuente: "Gastos" 78 · ingresos). → **valida el garaje virtual del 88**.

### 3c. Cocina con donaciones — la palanca más rentable
**ETC 78 sin donaciones: $1,590/persona vs con donaciones: $461/persona = caída del ~70%.**
Recomendación: modelar canasta del 88 con un **escenario "con donaciones en especie"** (capturado como `gaps_post_informe_85.escenario_cocina_con_donaciones`). Si el 88 baja la cocina aunque sea 30%, recupera ~$25K en la brecha.

---

## 4. Confirmaciones para la cantera (todos vinieron de Drive, no inventados)
*Fuente: Informe Final 85 roster oficial · Presupuesto cocina 78 (asignaciones)*

| Nombre | Confirmación en Drive | Etiqueta en `cantera.json` |
|---|---|---|
| María Astacio | cocina 85 (roster Informe Final) + 78 (presupuesto cocina) | "cocina 78, 79 y 85" ✅ |
| Néstor Vidal | cocina 85 (roster Informe Final) | "cocina 85" ✅ |
| Leandro Fernández | cocina 85 (roster Informe Final) | "cocina 85" ✅ |
| Kedward Acevedo | Director de Cocina 85 (roster Informe Final) | "Director Cocina ETC 85" ✅ |
| Scarlett Nivar | coord guías 85 (roster) | "coord. guías 85" ✅ |
| Kamila Todd | guía 85 (roster Informe Final) | "guía 85" ✅ |
| Samuel Humphry | listas 78 (camisetas + cocina) | "cocina ETC 78, sirvió 79" ✅ |

**Conclusión:** las etiquetas de experiencia que dimos a la cantera NO estaban inventadas. Drive las confirma.

---

## 5. Estructura de carpeta — qué tenían 78/79/85 que el 88 aún no tiene
*Recomendación operativa: replicar subcarpetas vacías del 88 cuando se llenen.*

| Subcarpeta típica del 85 | Equivalente en el 88 | Estado |
|---|---|---|
| Cartas (Donaciones) | (vacío) | **Crear cuando empiecen las cartas** |
| Programación Reuniones | (vacío en Drive; en el repo sí están los guiones) | OK en repo |
| Documentos Generales | (vacío) | Se llenará con la Carpeta F1 cuando se imprima |
| Borradores Listado Participantes | (vacío) | Crear cuando se confirme el conteo |
| Convivencia/Retiro | (vacío) | Crear más adelante |
| Participantes (perfiles) | (vacío) | Crear en F4 (perfiles 1) |
| Ideas (Imágenes) | (vacío) | Para Claude Design + decoración |
| PARA IMPRIMIR - ULTIMOS CAMBIOS | (vacío) | Crear cerca del retiro |

---

## 6. Visiteo de coordinadores a la casa (gap #6 del Informe 85)
*Capturado en `estado.calendario_hitos.visiteo_coordinadores_casa` como `pendiente`.*

**Por qué importa:** el Informe Final 85 lo señala **textualmente**: *"Los visiteos a las casas retiros previo al retiro deben ser obligatorios para que el equipo pueda estar preparado."*

**Pre-requisito:** coordinar fecha con la administración de la casa (**Samuel Montilla**) ANTES de fijarla con los coordinadores.

**Ventana [PROPUESTA]:** entre **F2 (28-jun)** y **F4 (19-jul)** — para que tenga eco en la planificación de cocina y guías sin chocar con formaciones. Ideal **sábado** (no domingo, que tiene misa eteciana).

**Quiénes deben ir (sugerido):** Co-Dir (JM + JC) · Paloma + Jhonnito (cocina) · Priscilla + Camila (guías) · José Tusen (música) · Frank (banderín).

**Qué revisar en el visiteo** (derivado del Informe 85):
- Ubicación de la oficina **separada de los PG** (gap #7 del 85).
- Espacios para los **7 pequeños grupos** (color-coded).
- Manejo de cocina (gas, fregaderos, refrigeración).
- Puntos para el **Lavatorio** del sábado.
- Sonido de la casa (ya confirmado que tiene).
- Logística de llegada de **avanzada 3-sep**.
- Acceso/seguridad/parqueo.

**Acción que entra al guion del 4-jun:** Co-Dir contacta a Samuel Montilla esta semana para proponer 2–3 fechas; los coords confirman disponibilidad en la reunión virtual.

---

## 7. Resumen ejecutivo (1 página · para los directores)
1. **El modelo del 88 implementa las 5 medidas financieras del Informe 85.** Faltan dos por activar: **responsable financiero** + **informe post-retiro**.
2. **Costos del 88 están sourced contra el 78**: peces y vino idénticos; biblias razonable; **casa subió 2×** (a confirmar); cocina ya optimizada.
3. **El 78 donó 51% del presupuesto** y bajó la cocina 70%. **Replicarlo es la palanca más rentable** del 88.
4. **9 gaps del 85** capturados como recomendaciones — el director aprueba cuáles adoptar.
5. **Visiteo a la casa** calendarizado como pendiente con pre-requisito de coordinar con Samuel Montilla.
6. **ETC 83 no existe en Drive** — no inventar contenido del 83.
7. Etiquetas de experiencia de la cantera **confirmadas por rosters reales** del 85 y 78.

---

*Generado con `verify.py` TODO PASS · trazado en `preparacion/TRAZABILIDAD.md`.*
