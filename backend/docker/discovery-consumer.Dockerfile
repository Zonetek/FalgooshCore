FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git build-essential


RUN git clone https://github.com/robertdavidgraham/masscan.git && \
    cd masscan && make && cp bin/masscan /usr/local/bin/ && cd .. && rm -rf masscan

COPY requirements/base.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api_applications/discovery/consumer.py ./
COPY api_applications/discovery/masscan_worker.py ./

CMD ["python", "consumer.py"]
