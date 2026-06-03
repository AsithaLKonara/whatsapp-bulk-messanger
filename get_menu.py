import time
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    user_data_dir = os.path.join(os.getcwd(), "whatsapp_session")
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/send?phone=94768521562")
    
    page.wait_for_selector('button[aria-label="Attach"], div[aria-label="Attach"]', timeout=60000)
    time.sleep(2)
    
    # Click Attach
    page.click('button[aria-label="Attach"], div[aria-label="Attach"]')
    time.sleep(2)
    
    # Dump menu HTML
    buttons = page.query_selector_all('ul li')
    for b in buttons:
        inner = b.inner_text()
        print(f"Menu Item: {inner.strip()}")
        svg = b.query_selector('svg, span')
        if svg:
            print(f"  Icon: {svg.get_attribute('data-icon')}")
            
    # Also find inputs
    inputs = page.query_selector_all('input[type="file"]')
    for i in inputs:
        print(f"File Input Accept: {i.get_attribute('accept')}")
            
    browser.close()
