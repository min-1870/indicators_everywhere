FROM python:3.12.10-slim

# Force the python to output everything
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

# Prevent pip caching to save some space
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# DRF port
EXPOSE 5000

CMD ["sh", "-c", "\
    cd src/app && \
    flask run --host=0.0.0.0 --port=5000"]