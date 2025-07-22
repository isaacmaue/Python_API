from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for tasks (will reset when container restarts)
tasks = []
next_id = 1

# Helper function to find task by ID
def find_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)

# GET /tasks - List all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    })

# POST /tasks - Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    new_task = {
        'id': next_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    next_id += 1
    
    return jsonify(new_task), 201

# GET /tasks/<id> - Get a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task)

# PUT /tasks/<id> - Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.now().isoformat()
    
    return jsonify(task)

# DELETE /tasks/<id> - Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    tasks.remove(task)
    return jsonify({'message': 'Task deleted successfully'})

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Task Manager API is running',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Flask Task Manager API...")
    print("Available endpoints:")
    print("  GET    /health")
    print("  GET    /tasks")
    print("  POST   /tasks")
    print("  GET    /tasks/<id>")
    print("  PUT    /tasks/<id>")
    print("  DELETE /tasks/<id>")
    
    app.run(host='0.0.0.0', port=5000, debug=True)