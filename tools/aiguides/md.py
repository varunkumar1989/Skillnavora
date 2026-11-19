"""Small markup helpers shared by the three guides. Each returns an HTML string that renders the same
on the website, in the PDF and in the interactive artifact (all three load guide.css-style rules)."""
import html, json, os

E = lambda s: html.escape(str(s), quote=True)
HERE = os.path.dirname(os.path.abspath(__file__))
_GIT = None


def git_out(key):
    """Real terminal output captured by git_capture.py."""
    global _GIT
    if _GIT is None:
        _GIT = json.load(open(os.path.join(HERE, "git_outputs.json")))
    return _GIT[key]


def P(*parts):
    """Paragraphs. Text may contain simple inline HTML written by us (<b>, <code>, <a>)."""
    return "".join(f"<p>{p}</p>" for p in parts)


def UL(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def OL(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def CODE(text, cap="", lang=""):
    c = f'<div class="g-cap">{E(cap)}</div>' if cap else ""
    return f'{c}<pre class="g-code" data-lang="{E(lang)}"><code>{E(text.strip())}</code></pre>'


def TERM(key, cap="Real terminal output (captured when this guide was built)"):
    return f'<div class="g-cap">{E(cap)}</div><pre class="g-term"><code>{E(git_out(key))}</code></pre>'


def TABLE(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="g-tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def NOTE(text, kind="tip", title=""):
    t = {"tip": "Tip", "warn": "Careful", "info": "Good to know", "do": "Try it"}.get(kind, "Note") if not title else title
    return f'<div class="g-note g-{kind}"><b>{E(t)}.</b> {text}</div>'


def STEPS(items):
    """Numbered how-to steps with bold menu names already in the text."""
    return '<ol class="g-steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def MENU(*parts):
    """A menu path such as Customize > Connectors, shown consistently."""
    return '<span class="g-menu">' + " &rsaquo; ".join(E(p) for p in parts) + "</span>"


def K(s):
    return f"<code>{E(s)}</code>"
