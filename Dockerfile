FROM ubuntu:22.04

WORKDIR /app

COPY requirements.txt requirements.txt
COPY ./src /app

RUN apt update && apt upgrade
RUN apt install python3 python3-pip -y
RUN pip install -r requirements.txt 

CMD ["python3", "./main.py"]

