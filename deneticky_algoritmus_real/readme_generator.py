import os
import re
import importlib.util
from datetime import datetime

MAIN_FILE = "main.py"
CHARTS_ROOT = "charts"
OUT_FILE = "readme.md"

# --- Text závěru ---
ZAVER = """\
## Závěr

Předpokládal jsem, že nejlépe si povede varianta s Gaussovskou mutací, protože pracuje s reálnými hodnotami a umožňuje jemné dolaďování řešení.
Výsledky mě ale překvapily – nejčastěji nejlepších výsledků dosáhla varianta IEEE754_bits, která používá bitovou reprezentaci čísel ve formátu float32.

Tato varianta se ukázala jako velmi přesná, hlavně u jednodušších funkcí (Sphere, Rosenbrock), zatímco reálné varianty měly větší rozptyl výsledků.
U složitější funkce Schwefel se nejlépe dařilo BCD reprezentaci, pravděpodobně díky větším skokům v prostoru, které pomáhají vyhnout se lokálním minimům.
"""


# --- Načtení main.py jako modulu ---
def load_main_config(file_path):
    spec = importlib.util.spec_from_file_location("ga_main", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- Oprava cest obrázků ---
def fix_image_paths(content: str, rel_dir: str) -> str:
    def repl(match):
        alt, path = match.groups()
        fixed = os.path.join(rel_dir, path).replace("\\", "/")
        return f"![{alt}]({fixed})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, content)


# --- Načtení všech stats.md ---
def read_all_stats(root):
    order = ["sphere", "rosenbrock", "schwefel"]
    combined = []
    for func_dir in order:
        func_path = os.path.join(root, func_dir)
        if not os.path.isdir(func_path):
            continue
        for sub in sorted(os.listdir(func_path)):
            stats_path = os.path.join(func_path, sub, "stats.md")
            if os.path.exists(stats_path):
                with open(stats_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                rel_dir = os.path.relpath(os.path.join(func_path, sub), start=os.getcwd())
                fixed_content = fix_image_paths(content, rel_dir)
                combined.append(f"## {func_dir.upper()}\n\n{fixed_content}\n")
    return "\n\n".join(combined)


# --- Generování hlavičky + popisů ---
def make_header(cfg):
    lines = []
    lines.append("# Souhrnný report genetického algoritmu (GA)")
    lines.append(f"**Datum generování:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## Nastavení experimentu")
    lines.append("")
    lines.append(f"- RNG_SEED = `{cfg.RNG_SEED}`")
    lines.append(f"- Počet běhů = `{cfg.RUNS}`")
    lines.append(f"- Dimenze (D) = `{cfg.D}`")
    lines.append(f"- Počet evaluací (budget) = `{cfg.EVAL_BUDGET}`")
    lines.append(f"- Velikost populace = `{cfg.POP_SIZE}`")
    lines.append(f"- Elitismus = `{int(cfg.ELITE_FRAC * 100)} %`")
    lines.append("")
    lines.append("## Princip fungování GA")
    lines.append("")
    lines.append("### Křížení (single-point crossover mezi dimenzemi)")
    lines.append(
        "Křížení probíhá mezi dvěma rodiči tak, že se náhodně zvolí **index dimenze (1 až D-1)**, "
        "na kterém se jejich vektory rozdělí. Potomci zdědí první část dimenzí od prvního rodiče a zbytek od druhého. "
        "Tento princip se používá jednotně pro všechny varianty, ale u bitových reprezentací se kříží celé 32bitové bloky."
    )
    lines.append("")
    lines.append("### Mutace")
    lines.append(
        f"- **Bitové varianty:** každý bit má pravděpodobnost `{cfg.P_MUT_BIT:.4f}` že se přepne (0→1 nebo 1→0). "
        "Tím vzniká jemná náhodná změna binární reprezentace. Po mutaci se každý jedinec znovu dekóduje do reálných hodnot."
    )
    lines.append(
        f"- **Reálné varianty:** každá dimenze má pravděpodobnost `{cfg.P_MUT_REAL}` na mutaci, přičemž se používají dvě metody:"
    )
    lines.append(
        f"  - **Gaussian mutace:** hodnota se posune o N(0, σ²), kde σ = {cfg.GAUSS_SIGMA_FRAC * 100:.1f}% rozsahu proměnné. "
        "Zajišťuje jemné ladění řešení v lokálním okolí."
    )
    lines.append(
        "  - **RandomReset:** vybrané dimenze se nastaví na náhodnou hodnotu z celého intervalu. "
        "Podporuje globální průzkum prostoru a překonávání lokálních minim."
    )
    lines.append("")
    lines.append("## Bitové reprezentace a jejich význam")
    lines.append("")
    lines.append("### IEEE754")
    lines.append(
        "Každý jedinec je reprezentován jako 32bitová hodnota ve formátu IEEE 754 (1 bit znaménko, 8 bitů exponent, 23 bitů mantisa). "
        "Bity se interpretují přímo jako `float32` a následně se převádí pomocí funkce tanh() do rozsahu (-1, 1), "
        "který se pak škáluje do domény dané funkce. Tato reprezentace umožňuje pracovat s velmi malými i velmi velkými čísly, "
        "ale kvůli nelineárnímu rozložení může být mutace neintuitivní (malá změna bitu může způsobit velký skok v hodnotě)."
    )
    lines.append("")
    lines.append("### Fixed-Point (Q16.16)")
    lines.append(
        "Každý parametr je reprezentován jako 32bitové celé číslo, kde 16 bitů je pro celou část a 16 bitů pro desetinnou část. "
        "Po dekódování se hodnota převede dělením 2^16. Tato metoda zaručuje lineární mapování, ale má omezené rozlišení a může "
        "způsobit, že sousední hodnoty jsou vzdálené o konstantní krok (kvantizační chyba)."
    )
    lines.append("")
    lines.append("### BCD (Binary Coded Decimal)")
    lines.append(
        "Každý parametr je tvořen 8 číslicemi po 4 bitech (celkem 32 bitů). Každý 4bitový blok reprezentuje číslici 0–9. "
        "Po dekódování se složí celé číslo 0–99 999 999, které se následně lineárně převede do domény funkce. "
        "Výhodou je snadná interpretace, nevýhodou hrubá granularita a neefektivní využití bitů."
    )
    lines.append("")
    if hasattr(cfg, "PROBLEMS"):
        lines.append("## Optimalizační funkce")
        funcs = ", ".join(cfg.PROBLEMS.keys())
        lines.append(funcs)
    lines.append("\n---\n")
    return "\n".join(lines)


# --- Hlavní funkce ---
def main():
    if not os.path.exists(MAIN_FILE):
        raise FileNotFoundError(f"Soubor {MAIN_FILE} nebyl nalezen.")

    cfg = load_main_config(MAIN_FILE)
    header = make_header(cfg)
    stats = read_all_stats(CHARTS_ROOT)

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(stats)
        f.write("\n\n---\n\n")
        f.write(ZAVER)

    print(f"✅ Souhrnný report uložen jako: {OUT_FILE}")


if __name__ == "__main__":
    main()
