import time
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
    
    page.wait_for_selector('button[aria-label="Attach"], div[aria-label="Attach"], span[data-icon="plus-rounded"]', timeout=60000)
    time.sleep(5)
    
    # Click Attach
    page.click('button[aria-label="Attach"], div[aria-label="Attach"], span[data-icon="plus-rounded"]')
    time.sleep(2)
    
    # Dump entire body to find the menu
    menu_html = page.evaluate('''() => {
        let menu = document.querySelector('ul') || document.querySelector('[role="menu"]');
        return menu ? menu.innerHTML : document.body.innerHTML;
    }''')
    
    with open("menu_dump.html", "w") as f:
        f.write(menu_html)
        
    print("Dumped menu HTML successfully.")
    browser.close()
