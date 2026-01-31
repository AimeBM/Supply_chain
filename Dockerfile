FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3

# ---------- ENV ----------
ENV PYTHONPATH="/app"
ENV API_URL="http://127.0.0.1:8000"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 8501

CMD bash -c "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run app/app.py --server.address=0.0.0.0 --server.port=8501"
