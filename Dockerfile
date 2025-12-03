FROM python:3.11-slim

WORKDIR /app

# install cron (and update packages)
RUN apt-get update && apt-get install -y cron

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy all source files
COPY app/ app/
COPY scripts/ scripts/

COPY student_private.pem .
COPY student_public.pem .
#COPY instructor_public.pem .

# 1. FIX: Correctly copies the cron configuration file with the .txt extension
COPY cron/2fa-cron.txt /etc/cron.d/2fa-cron
# 2. FIX: Only sets permissions. The cron daemon reads this file automatically.
RUN chmod 0644 /etc/cron.d/2fa-cron

RUN mkdir -p /data /cron

EXPOSE 8080

# FINAL FIX: Runs cron in the background and the main app (uvicorn) in the foreground.
# This avoids the line ending issue and correctly sets the process (PID 1) for signal handling.
ENTRYPOINT ["/usr/bin/env", "bash", "-c"]
CMD ["cron && exec uvicorn app.main:app --host 0.0.0.0 --port 8080"]