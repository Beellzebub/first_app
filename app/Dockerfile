FROM python:3.7

RUN mkdir -p /usr/src/app

COPY __init__.py /usr/src/app/
COPY main.py /usr/src/app/
COPY routes.py /usr/src/app/
COPY models.py /usr/src/app/
COPY static /usr/src/app/
COPY templates /usr/src/app/
COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

EXPOSE 5000
EXPOSE 5432

ENTRYPOINT ["python"]

CMD ["/usr/src/app/main.py"]