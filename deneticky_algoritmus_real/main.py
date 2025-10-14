import os
import matplotlib.pyplot as plt
import numpy as np

# ====== Konfigurace ======
RNG_SEED = 42
RUNS = 3
D = 10
EVAL_BUDGET = 10_000

# populace a GA
POP_SIZE = 200                  # zvoleno tak, aby rozumně naplnilo budget s elitismem
ELITE_FRAC = 0.10
P_CROSS = 1.0                   # single-point mezi dimenzemi
P_MUT_BIT = 1.0 / 32.0          # přibližně 1 bit na dimenzi v průměru
P_MUT_REAL = 0.1                # pravděpodobnost mutace jedné dimenze u real-GA

# real-GA mutace
GAUSS_SIGMA_FRAC = 0.05         # sigma jako 5 % šířky intervalu
# ====== /Konfigurace ======

rng = np.random.RandomState(RNG_SEED)

# ====== Benchmark funkce a jejich domény ======
def sphere(x):
    return np.sum(x * x)

def rosenbrock(x):
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2)

def schwefel(x):
    return 418.9829 * x.size - np.sum(x * np.sin(np.sqrt(np.abs(x))))

PROBLEMS = {
    "sphere":     {"fn": sphere,     "bounds": (-5.12, 5.12)},
    "rosenbrock": {"fn": rosenbrock, "bounds": (-5.0, 10.0)},
    "schwefel":   {"fn": schwefel,   "bounds": (-500.0, 500.0)},
}

# ====== Pomocné IO (grafy + statistiky) ======
def save_plot(mean_curve, std_curve, title, out_png):
    x = np.arange(1, mean_curve.size + 1)
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.figure()
    plt.plot(x, mean_curve, label="průměrný best-so-far")
    plt.fill_between(x, mean_curve - std_curve, mean_curve + std_curve, alpha=0.2, label="±1σ")
    plt.xlabel("počet evaluací")
    plt.ylabel("fitness (minimizační)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()

def compute_stats(finals):
    finals = np.asarray(finals, dtype=float)
    return {
        "best": float(np.min(finals)),
        "worst": float(np.max(finals)),
        "mean": float(np.mean(finals)),
        "median": float(np.median(finals)),
        "std": float(np.std(finals, ddof=1)) if len(finals) > 1 else 0.0
    }

def write_stats_md(problem, rows, out_md):
    os.makedirs(os.path.dirname(out_md), exist_ok=True)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"### {problem} – D={D}, budget={EVAL_BUDGET}, runs={RUNS}\n\n")
        f.write("| Varianta | best | worst | mean | median | std |\n")
        f.write("|----------|----------|-------|------|--------|-----|\n")
        for name, st in rows:
            f.write(f"| {name} | {st['best']:.6g} | {st['worst']:.6g} | {st['mean']:.6g} | {st['median']:.6g} | {st['std']:.6g} |\n")
        f.write("\n")
        headers = " | ".join(n for n,_ in rows)
        seps = " | ".join("---" for _ in rows)
        imgs = " | ".join(f"![{n}]({n}.png)" for n,_ in rows)
        f.write(f"| {headers} |\n| {seps} |\n| {imgs} |\n")

# ====== Výběr, křížení mezi dimenzemi (single-point), elitismus ======
def select_rank(fits):
    order = np.argsort(fits)  # vzestupně
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, len(fits) + 1)
    total = np.sum(ranks)
    pick = rng.randint(1, total + 1)
    s = 0
    for i, w in enumerate(ranks):
        s += int(w)
        if s >= pick:
            return i
    return len(fits) - 1

def crossover_dim_single(p1, p2):
    # p1, p2 tvaru (D,) — u bitových variant mají rozměr (D, WORD) a křížíme po dimenzích
    cut = rng.randint(1, len(p1))
    c1 = np.concatenate([p1[:cut], p2[cut:]], axis=0)
    c2 = np.concatenate([p2[:cut], p1[cut:]], axis=0)
    return c1, c2

# ====== BITOVÉ REPREZENTACE (32 b/dim) ======
WORD = 32

# --- Fixed-Point (signed two's complement, škálování 2^-16, poté klip do domény) ---
def fxp_decode(word_bits, bounds):
    low, high = bounds
    # word_bits: (32,) {0,1} -> int32
    u = 0
    for b in word_bits:
        u = (u << 1) | int(b)
    # interpretuj jako signed 32-bit
    if u & (1 << 31):
        u = u - (1 << 32)
    val = u / (1 << 16)    # Q16.16
    # mapuj/klipni do domény
    return float(np.clip(val, low, high))

# --- BCD (8 číslic po 4 bitech), lineární mapování <0..99_999_999> -> [low, high] ---
def bcd_decode(word_bits, bounds):
    low, high = bounds
    N = 0
    for i in range(8):
        nibble = 0
        base = 4 * i
        for k in range(4):
            nibble |= int(word_bits[base + k]) << (3 - k)
        digit = min(nibble, 9)  # ořízni na 0..9
        N = N * 10 + digit
    val = low + (N / 99_999_999.0) * (high - low)
    return float(val)

# --- IEEE754 (považuj 32 bitů za float32, poté tanh a škáluj do domény) ---
def ieee_decode(word_bits, bounds):
    low, high = bounds
    u = 0
    for b in word_bits:
        u = (u << 1) | int(b)
    f = np.frombuffer(np.uint32(u).tobytes(), dtype=np.float32)[0]
    if not np.isfinite(f):
        f = 0.0
    # squash do (-1,1), pak rozšiř do domény (symetrické i nesymetrické)
    span = max(abs(low), abs(high))
    val = float(np.tanh(float(f)) * span)
    return float(np.clip(val, low, high))

def bit_decode_genome(genome, bounds, decoder):
    # genome tvaru (D, 32)
    x = np.empty(D, dtype=float)
    for i in range(D):
        x[i] = decoder(genome[i], bounds)
    return x

def bit_mutate(genome, p_mut=P_MUT_BIT):
    # flip bitů v celé matici (D,32)
    mask = rng.rand(*genome.shape) < p_mut
    genome[mask] = 1 - genome[mask]

def bit_init_pop(pop_size):
    # návrat (pop_size, D, 32) v {0,1}
    return rng.randint(0, 2, size=(pop_size, D, WORD), dtype=np.uint8)

def bit_ga_run(problem_name, decoder, variant_name):
    fn = PROBLEMS[problem_name]["fn"]
    bounds = PROBLEMS[problem_name]["bounds"]

    elite_n = max(0, int(round(ELITE_FRAC * POP_SIZE)))
    pop = bit_init_pop(POP_SIZE)
    fits = np.empty(POP_SIZE, dtype=float)

    evals = 0
    best_hist = np.empty(EVAL_BUDGET, dtype=float)
    # inicializace
    for i in range(POP_SIZE):
        if evals >= EVAL_BUDGET: break
        x = bit_decode_genome(pop[i], bounds, decoder)
        val = fn(x)
        fits[i] = val
        best_hist[evals] = np.min(fits[:i+1])
        evals += 1

    while evals < EVAL_BUDGET:
        # elitismus
        if elite_n > 0:
            elite_idx = np.argsort(fits)[:elite_n]
            new_pop_parts = [pop[elite_idx].copy()]
        else:
            new_pop_parts = []

        # potomci přes single-point crossover MEZI DIMENZEMI
        while sum(p.shape[0] for p in new_pop_parts) < POP_SIZE:
            i1 = select_rank(fits)
            i2 = select_rank(fits)
            p1 = pop[i1]
            p2 = pop[i2]
            c1, c2 = crossover_dim_single(p1, p2)
            bit_mutate(c1)
            bit_mutate(c2)
            needed = POP_SIZE - sum(p.shape[0] for p in new_pop_parts)
            if needed >= 2:
                new_pop_parts.append(np.stack([c1, c2], axis=0))
            else:
                new_pop_parts.append(c1.reshape(1, D, WORD))

        pop = np.concatenate(new_pop_parts, axis=0)

        # ohodnocení
        for i in range(POP_SIZE):
            if evals >= EVAL_BUDGET: break
            x = bit_decode_genome(pop[i], bounds, decoder)
            val = fn(x)
            fits[i] = val
            best_hist[evals] = np.min(fits)
            evals += 1

        if evals < EVAL_BUDGET:
            best_hist[evals:] = np.min(fits)

    return best_hist, float(np.min(fits)), variant_name

# ====== REAL-VALUED GA ======
def real_init_pop(pop_size, bounds):
    low, high = bounds
    return rng.uniform(low, high, size=(pop_size, D))

def real_mutate_gaussian(x, bounds):
    low, high = bounds
    sigma = GAUSS_SIGMA_FRAC * (high - low)
    mask = rng.rand(D) < P_MUT_REAL
    x_new = x.copy()
    x_new[mask] = x_new[mask] + rng.normal(0.0, sigma, size=np.sum(mask))
    return np.clip(x_new, low, high)

def real_mutate_randomreset(x, bounds):
    low, high = bounds
    mask = rng.rand(D) < P_MUT_REAL
    x_new = x.copy()
    x_new[mask] = rng.uniform(low, high, size=np.sum(mask))
    return x_new

def real_ga_run(problem_name, mut_kind, variant_name):
    fn = PROBLEMS[problem_name]["fn"]
    bounds = PROBLEMS[problem_name]["bounds"]
    elite_n = max(0, int(round(ELITE_FRAC * POP_SIZE)))

    pop = real_init_pop(POP_SIZE, bounds)
    fits = np.empty(POP_SIZE, dtype=float)

    evals = 0
    best_hist = np.empty(EVAL_BUDGET, dtype=float)

    # eval init
    for i in range(POP_SIZE):
        if evals >= EVAL_BUDGET: break
        val = fn(pop[i])
        fits[i] = val
        best_hist[evals] = np.min(fits[:i+1])
        evals += 1

    mutator = real_mutate_gaussian if mut_kind == "gauss" else real_mutate_randomreset

    while evals < EVAL_BUDGET:
        if elite_n > 0:
            elite_idx = np.argsort(fits)[:elite_n]
            new_pop_parts = [pop[elite_idx].copy()]
        else:
            new_pop_parts = []

        # single-point crossover mezi dimenzemi
        while sum(p.shape[0] for p in new_pop_parts) < POP_SIZE:
            i1 = select_rank(fits)
            i2 = select_rank(fits)
            p1 = pop[i1]
            p2 = pop[i2]
            c1, c2 = crossover_dim_single(p1, p2)
            c1 = mutator(c1, bounds)
            c2 = mutator(c2, bounds)
            needed = POP_SIZE - sum(p.shape[0] for p in new_pop_parts)
            if needed >= 2:
                new_pop_parts.append(np.stack([c1, c2], axis=0))
            else:
                new_pop_parts.append(c1.reshape(1, D))

        pop = np.concatenate(new_pop_parts, axis=0)

        for i in range(POP_SIZE):
            if evals >= EVAL_BUDGET: break
            val = fn(pop[i])
            fits[i] = val
            best_hist[evals] = np.min(fits)
            evals += 1

        if evals < EVAL_BUDGET:
            best_hist[evals:] = np.min(fits)

    return best_hist, float(np.min(fits)), variant_name

# ====== Spouštěcí wrapper (porovnání všech variant) ======
VARIANTS = [
    ("IEEE754_bits", lambda prob: bit_ga_run(prob, ieee_decode, "IEEE754_bits")),
    ("FixedPoint_bits", lambda prob: bit_ga_run(prob, fxp_decode, "FixedPoint_bits")),
    ("BCD_bits", lambda prob: bit_ga_run(prob, bcd_decode, "BCD_bits")),
    ("Real_Gauss", lambda prob: real_ga_run(prob, "gauss", "Real_Gauss")),
    ("Real_RandomReset", lambda prob: real_ga_run(prob, "reset", "Real_RandomReset")),
]

def run_all():
    for problem in PROBLEMS.keys():
        out_dir = f"charts/{problem}/D{D}"
        os.makedirs(out_dir, exist_ok=True)

        rows_for_md = []
        for var_name, runner in VARIANTS:
            curves = []
            finals = []
            for _ in range(RUNS):
                best_hist, final_best, tag = runner(problem)
                curves.append(best_hist)
                finals.append(final_best)
            curves = np.vstack(curves)
            mean_curve = curves.mean(axis=0)
            std_curve = curves.std(axis=0, ddof=1) if RUNS > 1 else np.zeros_like(mean_curve)

            png_path = f"{out_dir}/{var_name}.png"
            save_plot(mean_curve, std_curve,
                      title=f"{problem} – {var_name} (D={D}, budget={EVAL_BUDGET})",
                      out_png=png_path)

            st = compute_stats(finals)
            rows_for_md.append((var_name, st))

        write_stats_md(problem, rows_for_md, f"{out_dir}/stats.md")

if __name__ == "__main__":
    run_all()
