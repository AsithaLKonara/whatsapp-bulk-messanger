from bs4 import BeautifulSoup

with open('preview_dump2.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

inputs = soup.find_all(attrs={'contenteditable': 'true'})
for i in inputs:
    print("ContentEditable:", i.get('aria-label') or i.get('aria-placeholder') or i.get('title') or i.get('data-lexical-editor'))

