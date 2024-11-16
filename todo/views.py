from pymongo import MongoClient
from django.conf import settings
from django.shortcuts import render, redirect
from datetime import datetime
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB_NAME]
col = db['todo']

def todo_list(request):
    filter_status = request.GET.get('filter_status', '')

    # Fetch todos from MongoDB
    if filter_status:
        filtered_todos = list(col.find({'status': filter_status}))
    else:
        filtered_todos = list(col.find())

    return render(request, 'todo_list.html', {
        'todos': filtered_todos,
        'filter_status': filter_status,
    })

def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date') + ' ' + request.POST.get('due_time')
        status = request.POST.get('status', 'Pending')  # Default status is 'Pending'
        if title and due_date:
            # Insert into MongoDB
            col.insert_one({
                'title': title,
                'due_date': datetime.strptime(due_date, '%Y-%m-%d %H:%M'),
                'status': status,
                'completed': False
            })
        return redirect('todo_list')
    return render(request, 'todo_form.html')

def todo_update(request, todo_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date') + ' ' + request.POST.get('due_time')
        status = request.POST.get('status')
        if title and due_date:
            # Update the todo in MongoDB
            col.update_one(
                {'_id': ObjectId(todo_id)},
                {'$set': {
                    'title': title,
                    'due_date': datetime.strptime(due_date, '%Y-%m-%d %H:%M'),
                    'status': status
                }}
            )
        return redirect('todo_list')

    # Fetch the todo to edit
    todo = col.find_one({'_id': ObjectId(todo_id)})
    return render(request, 'todo_form.html', {'todo': todo})

def todo_delete(request, todo_id):
    if request.method == 'POST':
        col.delete_one({'_id': ObjectId(todo_id)})  # Delete from MongoDB
        return redirect('todo_list')

    todo = col.find_one({'_id': ObjectId(todo_id)})
    return render(request, 'todo_confirm_delete.html', {'todo': todo})
