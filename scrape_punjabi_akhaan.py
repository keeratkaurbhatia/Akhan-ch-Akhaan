import requests
from bs4 import BeautifulSoup
import json
import time
import os

BASE_URL = "https://punjabi.com/akhaan"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Correct akhar list from the website (excluding "ਸਭ")
akhar_list = [
    "ੳ", "ਅ", "ੲ",
    "ਸ", "ਹ",
    "ਕ", "ਖ", "ਗ", "ਘ",
    "ਚ", "ਛ", "ਜ", "ਝ",
    "ਟ", "ਠ", "ਡ", "ਢ",
    "ਤ", "ਥ", "ਦ", "ਧ", "ਨ",
    "ਪ", "ਫ", "ਬ", "ਭ",
    "ਮ", "ਯ", "ਰ", "ਲ", "ਵ"
]

def fetch_page(letter, page):
    url = f"{BASE_URL}?category={letter}&page={page}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, "html.parser")

def extract_proverbs(soup):
    proverbs = []
    containers = soup.find_all("h2", class_="card-title")
    for c in containers:
        text = c.get_text(strip=True)
        if text:
            # Get only the part before dash (meaning removal)
            proverb = text.split("–")[0].strip()  # en dash
            proverb = proverb.split("-")[0].strip()  # fallback hyphen
            if proverb:
                proverbs.append(proverb)
    return proverbs

def save_to_json(data, filename="punjabi_proverbs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def scrape_all():
    all_proverbs = []
    id_counter = 1

    for letter in akhar_list:
        print(f"🔡 Starting letter '{letter}'")
        page = 1
        letter_proverbs = []

        while True:
            soup = fetch_page(letter, page)
            if soup is None:
                break

            extracted = extract_proverbs(soup)
            if not extracted:
                break

            for p in extracted:
                letter_proverbs.append({
                    "id": id_counter,
                    "proverb_gurmukhi": p,
                    "literal_translation": ""
                })
                id_counter += 1

            print(f"✓ Scraped {len(extracted)} from letter '{letter}' page {page}")
            page += 1
            time.sleep(1)  # Respectful delay

        all_proverbs.extend(letter_proverbs)

        # ✅ Save to file after each letter
        save_to_json(all_proverbs)
        print(f"💾 Saved {len(letter_proverbs)} proverbs from letter '{letter}'\n")

    print(f"\n✅ Done! Total proverbs scraped: {len(all_proverbs)}")

if __name__ == "__main__":
    scrape_all()
