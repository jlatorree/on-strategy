# on-strategy

Skill de [Claude Code](https://claude.com/claude-code) y Claude Cowork que actúa como socio de pensamiento estratégico. Co-construye con el usuario, en español y una decisión a la vez, la estrategia de una empresa o unidad de negocio, combinando los frameworks de Roger Martin (*Playing to Win*, con A.G. Lafley) y de Michael Porter (según *Understanding Michael Porter*, de Joan Magretta).

## Cómo procede el skill

Esa es la regla que gobierna todo lo demás. En cada elección: explica en lenguaje llano qué se decide y por qué importa, pregunta lo que solo el usuario sabe, propone opciones con su razonamiento y una recomendación, espera la decisión, y recién entonces la registra y avanza. Nunca asume una elección estratégica en nombre del usuario.

Toda sesión arranca con un **Paso 0 obligatorio**: diagnóstico de la entidad, la situación y lo que ya está decidido, seguido de una ruta de trabajo acordada explícitamente antes de tocar cualquier framework.

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

## Estructura del proyecto

```
on-strategy/
├── SKILL.md                          proceso, la regla de propone/decide, referencias
└── references/
    ├── playing-to-win.md             los tres marcos de Martin
    ├── understanding-porter.md       Porter según Magretta
    ├── ejemplos.md                   casos de ambos libros, indexados por concepto
    ├── investigacion.md              protocolo de evidencia y deep research
    └── entregable.md                 arquitectura del entregable modular
```

`SKILL.md` mantiene el proceso liviano y apunta a las referencias correspondientes; las referencias tienen las definiciones, criterios de calidad y errores típicos de cada marco. Ningún archivo copia contenido de los libros fuente: son síntesis y reformulación propia, con citas puntuales atribuidas.

## Cómo estructura el entregable

En vez de un documento monolítico que crece sin control, el skill construye la estrategia en secciones separadas dentro de la carpeta de trabajo del usuario, una por cada módulo que hay que decidir, en este orden:

- **Problema a resolver**: la brecha entre el resultado que se quiere y el que se tiene, dicha desde el cliente y no desde el estado financiero.
- **Winning Aspiration**: qué significa ganar, con quién y contra quién, traducido a medidas concretas.
- **Where to Play y How to Win**: dónde se compite (y con el mismo peso, dónde no) y la teoría de por qué se gana en ese campo. Van en un solo archivo porque son un par inseparable: separarlos es donde más riesgo hay de que queden incoherentes entre sí.
- **Must-Have Capabilities**: las pocas capacidades que sostienen el How to Win, con el sistema de actividades que las produce y cómo se refuerzan entre sí.
- **Enabling Management Systems**: qué sistemas construyen y sostienen esas capacidades, y qué se mide para saber si están funcionando.
- **Posibilidades descartadas**: qué otras opciones se consideraron en el camino, qué condición no se sostuvo y qué prueba lo demostró. Evita que alguien proponga de nuevo, dentro de un año, algo ya descartado.
- **Supuestos vivos**: condiciones que la estrategia necesita y que todavía no están verificadas, cada una con su prueba, su responsable y su fecha.
- **Señales de cambio**: las tres condiciones de Porter que, si ocurren, invalidan la estrategia elegida.
- **Strategic Logic Flow** *(anexo)*: el análisis de los siete elementos, con las Cinco Fuerzas dentro del atractivo estructural, que responde de dónde salió cada elección anterior.
- **Posibilidades y What Would Have To Be True** *(anexo)*: todas las posibilidades generadas, incluidas las que no llegaron a ningún lado, con el WWHTBT completo de cada una. El plano entero de la estrategia, para cuando alguien la cuestione más adelante.

Esos diez módulos viven junto a un índice y a dos registros transversales:

```
[carpeta de trabajo]/
├── index.md                  mapa de estado y dependencias entre secciones
├── inbox/                    para que el usuario deje contexto o feedback, se procesa y se vacía
├── secciones/                los diez módulos de arriba, cada uno con su frontmatter de estado
├── evidencia.md               cada dato marcado como verificado o como supuesto
├── bitacora-de-decisiones.md  registro cronológico, append-only
└── estrategia.md              el memo final, compilado solo cuando todo está decidido y es coherente
```

Cada sección lleva un frontmatter (`estado`, `depende_de`, `afecta_a`) que arma un grafo de dependencias. Antes de escribir cualquier sección, el skill relee de qué depende y qué depende de ella para detectar contradicciones y alertarlas antes de escribir. El memo (`estrategia.md`) se compila al final, respetando la regla de Roger Martin de que una estrategia que no cabe en cinco páginas probablemente no está bien pensada.

## Instalación

**A nivel de proyecto** (disponible solo en el repo donde lo instalas):

```bash
git clone https://github.com/jlatorree/on-strategy.git .claude/skills/on-strategy
```

**A nivel global** (disponible en cualquier proyecto):

```bash
git clone https://github.com/jlatorree/on-strategy.git ~/.claude/skills/on-strategy
```

Para actualizar a la última versión, entra a la carpeta del skill instalado y corre `git pull`.

## Uso

El skill dispara cuando el usuario quiere definir o rehacer una estrategia, cuestionar si lo que tiene es estrategia o solo un plan, decidir dónde competir, entender cómo ganarle a un competidor, o analizar su industria o posición competitiva, aunque no mencione explícitamente ningún framework.

## Fuentes

- A.G. Lafley y Roger L. Martin, *Playing to Win: How Strategy Really Works* (Harvard Business Review Press, 2013).
- Joan Magretta, *Understanding Michael Porter: The Essential Guide to Competition and Strategy* (Harvard Business Review Press, 2012).
- La serie de ensayos [Playing to Win / Practitioner Insights](https://rogermartin.medium.com/) de Roger Martin, para la evolución del SCSP y las guías de comunicación de estrategia posteriores al libro.

Este repositorio no incluye los libros fuente ni reproduce su texto: contiene una síntesis y reformulación original con fines de referencia operativa.
