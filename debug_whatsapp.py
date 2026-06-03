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
    
    # Wait for the chat to load
    page.wait_for_selector('div#main', timeout=60000)
    time.sleep(5)
    
    # Get the HTML of the footer area where the attach button is
    footer_html = page.evaluate('document.querySelector("footer").innerHTML')
    with open("footer_dump.html", "w") as f:
        f.write(footer_html)
    
    print("Dumped footer HTML successfully.")
    browser.close()
