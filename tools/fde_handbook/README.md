# FDE handbook sources

Content and builders for the AI Forward Deployed Engineer, Enterprise AI Architect & AI Automation Business Handbook.

- Content: `build_curriculum.py` (curriculum, volumes, jobs), `content_a.py` / `content_b.py` (module sections), `notes_a.py` / `notes_b.py` (every topic explained), `stages_12.py`, `stages_34.py`, `stages_567.py` (seven stage handbooks), `tracks_tools.py` (career tracks, tool directory, stacks).
- `python3 build_pdfs.py` writes the 23 PDFs to `pdf/`; copy them to `handbook/fde/`.
- `python3 build_app.py` writes the interactive page (`fde_curriculum.html`) that is published as the Claude artifact https://claude.ai/artifact/YcVe9ENf1hZJfk1yTZcxMA with the PDFs under `pdf/`.
- The site links: `tools/restabs.py` (`fde_box`, Resources → FDE) and the FDE guide block in `tools/gen_site.py`.
