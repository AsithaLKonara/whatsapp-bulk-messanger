import time
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    user_data_dir = os.path.join(os.getcwd(), "whatsapp_session")
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,  # VERY IMPORTANT: headless=False so WhatsApp works!
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/send?phone=94768521562")
    
    print("Waiting for chat to load...")
    page.wait_for_selector('footer', timeout=60000)
    time.sleep(5)
    
    print("Finding all buttons in footer...")
    buttons = page.query_selector_all('footer button, footer div[role="button"]')
    for b in buttons:
        title = b.get_attribute("title")
        aria_label = b.get_attribute("aria-label")
        inner = b.inner_html()
        print(f"Button: title={title}, aria-label={aria_label}, inner HTML length={len(inner)}")
        # If it has an SVG, let's get the data-icon
        svg = b.query_selector('svg, span')
        if svg:
            print(f"  Icon: {svg.get_attribute('data-icon')}")
            
    browser.close()
