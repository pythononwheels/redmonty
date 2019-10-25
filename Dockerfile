FROM python:3.7

EXPOSE 8080

RUN mkdir -p /usr/local/redmonty
WORKDIR /usr/local/redmonty

COPY requirements.txt /usr/local/redmonty/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python3 /usr/local/redmonty/server.py
