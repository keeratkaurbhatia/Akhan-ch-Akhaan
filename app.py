# app.py
# Final corrected version for Streamlit deployment.

import streamlit as st
from aksharamukha import transliterate
from thefuzz import process
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="ਅੱਖਾਂ 'ਚ ਅਖਾਣ",
    page_icon="👁️",
    layout="centered"
)

# --- Functions ---
@st.cache_data
def load_and_prepare_data(file_path):
    """Loads proverbs from JSON and transliterates them."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for p in data:
            if 'transliteration_iast' not in p:
                p['transliteration_iast'] = transliterate.process('Gurmukhi', 'IAST', p['proverb_gurmukhi'])
        return data
    except FileNotFoundError:
        return []

# --- Main App Interface ---
st.title("👁️ ਅੱਖਾਂ 'ਚ ਅਖਾਣ")
st.caption("Ancient wisdom through a modern lens.")

# Correctly loads the final, merged data file.
proverbs_list = load_and_prepare_data('proverbs_app_data.json')

if not proverbs_list:
    st.error("Could not load `proverbs_app_data.json`. Please ensure this file is in your GitHub repository.")
else:
    iast_to_proverb_map = {p['transliteration_iast']: p for p in proverbs_list}
    
    st.divider()

    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("🔎 Search for a Proverb")
        search_query = st.text_input("Type a rough Romanized version:", "")

        if search_query:
            best_matches = process.extract(search_query, iast_to_proverb_map.keys(), limit=3)
            st.write("**Did you mean...?**")
            
            for match, score in best_matches:
                if score > 50:
                    matched_proverb = iast_to_proverb_map[match]
                    
                    st.info(f"**Gurmukhi:** {matched_proverb['proverb_gurmukhi']}\n\n**Romanized:** *{matched_proverb['transliteration_iast']}*")

                    if st.button("Analyze This One", key=matched_proverb['id'], use_container_width=True):
                        st.session_state['selected_proverb'] = matched_proverb
                        st.rerun()
    
    with col2:
        st.subheader("📜 Proverb Analysis")
        if 'selected_proverb' in st.session_state:
            selected = st.session_state['selected_proverb']
            st.info(f"**Selected:** {selected['proverb_gurmukhi']}")

        
            if 'analysis' in selected:
                analysis_data = selected['analysis']
                st.success(f"**Meaning:** {analysis_data.get('actual_translation', 'Meaning not available.')}")
                with st.expander("View Deeper Context & Example"):
                    st.markdown(analysis_data.get('deeper_analysis', "Deeper analysis not available."))
            else:
                st.warning("Analysis data is missing for this proverb in the app data file.")
                
        else:
            st.info("Select a proverb from the search results to see its meaning here.")

