import os
import numpy as np
import matplotlib.pyplot as plt

# Nastavení
RNG_SEED = 42
np.random.seed(RNG_SEED)

RUNS = 3
D = 10
EVAL_BUDGET = 10_000
POP_SIZE = 200
ELITE_FRAC = 0.1
P_MUT_BIT = 1 / 32
P_MUT_REAL = 0.1
GAUSS_SIGMA_FRAC = 0.05
WORD = 32


# Testovací funkce
def sphere(x):
    return np.sum(x ** 2)


def rosenbrock(x):
    return np.sum(100 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2)


def schwefel(x):
    return 418.9829 * len(x) - np.sum(x * np.sin(np.sqrt(np.abs(x))))


PROBLEMS = {
    "sphere": {"fn": sphere, "bounds": (-5.12, 5.12)},
    "rosenbrock": {"fn": rosenbrock, "bounds": (-5, 10)},
    "schwefel": {"fn": schwefel, "bounds": (-500, 500)},
}


# Pomocné funkce
def save_plot(mean_curve, std_curve, title, path):
    x = np.arange(1, len(mean_curve) + 1)
    plt.figure()
    plt.plot(x, mean_curve, label="průměrný best-so-far")
    plt.fill_between(x, mean_curve - std_curve, mean_curve + std_curve, alpha=0.2, label="±1σ")
    plt.xlabel("počet evaluací")
    plt.ylabel("fitness (minimizační)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path, dpi=150)
    plt.close()


def save_stats_md(problem, results, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"### {problem} – D={D}, budget={EVAL_BUDGET}, runs={RUNS}\n\n")
        f.write("| Varianta | best | worst | mean | median | std |\n")
        f.write("|-----------|-------|-------|------|--------|------|\n")
        best_idx = np.argmin([v[1][2] for v in results])
        for i, (name, stats) in enumerate(results):
            b, w, m, med, s = stats
            row = f"| {name} | {b:.4f} | {w:.4f} | {m:.4f} | {med:.4f} | {s:.4f} |"
            if i == best_idx:
                row = f"| **{name}** | **{b:.4f}** | **{w:.4f}** | **{m:.4f}** | **{med:.4f}** | **{s:.4f}** |"
            f.write(row + "\n")
        f.write("\n")
        f.write("| " + " | ".join(v[0] for v in results) + " |\n")
        f.write("| " + " | ".join("---" for _ in results) + " |\n")
        f.write("| " + " | ".join(f"![{v[0]}]({v[0]}.png)" for v in results) + " |\n")


# GA operátory
def rank_selection(fitness):
    """Vybere index jedince podle hodnocení (menší = lepší)."""
    ranks = np.argsort(fitness)
    probs = np.linspace(1, len(fitness), len(fitness))
    probs = probs / np.sum(probs)
    return np.random.choice(ranks, p=probs[::-1])


def crossover(p1, p2):
    """Single-point crossover mezi dimenzemi."""
    point = np.random.randint(1, len(p1))
    return np.concatenate([p1[:point], p2[point:]]), np.concatenate([p2[:point], p1[point:]])


# Bitové reprezentace
def bit_init():
    return np.random.randint(0, 2, (POP_SIZE, D, WORD), dtype=np.uint8)


def bit_mutate(ind):
    mask = np.random.rand(D, WORD) < P_MUT_BIT
    ind[mask] = 1 - ind[mask]


def ieee_decode(bits, bounds):
    low, high = bounds
    val = np.frombuffer(np.uint32(int("".join(map(str, bits)), 2)).tobytes(), dtype=np.float32)[0]
    if not np.isfinite(val): val = 0.0
    span = max(abs(low), abs(high))
    return np.clip(np.tanh(val) * span, low, high)


def fxp_decode(bits, bounds):
    low, high = bounds
    num = int("".join(map(str, bits)), 2)
    if num & (1 << 31): num -= (1 << 32)
    val = num / (1 << 16)
    return np.clip(val, low, high)


def bcd_decode(bits, bounds):
    low, high = bounds
    N = 0
    for i in range(8):
        nib = bits[i * 4:(i + 1) * 4]
        digit = min(int("".join(map(str, nib)), 2), 9)
        N = N * 10 + digit
    return low + (N / 99_999_999.0) * (high - low)


def bit_to_real(bits, bounds, decode_fn):
    return np.array([decode_fn(bits[i], bounds) for i in range(D)])


# Reálné varianty
def real_init(bounds):
    low, high = bounds
    return np.random.uniform(low, high, (POP_SIZE, D))


def mutate_gauss(x, bounds):
    low, high = bounds
    sigma = GAUSS_SIGMA_FRAC * (high - low)
    for i in range(D):
        if np.random.rand() < P_MUT_REAL:
            x[i] += np.random.normal(0, sigma)
    return np.clip(x, low, high)


def mutate_random(x, bounds):
    low, high = bounds
    for i in range(D):
        if np.random.rand() < P_MUT_REAL:
            x[i] = np.random.uniform(low, high)
    return x


# Hlavní smyčka GA
def run_ga(problem, decode_fn=None, real_mut=None, mode="bit"):
    fn = PROBLEMS[problem]["fn"]
    bounds = PROBLEMS[problem]["bounds"]

    pop = bit_init() if mode == "bit" else real_init(bounds)
    evals = 0
    best_history = np.zeros(EVAL_BUDGET, dtype=float)
    best_so_far = np.inf

    while evals < EVAL_BUDGET:
        fitness = np.zeros(len(pop), dtype=float)
        for i, ind in enumerate(pop):
            x = bit_to_real(ind, bounds, decode_fn) if mode == "bit" else ind
            val = fn(x)
            fitness[i] = val

            if val < best_so_far:
                best_so_far = val
            best_history[evals] = best_so_far

            evals += 1
            if evals >= EVAL_BUDGET:
                break

        if evals >= EVAL_BUDGET:
            break

        elite_count = int(ELITE_FRAC * POP_SIZE)
        elite_idx = np.argsort(fitness)[:elite_count]
        new_pop = [pop[i].copy() for i in elite_idx]

        while len(new_pop) < POP_SIZE:
            p1 = pop[rank_selection(fitness)]
            p2 = pop[rank_selection(fitness)]
            c1, c2 = crossover(p1, p2)
            if mode == "bit":
                bit_mutate(c1);
                bit_mutate(c2)
            else:
                c1 = real_mut(c1, bounds);
                c2 = real_mut(c2, bounds)
            new_pop += [c1, c2]

        pop = np.array(new_pop[:POP_SIZE])

    return best_history


# Varianty
VARIANTS = [
    ("IEEE754_bits", lambda prob: run_ga(prob, ieee_decode, mode="bit")),
    ("FixedPoint_bits", lambda prob: run_ga(prob, fxp_decode, mode="bit")),
    ("BCD_bits", lambda prob: run_ga(prob, bcd_decode, mode="bit")),
    ("Real_Gauss", lambda prob: run_ga(prob, real_mut=mutate_gauss, mode="real")),
    ("Real_RandomReset", lambda prob: run_ga(prob, real_mut=mutate_random, mode="real")),
]


def run_all():
    for prob in PROBLEMS:
        print(f"{prob} (D={D}, budget={EVAL_BUDGET})\n")
        out_dir = f"charts/{prob}/D{D}"
        os.makedirs(out_dir, exist_ok=True)
        results = []
        for name, func in VARIANTS:
            print(f"\nVarianta: {name} - {prob}")
            print(f"====================== \n")
            runs = []
            for run in range(RUNS):
                print(f"Spuštění {run + 1}/{RUNS}...")
                hist = func(prob)
                runs.append(hist)
                print(f"hotovo, finální fitness = {hist[-1]:.4f}")
            runs = np.vstack(runs)
            mean_curve = runs.mean(axis=0)
            std_curve = runs.std(axis=0)
            finals = [r[-1] for r in runs]
            stats = (np.min(finals), np.max(finals), np.mean(finals), np.median(finals), np.std(finals))
            save_plot(mean_curve, std_curve, f"{prob} – {name} (D={D}, budget={EVAL_BUDGET})", f"{out_dir}/{name}.png")
            results.append((name, stats))
        save_stats_md(prob, results, f"{out_dir}/stats.md")
        print(f"Výsledky pro {prob} uloženy do {out_dir}/stats.md \n")


if __name__ == "__main__":
    run_all()
