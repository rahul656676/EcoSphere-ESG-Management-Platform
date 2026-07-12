-- ============================================================
-- EcoSphere: Seed Data
-- ============================================================

INSERT INTO department (name, code, head, parent_department_id, employee_count, status) VALUES
('Corporate', 'COR', 'A. Mehta', NULL, 41, 'Active'),
('Manufacturing', 'MFG', 'S. Nair', NULL, 134, 'Active'),
('Logistics', 'LOG', 'R. Iyer', 2, 58, 'Active'),
('Sales', 'SALE', 'V. Kapoor', NULL, 76, 'Active'),
('R&D', 'RND', 'N. Kulkarni', NULL, 39, 'Active');

INSERT INTO category (name, type, status) VALUES
('Tree Plantation', 'CSR Activity', 'Active'),
('Blood Donation', 'CSR Activity', 'Active'),
('Beach Cleanup', 'CSR Activity', 'Active'),
('Training', 'CSR Activity', 'Active'),
('Emission Reduction', 'Challenge', 'Active'),
('Recycling', 'Challenge', 'Active'),
('Commute', 'Challenge', 'Active');

INSERT INTO emission_factor (name, source_type, unit, co2_factor, status) VALUES
('Diesel Fuel (Fleet)', 'Fleet', 'litre', 2.68, 'Active'),
('Electricity Grid', 'Expense', 'kWh', 0.82, 'Active'),
('Raw Material - Steel', 'Manufacturing', 'kg', 1.85, 'Active'),
('Purchased Packaging', 'Purchase', 'kg', 1.15, 'Active'),
('Air Travel', 'Expense', 'km', 0.15, 'Active');

INSERT INTO product_esg_profile (product_name, category, co2_per_unit, notes) VALUES
('EcoPack Container', 'Packaging', 0.42, 'Recyclable packaging line'),
('SteelFrame Pro', 'Industrial', 12.5, 'High carbon intensity - target for reduction'),
('GreenBottle 500ml', 'Consumer Goods', 0.08, 'Made from recycled PET');

INSERT INTO environmental_goal (name, department_id, target_co2, current_co2, deadline, status) VALUES
('Reduce Fleet Emissions', 3, 500, 390, '2026-12-31', 'Active'),
('Cut Packaging Waste', 2, 120, 98, '2026-09-30', 'On Track'),
('Office Energy Cut', 1, 80, 80, '2026-06-30', 'Completed');

INSERT INTO esg_policy (title, description, department_id, status, created_date) VALUES
('Anti-Corruption Policy', 'Zero tolerance policy on bribery and corruption', NULL, 'Active', '2026-01-10'),
('Code of Conduct', 'Employee behavioral and ethical guidelines', NULL, 'Active', '2026-01-10'),
('Data Privacy Policy', 'Handling of employee and customer data', NULL, 'Active', '2026-02-01');

INSERT INTO badge (name, description, unlock_rule_type, unlock_rule_value, icon) VALUES
('Green Beginner', 'Earned your first 50 XP', 'XP', 50, 'leaf'),
('Carbon Saver', 'Earned 500 XP through sustainability actions', 'XP', 500, 'cloud'),
('Sustainability Champion', 'Completed 5 challenges', 'CHALLENGES_COMPLETED', 5, 'trophy'),
('Team Player', 'Completed 10 challenges', 'CHALLENGES_COMPLETED', 10, 'users');

INSERT INTO reward (name, description, points_required, stock, status) VALUES
('Eco Tote Bag', 'Reusable branded tote bag', 100, 50, 'Active'),
('Extra Day Off', 'One additional paid day off', 1000, 10, 'Active'),
('Plant a Tree Certificate', 'A tree planted in your name', 300, 100, 'Active'),
('Wireless Earbuds', 'Company-branded earbuds', 2000, 5, 'Active');

INSERT INTO employee (name, email, department_id, xp_total, points_balance, gender, role, password_hash) VALUES
('Priya Sharma', 'priya.sharma@ecosphere.com', 1, 620, 620, 'Female', 'Employee', 'x'),
('Aditi Rao', 'aditi.rao@ecosphere.com', 2, 3910, 3910, 'Female', 'Employee', 'x'),
('Karan Shah', 'karan.shah@ecosphere.com', 3, 1450, 1450, 'Male', 'Employee', 'x'),
('S. Nair', 'nair.s@ecosphere.com', 2, 2200, 2200, 'Male', 'Manager', 'x'),
('R. Iyer', 'iyer.r@ecosphere.com', 3, 980, 980, 'Male', 'Manager', 'x'),
('A. Mehta', 'mehta.a@ecosphere.com', 1, 1800, 1800, 'Male', 'Admin', 'x');

INSERT INTO carbon_transaction (department_id, source_type, emission_factor_id, quantity, amount_co2, date, auto_generated, remarks) VALUES
(3, 'Fleet', 1, 100, 268, '2026-06-01', 1, 'Monthly diesel usage'),
(2, 'Manufacturing', 3, 50, 92.5, '2026-06-05', 1, 'Steel batch production'),
(1, 'Expense', 2, 200, 164, '2026-06-10', 1, 'Corporate office electricity'),
(2, 'Purchase', 4, 80, 92, '2026-06-15', 1, 'Packaging materials purchase'),
(4, 'Expense', 5, 300, 45, '2026-06-20', 1, 'Sales team air travel');

INSERT INTO csr_activity (name, category_id, description, date, evidence_required, status) VALUES
('Tree Plantation', 1, 'Community tree plantation drive', '2026-07-05', 1, 'Open'),
('Blood Donation', 2, 'Quarterly blood donation camp', '2026-07-08', 1, 'Open'),
('Beach Cleanup', 3, 'Coastal cleanup initiative', '2026-07-10', 0, 'Open'),
('ESG Workshop', 4, 'Employee ESG awareness training', '2026-07-01', 0, 'Open');

INSERT INTO employee_participation (employee_id, activity_id, proof_file, approval_status, points_earned, completion_date) VALUES
(2, 1, 'photo.jpg', 'Pending', 50, NULL),
(3, 4, 'cert.pdf', 'Approved', 30, '2026-07-01');

INSERT INTO challenge (title, category_id, description, xp, difficulty, evidence_required, deadline, status) VALUES
('Sustainability Sprint', 5, 'Multi-week department-wide emission reduction sprint', 200, 'Hard', 1, '2026-07-20', 'Active'),
('Recycle Challenge', 6, 'Recycle office and packaging waste', 80, 'Easy', 1, '2026-07-15', 'Active'),
('Commute Green Week', 7, 'Use sustainable commute options for a week', 120, 'Medium', 1, '2026-07-25', 'Draft');

INSERT INTO challenge_participation (challenge_id, employee_id, progress, proof_file, approval_status, xp_awarded) VALUES
(1, 2, 60, NULL, 'Pending', 0),
(2, 3, 100, 'recycle_proof.jpg', 'Approved', 80);

INSERT INTO policy_acknowledgement (policy_id, employee_id, acknowledged_date, status) VALUES
(1, 5, '2026-06-11', 'Acknowledged'),
(2, 2, '2026-06-12', 'Acknowledged'),
(3, 3, NULL, 'Pending');

INSERT INTO audit (title, department_id, auditor, date, findings, status) VALUES
('Q2 Waste Audit', 2, 'S. Nair', '2026-06-12', '3 minor issues', 'Completed'),
('Vendor Compliance Check', 3, 'R. Iyer', '2026-07-01', '1 open issue', 'Under Review');

INSERT INTO compliance_issue (audit_id, severity, description, department_id, owner, due_date, status) VALUES
(1, 'High', 'Missing MSDS sheets', 2, 'S. Nair', '2026-07-15', 'Open'),
(2, 'Medium', 'Late vendor disclosure', 3, 'R. Iyer', '2026-07-05', 'Resolved');

INSERT INTO department_score (department_id, environmental_score, social_score, governance_score, total_score) VALUES
(4, 90, 88, 85, 88.1),
(2, 78, 70, 90, 78.6),
(3, 74, 68, 82, 74.4),
(1, 85, 80, 92, 85.5),
(5, 70, 65, 80, 71.5);

INSERT INTO esg_config (key, value) VALUES
('auto_emission_calculation', 'true'),
('require_evidence_csr', 'true'),
('auto_award_badges', 'true'),
('email_alerts_compliance', 'true'),
('env_weight', '40'),
('social_weight', '30'),
('governance_weight', '30');

INSERT INTO notification_settings (key, enabled) VALUES
('new_compliance_issue', 1),
('csr_challenge_approval', 1),
('policy_ack_reminder', 1),
('badge_unlock', 1);

INSERT INTO users (username, password_hash, role, employee_id) VALUES
('admin', 'pbkdf2:sha256:600000$placeholder$will_be_reset', 'Admin', 6);
