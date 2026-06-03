from bs4 import BeautifulSoup

with open('preview_dump3.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

buttons = soup.find_all('div', role='button') + soup.find_all('button') + soup.find_all('span', role='button')
for b in buttons:
    label = b.get('aria-label') or b.get('title') or b.get('data-icon')
    text = b.text.strip()
    if label or text:
        print(f"Button: label/title/icon='{label}', text='{text}'")

