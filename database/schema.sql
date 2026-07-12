-- ============================================================
-- EcoSphere: ESG Management Platform - Database Schema (SQLite)
-- ============================================================

PRAGMA foreign_keys = ON;

-- ---------------- MASTER DATA ----------------

CREATE TABLE IF NOT EXISTS department (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    head TEXT,
    parent_department_id INTEGER,
    employee_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (parent_department_id) REFERENCES department(id)
);

CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('CSR Activity','Challenge')),
    status TEXT DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS emission_factor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    source_type TEXT NOT NULL CHECK (source_type IN ('Purchase','Manufacturing','Expense','Fleet')),
    unit TEXT NOT NULL,
    co2_factor REAL NOT NULL,
    status TEXT DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS product_esg_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT,
    co2_per_unit REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS environmental_goal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_id INTEGER,
    target_co2 REAL,
    current_co2 REAL DEFAULT 0,
    deadline DATE,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (department_id) REFERENCES department(id)
);

CREATE TABLE IF NOT EXISTS esg_policy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    department_id INTEGER,
    status TEXT DEFAULT 'Active',
    created_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (department_id) REFERENCES department(id)
);

CREATE TABLE IF NOT EXISTS badge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    unlock_rule_type TEXT CHECK (unlock_rule_type IN ('XP','CHALLENGES_COMPLETED')),
    unlock_rule_value INTEGER,
    icon TEXT
);

CREATE TABLE IF NOT EXISTS reward (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    points_required INTEGER NOT NULL,
    stock INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    department_id INTEGER,
    xp_total INTEGER DEFAULT 0,
    points_balance INTEGER DEFAULT 0,
    gender TEXT,
    role TEXT DEFAULT 'Employee',
    password_hash TEXT,
    FOREIGN KEY (department_id) REFERENCES department(id)
);

-- ---------------- TRANSACTIONAL DATA ----------------

CREATE TABLE IF NOT EXISTS carbon_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER,
    source_type TEXT CHECK (source_type IN ('Purchase','Manufacturing','Expense','Fleet')),
    emission_factor_id INTEGER,
    quantity REAL DEFAULT 1,
    amount_co2 REAL NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    auto_generated INTEGER DEFAULT 0,
    remarks TEXT,
    FOREIGN KEY (department_id) REFERENCES department(id),
    FOREIGN KEY (emission_factor_id) REFERENCES emission_factor(id)
);

CREATE TABLE IF NOT EXISTS csr_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    description TEXT,
    date DATE,
    evidence_required INTEGER DEFAULT 1,
    status TEXT DEFAULT 'Open',
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS employee_participation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,
    proof_file TEXT,
    approval_status TEXT DEFAULT 'Pending' CHECK (approval_status IN ('Pending','Approved','Rejected')),
    points_earned INTEGER DEFAULT 0,
    completion_date DATE,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (activity_id) REFERENCES csr_activity(id)
);

CREATE TABLE IF NOT EXISTS challenge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category_id INTEGER,
    description TEXT,
    xp INTEGER DEFAULT 0,
    difficulty TEXT CHECK (difficulty IN ('Easy','Medium','Hard')),
    evidence_required INTEGER DEFAULT 1,
    deadline DATE,
    status TEXT DEFAULT 'Draft' CHECK (status IN ('Draft','Active','Under Review','Completed','Archived')),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS challenge_participation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    progress INTEGER DEFAULT 0,
    proof_file TEXT,
    approval_status TEXT DEFAULT 'Pending' CHECK (approval_status IN ('Pending','Approved','Rejected')),
    xp_awarded INTEGER DEFAULT 0,
    FOREIGN KEY (challenge_id) REFERENCES challenge(id),
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS policy_acknowledgement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    acknowledged_date DATE,
    status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending','Acknowledged')),
    FOREIGN KEY (policy_id) REFERENCES esg_policy(id),
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    department_id INTEGER,
    auditor TEXT,
    date DATE,
    findings TEXT,
    status TEXT DEFAULT 'Under Review' CHECK (status IN ('Under Review','Completed')),
    FOREIGN KEY (department_id) REFERENCES department(id)
);

CREATE TABLE IF NOT EXISTS compliance_issue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id INTEGER,
    severity TEXT CHECK (severity IN ('Low','Medium','High')),
    description TEXT,
    department_id INTEGER,
    owner TEXT NOT NULL,
    due_date DATE NOT NULL,
    status TEXT DEFAULT 'Open' CHECK (status IN ('Open','Resolved','Overdue')),
    FOREIGN KEY (audit_id) REFERENCES audit(id),
    FOREIGN KEY (department_id) REFERENCES department(id)
);

CREATE TABLE IF NOT EXISTS department_score (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    environmental_score REAL DEFAULT 0,
    social_score REAL DEFAULT 0,
    governance_score REAL DEFAULT 0,
    total_score REAL DEFAULT 0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES department(id)
);

CREATE TABLE IF NOT EXISTS employee_badge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    badge_id INTEGER NOT NULL,
    awarded_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (badge_id) REFERENCES badge(id)
);

CREATE TABLE IF NOT EXISTS reward_redemption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    reward_id INTEGER NOT NULL,
    points_deducted INTEGER NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (reward_id) REFERENCES reward(id)
);

CREATE TABLE IF NOT EXISTS notification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    message TEXT NOT NULL,
    employee_id INTEGER,
    is_read INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS esg_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notification_settings (
    key TEXT PRIMARY KEY,
    enabled INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'Admin',
    employee_id INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employee(id)
)
