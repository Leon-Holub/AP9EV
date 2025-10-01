import re
from ga_core import RNG_SEED, RUNS, DIM_LIST, PROBLEMS, POP_FACTOR, ELITE_FRAC, P_CROSS, P_MUT


def _read_if_exists(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def _rewrite_image_paths(md_text: str, base_dir: str) -> str:
    if not md_text:
        return md_text

    def repl(m):
        alt, url = m.group(1), m.group(2).strip()
        if url.startswith(("http://", "https://", "/", "charts/")):
            return m.group(0)
        while url.startswith("./"):
            url = url[2:]
        new_url = f"{base_dir}/{url}".replace("\\", "/")
        return f"![{alt}]({new_url})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, md_text)


def create_readme(
        problems=None,
        dims=None,
        runs: int = None,
        out_path: str = "readme.md"
):
    probs = problems or (PROBLEMS if "PROBLEMS" in globals() else ["onemax", "leading_ones"])
    dimensions = dims or (DIM_LIST if "DIM_LIST" in globals() else [10, 30, 100])
    runs_val = runs if runs is not None else (RUNS if "RUNS" in globals() else 10)

    lines = []

    lines.append("## Použité parametry")
    lines.append("Níže jsou uvedena hlavní nastavení genetického algoritmu a jejich vysvětlení.\n")

    lines.append(f"- **RNG_SEED** = `{RNG_SEED}`  \n"
                 f"  Seed generátoru náhodných čísel. Díky němu jsou výsledky reprodukovatelné.")

    lines.append(f"- **RUNS** = `{RUNS}`  \n"
                 f"  Počet běhů na každou kombinaci dimenze, úlohy a selekční strategie.")

    lines.append(f"- **DIM_LIST** = `{DIM_LIST}`  \n"
                 f"  Délky binárního řetězce (D), pro které se testuje.")

    lines.append(f"- **POP_FACTOR** = `{POP_FACTOR}`  \n"
                 f"  Populace má velikost `POP_FACTOR × D`, tedy např. {int(POP_FACTOR * 10)} jedinců pro D=10.")

    lines.append(f"- **ELITE_FRAC** = `{ELITE_FRAC:.2f}`  \n"
                 f"  {int(ELITE_FRAC * 100)} % nejlepších jedinců se zkopíruje přímo do další generace (elitismus).")

    lines.append(f"- **P_CROSS** = `{P_CROSS:.2f}`  \n"
                 f"  Pravděpodobnost, že dojde k jednobodovému křížení.")

    lines.append(f"- **P_MUT** = `{P_MUT:.4f}`  \n"
                 f"  Pravděpodobnost bitové mutace (otočení 0 ↔ 1) na jednotlivý bit.")

    lines.append("")
    lines.append("- **Selekce rodičů:** ruletová (*roulette*) a pořadová (*rank*).")
    lines.append("- **Křížení:** jednobodové (one-point crossover).")
    lines.append("- **Mutace:** bit-flip s pravděpodobností `P_MUT` na každý bit.")
    lines.append("")
    budget_info = ", ".join(f"{D} → {100 * D} evaluací" for D in DIM_LIST)
    lines.append(f"**Rozpočet hodnocení:** 100 × D ( {budget_info} )")
    lines.append("\n---\n")

    for problem in probs:
        lines.append(f"## Výsledky – {problem}\n")
        for D in dimensions:
            base = f"charts/{problem}/{D}"

            stats_md = _read_if_exists(f"{base}/stats.md")
            if stats_md:
                lines.append(_rewrite_image_paths(stats_md, base))
                lines.append("")

            psearch_md = _read_if_exists(f"{base}/param_search.md")
            if psearch_md:
                lines.append("#### Parametrické hledání (grid)\n")
                lines.append(_rewrite_image_paths(psearch_md, base))
                lines.append("")

            pstats_md = _read_if_exists(f"{base}/param_stats.md")
            if pstats_md:
                lines.append("#### Srovnání vybraných nastavení\n")
                lines.append(_rewrite_image_paths(pstats_md, base))
                lines.append("")

            if not any([stats_md, psearch_md, pstats_md]):
                lines.append("_(Pro tuto kombinaci zatím nejsou generované výstupy.)_\n")

        lines.append("\n---\n")

    lines.append("## Závěr\n")
    lines.append(
        "V rámci úkolu byl vytvořen genetický algoritmus, který pracuje s binární reprezentací a využívá elitismus, ruletovou a pořadovou selekci, jednobodové křížení a bitovou mutaci.\n")
    lines.append(
        "Algoritmus byl otestován na dvou úlohách – **OneMax** a **LeadingOnes** – pro délky řetězce 10, 30 a 100. Každý experiment byl proveden desetkrát a výsledky byly vyhodnoceny pomocí konvergenčních grafů a základních statistických ukazatelů (nejlepší, nejhorší, průměrná a mediánová hodnota, směrodatná odchylka).\n")
    lines.append(
        "Výsledky ukázaly, že genetický algoritmus dokáže spolehlivě nacházet optimální řešení v daném rozpočtu evaluací. Elitismus pomohl udržovat kvalitní jedince v populaci a urychlil dosažení maxima. Ruletová selekce fungovala dobře u jednodušší úlohy OneMax, zatímco pořadová selekce se ukázala jako stabilnější u LeadingOnes, kde absolutní rozdíly ve fitness nejsou tak výrazné.\n")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] readme vygenerováno → {out_path}")
