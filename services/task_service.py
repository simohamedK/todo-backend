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

    return get_task_by_id(new_task_id)

def update_task(id,title, completed, description):
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
    if completed :
        updates.append('completed = %s')
        values.append(completed)
    
    if not updates:
        return None
    
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
    values.append(id)

    cursor.execute(query, tuple(values))
    conn.commit()

    cursor.close()
    conn.close()

    return get_task_by_id(id)

def change_status_task(id):
    task = get_task_by_id(id)
    if not task:
        return None
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    new_completed= 0 if task["completed"] == 1 else 1

    cursor.execute("UPDATE tasks SET  completed = %s WHERE id = %s ", (new_completed,id ))
    conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE id= %s", (id,))
    updated_task=cursor.fetchone()

    
    cursor.close()
    conn.close()

    return updated_task

def remove_task(id):

    task=get_task_by_id(id)
    if not task :
        return False

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("DELETE FROM tasks WHERE id=%s",(id,))
    conn.commit()

    cursor.close()
    conn.close()
    return True

