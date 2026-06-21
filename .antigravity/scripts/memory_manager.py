#!/usr/bin/env python3
"""
memory_manager.py — Antigravity 4-Level Memory System
======================================================
Manages persistent memory for AI agents across four levels:
  Level 1: Chat (in-context, no persistence needed)
  Level 2: Session Log  → .antigravity/memory/SESSION_LOG.md
  Level 3: Facts (DNA)  → .antigravity/memory/FACTS.md
  Level 4: Obsidian Wiki → configurable vault path

Usage:
  python3 memory_manager.py log   "<activity>"
  python3 memory_manager.py fact  "<fact>"
  python3 memory_manager.py wiki  "<topic>" "<markdown_content>"
  python3 memory_manager.py read  [log|facts|all]
  python3 memory_manager.py status
  python3 memory_manager.py init
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from textwrap import dedent


# ─────────────────────────────────────────────
# Path Resolution
# ─────────────────────────────────────────────

def resolve_paths(script_path: Path) -> dict:
    """
    Resolves all relevant paths based on where the script is called from.

    Priority order:
      1. If the script lives inside <project>/.antigravity/scripts/ → use that project root.
      2. If CWD differs from master root → use CWD as the project root
         (works even before .antigravity/ exists, e.g. on first `init`).
      3. Fallback: use master project root.
    """
    master_root = Path.home() / "Documents/_PROJEKTE/05_Antigravity"
    script_dir  = script_path.parent.resolve()
    cwd         = Path.cwd().resolve()

    if script_dir.parts[-2:] == (".antigravity", "scripts"):
        # Script is already deployed inside a project
        project_root = script_dir.parent.parent
    elif cwd != master_root:
        # Called from a different project directory (e.g. during Boot-Sequenz)
        project_root = cwd
    else:
        project_root = master_root

    memory_dir = project_root / ".antigravity" / "memory"

    # Obsidian vault: prefer environment variable, then master location
    obsidian_env = os.environ.get("ANTIGRAVITY_OBSIDIAN_VAULT")
    if obsidian_env:
        wiki_dir = Path(obsidian_env) / "Wiki" / "Projekte" / project_root.name
    else:
        wiki_dir = master_root / "00_Obsidian" / "Antigravity-AIGENT" / "Wiki" / "Projekte" / project_root.name

    return {
        "project_root": project_root,
        "memory_dir":   memory_dir,
        "session_log":  memory_dir / "SESSION_LOG.md",
        "facts_file":   memory_dir / "FACTS.md",
        "wiki_dir":     wiki_dir,
        "scripts_dir":  project_root / ".antigravity" / "scripts",
    }


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def ensure_dir(path: Path):
    """Create directory (and parents) if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)


def ensure_file_with_header(path: Path, header: str):
    """Create a file with a header if it does not exist yet."""
    if not path.exists():
        path.write_text(header + "\n", encoding="utf-8")


def now_ts(fmt: str = "%Y-%m-%d %H:%M") -> str:
    return datetime.now().strftime(fmt)


def now_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


# ─────────────────────────────────────────────
# Level 2 — Session Log
# ─────────────────────────────────────────────

def cmd_log(paths: dict, activity: str):
    """
    Level 2: Append a timestamped activity entry to SESSION_LOG.md.
    Entries are grouped by date.
    """
    ensure_dir(paths["memory_dir"])
    log_path = paths["session_log"]

    header = dedent(f"""\
        # 📋 Session Log — {paths['project_root'].name}
        > Automatically managed by memory_manager.py
        > Do not edit manually.
    """)
    ensure_file_with_header(log_path, header)

    content = log_path.read_text(encoding="utf-8")
    date_header = f"\n## {now_date()}\n"

    # Add date section if not present for today
    if date_header.strip() not in content:
        with log_path.open("a", encoding="utf-8") as f:
            f.write(date_header)

    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"- `{now_ts()}` {activity}\n")

    print(f"✅ [L2 Log] {activity}")


# ─────────────────────────────────────────────
# Level 3 — Long-Term Facts (Setup-DNA)
# ─────────────────────────────────────────────

def cmd_fact(paths: dict, fact: str):
    """
    Level 3: Append a timestamped fact to FACTS.md.
    Facts represent stable project configuration/architecture decisions.
    """
    ensure_dir(paths["memory_dir"])
    facts_path = paths["facts_file"]

    header = dedent(f"""\
        # 🧬 Facts / Setup-DNA — {paths['project_root'].name}
        > Fundamental project facts, stack decisions, and architecture notes.
        > Automatically managed by memory_manager.py
    """)
    ensure_file_with_header(facts_path, header)

    with facts_path.open("a", encoding="utf-8") as f:
        f.write(f"- `{now_date()}` {fact}\n")

    print(f"✅ [L3 Fact] {fact}")


# ─────────────────────────────────────────────
# Level 4 — Obsidian Wiki
# ─────────────────────────────────────────────

def cmd_wiki(paths: dict, topic: str, content: str):
    """
    Level 4: Create or update a markdown page in the Obsidian wiki.
    Each topic maps to a single .md file. New content is appended as a dated update.
    """
    wiki_dir = paths["wiki_dir"]
    ensure_dir(wiki_dir)

    safe_filename = topic.replace("/", "-").replace(" ", "_") + ".md"
    wiki_path = wiki_dir / safe_filename

    if not wiki_path.exists():
        initial = dedent(f"""\
            # {topic}

            > Created: {now_date()}
            > Project: {paths['project_root'].name}

            ---

            {content}
        """)
        wiki_path.write_text(initial, encoding="utf-8")
        print(f"✅ [L4 Wiki] Created: {wiki_path}")
    else:
        update = dedent(f"""\
 

            ## Update {now_ts()}

            {content}
        """)
        with wiki_path.open("a", encoding="utf-8") as f:
            f.write(update)
        print(f"✅ [L4 Wiki] Updated: {wiki_path}")


# ─────────────────────────────────────────────
# Read / Status Commands
# ─────────────────────────────────────────────

def cmd_read(paths: dict, target: str = "all"):
    """Print the contents of log, facts, or both to stdout."""
    files = {
        "log":   ("📋 SESSION LOG", paths["session_log"]),
        "facts": ("🧬 FACTS",       paths["facts_file"]),
    }

    targets = ["log", "facts"] if target == "all" else [target]
    for key in targets:
        if key not in files:
            print(f"Unknown target: {key}. Use log|facts|all.")
            continue
        label, path = files[key]
        print(f"\n{'─'*60}")
        print(f"  {label}")
        print(f"{'─'*60}")
        if path.exists():
            print(path.read_text(encoding="utf-8"))
        else:
            print("  (no entries yet)")


def cmd_status(paths: dict):
    """Print a summary of the current memory system state."""
    print(dedent(f"""
    ╔══════════════════════════════════════════════════
    ║  🧠 Antigravity Memory Status
    ╠══════════════════════════════════════════════════
    ║  Project Root : {paths['project_root']}
    ║  Memory Dir   : {paths['memory_dir']}
    ║  Wiki Dir     : {paths['wiki_dir']}
    ╠══════════════════════════════════════════════════"""))

    for label, path_key in [("Session Log (L2)", "session_log"), ("Facts (L3)", "facts_file")]:
        p = paths[path_key]
        if p.exists():
            lines = p.read_text(encoding="utf-8").splitlines()
            entry_count = sum(1 for l in lines if l.startswith("- "))
            print(f"    ✅ {label:<22} {entry_count} entries  →  {p.name}")
        else:
            print(f"    ⬜ {label:<22} not created yet")

    wiki_dir = paths["wiki_dir"]
    if wiki_dir.exists():
        wiki_pages = list(wiki_dir.glob("*.md"))
        print(f"    ✅ Wiki (L4)              {len(wiki_pages)} pages  →  {wiki_dir}")
    else:
        print(f"    ⬜ Wiki (L4)              not created yet")
    print("    ╚══════════════════════════════════════════════════\n")


def cmd_init(paths: dict):
    """
    Ensure all memory directories and skeleton files exist.
    Safe to run multiple times (idempotent).
    """
    ensure_dir(paths["memory_dir"])
    ensure_dir(paths["wiki_dir"])

    # Skeleton SESSION_LOG
    if not paths["session_log"].exists():
        cmd_log(paths, "Memory system initialized.")
    # Skeleton FACTS
    if not paths["facts_file"].exists():
        cmd_fact(paths, f"Project initialized: {paths['project_root'].name}")

    print(f"✅ Memory infrastructure ready at {paths['memory_dir']}")


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────

def main():
    paths = resolve_paths(Path(__file__))

    parser = argparse.ArgumentParser(
        description="Antigravity 4-Level Memory Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
            Examples:
              python3 memory_manager.py log   "Responsive layout built with Tailwind"
              python3 memory_manager.py fact  "Stack: Next.js 14, TypeScript, Tailwind CSS"
              python3 memory_manager.py wiki  "Routing-Konzept" "## Next.js\\nApp Router..."
              python3 memory_manager.py read  all
              python3 memory_manager.py status
              python3 memory_manager.py init
        """)
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # log
    p_log = subparsers.add_parser("log", help="Level 2: Append activity to session log")
    p_log.add_argument("activity", help="Activity description")

    # fact
    p_fact = subparsers.add_parser("fact", help="Level 3: Store a long-term project fact")
    p_fact.add_argument("fact", help="Fact to store")

    # wiki
    p_wiki = subparsers.add_parser("wiki", help="Level 4: Create/update Obsidian wiki page")
    p_wiki.add_argument("topic",   help="Wiki page title / topic")
    p_wiki.add_argument("content", help="Markdown content to write")

    # read
    p_read = subparsers.add_parser("read", help="Read log, facts, or all")
    p_read.add_argument("target", nargs="?", default="all",
                        choices=["log", "facts", "all"], help="What to read")

    # status
    subparsers.add_parser("status", help="Show memory system status")

    # init
    subparsers.add_parser("init", help="Initialize memory infrastructure (idempotent)")

    args = parser.parse_args()

    try:
        if args.command == "log":
            cmd_log(paths, args.activity)
        elif args.command == "fact":
            cmd_fact(paths, args.fact)
        elif args.command == "wiki":
            cmd_wiki(paths, args.topic, args.content)
        elif args.command == "read":
            cmd_read(paths, args.target)
        elif args.command == "status":
            cmd_status(paths)
        elif args.command == "init":
            cmd_init(paths)
    except PermissionError as e:
        print(f"❌ Permission denied: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
