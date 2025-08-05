import json

PROVERBS_FILE = 'punjabi_proverbs.json'
CACHE_FILE = 'analysis_cache_final_direct_meaning.json'
FINAL_APP_DATA_FILE = 'proverbs_app_data.json' # Final file for the Streamlit app

def merge_data():
    """
    Combines the base proverbs with their AI analysis from the cache
    into a single file ready for the Streamlit application.
    """
    try:
        with open(PROVERBS_FILE, 'r', encoding='utf-8') as f:
            proverbs_base = json.load(f)

        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            analysis_cache = json.load(f)
    except FileNotFoundError as e:
        print(f"ERROR: Could not find a required file: {e}. Please run the scraper and analyzer first.")
        return

    merged_list = []
    for proverb in proverbs_base:
        gurmukhi_key = proverb['proverb_gurmukhi']
        analysis = analysis_cache.get(gurmukhi_key)
        
        # Only include proverbs that have a successful analysis
        if analysis and "error" not in analysis:
            proverb['analysis'] = analysis
            merged_list.append(proverb)

    with open(FINAL_APP_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(merged_list, f, indent=2, ensure_ascii=False)
        
    print(f"Success! Merged {len(merged_list)} proverbs with analysis into '{FINAL_APP_DATA_FILE}'")

if __name__ == "__main__":
    merge_data()