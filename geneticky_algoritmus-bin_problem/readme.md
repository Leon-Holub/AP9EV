## Použité parametry
Níže jsou uvedena hlavní nastavení genetického algoritmu a jejich vysvětlení.

- **RNG_SEED** = `40`  
  Seed generátoru náhodných čísel. Díky němu jsou výsledky reprodukovatelné.
- **RUNS** = `10`  
  Počet běhů na každou kombinaci dimenze, úlohy a selekční strategie.
- **DIM_LIST** = `[10, 30, 100]`  
  Délky binárního řetězce (D), pro které se testuje.
- **POP_FACTOR** = `5.0`  
  Populace má velikost `POP_FACTOR × D`, tedy např. 50 jedinců pro D=10.
- **ELITE_FRAC** = `0.10`  
  10 % nejlepších jedinců se zkopíruje přímo do další generace (elitismus).
- **P_CROSS** = `1.00`  
  Pravděpodobnost, že dojde k jednobodovému křížení.
- **P_MUT** = `0.0100`  
  Pravděpodobnost bitové mutace (otočení 0 ↔ 1) na jednotlivý bit.

- **Selekce rodičů:** ruletová (*roulette*) a pořadová (*rank*).
- **Křížení:** jednobodové (one-point crossover).
- **Mutace:** bit-flip s pravděpodobností `P_MUT` na každý bit.

**Rozpočet hodnocení:** 100 × D ( 10 → 1000 evaluací, 30 → 3000 evaluací, 100 → 10000 evaluací )

---

## Výsledky – onemax

### onemax – D=10

| Selekce | best | worst | mean | median | std |
|---------|------|-------|------|--------|-----|
| roulette | 10.00 | 10.00 | 10.00 | 10.00 | 0.00 |
| rank | 10.00 | 10.00 | 10.00 | 10.00 | 0.00 |

| roulette | rank |
| --- | --- |
| ![roulette](charts/onemax/10/roulette.png) | ![rank](charts/onemax/10/rank.png) |

### onemax – D=30

| Selekce | best | worst | mean | median | std |
|---------|------|-------|------|--------|-----|
| roulette | 30.00 | 29.00 | 29.60 | 30.00 | 0.52 |
| rank | 30.00 | 30.00 | 30.00 | 30.00 | 0.00 |

| roulette | rank |
| --- | --- |
| ![roulette](charts/onemax/30/roulette.png) | ![rank](charts/onemax/30/rank.png) |

### onemax – D=100

| Selekce | best | worst | mean | median | std |
|---------|------|-------|------|--------|-----|
| roulette | 87.00 | 81.00 | 83.90 | 83.50 | 1.85 |
| rank | 94.00 | 90.00 | 91.90 | 92.00 | 1.10 |

| roulette | rank |
| --- | --- |
| ![roulette](charts/onemax/100/roulette.png) | ![rank](charts/onemax/100/rank.png) |


---

## Výsledky – leading_ones

### leading_ones – D=10

| Selekce | best | worst | mean | median | std |
|---------|------|-------|------|--------|-----|
| roulette | 10.00 | 10.00 | 10.00 | 10.00 | 0.00 |
| rank | 10.00 | 10.00 | 10.00 | 10.00 | 0.00 |

| roulette | rank |
| --- | --- |
| ![roulette](charts/leading_ones/10/roulette.png) | ![rank](charts/leading_ones/10/rank.png) |

### leading_ones – D=30

| Selekce | best | worst | mean | median | std |
|---------|------|-------|------|--------|-----|
| roulette | 23.00 | 13.00 | 17.90 | 18.50 | 3.35 |
| rank | 27.00 | 14.00 | 20.70 | 21.50 | 3.92 |

| roulette | rank |
| --- | --- |
| ![roulette](charts/leading_ones/30/roulette.png) | ![rank](charts/leading_ones/30/rank.png) |

### leading_ones – D=100

| Selekce | best | worst | mean | median | std |
|---------|------|-------|------|--------|-----|
| roulette | 26.00 | 16.00 | 21.50 | 21.00 | 2.92 |
| rank | 29.00 | 18.00 | 22.30 | 21.00 | 3.40 |

| roulette | rank |
| --- | --- |
| ![roulette](charts/leading_ones/100/roulette.png) | ![rank](charts/leading_ones/100/rank.png) |


---

## Závěr

V rámci úkolu byl vytvořen genetický algoritmus, který pracuje s binární reprezentací a využívá elitismus, ruletovou a pořadovou selekci, jednobodové křížení a bitovou mutaci.

Algoritmus byl otestován na dvou úlohách – **OneMax** a **LeadingOnes** – pro délky řetězce 10, 30 a 100. Každý experiment byl proveden desetkrát a výsledky byly vyhodnoceny pomocí konvergenčních grafů a základních statistických ukazatelů (nejlepší, nejhorší, průměrná a mediánová hodnota, směrodatná odchylka).

Výsledky ukázaly, že genetický algoritmus dokáže spolehlivě nacházet optimální řešení v daném rozpočtu evaluací. Elitismus pomohl udržovat kvalitní jedince v populaci a urychlil dosažení maxima. Ruletová selekce fungovala dobře u jednodušší úlohy OneMax, zatímco pořadová selekce se ukázala jako stabilnější u LeadingOnes, kde absolutní rozdíly ve fitness nejsou tak výrazné.

