# evaluate.py

import json
from analyzer import analyze_proverb
from rouge_score import rouge_scorer
from bert_score import score as bert_score_calculator

def evaluate_performance():
    # This variable will point to our data source.
    # We will change it once in this process.
    EVALUATION_FILE = 'gold_standard_evaluation_set.json'    
    try:
        with open(EVALUATION_FILE, 'r', encoding='utf-8') as f:
            evaluation_data = json.load(f)
    except FileNotFoundError:
        print(f"FATAL ERROR: '{EVALUATION_FILE}' could not be found.")
        return
    except json.JSONDecodeError:
        print(f"FATAL ERROR: '{EVALUATION_FILE}' is not a valid JSON file.")
        return

    all_ai_meanings = []
    all_ideal_meanings = []
    
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    
    print(f"\nProcessing {len(evaluation_data)} proverbs from '{EVALUATION_FILE}'...")

    for i, proverb in enumerate(evaluation_data):
        print(f"  - Processing Proverb {i+1}/{len(evaluation_data)}: {proverb['proverb_gurmukhi']}")

        ai_parsed_data = analyze_proverb(proverb['proverb_gurmukhi'], proverb['literal_translation'])
        ideal_analysis = proverb.get('ideal_analysis')
        
        if "error" not in ai_parsed_data and ideal_analysis:
            ideal_meaning = ideal_analysis.get("meaning", "")
            ai_meaning = ai_parsed_data.get("actual_translation", "")
            
            if ideal_meaning and ai_meaning:
                all_ideal_meanings.append(ideal_meaning)
                all_ai_meanings.append(ai_meaning)
        else:
            print(f"  -> WARNING: Skipping proverb ID {proverb.get('id')} due to an error in analysis.")

    if not all_ai_meanings:
        print("\nNo valid proverb analyses were generated. Cannot run evaluation.")
        return

    print("\n\n" + "="*20 + " Evaluation Results " + "="*20)

    total_rouge_l_f1 = 0
    for ideal, ai in zip(all_ideal_meanings, all_ai_meanings):
        rouge_scores = scorer.score(ideal, ai)
        total_rouge_l_f1 += rouge_scores['rougeL'].fmeasure
    
    average_rouge_l_f1 = (total_rouge_l_f1 / len(all_ideal_meanings)) * 100
    print("\n--- ROUGE Score ---")
    print(f"Average ROUGE-L (F1-Score): {average_rouge_l_f1:.2f}%")

    print("\n--- BERTScore ---")
    (P, R, F1) = bert_score_calculator(all_ai_meanings, all_ideal_meanings, lang="en", model_type='microsoft/deberta-xlarge-mnli', verbose=True)
    
    print(f"\nAverage BERTScore Precision: {P.mean()*100:.2f}%")
    print(f"Average BERTScore Recall:    {R.mean()*100:.2f}%")
    print(f"Average BERTScore F1-Score:  {F1.mean()*100:.2f}%")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    evaluate_performance()