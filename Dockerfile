FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "flask", "--app", "app/main", "run", "--debug","--host", "0.0.0.0" ]