from flask import Blueprint, jsonify , request
from services.users_service import *
from utils.auth import JWTManager



users_bp=Blueprint('users',__name__)

@users_bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()

    username=data.get("username")
    email=data.get("email")
    password=data.get("password")
    role=data.get("role")

    if not username or not email or not password or not role :
        return  jsonify({"error": "All fields are required"}), 400 

    user=add_user(username, email, password, role)
    if not user:
        return jsonify({"error": "Email already exists"}), 400
    
    user.pop("password",None)
    return jsonify(user) , 201 

@users_bp.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    email= data.get("email")
    password=data.get("password")

    if not email or not password :
        return  jsonify({"error": "All fields are required"}), 400 
    
    user = get_user_by_email(email)

    if not user or not PasswordManager.verify_password(password,user.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401
    
    user.pop("password")
    token = JWTManager.generate_token(user)
    return jsonify({"access_token": token}), 200


@users_bp.route("/users/", methods=["GET"])
@JWTManager.admin_required
def fetch_users(user_id):
    users=get_all_users()
    if not users:
        return jsonify({"error": "aucun utulisateur trouver"})
    return jsonify(users)

@users_bp.route("/users/<int:id>", methods=["GET"])
@JWTManager.admin_required
def recuperer_user(id, user_id):
    user= get_user_by_id(id)

    if not user :
        return jsonify({"error" : "User not found"}), 400
    
    return jsonify(user)
    
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
@JWTManager.token_required
def update_user(user_id):
    data = request.get_json()
    updated_user = update_user_by_id(user_id, data)
    if updated_user:
        return jsonify(updated_user), 200
    return jsonify({"error": "Utilisateur non trouvé ou erreur de mise à jour"}), 400

# Supprimer un utilisateur
@users_bp.route("/users/<int:id>", methods=["DELETE"])
@JWTManager.admin_required  # S'assurer que l'utilisateur est admin pour supprimer un autre utilisateur
def delete_user(id,user_id):
    result = delete_user_by_id(id)
    if not result:
        return jsonify({"error": "Utilisateur non trouvé ou erreur de suppression"}), 400
    return jsonify(result), 200
    


#pour faire des tests
@users_bp.route("/users/mee", methods=["GET"])
@JWTManager.token_required
def get_current_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)