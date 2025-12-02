import numpy as np


class GAReal:
    """Genetic algorithm for continuous (real-valued) optimization.

    Args:
        func: Objective function to minimize. Accepts a 1D numpy array and returns a scalar.
        dim: Dimensionality of the search space.
        bounds: Tuple (low, high) specifying variable bounds (scalars or arrays).
        pop_size: Population size.
        max_evals: Maximum number of function evaluations.
        elite_frac: Fraction of population preserved as elite (not used in current implementation).
        p_mut: Per-variable mutation probability.
        sigma_frac: Fraction of the search range used as Gaussian mutation sigma.
        seed: RNG seed or None.
    """

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

    def _ensure_bounds(self, x):
        """Clip a solution vector to the provided bounds and return the clipped array."""
        return np.clip(x, self.low, self.high)

    def _eval(self, x):
        """Evaluate the objective function if evaluation budget remains.

        Returns +inf when the evaluation budget is exhausted to signal an invalid/very bad solution.
        """
        if self.eval_count >= self.max_evals:
            return np.inf
        self.eval_count += 1
        return self.func(x)

    def _init_pop(self):
        """Initialize the population uniformly within the bounds.

        Returns an array of shape (pop_size, dim).
        """
        return self.rng.uniform(self.low, self.high, (self.pop_size, self.dim))

    def _rank_selection(self, fitness):
        """Select a single individual index using rank-based probabilities.

        The selection probabilities favor better-ranked (lower fitness) individuals.
        """
        ranks = np.argsort(fitness)
        probs = np.linspace(1, len(fitness), len(fitness))
        probs = probs / np.sum(probs)
        return self.rng.choice(ranks, p=probs[::-1])

    def _crossover(self, p1, p2):
        """Perform one-point crossover between two parents and return two offspring."""
        point = self.rng.integers(1, self.dim)
        c1 = np.concatenate([p1[:point], p2[point:]])
        c2 = np.concatenate([p2[:point], p1[point:]])
        return c1, c2

    def _mutate_gauss(self, x):
        """Apply per-variable Gaussian mutation to a solution and ensure bounds.

        Each variable is mutated with probability `p_mut` using a Gaussian with
        standard deviation `sigma_frac * (high - low)`.
        """
        sigma = self.sigma_frac * (self.high - self.low)
        for i in range(self.dim):
            if self.rng.random() < self.p_mut:
                x[i] += self.rng.normal(0.0, sigma)
        return self._ensure_bounds(x)

    def run(self, sample_step=100):
        """Run the genetic algorithm until the evaluation budget is exhausted.

        Args:
            sample_step: Interval (in function evaluations) at which to record progress.

        Returns:
            A tuple (best_fit, history) where `best_fit` is the best objective value found
            and `history` is a list of (eval_count, best_fit) samples.
        """
        pop = self._init_pop()
        fitness = np.array([self._eval(ind) for ind in pop])
        best_fit = float(np.min(fitness))

        history = []
        history.append((self.eval_count, best_fit))

        while self.eval_count < self.max_evals:
            for i, ind in enumerate(pop):
                val = self._eval(ind)
                fitness[i] = val
                if val < best_fit:
                    best_fit = float(val)

                if self.eval_count % sample_step == 0:
                    history.append((self.eval_count, best_fit))

                if self.eval_count >= self.max_evals:
                    break

        return best_fit, history

