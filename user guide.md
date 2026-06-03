# Smart Hotel OS Lead Sender - User Guide

This guide explains how to use the automated WhatsApp sender for reaching out to your hotel leads.

## ⚠️ Important Rule: Maximum Contacts Per Day
To avoid your WhatsApp account being restricted or banned by WhatsApp for spam, **you MUST limit your messages to a maximum of 40 contacts per day.** Sending too many messages in a short period of time to people who haven't saved your number can result in your number getting blocked.

---

## 1. Preparing Your Leads

1. Open the **`sample.csv`** file in Excel or Google Sheets.
2. The file must contain at least two columns:
   - **`Business Name`**: The name of the hotel, villa, or resort.
   - **`Phone`**: The WhatsApp number of the lead (e.g., `0771234567` or `+94771234567`).
3. Add your daily leads into this file (ensure it does not exceed 40 leads per day).
4. Save the file as a **CSV** (Comma Separated Values).

## 2. Setting Up Your Message

1. Open the **`message template.md`** file.
2. This file contains the message that will be sent to the leads. You can edit the text here if you need to update the promotional content.
3. Make sure not to change the formatting too drastically if you rely on bolding (`*text*`) or emojis.
4. Save the file when you are done.

## 3. Running the Automation

Depending on your workflow, you have a few scripts available in your folder:

- **Filter Leads**: You can run `python filter_leads.py` if you need to clean up and filter your raw leads before sending.
- **Split Leads**: You can run `python split_leads.py` to break down large lead lists into smaller files (ideal for separating them into chunks of 40 per day).
- **Send Messages**: Run `python whatsapp_sender.py` to start the actual sending process.

### Step-by-Step Execution:
1. Open your Terminal (Mac).
2. Navigate to your leads folder:
   ```bash
   cd ~/Documents/leads
   ```
3. Run the sender script:
   ```bash
   python whatsapp_sender.py
   ```
4. The script will likely open a Chrome window and ask you to scan a WhatsApp Web QR code the first time.
5. Once logged in, the script will automatically read your CSV file and start sending the `message template.md` to the contacts listed.

## 4. Best Practices

- **Warm up your number**: If this is a new WhatsApp number, start by sending only 10-15 messages a day and slowly increase it to 40 over a few weeks.
- **Engage with replies**: If a lead replies, reply back manually. WhatsApp algorithms favor accounts that have real two-way conversations.
- **Clear out invalid numbers**: If you notice a number does not have WhatsApp, remove it from your future lists to keep a clean send rate.
