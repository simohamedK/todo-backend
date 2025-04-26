from flask import Blueprint, jsonify , request
from services.task_service import *
from utils.auth import *


tasks_bp= Blueprint('tasks', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
@JWTManager.token_required
def fetch_tasks(user_id):
    tasks=get_all_tasks(user_id)
    return jsonify(tasks)

@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
@JWTManager.token_required
def fetch_task(id,user_id):
    task= get_task_by_id(id,user_id)

    if not task :
        return jsonify({"error" : "Task not found"}), 404
    
    return jsonify(task)

@tasks_bp.route('/tasks', methods=['POST'])
@JWTManager.token_required
def create_task(user_id):
    data = request.get_json()
    
    title= data.get('title')
    completed= bool(data.get('completed', False))
    description = data.get("description")
    if not title:
        return jsonify({"error": "Title is required"}), 400 
    
    new_task=add_task(title,completed,description,user_id)

    return jsonify(new_task), 201

@tasks_bp.route("/tasks/<int:id>", methods=['PUT'])
@JWTManager.token_required
def modify_task(id,user_id):
    data = request.get_json()

    title= data.get('title')
    completed= data.get('completed')
    description = data.get("description")

    if not title and completed is None and not description :
        return jsonify({'error' : "At least one field (title , completed or description) must be provided"}), 400
    
    updated_task = update_task(id, title, completed,description,user_id)

    if not updated_task:
        return jsonify({"error" : "Task not found"}), 404
    
    return jsonify(updated_task)

@tasks_bp.route('/tasks/<int:id>',methods=['PATCH'])
@JWTManager.token_required
def modify_status_task(id,user_id):    
    updated_task= change_status_task(id,user_id)
    if not updated_task:
        return jsonify({"error":"Task not found"}), 404
    return jsonify(updated_task), 200

@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
@JWTManager.token_required
def delete_task(id,user_id):
    deleted= remove_task(id,user_id)

    if not deleted :
        return jsonify({"error" : "Task not found"}), 404
    
    return jsonify({"message" : "Task deleted succefully"}), 200

