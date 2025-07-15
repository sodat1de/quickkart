FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel -r requirements.txt --no-cache-dir --no-deps -w /wheels

FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . .
EXPOSE 8010
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8010"]