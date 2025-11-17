import os

ASSIGNMENT_TEXT = """
## Zadání

Otestujte tři varianty algoritmu PSO na vybraných testovacích funkcích:

- Lineární setrvačnost: **w = 0.8 → 0.3**, c1 = 2, c2 = 2, globální topologie (hvězda)
- Konstantní setrvačnost: **w = 0.7**, c1 = c2 = 1.49618, globální topologie
- Konstantní setrvačnost: **w = 0.6**, c1 = c2 = 1.49618, kruhová topologie (sousedství 2)

Parametry:
- Velikost populace: 20–100 (použito 40)
- MAXFES: 20 000
- vmax = 0.2 * (upper - lower)
- Ošetření hranic pomocí clamp + vynulování rychlosti

Během každé varianty je provedeno **10 běhů**, z nichž se počítá průměrná konvergenční křivka a statistiky výsledků.
"""

METHODOLOGY_TEXT = """
## Metodika

Experimenty používají následující postup:

1. Pro každou testovací funkci (Sphere, Rosenbrock, Schwefel) se spustí tři varianty PSO.
2. Každá varianta je spuštěna **10×** se shodnými parametry.
3. Z každé série 10 běhů se získá:
   - průměrná konvergenční křivka
   - nejlepší, nejhorší, průměrná, mediánová a směrodatná odchylka finální hodnoty
4. Výsledky se ukládají do:
   - `charts/<function>.png` — graf konvergence
   - `results/<function>_results.md` — statistická tabulka
5. Tento protokol (`README.md`) je generován automaticky.
"""

PARAMETERS_TEXT = """
## Parametry PSO variant

| Varianta | w | c1 | c2 | Topologie |
|----------|----|------|------|-------------|
| Lineární w | 0.8 → 0.3 | 2.0 | 2.0 | global |
| Konstantní w | 0.7 | 1.49618 | 1.49618 | global |
| Konstantní w | 0.6 | 1.49618 | 1.49618 | ring (2 sousedé) |
"""

def generate_readme(output_path="README.md"):
    """Generates a complete markdown protocol with assignment, results, graphs and interpretation."""

    result_dir = "results"
    chart_dir = "charts"

    files = sorted(f for f in os.listdir(result_dir) if f.endswith("_results.md"))

    lines = []

    lines.append("# PSO Benchmark – Protokol\n")
    lines.append(ASSIGNMENT_TEXT)
    lines.append(METHODOLOGY_TEXT)
    lines.append(PARAMETERS_TEXT)
    lines.append("---\n")
    lines.append("## Výsledky\n")

    # pro následné summary
    winners = []

    for filename in files:
        problem = filename.replace("_results.md", "")
        result_path = os.path.join(result_dir, filename)
        chart_path = os.path.join(chart_dir, f"{problem}.png")

        lines.append(f"### {problem.capitalize()}\n")

        # graf
        if os.path.exists(chart_path):
            lines.append(f"![graf]({chart_path})\n")

        # tabulka
        with open(result_path, "r", encoding="utf-8") as f:
            table = f.read()

        # najdi vítězný řádek
        for line in table.split("\n"):
            if line.startswith("| **"):
                winner = line.split("|")[1].strip("* ").strip()
                winners.append(winner)
                break

        lines.append(table)
        lines.append("\n")

        # automatická interpretace
        lines.append(f"**Hodnocení pro {problem}:**\n")
        lines.append(f"- Nejlepší varianta: **{winner}**\n")
        lines.append("")

        lines.append("---\n")

    # celkové shrnutí
    lines.append("## Celkové zhodnocení\n")

    if winners:
        from collections import Counter
        count = Counter(winners)
        best_overall = count.most_common(1)[0][0]

        lines.append(f"- Nejčastější vítěz přes všechny funkce: **{best_overall}**\n")
        lines.append(f"- Výskyt vítězů: `{dict(count)}`\n")
        lines.append("\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("README.md úspěšně vygenerováno:", output_path)

if __name__ == "__main__":
    generate_readme()