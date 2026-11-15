"""Run every companion example and save its real output to outputs.json for the guide pages,
then zip the examples for download. Needs: numpy, pandas, scipy, scikit-learn, statsmodels.
Run: python tools/mlguide/capture.py"""
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(HERE, "examples")
ROOT = os.path.dirname(os.path.dirname(HERE))
ZIP = os.path.join(ROOT, "handbook", "ML-Class-Guide-Code.zip")

out = {}
for i, name in enumerate(sorted(f for f in os.listdir(EX) if f.endswith(".py")), 1):
    r = subprocess.run([sys.executable, "-W", "ignore", name], cwd=EX, capture_output=True, text=True, timeout=300)
    if r.returncode:
        sys.exit(f"{name} failed:\n{r.stderr}")
    out[name.split("_")[0]] = r.stdout.rstrip()
    print(f"captured {name}: {len(r.stdout.splitlines())} lines")
json.dump(out, open(os.path.join(HERE, "outputs.json"), "w"), indent=1, ensure_ascii=False)

readme = """ML class guide: companion code (SkillNavora)
Each script builds its own synthetic data, so it runs anywhere without downloads.
Setup:  pip install numpy pandas scipy scikit-learn statsmodels
Run:    python c1_hypothesis_case.py   (and c2 ... c6)
Guide:  https://www.skillnavora.in/ml-class-guide.html
"""
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr(zipfile.ZipInfo("ml-class-guide-code/README.txt", (2026, 11, 15, 0, 0, 0)), readme)
    for name in sorted(os.listdir(EX)):
        if name.endswith(".py"):
            info = zipfile.ZipInfo(f"ml-class-guide-code/{name}", (2026, 11, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, open(os.path.join(EX, name), "rb").read())
print("wrote", os.path.relpath(ZIP, ROOT), os.path.getsize(ZIP) // 1024, "KB")
