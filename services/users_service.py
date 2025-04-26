from db.mysql import get_connection
from utils.security import PasswordManager
import mysql.connector

def add_user(username, email, password,role):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM roles WHERE name = %s ",(role,))
        role= cursor.fetchone()
        if not role :
            cursor.close()
            conn.close()
            return {"error": "Rôle invalide"}

        role_id=role.get("id")
        password_hached = PasswordManager.hash_password(password)
        cursor.execute("INSERT INTO users (username, email, password, role_id) VALUES (%s,%s,%s,%s)", (username, email, password_hached, role_id))
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE id = LAST_INSERT_ID()")
        user = cursor.fetchone()

        return user
    except mysql.connector.IntegrityError:
        return None
    
    finally: 
        cursor.close()
        conn.close()

def get_all_users():
    conn = get_connection()
    cursor=conn.cursor(dictionary=True)

    query = """
    SELECT users.id, users.email, users.username, roles.name AS role
    FROM users
    JOIN roles ON users.role_id = roles.id
    """

    cursor.execute(query)
    users = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return users

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Utilisation de JOIN pour récupérer l utilisateur avec son rôle
    query = """
    SELECT users.id, users.email, users.username, roles.name AS role
    FROM users
    JOIN roles ON users.role_id = roles.id
    WHERE users.id = %s
    """
    
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return None

    return user


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return None
    
    cursor.execute("SELECT * FROM roles WHERE id = %s",(user.get("role_id"),))
    role = cursor.fetchone()
    if role:
        user["role"]=role.get("name")

    user.pop("role_id", None)

    

    cursor.close()
    conn.close()
    return user
    


def update_user_by_id(user_id, data):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Récupérer le role_id en fonction du nom du rôle
    cursor.execute("SELECT * FROM roles WHERE name = %s", (data['role'],))
    role = cursor.fetchone()

    if not role:
        cursor.close()
        conn.close()
        return {"error": "Rôle invalide"}
    
    role_id = role.get("id")

    # Mise à jour de l'utilisateur avec les nouveaux champs
    query = """
    UPDATE users
    SET username = %s, email = %s, role_id = %s
    WHERE id = %s
    """
    try:
        cursor.execute(query, (data['username'], data['email'], role_id, user_id))
        conn.commit()  
    except Exception as e:
        conn.rollback()  
        print(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
        return None

    cursor.close()
    conn.close()
    return get_user_by_id(user_id)  


def update_user_password_by_id(user_id, data) :
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password :
        return  {"error" : "tous les champs sont obligatoires"}
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        user=cursor.fetchone()

        if not user :
            return {"error": "Utilisateur non trouvé."}
        
        old_password_hashed = user.get("password")

        if not PasswordManager.verify_password(old_password,old_password_hashed):
            cursor.close()
            conn.close()
            return {"error":"Ancien mot de passe incorrect"}
        
        new_password_hashed=PasswordManager.hash_password(new_password)
        
        cursor.execute(
            " UPDATE users SET password = %s WHERE id = %s",
            (new_password_hashed,user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la mise à jour du mot de passe : {e}")
        return {"error": "Erreur serveur, réessayez plus tard."}
    finally:
        cursor.close()
        conn.close()

def delete_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    user = get_user_by_id(user_id)
    if not user :
        cursor.close()
        conn.close()
        return None
    
    query = "DELETE FROM users WHERE id = %s"
    
    try:
        cursor.execute(query, (user_id,))
        conn.commit()  
    except Exception as e:
        conn.rollback()  # Annuler en cas d'erreur
        print(f"Erreur lors de la suppression de l'utilisateur : {e}")
        return None

    cursor.close()
    conn.close()

    return {"message": "Utilisateur supprimé avec succès"}
