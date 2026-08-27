import re

content = open(r'D:\Code2026\tcg-embedding-service\app\static\index.html', 'r', encoding='utf-8').read()

# 1. Add CSS for card image thumbnail
old_css = '.top5-item:first-child .top5-rank { color: var(--accent); font-size: 14px; }'
new_css = old_css + '\n.top5-item img { width: 48px; height: 48px; object-fit: cover; border-radius: 4px; background: var(--bg); border: 1px solid var(--border); flex-shrink: 0; }'
content = content.replace(old_css, new_css)

open(r'D:\Code2026\tcg-embedding-service\app\static\index.html', 'w', encoding='utf-8').write(content)
print('Done - CSS')
import re

content = open(r'D:\Code2026\tcg-embedding-service\app\static\index.html', 'r', encoding='utf-8').read()

# 1. Add CSS for card image thumbnail
old_css = '.top5-item:first-child .top5-rank { color: var(--accent); font-size: 14px; }'
new_css = old_css + '\n.top5-item img { width: 48px; height: 48px; object-fit: cover; border-radius: 4px; background: var(--bg); border: 1px solid var(--border); flex-shrink: 0; }'
content = content.replace(old_css, new_css)

# 2. Add image tag in the JS template
old_js = "'<span class=\"top5-rank\">#' + r.rank + '</span>' +"
new_js = old_js + "\n        '<img src=\"/v1/images/' + encodeURIComponent(r.card_id) + '\" alt=\"' + escapeHtml(r.card_id) + '\" loading=\"lazy\" onerror=\"this.style.display=\\'none\\'\">' +"
content = content.replace(old_js, new_js)

open(r'D:\Code2026\tcg-embedding-service\app\static\index.html', 'w', encoding='utf-8').write(content)
print('Done')
