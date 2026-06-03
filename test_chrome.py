import time
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    user_data_dir = os.path.join(os.getcwd(), "whatsapp_session")
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        channel="chrome",
        args=["--no-sandbox"]
    )
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/send?phone=94768521562")
    
    page.wait_for_selector('footer', timeout=60000)
    time.sleep(5)
    
    # Click Attach
    page.click('button[aria-label="Attach"], div[aria-label="Attach"], span[data-icon="plus-rounded"]')
    time.sleep(2)
    
    # Click Photos & videos
    with page.expect_file_chooser() as fc_info:
        page.click('button[aria-label="Photos & videos"]')
    fc_info.value.set_files("0528(3).mp4")
    
    print("Waiting 15 seconds for video to load into preview...")
    time.sleep(15)
    
    # Dump entire body
    html = page.evaluate('document.body.innerHTML')
    with open("preview_dump3.html", "w") as f:
        f.write(html)
        
    print("Dumped preview HTML successfully.")
    browser.close()
