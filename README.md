# on-strategy

Skill de [Claude Code](https://claude.com/claude-code) y Claude Cowork que actúa como socio de pensamiento estratégico. Co-construye con el usuario, en español y una decisión a la vez, la estrategia de una empresa o unidad de negocio, combinando los frameworks de Roger Martin (*Playing to Win*, con A.G. Lafley) y de Michael Porter (según *Understanding Michael Porter*, de Joan Magretta).

## Cómo procede el skill

Propone, el usuario decide. Esa es la regla que gobierna todo lo demás. En cada elección: explica en lenguaje llano qué se decide y por qué importa, pregunta lo que solo el usuario sabe, propone opciones con su razonamiento y una recomendación, espera la decisión, y recién entonces la registra y avanza. Nunca asume una elección estratégica en nombre del usuario.

Toda sesión arranca con un **Paso 0 obligatorio**: diagnóstico de la entidad, la situación y lo que ya está decidido, seguido de una ruta de trabajo acordada explícitamente antes de tocar cualquier framework.

Explica como guía, no como especialista. Un concepto nuevo por turno, el ejemplo antes que la definición, la jerga traducida la primera vez, y el detalle ofrecido en vez de volcado. Y verifica que el usuario entendió antes de pedirle que decida: una elección tomada sin entender las opciones no es una elección, y todo lo demás se construye encima de ella.

## Qué frameworks maneja

**De Roger Martin**, tratados como tres piezas separadas, no como uno solo:

- **Strategy Choice Cascade**: Winning Aspiration, Where to Play, How to Win, Must-Have Capabilities, Enabling Management Systems.
- **Strategic Logic Flow**: el análisis de cuatro dimensiones y siete elementos que alimenta el corazón de la Cascada (industria, clientes, posición relativa, competencia).
- **Strategic Choice Structuring Process (SCSP)**, con el manejo explícito del *What Would Have To Be True*: encuadrar el problema como una brecha, generar posibilidades, especificar condiciones, identificar barreras, diseñar y correr pruebas, elegir.

**De Michael Porter**, incrustados donde corresponde en vez de como sección aparte:

- **Cinco Fuerzas**: dentro del atractivo estructural del Strategic Logic Flow.
- **Estrategias genéricas** (costo, diferenciación, atascado en el medio): dentro de How to Win.
- **Cadena de valor y encaje (fit)**: dentro de Must-Have Capabilities y Enabling Management Systems.
- **Las cinco pruebas de una buena estrategia**: como control de calidad final, antes de compilar el memo.

## La estrategia como grafo de nodos

En vez de un documento monolítico que crece sin control, el skill construye la estrategia como **diez nodos**, uno por decisión, conectados por un **grafo de dependencias fijo**. Cada nodo declara su estado en su frontmatter (`vacio`, `borrador`, `decidido`, `desactualizado`), y el grafo dice qué alimenta a qué.

Eso compra tres cosas:

- **Lectura selectiva.** Para escribir un nodo se leen sus dependencias y sus dependientes ya decididos, no la carpeta entera.
- **Detección de contradicciones por construcción.** Tocar un nodo obliga a revisar los que lo usan, y los que quedaron colgando se marcan `desactualizado` solos.
- **Un final visible.** El índice recalcula en todo momento qué falta para poder compilar el memo.

Los ocho nodos que van al memo:

- **Problema a resolver**: la brecha entre el resultado que se quiere y el que se tiene, dicha desde el cliente y no desde el estado financiero.
- **Winning Aspiration**: qué significa ganar, con quién y contra quién, traducido a medidas concretas.
- **Where to Play y How to Win**: dónde se compite (y con el mismo peso, dónde no) y la teoría de por qué se gana en ese campo. Van en un solo nodo porque son un par inseparable: separarlos es donde más riesgo hay de que queden incoherentes entre sí.
- **Must-Have Capabilities**: las pocas capacidades que sostienen el How to Win, con el sistema de actividades que las produce.
- **Enabling Management Systems**: qué sistemas construyen y sostienen esas capacidades, y qué se mide.
- **Posibilidades descartadas**: qué otras opciones se consideraron, qué condición no se sostuvo y qué prueba lo demostró.
- **Supuestos vivos**: condiciones que la estrategia necesita y que todavía no están verificadas, cada una con su prueba, su responsable y su fecha.
- **Señales de cambio**: las tres condiciones de Porter que, si ocurren, invalidan la estrategia elegida.

Más dos anexos que no entran al memo y por eso pueden ser largos: el **Strategic Logic Flow** (de dónde salió cada elección) y **Posibilidades y What Would Have To Be True** (el plano entero, para cuando alguien cuestione una elección dentro de un año).

## La carpeta de trabajo

Tres capas con dueños distintos: lo que entra es del usuario y es inmutable, lo que se genera es del skill, y en la raíz quedan el mapa y la línea de tiempo.

```
[carpeta de trabajo]/
├── index.md            el hub: estado de los nodos, alertas, qué falta
├── log.md              cronológico, append only, una línea por decisión
├── 00_context/         lo que entra. Se lee, no se edita ni se borra.
│   ├── inbox/          sin procesar. Se vacía moviendo el archivo un nivel arriba.
│   └── sources.md      fuentes externas que no tienen archivo
└── 01_outputs/         todo lo que genera el skill
    ├── sections/       los diez nodos
    └── estrategia.md   el memo, compilado al final
```

Un archivo del inbox, una vez consumido, se **mueve** a `00_context/` en vez de borrarse: su procedencia queda registrada por el hecho de estar ahí, sin necesidad de un registro paralelo que haya que mantener sincronizado.

El memo se compila solo cuando todos los nodos están decididos, no hay contradicciones abiertas y pasa las cinco pruebas de Porter, respetando la regla de Roger Martin de que una estrategia que no cabe en cinco páginas probablemente no está bien pensada. Y nunca se edita directo: se cambia el nodo y se recompila.

## El script del grafo

`scripts/graph.py` hace el trabajo mecánico, que hecho a mano cuesta tokens y deriva. Sin dependencias, solo la librería estándar. Se corre desde la raíz de la carpeta de trabajo:

| Comando | Qué hace |
|---|---|
| `init "<entidad>" "<nivel>"` | Crea la estructura completa, los diez nodos y el índice |
| `status` | Tabla de estado de los diez nodos |
| `deps <nodo>` | Qué leer antes de escribir ese nodo |
| `touch <nodo> --apply "<motivo>"` | Marca `desactualizado` los dependientes decididos |
| `sync` | Regenera el índice y los wikilinks de cada nodo |
| `lint` | Nodos huecos, huérfanos, desactualizados, inbox pendiente, supuestos sin prueba |
| `archive` | Corta `log.md` en la última compilación del memo y archiva lo anterior |

`init` deja una copia del script dentro de la carpeta de trabajo, así que a partir de la segunda sesión se corre con una ruta relativa. Todos los comandos aceptan `--root "<ruta>"` para operar sin hacer `cd`.

Los wikilinks que el script escribe al pie de cada nodo hacen que la vista de grafo de Obsidian muestre la estructura real de la estrategia. Si el entorno no tiene Python, el skill hace lo mismo a mano: el grafo está declarado también en `SKILL.md`, y ningún paso del proceso depende de que el script corra.

## Compatibilidad

Probado en Claude Code y compatible con Claude Cowork. El script usa solo la librería estándar de Python (3.6+), opera con rutas relativas y tolera rutas con espacios y caracteres no ASCII.

Para subirlo a Cowork como skill individual (Customize → Skills → Upload), empaqueta el repo en un `.zip` o `.skill` cuya raíz sea una carpeta `on-strategy/`:

```bash
zip -r on-strategy.skill on-strategy -x '*.git*'
```

Claude.ai limita la descripción del skill a 200 caracteres en algunos flujos de subida. La descripción de `SKILL.md` es más larga porque es lo que hace que el skill dispare bien. Si la subida la rechaza, usa esta variante corta:

> Define la estrategia de una empresa o unidad con Playing to Win (Roger Martin) y Porter, co-construida decisión a decisión sobre una carpeta de trabajo: dónde competir, cómo ganar, qué capacidades.

## Estructura del skill

```
on-strategy/
├── .claude-plugin/             manifiestos de plugin y de marketplace
├── SKILL.md                    proceso, carpeta de trabajo, grafo, operaciones
├── scripts/
│   └── graph.py                init, status, deps, touch, sync, lint
└── references/
    ├── playing-to-win.md       los tres marcos de Martin
    ├── porter-analisis.md      Cinco Fuerzas, ventaja competitiva, cadena de valor
    ├── porter-pruebas.md       las cinco pruebas, genéricas, errores típicos
    ├── nodos.md                qué va en cada nodo y sus criterios de calidad
    ├── memo.md                 la compuerta y la compilación del memo
    ├── investigacion.md        protocolo de evidencia y deep research
    └── ejemplos.md             casos de ambos libros, indexados por concepto
```

`SKILL.md` mantiene el proceso liviano y apunta a la sección exacta de la referencia que corresponde a cada bloque, para no cargar archivos enteros. Ningún archivo copia contenido de los libros fuente: son síntesis y reformulación propia, con citas puntuales atribuidas.

## Instalación

Este repo es a la vez el skill y un marketplace de plugin, así que hay dos caminos. El de marketplace es el recomendado: sirve en Claude Code y en Claude Cowork, y se actualiza con un botón.

### Como plugin, desde este repo (recomendado)

**Claude Cowork:** Customize → Plugins → Add marketplace, y pega `jlatorree/on-strategy`. Después instala `on-strategy` desde la lista. El botón Update trae la última versión.

**Claude Code:**

```bash
claude plugin marketplace add jlatorree/on-strategy
```

```bash
claude plugin install on-strategy@on-strategy
```

Para actualizar:

```bash
claude plugin marketplace update on-strategy
```

### Como skill clonado

A nivel global, disponible en cualquier proyecto de Claude Code:

```bash
git clone https://github.com/jlatorree/on-strategy.git ~/.claude/skills/on-strategy
```

A nivel de proyecto, solo en el repo donde lo instalas:

```bash
git clone https://github.com/jlatorree/on-strategy.git .claude/skills/on-strategy
```

Para actualizar, entra a la carpeta del skill instalado y corre `git pull`.

**No uses los dos caminos a la vez.** Dos copias del mismo skill cargan su descripción dos veces en cada sesión y divergen en cuanto actualizas una sola.

## Uso

El skill dispara cuando el usuario quiere definir o rehacer una estrategia, cuestionar si lo que tiene es estrategia o solo un plan, decidir dónde competir, entender cómo ganarle a un competidor, o analizar su industria o posición competitiva, aunque no mencione explícitamente ningún framework.

## Fuentes

- A.G. Lafley y Roger L. Martin, *Playing to Win: How Strategy Really Works* (Harvard Business Review Press, 2013).
- Joan Magretta, *Understanding Michael Porter: The Essential Guide to Competition and Strategy* (Harvard Business Review Press, 2012).
- La serie de ensayos [Playing to Win / Practitioner Insights](https://rogermartin.medium.com/) de Roger Martin, para la evolución del SCSP y las guías de comunicación de estrategia posteriores al libro.

La arquitectura de la carpeta de trabajo (capa de fuentes inmutable, capa generada por el modelo, `index.md` como catálogo y `log.md` cronológico con prefijo parseable) sigue el patrón [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) de Andrej Karpathy.

Este repositorio no incluye los libros fuente ni reproduce su texto: contiene una síntesis y reformulación original con fines de referencia operativa.

## Licencia

[MIT](LICENSE). El código (`scripts/graph.py`) y el proceso del skill son de uso, modificación y redistribución libres. Ver la nota de fuentes arriba: la síntesis de los frameworks es reformulación original, no una copia de los libros.
