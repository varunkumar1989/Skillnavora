"""Builds data/sample_policy.pdf (a fictional policy used by the PDF chatbot lesson)."""
import os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ai-master-course-starter", "data", "sample_policy.pdf")

HTML = """<!doctype html><html><head><meta charset="utf-8"><title>Acme Employee Policy (sample)</title>
<style>body{font:12pt/1.5 Arial,sans-serif;margin:0}h1{font-size:20pt}h2{font-size:15pt;margin-top:18pt}.pb{page-break-before:always}</style></head><body>
<h1>Acme Employee Policy</h1>
<p>This is a fictional sample document for the SkillNavora AI Master Course. It is not a real company policy.</p>
<h2>Paid Leave</h2>
<p>Employees get 20 days of paid leave each calendar year. Leave is earned at 1.67 days per month from the joining date.</p>
<p>Unused leave can be carried forward up to 5 days into the next year. Any leave above 5 days lapses on 31 December.</p>
<p>Employees must apply for leave in the HR portal at least 7 days in advance, except for sick leave.</p>
<h2>Sick Leave</h2>
<p>Employees get 10 days of sick leave each year, separate from paid leave. A doctor's note is needed for sick leave longer than 2 days in a row.</p>
<h2>Expenses</h2>
<p>Expense claims must be submitted within 30 days of the expense, with a receipt for every item above 500 rupees.</p>
<p>Meals during business travel are reimbursed up to 1,500 rupees per day. Alcohol is never reimbursed.</p>
<p>Claims are paid with the next monthly salary after the manager approves them.</p>
<div class="pb"></div>
<h2>Remote Work</h2>
<p>Employees may work remotely up to 3 days a week with their manager's approval. Teams agree their office days each quarter.</p>
<p>Remote work from another country needs written approval from HR and Legal, because of tax and data rules.</p>
<h2>Travel</h2>
<p>All business travel is booked through the approved travel portal. Economy class is used for flights under 6 hours.</p>
<p>Hotels are booked at the negotiated rate where available. Travel insurance is provided by the company for every trip.</p>
<h2>Laptops and Security</h2>
<p>Company laptops must use full-disk encryption and a screen lock after 5 minutes. Passwords must be at least 14 characters.</p>
<p>Report a lost or stolen laptop to the IT helpdesk within 24 hours. Never share customer data on personal devices or personal email.</p>
<h2>Learning Budget</h2>
<p>Each employee has a learning budget of 40,000 rupees per year for courses, books and certifications related to their role.</p>
<p>Courses above 20,000 rupees need manager approval before purchase.</p>
</body></html>"""

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(HTML)
    subprocess.run(["node", os.path.join(os.path.dirname(HERE), "render_pdf.js"), fh.name, OUT, "plain"], check=True)
    os.unlink(fh.name)
    print("written", OUT)
