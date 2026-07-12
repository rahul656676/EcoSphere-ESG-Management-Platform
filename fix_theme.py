import re

with open('frontend/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

light_theme = '''[data-theme="light"] {
  --bg: #F4FCF4;
  --surface: #E8F5E9;
  --card-bg: #FFFFFF;
  --card-hover: #F9FFF9;
  --sidebar-bg: #FFFFFF;
  --border: #C8E6C9;
  --border-hover: #A5D6A7;
  
  --text-primary: #0F2914;
  --text-secondary: #1B5E20;
  --text-muted: #4CAF50;
  
  /* Make all module accents parrot green to fit the theme */
  --env: #32CD32;
  --soc: #32CD32;
  --gov: #32CD32;
  --gam: #32CD32;
  --rep: #32CD32;
  --primary: #32CD32;
}'''

css = re.sub(r'\[data-theme="light"\]\s*\{[^}]*\}', light_theme, css, flags=re.DOTALL)

with open('frontend/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Theme updated")
