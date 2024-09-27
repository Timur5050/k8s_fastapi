FROM python:3.12-slim
LABEL maintainer="stukantimur811@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /files/media

RUN chmod 755 /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
