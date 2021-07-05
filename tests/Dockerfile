FROM python:3.7

RUN mkdir -p /usr/src/tests

WORKDIR /usr/src/tests

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/usr/src/

ENTRYPOINT ["pytest"]