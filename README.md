# WhatsApp Bulk Messenger 🚀

An automated WhatsApp messaging solution built with Python and Playwright. This tool allows you to send personalized messages to a list of leads from a CSV file directly through WhatsApp Web, without requiring the official WhatsApp Business API.

⚠️ **DISCLAIMER & WARNING:** 
Sending unsolicited bulk messages can result in your WhatsApp account being permanently banned. 
**Always stick to a maximum of 40 contacts per day.** Slowly warm up new numbers. Use at your own risk.

## Features ✨

- **Automated Sending:** Opens WhatsApp Web via Playwright and sends messages automatically.
- **Media Support:** Ability to attach and send a video/image file along with the message caption.
- **Dynamic Templating:** Randomly selects from multiple message templates (`.md` files) to vary your messages and avoid spam detection.
- **Smart Delays:** Implements human-like random delays (4 to 6 minutes) between messages, and takes a 30-40 minute break after every 25 messages.
- **Session Caching:** Saves your WhatsApp Web session locally so you don't have to scan the QR code every time.
- **Lead Management:** Includes utility scripts to filter (`filter_leads.py`) and split (`split_leads.py`) your lead lists.

## Prerequisites 🛠️

- Python 3.8+
- Google Chrome browser installed
- A WhatsApp account (preferably a warmed-up number)

## Installation 📦

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AsithaLKonara/whatsapp-bulk-messanger.git
   cd whatsapp-bulk-messanger
   ```

2. **Install the required Python packages:**
   ```bash
   pip install playwright
   ```

3. **Install the Playwright browsers:**
   ```bash
   playwright install chromium
   ```

## Setup & Usage 🚀

### 1. Prepare your Leads
Add your leads to a CSV file (e.g., `sample.csv`). The file must have at least the following columns:
- `Business Name`: Used for personalization (e.g., "Hi [Business Name],")
- `Phone`: The WhatsApp number (e.g., `0771234567` or `+94771234567`)

*Tip: Use `python split_leads.py` to break down large CSV files into smaller daily chunks of 40 leads.*

### 2. Configure the Sender
Open `whatsapp_sender.py` and configure the following variables at the top of the script:
- `CSV_FILE_PATH`: The path to your active leads CSV.
- `TEST_MODE`: Set to `True` if you want to test the script on your own numbers first.
- `VIDEO_FILE_PATH`: (Optional) Path to a video or image you want to attach. Set to `None` for text-only.

### 3. Edit Message Templates
Place your markdown templates (e.g., `sample_message_template.md`) in the main folder or a `templates/` folder. The script will randomly pick one for each lead to keep your messages unique.

### 4. Run the Script
Execute the script using Python:
```bash
python whatsapp_sender.py
```
*Note: The first time you run this, a Chrome browser will open. You will have 3 minutes to scan the WhatsApp Web QR code using your phone. After logging in, the script will automatically take over.*

## Best Practices to Avoid Bans 🛡️

1. **Limit your volume:** Never send to more than 40 unknown contacts a day.
2. **Warm up new numbers:** Start with 5-10 messages per day and gradually increase over weeks.
3. **Encourage replies:** Your templates should encourage the user to reply (e.g., "Reply 'DEMO' to learn more"). Two-way conversations signal to WhatsApp that you are not a bot.
4. **Vary your messages:** Use the templating feature to send slightly different variations of your message.

## License 📄
This project is provided for educational and internal business automation purposes. Please respect WhatsApp's Terms of Service.
