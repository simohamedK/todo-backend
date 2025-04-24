from flask import Flask
from flask_cors import CORS
from routes.tasks_routes import tasks_bp
from routes.users_routes import users_bp
from config import SECRET_KEY


app= Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = SECRET_KEY

# Enregistrement des routes dans l'app Flask
app.register_blueprint(tasks_bp)
app.register_blueprint(users_bp)




if __name__ == '__main__':
    app.run(debug=True)