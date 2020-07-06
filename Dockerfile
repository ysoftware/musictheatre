FROM python:3.7-alpine

WORKDIR /usr/src/app

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev py-cffi openssl-dev
  
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./musictheatrebot.py" ]