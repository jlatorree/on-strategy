#!/usr/bin/env python3
"""on-strategy: operaciones sobre el grafo de nodos de una carpeta de trabajo.

    python3 graph.py init "<entidad>" "<nivel>"   crea la estructura completa
    python3 graph.py status                       tabla de estado
    python3 graph.py deps <nodo>                  que leer antes de escribirlo
    python3 graph.py touch <nodo> [--apply]       que queda desactualizado al tocarlo
    python3 graph.py sync                         regenera index.md y los wikilinks
    python3 graph.py lint                         chequeo de salud
    python3 graph.py archive [--keep N]           corta log.md y archiva lo viejo

Opera sobre el directorio actual. Si no puedes hacer cd a la carpeta de trabajo,
pasa --root "<ruta>" en cualquier comando.

`init` deja una copia de este script en <carpeta de trabajo>/scripts/graph.py, para
que las sesiones siguientes lo corran con una ruta relativa y no haya que ubicar el
skill de nuevo.

El grafo es una constante del framework, no del proyecto: no cambia entre carpetas.
"""
import os, re, shutil, sys, pathlib

ROOT = pathlib.Path(".")
SECTIONS = "01_outputs/sections"
CONTEXT = "00_context"
INBOX = "00_context/inbox"


def R(*parts):
    """Ruta dentro de la carpeta de trabajo."""
    return ROOT.joinpath(*parts)

# (id, titulo, destino)
NODES = [
    ("00-problema-a-resolver",      "Problema a resolver",                        "memo"),
    ("01-winning-aspiration",       "Winning Aspiration",                         "memo"),
    ("02-where-to-play-how-to-win", "Where to Play y How to Win",                 "memo"),
    ("03-capabilities",             "Must-Have Capabilities",                     "memo"),
    ("04-management-systems",       "Enabling Management Systems",                "memo"),
    ("05-posibilidades-descartadas","Posibilidades descartadas",                  "memo"),
    ("06-supuestos-vivos",          "Supuestos vivos",                            "memo"),
    ("07-senales-de-cambio",        "Senales de cambio",                          "memo"),
    ("a1-strategic-logic-flow",     "Strategic Logic Flow",                       "anexo"),
    ("a2-posibilidades-wwhtbt",     "Posibilidades y What Would Have To Be True", "anexo"),
]
TITLE = {n: t for n, t, _ in NODES}
DEST = {n: d for n, _, d in NODES}

# aristas dirigidas: origen -> nodos que dependen de el
EDGES = {
    "00-problema-a-resolver":       ["01-winning-aspiration", "a1-strategic-logic-flow"],
    "a1-strategic-logic-flow":      ["a2-posibilidades-wwhtbt", "02-where-to-play-how-to-win"],
    "01-winning-aspiration":        ["02-where-to-play-how-to-win"],
    "a2-posibilidades-wwhtbt":      ["02-where-to-play-how-to-win", "05-posibilidades-descartadas",
                                     "06-supuestos-vivos"],
    "02-where-to-play-how-to-win":  ["03-capabilities", "05-posibilidades-descartadas",
                                     "06-supuestos-vivos", "07-senales-de-cambio"],
    "03-capabilities":              ["04-management-systems"],
}
PARENTS = {n: [] for n, _, _ in NODES}
for src, dsts in EDGES.items():
    for d in dsts:
        PARENTS[d].append(src)

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
ENTRY = re.compile(r"^## \[", re.M)
LOG_MAX = 150  # por encima de esto, lint sugiere archivar


def path(node):
    return R(SECTIONS, f"{node}.md")


def read_fm(node):
    p = path(node)
    if not p.exists():
        return None
    m = FM.match(p.read_text(encoding="utf-8"))
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def state(node):
    fm = read_fm(node)
    if fm is None:
        return "(falta el archivo)"
    return fm.get("estado", "vacio") or "vacio"


def all_states():
    return {n: state(n) for n, _, _ in NODES}


# ---------------------------------------------------------------- init

NODE_TEMPLATE = """---
node: {node}
titulo: {titulo}
destino: {destino}
estado: vacio
version: 0
decidido_el:
desactualizado_por:
---

# {titulo}
"""


def cmd_init(entidad="", nivel=""):
    for d in (SECTIONS, INBOX, "scripts"):
        os.makedirs(str(R(d)), exist_ok=True)
    for node, titulo, destino in NODES:
        p = path(node)
        if not p.exists():
            p.write_text(NODE_TEMPLATE.format(node=node, titulo=titulo, destino=destino),
                         encoding="utf-8")
    src = R(CONTEXT, "sources.md")
    if not src.exists():
        src.write_text(
            "# Fuentes\n\nCada fuente externa que no tiene archivo en `00_context/`.\n\n"
            "| Fuente | Fecha | Que aporta | Marca |\n|---|---|---|---|\n",
            encoding="utf-8")
    log = R("log.md")
    if not log.exists():
        log.write_text("# Bitacora\n\nCronologica, append only. Nunca se reordena.\n\n"
                       "Formato: `## [AAAA-MM-DD] tipo | nodo`, una linea de detalle debajo.\n"
                       "Tipos: `ruta`, `decision`, `ingest`, `alerta`, `memo`.\n\n",
                       encoding="utf-8")
    idx = R("index.md")
    if not idx.exists():
        idx.write_text(index_skeleton(entidad, nivel), encoding="utf-8")
    here = pathlib.Path(__file__).resolve()
    dest = R("scripts", "graph.py").resolve()
    if here != dest:
        shutil.copyfile(str(here), str(dest))
    cmd_sync()
    print(f"Estructura creada. {len(NODES)} nodos en {SECTIONS}/, todos en estado vacio.")


def index_skeleton(entidad="", nivel=""):
    return f"""---
entidad: {entidad}
nivel: {nivel}
ruta_acordada: false
bloque_en_curso:
---

# Indice de la estrategia

**Entidad:** {entidad or "[nombre]"} · **Nivel:** {nivel or "[empresa / unidad / marca / funcion]"}

## Estado de los nodos

<!-- graph:status -->
<!-- /graph:status -->

## Alertas abiertas

Ninguna.

## Que falta para compilar el memo

<!-- graph:pending -->
<!-- /graph:pending -->
"""


# ---------------------------------------------------------------- status

def status_table():
    st = all_states()
    out = ["| Nodo | Estado | v | Depende de | Afecta a |", "|---|---|---|---|---|"]
    for node, titulo, destino in NODES:
        fm = read_fm(node) or {}
        deps = ", ".join(PARENTS[node]) or "(raiz)"
        aff = ", ".join(EDGES.get(node, [])) or "(hoja)"
        marca = " *(anexo)*" if destino == "anexo" else ""
        out.append(f"| `{node}`{marca} | {st[node]} | {fm.get('version','0')} | {deps} | {aff} |")
    return "\n".join(out)


def cmd_status():
    print(status_table())


# ---------------------------------------------------------------- deps

def cmd_deps(node):
    if node not in TITLE:
        sys.exit(f"nodo desconocido: {node}")
    st = all_states()
    arriba = PARENTS[node]
    abajo = [d for d in EDGES.get(node, []) if st[d] == "decidido"]
    print(f"Antes de escribir `{node}`, lee:\n")
    print("  Dependencias (de donde viene):")
    for d in arriba or ["(es raiz)"]:
        print(f"    - {d}" + (f"  [{st[d]}]" if d in st else ""))
    print("\n  Dependientes ya decididos (contra que hay que chequear contradiccion):")
    for d in abajo or ["(ninguno)"]:
        print(f"    - {d}" + (f"  [{st[d]}]" if d in st else ""))
    if node == "03-capabilities":
        print("\n  Regla de retorno: si el sistema de actividades no resulta factible,")
        print("  distintivo y defendible, marca 02-where-to-play-how-to-win como desactualizado.")


# ---------------------------------------------------------------- touch

def cmd_touch(node, apply=False, motivo=""):
    if node not in TITLE:
        sys.exit(f"nodo desconocido: {node}")
    st = all_states()
    afectados = [d for d in EDGES.get(node, []) if st[d] == "decidido"]
    if not afectados:
        print(f"Tocar `{node}` no desactualiza ningun nodo decidido.")
        return
    print(f"Tocar `{node}` desactualiza: " + ", ".join(afectados))
    if not apply:
        print("(usa --apply para escribirlo en el frontmatter)")
        return
    motivo = motivo or f"cambio en {node}"
    for d in afectados:
        p = path(d)
        t = p.read_text(encoding="utf-8")
        t = re.sub(r"^estado:.*$", "estado: desactualizado", t, count=1, flags=re.M)
        t = re.sub(r"^desactualizado_por:.*$", f"desactualizado_por: {motivo}", t,
                   count=1, flags=re.M)
        p.write_text(t, encoding="utf-8")
        print(f"  {d} -> desactualizado")


# ---------------------------------------------------------------- sync

def replace_block(text, name, body):
    open_t, close_t = f"<!-- graph:{name} -->", f"<!-- /graph:{name} -->"
    pat = re.compile(re.escape(open_t) + r".*?" + re.escape(close_t), re.S)
    new = f"{open_t}\n{body}\n{close_t}"
    return pat.sub(lambda _: new, text) if pat.search(text) else text


def pending_list():
    st = all_states()
    faltas = []
    for node, _, destino in NODES:
        if destino != "memo":
            continue
        if st[node] == "vacio":
            faltas.append(f"- `{node}` esta vacio.")
        elif st[node] == "desactualizado":
            fm = read_fm(node) or {}
            faltas.append(f"- `{node}` esta desactualizado: {fm.get('desactualizado_por','')}".rstrip(": "))
        elif st[node] == "borrador":
            faltas.append(f"- `{node}` es borrador, falta decidirlo.")
    return "\n".join(faltas) if faltas else "Nada. Corre la compuerta de `references/memo.md`."


def cmd_sync():
    idx = R("index.md")
    if not idx.exists():
        idx.write_text(index_skeleton(), encoding="utf-8")
    t = idx.read_text(encoding="utf-8")
    t = replace_block(t, "status", status_table())
    t = replace_block(t, "pending", pending_list())
    t = re.sub(r"^\*\*Actualizado:.*$", "", t, flags=re.M)
    idx.write_text(t, encoding="utf-8")

    for node, _, _ in NODES:
        p = path(node)
        if not p.exists():
            continue
        arriba = " · ".join(f"[[{d}]]" for d in PARENTS[node]) or "(raiz)"
        abajo = " · ".join(f"[[{d}]]" for d in EDGES.get(node, [])) or "(hoja)"
        body = (f"<!-- graph:links -->\n---\n\n**Depende de:** {arriba}\n"
                f"**Afecta a:** {abajo}\n<!-- /graph:links -->")
        t = p.read_text(encoding="utf-8")
        t = re.sub(r"\n*<!-- graph:links -->.*?<!-- /graph:links -->\n*", "\n", t, flags=re.S)
        p.write_text(t.rstrip() + "\n\n" + body + "\n", encoding="utf-8")
    print("index.md y los wikilinks de cada nodo, sincronizados.")


# ---------------------------------------------------------------- lint

def cmd_lint():
    st = all_states()
    p = []
    for node, _, destino in NODES:
        if not path(node).exists():
            p.append(f"[falta] {node}: el archivo no existe.")
            continue
        if st[node] == "desactualizado":
            fm = read_fm(node) or {}
            p.append(f"[stale] {node}: {fm.get('desactualizado_por','sin motivo registrado')}")
        if destino == "memo" and st[node] == "vacio":
            p.append(f"[vacio] {node}: nodo del memo sin contenido.")
        body = FM.sub("", path(node).read_text(encoding="utf-8"))
        body = re.sub(r"<!-- graph:links -->.*?<!-- /graph:links -->", "", body, flags=re.S)
        cuerpo = re.sub(r"^#.*$", "", body, flags=re.M).strip()
        if st[node] in ("borrador", "decidido") and len(cuerpo) < 80:
            p.append(f"[hueco] {node}: estado {st[node]} pero casi sin contenido.")
        if st[node] == "vacio" and len(cuerpo) > 80:
            p.append(f"[huerfano] {node}: tiene contenido pero sigue en vacio.")

    sup = path("06-supuestos-vivos")
    if sup.exists() and st["06-supuestos-vivos"] != "vacio":
        txt = sup.read_text(encoding="utf-8").lower()
        for campo in ("prueba", "responsable", "fecha"):
            if campo not in txt:
                p.append(f"[falsable] 06-supuestos-vivos: ningun supuesto declara {campo}.")

    inbox = R(INBOX)
    if inbox.exists():
        files = [f for f in inbox.iterdir() if f.is_file() and not f.name.startswith(".")]
        if files:
            p.append(f"[inbox] {len(files)} archivo(s) sin procesar: "
                     + ", ".join(f.name for f in files))

    log = R("log.md")
    if log.exists():
        n = len(log_entries(log.read_text(encoding="utf-8"))[1])
        if n > LOG_MAX:
            p.append(f"[log] {n} entradas en log.md (umbral {LOG_MAX}): corre `archive`.")

    idx = R("index.md")
    if idx.exists():
        m = re.search(r"## Alertas abiertas\n(.*?)(?=\n## |\Z)", idx.read_text(encoding="utf-8"), re.S)
        if m and m.group(1).strip() and not m.group(1).strip().lower().startswith("ninguna"):
            p.append("[alerta] hay alertas abiertas en index.md: bloquean la compilacion.")

    print("\n".join(p) if p else "Sin hallazgos. El grafo esta sano.")


# ---------------------------------------------------------------- archive

def log_entries(text):
    """Devuelve (cabecera, [entradas]). Una entrada es un bloque que abre con ## [."""
    marks = [m.start() for m in ENTRY.finditer(text)]
    if not marks:
        return text, []
    head = text[:marks[0]]
    bounds = marks + [len(text)]
    return head, [text[bounds[i]:bounds[i + 1]] for i in range(len(marks))]


def cmd_archive(keep=None):
    log = R("log.md")
    if not log.exists():
        sys.exit("no hay log.md")
    head, entries = log_entries(log.read_text(encoding="utf-8"))
    if not entries:
        print("log.md no tiene entradas todavia.")
        return

    if keep is None:
        cortes = [i for i, e in enumerate(entries) if re.match(r"^## \[[^\]]*\]\s*memo\b", e)]
        if cortes:
            corte = cortes[-1] + 1
        else:
            corte = max(0, len(entries) - 50)
            print("Sin entrada `memo` para cortar: archivo todo menos las ultimas 50.")
    else:
        corte = max(0, len(entries) - int(keep))

    if corte == 0:
        print(f"Nada que archivar: {len(entries)} entradas, todas dentro del ciclo vigente.")
        return

    viejas, vivas = entries[:corte], entries[corte:]
    n = 1
    while R(f"log-archivo-{n:02d}.md").exists():
        n += 1
    arch = R(f"log-archivo-{n:02d}.md")
    arch.write_text(f"# Bitacora archivada {n:02d}\n\n"
                    f"Entradas anteriores al corte. Cronologica, no se reordena.\n\n"
                    + "".join(viejas), encoding="utf-8")
    log.write_text(head.rstrip() + f"\n\nEntradas anteriores en [[{arch.stem}]].\n\n"
                   + "".join(vivas), encoding="utf-8")
    print(f"{len(viejas)} entradas archivadas en {arch.name}. Quedan {len(vivas)} en log.md.")


# ---------------------------------------------------------------- main

def main():
    global ROOT
    argv = sys.argv[1:]
    if "--root" in argv:
        i = argv.index("--root")
        ROOT = pathlib.Path(argv[i + 1]).expanduser()
        del argv[i:i + 2]
        if not ROOT.is_dir():
            sys.exit(f"--root no es un directorio: {ROOT}")
    if not argv:
        sys.exit(__doc__)
    cmd, args = argv[0], argv[1:]
    if cmd == "init":
        pos = [a for a in args if not a.startswith("--")]
        cmd_init(*(pos + ["", ""])[:2])
    elif cmd == "status":
        cmd_status()
    elif cmd == "deps":
        cmd_deps(args[0])
    elif cmd == "touch":
        cmd_touch(args[0], apply="--apply" in args,
                  motivo=next((a for a in args[1:] if not a.startswith("--")), ""))
    elif cmd == "sync":
        cmd_sync()
    elif cmd == "lint":
        cmd_lint()
    elif cmd == "archive":
        k = args[args.index("--keep") + 1] if "--keep" in args else None
        cmd_archive(k)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
