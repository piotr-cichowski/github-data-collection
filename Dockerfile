FROM python:3.9

WORKDIR /app

ENV POSTGRES_USER=postgres \
	POSTGRES_PASSWORD=test123

RUN mkdir -p /home/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
