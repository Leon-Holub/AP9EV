# main.py
# Minimalistický binární GA pro OneMax a LeadingOnes
import os
import numpy as np
import matplotlib.pyplot as plt

# ====== Nastavení ======
RNG_SEED     = 42
RUNS         = 10
DIM_LIST     = [10, 30, 100]
POP_FACTOR   = 5.0
ELITE_FRAC   = 0.10
P_CROSS      = 1.0
P_MUT        = 0.01
PROBLEMS     = ["onemax", "leading_ones"]
SELECTIONS   = ["roulette", "rank"]
# ========================

rng = np.random.RandomState(RNG_SEED)

# --- fitness funkce ---
def fit_onemax(x): return int(x.sum())
def fit_leading_ones(x):
    zeros = np.where(x == 0)[0]
    return int(zeros[0]) if zeros.size else int(x.size)

# --- selekce ---
def select_roulette(fits, rng):
    s = fits.sum()
    if s <= 0: return rng.randint(len(fits))
    r = rng.rand() * s; c = 0.0
    for i, f in enumerate(fits):
        c += f
        if c >= r: return i
    return len(fits) - 1

def select_rank(fits, rng):
    order = np.argsort(fits)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, len(fits)+1)
    total = ranks.sum()
    r = rng.randint(1, total+1); c = 0
    for i, w in enumerate(ranks):
        c += int(w)
        if c >= r: return i
    return len(fits) - 1

# --- operátory ---
def one_point_crossover(p1, p2, rng):
    L = p1.size
    if L < 2 or rng.rand() >= P_CROSS:
        return p1.copy(), p2.copy()
    cut = rng.randint(1, L)
    return (np.concatenate([p1[:cut], p2[cut:]]),
            np.concatenate([p2[:cut], p1[cut:]]))

def mutate_bits(x, rng):
    if P_MUT > 0:
        mask = rng.rand(x.size) < P_MUT
        x[mask] = 1 - x[mask]

# --- GA běh ---
def ga_run(D, fitness_fn, selection):
    budget   = 100 * D
    pop_size = max(2, int(POP_FACTOR * D))
    elite_n  = max(0, min(pop_size, int(round(ELITE_FRAC * pop_size))))

    pop  = rng.randint(0, 2, size=(pop_size, D), dtype=np.int8)
    fits = np.zeros(pop_size, dtype=np.int32)
    best_hist = np.zeros(budget, dtype=np.int32)
    evals = 0

    sel_fun = select_roulette if selection == "roulette" else select_rank

    # počáteční populace
    for i in range(pop_size):
        if evals >= budget: break
        fits[i] = fitness_fn(pop[i]); evals += 1
    best_so_far = int(fits.max()); best_hist[:evals] = best_so_far

    while evals < budget:
        # elitismus
        new_pop = [pop[np.argsort(-fits)[:elite_n]].copy()] if elite_n > 0 else []

        while sum(b.shape[0] for b in new_pop) < pop_size:
            p1, p2 = pop[sel_fun(fits, rng)], pop[sel_fun(fits, rng)]
            c1, c2 = one_point_crossover(p1, p2, rng)
            mutate_bits(c1, rng); mutate_bits(c2, rng)
            need = pop_size - sum(b.shape[0] for b in new_pop)
            if need >= 2: new_pop.append(np.stack([c1, c2], 0))
            else: new_pop.append(c1.reshape(1, -1))
        pop = np.concatenate(new_pop, axis=0)

        for i in range(pop_size):
            if evals >= budget: break
            fits[i] = fitness_fn(pop[i]); evals += 1
            if fits[i] > best_so_far: best_so_far = int(fits[i])
            best_hist[evals-1] = best_so_far
        if evals < budget: best_hist[evals:] = best_so_far

    return best_hist, int(fits.max())

# --- utility ---
def save_plot(mean_curve, std_curve, title, problem, D, selection):
    path = f"charts/{problem}/{D}"
    os.makedirs(path, exist_ok=True)
    x = np.arange(1, mean_curve.size + 1)
    plt.figure()
    plt.plot(x, mean_curve, label="průměrný best-so-far")
    plt.fill_between(x, mean_curve-std_curve, mean_curve+std_curve, alpha=0.2, label="±1σ")
    plt.xlabel("počet evaluací"); plt.ylabel("fitness")
    plt.title(title); plt.legend(); plt.tight_layout()
    fname = f"{path}/{selection}.png"
    plt.savefig(fname, dpi=150); plt.close()
    return fname

def compute_stats(finals):
    return {
        "best":   float(np.max(finals)),
        "worst":  float(np.min(finals)),
        "mean":   float(np.mean(finals)),
        "median": float(np.median(finals)),
        "std":    float(np.std(finals, ddof=1)) if len(finals) > 1 else 0.0,
    }

def write_stats_md(problem, D, rows):
    """
    rows: list of tuples (selection_name, stats_dict)
    Uloží Markdown tabulku + obrázky: charts/[problem]/[D]/stats.md
    """
    path = f"charts/{problem}/{D}"
    os.makedirs(path, exist_ok=True)
    md_path = f"{path}/stats.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"## {problem} – D={D}\n\n")
        f.write("| Selekce | best | worst | mean | median | std |\n")
        f.write("|---------|------|-------|------|--------|-----|\n")
        for sel, st in rows:
            f.write(f"| {sel} | {st['best']:.2f} | {st['worst']:.2f} | "
                    f"{st['mean']:.2f} | {st['median']:.2f} | {st['std']:.2f} |\n")
        f.write("\n")
        for sel, _ in rows:
            f.write(f"![{sel}](./{sel}.png)\n\n")
    print(f"  -> stats uložen: {md_path}")

def print_stats_row(problem, D, selection, stats):
    print(f"[{problem} | D={D} | sel={selection}] "
          f"best={stats['best']:.0f}, worst={stats['worst']:.0f}, "
          f"mean={stats['mean']:.2f}, median={stats['median']:.2f}, std={stats['std']:.2f}")

# --- hlavní experiment ---
def run_all():
    for problem in PROBLEMS:
        fitness = fit_onemax if problem == "onemax" else fit_leading_ones
        name = "OneMax" if problem == "onemax" else "LeadingOnes"
        for D in DIM_LIST:
            rows_for_md = []
            for selection in SELECTIONS:
                runs_hist, finals = [], []
                for _ in range(RUNS):
                    hist, fin = ga_run(D, fitness, selection)
                    runs_hist.append(hist); finals.append(fin)
                runs_hist = np.stack(runs_hist, 0)
                finals = np.array(finals)

                mean_curve = runs_hist.mean(0)
                std_curve  = runs_hist.std(0)

                # graf
                title = f"{name} – D={D} – sel={selection}"
                save_plot(mean_curve, std_curve, title, problem, D, selection)

                # statistiky
                stats = compute_stats(finals)
                print_stats_row(problem, D, selection, stats)
                rows_for_md.append((selection, stats))

            # uloží tabulku a oba grafy do stats.md
            write_stats_md(problem, D, rows_for_md)

if __name__ == "__main__":
    run_all()
