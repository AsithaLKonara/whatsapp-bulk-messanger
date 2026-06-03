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
    
    page.wait_for_selector('footer', timeout=60000)
    time.sleep(5)
    
    # Create a tiny dummy image
    with open("dummy.png", "wb") as f:
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    
    # Click Attach
    page.click('button[aria-label="Attach"], div[aria-label="Attach"], span[data-icon="plus-rounded"]')
    time.sleep(2)
    
    # Click Photos & videos
    with page.expect_file_chooser() as fc_info:
        page.click('button[aria-label="Photos & videos"]')
    fc_info.value.set_files("dummy.png")
    
    # Wait for the media preview to load (Send button is a good indicator)
    print("Waiting for send button...")
    page.wait_for_selector('span[data-icon="send"]', timeout=30000)
    time.sleep(2)
    
    # Dump entire body
    html = page.evaluate('document.body.innerHTML')
    with open("preview_dump.html", "w") as f:
        f.write(html)
        
    print("Dumped preview HTML successfully.")
    browser.close()
