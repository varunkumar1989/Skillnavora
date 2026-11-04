"""Helper to deepen an existing course dict: append deep-dive HTML to existing classes, add classes, Q&A, glossary and cheat-sheet rows."""
RANK = {"basic": 0, "intermediate": 1, "advanced": 2}

def extend(C, deep=None, new=None, qa=None, glossary=None, cheat=None, links=None, templates=None):
    cls = [list(c) for c in C["classes"]]
    for i, html in (deep or {}).items():
        cls[i][3] = cls[i][3] + html
    for n in (new or []):
        cls.append(list(n))
    cls.sort(key=lambda c: RANK[c[0]])          # stable: keeps original order inside a level
    cls = [c for c in cls if 'project' not in c[1].lower()] + [c for c in cls if 'project' in c[1].lower()]   # final-project classes stay last
    C["classes"] = [tuple(c) for c in cls]
    C["qa"] = list(C["qa"]) + list(qa or [])
    C["glossary"] = list(C["glossary"]) + list(glossary or [])
    C["cheat"] = list(C["cheat"]) + list(cheat or [])
    C["links"] = list(C["links"]) + list(links or [])
    if templates: C["templates_html"] = C["templates_html"] + templates
    return C
