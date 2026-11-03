import pytest

from app import create_app
from database import db
from models import Task


@pytest.fixture()
def app(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'tasks.db'}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_index_page_renders_welcome_screen(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Task Tracker" in response.data
    assert b"Welcome" in response.data
    assert b"Open tasks" in response.data


def test_list_tasks_page_displays_tasks(client):
    with client.application.app_context():
        task = Task(title="Write tests", description="Cover the task tracker flow", completed=False)
        db.session.add(task)
        db.session.commit()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert b"Your tasks" in response.data
    assert b"Write tests" in response.data
    assert b"Cover the task tracker flow" in response.data


def test_create_task_form_prevents_duplicate_submissions(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert b"data-prevent-duplicate-submit" in response.data
    assert b"data-submitting-label=\"Adding...\"" in response.data
    assert b"/static/js/prevent_duplicate_submit.js" in response.data


def test_create_task_adds_task_and_redirects(client):
    response = client.post(
        "/tasks",
        data={"title": "Ship feature", "description": "Implement a release checklist"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert Task.query.filter_by(title="Ship feature").count() == 1
    assert b"Ship feature" in response.data


def test_create_task_requires_title_and_description(client):
    response = client.post(
        "/tasks",
        data={"title": "Missing description"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert Task.query.filter_by(title="Missing description").count() == 0

    response = client.post(
        "/tasks",
        data={"description": "Missing title only"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert Task.query.filter_by(description="Missing title only").count() == 0


def test_mark_task_as_done_updates_completion_status(client):
    with client.application.app_context():
        task = Task(title="Review PR", description="Check the final changes")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post(f"/tasks/{task_id}/done", follow_redirects=True)

    assert response.status_code == 200
    with client.application.app_context():
        updated_task = db.session.get(Task, task_id)
        assert updated_task.completed is True
        assert b"Done" in response.data
