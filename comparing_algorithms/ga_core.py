# ga_core.py
import numpy as np


class GAReal:

    def __init__(
        self,
        func,
        dim,
        bounds,
        pop_size=200,
        max_evals=100_000,
        elite_frac=0.1,
        p_mut=0.1,
        sigma_frac=0.05,
        seed=None,
    ):
        self.func = func
        self.dim = dim
        self.low, self.high = bounds
        self.pop_size = pop_size
        self.max_evals = max_evals
        self.elite_frac = elite_frac
        self.p_mut = p_mut
        self.sigma_frac = sigma_frac

        self.rng = np.random.default_rng(seed)
        self.eval_count = 0

    # --- pomocné ---

    def _ensure_bounds(self, x):
        return np.clip(x, self.low, self.high)

    def _eval(self, x):
        if self.eval_count >= self.max_evals:
            # už nesmím dál hodnotit – vrátím něco hrozného
            return np.inf
        self.eval_count += 1
        return self.func(x)

    def _init_pop(self):
        return self.rng.uniform(self.low, self.high, (self.pop_size, self.dim))

    def _rank_selection(self, fitness):
        # stejné chování jako v původním kódu – rank selection :contentReference[oaicite:1]{index=1}
        ranks = np.argsort(fitness)
        probs = np.linspace(1, len(fitness), len(fitness))
        probs = probs / np.sum(probs)
        return self.rng.choice(ranks, p=probs[::-1])

    def _crossover(self, p1, p2):
        point = self.rng.integers(1, self.dim)
        c1 = np.concatenate([p1[:point], p2[point:]])
        c2 = np.concatenate([p2[:point], p1[point:]])
        return c1, c2

    def _mutate_gauss(self, x):
        sigma = self.sigma_frac * (self.high - self.low)
        for i in range(self.dim):
            if self.rng.random() < self.p_mut:
                x[i] += self.rng.normal(0.0, sigma)
        return self._ensure_bounds(x)

    # --- hlavní běh GA ---


    def run(self, sample_step=100):
        pop = self._init_pop()
        fitness = np.array([self._eval(ind) for ind in pop])
        best_fit = float(np.min(fitness))

        history = []
        history.append((self.eval_count, best_fit))

        while self.eval_count < self.max_evals:
            # GA generace...

            for i, ind in enumerate(pop):
                val = self._eval(ind)
                fitness[i] = val
                if val < best_fit:
                    best_fit = float(val)

                # ukládáme každých sample_step FES
                if self.eval_count % sample_step == 0:
                    history.append((self.eval_count, best_fit))

                if self.eval_count >= self.max_evals:
                    break

        return best_fit, history


