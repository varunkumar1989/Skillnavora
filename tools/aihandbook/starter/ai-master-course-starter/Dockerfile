# The FastAPI service in a small image. Build: docker build -t pdf-chatbot .
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir anthropic pypdf fastapi uvicorn python-multipart
COPY starter ./starter
COPY api ./api
COPY data ./data
RUN useradd --create-home appuser && mkdir -p logs && chown appuser logs
USER appuser
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
