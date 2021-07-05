FROM python:3.7

RUN mkdir -p /usr/src/

WORKDIR /usr/src/

COPY app ./app
COPY tests ./tests
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV PYTHONPATH=/usr/src/

WORKDIR /usr/src/tests/

ENTRYPOINT ["pytest"]
