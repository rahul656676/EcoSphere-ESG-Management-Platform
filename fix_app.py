import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

new_search_logic = '''
  window.globalSearchMenu = function(query) {
    const q = query.toLowerCase();
    
    // First, reset everything if query is empty
    if (!q) {
      document.querySelectorAll('.sidebar-nav-item').forEach(el => el.style.display = '');
      document.querySelectorAll('.sidebar-sub a').forEach(el => el.style.display = '');
      document.querySelectorAll('.sidebar-sub').forEach(el => el.style.display = '');
      return;
    }

    document.querySelectorAll('.sidebar-nav-item').forEach(item => {
      let text = item.textContent.toLowerCase();
      let hasMatch = text.includes(q);
      
      // Check if any sub-item matches
      let nextEl = item.nextElementSibling;
      if (nextEl && nextEl.classList.contains('sidebar-sub')) {
        let subMatches = false;
        nextEl.querySelectorAll('a').forEach(sub => {
          if (sub.textContent.toLowerCase().includes(q)) {
            sub.style.display = '';
            subMatches = true;
          } else {
            sub.style.display = 'none';
          }
        });
        
        if (subMatches) {
          hasMatch = true;
          nextEl.style.display = 'flex'; // Ensure sub-menu is open if child matches
        } else {
          nextEl.style.display = 'none';
        }
      }
      
      item.style.display = hasMatch ? '' : 'none';
    });
  };
'''

app_js = re.sub(r'window\.globalSearchMenu = function.*?};\n', new_search_logic, app_js, flags=re.DOTALL)

# Also fix bell icon notification
app_js = app_js.replace('<button class=\"topbar-btn\" title=\"Notifications\">', '<button class=\"topbar-btn\" title=\"Notifications\" onclick=\"toast(\'No new notifications\', false)\">')

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
print("app.js fixed")
