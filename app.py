"""Flask app to execute a todo list website"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from models import db, User, TodoTable


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'candy_crush'
# db.init_app(app)
db = SQLAlchemy(app)


class TodoTable(db.Model):
    # the id column of the db table
    id = db.Column(db.Integer, primary_key=True)

    # the task column of the db table
    task = db.Column(db.String(200), nullable=False)

    # the checkbox column of the db table: for if task is completed
    complete = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    # filter to get all tasks where the checkbox is true for completed i.e finished tasks
    finished_tasks = TodoTable.query.filter_by(complete=True).all()

    # filter to get all tasks where the checkbox is false for completed i.e incomplete tasks
    unfinished_tasks = TodoTable.query.filter_by(complete=False).all()

    # render them on the html first page
    return render_template('index.html', finished_tasks=finished_tasks, unfinished_tasks=unfinished_tasks)


@app.route('/add', methods=['POST'])
def add():
    """
    Adds entered text from the form into the db
    :return:
    """
    # error handling
    try:
        # get the tet intered into the form
        entered_task = request.form.get('task')

        # if entered task is empty
        if not entered_task:
            abort(400, description="Task content is required")

        # add the text to the db
        new_task = TodoTable(task=entered_task)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/completed/<int:task_id>')
def completed(task_id):
    """
    Assigns task with given task id to completed  as true in the db.
    :param task_id: id of  the task
    :return:
    """
    # error handling
    try:
        # get the task from the table using it's id
        task = TodoTable.query.get(task_id)

        # if task not found
        if not task:
            abort(404, description="Task not found")

        # set the value for complete to true
        task.complete = True

        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/delete/<int:task_id>')
def delete(task_id):
    """
    Deletes task with given task id from the db.
    :param task_id: id of  the task
    :return:
    """
    # error handling
    try:
        # get task from table using task id
        task = TodoTable.query.get(task_id)

        # if task not found
        if not task:
            abort(404, description="Task not found")

        # delete the task from table
        db.session.delete(task)

        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    # error handling
    try:
        task = TodoTable.query.get(task_id)

        # if task not found
        if not task:
            abort(404, description="Task not found")

        if request.method == 'POST':
            new_task_content = request.form.get('task')

            # if new content is empty
            if not new_task_content:
                abort(400, description="Task content is required")

            task.task = new_task_content
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('edit.html', task=task)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="An unexpected error occurred. Please try again later."), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

