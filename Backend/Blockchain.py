# backend/blockchain/ledger.py
import hashlib
import time
from web3 import Web3

class ThreatLedger:
    def __init__(self):
        # Connect to Ganache (for demo)
        self.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
        self.chain = []

    def log_detection(self, content_hash, confidence, model, timestamp=None):
        entry = {
            "content_hash": content_hash,
            "confidence": confidence,
            "suspected_model": model,
            "timestamp": timestamp or time.time()
        }
        entry["block_hash"] = hashlib.sha256(str(entry).encode()).hexdigest()
        self.chain.append(entry)
        return entry["block_hash"]

    def verify(self, block_hash):
        return any(block["block_hash"] == block_hash for block in self.chain)