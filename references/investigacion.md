# Investigación: cómo enriquecer cada paso con evidencia

La consigna es **suficiencia, no exhaustividad**. El objetivo no es saber todo sobre la industria: es saber lo justo para poder tomar la siguiente decisión con fundamento. Un exceso de información satura y termina retrasando la elección, que es lo único que produce estrategia.

Antes de buscar cualquier cosa, la pregunta es siempre la misma: **¿qué decisión depende de este dato, y qué haría distinto según cómo salga?** Si la respuesta es "nada", no lo busques.

---

## 1. Acordar el modo, en el Paso 0

Tres modos posibles, y el usuario elige en el Paso 0. Puede cambiar de modo entre bloques.

| Modo | Cuándo conviene | Qué haces |
|---|---|---|
| **Búsqueda directa** | Datos públicos, acotados, verificables: tamaños de mercado, competidores, precios de lista, benchmarks, noticias de industria. | Buscas con tu herramienta y traes el hallazgo con fuente. |
| **Prompt de deep research** | El usuario necesita profundidad, cobertura de fuentes cerradas o de pago, o quiere correrlo en otra herramienta. | Le entregas el prompt armado. Ver sección 3. |
| **El usuario aporta** | Datos internos: márgenes, participación real, costos, estudios de consumidor, resultados de pruebas. | Le pides lo que necesitas y trabajas con eso. |

Durante el proceso, **cuando falte un dato buscable y su ausencia bloquee un análisis, búscalo sin preguntar.** Preguntar por cada dato interrumpe el hilo de la conversación estratégica. Lo que sí se pregunta es cuando el dato es interno y solo el usuario lo tiene.

---

## 2. Qué buscar en cada bloque

Guía de suficiencia. Cada línea es lo mínimo que hace falta para decidir, no una lista completa.

**Segmentación de industria.** Cómo segmenta la industria hoy (informes sectoriales, cómo reportan las empresas cotizadas sus divisiones), y señales de segmentaciones emergentes que nadie está usando todavía. El hallazgo valioso rara vez es la lista de segmentos conocidos: es el segmento que el mapa vigente no muestra.

**Atractivo estructural (Cinco Fuerzas).** Concentración de compradores y proveedores; márgenes típicos de la industria y de los eslabones vecinos; entradas y salidas recientes; sustitutos que están ganando terreno; si la rivalidad se juega por precio o por otra dimensión. Un dato que vale por diez: **el ROIC promedio de la industria** en los últimos cinco a diez años, para tener contra qué medir.

**Valor del canal.** Márgenes del canal, rotación, cómo decide qué listar, qué peleas está teniendo con otros proveedores.

**Valor del consumidor.** Acá los datos públicos sirven poco. Lo que vale es lo que el usuario ya sabe o puede observar. Si no hay evidencia de consumidor, esa es una barrera que hay que nombrar, no un hueco que se llena con supuestos.

**Posición relativa.** Márgenes, ROIC y estructura de costos de los competidores relevantes (estados financieros públicos, reportes de analistas); precios de lista comparados; escala relativa.

**Reacción competitiva.** Historial: qué hizo cada rival la última vez que alguien entró a su territorio. El pasado de un competidor predice mucho mejor que la especulación sobre su racionalidad.

---

## 3. Prompts de deep research

Cuando el usuario elige este modo, tu trabajo es entregarle un prompt que produzca un resultado accionable, no un ensayo.

**Primero decide cuántos.** La regla: **un research por pregunta de decisión.** Si mezclas atractivo estructural con perfil de competidores y con comportamiento del consumidor en un solo pedido, la respuesta va a ser ancha y superficial en las tres. Recomiéndale al usuario partirlo cuando:
- Las preguntas exigen tipos de fuente distintos (estados financieros vs. estudios de consumidor vs. prensa sectorial).
- Las preguntas cubren geografías o segmentos distintos.
- Una pregunta depende del resultado de otra: ahí van en secuencia, no en paralelo.

Y recomiéndale mantenerlo en uno solo cuando las preguntas comparten fuentes y contexto, y partirlas obligaría a repetir el mismo trabajo de fondo tres veces.

Dile siempre cuántos recomiendas y por qué, y en qué orden correrlos si van en secuencia.

**Estructura del prompt.** Adáptalo al proyecto del usuario; esto es el esqueleto:

```
CONTEXTO
[Qué es la empresa o unidad, en qué industria, qué decisión está sobre la mesa.
Dos o tres frases. Sin esto, el research devuelve generalidades.]

PREGUNTA CENTRAL
[Una sola pregunta, la que la decisión necesita responder.]

PREGUNTAS ESPECÍFICAS
1. [...]
2. [...]
3. [...]
[Entre tres y seis. Cada una con una respuesta verificable, no interpretativa.]

FUENTES SUGERIDAS
[Nombra las que sabes que existen para esta industria: reportes anuales y
presentaciones a inversionistas de tales empresas, asociaciones sectoriales,
reguladores, bases de datos de mercado, prensa especializada. Si no conoces
las de esta industria, dilo en vez de inventar nombres de fuentes.]

CRITERIOS DE CALIDAD
- Cada dato con su fuente y su fecha.
- Distinguir dato reportado de estimación, y estimación de opinión.
- Cuando las fuentes se contradigan, presentar ambas y decir cuál es más
  confiable y por qué.
- Cuando un dato no exista o no sea público, decirlo explícitamente en vez de
  aproximarlo.
- Priorizar los últimos [N] años.

FORMATO DE ENTREGA
[Qué quieres de vuelta: una tabla comparativa, un rango con supuestos
explícitos, una lista con evidencia por punto. Sé específico, porque el formato
determina si el resultado se puede usar o hay que reprocesarlo.]
```

Cuando el usuario vuelva con el resultado, déjalo en `00_context/inbox/` y procésalo por el protocolo del inbox. Tu trabajo no es aceptarlo: es leerlo con el criterio de la sección 4 y marcar qué entra como dato verificado y qué queda como supuesto.

---

## 4. Cómo se trata la evidencia

**Todo lo que entra al documento está marcado.** Dos categorías, sin tercera:

- **Dato verificado**: con fuente y fecha. Ejemplo: *el mercado peruano de X fue de USD 340M en 2024 (Asociación Y, informe anual 2025)*.
- **Supuesto**: con la prueba que lo volvería verificable, quién la corre y para cuándo. Ejemplo: *supuesto: el 30% de los clientes actuales pagaría un 15% más por Z. Prueba: encuesta de intención de compra a 200 clientes actuales. Responsable: [nombre]. Fecha: [fecha]*.

**Cuando un dato no existe, dilo.** Un vacío nombrado es información útil: le dice al usuario dónde está ciego. Un número inventado o "estimado" sin base es peor que no tener nada, porque las decisiones que cuelgan de él quedan sin piso y nadie se entera hasta que es tarde.

**Cuando dos fuentes se contradigan**, investiga cuál es más confiable (quién la produjo, con qué método, con qué incentivo, de cuándo es) y explica por qué elegiste una. Registra que hubo contradicción; es información sobre la calidad del terreno.

**Cita siempre.** En los nodos y en el memo la cita va breve y entre paréntesis. La fuente completa va a `00_context/sources.md`, salvo que el archivo mismo viva en `00_context/`, en cuyo caso el archivo es la fuente.

**No inventes nada**: ni cifras, ni nombres de fuentes, ni citas de personas, ni estudios. Lo que creas saber de la industria del usuario sirve para preguntar mejor, no para llenar huecos. Si necesitas un número para que un razonamiento cierre y no lo tienes, escribe el razonamiento con el número como incógnita y márcalo como lo que falta averiguar.
