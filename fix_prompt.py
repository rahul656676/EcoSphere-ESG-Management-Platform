import re

with open('ai/reports.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_prompt = '''          prompt = "You are an AI ESG Copilot for the EcoSphere platform. "
          if report_type == "future-emissions":
              prompt += "Analyze the following JSON data and provide a 2-sentence AI-driven forecasting model predicting future emissions trends (e.g., 'Based on current trajectory, Scope 2 emissions are projected to increase by X% next quarter...'). Be predictive and forward-looking, rather than just summarizing."
          elif report_type == "carbon-reduction":
              prompt += "Analyze the following JSON data and provide 2 specific, smart, actionable recommendations to lower the carbon footprint and optimize supply chain efficiency."
          elif report_type == "compliance-risk":
              prompt += "Analyze the following JSON data and provide a 2-sentence proactive AI analysis of potential compliance risks or audit gaps. Warn about upcoming risks based on the current open issues or lack of policies."
          elif report_type == "smart-recommendations":
              prompt += "Analyze the following JSON data and provide 2 tailored operational recommendations to improve diversity metrics, governance policies, and community impact."
          else:
              prompt += f"Write an extremely short and concise (1-2 sentence) executive summary of the following {report_type} report JSON data. Be factual, do not invent numbers."
          
          prompt += f"\\n\\nData: {json.dumps(data, default=str)[:6000]}"'''

code = re.sub(r'prompt = \(\s*"You are an ESG reporting assistant.*?f"\{json\.dumps\(data, default=str\)\[:6000\]\}"\s*\)', new_prompt, code, flags=re.DOTALL)

with open('ai/reports.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Prompt fixed")
