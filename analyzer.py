import os
import json
import time
from dotenv import load_dotenv
from groq import Groq, RateLimitError

load_dotenv()

# Configuration
CACHE_FILE = "analysis_cache_final_direct_meaning.json" # Final cache file

# API Key Setup 
try:
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in .env file or environment.")
    client = Groq(api_key=GROQ_API_KEY)
    print("Groq API client configured successfully.")
except Exception as e:
    print(f"FATAL: API Key configuration error: {e}")
    exit()

system_prompt = """You are a wise native speaker explaining Punjabi proverbs to a friend. Your task is to produce a clear analysis in a valid JSON object.

Your entire response must be ONLY the JSON object, with no extra text or markdown.

The JSON must contain two keys:
1. "actual_translation": Provide the simple, direct meaning of the proverb as it is used in everyday conversation. Explain it clearly and concisely, like you would to a friend.
2. "deeper_analysis": Here, you can provide a more detailed paragraph explaining the key symbols, cultural context, and an example of its use.
"""

# Few-shot examples
few_shot_examples = """
---
**EXAMPLE 1**

**Proverb (Gurmukhi):** "ਉਜੜੇ ਬਾਗਾਂ ਦੇ ਗਾਲ੍ਹੜ ਪਟਵਾਰੀ"
**Literal Translation:** "Of the deserted gardens, squirrels are the land-record keepers"

**Analysis JSON:**
{{
  "actual_translation": "It means that when things fall apart, useless or unqualified people take charge.",
  "deeper_analysis": "The proverb powerfully contrasts an important official, the 'Patwari' (land-record keeper), with a common squirrel ('galhaṛ'). It's used to criticize situations where a skilled leader leaves and an incompetent person takes over, creating chaos. For example, if a great project manager quits and their unqualified assistant is promoted, leading to disaster."
}}
---
**EXAMPLE 2**

**Proverb (Gurmukhi):** "ਉੱਚੀ ਦੁਕਾਨ ਫਿੱਕਾ ਪਕਵਾਨ"
**Literal Translation:** "High shop, bland dish"

**Analysis JSON:**
{{
  "actual_translation": "This simply means something looks great on the outside but is disappointing in quality on the inside.",
  "deeper_analysis": "The 'high shop' is a metaphor for anything with a fancy appearance or great marketing, while the 'bland dish' represents the poor quality underneath. People use this all the time for things like a beautiful restaurant that serves bad food, or a movie with amazing trailers that turns out to be boring."
}}
---
"""

user_prompt_template = """
{examples}
**TASK**

**Proverb (Gurmukhi):** "{proverb_gurmukhi}"
**Literal Translation:** "{literal_translation}"

**Required JSON Format:**
{{
  "actual_translation": "The simple, direct meaning for everyday use.",
  "deeper_analysis": "The detailed explanation with symbols and a usage example."
}}
"""

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache_data):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)

def analyze_proverb(proverb_gurmukhi, literal_translation):
    cache = load_cache()
    cache_key = proverb_gurmukhi

    if cache_key in cache and "error" not in cache.get(cache_key, {}):
        print(f"  -> Found in cache: '{proverb_gurmukhi}'")
        return cache[cache_key]

    print(f"  -> Analyzing with Groq API (Llama3-70B, Direct Meaning Prompt): '{proverb_gurmukhi}'")

    max_retries = 5
    base_delay = 5

    for attempt in range(max_retries):
        try:
            user_prompt = user_prompt_template.format(
                examples=few_shot_examples,
                proverb_gurmukhi=proverb_gurmukhi,
                literal_translation=literal_translation
            )
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama3-70b-8192",
                temperature=0.2, # Lower temperature for more directness
                response_format={"type": "json_object"},
            )
            
            response_text = chat_completion.choices[0].message.content
            analysis_data = json.loads(response_text)
            
            cache[cache_key] = analysis_data
            save_cache(cache)
            
            time.sleep(0.5)
            
            return analysis_data
        
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = base_delay * (2 ** attempt)
                print(f"  -> WARNING: Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                error_message = f"API rate limit exceeded after multiple retries: {e}"
                print(f"  -> FATAL: {error_message}")
                cache[cache_key] = {"error": error_message}
                save_cache(cache)
                return {"error": error_message}

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(f"  -> ERROR: {error_message}")
            cache[cache_key] = {"error": error_message}
            save_cache(cache)
            return {"error": error_message}

print("Analyzer function is ready.")


if __name__ == "__main__":
    try:
        with open('punjabi_proverbs.json', 'r', encoding='utf-8') as f:
            all_proverbs = json.load(f)
        print(f"Loaded {len(all_proverbs)} proverbs from punjabi_proverbs.json")
    except FileNotFoundError:
        print("FATAL: 'punjabi_proverbs.json' not found. Please ensure it's in the same directory.")
        exit()
    except json.JSONDecodeError:
        print("FATAL: 'punjabi_proverbs.json' contains invalid JSON.")
        exit()

    # Loop through each proverb and analyze it
    for i, proverb_obj in enumerate(all_proverbs):
        print(f"\n🔄 Processing proverb {i+1}/{len(all_proverbs)}...")
        proverb_gurmukhi = proverb_obj.get('proverb_gurmukhi')
        literal_translation = proverb_obj.get('literal_translation')
        
        if proverb_gurmukhi and literal_translation:
            analyze_proverb(proverb_gurmukhi, literal_translation)
        else:
            print(f"   -> WARNING: Skipping proverb ID {proverb_obj.get('id')} due to missing Gurmukhi or literal translation.")
            
    print("\n\n All proverbs have been processed. The cache is now complete!")