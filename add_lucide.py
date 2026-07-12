import glob

for filepath in glob.glob('frontend/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'lucide@latest' not in html:
        html = html.replace('</body>', '<script src=\"https://unpkg.com/lucide@latest\"></script>\n<script>lucide.createIcons();</script>\n</body>')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
print('Lucide JS added!')
