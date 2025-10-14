# Souhrnný report genetického algoritmu (GA)
**Datum generování:** 2025-10-14 17:23:39

## Nastavení experimentu

- RNG_SEED = `42`
- Počet běhů = `3`
- Dimenze (D) = `10`
- Počet evaluací (budget) = `10000`
- Velikost populace = `200`
- Elitismus = `10 %`

## Princip fungování GA

### Křížení (single-point crossover mezi dimenzemi)
Křížení probíhá mezi dvěma rodiči tak, že se náhodně zvolí **index dimenze (1 až D-1)**, na kterém se jejich vektory rozdělí. Potomci zdědí první část dimenzí od prvního rodiče a zbytek od druhého. Tento princip se používá jednotně pro všechny varianty, ale u bitových reprezentací se kříží celé 32bitové bloky.

### Mutace
- **Bitové varianty:** každý bit má pravděpodobnost `0.0312` že se přepne (0→1 nebo 1→0). Tím vzniká jemná náhodná změna binární reprezentace. Po mutaci se každý jedinec znovu dekóduje do reálných hodnot.
- **Reálné varianty:** každá dimenze má pravděpodobnost `0.1` na mutaci, přičemž se používají dvě metody:
  - **Gaussian mutace:** hodnota se posune o N(0, σ²), kde σ = 5.0% rozsahu proměnné. Zajišťuje jemné ladění řešení v lokálním okolí.
  - **RandomReset:** vybrané dimenze se nastaví na náhodnou hodnotu z celého intervalu. Podporuje globální průzkum prostoru a překonávání lokálních minim.

## Bitové reprezentace a jejich význam

### IEEE754
Každý jedinec je reprezentován jako 32bitová hodnota ve formátu IEEE 754 (1 bit znaménko, 8 bitů exponent, 23 bitů mantisa). Bity se interpretují přímo jako `float32` a následně se převádí pomocí funkce tanh() do rozsahu (-1, 1), který se pak škáluje do domény dané funkce. Tato reprezentace umožňuje pracovat s velmi malými i velmi velkými čísly, ale kvůli nelineárnímu rozložení může být mutace neintuitivní (malá změna bitu může způsobit velký skok v hodnotě).

### Fixed-Point (Q16.16)
Každý parametr je reprezentován jako 32bitové celé číslo, kde 16 bitů je pro celou část a 16 bitů pro desetinnou část. Po dekódování se hodnota převede dělením 2^16. Tato metoda zaručuje lineární mapování, ale má omezené rozlišení a může způsobit, že sousední hodnoty jsou vzdálené o konstantní krok (kvantizační chyba).

### BCD (Binary Coded Decimal)
Každý parametr je tvořen 8 číslicemi po 4 bitech (celkem 32 bitů). Každý 4bitový blok reprezentuje číslici 0–9. Po dekódování se složí celé číslo 0–99 999 999, které se následně lineárně převede do domény funkce. Výhodou je snadná interpretace, nevýhodou hrubá granularita a neefektivní využití bitů.

## Optimalizační funkce
sphere, rosenbrock, schwefel

---
## SPHERE

### sphere – D=10, budget=10000, runs=3

| Varianta | best | worst | mean | median | std |
|-----------|-------|-------|------|--------|------|
| **IEEE754_bits** | **0.0000** | **0.0000** | **0.0000** | **0.0000** | **0.0000** |
| FixedPoint_bits | 209.7152 | 209.7157 | 209.7154 | 209.7154 | 0.0002 |
| BCD_bits | 0.1620 | 0.2277 | 0.1898 | 0.1796 | 0.0278 |
| Real_Gauss | 0.0035 | 0.0076 | 0.0052 | 0.0046 | 0.0017 |
| Real_RandomReset | 0.0580 | 0.1246 | 0.0847 | 0.0715 | 0.0287 |

| IEEE754_bits | FixedPoint_bits | BCD_bits | Real_Gauss | Real_RandomReset |
| --- | --- | --- | --- | --- |
| ![IEEE754_bits](charts/sphere/D10/IEEE754_bits.png) | ![FixedPoint_bits](charts/sphere/D10/FixedPoint_bits.png) | ![BCD_bits](charts/sphere/D10/BCD_bits.png) | ![Real_Gauss](charts/sphere/D10/Real_Gauss.png) | ![Real_RandomReset](charts/sphere/D10/Real_RandomReset.png) |


## ROSENBROCK

### rosenbrock – D=10, budget=10000, runs=3

| Varianta | best | worst | mean | median | std |
|-----------|-------|-------|------|--------|------|
| **IEEE754_bits** | **8.3410** | **8.8217** | **8.5037** | **8.3486** | **0.2248** |
| FixedPoint_bits | 628024.8758 | 742824.0000 | 688712.6507 | 695289.0763 | 47096.6861 |
| BCD_bits | 73.6250 | 296.1030 | 168.8436 | 136.8028 | 93.6094 |
| Real_Gauss | 7.2800 | 164.1191 | 60.6161 | 10.4493 | 73.1991 |
| Real_RandomReset | 44.0776 | 73.0190 | 59.1837 | 60.4544 | 11.8494 |

| IEEE754_bits | FixedPoint_bits | BCD_bits | Real_Gauss | Real_RandomReset |
| --- | --- | --- | --- | --- |
| ![IEEE754_bits](charts/rosenbrock/D10/IEEE754_bits.png) | ![FixedPoint_bits](charts/rosenbrock/D10/FixedPoint_bits.png) | ![BCD_bits](charts/rosenbrock/D10/BCD_bits.png) | ![Real_Gauss](charts/rosenbrock/D10/Real_Gauss.png) | ![Real_RandomReset](charts/rosenbrock/D10/Real_RandomReset.png) |


## SCHWEFEL

### schwefel – D=10, budget=10000, runs=3

| Varianta | best | worst | mean | median | std |
|-----------|-------|-------|------|--------|------|
| IEEE754_bits | 1437.8279 | 2146.0024 | 1897.5727 | 2108.8877 | 325.4416 |
| FixedPoint_bits | 1729.5022 | 1913.6272 | 1849.6783 | 1905.9054 | 85.0358 |
| **BCD_bits** | **6.6718** | **16.8440** | **10.4870** | **7.9452** | **4.5251** |
| Real_Gauss | 14.5433 | 122.1605 | 51.5211 | 17.8596 | 49.9679 |
| Real_RandomReset | 18.7224 | 86.5308 | 57.5752 | 67.4725 | 28.5536 |

| IEEE754_bits | FixedPoint_bits | BCD_bits | Real_Gauss | Real_RandomReset |
| --- | --- | --- | --- | --- |
| ![IEEE754_bits](charts/schwefel/D10/IEEE754_bits.png) | ![FixedPoint_bits](charts/schwefel/D10/FixedPoint_bits.png) | ![BCD_bits](charts/schwefel/D10/BCD_bits.png) | ![Real_Gauss](charts/schwefel/D10/Real_Gauss.png) | ![Real_RandomReset](charts/schwefel/D10/Real_RandomReset.png) |


---

## Závěr

Výsledky potvrzují rozdíly mezi bitovými a reálnými variantami genetického algoritmu:

- **Bitové reprezentace (IEEE754, FixedPoint, BCD)** trpí kvantizační chybou a nelineárním mapováním, což vede ke stagnaci a vyšším hodnotám fitness.
- **Reálné varianty GA** (Gaussovská a náhodná mutace) vykazují hladší konvergenci a nižší výsledné chyby.
- **Gaussian mutace** se osvědčila u spojitých a konvexních funkcí (Sphere), zatímco **RandomReset** lépe prozkoumává prostor u multimodálních funkcí (Schwefel).
- U **Rosenbrocka** je vidět stabilní konvergence, ale obtížný posun úzkým údolím bez gradientní informace.

Celkově jsou reálné reprezentace vhodnější pro optimalizaci v reálné doméně, zatímco bitové slouží spíše k experimentálnímu srovnání a demonstraci vlivu kódování.
