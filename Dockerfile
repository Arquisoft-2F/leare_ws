FROM python:3.12.1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENV HOST="0.0.0.0"
ENV PORT=8001
ENV DEBUG="False"

CMD ["python", "app/server.py"]