from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
)
import os
import requests


app = Flask(__name__)

# Récupérer l'adresse du backend depuis la variable d'environnement BACKEND_URL
backend_url = os.environ.get("BACKEND_URL", "http://localhost:5000")
environment = os.environ.get("ENV", "Development")


@app.route("/health")
def health_check():
    # Vérification de la disponibilité de l'application
    # Si tout est prêt, renvoyer un code de statut HTTP 200 OK
    return "OK", 200


# Endpoint pour servir le fichier index.html
@app.route("/", methods=["GET", "POST"])
def index():
    try:
        response = requests.get(f"{backend_url}/getall")
        response = response.json()
        todos = response["todos"] if "todos" in response else []
        print(todos)
        message = response["message"]
    except:
        message = request.args.get("message")
        response = {
            "message": message,
            "todos": [],
        }

    context = {
        "message": message,
        "todos": todos,
        "environment": environment,
    }
    return render_template("index.html", context=context)


# Endpoint pour ajouter une nouvelle todolist via l'API back-end
@app.route("/new", methods=["GET", "POST"])
def new_todolist():
    if request.method == "POST":
        # Récupérer la valeur du champ de formulaire 'todolist'
        todo = request.form.get("todo")
        print(todo)
        # Envoyer la valeur 'todolist' au backend en tant que JSON dans la requête POST
        response = requests.post(f"{backend_url}/new", json={"todo": todo})

        # Récupérer la réponse JSON du backend
        context = response.json()
        message = context["message"]
        # Retourner la réponse JSON au client
        return redirect(url_for("index", message=message))


# Endpoint pour marquer un todo comme terminé via l'API back-end
@app.route("/done", methods=["GET", "POST"])
def mark_todo_as_done():
    todo = request.form.get("todo")
    response = requests.post(f"{backend_url}/done/{todo}")
    context = response.json()
    message = context["message"]
    return redirect(url_for("index", message=message))


# Endpoint pour supprimer un todo via l'API back-end
@app.route("/delete", methods=["GET", "POST"])
def delete_todo():
    todo = request.form.get("todo")
    response = requests.delete(f"{backend_url}/delete/{todo}")
    context = response.json()
    message = context["message"]
    return redirect(url_for("index", message=message))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
