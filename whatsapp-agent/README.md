# WhatsApp agent knowledge base

`SkillNavora_WhatsApp_Agent_Knowledge.xlsx` is the source the WhatsApp agent answers from. It is generated from the website's own data, so it stays in step with the site.

## Rebuild after website changes
```
python3 whatsapp-agent/build_kb.py
```
Needs Python 3 with `openpyxl` (`pip install openpyxl`) and Node.js.

## Import into Google Sheets
1. Open Google Sheets, then File > Import > Upload, and choose the .xlsx file.
2. Choose "Replace spreadsheet" or "Insert new sheets", then Import data.

## Rules for the agent
- Read `START_HERE` first. Answer only from these tabs, with the source link.
- Yellow rows are marked CONFIRM. Do not quote them until the owner confirms.
- Never promise a job, placement or salary.
