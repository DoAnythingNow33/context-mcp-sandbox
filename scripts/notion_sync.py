#!/usr/bin/env python3
"""
notion_sync.py — Notion client-portal sync

Projects client entity state from the vault (source of truth) into a Notion
client portal. One-way: vault -> Notion. Idempotent upsert keyed on client slug.

Usage:
    python scripts/notion_sync.py --client growify
    python scripts/notion_sync.py --all

Requirements:
    pip install notion-client
    env vars: NOTION_TOKEN, NOTION_PORTAL_DB_ID

Never commit NOTION_TOKEN. Keep it in a local .env or shell profile.
See docs/DEFERRED.md for first-time setup steps.
"""

import os
import re
import sys
import argparse
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
PEOPLE_DIR = VAULT_ROOT / "entities" / "people"

# ---------------------------------------------------------------------------
# Property map — vault frontmatter fields -> Notion database property names.
#
# *** Dan: confirm these names against your actual portal DB schema ***
# Open your Notion portal DB -> ... -> Properties to see the exact names.
# Rename the right-hand strings here to match. The left-hand keys are fixed.
# ---------------------------------------------------------------------------
PROPERTY_MAP = {
    "slug":           "Slug",           # Rich text — stable match key (don't rename in Notion)
    "name":           "Name",           # Title property
    "current_state":  "Status",         # Rich text — one-paragraph state summary
    "current_focus":  "Current Focus",  # Rich text — bullet list of focus items
    "next_actions":   "Next Actions",   # Rich text — bullet list of actions
    "open_questions": "Open Questions", # Rich text — bullet list
    "tensions":       "Tensions",       # Rich text — bullet list
    "last_updated":   "Last Updated",   # Date property
    "last_meeting":   "Last Meeting",   # Rich text — most-recent meeting wikilink stem
}

# Matches [[some/path/slug]] or [[slug]]
WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")


# ---------------------------------------------------------------------------
# Frontmatter parser — pure stdlib, mirrors generate_digest.py / validate_freshness.py
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter key/value pairs. Lists become Python lists."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm: dict = {}
    lines = match.group(1).splitlines()
    current_key = None
    current_list: list[str] = []

    for line in lines:
        # List item under current key (indented "  - value")
        if re.match(r"^\s{2,}- ", line):
            val = re.sub(r'^\s*-\s*"?|"?\s*$', "", line).strip().strip('"')
            if val:
                current_list.append(val)
            continue

        # New key: value line
        m = re.match(r'^(\w[\w_]*):\s*(.*)', line)
        if m:
            # Flush previous list
            if current_key and current_list:
                fm[current_key] = current_list
                current_list = []
            key = m.group(1)
            value = m.group(2).strip().strip('"')
            if value:
                fm[key] = value
            current_key = key
        else:
            # Continuation of a quoted / multi-line scalar
            if current_key and current_key in fm and isinstance(fm[current_key], str):
                fm[current_key] += " " + line.strip().strip('"')

    if current_key and current_list:
        fm[current_key] = current_list

    return fm


def extract_last_meeting(content: str) -> str:
    """Return the most-recent (last listed) meeting wikilink stem from the ## Meetings section."""
    in_meetings = False
    links: list[str] = []
    for line in content.splitlines():
        if re.match(r"^##\s+Meetings\b", line, re.IGNORECASE):
            in_meetings = True
            continue
        if in_meetings:
            if re.match(r"^##\s+", line):
                break
            for m in WIKILINK_RE.finditer(line):
                links.append(Path(m.group(1).strip()).stem)
    return links[-1] if links else ""


# ---------------------------------------------------------------------------
# load_client
# ---------------------------------------------------------------------------

def load_client(slug: str) -> dict:
    """
    Read entities/people/<slug>.md and return a normalised data dict with keys:
        slug, name, current_state, current_focus, next_actions,
        open_questions, tensions, last_updated, last_meeting
    Raises FileNotFoundError if the file doesn't exist.
    Raises ValueError if the file has no valid snapshot frontmatter.
    """
    path = PEOPLE_DIR / f"{slug}.md"
    if not path.exists():
        raise FileNotFoundError(f"No entity file at {path}")

    content = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)

    if not fm:
        raise ValueError(f"{path}: no frontmatter found")
    if fm.get("type") != "snapshot":
        raise ValueError(f"{path}: type is '{fm.get('type')}', expected 'snapshot'")

    def _as_list(val) -> list[str]:
        if not val:
            return []
        if isinstance(val, list):
            return val
        return [val]

    return {
        "slug":           slug,
        "name":           fm.get("entity", slug),
        "current_state":  fm.get("current_state", ""),
        "current_focus":  _as_list(fm.get("current_focus")),
        "next_actions":   _as_list(fm.get("next_actions")),
        "open_questions": _as_list(fm.get("open_questions")),
        "tensions":       _as_list(fm.get("tensions")),
        "last_updated":   fm.get("last_updated", ""),
        "last_meeting":   extract_last_meeting(content),
    }


# ---------------------------------------------------------------------------
# Notion helpers — lazy import
# ---------------------------------------------------------------------------

def _get_notion_client(token: str):
    """Import notion_client lazily so the script is still usable if it's missing."""
    try:
        from notion_client import Client  # type: ignore
    except ImportError:
        print("ERROR: notion-client library not installed.")
        print("       Run: pip install notion-client")
        print("       (or: pip install -r scripts/requirements.txt)")
        sys.exit(1)
    return Client(auth=token)


def _rich_text(text: str) -> list[dict]:
    """Wrap a plain string in a Notion rich_text array."""
    return [{"type": "text", "text": {"content": text}}]


def _bullets_rich_text(items: list[str]) -> list[dict]:
    """Join a list of strings as newline-separated bullet lines in a rich_text block."""
    if not items:
        return _rich_text("")
    joined = "\n".join(f"• {item}" for item in items)
    # Notion rich_text content max is 2000 chars — truncate gracefully
    if len(joined) > 2000:
        joined = joined[:1997] + "…"
    return _rich_text(joined)


def _build_properties(data: dict) -> dict:
    """
    Build the Notion properties payload from the client data dict.
    Uses PROPERTY_MAP to resolve property names.
    """
    pm = PROPERTY_MAP
    props: dict = {}

    # Title (Name)
    props[pm["name"]] = {
        "title": _rich_text(data["name"])
    }

    # Slug — rich_text, stable match key
    props[pm["slug"]] = {
        "rich_text": _rich_text(data["slug"])
    }

    # current_state — rich_text
    if data.get("current_state"):
        state = data["current_state"]
        if len(state) > 2000:
            state = state[:1997] + "…"
        props[pm["current_state"]] = {
            "rich_text": _rich_text(state)
        }

    # List fields — rich_text bullets
    for field in ("current_focus", "next_actions", "open_questions", "tensions"):
        items = data.get(field, [])
        if items:
            props[pm[field]] = {
                "rich_text": _bullets_rich_text(items)
            }

    # last_updated — date (ISO YYYY-MM-DD)
    if data.get("last_updated"):
        props[pm["last_updated"]] = {
            "date": {"start": data["last_updated"]}
        }

    # last_meeting — rich_text
    if data.get("last_meeting"):
        props[pm["last_meeting"]] = {
            "rich_text": _rich_text(data["last_meeting"])
        }

    return props


# ---------------------------------------------------------------------------
# find_page / upsert_client
# ---------------------------------------------------------------------------

def find_page(notion, db_id: str, slug: str) -> dict | None:
    """
    Query the Notion DB for a page where the Slug property equals slug.
    Returns the first matching page dict, or None.
    """
    slug_prop = PROPERTY_MAP["slug"]
    try:
        response = notion.databases.query(
            database_id=db_id,
            filter={
                "property": slug_prop,
                "rich_text": {"equals": slug},
            },
        )
    except Exception as exc:
        raise RuntimeError(f"Notion query failed for slug='{slug}': {exc}") from exc

    results = response.get("results", [])
    return results[0] if results else None


def upsert_client(slug: str, notion, db_id: str) -> tuple[str, str]:
    """
    Create or update the client's Notion portal page.
    Returns (action, page_url) where action is 'created' or 'updated'.
    """
    data = load_client(slug)
    props = _build_properties(data)

    existing = find_page(notion, db_id, slug)

    if existing is None:
        # Create new page
        page = notion.pages.create(
            parent={"database_id": db_id},
            properties=props,
        )
        action = "created"
    else:
        # Update existing page
        page = notion.pages.update(
            page_id=existing["id"],
            properties=props,
        )
        action = "updated"

    url = page.get("url", "")
    return action, url


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync client entity state from vault to Notion portal (one-way).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/notion_sync.py --client growify\n"
            "  python scripts/notion_sync.py --all\n\n"
            "Required env vars:\n"
            "  NOTION_TOKEN         — Notion internal integration token\n"
            "  NOTION_PORTAL_DB_ID  — ID of the client portal database\n\n"
            "See docs/DEFERRED.md for first-time setup."
        ),
    )
    parser.add_argument("--client", metavar="SLUG",
                        help="sync a single client by slug (e.g. growify)")
    parser.add_argument("--all", action="store_true",
                        help="sync every entities/people/*.md with type: snapshot")
    args = parser.parse_args()

    if not args.client and not args.all:
        parser.print_help()
        return 1

    # Config validation
    token = os.environ.get("NOTION_TOKEN", "")
    db_id = os.environ.get("NOTION_PORTAL_DB_ID", "")
    config_ok = True

    if not token:
        print("ERROR: NOTION_TOKEN is not set.")
        print("       Create a Notion internal integration at https://www.notion.so/my-integrations")
        print("       then export NOTION_TOKEN=secret_... in your shell profile or .env file.")
        print("       See docs/DEFERRED.md § 'Notion client-portal sync' for full setup steps.")
        config_ok = False

    if not db_id:
        print("ERROR: NOTION_PORTAL_DB_ID is not set.")
        print("       Open your Notion client portal DB -> Share -> Copy link.")
        print("       The 32-char hex ID comes after the last slash before the '?'.")
        print("       Then: export NOTION_PORTAL_DB_ID=<that-id>")
        print("       See docs/DEFERRED.md § 'Notion client-portal sync' for full setup steps.")
        config_ok = False

    if not config_ok:
        return 1

    # Lazy-load the Notion client (exits 1 with install hint if lib missing)
    notion = _get_notion_client(token)

    # Collect slugs to sync
    if args.client:
        slugs = [args.client]
    else:
        slugs = []
        for path in sorted(PEOPLE_DIR.glob("*.md")):
            if path.name.startswith("_"):
                continue
            try:
                content = path.read_text(encoding="utf-8")
                fm = parse_frontmatter(content)
                if fm.get("type") == "snapshot":
                    slugs.append(path.stem)
            except Exception:
                pass

    if not slugs:
        print("No client snapshots found to sync.")
        return 0

    # Sync each client
    exit_code = 0
    for slug in slugs:
        try:
            action, url = upsert_client(slug, notion, db_id)
            url_str = f"  {url}" if url else ""
            print(f"  {action.upper():<8}  {slug}{url_str}")
        except FileNotFoundError as exc:
            print(f"  SKIP     {slug}  ({exc})")
        except ValueError as exc:
            print(f"  SKIP     {slug}  ({exc})")
        except Exception as exc:
            print(f"  ERROR    {slug}  ({exc})")
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
