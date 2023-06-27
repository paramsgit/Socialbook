FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/database
RUN chown -R root:root /app/database
RUN python manage.py makemigrations
RUN python manage.py migrate



EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
