import csv
import json
import os
from collections import Counter


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CASES_FILE = os.path.join(BASE_DIR, "data", "cases.csv")
RESULTS_FILE = os.path.join(BASE_DIR, "results", "results.csv")
REVIEW_FILE = os.path.join(BASE_DIR, "results", "responsible_ai_log.csv")

OUTPUT_DIR = os.path.join(BASE_DIR, "dashboard")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "index.html")


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def bar_chart(counter):
    if not counter:
        return "<p>No data available.</p>"

    maximum = max(counter.values())

    html = '<div class="bars">'

    for name, value in counter.items():
        width = (value / maximum) * 100 if maximum else 0

        html += f"""
        <div class="bar-row">
            <div class="bar-label">{name}</div>
            <div class="bar-track">
                <div class="bar" style="width:{width}%"></div>
            </div>
            <div class="bar-value">{value}</div>
        </div>
        """

    html += "</div>"

    return html


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cases = read_csv(CASES_FILE)
    results = read_csv(RESULTS_FILE)
    reviews = read_csv(REVIEW_FILE)

    issue_types = Counter(row["issue_type"] for row in cases)
    severity = Counter(row["severity"] for row in cases)
    rules = Counter(row["rule_status"] for row in results)
    decisions = Counter(row["human_decision"] for row in reviews)

    edited = [
        row for row in reviews
        if row["human_decision"] == "Edited"
    ]

    rows_html = ""

    for row in results:
        rows_html += f"""
        <tr>
            <td>{row['case_id']}</td>
            <td>{row['issue_type']}</td>
            <td>{row['severity']}</td>
            <td>{row['ai_root_cause']}</td>
            <td>{row['ai_confidence']}</td>
            <td>{row['rule_status']}</td>
        </tr>
        """

    edited_html = ""

    for row in edited:
        edited_html += f"""
        <tr>
            <td>{row['case_id']}</td>
            <td>{row['issue_type']}</td>
            <td>{row['ai_diagnosis']}</td>
            <td>{row['human_correction']}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>NetSolve AI Dashboard</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 0;
    background: #f4f6f8;
    color: #222;
}}

header {{
    background: #17202a;
    color: white;
    padding: 28px 40px;
}}

header h1 {{
    margin: 0;
}}

header p {{
    margin-bottom: 0;
    color: #ccd1d1;
}}

.container {{
    padding: 30px 40px;
}}

.cards {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 30px;
}}

.card {{
    background: white;
    padding: 22px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.card h3 {{
    margin: 0;
    font-size: 14px;
    color: #666;
}}

.card .number {{
    font-size: 30px;
    font-weight: bold;
    margin-top: 10px;
}}

.grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
}}

.panel {{
    background: white;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 25px;
}}

.bar-row {{
    display: grid;
    grid-template-columns: 100px 1fr 40px;
    align-items: center;
    gap: 10px;
    margin: 12px 0;
}}

.bar-label {{
    font-size: 13px;
}}

.bar-track {{
    background: #e5e7e9;
    height: 20px;
    border-radius: 10px;
    overflow: hidden;
}}

.bar {{
    background: #3498db;
    height: 100%;
}}

.bar-value {{
    font-weight: bold;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

th, td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}

th {{
    background: #f1f2f3;
}}

.notice {{
    padding: 18px;
    background: #eafaf1;
    border-left: 5px solid #27ae60;
    margin-bottom: 25px;
}}

</style>
</head>

<body>

<header>
    <h1>NetSolve AI</h1>
    <p>AI-Assisted Network Troubleshooting Dashboard</p>
</header>

<div class="container">

<div class="notice">
    <strong>Responsible AI:</strong>
    Human review is required before accepting a troubleshooting recommendation.
    5 cases were edited during human review.
</div>

<div class="cards">

    <div class="card">
        <h3>Total Cases</h3>
        <div class="number">{len(cases)}</div>
    </div>

    <div class="card">
        <h3>Processed</h3>
        <div class="number">{len(results)}</div>
    </div>

    <div class="card">
        <h3>Human Accepted</h3>
        <div class="number">{decisions.get("Accepted", 0)}</div>
    </div>

    <div class="card">
        <h3>Human Edited</h3>
        <div class="number">{decisions.get("Edited", 0)}</div>
    </div>

</div>

<div class="grid">

<div class="panel">
<h2>Issue Types</h2>
{bar_chart(issue_types)}
</div>

<div class="panel">
<h2>Severity</h2>
{bar_chart(severity)}
</div>

</div>

<div class="grid">

<div class="panel">
<h2>Deterministic Rule Checker</h2>
{bar_chart(rules)}
</div>

<div class="panel">
<h2>Human Decisions</h2>
{bar_chart(decisions)}
</div>

</div>

<div class="panel">

<h2>Human Corrections</h2>

<table>

<tr>
    <th>Case</th>
    <th>Type</th>
    <th>AI Diagnosis</th>
    <th>Human Correction</th>
</tr>

{edited_html}

</table>

</div>

<div class="panel">

<h2>Case Results</h2>

<table>

<tr>
    <th>Case</th>
    <th>Issue</th>
    <th>Severity</th>
    <th>AI Root Cause</th>
    <th>Confidence</th>
    <th>Rule Check</th>
</tr>

{rows_html}

</table>

</div>

</div>

</body>
</html>
"""

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(html)

    print("NetSolve AI Dashboard created.")
    print(f"Open: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

