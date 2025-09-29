# param_eval.py
import os
import numpy as np
from ga_core import (
    ga_run, fit_onemax, fit_leading_ones, set_hyperparams, compute_stats
)

def _score(stats, success_rate, med_evals):
    # menší je lepší (lexikograficky)
    return (
        -success_rate,
        -stats["mean"],
        -stats["median"],
        stats["std"],
        (med_evals if med_evals is not None else 1e12),
    )

def _eval_one(problem, D, selection, pop_factor, elite_frac, p_crossover, p_mut, runs):
    fitness = fit_onemax if problem == "onemax" else fit_leading_ones
    target = D
    # dočasně nastav GA hyperparametry
    set_hyperparams(pop_factor, elite_frac, p_crossover, p_mut)
    finals, hit = [], []
    for _ in range(runs):
        hist, fin = ga_run(D, fitness, selection)
        finals.append(fin)
        if fin >= target and np.any(hist >= target):
            hit.append(int(np.argmax(hist >= target)) + 1)
    finals = np.array(finals, dtype=float)
    stats = compute_stats(finals)
    sr = float(np.mean(finals >= target))
    med = float(np.median(hit)) if hit else None
    return stats, sr, med

def evaluate_param_settings_benchmark(problem, D, settings, runs, out_path="eval_stats.md"):
    """
    Otestuje zadaná nastavení jen pro konkrétní problem ('onemax' nebo 'leading_ones') a D (např. 50).
    Uloží Markdown tabulku s porovnáním do souboru `out_path` (výchozí: eval_stats.md).

    settings: list(dict(
        name, selection, pop_factor, elite_frac, p_crossover, p_mut
    ))
    - p_mut může být číslo nebo řetězec '1/D'
    """
    rows = []
    for s in settings:
        pmut = (1.0 / D) if (isinstance(s["p_mut"], str) and s["p_mut"].lower() == "1/d") else float(s["p_mut"])
        stats, sr, med = _eval_one(
            problem, D,
            s["selection"], s["pop_factor"], s["elite_frac"], s["p_crossover"], pmut,
            runs
        )
        rows.append({
            **s, "p_mut": (s["p_mut"] if isinstance(s["p_mut"], str) else float(s["p_mut"])),
            "stats": stats, "sr": sr, "med_evals": med, "score": _score(stats, sr, med)
        })

    rows.sort(key=lambda r: r["score"])   # nejlepší první
    best = rows[0]

    # Markdown tabulka + doporučení
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"## Benchmark parametrů – {problem} – D={D}\n\n")
        f.write("Řazeno dle: success rate, mean, median, std, medián evaluací do optima.\n\n")
        f.write("| name | selection | pop_factor | elite_frac | p_crossover | p_mut | best | worst | mean | median | std | success_rate | median_evals_to_opt |\n")
        f.write("|------|-----------|------------|------------|-------------|------|------|-------|------|--------|-----|--------------|---------------------|\n")
        for r in rows:
            st = r["stats"]
            f.write(
                f"| {r['name']} | {r['selection']} | {r['pop_factor']} | {r['elite_frac']} | {r['p_crossover']} | {r['p_mut']} | "
                f"{st['best']:.2f} | {st['worst']:.2f} | {st['mean']:.2f} | {st['median']:.2f} | {st['std']:.2f} | "
                f"{r['sr']:.2f} | {'' if r['med_evals'] is None else int(r['med_evals'])} |\n"
            )
        f.write("\n")
        f.write(f"**Doporučeno:** `{best['name']}` "
                f"(selection={best['selection']}, pop_factor={best['pop_factor']}, "
                f"elite_frac={best['elite_frac']}, p_crossover={best['p_crossover']}, "
                f"p_mut={best['p_mut']}).\n")

    print(f"Benchmark uložen do: {out_path}")
    return out_path
