FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py .

CMD [ "python", "-m", "flask" , "--app", "main", "run", "-p", "8080" ]

