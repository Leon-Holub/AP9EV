#Porovnání evolučních algoritmů 

## Zadání


Vybrané algoritmy pro porovnání:

- **GA** – real-valued encoding  
- **DE** – rand/1/bin, best/1/bin, jDE  
- **PSO** – linear inertia, const-global, const-ring  

Testované funkce jsou automaticky detekované podle vygenerovaných tabulek (včetně *sphere*, která sloužila jako rychlý benchmark).

Každý algoritmus optimalizuje každou funkci **11×**.

Limit počtu vyhodnocení:

- **100 000** pro dimenzi **D=10**  
- **200 000** pro dimenzi **D=20**

Pro každou kombinaci se ukládá:

- Průměr  
- Směrodatná odchylka  
- Medián  
- Minimum  
- Maximum  

Dále jsou generovány grafy konvergence:
- 1 graf pro každou kombinaci funkce × dimenze = 2 grafy na funkci.


# Výsledky podle funkcí


# Funkce: **rastrigin**


## Výsledky – D=10


| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |
|-----------|------|----------|--------|-----|------|----------------|
| GA_real_gauss | 1.057078e+02 | 8.857129e+00 | 1.033402e+02 | 9.422563e+01 | 1.216259e+02 | 0.78 |
| DE_rand1bin | 2.374150e+00 | 3.496948e+00 | 6.408430e-02 | 0.000000e+00 | 1.124015e+01 | 4.89 |
| DE_best1bin | 7.597864e+00 | 3.125457e+00 | 6.964708e+00 | 3.979836e+00 | 1.492435e+01 | 4.95 |
| **jDE_rand1bin** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **5.16** |
| PSO_linear_global | 1.356762e+00 | 6.395839e-01 | 9.949591e-01 | 9.949591e-01 | 2.984877e+00 | 1.60 |
| PSO_const_global | 8.411922e+00 | 3.533371e+00 | 7.959667e+00 | 1.989918e+00 | 1.293446e+01 | 1.58 |
| PSO_const_ring | 5.607950e+00 | 2.295383e+00 | 5.969754e+00 | 1.989918e+00 | 9.949586e+00 | 1.74 |


### Konvergence – D=10

![D10_rastrigin_convergence.png](charts\D10_rastrigin_convergence.png)



## Výsledky – D=20


| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |
|-----------|------|----------|--------|-----|------|----------------|
| GA_real_gauss | 2.498751e+02 | 1.161407e+01 | 2.509593e+02 | 2.301923e+02 | 2.709430e+02 | 1.96 |
| DE_rand1bin | 3.972516e+01 | 1.400291e+01 | 3.830320e+01 | 1.226515e+01 | 6.071060e+01 | 10.99 |
| DE_best1bin | 3.862242e+01 | 8.866911e+00 | 3.681335e+01 | 2.686385e+01 | 5.571755e+01 | 10.45 |
| **jDE_rand1bin** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **10.93** |
| PSO_linear_global | 1.121590e+01 | 3.032461e+00 | 9.949591e+00 | 7.959672e+00 | 1.790925e+01 | 3.42 |
| PSO_const_global | 2.650206e+01 | 9.741831e+00 | 2.487396e+01 | 1.591934e+01 | 5.173778e+01 | 3.38 |
| PSO_const_ring | 2.560576e+01 | 5.917850e+00 | 2.885377e+01 | 1.591934e+01 | 3.482352e+01 | 3.74 |


### Konvergence – D=20

![D20_rastrigin_convergence.png](charts\D20_rastrigin_convergence.png)



# Funkce: **rosenbrock**


## Výsledky – D=10


| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |
|-----------|------|----------|--------|-----|------|----------------|
| GA_real_gauss | 6.569429e+04 | 2.405901e+04 | 6.642491e+04 | 1.844231e+04 | 1.078089e+05 | 0.90 |
| DE_rand1bin | 3.164309e+00 | 6.007211e-01 | 3.113201e+00 | 2.060451e+00 | 4.247867e+00 | 5.40 |
| DE_best1bin | 7.248326e-01 | 1.537602e+00 | 0.000000e+00 | 0.000000e+00 | 3.986579e+00 | 5.55 |
| **jDE_rand1bin** | **1.157158e-11** | **1.904969e-11** | **6.959651e-13** | **5.058041e-14** | **6.312581e-11** | **5.82** |
| PSO_linear_global | 1.750138e+00 | 1.167165e+00 | 2.414186e+00 | 6.857889e-03 | 3.051880e+00 | 1.88 |
| PSO_const_global | 9.689924e-01 | 1.974685e+00 | 2.436440e-02 | 6.724984e-03 | 6.100423e+00 | 1.85 |
| PSO_const_ring | 2.069372e-01 | 1.677588e-01 | 1.518612e-01 | 2.595847e-02 | 5.731552e-01 | 2.10 |


### Konvergence – D=10

![D10_rosenbrock_convergence.png](charts\D10_rosenbrock_convergence.png)



## Výsledky – D=20


| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |
|-----------|------|----------|--------|-----|------|----------------|
| GA_real_gauss | 4.231092e+05 | 1.044937e+05 | 4.340743e+05 | 2.415322e+05 | 6.294057e+05 | 1.92 |
| DE_rand1bin | 8.813903e+00 | 9.375299e-01 | 8.552672e+00 | 7.331771e+00 | 1.011117e+01 | 19.00 |
| DE_best1bin | 1.087261e+00 | 1.775490e+00 | 3.302468e-27 | 3.298794e-28 | 3.986624e+00 | 12.98 |
| **jDE_rand1bin** | **1.510401e-07** | **1.468750e-07** | **9.233111e-08** | **1.465779e-09** | **4.670243e-07** | **10.99** |
| PSO_linear_global | 9.446830e+00 | 5.279566e+00 | 1.224959e+01 | 1.314095e-04 | 1.601426e+01 | 3.52 |
| PSO_const_global | 3.420770e+00 | 2.491069e+00 | 3.761642e+00 | 8.598450e-05 | 7.255170e+00 | 3.56 |
| PSO_const_ring | 1.461744e+00 | 2.163159e+00 | 6.616686e-02 | 2.696229e-04 | 6.242796e+00 | 3.96 |


### Konvergence – D=20

![D20_rosenbrock_convergence.png](charts\D20_rosenbrock_convergence.png)



# Funkce: **schwefel**


## Výsledky – D=10


| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |
|-----------|------|----------|--------|-----|------|----------------|
| GA_real_gauss | 2.466808e+03 | 2.866338e+02 | 2.543444e+03 | 1.872678e+03 | 2.930357e+03 | 0.60 |
| DE_rand1bin | 9.247558e+01 | 9.823936e+01 | 6.143134e+01 | 1.272757e-04 | 2.368768e+02 | 5.15 |
| DE_best1bin | 8.003607e+02 | 1.594651e+02 | 8.108485e+02 | 5.922247e+02 | 1.070496e+03 | 5.25 |
| **jDE_rand1bin** | **1.272757e-04** | **0.000000e+00** | **1.272757e-04** | **1.272757e-04** | **1.272757e-04** | **5.49** |
| PSO_linear_global | 7.088359e+02 | 1.516130e+02 | 7.106301e+02 | 4.737535e+02 | 9.475068e+02 | 1.43 |
| PSO_const_global | 1.069562e+03 | 2.720875e+02 | 1.006734e+03 | 7.501232e+02 | 1.717433e+03 | 1.48 |
| PSO_const_ring | 1.062371e+03 | 2.415981e+02 | 1.046208e+03 | 6.908931e+02 | 1.559487e+03 | 1.62 |


### Konvergence – D=10

![D10_schwefel_convergence.png](charts\D10_schwefel_convergence.png)



## Výsledky – D=20


| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |
|-----------|------|----------|--------|-----|------|----------------|
| GA_real_gauss | 6.065535e+03 | 2.137805e+02 | 6.121866e+03 | 5.715711e+03 | 6.440789e+03 | 1.24 |
| DE_rand1bin | 4.537535e+02 | 2.532643e+02 | 3.554542e+02 | 1.365475e+02 | 1.088011e+03 | 9.76 |
| DE_best1bin | 2.228701e+03 | 5.407681e+02 | 2.250369e+03 | 1.169198e+03 | 3.102355e+03 | 10.56 |
| **jDE_rand1bin** | **1.076738e+01** | **3.404863e+01** | **2.545513e-04** | **2.545513e-04** | **1.184386e+02** | **10.74** |
| PSO_linear_global | 1.564830e+03 | 2.353948e+02 | 1.618663e+03 | 1.144910e+03 | 1.895033e+03 | 2.92 |
| PSO_const_global | 3.246419e+03 | 6.223521e+02 | 3.316378e+03 | 2.171435e+03 | 4.737784e+03 | 3.03 |
| PSO_const_ring | 2.979247e+03 | 4.393725e+02 | 2.982376e+03 | 2.250369e+03 | 3.612598e+03 | 3.30 |


### Konvergence – D=20

![D20_schwefel_convergence.png](charts\D20_schwefel_convergence.png)



# Funkce: **sphere**


## Výsledky – D=10


| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |
|-----------|------|----------|--------|-----|------|----------------|
| GA_real_gauss | 2.863385e+01 | 8.128783e+00 | 2.943724e+01 | 1.580964e+01 | 4.553825e+01 | 0.42 |
| DE_rand1bin | 1.234506e-86 | 2.480731e-86 | 3.227286e-87 | 1.490002e-88 | 8.890336e-86 | 4.66 |
| **DE_best1bin** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **0.000000e+00** | **4.71** |
| jDE_rand1bin | 1.375771e-85 | 3.184561e-85 | 2.106442e-86 | 2.125314e-87 | 1.132340e-84 | 4.93 |
| PSO_linear_global | 5.953951e-112 | 1.706997e-111 | 8.381211e-114 | 1.398735e-117 | 5.980100e-111 | 1.23 |
| PSO_const_global | 7.408389e-154 | 9.358111e-154 | 4.234200e-154 | 2.097300e-156 | 2.892629e-153 | 1.24 |
| PSO_const_ring | 2.053333e-113 | 3.217997e-113 | 7.011784e-114 | 2.332608e-115 | 1.098247e-112 | 1.37 |


### Konvergence – D=10

![D10_sphere_convergence.png](charts\D10_sphere_convergence.png)



## Výsledky – D=20


| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |
|-----------|------|----------|--------|-----|------|----------------|
| GA_real_gauss | 8.605644e+01 | 7.946211e+00 | 8.511560e+01 | 7.367965e+01 | 9.960026e+01 | 0.89 |
| DE_rand1bin | 7.083631e-82 | 1.238596e-81 | 3.087075e-82 | 8.013151e-84 | 4.467321e-81 | 9.81 |
| **DE_best1bin** | **4.940656e-324** | **0.000000e+00** | **4.940656e-324** | **0.000000e+00** | **2.964394e-323** | **10.04** |
| jDE_rand1bin | 6.823175e-90 | 8.006967e-90 | 3.250958e-90 | 1.113520e-90 | 2.480140e-89 | 10.44 |
| PSO_linear_global | 1.545386e-100 | 2.907994e-100 | 1.293550e-101 | 1.957902e-105 | 1.008759e-99 | 2.68 |
| PSO_const_global | 3.891706e-183 | 0.000000e+00 | 1.287637e-184 | 1.565090e-188 | 2.727124e-182 | 2.64 |
| PSO_const_ring | 1.626521e-120 | 2.250964e-120 | 4.900050e-121 | 1.031664e-122 | 6.762544e-120 | 2.94 |


### Konvergence – D=20

![D20_sphere_convergence.png](charts\D20_sphere_convergence.png)

