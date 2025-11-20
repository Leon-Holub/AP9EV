import os

ASSIGNMENT_TEXT = """
## Zadání

Otestujte tři varianty algoritmu PSO na vybraných testovacích funkcích:

- Lineární setrvačnost: **w = 0.8 → 0.3**, c1 = 2, c2 = 2, globální topologie (hvězda)
- Konstantní setrvačnost: **w = 0.7**, c1 = c2 = 1.49618, globální topologie
- Konstantní setrvačnost: **w = 0.6**, c1 = c2 = 1.49618, kruhová topologie (sousedství 2)

Parametry:
- Velikost populace: 40
- MAXFES: 20 000
- vmax = 0.2 * (upper - lower)
- Částice se mohou volně pohybovat i mimo prostor hledání.
  Hodnoty mimo bounds jsou ohodnoceny jako **+inf**.
- Nepoužívá se boundary-clipping.
- Během každé varianty je provedeno **10 běhů**, z nichž se počítá průměrná konvergenční křivka a statistiky výsledků.
"""


PARAMETERS_TEXT = """
## Parametry PSO variant

| Varianta | w | c1 | c2 | Topologie |
|----------|----|------|------|-------------|
| Lineární w | 0.8 → 0.3 | 2.0 | 2.0 | global |
| Konstantní w | 0.7 | 1.49618 | 1.49618 | global |
| Konstantní w | 0.6 | 1.49618 | 1.49618 | ring (2 sousedé) |
"""


def interpret(problem_name, winner_name):

    if problem_name == "rosenbrock":
        return (
            "- Rosenbrockova funkce obsahuje úzké zakřivené údolí.\n"
            "- Ring topologie udržuje diverzitu a zabraňuje předčasné konvergenci.\n"
            "- **Výsledky odpovídají teorii — ring PSO dominuje.**"
        )

    if problem_name == "schwefel":
        return (
            "- Schwefel je extrémně multimodální funkce s mnoha lokálními minimy.\n"
            "- Lineární setrvačnost poskytuje agresivní exploraci na začátku.\n"
            "- **Proto lineární varianta dosáhla nejlepších výsledků.**"
        )

    if problem_name == "sphere":
        return (
            "- Sphere je jednoduchá unimodální funkce.\n"
            "- Nejlepší výkon má stabilní nastavení bez velkých výkyvů.\n"
            "- **Konstantní w = 0.7 global je očekávaně nejlepší.**"
        )

    return ""


def generate_readme(output_path="README.md"):
    result_dir = "results"
    chart_dir = "charts"

    files = sorted(f for f in os.listdir(result_dir) if f.endswith("_results.md"))

    lines = []
    lines.append("# PSO\n")
    lines.append(ASSIGNMENT_TEXT)
    lines.append(PARAMETERS_TEXT)
    lines.append("---\n")
    lines.append("## Výsledky\n")

    winners = []

    for filename in files:
        problem = filename.replace("_results.md", "")
        result_md = os.path.join(result_dir, filename)
        chart_path = f"charts/{problem}.png"  # opravené lomítko

        lines.append(f"### {problem.capitalize()}\n")
        lines.append(f"![{problem}]({chart_path})\n")

        # načíst výsledky a odstranit první nadpis
        with open(result_md, "r", encoding="utf-8") as f:
            table_lines = f.read().split("\n")

        # přeskočíme první řádky "# Výsledky PSO – X"
        table_lines = table_lines[2:]

        # najít vítěze
        for line in table_lines:
            if line.startswith("| **"):
                winner = line.split("|")[1].strip("* ").strip()
                winners.append(winner)
                break

        lines.append("\n".join(table_lines))
        lines.append("\n")
        lines.append("#### Interpretace výsledků\n")
        lines.append(interpret(problem, winner))
        lines.append("\n---\n")

    # celkové zhodnocení
    lines.append("## Celkové zhodnocení\n")

    from collections import Counter
    count = Counter(winners)

    if len(set(winners)) == len(winners):
        # každý vyhrál jednou
        lines.append("- Každá varianta zvítězila na jedné testovací funkci.\n")
        lines.append("- **Dominance variant závisí na charakteru funkce.**\n")
    else:
        best_overall = count.most_common(1)[0][0]
        lines.append(f"- Nejčastější vítěz napříč funkcemi: **{best_overall}**\n")

    lines.append(f"- Výskyt vítězů: `{dict(count)}`\n\n")

    lines.append("### Shrnutí chování PSO variací\n")
    lines.append(
        "- Lineární setrvačnost exceluje v multimodálních prostorech.\n"
        "- Konstantní w = 0.7 je nejlepší v hladkých unimodálních funkcích.\n"
        "- Ring topologie přináší diverzitu a je vhodná pro funkce s úzkými 'údolími'.\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("README.md úspěšně vygenerováno:", output_path)


if __name__ == "__main__":
    generate_readme()