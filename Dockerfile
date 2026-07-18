FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=1000 --retries=10 -r requirements.txt

COPY app/ ./app/
COPY model/ ./model/
COPY scraper/ ./scraper/
COPY .streamlit/ ./.streamlit/

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
