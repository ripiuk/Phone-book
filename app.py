from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, IntegerField, validators
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sany:sany12345@localhost/phones'
db = SQLAlchemy(app)


# Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), unique=False)
    last_name = db.Column(db.String(200), unique=False)
    number = db.Column(db.String(50), unique=False)

    def __init__(self, first_name, last_name, number):
        self.first_name = first_name
        self.last_name = last_name
        self.number = number


# home
@app.route('/')
def main():
    result = db.session.query(Book)
    try:
        result[0]
        return render_template("index.html", result=result)
    except IndexError:
        msg = 'No data found'
        return render_template("index.html", msg=msg)


# Add number form
class NumberForm(Form):
    first_name = StringField('First name', [validators.Length(min=1, max=200)])
    last_name = StringField('Last name', [validators.Length(min=1, max=200)])
    number = StringField('Number', [validators.Length(min=1, max=40)])


# Add number
@app.route('/add_number', methods=['GET', 'POST'])
def add_number():
    form = NumberForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        number = form.number.data
        book = Book(first_name, last_name, number)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('add_number.html', form=form)

if __name__ == '__main__':
    import os
    db.create_all()
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, debug=True)
