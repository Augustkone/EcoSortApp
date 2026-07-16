FROM python:3.12-slim

WORKDIR /app

# Copie et installation des dependances des 3 sous-projets
COPY app/requirements.txt ./app-requirements.txt
COPY model/requirements.txt ./model-requirements.txt
COPY scraper/requirements.txt ./scraper-requirements.txt

RUN pip install --no-cache-dir -r app-requirements.txt \
    && pip install --no-cache-dir -r model-requirements.txt \
    && pip install --no-cache-dir -r scraper-requirements.txt

# Copie du code des 3 dossiers
COPY app/ ./app/
COPY model/ ./model/
COPY scraper/ ./scraper/

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]