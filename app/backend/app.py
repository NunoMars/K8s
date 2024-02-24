from flask_cors import CORS
from flask import Flask, request, jsonify
import sqlite3
import os

db_path = "data/todolists.db"


app = Flask(__name__)

# Activer CORS
CORS(app)

# Crete db if not exists
if not os.path.exists(db_path):
    open(db_path, "w").close()


# Fonction pour établir une connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/health")
def health_check():
    # Vérification de la disponibilité de l'application
    # Si tout est prêt, renvoyer un code de statut HTTP 200 OK
    return "OK", 200


# Créer la table Todolists si elle n'existe pas
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Todos (
                        id INTEGER PRIMARY KEY,
                        todo TEXT NOT NULL UNIQUE,
                        status TEXT DEFAULT 'TODO'
                    )"""
    )
    conn.commit()
    conn.close()


create_table()


# Endpoint pour ajouter une nouvelle todo
@app.route("/new", methods=["POST"])
def new_todo():
    try:
        data = request.json
        if "todo" not in data:
            return jsonify({"message": "Missing required parameters"}), 400

        todo = data["todo"]
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Todos (todo) VALUES (?)", (todo,))
            conn.commit()
        return jsonify({"message": "Todo added successfully"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"message": "Todo already exists"}), 409
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500


# Endpoint pour marquer un todo comme terminé
@app.route("/done/<int:todo_id>", methods=["POST"])
def mark_todo_as_done(todo_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Todos SET status='DONE' WHERE id=?", (todo_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Todo marked as done successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500


# Endpoint pour supprimer une todo
@app.route("/delete/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Todos WHERE id=?", (todo_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Todo deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500


# Endpoint pour obtenir toutes les todos
@app.route("/getall", methods=["GET"])
def get_all_todos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Todos")
        todos = cursor.fetchall()
        conn.close()
        todos_list = [
            {"id": todo["id"], "todo": todo["todo"], "status": todo["status"]}
            for todo in todos
        ]
        if len(todos_list) == 0:
            return jsonify({"message": "No todos found in database"}), 404
        return jsonify({"todos": todos_list})
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
