# backend/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from detection.detector import AIDetector
from gnn.gnn_mapper import DisinfoGNN
from forensics.attribution import AttributionEngine
from blockchain.ledger import ThreatLedger

app = FastAPI(title="AEGIS-X API")
detector = AIDetector()
gnn = DisinfoGNN()
attributor = AttributionEngine()
ledger = ThreatLedger()

class TextInput(BaseModel):
    text: str
    lang: str = "en"

@app.post("/analyze")
def analyze(input: TextInput):
    # 1. Detection
    detection = detector.predict(input.text, input.lang)
    
    # 2. Attribution
    model, score = attributor.match_model(input.text)
    has_watermark = attributor.generate_watermark_check(input.text)
    
    # 3. Blockchain log
    content_hash = hashlib.sha256(input.text.encode()).hexdigest()
    block_hash = ledger.log_detection(content_hash, detection["confidence"], model)
    
    # 4. GNN Graph (simulate)
    graph = gnn.simulate_graph("post_0")
    
    return {
        "detection": detection,
        "attribution": {
            "model": model,
            "match_score": score,
            "watermark_detected": has_watermark
        },
        "blockchain": {
            "content_hash": content_hash,
            "block_hash": block_hash
        },
        "propagation_graph": graph
    }