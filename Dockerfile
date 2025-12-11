FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUMBUFFERED=1

WORKDIR /app

COPY all_the_buzz/ /app/all_the_buzz/

RUN pip install --no-cache-dir -r all_the_buzz/requirements.txt

EXPOSE 8080
EXPOSE 42068

CMD ["python","-m", "all_the_buzz.server"]