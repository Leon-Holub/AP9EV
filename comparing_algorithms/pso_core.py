import numpy as np

class PSO:
    """Particle Swarm Optimization without boundary clipping.
    Evaluations outside bounds return +inf. History recorded by FES.
    """

    def __init__(self, func, dim, lower, upper, npop=40, max_fes=20000,
                 w_strategy="linear", w_max=0.8, w_min=0.3, w_const=0.7,
                 c1=2.0, c2=2.0, topology="global", seed=None):

        self.func = func
        self.dim = dim

        self.lower = np.full(dim, lower)
        self.upper = np.full(dim, upper)

        self.npop = npop
        self.max_fes = max_fes

        self.range = self.upper - self.lower
        self.vmax = 0.2 * self.range

        self.w_strategy = w_strategy
        self.w_max = w_max
        self.w_min = w_min
        self.w_const = w_const

        self.c1 = c1
        self.c2 = c2
        self.topology = topology

        self.rng = np.random.default_rng(seed)
        self.fes = 0

    def _current_w(self):
        if self.w_strategy == "linear":
            r = self.fes / self.max_fes
            return self.w_max - (self.w_max - self.w_min) * r
        return self.w_const

    def _evaluate(self, x):
        """Evaluate only if inside bounds, otherwise return +inf."""
        if self.fes >= self.max_fes:
            return np.inf

        self.fes += 1

        if np.any(x < self.lower) or np.any(x > self.upper):
            return np.inf

        return self.func(x)

    def _apply_vmax(self, v):
        return np.clip(v, -self.vmax, self.vmax)

    def _ring_index(self, pbest_vals, i):
        left = (i - 1) % self.npop
        right = (i + 1) % self.npop
        return min([left, i, right], key=lambda j: pbest_vals[j])

    def run(self):
        X = self.rng.uniform(self.lower, self.upper, (self.npop, self.dim))
        V = self.rng.uniform(-self.vmax, self.vmax, (self.npop, self.dim))

        pbest = X.copy()
        pbest_vals = np.array([self._evaluate(x) for x in X])

        g_idx = int(np.argmin(pbest_vals))
        gbest = pbest[g_idx].copy()
        gbest_val = pbest_vals[g_idx]

        history = [(self.fes, gbest_val)]

        while self.fes < self.max_fes:

            w = self._current_w()

            if self.topology == "ring":
                nbest = np.array([pbest[self._ring_index(pbest_vals, i)]
                                  for i in range(self.npop)])
            else:
                nbest = np.tile(gbest, (self.npop, 1))

            r1 = self.rng.random((self.npop, self.dim))
            r2 = self.rng.random((self.npop, self.dim))

            V = w * V + self.c1 * r1 * (pbest - X) + self.c2 * r2 * (nbest - X)
            V = self._apply_vmax(V)

            X = X + V  # NO boundary clipping

            for i in range(self.npop):
                if self.fes >= self.max_fes:
                    break

                fval = self._evaluate(X[i])

                if fval < pbest_vals[i]:
                    pbest_vals[i] = fval
                    pbest[i] = X[i].copy()

                    if fval < gbest_val:
                        gbest_val = fval
                        gbest = X[i].copy()

            history.append((self.fes, gbest_val))

        return gbest, gbest_val, history


# ------------------------
#  TEST FUNCTIONS
# ------------------------

def sphere(x):
    return np.sum(x**2)

def rosenbrock(x):
    return np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

def schwefel(x):
    return 418.9829 * len(x) - np.sum(x * np.sin(np.sqrt(np.abs(x))))

PROBLEMS = {
    "sphere": {"fn": sphere, "bounds": (-5.12, 5.12)},
    "rosenbrock": {"fn": rosenbrock, "bounds": (-5, 10)},
    "schwefel": {"fn": schwefel, "bounds": (-500, 500)},
}

# ------------------------
#  VARIANTS
# ------------------------
# v pso_core.py – dole úprava variant (nepovinné, ale užitečné)
def variant_linear(func, bounds, dim, max_fes, npop=40, seed=None):
    return PSO(
        func, dim, bounds[0], bounds[1],
        npop=npop, max_fes=max_fes,
        w_strategy="linear", w_max=0.8, w_min=0.3,
        c1=2.0, c2=2.0, topology="global",
        seed=seed,
    )


def variant_const_global(func, bounds, dim, max_fes, npop=40, seed=None):
    return PSO(
        func, dim, bounds[0], bounds[1],
        npop=npop, max_fes=max_fes,
        w_strategy="const", w_const=0.7,
        c1=1.49618, c2=1.49618, topology="global",
        seed=seed,
    )


def variant_const_ring(func, bounds, dim, max_fes, npop=40, seed=None):
    return PSO(
        func, dim, bounds[0], bounds[1],
        npop=npop, max_fes=max_fes,
        w_strategy="const", w_const=0.6,
        c1=1.49618, c2=1.49618, topology="ring",
        seed=seed,
    )

