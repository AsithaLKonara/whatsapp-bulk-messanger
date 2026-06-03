import csv
import time
import os
import re
from playwright.sync_api import sync_playwright

# ================= CONFIGURATION =================

# Path to the CSV file you want to use
CSV_FILE_PATH = "/Users/asithalakmal/Documents/leads/categorized_leads/hotels.csv"

# TEST MODE: Set this to True to test sending to your numbers first. Set to False to send to the full CSV.
TEST_MODE = False
TEST_NUMBERS = [
    {'name': 'Asitha Test 1', 'phone': '94768521562'},
    {'name': 'Asitha Test 2', 'phone': '94715484520'}
]

# The video file you want to attach
VIDEO_FILE_PATH = None

import glob

# Load all message templates from the templates directory
TEMPLATE_FILES = glob.glob("/Users/asithalakmal/Documents/leads/templates/*.md")
if not TEMPLATE_FILES:
    # Fallback to the original file if the directory is empty
    TEMPLATE_FILES = ["/Users/asithalakmal/Documents/leads/message template.md"]


# The base delay between sending messages in seconds (e.g., 420 seconds = 7 minutes)
DELAY_BETWEEN_MESSAGES = 420

# =================================================

def format_phone_number(phone):
    """
    Format the phone number to WhatsApp's required format.
    Assumes Sri Lankan numbers starting with 0 (e.g., 077 123 4567 -> 94771234567)
    """
    phone = re.sub(r'\D', '', phone) # Remove non-numeric characters
    if phone.startswith('0'):
        phone = '94' + phone[1:]
    elif not phone.startswith('94') and len(phone) == 9:
        phone = '94' + phone
    return phone

def send_whatsapp_messages():
    # Load leads from CSV
    leads = []
    
    if TEST_MODE:
        leads = TEST_NUMBERS
        print(f"TEST MODE IS ON. Loaded {len(leads)} test numbers.")
    else:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Phone'] and row['Phone'].lower() != 'n/a':
                    leads.append({
                        'name': row.get('Business Name', 'there'),
                        'phone': format_phone_number(row['Phone'])
                    })
        print(f"Loaded {len(leads)} leads from {CSV_FILE_PATH}.")

    # Start Playwright
    with sync_playwright() as p:
        # Use a persistent context so you don't have to scan the QR code every time
        user_data_dir = os.path.join(os.getcwd(), "whatsapp_session")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False, # Must be False to see what's happening
            channel="chrome",
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        page = browser.new_page()
        print("Opening WhatsApp Web. If you are not logged in, please scan the QR code now.")
        page.goto("https://web.whatsapp.com/")
        
        # Wait for the user to scan the QR code (wait for the chat list to appear)
        try:
            # We wait for the main chat list container to appear, which confirms login
            page.wait_for_selector('div#pane-side', timeout=180000)
            print("Successfully logged into WhatsApp Web!")
        except:
            print("Timeout waiting for WhatsApp to load. Did you scan the QR code? Exiting.")
            return

        for idx, lead in enumerate(leads):
            import random
            print(f"[{idx+1}/{len(leads)}] Preparing message for {lead['name']} ({lead['phone']})...")
            
            # Select a random template file
            template_path = random.choice(TEMPLATE_FILES)
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()
            
            # Format the message
            message = f"Hi {lead['name']},\n\n" + template_content
            
            # Navigate to the specific chat via URL
            url = f"https://web.whatsapp.com/send?phone={lead['phone']}"
            page.goto(url)
            
            # Wait for the chat to load or for an invalid number alert
            try:
                # Wait until the message input box is visible
                page.wait_for_selector('div[title="Type a message"], div[aria-placeholder="Type a message"], div[data-tab="10"], div[data-tab="11"]', timeout=15000)
            except:
                # Check if it's an invalid number dialog
                invalid_dialog = page.query_selector('text="Phone number shared via url is invalid."')
                if invalid_dialog:
                    print(f"Skipping {lead['phone']} - Invalid WhatsApp number.")
                    # Close the dialog
                    page.click('button[data-testid="popup-controls-ok"]')
                    time.sleep(2)
                    continue
                else:
                    print(f"Could not load chat for {lead['phone']}. Skipping...")
                    continue
            
            time.sleep(2) # Buffer time for the UI to settle
            
            if VIDEO_FILE_PATH and os.path.exists(VIDEO_FILE_PATH):
                # Process for attaching a video
                print("Attaching video via UI click...")
                
                try:
                    # Click the Attach button using the exact latest selectors
                    page.click('button[aria-label="Attach"], div[aria-label="Attach"], span[data-icon="plus"], span[data-icon="plus-rounded"]')
                    time.sleep(1.5)
                    
                    # Click the "Photos & videos" menu item
                    with page.expect_file_chooser() as fc_info:
                        page.click('button[aria-label="Photos & videos"]')
                        
                    file_chooser = fc_info.value
                    file_chooser.set_files(VIDEO_FILE_PATH)
                except Exception as e:
                    print("Failed to attach video via UI:", e)
                    continue
                
                # Wait for the media preview screen to load! 
                print("Waiting for media preview screen to load...")
                time.sleep(8) # Give the UI plenty of time to transition to the preview screen
                
                # We don't need to find the caption box with fragile selectors. 
                # WhatsApp AUTO-FOCUSES the caption box instantly!
                print("Typing message into auto-focused caption box...")
                page.keyboard.insert_text(message)
                time.sleep(2)
                
                # We MUST wait for compression to finish before Enter or Click will work.
                print("Waiting for video compression and hitting Send...")
                sent = False
                for _ in range(30):  # Try for 60 seconds
                    try:
                        # Click the "Send 1 selected" button
                        page.click('div[aria-label^="Send "]', timeout=2000)
                        sent = True
                        break
                    except:
                        try:
                            page.click('span[data-icon="wds-ic-send-filled"]', timeout=1000)
                            sent = True
                            break
                        except:
                            # Fallback to pressing Enter
                            page.keyboard.press('Enter')
                            time.sleep(2)
                            
                if not sent:
                    print("Warning: Send button may not have been clicked, but Enter was pressed.")
                    time.sleep(2)
                
                # IMPORTANT: Wait for the video to fully upload before moving on!
                print("Waiting for video to fully upload (this may take a few minutes)...")
                try:
                    # Wait up to 5 minutes for the 'clock' icon to disappear, meaning it's sent
                    page.wait_for_selector('span[data-icon="msg-time"]', state="hidden", timeout=300000)
                    print("Upload complete! Message sent.")
                except Exception as e:
                    print("Could not verify if upload finished, or it took too long.")
                
            else:
                # Process for sending text only
                print("No video found, sending text only...")
                try:
                    page.focus('div[title="Type a message"], div[aria-placeholder="Type a message"], div[data-tab="10"], div[data-tab="11"]')
                except:
                    page.click('div[title="Type a message"], div[aria-placeholder="Type a message"], div[data-tab="10"], div[data-tab="11"]', force=True)
                
                page.keyboard.insert_text(message)
                time.sleep(1)
                # Click send button or press enter
                page.keyboard.press('Enter')
            
            import random
            if TEST_MODE:
                total_delay = 45 # 45 seconds is needed to allow a 35MB video to upload before navigating away!
            
            # If we've sent 25 messages, take a long break to avoid bans
            if (idx + 1) % 25 == 0 and (idx + 1) != len(leads):
                long_break = random.uniform(1800, 2400) # 30 to 40 minutes break
                print(f"*** BATCH LIMIT REACHED: Taking a {int(long_break/60)} minute cooling break... ***")
                time.sleep(long_break)
            
            # Wait between 4 to 6 minutes (240 to 360 seconds) to avoid getting banned
            wait_time = random.uniform(240, 360)
            print(f"Waiting {int(wait_time/60)} minutes and {int(wait_time%60)} seconds before next lead to prevent bans...")
            time.sleep(wait_time)
            
        print("\nFinished sending messages to all leads.")
        print("Waiting 60 seconds before closing to ensure all background tasks in WhatsApp finish...")
        time.sleep(60)
        
        browser.close()

if __name__ == "__main__":
    send_whatsapp_messages()
