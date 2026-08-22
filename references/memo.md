# Compilar el memo

El último paso, y es una **compilación con compuerta**, no una redacción. Lee este archivo solo cuando vayas a compilar.

La regla de Roger Martin que lo gobierna: **si son más de cinco páginas, es muy probable que sea una mala estrategia.** Un documento largo casi siempre significa que las elecciones no se hicieron.

---

## 1. La compuerta

Córrela y muéstrale al usuario el resultado antes de compilar. Si algo falla, dilo y nombra qué falta. El memo no se compila con una pieza rota adentro: un memo con dos elecciones incompatibles adentro es peor que uno incompleto, porque nadie se entera hasta que la ejecución falla.

`graph.py lint` responde los puntos 1 y 7 solo. Los demás los evalúas tú leyendo los nodos.

1. **Estado completo.** Ningún nodo con `destino: memo` está `vacio` o `desactualizado`, y no hay alertas abiertas en `index.md`.
2. **Las cinco pruebas de Porter.** Propuesta de valor distintiva, cadena de valor a medida, renuncias distintas de los rivales, encaje a lo largo de la cadena, continuidad en el tiempo. Detalle en `porter-pruebas.md`, sección 1.
3. **Coherencia de la Cascada.** Cada caja sostiene a la de al lado. El Where to Play y el How to Win se refuerzan. Las capacidades sirven al How to Win elegido y no a uno genérico.
4. **La prueba can't/won't.** ¿Por qué un rival no puede copiar esto, o no va a querer copiarlo? Si no hay respuesta, todavía no hay ventaja.
5. **Consistencia interna.** Los números de cada nodo coinciden entre sí y con lo que dicen las fuentes citadas.
6. **Nada genérico ni vacío.** Ningún nodo dice algo que cualquier competidor podría firmar igual.
7. **Hipótesis falsables.** Cada supuesto vivo tiene una prueba concreta, un responsable y una fecha.

---

## 2. La compilación

Lee los ocho nodos con `destino: memo` y destila. Destilar es podar: de cada nodo entra solo lo distintivo, lo que hace a esta organización distinta de sus rivales. **Si la frase la podría firmar igual cualquier competidor, no entra.** Hacer cosas cuyo opuesto es obviamente estúpido no es estrategia.

Estructura de `01_outputs/estrategia.md`:

```markdown
# Estrategia: [entidad]
[Nivel] · [fecha] · v[N] · Decide: [quién]
[Si esta cascada está anidada, las elecciones del nivel superior que entran como restricción]

## El problema a resolver
[de 00-problema-a-resolver]

## La estrategia en una página
[las cinco cajas, dos o tres líneas cada una]

## Winning Aspiration
[de 01]

## Where to Play
[de 02, primera parte, incluida la lista de dónde no jugar]

## How to Win
[de 02, segunda parte, incluida la prueba can't/won't]

## Must-Have Capabilities
[de 03]

## Enabling Management Systems y medidas
[de 04]

## Por qué esta y no las otras
[de 05]

## Lo que tendría que ser cierto y todavía no sabemos
[de 06]

## Qué nos haría cambiar de estrategia
[de 07]
```

**La sección "La estrategia en una página" se lee sola.** Alguien que solo lea eso tiene que entender la estrategia completa. Si no cabe en una página, las elecciones todavía no están hechas.

---

## 3. Visuales opcionales

Valen la pena cuando el memo va a circular. Van a `01_outputs/`.

- **Mapa de Where to Play.** Tu posición y la de los competidores en los dos ejes que más importan en esta industria. Lo que se busca ver es poco traslape: si tu punto está encima del de un rival, ahí está el problema.
- **Gráfico de How to Win.** Dónde estás en el eje precio relativo por costo relativo, y dónde están los rivales.

---

## 4. Después de compilar

El memo queda como salida derivada. Si más adelante cambia una decisión, se cambia el nodo correspondiente y se recompila. **El memo nunca se edita directo**, porque dejaría de reflejar los nodos y volveríamos al monolito.

Registra la compilación en `log.md` con el tipo `memo`.
