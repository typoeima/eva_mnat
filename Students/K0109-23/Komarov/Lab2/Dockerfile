# ---------- builder ----------
FROM python:3.12-slim AS builder

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ---------- runtime ----------
FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache libstdc++

COPY --from=builder /opt/venv /opt/venv
COPY app.py .

ENV PATH="/opt/venv/bin:$PATH"
ENV APP_VERSION=2.0

RUN adduser -D appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]