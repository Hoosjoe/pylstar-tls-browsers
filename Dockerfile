FROM python:3.10-buster

WORKDIR /root

COPY requirements.txt /root
RUN pip install -r requirements.txt

COPY src tls-inferer
RUN mv src/fingerprinting/* tls-inferer
