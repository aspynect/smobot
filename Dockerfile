# smobot/Dockerfile
FROM python:3.13
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Number of seconds to be eligible for runner role
ENV RUNNER_THRESHOLD=3600

COPY src/ /app

CMD [ "python", "main.py" ]
