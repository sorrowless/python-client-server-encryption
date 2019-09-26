FROM python:3.7-alpine

WORKDIR /sender
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY sender.py sender.py
CMD ["python3", "sender.py"]
