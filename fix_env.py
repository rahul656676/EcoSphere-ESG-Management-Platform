import re

with open('frontend/environmental.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure each panel toolbar has a refresh button
html = re.sub(r'(<div class=\"toolbar\">.*?<button class=\"btn btn-green\".*?>\+ New Emission Factor</button>)', r'\1\n              <button class=\"btn btn-outline\" onclick=\"loadFactors()\"><i data-lucide=\"refresh-cw\" class=\"icon\"></i></button>', html)

html = re.sub(r'(<div class=\"toolbar\">.*?<button class=\"btn btn-green\".*?>\+ New Product Profile</button>)', r'\1\n              <button class=\"btn btn-outline\" onclick=\"loadProducts()\"><i data-lucide=\"refresh-cw\" class=\"icon\"></i></button>', html)

html = re.sub(r'(<div class=\"toolbar\">.*?<button class=\"btn btn-green\".*?>\+ Log Carbon Data</button>)', r'\1\n              <button class=\"btn btn-outline\" onclick=\"loadCarbon()\"><i data-lucide=\"refresh-cw\" class=\"icon\"></i></button>', html)

with open('frontend/environmental.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("environmental.html fixed")
