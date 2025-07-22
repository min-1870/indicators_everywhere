FROM python:3.12-alpine

RUN apk add --no-cache --virtual .build-deps \
      gcc musl-dev linux-headers \
    && apk add --no-cache \
      libpq \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", \
     "--bind=0.0.0.0:5000", \
     "--workers=2", \
     "--worker-class=gthread", \
     "--threads=4", \
     "--preload", \
     "src.app:app" \
]
