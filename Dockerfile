FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["mitmdump", "-s", "addons.py"]
EXPOSE 5000
