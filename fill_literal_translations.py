import os
import json
import time
from dotenv import load_dotenv
from groq import Groq, RateLimitError

load_dotenv()

# ---- Setup Groq API ----
try:
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in .env file.")
    client = Groq(api_key=GROQ_API_KEY)
    print("✅ Groq API client configured.")
except Exception as e:
    print(f"FATAL: {e}")
    exit()

# ---- Load JSON ----
INPUT_FILE = "punjabi_proverbs.json"

try:
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"FATAL: File '{INPUT_FILE}' not found.")
    exit()

# ---- Prompt Setup ----
system_prompt = "You are a Punjabi language translator. Translate the following proverb word-for-word from Gurmukhi to English. Do not interpret or explain. Just give the literal translation."

user_template = "Proverb: \"{proverb}\"\nLiteral Translation:"

# ---- Main Loop ----
updated = 0
for entry in data:
    if not entry.get("literal_translation"):
        proverb = entry["proverb_gurmukhi"]
        user_prompt = user_template.format(proverb=proverb)

        print(f"🔍 Translating: {proverb}")

        try:
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            translation = chat_completion.choices[0].message.content.strip()
            entry["literal_translation"] = translation
            updated += 1
            time.sleep(0.5)

        except RateLimitError:
            print("⏳ Rate limit hit. Waiting 10 seconds...")
            time.sleep(10)
            continue
        except Exception as e:
            print(f"⚠️ ERROR for '{proverb}': {e}")
            entry["literal_translation"] = ""

# ---- Save JSON ----
with open(INPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done! Literal translations updated for {updated} proverbs.")
