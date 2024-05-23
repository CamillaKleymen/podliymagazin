FROM python:3.12
COPY . /shopbot
WORKDIR /shopbot
RUN pip install -r requirements.txt
CMD ["python", "main.py"]


