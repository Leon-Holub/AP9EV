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
# Detect functions automatically from tables folder
# ---------------------------------------------------------

def detect_functions(tables_dir):
    files = glob.glob(os.path.join(tables_dir, "D10_*_summary.md"))

    fnames = []
    for f in files:
        base = os.path.basename(f)
        # pattern D10_<fname>_summary.md
        parts = base.split("_")
        if len(parts) >= 3:
            fname = parts[1]
            fnames.append(fname)

    return sorted(fnames)


# ---------------------------------------------------------
# Main protocol generator
# ---------------------------------------------------------

def generate_protocol():

    tables_dir = "tables"
    charts_dir = "charts"

    dims = [10, 20]

    # Detekce funkcí podle tabulek pro D10
    functions = detect_functions(tables_dir)

    lines = []

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    lines.append("#Porovnání evolučních algoritmů \n")

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

Pro každou kombinaci se ukládá:

- Průměr  
- Směrodatná odchylka  
- Medián  
- Minimum  
- Maximum  

Dále jsou generovány grafy konvergence:
- 1 graf pro každou kombinaci funkce × dimenze = 2 grafy na funkci.
"""
    )

    # ---------------------------------------------------------
    # Per-function results (tables + charts)
    # ---------------------------------------------------------

    lines.append("\n# Výsledky podle funkcí\n")

    for fname in functions:
        lines.append(f"\n# Funkce: **{fname}**\n")

        # TABLES for D10 & D20
        for D in dims:
            table_path = os.path.join(tables_dir, f"D{D}_{fname}_summary.md")
            if os.path.exists(table_path):
                lines.append(f"\n## Výsledky – D={D}\n")
                lines.append(load_table(table_path))
            else:
                lines.append(f"\n⚠️ Chybí tabulka: {table_path}\n")

            # GRAPH after table
            chart_path = os.path.join(charts_dir, f"D{D}_{fname}_convergence.png")
            if os.path.exists(chart_path):
                lines.append(f"\n### Konvergence – D={D}\n")
                lines.append(embed_image(chart_path))
                lines.append("\n")
            else:
                lines.append(f"\n⚠️ Chybí graf: {chart_path}\n")

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
