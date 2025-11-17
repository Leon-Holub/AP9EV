# PSO Benchmark – Protokol


## Zadání

Otestujte tři varianty algoritmu PSO na vybraných testovacích funkcích:

- Lineární setrvačnost: **w = 0.8 → 0.3**, c1 = 2, c2 = 2, globální topologie (hvězda)
- Konstantní setrvačnost: **w = 0.7**, c1 = c2 = 1.49618, globální topologie
- Konstantní setrvačnost: **w = 0.6**, c1 = c2 = 1.49618, kruhová topologie (sousedství 2)

Parametry:
- Velikost populace: 20–100 (použito 40)
- MAXFES: 20 000
- vmax = 0.2 * (upper - lower)
- Ošetření hranic pomocí clamp + vynulování rychlosti

Během každé varianty je provedeno **10 běhů**, z nichž se počítá průměrná konvergenční křivka a statistiky výsledků.


## Metodika

Experimenty používají následující postup:

1. Pro každou testovací funkci (Sphere, Rosenbrock, Schwefel) se spustí tři varianty PSO.
2. Každá varianta je spuštěna **10×** se shodnými parametry.
3. Z každé série 10 běhů se získá:
   - průměrná konvergenční křivka
   - nejlepší, nejhorší, průměrná, mediánová a směrodatná odchylka finální hodnoty
4. Výsledky se ukládají do:
   - `charts/<function>.png` — graf konvergence
   - `results/<function>_results.md` — statistická tabulka
5. Tento protokol (`README.md`) je generován automaticky.


## Parametry PSO variant

| Varianta | w | c1 | c2 | Topologie |
|----------|----|------|------|-------------|
| Lineární w | 0.8 → 0.3 | 2.0 | 2.0 | global |
| Konstantní w | 0.7 | 1.49618 | 1.49618 | global |
| Konstantní w | 0.6 | 1.49618 | 1.49618 | ring (2 sousedé) |

---

## Výsledky

### Rosenbrock

![graf](charts\rosenbrock.png)

# Výsledky PSO – rosenbrock

| Varianta | Best | Worst | Mean | Median | Std |
|----------|------|-------|------|--------|------|
| lineární w (0.8→0.3) – global | 2.698724e+01 | 1.398901e+02 | 7.184747e+01 | 7.852437e+01 | 3.383196e+01 |
| w = 0.7 – global | 5.602839e+00 | 7.775462e+01 | 3.379981e+01 | 2.639522e+01 | 2.262980e+01 |
| **w = 0.6 – ring** | **2.506728e+00** | **1.415775e+02** | **4.776014e+01** | **4.496724e+01** | **4.420035e+01** |


**Hodnocení pro rosenbrock:**

- Nejlepší varianta: **w = 0.6 – ring**


---

### Schwefel

![graf](charts\schwefel.png)

# Výsledky PSO – schwefel

| Varianta | Best | Worst | Mean | Median | Std |
|----------|------|-------|------|--------|------|
| **lineární w (0.8→0.3) – global** | **2.903537e+03** | **5.433110e+03** | **3.950219e+03** | **3.911570e+03** | **6.990780e+02** |
| w = 0.7 – global | 3.336084e+03 | 6.121119e+03 | 4.664569e+03 | 4.513648e+03 | 8.980272e+02 |
| w = 0.6 – ring | 3.813326e+03 | 5.313214e+03 | 4.901484e+03 | 5.045657e+03 | 4.135127e+02 |


**Hodnocení pro schwefel:**

- Nejlepší varianta: **lineární w (0.8→0.3) – global**


---

### Sphere

![graf](charts\sphere.png)

# Výsledky PSO – sphere

| Varianta | Best | Worst | Mean | Median | Std |
|----------|------|-------|------|--------|------|
| lineární w (0.8→0.3) – global | 5.864500e-07 | 1.755876e-05 | 4.217092e-06 | 1.503929e-06 | 5.394013e-06 |
| **w = 0.7 – global** | **9.534390e-12** | **1.954348e-10** | **6.481594e-11** | **5.178048e-11** | **5.822667e-11** |
| w = 0.6 – ring | 4.708707e-08 | 3.643971e-07 | 1.133293e-07 | 9.148477e-08 | 8.915055e-08 |


**Hodnocení pro sphere:**

- Nejlepší varianta: **w = 0.7 – global**


---

## Celkové zhodnocení

- Nejčastější vítěz přes všechny funkce: **w = 0.6 – ring**

- Výskyt vítězů: `{'w = 0.6 – ring': 1, 'lineární w (0.8→0.3) – global': 1, 'w = 0.7 – global': 1}`


