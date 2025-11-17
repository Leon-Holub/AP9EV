from pso_core import PROBLEMS, variant_linear, variant_const_global, variant_const_ring
from reporting import ensure_dirs, run_multiple, plot_convergence, compute_stats, save_markdown

if __name__ == "__main__":
    ensure_dirs()

    for name, prob in PROBLEMS.items():
        print("Zpracovávám problém:", name)

        func = prob["fn"]
        bounds = prob["bounds"]

        print("Spouštím varianty PSO...")
        print("  Lineární w (0.8→0.3), global")
        (mean1, _), hist1 = run_multiple(lambda: variant_linear(func, bounds))

        print("  Konstantní w = 0.7, global")
        (mean2, _), hist2 = run_multiple(lambda: variant_const_global(func, bounds))

        print("  Konstantní w = 0.6, ring")
        (mean3, _), hist3 = run_multiple(lambda: variant_const_ring(func, bounds))

        curves = [
            (mean1, "lineární w (0.8→0.3), global"),
            (mean2, "w = 0.7, global"),
            (mean3, "w = 0.6, ring"),
        ]

        plot_convergence(curves, f"Konvergence PSO – {name}", f"charts/{name}.png")

        stats = {
            "lineární w (0.8→0.3) – global": compute_stats(hist1),
            "w = 0.7 – global": compute_stats(hist2),
            "w = 0.6 – ring": compute_stats(hist3),
        }

        save_markdown(name, stats)
        print(f"  Výsledky uloženy pro problém: {name}\n")
        print("\n")

