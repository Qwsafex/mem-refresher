import datetime

from flask import Flask
from flask import render_template
from flask import request
from random import randrange

from db import session, Todo

app = Flask(__name__)


def get_index():
    todos = session.query(Todo).all()
    todos = sorted(todos, key=lambda x: x.date_)
    def processed_date(todo):
        left = todo.date_ - datetime.datetime.now()
        todo.days_left = left.days
        todo.hours_left = left.seconds // 3600
        todo.minutes_left = (left.seconds % 3600) // 60
        todo.date = todo.date_.strftime("%d %B %H:%M")
        return todo
    todos = list(map(lambda x: processed_date(x), todos))
    return render_template('index.html', todos=todos)

@app.route('/', methods=['GET'])
def index():
    print("index")
    return get_index()

@app.route('/', methods=['POST'])
def add_todo():
    if request.form["action"] == "Add":
        print("adding")
        date = datetime.datetime.strptime(request.form["date"], "%d/%m %H:%M")
        date = date.replace(year=datetime.datetime.now().year)
        todo = Todo(text=request.form["text"],
                    date_=date)
        session.add(todo)
        session.commit()
    if request.form["action"] == "Delete":
        print("deleting")
        todo = session.query(Todo).filter_by(id=request.form["todo_id"]).first()
        if todo: 
            session.delete(todo)
            session.commit()

    return get_index()

if __name__ == '__main__':
    app.run(debug=True)
