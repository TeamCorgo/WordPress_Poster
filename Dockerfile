FROM python
ENV PYTHONUNBUFFERED=1

WORKDIR /var/www/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
