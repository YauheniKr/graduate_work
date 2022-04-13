FROM python:3.9

WORKDIR /opt/payment_gateway

COPY src/payment_gateway/requirements.txt /var/opt/payment_gateway/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /var/opt/payment_gateway/requirements.txt --no-cache-dir

COPY src/payment_gateway /opt/payment_gateway

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
