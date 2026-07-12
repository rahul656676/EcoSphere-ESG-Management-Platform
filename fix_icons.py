import glob

icon_map = {
    '??': '<i data-lucide=\"layout-dashboard\"></i>',
    '??': '<i data-lucide=\"leaf\"></i>',
    '??': '<i data-lucide=\"users\"></i>',
    '??': '<i data-lucide=\"scale\"></i>',
    '??': '<i data-lucide=\"trophy\"></i>',
    '?': '<i data-lucide=\"sparkles\"></i>',
    '??': '<i data-lucide=\"file-text\"></i>',
    '??': '<i data-lucide=\"settings\"></i>',
    '??': '<i data-lucide=\"trending-up\"></i>',
    '??': '<i data-lucide=\"alert-triangle\"></i>',
    '??': '<i data-lucide=\"lightbulb\"></i>',
    '?': '<i data-lucide=\"zap\"></i>',
    '??': '<i data-lucide=\"moon\"></i>',
    '??': '<i data-lucide=\"search\"></i>',
    '??': '<i data-lucide=\"factory\"></i>',
    '??': '<i data-lucide=\"car\"></i>',
    '???': '<i data-lucide=\"trash-2\"></i>',
    '??': '<i data-lucide=\"flame\"></i>',
    '??': '<i data-lucide=\"plane\"></i>',
    '??': '<i data-lucide=\"globe\"></i>',
    '??': '<i data-lucide=\"bot\"></i>',
    '??': '<i data-lucide=\"medal\"></i>',
    '?': '<i data-lucide=\"star\"></i>'
}

for filepath in glob.glob('frontend/*.html') + ['frontend/app.js']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for emoji, icon in icon_map.items():
        content = content.replace(emoji, icon)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Icons replaced!')
