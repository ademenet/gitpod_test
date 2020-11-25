FROM python:3.9.0
# FROM python:3.8.0

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /notebooks

EXPOSE 8888

CMD jupyter lab --ip=* --port=8888 --allow-root --no-browser
