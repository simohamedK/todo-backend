from db.mysql import get_connection

def get_all_tasks(user_id) :
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("Select * from tasks WHERE user_id = %s ORDER BY id DESC",(user_id,))
    tasks= cursor.fetchall()

    cursor.close()
    conn.close()

    return tasks

def get_task_by_id(id,user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks WHERE id = %s and user_id = %s", (id,user_id))
    task= cursor.fetchone()    

    cursor.close()
    conn.close()

    return task

def add_task(title,completed,description,user_id) :
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO tasks (title,completed,description,user_id) VALUES (%s,%s,%s,%s)",
          (title,completed,description,user_id)
    )

    conn.commit()

    new_task_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return get_task_by_id(new_task_id,user_id)

def update_task(id,title, completed, description,user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    updates = []
    values = []

    if title :
        updates.append('title = %s')
        values.append(title)
    if description :
        updates.append('description = %s')
        values.append(description)
    if completed is not None:
        updates.append('completed = %s')
        values.append(completed)
    
    if not updates:
        return None
    
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s AND user_id = %s"
    values.append(id)
    values.append(user_id)

    cursor.execute(query, tuple(values))
    conn.commit()

    cursor.close()
    conn.close()

    return get_task_by_id(id, user_id)

def change_status_task(id,user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        task = get_task_by_id(id,user_id)
        if not task:
            return None
        
        new_completed= 0 if task["completed"] == 1 else 1

        cursor.execute(
            "UPDATE tasks SET  completed = %s WHERE id = %s AND user_id = %s", 
            (new_completed,id,user_id )
        )
        conn.commit()

        return get_task_by_id(id,user_id)
    finally:
        cursor.close()
        conn.close()

def remove_task(id,user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        task=get_task_by_id(id,user_id)
        if not task :
            return False

        cursor.execute("DELETE FROM tasks WHERE id=%s AND user_id = %s",(id,user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression de la tâche : {e}")
        conn.rollback()  # Annuler la transaction en cas d'erreur
        return False
    finally :
        cursor.close()
        conn.close()
    
