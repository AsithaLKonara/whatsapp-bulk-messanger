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
    page.wait_for_selector('footer', timeout=60000)
    time.sleep(5)
    
    print("Trying to set files...")
    page.set_input_files('input[accept="image/*"]', "0528(3).mp4")
    
    print("Waiting for caption box...")
    try:
        page.wait_for_selector('div[aria-placeholder="Add a caption"]', timeout=30000)
        print("SUCCESS! Media preview loaded.")
    except Exception as e:
        print("FAILED to load media preview.")
            
    browser.close()
