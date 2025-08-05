# 👁️ Akhan 'ch Akhaan — Proverbs in the Eyes
---

### The Story

I used to nod along to Punjabi proverbs I didn’t really understand.

Growing up, **akhaan** (proverbs) were everywhere — in scoldings, advice, and even casual banter. I always knew they meant something deeper... I just didn’t always know what. So I’d nod, smile, pretend I got it, and move on.

Cut to a few weeks ago, when this random thought hit me: *What if I pointed all this AI stuff toward something closer to home?*

So I built a thing. I scraped data from various Punjabi websites, collected over a thousands of proverbs, and began the process of feeding them to a LLaMA 3 model through the Groq API, refining the prompts through countless trials and errors.

### The Name? A Happy Accident.

I Googled "akhaan" (proverbs) — and the search results showed me *eyes*. I thought I was hallucinating from sleep deprivation. Then it clicked:

**ਅਖਾਣ** (proverbs) and **ਅੱਖਾਂ** (eyes) look exactly the same in Roman script: **akhaan**.

Suddenly, the name made perfect sense: **ਅੱਖਾਂ 'ਚ ਅਖਾਣ — Proverbs in our eyes.** Because proverbs really are tiny windows into how a culture sees the world.

---

### 📊 Project Status (Work in Progress)

This project is an active work in progress.
* **Data Processed:** So far, over **650 proverbs** have been successfully analyzed by the AI. The script is still processing the full dataset.
* **Evaluation:** A formal evaluation using NLP metrics is planned but **not yet complete**. The current focus is on completing the AI analysis for the entire dataset.

---

### Features & Tech Stack

* **🧠 AI-Powered Analysis:** Extracts figurative meanings for Punjabi proverbs using **LLaMA 3** via the Groq API and layered prompt engineering.
* **📚 Growing Database:** Currently contains over 650 analyzed proverbs, collected via web scraping with Python (`requests`, `BeautifulSoup`).
* **🔍 Fuzzy Search:** Easily find proverbs in Gurmukhi or Romanized Punjabi (`thefuzz`).
* **🖥️ Full-Stack Application:** Built and deployed entirely with **Python** and **Streamlit**.

---

### What I Learned

* LLM API integration and robust error handling for large-scale data processing.
* Prompt design for extracting culturally nuanced and figurative meanings.
* The fundamentals of creating a gold-standard dataset for future NLP evaluation.
* Full-stack development and deployment using Python and Streamlit.

---

### Limitations & Future Work

This is a solo project and a work in progress. Here's what it can't do (yet):
* **No Shahmukhi Support:** My current knowledge is limited to the Gurmukhi script.
* **Incomplete Database:** The analysis is still running. The goal is to process over 1000+ proverbs.
* **Interpretations May Vary:** AI can miss the mark. User feedback is more than welcome!

---

### Why This Matters

The most meaningful moment of this project was showing it to my family and watching them debate whether the AI "got it right." AI can’t replace cultural wisdom, but maybe it can help keep it alive. Punjabi is just one of many low-resource languages rich in metaphor and knowledge that is often overlooked. This is just a small nudge to help make sure those languages don’t quietly fade out.

I’d love to hear what the AI gets right — and what your *bibi ji* might say instead. :)

---
