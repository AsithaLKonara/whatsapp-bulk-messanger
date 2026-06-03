import time
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    user_data_dir = os.path.join(os.getcwd(), "whatsapp_session")
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=True, 
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/send?phone=94768521562")
    
    # Wait for the chat text box to load
    page.wait_for_selector('div[title="Type a message"], div[aria-placeholder="Type a message"], div[data-tab="10"], div[data-tab="11"]', timeout=60000)
    time.sleep(5)
    
    # Dump the HTML
    html = page.content()
    with open("whatsapp_dump.html", "w") as f:
        f.write(html)
    
    print("Dumped WhatsApp HTML successfully.")
    browser.close()
