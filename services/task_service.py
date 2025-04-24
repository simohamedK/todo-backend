from db.mysql import get_connection

def get_all_tasks() :
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("Select * from tasks")
    tasks= cursor.fetchall()

    cursor.close()
    conn.close()

    return tasks

def get_task_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task= cursor.fetchone()    

    cursor.close()
    conn.close()

    return task

def add_task(title,completed) :
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("INSERT INTO tasks (title,completed) VALUES (%s,%s)", (title,completed))
    
    # Commit pour enregistrer la transaction
    conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE id= LAST_INSERT_ID()")
    new_task=cursor.fetchone()

    cursor.close()
    conn.close()

    return new_task

def update_task(id,title, completed):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    updates = []
    values = []

    if title :
        updates.append('title = %s')
        values.append(title)
    if completed :
        updates.append('completed = %s')
        values.append(completed)
    
    if not updates:
        return None
    
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
    values.append(id)

    cursor.execute(query, tuple(values))
    conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE id= %s", (id,))
    updated_task=cursor.fetchone()

    cursor.close()
    conn.close()

    return updated_task

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

