from flask import Blueprint, redirect, render_template, request, url_for

from database import db
from models import Task


routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


@routes.route('/tasks', methods=['POST'])
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')
    if not title or not description:
        return redirect(url_for('routes.list_tasks'))
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('routes.list_tasks'))


@routes.route('/tasks/<int:task_id>/done', methods=['POST'])
def mark_task_as_done(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
    return redirect(url_for('routes.list_tasks'))