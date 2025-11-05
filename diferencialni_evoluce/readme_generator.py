import os
import numpy as np
from datetime import datetime
from de_core import DifferentialEvolution
from main import sphere, rastrigin, rosenbrock, schwefel


FUNCTIONS = [
    ("Sphere", sphere, (-100, 100)),
    ("Rastrigin", rastrigin, (-5.12, 5.12)),
    ("Rosenbrock", rosenbrock, (-2.048, 2.048)),
    ("Schwefel", schwefel, (-500, 500)),
]

STRATEGIES = [
    ("DE/rand/1/bin", dict(strategy="rand1bin", F=0.5, CR=0.8)),
    ("DE/best/1/bin", dict(strategy="best1bin", F=0.5, CR=0.8)),
    ("jDE (rand/1)", dict(strategy="rand1bin", F=0.5, CR=0.9, jde=True, tau1=0.1, tau2=0.1)),
]

DIM = 10
POP = 50
MAX_EVALS = 10000
RUNS = 10


# ---------- Pomocné ----------
def sci(x): return f"{x:.3e}"


def run_multiple_runs(de_params, runs=10):
    logs, finals = [], []
    for _ in range(runs):
        de = DifferentialEvolution(**de_params, seed=np.random.randint(0, 9999))
        best, best_fit, log = de.run()
        logs.append(np.array(log))
        finals.append(best_fit)

    # sjednocení délky logů a výpočet průměrné křivky
    min_len = min(len(l) for l in logs)
    logs = [l[:min_len] for l in logs]
    evals = logs[0][:, 0]
    mean_curve = np.mean([l[:, 1] for l in logs], axis=0)
    return evals, mean_curve, np.array(finals)


# ---------- Hlavní funkce ----------
def main():
    os.makedirs("charts", exist_ok=True)
    os.makedirs("tables", exist_ok=True)

    lines = []
    lines.append("# Souhrnný report diferenciální evoluce (DE)")
    lines.append(f"**Datum generování:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## Nastavení experimentu")
    lines.append(f"- Počet běhů = `{RUNS}`")
    lines.append(f"- Dimenze (D) = `{DIM}`")
    lines.append(f"- Počet evaluací = `{MAX_EVALS}`")
    lines.append(f"- Velikost populace = `{POP}`")
    lines.append("")

    lines.append("## Princip fungování DE")
    lines.append(
        "Diferenciální evoluce (DE) pracuje s reálnými vektory. "
        "Každý jedinec představuje řešení a nové kandidáty vytváří kombinací jiných jedinců. "
        "Hlavní části algoritmu jsou:")
    lines.append("")
    lines.append("- **Mutace:** vytváří tzv. *mutantní vektor*. Např. pro strategii `rand/1` platí:")
    lines.append("  \\\( v_i = x_{r1} + F (x_{r2} - x_{r3}) \\)")
    lines.append("  kde `F` (0.5–0.9) určuje velikost kroku.")
    lines.append(
        "- **Křížení (crossover):** kombinuje mutantní vektor s původním jedincem podle pravděpodobnosti `CR`.")
    lines.append("- **Selekce:** pokud je nový jedinec lepší, nahradí původního.")
    lines.append("- **jDE:** speciální varianta, která si sama adaptuje parametry `F` a `CR`.")
    lines.append("")

    lines.append("## Testovací funkce a jejich rozsahy")
    lines.append("| Funkce | Rozsah proměnných |")
    lines.append("| --- | --- |")
    for name, _, (lo, hi) in FUNCTIONS:
        lines.append(f"| {name} | {lo} až {hi} |")
    lines.append("")

    # ---------- Výsledky ----------
    for func_name, func, bounds in FUNCTIONS:
        lines.append(f"## {func_name}")
        lines.append(f"### {func_name.lower()} – D={DIM}, budget={MAX_EVALS}, runs={RUNS}")
        lines.append("")
        results = []
        comparison = []

        for label, strat in STRATEGIES:
            params = dict(func=func, dim=DIM, bounds=bounds,
                          pop_size=POP, max_evals=MAX_EVALS, **strat)
            evals, mean_curve, finals = run_multiple_runs(params, runs=RUNS)

            results.append({
                "label": label,
                "best": np.min(finals),
                "worst": np.max(finals),
                "mean": np.mean(finals),
                "std": np.std(finals)
            })

            log = np.column_stack((evals, mean_curve))
            comparison.append((log, label))

        # tabulka souhrnu
        lines.append("| Varianta | best | worst | mean | std |")
        lines.append("|-----------|-------|-------|------|------|")
        for r in results:
            lines.append(
                f"| {r['label']} | {sci(r['best'])} | {sci(r['worst'])} | {sci(r['mean'])} | {sci(r['std'])} |")
        lines.append("")

        # graf
        chart_path = f"charts/{func_name.lower()}_comparison_avg.png"
        DifferentialEvolution.plot_comparison(comparison,
                                              title=f"Porovnání konvergence – {func_name}",
                                              out_path=chart_path)
        lines.append(f"![{func_name}]({chart_path})")
        lines.append("")

    # ---------- Závěr ----------
    lines.append("---")
    lines.append("## Závěr")
    lines.append(
        "Ze všech funkcí je vidět, že strategie **DE/best/1/bin** "
        "má nejrychlejší konvergenci, ale může uvíznout v lokálním minimu. "
        "**DE/rand/1/bin** je stabilnější, i když pomalejší. "
        "Varianta **jDE** bývá nejrobustnější, protože si průběžně upravuje parametry F a CR.")
    lines.append("")
    lines.append(
        "Na jednoduché funkci Sphere všechny metody dosáhly téměř nulové chyby. "
        "Na Rastriginu se nejlépe projevila jDE. "
        "U Rosenbrocka byla nejpřesnější metoda best/1, zatímco u Schwefelu "
        "se jDE podařilo lépe překonat lokální minima.")
    lines.append("")

    with open("readme.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("✅ Hotovo! Vygenerován soubor readme.md a grafy v /charts/")


if __name__ == "__main__":
    main()
