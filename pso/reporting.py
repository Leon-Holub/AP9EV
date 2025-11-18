import numpy as np
import matplotlib.pyplot as plt
import os

def ensure_dirs():
    os.makedirs("charts", exist_ok=True)
    os.makedirs("results", exist_ok=True)

def run_multiple(factory, runs=10):
    histories = []

    for run_num in range(runs):
        print(f"  Spouštím běh {run_num + 1}/{runs}...")
        _, _, hist = factory().run()
        histories.append(hist)

    max_fes = max(h[-1][0] for h in histories)

    padded = []
    for h in histories:
        fes_vals = [t[0] for t in h]
        best_vals = [t[1] for t in h]

        if fes_vals[-1] < max_fes:
            fes_vals.append(max_fes)
            best_vals.append(best_vals[-1])

        padded.append((np.array(fes_vals), np.array(best_vals)))

    all_fes = padded[0][0]
    all_vals = np.vstack([p[1] for p in padded])

    mean_curve = np.mean(all_vals, axis=0)
    std_curve = np.std(all_vals, axis=0)

    return (all_fes, mean_curve, std_curve), histories


def compute_stats(histories):
    finals = np.array([h[-1][1] for h in histories])
    return {
        "best": float(finals.min()),
        "worst": float(finals.max()),
        "mean": float(finals.mean()),
        "median": float(np.median(finals)),
        "std": float(finals.std()),
    }


def plot_convergence(curves, title, save_as):
    plt.figure(figsize=(12, 6))

    for fes, mean_curve, label in curves:
        plt.plot(fes, mean_curve, linewidth=2, label=label)

    plt.yscale("log")
    plt.xlabel("FES (počet vyhodnocení)")
    plt.ylabel("Best f(x)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_as, dpi=200)
    plt.close()


def save_markdown(problem_name, stats):
    path = f"results/{problem_name}_results.md"
    best_variant = min(stats, key=lambda k: stats[k]["best"])

    lines = [
        f"# Výsledky PSO – {problem_name}\n",
        "| Varianta | Best | Worst | Mean | Median | Std |",
        "|----------|------|-------|------|--------|------|",
    ]

    for name, s in stats.items():
        if name == best_variant:
            line = (
                f"| **{name}** | **{s['best']:.6e}** | **{s['worst']:.6e}** | "
                f"**{s['mean']:.6e}** | **{s['median']:.6e}** | **{s['std']:.6e}** |"
            )
        else:
            line = (
                f"| {name} | {s['best']:.6e} | {s['worst']:.6e} | "
                f"{s['mean']:.6e} | {s['median']:.6e} | {s['std']:.6e} |"
            )
        lines.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
