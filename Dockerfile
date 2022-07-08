FROM ubuntu

COPY src /opt/app/src

COPY requirements.txt /opt/app/
COPY keys.txt /opt/app/

RUN apt update

RUN apt upgrade -y

RUN apt install python3 -y

RUN apt install python3-pip -y

RUN pip install -r opt/app/requirements.txt

RUN mkdir /opt/app/data

WORKDIR /opt/app

CMD [ "python3", "-m" , "src.data_pull"]