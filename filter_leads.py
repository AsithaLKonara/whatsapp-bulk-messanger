import csv
import sys

input_file = '/Users/asithalakmal/Documents/leads/gmap_qualified_leads.csv'
output_file = '/Users/asithalakmal/Documents/leads/filtered_leads.csv'

allowed_keywords = [
    'booking', 'facebook', 'whatsapp', 'instagram', 'agoda', 'bluepillow',
    'freecancellations', 'vrbo', 'expedia', 'decolar', 'zenhotels', 
    'cloudbeds', 'channelmanager', 'travelnest', 'airbnb', 'tripadvisor',
    'makemytrip', 'twitter', 'linkedin', 'tiktok', 'youtube'
]

def is_allowed_website(website):
    website_lower = website.lower()
    if website_lower == 'n/a' or website_lower == '' or website_lower == 'null':
        return True
    
    for kw in allowed_keywords:
        if kw in website_lower:
            return True
            
    return False

filtered_leads = []
seen = set()

with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        phone = row.get('Phone', '').strip()
        website = row.get('Website', '').strip()
        name = row.get('Business Name', '').strip()
        
        if phone and phone.lower() != 'n/a':
            if is_allowed_website(website):
                # Optionally dedup by name + phone
                key = (name, phone)
                if key not in seen:
                    seen.add(key)
                    filtered_leads.append({'Business Name': name, 'Phone': phone})

with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['Business Name', 'Phone'])
    writer.writeheader()
    writer.writerows(filtered_leads)

print(f"Processed leads. Found {len(filtered_leads)} matching leads.")
