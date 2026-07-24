#!/usr/bin/env python3
"""Deterministic validator for a client context bundle (OKF v0.1).

Usage:
    python3 validate_bundle.py <bundle-dir> [--template <template-bundle-dir>]

Checks (ERRORS fail the run; WARNINGS are listed for human judgment):
  E1  Every non-reserved .md has YAML frontmatter that parses, with a
      non-empty `type` and a `status` in {scaffold, partial, active}.
  E2  index.md files carry no frontmatter (root index may carry okf_version
      only). log.md exists at the root.
  E3  Every folder's index.md links every .md file in that folder (except
      itself), and links no file that doesn't exist.
  E4  Internal links resolve: /path.md (bundle-relative), relative links,
      and directory links (resolve to <dir>/index.md).
  E5  No unresolved template tokens ({{...}}).
  E6  With --template: AGENTS.md is byte-identical to the template's at the
      same template_version (version drift is W4, not an error).
  E7  Multi-entity bundles: links to /d-books/<file>.md without an entity
      subfolder are errors.
  W1  Possible credential values: password/token/secret assignments, or
      unbroken digit runs of 9+ (bank/routing shape) outside allowlisted
      ID fields.
  W2  Live-state property names appearing as stored schema_properties
      (bank_feed_connection_status, cleanup_progress,
      open_uncategorized_items).
  W3  Concept files missing schema_properties (informational).
  W4  AGENTS.md template_version drift vs. the skill template.

Requires PyYAML. `status` is required on every concept file.

Prints a status-count summary (active/partial/scaffold) on success.
"""
import os, re, sys

RESERVED = {"index.md", "log.md"}
STATUSES = {"scaffold", "partial", "active"}
LIVE_STATE = {"bank_feed_connection_status", "cleanup_progress", "open_uncategorized_items"}
ID_ALLOWLIST = {"workspace-locations.md", "qbo-configuration.md"}

def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    try:
        import yaml
    except ImportError:
        print("ERROR   validate_bundle.py requires PyYAML (pip install pyyaml)")
        sys.exit(2)
    try:
        return yaml.safe_load(m.group(1)) or {}, text[m.end():]
    except Exception:
        return "INVALID", text[m.end():]

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    root = os.path.abspath(sys.argv[1])
    template = None
    if "--template" in sys.argv:
        template = os.path.abspath(sys.argv[sys.argv.index("--template") + 1])

    errors, warnings = [], []
    counts = {"scaffold": 0, "partial": 0, "active": 0}
    all_md = {}
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not d.startswith(".")]
        for fn in fns:
            if fn.endswith(".md"):
                rel = os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, "/")
                all_md[rel] = open(os.path.join(dp, fn)).read()

    if "log.md" not in all_md:
        errors.append("E2 | log.md missing at bundle root")

    for rel, text in sorted(all_md.items()):
        base = os.path.basename(rel)
        fm, body = parse_fm(text)
        if base in RESERVED:
            if base == "index.md":
                if fm not in (None,) and rel != "index.md":
                    errors.append(f"E2 | {rel} | non-root index.md must not have frontmatter")
                if rel == "index.md" and fm not in (None,) and set(fm or {}) - {"okf_version"}:
                    errors.append(f"E2 | {rel} | root index frontmatter may carry okf_version only")
        else:
            if fm is None:
                errors.append(f"E1 | {rel} | missing frontmatter")
            elif fm == "INVALID":
                errors.append(f"E1 | {rel} | frontmatter is not valid YAML")
            else:
                if not fm.get("type"):
                    errors.append(f"E1 | {rel} | missing/empty `type`")
                st = fm.get("status")
                if st is None:
                    errors.append(f"E1 | {rel} | missing `status` (required: scaffold/partial/active)")
                elif st not in STATUSES:
                    errors.append(f"E1 | {rel} | status '{st}' not in {sorted(STATUSES)}")
                else:
                    counts[st] += 1
                props = fm.get("schema_properties")
                if props:
                    plist = props if isinstance(props, list) else re.findall(r"[\w-]+", str(props))
                    hit = LIVE_STATE.intersection(plist)
                    if hit:
                        warnings.append(f"W2 | {rel} | stores live-state property: {sorted(hit)}")
                elif "/" in rel:
                    warnings.append(f"W3 | {rel} | concept file without schema_properties")

        # E5 tokens
        for tok in re.findall(r"\{\{[^}]+\}\}", text):
            errors.append(f"E5 | {rel} | unresolved template token {tok}")

        # E4 links
        curdir = os.path.dirname(rel)
        for txt, href in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", text):
            if re.match(r"^(https?:|mailto:|#)", href):
                continue
            path = href[1:] if href.startswith("/") else os.path.normpath(os.path.join(curdir, href)).replace(os.sep, "/")
            if path.endswith("/"):
                path += "index.md"
            if not path.endswith(".md"):
                path += "/index.md" if (path and path + "/index.md" in all_md) else ".md"
            if path not in all_md:
                errors.append(f"E4 | {rel} | broken link -> {href}")

        # W1 secrets
        for i, ln in enumerate(text.split("\n"), 1):
            if re.search(r"(?i)(password|passwd|secret|api[_ ]?key|token)\s*[:=]\s*\S{6,}", ln):
                warnings.append(f"W1 | {rel}:{i} | possible credential assignment")
            if base not in ID_ALLOWLIST and re.search(r"(?<!\d)\d{9,}(?!\d)", ln):
                warnings.append(f"W1 | {rel}:{i} | unbroken 9+ digit run (account/routing shape?)")

    # E3 index coverage
    folders = {}
    for rel in all_md:
        folders.setdefault(os.path.dirname(rel), []).append(rel)
    for folder, rels in folders.items():
        idx = (folder + "/" if folder else "") + "index.md"
        if idx not in all_md:
            if folder:
                errors.append(f"E3 | {folder}/ | missing index.md")
            continue
        idx_text = all_md[idx]
        linked = set()
        for _, href in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", idx_text):
            if re.match(r"^(https?:|mailto:|#)", href):
                continue
            p = href[1:] if href.startswith("/") else os.path.normpath(os.path.join(folder, href)).replace(os.sep, "/")
            if p.endswith("/"):
                p += "index.md"
            linked.add(p)
        for rel in rels:
            if rel == idx:
                continue
            if rel not in linked:
                errors.append(f"E3 | {idx} | does not list {rel}")

    # E7 multi-entity: unscoped d-books links are errors when entity subfolders exist
    entity_dirs = {os.path.dirname(r).split("/")[1] for r in all_md
                   if r.startswith("d-books/") and r.count("/") >= 2}
    if entity_dirs:
        flat_books = re.compile(r"\]\(/d-books/([^/)]+\.md)\)")
        for rel, text in all_md.items():
            for fname in flat_books.findall(text):
                if fname == "index.md":
                    continue  # the all-entities directory link is the prescribed form
                errors.append(f"E7 | {rel} | unscoped d-books link /d-books/{fname} in a multi-entity bundle")

    # E6 AGENTS.md vs template
    if template:
        t = os.path.join(template, "AGENTS.md")
        b = os.path.join(root, "AGENTS.md")
        if not os.path.exists(b):
            errors.append("E6 | AGENTS.md missing from bundle")
        elif os.path.exists(t):
            tt, bt = open(t).read(), open(b).read()
            def ver(x):
                m2 = re.search(r'template_version:\s*"?([\d.]+)"?', x)
                return m2.group(1) if m2 else None
            tv, bv = ver(tt), ver(bt)
            if tv and bv and tv != bv:
                warnings.append(f"W4 | AGENTS.md | template_version {bv} differs from skill template {tv} — version drift; migrate via a dedicated update, never silently")
            elif tt != bt:
                errors.append("E6 | AGENTS.md differs from the firm template at the same template_version (must be unmodified)")

    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARN   ", w)
    print(f"\nStatus counts: {counts['active']} active, {counts['partial']} partial, {counts['scaffold']} scaffold; {len(all_md)} files.")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s).")
        sys.exit(1)
    print(f"PASS: 0 errors, {len(warnings)} warning(s) for human review.")

if __name__ == "__main__":
    main()
