import re

with open('frontend/ai.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace toast calls on cards with actual functions
html = html.replace('onclick=\"toast(\'Loading predictive models...\', false)\"', '')
html = html.replace('onclick=\"toast(\'Analyzing operational data for reductions...\', false)\"', '')
html = html.replace('onclick=\"toast(\'Scanning regulatory databases...\', false)\"', '')
html = html.replace('onclick=\"toast(\'Fetching tailored recommendations...\', false)\"', '')

# Update buttons to actually call the correct functions
html = html.replace('onclick=\"runAIReport(\'environmental\', this)\"', 'onclick=\"runAIReport(\'future-emissions\', this)\"')
html = html.replace('onclick=\"runAIReport(\'esg-summary\', this)\"', 'onclick=\"runAIReport(\'compliance-risk\', this)\"')

# Wait, there are more buttons. Let's find all buttons and replace them properly.
# The easiest way is to use regex.
html = re.sub(r'<button class=\"btn btn-outline mt-4\".*?>View Forecast.*?</button>', '<button class=\"btn btn-outline mt-4\" style=\"width: 100%; border-color:var(--soc); color:var(--soc)\" onclick=\"runAIReport(\'future-emissions\', this)\">View Forecast <i data-lucide=\"arrow-right\" class=\"icon\" style=\"width:14px;height:14px\"></i></button>', html)
html = re.sub(r'<button class=\"btn btn-outline mt-4\".*?>Get Suggestions.*?</button>', '<button class=\"btn btn-outline mt-4\" style=\"width: 100%; border-color:var(--env); color:var(--env)\" onclick=\"runAIReport(\'carbon-reduction\', this)\">Get Suggestions <i data-lucide=\"arrow-right\" class=\"icon\" style=\"width:14px;height:14px\"></i></button>', html)
html = re.sub(r'<button class=\"btn btn-outline mt-4\".*?>Run Risk Scan.*?</button>', '<button class=\"btn btn-outline mt-4\" style=\"width: 100%; border-color:var(--error); color:var(--error)\" onclick=\"runAIReport(\'compliance-risk\', this)\">Run Risk Scan <i data-lucide=\"arrow-right\" class=\"icon\" style=\"width:14px;height:14px\"></i></button>', html)
html = re.sub(r'<button class=\"btn btn-outline mt-4\".*?>Explore Insights.*?</button>', '<button class=\"btn btn-outline mt-4\" style=\"width: 100%; border-color:var(--gov); color:var(--gov)\" onclick=\"runAIReport(\'smart-recommendations\', this)\">Explore Insights <i data-lucide=\"arrow-right\" class=\"icon\" style=\"width:14px;height:14px\"></i></button>', html)

with open('frontend/ai.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("ai.html fixed")
