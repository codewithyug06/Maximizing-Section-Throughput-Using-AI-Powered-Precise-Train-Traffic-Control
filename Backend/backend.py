# backend/detection/detector.py
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.stats import entropy
import numpy as np

class AIDetector:
    def __init__(self):
        # English detector (RoBERTa fine-tuned on AI vs Human)
        self.en_pipe = pipeline("text-classification", 
                                model="roberta-base-openai-detector",
                                tokenizer="roberta-base-openai-detector")
        
        # Indian languages (IndicBERT)
        self.indic_tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-bert")
        self.indic_model = AutoModelForSequenceClassification.from_pretrained("aegis-x/indic-ai-detector")
        
    def _stylometric_features(self, text):
        tokens = text.split()
        if len(tokens) == 0: return 0, 0
        freq = np.array([tokens.count(t) for t in set(tokens)])
        prob = freq / freq.sum()
        ent = entropy(prob)
        burst = np.std([len(w) for w in tokens])
        return float(ent), float(burst)
    
    def predict(self, text: str, lang: str = "en"):
        # Stylometric fallback
        ent, burst = self._stylometric_features(text)
        if ent < 3.0 or burst < 2.0:
            stylometric_score = 0.9
        else:
            stylometric_score = 0.3

        if lang == "en":
            res = self.en_pipe(text[:512])
            ai_score = res[0]['score'] if res[0]['label'] == 'AI' else 1 - res[0]['score']
        else:
            inputs = self.indic_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                logits = self.indic_model(**inputs).logits
                probs = torch.softmax(logits, dim=1)
                ai_score = probs[0][1].item()  # class 1 = AI

        # Hybrid confidence
        final_score = 0.7 * ai_score + 0.3 * stylometric_score
        return {
            "is_ai": final_score > 0.5,
            "confidence": round(final_score, 3),
            "entropy": round(ent, 2),
            "burstiness": round(burst, 2)
        }