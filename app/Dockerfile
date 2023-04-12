FROM python:3.11-slim

# Set timezone to UTC+4
ENV TZ=Asia/Dubai

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y sqlite3 tzdata

# Create and populate database
RUN mkdir /data && \
    chown -R 1001:1001 /data && \
    sqlite3 /data/birthdays.db && \
    sqlite3 /data/birthdays.db < create_table.sql && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime
