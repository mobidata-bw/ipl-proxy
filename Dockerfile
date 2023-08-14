FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["mitmdump", "-s", "addons.py"]
EXPOSE 8080
