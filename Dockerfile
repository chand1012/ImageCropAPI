FROM ubuntu:20.04

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update
RUN apt-get install build-essential python3-dev python3-pip -y
RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install uvicorn
RUN apt-get purge build-essential -y && apt-get autoremove -y
COPY ./ .
CMD ["uvicorn", "main:app", "--port", "5000"]
EXPOSE 5000