FROM alpine

RUN apk add --no-cache bash python3 py3-pip
RUN pip3 install --upgrade pip  --break-system-packages
RUN mkdir /app
ADD ./requirements.txt /app
RUN pip3 install -r /app/requirements.txt --break-system-packages
ADD . /app
WORKDIR /app
CMD uvicorn server:app --host 0.0.0.0
