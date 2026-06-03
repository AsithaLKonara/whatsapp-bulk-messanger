import csv
import sys
import os

input_file = '/Users/asithalakmal/Documents/leads/gmap_qualified_leads.csv'
output_dir = '/Users/asithalakmal/Documents/leads/categorized_leads'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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

# Grouping logic
categories = {
    'hotels': ['hotel', 'boutique hotel', 'resort', 'inn', 'lodge', 'homestay', 'villa', 'guest house'],
    'salons': ['salon', 'beauty salon'],
    'dentals': ['dental clinic'],
    'cafe_restaurants': ['cafe', 'restaurant'],
    'tuition_classes': ['tuition class']
}

def get_category(query):
    query = query.lower().split(' in ')[0].strip()
    for cat_name, keywords in categories.items():
        if query in keywords:
            return cat_name
    return 'others'

files = {}
writers = {}
seen = {}

try:
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            phone = row.get('Phone', '').strip()
            website = row.get('Website', '').strip()
            name = row.get('Business Name', '').strip()
            query = row.get('Search Query', '').strip()
            
            if phone and phone.lower() != 'n/a':
                if is_allowed_website(website):
                    cat_name = get_category(query)
                    
                    if cat_name not in files:
                        files[cat_name] = open(os.path.join(output_dir, f"{cat_name}.csv"), mode='w', encoding='utf-8', newline='')
                        writers[cat_name] = csv.DictWriter(files[cat_name], fieldnames=['Business Name', 'Phone'])
                        writers[cat_name].writeheader()
                        seen[cat_name] = set()
                    
                    key = (name, phone)
                    if key not in seen[cat_name]:
                        seen[cat_name].add(key)
                        writers[cat_name].writerow({'Business Name': name, 'Phone': phone})

    print("Successfully separated leads into categories:")
    for cat, s in seen.items():
        print(f" - {cat}.csv: {len(s)} leads")

finally:
    for f in files.values():
        f.close()
