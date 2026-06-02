# Conectar el tablero a un Google Sheet en vivo

El tablero (`index.html`) puede leer el equipo directamente de un Google Sheet.
Editás la hoja, recargás la página, y los cambios aparecen. Si no hay internet
o la hoja no está configurada, usa una **copia local** de respaldo (nunca se
rompe).

## Paso 1 — Subir la hoja maestra a Google Sheets

1. Entrá a [Google Drive](https://drive.google.com) e iniciá sesión.
2. **Nuevo → Subir archivo** → elegí `Equipo_ETC88.xlsx`.
3. Clic derecho sobre el archivo subido → **Abrir con → Hojas de cálculo de Google**.
   (Esto crea una copia editable en formato Google Sheets; los menús desplegables se conservan.)

> A partir de acá, **esta hoja de Google es tu fuente de verdad.** Editás ahí:
> mover gente entre equipos, cambiar coordinadores, marcar operativo/no-operativo.

## Paso 2 — Publicar la pestaña "Equipo" como CSV

1. En la hoja de Google: **Archivo → Compartir → Publicar en la web**.
2. En el primer menú, elegí la pestaña **"Equipo"** (no "Todo el documento").
3. En el segundo menú, elegí **Valores separados por comas (.csv)**.
4. Clic en **Publicar** → confirmá.
5. Copiá el enlace que aparece. Termina en algo como:
   `…/pub?gid=0&single=true&output=csv`

## Paso 3 — Pegar el enlace en el tablero

1. Abrí `index.html` en el navegador.
2. Arriba, en la barra clara, clic en **⚙ Datos**.
3. Pegá el enlace CSV y clic en **Guardar y cargar**.
4. El indicador debe pasar a verde: **● Hoja en vivo**.

El enlace se guarda en ese navegador (localStorage), así que la próxima vez carga solo.
Para compartir el tablero ya conectado con otros coordinadores, cada uno pega el
enlace una vez (o lo dejamos fijo en el código y te paso el archivo listo).

## Uso diario

- **Editar equipo:** abrí la hoja de Google, cambiá lo que sea en la pestaña *Equipo*.
- **Ver cambios:** recargá el tablero (o clic en **↻ Recargar**).
- **Sin internet:** el tablero muestra la última copia local y avisa con **● Copia local**.

## Qué columnas lee

De la pestaña **Equipo**: Nombre, Sexo, Edad, Área, Rol, Coordinador (Sí/No),
Operativo (Sí/No), Comunidad, Residencia, ETC propio, Año ETC, ETCs servidos,
Cumpleaños, Teléfono, Talla, Sin formulario.

Los textos largos del formulario (qué espera, miedos, alergias, contacto de
emergencia, etc.) **no están en esa pestaña**: el tablero los conserva de su copia
interna y los cruza por nombre. Por eso conviene no renombrar personas: si cambiás
un nombre en la hoja, perdés el cruce con su ficha del formulario.

## Valores válidos de "Área"

`directores`, `asesores`, `guias`, `cocina`, `musica`, `asesores_cocina`,
`asesores_espirituales`, `asesores_diocesanos`.

(La pestaña ya trae estos valores como menú desplegable.)
