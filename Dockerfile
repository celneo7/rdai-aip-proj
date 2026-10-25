FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/ 
COPY data/examples/ data/examples/

RUN python -m src.utils.seed_examples

RUN useradd --create-home appuser
ENV HOME=/home/appuser
USER appuser

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]