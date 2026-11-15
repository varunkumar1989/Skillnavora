"""Zip the starter project for download: python3 tools/aihandbook/starter/package.py
Writes handbook/AI-Master-Course-Starter-Project.zip (a gated download on the site)."""
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "ai-master-course-starter")
OUT = os.path.join(HERE, "..", "..", "..", "handbook", "AI-Master-Course-Starter-Project.zip")
SKIP_DIRS = {"__pycache__", "logs", ".pytest_cache", ".venv"}
SKIP_FILES = {".env"}

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    count = 0
    for root, dirs, files in os.walk(SRC):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if name in SKIP_FILES or name.endswith(".pyc"):
                continue
            path = os.path.join(root, name)
            arc = os.path.join("ai-master-course-starter", os.path.relpath(path, SRC))
            info = zipfile.ZipInfo(arc, date_time=(2026, 11, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(path, "rb") as f:
                z.writestr(info, f.read())
            count += 1
print(f"wrote {os.path.normpath(OUT)}: {count} files, {os.path.getsize(OUT) // 1024} KB")
