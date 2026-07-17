from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default = datetime.now())

    def __repr__(self) -> str:
        return f'Task {self.id}'


@app.route('/',methods=['POST', 'GET'])
def index():
    # adding a task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = Mytask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'ERROR: {e}')
            return f'ERROR:{e}'

    # see all the current task
    else:
        tasks = Mytask.query.order_by(Mytask.created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = Mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'ERROR: {e}'
    
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id:int):
    task = Mytask.query.get_or_404(id)
    if request.method=="POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template('edit.html', task=task)



if __name__ in '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)