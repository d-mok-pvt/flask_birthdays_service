FROM python:3.11-slim

WORKDIR /tests
COPY . /tests
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests-to-curl
