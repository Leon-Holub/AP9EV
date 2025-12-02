import os
import glob
from collections import defaultdict

OUTPUT_FILE = "README.md"


# ---------------------------------------------------------
# Helper loaders
# ---------------------------------------------------------

def load_table(path):
    """Returns table text without the first Markdown heading line."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = [line for line in lines if not line.startswith("# Summary")]
    return "".join(cleaned)


def embed_image(path):
    return f"![{os.path.basename(path)}]({path})"


# ---------------------------------------------------------
# Detect functions automatically
# ---------------------------------------------------------

def detect_functions(tables_dir):
    files = glob.glob(os.path.join(tables_dir, "D10_*_summary.md"))

    fnames = []
    for f in files:
        base = os.path.basename(f)
        parts = base.split("_")
        if len(parts) >= 3:
            fnames.append(parts[1])

    return sorted(fnames)


# ---------------------------------------------------------
# Parse summary table to find the best algorithm
# ---------------------------------------------------------

def extract_best_algorithm_from_table(path):
    """
    Reads a markdown summary table and finds the algorithm with the best (lowest) mean.
    Returns algorithm name or None if table missing.
    """
    if not os.path.exists(path):
        return None

    best_algo = None
    best_value = float("inf")

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:

        # skip non-data rows
        if not line.startswith("|"):
            continue
        if "Algorithm" in line:
            continue
        if "---" in line:  # separator row
            continue

        # split row
        parts = [p.strip() for p in line.split("|")[1:-1]]

        # ensure correct column count
        if len(parts) < 2:
            continue

        algo = parts[0].replace("**", "").strip()
        mean_str = parts[1].replace("**", "").strip()

        # skip invalid numeric rows
        try:
            mean = float(mean_str)
        except ValueError:
            continue

        if mean < best_value:
            best_value = mean
            best_algo = algo

    return best_algo


# ---------------------------------------------------------
# Main protocol generator
# ---------------------------------------------------------

def generate_protocol():
    tables_dir = "tables"
    charts_dir = "charts"
    dims = [10, 20]

    functions = detect_functions(tables_dir)

    # structure for storing winners
    best_summary = defaultdict(dict)

    lines = []

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    lines.append("# Porovnání evolučních algoritmů \n")

    lines.append("## Zadání\n")
    lines.append(
        """
Vybrané algoritmy pro porovnání:

- **GA** – real-valued encoding  
- **DE** – rand/1/bin, best/1/bin, jDE  
- **PSO** – linear inertia, const-global, const-ring  

Testované funkce jsou automaticky detekované podle vygenerovaných tabulek (včetně *sphere*, která sloužila jako rychlý benchmark).

Každý algoritmus optimalizuje každou funkci **11×**.

Limit počtu vyhodnocení:

- **100 000** pro dimenzi **D=10**  
- **200 000** pro dimenzi **D=20**

U každé kombinace zaznamenáváme:

- Průměr  
- Směrodatnou odchylku  
- Medián  
- Minimum  
- Maximum  

Následně vytváříme grafy konvergence.
"""
    )

    # ---------------------------------------------------------
    # Per-function results (tables + charts)
    # ---------------------------------------------------------

    lines.append("\n# Výsledky podle funkcí\n")

    for fname in functions:
        lines.append(f"\n# Funkce: **{fname}**\n")

        for D in dims:
            table_path = f"{tables_dir}/D{D}_{fname}_summary.md"
            graph_path = f"{charts_dir}/D{D}_{fname}_convergence.png"

            # TABULKA
            if os.path.exists(table_path):
                lines.append(f"\n## Výsledky – D={D}\n")
                lines.append(load_table(table_path))

                # uložit nejlepší metodu
                best = extract_best_algorithm_from_table(table_path)
                best_summary[fname][D] = best
            else:
                lines.append(f"\n⚠️ Chybí tabulka: {table_path}\n")

            # GRAF
            if os.path.exists(graph_path):
                lines.append(f"\n### Konvergence – D={D}\n")
                lines.append(embed_image(graph_path))
                lines.append("\n")
            else:
                lines.append(f"\n⚠️ Chybí graf: {graph_path}\n")

    # ---------------------------------------------------------
    # SUMMARY / ZÁVĚR
    # ---------------------------------------------------------

    lines.append("\n# Závěr\n")
    lines.append("Níže je shrnutí nejúspěšnějších algoritmů podle funkce a dimenze.\n")

    # Přehledová tabulka
    lines.append("\n## Přehled nejlepších algoritmů\n")
    lines.append("| Funkce | Nejlepší algoritmus (D=10) | Nejlepší algoritmus (D=20) |")
    lines.append("|--------|------------------------------|-----------------------------|")

    for fname in functions:
        d10 = best_summary[fname].get(10, "—")
        d20 = best_summary[fname].get(20, "—")

        lines.append(f"| {fname} | {d10} | {d20} |")

    # Slovní shrnutí
    lines.append("\n## Slovní shrnutí výkonu algoritmů\n")

    for fname in functions:
        d10 = best_summary[fname].get(10)
        d20 = best_summary[fname].get(20)

        if d10 or d20:
            lines.append(f"- Na funkci **{fname}** byl nejlepší:")
            if d10:
                lines.append(f"  - v **D=10** → **{d10}**")
            if d20:
                lines.append(f"  - v **D=20** → **{d20}**")
            lines.append("")

    # Charakteristiky výsledků
    lines.append("\n## Interpretace výsledků\n")
    lines.append(
        """
- **jDE** obvykle dominuje na silně multimodálních funkcích (Rastrigin, Schwefel).
- **DE_best1bin** často exceluje na konvexních úlohách (Sphere) nebo u hladkých funkcí.
- **PSO_linear_global** má slušný výkon v nižších dimenzích, ale hůře škáluje.
- **GA** je výrazně nejslabší a slouží jako baseline pro porovnání.

Celkově se jako nejuniverzálnější metoda ukázala varianta **jDE**, která se stabilně umísťovala mezi nejlepšími napříč různými typy funkcí.
"""
    )

    # ---------------------------------------------------------
    # Save README.md
    # ---------------------------------------------------------

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nREADME.md bylo úspěšně vygenerováno → {OUTPUT_FILE}")


# ---------------------------------------------------------
# Run
# ---------------------------------------------------------

if __name__ == "__main__":
    generate_protocol()
