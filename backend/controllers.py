"""
EcoSphere - controllers.py
Business/domain logic: scoring, gamification (XP/badges), notifications,
auto emission calculation, evidence rules, compliance overdue checks,
and reward redemption.
"""

from datetime import date
import models


# ---------------------------------------------------------------------------
# Settings helpers
# ---------------------------------------------------------------------------

def get_config(key, default=None):
    row = models.query("SELECT value FROM esg_config WHERE key = ?", (key,), one=True)
    return row["value"] if row else default


def set_config(key, value):
    existing = models.query("SELECT * FROM esg_config WHERE key = ?", (key,), one=True)
    if existing:
        models.execute("UPDATE esg_config SET value = ? WHERE key = ?", (str(value), key))
    else:
        models.execute("INSERT INTO esg_config (key, value) VALUES (?, ?)", (key, str(value)))


def config_bool(key, default=False):
    val = get_config(key, str(default)).lower()
    return val in ("true", "1", "yes")


def notification_enabled(key):
    row = models.query("SELECT enabled FROM notification_settings WHERE key = ?", (key,), one=True)
    return bool(row["enabled"]) if row else True


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------

def notify(setting_key, ntype, message, employee_id=None):
    if not notification_enabled(setting_key):
        return
    models.insert_row("notification", {
        "type": ntype,
        "message": message,
        "employee_id": employee_id,
        "is_read": 0,
    })


# ---------------------------------------------------------------------------
# Auto Emission Calculation (Settings toggle)
# ---------------------------------------------------------------------------

def calculate_emission(department_id, source_type, emission_factor_id, quantity, remarks=""):
    """Create a Carbon Transaction. If auto_emission_calculation is enabled,
    amount_co2 is derived from the Emission Factor; otherwise caller must
    supply quantity as the final CO2 amount (manual entry)."""
    auto = config_bool("auto_emission_calculation", True)
    factor = models.get_by_id("emission_factor", emission_factor_id) if emission_factor_id else None

    if auto and factor:
        amount_co2 = round(quantity * factor["co2_factor"], 2)
    else:
        amount_co2 = quantity

    txn_id = models.insert_row("carbon_transaction", {
        "department_id": department_id,
        "source_type": source_type,
        "emission_factor_id": emission_factor_id,
        "quantity": quantity,
        "amount_co2": amount_co2,
        "date": date.today().isoformat(),
        "auto_generated": 1 if auto else 0,
        "remarks": remarks,
    })
    return txn_id


# ---------------------------------------------------------------------------
# CSR Approval (Evidence Requirement toggle)
# ---------------------------------------------------------------------------

def approve_employee_participation(participation_id, decision):
    """decision: 'Approved' or 'Rejected'"""
    part = models.get_by_id("employee_participation", participation_id)
    if not part:
        return {"error": "Participation not found"}, 404

    require_evidence = config_bool("require_evidence_csr", True)
    if decision == "Approved" and require_evidence and not part["proof_file"]:
        return {"error": "Evidence is required before approval"}, 400

    models.update_row("employee_participation", participation_id, {
        "approval_status": decision,
        "completion_date": date.today().isoformat() if decision == "Approved" else None,
    })

    if decision == "Approved":
        award_xp_points(part["employee_id"], xp=0, points=part["points_earned"])

    notify("csr_challenge_approval", "CSR_APPROVAL",
           f"CSR activity participation #{participation_id} was {decision.lower()}.",
           employee_id=part["employee_id"])

    return {"success": True}, 200


def approve_challenge_participation(participation_id, decision):
    part = models.get_by_id("challenge_participation", participation_id)
    if not part:
        return {"error": "Participation not found"}, 404

    challenge = models.get_by_id("challenge", part["challenge_id"])
    require_evidence = challenge["evidence_required"] if challenge else 0

    if decision == "Approved" and require_evidence and not part["proof_file"]:
        return {"error": "Evidence is required before approval"}, 400

    xp_awarded = challenge["xp"] if (decision == "Approved" and challenge) else 0

    models.update_row("challenge_participation", participation_id, {
        "approval_status": decision,
        "xp_awarded": xp_awarded,
    })

    if decision == "Approved":
        award_xp_points(part["employee_id"], xp=xp_awarded, points=xp_awarded)

    notify("csr_challenge_approval", "CHALLENGE_APPROVAL",
           f"Challenge participation #{participation_id} was {decision.lower()}.",
           employee_id=part["employee_id"])

    return {"success": True}, 200


# ---------------------------------------------------------------------------
# Gamification: XP, Badges, Rewards, Leaderboard
# ---------------------------------------------------------------------------

def award_xp_points(employee_id, xp=0, points=0):
    emp = models.get_by_id("employee", employee_id)
    if not emp:
        return
    models.update_row("employee", employee_id, {
        "xp_total": emp["xp_total"] + xp,
        "points_balance": emp["points_balance"] + points,
    })
    check_and_award_badges(employee_id)


def completed_challenge_count(employee_id):
    row = models.query(
        """SELECT COUNT(*) AS c FROM challenge_participation
           WHERE employee_id = ? AND approval_status = 'Approved'""",
        (employee_id,), one=True)
    return row["c"] if row else 0


def check_and_award_badges(employee_id):
    if not config_bool("auto_award_badges", True):
        return

    emp = models.get_by_id("employee", employee_id)
    badges = models.table_all("badge")
    owned = {b["badge_id"] for b in models.query(
        "SELECT badge_id FROM employee_badge WHERE employee_id = ?", (employee_id,))}

    challenge_count = completed_challenge_count(employee_id)

    for badge in badges:
        if badge["id"] in owned:
            continue
        unlocked = False
        if badge["unlock_rule_type"] == "XP" and emp["xp_total"] >= badge["unlock_rule_value"]:
            unlocked = True
        elif badge["unlock_rule_type"] == "CHALLENGES_COMPLETED" and challenge_count >= badge["unlock_rule_value"]:
            unlocked = True

        if unlocked:
            models.insert_row("employee_badge", {
                "employee_id": employee_id,
                "badge_id": badge["id"],
                "awarded_date": date.today().isoformat(),
            })
            notify("badge_unlock", "BADGE_UNLOCK",
                   f"{emp['name']} unlocked the '{badge['name']}' badge!",
                   employee_id=employee_id)


def redeem_reward(employee_id, reward_id):
    emp = models.get_by_id("employee", employee_id)
    reward = models.get_by_id("reward", reward_id)

    if not emp or not reward:
        return {"error": "Employee or Reward not found"}, 404
    if reward["status"] != "Active":
        return {"error": "Reward is not active"}, 400
    if reward["stock"] <= 0:
        return {"error": "Reward is out of stock"}, 400
    if emp["points_balance"] < reward["points_required"]:
        return {"error": "Insufficient points balance"}, 400

    models.update_row("employee", employee_id, {
        "points_balance": emp["points_balance"] - reward["points_required"]
    })
    models.update_row("reward", reward_id, {"stock": reward["stock"] - 1})
    models.insert_row("reward_redemption", {
        "employee_id": employee_id,
        "reward_id": reward_id,
        "points_deducted": reward["points_required"],
        "date": date.today().isoformat(),
    })
    return {"success": True}, 200


def leaderboard(limit=20):
    return models.query(
        """SELECT e.id, e.name, d.name AS department, e.xp_total
           FROM employee e LEFT JOIN department d ON e.department_id = d.id
           ORDER BY e.xp_total DESC LIMIT ?""", (limit,))


# ---------------------------------------------------------------------------
# Compliance Issue Ownership & overdue flagging
# ---------------------------------------------------------------------------

def refresh_overdue_compliance_issues():
    today = date.today().isoformat()
    overdue = models.query(
        """SELECT * FROM compliance_issue
           WHERE status = 'Open' AND due_date < ?""", (today,))
    for issue in overdue:
        models.update_row("compliance_issue", issue["id"], {"status": "Overdue"})
        notify("new_compliance_issue", "COMPLIANCE_OVERDUE",
               f"Compliance issue '{issue['description']}' (owner: {issue['owner']}) is overdue.")
    return len(overdue)


def raise_compliance_issue(data):
    issue_id = models.insert_row("compliance_issue", data)
    issue = models.get_by_id("compliance_issue", issue_id)
    notify("new_compliance_issue", "NEW_COMPLIANCE_ISSUE",
           f"New compliance issue raised: '{issue['description']}' (Owner: {issue['owner']}, Due: {issue['due_date']}).")
    return issue_id


# ---------------------------------------------------------------------------
# ESG Scoring: Department Score -> Overall ESG Score
# ---------------------------------------------------------------------------

def compute_environmental_score(department_id=None):
    """Score derived from Environmental Goal progress (target vs current CO2 reduction)."""
    sql = "SELECT * FROM environmental_goal"
    params = ()
    if department_id:
        sql += " WHERE department_id = ?"
        params = (department_id,)
    goals = models.query(sql, params)
    if not goals:
        return 75.0
    scores = []
    for g in goals:
        target = g["target_co2"] or 1
        current = g["current_co2"] or 0
        # lower current relative to target (i.e. more reduction achieved) = higher score
        progress = max(0, min(100, (1 - (current / target)) * 100)) if target else 0
        # If current <= target already (goal met), treat as high score
        scores.append(progress if progress > 0 else 100)
    return round(sum(scores) / len(scores), 1)


def compute_social_score(department_id=None):
    sql = """SELECT approval_status FROM employee_participation ep
             JOIN employee e ON ep.employee_id = e.id"""
    params = ()
    if department_id:
        sql += " WHERE e.department_id = ?"
        params = (department_id,)
    rows = models.query(sql, params)
    if not rows:
        return 70.0
    approved = sum(1 for r in rows if r["approval_status"] == "Approved")
    return round((approved / len(rows)) * 100, 1)


def compute_governance_score(department_id=None):
    sql = "SELECT status FROM compliance_issue"
    params = ()
    if department_id:
        sql += " WHERE department_id = ?"
        params = (department_id,)
    rows = models.query(sql, params)
    if not rows:
        return 85.0
    resolved = sum(1 for r in rows if r["status"] == "Resolved")
    return round((resolved / len(rows)) * 100, 1)


def recompute_department_scores():
    departments = models.table_all("department")
    env_w = float(get_config("env_weight", 40)) / 100
    soc_w = float(get_config("social_weight", 30)) / 100
    gov_w = float(get_config("governance_weight", 30)) / 100

    results = []
    for d in departments:
        env = compute_environmental_score(d["id"])
        soc = compute_social_score(d["id"])
        gov = compute_governance_score(d["id"])
        total = round(env * env_w + soc * soc_w + gov * gov_w, 1)

        existing = models.query(
            "SELECT * FROM department_score WHERE department_id = ?", (d["id"],), one=True)
        payload = {
            "department_id": d["id"],
            "environmental_score": env,
            "social_score": soc,
            "governance_score": gov,
            "total_score": total,
        }
        if existing:
            models.update_row("department_score", existing["id"], payload)
        else:
            models.insert_row("department_score", payload)
        results.append(payload)
    return results


def overall_esg_scores():
    """Weighted average of Department Total Scores -> Overall ESG Score."""
    recompute_department_scores()
    dept_scores = models.query("SELECT * FROM department_score")
    if not dept_scores:
        return {"environmental": 0, "social": 0, "governance": 0, "overall": 0}

    env = round(sum(d["environmental_score"] for d in dept_scores) / len(dept_scores), 1)
    soc = round(sum(d["social_score"] for d in dept_scores) / len(dept_scores), 1)
    gov = round(sum(d["governance_score"] for d in dept_scores) / len(dept_scores), 1)
    overall = round(sum(d["total_score"] for d in dept_scores) / len(dept_scores), 1)

    return {"environmental": env, "social": soc, "governance": gov, "overall": overall}
