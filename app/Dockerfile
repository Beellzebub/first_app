FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app/

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python"]

CMD ["main.py"]