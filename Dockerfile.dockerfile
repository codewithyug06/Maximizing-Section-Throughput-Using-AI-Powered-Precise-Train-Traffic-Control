# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD ["bash", "-c", "uvicorn backend.api:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port=8501"]