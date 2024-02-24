
FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py /app
COPY templates /app/templates


EXPOSE 80

# Commande pour exécuter l'application lorsque le container démarre
CMD ["python", "app.py"]