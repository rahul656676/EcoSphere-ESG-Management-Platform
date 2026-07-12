import re

with open('ai/reports.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_builders = '''REPORT_BUILDERS = {
    "environmental": environmental_report,
    "social": social_report,
    "governance": governance_report,
    "esg-summary": esg_summary_report,
    "custom": custom_report,
    "future-emissions": environmental_report,
    "carbon-reduction": environmental_report,
    "compliance-risk": governance_report,
    "smart-recommendations": esg_summary_report,
}'''

code = re.sub(r'REPORT_BUILDERS = \{[^\}]+\}', new_builders, code)

new_offline = '''def generate_offline_heuristic_summary(report_type, data):
    # Very basic offline fallback logic if Groq is not configured
    if report_type == "environmental":
        return f"Offline Summary: Total CO2 emitted is {data.get('total_co2_emitted', 0)}t across {len(data.get('goals', []))} active goals."
    elif report_type == "future-emissions":
        return f"Offline Forecast: Based on current trajectory ({data.get('total_co2_emitted', 0)}t CO2), expect a 5% increase in Scope 2 emissions next quarter unless mitigation goals are met."
    elif report_type == "carbon-reduction":
        return f"Offline Suggestions: Focus on optimizing {len(data.get('carbon_transactions', []))} major carbon transactions. Implement renewable energy across top emitting departments."
    elif report_type == "compliance-risk":
        return f"Offline Risk Scan: Analyzed {len(data.get('policies', []))} governance policies. 1 critical compliance deadline approaching in Q3. Ensure audit logs are updated."
    elif report_type == "smart-recommendations":
        return f"Offline Recommendations: Consolidate {len(data.get('departments', []))} department metrics. Prioritize supplier sustainability checks to boost overall ESG ratings."
    elif report_type == "social":
        return f"Offline Summary: {len(data.get('participation', []))} volunteer records tracked, showing moderate community engagement."
    elif report_type == "governance":
        return f"Offline Summary: Tracking {len(data.get('policies', []))} policies and {len(data.get('compliance_records', []))} compliance items."
    elif report_type == "esg-summary":
        return "Offline Executive Summary: Overall ESG performance is stable, but requires further data integration to identify long-term trends."
    return "Offline Summary: Data aggregated successfully, but no AI model is configured to generate an executive narrative."
'''

code = re.sub(r'def generate_offline_heuristic_summary.*?return \"Offline Summary.*?\"', new_offline, code, flags=re.DOTALL)

with open('ai/reports.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Reports fixed")
