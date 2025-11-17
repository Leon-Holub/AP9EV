import numpy as np
import matplotlib.pyplot as plt
import os

def ensure_dirs():
    """Creates charts/ and results/ folders."""
    os.makedirs("charts", exist_ok=True)
    os.makedirs("results", exist_ok=True)

def run_multiple(factory, runs=10):
    """Runs a PSO variant multiple times and returns mean/std + raw histories."""
    histories = []
    for _ in range(runs):
        print(f"  Run {_ + 1}/{runs}")
        _, _, hist = factory().run()
        histories.append(np.array(hist))

    max_len = max(len(h) for h in histories)
    padded = [np.pad(h, (0, max_len - len(h)), constant_values=h[-1]) for h in histories]
    data = np.vstack(padded)
    return (data.mean(axis=0), data.std(axis=0)), histories

def compute_stats(histories):
    """Returns best, worst, mean, median, std."""
    finals = np.array([h[-1] for h in histories])
    return {
        "best": float(finals.min()),
        "worst": float(finals.max()),
        "mean": float(finals.mean()),
        "median": float(np.median(finals)),
        "std": float(finals.std()),
    }

def plot_convergence(curves, title, save_as):
    """Plots convergence curves."""
    plt.figure(figsize=(12, 6))
    for mean_curve, label in curves:
        plt.plot(mean_curve, linewidth=2, label=label)

    plt.yscale("log")
    plt.xlabel("Iterace")
    plt.ylabel("Best f(x)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_as, dpi=200)
    plt.close()

def save_markdown(problem_name, stats):
    """Creates markdown file with bolded best variant."""
    path = f"results/{problem_name}_results.md"
    best_variant = min(stats, key=lambda k: stats[k]["best"])

    lines = [
        f"# Výsledky PSO – {problem_name}\n",
        "| Varianta | Best | Worst | Mean | Median | Std |",
        "|----------|------|-------|------|--------|------|",
    ]

    for name, s in stats.items():
        if name == best_variant:
            l = f"| **{name}** | **{s['best']:.6e}** | **{s['worst']:.6e}** | **{s['mean']:.6e}** | **{s['median']:.6e}** | **{s['std']:.6e}** |"
        else:
            l = f"| {name} | {s['best']:.6e} | {s['worst']:.6e} | {s['mean']:.6e} | {s['median']:.6e} | {s['std']:.6e} |"
        lines.append(l)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
