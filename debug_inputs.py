import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    user_data_dir = os.path.join(os.getcwd(), "whatsapp_session")
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=["--no-sandbox"]
    )
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/send?phone=94768521562")
    page.wait_for_selector('footer', timeout=60000)
    
    # Get all file inputs
    inputs = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('input[type="file"]')).map(i => i.accept);
    }''')
    print("File Inputs:", inputs)
    browser.close()
