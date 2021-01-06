FROM python:3.8.2
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
