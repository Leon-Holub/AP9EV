import numpy as np
import matplotlib.pyplot as plt
import os


class DifferentialEvolution:
    def __init__(self, func, dim, bounds, pop_size=30, max_evals=10000,
                 strategy="rand1bin", F=0.5, CR=0.8,
                 jde=False, tau1=0.1, tau2=0.1, seed=42):

        self.func = func
        self.dim = dim
        self.lower, self.upper = bounds
        self.pop_size = pop_size
        self.max_evals = max_evals
        self.strategy = strategy
        self.F = F
        self.CR = CR
        self.jde = jde
        self.tau1 = tau1
        self.tau2 = tau2

        self.rng = np.random.default_rng(seed)
        self.eval_count = 0
        self.log = []  # (evals, best_fitness)

    def initialize(self):
        pop = self.rng.uniform(self.lower, self.upper, (self.pop_size, self.dim))
        fits = np.array([self.evaluate(ind) for ind in pop])
        return pop, fits

    def evaluate(self, individual):
        self.eval_count += 1
        return self.func(individual)

    def ensure_bounds(self, vec):
        return np.clip(vec, self.lower, self.upper)

    def mutate(self, pop, best, i, Fi):
        idxs = [idx for idx in range(self.pop_size) if idx != i]
        r1, r2, r3 = self.rng.choice(idxs, 3, replace=False)

        if self.strategy == "rand1bin":
            v = pop[r1] + Fi * (pop[r2] - pop[r3])
        elif self.strategy == "best1bin":
            v = best + Fi * (pop[r1] - pop[r2])
        else:
            raise ValueError("Neznámá strategie DE")
        return self.ensure_bounds(v)

    def crossover(self, xi, vi, CRi):
        ui = xi.copy()
        jrand = self.rng.integers(0, self.dim)
        mask = self.rng.random(self.dim) < CRi
        mask[jrand] = True
        ui[mask] = vi[mask]
        return self.ensure_bounds(ui)


    def run(self):
        pop, fits = self.initialize()
        best_idx = np.argmin(fits)
        best = pop[best_idx].copy()
        best_fit = fits[best_idx]

        if self.jde:
            F_i = np.full(self.pop_size, self.F)
            CR_i = np.full(self.pop_size, self.CR)

        self.log.append((self.eval_count, best_fit))

        while self.eval_count < self.max_evals:
            new_pop = pop.copy()
            new_fits = fits.copy()

            for i in range(self.pop_size):
                if self.jde:
                    if self.rng.random() < self.tau1:
                        F_i[i] = 0.1 + 0.8 * self.rng.random()
                    if self.rng.random() < self.tau2:
                        CR_i[i] = self.rng.random()
                    Fi, CRi = F_i[i], CR_i[i]
                else:
                    Fi, CRi = self.F, self.CR

                vi = self.mutate(pop, best, i, Fi)
                ui = self.crossover(pop[i], vi, CRi)
                fu = self.evaluate(ui)

                if fu <= fits[i]:
                    new_pop[i] = ui
                    new_fits[i] = fu
                    if fu < best_fit:
                        best_fit = fu
                        best = ui.copy()

                self.log.append((self.eval_count, best_fit))
                if self.eval_count >= self.max_evals:
                    break

            pop, fits = new_pop, new_fits

        return best, best_fit, np.array(self.log)

    def plot_convergence(self, label, out_path=None):
        log = np.array(self.log)
        plt.figure()
        plt.plot(log[:, 0], log[:, 1], label=label)
        plt.yscale("log")
        plt.xlabel("Počet evaluací")
        plt.ylabel("Nejlepší fitness")
        plt.title(f"Konvergence – {label}")
        plt.legend()
        plt.tight_layout()

        if out_path:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            plt.savefig(out_path, dpi=150)
        plt.show()

    @staticmethod
    def plot_comparison(results, title, out_path=None):
        """
        Porovná konvergenci více variant DE v jednom grafu.
        results: list of (log, label)
        """
        plt.figure()
        for log, label in results:
            arr = np.array(log)
            plt.plot(arr[:, 0], arr[:, 1], label=label)
        plt.yscale("log")
        plt.xlabel("Počet evaluací")
        plt.ylabel("Nejlepší fitness")
        plt.title(title)
        plt.legend()
        plt.tight_layout()

        if out_path:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            plt.savefig(out_path, dpi=150)
        plt.show()
