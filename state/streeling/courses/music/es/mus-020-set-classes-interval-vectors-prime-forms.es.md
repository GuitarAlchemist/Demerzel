---
module_id: mus-020-set-classes-interval-vectors-prime-forms
department: music
course: Clases de conjuntos, vectores interválicos, relación Z y formas primas
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-001-what-is-a-chord, mus-002-beyond-tonality]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Clases de conjuntos, vectores interválicos, relación Z y formas primas — Dos compactaciones, un catálogo

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración estimada: 60 minutos

## Objetivos

Al terminar esta lección, podrás:
- Agrupar conjuntos de clases de altura solo por transposición y por transposición e inversión, y deducir de la simetría de un conjunto cuántos conjuntos contiene su clase
- Calcular un vector de clases de intervalo, mostrar que toda una clase de conjuntos lo comparte, y decir qué le hace la multiplicación por 5
- Hallar un orden normal y una forma prima con la regla de Forte y con la de Rahn, y nombrar las seis clases de conjuntos en las que discrepan
- Explicar por qué el menor número de 12 bits entre las 24 formas de un conjunto es su forma prima según la regla de Rahn
- Contar clases de conjuntos con el lema de Burnside
- Enunciar el teorema del complemento y el teorema del hexacordio, y usarlos con la relación M para explicar cómo se reparten los 23 pares en relación Z y cómo se relacionan algunos de ellos
- Leer un número de Forte, y distinguirlo de un ordinal que solo se le parece
- Rastrear lo que GA calcula para cada uno de estos puntos, y dónde sus nombres, su documentación y sus pruebas dicen otra cosa

---

## 1. Conjuntos de clases de altura y sus simetrías

Numera las clases de altura de do = 0 a si = 11, como hace MUS-002. Un acorde, una escala o las notas de una melodía se convierten entonces en un **conjunto de clases de altura**, un subconjunto de las 12 clases de altura. Hay 2¹² = 4,096, desde el conjunto vacío hasta el agregado completo.

Dos tipos de operación mueven un conjunto sin cambiar su forma. La **transposición** Tn suma n a cada clase de altura, módulo 12. La **inversión seguida de una transposición**, TnI (In para abreviar), envía cada x a n − x. Juntas forman 24 operaciones. T2 convierte do mayor {0, 4, 7} en re mayor {2, 6, 9}. I0 lo convierte en {0, 8, 5}, fa menor, e I7 en {7, 3, 0}, do menor: un espejo que intercambia do y sol y convierte mi en mi♭.

Los conjuntos relacionados por una transposición forman un **tipo Tn**; los conjuntos relacionados por una transposición o una inversión forman una **clase de conjuntos**. Los 4,096 conjuntos se reparten en 352 tipos Tn y 224 clases de conjuntos. Una tríada mayor y una tríada menor son dos tipos Tn de una misma clase de conjuntos, que el catálogo de Forte (§6) etiqueta 3-11.

El número de conjuntos de una clase depende de la simetría de sus miembros. Si k de las 24 operaciones llevan un conjunto sobre sí mismo, su clase contiene 24 / k conjuntos. Solo T0 lleva una tríada mayor sobre sí misma, así que su clase contiene 24 conjuntos: las 12 tríadas mayores y las 12 menores. T0, T4, T8 y tres inversiones llevan la tríada aumentada do mi sol♯ sobre sí misma, así que su clase contiene 24 / 6 = 4 conjuntos. La clase del acorde de séptima disminuida contiene 3 conjuntos, la de la escala de tonos enteros 2, y la del agregado 1.

### Ejercicio práctico

La clase de C7, do mi sol si♭, contiene 24 conjuntos; la de Cmaj7, do mi sol si, solo 12. ¿Por qué?

> *Solución:* Solo T0 lleva C7 sobre sí mismo, así que su clase contiene 24 conjuntos: las 12 séptimas de dominante y sus 12 inversiones, las séptimas semidisminuidas (I0 convierte {0, 4, 7, 10} en {0, 8, 5, 2}, re fa la♭ do, Dø7). Cmaj7 es su propia inversión: I11 intercambia do con si y mi con sol. Dos de las 24 operaciones lo llevan sobre sí mismo, así que su clase contiene 24 / 2 = 12 conjuntos, las séptimas mayores.

---

## 2. Vectores de clases de intervalo

Toma cada par de notas de un conjunto, mide el intervalo entre ellas en semitonos, y redúcelo a una **clase de intervalo** de 1 a 6: un intervalo y su inversión, como una cuarta y una quinta, forman una sola clase. Los seis recuentos forman el **vector de clases de intervalo** del conjunto, también llamado vector interválico. Un conjunto de n notas tiene n(n − 1)/2 pares, y los recuentos suman ese número. Do mayor tiene una tercera menor (mi–sol), una tercera mayor (do–mi) y una quinta (do–sol): <001110>. C7 tiene <012111>, Cmaj7 <101220>, el acorde de séptima disminuida <004002> y la escala mayor <254361>.

Todos los conjuntos de una clase de conjuntos tienen el mismo vector. Una transposición conserva la diferencia entre dos notas cualesquiera. Una inversión convierte una diferencia d en −d, que es la misma clase de intervalo. Así, do mayor y do menor comparten <001110>, y C7 y Cø7 comparten <012111>. Lo recíproco es falso: dos conjuntos pueden compartir un vector sin compartir una clase (§5).

Multiplicar cada clase de altura por 5, la operación **M5**, no es una de las 24 operaciones del §1, pero su efecto sobre el vector es sencillo. Multiplica cada intervalo por 5: 1 se convierte en 5; 2 se convierte en 10, clase de intervalo 2; 3 se convierte en 15, es decir, 3; 4 se convierte en 20, es decir, 8, clase de intervalo 4; 5 se convierte en 25, es decir, 1; y 6 se convierte en 30, es decir, 6. Así que M5 intercambia los recuentos de las clases de intervalo 1 y 5 y conserva los demás. El pentacordio cromático do do♯ re mi♭ mi, <432100>, se convierte en do fa si♭ mi♭ la♭, <032140>: una pila de cuartas, la escala pentatónica. M5 envía 132 de las 224 clases de conjuntos a otra clase: envía do mayor a do la♭ si, un miembro de la clase escrita (014) en el §3. M7 es M5 seguida de I0, ya que 7 = −5 mod 12.

### Ejercicio práctico

Calcula el vector de do mi sol la, que es a la vez C6 y Am7.

> *Solución:* Seis pares, por clase de intervalo: do–mi (4), do–sol (5), do–la (3), mi–sol (3), mi–la (5) y sol–la (2). Una clase de intervalo 2, dos 3, una 4 y dos 5: <012120>.

---

## 3. Orden normal y forma prima: dos maneras de compactar

Para nombrar una clase de conjuntos, los teóricos eligen un miembro y lo escriben en un orden estándar. El **orden normal** de un conjunto es la rotación de sus notas, en orden ascendente alrededor de la octava, con la menor amplitud de la primera a la última nota. Cuando varias rotaciones empatan, se comparan por sus intervalos desde la primera nota, y el empate puede deshacerse desde cualquiera de los dos extremos:

- **Forte (1973)** compacta hacia la izquierda: el menor intervalo de la primera nota a la segunda, luego a la tercera, y así sucesivamente.
- **Rahn (1980)** compacta desde la derecha: el menor intervalo de la primera nota a la penúltima, luego a la anterior, y así sucesivamente.

La **forma prima** compara los órdenes normales del conjunto y de su inversión, ambos transpuestos para empezar en 0, con la misma regla, y conserva el más compacto. Las formas primas se escriben entre paréntesis sin comas, con T y E para 10 y 11: (037) para ambas tríadas.

Las dos reglas solo pueden diferir cuando hay candidatos empatados en la amplitud. Toma 5-20, do do♯ fa fa♯ la♭, {0, 1, 5, 6, 8}. Dos rotaciones tienen amplitud 8: 0 1 5 6 8 y, desde fa, 0 1 3 7 8. La inversión da dos más de amplitud 8, 0 1 5 7 8 y 0 2 3 7 8. Desde la izquierda, los segundos intervalos son 1, 1, 1 y 2; entre las tres primeras, los terceros intervalos son 5, 3 y 5, así que la forma prima de Forte es (01378). Desde la derecha, los penúltimos intervalos son 6, 7, 7 y 7, así que la forma prima de Rahn es (01568). En las 224 clases de conjuntos, las dos reglas discrepan en seis:

| Clase de conjuntos | Rahn | Forte |
|---|---|---|
| 5-20 | (01568) | (01378) |
| 6-Z29 | (023679) | (013689) |
| 6-31 | (014579) | (013589) |
| 7-Z18 | (0145679) | (0123589) |
| 7-20 | (0125679) | (0124789) |
| 8-26 | (0134578T) | (0124579T) |

Estas seis clases contienen 120 de los 4,096 conjuntos. Todos los demás conjuntos reciben la misma forma prima de ambas reglas.

**Por qué un ordenador puede prescindir de las reglas.** Escribe un conjunto como un número de 12 bits, con el bit p activado cuando la clase de altura p está presente: do mayor {0, 4, 7} es 1 + 16 + 128 = 145. Comparar dos de esos números compara primero sus clases de altura más altas, ya que 2^p es mayor que la suma de todas las potencias de 2 inferiores. Entre las 24 formas de un conjunto, el menor número contiene 0, porque transponer un conjunto hacia abajo baja cada bit. Después tiene la menor última nota, que es la menor amplitud, luego la menor penúltima nota, y así sucesivamente. Esa es la regla de Rahn. Para 5-20, (01568) es 1 + 2 + 32 + 64 + 256 = 355, y (01378) es 395.

### Ejercicio práctico

El conjunto do do♯ mi fa sol la, {0, 1, 4, 5, 7, 9}, pertenece a 6-31. Da su forma prima según cada regla, y el número de 12 bits de cada una.

> *Solución:* Cuatro formas tienen amplitud 9: 0 1 4 5 7 9 y, desde mi, 0 1 3 5 8 9, luego 0 2 4 5 8 9 y 0 1 4 6 8 9, que vienen de la inversión. Desde la izquierda, los segundos intervalos son 1, 1, 2 y 1, y los terceros intervalos de las tres restantes son 4, 3 y 4: la de Forte, (013589), 1 + 2 + 8 + 32 + 256 + 512 = 811. Desde la derecha, los penúltimos intervalos son 7, 8, 8 y 8: la de Rahn, (014579), 1 + 2 + 16 + 32 + 128 + 512 = 691. El número menor es el de Rahn.

---

## 4. Contar clases de conjuntos

El **lema de Burnside** cuenta clases sin enumerarlas: el número de clases es la media, sobre las operaciones, del número de conjuntos que cada operación deja sin cambios.

Toma los 220 conjuntos de tres notas. Entre las 12 transposiciones, T0 deja sin cambios los 220, T4 y T8 dejan sin cambios las 4 tríadas aumentadas, y las demás no dejan ninguno: (220 + 4 + 4) / 12 = 19 tipos Tn. Añade ahora las 12 inversiones. Cuando n es par, TnI refleja el círculo de las clases de altura respecto de un eje que pasa por dos clases de altura, n/2 y n/2 + 6. Deja sin cambios un conjunto de tres notas cuando el conjunto contiene una de esas dos y uno de los cinco pares que el espejo intercambia: 2 × 5 = 10 conjuntos. Cuando n es impar, el eje pasa entre clases de altura, cada nota se intercambia con otra, y ningún conjunto de tres notas queda sin cambios. Así que (228 + 6 × 10) / 24 = 12 clases de conjuntos.

| Notas | Clases de conjuntos | Tipos Tn |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 6 | 6 |
| 3 | 12 | 19 |
| 4 | 29 | 43 |
| 5 | 38 | 66 |
| 6 | 50 | 80 |
| 7 | 38 | 66 |
| 8 | 29 | 43 |
| 9 | 12 | 19 |
| 10 | 6 | 6 |
| 11 | 1 | 1 |
| 12 | 1 | 1 |
| Total | 224 | 352 |

Las columnas son simétricas, porque la complementación empareja los conjuntos de n notas con los de 12 − n. Una clase contiene un solo tipo Tn cuando una inversión lleva sus miembros sobre sí mismos, y dos en caso contrario, como 3-11A, las tríadas menores, y 3-11B, las tríadas mayores. Así que 352 − 224 = 128 clases contienen dos tipos Tn, y las otras 96 son simétricas por inversión. Los totales son los números de pulseras y de collares binarios de 12 cuentas (OEIS A000029 y A000031).

### Ejercicio práctico

¿Cuáles de las 12 clases de tricordios son su propia inversión? Comprueba que el recuento concuerda con los 19 tipos Tn.

> *Solución:* (012), (024), (027), (036) y (048), las clases de do do♯ re, do re mi, do re sol, do mi♭ sol♭ y do mi sol♯: invertir cualquiera de ellas da una transposición del mismo conjunto. Las otras 7 clases contienen dos tipos Tn cada una, así que 5 + 2 × 7 = 19.

---

## 5. Complementos y relación Z

El **complemento** de un conjunto contiene las clases de altura que le faltan, y su vector se deduce del vector del conjunto. Fija una clase de intervalo k de 1 a 5. El agregado contiene 12 pares de clase de intervalo k, y cada nota tiene dos compañeras a esa distancia. Si un conjunto de n notas contiene a_k de esos pares, sus notas participan en 2n pares contados desde su lado, 2a_k de ellos dentro del conjunto, así que 2n − 2a_k pares cruzan hacia el complemento. El complemento conserva el resto: 12 − a_k − (2n − 2a_k) = a_k + 12 − 2n. Para el tritono, con 6 pares en total y una compañera por nota, el mismo recuento da a_6 + 6 − n. Este es el **teorema del complemento**: cada recuento salvo el del tritono varía en 12 − 2n, y el del tritono en 6 − n.

Para un hexacordio, n = 6, así que un hexacordio y su complemento tienen el mismo vector. Este es el **teorema del hexacordio**, a menudo atribuido a Babbitt.

Dos clases de conjuntos con el mismo número de notas y el mismo vector están **en relación Z**. Hay 23 de esos pares. Uno está entre los tetracordios, 4-Z15 (0146) y 4-Z29 (0137), ambos <111111>. Tres están entre los pentacordios, 15 entre los hexacordios, 3 entre los heptacordios y 1 entre los octacordios. El teorema del complemento explica la simetría: los complementos de dos conjuntos en relación Z también comparten un vector, así que los pares de 4 y 8 notas, y los de 5 y 7, van juntos. De las 50 clases de hexacordios, 20 contienen sus propios complementos. Cada una de las otras 30 tiene sus complementos en su compañera Z, lo que da cuenta de los 15 pares de hexacordios.

M5 da cuenta de algunos pares de otra manera. Intercambia los recuentos de las clases de intervalo 1 y 5 (§2), así que un conjunto cuyos dos recuentos son iguales conserva su vector bajo M5: la imagen está en la misma clase o en su compañera Z. 4-Z15 es un caso así: 0 1 4 6 por 5 da 0 5 8 6, cuyo orden normal 5 6 8 0 da (0137), 4-Z29. Nueve de los 23 pares están relacionados así: 4-Z15/4-Z29, 5-Z17/5-Z37, 5-Z18/5-Z38, 6-Z6/6-Z38, 6-Z11/6-Z40, 6-Z19/6-Z44, 7-Z17/7-Z37, 7-Z18/7-Z38 y 8-Z15/8-Z29.

### Ejercicio práctico

Muestra que 5-Z17 (01348) y 5-Z37 (03458) tienen el mismo vector, y que M5 lleva una sobre la otra.

> *Solución:* Ambas tienen <212320>. Multiplicar 0 1 3 4 8 por 5 da 0 5 3 8 4, es decir, {0, 3, 4, 5, 8}. Su única rotación de amplitud 8 empieza en 0, y su inversión da la misma, así que su forma prima es (03458).

---

## 6. Números de Forte

Forte (1973) dio a cada clase de 3 a 9 notas, 208 en total, un nombre de la forma cardinalidad-índice: 3-11 es la undécima clase de tricordios. Una Z delante del índice marca una clase en relación Z. Dos convenciones hacen el catálogo más cómodo. Salvo en los hexacordios en relación Z, cuyos complementos están en la compañera Z, una clase de n notas y la clase de sus complementos llevan el mismo índice: 4-Z15 y 8-Z15, o 5-35, la escala pentatónica, y 7-35, la colección diatónica que forma su complemento. Y de cada par de hexacordios en relación Z, uno lleva un índice de 3 a 29 y el otro un índice de 36 a 50.

Las etiquetas son de Forte; las formas impresas junto a ellas dependen de la compactación. Una tabla que sigue a Rahn imprime (01568) junto a 5-20, una que sigue a Forte imprime (01378). Un ordinal que cuenta según otro orden no es un número de Forte, aunque tenga la misma forma (§7).

### Ejercicio práctico

Las teclas negras de un piano, do♯ re♯ fa♯ sol♯ la♯, forman una escala pentatónica. Nombra su clase y la clase de las teclas blancas.

> *Solución:* 5-35, (02479), y 7-35, (013568T), para las siete teclas blancas, su complemento. El índice es el mismo, como en todo par de clases complementarias salvo los hexacordios en relación Z.

---

## 7. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); esta lección documenta ese código sin modificarlo, y no ha ejecutado GA ni sus pruebas. Los archivos que cita no han cambiado en la rama `main` de GA en `6d5ff22`. La [lección 4 de music-theory-ga](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/04-set-classes.mdx) de Learn compila una versión anterior de GA, `a826864`, y comprueba sus clases de conjuntos frente a las definiciones de los manuales. Los demás números de abajo vienen de una transcripción en Python, línea por línea, del código de GA nombrado.

**Las formas primas son las de Rahn, por el número.** [`PitchClassSetId.PrimeForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L137) conserva el menor identificador entre las 24 formas, y [`PitchClassSet.PrimeForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L161) y [`SetClass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L53) se basan en él. Según el §3, esa es la regla de Rahn, y el programa de Learn, compilado en `a826864`, la encontró en [4,096 de 4,096 conjuntos](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l4.txt#L45). La propia prueba de GA compara la forma prima con lo que llama un [oráculo independiente](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L32), que también toma el menor de los 24 identificadores. Fija la definición en lugar de contrastarla con una regla de compactación, y ninguno de sus [tres puntos de anclaje](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L89) está entre las seis clases del §3.

**La forma normal no es la de los manuales.** [`ToNormalForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L420) conserva la rotación cuyas separaciones entre notas sucesivas, alrededor del círculo, son las más regulares: la menor diferencia entre la separación mayor y la menor, y luego la secuencia de separaciones lexicográficamente menor. Sus observaciones lo dicen, [«This is not the textbook normal form»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L415), y el código llama a esa diferencia de separaciones [«span»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L671). La tabla que lee `ToNormalForm` la construye [este bucle](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L631):

```csharp
                var rotation = Rotr12(set, member);
                Gaps(rotation, count, gaps);
                var span = Span(gaps[..count]);
                if (span > bestSpan || (span == bestSpan && !MoreCompact(gaps[..count], bestGaps[..count])))
                {
                    continue;
                }
```

En los 4,095 conjuntos no vacíos, su respuesta difiere en 1,998 del orden normal de la regla de Rahn transpuesto a 0. El ejemplo del propio método todavía describe la regla de los manuales: para sol si re, dice que el resultado 0 3 8 es el más compacto, con una amplitud [de 0 a 8](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L402), aunque 0 4 7, desde sol, abarca 7. La forma prima no usa este método, pero la [búsqueda de la tonalidad más cercana](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L559) de GA sí lo usa: espera una tonalidad menor cuando la forma normal contiene la clase de altura 3. Toda tríada mayor recibe 0 3 8, así que para do mi sol, que contienen tres tonalidades mayores y tres menores, la búsqueda elige una tonalidad menor.

**La relación Z y la relación M.** [`IsZRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L199) busca en la [familia modal](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L114) del conjunto, los conjuntos que contienen 0 y comparten su vector, un miembro que no esté entre las 24 formas del primer miembro de la familia. La transcripción concuerda con el vector en los 4,096 conjuntos, y [una prueba](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L82) la contrasta con la Z de cada etiqueta almacenada. [`SetClass.MRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L80) aplica M5 a una clase, y 92 de las 224 clases son su propia imagen por M5.

**Dos catálogos.** [`CanonicalForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L25) almacena las etiquetas de Forte de 1 a 6 notas y deduce las de 7 a 11 notas [del complemento](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L227). Sus observaciones dicen que [«the stored prime forms are Rahn's»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L16) y nombran las seis clases del §3. [`ProgrammaticForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L110) numera las clases de cada tamaño por el identificador de su vector, y luego por el de su forma prima:

```csharp
            var ordered = group
                .OrderBy(sc => sc.IntervalClassVector.Id)
                .ThenBy(sc => sc.PrimeForm.Id.Value)
                .ToList();

            for (var i = 0; i < ordered.Count; i++)
            {
                var setClass = ordered[i];
                var forte = new ForteNumber(cardinality, i + 1);
                result[setClass.PrimeForm.Id] = forte;
            }
```

Su resumen llama al resultado un [«Forte-style catalog»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L6), y sus observaciones califican de [«minor»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L18) las diferencias con la numeración de Forte. De las 208 clases de la tabla de Forte, da el mismo índice que Forte a 3: 5-Z18, 6-21 y 8-Z15. La tríada mayor sale 3-2, y la colección diatónica 7-1. [`ForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ForteCatalog.cs#L11) dice que el ordinal «diverges for most set classes» y no debe mostrarse a los usuarios. La issue [#544](https://github.com/GuitarAlchemist/ga/issues/544) de GA, ya cerrada, encontró {4, 5, 10, 11} etiquetado 4-21 en lugar de 4-9, y el reconocedor de acordes la cita donde [nombra un acorde según el catálogo de Forte](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L327). [`SetClassLabelFormatter`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClassLabelFormatter.cs#L32) sigue ofreciendo el ordinal como la notación «Rahn», aunque el nombre de Rahn corresponde a una regla de compactación, no a una numeración.

**Lo que comprueban las pruebas del catálogo.** Las [pruebas del catálogo](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L7) lo demuestran «against GA's own atonal engine» con cuatro restricciones: cada forma almacenada es una clase de conjuntos de GA, los recuentos por tamaño coinciden, las etiquetas corresponden una a una a las clases de GA, y los marcadores Z concuerdan con `IsZRelated`. Tres pruebas las imponen: [los recuentos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L32), [la correspondencia una a una](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L47), que también cubre la pertenencia, y [los marcadores Z](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L82). Una cuarta comprueba [el viaje de ida y vuelta](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L145) de la forma a la etiqueta y de vuelta a la forma. Muestran que la tabla concuerda con GA y consigo misma, no que sea la de Forte: intercambiar las formas de dos etiquetas almacenadas del mismo tamaño y el mismo estado Z, como 5-1 y 5-2, las mantendría todas verdaderas. Las otras pruebas del archivo nombran nueve etiquetas, y ninguna de 5-1, 5-2, 7-1 o 7-2 está entre ellas (§8, paso 5).

**El identificador del vector.** [`IntervalClassVectorId`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L17) empaqueta los seis recuentos como dígitos en base 12. Los recuentos de 12 del agregado no caben en un dígito, y su identificador se [decodifica ahora como un caso especial](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L49). La lección 4 de Learn, compilada en `a826864`, todavía muestra la respuesta anterior, [<1 1 1 1 0 6>](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l4.txt#L18).

**Lo que lee el chatbot.** La habilidad [`IntervalClassVectorSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L31) del chatbot construye un acorde a partir de su propia tabla de cualidades. Pasa la cualidad a minúsculas [antes de comparar](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L199), así que «CM7» se convierte en «m7» y recibe el vector de una séptima menor, <012120>, en lugar del de la séptima mayor, <101220>, aunque [su tabla incluye «M7»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L206). Una cualidad que no está en la tabla, como C7♯9, C13 o Cadd9, recae en [la tríada mayor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L216), y la respuesta lleva igualmente [una confianza de 1.0](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L226). Su [patrón de acordes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L66) también toma el artículo de «ICV of a major scale» por el acorde A.

Corregir cualquiera de estas cosas corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

El método `ToNormalForm` de GA devuelve 0 3 8 para sol si re. ¿Qué da el orden normal de los manuales, y por qué la forma prima de GA sigue saliendo bien?

> *Solución:* Las rotaciones son sol si re (0 4 7, amplitud 7), si re sol (0 3 8, amplitud 8) y re sol si (0 5 9, amplitud 9). Tanto la regla de Forte como la de Rahn conservan sol si re, 0 4 7, ya que su amplitud es la única menor. La forma prima de GA nunca llama a `ToNormalForm`: toma el menor identificador de las 24 formas, lo que da (037).

---

## 8. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA; la versión de GA fijada en el laboratorio pasaría primero a `5c3a52a`. Nada en ella es una medición. Las predicciones vienen de la transcripción del §7 y se escriben antes de cualquier ejecución; una versión posterior de esta lección dará los resultados. Cada paso llama a los tipos de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **Formas primas.** Para los 4,096 conjuntos, comparar `PitchClassSet.PrimeForm` con las reglas de Rahn y de Forte. Predicción: la de Rahn en los 4,096 conjuntos; la de Forte en todos salvo los 120 conjuntos de las seis clases del §3.
2. **Formas normales.** Comparar `ToNormalForm` con el orden normal de Rahn transpuesto a 0. Predicción: 1,998 diferencias entre los 4,095 conjuntos no vacíos, entre ellas sol si re, dada como 0 3 8.
3. **Complementos y Z.** En las 224 clases, contar las clases para las que `IsZRelated` es verdadero, y comparar cada clase de hexacordios con la clase de su complemento. Predicción: 46; el complemento está en la misma clase para 20 clases de hexacordios y en la compañera Z para las otras 30; y el teorema del complemento del §5 se cumple en los 4,096 conjuntos.
4. **La relación M.** Aplicar `SetClass.MRelated` a cada clase. Predicción: 92 clases son su propia imagen, y 9 de los 23 pares Z son imagen el uno del otro.
5. **Las pruebas del catálogo tras un intercambio.** En una copia de `CanonicalForteCatalog` dentro del laboratorio, nunca en GA mismo, intercambiar las formas de 5-1 y 5-2 y ejecutar las mismas cuatro pruebas sobre la copia. Predicción: las cuatro pasan.
6. **Dos numeraciones.** Comparar `ProgrammaticForteCatalog` con `CanonicalForteCatalog`, sin tener en cuenta la Z. Predicción: el mismo índice para 7 de las 224 clases: las cuatro clases de 0, 1, 11 y 12 notas, y 5-Z18, 6-21 y 8-Z15.
7. **Los vectores del chatbot.** Llamar a `IntervalClassVectorSkill.ExecuteAsync` con «ICV of CM7», «ICV of C7#9» y «ICV of a major scale». Predicción: <012120>; <001110> con una confianza de 1.0; y <001110> de nuevo.

### Ejercicio práctico

El paso 5 predice que las cuatro pruebas siguen pasando tras el intercambio. ¿Qué tipo de prueba fallaría?

> *Solución:* Una que compare cada forma almacenada con una copia de la tabla de Forte hecha independientemente del archivo de GA, introducida a partir de otra fuente. La pertenencia, los recuentos, una correspondencia una a una, los marcadores Z y un viaje de ida y vuelta no pueden distinguir dos etiquetas del mismo tamaño y el mismo estado Z.

---

## 9. Errores comunes

- **Llamar dos clases de conjuntos a las tríadas mayor y menor.** Son dos tipos Tn de una misma clase, 3-11.
- **Leer una forma prima sin su regla.** Seis clases tienen dos formas primas; comprueba si una tabla compacta hacia la izquierda o desde la derecha.
- **Tomar un vector compartido por una clase compartida.** 23 pares de clases comparten su vector.
- **Suponer que M5 conserva la clase de un conjunto o su vector.** Envía do mayor a (014); conserva el vector solo cuando los recuentos de las clases de intervalo 1 y 5 son iguales.
- **Tomar un ordinal por un número de Forte.** Una etiqueta de la forma n-k es de Forte solo si viene de la tabla de Forte.
- **Fiarse del nombre de un método.** La «forma normal» o el «span» de una biblioteca puede no ser el de los manuales; lee la definición.
- **Leer una prueba de coherencia como una prueba de corrección.** Una tabla puede concordar consigo misma en todas partes y aun así llevar una etiqueta errónea.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Conjunto de clases de altura** | Un subconjunto de las 12 clases de altura, numeradas de do = 0 a si = 11 |
| **Tipo Tn** | Los conjuntos relacionados entre sí por transposición |
| **Clase de conjuntos** | Los conjuntos relacionados entre sí por transposición o por inversión seguida de una transposición |
| **Vector de clases de intervalo** | Los recuentos de las seis clases de intervalo entre todos los pares de notas de un conjunto |
| **Orden normal** | La rotación de un conjunto con la menor amplitud, con los empates deshechos por la regla de Forte o la de Rahn |
| **Forma prima** | El más compacto de los órdenes normales de un conjunto y de su inversión, transpuesto para empezar en 0 |
| **Complemento** | Las clases de altura que un conjunto no contiene |
| **Relación Z** | La relación entre dos clases de conjuntos del mismo tamaño con el mismo vector de clases de intervalo |
| **M5** | La multiplicación de cada clase de altura por 5, que intercambia los recuentos de las clases de intervalo 1 y 5 |
| **Número de Forte** | La etiqueta cardinalidad-índice de Forte, con una Z para una clase en relación Z |

---

## Autoevaluación

**1. ¿Cuántos conjuntos contiene la clase del acorde de séptima disminuida, y por qué?**
> 3. T0, T3, T6, T9 y cuatro inversiones, 8 de las 24 operaciones, llevan do mi♭ sol♭ la sobre sí mismo, así que su clase contiene 24 / 8 = 3 conjuntos: los tres acordes de séptima disminuida.

**2. Un conjunto de cinco notas tiene el vector <212320>. ¿Cuál es el vector de su complemento?**
> <434541>. Con n = 5, el teorema del complemento suma 12 − 2n = 2 a los cinco primeros recuentos y 6 − n = 1 al del tritono.

**3. ¿Qué forma prima imprime para 6-Z29 una tabla que sigue a Forte, y cuál una que sigue a Rahn?**
> La de Forte, (013689), y la de Rahn, (023679). 6-Z29 es una de las seis clases en las que las reglas discrepan.

**4. El [`ProgrammaticForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L110) de GA etiqueta la tríada mayor como 3-2. ¿Es ese su número de Forte?**
> No. La tríada mayor es 3-11 en el catálogo de Forte, y 3-2 allí es (013). El ordinal programático sigue el identificador del vector, y da el mismo índice que Forte solo a 3 de las 208 clases de su tabla.

**Criterio de aprobación:** Agrupar conjuntos en tipos Tn y en clases de conjuntos y deducir el tamaño de una clase de su simetría; calcular un vector de clases de intervalo y el de su complemento; hallar la forma prima con ambas reglas y nombrar las seis clases en las que difieren; contar clases con el lema de Burnside; explicar la relación Z con el teorema del complemento y con M5; y distinguir un número de Forte de un ordinal.

---

## Base de investigación

- A. Forte, *The Structure of Atonal Music*, Yale University Press, 1973: el catálogo de clases de conjuntos, el orden normal compactado hacia la izquierda, los números de Forte y la relación Z
- J. Rahn, *Basic Atonal Theory*, Longman, 1980: el orden normal compactado desde la derecha
- J. N. Straus, *Introduction to Post-Tonal Theory*, 4.ª edición, W. W. Norton, 2016: orden normal, forma prima, vectores de clases de intervalo, complementos y relación Z
- OEIS A000029 y A000031: los números de pulseras y de collares binarios, 224 y 352 para 12 cuentas
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §7 enlaza a su línea; issue #544 de GA
- Learn, lección 4 de music-theory-ga y su salida esperada en el commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: la comprobación compilada de las formas primas de GA citada en el §7
- Experimento: propuesto en el §8, no ejecutado; esta lección no contiene ninguna medición propia
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
