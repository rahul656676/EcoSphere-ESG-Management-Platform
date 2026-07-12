# EcoSphere: ESG Management Platform

A full-stack ESG (Environmental, Social, Governance) management platform that
integrates carbon accounting, CSR/employee engagement, governance/compliance
tracking, and gamification into a single dashboard, as described in the
challenge brief.

## Folder Structure

```
EcoSphere/
├── frontend/                # Static HTML/CSS/JS UI (served by Flask)
│   ├── login.html
│   ├── dashboard.html
│   ├── environmental.html
│   ├── social.html
│   ├── governance.html
│   ├── gamification.html
│   ├── reports.html
│   ├── settings.html
│   ├── style.css            # shared styling
│   └── app.js                # shared frontend helpers (fetch wrapper, nav, modals)
├── backend/
│   ├── app.py                # Flask app entrypoint, static serving, DB bootstrap
│   ├── auth.py                # session-based login/logout
│   ├── controllers.py         # business rules: scoring, XP/badges, notifications
│   └── routes.py              # REST API endpoints for every module
├── database/
│   ├── schema.sql              # full SQLite schema (master + transactional data)
│   └── seed.sql                 # demo seed data matching the wireframes
├── ai/
│   ├── prompts.txt             # documented LLM prompts used for report narratives
│   └── reports.py               # report builders + optional Claude-generated summary
└── docs/
    └── README.md
```

## Running It

Requirements: Python 3.10+, `flask`, `werkzeug` (install with pip if missing:
`pip install flask --break-system-packages`). Optional: `anthropic` python
package + `ANTHROPIC_API_KEY` env var if you want AI-generated report
narratives (the platform works fully without it).

```bash
cd backend
python3 app.py
```

Open **http://localhost:5000** in a browser.

Default login: **admin / admin123**

The SQLite database (`database/ecosphere.db`) is created automatically from
`schema.sql` and seeded from `seed.sql` on first run. To reset to a clean demo
state at any time, call `POST /api/reset-demo-data` or delete
`database/ecosphere.db` and restart the app.

## Modules Implemented

- **Environmental**: Emission Factors, Product ESG Profiles, Carbon
  Transactions (auto-calculated from Emission Factors when the "Auto
  Emission Calculation" setting is enabled), Environmental Goals with
  progress tracking.
- **Social**: CSR Activities, Employee Participation (approval queue with
  Evidence Requirement business rule), Diversity Dashboard.
- **Governance**: ESG Policies, Policy Acknowledgements, Audits, Compliance
  Issues (mandatory Owner + Due Date, automatic Overdue flagging).
- **Gamification**: Challenges (full Draft → Active → Under Review →
  Completed / Archived lifecycle), Challenge Participation, XP, Badges
  (auto-awarded from Unlock Rules), Rewards (redeemable, stock-limited),
  Leaderboard.
- **Reports**: Environmental / Social / Governance / ESG Summary reports plus
  a Custom Report Builder filterable by Department, Date Range, Employee,
  Challenge, ESG Category, with CSV/JSON export in the demo UI and an
  optional AI-written executive summary per report.
- **Settings**: Departments, Categories, ESG Configuration (business-rule
  toggles + score weighting), Notification Settings.

## Business Rules Implemented (Section 8 of the brief)

- **Reward Redemption**: deducts points, respects stock availability.
- **Notification System**: in-app notification rows generated for new
  compliance issues, CSR/Challenge approval decisions, policy acknowledgement
  reminders, and badge unlocks — each independently toggleable in Settings.
- **Auto Emission Calculation**: toggle in Settings controls whether Carbon
  Transactions are computed from `quantity × emission_factor.co2_factor` or
  accepted as a manual CO2 amount.
- **Evidence Requirement**: CSR participation cannot be Approved without a
  proof file when the toggle is enabled; Challenge participation follows the
  per-Challenge `evidence_required` flag.
- **Badge Auto-Award**: badges unlock automatically the moment an employee's
  XP or completed-challenge count satisfies the badge's Unlock Rule.
- **Compliance Issue Ownership**: Owner + Due Date are mandatory on creation;
  Open issues past their Due Date are automatically flagged Overdue (and
  notified) whenever the Compliance Issues list is loaded.

## Scoring Model (Section 5 of the brief)

`Department Score` = weighted average of that department's Environmental,
Social and Governance sub-scores (default weighting 40/30/30, configurable in
Settings → ESG Configuration). The `Overall ESG Score` shown on the Dashboard
is the average of all Department Total Scores — recomputed on every dashboard
load and report generation.

## AI Integration

`ai/reports.py` optionally calls the Anthropic API (`claude-sonnet-4-6`) to
turn a generated report's structured numbers into a short executive summary.
This is entirely additive — if `ANTHROPIC_API_KEY` isn't set, reports are
still fully generated with all underlying data, just without the narrative
paragraph. All prompts used are documented in `ai/prompts.txt`.

## Notes / Known Simplifications (demo-scope)

- PDF/Excel export buttons in the Reports UI currently download the report's
  JSON payload as a stand-in; wiring real PDF/XLSX generation is a
  straightforward next step (e.g. via `reportlab` / `openpyxl`) on top of the
  same `ai/reports.py` data.
- Authentication is a single shared Admin login for demo purposes; the
  `users` table already supports per-employee accounts if you want to extend
  it to role-based login.
