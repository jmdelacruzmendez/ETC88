# Logo del ETC — el pez ΙΧΘΥΣ · prompt + pasos para generarlo en Claude

## Qué es
El logo es el **pez ICTUS** (ΙΧΘΥΣ = *"Jesucristo, Hijo de Dios, Salvador"*), símbolo cristiano y eteciano. Versión a usar (la que eligió el director): **pez amarillo estilizado, amistoso, con las cinco letras griegas en colores.**

## Referencia que ya tenemos
- **Borrador vectorial:** `design/logo_eteciano.svg` — recreación de esta misma versión (sirve de referencia de forma y colores).
- **Importante:** al generarlo en Claude, **adjunta la imagen original del director** como referencia exacta (la imagen pegada no se guarda en el repo; necesitas subir el archivo).

---

## EL PROMPT (cópialo en Claude)

> Diseña un **logo vectorial limpio de un pez estilizado** (símbolo cristiano, *pez ICTUS*), visto de lado, **mirando a la izquierda**, con la cola a la derecha.
>
> **Cuerpo:** amarillo dorado con un degradado suave y un sombreado 3D sutil (como esmalte o galleta), **contorno grueso marrón oscuro**, esquinas redondeadas. Aspecto amistoso y cálido, pero sobrio (es para un retiro católico).
>
> **Sobre el cuerpo, centradas, las cinco letras griegas de ΙΧΘΥΣ**, cada una de un color plano distinto:
> - **Ι** (iota) — celeste claro
> - **Χ** (ji) — rojo
> - **Θ** (theta) — azul
> - **Υ** (ípsilon) — naranja
> - **Ϲ** (sigma lunar, forma de "C") — magenta / fucsia
>
> **Detalles:** un ojo pequeño (círculo con contorno marrón) y una boca curva cerca de la cabeza; **tres líneas curvas marrón oscuro arriba y dos abajo** (aletas/branquias estilizadas).
>
> **Fondo:** blanco o transparente. Composición centrada, alta resolución, estilo plano con sombreado suave, **sin texto adicional ni marca de agua.** Apto para imprimir y para usar como ícono.

---

## Variantes a pedir (en el mismo chat)
1. **A color** — la principal.
2. **A 1 tinta** (solo el contorno, para impresión barata).
3. **PNG con fondo transparente.**
4. **SVG** si el modelo puede entregarlo (vector editable).
5. *(Opcional)* una versión alineada a la paleta de la Carpeta (azul profundo · arena · coral) por si se quiere combinar con la Dirección A.

## Pasos (en Claude)
1. Abre un **chat nuevo** en Claude (o en Claude Design).
2. **Adjunta la imagen original** del pez (sube el archivo, no la pegues).
3. Pega el **prompt** de arriba y añade: *"usa la imagen adjunta como referencia exacta de estilo y colores."*
4. **Itera**: pide ajustes de color o forma hasta que calce con la referencia.
5. Pide la **entrega final**: *"dame un PNG de alta resolución con fondo transparente"* (y un SVG si puede).
6. **Descarga** el archivo.
7. **Reemplaza** `design/logo_eteciano.png` en el repo con el oficial (mismo nombre).
8. Corre **`bash scripts/run_all.sh`** — la Carpeta y el doc de trabajo se regeneran con el logo oficial.

## Nota importante
- El pez con letras de colores es el **símbolo eteciano**; tiene **sus propios colores** (celeste/rojo/azul/naranja/magenta), distintos de la paleta de la Carpeta (Dirección A: azul/arena/coral). Eso está bien: el pez es el **acento/ícono**; el sistema de la Carpeta lo enmarca.
- Antes de finalizar, **confirmar con el director / la asociación** si existe un **logo oficial registrado** del ETC que debamos respetar.

---
*Prompt del logo ETC 88 · el pez ICTUS de colores · para generar en Claude y reemplazar el placeholder del repo.*
