# redteam/simulator.py
from transformers import pipeline

def generate_adversarial_text(prompt="The government is hiding the truth about..."):
    generator = pipeline("text-generation", model="gpt2")
    return generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]