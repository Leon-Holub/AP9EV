# Souhrnný report genetického algoritmu (GA)
**Datum generování:** 2025-10-14 17:41:03

## Nastavení experimentu

- RNG_SEED = `42`
- Počet běhů = `10`
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

### sphere – D=10, budget=10000, runs=10

| Varianta | best | worst | mean | median | std |
|-----------|-------|-------|------|--------|------|
| **IEEE754_bits** | **0.0000** | **0.0000** | **0.0000** | **0.0000** | **0.0000** |
| FixedPoint_bits | 192.5742 | 235.9296 | 214.5038 | 209.7309 | 15.0625 |
| BCD_bits | 0.0113 | 0.2076 | 0.0645 | 0.0530 | 0.0535 |
| Real_Gauss | 0.0024 | 0.0155 | 0.0088 | 0.0083 | 0.0039 |
| Real_RandomReset | 0.0298 | 0.2568 | 0.1383 | 0.1278 | 0.0657 |

| IEEE754_bits | FixedPoint_bits | BCD_bits | Real_Gauss | Real_RandomReset |
| --- | --- | --- | --- | --- |
| ![IEEE754_bits](charts/sphere/D10/IEEE754_bits.png) | ![FixedPoint_bits](charts/sphere/D10/FixedPoint_bits.png) | ![BCD_bits](charts/sphere/D10/BCD_bits.png) | ![Real_Gauss](charts/sphere/D10/Real_Gauss.png) | ![Real_RandomReset](charts/sphere/D10/Real_RandomReset.png) |


## ROSENBROCK

### rosenbrock – D=10, budget=10000, runs=10

| Varianta | best | worst | mean | median | std |
|-----------|-------|-------|------|--------|------|
| **IEEE754_bits** | **8.3505** | **8.8165** | **8.6578** | **8.7614** | **0.1969** |
| FixedPoint_bits | 374943.6353 | 742824.0000 | 607951.3262 | 625523.1817 | 105092.5129 |
| BCD_bits | 48.6439 | 273.9253 | 175.3783 | 168.9099 | 60.9190 |
| Real_Gauss | 9.1093 | 27.1451 | 14.0887 | 12.0019 | 5.2516 |
| Real_RandomReset | 30.6240 | 156.0426 | 91.3999 | 92.3007 | 35.3104 |

| IEEE754_bits | FixedPoint_bits | BCD_bits | Real_Gauss | Real_RandomReset |
| --- | --- | --- | --- | --- |
| ![IEEE754_bits](charts/rosenbrock/D10/IEEE754_bits.png) | ![FixedPoint_bits](charts/rosenbrock/D10/FixedPoint_bits.png) | ![BCD_bits](charts/rosenbrock/D10/BCD_bits.png) | ![Real_Gauss](charts/rosenbrock/D10/Real_Gauss.png) | ![Real_RandomReset](charts/rosenbrock/D10/Real_RandomReset.png) |


## SCHWEFEL

### schwefel – D=10, budget=10000, runs=10

| Varianta | best | worst | mean | median | std |
|-----------|-------|-------|------|--------|------|
| IEEE754_bits | 1609.5940 | 2176.7617 | 1918.7108 | 1914.4968 | 172.4852 |
| FixedPoint_bits | 1476.3828 | 1913.2094 | 1697.9429 | 1683.9743 | 138.3659 |
| **BCD_bits** | **3.6658** | **17.4658** | **10.0753** | **10.5058** | **4.7065** |
| Real_Gauss | 3.1844 | 369.9057 | 77.9084 | 6.7505 | 123.2230 |
| Real_RandomReset | 13.8739 | 113.1372 | 58.9407 | 61.6960 | 25.2869 |

| IEEE754_bits | FixedPoint_bits | BCD_bits | Real_Gauss | Real_RandomReset |
| --- | --- | --- | --- | --- |
| ![IEEE754_bits](charts/schwefel/D10/IEEE754_bits.png) | ![FixedPoint_bits](charts/schwefel/D10/FixedPoint_bits.png) | ![BCD_bits](charts/schwefel/D10/BCD_bits.png) | ![Real_Gauss](charts/schwefel/D10/Real_Gauss.png) | ![Real_RandomReset](charts/schwefel/D10/Real_RandomReset.png) |


---

## Závěr

Předpokládal jsem, že nejlépe si povede varianta s Gaussovskou mutací, protože pracuje s reálnými hodnotami a umožňuje jemné dolaďování řešení.
Výsledky mě ale překvapily – nejčastěji nejlepších výsledků dosáhla varianta IEEE754_bits, která používá bitovou reprezentaci čísel ve formátu float32.

Tato varianta se ukázala jako velmi přesná, hlavně u jednodušších funkcí (Sphere, Rosenbrock), zatímco reálné varianty měly větší rozptyl výsledků.
U složitější funkce Schwefel se nejlépe dařilo BCD reprezentaci, pravděpodobně díky větším skokům v prostoru, které pomáhají vyhnout se lokálním minimům.
