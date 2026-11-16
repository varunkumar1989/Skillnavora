"""Original illustrations for the Claude and AI coding guide (claude-free-setups.html).
Drawn for SkillNavora (not taken from any video). Run: python3 tools/cf_illustrations.py  -> writes assets/cf/*.svg"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "cf")

PAL = dict(ink="#0d1630", mu="#55607a", line="#d9dfeb", brand="#6c4cf5", soft="#ece8ff",
           green="#16a34a", greensoft="#dcfce7", amber="#d97706", amsoft="#fef3c7", bg="#ffffff")
FONT = "font-family='Inter,Arial,sans-serif'"


def svg(w, h, body, title):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' role='img' aria-label='{title}'>"
            f"<rect width='{w}' height='{h}' rx='18' fill='{PAL['bg']}' stroke='{PAL['line']}'/>{body}</svg>")


def t(x, y, s, size=16, weight=600, fill=None, anchor="start"):
    return f"<text x='{x}' y='{y}' {FONT} font-size='{size}' font-weight='{weight}' fill='{fill or PAL['ink']}' text-anchor='{anchor}'>{s}</text>"


def box(x, y, w, h, fill, stroke=None, r=14):
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{fill}' stroke='{stroke or fill}' stroke-width='2'/>"


def arrow(x1, y1, x2, y2, color=None):
    c = color or PAL["mu"]
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{c}' stroke-width='2.5' marker-end='url(#a)'/>")


ARROW_DEF = ("<defs><marker id='a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'>"
             f"<path d='M0 0 L10 5 L0 10 z' fill='{PAL['mu']}'/></marker></defs>")


def agent_engine():
    b = ARROW_DEF
    b += t(40, 46, "The agent is the body. The model is the engine.", 20, 800)
    b += t(40, 72, "Swap the engine without changing how you work.", 15, 500, PAL["mu"])
    # the body
    b += box(40, 110, 260, 170, PAL["soft"], PAL["brand"])
    b += t(170, 150, "Coding agent", 18, 800, anchor="middle")
    b += t(170, 176, "reads files, edits code,", 14, 500, PAL["mu"], "middle")
    b += t(170, 196, "runs commands", 14, 500, PAL["mu"], "middle")
    b += "<circle cx='170' cy='240' r='22' fill='white' stroke='" + PAL["brand"] + "' stroke-width='3'/>" + t(170, 246, "you", 13, 700, PAL["brand"], "middle")
    # three engines
    engines = [("Local engine", "Ollama on your laptop", "Private · offline · hardware limit", PAL["greensoft"], PAL["green"], 110),
               ("Cloud free engine", "OpenRouter free models", "Daily limits · your prompts leave the laptop", PAL["amsoft"], PAL["amber"], 210),
               ("Router", "Omni Route, several providers", "Switches when one runs out · check terms", PAL["soft"], PAL["brand"], 310)]
    for name, who, note, fill, stroke, y in engines:
        b += arrow(300, 195, 380, y + 30, stroke)
        b += box(380, y, 360, 66, fill, stroke)
        b += t(398, y + 28, f"{name}: {who}", 15, 800)
        b += t(398, y + 50, note, 13, 500, PAL["mu"])
    return svg(780, 400, b, "Coding agent with swappable model engines")


def setups():
    b = t(40, 46, "Pick the setup that fits your work", 20, 800)
    cols = ["Private", "Free to start", "Works offline", "No daily cap"]
    rows = [("Ollama (laptop)", [1, 1, 1, 0]), ("OpenRouter (cloud)", [0, 1, 0, 0]),
            ("OpenCode", [1, 1, 1, 0]), ("Omni Route", [0, 1, 0, 0]), ("Kilo Code", [0, 1, 0, 0])]
    x0, y0, cw, rh = 240, 96, 130, 52
    for i, c in enumerate(cols):
        b += t(x0 + i * cw + cw / 2, y0 - 12, c, 13, 700, PAL["mu"], "middle")
    for r, (name, vals) in enumerate(rows):
        y = y0 + r * rh
        b += t(40, y + 32, name, 15, 700)
        for i, v in enumerate(vals):
            fill = PAL["greensoft"] if v else "#f3f4f6"
            stroke = PAL["green"] if v else PAL["line"]
            mark = "✓" if v else "–"
            b += box(x0 + i * cw + 12, y + 8, cw - 24, rh - 16, fill, stroke, 10)
            b += t(x0 + i * cw + cw / 2, y + 32, mark, 17, 800, PAL["green"] if v else PAL["mu"], "middle")
    b += t(40, 370, "Ticks are general. Check each provider's current terms and limits before you rely on one.", 13, 500, PAL["mu"])
    return svg(880, 400, b, "Comparison of setups by privacy, cost, offline use and limits")


def fallback():
    b = ARROW_DEF
    b += t(40, 46, "How a router keeps one task going", 20, 800)
    b += t(40, 72, "If the first provider is out of quota, the next one answers.", 15, 500, PAL["mu"])
    b += box(40, 150, 150, 80, PAL["soft"], PAL["brand"]) + t(115, 185, "Your request", 15, 800, anchor="middle")
    b += arrow(190, 190, 250, 190)
    b += box(250, 150, 170, 80, PAL["soft"], PAL["brand"]) + t(335, 185, "Router", 15, 800, anchor="middle")
    b += t(335, 208, "tries in order", 13, 500, PAL["mu"], "middle")
    b += arrow(420, 175, 500, 115)
    b += arrow(420, 205, 500, 265)
    b += box(500, 80, 240, 70, "#fee2e2", "#dc2626") + t(620, 112, "Provider 1: quota used up", 15, 700, "#991b1b", "middle")
    b += box(500, 230, 240, 70, PAL["greensoft"], PAL["green"]) + t(620, 262, "Provider 2: answers", 15, 700, PAL["green"], "middle")
    b += arrow(740, 265, 760, 265)
    b += t(40, 350, "Keep the router's key in a password manager, and connect only providers whose terms allow it.", 13, 500, PAL["mu"])
    return svg(800, 380, b, "Router trying providers in order until one answers")


def local_offline():
    b = t(40, 46, "Offline with Ollama: once a model is downloaded", 20, 800)
    b += box(60, 96, 300, 170, "#f3f4f6", PAL["line"])
    b += t(210, 128, "Your laptop", 16, 800, anchor="middle")
    b += box(96, 146, 228, 70, PAL["greensoft"], PAL["green"], 10) + t(210, 176, "Model runs here", 15, 800, PAL["green"], "middle")
    b += t(210, 200, "code and prompts stay on this machine", 13, 500, PAL["mu"], "middle")
    b += "<g transform='translate(430,120)'><path d='M0 30 Q40 0 80 30' fill='none' stroke='" + PAL["mu"] + "' stroke-width='3'/><path d='M12 46 Q40 22 68 46' fill='none' stroke='" + PAL["mu"] + "' stroke-width='3'/><circle cx='40' cy='62' r='5' fill='" + PAL["mu"] + "'/><line x1='0' y1='0' x2='80' y2='80' stroke='#dc2626' stroke-width='5'/></g>"
    b += t(430, 230, "Wi-Fi off", 15, 700, "#991b1b", "middle")
    b += t(40, 300, "Check the model is installed before you go offline (run it once while online).", 14, 500, PAL["mu"])
    return svg(640, 330, b, "Laptop running a model with Wi-Fi off")


def safety():
    items = ["Nothing is unlimited: plan for daily caps",
             "Free is not private: keep client code local",
             "Check terms before connecting any account",
             "Keys are passwords: store and rotate them",
             "Check the billing page, not the menu label",
             "Expect errors: copy the message, fix one thing"]
    b = t(40, 46, "Six rules before you use a free setup", 20, 800)
    for i, it in enumerate(items):
        y = 84 + i * 46
        b += box(40, y, 620, 36, PAL["soft"] if i % 2 == 0 else "#f8f9fc", PAL["line"], 10)
        b += f"<circle cx='64' cy='{y+18}' r='11' fill='{PAL['brand']}'/>" + t(64, y + 23, str(i + 1), 13, 800, "white", "middle")
        b += t(88, y + 23, it, 15, 600)
    return svg(700, 380, b, "Six safety rules for free AI coding setups")


FILES = {"agent-engine.svg": agent_engine, "setups.svg": setups, "fallback.svg": fallback,
         "local-offline.svg": local_offline, "safety.svg": safety}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in FILES.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", name)
