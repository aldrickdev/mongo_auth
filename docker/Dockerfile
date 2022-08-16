FROM python:3.10.4

WORKDIR /project
COPY ../requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY /app /project/app

WORKDIR /project/app
CMD ["python", "main.py"]
