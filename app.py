# frontend/app.py
import streamlit as st
import requests
import json

st.set_page_config(page_title="AEGIS-X", layout="wide")
st.title("🛡️ AEGIS-X: AI Threat Intelligence Dashboard")

text = st.text_area("Paste suspicious text or social post", height=150)
lang = st.selectbox("Language", ["en", "hi", "ta", "bn"])

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        res = requests.post("http://localhost:8000/analyze", json={"text": text, "lang": lang}).json()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔍 Detection Result")
        conf = res["detection"]["confidence"]
        st.metric("AI-Generated?", "YES" if conf > 0.5 else "NO", f"{conf*100:.1f}%")
        st.json(res["detection"])
        
        st.subheader("🕵️ Attribution")
        st.write(f"**Likely Model**: {res['attribution']['model']}")
        st.write(f"**Watermark**: {'✅ Detected' if res['attribution']['watermark_detected'] else '❌ Absent'}")
    
    with col2:
        st.subheader("⛓️ Blockchain Log")
        st.code(f"Content Hash: {res['blockchain']['content_hash'][:16]}...\nBlock: {res['blockchain']['block_hash'][:16]}...")
        
        st.subheader("🕸️ Propagation Graph")
        st.info("Interactive graph would render here (D3.js in React version)")
        st.json({"nodes": len(res["propagation_graph"]["nodes"]), "edges": len(res["propagation_graph"]["edges"])})