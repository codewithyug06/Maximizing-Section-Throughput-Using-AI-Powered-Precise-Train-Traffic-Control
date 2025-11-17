# backend/forensics/attribution.py
import hashlib
import pickle
import os

class AttributionEngine:
    def __init__(self, fingerprint_path="data/model_fingerprints.pkl"):
        with open(fingerprint_path, "rb") as f:
            self.signatures = pickle.load(f)  # {model_name: avg_token_dist}

    def extract_token_signature(self, text):
        tokens = text.lower().split()
        vocab = set(tokens)
        return {w: tokens.count(w)/len(tokens) for w in list(vocab)[:50]}

    def match_model(self, text):
        query_sig = self.extract_token_signature(text)
        best_match, best_score = "Unknown", 0.0
        for model, sig in self.signatures.items():
            score = sum(abs(query_sig.get(w, 0) - sig.get(w, 0)) for w in set(query_sig) | set(sig))
            if score > best_score:
                best_score, best_match = score, model
        return best_match, round(best_score, 3)

    def generate_watermark_check(self, text):
        # Simulate cryptographic watermark (real: use OpenAI-style watermark)
        h = hashlib.sha256(text.encode()).hexdigest()
        return h[-4:] in ["a1b2", "c3d4", "e5f6"]  # fake watermark presence