# smobot/Dockerfile
FROM python:3.13
ADD . /app
WORKDIR /app
# Number of seconds to be eligible for runner role
ENV RUNNER_THRESHOLD=3600
RUN pip install -r requirements.txt
CMD python ./main.py