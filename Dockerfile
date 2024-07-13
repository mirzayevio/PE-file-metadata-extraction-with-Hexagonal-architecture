FROM python:3.11-slim

RUN apt-get update && \
    apt-get install default-jdk curl zip -y \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /opt/spark/jars

RUN zip -r /opt/spark/jars/src.zip src

RUN curl -k -o /opt/spark/jars/postgresql-42.7.3.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

RUN pex --requirement requirements.txt --output-file /opt/spark/pex/app.pex

RUN chmod +x /opt/spark/pex/app.pex

ENV PYSPARK_PYTHON /opt/spark/pex/app.pex

CMD ["python", "-m", "src.adapters.entrypoints.cli.main"]
