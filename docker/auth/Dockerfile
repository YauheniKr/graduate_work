FROM python:3.9.7-buster
EXPOSE 8000
WORKDIR /src
COPY src/auth/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY src/auth .
ENV PYTHONPATH /