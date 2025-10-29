from de_core import DifferentialEvolution
import numpy as np
import math

# ---------- Testovací funkce ----------
def sphere(x):
    return np.sum(x * x)

def rastrigin(x):
    return 10 * len(x) + np.sum(x * x - 10 * np.cos(2 * math.pi * x))


if __name__ == "__main__":
    dim = 10
    bounds = (-5.12, 5.12)
    max_evals = 20000
    pop = 40

    # 1) DE/rand/1/bin
    de_rand = DifferentialEvolution(
        func=sphere, dim=dim, bounds=bounds,
        pop_size=pop, max_evals=max_evals,
        strategy="rand1bin", F=0.5, CR=0.8
    )
    best, best_fit, log = de_rand.run()
    print(f"[Sphere] DE/rand/1/bin: best_fit={best_fit:.3e}")
    de_rand.plot_convergence("DE/rand/1/bin", "charts/sphere_rand1bin.png")

    # 2) DE/best/1/bin
    de_best = DifferentialEvolution(
        func=sphere, dim=dim, bounds=bounds,
        pop_size=pop, max_evals=max_evals,
        strategy="best1bin", F=0.5, CR=0.8
    )
    best, best_fit, log = de_best.run()
    print(f"[Sphere] DE/best/1/bin: best_fit={best_fit:.3e}")
    de_best.plot_convergence("DE/best/1/bin", "charts/sphere_best1bin.png")

    # 3) jDE (rand/1)
    de_jde = DifferentialEvolution(
        func=sphere, dim=dim, bounds=bounds,
        pop_size=pop, max_evals=max_evals,
        strategy="rand1bin", F=0.5, CR=0.9,
        jde=True, tau1=0.1, tau2=0.1
    )
    best, best_fit, log = de_jde.run()
    print(f"[Sphere] jDE (rand/1): best_fit={best_fit:.3e}")
    de_jde.plot_convergence("jDE (rand/1)", "charts/sphere_jde.png")
